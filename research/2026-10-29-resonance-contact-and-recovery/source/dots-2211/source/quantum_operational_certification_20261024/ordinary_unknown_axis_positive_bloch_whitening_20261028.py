#!/usr/bin/env python3
"""Exact physical response/whitening identities plus floating finite-guard fixtures.
No source outcomes sampled. No generic learner or finite rational compiler executed.
"""
from pathlib import Path
import itertools,json,hashlib
import sympy as s
import numpy as np
I=s.eye(2); X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z]
def kron(*ms):
 out=s.ones(1,1)
 for m in ms:out=s.kronecker_product(out,m)
 return out
def clean(m):return m.applyfunc(s.simplify)
def ad(c,u):
 # c=sqrt(1-gamma), u rational unitary rotating the damping axis.
 gamma=1-c*c
 k0=u*s.diag(1,c)*u.H;k1=u*s.Matrix([[0,s.sqrt(gamma)],[0,0]])*u.H
 channel=lambda a:clean(k0*a*k0.H+k1*a*k1.H)
 axis=s.Matrix([s.trace(p*u*Z*u.H)/2 for p in P])
 T=c*s.eye(3)+(c*c-c)*(axis*axis.T)
 assert axis.dot(axis)==1
 for j,p in enumerate(P):assert channel(p/2)==sum((T[k,j]*P[k]/2 for k in range(3)),s.zeros(2))
 assert channel(I/2)==(I+gamma*u*Z*u.H)/2
 return channel,T,channel(I/2),gamma
u0=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
u1=(s.Rational(5,13)*I-s.I*s.Rational(12,13)*X)
c0=s.Rational(4,5);c1=s.Rational(12,13)
ch0,t0,rho0,gamma0=ad(c0,u0);ch1,t1,rho1,gamma1=ad(c1,u1)
V=clean((s.Rational(3,5)*s.eye(4)-s.I*s.Rational(4,5)*kron(Z,Z))*(s.Rational(5,13)*s.eye(4)-s.I*s.Rational(12,13)*kron(X,X)))
assert clean(V.H*V)==s.eye(4)
rows=[];exact_entries=0;all_delta=[];all_B=[]
for i,(ch,T,rhoother) in enumerate([(ch0,t0,rho1),(ch1,t1,rho0)]):
 B=[clean(V*(kron(p,I) if i==0 else kron(I,p))*V.H) for p in P]
 R=clean(V*(kron(I/2,rhoother) if i==0 else kron(rhoother,I/2))*V.H)
 D=[]
 for j,p in enumerate(P):
  plus=ch((I+p)/2);minus=ch((I-p)/2)
  dp=clean(V*(kron((plus-minus)/2,rhoother) if i==0 else kron(rhoother,(plus-minus)/2))*V.H)
  theory=clean(sum((T[k,j]*B[k] for k in range(3)),s.zeros(4))*R)
  assert dp==theory;D.append(dp);exact_entries+=16
  assert clean(R*B[j]-B[j]*R)==s.zeros(4);exact_entries+=16
 G=s.Matrix(3,3,lambda j,k:s.trace(D[j]*D[k]));c=s.trace(R*R)
 assert clean(G)==clean(c*T*T);exact_entries+=9
 W=T.inv()/s.sqrt(c)
 for j in range(3):
  C=clean(sum((D[k]*W[k,j] for k in range(3)),s.zeros(4)))
  assert C==clean(B[j]*R/s.sqrt(c));exact_entries+=16
  # The true sign is B since its commuting factor has strictly positive eigenvalues.
  assert all(v>0 for v in R.eigenvals())
  A=sum((T[k,j]*B[k] for k in range(3)),s.zeros(4));colnorm=s.sqrt(sum(T[k,j]**2 for k in range(3)))
  rawsign=A/colnorm
  discrepancy=float(np.linalg.norm(np.array((rawsign-B[j]).evalf(),dtype=complex),2))
  rows.append({'input':i,'axis':'XYZ'[j],'unwhitened_sign_operator_error':discrepancy,'whitened_exact_sign_correct':True})
 all_delta.append(D);all_B.append(B)
# Local spectator cancellation: two disjoint pair mixers, arbitrary outside pair states.
V4=kron(V,V)
for outside in [kron(I/2,I/2),kron(s.diag(s.Rational(999,1000),s.Rational(1,1000)),s.diag(s.Rational(1,10000),s.Rational(9999,10000)))]:
 R4=clean(V4*kron(I/2,rho1,outside)*V4.H)
 RJ=s.Matrix(4,4,lambda a,b:sum(R4[4*a+k,4*b+k] for k in range(4)))
 assert clean(RJ)==clean(V*kron(I/2,rho1)*V.H);exact_entries+=16
# Ordinary three-axis signed shadow means and conditional matrix variances, exact probabilities.
# Do numerically enumerate actual physical Born probabilities, not sample artificial observations.
nV=np.array(V,dtype=complex);nI=np.eye(2);nP=[np.array(p,dtype=complex) for p in P]
kraus=[]
for c,u in [(c0,u0),(c1,u1)]:
 kraus.append([np.array(u*s.diag(1,c)*u.H,dtype=complex),np.array(u*s.Matrix([[0,s.sqrt(1-c*c)],[0,0]])*u.H,dtype=complex)])
