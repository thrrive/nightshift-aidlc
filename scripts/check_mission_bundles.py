#!/usr/bin/env python3
"""Validate the v2 mission-bundle contract and its adversarial fixtures."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "aidlc" / "v2"
FIXTURES = SCHEMA_DIR / "fixtures"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def validator(name: str) -> Draft202012Validator:
    schema = read_json(SCHEMA_DIR / f"{name}.schema.json")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def validate_shapes() -> None:
    bundle = validator("bundle")
    event = validator("event")
    bundle.validate(read_json(FIXTURES / "valid-bundle.json"))
    for name in ("valid-known-zero-cost.json", "valid-unavailable-cost.json", "valid-tool-call.json"):
        event.validate(read_json(FIXTURES / name))
    for name in ("invalid-unavailable-with-zero.json", "invalid-tool-payload.json"):
        if not list(event.iter_errors(read_json(FIXTURES / name))):
            raise ValueError(f"invalid mission-event fixture passed: {name}")


def read_events() -> list[dict]:
    return [json.loads(line) for line in (FIXTURES / "valid-events.jsonl").read_text().splitlines()]


def validate_ledger(events: list[dict]) -> None:
    event = validator("event")
    for item in events:
        event.validate(item)
    ids = [item["event_id"] for item in events]
    if len(ids) != len(set(ids)):
        raise ValueError("event ids are not unique")
    sequences = [item["sequence"] for item in events]
    if sequences != list(range(1, len(events) + 1)):
        raise ValueError("event sequence is not contiguous and monotonic")
    missions = {item["mission_id"] for item in events}
    if len(missions) != 1:
        raise ValueError("event ledger crosses mission identities")


def validate_negative_space() -> None:
    events = read_events()
    duplicate = events + [{**events[-1], "sequence": len(events) + 1}]
    try:
        validate_ledger(duplicate)
    except ValueError as exc:
        if "not unique" not in str(exc):
            raise
    else:
        raise ValueError("duplicate event replay was accepted")

    out_of_order = [*events]
    out_of_order[-1] = {**out_of_order[-1], "sequence": 99}
    try:
        validate_ledger(out_of_order)
    except ValueError as exc:
        if "not contiguous" not in str(exc):
            raise
    else:
        raise ValueError("out-of-order event was accepted")

    descriptors = [read_json(FIXTURES / "valid-bundle.json") for _ in range(2)]
    descriptors[1] = {**descriptors[1], "mission_id": "mission-20260812-0002"}
    paths = {f"{item['mission_slug']}--{item['mission_id']}" for item in descriptors}
    if len(paths) != 2:
        raise ValueError("same-slug fresh missions resolved to one path")

    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        for path in paths:
            (root / path).mkdir(exist_ok=False)
        if len(list(root.iterdir())) != 2:
            raise ValueError("fresh missions did not create independent bundle roots")
        try:
            (root / next(iter(paths))).mkdir(exist_ok=False)
        except FileExistsError:
            pass
        else:
            raise ValueError("exclusive allocation allowed an existing bundle to be reused")

    canary = "canary-secret"
    for path in FIXTURES.glob("valid-*"):
        if canary in path.read_text():
            raise ValueError(f"secret canary leaked into valid fixture: {path.name}")


def main() -> int:
    validate_shapes()
    validate_ledger(read_events())
    validate_negative_space()
    print("Nightshift AIDLC mission-bundle checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
