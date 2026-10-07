#!/usr/bin/env python3
"""Finite diagnostics for the loss-robust heralding obstruction.

These checks are not a proof of the quantified complexity theorem.
Standard-library exact checks are supplemented by SymPy and NumPy diagnostics.
Run from the package root: python tests/verify_obstruction.py
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from math import comb, factorial, ceil, log2
from pathlib import Path
import json
import random
import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
SEED = 20261007
rng = random.Random(SEED)
counts: dict[str, int] = {}

def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    counts[name] = counts.get(name, 0) + 1

# Binomial domination, valid beyond binary target counts as well.
for k in range(9):
    for loss in range(31):
        check('binomial_domination', comb(k + loss, k) <= (k + 1) ** loss)

# Exact contamination bound on finitely supported input photon distributions.
# Its proof in PROOF.md covers arbitrary countable support and quantum blocks.
max_ratio = F(0)
for modes in (1, 2, 3):
    occupations = list(product(range(5), repeat=modes))
    for _ in range(80):
        k = tuple(rng.randrange(2) for _ in range(modes))
        weights = {n: rng.randrange(1, 100) for n in occupations}
        z = sum(weights.values())
        p0 = F(weights[k], z)
        gain = F(1, 2 ** rng.randrange(2, 8))
        eta = F(1, rng.randrange(2, 100))
        a = (1 - eta) * gain * gain
        bad = F(0)
        lost_moment = F(0)
        for n, w in weights.items():
            if any(n_i < k_i for n_i, k_i in zip(n, k)) or n == k:
                continue
            ell = tuple(n_i - k_i for n_i, k_i in zip(n, k))
            coefficient = 1
            for n_i, k_i in zip(n, k):
                coefficient *= comb(n_i, k_i)
            term = F(w, z) * coefficient * a ** sum(ell)
            bad += term
            lost_moment += sum(ell) * term
        ratio = bad / p0
        bound = 2 * gain * gain / p0
        check('exact_contamination_bound', ratio <= bound)
        check('exact_bad_mixture_weight', bad / (p0 + bad) <= bound)
        check('exact_conditional_excess_energy', lost_moment / (p0 + bad) <= bound)
        max_ratio = max(max_ratio, ratio / bound)

# Exact tight first-order example: a target one-photon branch and a two-photon
# contaminant with orthogonal output labels. Bound necessarily depends on p0.
p0, gain, eta = F(1, 100), F(1, 1000), F(1, 7)
a = (1 - eta) * gain * gain
w = 2 * a * (1 - p0) / (p0 + 2 * a * (1 - p0))
check('two_branch_contamination_identity', w == F(594, 3500594))

# Full Kraus calculation for an entangled herald-output state, compared against
# the block formula. The output is a two-dimensional reference; no assumption
# of classical input blocks is made.
rng_np = np.random.default_rng(SEED)
max_kraus_residual = 0.0
for _ in range(100):
    cutoff, outdim = 4, 2
    herald_modes = 2
    occ = list(product(range(cutoff), repeat=herald_modes))
    vec = rng_np.normal(size=(len(occ), outdim)) + 1j*rng_np.normal(size=(len(occ), outdim))
    vec /= np.linalg.norm(vec)
    eta = float(rng_np.uniform(0.01, 0.8))
    gain = float(rng_np.uniform(0.01, 0.3))
    k = tuple(int(x) for x in rng_np.integers(0, 2, size=herald_modes))
    filtered = vec * np.array([gain**sum(n) for n in occ])[:, None]
    norm = float(np.sum(np.abs(filtered)**2))
    filtered /= np.sqrt(norm)
    psi = filtered.reshape(-1)
    rho = np.outer(psi, psi.conj())
    kraus = []
    for ell in range(cutoff):
        K = np.zeros((cutoff, cutoff))
        for n in range(ell, cutoff):
            K[n-ell,n] = np.sqrt(comb(n,ell)*(1-eta)**ell*eta**(n-ell))
        kraus.append(K)
    joint_out = np.zeros_like(rho)
    for l1, l2 in product(range(cutoff), repeat=2):
        K = np.kron(np.kron(kraus[l1], kraus[l2]), np.eye(outdim))
        joint_out += K@rho@K.conj().T
    ki = occ.index(k)
    direct = joint_out[ki*outdim:(ki+1)*outdim,ki*outdim:(ki+1)*outdim]
    formula = np.zeros((outdim,outdim), complex)
    for ni,n in enumerate(occ):
        if any(x<y for x,y in zip(n,k)):
            continue
        ell = tuple(x-y for x,y in zip(n,k))
        coeff = eta**sum(k)*(1-eta)**sum(ell)*gain**(2*sum(n))
        for n_i,k_i in zip(n,k):
            coeff *= comb(n_i,k_i)
        formula += coeff*np.outer(vec[ni],vec[ni].conj())/norm
    res = float(np.max(np.abs(direct-formula)))
    max_kraus_residual = max(max_kraus_residual,res)
    check('full_kraus_block_formula', res < 1e-12)
    target = np.outer(vec[ki],vec[ki].conj())
    p = float(np.trace(target).real)
    target /= p
    posterior = direct / np.trace(direct)
    distance = float(np.sum(np.abs(np.linalg.eigvalsh(posterior-target)))/2)
    check('quantum_conditional_trace_bound', distance <= 2*gain*gain/p+1e-11)

# Inherited KLM primitive, independently checked symbolically.
# A contraction on target+one-photon ancilla has a passive unitary dilation.
s = sp.sqrt(2)
A = sp.Matrix([[1-s, 2**sp.Rational(-1,4)], [2**sp.Rational(-1,4), sp.Rational(1,2)]])
for n, expected in enumerate([sp.Rational(1,2), sp.Rational(1,2), -sp.Rational(1,2)]):
    amp = A[1,1]*A[0,0]**n
    if n:
        amp += n*A[0,1]*A[1,0]*A[0,0]**(n-1)
    check('exact_KLM_NS_amplitudes', sp.simplify(amp-expected)==0)
check('exact_KLM_contraction_eigenvalue_1', sp.simplify((A-sp.eye(2)).det())==0)
other = sp.Rational(1,2)-s
check('exact_KLM_other_eigenvalue', sp.simplify(A.det()-other)==0)
check('exact_KLM_contraction_range', bool(other>-1) and bool(other<1))

# Two-mode Hadamard action in the {|20>,|11>,|02>} sector.
H2 = sp.Matrix([[sp.Rational(1,2),1/s,sp.Rational(1,2)],
                [1/s,0,-1/s],
                [sp.Rational(1,2),-1/s,sp.Rational(1,2)]])
NS = sp.diag(-1,1,-1) / 4
v11 = sp.Matrix([0,1,0])
check('exact_KLM_CZ_two_photon', sp.simplify(H2.T*NS*H2*v11+v11/4)==sp.zeros(3,1))
check('exact_KLM_Hadamard_unitarity', H2.T*H2==sp.eye(3))

# Fan-out does not clone arbitrary quantum states: it copies the computational
# basis bit. Its count decoder has a constant decision gap after uniform loss.
readout_cases = []
for R in [2,3,4,10,20,50,100,1000]:
    eta = F(1,R)
    survival = 1-(1-eta)**R
    gap = survival/F(6)-F(3,100)
    check('exact_constant_readout_gap', gap > F(3,40))
    readout_cases.append({'R':R,'survival_probability':float(survival),
                          'gap_after_three_percent_error':float(gap)})

# Schur certificate for uniform loss, evaluated exactly for rational squeezing
# singular values beta=tanh(r). Each mode contributes two quadratures.
for eta in [F(1,10),F(1,20),F(1,100),F(1,1000)]:
    for gain in [F(1,4),F(1,8),F(1,32),F(1,1024)]:
        for beta in [gain/4,gain/2,gain]:
            n = beta*beta/(1-beta*beta)
            m = beta/(1-beta*beta)
            c = 1/(1-eta)
            phi = eta**3*((n+m+c)*(n+m)**2+(n-m+c)*(n-m)**2)
            check('exact_uniform_loss_Phi_bound', 0 <= phi <= 8*eta**3*gain*gain)
            check('exact_energy_bound', eta*n <= 2*eta*gain*gain)

# Rational balanced bunchers: the first row is 1/sqrt(R), with R=4^k.
# Input |1,...,1> has probability R!/R^R of placing all photons in port 0.
bunching_cases = []
for R in [4, 16]:
    root = int(R**0.5)
    W = [[F((-1)**((i & j).bit_count()), root) for j in range(R)] for i in range(R)]
    for i in range(R):
        for j in range(R):
            check('exact_buncher_unitarity', sum(W[i][k]*W[j][k] for k in range(R)) == int(i==j))
    bunch_prob = F(factorial(R), R**R)
    check('exact_buncher_probability', F(factorial(R))*W[0][0]**(2*R)==bunch_prob)
    check('exact_buncher_lower_bound', bunch_prob >= F(1,R**R))
    eta=F(1,R)
    probs=[F(comb(R,k))*eta**k*(1-eta)**(R-k) for k in range(R+1)]
    check('exact_bunched_loss_normalization', sum(probs)==1)
    check('exact_bunched_loss_mean', sum(k*v for k,v in enumerate(probs))==1)
    bunching_cases.append({'R':R,'bunching_success_probability':float(bunch_prob),
                           'ideal_two_mode_mean_after_loss':1})

# Explicit finite-bit accounting fixture. Not a generated PP-complete instance.
# Source rounding is performed BEFORE the diagonal filter, so its precision
# is charged to p_* rather than to the much smaller final herald probability.
R,h,q,d = 256,1000,4096,4096
ell = max(R, (q+11)//2, 2)
source_precision_b = max(d+q+ceil(log2(12800*d)), ceil(log2(16*d)))
final_entry_bits_bound = source_precision_b+2*ell+4
# p0' >= p_*/2. Z_g <= 1. This is a LOWER bound on herald success.
log_w_inv_upper = h*ceil(log2(R))+2*ell*h+q+1
check('polynomial_precision_schedule', source_precision_b > d+q)
check('structured_filter_error_budget', F(4,2**(2*ell-q)) < F(1,100))
check('structured_source_rounding_budget', F(32*d,2**(source_precision_b-d-q)) <= F(1,400))
check('structured_small_norm_budget', F(2*d,2**source_precision_b) <= F(1,8))

summary = {
    'status':'Finite diagnostics only; no formal proof or external validation.',
    'seed':SEED,
    'assertion_counts':counts,
    'total_assertions':sum(counts.values()),
    'max_contamination_to_bound_ratio':float(max_ratio),
    'max_full_kraus_residual':max_kraus_residual,
    'readout_cases':readout_cases,
    'bunching_cases':bunching_cases,
    'precision_accounting_fixture':{
        'R':R,'herald_total_h':h,'source_probability_exponent_q':q,
        'physical_modes_d':d,'filter_exponent_ell':ell,
        'log2_inverse_herald_lower_bound_upper':log_w_inv_upper,
        'source_dyadic_precision_b':source_precision_b,
        'final_entry_bits_conservative':final_entry_bits_bound,
        'note':'Accounting fixture, not an emitted universal circuit or empirical runtime.'
    },
    'not_executed':['General PostBQP-to-Gaussian circuit compiler',
                    'PP-complete computational benchmark',
                    'Full certified optical parameter compiler',
                    'Formal proof kernel or external review']
}
(ROOT/'VERIFICATION.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
