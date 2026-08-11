"""Spec for the solver. Week 4.

The property that matters most is in ``test_required_steps_is_a_valid_topological_order``.
⭐ It is the same check the Milestone 3 route-validity scorer runs, which is why
agent output can be scored objectively with no judge model. See ADR-001.
"""

import pytest

from pylon.graph.solver import GraphView, can_reach, reachable_regions, required_steps
from pylon.rules.ast import And, HasItem, Or
from pylon.rules.evaluator import CollectionState

xfail_week4 = pytest.mark.xfail(
    raises=NotImplementedError, strict=True, reason="week 4: solver not implemented"
)


@pytest.fixture
def toy_graph() -> GraphView:
    """A three-region chain with one gated branch.

    Start -> Field (free)
    Field -> Cave  (needs Lantern)
    Field -> Peak  (needs Rope and (Boots or Wings))
    """
    return GraphView(
        game_slug="toy",
        start_region="Start",
        regions=frozenset({"Start", "Field", "Cave", "Peak"}),
        edges=(
            ("Start", "Field", None),
            ("Field", "Cave", HasItem("Lantern")),
            (
                "Field",
                "Peak",
                And((HasItem("Rope"), Or((HasItem("Boots"), HasItem("Wings"))))),
            ),
        ),
        locations={
            "Cave Chest": ("Cave", None),
            "Peak Summit": ("Peak", None),
            "Field Rupee": ("Field", None),
        },
        location_items={"Cave Chest": "Rope", "Field Rupee": "Lantern"},
        macros={},
    )


@xfail_week4
def test_start_region_is_always_reachable(toy_graph):
    assert "Start" in reachable_regions(toy_graph, CollectionState())


@xfail_week4
def test_unconditional_edge_is_followed(toy_graph):
    assert "Field" in reachable_regions(toy_graph, CollectionState())


@xfail_week4
def test_gated_edge_is_not_followed_without_the_item(toy_graph):
    assert "Cave" not in reachable_regions(toy_graph, CollectionState())


@xfail_week4
def test_gated_edge_is_followed_with_the_item(toy_graph):
    state = CollectionState(items=frozenset({"Lantern"}))
    assert "Cave" in reachable_regions(toy_graph, state)


@xfail_week4
def test_or_branch_satisfied_by_either_side(toy_graph):
    for alternative in ("Boots", "Wings"):
        state = CollectionState(items=frozenset({"Rope", alternative}))
        assert "Peak" in reachable_regions(toy_graph, state), alternative


@xfail_week4
def test_can_reach_accepts_a_location_name(toy_graph):
    state = CollectionState(items=frozenset({"Lantern"}))
    assert can_reach(toy_graph, state, "Cave Chest") is True


@xfail_week4
def test_required_steps_is_empty_when_already_reachable(toy_graph):
    assert required_steps(toy_graph, CollectionState(), "Field") == []


@xfail_week4
def test_required_steps_lists_the_missing_prerequisite(toy_graph):
    steps = required_steps(toy_graph, CollectionState(), "Cave Chest")
    assert [s.target for s in steps] == ["Lantern"]


@xfail_week4
def test_required_steps_is_a_valid_topological_order(toy_graph):
    """⭐ The core correctness property of the whole system.

    Replaying the steps in order, from the starting state, every step's own rule
    must already be satisfied by the time it is taken. This is the check the eval
    harness reuses to score agent output objectively.
    """
    state = CollectionState()
    steps = required_steps(toy_graph, state, "Peak Summit")
    accumulated = set(state.items)
    for step in steps:
        replay = CollectionState(items=frozenset(accumulated))
        assert can_reach(toy_graph, replay, step.target), (
            f"step {step.target!r} was not reachable when it was scheduled"
        )
        accumulated.add(step.target)
    assert can_reach(toy_graph, CollectionState(items=frozenset(accumulated)), "Peak Summit")


@xfail_week4
def test_cycles_do_not_hang(toy_graph):
    """CanReach makes evaluation mutually recursive. Guard it in the solver."""
    cyclic = GraphView(
        game_slug="cycle",
        start_region="A",
        regions=frozenset({"A", "B"}),
        edges=(("A", "B", None), ("B", "A", None)),
        locations={},
        location_items={},
        macros={},
    )
    assert reachable_regions(cyclic, CollectionState()) == frozenset({"A", "B"})
