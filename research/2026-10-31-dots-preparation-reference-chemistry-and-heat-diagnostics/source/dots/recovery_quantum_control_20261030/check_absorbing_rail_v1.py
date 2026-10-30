import numpy as np,json
from scipy.linalg import expm,eigvalsh
A=['v','0','1'];B=['v','e0','e1','d0','d1','x'];G=['e_v','e_0','e_1','d_v','d_0','d_1','s','f0','f1']
idx=lambda a,b:6*A.index(a)+B.index(b)
V=np.zeros((18,18),complex)
for b in range(2):
 for a in A:
  for r in ['e','d']:V[idx(a,r+str(b)),b*9+G.index(r+'_'+a)]=1
 V[idx(str(b),'v'),b*9+G.index('s')]=1
for b,g,a,c in [(0,'f0','v','v'),(1,'f0','v','x'),(0,'f1','0','x'),(1,'f1','1','x')]:V[idx(a,c),b*9+G.index(g)]=1
Om=1.3;ka=.8
H=np.zeros((18,18),complex);J=np.zeros_like(H)
for b in range(2):
 s=idx(str(b),'v');e=idx('v','e'+str(b));H[e,s]=H[s,e]=Om
 for a in A:J[idx(a,'d'+str(b)),idx(a,'e'+str(b))]=np.sqrt(ka)
h=np.zeros((9,9),complex);h[G.index('e_v'),G.index('s')]=h[G.index('s'),G.index('e_v')]=Om
j=np.zeros_like(h)
for a in A:j[G.index('d_'+a),G.index('e_'+a)]=np.sqrt(ka)
P=np.diag([int(c in ('d0','d1')) for a in A for c in B])
R=np.array([[2/ka+ka/(4*Om**2),-1j/(2*Om)],[1j/(2*Om),2/ka]],complex)
ha=np.array([[0,Om],[Om,0]],complex);pe=np.diag([0,1]);res=1j*(ha@R-R@ha)-ka/2*(pe@R+R@pe)+np.eye(2)
# Full arbitrary source operators, not only basis projectors, leave B logical unchanged on done rails.
rng=np.random.default_rng(83);F=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));F=(F+F.conj().T)/2
Fc=V.conj().T@np.kron(F,np.eye(6))@V
Pg=np.diag([int(g.startswith('d_')) for g in G]);gf=np.zeros((9,9),complex)
for a in A:
 for aa in A:gf[G.index('d_'+a),G.index('d_'+aa)]=F[A.index(a),A.index(aa)]
err=float(np.linalg.norm(np.kron(np.eye(2),Pg)@Fc@np.kron(np.eye(2),Pg)-np.kron(np.eye(2),gf)))
# Exact active survival dominated by the Gramian exponential bound.
r=1/eigvalsh(R)[-1];C=eigvalsh(R)[-1]/eigvalsh(R)[0];K=-1j*ha-ka*pe/2
surv=[]
for t in [0,1,2,5,10,30]:
 q=np.linalg.norm(expm(K*t)@np.array([1,0]))**2;bound=C*np.exp(-r*t);assert q<=bound+1e-12
 surv.append({'time':t,'survival':float(q),'bound':float(bound)})
result={'basis_unitarity_residual':float(np.linalg.norm(V.conj().T@V-np.eye(18))),'full_H_factorization_residual':float(np.linalg.norm(V.conj().T@H@V-np.kron(np.eye(2),h))),'full_J_factorization_residual':float(np.linalg.norm(V.conj().T@J@V-np.kron(np.eye(2),j))),'dark_HP_residual':float(np.linalg.norm(H@P)),'dark_JP_residual':float(np.linalg.norm(J@P)),'arbitrary_source_done_sector_factorization_residual':err,'Gramian_residual':float(np.linalg.norm(res)),'survival':surv,'scope':'Exact small physical transfer/canonical table; does not verify encoded noisy handoff, late arrival freshness or apparatus composition.'}
assert max(result[x] for x in ['basis_unitarity_residual','full_H_factorization_residual','full_J_factorization_residual','dark_HP_residual','dark_JP_residual','arbitrary_source_done_sector_factorization_residual','Gramian_residual'])<1e-12
print(json.dumps(result,indent=2))
