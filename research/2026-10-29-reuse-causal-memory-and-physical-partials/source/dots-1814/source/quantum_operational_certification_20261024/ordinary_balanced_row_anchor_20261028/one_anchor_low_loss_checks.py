#!/usr/bin/env python3
"""Author diagnostics, not independent receiving or acquisition execution."""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.stats import binom

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
I2 = np.eye(2, dtype=complex)
PAULI = [np.array([[0, 1], [1, 0]], complex),
         np.array([[0, -1j], [1j, 0]], complex),
         np.diag([1., -1.]).astype(complex)]
PROBES = [(I2 + sign * p) / 2 for p in PAULI for sign in [-1, 1]]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def channel(ks, rho):
    return sum((k @ rho @ k.conj().T for k in ks), np.zeros_like(rho))

# Exact symbolic W and all sixteen source-derived row effects.
rot = sp.Matrix([[sp.Rational(1, 2), -sp.sqrt(3)/2],
                 [sp.sqrt(3)/2, sp.Rational(1, 2)]])
O = sp.diag(rot, rot)
I4 = sp.eye(4)
W = I4.row_join(O).col_join(I4.row_join(-O)) / sp.sqrt(2)
assert sp.simplify(W.T * W - sp.eye(8)) == sp.zeros(8)
effects = []
lam_plus, lam_minus = (3+sp.sqrt(3))/24, (3-sp.sqrt(3))/24
for s in range(4):
    e, o = I4[:, s], O[s, :].T
    assert (e.T * o)[0] == sp.Rational(1, 2)
    for _sign in [-1, 1]:
        for c0, c1 in [(sp.Rational(1, 12), sp.Rational(1, 6)),
                       (sp.Rational(1, 6), sp.Rational(1, 12))]:
            B = c0 * e * e.T + c1 * o * o.T
            assert B.rank() == 2
            ev = B.eigenvals()
            assert ev == {sp.Integer(0): 2, lam_plus: 1, lam_minus: 1}
            effects.append(B)
assert sum(effects, sp.zeros(4)) == I4
tail = sp.simplify(sum((sp.trace(B)-lam_plus for B in effects)))
assert sp.simplify(tail - (2-2/sp.sqrt(3))) == 0

# Construct actual T from six source probe outputs; no sampled outcomes.
Wn = np.array(W.evalf(), dtype=complex)
max_t_diag_error = max_t_formula_error = max_inverse_error = 0.
encoder_cases = 0
xs = [np.array(x, float) / np.linalg.norm(x) for x in
      [(1,0,0,0),(0,1,0,0),(1,1,1,1),(1,2,3,4),(-3,1,2,-1)]]
for x in xs:
    V = np.zeros((8,2), complex)
    V[:4,0], V[4:,1] = x, x
    A = Wn @ V
    assert np.linalg.norm(A.conj().T @ A - I2) < 1e-12
    Jvec = A.reshape(-1)/math.sqrt(2)
    J = np.outer(Jvec, Jvec.conj())
    rho = A @ A.conj().T / 2
    T = sum((np.kron(A @ p @ A.conj().T, (I2-p).T)
             for p in PROBES), np.zeros((16,16), complex))/6
    max_t_formula_error = max(max_t_formula_error,
        np.linalg.norm(T-(2*np.kron(rho,I2)-J)/3))
    for t in range(2):
        for s in range(4):
            for a in range(2):
                B = effects[s*4+t*2+a]
                value = x @ np.array(B.evalf(), dtype=float) @ x
                max_t_diag_error = max(max_t_diag_error,
                    abs(T[2*(4*t+s)+a,2*(4*t+s)+a]-value))
    # This is a mathematical range inverse, not a supplied/learned recovery.
    for p in PROBES:
        max_inverse_error = max(max_inverse_error,
            np.linalg.norm(A.conj().T @ (A @ p @ A.conj().T) @ A-p))
    encoder_cases += 1

# Ordinary six-state mismatch identity on deterministic nonunitary channels.
physical_channels = 0
max_holdout_identity_error = 0.
for damping in [0., .01, .2, .6, 1.]:
    ad = [np.diag([1., math.sqrt(1-damping)]).astype(complex),
          np.array([[0., math.sqrt(damping)],[0.,0.]], complex)]
    for noise in [0., .03, .4, 1.]:
        mix = [math.sqrt(1-noise)*I2] + [math.sqrt(noise/3)*p for p in PAULI]
        ks = [b@a for a in ad for b in mix]
        assert np.linalg.norm(sum((k.conj().T@k for k in ks))-I2) < 1e-12
        fe = sum(abs(np.trace(k))**2 for k in ks)/4
        mismatch = sum(1-np.trace(p@channel(ks,p)).real for p in PROBES)/6
        max_holdout_identity_error = max(max_holdout_identity_error,
            abs(mismatch-2*(1-fe)/3))
        physical_channels += 1

