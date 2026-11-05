#!/usr/bin/env python3
"""Numerical checks of the backward boundary construction.

These floating-point checks are illustrations, not interval arithmetic proofs.
The report supplies the analytic proof and an exact-rational certificate method.
"""
from itertools import combinations
from pathlib import Path
import json
import math
from fractions import Fraction
from exact_certificate import certify_restricted_lower_bound, certify_all_row_residuals, dyadic_scaled_matrix, positive_definite_integer
import numpy as np
from scipy.optimize import brentq

OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(44302026)

def bump_grad(z):
    s = float(z @ z)
    if s >= 1:
        return np.zeros_like(z)
    e = np.zeros_like(z); e[0] = 1
    return e * (1-s)**3 - 6*z[0]*(1-s)**2*z

def bump_hessian(z):
    s = float(z @ z)
    if s >= 1:
        return np.zeros((len(z), len(z)))
    e = np.zeros_like(z); e[0] = 1
    return (-6*(1-s)**2*(np.outer(e,z)+np.outer(z,e)+z[0]*np.eye(len(z)))
            +24*z[0]*(1-s)*np.outer(z,z))

def restricted_sigma(A, k):
    best = float('inf'); support = None
    for S in combinations(range(A.shape[1]), k):
        v = np.linalg.svd(A[:,S], compute_uv=False)[-1]
        if v < best:
            best = float(v); support = S
    return best, support

def fit_rows(A, Y, s):
    d = A.shape[1]
    coeff = np.zeros((d,d))
    residual = np.full(d, np.inf)
    supports = list(combinations(range(d), s))
    # Candidate supports are shared across output rows. Fit every row at once.
    for S in supports:
        C, *_ = np.linalg.lstsq(A[:,S], Y, rcond=None)
        rr = np.linalg.norm(A[:,S] @ C - Y, axis=0)
        improve = rr < residual
        for i in np.flatnonzero(improve):
            coeff[i,:] = 0
            coeff[i,list(S)] = C[:,i]
        residual[improve] = rr[improve]
    return coeff, residual

# Analytic maximum on the piecewise low-radius Hessian branch.
sstar = (15 - 2*np.sqrt(30))/35
max_hessian_analytic = 6*np.sqrt(sstar)*(1-sstar)*(3-7*sstar)
observed = 0.0
for dim in [1, 2, 7, 20]:
    for _ in range(1000):
        z = rng.normal(size=dim); z /= np.linalg.norm(z)
        z *= rng.uniform()
        observed = max(observed, float(np.max(np.abs(np.linalg.eigvalsh(bump_hessian(z))))))
# Along the symmetry axis, the equilibrium displacement solves u+a*psi'(u)=0.
a = 1/8
u_star = brentq(lambda u: u+a*(1-u*u)**2*(1-7*u*u), -0.5, 0)
epsilon = 1e-3
radius = 25*epsilon
bump = {
    'analytic_hessian_sup': float(max_hessian_analytic),
    'sampled_hessian_sup': observed,
    'certified_hessian_upper': 4,
    'chosen_amplitude': a,
    'normalized_center_displacement': abs(u_star),
    'displacement_over_epsilon': abs(u_star)*radius/epsilon,
    'proven_displacement_over_epsilon_lower': 25/12,
    'hessian_lower_bound': 0.5,
    'hessian_upper_bound': 1.5,
}
assert max_hessian_analytic < 4
assert abs(u_star)*radius > 2*epsilon

# A symmetric ring is an unknown sparse physical network with degree 3,
# including its diagonal. Ten controls read all sixteen positions each time.
d, s, q = 16, 3, 10
K = np.diag(rng.uniform(1.8, 2.2, size=d))
for i in range(d):
    j = (i+1) % d
    K[i,j] = K[j,i] = -rng.uniform(0.12,0.22)
eigs = np.linalg.eigvalsh(K)
m, L = float(eigs[0]), float(eigs[-1])
H = rng.normal(size=(d,q))
X = np.linalg.solve(K,H)
A = X.T/np.sqrt(q)
Y = H.T/np.sqrt(q)
alpha, support = restricted_sigma(A, 2*s)
Kexact, rexact = fit_rows(A,Y,s)
assert np.max(np.abs(Kexact-K)) < 1e-9

