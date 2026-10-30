import sys,time,json
sys.dont_write_bytecode=True
from triad_core import *
aa=S.symbols('a0:6'); ks=[(1,0),(0,1),(1,1)];rs=[conformal(aa[2*j:2*j+2],ks[j]) for j in range(3)]
N=moments([v[0] for v in rs],[v[1] for v in rs]);print('matrix constructed',time.time(),flush=True)
det=N.det(method='domain-ge');print('det computed',time.time(),flush=True)
pp=S.Poly(det,*aa);terms=pp.terms();print('terms',len(terms),'negative',sum(1 for mon,co in terms if co<0),'odd',sum(any(q%2 for q in mon) for mon,co in terms),flush=True)
open(__file__.replace('.py','.json'),'w').write(json.dumps([[list(mon),str(co)] for mon,co in terms]))
# Full symbolic factorization was abandoned after determinant reconstruction; it is not needed by the proof.
