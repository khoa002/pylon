"""Tests for what the scaffold already provides. These must pass from commit one.

If any of these fail, the environment is wrong, not the code.
"""

import pylon
from pylon.adapters.base import Adapter, AdapterResult, SourceMeta
from pylon.config import Settings, get_settings
from pylon.models import Base, Entrance, Game, Item, ItemClassification, Location, Region
from pylon.rules.evaluator import CollectionState


def test_version_is_exposed():
    assert pylon.__version__


def test_settings_default_to_local_postgres():
    settings = Settings(_env_file=None)  # type: ignore[call-arg]
    assert "postgresql" in settings.database_url


def test_settings_read_the_environment(monkeypatch):
    monkeypatch.setenv("PYLON_LOG_LEVEL", "DEBUG")
    assert get_settings().log_level == "DEBUG"


def test_all_graph_tables_are_registered():
    """Guards against a model file that is never imported and so never migrated."""
    expected = {"games", "regions", "entrances", "locations", "items"}
    assert expected <= set(Base.metadata.tables)


def test_every_ingested_table_carries_provenance():
    """⚠️ Non-negotiable. Attribution obligations depend on these columns.

    ``games`` is exempt: it is an identity row, not ingested content.
    """
    required = {"source", "source_version", "license", "upstream_url", "ingested_at"}
    for model in (Region, Entrance, Location, Item):
        columns = set(model.__table__.columns.keys())
        assert required <= columns, f"{model.__name__} is missing provenance columns"

    assert "source" not in set(Game.__table__.columns.keys())


def test_item_classification_values():
    assert ItemClassification.PROGRESSION == "progression"


def test_collection_state_membership():
    state = CollectionState(items=frozenset({"Bow"}))
    assert state.has("Bow")
    assert not state.has("Hookshot")


def test_collection_state_counts():
    state = CollectionState(items=frozenset({"Key"}), counts={"Key": 5})
    assert state.has("Key", 5)
    assert not state.has("Key", 6)


def test_adapter_protocol_is_runtime_checkable():
    """Lets the registry validate an adapter at load time rather than at first use."""

    class Stub:
        name = "stub"

        def fetch(self, destination: object) -> SourceMeta:
            return SourceMeta("stub", "v0", "MIT", "https://example.invalid")

        def load(self, source_path: object) -> AdapterResult:
            return AdapterResult(
                game_slug="stub",
                game_name="Stub",
                meta=self.fetch(None),
                start_region="Start",
            )

    assert isinstance(Stub(), Adapter)
