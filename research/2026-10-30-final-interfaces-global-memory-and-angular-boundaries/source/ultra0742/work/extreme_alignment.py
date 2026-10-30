"""Exact binary-quartic square conditions for possible Hopf extreme rays."""
from pathlib import Path
import sympy as S,json,time,signal
signal.alarm(120);start=time.perf_counter()
n,p,q,r,x,y=S.symbols('n p q r x y',real=True)
B=S.diag(1,n);dd=S.Matrix([p,q]);H=2*n*S.eye(2)-B*B-dd*dd.T
J=S.Matrix([[0,1],[-1,0]]);tt=J*n*B.inv()*dd
ee=S.Matrix([x,y]);Q=S.expand((ee.T*H*ee)[0]*(ee.T*(2*r*B-B*B-3*dd*dd.T)*ee)[0]-4*(ee.dot(tt))**2*(x*x+y*y))
co=[S.factor(S.Poly(Q,x,y).coeff_monomial(x**(4-i)*y**i)) for i in range(5)]
A,Bb,C,D,E=co
f1=S.factor(A*D*D-E*Bb*Bb)
f2=S.factor(4*A*Bb*C-8*A*A*D-Bb**3)
print('quartic coefficients',co,flush=True)
print('f1',f1,flush=True);print('f2',f2,flush=True)
# Strip only factors declared nonzero on the candidate nonaligned branch.
ff1=S.Poly(f1,r).primitive()[1].as_expr();ff2=S.Poly(f2,r).primitive()[1].as_expr()
result=S.factor(S.resultant(ff1,ff2,r))
out={'quartic_coefficients':list(map(str,co)),'square_conditions':list(map(str,(f1,f2))),
     'resultant':str(result),'seconds':time.perf_counter()-start,
     'scope':'Necessary square conditions on the nonzero-coefficient branch; positivity and exceptional branches are separate obligations.'}
Path(__file__).with_name('extreme_alignment.json').write_text(json.dumps(out,indent=2)+'\n')
print('resultant',result,'seconds',out['seconds'],flush=True)
