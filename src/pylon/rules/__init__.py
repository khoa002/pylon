"""Rule expressions: AST, parser, evaluator.

A rule is a boolean expression over items, settings, macros, and reachability.
It is parsed once at ingest and stored as a serialized AST. It is never eval'd.
See docs/DECISIONS/ADR-003.
"""

from pylon.rules.ast import (
    And,
    CanReach,
    HasItem,
    Literal,
    Macro,
    Not,
    Or,
    Rule,
    Setting,
)
from pylon.rules.evaluator import CollectionState, evaluate, explain
from pylon.rules.parser import ParseError, parse

__all__ = [
    "And",
    "CanReach",
    "CollectionState",
    "HasItem",
    "Literal",
    "Macro",
    "Not",
    "Or",
    "ParseError",
    "Rule",
    "Setting",
    "evaluate",
    "explain",
    "parse",
]
