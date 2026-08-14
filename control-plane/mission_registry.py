"""Durable mission index and safe document projection for the control plane."""

from __future__ import annotations

import html
import hashlib
import json
import re
import secrets
import threading
from pathlib import Path
from typing import Callable
from urllib.parse import urlparse


MAX_ASK = 12_000
MAX_DOCUMENT = 512 * 1024
SLUG_RE = re.compile(r"[^a-z0-9]+")
STATUSES = {
    "proposed", "framing", "awaiting_approval", "building", "landing",
    "complete", "blocked", "rejected",
}
TRANSITIONS = {
    "proposed": {"framing", "rejected"},
    "framing": {"awaiting_approval", "blocked", "rejected"},
    "awaiting_approval": {"building", "blocked", "rejected"},
    "building": {"landing", "blocked", "rejected"},
    "landing": {"complete", "blocked"},
    "blocked": {"framing", "rejected"},
    "complete": set(),
    "rejected": set(),
}
DOCUMENT_NAMES = {"MISSION.md", "TASKS.md", "investigation.md", "blueprint.md", "plan.md"}
RECORD_TYPES = {"mission", "subtask"}


class MissionRegistryError(ValueError):
    """A caller supplied invalid registry data or requested an invalid transition."""


def _slug(value: str) -> str:
    result = SLUG_RE.sub("-", value.lower()).strip("-")
    return (result or "mission")[:80]


def _now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _safe_url(value: str) -> bool:
    parsed = urlparse(value)
    if parsed.scheme == "https":
        return True
    # Empty-scheme links are relative paths only. Reject protocol-relative URLs,
    # which otherwise look relative but can send the reader to another origin.
    return parsed.scheme == "" and not parsed.netloc and not value.startswith("//")


