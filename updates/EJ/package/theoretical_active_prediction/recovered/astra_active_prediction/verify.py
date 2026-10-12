"""Finite diagnostics for active imaginary-time prediction certification.

These are numerical checks, not general-proof verification.
Requires Python 3.10+, NumPy, SciPy. Run: python verify.py
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import expm, logm

RNG = np.random.default_rng(271828)
COUNTS: dict[str, int] = {}
METRICS: dict[str, float] = {}

def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    COUNTS[name] = COUNTS.get(name, 0) + 1

def hermitian_band(d: int) -> np.ndarray:
    z=RNG.normal(size=(d,d))+1j*RNG.normal(size=(d,d))
    q,_=np.linalg.qr(z)
    return (q * RNG.uniform(.02,.98,d)) @ q.conj().T

def unit(d: int) -> np.ndarray:
    x=RNG.normal(size=d)+1j*RNG.normal(size=d)
    return x/np.linalg.norm(x)

def pair_p(B: np.ndarray,C: np.ndarray,v:np.ndarray,w:np.ndarray) -> float:
    x=np.concatenate((B@v,B@w)); y=np.concatenate((C@v,C@w))
    p=1-abs(np.vdot(x,y))**2/(np.vdot(x,x).real*np.vdot(y,y).real)
    return max(0.,float(p))

h=.25; a=np.exp(-h); b=a*a
L=np.sqrt(2)*(1+1/a)/a
Cstar=L/(h*b)
METRICS['Cstar_M_equals_1']=float(Cstar)
rs,rw=leggauss(48); rs=(rs+1)/2; rw=rw/2
max_identity=0.; max_phase_ratio=0.; max_action_ratio=0.

# Independent noncommuting random matrices: projection-to-action and log identity.
for d in [2,3,4,7]:
  for rep in range(8):
    H=hermitian_band(d); K=hermitian_band(d); I=np.eye(d)
    B=expm(-h*H); C=expm(-h*K); w=unit(d)
    c=float(np.vdot(w,B@w).real/np.vdot(w,C@w).real)
    D=B/c
    check('scalar_bracket', a-1e-12<=c<=1/a+1e-12)
    J=np.zeros((d,d),complex)
    for r,weight in zip(rs,rw):
      F=np.linalg.inv((1-r)*I+(r/b)*D)
      G=np.linalg.inv((1-r)*I+(r/b)*C)
      J+=weight*(F@(D-C)@G)/b
      check('resolvent_contraction',np.linalg.norm(F,2)<=1+1e-11)
      check('candidate_resolvent_condition',np.linalg.eigvalsh(G).min()>=b-1e-11)
    err=np.linalg.norm(J-(logm(D)-logm(C)),2)
    max_identity=max(max_identity,float(err))
    check('noncommuting_log_identity',err<2e-11)
    for k in range(12):
      v=unit(d); p=pair_p(B,C,v,w)
      defect=np.linalg.norm((D-C)@v)
      check('paired_state_action_bound',defect<=L*np.sqrt(p)+2e-11)
      if p>1e-20: max_action_ratio=max(max_action_ratio,float(defect/(L*np.sqrt(p))))

    # Full trajectory certificate at a finite collection of times, quadrature in s,r.
    T=float(RNG.uniform(.1,8))
    sx,sw=leggauss(32); times=(sx+1)*T/2; sw=sw/2
    pmean=0.
    residual=0.
    for s,weight_s in zip(times,sw):
      phi=expm(-1j*s*K)@w
      residual+=weight_s*np.linalg.norm((H+(np.log(c)/h)*I-K)@phi)**2
      for r,weight_r in zip(rs,rw):
        G=np.linalg.inv((1-r)*I+(r/b)*C)
        v=G@phi; v/=np.linalg.norm(v)
        pmean+=weight_s*weight_r*pair_p(B,C,v,w)
    check('integrated_generator_bound',residual<=(Cstar**2)*pmean+2e-10)
    for t in np.linspace(0,T,17):
      error=np.linalg.norm(expm(-1j*t*(H+(np.log(c)/h)*I))@w-expm(-1j*t*K)@w)
      bound=Cstar*T*np.sqrt(pmean)
      check('uniform_trajectory_grid_bound',error<=bound+1e-10)
      if bound>1e-15: max_phase_ratio=max(max_phase_ratio,float(error/bound))

METRICS['max_log_identity_operator_error']=max_identity
METRICS['max_action_bound_ratio']=max_action_ratio
METRICS['max_trajectory_bound_ratio']=max_phase_ratio

# Exact-zero structure: differing Hamiltonians outside the queried cyclic subspace.
for d in [3,4,8]:
    K=np.diag(np.linspace(.1,.7,d)); H=K.copy()
    H[:2,:2]+=.07*np.eye(2)
    H[2:,2:]=.9*np.eye(d-2)
    w=np.zeros(d,complex); w[0]=1/np.sqrt(2); w[1]=1j/np.sqrt(2)
    B=expm(-h*H); C=expm(-h*K)
    for s in [0.,.3,3.,12.]:
      for r in [0.,.2,.75,1.]:
        G=np.linalg.inv((1-r)*np.eye(d)+(r/b)*C)
        v=G@expm(-1j*s*K)@w; v/=np.linalg.norm(v)
        check('equivalent_rays_zero_witness',pair_p(B,C,v,w)<2e-14)

# Forward-filter lower bound: canonical Stinespring overlap is second-order,
# uniformly over filter durations. H0=.5 I, Hdelta=.5 I+delta Z.
for delta in [.001,.01,.05,.2]:
  for tfilter in np.geomspace(1e-6,1e3,101):
    x=np.exp(-tfilter*.5)
    y=np.exp(-tfilter*(.5+np.array([delta,-delta])))
    overlap=x*y+np.sqrt(-np.expm1(-2*tfilter*.5))*np.sqrt(-np.expm1(-2*tfilter*(.5+np.array([delta,-delta]))))
    check('all_duration_isometry_overlap',np.max(abs(1-overlap))<=2*delta**2+2e-14)
    check('duration_weighted_isometry_overlap',np.max(abs(1-overlap))<=delta**2*tfilter+2e-14)
    check('stinespring_overlap_positive',overlap.min()>0)

# The elementary scalar inequality used in the preceding analytic proof.
for x in np.geomspace(1e-10,100,301):
    check('exp_scalar_inequality',np.expm1(x)>=x*x)

# Explicit obstruction to a fully tolerant interpretation of this certificate.
for small in [.001,.01,.1,.2]:
    H=np.zeros((2,2));K=np.diag([0.,1.]);B=np.eye(2);C=expm(-h*K)
    w=np.array([np.sqrt(1-small**2),small],complex)
    pw=small**2*(1-small**2)*(1-a)**2/(1-small**2+a*a*small**2)
    for s in [0.,1.,3.,9.]:
      for r in [0.,.5,1.]:
        G=np.linalg.inv((1-r)*np.eye(2)+(r/b)*C)
        v=G@expm(-1j*s*K)@w;v/=np.linalg.norm(v)
        check('tolerance_counterexample_witness_floor',pair_p(B,C,v,w)>=pw/2-1e-14)
      state=expm(-1j*s*K)@w
      distance=np.sqrt(max(0.,1-abs(np.vdot(w,state))**2))
      check('tolerance_counterexample_trajectory_small',distance<=2*small+1e-13)

out={
 'status':'All finite diagnostics passed. Floating-point/quadrature evidence only.',
 'seed':271828,
 'checks_by_type':COUNTS,
 'total_assertions':sum(COUNTS.values()),
 'metrics':METRICS,
 'scope':'No quantum circuit was compiled; no laboratory samples were acquired. The general proofs are in research_note.md.'
}
path=Path(__file__).with_name('diagnostics.json');path.write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
