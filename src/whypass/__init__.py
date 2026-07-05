"""whypass — a claim-discipline linter for text.

Not a lie detector — the science says intent is unreadable from text, and this tool
does not pretend otherwise. It catches two checkable things: assertions that outrun
their shown evidence, and claims that contradict your record.
"""
from .lint import Finding, grounded, lint
from .record import Record

__version__ = "0.1.0"
__all__ = ["lint", "Finding", "Record", "grounded", "__version__"]
