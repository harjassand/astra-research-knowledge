import os
os.environ['OPENBLAS_NUM_THREADS']='2'
import numpy as np,itertools,scipy.linalg as la,json,time
from piecewise_texture import evaluate,matrix
D='producer-workspace/chiral_hamiltonian_interface_20261102'
z=np.load(D+'cubic_move.npz',allow_pickle=True);pa=z['phi_a'];pb=z['phi_b']
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);G=[np.kron(X,X),np.kron(X,Y),np.kron(X,Z),np.kron(Y,I),np.kron(Z,I)]
def sampled(phi,r):
 N=3*r;xs=list(itertools.product(range(N),repeat=3));out=[]
 for xx in xs:
  x=(np.array(xx)+np.array([.173,.389,.617]))/r;base=np.floor(x).astype(int);f=x-base;order=np.argsort(-f);vv=[base.copy()];v=base.copy()
  for d in order:v=v.copy();v[d]+=1;vv.append(v)
  ids=[int((v[0]%3)*9+(v[1]%3)*3+v[2]%3) for v in vv]
  fs=f[order];b=np.array([1-fs[0],fs[0]-fs[1],fs[1]-fs[2],fs[2]])
  out.append(matrix(evaluate(phi,ids,b)))
 return np.array(out)
def boundary_green(N,L):
 gg=np.empty((N,N,N,4,4),complex)
 for i,j,k in itertools.product(range(N),repeat=3):
  p=2*np.pi*np.array([i+.5,j,k])/N
  on=sum(np.sin(p[d])*G[d] for d in range(3))+(-1+sum(1-np.cos(p)) +1)*G[4]
  h=np.kron(np.eye(L),on);hop=-G[4]/2+G[3]/(2j)
  for w in range(L-1):h[4*w:4*w+4,4*w+4:4*w+8]=hop;h[4*w+4:4*w+8,4*w:4*w+4]=hop.conj().T
  gg[i,j,k]=la.inv(h)[:4,:4]
 ker=np.fft.ifftn(gg,axes=(0,1,2));coords=np.array(list(itertools.product(range(N),repeat=3)));diff=coords[:,None,:]-coords[None,:,:];di=diff%N
 blocks=ker[di[:,:,0],di[:,:,1],di[:,:,2]]*np.exp(1j*np.pi*diff[:,:,0]/N)[:,:,None,None]
 g=blocks.transpose(0,2,1,3).reshape(4*N**3,4*N**3)
 assert la.norm(g-g.conj().T)<1e-8
 return g
results=[]
for r in [2]:
 N=3*r;L=5;g=boundary_green(N,L);n=len(g);U=[sampled(p,r) for p in [pa,pb]]
 for M in [.5,1,2]:
  row={'refinement':r,'N':N,'L':L,'M':M,'s_a':int(z['q_a']),'s_b':int(z['q_b'])};vals=[]
  for u in U:
   K=-la.block_diag(g,g,-g,-g)
   for site,us in enumerate(u):
    for a in range(2):
     for b in range(2):
      aa=slice(a*n+4*site,a*n+4*site+4);bb=slice((2+b)*n+4*site,(2+b)*n+4*site+4)
      K[aa,bb]-=us[a,b]*I.repeat(2,axis=0).repeat(2,axis=1)/M if False else us[a,b]*np.eye(4)/M
      K[bb,aa]-=us[a,b].conjugate()*np.eye(4)/M
   e=la.eigvalsh(K,driver='evr');vals.append((int(sum(e<0))-2*n,float(min(abs(e)))))
  row.update(axial_charge_a=vals[0][0],axial_charge_b=vals[1][0],minabs_schur_a=vals[0][1],minabs_schur_b=vals[1][1]);results.append(row);print(row,flush=True)
  json.dump(results,open(D+'refined_charge_shifted_results.json','w'),indent=2)
