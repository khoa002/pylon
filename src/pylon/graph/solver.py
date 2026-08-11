"""Reachability and prerequisite ordering.

This module is the answer to "what do I need to do first?". Everything else in
Pylon exists to feed it or to present its output.

⚠️ The LLM never enters this file. See ADR-001.
"""

from dataclasses import dataclass

from pylon.rules.ast import Rule
from pylon.rules.evaluator import CollectionState

__all__ = ["GraphView", "Step", "can_reach", "reachable_regions", "required_steps"]


@dataclass(frozen=True, slots=True)
class GraphView:
    """An in-memory, read-only projection of one game's graph.

    Loaded once from Postgres, then handed to the pure solver functions. Keeping
    the ORM out of the solver is what makes the solver testable without a database.
    """

    game_slug: str
    start_region: str
    regions: frozenset[str]
    edges: tuple[tuple[str, str, Rule | None], ...]
    """(from_region, to_region, rule)."""

    locations: dict[str, tuple[str, Rule | None]]
    """location name -> (region, rule)."""

    location_items: dict[str, str]
    """location name -> vanilla item name. Empty when placement is unknown."""

    macros: dict[str, Rule]
    """Source-defined helpers, already resolved to ASTs."""


@dataclass(frozen=True, slots=True)
class Step:
    """One prerequisite in an ordered answer."""

    target: str
    """What is obtained or reached."""

    rule: Rule | None
    """The rule that gated it."""

    reason: str
    """Human-readable rendering of ``rule``, for the CLI and API."""


def reachable_regions(graph: GraphView, state: CollectionState) -> frozenset[str]:
    """Fixed-point search for every region reachable from the start.

    TODO(week 4). Repeatedly relax edges until nothing new becomes reachable.
    ``CanReach`` nodes make rule evaluation mutually recursive with this function,
    so memoize per (region, state) and guard against cycles here rather than in
    the evaluator.
    """
    raise NotImplementedError("week 4")


def can_reach(graph: GraphView, state: CollectionState, target: str) -> bool:
    """True when ``target`` (a region or a location) is accessible right now.

    TODO(week 4).
    """
    raise NotImplementedError("week 4")


def required_steps(graph: GraphView, state: CollectionState, target: str) -> list[Step]:
    """Ordered prerequisites still missing before ``target`` is accessible.

    TODO(week 4). Empty list means the target is already reachable.

    Ordering must be a valid topological order: every step's own rule is satisfied
    by the starting state plus the steps before it. ⭐ That property is exactly
    what the Milestone 3 route-validity scorer checks, which is why it can be
    verified in pure Python with no judge model.
    """
    raise NotImplementedError("week 4")
