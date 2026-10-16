"""Deterministic finite diagnostics for this audit, never hardware evidence.

Run with the bundled Python that supplies numpy. No downloaded code executes.
The proofs in ACQUISITION_IDENTIFICATION_PROOFS.md establish general claims;
these diagnostics check explicit witnesses, conventions and displayed costs.
"""
from pathlib import Path
import itertools
import json
import math
import numpy as np

OUT = Path(__file__).resolve().parent
I = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.diag([1, -1]).astype(complex)
PAULI = [I, X, Y, Z]


def projector(v):
    return np.outer(v, v.conj())


def evolve(h, t):
    w, v = np.linalg.eigh(h)
    return (v * np.exp(-1j * t * w)) @ v.conj().T


def opnorm(a):
    return float(np.linalg.norm(a, 2))


def trace_distance(a, b):
    return float(np.abs(np.linalg.eigvalsh(a - b)).sum() / 2)


def partial_trace_b(rho):
    return np.trace(rho.reshape(2, 2, 2, 2), axis1=1, axis2=3)


records = {}

# Supplied finite constant-pulse obstruction, recomputed without source code.
phi = np.array([1, 0, 0, 1], dtype=complex) / math.sqrt(2)
p = projector(phi)
hc = (np.kron(Z, I) + np.kron(I, Z)) / 2
h0 = math.sqrt(5) * (np.eye(4) - np.kron(X, X)) / 2
u = evolve(hc + h0, math.pi)
bad = float(np.vdot(u @ phi, (np.eye(4) - p) @ u @ phi).real)
records['finite_constant_pulse'] = dict(selected_bad=bad, fair_bad=bad/2,
    original_coarse_odd_norm=opnorm(h0 - (2*p-np.eye(4)) @ h0 @ (2*p-np.eye(4)))/2,
    pass_=abs(bad - 4/9) < 1e-12)

# Perfect reduced branches can preserve a bath copy of the fresh seed.
plus = np.array([1, 1], dtype=complex) / math.sqrt(2)
zero = np.array([1, 0], dtype=complex)
rin = projector(np.kron(plus, zero))
u1 = np.kron(Z, X)
actual = (rin + u1 @ rin @ u1.conj().T) / 2
target = np.kron(I/2, projector(zero))
undo = np.diag([1, 1, 1, -1]).astype(complex)
returned = undo @ actual @ undo.conj().T
records['seed_copy'] = dict(joint_trace_distance=trace_distance(actual, target),
    reduced_before=partial_trace_b(actual).real.tolist(),
    returned_plus_overlap=float(np.trace(projector(plus) @ partial_trace_b(returned)).real),
    target_returned_plus_overlap=float(np.trace(projector(plus) @ partial_trace_b(undo @ target @ undo.conj().T)).real),
    pass_=abs(trace_distance(actual, target)-0.5)<1e-12 and
          abs(np.trace(projector(plus) @ partial_trace_b(returned)).real-1)<1e-12)

# Nullspace witness within valid one-time state preparations.
rho_a, rho_b = (I+0.6*X)/2, (I-0.6*X)/2
tz, tx = (I+Z)/2, (I+X)/2
records['unobserved_effect'] = dict(
    observed_z=[float(np.trace(tz @ r).real) for r in [rho_a,rho_b]],
    unobserved_x=[float(np.trace(tx @ r).real) for r in [rho_a,rho_b]],
    pass_=abs(np.trace(tz @ (rho_a-rho_b)))<1e-12 and
          abs(np.trace(tx @ (rho_a-rho_b)).real-0.6)<1e-12)

# Check every 2-qubit Pauli derivative extraction, including cross terms.
ps = [np.kron(a,b) for a,b in itertools.product(PAULI, repeat=2)][1:]
theta = np.arange(1,16,dtype=float) / 200
h = sum(c*q for c,q in zip(theta,ps))
lam = opnorm(h)
t = 0.03
unit = evolve(h,t)
max_derivative_error = 0.0
max_interval_excess = 0.0
for pj,c in zip(ps,theta):
    qj = next(q for q in ps if opnorm(q @ pj + pj @ q)<1e-12)
    rj = -1j * pj @ qj
    rho = (np.eye(4)+qj)/4
    deriv = np.trace(1j*(h@rj-rj@h)@rho).real
    aj = np.trace(rj @ unit @ rho @ unit.conj().T).real
    max_derivative_error=max(max_derivative_error,abs(deriv-2*c))
    max_interval_excess=max(max_interval_excess,abs(c-aj/(2*t))-lam**2*t)
records['coefficient_extraction'] = dict(tested_coefficients=15,
    max_derivative_error=max_derivative_error,
    max_interval_excess=max_interval_excess,
    pass_=max_derivative_error<1e-12 and max_interval_excess<1e-12)

# Cross-block bound remains independent of a large discarded-sector energy.
cross=[]
for energy in [0,1,100,1e6]:
    g,t = 0.2,0.1
    hcut=np.array([[0,g],[g,energy]],dtype=complex)
    hbd=np.diag([0,energy]).astype(complex)
    err=np.linalg.norm((evolve(hcut,t)-evolve(hbd,t))@zero)
    cross.append(dict(discarded_energy=energy,actual_vector_error=float(err),bound=g*t))
records['cutoff_cross_block'] = dict(cases=cross,
    pass_=all(v['actual_vector_error']<=v['bound']+1e-12 for v in cross))

# Sufficient shot budgets and nonuniform allocation.
def shots(k,alpha,epsilon,weights):
    l=math.log(2*k/alpha)/2
    s=sum(a**(2/3) for a in weights)
    n=[math.ceil(l*s*s*a**(2/3)/epsilon**2) for a in weights]
    radius=sum(a*math.sqrt(l/ni) for a,ni in zip(weights,n))
    return dict(K=k,alpha=alpha,epsilon=epsilon,shots=sum(n),radius=radius,n=n if k<5 else None)

costs=[shots(1,.01,.01,[1]), shots(1,.01,.001,[1]),
       shots(324,.01,.01,[1]*324), shots(3,.01,.01,[1,2,8])]
records['shot_allocation'] = dict(cases=costs,
    pass_=all(x['radius']<=x['epsilon']+1e-12 for x in costs))
records['scope']='Finite diagnostics only; no general proof, statistical hardware pass, physical calibration, novelty or advantage follows.'
all_pass=all(v.get('pass_',True) for v in records.values() if isinstance(v,dict))
records['all_finite_diagnostics_pass']=all_pass
encoded=json.dumps(records,indent=2,default=lambda value:value.item())
(OUT/'check_results.json').write_text(encoded+'\n')
print(encoded)
if not all_pass:
    raise SystemExit(1)
