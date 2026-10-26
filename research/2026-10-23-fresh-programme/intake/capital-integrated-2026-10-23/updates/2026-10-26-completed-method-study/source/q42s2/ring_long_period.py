"""Follow up the active period bound in the first ring-isolation search."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
from architecture_search import phases_for, metrics
from thermal_network import response
from scipy.optimize import minimize_scalar
import numpy as np
import csv

rows = []
for P in [148.413159, 300., 1000., 3000., 10000.]:
    def loss(share):
        Y = response(phases_for('gated_ports_fixed_ring', share, P), np.ones(3)/3, 3)['Y']
        return -np.log(metrics(Y)[1])
    sol = minimize_scalar(loss, bounds=(.001, .999999), method='bounded',
                          options={'xatol': 1.e-12})
    out = response(phases_for('gated_ports_fixed_ring', sol.x, P), np.ones(3)/3, 3)
    excess, ratio, f, b = metrics(out['Y'])
    rows.append(dict(period=P, fixed_share=sol.x, isolation=ratio,
                     directional_excess=excess, forward=f, reverse=b))
with (ROOT/'ring_isolation_long_period.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(rows)
