#!/usr/bin/env python3
"""Independent finite-dimensional corroboration; not a full circuit/SDP execution."""
from pathlib import Path
import json, math
from fractions import Fraction as F
import numpy as np
import sympy as sp

OUT=Path(__file__).with_suffix('.json')
rng=np.random.default_rng(202610271849)
b=1.5
I2=np.eye(2,dtype=complex)
Paulis=[np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1,-1]).astype(complex)]
Ps=[(I2+sgn*p)/2 for p in Paulis for sgn in [1,-1]]

def herm(a): return (a+a.conj().T)/2

def root(a):
    w,v=np.linalg.eigh(herm(a));return (v*np.sqrt(np.maximum(w,0)))@v.conj().T

def invroot(a):
    w,v=np.linalg.eigh(herm(a));return (v/np.sqrt(w))@v.conj().T

def density(d,rank=None):
    a=rng.normal(size=(d,rank or d))+1j*rng.normal(size=(d,rank or d)); a=a@a.conj().T
    return a/np.trace(a).real

def kraus(di,do,rank):
    a=rng.normal(size=(do*rank,di))+1j*rng.normal(size=(do*rank,di))
    q,_=np.linalg.qr(a)
    return [q[j*do:(j+1)*do,:] for j in range(rank)]

def apply(ks,a): return sum(k@a@k.conj().T for k in ks)
def adjoint(ks,a): return sum(k.conj().T@a@k for k in ks)
def choi(ks):
    vs=[k.T.reshape(-1) for k in ks]
    return sum(np.outer(v,v.conj()) for v in vs)
def partial(C,k): return np.trace(C.reshape(k,2,k,2),axis1=1,axis2=3)
def risk(ks,rs): return b*sum((1-np.trace(p@apply(ks,r)).real) for p,r in zip(Ps,rs))/6

def fidelityroot(a,c):
    # Nuclear-norm definition avoids an unstable second positive square root.
    return min(1.,float(np.linalg.svd(root(a)@root(c),compute_uv=False).sum()))

metrics={k:0. for k in ['identity_residual','choi_objective_residual','tp_residual','effect_psd_violation','bures_transfer_violation','two_transfer_violation','young_violation','repair_tp_residual','repair_psd_violation','repair_objective_perturbation','top_vector_violation','affine_repair_tp_residual','affine_repair_psd_violation','affine_repair_op_error_violation']}
rows=[]
for k in [2,3,4,6,8]:
  for rep in range(12):
    E=kraus(2,k,min(3,k));D=kraus(k,2,k)
    rs=[apply(E,p) for p in Ps]
    ell=1-sum(abs(np.trace(d@e))**2 for d in D for e in E)/4
    rt=risk(D,rs)
    metrics['identity_residual']=max(metrics['identity_residual'],abs(ell-rt))
    C=choi(D)
    H=sum(np.kron(r.T,I2-p) for r,p in zip(rs,Ps))*b/6
    metrics['choi_objective_residual']=max(metrics['choi_objective_residual'],abs(np.trace(H@C).real-rt))
    metrics['tp_residual']=max(metrics['tp_residual'],float(np.linalg.norm(partial(C,k)-np.eye(k))))
    for p in Ps:
      ev=np.linalg.eigvalsh(b*(np.eye(k)-adjoint(D,p)))
      metrics['effect_psd_violation']=max(metrics['effect_psd_violation'],float(-ev.min()),float(ev.max()-b))
    weight=10**rng.uniform(-5,-.1)
    ts=[(1-weight)*r+weight*density(k) for r in rs]
    delta=sum(1-fidelityroot(r,t) for r,t in zip(rs,ts))/6
    rr=risk(D,ts)
    metrics['bures_transfer_violation']=max(metrics['bures_transfer_violation'],abs(math.sqrt(rt)-math.sqrt(rr))-math.sqrt(2*b*delta))
    # Optimize over a finite, explicitly feasible family only. This is NOT a full SDP solver.
    family=[D]+[kraus(k,2,k) for _ in range(9)]
    true=np.array([risk(d,rs) for d in family]); estimated=np.array([risk(d,ts) for d in family])
    h=int(estimated.argmin());o=int(true.argmin()); eta=10**rng.uniform(-8,-2)
    bound=(math.sqrt(true[o])+2*math.sqrt(2*b*delta)+math.sqrt(eta))**2
    metrics['two_transfer_violation']=max(metrics['two_transfer_violation'],float(true[h]-bound))
    gamma=10**rng.uniform(-4,0)
    ybound=(1+gamma)*true[o]+48*delta/gamma+4*eta/gamma
    metrics['young_violation']=max(metrics['young_violation'],float(bound-ybound))
    # PSD/TP feasibility repair under finite perturbations.
    theta=.02
    mixed=(1-theta)*C+theta*np.eye(2*k)/2
    noise=herm(rng.normal(size=(2*k,2*k))+1j*rng.normal(size=(2*k,2*k)))
    noise*=1e-7/max(abs(np.linalg.eigvalsh(noise)))
    rounded=mixed+noise; S=partial(rounded,k); A=np.kron(invroot(S),I2); fixed=herm(A@rounded@A)
    metrics['repair_tp_residual']=max(metrics['repair_tp_residual'],float(np.linalg.norm(partial(fixed,k)-np.eye(k))))
    metrics['repair_psd_violation']=max(metrics['repair_psd_violation'],float(-np.linalg.eigvalsh(fixed).min()))
    Ht=sum(np.kron(t.T,I2-p) for t,p in zip(ts,Ps))*b/6
    metrics['repair_objective_perturbation']=max(metrics['repair_objective_perturbation'],abs(float(np.trace(Ht@(fixed-mixed)).real)))
    affine=rounded+np.kron(np.eye(k)-S,I2/2)
    metrics['affine_repair_tp_residual']=max(metrics['affine_repair_tp_residual'],float(np.linalg.norm(partial(affine,k)-np.eye(k))))
    metrics['affine_repair_psd_violation']=max(metrics['affine_repair_psd_violation'],float(-np.linalg.eigvalsh(affine).min()))
    metrics['affine_repair_op_error_violation']=max(metrics['affine_repair_op_error_violation'],float(np.linalg.norm(affine-mixed,2)-2e-7))
    rows.append({'k':k,'rep':rep,'ell':float(ell),'delta':float(delta),'finite_family_empirical_regret':float(estimated[h]-estimated.min())})

