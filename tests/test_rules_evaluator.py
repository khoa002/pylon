"""Spec for rule evaluation. Week 2.

``xfail(strict=True)`` until implemented. Deleting the marker is part of the
commit that makes each one pass.
"""

import pytest

from pylon.rules.ast import And, CanReach, HasItem, Literal, Not, Or, Setting
from pylon.rules.evaluator import CollectionState, evaluate, explain

xfail_week2 = pytest.mark.xfail(
    raises=NotImplementedError, strict=True, reason="week 2: evaluator not implemented"
)


@xfail_week2
def test_none_rule_is_unconditional(empty_state):
    """A null rule column means no gate at all. This must never be False."""
    assert evaluate(None, empty_state) is True


@xfail_week2
def test_literal(empty_state):
    assert evaluate(Literal(True), empty_state) is True
    assert evaluate(Literal(False), empty_state) is False


@xfail_week2
def test_has_item(child_start_state):
    assert evaluate(HasItem("Kokiri_Sword"), child_start_state) is True
    assert evaluate(HasItem("Megaton_Hammer"), child_start_state) is False


@xfail_week2
def test_has_item_with_count():
    state = CollectionState(items=frozenset({"Heart_Container"}), counts={"Heart_Container": 3})
    assert evaluate(HasItem("Heart_Container", 3), state) is True
    assert evaluate(HasItem("Heart_Container", 4), state) is False


@xfail_week2
def test_and_or_not(child_start_state):
    assert evaluate(And((HasItem("Kokiri_Sword"), HasItem("Slingshot"))), child_start_state) is True
    assert evaluate(And((HasItem("Kokiri_Sword"), HasItem("Bow"))), child_start_state) is False
    assert evaluate(Or((HasItem("Bow"), HasItem("Slingshot"))), child_start_state) is True
    assert evaluate(Not(HasItem("Bow")), child_start_state) is True


@xfail_week2
def test_empty_and_is_true_empty_or_is_false(empty_state):
    """Standard identities. Adapters emit empty nodes when a source has no gate."""
    assert evaluate(And(()), empty_state) is True
    assert evaluate(Or(()), empty_state) is False


@xfail_week2
def test_setting(child_start_state):
    assert evaluate(Setting("open_forest", "closed"), child_start_state) is True
    assert evaluate(Setting("open_forest", "open"), child_start_state) is False


@xfail_week2
def test_can_reach_delegates_to_injected_callable(empty_state):
    """The solver owns reachability. The evaluator must not try to compute it."""
    calls: list[str] = []

    def fake_can_reach(region: str) -> bool:
        calls.append(region)
        return region == "Fire Temple"

    assert evaluate(CanReach("Fire Temple"), empty_state, can_reach=fake_can_reach) is True
    assert evaluate(CanReach("Water Temple"), empty_state, can_reach=fake_can_reach) is False
    assert calls == ["Fire Temple", "Water Temple"]


@xfail_week2
def test_explain_returns_only_the_failing_leaves(child_start_state, fire_temple_boss_rule):
    """Powers "here is what is stopping you". Satisfied terms must not appear."""
    failing = explain(fire_temple_boss_rule, child_start_state, can_reach=lambda _: True)
    assert HasItem("Goron_Tunic") in failing
    assert HasItem("Kokiri_Sword") not in failing


@xfail_week2
def test_explain_returns_empty_when_rule_passes(child_start_state):
    assert explain(HasItem("Kokiri_Sword"), child_start_state) == []