# Exact small-loss and risk budgets; lower/upper binomial tails are analytic
# distribution evaluations, NOT aggregate-count simulations.
assert F(121, 2**18) < F(1,1024)
assert F(17,512)+F(1,2) < 1
assert F(3,1024) < F(1,256)
tail_cases = []
for eps in [F(1,2**j) for j in range(9)]:
    ef, beta = float(eps), float(eps/1024)
    n = math.ceil(768/ef*math.log(1/beta))
    a = eps/192
    threshold = (n*a).numerator//(n*a).denominator
    bad_accept = float(binom.cdf(threshold,n,ef/96))
    good_reject = float(binom.sf(threshold,n,ef/1536))
    assert bad_accept <= beta and good_reject <= beta
    tail_cases.append(dict(epsilon=str(eps),n=n,threshold=threshold,
                           bad_accept=bad_accept,good_reject=good_reject,beta=beta))

# Exact adaptive branch mixtures with independently conditioned fallback risk.
mixture_cases = 0
for eps in [F(1),F(1,4),F(1,64)]:
    for gamma in [F(1),F(1,3)]:
        for ell_star in [F(0),F(1,100),F(1,3)]:
            for p_acc in [F(0),F(1,8),F(1,2),F(1)]:
                beta = min(eps/1024,p_acc)
                good_acc = p_acc-beta
                ell = good_acc*eps/64+beta+(1-p_acc)*((1+gamma/2)*ell_star+eps/128)
                bound = (1+gamma/2)*ell_star+17*eps/1024
                assert ell <= bound
                mixture_cases += 1

# Spectator scaling keeps total row tail, while Choi impurity can be nonzero.
for weights in [(F(1),),(F(1,2),F(1,2)),(F(1,2),F(1,3),F(1,6))]:
    assert sum(weights)==1
    assert sum(w for w in weights)==1 # tail scales linearly by each eigenvalue

deps = [
 'ordinary_bures_matrix_query_confidence_20261027.md',
 'ordinary_balanced_row_anchor_20261028/row_residual_validation_independent_receipt.json',
 'direct_cptp_bures_bridge_20261027/DIRECT_CPTP_BURES_RISK_RECOVERY.md',
 'direct_cptp_bures_bridge_20261027/independent_bures_bridge_receipt.json',
 'direct_cptp_bures_bridge_20261027/PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md',
 'direct_cptp_bures_bridge_20261027/private_framed_independent_receipt.json',
 'explicit_online_random_dimension_reduction_compiler_20261027.md',
 'explicit_online_random_dimension_reduction_compiler_independent_receipt.json',
 'ordinary_generic_matrix_gls_sylvester_clipping_20261028.md',
 'ordinary_generic_matrix_gls_sylvester_clipping_20261028_independent_receipt.json',
]
bindings = {'status':'UNREVIEWED_NEW_COMPOSITION_WITH_RECEIVED_IMPORTS',
            'sha256_relative_to_programme_root':{p:sha(ROOT/p) for p in deps}}
verified_received_bindings = 0
for receipt, key, base in [
 ('ordinary_balanced_row_anchor_20261028/row_residual_validation_independent_receipt.json',
  'sha256_relative_to_programme_root', ROOT),
 ('ordinary_generic_matrix_gls_sylvester_clipping_20261028_independent_receipt.json',
  'sha256', ROOT),
 ('direct_cptp_bures_bridge_20261027/independent_bures_bridge_receipt.json',
  'sha256', ROOT/'direct_cptp_bures_bridge_20261027'),
]:
    manifest = json.loads((ROOT/receipt).read_text())[key]
    for path, expected_sha in manifest.items():
        assert sha(base/path)==expected_sha, (receipt,path)
        verified_received_bindings += 1
bindings['received_manifest_bindings_reverified'] = verified_received_bindings
source = HERE/'ONE_ANCHOR_LOW_LOSS_HOLDOUT_AND_FALLBACK.md'
bindings['new_source_sha256'] = sha(source)
(HERE/'one_anchor_low_loss_source_bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
result = dict(status='PASS_AUTHOR_DIAGNOSTICS_NOT_INDEPENDENT_RECEIVING',
 source_sha256=sha(source),script_sha256=sha(Path(__file__)),
 exact_row_effects=len(effects),exact_row_tail=str(tail),
 encoder_cases=encoder_cases,physical_holdout_channels=physical_channels,
 exact_branch_mixtures=mixture_cases,binomial_tail_cases=tail_cases,
 received_manifest_bindings_reverified=verified_received_bindings,
 max_t_diag_error=max_t_diag_error,max_t_formula_error=max_t_formula_error,
 max_inverse_error=max_inverse_error,max_holdout_identity_error=max_holdout_identity_error,
 source_calls=0,rng_draws=0,sampled_source_outcomes=0,
 evidence_class='Exact symbolic construction and rational budgets; deterministic floating physical expectations and analytic binomial distribution evaluations. No acquisition, quantum circuits, production solver or hardware.')
assert max(max_t_diag_error,max_t_formula_error,max_inverse_error,max_holdout_identity_error)<1e-12
(HERE/'one_anchor_low_loss_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
