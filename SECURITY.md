# Security policy

whypass is small, offline and dependency-free, which removes most of the usual surface. What is left
is worth stating precisely, because one rail does something unusual.

**`A6-T2` reads files that a draft names.** That is the point of the rail — *"Finished, results in
`out.jsonl`"* should check whether `out.jsonl` is there. But it means **the linted text chooses which
paths the tool opens**, and if you run whypass on text from someone else, they influence what it
reads.

---

## Reporting a vulnerability

**Email:** [ihladkyi2@gmail.com](mailto:ihladkyi2@gmail.com) — please do not open a public issue for a
suspected vulnerability; a public report is a disclosure, not a report.

Include what you saw, the smallest input that shows it, the version, and whether you want credit or
anonymity. Acknowledgement within **7 days**, a first assessment within **30**, and coordinated
disclosure within **90** by default. We will not sue good-faith researchers. No bounty program.

---

## Scope

**In scope:**

- **Reading outside the intended tree.** A draft that names `../../etc/passwd`, an absolute path, or a
  symlink out of the working directory, causing whypass to read something it should not have. Note
  it is **read-only and never executes anything** — the question is what it *reads*, and what it then
  prints.
- **Information surfaced in findings.** A `MISSING`/present verdict that reveals a path's existence
  to someone who should not know it, when the draft came from an untrusted source.
- **Resource exhaustion from a crafted draft** — a pathological number of named artifacts, or a
  recursive symlink loop.
- **Any path where a *rail* could be made to do something other than match.** The rails are regexes
  and filesystem checks by design; a change that lets them execute something is a vulnerability and a
  design violation at once.

**Out of scope:**

- **A miss.** whypass not catching a claim is the tool working as designed in the general case —
  false negatives are published in the silenced-lies suite, with the tests that show them. A miss that
  is *not* in that suite is a documentation bug worth an issue, not a CVE.
- **A false positive you disagree with.** Say so with the text; that is the normal way this tool is
  argued with, and the README invites it.
- Anything requiring an already-compromised environment.
- Findings that need a model to demonstrate. See `CONTRIBUTING.md` rule 1.

---

## Secrets and private data

This repository ships code and tests only. It must never carry a credential, and a fixture that needs
one synthesises it at test time rather than committing it. The linted *content* is not stored
anywhere: whypass has no cache, no telemetry, no network access, and no state between runs.

---

## Thank you

Reports that arrive privately are doing us a favour, and we know it. 🖖
