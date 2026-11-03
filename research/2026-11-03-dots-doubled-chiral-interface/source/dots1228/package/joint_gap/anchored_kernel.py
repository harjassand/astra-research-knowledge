"""Exterior-independent V-covariant local kernels for actual Wilson/mass patch.
No gap assumption; no claim that finite patch filtering supplies a full-slab ground map.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import sys,itertools,json,numpy as np
sys.path.insert(0,'producer-workspace/chiral_hamiltonian_interface_20261102')
from piecewise_texture import evaluate,matrix
D='producer-workspace/chiral_hamiltonian_interface_20261102'
I=np.eye(2);X=np.array([[0,1],[1,0]]);Y=np.array([[0,-1j],[1j,0]]);Z=np.diag([1,-1]);G=[np.kron(X,X),np.kron(X,Y),np.kron(X,Z),np.kron(Y,I),np.kron(Z,I)]
N=2;L=2;coords=list(itertools.product(range(N),repeat=3));ix={x:i for i,x in enumerate(coords)};n=4*N**3*L
h=np.zeros((n,n),complex)
for w in range(L):
 for x in coords:
  j=(w*N**3+ix[x])*4;h[j:j+4,j:j+4]=3*G[4]
  for d in range(4):
   if d==3:
    if w+1==L:continue
    k=((w+1)*N**3+ix[x])*4
   else:
    if x[d]+1==N:continue
    y=list(x);y[d]+=1;k=(w*N**3+ix[tuple(y)])*4
   hop=-G[4]/2+G[d]/(2j)
   h[j:j+4,k:k+4]+=hop;h[k:k+4,j:j+4]+=hop.conj().T

def H(phi,M=1.2):
 out=np.zeros((4*n,4*n),complex)
 for a in range(4):out[a*n:(a+1)*n,a*n:(a+1)*n]=h*(1 if a<2 else -1)
 for xx in coords:
  x=(np.array(xx)+.3)/2;base=np.floor(x).astype(int);f=x-base;order=np.argsort(-f);vv=[base.copy()];v=base.copy()
  for d in order:v=v.copy();v[d]+=1;vv.append(v)
  ids=[int((v[0]%3)*9+(v[1]%3)*3+v[2]%3) for v in vv];fs=f[order];bary=np.array([1-fs[0],fs[0]-fs[1],fs[1]-fs[2],fs[2]])
  U=matrix(evaluate(phi,ids,bary));j=ix[xx]*4
  for a in range(2):
   for b in range(2):
    aa=slice(a*n+j,a*n+j+4);bb=slice((b+2)*n+j,(b+2)*n+j+4)
    out[aa,bb]=M*U[a,b]*np.eye(4);out[bb,aa]=M*U[a,b].conjugate()*np.eye(4)
 return out
q=np.repeat([1,-1,0,0],n)
def rot(alpha):return np.exp(2j*np.pi*alpha*q)
# Uniform bound: onsite Wilson norm3 + at most eight unit-norm hopping terms + mass1.2.
W=13.0

def filtered(phi,anchor=1,seed=0,iterations=2):
 angle=phi[anchor];hh=H(phi-angle)
 # McWeeny polynomial, degree 3**iterations. Defined/contractive without any gap premise.
 p=(np.eye(len(hh))-hh/W)/2
 for _ in range(iterations):p=3*p@p-2*p@p@p
 return rot(angle)*p[:,seed]

z=np.load(D+'cubic_move.npz',allow_pickle=True);pa=z['phi_a'];pb=z['phi_b']
rng=np.random.default_rng(9);errs=[]
for phi in [pa,pb]:
 hh=H(phi);f=filtered(phi)
 for alpha in [.123,.49,.973]:
  rr=rot(alpha);shifted=(phi+alpha)%1
  errs.append(dict(h_covariance=float(np.linalg.norm(H(shifted)-rr[:,None]*hh*rr.conj()[None,:])),kernel_covariance=float(np.linalg.norm(filtered(shifted)-rr*f))))
 periodic=float(np.linalg.norm(filtered(phi+rng.integers(-3,4,len(phi)))-f))
 assert periodic<1e-10
 assert np.linalg.norm(f)<=1+1e-10
# Locality check: patch texture only sees coarse vertices of [0,1]^3.
inside={i*9+j*3+k for i,j,k in itertools.product(range(2),repeat=3)}
changed=pa.copy()
for j in range(27):
 if j not in inside:changed[j]=rng.random()
ext_error=float(np.linalg.norm(filtered(changed)-filtered(pa)))
# Actual saved decoration reconnection: no inverse decoration oracle.
dz=np.load(D+'decor_transfer.npz');mz=np.load(D+'matching.npz',allow_pickle=True)
sg={tuple(e):s for e,s in zip(mz['edges'],mz['signs'])};verts=[8,9,11,12,13,14,16,17];idx={v:i for i,v in enumerate(verts)};gam=dz['gamma']
pair_a=[(8,17),(9,11),(12,16),(13,14)];pair_b=[(8,11),(9,13),(12,14),(16,17)]
def K(pairs):return sum((np.eye(16)-1j*sg[e]*gam[idx[e[0]]]@gam[idx[e[1]]])/2 for e in pairs)
ka,kb=K(pair_a),K(pair_b);ts=[dz['Q']@g@dz['P'] for g in gam];norms=[np.linalg.norm(t,2) for t in ts];j=int(np.argmax(norms));t=ts[j]
charge_error=float(np.linalg.norm((kb+np.eye(16))@t-t@ka-t))
parity=np.eye(16,dtype=complex)
for j in range(0,8,2):parity=parity@(1j*gam[j]@gam[j+1])
parity_error=float(np.linalg.norm(parity@t+t@parity))
out=dict(patch_one_body_dimension=4*n,polynomial_degree=9,max_h_covariance_error=max(e['h_covariance'] for e in errs),max_kernel_covariance_error=max(e['kernel_covariance'] for e in errs),exterior_change_error=ext_error,decoration_partial_norm=max(norms),decoration_axial_charge_plus_one_error=charge_error,decoration_odd_parity_error=parity_error,scope='Exact local coefficient/covariance/compiler diagnostic; no uniform actual-ground-state transfer or interface gap asserted')
assert max(out[k] for k in ['max_h_covariance_error','max_kernel_covariance_error','exterior_change_error','decoration_axial_charge_plus_one_error','decoration_odd_parity_error'])<1e-9
open(D+'joint_gap/anchored_kernel_results.json','w').write(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
