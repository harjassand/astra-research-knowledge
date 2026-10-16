#!/usr/bin/env python3
"""Independent decimal CP obstructions and isolated-qubit compiler checks.
No author code imports, fits, measured-channel completion or hardware claim.
"""
from pathlib import Path
from decimal import Decimal
import csv, json, math, hashlib
import numpy as np

OUT = Path(__file__).resolve().parent
A = Path('/Users/harjas/Downloads/Dots/autonomous_correction_decision_2026-10-15')
chi = {}
for stem in ('Fig2b', 'Fig3e', 'Fig3f'):
    p = A / f'autonomous_correction_evaluator/QEC data/source_data/{stem}_chi_matrix.csv'
    b = p.read_bytes()
    lines = b.decode().splitlines()
    i = next(i for i,l in enumerate(lines) if l.startswith('basis_element,'))
    rows = {r['basis_element']: r for r in csv.DictReader(lines[i:])}
    a = {k: Decimal(v['chi_real']) for k,v in rows.items()}
    negatives = {k: str(a[k]) for k in ('II','XX','YY','ZZ') if a[k] < 0}
    asymmetry = max(abs(a[x+y] - a[y+x]) for x in 'IXYZ' for y in 'IXYZ')
    assert negatives and asymmetry > 0
    chi[stem] = {'source': str(p), 'sha256': hashlib.sha256(b).hexdigest(),
                 'exact_decimal_negative_diagonals': negatives,
                 'exact_decimal_max_real_asymmetry': str(asymmetry),
                 'fixed_central_real_parts_admit_CP_completion': False,
                 'statistical_or_physical_non_CP_claim': False}

I = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Z = np.diag([1.,-1.]).astype(complex)
Ps = [np.diag([1.,0.]), np.diag([0.,1.])]
def choi(ks):
    return sum(np.outer(k.reshape(-1), k.reshape(-1).conj()) for k in ks)
JD = choi(Ps)
JT = np.eye(4) / 2
def w(theta, eta):
    if eta == 0:
        return 1. if theta == 0 else 0.
    s2 = math.sin(theta)**2
    return eta*(2-eta) / (2*(eta + 2*(1-eta)*s2))
tests = []
for theta in (1e-4, 1e-3, .01, .1, .4, math.pi/4, 1.0):
    U = math.cos(theta)*I - 1j*math.sin(theta)*X
    JE = choi([U @ p for p in Ps])
    for eta in (.001, .01, .1, .5, 1.):
        J = (1-eta)*JE + eta*JT
        ww = w(theta, eta)
        ev = np.linalg.eigvalsh(J-ww*JD)
        assert ev.min() > -2e-14 and abs(ev.min()) < 2e-14
        assert np.linalg.eigvalsh(J-(ww+1e-6)*JD).min() < -1e-10
    s, c = abs(math.sin(theta)), abs(math.cos(theta))
    eta_star = min(1., 2*s/(c+s))
    w_star = 1/(c+s)**2 if s <= c else .5
    assert abs(w(theta, eta_star)-w_star) < 5e-15
    assert max(w(theta,j/10000) for j in range(1,10001)) <= w_star + 2e-14
    # Ideal output randomization with fresh equiprobable I/Z has no depolarizing
    # replacement. For this isolated known channel its exact pinching weight is c².
    Jtwirl = choi([U @ p/math.sqrt(2) for p in Ps] + [Z @ U @ p/math.sqrt(2) for p in Ps])
    Jexpected = c*c*JD + s*s*choi([X @ p for p in Ps])
    assert np.linalg.norm(Jtwirl-Jexpected) < 1e-14
    assert c*c >= w_star - 1e-14 if theta <= math.pi/4 else True
    tests.append({'theta_rad': theta, 'optimal_replacement_probability': eta_star,
                  'max_ideal_pinching_weight_with_uniform_replacement': w_star,
                  'uniform_replacement_fault_weight': 1-w_star,
                  'ideal_output_I_Z_twirl_pinching_weight': c*c,
                  'ideal_output_I_Z_twirl_fault_weight': s*s})
result = {'status': 'PASS', 'numpy_version': np.__version__,
          'central_chi_obstructions': chi,
          'isolated_qubit_floor_and_twirl': tests,
          'positive_and_negative_Choi_boundary_checks': 35,
          'analytic_formula': 'w=eta(2-eta)/(2[eta+2(1-eta)sin(theta)^2])',
          'limitations': 'Bath-independent unread single-qubit channel; ideal independently sampled output controls/replacement. No persistent bath, outcome instrument, actual calibration, independent slot selectors or hardware advantage inferred.'}
(OUT/'cp_floor_results.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'status':'PASS','central_CP_obstructions':len(chi),'Choi_boundary_checks':35,'compiler_comparisons':len(tests)},indent=2))
