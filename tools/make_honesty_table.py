#!/usr/bin/env python3
"""Render the README's honesty table from tests/test_silence.py.

    python tools/make_honesty_table.py            # print
    python tools/make_honesty_table.py --check    # exit 1 if the README is out of date

The table is the claim this tool lives or dies by, and it used to be kept by hand — which is
the drift whypass is built to catch. Generating it from the test file means documentation and
behaviour cannot disagree: if they differ, CI fails.

Importing the test module is deliberate. The cases ARE the documentation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BEGIN = "<!-- BEGIN generated: honesty table -->"
END = "<!-- END generated: honesty table -->"


def table() -> str:
    sys.path.insert(0, str(ROOT / "tests"))
    from test_silence import CASES  # type: ignore[import-not-found]

    lines = [
        BEGIN,
        "| draft | flagged? | why that is right — or the rail that is wrong |",
        "|---|---|---|",
    ]
    for c in CASES:
        draft = c.draft if len(c.draft) <= 84 else c.draft[:81] + "…"
        draft = draft.replace("|", "\\|")
        # a draft containing a backtick needs a double-backtick fence, or it breaks the table
        fence = "``" if "`" in draft else "`"
        draft = f"{fence}{draft}{fence}"
        if c.misfire:
            m = re.search(r"\b(A\d(?:-T\d)?|ABS|REC|SIL)\b", c.misfire)
            state = f"❌ **wrongly** — `{m.group(1) if m else '?'}`"
            why = c.misfire
        else:
            state = "✅ **not** flagged"
            why = c.why
        # NB: no backslash inside an f-string expression — that is a SyntaxError before
        # Python 3.12, and this project supports 3.10. Escape first, interpolate after.
        why_cell = why.replace("|", "\\|")
        lines.append(f"| {draft} | {state} | {why_cell} |")
    misfires = sum(1 for c in CASES if c.misfire)
    lines.append(
        f"\n*Generated from `tests/test_silence.py` — {len(CASES)} cases, "
        f"{misfires} of them currently misfiring. Do not edit by hand: edit the test file and "
        "run `tools/make_honesty_table.py`.*"
    )
    lines.append(END)
    return "\n".join(lines)


def main() -> int:
    rendered = table()
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    if "--check" in sys.argv:
        start, end = text.find(BEGIN), text.find(END)
        if start == -1 or end == -1:
            print("README has no generated-table markers")
            return 1
        if text[start : end + len(END)].strip() != rendered.strip():
            print("README's honesty table is out of date with tests/test_silence.py")
            return 1
        print("honesty table is current")
        return 0
    if BEGIN in text:
        readme.write_text(
            text[: text.find(BEGIN)] + rendered + text[text.find(END) + len(END) :],
            encoding="utf-8",
        )
        print("README's honesty table regenerated")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
