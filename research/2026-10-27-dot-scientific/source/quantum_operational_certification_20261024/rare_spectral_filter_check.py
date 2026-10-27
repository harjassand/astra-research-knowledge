"""Corroboration, not substitute for operator proof: arbitrary rank/coefficients and coherent uncompute."""
import numpy as np
rng=np.random.default_rng(20261027)
def state(n):
 z=rng.normal(size=(n,n))+1j*rng.normal(size=(n,n));x=z@z.conj().T;return x/np.trace(x)
def adj(s,h,X):
 c=np.cos(h);v=np.sin(h)
 return c*c*X+v*v*np.trace(s@X)*np.eye(len(s))-1j*c*v*(s@X-X@s)
count=0;ranks=set()
for n in [3,5,8,12]:
 for A,B in [(4,6),(.01,3),(7,.3),(.001,.002),(100,70)]:
  ell=A+B
  for rep in range(10):
   s=state(n);t=state(n);ev,U=np.linalg.eigh(A*s-B*t)
   # Every spectral projector commutes with H; stress arbitrary rank as well as positive band.
   for mask in [ev>0,np.arange(n)>=n//2]:
    P=U[:,mask]@U[:,mask].conj().T;ranks.add(int(sum(mask)))
    W=max(np.trace(P@s).real,np.trace(P@t).real)
    for angle in [-1,-.1,-.0001,.01,.5,1]:
     delta=angle/ell
     exact=adj(s,A*delta,adj(t,-B*delta,P))
     bound=(1+8*ell**2*delta**2)*P+8*ell**2*delta**2*W*np.eye(n)
     assert np.linalg.eigvalsh(bound-exact).min()>-1e-11
     count+=1
# QPE compute/classify/uncompute on several different eigenphases, retaining same positive-band bit.
M=64;k=np.arange(M);F=np.exp(2j*np.pi*np.outer(k,k)/M)/np.sqrt(M)
# Any unitary sending |0> to uniform works; use DFT as preparation.
mask=((k/M)>=.3)&((k/M)<.75)
maxratio=0
for phase in [.05,.22,.28,.34,.41,.51]:
 Q=F.conj().T@np.diag(np.exp(2j*np.pi*k*phase))@F
 v=Q[:,0];accepted=Q.conj().T@(mask*v);rejected=Q.conj().T@((~mask)*v)
 positive=.3<=phase<.75
 wrong=np.sum(abs(v[~mask if positive else mask])**2)
 ideal=np.zeros(M);ideal[0]=1
 err=np.linalg.norm(accepted-(ideal if positive else 0))**2+np.linalg.norm(rejected-(0 if positive else ideal))**2
 assert abs(err-2*wrong)<1e-12
 assert abs(np.vdot(accepted,accepted).real-np.sum(abs(v[mask])**2))<1e-12
 maxratio=max(maxratio,err/(wrong or 1))
print('PASS:',count,'arbitrary-rank/operator coefficient cases; ranks',sorted(ranks))
print('PASS: six coherent QPE uncompute cases; squared isometry error / classification error =',maxratio)
