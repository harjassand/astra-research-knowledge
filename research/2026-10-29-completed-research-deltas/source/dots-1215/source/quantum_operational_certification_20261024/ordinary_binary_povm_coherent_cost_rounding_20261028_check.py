#!/usr/bin/env python3
"""Author finite matrix/algebra checks; not a production SDP or Gaussian compiler."""
from pathlib import Path
import json,hashlib,math
import numpy as np
import sympy as s
rng=np.random.default_rng(281126)
max_complete=max_identity=max_cost=max_num=0.;min_dom=1.;physical=0;exact=0
# Actual noncommuting effects and their coherent dominance/completions.
for a,b in [(1,1),(1,3),(2,2),(2,3),(3,2),(3,3)]:
 d=a+b
 for rep in range(12):
  Z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));U,_=np.linalg.qr(Z)
  eig=rng.uniform(0,1,size=d);E=(U*eig)@U.conj().T
  A=np.eye(a)-E[:a,:a];D=E[a:,a:];B=E[:a,a:]
  H=B@B.conj().T;K=B.conj().T@B
  min_dom=min(min_dom,np.linalg.eigvalsh(A-H)[0],np.linalg.eigvalsh(D-K)[0]);assert min_dom>-1e-11
  assert np.linalg.norm(B,2)<=.5+1e-12
  EM=np.block([[np.eye(a)-2*H,B],[B.conj().T,2*K]])
  EN=np.block([[np.eye(a)-2*H,-B],[-B.conj().T,2*K]])
  residual=EM-EM@EM-np.block([[H-4*H@H,np.zeros((a,b))],[np.zeros((b,a)),K-4*K@K]])
  max_identity=max(max_identity,np.linalg.norm(residual));assert np.linalg.eigvalsh(EM)[0]>-1e-12 and np.linalg.eigvalsh(EM)[-1]<1+1e-12
  Z=rng.normal(size=(a,a))+1j*rng.normal(size=(a,a));Wm=Z@Z.conj().T
  Z=rng.normal(size=(b,b))+1j*rng.normal(size=(b,b));Wp=Z@Z.conj().T
  m=2.**(-rep);q=np.trace(Wm@H).real+np.trace(Wp@K).real
  cost=m+np.trace(Wm@(np.eye(a)-EM[:a,:a])).real+np.trace(Wp@EM[a:,a:]).real
  max_cost=max(max_cost,abs(cost-(m+2*q)))
  Os=[]
  for _ in range(5):
   Z=rng.normal(size=(d,d))+1j*rng.normal(size=(d,d));Os.append((Z+Z.conj().T)/2)
  c=rng.normal(size=5)
  L=lambda E:np.array([np.trace(O@E).real for O in Os])
  NB=np.sum(L(np.block([[np.zeros((a,a)),B],[B.conj().T,np.zeros((b,b))]]))**2)
  vals=[np.sum((c+L(F))**2) for F in [EM,EN]]
  assert max(vals)>=NB-1e-10
  max_num=max(max_num,max(0,NB-max(vals)));physical+=1
# Exact rational polynomial completion identities including complex B.
for rep in range(16):
 a=1+rep%3;b=1+(rep//3)%3
 B=s.Matrix(a,b,lambda i,j:s.Rational(int(rng.integers(-2,3)),64)+s.I*s.Rational(int(rng.integers(-2,3)),64))
 H=B*B.conjugate().T;K=B.conjugate().T*B
 E=(s.eye(a)-2*H).row_join(B).col_join(B.conjugate().T.row_join(2*K))
 target=s.diag(H-4*H*H,K-4*K*K)
 assert all(s.simplify(x)==0 for x in E-E*E-target)
 assert s.re(s.trace(H))<s.Rational(1,4);exact+=1
# Ideal Gaussian joint-event experiments with actual noncommuting matrix series.
gauss=0;min_success=1.;max_moment=0.
for a,b in [(1,2),(2,2),(2,3),(3,3)]:
 d=a+b;h=8
 coeff=[rng.normal(size=(a,b))+1j*rng.normal(size=(a,b)) for _ in range(h)]
 R0=sum(F@F.conj().T for F in coeff);C0=sum(F.conj().T@F for F in coeff)
 scale=math.sqrt(4*max(np.linalg.norm(R0,2),np.linalg.norm(C0,2)))
 coeff=[F/scale for F in coeff]
 Q=rng.normal(size=(5,2*a*b));Hh=Q.T@Q
 Z=rng.normal(size=(a,a))+1j*rng.normal(size=(a,a));Wm=Z@Z.conj().T
 Z=rng.normal(size=(b,b))+1j*rng.normal(size=(b,b));Wp=Z@Z.conj().T
 coord=lambda G:np.concatenate([G.real.ravel(),G.imag.ravel()])
 S=sum(coord(F)@Hh@coord(F) for F in coeff)
 q=sum(np.trace(Wm@F@F.conj().T).real+np.trace(Wp@F.conj().T@F).real for F in coeff)
 ell=(48*d-1).bit_length();R=2*math.isqrt(ell)
 if (R//2)**2<ell:R+=2
 successes=0
 for _ in range(1200):
  zz=rng.normal(size=h);G=sum(z*F for z,F in zip(zz,coeff));v=coord(G);ng=v@Hh@v
  qg=np.trace(Wm@G@G.conj().T).real+np.trace(Wp@G.conj().T@G).real
  ok=ng>=S/2 and qg<=48*q and np.linalg.norm(G,2)<=R/2
  successes+=ok
  if ok:
   B=G/(2*R);nb=ng/(4*R*R);qb=qg/(4*R*R);m=.003
   assert nb/(m+2*qb)>=S/(max(8*R*R,192)*(m+q))-1e-12
  gauss+=1
 min_success=min(min_success,successes/1200)
# Exact event-union, perturbation, and cap constants.
assert s.Rational(1,12)-2*s.Rational(1,48)==s.Rational(1,24)
assert s.Rational(1,24)-s.Rational(1,96)==s.Rational(1,32)
assert (1/s.sqrt(2)-s.Rational(1,4))**2>s.Rational(1,8)
for v in [s.Rational(1,2**i) for i in range(0,100,5)]+[s.Integer(2)**i for i in range(0,100,5)]:
 dd=v/(16*(1+v));assert dd*dd<=v/16
p=Path(__file__).resolve().parent/'ordinary_binary_povm_coherent_cost_rounding_20261028.md'
out={'status':'PASS_AUTHOR_COHERENT_BINARY_EFFECT_ROUNDING','source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'physical_noncommuting_effect_cases':physical,'exact_rational_completion_cases':exact,'gaussian_joint_event_trials':gauss,'minimum_experimental_joint_event_fraction':min_success,'minimum_original_diagonal_dominance_eigenvalue':min_dom,'max_completion_identity_residual':max_identity,'max_exact_cost_numerical_residual':max_cost,'max_affine_sign_choice_violation':max_num,'scope':'Feasible coherent off-diagonal branch only; diagonal one-sided-effect and full-CPTP rounding remain open. No production SDP/Gaussian compiler or hardware.'}
p.with_name(p.stem+'_check.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
