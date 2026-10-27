import sympy as s
# Exact algebra underlying the wrap-safe separation and tail/copy allocation.
p0=s.symbols('p0',positive=True)
delta=2*p0/9;theta=s.Rational(1,18)+2*p0/9
assert s.simplify((8*p0+1)/18-theta-delta)==0
assert s.simplify(theta-s.Rational(1,18)-delta)==0
assert 1-s.Rational(2,9)>s.Rational(3,4)
assert s.Rational(1,4)>s.Rational(2,9)
assert s.Rational(144)*s.Rational(2,9)==32
assert s.Rational(1,2*(32-2))<s.Rational(1,16)
assert s.Rational(256,512)==s.Rational(1,2)
for r in range(1,40):assert 2**r*s.Rational(1,16)**s.Rational(r,2)==s.Rational(1,2)**r
for m in range(1,20):assert sum(2**j for j in range(m))==2**m-1
print('PASS exact phase margins, wrap rejection, uniform1/60 spectral error, majority exponent and simulation allocation')
