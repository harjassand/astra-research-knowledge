#!/usr/bin/env python3
"""Independent-form algebra and numerical regression for coherent receiver candidate."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
import numpy as np,sympy as s,mpmath as mp
from scipy.linalg import expm
from exact_source_overlap import certify_overlap,sqrt_up
import exact_source_overlap as eo
from certify_scalar_budget import receive
from check_coherent_cascade import coh_f,finite_source_f
checks={'exact':0,'floating':0,'high_precision':0}
def exact(q):assert q;checks['exact']+=1

def close(a,b,tol=1e-10):assert abs(a-b)<tol,(a,b);checks['floating']+=1
# Projection generator, not merely a fitted source channel.
l,b=s.symbols('l b',positive=True,real=True);c=s.sqrt(l)*b
B=s.Matrix([[-2*b*b,c],[c,-l/2-2*b*b]])
exact(s.simplify(B.det()-4*b**4)==0);exact(s.simplify(B.trace()+l/2+4*b*b)==0)
sm=s.Matrix([[0,1],[0,0]]);X=sm+sm.T;Q=sm.T*sm
A=-s.I*c*X-l*Q/2+2*s.I*b*s.sqrt(l)*sm-2*b*b*s.eye(2)
U=s.diag(1,-s.I);exact(s.simplify(U.H*A*U-B)==s.zeros(2))
# Rational exact contraction-overlap geometry (no random floating acceptance).
for m,n in [(1,2),(2,3),(3,4),(1,10)]:
 phase=F(m*m-n*n,m*m+n*n)+s.I*s.Rational(2*m*n,m*m+n*n)
 O=s.diag(phase,s.conjugate(phase));v=s.Matrix([s.Rational(3,5),s.Rational(4,5)]);w=s.Matrix([-s.Rational(4,5),s.Rational(3,5)])
 for a,zz in [(s.Rational(15,17),s.Rational(8,17)),(s.Rational(99,101),s.Rational(20,101))]:
  psi=a*v+zz*w;f=(psi.H*O*psi)[0];f0=(v.H*O*v)[0]
  R=sqrt_up(F(s.simplify((1-f0)*s.conjugate(1-f0))))
  delta=F(1-a*a);rhs=R+2*delta+2*sqrt_up(2*delta*R)
  exact(F(s.simplify((1-f)*s.conjugate(1-f)))<=rhs*rhs)
# High precision exact-overlap enclosures.
mp.mp.dps=90
for lam in [64,256,1024,4096,16384,65536,10**6]:
 row=certify_overlap(F(lam),F(1,5),F(1));L=mp.mpf(lam);bb=mp.mpf(1)/5;d=mp.sqrt(L*L/16+L*bb*bb);tr=-L/4-2*bb*bb
 val=(1+L/(4*d))/2*mp.exp(tr+d)+(1-L/(4*d))/2*mp.exp(tr-d)
 lo,hi=[mp.mpf(F(x).numerator)/F(x).denominator for x in row['amplitude_interval']]
 assert lo<=val<=hi;checks['high_precision']+=1
# Higher-bit rigorous enclosure overlap, no historical snapshot writes.
old=(eo.BITS,eo.S,eo.DEGREE);prior=certify_overlap(F(4096),F(1,5),F(1));eo.BITS=160;eo.S=1<<160;eo.DEGREE=56
replay=certify_overlap(F(4096),F(1,5),F(1));eo.BITS,eo.S,eo.DEGREE=old
exact(max(F(prior['amplitude_interval'][0]),F(replay['amplitude_interval'][0]))<=min(F(prior['amplitude_interval'][1]),F(replay['amplitude_interval'][1])))
# No silent loss-free or phase-free comparator.
for zeta in [1,.99,.5,0]:
 for T in [0,.01,1,10]:
  f=coh_f(.2,128,T,zeta)
  assert abs(f)<=1+1e-14;checks['floating']+=1
  if zeta==0:close(f,np.exp(-8*.2**2*T))
# Stronger variance-sensitive bound against actual always-on finite-cavity diagnostic.
for lam,k,T in [(64,128,1),(256,128,1),(4096,128,1)]:
 f=finite_source_f(lam,.2,k,0,T,8)
 a=certify_overlap(F(lam),F(1,5),F(T));delta=1-F(a['amplitude_interval'][0])**2
 f0=coh_f(.2,k,T);R=abs(1-f0);ub=R+2*float(delta)+2*np.sqrt(2*float(delta)*R)
 assert abs(1-f)<=ub+1e-10;checks['floating']+=1
# Certified model separation includes both phase and stated extra budget.
row=receive(F(4096),F(1,5),F(128),F(1),F(998001,1000000),F(1,1000))
exact(F(row['actual_total_complete_channel_upper'])<F(1,100));exact(F(row['unchanged_source_complete_channel_lower'])>F(1,5))
# Actual source/data-correlated SWAP handoff diagnostics, source never turned off.
def pt(rho,dims,keep):
 r=rho.reshape(*dims,*dims);dims=list(dims)
 for j in reversed(range(len(dims))):
  if j not in keep:r=np.trace(r,axis1=j,axis2=j+len(dims));dims.pop(j)
 return r.reshape(np.prod(dims),np.prod(dims))
I=np.eye(2);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]);sm=np.array([[0,1],[0,0]],complex)
SW=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
for lam,tau in [(64,.01),(256,.003),(4096,.001)]:
 b=.2;c=np.sqrt(lam)*b;p=4*b*b/lam
 # Order source,old data,output memory,reference; maximally offdiagonal reachable energy envelope.
 vec=np.zeros(16,complex);vec[0]=np.sqrt(1-p);vec[1*8+1*4+0*2+1]=np.sqrt(p)
 rho=np.outer(vec,vec.conj())
 H=c*np.kron(np.kron(X,Z),np.eye(4))+np.kron(np.kron(I,np.pi/(2*tau)*SW),I)
 L=np.sqrt(lam)*np.kron(sm,np.eye(8));Q=L.conj().T@L;Id=np.eye(16)
 G=-1j*(np.kron(Id,H)-np.kron(H.T,Id))+np.kron(L.conj(),L)-.5*(np.kron(Id,Q)+np.kron(Q.T,Id))
 out=(expm(tau*G)@rho.reshape(-1,order='F')).reshape(16,16,order='F')
 W=np.kron(np.kron(I,SW),I);target=W@rho@W.conj().T
 diff=pt(out,[2,2,2,2],[2,3])-pt(target,[2,2,2,2],[2,3]);err=np.linalg.norm(diff,ord='nuc')
 assert err<=16*b*b/lam+8*b*b*tau+1e-10;checks['floating']+=1
out={'checks':checks,'scope':'Exact source projection/geometry and interval replay plus high-precision and full finite-cutoff/channel diagnostics. Handoff test uses actual correlated source, not reset. Not physical calibration or an infinite-mode numerical certificate.'}
Path(__file__).with_name('test_coherent_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
