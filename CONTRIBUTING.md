# Contributing to whypass

whypass is small — around 500 lines, zero dependencies — and it is small on purpose. This file is
what we ask before you send code, and the rules we hold ourselves to before we merge it.

---

## How we take contributions

Pull requests on GitHub. No CLA. Sign-off on every commit is the whole agreement:

    git commit -s -m "your message"

The `-s` adds a `Signed-off-by:` line and asserts the **Developer Certificate of Origin** — that you
wrote the change or have the right to submit it under Apache-2.0. CI enforces it.

**One concern per PR.** If your change touches a rail's *behaviour* — what it catches, or what it
stops catching — open an issue first. The second half of that sentence is the part people skip, and
it is the part that matters most here.

---

## The two rules this tool cannot break without becoming worthless

**1. The detector must never be a model.** Every rail is a **regex or a filesystem check**, and this
is a design commitment, not a limitation we have not got around to. A detector that can be reasoned
with is a detector that can be talked out of its finding — and it would be the one thing this project
could not justify.

**2. It must not get cleverer about intent.** The README's honesty table has a row for a lie the tool
**correctly refuses to flag**, because that lie lives entirely in intent and no text method reaches
intent. That refusal is the product. If your change makes the tool flag it, your change is wrong even
if it looks like an improvement.

---

## The rules that were paid for

Each of these was learned by getting it wrong first.

### Measurement

- **Nothing at n=1 is a measurement.** Report the **median of ≥3 runs plus the call count**.
- **Make a checker fail once before you trust it.** A green that has never been red is a green you
  have not tested. Here that means: **a rail change needs a case that shows the rail going red**, and
  a case in the silenced-lies suite showing it going green.
- **State the kill criterion before you measure.** "This rail catches more" needs "and here is what
  would show it catches too much".

### Honesty

- **Say "unknown" when you do not know.** Absence of a visible cause is not evidence of no cause.
- **Retract in public.** If a number you published turns out to be wrong, correct it where you said
  it, not only in the next message.
- **Do not oversell the tool.** It is not a lie detector and it never will be. Every sentence added to
  the README should be one a sceptical reader could check.

### Files, hashes, ledgers

- **Sidecar `.md5` is the sole hash carrier.** A document body never carries its own hash — a check
  that verifies itself verifies nothing.
- **Tombstone, do not delete.** Where a record exists, mark a thing dead rather than erase it.
- **A release is traceable to a commit.** Tag before you publish; the version in the tree and the tag
  are the same claim stated twice.

### Failure modes

- **Fail open, loudly.** A linter that silently stops linting is indistinguishable from a clean draft.
  If a rail cannot decide, it must say so rather than staying quiet.
- **A finding carries its evidence.** Every finding prints the text that triggered it. A friction
  device that cannot be argued with is just noise — and readers are told to disagree out loud when a
  rail is wrong.
- **Never claim a check you have not run.** This one is the tool's own subject, so it is the least
  forgivable here: do not write "tests pass" in a PR description without the command and its output.

---

## Testing

    python -m pip install -e ".[dev]"
    pytest -q

Two suites, and they matter equally:

- `tests/test_whypass.py` — what the rails **catch**.
- the **silenced-lies suite** — what they must **not** catch. The README's honesty table is generated
  from it, so documentation and behaviour cannot drift apart.

CI runs both on Python 3.10–3.13, on Linux and macOS, with lint and type checks.

---

## What we will not take

- **A model.** See rule 1. Not as a fallback, not behind a flag, not "only when a rail is unsure".
- **A new dependency.** The tool has zero, and that is a feature: it drops into a pre-commit hook or
  an agent's pipeline without asking anything of the environment.
- **A rail that fires on intent.** See rule 2.
- **A silent behaviour change.** If a draft that produced no findings now produces some, that is a
  breaking change and it needs a note, a test, and a version.

---

## Register

Direct is welcome. Unkind is not. A tight correction is a gift.

And a note specific to this project: **a finding is an invitation, not a verdict.** If a rail fires on
something you think is fair, say so — with the text — and we will narrow the rail or record the case
in the silenced-lies suite. The tool is worth less if it cannot be argued with.

🖖
