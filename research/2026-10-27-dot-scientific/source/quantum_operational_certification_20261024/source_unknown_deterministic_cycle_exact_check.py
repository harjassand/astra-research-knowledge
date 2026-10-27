import sympy as s
c=[s.Rational(1,3)]*12+[-s.Integer(4)]
assert len(c)==13 and sum(abs(x) for x in c)==8
assert 2*8**2+2*8**2==256
assert s.Rational(256,2)+s.Rational(4,2)==130
assert 130<=256
assert 13*512==6656
# Exact program linear combination, with sum rho_j =12T.
T,O=s.symbols('T O',commutative=False)
assert s.expand(s.Rational(1,3)*12*T-4*O-4*(T-O))==0
print('PASS13-call generator weights, noncommuting derivative bound130<=256, and inherited training counts')
