"""Symbolically verify the small, density-uniform transport certificates."""
from explore import dual_setup,grad_sum,poly_add
import sympy as s
from sympy.polys.matrices import DomainMatrix
from pathlib import Path
p=s.symbols('p');q=s.symbols('q');pair=frozenset((-1,2))
basis,N=dual_setup(3)
cols=[[(i,N[i,j]) for i in range(N.rows) if N[i,j]] for j in range(N.cols)]
v=s.Matrix([s.expand(sum(x*(p**len(basis[i])-p**len(basis[i]|pair)) for i,x in col)) for col in cols])
H=s.Matrix(N.cols,N.cols,lambda a,b:s.expand(sum(x*y*(p**len(basis[i]|basis[j])-p**len(basis[i]|basis[j]|pair)) for i,x in cols[a] for j,y in cols[b])))
z=DomainMatrix.from_Matrix(H).to_field().inv().to_Matrix()*v
z=z.applyfunc(s.factor)
L=(1-p)*(-p**4+4*p**3+8*p+5)/(-p**3+p**2+3*p+5)
assert s.cancel((v.T*z)[0]-L)==0
assert all(s.cancel(x)==0 for x in H*z-v)
# Independently check exact cancellation of the compiled trial current's orbits.
raw=N*z;orbit={}
for a,coef in zip(basis,raw):
 for point,sign in [(0,1),(1,-1)]:
  for shape,val in [(a|{point},sign*coef),(a|{point}|pair,-sign*coef)]:
   m=min(shape);key=tuple(sorted(x-m for x in shape));orbit[key]=orbit.get(key,0)+val
assert all(s.cancel(value)==0 for value in orbit.values())
U=(1-p)*(p**3-p**2+5*p+3)/((3-p)*(p+1))
# f=t[h0 h1 h3 - h0 h2 h3], t=1/((p-3)(p+1)); h_i=eta_i-p.
t=1/((p-3)*(p+1));chi=p*(1-p)
# Derive the full polynomial moments instead of inserting precomputed values.
gradient = {}
for shape, sign in [(frozenset((0,1,3)), 1), (frozenset((0,2,3)), -1)]:
 for a, value in grad_sum(shape).items():
  poly_add(gradient, a, sign*value)
mu = [1, 0, chi]
nu = [p, chi, p*(1-p)**2]
def local_inner(a,b):
 outside_a, outside_b = a-pair, b-pair
 if outside_a != outside_b:
  return 0
 k, ell = int(-1 in a)+int(-1 in b), int(2 in a)+int(2 in b)
 return chi**len(outside_a)*(mu[k]*mu[ell]-nu[k]*nu[ell])/(2*chi)
a_poly = {frozenset((0,)): 1, frozenset((1,)): -1}
vf = s.factor(sum(v*w*local_inner(a,b) for a,v in gradient.items() for b,w in a_poly.items()))
Hf = s.factor(sum(v*w*local_inner(a,b) for a,v in gradient.items() for b,w in gradient.items()))
assert s.cancel(vf-2*p**2*(p-1)**2)==0
assert s.cancel(Hf+2*p**2*(p-3)*(p-1)**2*(p+1))==0
assert s.cancel(1-p*p+2*t*vf+t*t*Hf-U)==0
report=['# Density-uniform symbolic certificate','',
        'p is the particle density, q=1-p. All identities checked symbolically.','',
        f'L(p) = {s.factor(L)}',f'U(p) = {s.factor(U)}',
        f'U(p)-L(p) = {s.factor(U-L)}','',
        f'L(1-q) = {s.series(L.subs(p,1-q),q,0,5)}',
        f'U(1-q) = {s.series(U.subs(p,1-q),q,0,5)}','',
        'The dual current is (eta0-eta1)*(1-eta[-1]*eta[2])*sum_A g_A product(eta_i for i in A).',
        'Nonzero coefficients g_A follow.']
for a,coef in zip(basis,raw):
 coef=s.factor(coef)
 if coef:report.append(f'{tuple(sorted(a))}: {coef}')
Path(__file__).with_name('symbolic_certificate.txt').write_text('\n'.join(report)+'\n')
print('\n'.join(report[:12]))