for d in [2,4,8,16]:
 for rep in range(30):
  v=rng.normal(size=d)+1j*rng.normal(size=d);v/=np.linalg.norm(v);P=np.outer(v,v.conj())
  e=10**rng.uniform(-5,-.1);a=10**rng.uniform(-6,-.3)
  B=herm(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)));B*=e/max(abs(np.linalg.eigvalsh(B)))
  A=herm(rng.normal(size=(d,d))+1j*rng.normal(size=(d,d)));A*=a/max(abs(np.linalg.eigvalsh(A)))
  _,V=np.linalg.eigh(P+B+A);w=V[:,-1];loss=1-abs(np.vdot(v,w))**2
  metrics['top_vector_violation']=max(metrics['top_vector_violation'],float(loss-min(1,4*(e+a)**2)))

# Exact symbolic six-state projective 2-design and single-qubit Clifford moments.
Si=sp.eye(2); SX=sp.Matrix([[0,1],[1,0]]);SY=sp.Matrix([[0,-sp.I],[sp.I,0]]);SZ=sp.diag(1,-1)
SP=[(Si+s*A)/2 for A in [SX,SY,SZ] for s in [1,-1]]
Swap=sp.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
sum2=sum((sp.kronecker_product(p,p) for p in SP),sp.zeros(4))
assert sp.simplify(sum2-sp.eye(4)-Swap)==sp.zeros(4)
x,y,z=sp.symbols('x y z',real=True);rho=(Si+x*SX+y*SY+z*SZ)/2
mean=sp.zeros(2); second=sp.zeros(2)
for p in SP:
 pr=sp.trace(rho*p)/3; est=3*p-Si
 mean+=pr*est;second+=pr*est*est
assert sp.simplify(mean-rho)==sp.zeros(2)
assert sp.simplify(second-(2*Si+rho))==sp.zeros(2)
# Scalar constants, exactly rational where possible.
assert 4*(F(1,4)+F(1,4))**2==1
assert 48*F(1,192)+4*F(1,16)==F(1,2)
for D in [2,4,8,32,128]: assert 4*D+F(2,3)*(D+1)<=5*D
for D in [2,4,8,32]:
 for m in [1.,1e-2,1e-6]:
  for beta in [.4,.01,1e-5]:
   n=math.ceil(80*D/m*math.log(12*D/beta));tail=12*D*math.exp(-n*m/(80*D))
   assert tail<=beta*(1+1e-12)

for key,value in metrics.items():
 if key!='repair_objective_perturbation': assert value<1e-9,(key,value)
assert metrics['repair_objective_perturbation']<1e-5
result={'status':'PASS','seed':202610271849,'physical_channel_cases':len(rows),'top_vector_cases':120,'exact_symbolic_six_pauli_2design':True,'exact_symbolic_clifford_first_second_moments':True,'exact_budget_and_bernstein_constants':True,'metrics':metrics,'cases':rows,'scope':'Independent algebra and finite-dimensional numerical corroboration only. Finite-family optimization is not a full CPTP SDP, and no Schur/purification circuit or gate synthesis was executed. Asymptotic conclusions rely on the proof and stated imported primitive theorems.'}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
