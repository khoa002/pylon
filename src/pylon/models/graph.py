"""Canonical graph tables: Game, Region, Entrance, Location, Item.

Shape modelled on the OoT Randomizer world format, which is the most declarative
of the sources. See docs/DECISIONS/ADR-002 and ADR-003.

Rules are stored as serialized ASTs in the ``rule`` JSON columns. They are never
stored as raw strings to be eval'd, and never as pickled callables.
"""

import enum
from typing import Any

from sqlalchemy import Enum, ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from pylon.models.base import Base, ProvenanceMixin


class ItemClassification(enum.StrEnum):
    """How much an item matters to progression.

    Mirrors Archipelago's classification, which is the most widely used vocabulary.
    ``PROGRESSION`` is the only one the solver cares about; the others are kept
    because they are cheap to carry and useful for explanation.
    """

    PROGRESSION = "progression"
    USEFUL = "useful"
    FILLER = "filler"
    TRAP = "trap"


class Game(Base):
    """A game. Not a catalog entry: we hold only what the graph needs."""

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))

    regions: Mapped[list["Region"]] = relationship(back_populates="game")
    items: Mapped[list["Item"]] = relationship(back_populates="game")


class Region(Base, ProvenanceMixin):
    """A logical area. Nodes of the graph."""

    __tablename__ = "regions"
    __table_args__ = (UniqueConstraint("game_id", "name", name="uq_region_game_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    is_start: Mapped[bool] = mapped_column(default=False)

    game: Mapped[Game] = relationship(back_populates="regions")
    locations: Mapped[list["Location"]] = relationship(back_populates="region")


class Entrance(Base, ProvenanceMixin):
    """A directed edge between two regions, optionally gated by a rule."""

    __tablename__ = "entrances"
    __table_args__ = (Index("ix_entrance_from_to", "from_region_id", "to_region_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    from_region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    to_region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"))
    name: Mapped[str] = mapped_column(String(255))

    rule: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
    """Serialized rule AST. ``None`` means unconditional."""

    rule_confidence: Mapped[float] = mapped_column(default=1.0)
    """1.0 for declaratively-sourced rules. Lower for probed Archipelago rules.

    Surfaced in API responses so a consumer can tell a verified rule from an
    approximate one. See ADR-003.
    """


class Location(Base, ProvenanceMixin):
    """A place where something can be obtained, gated by a rule."""

    __tablename__ = "locations"
    __table_args__ = (UniqueConstraint("game_id", "name", name="uq_location_game_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))

    rule: Mapped[dict[str, Any] | None] = mapped_column(JSONB, default=None)
    rule_confidence: Mapped[float] = mapped_column(default=1.0)

    vanilla_item_id: Mapped[int | None] = mapped_column(ForeignKey("items.id"), default=None)
    """What is here in an unmodified game. Null when the source only describes
    a randomized world and vanilla placement is unknown."""

    region: Mapped[Region] = relationship(back_populates="locations")


class Item(Base, ProvenanceMixin):
    """Something that can gate access."""

    __tablename__ = "items"
    __table_args__ = (UniqueConstraint("game_id", "name", name="uq_item_game_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    classification: Mapped[ItemClassification] = mapped_column(
        Enum(
            ItemClassification,
            name="itemclassification",
            # Without values_callable the native enum stores member *names*
            # ("PROGRESSION"), not the StrEnum values ("progression"). The lowercase
            # value is the documented vocabulary and what adapters and API payloads
            # carry, so a bulk insert of "progression" would otherwise be rejected
            # by the database.
            values_callable=lambda enum: [member.value for member in enum],
        ),
        default=ItemClassification.FILLER,
    )

    game: Mapped[Game] = relationship(back_populates="items")
