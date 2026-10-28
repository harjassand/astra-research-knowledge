#!/usr/bin/env python3
"""Independent adaptive calibration tree, general decoder stress, and record cancellation."""
from pathlib import Path
import json,itertools,math
import numpy as np
import sympy as s
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);P=[X,Y,Z]
p=s.Rational(1,4);z=(12-5*s.I)/13;V=s.diag(z,s.conjugate(z));c=s.Rational(119,169);ss=s.Rational(120,169)
def noise(rho):return (1-p)*rho+p*Z*rho*Z
def probs(hist,world):
 # Real classical feedback selects both next preparation and next readout.
 num=sum((i+1)*(b+1) for i,b in enumerate(hist));A=P[num%3];B=P[(num+len(hist)+1)%3]
 sign=1 if (num+len(hist))%2 else -1;rho=(I+sign*A)/2;U=V if world==1 else V.H;out=U*noise(rho)*U.H
 return [s.simplify(s.trace((I+b*B)*out)/2) for b in [-1,1]]
conditional=0;trees=[]
for N in range(1,7):
 laws=[{():s.S.One},{():s.S.One}]
 for t in range(N):
  fresh=[{},{}]
  for hist in laws[0]:
   pair=[probs(hist,w) for w in [1,-1]]
   bc=sum(s.sqrt(a*b) for a,b in zip(*pair));assert float(s.N(bc-c,50))>=-1e-45;conditional+=1
   for wi in range(2):
    for bit,prob in zip([-1,1],pair[wi]):fresh[wi][hist+(bit,)]=laws[wi][hist]*prob
  laws=fresh
 assert sum(laws[0].values())==1 and sum(laws[1].values())==1
 bc=sum(s.sqrt(laws[0][h]*laws[1][h]) for h in laws[0]);tv=sum(abs(laws[0][h]-laws[1][h]) for h in laws[0])/2
 assert float(s.N(bc-c**N,50))>=-1e-45
 assert float(s.N(tv*tv-(1-bc*bc),50))<=1e-45
 trees.append({'N':N,'histories':2**N,'BC':float(bc),'TV':float(tv),'BC_lower':float(c**N)})
# Numeric general CPTP decoders from Haar-isometry QR, not only fitted rotations.
rng=np.random.default_rng(202610282018);In=np.eye(2);Zn=np.diag([1,-1]);plus=np.array([1,1])/np.sqrt(2);minus=np.array([1,-1])/np.sqrt(2)
psi=np.sqrt(.75)*np.kron(plus,[1,0])+np.sqrt(.25)*np.kron(minus,[0,1]);target=np.outer(psi,psi.conj())
Vn=np.diag([complex(z),complex(s.conjugate(z))]);worlds=[np.kron(U,In)@target@np.kron(U.conj().T,In) for U in [Vn,Vn.conj().T]]
def loss(Ks,rho):
 out=sum(np.kron(K,In)@rho@np.kron(K.conj().T,In) for K in Ks)
 return np.linalg.eigvalsh(out-target).__abs__().sum()/2
ratios=[];tp=0
for j in range(512):
 M=rng.normal(size=(8,2))+1j*rng.normal(size=(8,2));Q,_=np.linalg.qr(M);Ks=[Q[2*k:2*k+2] for k in range(4)]
 tp=max(tp,np.linalg.norm(sum(K.conj().T@K for K in Ks)-In,ord=2))
 losses=[loss(Ks,rho) for rho in worlds];ratio=sum(losses)/(.25*float(ss));assert ratio>=1-1e-12;ratios.append(ratio)
# Exact record cancellation at true orientation zero.
ps=s.sqrt(1-p)*s.kronecker_product(s.Matrix([1,1])/s.sqrt(2),s.Matrix([1,0]))+s.sqrt(p)*s.kronecker_product(s.Matrix([1,-1])/s.sqrt(2),s.Matrix([0,1]));R=ps*ps.H
outs=[s.kronecker_product(U,I)*R*s.kronecker_product(U.H,I) for U in [V,V.H]]
def trdist(A):return s.simplify(sum(abs(a)*b for a,b in A.eigenvals().items())/2)
conditional_loss=trdist(outs[0]-R);averaged_loss=trdist((outs[0]+outs[1])/2-R)
assert conditional_loss==s.Rational(5,13) and averaged_loss==s.Rational(25,169)
out={'status':'PASS_RECORD_RETAINING_LOWER_BOUND_INDEPENDENT_CHECKS','source_draws':0,'numeric_random_decoder_draws':512,'conditional_tree_nodes':conditional,'adaptive_trees':trees,'min_arbitrary_CPTP_decoder_separation_ratio':min(ratios),'maximum_TP_residual':tp,'exact_retained_record_cancellation_loss':str(conditional_loss),'exact_discarded_record_loss':str(averaged_loss),'scope':'Exact rational adaptive probability trees evaluated to50digits; analytic proof supplies general bounds. Decoder stress is floating numerical evidence, not proof or acquired data.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
