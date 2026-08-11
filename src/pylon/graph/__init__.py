"""The solver: reachability and ordering over the canonical graph.

Pure. No I/O, no ORM session, no network. Takes a loaded graph and a state,
returns answers. ⚠️ Must never import from ``pylon.adapters``. See ADR-002.
"""

from pylon.graph.solver import (
    GraphView,
    Step,
    can_reach,
    reachable_regions,
    required_steps,
)

__all__ = [
    "GraphView",
    "Step",
    "can_reach",
    "reachable_regions",
    "required_steps",
]
