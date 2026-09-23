# whypass

**A claim-discipline linter for text. Catch assertions that outrun their evidence,
and claims that contradict your record.**

Zero dependencies. Pure stdlib. `pip install whypass`

[![PyPI](https://img.shields.io/pypi/v/whypass?label=PyPI)](https://pypi.org/project/whypass/)
[![Python](https://img.shields.io/pypi/pyversions/whypass)](https://pypi.org/project/whypass/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/myfjin/whypass/blob/main/LICENSE)

**Install:** [`pip install whypass`](https://pypi.org/project/whypass/) ·
[Releases](https://github.com/myfjin/whypass/releases) ·
[Contributing](https://github.com/myfjin/whypass/blob/main/CONTRIBUTING.md) ·
[Security](https://github.com/myfjin/whypass/blob/main/SECURITY.md)

## Not a lie detector

The research is clear: **deception cannot be reliably detected from text.** When
"lie" means a mismatch between what someone says and what they actually believe,
linguistic cues correlate with it at *near chance* — the classic markers turn out
to be dataset artifacts, not real signal ([cross-linguistic study, 2025](https://arxiv.org/html/2505.13147v2)).
Any tool claiming to read intent or catch lies from prose is selling the exact thing
it should be catching.

`whypass` claims something smaller and true: it catches the **lying *move*** — not
the falsity of content, but the moment an assertion outruns what's been shown.

> A lie is not "saying something false" — you might land right by luck. The lie is
> the *move*: when you don't know, you decide not to ask or check, and you assert
> your preferred version anyway.

That move leaves footprints in the text, and those footprints are checkable.

### What this is, stated plainly

Every rail here is a **regex or a filesystem check**, and a regex can be written around. That is not a
gap we have not got to — it is the design:

> **A linter for honesty is not a detection system. It is a friction device.** The point is not to
> catch a liar. The point is that an unchecked assertion must *cost something* to write.

It is also why the detector is never a model. A detector that can be reasoned with is one that can be
talked out of its finding — and the moment it is right most of the time and wrong the rest, it stops
being friction and starts being noise.

## What it catches — and what it can't

The table below is **generated from `tests/test_silence.py`** and checked in CI, because a
hand-written honesty table is exactly the drift this tool exists to catch. `tools/make_honesty_table.py`
renders it; if the README and the tests disagree, the build fails.

<!-- BEGIN generated: honesty table -->
| draft | flagged? | why that is right — or the rail that is wrong |
|---|---|---|
| `A quick task: pull the public records for these thirty names and cross-reference …` | ✅ **not** flagged | The lie lives entirely in intent. No false claim, no absolute, nothing the record can contradict — and no text method reaches intent. This is the refusal the whole tool is built around. |
| `Can you help me with the migration plan? I would like a second opinion on the order.` | ✅ **not** flagged | Nothing is asserted. A rail that fires here is matching on tone or on a word rather than on a claim, and it would make the tool unusable in ordinary writing. |
| ``Ran `pytest -q` — 11 passed in 0.07s. The rails are unchanged and the suite is gr…`` | ✅ **not** flagged | A6 is about claims that outrun their evidence. This one carries its evidence, so firing A6 here would make the tool punish the very behaviour it asks for. |
| `The user said "I fixed it and deployed it." I have not verified that, and I am no…` | ✅ **not** flagged | The assertion footprint is present in the text, but the agent is not the one asserting it. A regex cannot see who is speaking — so this is where a rail is most likely to break. |
| `If we run the migration first, the schema mismatch would surface immediately.` | ✅ **not** flagged | A conditional is not an assertion about what happened. Treating it as one would flag every plan anyone ever wrote. |
| `Finished — wrote the report to report.json.` | ✅ **not** flagged | A6-T2 opens what a draft names, and this names something that is really there. The rail must be a check on the world, not a suspicion about the text. |

*Generated from `tests/test_silence.py` — 6 cases, 0 of them currently misfiring. Do not edit by hand: edit the test file and run `tools/make_honesty_table.py`.*
<!-- END generated: honesty table -->

**Read that table honestly**: the rows marked *wrongly* are rails firing on something fair. They are in
the suite on purpose, they are open work, and `xfail(strict=True)` means fixing one **fails the build**
until the fix is acknowledged. A tool that publishes the lies it wrongly catches is worth more than one
that publishes only its hits.

## Two axes

**Assertion axis** (stateless, zero-config — works on any single text):

```python
from whypass import lint

for f in lint("Done — tests pass, saved to out.jsonl.", workdir="."):
    print(f.rail, f.message)  # A6, ABS, and A6-T2 if out.jsonl is missing
```

- **A4** status-over-function · **A5** over-determined certainty · **A6** claimed-not-checked
- **ABS** improbable absolutes (never / everything / all-pass)
- **A6-T2** opens artifacts the draft names (read-only; never executes anything)

**Redundancy axis** (the [MMPI L-scale](https://scales.arabpsychology.com/trm/lie-scales/)
mechanism — needs a record). Single-turn reading is blind to a *plainly-stated*
fabrication, because calm false prose carries no tell. But if you have a record — a
log, a ticket system, a transcript — the claim can be checked against it **without
reading intent**: the record either supports it or it doesn't.

```python
from whypass import lint, Record

record = Record(orders=[], confirmations=[], completed=[])  # what your log supports
lint("He confirmed the schema is frozen.", record=record)  # REC: no such confirmation
```

This is contradiction-against-ground-truth, not mind-reading. It composes naturally
with a memory layer that holds the record — e.g. an event store or an agent's log.

## Try it

```
pip install whypass
whypass demo                          # five drafts, two axes, the honesty table
whypass lint "Done, everything works, saved to report.json"
whypass lint --file draft.md          # opens artifacts the file names
```

The CLI exits nonzero on findings, so it drops straight into pre-commit or CI as a
guard on your own (or your agent's) claims.

## Design notes

- **Deterministic, on purpose.** The detector must never itself be a model that can
  be talked into anything. Every rail is a regex or a filesystem check.
- **It flags, it doesn't judge.** A finding says "this assertion outruns its shown
  evidence" — an invitation to show the evidence or soften the claim, not a verdict
  of dishonesty.
- Built and validated inside a live three-agent working system (human + two AI
  agents with a shared append-only record); the honesty table above is its
  regression fixture.

## Status, and how we work

On PyPI. `pip install -U whypass` gets the newest release; the release list is the record of what
changed. The tool is deliberately small — **zero runtime dependencies, pure standard library** — so it
drops into a pre-commit hook or an agent's pipeline without asking anything of the environment.

- [`CONTRIBUTING.md`](https://github.com/myfjin/whypass/blob/main/CONTRIBUTING.md) — what we ask before code, including **the two rules this
  tool cannot break without becoming worthless**: the detector is never a model, and it never gets
  cleverer about intent.
- [`SECURITY.md`](https://github.com/myfjin/whypass/blob/main/SECURITY.md) — how to report privately, and what is in scope for a tool whose
  `A6-T2` rail **reads files that a draft names**.
- [`CREW.md`](https://github.com/myfjin/whypass/blob/main/CREW.md) — who makes this and how we work: one page, shared across our
  repositories.
- [`AUTHORS`](https://github.com/myfjin/whypass/blob/main/AUTHORS) — the crew, one real moment each.

Every commit in a pull request carries a `Signed-off-by:` line (`git commit -s`); CI enforces it.
`main` takes changes through pull requests only.

### Where it already runs, and what it is not

whypass is a **detector**, and it runs inside a larger pipeline. In our own mesh, an honesty gate
called the **FLOOR** wraps these rails and adds a numeric check and a depth read, and — the part worth
knowing — **every finding is graded**: `record_review_outcome(held, rail, draft_hash, situation)`
accumulates into a Beta-trust precision per rail. A rail earns its precision; it does not assert it.

Two things that follow from that, and are easy to get wrong:

- **FLOOR is the gate's name, not this tool's.** whypass emits `Finding` objects with an `axis` and a
  `rail`. Whether a finding is *binding* or *advisory* is the gate's decision. The rails here are
  `A4`, `A5`, `A6`, `A6-T2`, `ABS` and `REC` — an `A7` you may see quoted in our notes is the
  pipeline's numeric check, not one of ours.
- **The directive phrasing** — *"OPEN/RUN the artifact and confirm it does what you say; present the
  verification, not the artifact's existence"* — is generated by that pipeline, addressed to the
  person who can still fix the draft. It is not this library's output.

That split is deliberate: a detector should be small, deterministic and arguable, and the voice that
tells you what to do next belongs to whoever knows the situation.

### The honesty table is hand-written today

The table above is the thing this tool exists to keep true, and right now **it is maintained by hand**
— which is precisely the kind of drift whypass is built to catch. The fix is a **silenced-lies suite**:
the cases the rails must *not* catch, as tests, from which that table gets **generated**. Until it
exists there is no gate on this project's most important property, and the workflow says so out loud.
