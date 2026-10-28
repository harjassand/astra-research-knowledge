#!/usr/bin/env python3
"""Deterministic margin-free coarse law and exact finite schedule checks; zero RNG."""
from fractions import Fraction as F
from pathlib import Path
import itertools,json,math,hashlib
import numpy as np
from scipy.linalg import expm
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex);AX=[X,Y,Z];P=[I,X,Y,Z]
def kron(*xs):
 z=np.array([[1]],complex)
 for x in xs:z=np.kron(z,x)
 return z
def op(x):return np.linalg.norm(x,2)
def tn(x):return float(np.sum(np.abs(np.linalg.eigvalsh((x+x.conj().T)/2))))
def partial(a,keep,n):
 t=a.reshape([2]*(2*n));remaining=list(range(n))
 for l in reversed(range(n)):
  if l not in keep:
   p=remaining.index(l);t=np.trace(t,axis1=p,axis2=p+len(remaining));remaining.pop(p)
 return t.reshape(2**len(keep),2**len(keep))
viol={};counts={}
def ck(k,v,tol=3e-11):
 viol[k]=max(viol.get(k,-1e99),float(v));counts[k]=counts.get(k,0)+1;assert v<=tol,(k,v)
# True common support {0,1}; candidate windows {0,1},{1,2},{2,3} include a genuinely disjoint one.
swap=np.zeros((4,4),complex)
for a,b in itertools.product(range(2),repeat=2):swap[2*b+a,2*a+b]=1
U=kron(expm(-.43j*swap),I,I);gauge=kron((I+.6*Z)/2,(I+.3*X)/2,(I-.4*Y)/2)
BX=U@kron(X,I,I,I)@U.conj().T;BZ=U@kron(Z,I,I,I)@U.conj().T
ck('exact_common_reflections',op(BX@BX-np.eye(16))+op(BZ@BZ-np.eye(16)))
ck('exact_complementary_anticommutation',op(BX@BZ+BZ@BX))
windows=[[0,1],[1,2],[2,3]];laws=[]
for lam in [0.,.0001,.01,.3,1.]:
 weights=[(1+3*lam)/4]+[(1-lam)/4]*3
 rho=U@kron(I/2,gauge)@U.conj().T;R=lam*rho;Delta=BX@R
 ck('positive_qualitative_block',-np.linalg.eigvalsh(R).min())
 ck('true_containing_trace_mass',abs(tn(partial(Delta,windows[0],4))-lam))
 ck('disjoint_exact_zero',op(partial(Delta,windows[2],4)))
 laws.append({'lambda':lam,'true_norm':tn(partial(Delta,windows[0],4)),'overlapping_norm':tn(partial(Delta,windows[1],4)),'disjoint_norm':tn(partial(Delta,windows[2],4))})
 if lam==.3: selected=(weights,rho,Delta)
weights,rho,Delta=selected
means=[np.zeros((4,4),complex) for _ in windows];squares=[np.zeros((4,4),complex) for _ in windows];events=0;ptotal=0.
for s in [-1,1]:
 rin=(I+s*X)/2;rout=sum((w*U@kron(pp@rin@pp,gauge)@U.conj().T for w,pp in zip(weights,P)),np.zeros((16,16),complex))
 for axes in itertools.product(range(3),repeat=4):
  for outs in itertools.product([-1,1],repeat=4):
   proj=kron(*((I+b*AX[a])/2 for a,b in zip(axes,outs)));pr=np.trace(proj@rout).real/(2*3**4);ptotal+=pr;events+=1
   ck('Born_probability',-pr)
   for k,J in enumerate(windows):
    shadow=kron(*((I+3*outs[l]*AX[axes[l]])/2 for l in J));rec=s*shadow;mu=partial(Delta,J,4)
    means[k]+=pr*rec;squares[k]+=pr*(rec@rec);ck('coarse_increment_cap',op(rec-mu)-8)
ck('Born_normalization',abs(ptotal-1))
for k,J in enumerate(windows):
 mu=partial(Delta,J,4);ck('coarse_signed_shadow_mean',op(means[k]-mu));ck('coarse_variance',np.linalg.eigvalsh(squares[k]-mu@mu-9*np.eye(4)).max())

# Exact rational score margins and finite coarse/fine confidence/resource caps.
def clog2(x):
 k=0
 while F(2)**k<x:k+=1
 return k
