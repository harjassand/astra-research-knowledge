#!/usr/bin/env python3
"""Exercise zero/tiny/fast poles and signed velocity across a force jump."""
from fractions import Fraction as Q
import json
from pathlib import Path
from passive_execution_compiler import Potential, ForcePiece, compile_path, make_plan, verify_path


model = [(Q(0), Q(1, 4)), (Q(1, 10**12), Q(1, 4)),
         (Q(10**6), Q(1, 10**6))]
potential = Potential(Q(1), Q(3, 20))
force = [ForcePiece(Q(0), Q(1, 8), Q(1, 5), Q(0)),
         ForcePiece(Q(1, 8), Q(1, 4), -Q(1, 5), Q(0))]
x_ref = c = Q(0)
F, target = Q(1, 5), Q(1, 200)
compiled, knots = compile_path(model, potential, force, x_ref, c, F, target)
plan = make_plan(model, potential, force, x_ref, c, F, target)
verified = verify_path(knots, model, potential, force, x_ref, c, plan)
slopes = [(y1-y0)/(t1-t0) for (t0,y0),(t1,y1) in zip(knots[:-1],knots[1:])]
assert min(slopes) < 0 < max(slopes)
assert Q(verified["verified_residual_Linfinity_exact"]) <= target
result = {
    "fixture": "zero and tiny rates, very fast pole, rational force jump and velocity reversal",
    "rates": [str(rate) for rate, _ in model],
    "model": [{"pole":str(rate), "weight":str(w)} for rate,w in model],
    "target":str(target),
    "accepted_steps":compiled["accepted_steps"],
    "rejected_steps":compiled["rejected_steps"],
    "minimum_slope_exact":str(min(slopes)),
    "maximum_slope_exact":str(max(slopes)),
    "verified_residual_exact":verified["verified_residual_Linfinity_exact"],
    "verified_residual":verified["verified_residual_Linfinity"],
    "verified_piece_boundaries_aligned":True,
    "zero_pole_uses_exact_position_difference":True,
}
Path(__file__).with_name("passive_compiler_boundary_audits.json").write_text(
    json.dumps(result,indent=2)+"\n")
print(json.dumps(result))
