#!/usr/bin/env python3
"""Office Artifacts: The One-Line Placard.

Writes a single-line museum placard for an ordinary office object --
the whiteboard -- treated as an ancient artifact, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default: output/entry.txt).

Python 3.13 standard library only.
"""

import os
import sys

# The placard is one sentence-chain: object, date, relic, provenance.
# Joined with single spaces so the line is exactly 153 characters.
ENTRY = " ".join(
    [
        "Whiteboard, c. 2011. Its surface still bears last quarter's targets,",
        "in a hand no one can read, for a product no one sells.",
        "Gift of the Strategy Offsite.",
    ]
)

MAX_CHARS = 180


def validate(text: str) -> None:
    """Enforce the competition gate on the entry text.

    Raises ValueError with a plain reason on the first failure.
    """
    if not isinstance(text, str):
        raise ValueError("entry is not text")
    if len(text) < 1:
        raise ValueError("entry is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} characters, over the 180 limit")
    if text.strip() == "":
        raise ValueError("entry is only whitespace")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    for ch in text:
        if ord(ch) < 0x20 or ord(ch) == 0x7F:
            raise ValueError(f"entry contains control character U+{ord(ch):04X}")
    # Must round-trip as strict UTF-8 with no surrogate or odd encoding.
    text.encode("utf-8")


def main() -> int:
    validate(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts the line itself, so write
    # exactly the line bytes and nothing else.
    with open(path, "wb") as f:
        f.write(ENTRY.encode("utf-8"))
    # Round-trip check: what landed on disk must be byte-identical to
    # the entry, so a partial write or encoding slip fails loudly
    # instead of shipping a corrupt placard.
    with open(path, "rb") as f:
        written = f.read()
    if written != ENTRY.encode("utf-8"):
        raise ValueError(
            f"entry.txt round-trip mismatch: wrote {len(written)} bytes, "
            f"expected {len(ENTRY.encode('utf-8'))}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
