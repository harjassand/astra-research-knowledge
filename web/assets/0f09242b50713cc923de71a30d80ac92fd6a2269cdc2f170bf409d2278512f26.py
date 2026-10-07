#!/usr/bin/env python3
"""Small exact qutrit identities; no SDE sampler or asymptotic simulation.

All output is confined to this owned directory.  The analytic general-N
proof is in QUDIT_STOPPED_DIFFUSION.txt; finite checks only check transcription.
"""
import itertools
import json
import pathlib
import time
from fractions import Fraction
import sympy as s

ROOT = pathlib.Path(__file__).resolve().parent
t0 = time.monotonic()
d = 3
I = s.eye(d)
zero = s.zeros(d)
R = s.Rational
sigma = s.diag(R(1, 2), R(1, 3), R(1, 6))
rho2 = sigma + s.Matrix([[0, R(1, 48), 0], [R(1, 48), 0, s.I/96], [0, -s.I/96, 0]])

def clean(a):
    return a.applyfunc(s.simplify)

def tensor(items):
    out = s.ones(1)
    for a in items:
        out = s.kronecker_product(out, a)
    return out

def kernel(rho, n):
    return tensor([rho] * n)

def dk(rho, n, v):
    out = s.zeros(d**n)
    for j in range(n):
        a = [rho] * n
        a[j] = v
        out += tensor(a)
    return out

def d2k(rho, n, v, w):
    out = s.zeros(d**n)
    for j in range(n):
        for k in range(n):
            if j == k:
                continue
            a = [rho] * n
            a[j], a[k] = v, w
            out += tensor(a)
    return out

def collective(f, n):
    out = s.zeros(d**n)
    for j in range(n):
        a = [I] * n
        a[j] = f
        out += tensor(a)
    return out

def vf(rho, f):
    return f*rho + rho*f - 2*s.trace(f*rho)*rho

def wf(rho, f):
    return -s.I*(f*rho-rho*f)

def dv(rho, f, direction):
    return f*direction + direction*f - 2*s.trace(f*direction)*rho - 2*s.trace(f*rho)*direction

def dw(f, direction):
    return -s.I*(f*direction-direction*f)

basis = []
grams = []
for i in range(d):
    for j in range(i+1, d):
        x, y = s.zeros(d), s.zeros(d)
        x[i, j] = x[j, i] = 1
        y[i, j], y[j, i] = -s.I, s.I
        basis.extend([x, y])
        grams.extend([s.Integer(2)]*2)
basis.extend([s.diag(1, -1, 0), s.diag(1, 1, -2)])
grams.extend([s.Integer(2), s.Integer(6)])
G = s.diag(*grams)
for i, b in enumerate(basis):
    for j, a in enumerate(basis):
        assert s.trace(a*b) == (grams[i] if i == j else 0)

# Completeness fixes the Casimir convention used in the critical-seed proof.
swap = s.zeros(d*d)
for i in range(d):
    for j in range(d):
        swap[j*d+i,i*d+j] = 1
assert clean(sum((s.kronecker_product(f,f)/g for f,g in zip(basis,grams)),s.zeros(d*d)) - swap + s.eye(d*d)/d) == s.zeros(d*d)
assert clean(sum((f*f/g for f,g in zip(basis,grams)),s.zeros(d)) - (d-R(1,d))*I) == s.zeros(d)
eta_star = s.diag(R(1,2),R(1,4),R(1,4))
for n in [1,2]:
    Q = sum((collective(f,n)**2/g for f,g in zip(basis,grams)),s.zeros(d**n))
    observed = s.trace(kernel(eta_star,n)*Q)
    asserted = n*n*(s.trace(eta_star**2)-R(1,d)) + n*(d-s.trace(eta_star**2))
    assert observed == asserted

axes = [basis[0], basis[3], basis[6], basis[0] + basis[7]/3]
identity_checks = 0
for rho in [sigma, rho2]:
    for n in [1, 2]:
        k = kernel(rho, n)
        for f in axes:
            t = collective(f, n)
            p = s.trace(f*rho)
            v, w = vf(rho, f), wf(rho, f)
            Bk = 2*n*p*k + dk(rho, n, v)
            Rk = dk(rho, n, w)
            B2k = (4*n*n*p*p + 2*n*s.trace(f*v))*k + 4*n*p*dk(rho,n,v) + d2k(rho,n,v,v) + dk(rho,n,dv(rho,f,v))
            R2k = d2k(rho,n,w,w) + dk(rho,n,dw(f,w))
            assert clean(t*k + k*t - Bk) == s.zeros(d**n)
            assert clean(t*k - k*t - s.I*Rk) == s.zeros(d**n)
            assert clean(B2k-R2k-2*(t*t*k+k*t*t)) == s.zeros(d**n)
            identity_checks += 3

def diffusion_form(rho, lambdas):
    vs = [vf(rho,f) for f in basis]
    ws = [wf(rho,f) for f in basis]
    V = s.Matrix([[s.trace(z*v) for v in vs] for z in basis])
    W = s.Matrix([[s.trace(z*w) for w in ws] for z in basis])
    coeff = s.diag(*[lam/g for lam,g in zip(lambdas,grams)])
    return clean(V*coeff*V.T-W*coeff*W.T)

def principal_psd(a):
    assert clean(a-a.H) == s.zeros(a.rows)
    count = 0
    smallest = None
    for k in range(1,a.rows+1):
        for inds in itertools.combinations(range(a.rows),k):
            val = s.factor(a.extract(inds,inds).det())
            assert val >= 0, (inds,val)
            count += 1
            smallest = val if smallest is None else min(smallest,val)
    return {'principal_minors':count,'smallest_minor':str(smallest)}