budget=[];guardcases=[]
for w in [1,2,3]:
 d0=2**w;n=2*w+2;M=n-w+1
 for q in [1,2]:
  for beta in [F(1,8),F(1,1000)]:
   S0=20;Lc=clog2(F(2*d0*q*M*(S0+1))/(beta/2))
   for lam in [F(1),F(1,3),F(1,100),F(1,10000)]:
    s=0
    while F(1,2**(s+2))>lam/4:s+=1
    assert 0<=s<=S0
    eta=F(1,2**(s+2));Nc=4*12**w*Lc/eta**2;assert Nc.denominator==1
    denom=2*(3**w+2*eta/3)
    assert denom<=3*3**w and Nc*(eta/d0)**2/denom>=Lc
    assert F(5,4)*eta<2*eta and lam-F(5,4)*eta>2*eta
    assert eta>lam/8 and Nc<F(256*12**w*Lc)/(lam*lam)
    total=64*12**w*Lc*F(4**(s+1)-1,3);assert total<4*Nc/3
    budget.append({'w':w,'q':q,'beta':str(beta),'lambda':str(lam),'stage':s,'stage_calls':int(Nc),'cumulative_calls':int(total)})
# Fixed-stage score examples include zero signal, exact threshold rejection and successful overlap.
for eta in [F(1,2),F(1,8),F(1,128)]:
 assert F(5,4)*eta<=2*eta
 for lam in [F(0),4*eta]:
  worst_true=lam-F(5,4)*eta;guardcases.append({'eta':str(eta),'lambda':str(lam),'worst_score':str(worst_true),'passes':worst_true>2*eta})
 assert not (2*eta>2*eta)
# Fine direct-only guard and 2q confidence count, with no kappa variable.
fine=[]
for W in [1,2,3]:
 d=2**W
 for q in [1,2]:
  A=q
  for eps in [F(1),F(1,100)]:
   beta=eps/8;S1=24;Lf=clog2(F(4*d*q*(S1+1))/(beta/2));b=F(1)
   while b*b>eps/F(18*A*q):b/=2
   for gam in [F(1,d),F(1,100*d)]:
    t=0
    while F(1,16*d*2**t)>b*gam/5:t+=1
    assert t<=S1;a=F(1,16*d*2**t);e=5*a/4;h=gam-e
    assert h>e and 10*a<=b*(8*h-5*a)
    Nf=8*3**W*Lf/a**2;assert Nf.denominator==1
    den=2*(2*3**W+F(4*d)*a/3);assert Nf*a*a/den>=Lf
    assert Nf<=F(57600*A*q*3**W*Lf)/(gam*gam*eps)+1
    fine.append({'W':W,'q':q,'epsilon':str(eps),'gamma':str(gam),'stage':t,'calls':int(Nf)})
# Asynchronous certificates: physical Pauli phases have complementary informative axes.
rho=selected[1];gamma=F(21,2000);ck('asynchronous_full_gauge_gap',abs(np.linalg.eigvalsh(rho).min()-float(gamma)))
phase_data=[];retained={};b=F(1,16);stage=0
while F(1,16*16*2**stage)>b*gamma/5:stage+=1
for offset,weights2 in enumerate([[F(1,2),F(1,2),F(0),F(0)],[F(1,2),F(0),F(0),F(1,2)]]):
 aa=F(1,16*16*2**(stage+offset));ee=5*aa/4;qualified=[]
 for j,bb in [(0,BX),(2,BZ)]:
  chars=[round(np.trace(pp@AX[j]@pp@AX[j]).real/2) for pp in P]
  lam=sum((w*c for w,c in zip(weights2,chars)),F(0));assert lam>=0
  hh=lam*gamma
  qualifies=hh>ee and 10*aa<=b*(8*hh-5*aa)
  if qualifies:
   dd=float(lam)*bb@rho;vals,vec=np.linalg.eigh((dd+dd.conj().T)/2);ss=(vec*np.where(vals>=0,1,-1))@vec.conj().T
   ck('asynchronous_mean_sign',op(ss-bb));retained[j]=ss;qualified.append(j)
 phase_data.append({'stage':stage+offset,'certified_this_stage':qualified,'all_same_stage':len(qualified)==2})
