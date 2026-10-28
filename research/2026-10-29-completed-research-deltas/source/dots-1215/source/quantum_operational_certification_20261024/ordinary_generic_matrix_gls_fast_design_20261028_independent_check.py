#!/usr/bin/env python3
"""Independent physical erasure-bank/block-GLS checks; not actual oracle sampling."""
from pathlib import Path
import numpy as np, math,json,hashlib
from fractions import Fraction as Q
rng=np.random.default_rng(281145)
base=Path(__file__).resolve().parent
src=base/'ordinary_generic_matrix_gls_fast_design_20261028.md'
def feat(x):return np.array([x[i]**2 for i in range(4)]+[2*x[i]*x[j] for i in range(4) for j in range(i+1,4)])
anchors=list(np.eye(4))
for i in range(4):
 for j in range(i+1,4):
  x=np.zeros(4);x[i]=x[j]=1/math.sqrt(2);anchors.append(x)
Fa=np.array([feat(x) for x in anchors]);encmin=np.linalg.eigvalsh(Fa.T@Fa/10)[0]
def herm_basis(d):
 B=[];pairs=[]
 for i in range(d):
  O=np.zeros((d,d),complex);O[i,i]=1;B.append(O);pairs.append((i,i))
 for i in range(d):
  for j in range(i+1,d):
   O=np.zeros((d,d),complex);O[i,j]=O[j,i]=1/math.sqrt(2);B.append(O);pairs.append((i,j))
   O=np.zeros((d,d),complex);O[i,j]=1j/math.sqrt(2);O[j,i]=-1j/math.sqrt(2);B.append(O);pairs.append((i,j))
 return np.array(B),pairs
# Work in the known Bell/flag eigenbasis of an actual qubit-erasure loss state.
k=3;d=6;basis,pairs=herm_basis(d);p=d*d;D=10*p;L=8*D;r=d
maxcov=maxbias=maxpred=maxdecoder=0.;minloewner=1.;maxlevfactor=0.;updates=0;designcases=0;projcases=0;deccases=0
for rep in range(5):
 U,_=np.linalg.qr(rng.normal(size=(4,4)));G=U[:,:2]@U[:,:2].T
 grid=anchors+[U[:,2],U[:,3]]
 for _ in range(18):
  x=rng.normal(size=4);grid.append(x/np.linalg.norm(x))
 F=np.array([feat(x) for x in grid]);eras=np.array([x@G@x for x in grid])
 tv=np.array([[0]+[(1-e)/3]*3+[e/2]*2 for e in eras])
 # Six-state loss preparation identity for the erasure channel, before basis change.
 for e in eras[:3]:
  phi=np.array([1,0,0,1,0,0],complex)/math.sqrt(2)
  J=(1-e)*np.outer(phi,phi.conj());J[4,4]+=e/2;J[5,5]+=e/2
  rho=np.diag([(1-e)/2,(1-e)/2,e]);T=(2*np.kron(rho,np.eye(2))-J)/3
  assert np.allclose(np.linalg.eigvalsh(T),sorted([0]+[(1-e)/3]*3+[e/2]*2),atol=1e-12)
 for eta in [0.125,0.01,0.0001]:
  uu=tv+2*eta
  kval=np.array([[(row[i]+row[j])/2 for i,j in pairs] for row in uu])
  weights=np.zeros(len(grid));weights[:10]=.1
  V=np.einsum('x,xi,xj,xq->qij',weights,F,F,1/kval)
  Vinit=V.copy();det0=np.linalg.slogdet(V)[1].sum();lstar=2.**-20;Lambda=4/eta
  Tmax=math.ceil(D*math.log2(Lambda/lstar))+1
  tl=0
  while True:
   Vinv=np.linalg.inv(V)
   leverage=np.einsum('xi,qij,xj,xq->x',F,Vinv,F,1/kval)
   im=int(np.argmax(leverage))
   if leverage[im]<=L+1e-7:break
   vold=np.linalg.slogdet(V)[1].sum()
   weights*=1-1/D;weights[im]+=1/D
   V=np.einsum('x,xi,xj,xq->qij',weights,F,F,1/kval)
   vnew=np.linalg.slogdet(V)[1].sum()
   assert vnew-vold>math.log(2)-1e-9
   tl+=1;assert tl<=Tmax
  updates+=tl;designcases+=1
  assert np.linalg.eigvalsh(Vinit).min()>lstar
  lamlow=lstar*(eta*lstar/4)**4/4
  assert np.linalg.eigvalsh(V).min()>=lamlow
  # Every coordinate block's query leverage is <= summed block trace leverage.
  indiv=np.einsum('xi,qij,xj->xq',F,Vinv,F)/kval
  maxlevfactor=max(maxlevfactor,float(indiv.max()/L));assert indiv.max()<=L+1e-7
  support=np.flatnonzero(weights);n=math.ceil(2**24*D*L/eta)
  mi=np.array([math.ceil(n*weights[i])+math.ceil(2+r/eta) for i in support],dtype=float)
  covcore=np.einsum('x,xi,xj,xq->qij',weights[support]**2/mi,F[support],F[support],1/kval[support])
  cov=np.einsum('qij,qjk,qkl->qil',Vinv,covcore,Vinv)*100
  for qidx in range(p):
   C=np.linalg.cholesky(V[qidx]);ratio=np.linalg.eigvalsh(C.T@cov[qidx]@C*n/100).max();maxcov=max(maxcov,float(ratio));assert ratio<=1+1e-8
  mbar=n+math.ceil(2+r/eta)+1
  zeta=min(eta/(10**6*D*n),1/(mbar*mbar))
  assert all(zeta<=1/(mm*mm)*(1+1e-12) for mm in mi)
  bs=[]
  for _ in support:
   v=rng.normal(size=d)+1j*rng.normal(size=d);v/=np.linalg.norm(v);bb=zeta*np.outer(v,v.conj())
   bs.append(np.einsum('qij,ji->q',basis,bb).real)
  bs=np.array(bs)
  rhs=np.einsum('x,xi,xq->qi',weights[support],F[support],bs/kval[support])
  bias=np.einsum('qij,qj->qi',Vinv,rhs)
  bnorm=np.einsum('qi,qij,qj->',bias,V,bias);bound=zeta*zeta/eta
  maxbias=max(maxbias,float(bnorm/bound));assert bnorm<=bound*(1+1e-8)
  # Draw a coefficient error at the exact allowed V-norm boundary.
  white=rng.normal(size=(p,10));white*=64*math.sqrt(D/n)/np.linalg.norm(white)
  err=np.array([np.linalg.solve(np.linalg.cholesky(V[q]).T,white[q]) for q in range(p)])
  assert abs(np.einsum('qi,qij,qj->',err,V,err)-64**2*D/n)<1e-14
  for xi in range(len(grid)):
   evec=err@F[xi];Em=np.einsum('q,qij->ij',evec,basis);T=np.diag(tv[xi]);Up=np.diag(uu[xi]);That=T+Em
   Un=2*That+2*eta*np.eye(d)
   minloewner=min(minloewner,float(np.linalg.eigvalsh(Un-T-1.25*eta*np.eye(d))[0]))
   assert np.linalg.eigvalsh(Un-T-1.25*eta*np.eye(d))[0]>-1e-10
   assert np.linalg.eigvalsh(3*T+2.75*eta*np.eye(d)-Un)[0]>-1e-10
   for _ in range(4):
    v=rng.normal(size=d)+1j*rng.normal(size=d);v/=np.linalg.norm(v)
    ratio=abs(np.vdot(v,Em@v))/math.sqrt(eta*np.vdot(v,Up@v).real)
    maxpred=max(maxpred,float(ratio));assert ratio<=1/64+1e-10;projcases+=1
   # Arbitrary full-CPTP Choi matrices, conjugated into this known output basis.
   Z=rng.normal(size=(2*k,k))+1j*rng.normal(size=(2*k,k));Qm,_=np.linalg.qr(Z)
   C=np.zeros((d,d),complex)
   for env in range(k):
    Kraus=Qm[env*2:(env+1)*2,:];vv=Kraus.T.reshape(-1);C+=np.outer(vv,vv.conj())
   assert abs(np.trace(C).real-k)<1e-10
   # The known Bell eigenbasis transformation preserves positivity and trace; for (20) only those are needed.
   qtrue=np.trace(T@C).real;qh=np.trace(That@C).real;tau=k*eta
   denom=(1/16)*math.sqrt(3*tau*qtrue+32*tau*tau)
   maxdecoder=max(maxdecoder,abs(qh-qtrue)/denom)
   assert abs(qh-qtrue)<=denom+1e-10;deccases+=1
