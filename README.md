# whypass

**A claim-discipline linter for text. Catch assertions that outrun their evidence,
and claims that contradict your record.**

Zero dependencies. Pure stdlib. `pip install whypass`

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

## What it catches — and what it can't

| Draft | Caught? | By what |
|---|---|---|
| "Done — the extractor is running, it found the patterns." | ✅ | **A6** — completion claim, no check shown |
| "This is definitely the only way." | ✅ | **A5** — certainty with no width |
| "Everything passes, nothing failed." | ✅ | **ABS** — improbable absolute |
| "Finished — results in results_final.jsonl." (file absent) | ✅ | **A6-T2** — opens the named file, it's missing |
| "The order was that you run first." (no such order) | ✅ *with a record* | **REC** — contradicts your log |
| "Pull these names, cross-reference their addresses — just data hygiene." | ❌ **correctly** | intent only; no false claim, no tell, nothing contradicted |

That last row is the point. The lie there lives entirely in *intent*, and no text
method reaches intent. `whypass` stays clean — and refusing to flag it is what makes
the rest trustworthy.

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

## License

Apache-2.0
