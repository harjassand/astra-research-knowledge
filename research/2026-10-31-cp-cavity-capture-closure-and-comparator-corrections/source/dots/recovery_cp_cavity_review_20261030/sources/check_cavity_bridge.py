"""Finite two-site, two-time regression. No numerical test substitutes for theorem.
Individual HP summand is non-GKSL; the total and all cavity evolutions are CPTP.
Unnormalized Choi trace norms give conservative upper bounds on diamond norms.
"""
import itertools,json,numpy as np
from scipy.linalg import expm
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
d=4
ops={'X0':np.kron(X,I),'X1':np.kron(I,X),'Y0':np.kron(Y,I),'Z0':np.kron(Z,I),'Z1':np.kron(I,Z),'XX':np.kron(X,X)}
def smap(f):
 return np.column_stack([f(np.eye(d*d,dtype=complex)[:,k].reshape(d,d)).reshape(-1) for k in range(d*d)])
def diss(U):return smap(lambda A:U@A@U.conj().T-A)
def ham(H):return smap(lambda A:-1j*(H@A-A@H))
def traceout(A,R):
 remain=[i for i in range(2) if i not in R];out=np.zeros((2**len(remain),)*2,complex)
 for i,j in itertools.product(range(d),repeat=2):
  bi=((i>>1)&1,i&1);bj=((j>>1)&1,j&1)
  if all(bi[k]==bj[k] for k in R):
   a=sum(bi[k]<<(len(remain)-1-l) for l,k in enumerate(remain));b=sum(bj[k]<<(len(remain)-1-l) for l,k in enumerate(remain));out[a,b]+=A[i,j]
 return out
# For superoperators P_R(N) = identity on selected sites times reduced N.
def cavity(N,R):
 R=set(R)
 if not R:return N.copy()
 remain=[i for i in range(2) if i not in R];dr=2**len(remain)
 def reduced(B):
  E=np.zeros((d,d),complex)
  for i,j in itertools.product(range(d),repeat=2):
   bi=((i>>1)&1,i&1);bj=((j>>1)&1,j&1)
   if all(bi[k]==bj[k] for k in R):
    a=sum(bi[k]<<(len(remain)-1-l) for l,k in enumerate(remain));b=sum(bj[k]<<(len(remain)-1-l) for l,k in enumerate(remain));E[i,j]=B[a,b]/2**len(R)
  return traceout((N@E.reshape(-1)).reshape(d,d),R)
 def apply(A):
  out=np.zeros_like(A)
  # Apply reduced map separately in each selected-site matrix block.
  rlist=sorted(R)
  for ri,rj in itertools.product(range(2**len(R)),repeat=2):
   ii=[];jj=[]
   for x in range(dr):
    bits=[0,0];bits2=[0,0]
    for l,k in enumerate(remain):bits[k]=bits2[k]=(x>>(len(remain)-1-l))&1
    for l,k in enumerate(rlist):bits[k]=(ri>>(len(R)-1-l))&1;bits2[k]=(rj>>(len(R)-1-l))&1
    ii.append(2*bits[0]+bits[1]);jj.append(2*bits2[0]+bits2[1])
   block=A[np.ix_(ii,jj)];out[np.ix_(ii,jj)]=reduced(block)
  return out
 return smap(apply)
def choi(S):
 J=np.zeros((d*d,d*d),complex)
 for i,j in itertools.product(range(d),repeat=2):
  A=np.zeros((d,d),complex);A[i,j]=1;B=(S@A.reshape(-1)).reshape(d,d)
  J[i*d:(i+1)*d,j*d:(j+1)*d]=B
 return J
def subsets(S):
 S=list(S)
 return [frozenset(S[k] for k in range(len(S)) if mask>>k&1) for mask in range(2**len(S))]
locs=frozenset(range(4));tau=1.;rows=[]
for mu in [1e-5,1e-4,1e-3]:
 N1=mu*(diss(ops['Z0'])-diss(ops['X0'])) # deliberately not GKSL
 N2=mu*(diss(ops['X0'])+diss(ops['XX']))
 N=N1+N2;eta=8*mu;x=np.sqrt(6*eta*tau)
 Hs=[ham(.2*ops['X0']+.3*ops['Z1']),ham(.4*ops['Y0']+.2*ops['X1'])]
 Ts={}
 for R in subsets(locs):
  Ts[R]=np.eye(d*d,dtype=complex)
  for layer in range(2):
   r={j-2*layer for j in R if 2*layer<=j<2*layer+2}
   Ts[R]=expm(tau*(Hs[layer]+cavity(N,r)))@Ts[R]
 min_cp=min(np.linalg.eigvalsh(choi(T)).min() for T in Ts.values())
 bad_min=float(np.linalg.eigvalsh(choi(expm(N1))).min())
 E={F:sum(((-1)**len(A))*Ts[(locs-F)|A] for A in subsets(F)) for F in subsets(locs)}
 reconstruction=np.linalg.norm(sum(E.values())-Ts[frozenset()])
 max_cancel=0.;ratios=[]
 for S in subsets(locs):
  if not S:continue
  incl=sum(T for F,T in E.items() if S<=F)
  finite=sum(((-1)**len(R))*Ts[R] for R in subsets(S))
  max_cancel=max(max_cancel,np.linalg.norm(incl-finite))
  # Choi nuclear norm is a valid dimension-conservative diamond upper bound.
  upper=np.linalg.norm(choi(finite),ord='nuc');bound=x**len(S)
  ratios.append(float(upper/bound))
 assert min_cp>-1e-10 and bad_min<0 and reconstruction<1e-10 and max_cancel<1e-10 and max(ratios)<1
 rows.append(dict(mu=mu,cavity_min_choi_eigenvalue=float(min_cp),nonCP_summand_choi_eigenvalue=bad_min,reconstruction_residual=float(reconstruction),inclusive_cancellation_residual=float(max_cancel),max_choi_bound_ratio=max(ratios)))
print(json.dumps({'scope':'finite regression only','q':2,'g':1,'locations':4,'tests':rows},indent=2))
