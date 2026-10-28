"""Reproducible algebra/numerical audit for PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md.
No collective learner, Schur transform, purification circuit, or hardware execution.
"""
from pathlib import Path
import hashlib, itertools, json
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parent
rng=np.random.default_rng(202610271933)
I=np.eye(2,dtype=complex)
PS=[I,np.array([[0,1],[1,0]],complex),np.array([[0,-1j],[1j,0]],complex),np.diag([1.,-1.])]
def herm(x):return (x+x.conj().T)/2
def norm(x):return float(np.linalg.norm(x,2))
def trnorm(x):return float(np.abs(np.linalg.eigvalsh(herm(x))).sum())
def kraus(d,s,r):
 z=rng.normal(size=(s*r,d))+1j*rng.normal(size=(s*r,d))
 return list(np.linalg.qr(z)[0].reshape(r,s,d))
def cj(ks):
 vs=[k.T.reshape(-1) for k in ks]
 return sum(np.outer(v,v.conj()) for v in vs)
def hcoeff(ks):
 d=ks[0].shape[1];vs=[k.conj().reshape(-1) for k in ks]
 return sum(np.outer(v,v.conj()) for v in vs)/d**2
def fe(ks):
 d=ks[0].shape[1]
 return float(sum(abs(np.trace(k))**2 for k in ks)/d**2)
def comp(ds,es):return [d@e for d in ds for e in es]
def ptr(x,s,d):return np.einsum('aibi->ab',x.reshape(s,d,s,d))
def grouped_tensor(x,y,s1,d1,s2,d2):
 # Input x/y have order B1,A1 and B2,A2. Group as B1,B2,A1,A2.
 z=np.kron(x,y).reshape(s1,d1,s2,d2,s1,d1,s2,d2)
 return z.transpose(0,2,1,3,4,6,5,7).reshape(s1*s2*d1*d2,s1*s2*d1*d2)

