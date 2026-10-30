"""Numerical first-order regression, full 3-clock tensor product (all dirty occupations)."""
import numpy as np,json
from scipy.linalg import sqrtm
N=8;I=np.eye(N);adj=[[1,2],[0],[0]]
a=[];n=[];P=[]
for h in range(3):
 z=np.zeros((N,N))
 for s in range(N):
  if (s>>h)&1:z[s^(1<<h),s]=1
 a.append(z);n.append(z.T@z);P.append(I-n[-1])
G=[];Y=[];X=[];m=[]
for h in range(3):
 gg=I.copy()
 for j in adj[h]:gg=gg@P[j]
 G.append(gg);Y.append(1j*(a[h]-a[h].T));X.append(a[h]+a[h].T);m.append(sum((n[j] for j in adj[h]),np.zeros((N,N))))
f=[[0,1,1],[0,0,2],[0,1,2]];v=[1.,3.,4.];V=[x*I for x in v]
def run(nu,t):
 H=nu*sum((G[h]@X[h] for h in range(3)),np.zeros((N,N)))
 B=[n[h]+2*nu*G[h]@Y[h]+nu**2*np.diag(8*.05**np.diag(m[h])) for h in range(3)]
 roots=[np.asarray(sqrtm(b),complex) for b in B]
 def LL(O):
  return [1j*(H@O[x]-O[x]@H)+sum((a[j].T@O[f[j][x]]@a[j]-.5*(n[j]@O[x]+O[x]@n[j]) for j in range(3)),np.zeros((N,N),complex)) for x in range(3)]
 def ZZ(O,h):return [roots[h]@O[f[h][x]]@roots[h]-.5*(B[h]@O[x]+O[x]@B[h]) for x in range(3)]
 LV=LL(V);R=[z.copy() for z in LV]
 for h in range(3):
  LZ=LL(ZZ(V,h));ZL=ZZ(LV,h)
  for x in range(3):R[x]+=t*(LZ[x]-ZL[x])
 rows=[]
 for x in [1,2]:
  ds=[v[x]-v[f[h][x]] for h in range(3)]
  target=R[x]+.25*sum((n[h]*ds[h] for h in range(3)),np.zeros((N,N)))+.05*t*nu**2*sum(ds)*I
  rows.append({'data':x,'max_drift_eigenvalue':float(np.linalg.eigvalsh(R[x]).max()),'max_target_residual_eigenvalue':float(np.linalg.eigvalsh(target).max())})
 return {'nu':nu,'t':t,'min_B_eigenvalue':min(float(np.linalg.eigvalsh(b).min()) for b in B),'rows':rows}
out={'clock_dimension':N,'includes_all_occupancy_sectors':True,'f0':8,'r':.05,'target':'first_order_drift <= -.25 sum n_h d_h - .05 t nu^2 sum d_h','cases':[run(.001,.001),run(.0001,.001),run(.001,.0001)]}
print(json.dumps(out,indent=2))
assert all(z['max_target_residual_eigenvalue']<0 for case in out['cases'] for z in case['rows'])
