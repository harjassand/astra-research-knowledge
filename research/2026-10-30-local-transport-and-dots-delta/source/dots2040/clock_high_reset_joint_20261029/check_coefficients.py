import itertools,json
import numpy as np
I=np.eye(2,dtype=complex);n=np.diag([0,1]).astype(complex);sm=np.array([[0,1],[0,0]],complex);sp=sm.T;B=[I,n,sp,sm];P=I-n;X=sm+sp

def tensor(xs):
 r=np.ones((1,1),complex)
 for x in xs:r=np.kron(r,x)
 return r

def check(name,N,edges):
 D=max([sum(v in e for e in edges) for v in range(N)]);C=2**(D+2)*(D+1);k=1.;g=1/(8*C);d=2**N;ident=np.eye(d)
 H=np.zeros((d,d),complex)
 for x in range(N):
  near={v if u==x else u for u,v in edges if x in (u,v)}
  H+=g*tensor([X if z==x else P if z in near else I for z in range(N)])
 LH=1j*(np.kron(ident,H)-np.kron(H.T,ident));LD=np.zeros_like(LH)
 for x in range(N):
  b=tensor([sm if z==x else I for z in range(N)]);nn=b.T@b
  LD+=k*(np.kron(b.T,b.T)-.5*np.kron(ident,nn)-.5*np.kron(nn.T,ident))
 labels=list(itertools.product(range(4),repeat=N));T=np.column_stack([tensor([B[a] for a in lab]).reshape(-1,order='F') for lab in labels]);Ti=np.linalg.inv(T)
 KH=Ti@LH@T;KD=Ti@LD@T;K=KH+KD;sizes=np.array([sum(a!=0 for a in lab) for lab in labels]);rates=np.array([sum(1 if a==1 else .5 if a else 0 for a in lab) for lab in labels])
 residual=np.max(np.abs(KD+np.diag(rates)))
 columnH=np.abs(KH).sum(axis=0);ratio=max(columnH[1:]/sizes[1:])/g
 off=np.abs(K);np.fill_diagonal(off,0);logs=np.real(np.diag(K))+off.sum(axis=0)
 Q=K[1:,1:];offQ=np.abs(Q);np.fill_diagonal(offQ,0);qlogs=np.real(np.diag(Q))+offQ.sum(axis=0)
 lam=.5-C*g
 assert residual<1e-9 and logs.max()<1e-9 and qlogs.max()<=-lam+1e-9 and ratio<=C+1e-9
 return dict(graph=name,N=N,D=D,C=C,actual_H_column_per_g_support=ratio,damping_residual=float(residual),full_log_norm=float(logs.max()),quotient_log_norm=float(qlogs.max()),claimed_bound=-lam)
if __name__=='__main__':
 print(json.dumps([check('isolated',1,[]),check('edge',2,[(0,1)]),check('path4',4,[(0,1),(1,2),(2,3)]),check('star3',4,[(0,1),(0,2),(0,3)]),check('clique4',4,list(itertools.combinations(range(4),2)))],indent=2))
