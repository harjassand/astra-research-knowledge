import sys,json,numpy as np
from scipy.linalg import expm
sys.path.insert(0,'producer-workspace/local_clock_progress_20261029')
from check_progress import matrices
out=[]
for name,n,edges in [('edge',2,[(0,1)]),('path3',3,[(0,1),(1,2)]),('triangle',3,[(0,1),(1,2),(2,0)])]:
 for g in [.05,.2,1.]:
  st,bs,H,Lstar=matrices(n,edges,g,1.); d=len(st); L=Lstar.T.conj(); v=np.zeros(d*d,complex);v[0]=1
  rate=4*g*g
  for sites in [(0,),(0,0),(0,1),(0,1,0),(0,0,0),(0,n-1,0,n-1)]:
   for dt in [.01,.2,2.]:
    z=v.copy();T=expm(dt*L)
    for x in sites:z=np.kron(bs[x].conj(),bs[x])@T@z
    density=float(np.trace(z.reshape((d,d),order='F')).real)
    bound=rate**len(sites)
    out.append(dict(graph=name,g=g,sites=sites,dt=dt,density=density,bound=bound,ratio=density/bound))
assert max(x['ratio'] for x in out)<=1+1e-9
print(json.dumps(dict(max_ratio=max(x['ratio'] for x in out),cases=out),indent=2))
