import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, json,time,os
from pathlib import Path
out=Path(__file__).parent
I2=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1]); I4=np.eye(4)
paulis=[[np.kron(Z,I2),np.kron(I2,Z)],[np.kron(X,I2),np.kron(I2,X)]]
# idle=0; g1=1,2;e1=3,4;g2=5,6;e2=7,8;final=9,10
states=[('idle',0,0)]+[(p,j,b) for p,j in [('g',0),('e',0),('g',1),('e',1),('f',2)] for b in (0,1)]+[('idle',0,0)]
prefix=[]
for a in (0,1):
 q=[]
 for p,j,b in states:
  length=j+(p=='e'); Q=I4.copy()
  for k in range(length):
   if b: Q=paulis[a][k]@Q
  q.append(Q)
 prefix.append(q)
D=144; eye=sp.eye(D,format='csc'); sector=int(os.environ.get("BELL_SECTOR","0")); bell=np.array([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]][sector])/np.sqrt(2)
V=sp.block_diag([(prefix[0][i]@prefix[1][j]@bell).reshape(4,1) for i in range(12) for j in range(12)],format='csc')
def local(O,a):
 return sp.kron(O,sp.eye(12)) if a==0 else sp.kron(sp.eye(12),O)
def physical_edge(a,t,s,P=I4):
 o=sp.csc_matrix(([1.],([t],[s])),shape=(12,12)); return sp.kron(local(o,a),sp.csc_matrix(P),format='csc')
leak=0.
def reduce(O):
 global leak
 R=(V.conj().T@O@V).tocsc(); E=O@V-V@R; leak=max(leak,float(sla.norm(E))); return R
H=sp.csc_matrix((D,D),dtype=complex); dec=[]; prep=[[],[]]; read=[[],[]]
for a in (0,1):
 for j in (0,1):
  edge=sum((physical_edge(a,3+4*j+b,1+4*j+b,paulis[a][j] if b else I4) for b in (0,1)))
  H+=reduce(edge+edge.conj().T)
  L=sum((physical_edge(a,(5 if j==0 else 9)+b,3+4*j+b) for b in (0,1)))
  dec.append(reduce(L))
 for s in (1,-1):
  prep[a].append(reduce((physical_edge(a,1,0)+s*physical_edge(a,2,0))/np.sqrt(2)))
  read[a].append(reduce((physical_edge(a,11,9)+s*physical_edge(a,11,10))/np.sqrt(2)))

for a,sign in enumerate([(1,1),(1,-1),(-1,1),(-1,-1)][sector]):
 if sign<0: read[a]=read[a][::-1]
print('full data off-sector residual',leak,flush=True)
assert leak<1e-12

def gain(L):return sp.kron(L.conjugate(),L,format='csc')
def diss(L):
 A=L.conj().T@L
 return gain(L)-.5*(sp.kron(eye,A,format='csc')+sp.kron(A.T,eye,format='csc'))
base=-1j*(sp.kron(eye,H,format='csc')-sp.kron(H.T,eye,format='csc'))
for L in dec+read[0]+read[1]:base+=diss(L)
tr=np.zeros(D*D);tr[np.arange(D)*(D+1)]=1


# Both token-diagonal density blocks remain invariant exactly.
M=D*D; trace2=np.tile(tr,2); zero=sp.csc_matrix((M,M)); ident=sp.eye(M,format='csc')
handoff=[reduce(physical_edge(a,0,11)) for a in (0,1)]
def loss(J):
 A=J.conj().T@J
 return -.5*(sp.kron(eye,A,format='csc')+sp.kron(A.T,eye,format='csc'))
def steady(L,trace):
 A=L.tolil();A[0,:]=trace;b=np.zeros(len(trace),complex);b[0]=1
 return sla.spsolve(A.tocsc(),b)
def eigmin(v):
 return min(float(np.linalg.eigvalsh((R+R.conj().T)/2).min()) for R in [v[k*M:(k+1)*M].reshape((D,D),order='F') for k in range(len(v)//M)])
records=[]
for p in (0.,.001):
 for mode,r,eta in [('token',1.,e) for e in (0.,.0001,.001,.01)]+[('random',r,.001) for r in (.1,.01)]:
  start=time.time()
  if mode=='token':
   blocks=[[base.copy(),zero.copy()],[zero.copy(),base.copy()]]
   for a in (0,1):
    blocks[a][a]+=r*((1-p)*diss(prep[a][0])+p*diss(prep[a][1]))
    # Explicit separate owner/nonowner handoff jumps; no coherent many-to-one jump.
    for t in (0,1):
     blocks[t][t]+=loss(handoff[a]);blocks[1-a][t]+=gain(handoff[a])
   for t in (0,1):blocks[t][t]-=eta*ident;blocks[1-t][t]+=eta*ident
   L=sp.bmat(blocks,format='csc');trace=trace2
  else:
   # Token is physically present but decoupled, with stationary I/2.
   L=base.copy()
   for a in (0,1):L+=r*((1-p)*diss(prep[a][0])+p*diss(prep[a][1]))+diss(handoff[a])
   trace=tr
  rho=steady(L,trace)
  rec=dict(mode=mode,r=r,token_flip_rate=eta,p=p,trace=float(trace@rho.real),min_eig=eigmin(rho),residual=float(np.linalg.norm(L@rho)),caches=[])
  for a in (0,1):
   Jc=gain(read[a][0]);Jw=gain(read[a][1])
   if mode=='token':Jc=sp.block_diag([Jc,Jc],format='csc');Jw=sp.block_diag([Jw,Jw],format='csc')
   K=L-Jc-Jw;rw=sla.spsolve(K,-Jw@rho)
   rec['caches'].append(dict(wrong=float(trace@rw.real),flux=float(trace@((Jc+Jw)@rho).real),wrong_report_fraction=float((trace@(Jw@rho).real)/(trace@((Jc+Jw)@rho).real)),wrong_min_eig=eigmin(rw),correct_min_eig=eigmin(rho-rw),cache_residual=float(np.linalg.norm(K@rw+Jw@rho))))
  pop=np.zeros(D)
  for k in range(len(rho)//M):pop+=np.diag(rho[k*M:(k+1)*M].reshape((D,D),order='F')).real
  active=np.array([int(1<=i<=10)+int(1<=j<=10) for i in range(12) for j in range(12)])
  overlap=np.array([int(1<=i<=10 and 1<=j<=10) for i in range(12) for j in range(12)])
  done=np.array([int(i==11)+int(j==11) for i in range(12) for j in range(12)])
  rec.update(mean_active=float(pop@active),prob_both_active=float(pop@overlap),mean_done=float(pop@done),total_flux=sum(c['flux'] for c in rec['caches']),seconds=time.time()-start,liouvillian_shape=L.shape,liouvillian_nnz=L.nnz)
  records.append(rec);print(json.dumps(rec),flush=True);(out/('results.json' if sector==0 else f'results_sector{sector}.json')).write_text(json.dumps(dict(leak=leak,results=records),indent=2))
import resource
print('max_rss_kib',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)
