"""Stress the original comparator's full constant-SPD-capacity hypothesis.

These nonlocal storage matrices are mathematical cases, not assumed ordinary
lumped heat capacities. The new positivity/support theorem does not cover them.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent/'stage1'))
from thermal_network import Phase, laplacian, response, contrast_basis, symmetric
import numpy as np
import csv

rng = np.random.default_rng(202610264202)
rows = []
for case in range(64):
    n = [3, 4][case % 2]
    m = [2, 3, 5][case % 3]
    Q = np.linalg.qr(rng.normal(size=(m, m)))[0]
    eigs = np.exp(rng.uniform(-2., 2., m))
    C = (Q*eigs)@Q.T
    N = n+m
    order = rng.permutation(N)
    phases = []
    for k in range(1, N):
        i, j = int(order[k]), int(order[int(rng.integers(k))])
        phases.append(Phase(float(rng.uniform(.1, 1.)),
            laplacian(N, [(i, j, float(rng.uniform(.2, 2.)))])))
    rng.shuffle(phases)
    out = response(phases, C, n, 64)
    back = response(list(reversed(phases)), C, n)
    U = contrast_basis(n)
    Y, Ybar = U.T@out['Y']@U, U.T@out['Ybar']@U
    circle = symmetric(Y)-Y.T@np.linalg.solve(Ybar, Y)
    scale = max(np.linalg.norm(Ybar), 1.)
    off = out['Y']-np.diag(np.diag(out['Y']))
    row = dict(case=case, ports=n, internal=m, capacity_condition=eigs.max()/eigs.min(),
        gap_identity_relative_error=np.linalg.norm(out['Ybar']-symmetric(out['Y'])-out['gap_integral'])/scale,
        reversal_relative_error=np.linalg.norm(out['Y']-back['Y'].T)/scale,
        min_dominance_eigenvalue=np.linalg.eigvalsh(Ybar-symmetric(Y))[0],
        min_circle_eigenvalue=np.linalg.eigvalsh(symmetric(circle))[0],
        largest_off_diagonal_response=np.max(off))
    rows.append(row)
    assert row['gap_identity_relative_error'] < 2.e-9
    assert row['reversal_relative_error'] < 2.e-9
    assert row['min_dominance_eigenvalue'] > -2.e-10
    assert row['min_circle_eigenvalue'] > -2.e-10
    if row['largest_off_diagonal_response'] > 1.e-7 and not (ROOT/'nonlocal_capacity_example.npz').exists():
        np.savez(ROOT/'nonlocal_capacity_example.npz', capacity=C, **out)
with (ROOT/'matrix_capacity_checks.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
report = (f'Constant nonlocal SPD storage cases: {len(rows)}\n'
    f'Max gap relative error: {max(r["gap_identity_relative_error"] for r in rows):.16g}\n'
    f'Max reversal relative error: {max(r["reversal_relative_error"] for r in rows):.16g}\n'
    f'Min circle eigenvalue: {min(r["min_circle_eigenvalue"] for r in rows):.16g}\n'
    f'Cases with positive off-diagonal response >1e-7: '
    f'{sum(r["largest_off_diagonal_response"] > 1.e-7 for r in rows)}\n')
(ROOT/'MATRIX_CAPACITY_RESULTS.txt').write_text(report)
print(report)
