"""Exact finite certificates for the rejected construction routes.

This checks particular witnesses and conservation, not full endotacticity
or the general Foster theorem. Run with Python 3; no dependencies.
"""
from fractions import Fraction as F
import json


def dot(u, v):
    return sum(a*b for a, b in zip(u, v))


def witness(reactions, direction):
    rows = []
    for source, target in reactions:
        delta = tuple(b-a for a, b in zip(source, target))
        rows.append({"source": source, "target": target,
                     "source_projection": dot(direction, source),
                     "reaction_projection": dot(direction, delta)})
    active = [r for r in rows if r["reaction_projection"] != 0]
    maximal = max(r["source_projection"] for r in active)
    violations = [r for r in active
                  if r["source_projection"] == maximal
                  and r["reaction_projection"] > 0]
    assert violations, "Claimed witness is not a violation"
    assert all(sum(source) <= 3 for source, _ in reactions)
    return {"direction": direction, "rows": rows,
            "maximal_active_projection": maximal,
            "violating_sources": [r["source"] for r in violations]}


cycle = [((2, 0, 0), (1, 0, 2)),
         ((1, 0, 2), (2, 1, 0)),
         ((2, 1, 0), (2, 0, 0))]
resource = (2, 0, 1)
increments = [dot(resource, tuple(b-a for a, b in zip(y, yp)))
              for y, yp in cycle]
assert increments == [0, 0, 0]

extra_yield = [((2, 0, 0), (1, 0, 3)),
               ((1, 0, 2), (2, 1, 0)),
               ((2, 1, 0), (2, 0, 0))]
token_switch = [((2, 0, 0), (0, 0, 3)),
                ((1, 0, 2), (2, 0, 1)),
                ((2, 0, 1), (2, 1, 0)),
                ((2, 1, 0), (2, 0, 1)),
                ((0, 3, 0), (0, 2, 0)),
                ((0, 0, 3), (0, 0, 2))]

result = {
    "cycle_resource": {"weight": resource, "increments": increments},
    "extra_yield": witness(extra_yield, tuple(map(F, (2, -1, 1)))),
    "token_switch": witness(token_switch, (F(3, 2), F(1), F(1))),
    "status": "PASS: exact rejection witnesses and cycle conservation only",
}
print(json.dumps(result, default=str, indent=2))
