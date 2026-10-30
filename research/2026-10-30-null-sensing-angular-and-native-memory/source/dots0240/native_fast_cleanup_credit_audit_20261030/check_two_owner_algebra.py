"""Independent exhaustive matrix-unit check of the proposed commuting algebras."""
import numpy as np,json
# Labels free, o_h,z_h,o_g,z_g; one actual monitor; two private registers.
n=40;ix=lambda l,m,h,g:(((l*2+m)*2+h)*2+g)
def basis(owner):
 own=[1,2] if owner==0 else [3,4];out=[]
 for a in range(8):
  la,ma,pa=own[a//4],(a//2)%2,a%2
  for b in range(8):
   lb,mb,pb=own[b//4],(b//2)%2,b%2
   X=np.zeros((n,n),complex)
   for q in range(2):X[ix(la,ma,pa if owner==0 else q,q if owner==0 else pa),ix(lb,mb,pb if owner==0 else q,q if owner==0 else pb)]=1
   out.append(X)
 for a in range(2):
  for b in range(2):
   X=np.zeros((n,n),complex)
   for l in set(range(5))-set(own):
    for m in range(2):
     for q in range(2):X[ix(l,m,a if owner==0 else q,q if owner==0 else a),ix(l,m,b if owner==0 else q,q if owner==0 else b)]=1
   out.append(X)
 return out
Bh,Bg=basis(0),basis(1)
def labelop(dst,src):
 X=np.zeros((n,n),complex)
 for m in range(2):
  for h in range(2):
   for g in range(2):X[ix(dst,m,h,g),ix(src,m,h,g)]=1
 return X
def mon(l):
 X=np.zeros((n,n),complex)
 for h in range(2):
  for g in range(2):X[ix(l,0,h,g),ix(l,1,h,g)]=1
 return X
# Exterior acquisition contains its actual private g phase change.
acq=np.zeros((n,n),complex)
for m in range(2):
 for h in range(2):acq[ix(3,m,h,1),ix(0,m,h,0)]=1
acq+=acq.conj().T
exterior=[acq,labelop(3,4)+labelop(4,3),labelop(0,4),mon(0),mon(3),mon(4)]
comm=lambda X,Y:np.linalg.norm(X@Y-Y@X)
Hown=labelop(1,2)+labelop(2,1)+mon(1)+mon(1).conj().T+mon(2)+mon(2).conj().T
Hother=sum(mon(l)+mon(l).conj().T for l in [0,3,4])
def adj(H,js,X):
 Y=1j*(H@X-X@H)
 for j in js:
  a=j.conj().T@j;Y+=j.conj().T@X@j-(a@X+X@a)/2
 return Y
norms=[np.vdot(b,b).real for b in Bh]
def closure_error(X):return np.linalg.norm(X-sum(b*(np.vdot(b,X)/norm) for b,norm in zip(Bh,norms)))
results={
 'dimension':n,'basis_dimension_each':len(Bh),
 'all_4624_pairwise_basis_commutators':float(max(comm(x,y) for x in Bh for y in Bg)),
 'all_exterior_generator_basis_commutators':float(max(comm(x,y) for x in Bh for y in exterior)),
 'full_other_monitor_annihilates_algebra':float(max(np.linalg.norm(adj(Hother,[mon(l) for l in [0,3,4]],x)) for x in Bh)),
 'own_cleanup_reset_monitor_adjoint_closure':float(max(closure_error(adj(Hown,[labelop(0,2),mon(1),mon(2)],x)) for x in Bh)),
 'own_monitor_not_spectator':float(max(comm(x,mon(1)) for x in Bh)),
}
for k,v in results.items():
 if k not in ['dimension','basis_dimension_each','own_monitor_not_spectator']:assert v<1e-12
assert results['own_monitor_not_spectator']>0
print(json.dumps(results,indent=2))
