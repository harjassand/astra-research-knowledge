#!/usr/bin/env python3
"""Zero-source algebra/Born-law diagnostic, not a sampled learner or practical pilot."""
import json,hashlib,math,itertools
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as s
I=s.eye(2);P=[I,s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
def U(q):return q[0]*I-s.I*sum((q[i+1]*P[i+1] for i in range(3)),s.zeros(2))
def RR(q):
 v=U(q);return s.Matrix(3,3,lambda a,j:s.simplify(s.trace(P[a+1]*v*P[j+1]*v.conjugate().T)/2))
def KK(M):
 x,y,z=0,1,2
 K=s.zeros(4);K[0,0]=s.trace(M)
 for a in range(3):K[a+1,a+1]=2*M[a,a]-s.trace(M)
 K[0,1]=K[1,0]=M[2,1]-M[1,2];K[0,2]=K[2,0]=M[0,2]-M[2,0];K[0,3]=K[3,0]=M[1,0]-M[0,1]
 for a in range(3):
  for b in range(a+1,3):K[a+1,b+1]=K[b+1,a+1]=M[a,b]+M[b,a]
 return K
def stereo(t):
 n=sum(x*x for x in t);return s.Matrix([(1-n)/(1+n)]+[2*x/(1+n) for x in t])
def fsq(M):return s.simplify(s.trace(M.conjugate().T*M))
quats=[stereo(list(map(s.Rational,t))) for t in [(0,0,0),(s.Rational(1,3),0,0),(0,s.Rational(-2,5),0),(0,0,1),(s.Rational(1,2),s.Rational(1,3),s.Rational(-1,4))]]
quats +=[s.Matrix([0,1,0,0]),s.Matrix([0,0,1,0])]
kappa=s.Rational(1,5);exact=0
for q in quats:
 v=U(q);r=RR(q)
 assert v.conjugate().T*v==I and r.T*r==s.eye(3) and r.det()==1
 assert 1-r[1,1]<=2-r[0,0]-r[2,2]
 for lx,lz in[(kappa,kappa),(s.Rational(1,2),s.Rational(3,5)),(s.Rational(1,4),1)]:
  D=s.diag(lx,0,lz)
  assert s.trace(D*(s.eye(3)-r))>=kappa*fsq(r-s.eye(3))/4
  exact+=1
 for M in [s.Matrix([[s.Rational(3,10),0,s.Rational(1,10)],[-s.Rational(1,5),0,s.Rational(7,20)],[s.Rational(3,20),0,s.Rational(2,5)]]),s.diag(1,0,-1),s.zeros(3)]:
  assert s.simplify((q.T*KK(M)*q)[0]-s.trace(r.T*M))==0
  exact+=1
# Explicit improper branch obstruction: same X/Z, reversed Y, zero fitting cost.
improper=s.diag(1,-1,1);assert improper.det()==-1 and s.trace(s.diag(kappa,0,kappa)*(s.eye(3)-improper))==0 and fsq(improper-s.eye(3))==4
# A small actual rational backward-Jacobi fit, with every returned constraint exact.
M=s.Matrix([[s.Rational(3,10),0,s.Rational(1,10)],[-s.Rational(1,5),0,s.Rational(7,20)],[s.Rational(3,20),0,s.Rational(2,5)]])
K=KK(M);A=K.copy();Q=s.eye(4);tau=s.Rational(1,1024);cap=16*math.ceil(math.log2(32*4*12**2/float(tau)**2));rotations=0
while fsq(A-s.diag(*A.diagonal()))>tau*tau:
 assert rotations<cap
 a,b=max(((i,j) for i in range(4) for j in range(i+1,4)),key=lambda ij:abs(A[ij[0],ij[1]]))
 angle=.5*math.atan2(2*float(A[a,b]),float(A[a,a]-A[b,b]))
 # Float proposals are followed by exact rational orthogonality/residual certificates.
 t=s.Rational(round(math.tan(angle/2)*2**38),2**38)
 c=(1-t*t)/(1+t*t);ss=2*t/(1+t*t);G=s.eye(4);G[a,a]=G[b,b]=c;G[a,b]=-ss;G[b,a]=ss
 assert G.T*G==s.eye(4)
 A=G.T*A*G;Q=Q*G;rotations+=1
assert Q.T*Q==s.eye(4)
j=max(range(4),key=lambda j:A[j,j]);u=Q[:,j];fit=RR(u)
assert U(u).conjugate().T*U(u)==I and fit.det()==1
assert fsq(K-Q*s.diag(*A.diagonal())*Q.T)<=tau*tau
assert s.simplify((u.T*K*u)[0]-A[j,j])==0
# Actual conditional coherent-memory source with two on-site logical factors.
NP=[np.array(x,dtype=complex) for x in P]
def kron(*xs):
 a=np.array([[1]],complex)
 for x in xs:a=np.kron(a,x)
 return a
def ptrace(a,keep,dims):
 n=len(dims);a=a.reshape(tuple(dims)*2);dims=list(dims)
 for i in reversed(range(n)):
  if i not in keep:a=np.trace(a,axis1=i,axis2=i+len(dims));dims.pop(i)
 return a.reshape(math.prod(dims),math.prod(dims))
def embed(a,sites,n):
 rest=[i for i in range(n) if i not in sites];order=list(sites)+rest
 z=kron(a,np.eye(2**len(rest))).reshape([2]*(2*n));perm=[order.index(i) for i in range(n)]
 return z.transpose(perm+[x+n for x in perm]).reshape(2**n,2**n)
def permutation(order):
 out=np.zeros((2**len(order),2**len(order)),complex)
 for k in range(2**len(order)):
  bits=[(k>>(len(order)-1-i))&1 for i in range(len(order))];nb=[bits[i] for i in order];dest=sum(x<<(len(order)-1-i) for i,x in enumerate(nb));out[dest,k]=1
 return out
vq=[np.array(U(q),complex) for q in[quats[4],quats[1]]];rots=[np.array(RR(q),float) for q in[quats[4],quats[1]]]
# Input order L0,L1,G; physical order L1,G,L0. Unknown matching pi=(2,0).
perm=permutation([1,2,0]);hidden=perm@kron(*vq,np.eye(2));mapping=[2,0]
t=1/97;aa=(1-t*t)/(1+t*t);bb=2*t/(1+t*t)
V=np.array([[aa,0],[0,bb],[0,aa],[bb,0]],complex)
H=np.array([[1,1],[1,-1]])/math.sqrt(2)
VA=V@np.diag([3/5,4/5]);VB=kron(np.eye(2),H)@V@np.diag([4/5,3/5])
assert np.linalg.norm(VA.conj().T@VA+VB.conj().T@VB-np.eye(2))<1e-12
pA=np.array([.35,.25,.10,.30]);pB=np.array([.55,.20,.05,.20])
for probs in[pA,pB]:
 assert probs[0]>=max(probs[1:]) and probs.sum()==1
 assert probs[0]+probs[1]-probs[2]-probs[3]>=.2-1e-12
 assert probs[0]+probs[3]-probs[1]-probs[2]>=.2-1e-12
assert pA[0]+pA[2]-pA[1]-pA[3]<0 # no hidden Y-margin assumption
Uext=kron(hidden,np.eye(2))
def output(l,sigma):
 out=np.zeros((16,16),complex)
 for pa,paA,paB in zip(NP,pA,pB):
  pp=kron(pa,pa);g=paA*VA@sigma@VA.conj().T+paB*VB@sigma@VB.conj().T
  out+=kron(pp@l@pp.conj().T,g)
 return Uext@out@Uext.conj().T
psi=np.array([1,1j])/math.sqrt(2);sigmas=[np.outer(psi,psi.conj())];branchps=[]
for axes,signs,outaxes,outs in[((1,1),(1,-1),(2,3,1),(1,-1,1)),((3,1),(-1,1),(3,2,1),(-1,1,1))]:
 l=kron(*((NP[0]+ss*NP[j])/2 for j,ss in zip(axes,signs)))
 eff=kron(*((NP[0]+ss*NP[j])/2 for j,ss in zip(outaxes,outs)))
 post=ptrace(kron(eff,NP[0])@output(l,sigmas[-1])@kron(eff,NP[0]),[3],[2]*4);pr=np.trace(post).real;assert pr>1e-8
 branchps.append(float(pr));sigmas.append(post/pr)
res=[];born=0;negative_y=[];margins=[]
for hi,sigma in enumerate(sigmas):
 wA=float(np.trace(VA@sigma@VA.conj().T).real);wB=1-wA;probs=wA*pA+wB*pB
 lx=probs[0]+probs[1]-probs[2]-probs[3];lz=probs[0]+probs[3]-probs[1]-probs[2];ly=probs[0]+probs[2]-probs[1]-probs[3]
 margins.append([lx,lz]);negative_y.append(ly)
 mean=[np.zeros((3,3)) for i in range(2)]
 for axes in itertools.product([1,3],repeat=2):
  for signs in itertools.product([-1,1],repeat=2):
   l=kron(*((NP[0]+ss*NP[j])/2 for j,ss in zip(axes,signs)));rho=ptrace(output(l,sigma),[0,1,2],[2]*4)
   for a in itertools.product([1,2,3],repeat=3):
    for b in itertools.product([-1,1],repeat=3):
     e=kron(*((NP[0]+ss*NP[j])/2 for j,ss in zip(a,b)));pr=float(np.trace(e@rho).real)/(16*27);assert pr>=-1e-12
     for i in range(2):mean[i][a[mapping[i]]-1,axes[i]-1]+=pr*6*signs[i]*b[mapping[i]]
     born+=1
 for i in range(2):res.append(float(np.linalg.norm(mean[i]-rots[i]@np.diag([lx,0,lz]))))
 # Coarse true-site matching, direct actual input-state enumeration.
 for i in range(2):
  contrast=[np.zeros((2,2),complex) for _ in range(3)]
  for signs in itertools.product([-1,1],repeat=2):
   l=kron(*((NP[0]+ss*NP[1])/2 for ss in signs));rho=ptrace(output(l,sigma),[0,1,2],[2]*4)
   for site in range(3):contrast[site]+=signs[i]*ptrace(rho,[site],[2]*3)/4
  for site in range(3):
   if site==mapping[i]:assert np.linalg.norm(contrast[site],'nuc')>=.2-1e-12
   else:res.append(float(np.linalg.norm(contrast[site])))
 # Frozen product-rotation error is gauge/memory independent; noisy errors remain correlated.
 small=np.array(U(stereo([s.Rational(1,71),0,s.Rational(-1,89)])),complex)
 W=kron(small,small);f0=abs(np.trace(W))**2/16;ell0=1-f0
 noisyfe=sum(float(probs[a])*abs(np.trace(W@kron(NP[a],NP[a])))**2/16 for a in range(4));oracle=1-probs[0]
 assert -1e-12<=1-noisyfe-oracle<=ell0+1e-12
resmax=max(res);assert resmax<2e-10
# Fixed finite confidence caps checked with rational thresholds, no float logarithm.
caps=[]
for q,n,eps,kap,beta in[(1,3,s.Rational(1,4),s.Rational(1,5),s.Rational(1,16)),(4,20,s.Rational(1,8),s.Rational(1,2),s.Rational(1,64)),(20,32,s.Rational(1,20),s.Rational(1,4),s.Rational(1,100))]:
 def clog(x):
  k=0
  while 2**k<x:k+=1
  return k
 L1=clog(24*q/beta);N1=s.ceiling(4096*q*L1/(kap*kap*eps));exponent=N1*kap*kap*eps/(3456*q)
 assert exponent>=L1
 a2=kap*kap*eps/(8*q);delta=kap*eps/(32*q);loss=2*a2/(kap*kap)+delta/kap
 assert q*loss==9*eps/32
 caps.append({'q':q,'n':n,'L1':L1,'N1':int(N1),'global_good_event_bound':str(q*loss)})
source=Path(__file__).with_name('ordinary_onsite_two_axis_frozen_memory_recovery_20261028.md')
out={'status':'PASS_ZERO_SOURCE_EXACT_AND_BORN_LAW_DIAGNOSTIC','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'source_calls':0,'RNG_draws':0,'acquired_learner_run':False,'exact_rotation_curvature_K_cases':exact,'improper_rotation_obstruction_checked':True,'rational_Jacobi_rotations':rotations,'Jacobi_fixed_cap':cap,'Jacobi_F_residual_squared_upper':str(tau*tau),'exact_rational_SU2_control_certified':True,'actual_Born_record_terms':born,'conditional_memory_states':3,'conditional_memory_commutator_norm':max(float(np.linalg.norm(x@y-y@x)) for x in sigmas for y in sigmas),'actual_prefix_branch_probabilities':branchps,'conditional_XZ_margins':margins,'conditional_Y_contrasts':negative_y,'negative_Y_admissible_CP_component':True,'max_Born_law_residual':resmax,'fixed_bank_caps':caps,'scope':'Only prescribed-matrix/exact rational rotation fitting and actual Born-law enumeration. No sampled count acquisition, unknown-encoder experiment, practical timing or hardware compilation. Source truth used only in diagnostics.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
