"""Exploratory shared-baseline fit. Does not write immutable source files."""
from pathlib import Path
import sys, json, math
import numpy as np
from scipy.optimize import linprog

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'sources' / 'astra_pulse_observable'
sys.path.insert(0, str(SOURCE / 'code'))
from compact_model import make_problem, target

s, f, B, y, bounds, phi = make_problem(n=1600)
q = np.r_[target(s, 1000.), 0.]
bounds[-1] = (0, None)  # Retained witnesses must have physical positive L.
records = []
for denominator in [20, 30, 40, 60, 80, 100, 160]:
    delta = 2 * np.pi * .01 / denominator
    for amp in [50., 75., 100., 125., 150., 200.]:
        zp = 2 * amp / (1 + 1j * 2 * np.pi * f / delta)
        zm = amp / (1 + 1j * 2 * np.pi * f / (2 * delta))
        yp, ym = [np.r_[z.real, z.imag] for z in (zp, zm)]
        qp = 2 * amp * -np.expm1(-delta * 1000.)
        qm = amp * -np.expm1(-2 * delta * 1000.)
        # Fit both models at once, optionally putting the threshold between them.
        constraints = np.vstack([B, -B, B, -B])
        rhs = np.r_[y - yp, -y + yp, y - ym, -y + ym]
        constraints = np.column_stack([constraints, -np.ones(len(rhs))])
        extra = np.vstack([np.r_[q, 0.], np.r_[-q, 0.]])
        all_constraints = np.vstack([constraints, extra])
        all_rhs = np.r_[rhs, 195. - qm, -205. + qp]
        objective = np.r_[np.zeros(B.shape[1]), 1.]
        result = linprog(objective, A_ub=all_constraints, b_ub=all_rhs,
                         bounds=bounds + [(0, None)], method='highs-ds')
        if not result.success:
            continue
        err = result.x[-1]
        rec = {'n': 2, 'd': f'1/{denominator}', 'amp_mohm': amp,
               'joint_error_mohm': float(err),
               'baseline_q1000_mohm': float(q @ result.x[:-1]),
               'pair_q1000_mohm': [float(qm + q @ result.x[:-1]),
                                    float(qp + q @ result.x[:-1])],
               'nodes': s.tolist(), 'frequencies_hz': f.tolist(),
               'baseline_coefficients': result.x[:-1].tolist()}
        records.append(rec)
        print({k:v for k,v in rec.items() if k not in
               ('nodes','frequencies_hz','baseline_coefficients')}, flush=True)
records.sort(key=lambda z: z['joint_error_mohm'])
(HERE / 'joint_pair_candidates.json').write_text(json.dumps(records, indent=2))
