import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as sla, json,time,os
from pathlib import Path
out=Path(__file__).parent
I2=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1]); I4=np.eye(4)
paulis=[[np.kron(Z,I2),np.kron(I2,Z)],[np.kron(X,I2),np.kron(I2,X)]]
# idle=0; g1=1,2;e1=3,4;g2=5,6;e2=7,8;final=9,10
states=[('idle',0,0)]+[(p,j,b) for p,j in [('g',0),('e',0),('g',1),('e',1),('f',2)] for b in (0,1)]
prefix=[]
for a in (0,1):
 q=[]
 for p,j,b in states:
  length=j+(p=='e'); Q=I4.copy()
  for k in range(length):
   if b: Q=paulis[a][k]@Q
  q.append(Q)
 prefix.append(q)
D=121; eye=sp.eye(D,format='csc'); sector=int(os.environ.get("BELL_SECTOR","0")); bell=np.array([[1,0,0,1],[1,0,0,-1],[0,1,1,0],[0,1,-1,0]][sector])/np.sqrt(2)
V=sp.block_diag([(prefix[0][i]@prefix[1][j]@bell).reshape(4,1) for i in range(11) for j in range(11)],format='csc')
def local(O,a):
 return sp.kron(O,sp.eye(11)) if a==0 else sp.kron(sp.eye(11),O)
def physical_edge(a,t,s,P=I4):
 o=sp.csc_matrix(([1.],([t],[s])),shape=(11,11)); return sp.kron(local(o,a),sp.csc_matrix(P),format='csc')
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
  read[a].append(reduce((physical_edge(a,0,9)+s*physical_edge(a,0,10))/np.sqrt(2)))

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

def steady(L):
 A=L.tolil();A[0,:]=tr; b=np.zeros(D*D,complex);b[0]=1
 v=sla.spsolve(A.tocsc(),b);return v
records=[]
for p in (0.,.001):
 for r in (.001,.01,.05,.1):
  start=time.time(); L=base.copy()
  for a in (0,1):L+=r*((1-p)*diss(prep[a][0])+p*diss(prep[a][1]))
  rho=steady(L); R=rho.reshape((D,D),order='F'); rec=dict(r=r,p=p,trace=float(np.trace(R).real),mineig=float(np.linalg.eigvalsh((R+R.conj().T)/2).min()),residual=float(np.linalg.norm(L@rho)),caches=[])
  for a in (0,1):
   Jc=gain(read[a][0]);Jw=gain(read[a][1]); K=L-Jc-Jw
   rw=sla.spsolve(K,-Jw@rho);RW=rw.reshape((D,D),order='F')
   rec['caches'].append(dict(wrong=float(tr@rw.real),flux=float(tr@((Jc+Jw)@rho).real),wrong_report_fraction=float((tr@(Jw@rho).real)/(tr@((Jc+Jw)@rho).real)),wrong_min_eig=float(np.linalg.eigvalsh((RW+RW.conj().T)/2).min()),correct_min_eig=float(np.linalg.eigvalsh((R-RW+(R-RW).conj().T)/2).min()),cache_residual=float(np.linalg.norm(K@rw+Jw@rho))))
  # Exact retained-cache Poisson observable: h_w-h_c=d.
  Jw=gain(read[0][1]);Jc=gain(read[0][0]);K=L-Jc-Jw
  dv=sla.spsolve(K.conj().T,-tr.astype(complex))
  mu=rec['caches'][0]['wrong']; rhs=mu*tr-Jw.conj().T@dv
  LA=L.conj().T.tolil();LA[0,:]=rho.conjugate();rhs[0]=0
  hv=sla.spsolve(LA.tocsc(),rhs)
  hc=hv.reshape((D,D),order='F'); hw=(hv+dv).reshape((D,D),order='F')
  ec=np.linalg.eigvalsh((hc+hc.conj().T)/2);ew=np.linalg.eigvalsh((hw+hw.conj().T)/2)
  rec['poisson']=dict(positive_range=float(max(ec.max(),ew.max())-min(ec.min(),ew.min())),min=float(min(ec.min(),ew.min())),max=float(max(ec.max(),ew.max())),difference_norm=float(np.linalg.norm(dv.reshape((D,D),order='F'),ord=2)),hermiticity=float(np.linalg.norm(hc-hc.conj().T)),residual_correct=float(np.linalg.norm(L.conj().T@hv+Jw.conj().T@dv-mu*tr)),residual_wrong=float(np.linalg.norm(L.conj().T@(hv+dv)-Jc.conj().T@dv+(1-mu)*tr)))
  rec['seconds']=time.time()-start;records.append(rec);print(json.dumps(rec),flush=True);(out/('results.json' if sector==0 else f'results_sector{sector}.json')).write_text(json.dumps(dict(leak=leak,results=records),indent=2))

import resource
print("resources",json.dumps(dict(liouvillian_shape=L.shape,liouvillian_nnz=L.nnz,max_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)),flush=True)
