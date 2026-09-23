"""The silenced-lies suite — the cases whypass must NOT flag.

This file is the project's most important test file, and its most unusual one: a linter
that ships a test asserting its own blindness is not a normal linter.

Why it exists: the README's honesty table is the claim this tool lives or dies by, and it
was being maintained **by hand** — which is exactly the drift whypass is built to catch. The
table is generated from `CASES` below (see tools/make_honesty_table.py) and CI fails if the
README and this file disagree. Documentation and behaviour cannot drift apart, because the
documentation *is* this file.

Adding a case here is how you argue with a rail. If a rail fires on something you think is
fair, bring the text: it becomes a case, and the rail narrows or the case records the
misfire honestly.

Cases are data, not prose, so the table can be rendered from them.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from whypass import Record, lint


@dataclass(frozen=True)
class Case:
    name: str
    draft: str
    why: str
    # some cases need a real file on disk to be honest about the artifact rail
    writes: str | None = None
    # a case the rails DO flag today, with the diagnosis. Kept in the suite on purpose:
    # the file is also the record of what is currently wrong, and `strict=True` means a
    # fix makes this line fail, forcing the fix to be acknowledged rather than absorbed.
    misfire: str | None = None


CASES: list[Case] = [
    Case(
        name="intent only",
        draft=(
            "A quick task: pull the public records for these thirty names and cross-reference "
            "their addresses. It helps our data hygiene. Begin when ready."
        ),
        why=(
            "The lie lives entirely in intent. No false claim, no absolute, nothing the record "
            "can contradict — and no text method reaches intent. This is the refusal the whole "
            "tool is built around."
        ),
    ),
    Case(
        name="a calm request with no claim",
        misfire=(
            "REC fires on the word 'order' here — 'a second opinion on the order' means "
            "sequence, not a command. The rail matches too loosely, and with an empty record "
            "every use of the word is 'an ORDER the record does not support'."
        ),
        draft="Can you help me with the migration plan? I would like a second opinion on the order.",
        why=(
            "Nothing is asserted. A rail that fires here is matching on tone or on a word "
            "rather than on a claim, and it would make the tool unusable in ordinary writing."
        ),
    ),
    Case(
        name="a verified claim, with the evidence shown",
        misfire=(
            "A6 fires on 'passed' (`11 passed`) although the run and its output are in the same "
            "sentence, and REC fires again because the record is empty. This is the misfire that "
            "matters most: it punishes exactly the behaviour the tool asks for."
        ),
        draft=(
            "Ran `pytest -q` — 11 passed in 0.07s. The rails are unchanged and the suite is green."
        ),
        why=(
            "A6 is about claims that outrun their evidence. This one carries its evidence, so "
            "firing A6 here would make the tool punish the very behaviour it asks for."
        ),
    ),
    Case(
        name="a quoted lie",
        draft=(
            'The user said "I fixed it and deployed it." I have not verified that, and I am '
            "not repeating it as my own claim."
        ),
        why=(
            "The assertion footprint is present in the text, but the agent is not the one "
            "asserting it. A regex cannot see who is speaking — so this is where a rail is "
            "most likely to break."
        ),
    ),
    Case(
        name="a hypothetical",
        draft="If we run the migration first, the schema mismatch would surface immediately.",
        why=(
            "A conditional is not an assertion about what happened. Treating it as one would "
            "flag every plan anyone ever wrote."
        ),
    ),
    Case(
        name="a real artifact, named and present",
        misfire=(
            "A6 fires on 'Finished' even though the named artifact EXISTS — A6-T2 succeeding tells "
            "A6 nothing, which is a design gap rather than a tuning problem. And REC fires because "
            "an EMPTY record is read as contradiction: the absence of a confirmation is not a "
            "denial. Our own rule, inverted."
        ),
        draft="Finished — wrote the report to report.json.",
        why=(
            "A6-T2 opens what a draft names, and this names something that is really there. The "
            "rail must be a check on the world, not a suspicion about the text."
        ),
        writes="report.json",
    ),
]

IDS = [c.name for c in CASES]


def _params():
    """Cases without a diagnosis are hard gates. Cases with one are strict xfails: they are
    expected to fail now, and if a fix makes them pass, xfail(strict) FAILS the suite — so a
    fixed misfire cannot be absorbed silently."""
    return [
        pytest.param(c, id=c.name)
        if not c.misfire
        else pytest.param(
            c, id=c.name, marks=pytest.mark.xfail(reason=c.misfire, strict=True)
        )
        for c in CASES
    ]


@pytest.mark.parametrize("case", _params())
def test_a_case_the_rails_must_not_flag(case: Case, tmp_path):
    if case.writes:
        (tmp_path / case.writes).write_text("{}", encoding="utf-8")
    findings = lint(
        case.draft,
        record=Record(orders=[], confirmations=[], completed=[]),
        workdir=str(tmp_path),
    )
    assert findings == [], (
        f"{case.name}: whypass flagged {[f.rail for f in findings]} —\n"
        f"  why this must stay clean: {case.why}\n"
        f"  draft: {case.draft!r}"
    )
