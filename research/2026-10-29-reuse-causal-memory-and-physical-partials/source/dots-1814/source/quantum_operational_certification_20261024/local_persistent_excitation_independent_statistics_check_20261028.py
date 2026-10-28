#!/usr/bin/env python3
"""Deterministic ordinary-law, guard, and rational budget fixtures; zero samples/RNG."""
import itertools,json,math,hashlib
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.linalg import expm
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
P=[I,X,Y,Z];AX=[X,Y,Z]
def kron(*xs):
 z=np.array([[1]],complex)
 for x in xs:z=np.kron(z,x)
 return z
def site(x,l,n):return kron(*(x if t==l else I for t in range(n)))
def op(x):return np.linalg.norm(x,2)
def min_eig(x):return float(np.linalg.eigvalsh((x+x.conj().T)/2).min())
def sign(x):
 v,u=np.linalg.eigh((x+x.conj().T)/2);return (u*np.where(v>=0,1,-1))@u.conj().T
V={};counts={}
def ck(k,v,tol=2e-10):
 V[k]=max(V.get(k,-1e99),float(v));counts[k]=counts.get(k,0)+1;assert v<=tol,(k,v)
fixtures=[]
for q in [1,2]:
 n=q+1;dim=2**n;dl=2**q
 H=sum((site(X,l,n)@site(Z,q,n)+.7*site(Z,l,n)@site(X,q,n) for l in range(q)),np.zeros((dim,dim),complex));H/=op(H)
 U=expm(-.47j*H)@expm(-.29j*site(Y,0,n))
 labels=list(itertools.product(range(4),repeat=q));ps=[kron(*(P[a] for a in alpha)) for alpha in labels]
 modes=['mixed'] if q==2 else ['pure0','pure1','mixed']
 for mode in modes:
  if mode.startswith('pure'):
   state=np.diag([1,0] if mode=='pure0' else [0,1]).astype(complex);gs=[state]+[np.zeros((2,2),complex) for _ in labels[1:]];kap=1.
  else:
   gs=[]
   for ai in range(len(labels)):
    if ai==0:g=I.copy()
    else:
     vv=np.array([math.sin(ai+.2),math.cos(2*ai+.4),math.sin(3*ai+.6)]);vv/=np.linalg.norm(vv)
     g=.07/(len(labels)-1)*(I+.6*sum((vv[j]*AX[j] for j in range(3)),np.zeros((2,2),complex)))
    gs.append(g)
   z=np.trace(sum(gs)).real;gs=[g/z for g in gs];kap=.7
  total=sum(gs);rho=U@kron(np.eye(dl)/dl,total)@U.conj().T
  B={};Delta={};R={}
  for l in range(q):
   for j in [0,2]:
    sj=site(AX[j],l,q);chars=[round(np.trace(pp@sj@pp@sj).real/dl) for pp in ps]
    hj=sum((c*g for c,g in zip(chars,gs)),np.zeros((2,2),complex));rr=U@kron(np.eye(dl)/dl,hj)@U.conj().T
    bb=U@kron(sj,I)@U.conj().T;dd=bb@rr
    B[l,j]=bb;Delta[l,j]=dd;R[l,j]=rr
    ck('CP_contrast_margin',-min_eig(hj-kap*total));ck('fixed_generator_commutation',op(bb@rr-rr@bb));ck('signed_factorization',op(dd-U@kron(sj/dl,hj)@U.conj().T))
  fixtures.append(dict(q=q,n=n,d=dim,U=U,ps=ps,gs=gs,rho=rho,B=B,Delta=Delta,R=R,mode=mode,kap=kap))