def render_markdown(source: str) -> str:
    """Render a deliberately bounded Markdown subset with escaped output."""
    if len(source.encode()) > MAX_DOCUMENT:
        raise MissionRegistryError("document exceeds the 512 KiB limit")
    out: list[str] = []
    in_code = False
    in_list = False
    for raw in source.splitlines():
        line = raw.rstrip()
        if line.startswith("```"):
            if in_code:
                out.append("</code></pre>")
            else:
                out.append("<pre><code>")
            in_code = not in_code
            continue
        escaped = html.escape(line, quote=True)
        if in_code:
            out.append(escaped)
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", line)
        item = re.match(r"^[-*]\s+(.+)$", line)
        if heading:
            if in_list:
                out.append("</ul>")
                in_list = False
            level = len(heading.group(1))
            out.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
        elif item:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline(item.group(1))}</li>")
        elif not line:
            if in_list:
                out.append("</ul>")
                in_list = False
        else:
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<p>{_inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    if in_code:
        out.append("</code></pre>")
    return "\n".join(out)


def _inline(value: str) -> str:
    text = html.escape(value, quote=True)
    text = re.sub(r"`([^`]{1,200})`", r"<code>\1</code>", text)

    def link(match: re.Match[str]) -> str:
        label, href = match.group(1), match.group(2)
        if not _safe_url(href):
            return label
        return f'<a href="{html.escape(href, quote=True)}" rel="noreferrer">{label}</a>'

    return re.sub(r"\[([^\]]{1,200})\]\(([^)\s]{1,1000})\)", link, text)


class MissionRegistry:
    """JSON-backed registry with atomic writes and a confined document root."""

    def __init__(self, root: Path, *, create_job: Callable[..., dict] | None = None,
                 project_roots: list[Path | str] | None = None):
        self.root = root.resolve()
        self.directory = self.root / "missions"
        self.index_path = self.directory / "registry.json"
        self.create_job = create_job
        self.project_roots = [Path(p).expanduser().resolve() for p in (project_roots or [])]
        self._lock = threading.RLock()
        self.directory.mkdir(parents=True, exist_ok=True)

    def discover(self) -> list[dict]:
        """Import mission bundles from explicitly configured local project roots.

        Discovery only checks the two documented bundle layouts and copies bounded,
        allowlisted documents into the control-plane registry. It never walks an
        arbitrary path supplied by a request and never starts a mission.
        """
        imported: list[dict] = []
        for project_root in self.project_roots:
            candidates = list((project_root / "nightshift" / "missions").glob("*/.aidlc/mission.json"))
            candidates += list((project_root / "nightshift").glob("*/mission.json"))
            for mission_file in candidates:
                try:
                    mission = json.loads(mission_file.read_text())
                    if not isinstance(mission, dict) or not mission.get("ask"):
                        continue
                    imported.append(self._import_bundle(project_root, mission_file, mission))
                except (OSError, json.JSONDecodeError, MissionRegistryError):
                    continue
        return imported

    def _import_bundle(self, project_root: Path, mission_file: Path, mission: dict) -> dict:
        mission_id = str(mission.get("mission_id") or mission.get("id") or "")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{5,127}", mission_id):
            stable_key = f"{project_root.resolve()}\0{mission_file.parent.resolve()}".encode()
            mission_id = f"local-{hashlib.sha256(stable_key).hexdigest()[:20]}"
        with self._lock:
            data = self._read()
            source_bundle = str(mission_file.parent)
            stale_ids = [old_id for old_id, old in data["missions"].items()
                         if old_id != mission_id and old.get("source_bundle") == source_bundle
                         and not old.get("job_id")]
            for stale_id in stale_ids:
                del data["missions"][stale_id]
            existing = data["missions"].get(mission_id)
            if existing is not None:
                parent_id = mission.get("parent_id")
                record_type = mission.get("record_type") or mission.get("type")
                if record_type == "task":
                    record_type = "subtask"
                if record_type not in RECORD_TYPES:
                    record_type = "subtask" if parent_id else "mission"
                existing.update({
                    "parent_id": parent_id,
                    "root_id": mission.get("root_id") or (parent_id or mission_id),
                    "record_type": record_type,
                    "source_bundle": source_bundle,
                    "updated_at": _now(),
                })
                self._write(data)
                return self._record(existing)
            parent_id = mission.get("parent_id")
            record_type = mission.get("record_type") or mission.get("type")
            if record_type == "task":
                record_type = "subtask"
            if record_type not in RECORD_TYPES:
                record_type = "subtask" if parent_id else "mission"
            record = {
                "mission_id": mission_id, "slug": _slug(str(mission.get("ask"))),
                "ask": str(mission["ask"])[:MAX_ASK], "target": project_root.name,
                "status": "framing", "next_action": "inspect discovered mission",
                "done_state": mission.get("done_state", "pr-ready"), "parent_id": parent_id,
                "root_id": mission.get("root_id") or (parent_id or mission_id),
                "relationship": "sub-mission" if parent_id else "root",
                "record_type": record_type, "job_id": None,
                "pr_url": None, "source_project": str(project_root),
                "source_bundle": source_bundle, "created_at": _now(), "updated_at": _now(),
            }
            data["missions"][mission_id] = record
            self._write(data)
            source_dir = mission_file.parent
            if source_dir.name == ".aidlc":
                source_dir = source_dir.parent
            documents = {}
            for name in DOCUMENT_NAMES:
                path = source_dir / name
                if path.is_file() and path.stat().st_size <= MAX_DOCUMENT:
                    documents[name] = path.read_text()
            if documents:
                self._write_documents(mission_id, documents)
            return self._record(record)

    def _read(self) -> dict:
        if not self.index_path.exists():
            return {"version": 1, "missions": {}}
        try:
            data = json.loads(self.index_path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            raise MissionRegistryError(f"registry is unreadable: {exc}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("missions"), dict):
            raise MissionRegistryError("registry has an invalid shape")
        return data

    def _write(self, data: dict) -> None:
        temporary = self.index_path.with_suffix(".tmp")
        temporary.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
        temporary.replace(self.index_path)

    def _record(self, record: dict) -> dict:
        result = dict(record)
        children = [r for r in self._read()["missions"].values()
                    if r.get("parent_id") == record["mission_id"]]
        result["children"] = [self._summary(child) for child in sorted(children, key=lambda r: r["mission_id"])]
        result["task_count"] = sum(1 for child in children if self._record_type(child) == "subtask")
        result["child_count"] = len(children)
        result["record_type"] = self._record_type(record)
        return result

    @staticmethod
    def _record_type(record: dict) -> str:
        value = record.get("record_type")
        if value == "task":
            return "subtask"
        return value if value in RECORD_TYPES else ("subtask" if record.get("parent_id") else "mission")

    @staticmethod
    def _summary(record: dict) -> dict:
        return {key: record.get(key) for key in
                ("mission_id", "slug", "status", "next_action", "relationship", "record_type")}

    def list(self, *, status: str | None = None, target: str | None = None,
             parent_id: str | None = None) -> list[dict]:
        with self._lock:
            records = list(self._read()["missions"].values())
            if status:
                records = [r for r in records if r.get("status") == status]
            if target:
                records = [r for r in records if r.get("target") == target]
            if parent_id:
                records = [r for r in records if r.get("parent_id") == parent_id]
            return [self._record(r) for r in sorted(records, key=lambda r: (r.get("updated_at", ""), r["mission_id"]), reverse=True)]

    def get(self, mission_id: str) -> dict:
        with self._lock:
            record = self._read()["missions"].get(mission_id)
            if record is None:
                raise MissionRegistryError(f"no such mission: {mission_id}")
            return self._record(record)

    def create(self, *, ask: str, target: str = "", parent_id: str | None = None,
               relationship: str = "follow-up", done_state: str = "pr-ready",
               next_action: str = "frame", documents: dict[str, str] | None = None,
               record_type: str | None = None) -> dict:
        ask = ask.strip()
        if not ask or len(ask) > MAX_ASK:
            raise MissionRegistryError("ask is required and must be at most 12,000 characters")
        if relationship not in {"follow-up", "sub-mission", "root"}:
            raise MissionRegistryError("relationship must be follow-up, sub-mission, or root")
        if record_type is None:
            record_type = "subtask" if parent_id else "mission"
        if record_type == "task":
            record_type = "subtask"
        if record_type not in RECORD_TYPES:
            raise MissionRegistryError("record_type must be mission or subtask")
        if record_type == "subtask" and not parent_id:
            raise MissionRegistryError("subtask records require a parent mission")
        if record_type == "mission" and parent_id:
            raise MissionRegistryError("child records must use record_type subtask")
        with self._lock:
            data = self._read()
            if parent_id:
                parent = data["missions"].get(parent_id)
                if parent is None:
                    raise MissionRegistryError(f"parent mission does not exist: {parent_id}")
                root_id = parent.get("root_id") or parent_id
            else:
                root_id = None
            mission_id = secrets.token_hex(12)
            record = {
                "mission_id": mission_id, "slug": _slug(ask), "ask": ask,
                "target": target.strip(), "status": "proposed" if parent_id else "framing",
                "next_action": next_action.strip()[:500], "done_state": done_state,
                "parent_id": parent_id, "root_id": root_id or mission_id,
                "relationship": relationship if parent_id else "root",
                "record_type": record_type,
                "job_id": None, "pr_url": None, "created_at": _now(), "updated_at": _now(),
            }
            data["missions"][mission_id] = record
            self._write(data)
            if documents:
                self._write_documents(mission_id, documents)
            return self._record(record)

    def _write_documents(self, mission_id: str, documents: dict[str, str]) -> None:
        directory = self.directory / mission_id
        directory.mkdir(exist_ok=True)
        for name, content in documents.items():
            if name not in DOCUMENT_NAMES or not isinstance(content, str):
                raise MissionRegistryError(f"unsupported mission document: {name}")
            if len(content.encode()) > MAX_DOCUMENT:
                raise MissionRegistryError(f"document exceeds the 512 KiB limit: {name}")
            (directory / name).write_text(content)

    def document(self, mission_id: str, name: str, *, rendered: bool = False) -> str:
        if name not in DOCUMENT_NAMES or Path(name).name != name:
            raise MissionRegistryError("document is not allowlisted")
        self.get(mission_id)
        path = self.directory / mission_id / name
        try:
            text = path.read_text()
        except OSError as exc:
            raise MissionRegistryError(f"document is not present: {name}") from exc
        return render_markdown(text) if rendered else text

    def transition(self, mission_id: str, status: str, *, next_action: str | None = None) -> dict:
        if status not in STATUSES:
            raise MissionRegistryError(f"unknown status: {status}")
        with self._lock:
            data = self._read()
            record = data["missions"].get(mission_id)
            if record is None:
                raise MissionRegistryError(f"no such mission: {mission_id}")
            current = record["status"]
            if status != current and status not in TRANSITIONS[current]:
                raise MissionRegistryError(f"invalid transition: {current} -> {status}")
            record["status"] = status
            if next_action is not None:
                record["next_action"] = next_action.strip()[:500]
            record["updated_at"] = _now()
            self._write(data)
            return self._record(record)

    def promote(self, mission_id: str, *, by: str) -> dict:
        if not by.strip():
            raise MissionRegistryError("operator identity is required for promotion")
        with self._lock:
            record = self.get(mission_id)
            if record["status"] != "proposed":
                raise MissionRegistryError("only proposed missions can be promoted")
            if self.create_job is None:
                raise MissionRegistryError("job creation is unavailable")
            job = self.create_job(record["target"], record["ask"], submitted_by=by)
            data = self._read()
            stored = data["missions"][mission_id]
            stored.update({"status": "framing", "next_action": "inspect frame gate",
                           "job_id": job.get("id"), "updated_at": _now()})
            self._write(data)
            return self._record(stored)
