import numpy as np, math, json
from fractions import Fraction
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1])
def kron(xs):
 r=np.array([[1.]])
 for x in xs:r=np.kron(r,x)
 return r
J=[sum(kron([p if j==i else I for j in range(4)]) for i in range(4))/2 for p in [X,Y,Z]]
e,v=np.linalg.eigh(sum(j@j for j in J));E4=v[:,e<1e-9]
sing=np.array([0,1,-1,0])/np.sqrt(2)
out=[]
for n in [4,6,8,10]:
 D=2**n;m=n//2;E=E4
 for k in range((n-4)//2):E=np.kron(E,sing[:,None])
 signs=np.array([(-1)**sum((x>>(n-1-i))&1 for i in range(0,n,2)) for x in range(D)])
 E=signs[:,None]*E
 F=np.zeros((D,n+1))
 for x in range(D):w=x.bit_count();F[x,w]=1/math.sqrt(math.comb(n,w))
 A=(F.T@E).conj().T@(F.T@E);ev,es=np.linalg.eigh(A);w=float(ev[-1]);wf=Fraction(4*2**m,3*math.comb(n,m))
 assert abs(w-float(wf))<1e-12 and abs(ev[0])<1e-12
 raw=2*w-w*w;resetgain=w-w*w;complete=raw-resetgain
 # Direct physical Kraus decode, optimized reset onto rank-one eigenvector.
 UE=E-2*F@(F.T@E);K=E.conj().T@UE;leak=np.eye(2)-K.conj().T@K;tau=np.outer(es[:,-1],es[:,-1].conj())
 Fe=(abs(np.trace(K))**2+np.trace(tau@leak).real)/4
 assert abs((1-Fe)-w)<1e-12
 ds=[]
 for i in range(1,n):
  ix=np.arange(D);b0=(ix>>(n-1))&1;bi=(ix>>(n-1-i))&1;swap=ix^((b0^bi)<<(n-1))^((b0^bi)<<(n-1-i))
  # Twisted swap W swap W; F^dag S F determines commutator norm.
  SF=signs[:,None]*signs[swap,None]*F[swap];B=F.T@SF
  delta=4*((n+1)-np.sum(abs(B)**2))/D;ds.append(delta)
 assert sum(ds)<=4*(n*n-1)/D+1e-12
 out.append(dict(n=n,w=w,raw_loss=raw,completed_loss=1-Fe,star_loss=sum(ds),ratio=w/sum(ds),rank_eigenvalues=ev.tolist(),star_deltas=ds))
exact=[]
for n in [20,40,80,160]:
 lower=Fraction(2**(n//2),3*(n*n-1));exact.append(dict(n=n,ratio_lower_bound=str(lower),ratio_lower_float=float(lower)))
blocks=[]
for h in [1,2,3]:
 n=4*h;D=2**n;Kdim=2**h;E=kron([E4]*h)
 signs=np.array([(-1)**sum((x>>(n-1-i))&1 for i in range(0,n,2)) for x in range(D)])
 E=signs[:,None]*E;dicke=np.array([1/math.sqrt(math.comb(n,n//2)) if x.bit_count()==n//2 else 0 for x in range(D)])
 v=E.conj().T@dicke;A=np.outer(v,v.conj());w=np.vdot(v,v).real
 wf=Fraction(16**h,3**h*math.comb(n,n//2));assert abs(w-float(wf))<1e-12
 raw=4*w/Kdim-4*w*w/Kdim**2;gain=4*(w-w*w)/Kdim**2;loss=raw-gain
 lower=4*w*(Kdim-1)/Kdim**2;assert abs(loss-lower)<1e-12
 blocks.append(dict(h=h,n=n,K=Kdim,w=w,raw_loss=raw,optimal_reset_completed_loss=loss,ratio_lower_bound=float(Fraction((2**h-1)*8**h,2**h*3**h*(n*n-1)))))
result=dict(full_product_block_checks=blocks,scope='Pointwise same-star-loss transfer obstruction, not sample/computational separation',finite_matrix_checks=out,exact_ratio_bounds=exact)
print(json.dumps(result,indent=2));open(__file__.replace('.py','.json'),'w').write(json.dumps(result,indent=2)+'\n')
