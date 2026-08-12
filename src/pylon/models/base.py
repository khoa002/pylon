"""Declarative base and the provenance mixin every ingested row must carry."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, MetaData, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
"""Deterministic names for constraints and indexes.

Without this, Postgres assigns its own names and a later migration cannot drop a
constraint it is unable to name. Explicit names already given in ``__table_args__``
win over the convention.
"""


class Base(DeclarativeBase):
    """Declarative base for all Pylon tables."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class ProvenanceMixin:
    """Where a row came from, and what that obligates us to.

    Non-negotiable on every ingested table. `docs/LICENSES.md` explains the
    obligations each ``license`` value carries. Attribution requirements are met
    by reading these columns, so they must be populated at ingest time, never
    backfilled.
    """

    source: Mapped[str] = mapped_column(String(64), index=True)
    """Adapter identifier, e.g. "oot_json", "archipelago"."""

    source_version: Mapped[str] = mapped_column(String(64))
    """Upstream version, commit sha, or release tag. Never "latest"."""

    license: Mapped[str] = mapped_column(String(64))
    """SPDX-ish identifier, e.g. "MIT", "CC-BY-4.0"."""

    upstream_url: Mapped[str] = mapped_column(String(512))
    """Direct link to the file or module this row was derived from."""

    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=func.now(),
    )
