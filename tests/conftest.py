"""Shared fixtures.

Everything here is in-memory. Tests that need Postgres must be marked
``@pytest.mark.db`` so the pure-logic suite stays fast and runnable anywhere.
"""

import pytest

from pylon.rules.ast import And, CanReach, HasItem, Or, Rule
from pylon.rules.evaluator import CollectionState


@pytest.fixture
def empty_state() -> CollectionState:
    """A fresh save. Nothing collected."""
    return CollectionState()


@pytest.fixture
def child_start_state() -> CollectionState:
    """Roughly what you hold after leaving Kokiri Forest."""
    return CollectionState(
        items=frozenset({"Kokiri_Sword", "Deku_Shield", "Slingshot"}),
        settings={"open_forest": "closed", "shuffle_ocarinas": False},
    )


@pytest.fixture
def fire_temple_boss_rule() -> Rule:
    """The worked example from the README.

    ``Goron_Tunic and (Megaton_Hammer or can_use(Bow))``, with the macro already
    resolved to its expansion.
    """
    return And(
        (
            HasItem("Goron_Tunic"),
            Or((HasItem("Megaton_Hammer"), HasItem("Bow"))),
            CanReach("Fire Temple"),
        )
    )
