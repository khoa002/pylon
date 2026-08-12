"""Alembic environment.

The database URL comes from ``pylon.config.Settings``, never from ``alembic.ini``.
That keeps one source of truth for connection details across the CLI, the app, and
migrations, and it means ``PYLON_DATABASE_URL`` works here too.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from pylon.config import get_settings
from pylon.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# Native Postgres ENUM changes are invisible to autogenerate; adding a value to
# ItemClassification needs a hand-written ALTER TYPE. See the M1 week 1 decision.
CONTEXT_OPTS = {
    "target_metadata": target_metadata,
    "compare_type": True,
    "compare_server_default": True,
}


def get_url() -> str:
    """Return the database URL from application settings."""
    return get_settings().database_url


def run_migrations_offline() -> None:
    """Emit SQL to stdout without connecting to a database."""
    context.configure(
        url=get_url(),
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **CONTEXT_OPTS,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live connection."""
    connectable = create_engine(get_url(), poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, **CONTEXT_OPTS)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
