import sys,json
sys.dont_write_bytecode=True
from triad_core import *
A,B,C,D,E=S.symbols('A B C D E',real=True);rs=[conformal((0,A),(1,0)),conformal((B,C),(0,1)),conformal((D+E,-D+E),(1,1))]
N=moments([r[0] for r in rs],[r[1] for r in rs]);print('matrix',flush=True)
det=S.Poly(N.det(method='domain-ge'),A,B,C,D,E);terms=det.terms();print('terms',len(terms),'negative',sum(1 for m,c in terms if c<0),'negative even',sum(1 for m,c in terms if c<0 and all(i%2==0 for i in m)),flush=True)
open(__file__.replace('.py','.json'),'w').write(json.dumps([[list(m),str(c)] for m,c in terms]))
