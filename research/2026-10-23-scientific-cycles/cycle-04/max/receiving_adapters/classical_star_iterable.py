"""Receive one-shot edge iterables using the unchanged Pro2 comparator.

Only the Python iterable interface is repaired. Same chordal/PEO, row-energy,
action-noise and exact-arithmetic contracts; no new coloring or solver.
"""
from pathlib import Path
import importlib.util

_source = Path(__file__).resolve().parents[1] / "native/pro2/src/classical_star.py"
_spec = importlib.util.spec_from_file_location("_astra_cycle3_classical_star", _source)
_native = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_native)

def prepare(n, edges, t):
    return _native.prepare(n, tuple(edges), t)

recover = _native.recover
