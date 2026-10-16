import sympy as S,numpy as np,json
from pathlib import Path
p=Path(__file__).resolve().parent.parent/'certificates';data=Path(__file__).resolve().parent.parent/'data'
f=json.loads((p/'frozen_design.json').read_text());pc=json.loads((p/'physical_candidate.json').read_text())
def rat(A,d):return (S.Matrix(np.rint(A.real*d).astype(int))+S.I*S.Matrix(np.rint(A.imag*d).astype(int)))/d
E=[rat(e,1000) for e in np.load(data/'huang_theta_pi_over_4_printed.npy')]
F=[(S.Matrix(e['real_numerators'])+S.I*S.Matrix(e['imag_numerators']))/pc['denominator'] for e in pc['effects']]
assert sum(F,S.zeros(4))==S.eye(4)
for e,er in zip(F,E):
 assert e==e.conjugate().T
 assert all(e[:k,:k].det()>0 for k in range(1,5))
 assert all(abs(S.re(v))<=S.Rational(1,1000) and abs(S.im(v))<=S.Rational(1,1000) for v in e-er)
I=S.eye(2);P=[S.Matrix([[0,1],[1,0]]),S.Matrix([[0,-S.I],[S.I,0]]),S.diag(1,-1)];U=[]
for ns in f['stereographic_numerators']:
 v=[S.Rational(n,f['stereographic_denominator']) for n in ns];v2=sum(x*x for x in v)
 u=((1-v2)*I-2*S.I*sum((x*pa for x,pa in zip(v,P)),S.zeros(2)))/(1+v2)
 assert S.simplify(u.conjugate().T*u)==I;U.append(u)
unitary=S.kronecker_product(*U);b=9*S.sqrt(2)/20;r=S.Rational(6,11);z=S.Rational(9,11)
states=[]
for label in [-1,1]:
 rho=sum((S.kronecker_product((I+b*P[2]+x*b*P[0])/2,(I+label*x*r*P[0]+z*P[2])/2) for x in [-1,1]),S.zeros(4))/2
 rho=(unitary*rho*unitary.conjugate().T).applyfunc(S.expand)
 assert S.simplify(S.trace(rho))==1;states.append(rho)
scores=[S.Rational(n,f['score_denominator']) for n in f['score_numerators']]
losses=[sum(((label-score)**2*rho/2 for label,rho in zip([-1,1],states)),S.zeros(4)) for score in scores]
center=rat(np.load(p/'frozen_arrays.npz')['center'],10**9)
assert center==center.conjugate().T
base=S.simplify(S.re(S.trace(center)+sum(S.trace(e*(l-center)) for e,l in zip(E,losses))))
coef=0
for l in losses:
 for val in l-center:
  for part in [S.re(val),S.im(val)]:
   part=S.simplify(part)
   sign=S.sign(part)
   assert sign in [-1,0,1]
   coef+=sign*part
coef=S.simplify(coef)
assert base<S.Rational(864558,10**6)
assert coef<S.Rational(3187,1000)
raw=S.simplify(S.re(sum(S.trace(e*l) for e,l in zip(E,losses))))
physical=S.simplify(sum(S.trace(e*l) for e,l in zip(F,losses)))
source=S.Rational(2638,3025)
bound=source-S.Rational(864558,10**6)-S.Rational(3187,10**6)
assert bound==S.Rational(104571,24200000)
assert source-physical>bound
print('All exact signs, SU2 local product, physical PSD/completeness and box, centered bound PASS')
print('raw risk',S.N(raw,20),'center',S.N(base,20),'coefficient',S.N(coef,20))
print('constructed physical candidate risk',S.N(physical,20),'guaranteed box gap',bound)
