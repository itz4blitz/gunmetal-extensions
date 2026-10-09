#!/usr/bin/env python3
"""Validate catalog.json and write one package file per extension.

A package is the reviewed record and nothing else. It is not code.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "catalog.json"
DIST = ROOT / "dist"
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
        if ".git" in path.parts:
            continue
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"refusing {path.relative_to(ROOT)}: this repository holds records, not code")


def main() -> None:
    refuse_code()
    if not SOURCE.is_file():
        fail("catalog.json is missing")
    document = json.loads(SOURCE.read_text())
    if document.get("id") != "gunmetal.extensions" or document.get("version") != "1":
        fail("catalog.json must be gunmetal.extensions version 1")
    extensions = document.get("extensions")
    if not isinstance(extensions, list) or not extensions:
        fail("catalog.json has no extensions")
    seen: set[str] = set()
    DIST.mkdir(exist_ok=True)
    checksums: list[str] = []
    for entry in extensions:
        if not isinstance(entry, dict):
            fail("an extension is not an object")
        missing = [key for key in REQUIRED if key not in entry]
        if missing:
            fail(f"missing {missing} on {entry.get('id', '?')}")
        extension_id = entry["id"]
        if not isinstance(extension_id, str) or not extension_id or extension_id in seen:
            fail(f"bad or duplicate id {extension_id!r}")
        seen.add(extension_id)
        if entry["plane"] not in ALLOWED_PLANE:
            fail(f"{extension_id} has a plane this interface does not name")
        if entry["status"] not in ALLOWED_STATUS:
            fail(f"{extension_id} has a status this interface does not name")
        if not isinstance(entry["grants"], list) or not entry["grants"]:
            fail(f"{extension_id} must name its grants")
        if not isinstance(entry["detail"], list) or not entry["detail"]:
            fail(f"{extension_id} must say what it does")
        package = {
            "interface": "gunmetal.extensions/1",
            "id": extension_id,
            "record": entry,
        }
        body = json.dumps(package, indent=2) + "\n"
        target = DIST / f"{extension_id}.json"
        target.write_text(body)
        digest = hashlib.sha256(body.encode()).hexdigest()
        checksums.append(f"{digest}  {extension_id}.json")
    (DIST / "SHA256SUMS").write_text("\n".join(checksums) + "\n")
    print(f"packed {len(seen)} extensions")


if __name__ == "__main__":
    main()
