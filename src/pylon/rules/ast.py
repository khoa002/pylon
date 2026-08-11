"""Rule AST node types.

Every adapter's job ends here: produce one of these trees. The solver and the
explanation surface consume nothing else.

Nodes are frozen dataclasses so they are hashable and safe to memoize on.
"""

from dataclasses import dataclass, field
from typing import Any

__all__ = [
    "And",
    "CanReach",
    "HasItem",
    "Literal",
    "Macro",
    "Not",
    "Or",
    "Rule",
    "to_dict",
]


@dataclass(frozen=True, slots=True)
class Literal:
    """A constant. ``Literal(True)`` means unconditional access."""

    value: bool


@dataclass(frozen=True, slots=True)
class HasItem:
    """True when the state holds at least ``count`` of ``name``."""

    name: str
    count: int = 1


@dataclass(frozen=True, slots=True)
class CanReach:
    """True when ``region`` is reachable from the current state.

    Mutually recursive with the solver: evaluating this calls back into
    reachability, which evaluates more rules. The solver is responsible for
    memoization and for cycle handling, not this module.
    """

    region: str


@dataclass(frozen=True, slots=True)
class Setting:
    """True when a world setting equals ``value``.

    OoT uses these heavily, e.g. ``open_kakariko == 'open'``.
    """

    name: str
    value: str | bool | int


@dataclass(frozen=True, slots=True)
class Macro:
    """A named helper defined by the source, e.g. ``can_play(Prelude_of_Light)``.

    Resolved at ingest where possible (OoT ``LogicHelpers.json``). Kept as a Macro
    node when the source does not define it, so an unresolved macro is visible in
    the data rather than silently dropped.
    """

    name: str
    args: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Not:
    """Negation."""

    operand: "Rule"


@dataclass(frozen=True, slots=True)
class And:
    """Conjunction. Empty ``operands`` is vacuously true."""

    operands: tuple["Rule", ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Or:
    """Disjunction. Empty ``operands`` is vacuously false."""

    operands: tuple["Rule", ...] = field(default_factory=tuple)


type Rule = Literal | HasItem | CanReach | Setting | Macro | Not | And | Or


def to_dict(rule: Rule) -> dict[str, Any]:
    """Serialize a rule to the JSONB shape stored on Entrance and Location.

    TODO(week 2): implement alongside ``from_dict``. Round-tripping is the
    property that matters; see the xfail test in tests/test_rules_ast.py.
    """
    raise NotImplementedError("week 2")
