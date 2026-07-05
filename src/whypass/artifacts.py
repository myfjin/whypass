"""whypass.artifacts — the assertion axis, tier 2: OPEN what a draft NAMES.

Tier-1 footprints read the claim WORDS; tier-2 opens what the words name. When a
draft claims completion AND names a checkable artifact, look: does it exist on this
filesystem? A completion claim behind a MISSING file is the catch that evidence-
words can't talk away.

READ-ONLY. Never executes anything on its own — a linter that runs whatever filename
a draft mentions is an injection vector. Local claims only: paths outside the given
workdir tree are UNCHECKED, never MISSING.
"""
from __future__ import annotations

import re
from pathlib import Path

_EXTS = "py|jsonl|json|md|txt|yaml|yml|toml|cfg|sh|rs|go|c|cpp|h|csv|db|log"
_PATH = re.compile(rf"(?:\./|/)?[\w][\w./-]*\.(?:{_EXTS})\b")
_COMPLETION = re.compile(
    r"\b(built|saved|wrote|written|created|shipped|deployed|verified|confirmed|"
    r"fixed|done|finished|compiles?|results? (?:in|are)|tests?\s+pass|self-?tests?)\b", re.I)


def claims_completion(text: str) -> bool:
    return bool(text and _COMPLETION.search(text))


def scan(text: str, workdir: str | Path = ".") -> list[dict]:
    """Every artifact the draft names, opened read-only. workdir bounds the tree we
    are willing to call MISSING (outside it → UNCHECKED)."""
    if not text:
        return []
    root = Path(workdir).resolve()
    out, seen = [], set()
    for tok in _PATH.findall(text):
        tok = tok.rstrip(".")
        if tok in seen:
            continue
        seen.add(tok)
        p = (root / tok) if not tok.startswith("/") else Path(tok)
        if p.exists():
            st = p.stat()
            out.append({"ref": tok, "verdict": "EXISTS", "detail": f"{st.st_size} bytes"})
        elif tok.startswith("/") and root not in p.parents:
            out.append({"ref": tok, "verdict": "UNCHECKED",
                        "detail": "absolute path outside workdir — not opened"})
        else:
            out.append({"ref": tok, "verdict": "MISSING", "detail": "named but not found"})
    return out
