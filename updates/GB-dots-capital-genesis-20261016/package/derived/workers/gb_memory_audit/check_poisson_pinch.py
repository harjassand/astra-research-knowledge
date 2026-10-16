#!/usr/bin/env python3
"""Independent Poisson-gap identity and actual shared-bath HISTORY effects.

The numerical calculation tracks genuine syndrome changes at every latent
Poisson full-pinch jump and exact endpoint. It never substitutes endpoint-only
syndrome flags. No source scripts are imported.
"""
import json
from pathlib import Path
import sympy as S
import numpy as np

x = S.symbols("x", positive=True)
u = S.symbols("u", nonnegative=True)
gap_average = S.simplify(2*S.exp(-x)*S.integrate(u*S.exp(x*u),(u,0,1)))
target = 2*(x-1+S.exp(-x))/x**2
assert S.simplify(gap_average-target) == 0
assert S.limit(target,x,0) == 1
coeffs = []
for n in range(7):
    # With n uniform ordered cuts, n+1 Dirichlet spacings:
    # E sum gap^2 / tau^2 = 2/(n+2).
    coeffs.append(str(S.Rational(2,n+2)))
series = S.series(target,x,0,7)
poisson_series = S.series(
    S.exp(-x)*sum(x**n/S.factorial(n)*S.Rational(2,n+2) for n in range(7)),
    x,0,7)
assert S.expand(series.removeO()-poisson_series.removeO()) == 0

eye = np.eye(2,dtype=complex)
X = np.array([[0,1],[1,0]],dtype=complex)
Z = np.diag([1,-1]).astype(complex)
def kron(*ms):
    out = np.ones((1,1),dtype=complex)
    for m in ms:
        out = np.kron(out,m)
    return out

dim = 8
qsize = dim*dim
blocks = 16
ident = np.eye(dim,dtype=complex)
zops = [kron(Z,eye,eye),kron(eye,Z,eye)]
projectors = [[(ident+(-1)**r*z)/2 for r in range(2)] for z in zops]
hops = [kron(X,eye,X),kron(eye,X,Z)]
baseline = np.zeros((dim,dim),complex)
assert np.linalg.norm(hops[0]@hops[1]+hops[1]@hops[0]) < 1e-14

# Bits: r_A,r_C,b_A,b_C.
def meas_adjoint(v,i,initialize=False):
    out = np.zeros_like(v)
    for old in range(blocks):
        old_r = (old>>i)&1
        old_b = (old>>(2+i))&1
        for new_r in range(2):
            new_b = 0 if initialize else (old_b or (new_r != old_r))
            new = old & ~(1<<i) & ~(1<<(2+i))
            new |= new_r<<i
            new |= int(new_b)<<(2+i)
            p = projectors[i][new_r]
            out[old] += p@v[new]@p
    return out

def generator_adjoint(v,active,strengths,rates):
    h = baseline+sum((strengths[i]*hops[i] for i in active),np.zeros((dim,dim),complex))
    out = 1j*(h@v-v@h)
    for i in active:
        out += rates[i]*(meas_adjoint(v,i)-v)
    return out

def evolve_adjoint(v,duration,active,strengths,rates):
    # Scaled Taylor action. With this finite small generator, 28 terms per
    # step and ||dt L|| <= 1/2 make the analytic truncation < 1e-35.
    norm_bound = 2*np.linalg.norm(baseline,2)+2*sum(strengths[i]+rates[i] for i in active)
    steps = max(1,int(np.ceil(2*duration*norm_bound)))
    dt = duration/steps
    for _ in range(steps):
        term = v.copy()
        total = v.copy()
        for order in range(1,29):
            term = (dt/order)*generator_adjoint(term,active,strengths,rates)
            total += term
        v = total
    return v

def final_effect(selected,kind="history"):
    out = np.zeros((blocks,dim,dim),dtype=complex)
    for block in range(blocks):
        offset = 2 if kind == "history" else 0
        if all((block>>(offset+i))&1 for i in selected):
            out[block] = ident
    return out

def effect(selected, strengths, rates, crossing_start,kind="history"):
    # Parents [0,1] and [d,1+d]. Measurements at all four endpoints.
    d = crossing_start
    v = final_effect(selected,kind)
    v = meas_adjoint(v,1)
    v = evolve_adjoint(v,d,[1],strengths,rates)
    v = meas_adjoint(v,0)
    v = evolve_adjoint(v,1-d,[0,1],strengths,rates)
    v = meas_adjoint(v,1,True)
    v = evolve_adjoint(v,d,[0],strengths,rates)
    v = meas_adjoint(v,0,True)
    e = v[0]
    assert np.linalg.norm(e-e.conjugate().T) < 1e-12
    return (e+e.conjugate().T)/2