# Exact bias, median, envelope and final additive budget algebra.
assert Q(101,64**2)<Q(1,16)
assert Q(3,256)+math.sqrt(32)/8<.75
comp=Q(3,2)*Q(5,4)*Q(1,128)+Q(375,2)*Q(1,32768)
assert comp<Q(1,16)
for dd in range(2,16):
 DD=10*dd*dd
 for eta in [Q(1,2),Q(1,2**20)]:
  nn=math.ceil(Q(2**24*DD*(8*DD),1)/eta);mb=nn+math.ceil(2+dd/eta)+1;zz=min(eta/(10**6*DD*nn),Q(1,mb*mb))
  assert zz<=Q(1,mb*mb)
  assert zz*zz/eta<=Q(1,nn)
out={'status':'PASS_INDEPENDENT_MATRIX_GLS_AND_PHYSICAL_BLOCK_DESIGN','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'encoder_anchor_min_eigenvalue':encmin,'physical_block_design_cases':designcases,'actual_determinant_updates':updates,'rank_one_projector_transfer_cases':projcases,'positive_trace_k_decoder_transfer_cases':deccases,'max_coordinate_leverage_over_stop_bound':maxlevfactor,'max_normalized_GLS_covariance_eigenvalue':maxcov,'max_GLS_bias_Vnorm_over_claimed_bound':maxbias,'max_projector_error_over_root_eta_U':maxpred,'min_good_update_Loewner_slack':minloewner,'max_decoder_error_over_final_bound':maxdecoder,'exact_final_comparator_additive_coefficient':str(comp),'scope':'Physical erasure-state block designs and exact covariance/bias/ledger algebra. Synthetic errors test deterministic transfer; no actual local quantum query, production solver, compiler or hardware execution.'}
(base/(src.stem+'_independent_check.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
