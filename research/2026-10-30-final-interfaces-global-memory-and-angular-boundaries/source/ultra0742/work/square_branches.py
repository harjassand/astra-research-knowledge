from pathlib import Path
import sympy as S,json,numpy as np
from scipy.optimize import root
here=Path(__file__).parent
raw=json.loads((here/'extreme_alignment.json').read_text())
n,p,q,r=S.symbols('n p q r',real=True);loc={str(x):x for x in (n,p,q,r)}
A,B,C,D,E=[S.sympify(x,locals=loc) for x in raw['quartic_coefficients']]
f1=S.cancel((A*D*D-E*B*B)/(16*p*p*q*q));f2=S.cancel((4*A*B*C-8*A*A*D-B**3)/(-32*p*q))
relation=n*(p*p+1-n)
aa=S.rem(S.Poly(f1,q),S.Poly(q*q-relation,q)).as_expr()
bb=S.rem(S.Poly(f2,q),S.Poly(q*q-relation,q)).as_expr()
gg=S.factor(S.gcd(S.Poly(aa,r),S.Poly(bb,r)).as_expr())
print('special nonaligned square-branch common r factor',gg,flush=True)
fn=S.lambdify((n,p,q,r),(f1,f2),'numpy',cse=True)
coeff=S.lambdify((n,p,q,r),(A,B,C,D,E),'numpy',cse=True)
results=[]
for nn,pp in [(1.5,.4),(1.5,.8),(1.15,.45),(1.8,.3),(1.8,1.)]:
    sols=[]
    for qq in [.1,.3,.55,.75]:
        for rr in [.8,1.5,3.,6.]:
            fit=root(lambda y:np.array(fn(nn,pp,y[0],y[1]),float),[qq,rr])
            if not fit.success or np.linalg.norm(fit.fun)>1e-6:continue
            qv,rv=fit.x
            if qv<.001 or qv>2 or rv<0 or rv>30:continue
            if any(np.linalg.norm(np.array([qv,rv])-x)<1e-4 for x in sols):continue
            sols.append(np.array([qv,rv]));ac,bc,cc,dc,ec=coeff(nn,pp,qv,rv)
            H=np.diag([2*nn-1,nn*(2-nn)])-np.outer([pp,qv],[pp,qv])
            h=np.linalg.eigvalsh(H)
            roots=np.roots([ac,bc,cc,dc,ec]);vals=[ac,ec]
            discr=bc*bc/(4*ac)-4*ac*dc/bc if abs(ac*bc)>1e-10 else None
            results.append({'n':nn,'p':pp,'q':qv,'r':rv,'H_eigenvalues':h.tolist(),
                            'quartic':list(map(float,(ac,bc,cc,dc,ec))),
                            'square_quadratic_discriminant':None if discr is None else float(discr),
                            'roots':[[float(z.real),float(z.imag)] for z in roots]})
            print(json.dumps(results[-1]),flush=True)
(here/'square_branches.json').write_text(json.dumps({'symbolic_special_gcd':str(gg),'diagnostics':results},indent=2)+'\n')
