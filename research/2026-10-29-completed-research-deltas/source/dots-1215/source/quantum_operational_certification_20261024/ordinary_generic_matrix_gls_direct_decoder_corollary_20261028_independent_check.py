#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,math
from fractions import Fraction as F
import numpy as np
rng=np.random.default_rng(281200)
physical=0;zero=0;maxratio=0.;min_eig=1.
for k in [2,3,4,6]:
 for env in [1,2,4]:
  for rep in range(5):
   Z=rng.normal(size=(k*env,2))+1j*rng.normal(size=(k*env,2));Qm,_=np.linalg.qr(Z)
   if env==1:
    Qm=np.zeros((k,2),complex);per=rng.permutation(k)[:2]
    Qm[per[0],0]=[1,-1,1j,-1j][rep%4];Qm[per[1],1]=1
   J=np.zeros((2*k,2*k),complex);rho=np.zeros((k,k),complex)
   for r in range(env):
    V=Qm[r*k:(r+1)*k,:];vec=V.reshape(-1)
    J+=np.outer(vec,vec.conj())/2;rho+=V@V.conj().T/2
   T=(2*np.kron(rho,np.eye(2))-J)/3;assert np.linalg.eigvalsh(T)[0]>-1e-11
   if env==1:
    C=2*J+np.kron(np.eye(k)-2*rho,np.eye(2)/2);zero+=1
   else:
    rdec=k;Z=rng.normal(size=(2*rdec,k))+1j*rng.normal(size=(2*rdec,k));Vd,_=np.linalg.qr(Z)
    C=np.zeros((2*k,2*k),complex)
    for r in range(rdec):
     K=Vd[2*r:2*r+2,:];v=K.T.reshape(-1);C+=np.outer(v,v.conj())
    C=C.T
   assert abs(np.trace(C).real-k)<1e-10
   assert np.linalg.eigvalsh(C)[0]>-1e-10 and np.linalg.eigvalsh(C)[-1]<2+1e-10
   pt=np.array([[sum(C[2*i+a,2*j+a] for a in range(2)) for j in range(k)] for i in range(k)])
   assert np.linalg.norm(pt-np.eye(k))<1e-9
   q=max(0.,np.trace(T@C).real)
   for eta in [2.**-3,2.**-10,2.**-24,2.**-40]:
    U=3*T+32*eta*np.eye(2*k);KUC=(U@C+C@U)/2;cc=np.trace(C@KUC).real
    assert cc<=6*q+64*k*eta+1e-9
    E=math.sqrt(eta)/64*KUC/math.sqrt(cc)+eta/(64*k)*np.eye(2*k)
    actual=abs(np.trace(C@E).real);bound=math.sqrt(6*eta*q+64*k*eta*eta)/64+eta/64
    maxratio=max(maxratio,actual/bound);assert actual<=bound*(1+1e-6)+1e-14
    physical+=1
budgets=0
for k in [1,2,3,4,7,16,31,64,127,256]:
 K=math.isqrt(k)+(math.isqrt(k)**2<k)
 for gamma in [F(1),F(1,2),F(1,7),F(1,64),F(1,2**20)]:
  delta=gamma/16;B=1/gamma+K
  assert F(9,1024)/gamma+F(9*K,64)<=B/4
  assert (1+delta)/(1-delta)<=1+gamma/4
  assert (B/2+1)/(1-delta)<=2*B
  for eps in [F(1),F(1,13),F(1,2**20)]:
   target=gamma*eps/(1024*(1+gamma*K));J=0
   while F(1,2**J)>target:J+=1
   eta=F(1,2**J);assert target/2<eta<=target
   add=F(3,2)*(1+gamma/4)*(2*eps/256)+3*eta*B
   assert add<=F(18,1024)*eps<eps/32
   for opt in [F(0),F(1,10**9),F(1,3),F(2,3)]:
    A=eta*B/4;selected=((1+delta)*opt+2*A+eta)/(1-delta)
    assert selected<=(1+gamma/4)*opt+2*eta*B;budgets+=1
p=Path(__file__).resolve().parent/'ordinary_generic_matrix_gls_direct_decoder_corollary_20261028.md'
out={'status':'PASS_INDEPENDENT_DIRECT_DECODER_REFINEMENT','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'physical_channel_CPTP_decoder_direction_cases':physical,'perfect_isometry_decoder_fixtures':zero,'maximum_direct_direction_error_over_claimed_bound':maxratio,'exact_relative_decision_budget_cases':budgets,'maximum_additive_coefficient':'18/1024 < 1/32','scope':'The received GLS event tested directly on full-CPTP decoder directions, with exact decision/budget algebra. No new measurement, matrix tail, production SDP, or hardware execution.'}
p.with_name(p.stem+'_independent_check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