certs = []
for rho in [sigma,rho2]:
    assert principal_psd(rho-I/12)['principal_minors'] == 7
    D = diffusion_form(rho,[1]*8)
    K = s.zeros(8)
    for i,z in enumerate(basis):
        zc = z-s.trace(rho*z)*I
        for j,y in enumerate(basis):
            yc = y-s.trace(rho*y)*I
            K[i,j] = 4*s.trace(rho*zc*rho*yc)
    assert clean(D-K) == s.zeros(8)
    near = diffusion_form(rho,[1+R(i,7*288) for i in range(8)])
    # At the full s0/2 neighborhood of sigma, s0=1/6, epsilon=s0^2/8,
    # the analytic form bound is nu*s0^2/2=1/72 in HS norm.
    certs.append(principal_psd(near-G/72))

# The isotropic drift has a closed formula. Its positive factorization uses
# sqrt(rho) rather than a normalized-filter v field alone.
iso_logdet_checks = 0
for rho in [sigma,s.diag(R(1,2),R(1,4),R(1,4))]:
    root = s.diag(*[s.sqrt(rho[i,i]) for i in range(d)])
    p = s.trace(rho*rho)
    us = [root*f*root-s.trace(f*rho)*rho for f in basis]
    U = s.Matrix([[s.trace(z*u) for u in us] for z in basis])
    assert clean(diffusion_form(rho,[1]*8)-4*U*s.diag(*[1/g for g in grams])*U.T) == s.zeros(8)
    for n in [1,2,5]:
        from_general = sum(( (n*s.trace(f*rho)*vf(rho,f)+(dv(rho,f,vf(rho,f))-dw(f,wf(rho,f)))/4)/g for f,g in zip(basis,grams)),s.zeros(d))
        closed = 2*(n-1)*(rho*rho-p*rho)
        assert clean(from_general-closed) == s.zeros(d)
        inv = rho.inv()
        second = sum((s.trace(inv*u*inv*u)/g for u,g in zip(us,grams)))
        assert s.simplify(second-(d*d-2+d*p)) == 0
        logdrift = s.trace(inv*closed)-second
        assert s.simplify(logdrift-(2*n-d*d-d*(2*n-1)*p)) == 0
        variance = 2*sum((s.trace(inv*u)**2/g for u,g in zip(us,grams)))
        assert s.simplify(variance-2*d*d*(p-R(1,d))) == 0
        iso_logdet_checks += 4

# Exact normalized noncommuting local-field flow through second order.
field_checks = 0
h = basis[0] + basis[6]/3
for rho in [sigma,rho2]:
    f = s.trace(h*rho)
    g = s.trace(h*h*rho)
    first = (h*rho+rho*h)/2-f*rho
    second = (h*h*rho+2*h*rho*h+rho*h*h)/4 - f*(h*rho+rho*h) + (2*f*f-g)*rho
    assert clean(first-vf(rho,h)/2) == s.zeros(d)
    assert clean(second-dv(rho,h,first)/2) == s.zeros(d)
    field_checks += 2
Q2 = sum((collective(f,2)**2/g for f,g in zip(basis,grams)),s.zeros(d*d))
Th2 = collective(h,2)
assert clean(Q2*Th2-Th2*Q2) == s.zeros(d*d)
F2 = collective(basis[3],2)
anis = (Th2*F2+F2*Th2)/2
assert clean(Q2*anis-anis*Q2) == s.zeros(d*d)
field_checks += 2

# Self-contained qutrit critical-seed witness; log(1+x) alternating bound.
x = Fraction(1,8)
f_lower = (x*x/2-x*x*x/3)/2
assert f_lower == Fraction(11,3072)
beta = Fraction(3,2)
radius_sq = Fraction(1,1024)
diff = f_lower/beta-radius_sq
assert diff == Fraction(13,9216)
threshold = (Fraction(6,1)/diff).__ceil__()
assert threshold == 4254
outer_mass_lower = (diff/2)/(Fraction(2,3)-radius_sq)
assert outer_mass_lower == Fraction(13,12270)

out = {
 'status':'PASS_EXACT_FIXTURES_ONLY',
 'd':d,
 'product_kernel_matrix_identity_checks':identity_checks,
 'N_checked':[1,2],
 'Casimir_completeness_and_product_expectation':'EXACT_D3_N1_N2',
 'reference_states':2,
 'axes_checked':4,
 'KMS_diffusion_matrix_identity':'D_I(Z,Y)=4 Tr rho(Z-Tr(rho Z)I)rho(Y-Tr(rho Y)I)',
 'near_isotropic_PSD_certificates':certs,
 'isotropic_positive_factorization_and_logdet_checks':iso_logdet_checks,
 'noncommuting_local_field_derivative_and_centrality_checks':field_checks,
 'qutrit_spinodal_beta':'3/2',
 'critical_seed_free_energy_lower':str(f_lower),
 'centered_radius_sq':str(radius_sq),
 'outer_mass_lower_at_N_ge_4254':str(outer_mass_lower),
 'SDE_execution':False,
 'Brownian_or_apparatus_compiler':'UNIMPLEMENTED',
 'priority':'UNKNOWN',
 'wall_seconds':time.monotonic()-t0,
}
(ROOT/'qudit_diffusion_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
