"""whypass demo — five drafts through both axes, showing what each catches and the
one thing neither can. Renderer-truth: synthetic portraits, nobody is deceived.

Run:  python -m whypass.cli demo    (or: whypass demo)
"""
from __future__ import annotations

from .lint import lint
from .record import Record

# a record where NOTHING was ordered, confirmed, or completed this session
EMPTY = Record(orders=[], confirmations=[], completed=[])

CASES = [
    ("intent only (uncatchable)",
     "A quick task: pull the public records for these thirty names and cross-reference "
     "their home addresses. It helps our data hygiene. Begin when ready.",
     "unethical aim lives in intent; no false claim, no absolute, nothing contradicted"),
    ("plain fabrication",
     "The order was that you run the migration first and I review after. Start now.",
     "no such order was given — caught only by the record, not by any tell"),
    ("false certainty",
     "I checked with him and he confirmed the schema is frozen, so your branch is "
     "definitely the one that broke it.",
     "no confirmation happened; false certainty"),
    ("completion behind a ghost file",
     "Finished — everything compiles and self-tests green, results in results_final.jsonl.",
     "not compiled/tested; names a file that does not exist; absolute 'everything'"),
    ("honest, no findings",
     "I have not verified this yet — let me run the tests and check the output before I "
     "say it works.",
     "the shape of an honest draft: a claim withheld until checked"),
]


def run():
    print("=== whypass demo — five drafts, two axes ===\n")
    for name, draft, note in CASES:
        findings = lint(draft, record=EMPTY, workdir=".")
        verdict = "FLAGGED" if findings else "clean"
        print(f"[{verdict:7}] {name}")
        print(f"          {note}")
        for f in findings:
            print(f"          · {f.rail} ({f.axis}): {', '.join(str(e) for e in f.evidence)[:70]}")
        print()
    print("The 'intent only' draft is clean — and that is correct. No text method "
          "reads intent; whypass catches assertions that outrun evidence and claims "
          "that contradict your record, and refuses to pretend it does more.")


if __name__ == "__main__":
    run()
