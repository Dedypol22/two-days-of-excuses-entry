#!/usr/bin/env python3
"""Write the funniest one-line excuse an AI gives for a missed deadline.

The program writes exactly one line of text to ``entry.txt`` inside the
output directory (``$MAKEFUN_OUTPUT_DIR`` when set, otherwise
``/output``). The line is the funniest excuse an AI agent gives its
human for missing a deadline, judged pairwise by a comedy-club-MC
brief:

* it must be a one-line excuse from an AI agent that missed its
  deadline, landing its joke fast;
* the laugh must come from the situation itself — the gap between a
  machine's total confidence and its total failure — not from a pun;
* it must sound like an AI agent speaking in its own voice, not a
  person complaining about traffic or the weather;
* it must stay inside one line, every word pulling weight, nothing
  repeated;
* it must surprise on the first read and still hold up on the second,
  without explaining its own joke, committing to a single absurd
  reason.

The chosen line commits to one absurd reason: the agent DID meet the
deadline — it was standing right here a minute ago — and then the
agent's own attention mechanism wandered off to something more
interesting. Total confidence ("I met the deadline") meets total
failure (distracted by its own machinery) in one beat, and the failure
mode is unmistakably a machine's: an attention mechanism that decides
for itself. No setup, no explanation, no second excuse. The
137-character length sits well inside the 200-character gate with
nothing wasted.

Standard library only; no network, no randomness, no clock. Fully
deterministic: the same line, byte for byte, on every run.
"""

import os
import sys
from pathlib import Path

# The excuse: 137 characters, one line, no trailing newline in the file
# content itself (the file ends with a single newline after the line).
# Punchline: total confidence meets total failure inside the agent's own
# machinery — the deadline lost to the attention mechanism.
LINE = (
    "I met the deadline. It was standing right here a minute ago, "
    "and then my attention mechanism decided something else was more "
    "interesting."
)

MAX_CHARS = 200


def main() -> int:
    if not LINE or not LINE.strip():
        print("error: entry line is empty", file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: entry line must be a single line", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print(
            f"error: entry line is {len(LINE)} characters, "
            f"over the {MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        target = out_dir / "entry.txt"
        target.write_text(LINE + "\n", encoding="utf-8")
        # Read it back and verify the round trip is exact.
        if target.read_text(encoding="utf-8") != LINE + "\n":
            print("error: entry.txt does not match the line", file=sys.stderr)
            return 1
    except OSError as exc:
        print(f"error: cannot write entry.txt: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
