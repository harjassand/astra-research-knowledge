import sympy as s
from fractions import Fraction as Q
from math import factorial
z=s.symbols('z',positive=True);n=s.Rational(27,4);a=n-1;b=3*a/(n+3);rho=a/(2*n)
w=2*b/(z*(z+b))-a/(z*(z+a));k=w-rho/z**2
expected=-(n-1)**2*(z-1)*((2*n-3)*z-3*n+3)/(2*n*z**2*(n+z-1)*((n+3)*z+3*n-3))
assert s.cancel(k-expected)==0
parts=-s.Rational(6877,648)/(13*z+23)+s.Rational(2116,729)/(4*z+23)+s.Rational(529,5832)/(z-1)
assert s.cancel(k*z*z/(z-1)**2-parts)==0
z0=s.Rational(23,14)
ratio=s.cancel((z0+b)**9/((z0-1)*(z0+a)**8))
assert ratio==s.Rational(2**8*3**9*23,13**9)
assert sum(Q(23,5)**j/factorial(j) for j in range(9))>Q(13**9,2**8*3**9*23)
assert Q(23,54)-Q(529,5832)*Q(23,5)==Q(253,29160)
assert Q(27,46)*Q(253,29160)==Q(11,2160)
assert 8*n/(9-n)==24
print('PASS exact kernel, partial fractions, endpoint log ratio, rational exponential certificate, condition24 and quantitative11/2160.')
