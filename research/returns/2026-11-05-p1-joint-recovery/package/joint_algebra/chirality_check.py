import numpy as np,json
from yangian_weak import local
for n in range(3,8):
 d=2**n;site=[[local(n,j,a) for a in range(1,4)] for j in range(n)];J=[sum(site[j][a] for j in range(n)) for a in range(3)]
 Y=[sum(site[i][b]@site[j][c]-site[i][c]@site[j][b] for i in range(n) for j in range(i+1,n)) for a,b,c in [(0,1,2),(1,2,0),(2,0,1)]]
 C=sum(j@y for j,y in zip(J,Y));J2=sum(j@j for j in J);vals,V=np.linalg.eigh(J2);Ji=(V*np.where(vals>1e-8,1/np.maximum(vals,1e-8),0))@V.conj().T
 c2=np.trace(C@C).real/d;c2j2=np.trace(C@C@J2).real/d;parallel=np.trace(C@C@Ji).real/d
 print(json.dumps(dict(n=n,c2=float(c2),c2j2=float(c2j2),formula_c2=n*(n-1)*(n-2),formula_c2j2=n*(n-1)*(n-2)*(5*n-12),parallel_energy=float(parallel/8),lower_bound=n*(n-1)*(n-2)/(8*(5*n-12)))),flush=True)