assert set(retained)=={0,2} and all(not x['all_same_stage'] for x in phase_data)
ck('asynchronous_retained_signs_compatible_with_fixed_truth',op(retained[0]-BX)+op(retained[2]-BZ))
# Coarse logical discoveries can likewise be retained from noncoincident positive-mass epochs.
coarse_found=set();eta=F(1,16);coarse_phases=[]
for masses in [(F(1),F(0)),(F(0),F(1))]:
 eligible=[i for i,lam in enumerate(masses) if lam-F(5,4)*eta>2*eta]
 coarse_found.update(eligible);coarse_phases.append(eligible)
assert coarse_found=={0,1} and all(len(x)==1 for x in coarse_phases)

# Exact qualitative-positive source with NO positive per-call common margin.
rank_two_cases=[];HXs=[]
for proj in [[F(1),F(1),F(0),F(0)],[F(0),F(0),F(1),F(1)]]:
 GI=[(1+x)/8 for x in proj];GZ=[(1-x)/8 for x in proj];GT=[x+y for x,y in zip(GI,GZ)];HX=[x-y for x,y in zip(GI,GZ)];HZ=GT
 assert GT==[F(1,4)]*4 and sum(GT)==1
 assert min(HX)==0 and min(HZ)>0 and all(x>=0 for x in HX)
 assert any(hx==0 and gt>0 for hx,gt in zip(HX,GT))
 assert sum(HX)==F(1,2) and sum(GZ)==F(1,4)
 HXs.append(HX);rank_two_cases.append({'coarse_X_mass':'1/2','X_gap':0,'Z_gap_with_logical_factor':'1/8','oracle_loss':'1/4','positive_common_margin_impossible':True})
assert [(x+y)/2 for x,y in zip(*HXs)]==[F(1,8)]*4
assert all(x['stage_calls']%2==0 for x in budget) and all(x['calls']%2==0 for x in fine)
# Identity dominance alone does not orient every signed contrast.
pI,pX,pY,pZ=F(3,10),F(3,25),F(29,100),F(29,100)
assert pI+pX+pY+pZ==1 and pI>=max(pX,pY,pZ)
assert pI+pX-pY-pZ==F(-4,25)

# Earlier received sources and receipts are read-only and hash-bound.
protected={
 'ordinary_approximate_onsite_frozen_memory_recovery_statistics_receipt_20261028.json':'be8bf0b4559e1ee571de283d1425d1ec064484af572ab9739b79abb2a3b64b9f',
 'ordinary_acquired_patch_excitation_frozen_recovery_statistics_receipt_20261028.json':'3029fd8fcbf1d80497f1a32c3c4dbe2ad046b9cb8d3c2d8679a78db99486df85'}
protected_counts={}
for fn,h in protected.items():
 assert hashlib.sha256(Path(fn).read_bytes()).hexdigest()==h
 jj=json.loads(Path(fn).read_text())
 for p,hh in jj['sha256'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==hh
 protected_counts[fn]=len(jj['sha256'])
out={'status':'PASS','scope':'Deterministic source-disabled coarse Born laws and exact κ-free geometric thresholds/guards; no sampled acquisition, RNG or production eigensolver.','born_events_enumerated':events,'physical_width':4,'true_common_support':[0,1],'candidate_windows':windows,'contrast_mass_cases':laws,'test_counts':counts,'max_positive_floating_residual':max(0.,max(viol.values())),'exact_coarse_budget_cases':len(budget),'coarse_budgets':budget,'exact_fine_direct_budget_cases':len(fine),'fine_budgets':fine,'strict_threshold_cases':guardcases,'zero_uniform_margin_rank_two_cases':rank_two_cases,'averaged_X_signed_gap':'1/16','identity_dominance_does_not_imply_positive_X_contrast':'-4/25','asynchronous_fine_phases':phase_data,'asynchronous_retained_all_generators':True,'no_stage_individually_certifies_all_generators':True,'asynchronous_coarse_phases':coarse_phases,'protected_prior_receipt_hashes':protected,'protected_prior_bindings_reverified':protected_counts,'sha256':{}}
for p in ['margin_free_local_acquisition_independent_statistics_20261028.md',Path(__file__).name]:out['sha256'][p]=hashlib.sha256(Path(p).read_bytes()).hexdigest()
Path('margin_free_local_acquisition_independent_statistics_check_20261028.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','born_events_enumerated','exact_coarse_budget_cases','exact_fine_direct_budget_cases','max_positive_floating_residual','protected_prior_bindings_reverified']},indent=2))
