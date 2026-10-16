"""Diagnostic only: finite minor-moment relaxation, never a gradient witness."""
import json
from pathlib import Path
import sys
import numpy as np

deps = Path('/Users/harjas/Documents/ChatGPT/ultra/research/2026-10-15-enabling-capability-v1/workers/measurement_search/deps')
sys.path.insert(0, str(deps))
from scipy.optimize import linprog

rng = np.random.default_rng(20261016)
points = [np.array([[8, 0, 0, 8]], dtype=int)]
for size in [100_000]:
    pts = rng.integers(-24, 33, (size, 4))
    points.append(pts)
grid = np.concatenate(points)
A = grid / 8
a,b,c,d = A.T
u = a*a+c*c
j = a*d-b*c
J = ((a-d)**2+(b+c)**2)**2/8+j*j+u*j
eq = np.array([np.ones_like(a),a,d,j])
fit = linprog(J, A_eq=eq, b_eq=[1,1,1,1], bounds=(0,None), method='highs')
idx = np.flatnonzero(fit.x > 1e-9)
out = {'diagnostic_only':True, 'symmetric_pairs':'(a,b,c,d) and (a,-b,-c,d)',
       'grid_denominator':8,'grid_numerators':grid[idx].tolist(),
       'pair_weights_float':fit.x[idx].tolist(), 'objective_float':float(fit.fun),
       'status':fit.message, 'points_examined':int(len(grid))}
Path(__file__).with_name('MOMENT_DISCOVERY.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