nu = 1e-6
E = rng.uniform(-nu,nu,size=X.shape)
Ahat = (X+E).T/np.sqrt(q)
alphahat, supporthat = restricted_sigma(Ahat,2*s)
Kraw, rfit = fit_rows(Ahat,Y,s)
eta = nu*np.sqrt(s)*L
row_error_bound = 2*eta/alphahat
B = Kraw.copy()
B[np.abs(B) <= row_error_bound] = 0
Ktilde = (B+B.T)/2
Delta = 2*s*row_error_bound
actual_spectral = float(np.linalg.norm(Ktilde-K,2))
actual_operator = float(np.linalg.norm(np.linalg.inv(Ktilde)-np.linalg.inv(K),2))
response_bound = Delta/(m*(m-Delta))
true_row_residual = float(np.max(np.linalg.norm(Ahat@K.T-Y,axis=0)))
assert np.max(rfit) <= eta*(1+1e-5)
assert true_row_residual <= eta
assert np.max(np.linalg.norm(Kraw-K,axis=1)) <= row_error_bound
assert np.all(np.abs(Ktilde[K==0]) < 1e-14)
assert actual_spectral <= Delta
assert np.linalg.eigvalsh(Ktilde)[0] > 0
assert actual_operator <= response_bound

# Repeated identical controls deliberately fail restricted injectivity.
Abad = np.repeat(X[:,0:1],q,axis=1).T/np.sqrt(q)
badalpha, _ = restricted_sigma(Abad,2*s)
network = {
    'dimension':d, 'nonzeros_per_row':s, 'experiments':q,
    'scalar_state_outputs':d*q,
    'm':m, 'L':L,
    'restricted_certificate_supports':math.comb(d,2*s),
    'row_fit_supports_per_row':math.comb(d,s),
    'alpha_float':alpha, 'alpha_noisy_float':alphahat,
    'worst_support':support, 'worst_noisy_support':supporthat,
    'exact_max_entry_error':float(np.max(np.abs(Kexact-K))),
    'coordinate_noise_bound':nu, 'eta_bound':eta,
    'true_max_residual':true_row_residual,
    'fit_max_residual':float(np.max(rfit)),
    'row_error_bound':row_error_bound,
    'actual_max_row_error':float(np.max(np.linalg.norm(Kraw-K,axis=1))),
    'spectral_error_bound':Delta, 'actual_spectral_error':actual_spectral,
    'response_operator_error_bound':response_bound,
    'actual_response_operator_error':actual_operator,
    'bad_design_alpha_float':badalpha,
    'svd_estimate_is_used_as_formal_certificate':False,
}
Ki,Kden = dyadic_scaled_matrix(K)
assert positive_definite_integer([[Ki[i][j]-(3*Kden//2 if i==j else 0) for j in range(d)] for i in range(d)])
assert positive_definite_integer([[(5*Kden//2 if i==j else 0)-Ki[i][j] for j in range(d)] for i in range(d)])
exact_alpha = certify_restricted_lower_bound(X+E, 2*s)
eta2 = Fraction(3)*Fraction(5,2)**2*Fraction(1,1000000)**2
exact_fit = certify_all_row_residuals(Kraw,X+E,H,eta2)
exact_true = certify_all_row_residuals(K,X+E,H,eta2)
assert exact_alpha['passed'] and exact_fit['passed'] and exact_true['passed']
network['exact_dyadic_restricted_certificate'] = exact_alpha
network['exact_rational_fit_residual_certificate'] = exact_fit
network['exact_rational_true_residual_check_simulation_only'] = exact_true
network['certified_L_used_for_residual_budget'] = 2.5
network['exact_certificate_response_bound_using_m_1p5_L_2p5'] = float((12*np.sqrt(3)*2.5*1e-6*64)/(1.5*(1.5-12*np.sqrt(3)*2.5*1e-6*64)))
tau2 = 4*eta2*64**2
Bf = [[Fraction(float(Kraw[i,j])) if Fraction(float(Kraw[i,j]))**2 > tau2 else Fraction(0) for j in range(d)] for i in range(d)]
Kout = [[(Bf[i][j]+Bf[j][i])/2 for j in range(d)] for i in range(d)]
assert all(float(Bf[i][j]) == B[i,j] for i in range(d) for j in range(d))
artifact = {'dimension':d,'sparsity':s,'experiments':q,'state_hex':[[float(v).hex() for v in row] for row in X+E], 'control_hex':[[float(v).hex() for v in row] for row in H], 'raw_coefficients_hex':[[float(v).hex() for v in row] for row in Kraw], 'alpha_lower':'1/64', 'eta_squared':str(eta2),'m_assumption':'3/2','L_assumption':'5/2','output_stiffness_rational':[[str(v) for v in row] for row in Kout]}
(OUT/'certified_network.json').write_text(json.dumps(artifact,indent=2)+'\n')
network['m_1p5_L_2p5_exact_simulation_check'] = True
network['threshold_and_symmetrization_are_exact_in_artifact'] = True
result = {'bump':bump,'network':network}
(OUT/'verification_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