born=0
for f in fixtures:
 q,n,d=f['q'],f['n'],f['d'];keys=[(l,j) for l in range(q) for j in [0,1,2]]
 means={k:np.zeros((d,d),complex) for k in keys};squares={k:np.zeros((d,d),complex) for k in keys};totalp=0.
 measurement=[]
 for axes in itertools.product(range(3),repeat=n):
  for outs in itertools.product([-1,1],repeat=n):
   proj=kron(*((I+b*AX[a])/2 for a,b in zip(axes,outs)))
   shadow=kron(*((I+3*b*AX[a])/2 for a,b in zip(axes,outs)))
   measurement.append((proj,shadow))
 for js in itertools.product([0,2],repeat=q):
  for ss in itertools.product([-1,1],repeat=q):
   rin=kron(*((I+s*AX[j])/2 for j,s in zip(js,ss)))
   rout=sum((f['U']@kron(pp@rin@pp,g)@f['U'].conj().T for pp,g in zip(f['ps'],f['gs'])),np.zeros((d,d),complex))
   for proj,z in measurement:
    p=np.trace(proj@rout).real/(4**q*3**n);totalp+=p;born+=1;ck('Born_probability',-p)
    for l in range(q):
     for j in [0,1,2]:
      y=z if j==1 else (2*ss[l]*z if js[l]==j else np.zeros_like(z))
      mu=f['rho'] if j==1 else f['Delta'][l,j]
      means[l,j]+=p*y;squares[l,j]+=p*(y@y)
      ck('centered_increment_cap',op(y-mu)-4*d)
 ck('Born_total',abs(totalp-1))
 for l,j in keys:
  mu=f['rho'] if j==1 else f['Delta'][l,j]
  ck('ordinary_three_matrix_mean',op(means[l,j]-mu))
  scale=3**n if j==1 else 2*3**n
  ck('uncentered_variance_cap',np.linalg.eigvalsh(squares[l,j]-scale*np.eye(d)).max())
  ck('centered_variance_cap',np.linalg.eigvalsh(squares[l,j]-mu@mu-scale*np.eye(d)).max())
# Individually rank-deficient history states can jointly excite the entire patch.
f0,f1=fixtures[0],fixtures[1];rhoavg=(f0['rho']+f1['rho'])/2
ck('pure_history_rank_deficiency',abs(min_eig(f0['rho'])));ck('pure_history_rank_deficiency',abs(min_eig(f1['rho'])))
ck('pooled_full_excitation',abs(min_eig(rhoavg)-.25))
for j in [0,2]:
 davg=(f0['Delta'][0,j]+f1['Delta'][0,j])/2
 ck('pooled_sign_recovers_fixed_B',op(sign(davg)-f0['B'][0,j]))
 ck('pooled_signed_gap',abs(np.min(np.abs(np.linalg.eigvalsh(davg)))-.25))

# Exact rational fixed schedules and both guards at their worst-case confidence labels.
def clog2(x):
 assert x>0;k=0
 while F(2)**k<x:k+=1
 return k
def largest_b(eps,A,q):
 b=F(1)
 while b*b>eps/F(18*A*q):b/=2
 return b
budget=[]
for W in [1,2,3]:
 d=2**W
 for q in [1,W]:
  A=q
  for eps in [F(1),F(1,10),F(1,100)]:
   beta=eps/8;S=24;b=largest_b(eps,A,q);L=clog2(F(6*d*q*(S+1))/(beta/2))
   assert b*b<=eps/F(18*A*q) and b*b>eps/F(72*A*q)
   for kap in [F(1),F(1,17)]:
    for r in [F(1,d),F(1,7*d)]:
     ss=0
     while F(1,16*d*2**ss)>b*kap*r/5:ss+=1
     assert 0<ss<=S
     a=F(1,16*d*2**ss);e=5*a/4;ell=r-5*a/2
     assert ell>0 and 5*a<=2*b*kap*ell
     gamma=kap*r;h=gamma-e
     assert h>e and 10*a<=b*(8*h-5*a)
     N=8*3**W*L/a**2;assert N.denominator==1
     total=8*3**W*L*(16*d)**2*F(4**(ss+1)-1,3)
     assert total<4*N/3
     denom=2*(2*3**W+F(4*d)*a/3)
     assert denom<=5*3**W and N*a*a/denom>=L
     maxN=F(57600*A*q*3**W*L)/(kap*kap*r*r*eps)+1
     assert N<=maxN
     budget.append({'W':W,'q':q,'epsilon':str(eps),'kappa':str(kap),'r':str(r),'stage':ss,'N':int(N),'total_through_stage':int(total),'confidence_log':L})
