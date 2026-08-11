"""Pylon CLI.

pylon ingest oot
pylon can-reach "Fire Temple Boss" --game oot --have Slingshot,Kokiri_Sword
pylon graph-stats --game oot
"""

import typer
from rich.console import Console

from pylon import __version__

app = typer.Typer(
    name="pylon",
    help="What do I need to do first? A prerequisite-graph engine for games.",
    no_args_is_help=True,
    add_completion=False,
)
console = Console()


@app.command()
def version() -> None:
    """Print the Pylon version."""
    console.print(f"pylon {__version__}")


@app.command()
def ingest(
    source: str = typer.Argument(..., help="Adapter name, e.g. 'oot'."),
    refresh: bool = typer.Option(False, help="Re-download instead of using the cache."),
) -> None:
    """Load a data source into the canonical graph.

    Must be idempotent: running it twice changes nothing.

    TODO(week 3): wire to the adapter registry.
    """
    raise NotImplementedError(f"week 3: no adapter registered for {source!r}")


@app.command(name="can-reach")
def can_reach(
    target: str = typer.Argument(..., help="Region or location name."),
    game: str = typer.Option("oot", help="Game slug."),
    have: str = typer.Option("", help="Comma-separated items you already hold."),
) -> None:
    """Answer whether a target is reachable, and if not, what is missing.

    TODO(week 4): load a GraphView, build a CollectionState from --have, call
    pylon.graph.required_steps, and render the result.
    """
    raise NotImplementedError("week 4")


@app.command(name="graph-stats")
def graph_stats(game: str = typer.Option("oot", help="Game slug.")) -> None:
    """Print node and edge counts for a loaded game.

    The cheapest sanity check that an adapter did something reasonable. Worth
    having early.

    TODO(week 3).
    """
    raise NotImplementedError("week 3")


if __name__ == "__main__":
    app()
