#!/usr/bin/env python3
"""Build the store index from records/*.json.

A record is data. This script does not run an extension. TEMPLATE.json is
the copy a pull request starts from, and it is not listed.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "records"
CATALOG = ROOT / "catalog.json"
DIST = ROOT / "dist"
TEMPLATE = "TEMPLATE.json"
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(r"^(?:0|[1-9][0-9]{0,2})\.(?:0|[1-9][0-9]{0,2})\.(?:0|[1-9][0-9]{0,2})$")
TOKEN_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*:[a-z0-9]+(?:-[a-z0-9]+)*$")
SLOT_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ALLOWED_STATUS = {"on", "not-in-build"}
ALLOWED_PLANE = {"server", "client"}
REQUIRED = ("id", "title", "version", "plane", "slot", "status", "summary", "detail", "grants")
FORBIDDEN_SUFFIXES = {
    ".wasm",
    ".js",
    ".mjs",
    ".cjs",
    ".py",
    ".so",
    ".dylib",
    ".dll",
    ".exe",
    ".sh",
}


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def refuse_code() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path == Path(__file__).resolve():
            continue
        if ".git" in path.parts or "dist" in path.parts:
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"refusing {path.relative_to(ROOT)}: this repository holds records, not code")


def text_field(entry: dict, key: str, limit: int, extension_id: str) -> str:
    value = entry[key]
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        fail(f"{extension_id} {key} must be 1 to {limit} characters")
    return value


def validate(entry: dict, path: Path) -> str:
    if not isinstance(entry, dict):
        fail(f"{path.name} is not an object")
    extra = sorted(set(entry) - set(REQUIRED))
    if extra:
        fail(f"{path.name} has unknown keys {extra}")
    missing = [key for key in REQUIRED if key not in entry]
    if missing:
        fail(f"{path.name} is missing {missing}")
    extension_id = entry["id"]
    if not isinstance(extension_id, str) or ID_RE.fullmatch(extension_id) is None or len(extension_id) > 64:
        fail(f"{path.name} has a bad id {extension_id!r}")
    if path.stem != extension_id:
        fail(f"{path.name} must be named {extension_id}.json")
    if not isinstance(entry["version"], str) or VERSION_RE.fullmatch(entry["version"]) is None:
        fail(f"{extension_id} version must be major.minor.patch")
    if entry["plane"] not in ALLOWED_PLANE:
        fail(f"{extension_id} plane must be server or client")
    if not isinstance(entry["slot"], str) or SLOT_RE.fullmatch(entry["slot"]) is None:
        fail(f"{extension_id} slot must be a lowercase name")
    if entry["status"] not in ALLOWED_STATUS:
        fail(f"{extension_id} status must be on or not-in-build")
    text_field(entry, "title", 80, extension_id)
    text_field(entry, "summary", 200, extension_id)
    detail = entry["detail"]
    if not isinstance(detail, list) or not detail or len(detail) > 8:
        fail(f"{extension_id} detail must be 1 to 8 sentences")
    for line in detail:
        if not isinstance(line, str) or not line.strip() or len(line) > 240:
            fail(f"{extension_id} has a detail line that is empty or too long")
    grants = entry["grants"]
    if not isinstance(grants, list) or not grants or len(grants) > 8:
        fail(f"{extension_id} must name 1 to 8 grants")
    seen: set[str] = set()
    for grant in grants:
        if not isinstance(grant, str) or TOKEN_RE.fullmatch(grant) is None or grant in seen:
            fail(f"{extension_id} has a bad or repeated grant {grant!r}")
        seen.add(grant)
    return extension_id


def load_records() -> list[dict]:
    if not RECORDS.is_dir():
        fail("records/ is missing")
    files = sorted(path for path in RECORDS.glob("*.json") if path.name != TEMPLATE)
    if not files:
        fail("records/ has no extension")
    entries: list[dict] = []
    seen: set[str] = set()
    for path in files:
        entry = json.loads(path.read_text())
        extension_id = validate(entry, path)
        if extension_id in seen:
            fail(f"duplicate id {extension_id}")
        seen.add(extension_id)
        entries.append(entry)
    return entries


def catalog_text(entries: list[dict]) -> str:
    document = {
        "id": "gunmetal.extensions",
        "version": "1",
        "extensions": entries,
    }
    return json.dumps(document, indent=2) + "\n"


def pack(entries: list[dict]) -> None:
    DIST.mkdir(exist_ok=True)
    for stale in DIST.glob("*"):
        if stale.is_file():
            stale.unlink()
    checksums: list[str] = []
    for entry in entries:
        extension_id = entry["id"]
        package = {
            "interface": "gunmetal.extensions/1",
            "id": extension_id,
            "record": entry,
        }
        body = json.dumps(package, indent=2) + "\n"
        (DIST / f"{extension_id}.json").write_text(body)
        digest = hashlib.sha256(body.encode()).hexdigest()
        checksums.append(f"{digest}  {extension_id}.json")
    (DIST / "SHA256SUMS").write_text("\n".join(checksums) + "\n")
    CATALOG.write_text(catalog_text(entries))


def main() -> None:
    refuse_code()
    check = "--check" in sys.argv
    entries = load_records()
    expected = catalog_text(entries)
    if check:
        if not CATALOG.is_file() or CATALOG.read_text() != expected:
            fail("catalog.json is stale. Run python3 tools/pack.py")
        print(f"catalog.json matches {len(entries)} records")
        return
    pack(entries)
    print(f"packed {len(entries)} extensions")


if __name__ == "__main__":
    main()
