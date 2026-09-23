"""whypass.record — the redundancy axis (the MMPI L-scale mechanism).

The L-scale catches lies NOT by reading intent but by checking a claim against
NORMATIVE data — what is actually supported. Single-turn footprints are blind to a
plainly-stated fabrication ("Illia ordered you to run first") because the words
carry no tell. But if you have a RECORD — a shared log, a ticket system, a
transcript — the claim can be checked against it WITHOUT reading intent: the record
either supports it or it doesn't.

This is not intent-detection. It is contradiction-against-ground-truth. Provide what
your record actually supports; the linter flags claims that outrun it.
"""

from __future__ import annotations

import re

_CLAIM_ORDER = re.compile(
    r"\b(order(?:ed)?|told (?:you|him|her|them)|instruct(?:ed)?)\b", re.IGNORECASE
)
_CLAIM_CONFIRM = re.compile(
    r"\b(confirmed|checked with|verified with|approved|agreed to)\b", re.IGNORECASE
)
_CLAIM_DONE = re.compile(
    r"\b(done|finished|completed|passed|compiles?|green|handled it|shipped)\b",
    re.IGNORECASE,
)


class Record:
    """The normative ground truth a claim gets checked against. Provide the facts
    your log actually supports; empty means 'nothing of this kind is supported'.

    orders        — directives that were actually given
    confirmations — approvals/checks that actually happened
    completed     — things that are actually finished
    """

    def __init__(self, orders=(), confirmations=(), completed=()):
        self.orders = list(orders)
        self.confirmations = list(confirmations)
        self.completed = list(completed)

    def check(self, text: str) -> list[str]:
        flags = []
        if _CLAIM_ORDER.search(text) and not self.orders:
            flags.append("claims an ORDER the record does not support")
        if _CLAIM_CONFIRM.search(text) and not self.confirmations:
            flags.append("claims a CONFIRMATION the record does not support")
        if _CLAIM_DONE.search(text) and not self.completed:
            flags.append("claims COMPLETION the record does not support")
        return flags
