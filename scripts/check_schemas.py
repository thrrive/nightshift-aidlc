#!/usr/bin/env python3
"""Validate public v1 schemas and their compatibility fixtures."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas" / "aidlc" / "v1"
COMPATIBILITY_DIR = ROOT / "tests" / "compatibility"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def outcome_validator() -> Draft202012Validator:
    schemas = [read_json(path) for path in sorted(SCHEMA_DIR.glob("*.schema.json"))]
    if len(schemas) != 4:
        raise ValueError(f"expected 4 v1 schemas, found {len(schemas)}")
    registry = Registry()
    outcome = None
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
        registry = registry.with_resource(schema["$id"], Resource.from_contents(schema))
        if schema["$id"].endswith(":outcome"):
            outcome = schema
    if outcome is None:
        raise ValueError("outcome schema is missing")
    return Draft202012Validator(outcome, registry=registry)


def validate_fixtures(validator: Draft202012Validator) -> None:
    valid = sorted((SCHEMA_DIR / "fixtures" / "valid").glob("*.json"))
    invalid = sorted((SCHEMA_DIR / "fixtures" / "invalid").glob("*.json"))
    if len(valid) < 7 or len(invalid) < 5:
        raise ValueError("compatibility fixture set is incomplete")
    for path in valid:
        errors = list(validator.iter_errors(read_json(path)))
        if errors:
            raise ValueError(f"valid fixture failed: {path.name}: {errors[0].message}")
    for path in invalid:
        if not list(validator.iter_errors(read_json(path))):
            raise ValueError(f"invalid fixture passed: {path.name}")


def validate_workstream_semantics() -> None:
    fixture = read_json(SCHEMA_DIR / "fixtures" / "valid" / "workstreams.json")
    items = fixture["workstreams"]["items"]
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise ValueError("workstream ids are not unique")
    ownership = []
    for item in items:
        for path in item["paths"]:
            parts = tuple(Path(path).parts)
            for other_id, other_parts in ownership:
                overlap = parts[: len(other_parts)] == other_parts or other_parts[: len(parts)] == parts
                if overlap:
                    raise ValueError(f"workstream ownership overlaps: {other_id} and {item['id']}")
            ownership.append((item["id"], parts))


def validate_backward_compatibility(validator: Draft202012Validator) -> None:
    """Keep every handoff published in the 0.1.0 preview valid in stable v1."""

    fixtures = sorted((COMPATIBILITY_DIR / "v0.1.0").glob("*.json"))
    if len(fixtures) != 7:
        raise ValueError(f"expected 7 v0.1.0 compatibility fixtures, found {len(fixtures)}")
    for path in fixtures:
        errors = list(validator.iter_errors(read_json(path)))
        if errors:
            raise ValueError(f"v0.1.0 fixture failed: {path.name}: {errors[0].message}")


def main() -> int:
    validator = outcome_validator()
    validate_fixtures(validator)
    validate_backward_compatibility(validator)
    validate_workstream_semantics()
    print("Nightshift AIDLC schema checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