rows=[]
for d in [2,3,4]:
 for s in [2,3,4]:
  for r in [2,3]:
   if s*r<d:continue
   for rep in range(3):
    es=kraus(d,s,r);ds=kraus(s,d,max(2,(s+d-1)//d))
    h=hcoeff(es);x=cj(ds);f=fe(comp(ds,es))
    # Source Choi FULL transpose after swap, not partial transpose.
    src=cj(es).reshape(d,s,d,s).transpose(1,0,3,2).reshape(s*d,s*d)
    err=max(abs(np.trace(h@x).real-f),abs(np.trace(h).real-1/d),norm(h-src.T/d**2),norm(ptr(x,s,d)-np.eye(s)))
    assert err<1e-12
    rows.append({'d':d,'s':s,'r':r,'max_residual':float(err)})

twirls=[]
for n in [1,2]:
 d=2**n
 pas=[np.array([[1]],complex)]
 for _ in range(n):pas=[np.kron(a,b) for a in pas for b in PS]
 for rep in range(12):
  es=kraus(d,d,3)
  ts=[p.conj().T@e@p/np.sqrt(len(pas)) for p in pas for e in es]
  j=cj(ts)/d;fid=fe(es)
  phi=np.eye(d).reshape(-1)/np.sqrt(d)
  ideal=np.outer(phi,phi)
  weights=np.array([sum(abs(np.trace(p.conj().T@e))**2 for e in es)/d**2 for p in pas])
  pc=sum(w*cj([p])/d for w,p in zip(weights,pas))
  err=max(norm(j-pc),abs(weights.sum()-1),abs(weights[0]-fid),abs(trnorm(j-ideal)-2*(1-fid)))
  assert err<1e-12
  twirls.append({'qubits':n,'max_residual':float(err)})

products=[]
for s1,s2 in [(2,2),(2,3),(3,4)]:
 e=kraus(2,s1,2);f=kraus(2,s2,2)
 ep=[np.kron(a,b) for a in e for b in f]
 hp=hcoeff(ep);ht=grouped_tensor(hcoeff(e),hcoeff(f),s1,2,s2,2)
 # Tensor a pair of valid positive duals, including a nonscalar diagonal excess.
 y1=(norm(hcoeff(e))+.1)*np.eye(s1)+np.diag(rng.uniform(0,.2,s1))
 y2=(norm(hcoeff(f))+.1)*np.eye(s2)+np.diag(rng.uniform(0,.2,s2))
 a=np.kron(y1,I);b=np.kron(y2,I);he=hcoeff(e);hf=hcoeff(f)
 slack=grouped_tensor(a,b,s1,2,s2,2)-hp
 decomp=grouped_tensor(a-he,b,s1,2,s2,2)+grouped_tensor(he,b-hf,s1,2,s2,2)
 err=max(norm(hp-ht),norm(slack-decomp))
 mineig=float(np.linalg.eigvalsh(herm(slack)).min())
 assert err<1e-12 and mineig>-1e-12
 products.append({'receiver_dimensions':[s1,s2],'coefficient_and_slack_residual':err,'minimum_product_slack_eigenvalue':mineig})

# Exact rational amplitude-damping optimizer and uniqueness witness.
t=sp.Rational(3,5);p=1-t*t
v=sp.Matrix([1,0,0,t]);z=sp.Matrix([0,1,0,0]);ident=sp.Matrix([1,0,0,1])
h=(v*v.T+p*z*z.T)/4;x=ident*ident.T
y=sp.diag((1+t)/4,t*(1+t)/4);a=sp.trace(h*x)
sl=sp.kronecker_product(y,sp.eye(2))-h
assert a==sp.trace(y)==sp.Rational(16,25)
assert sl.nullspace()==[ident]
assert all(q>=0 for q in h.eigenvals()) and all(q>=0 for q in sl.eigenvals())
assert 2*p>2*(1-a)
# Exact product primal/dual certificates, with the tensor-order permutation explicit.
def sxptr(c,s,d):return sp.Matrix(s,s,lambda i,j:sum(c[i*d+k,j*d+k] for k in range(d)))
def sg(x,y):
 z=sp.kronecker_product(x,y)
 order=[((b1*2+a1)*2+b2)*2+a2 for b1 in range(2) for b2 in range(2) for a1 in range(2) for a2 in range(2)]
 return z.extract(order,order)
hp=sg(h,h);xp=sg(x,x);yp=sp.kronecker_product(y,y)
assert sxptr(xp,4,4)==sp.eye(4)
sp_sl=sp.kronecker_product(yp,sp.eye(4))-hp
assert sp_sl==sg(sl,sp.kronecker_product(y,sp.eye(2)))+sg(h,sl)
assert sp.trace(hp*xp)==sp.trace(yp)==a*a
exact={'t':str(t),'damping_p':str(p),'f_opt':str(a),'framed_opt':str(2*(1-a)),'identity_unframed_lower_bound':str(2*p),'slack_eigenvalues':{str(q):m for q,m in sl.eigenvals().items()},'unique_optimal_decoder':'identity','two_copy_primal_value':str(sp.trace(hp*xp)),'two_copy_dual_value':str(sp.trace(yp)),'exact_product_partial_trace_and_slack_decomposition':True}

# General scalar mixture inequalities, including shared latent failures.
max_violation=-1.0
scalars=0
for m in [1,2,3,7,30,100,1000]:
 for a in [0.,1e-10,.25,.6,.99,1.]:
  for _ in range(80):
   fs=a*rng.uniform(0,1,15);w=rng.dirichlet(np.ones(15));g=rng.uniform(.001,1)
   regret=float(a-np.dot(w,fs));eps0=max(0.,regret-g*(1-a))
   lhs=float(a**m-np.dot(w,fs**m));rhs=g*(1-a**m)+m*eps0
   viol=lhs-rhs;max_violation=max(max_violation,viol)
   assert viol<1e-10
   scalars+=1

budgets=[]
for r in [1,2,7,20]:
 for m in [1,3,100]:
  for g,e in [(.1,.01),(1.,1.),(.5,.001)]:
   k=2*r;rr=r;dim=2**int(np.ceil(np.log2(k*rr)));ld=np.log(2*dim)+1
   n=int(np.ceil(30720*dim*ld*m/(g*e)))
   ae2=g*e/(6144*m)
   mean=40*dim*ld/n+8*ae2
   eta=g*e/(32*m)
   loss=48*mean/g+4*eta/g
   complete=2*m*loss+e/2
   assert mean<=g*e/(384*m)*(1+1e-12) and complete<=e*(1+1e-12)
   budgets.append({'R':r,'M':m,'gamma':g,'epsilon':e,'calibration_N':6*n,'ideal_local_excess':float(loss),'total_additive_complete_bound':float(complete)})

th=.2
u=np.diag([np.exp(-1j*th),np.exp(1j*th)])
flagged=trnorm(cj([u])/2-cj([I])/2)
twirl=2*(1-fe([u]))
assert abs(flagged-2*abs(np.sin(th)))<1e-12 and flagged>twirl
out={'status':'PASS','seed':202610271933,'scope':'Algebra/numerical proof checks; collective physical learner not executed','random_choi_normalization_cases':len(rows),'maximum_normalization_residual':max(z['max_residual'] for z in rows),'twirl_cases':len(twirls),'maximum_twirl_residual':max(z['max_residual'] for z in twirls),'tensor_coefficient_and_positive_dual_cases':products,'exact_amplitude_damping_and_tensor_certificate':exact,'scalar_mixture_cases':scalars,'maximum_scalar_bound_violation':max_violation,'finite_budget_cases':len(budgets),'budget_examples':budgets[:3]+budgets[-3:],'exposed_key_counterexample':{'theta':th,'private_twirl_error':twirl,'flagged_Bell_trace_distance':flagged},'proof_sha256':hashlib.sha256((ROOT/'PRIVATE_FRAMED_COMPLETE_OPTIMALITY.md').read_bytes()).hexdigest()}
(ROOT/'private_framed_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
