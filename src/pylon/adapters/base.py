"""The contract every data source adapter implements.

Adding a game means adding a file here. If supporting a new source appears to
require changing ``graph/`` or ``rules/``, stop and write an ADR. That constraint
is the architecture test, and the Milestone 2 definition of done depends on it.
"""

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from pylon.rules.ast import Rule

__all__ = ["Adapter", "AdapterResult", "SourceMeta"]


@dataclass(frozen=True, slots=True)
class SourceMeta:
    """Provenance for everything one adapter run produces.

    Copied onto every row via ``ProvenanceMixin``. ``version`` must be a real
    commit sha or release tag, never "latest": attribution and reproducibility
    both depend on it.
    """

    source: str
    version: str
    license: str
    upstream_url: str


@dataclass(slots=True)
class AdapterResult:
    """What an adapter produces, before it touches the database.

    Deliberately plain data. Adapters are pure functions from source files to this
    structure, which makes them testable against a fixture without Postgres.
    """

    game_slug: str
    game_name: str
    meta: SourceMeta
    start_region: str

    regions: list[str] = field(default_factory=list)
    edges: list[tuple[str, str, str, Rule | None]] = field(default_factory=list)
    """(name, from_region, to_region, rule)."""

    locations: list[tuple[str, str, Rule | None]] = field(default_factory=list)
    """(name, region, rule)."""

    items: list[tuple[str, str]] = field(default_factory=list)
    """(name, classification)."""

    vanilla_placement: dict[str, str] = field(default_factory=dict)
    """location name -> item name. Empty when the source does not describe it."""

    rule_confidence: dict[str, float] = field(default_factory=dict)
    """Rule identifier -> confidence in [0, 1]. Absent means 1.0.

    Declarative sources are always 1.0. Archipelago rules recovered by black-box
    probing are lower, and the value is surfaced in API responses so a consumer
    can tell a verified rule from an approximate one. See ADR-003.
    """

    warnings: list[str] = field(default_factory=list)
    """Anything lossy or unresolved. ⚠️ Never swallow these. Ingest prints them,
    and a growing list is the signal that the canonical model needs an ADR."""


@runtime_checkable
class Adapter(Protocol):
    """Translate one upstream source into the canonical model."""

    name: str
    """Registry key, matching the CLI argument, e.g. ``"oot_json"``."""

    def fetch(self, destination: Any) -> SourceMeta:
        """Download or locate the source data, returning its pinned provenance.

        Must be safe to call repeatedly. Cache to disk under ``data/raw/``, which
        is gitignored.
        """
        ...

    def load(self, source_path: Any) -> AdapterResult:
        """Parse cached source data into the canonical shape.

        Pure: no network, no database. This is what unit tests exercise.
        """
        ...
