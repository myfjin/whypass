"""whypass.lint — the composed claim-discipline linter.

Two axes:
  ASSERTION  (stateless, zero-config): footprints + grounding + named-artifact check
  REDUNDANCY (needs a record): claims that contradict known ground truth

What it catches: assertions that outrun their shown evidence, and claims that
contradict your record. What it does NOT and CANNOT catch: intent. A calm request
whose only lie is its purpose carries no textual tell and no record contradiction —
no text method reaches it, and this one does not pretend to.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import artifacts, footprints, grounding
from .record import Record


@dataclass
class Finding:
    axis: str  # "assertion" | "redundancy"
    rail: str  # A4 | A5 | A6 | A6-T2 | ABS | REC
    message: str
    evidence: list = field(default_factory=list)


def lint(
    text: str, record: Record | None = None, workdir: str | None = None
) -> list[Finding]:
    """Lint a draft. Pass `record` to enable the redundancy axis; pass `workdir` to
    open named artifacts on disk."""
    out: list[Finding] = []

    if hits := footprints.status_over_function(text):
        out.append(Finding("assertion", "A4", footprints.A4_MSG, hits))
    if hits := footprints.over_determined(text):
        out.append(Finding("assertion", "A5", footprints.A5_MSG, hits))
    if hits := footprints.unchecked_claim(text):
        out.append(Finding("assertion", "A6", footprints.A6_MSG, hits))
    if hits := footprints.improbable_absolutes(text):
        out.append(Finding("assertion", "ABS", footprints.ABS_MSG, hits))

    if workdir is not None and artifacts.claims_completion(text):
        missing = [
            e["ref"] for e in artifacts.scan(text, workdir) if e["verdict"] == "MISSING"
        ]
        if missing:
            out.append(
                Finding(
                    "assertion",
                    "A6-T2",
                    "completion claimed but named artifact(s) do not exist: "
                    + ", ".join(missing),
                    missing,
                )
            )

    if record is not None and (flags := record.check(text)):
        out.append(Finding("redundancy", "REC", "; ".join(flags), flags))

    return out


def grounded(text: str) -> str:
    """Convenience: the grounding verdict for a passage (GROUNDED/mixed/FLOATING)."""
    return grounding.score(text)["verdict"]