K=[np.kron(k,l) for k in kraus[0] for l in kraus[1]]
means=[[np.zeros((4,4),complex) for _ in range(3)] for i in range(2)]
seconds=[[np.zeros((4,4),complex) for _ in range(3)] for i in range(2)]
count=0;max_normerr=0
for axs in itertools.product(range(3),repeat=2):
 for signs in itertools.product([-1,1],repeat=2):
  inp=np.kron((nI+signs[0]*nP[axs[0]])/2,(nI+signs[1]*nP[axs[1]])/2)
  out=nV@sum((k@inp@k.conj().T for k in K),np.zeros((4,4),complex))@nV.conj().T
  for meas in itertools.product(range(3),repeat=2):
   norm=0
   for results in itertools.product([-1,1],repeat=2):
    pis=[(nI+results[z]*nP[meas[z]])/2 for z in range(2)]
    prob=np.trace(out@np.kron(*pis)).real;norm+=prob
    shadow=np.kron(3*pis[0]-nI,3*pis[1]-nI)
    for i in range(2):
     yy=3*signs[i]*shadow
     means[i][axs[i]]+=prob*yy/(3**2*2**2*3**2)
     seconds[i][axs[i]]+=prob*(yy@yy)/(3**2*2**2*3**2)
    count+=1
   max_normerr=max(max_normerr,abs(norm-1))
mean_err=max(np.linalg.norm(means[i][j]-np.array(all_delta[i][j],dtype=complex),2) for i in range(2) for j in range(3))
max_second=max(np.linalg.eigvalsh(seconds[i][j]).max() for i in range(2) for j in range(3))
assert mean_err<1e-12 and max_second<=3*3**2+1e-12 and max_normerr<1e-12
# Perturbed known-matrix fixtures: bounds of Section 4, NOT acquired outcomes.
rng=np.random.default_rng(202610282013);finite=[]
for i in range(2):
 D=[np.array(m,dtype=complex) for m in all_delta[i]];B=[np.array(m,dtype=complex) for m in all_B[i]]
 for a in [1e-6,1e-7,1e-8]:
  H=[]
  for j in range(3):
   m=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4));m=(m+m.conj().T)/2;m=m/np.linalg.norm(m,2)
   H.append(D[j]+a*m)
  G=np.array([[np.trace(x@y).real for y in H] for x in H]);ev,U=np.linalg.eigh(G)
  h=ev.min();g=3*4*(2*a+a*a);assert h>g
  W=U@np.diag(ev**-.5)@U.T
  # A coarse, checked rounding error allowance; the executed numpy step is not the rational algorithm.
  W0=np.round(W,14);u=np.linalg.norm(W0-W,2)+1e-14
  E=np.sqrt(3)*a/np.sqrt(h)+np.sqrt(3)*g/(2*(h-g)**1.5)+np.sqrt(3)*(1+a)*u
  C=[sum(H[k]*W0[k,j] for k in range(3)) for j in range(3)]
  c=float(s.trace((V*(kron(I/2,rho1) if i==0 else kron(rho0,I/2))*V.H)**2))
  R=np.array(V*(kron(I/2,rho1) if i==0 else kron(rho0,I/2))*V.H,dtype=complex)
  errs=[];signerrs=[];bounds=[]
  for j in range(3):
   errs.append(np.linalg.norm(C[j]-B[j]@R/np.sqrt(c),2));vals,vec=np.linalg.eigh(C[j]);ell=np.min(abs(vals))
   S=(vec*np.sign(vals))@vec.conj().T;signerrs.append(np.linalg.norm(S-B[j],2));bounds.append(2*E/(2*ell-E))
  assert max(errs)<=E+1e-12 and all(x<=b+1e-12 for x,b in zip(signerrs,bounds))
  finite.append({'input':i,'matrix_error_allowance':a,'computed_contrast_error_bound':E,'actual_max_contrast_error':max(errs),'actual_max_reflection_error':max(signerrs),'max_guard_reflection_bound':max(bounds)})
# Orthogonal-polar boundary: an unknown rotation survives whitening if T is not positive symmetric.
angle=np.pi/5;O=np.array([[np.cos(angle),-np.sin(angle),0],[np.sin(angle),np.cos(angle),0],[0,0,1.]])
D=[np.array(m,dtype=complex) for m in all_delta[0]];T=np.array(t0,dtype=float);R=np.array(V*kron(I/2,rho1)*V.H,dtype=complex);B=[np.array(m,dtype=complex) for m in all_B[0]]
A=O@T;DR=[sum(A[k,j]*B[k]@R for k in range(3)) for j in range(3)]
G=np.array([[np.trace(x@y).real for y in DR] for x in DR]);ev,U=np.linalg.eigh(G);W=U@np.diag(ev**-.5)@U.T
polarerr=[]
for j in range(3):
 C=sum(DR[k]*W[k,j] for k in range(3));evc,Uc=np.linalg.eigh(C);S=(Uc*np.sign(evc))@Uc.conj().T
 expected=sum(O[k,j]*B[k] for k in range(3));assert np.linalg.norm(S-expected,2)<1e-12
 polarerr.append(np.linalg.norm(S-B[j],2))
assert max(polarerr)>0.5
out={'status':'PASS_UNKNOWN_AXIS_POSITIVE_BLOCH_WHITENING_FIXTURES','source_outcomes':0,'rng_draws_are_only_known_matrix_perturbations':True,'exact_rational_matrix_entries':exact_entries,'fully_enumerated_three_axis_born_law_events':count,'maximum_shadow_mean_error':mean_err,'maximum_shadow_second_moment_eigenvalue':max_second,'declared_second_moment_bound':27,'maximum_Born_normalization_error':max_normerr,'raw_sign_failure_and_whitened_sign_success':rows,'finite_perturbation_fixtures':finite,'nonpositive_polar_rotation_boundary_errors':polarerr,'scope':'exact source-disabled algebra and fully enumerated Born-law identities; numerical perturbations are not sampled calibration records, rational compiler or hardware','sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(__file__).with_suffix('.md')]}}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