def bare_generator_adjoint(v,active,strengths,rates):
    h = baseline+sum((strengths[i]*hops[i] for i in active),np.zeros((dim,dim),complex))
    out = 1j*(h@v-v@h)
    for i in active:
        out += rates[i]*(sum((p@v@p for p in projectors[i]),np.zeros_like(v))-v)
    return out

def bare_evolve(v,duration,active,strengths,rates):
    norm_bound = 2*np.linalg.norm(baseline,2)+2*sum(strengths[i]+rates[i] for i in active)
    steps = max(1,int(np.ceil(2*duration*norm_bound)))
    dt = duration/steps
    for _ in range(steps):
        term,total = v.copy(),v.copy()
        for order in range(1,29):
            term = dt/order*bare_generator_adjoint(term,active,strengths,rates)
            total += term
        v = total
    return v

def bare_endpoint_effect(selected,strengths,rates,d):
    v = ident.copy()
    for i in selected:
        v = projectors[i][1]@v
    v = bare_evolve(v,d,[1],strengths,rates)
    v = bare_evolve(v,1-d,[0,1],strengths,rates)
    v = bare_evolve(v,d,[0],strengths,rates)
    return v

records = []
cases = [([.2,.27],[.9,1.3],.25),([.17,.13],[4.,2.],.6),([.3,.25],[.01,.03],.4),([.23,.19],[1.1,.7],0.)]
initial = projectors[0][0]@projectors[1][0]
for case,(strengths,rates,d) in enumerate(cases):
    if case == 3:
        # Source-general case: each flip depends on the other parity, and
        # an arbitrary diagonal memory/bath baseline preserves both parities.
        by = np.array([[0,-1j],[1j,0]])
        hs = [kron(X,eye,X)+.3*kron(X,Z,by),kron(eye,X,Z)+.2*kron(Z,by,X)]
        hops = [h/np.linalg.norm(h,2) for h in hs]
        baseline = .17*kron(eye,eye,by)+.13*kron(Z,Z,X)
        for i in range(2):
            assert np.linalg.norm(hops[i]@zops[i]+zops[i]@hops[i]) < 1e-14
            assert np.linalg.norm(hops[i]@zops[1-i]-zops[1-i]@hops[i]) < 1e-14
            assert np.linalg.norm(baseline@zops[i]-zops[i]@baseline) < 1e-14
    ps = [2*j*j*(1/r-(1-np.exp(-r))/r**2) for j,r in zip(strengths,rates)]
    checks = []
    for subset in [[0],[1],[0,1]]:
        e = effect(subset,strengths,rates,d)
        eigs = np.linalg.eigvalsh(e)
        bound = float(np.prod([min(1,ps[i]) for i in subset]))
        slack = bound-float(eigs[-1])
        assert eigs[0] >= -2e-12
        assert slack >= -2e-12
        end = initial@effect(subset,strengths,rates,d,"endpoint")@initial
        bare = initial@bare_endpoint_effect(subset,strengths,rates,d)@initial
        equality_error = float(np.linalg.norm(end-bare,2))
        assert equality_error < 3e-12
        endpoint_max = float(np.linalg.eigvalsh(end)[-1])
        assert endpoint_max <= bound+2e-12
        assert np.linalg.eigvalsh(initial@e@initial-end)[0] >= -2e-12
        checks.append({"subset":subset,"max_history_effect_eigenvalue":float(eigs[-1]),"bound":bound,"history_slack":slack,"max_endpoint_effect_initial_plus_sector":endpoint_max,"history_dilation_vs_actual_lindblad_endpoint_error":equality_error})
    records.append({"strengths":strengths,"pinch_rates":rates,"source_gamma": [r/2 for r in rates],"crossing_offset":d,"conditional_parity_coupling_and_baseline":case == 3,"checks":checks})

result = {
    "exact_poisson_identity":"E sum gap^2 = 2 tau^2 (x-1+exp(-x))/x^2; x=lambda tau",
    "zero_rate_limit":"tau^2",
    "conditional_gap_coefficients_n_0_to_6":coeffs,
    "series":str(series),
    "numerical_scope":"Full-joint-input HISTORY effects plus initial-sector ENDPOINT effects. First three cases have crossing disjoint memory parents with anticommuting bath couplings; fourth has source-admissible parity-dependent interactions and a noncommuting syndrome-preserving baseline. Latent record dilation matches the actual bare Lindblad endpoint.",
    "models":records,
    "status":"PASS: exact gap identity, twelve full-input history bounds, twelve source endpoint-product bounds, and twelve latent-dilation/actual-generator endpoint equalities",
    "limitation":"Finite numerical stress test, not proof, lifetime benchmark, novelty, or device qualification.",
}
Path(__file__).with_name("poisson_pinch_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
