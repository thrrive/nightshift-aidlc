#!/usr/bin/env python3
"""Serve the optional, read-only local Mission Control explorer.

This process indexes durable AIDLC mission bundles and serves their bounded Markdown
documents. It never starts missions, invokes an agent, or exposes the execution runtime.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from mission_registry import MissionRegistry, MissionRegistryError  # noqa: E402

STATIC = ROOT / "static" / "missions.html"


class Handler(BaseHTTPRequestHandler):
    registry: MissionRegistry
    token: str | None = None

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, value: object) -> None:
        self._send(status, json.dumps(value).encode(), "application/json; charset=utf-8")

    def _authorized(self) -> bool:
        return self.token is None or self.headers.get("X-AISDLC-Token", "") == self.token

    def do_GET(self) -> None:  # noqa: N802 - stdlib HTTP handler API
        parsed = urlparse(self.path)
        if parsed.path == "/missions":
            self._send(200, STATIC.read_bytes(), "text/html; charset=utf-8")
            return
        if not parsed.path.startswith("/api/"):
            self._json(404, {"error": "not found"})
            return
        if not self._authorized():
            self._json(401, {"error": "AIDLC token required"})
            return
        try:
            if parsed.path == "/api/missions":
                self.registry.discover()
                query = parse_qs(parsed.query)
                self._json(200, {"missions": self.registry.list(
                    status=query.get("status", [None])[0],
                    target=query.get("target", [None])[0],
                    parent_id=query.get("parent_id", [None])[0],
                )})
                return
            prefix = "/api/missions/"
            if not parsed.path.startswith(prefix):
                self._json(404, {"error": "not found"})
                return
            remainder = parsed.path[len(prefix):]
            mission_id, separator, action = remainder.partition("/")
            if not separator:
                self._json(200, self.registry.get(mission_id))
                return
            if action != "document":
                self._json(404, {"error": "not found"})
                return
            name = parse_qs(parsed.query).get("name", [""])[0]
            rendered = parse_qs(parsed.query).get("render", ["0"])[0] == "1"
            content = self.registry.document(mission_id, name, rendered=rendered)
            self._send(200, content.encode(), "text/html; charset=utf-8" if rendered else "text/plain; charset=utf-8")
        except MissionRegistryError as exc:
            self._json(404, {"error": str(exc)})
        except (OSError, ValueError) as exc:
            self._json(500, {"error": str(exc)})

    def log_message(self, format: str, *args: object) -> None:
        print("mission-control:", format % args, file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8091)
    parser.add_argument("--mission-root", action="append", default=[], type=Path,
                        help="project root to scan (repeat for multiple local repos)")
    parser.add_argument("--state-dir", type=Path,
                        default=Path(os.environ.get("AIDLC_CONTROL_PLANE_STATE", ".mission-control")))
    parser.add_argument("--token", default=os.environ.get("AIDLC_INBOUND_TOKEN"),
                        help="optional token required for API requests")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    roots = args.mission_root or [Path.cwd()]
    registry = MissionRegistry(args.state_dir, project_roots=roots)
    Handler.registry = registry
    Handler.token = args.token
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Mission Control: http://{args.host}:{args.port}/missions")
    print("Scanning roots:", ", ".join(str(root.resolve()) for root in roots))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    finally:
        server.server_close()


if __name__ == "__main__":
    raise SystemExit(main())
