import numpy as np,cvxpy as cp,json,argparse,time
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import LinearOperator,expm_multiply
from math import sqrt
from pathlib import Path
HERE=Path(__file__).resolve().parent
from itertools import combinations
exec((HERE / 'yangian_gap.py').read_text().split('for n in map(int,sys.argv')[0])
PAULI=[np.eye(2),np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
def paths(n):
 p=[()]
 for _ in range(n):p=[a+(b,) for a in p for b in [(a[-1] if a else 0)-1,(a[-1] if a else 0)+1] if b>=0]
 return sorted(p)
def chi_sum(n):
 d=2**n;R=[];C=[];V=[]
 def sw(x,i,j):return x if ((x>>(n-1-i))&1)==((x>>(n-1-j))&1) else x^(1<<(n-1-i))^(1<<(n-1-j))
 for i,j,k in combinations(range(n),3):
  for b in range(d):
   R.extend([sw(sw(b,j,k),i,j),sw(sw(b,i,j),j,k)]);C.extend([b,b]);V.extend([2j,-2j])
 return coo_matrix((V,(R,C)),shape=(d,d)).tocsr()
def build(n):
 Q,groups=schur(n);d=2**n;js=sorted(set(j for j,m in groups));mult={j:len(groups[j,j]) for j in js};offset={};size=0
 for j in js:offset[j]=size;size+=mult[j]**2
 yz=Q.T@(Yz(n)@Q);hfull=Q.T@(chi_sum(n)@Q)/8;H={j:hfull[np.ix_(groups[j,j],groups[j,j])] for j in js};del hfull
 blocks={};S={j:np.zeros((mult[j],mult[j]),complex) for j in js}
 for j in js:
  for k in js:
   if abs(j-k)>2:continue
   YY=[yz[np.ix_(groups[j,m],groups[k,m])] for m in range(-min(j,k),min(j,k)+1,2)];blocks[j,k]=YY
   for A in YY:S[j]+=A@A.conj().T
 trL=sum((3/(8*(j+1)))*mult[j]*np.trace(S[j]).real for j in js)
 def unpack(v):return {j:v[offset[j]:offset[j]+mult[j]**2].reshape(mult[j],mult[j])/sqrt(j+1) for j in js}
 def pack(X):return np.concatenate([sqrt(j+1)*X[j].reshape(-1) for j in js])
 def apply(v,adj=False):
  X=unpack(np.asarray(v).reshape(-1));R={j:S[j]@X[j]+X[j]@S[j] for j in js}
  for (j,k),YY in blocks.items():
   for A in YY:R[j]-=2*A@X[k]@A.conj().T
  return pack({j:-(3/(32*(j+1)))*R[j]+(-1j if adj else 1j)*(H[j]@X[j]-X[j]@H[j]) for j in js})
 G=LinearOperator((size,size),matvec=apply,rmatvec=lambda v:apply(v,True),dtype=complex)
 perm=np.array([(b>>1)+((b&1)<<(n-1)) for b in range(d)]);Qlast=np.zeros_like(Q);Qlast[perm,:]=Q
 rec={j:Qlast[:,groups[j,j]].T@Q[:,groups[j,j]] for j in js};allpaths=paths(n);parent={}
 for j in js:
  pp=[p for p in allpaths if p[-1]==j]
  for k in [j-1,j+1]:
   ids=[i for i,p in enumerate(pp) if (p[-2] if n>1 else 0)==k]
   if ids:parent[j,k]=ids
 return dict(n=n,Q=Q,groups=groups,js=js,mult=mult,size=size,G=G,traceG=-trL/2,pack=pack,unpack=unpack,rec=rec,parent=parent)
def frame(k,name='triad'):
 z=np.array([1,0],complex);x=np.array([1,1],complex)/sqrt(2);y=np.array([1,1j],complex)/sqrt(2);seq={'triad':[z,x,y],'zx':[z,x],'z':[z]}[name];psi=np.array([1.],complex)
 for i in range(k):psi=np.kron(psi,seq[i%len(seq)])
 return psi
def initial(B,psi):
 Q=B['Q'];groups=B['groups'];js=B['js'];vectors=[Q.T@np.kron(np.eye(2)[:,a],psi) for a in range(2)];out=[]
 for P in PAULI:
  X={}
  for j in js:
   X[j]=np.zeros((B['mult'][j],B['mult'][j]),complex)
   for mm in range(-j,j+1,2):
    v=[vec[groups[j,mm]] for vec in vectors]
    for a in range(2):
     for b in range(2):X[j]+=P[a,b]*np.outer(v[a],v[b].conj())/(2*(j+1))
  out.append(B['pack'](X))
 return np.stack(out,axis=1)
def output_blocks(B,V):
 out={}
 for mu in range(4):
  X=B['unpack'](V[:,mu]);Y={}
  for j in B['js']:
   Xj=B['rec'][j]@X[j]@B['rec'][j].T
   for (jj,k),ids in B['parent'].items():
    if jj!=j:continue
    Y[k]=Y.get(k,0)+(j+1)*Xj[np.ix_(ids,ids)]
  for k,C in Y.items():out.setdefault(k,[]).append((C+C.conj().T)/2)
 return out
def inverse_quarter(X):
 e,U=np.linalg.eigh((X+X.conj().T)/2);a=np.zeros_like(e);ids=e>1e-12;a[ids]=e[ids]**(-.25);return (U*a)@U.conj().T
def evaluate(B,V,decoder=True):
 out=output_blocks(B,V);a=0;Fe=0;records=[]
 for j,C in out.items():
  inv=inverse_quarter(C[0]);a+=sum(np.linalg.norm(inv@x@inv,'fro')**2 for x in C[1:])/3
  rho=sum(np.kron(P.T,x) for P,x in zip(PAULI,C))/2;rho=(rho+rho.conj().T)/2;dim=C[0].shape[0];p=np.trace(C[0]).real
  if decoder:
   if dim==1:f=np.linalg.eigvalsh(rho)[-1]/2
   else:
    Z=cp.Variable((dim,dim),hermitian=True);prob=cp.Problem(cp.Minimize(cp.real(cp.trace(Z))/2),[cp.kron(np.eye(2),Z)-rho>>0]);prob.solve(solver='CLARABEL',tol_gap_abs=2e-8,tol_feas=2e-8,tol_gap_rel=2e-8,max_iter=150);f=prob.value
   Fe+=f
  records.append([j,dim,p])
 return dict(a=float(a),Fe_opt=float(Fe),trace=float(sum(r[2] for r in records)),blocks=records)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--k',type=int,nargs='+',default=[2,3,4,5]);ap.add_argument('--t',type=float,nargs='+',default=[.1,.3,.7,1.,1.5,3.]);ap.add_argument('--frame',default='triad');ap.add_argument('--skip-decoder',action='store_true');args=ap.parse_args()
 for k in args.k:
  start=time.time();B=build(k+1);V0=initial(B,frame(k,args.frame));print(json.dumps(dict(k=k,size=B['size'],build_seconds=time.time()-start)),flush=True)
  for t in args.t:
   start=time.time();V=expm_multiply(t*B['G'],V0,traceA=t*B['traceG']);ans=evaluate(B,V,not args.skip_decoder);ans.update(k=k,t=t,frame=args.frame,seconds=time.time()-start);print(json.dumps(ans),flush=True)
