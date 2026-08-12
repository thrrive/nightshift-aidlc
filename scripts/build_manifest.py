#!/usr/bin/env python3
"""Build the deterministic public-package integrity manifest."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "PACKAGE-MANIFEST.json"


def package_files() -> list[Path]:
    output = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return [
        ROOT / line
        for line in sorted(output.splitlines())
        if line and line != MANIFEST.name and not line.startswith("tests/")
    ]


def main() -> int:
    entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in package_files()
    ]
    MANIFEST.write_text(json.dumps({"files": entries}, indent=2) + "\n")
    print(f"Wrote {len(entries)} entries to {MANIFEST.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
