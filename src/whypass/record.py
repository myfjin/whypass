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

# `order` is two different words wearing one spelling. "The order was that you run first"
# is a directive; "a second opinion on the order" is a sequence, and the bare-word match
# flagged ordinary prose (issue #5).
_ORDER_SEQUENCE = re.compile(
    r"\b(in order to|on the order of|the order of|order of magnitude|order by|in the order|"
    r"chronological order|alphabetical order)\b",
    re.IGNORECASE,
)
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

    @staticmethod
    def _supports(entries, text: str) -> bool:
        """Does any entry actually bear on this text?

        The rail used to ask only whether the list was **empty** — so any record at all
        silenced it, and an empty one flagged everything. Neither is a check: the first is
        useless, the second reads absence as denial (issue #7). This asks the real question.

        Content words are 3+ letters, no stopword list needed, because the threshold does the
        work: two words in common, or a majority of the shorter side. A short entry cannot
        share two words, so demanding two would mean short records could never support
        anything; a single shared word across two long passages is a coincidence.
        """
        words = set(re.findall(r"[a-z]{3,}", (text or "").lower()))
        for e in entries:
            other = set(re.findall(r"[a-z]{3,}", str(e).lower()))
            if not words or not other:
                continue
            shared = words & other
            if len(shared) >= 2 or len(shared) / min(len(words), len(other)) >= 0.5:
                return True
        return False

    def empty(self) -> bool:
        """True when this record asserts nothing at all — which is not the same as
        asserting that nothing happened."""
        return not (self.orders or self.confirmations or self.completed)

    def check(self, text: str) -> list[str]:
        # An EMPTY record is the natural thing to pass when you have no record yet, and it
        # used to mean 'the record denies everything' — so every completion claim in the
        # draft became a finding. Absence of a confirmation is not a denial (issue #7).
        # A caller with no record can pass `record=None`; a caller who passes an empty one
        # is not making a claim about the world, so there is nothing to contradict.
        if self.empty():
            return []

        flags = []
        # The wording matters as much as the firing. "does not support" reads as a
        # contradiction; the rail knows only that the record has nothing about this.
        # Silence, not denial — say so.
        if (
            _CLAIM_ORDER.search(text)
            and not _ORDER_SEQUENCE.search(text)
            and not self._supports(self.orders, text)
        ):
            flags.append("claims an ORDER the record does not show")
        if _CLAIM_CONFIRM.search(text) and not self._supports(self.confirmations, text):
            flags.append("claims a CONFIRMATION the record does not show")
        if _CLAIM_DONE.search(text) and not self._supports(self.completed, text):
            flags.append("claims COMPLETION the record does not show")
        return flags
