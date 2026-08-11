"""Pure evaluation of rule ASTs against a collection state.

Pure and side-effect free, so results can be memoized. Reachability calls this
very heavily, so it is on the hot path.
"""

from collections.abc import Callable
from dataclasses import dataclass, field

from pylon.rules.ast import Rule

__all__ = ["CollectionState", "evaluate", "explain"]


@dataclass(frozen=True, slots=True)
class CollectionState:
    """What the player currently has.

    ⚠️ Assumes monotonic accumulation: you never lose an item. That assumption
    breaks on OoT's child/adult time travel, which is the first real stress test
    of the canonical model. See the open question in docs/STATE.md, and write an
    ADR before week 3 rather than patching around it here.
    """

    items: frozenset[str] = frozenset()
    counts: dict[str, int] = field(default_factory=dict)
    settings: dict[str, str | bool | int] = field(default_factory=dict)

    def has(self, name: str, count: int = 1) -> bool:
        """True when the state holds at least ``count`` of ``name``."""
        if count <= 1:
            return name in self.items
        return self.counts.get(name, 1 if name in self.items else 0) >= count


def evaluate(
    rule: Rule | None,
    state: CollectionState,
    *,
    can_reach: Callable[[str], bool] | None = None,
    macros: dict[str, Rule] | None = None,
) -> bool:
    """Evaluate a rule against a state.

    TODO(week 2). ``None`` means unconditional and must return True.

    ``can_reach`` is injected by the solver rather than imported, so this module
    stays pure and the solver keeps ownership of memoization and cycle handling.

    See tests/test_rules_evaluator.py for the cases that define correct behaviour.
    """
    raise NotImplementedError("week 2")


def explain(
    rule: Rule | None,
    state: CollectionState,
    *,
    can_reach: Callable[[str], bool] | None = None,
    macros: dict[str, Rule] | None = None,
) -> list[Rule]:
    """Return the leaf terms that are currently false.

    This is what powers "here is the rule that gates this step", which is a
    product requirement rather than a nicety. Walking the AST makes it cheap,
    which is the main argument for ADR-003.

    TODO(week 2), after ``evaluate``.
    """
    raise NotImplementedError("week 2")
