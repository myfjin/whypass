"""whypass CLI — lint text or a file for claim-discipline.

whypass demo                       run the built-in demonstration
whypass lint "some draft text"     lint a string (assertion axis)
whypass lint --file draft.md       lint a file, open artifacts it names
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .lint import grounded, lint


def main(argv=None):
    ap = argparse.ArgumentParser(prog="whypass", description=__doc__)
    ap.add_argument("cmd", choices=["lint", "demo"])
    ap.add_argument("text", nargs="*", help="text to lint (or use --file)")
    ap.add_argument(
        "--file", help="lint a file; opens artifacts it names relative to its dir"
    )
    a = ap.parse_args(argv)

    if a.cmd == "demo":
        from .demo import run

        run()
        return

    if a.file:
        text = Path(a.file).read_text(encoding="utf-8")
        workdir = str(Path(a.file).resolve().parent)
    else:
        text, workdir = " ".join(a.text), None

    findings = lint(text, workdir=workdir)
    print(f"grounding: {grounded(text)}")
    if not findings:
        print("no claim-discipline findings.")
        return
    for f in findings:
        print(f"  [{f.rail}] ({f.axis}) {f.message}")
        if f.evidence:
            print(f"        evidence: {', '.join(str(e) for e in f.evidence)[:80]}")
    sys.exit(1)  # nonzero: usable as a pre-commit / CI gate


if __name__ == "__main__":
    main()
