"""Independent cases using frozen generic projection helper; tests non-CP total noise.
No numerical test replaces the generator/partition proof.
"""
from pathlib import Path
base=Path(__file__).parent
src=(base/'sources/check_cavity_bridge.py').read_text().split('locs=frozenset(range(4))')[0]
exec(src)
def lind(J):
 A=J.conj().T@J
 return smap(lambda r:J@r@J.conj().T-.5*(A@r+r@A))
sm=np.array([[0,1],[0,0]],complex)
D0=lind(np.kron(sm,I));D1=lind(np.kron(I,sm))
Lid0=.3*D0+ham(.2*ops['X0'])
Lid1=.2*D1+ham(.3*ops['Z1'])
Lid=Lid0+Lid1
rows=[]
for mu in [.0001,.001,.01]:
 N=-mu*D0+mu*diss(ops['XX'])
 actual=Lid+N
 mincp=1.;maxidentity=0.;maxprojection=0.
 for R in subsets({0,1}):
  C=Lid+cavity(N,R)
  intended=sum(([Lid0,Lid1][j] for j in R),np.zeros_like(Lid))
  direct=cavity(actual,R)+intended
  maxidentity=max(maxidentity,float(np.linalg.norm(C-direct)))
  mincp=min(mincp,float(np.linalg.eigvalsh(choi(expm(C))).min()))
  maxprojection=max(maxprojection,float(np.linalg.norm(cavity(cavity(N,R),R)-cavity(N,R))))
 # Deleting negative damping correction need not be a valid noise-only channel.
 ncp=float(np.linalg.eigvalsh(choi(expm(N))).min())
 assert ncp<-1e-8 and mincp>-1e-10 and maxidentity<1e-10 and maxprojection<1e-10
 # All bilinear cube interpolants are convex cavity generators.
 interpmin=1.
 Cs={R:Lid+cavity(N,R) for R in subsets({0,1})}
 for z0,z1 in [(0.17,0.61),(.5,.5),(.9,.03)]:
  Lz=sum((z0 if 0 in R else 1-z0)*(z1 if 1 in R else 1-z1)*C for R,C in Cs.items())
  interpmin=min(interpmin,float(np.linalg.eigvalsh(choi(expm(Lz))).min()))
 assert interpmin>-1e-10
 rows.append({'mu':mu,'noise_only_channel_min_choi_eigenvalue':ncp,'min_cavity_channel_choi_eigenvalue':mincp,'min_interpolated_channel_choi_eigenvalue':interpmin,'cavity_identity_residual':maxidentity,'projection_idempotence_residual':maxprojection})
print(json.dumps({'scope':'finite nonunital intended generators with non-GKSL TOTAL perturbation, not merely non-GKSL summands','tests':rows},indent=2))
