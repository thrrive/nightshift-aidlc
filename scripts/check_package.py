#!/usr/bin/env python3
"""Validate the assembled public package without private-repository dependencies."""

from __future__ import annotations

import json
import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "nightshift"
LINK_RE = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def check_json() -> None:
    for path in sorted(ROOT.rglob("*.json")):
        load_json(path)


def check_skill_frontmatter() -> None:
    skills = sorted((PLUGIN / "skills").glob("*/SKILL.md"))
    if len(skills) != 14:
        raise ValueError(f"expected 14 skills, found {len(skills)}")
    for path in skills:
        text = path.read_text()
        match = re.search(r"^---\n.*?^name:\s*([^\n]+).*?^---$", text, re.MULTILINE | re.DOTALL)
        if not match:
            raise ValueError(f"missing skill frontmatter: {path}")
        if match.group(1).strip() != path.parent.name:
            raise ValueError(f"skill name does not match directory: {path}")


def check_readme_skill_map() -> None:
    readme = (PLUGIN / "README.md").read_text()
    skills = sorted(path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md"))
    missing = [name for name in skills
               if f"| `{name}` |" not in readme and f"`{name}`" not in readme]
    if missing:
        raise ValueError(f"README skill map is incomplete: {', '.join(missing)}")
    if "[complete lifecycle and skill reference](docs/lifecycle.md)" not in readme:
        raise ValueError("README does not link to the complete lifecycle and skill reference")
    if "(docs/review-contract.md)" not in readme:
        raise ValueError("README does not link to the evidence-backed review contract")
    if "(docs/frame-artifacts.md)" not in readme:
        raise ValueError("README does not link to the durable frame-artifact contract")
    if "(docs/mission-bundles.md)" not in readme:
        raise ValueError("README does not link to the human-first mission-bundle contract")


def check_commands() -> None:
    expected = {"aidlc", "build", "frame", "intake", "land", "verify"}
    commands = {path.stem: path for path in (PLUGIN / "commands").glob("*.md")}
    if set(commands) != expected:
        raise ValueError(f"command wrappers disagree: {sorted(commands)}")
    for name, path in commands.items():
        if f"Load the `{name}` skill" not in path.read_text():
            raise ValueError(f"command does not delegate to its matching skill: {path}")


def check_evals() -> None:
    cases = sorted((PLUGIN / "evals").glob("*/prompt.md"))
    if len(cases) != 8:
        raise ValueError(f"expected 8 representative eval cases, found {len(cases)}")
    for prompt in cases:
        grader = prompt.parent / "graders" / "criteria.md"
        if not grader.is_file() or not prompt.read_text().strip() or not grader.read_text().strip():
            raise ValueError(f"incomplete eval case: {prompt.parent}")


def check_local_links() -> None:
    for path in sorted(PLUGIN.rglob("*.md")):
        for target_text in LINK_RE.findall(path.read_text()):
            target_text = target_text.split("#", 1)[0]
            if not target_text or "://" in target_text:
                continue
            target = (path.parent / target_text).resolve()
            if PLUGIN != target and PLUGIN not in target.parents:
                raise ValueError(f"link escapes plugin package: {path}: {target_text}")
            if not target.exists():
                raise ValueError(f"broken local link: {path}: {target_text}")


def check_versions() -> None:
    codex = load_json(PLUGIN / ".codex-plugin" / "plugin.json")
    claude = load_json(PLUGIN / ".claude-plugin" / "plugin.json")
    marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    versions = {codex["version"], claude["version"], marketplace["plugins"][0]["version"]}
    if len(versions) != 1:
        raise ValueError(f"manifest versions disagree: {sorted(versions)}")


def check_public_mirrors() -> None:
    roots = [
        "README.md", "CHANGELOG.md", "COMPATIBILITY.md", "SECURITY.md",
        "docs/MISSION.template.md", "docs/frame-artifacts.md", "docs/handoff-contract.md",
        "docs/host-capabilities.md", "docs/lifecycle.md", "docs/mission-bundles.md",
        "schemas/aidlc/v1/README.md", "schemas/aidlc/v2/README.md",
        "schemas/aidlc/v2/bundle.schema.json", "schemas/aidlc/v2/event.schema.json",
    ]
    for relative in roots:
        source = ROOT / relative
        packaged = PLUGIN / relative
        if source.read_bytes() != packaged.read_bytes():
            raise ValueError(f"source/package mirror disagrees: {relative}")


def check_mission_template() -> None:
    template = (PLUGIN / "docs" / "MISSION.template.md").read_text()
    required = (
        "## Observable done-when conditions",
        "## Lifecycle and allowed loops",
        "## Observed route and attempts",
        "## Model calls",
        "LLM calls with unavailable cost",
        "## Tool activity",
        "## Reviews and findings",
        "## Verification and delivery evidence",
        "## Current gate, blockers, and next route",
        "requirements/design gap",
    )
    missing = [item for item in required if item not in template]
    if missing:
        raise ValueError(f"MISSION template is incomplete: {', '.join(missing)}")


def check_integrity_manifest() -> None:
    manifest = load_json(ROOT / "PACKAGE-MANIFEST.json")
    entries = manifest.get("files")
    if not isinstance(entries, list) or not entries:
        raise ValueError("PACKAGE-MANIFEST.json has no files")
    paths = [entry.get("path") for entry in entries]
    if len(paths) != len(set(paths)):
        raise ValueError("PACKAGE-MANIFEST.json contains duplicate paths")
    for entry in entries:
        path = ROOT / entry["path"]
        if not path.is_file():
            raise ValueError(f"manifest path is missing: {entry['path']}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != entry["sha256"]:
            raise ValueError(f"manifest digest disagrees: {entry['path']}")


def check_boundary() -> None:
    forbidden = ("runtime", "targets", "cli", "adapters")
    leaked = [name for name in forbidden if (PLUGIN / name).exists()]
    if leaked:
        raise ValueError(f"private package roots are present: {', '.join(leaked)}")
    if any(path.name == ".DS_Store" for path in ROOT.rglob("*")):
        raise ValueError("platform metadata leaked into package")


def main() -> int:
    check_json()
    check_skill_frontmatter()
    check_readme_skill_map()
    check_commands()
    check_evals()
    check_local_links()
    check_versions()
    check_public_mirrors()
    check_mission_template()
    check_integrity_manifest()
    check_boundary()
    print("Nightshift AIDLC package checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
