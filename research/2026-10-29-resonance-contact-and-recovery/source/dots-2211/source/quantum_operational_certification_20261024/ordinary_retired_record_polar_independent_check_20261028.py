#!/usr/bin/env python3
"""Independent finite Born-law/moment and polar-bias mechanism checks.
Exact probabilities, no acquired samples. Numerical SVD diagnostics are not the proof.
"""
from pathlib import Path
import itertools,json,hashlib
import sympy as s
import numpy as np
R=s.Matrix([[s.Rational(3,5),-s.Rational(4,5),0],[s.Rational(4,5),s.Rational(3,5),0],[0,0,1]])
axis=s.Matrix([s.Rational(3,5),s.Rational(4,5),0]);S=s.Rational(4,5)*s.eye(3)-s.Rational(4,25)*axis*axis.T;B=R*S;c=s.Rational(9,25)*R*axis;a=s.Rational(16,25)
assert R.T*R==s.eye(3) and R.det()==1
basis=[s.eye(3)[:,i]*sign for i in range(3) for sign in [1,-1]]
mean=s.zeros(3);second=s.Rational(0);mass=s.Rational(0);events=0
for u,v,y in itertools.product(basis,basis,[1,-1]):
 p=(1+y*(v.T*(B*u+c))[0])/72
 assert p>=0
 Z=9*y*v*u.T;mean+=p*Z;second+=p*sum(z*z for z in Z);mass+=p;events+=1
assert mean==B and second==81 and mass==1
variance=second-s.trace(B.T*B);assert variance==81-s.trace(S*S)
# Exact first derivative, independently solved from the three skew coordinates.
x,y,z=s.symbols('x y z');Om=s.Matrix([[0,-z,y],[z,0,-x],[-y,x,0]])
H=s.Matrix([[s.Rational(2,7),s.Rational(-1,5),s.Rational(1,9)],[s.Rational(3,8),s.Rational(1,6),s.Rational(-2,9)],[s.Rational(1,11),s.Rational(2,13),s.Rational(-1,7)]])
F=R.T*H;sol=s.solve(list(S*Om+Om*S-F+F.T),[x,y,z]);Omega1=Om.subs(sol)
assert S*Omega1+Omega1*S==F-F.T
Bn=np.array(B,float);Rn=np.array(R,float);Sn=np.array(S,float);Hn=np.array(H,float);On=np.array(Omega1,float);an=float(a)
def proper(M):
 U,sv,Vh=np.linalg.svd(M);return U@np.diag([1,1,np.linalg.det(U@Vh)])@Vh
rows=[]
for t in [0.05,0.01,0.002,0.0004]:
 Ks=[]
 for coef in [1,-2]:
  En=coef*t*Hn;fn=Rn.T@En;Q=proper(Bn+En);O=Rn.T@Q;K=O-np.eye(3);omega=coef*t*On
  norm=np.linalg.norm(En,'fro');assert norm<=an/2
  identity=Sn@(K-omega)+(K-omega)@Sn+fn.T@K-K.T@fn+K.T@K@Sn
  assert np.linalg.norm(identity,'fro')<2e-14
  rem=np.linalg.norm(K-omega,'fro');bound=4*norm**2/an**3;assert rem<=bound+2e-14
  Ks.append(K)
 avg=(2*Ks[0]+Ks[1])/3;var=2*t*t*np.linalg.norm(Hn,'fro')**2
 assert np.linalg.norm(avg,'fro')<=20*var/an**3
 rows.append({'scale':t,'unequal_weight_mean_bias_fro':float(np.linalg.norm(avg,'fro')),'mean_bias_over_scale_squared':float(np.linalg.norm(avg,'fro')/t**2),'proved_second_moment_bound':float(20*var/an**3)})
# Proper fallback is defined on singular, reflected, and zero matrices.
fallback=[]
for M in [np.zeros((3,3)),np.diag([1,0,0]),np.diag([-1,1,1])]:
 Q=proper(M);assert np.linalg.norm(Q.T@Q-np.eye(3))<1e-12 and abs(np.linalg.det(Q)-1)<1e-12
 fallback.append(float(np.linalg.det(Q)))
# Record-retirement boundary: opposite rational unitaries have quadratic averaged
# dephasing error but linear classical-record-resolved unitary error.
retired=[]
for t in [s.Rational(1,10),s.Rational(1,100)]:
 u=2*t/(1+t*t);v=(1-t*t)/(1+t*t);assert u*u+v*v==1
 retired.append({'rational_angle_parameter':str(t),'record_averaged_half_diamond':str(u*u),'record_resolved_half_diamond':str(u),'ratio':str(1/u)})
result={'status':'PASS','scope':'Exact 72-outcome finite CPTP Born law and moment; numerical anisotropic polar remainders with exact derivative; exact record-retirement boundary. No source samples or production compiler.','source_outcomes':0,'rng_draws':0,'born_events':events,'single_record_frobenius_variance':str(variance),'nonunital_translation':[str(x) for x in c],'polar_bias_fixtures':rows,'bad_estimate_proper_fallback_determinants':fallback,'retirement_boundary':retired,'sha256':{Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
