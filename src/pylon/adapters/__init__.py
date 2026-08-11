"""Adapters: the only place that knows about upstream data formats.

One file per source. Each one translates its source into the canonical model in
``pylon.models``. ``graph/`` and ``rules/`` never import from here. See ADR-002.

Registered adapters:

===============  =========  ============================================
name             license    status
===============  =========  ============================================
``oot_json``     MIT        week 3
``archipelago``  MIT        weeks 7 to 8
===============  =========  ============================================
"""

from pylon.adapters.base import Adapter, AdapterResult, SourceMeta

__all__ = ["Adapter", "AdapterResult", "SourceMeta"]