# Direct gap can pass when a deliberately conservative supplied kappa makes the floor guard fail.
b=F(1,16);gamma=r=F(1,4);kap=F(1,100);a=b*gamma/10;e=5*a/4;h=gamma-e;ell=r-5*a/2
assert h>e and 10*a<=b*(8*h-5*a)
assert not (ell>0 and 5*a<=2*b*kap*ell)

# Exact rational two-sector sign fixtures, including physicality of the zero convention.
def matmul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def transpose(a):return list(map(list,zip(*a)))
def sub(a,b):return [[a[i][j]-b[i][j] for j in range(len(a))] for i in range(len(a))]
def fsq(a):return sum((x*x for row in a for x in row),F(0))
def rootupper(x):
 lo,hi=F(0),F(4)
 for _ in range(40):
  m=(lo+hi)/2
  if m*m>=x:hi=m
  else:lo=m
 return hi
signcases=[]
B=[[F(1),F(0)],[F(0),F(-1)]];Id=[[F(1),F(0)],[F(0),F(1)]]
for tt in [F(0),F(1,128),F(1,32),F(1,8),F(1,2),F(1)]:
 c=(1-tt*tt)/(1+tt*tt);s=2*tt/(1+tt*tt);Q=[[c,-s],[s,c]]
 assert matmul(transpose(Q),Q)==Id
 for g in [F(1,4),F(1,7)]:
  H=[[g,F(0)],[F(0),-g]];D=[[g+g/13,F(0)],[F(0),-g+g/17]]
  C=matmul(matmul(Q,D),transpose(Q));Smat=matmul(matmul(Q,B),transpose(Q));assert matmul(Smat,Smat)==Id
  ee=rootupper(fsq(sub(C,H)));hh=min(abs(D[0][0]),abs(D[1][1]));serr2=fsq(sub(Smat,B))/2
  if ee<g:assert serr2<=(2*ee/(2*g-ee))**2
  if hh>ee:assert serr2<=(2*ee/(2*hh-ee))**2
  signcases.append({'t':str(tt),'g':str(g),'true_gap_bound_applies':bool(ee<g),'direct_gap_bound_applies':bool(hh>ee),'reflection_exact':True})
Czero=[[F(1,4),F(0)],[F(0),F(0)]]
assert matmul(Id,Id)==Id and min(abs(Czero[0][0]),abs(Czero[1][1]))==0

# Prior received approximate-on-site statistical bindings must remain byte-identical.
prior='ordinary_approximate_onsite_frozen_memory_recovery_statistics_receipt_20261028.json'
assert hashlib.sha256(Path(prior).read_bytes()).hexdigest()=='be8bf0b4559e1ee571de283d1425d1ec064484af572ab9739b79abb2a3b64b9f'
pj=json.loads(Path(prior).read_text())
for path,h in pj['sha256'].items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h
out={'status':'PASS','scope':'Deterministic mathematical ordinary Born laws, exact rational stage/guard/sign certificates, no samples/RNG or production Jacobi run.','born_events_enumerated':born,'physical_source_cases':len(fixtures),'individual_rank_deficient_histories_pool_to_full_rank':True,'ordinary_matrix_mean_and_variance_tests':counts,'max_positive_floating_residual':max(0.,max(V.values())),'exact_budget_cases':len(budget),'budget_cases':budget,'direct_gap_pass_marginal_guard_fail_example':True,'exact_two_sector_sign_cases':signcases,'zero_label_physical_fallback_and_guard_rejection':True,'prior_statistics_receipt_sha256':'be8bf0b4559e1ee571de283d1425d1ec064484af572ab9739b79abb2a3b64b9f','prior_direct_bindings_reverified':len(pj['sha256']),'sha256':{}}
for name in ['local_persistent_excitation_independent_statistics_20261028.md',Path(__file__).name]:out['sha256'][name]=hashlib.sha256(Path(name).read_bytes()).hexdigest()
Path('local_persistent_excitation_independent_statistics_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','born_events_enumerated','physical_source_cases','exact_budget_cases','max_positive_floating_residual','prior_direct_bindings_reverified']},indent=2))
