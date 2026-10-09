#!/usr/bin/env python3
"""Read-only SymPy replay of the exact blind scalar baseline control."""
import sympy as s

h = s.Matrix([[2, 1], [1, 1]])
h2, h4 = h*h, h**4
assert h.det() == 1 and s.trace(h4) == 47
sigma = h4 / 47
post = [h2[:, i]*h2[:, i].T/h4[i, i] for i in range(2)]
p = [h4[i, i]/47 for i in range(2)]
assert sum((p[i]*post[i] for i in range(2)), s.zeros(2)) == sigma
for i in range(2):
    assert post[i]*post[i] == post[i] and s.trace(post[i]) == 1
    effect = s.simplify(p[i]*47*h2.inv()*post[i]*h2.inv())
    expected = s.zeros(2)
    expected[i, i] = 1
    assert effect == expected
a0 = s.diag(s.Rational(101,100),s.Rational(99,100))
norm = s.trace(a0*a0)
rho = a0*a0/norm
f = s.factor(sum((h*a0*h)[i,i]**2/h4[i,i] for i in range(2))/norm)
g = s.factor(sum((h2*a0)[i,i]**2/h4[i,i] for i in range(2))/norm)
assert norm == s.Rational(10001,5000)
assert rho == s.diag(s.Rational(10201,20002),s.Rational(9801,20002))
assert f == s.Rational(4649117,8840884)
assert g == s.Rational(4648261,8840884)
assert g-f == -s.Rational(214,2210221)
out = sum((rho[i,i]*post[i] for i in range(2)),s.zeros(2))
diff = rho-out
assert s.trace(diff) == 0
err2 = s.factor(-diff.det())
assert err2 == s.Rational(43368944841,176835361768)
assert err2/(1-f) == s.Rational(43368944841,83843723534)
assert err2 < 1-f and err2 <= 1-g
z=s.symbols('z0:4',real=True)
basis=[s.eye(2),s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
a=sum((x*b for x,b in zip(z,basis)),s.zeros(2))
ff=sum((h*a*h)[i,i]**2/h4[i,i] for i in range(2))
gg=sum(s.expand_complex((h2*a)[i,i]*s.conjugate((h2*a)[i,i]))/h4[i,i] for i in range(2))
claimed=(6*z[0]*z[1]-12*z[0]*z[3]+79*z[1]**2-330*z[1]*z[3]+423*z[2]**2+344*z[3]**2)/442
assert s.simplify(gg-ff-claimed) == 0
print('PASS: exact legal pure-canonical control, negative g-f, actual e2/E<1, and full symbolic shortcut form.')
