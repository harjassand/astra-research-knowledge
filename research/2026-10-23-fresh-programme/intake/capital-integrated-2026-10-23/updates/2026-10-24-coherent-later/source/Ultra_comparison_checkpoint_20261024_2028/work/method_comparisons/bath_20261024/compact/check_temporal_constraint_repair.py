#!/usr/bin/env python3
"""Focused regression for the post-review temporal-access phase-gain repair."""
import importlib.util
import json
from pathlib import Path

import numpy as np

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("revised", here/"native_multiport_check_revised.py")
revised = importlib.util.module_from_spec(spec)
spec.loader.exec_module(revised)

# A one-mode collector may only use the first temporal coordinate. The full
# covariance has correlations that previously sent the phase adjustment out
# of this allowed subspace.
metric = np.array([[2.0,0.3,0.4],[0.3,1.0,0.2],[0.4,0.2,3.0]])
predictor = np.array([0.4,0.6,0.2])
constraint = np.array([1.0,2.0,0.5])
basis = np.array([[1.0],[0.0],[0.0]])
target = 0.75
gain = revised.gaussian_feedback_gain(metric,predictor,basis,constraint,target)
projection_error = float(np.linalg.norm(gain-basis@(basis.T@gain)))
phase_error = float(constraint@gain-target)
assert projection_error < 1e-14
assert abs(phase_error) < 1e-14

# Show that the regression detects the frozen implementation's actual failure.
old_projected_wiener = basis@np.linalg.solve(basis.T@metric@basis,basis.T@predictor)
old_adjustment = np.linalg.solve(metric,constraint)
old_gain = old_projected_wiener+old_adjustment*(target-constraint@old_projected_wiener)/(constraint@old_adjustment)
old_leak = float(np.linalg.norm(old_gain-basis@(basis.T@old_gain)))
assert old_leak > 0.1

try:
    revised.gaussian_feedback_gain(metric,predictor,basis,np.array([0.0,1.0,0.0]),0.5)
except ValueError as exc:
    infeasible_message = str(exc)
else:
    raise AssertionError("Missing temporal phase direction was silently imported")

# A zero target with the same inaccessible constraint is feasible and needs
# no unavailable adjustment. A very small NONZERO projection remains real.
zero_gain = revised.gaussian_feedback_gain(metric,predictor,basis,np.array([0.0,1.0,0.0]),0.0)
tiny_gain = revised.gaussian_feedback_gain(metric,predictor,basis,np.array([1e-20,0.0,0.0]),1e-20)
assert abs(tiny_gain[0]-1.0) < 1e-14
assert np.all(zero_gain[1:] == 0)

# All recorded full-space fixed-phase gains are unchanged. Check the actual
# full-space optimum against its closed formula on this correlated fixture.
unconstrained = np.linalg.solve(metric,predictor)
adjustment = np.linalg.solve(metric,constraint)
expected = unconstrained+adjustment*(target-constraint@unconstrained)/(constraint@adjustment)
unrestricted = revised.gaussian_feedback_gain(metric,predictor,None,constraint,target)
assert np.max(np.abs(unrestricted-expected)) < 1e-14

# Exercise the public gate evaluator too, with two temporal bins per site.
# The available first-bin gain must be .8 to retain the actual ZZ phase;
# silently using the second bin would give a different residual covariance.
q, p = np.array([0.4,0.8]), np.array([0.2,0.1])
yp = np.zeros((4,8))
generators = np.zeros((2,8))
for k in range(2):
    yp[k,2*k+1] = 1
    yp[2+k,4+2*k+1] = 1
    generators[0,2*k+1] = q[k]
    generators[0,4+2*k] = -p[k]
    generators[1,4+2*k+1] = q[k]
    generators[1,2*k] = -p[k]
model = {"outputs":np.eye(8),"bins":2,"aligned_p":yp,"generator":generators,
         "q":q,"p":p,"raw_phase":-0.3,"phase_ideal":-0.3+float(q@p)}
gate = revised.evaluate(model,1.0,1.0,0.5,0.5,0.5,"wiener_fixed_phase",np.array([[1.0],[0.0]]))
assert abs(gate["theta"]-model["phase_ideal"]) < 1e-14
assert abs(gate["gain_norm2"]-0.64) < 1e-14
assert np.max(np.abs(np.array(gate["residual_phase_covariance"])-0.425*np.eye(2))) < 1e-14

result = {"restricted_gain":gain.tolist(),"projection_error":projection_error,
          "actual_phase_error":phase_error,"frozen_formula_subspace_leak":old_leak,
          "infeasible_constraint_rejected":infeasible_message,
          "tiny_nonzero_available_direction_retained":tiny_gain.tolist(),
          "full_space_gain_max_change":float(np.max(np.abs(unrestricted-expected))),
          "gate_evaluator_actual_theta":gate["theta"],
          "gate_evaluator_expected_theta":model["phase_ideal"],
          "gate_evaluator_gain_norm2":gate["gain_norm2"],
          "gate_evaluator_phase_covariance":gate["residual_phase_covariance"]}
(here/"TEMPORAL_CONSTRAINT_REPAIR_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
