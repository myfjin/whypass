"""whypass.grounding — does a passage CASH OUT in something checkable, or float as
eloquent essay? The anti-bullshit axis: bullshit is talk that does not cash out.

GROUNDED  = carries specifics that can be checked/acted on (numbers, file refs,
            code, named mechanisms, imperatives)
FLOATING  = leans on hedges, abstraction-nouns, essay-connectors with nothing under
mixed     = between

Deterministic; a companion signal to the footprints, not a verdict on truth.
"""

from __future__ import annotations

import re

_CONCRETE = [
    r"\d",
    r"[\w./-]+\.(?:py|jsonl?|md|txt|yaml|yml|toml|cfg|sh|rs|go|c|cpp|h)",
    r"[a-z_]{3,}\([^)]*\)",
    r"\b[a-z]+_[a-z_]+\b",
    (
        r"\b(build|ship|run|set|use|add|fix|deploy|store|write|read|merge|wire|cap|flag|"
        r"solve|factor|score|rank|compile|test|commit|open)\b"
    ),
]
_FLOAT = [
    r"\b(maybe|probably|perhaps|kind of|sort of|somehow|i guess|i think|i mean)\b",
    r"\b(essence|momentum|synergy|holistic|paradigm|the journey|the vision|the future)\b",
    r"\b(that means|in other words|the thing is|the real question|at the end of the day)\b",
    r"…|\.\.\.",
]


def _count(patterns, text):
    t = text.lower()
    return sum(len(re.findall(p, t)) for p in patterns)


def score(text: str) -> dict:
    c, f = _count(_CONCRETE, text or ""), _count(_FLOAT, text or "")
    g = c / (c + f) if (c + f) else 0.0
    verdict = (
        "GROUNDED" if (g >= 0.55 and c >= 2) else ("mixed" if g >= 0.40 else "FLOATING")
    )
    return {"concrete": c, "float": f, "groundedness": round(g, 2), "verdict": verdict}
