"""Make an explicit public derivative of selected UTF-8 source evidence.

Only absolute resource locators with a path component below a known local
root are replaced. Relative links and scientific slash notation are evidence.
This is a curator utility, not a scientific transformation or a producer form.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

# A left word/slash boundary prevents matching the suffix of a relative path
# such as reviews/root_receipt.json or the scientific phrase gates/workspace.
# Requiring a slash BELOW the root prevents /privately and /rooted from
# matching a root prefix. Bare root names contain no private path component.
_LOCATOR = re.compile(
    r"(?<![\w/])(?:sandbox:)?/(?:workspace|root|Users|home|tmp|private|mnt|content)/"
    r"[^\s\"'`<>\]\[(){};,]+"
)


def portable_source(original: bytes) -> tuple[bytes, list[dict[str, str]]]:
    """Return a derivative and a non-sensitive ledger; leave input bytes intact."""
    text = original.decode("utf-8")  # Binary evidence requires its own route.
    replacements: list[dict[str, str]] = []

    def replace(match: re.Match[str]) -> str:
        raw = match.group(0)
        public = "producer-workspace/" + raw.rstrip("/").rsplit("/", 1)[-1]
        replacements.append({
            "original_locator_sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "public_locator": public,
        })
        return public

    return _LOCATOR.sub(replace, text).encode("utf-8"), replacements


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args(argv)
    if args.input.resolve() == args.output.resolve() or args.output.exists():
        parser.error("Use a new derivative path; original and historical bytes must remain.")
    original = args.input.read_bytes()
    public, replacements = portable_source(original)
    # Exclusive creation protects an existing artifact even if it appeared
    # between the existence check and the write. No implicit parent creation.
    with args.output.open("xb") as stream:
        stream.write(public)
    print(json.dumps({
        "original_sha256": hashlib.sha256(original).hexdigest(),
        "public_sha256": hashlib.sha256(public).hexdigest(),
        "original_bytes": len(original), "public_bytes": len(public),
        "resource_locator_replacements": replacements,
        "scope": "Explicit resource-locator derivative; index it using the existing source-index format.",
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
