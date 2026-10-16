import sympy as s
x,y,z,t,w=s.symbols('x y z t w');a=lambda x:(1-2*x)/(10*x*(x+s.Rational(1,3)))
den=300*x*y*z*(x+s.Rational(1,3))*(y+s.Rational(1,3))*(z+s.Rational(1,3))
N=s.factor(den*(a(x)*a(y)+a(x)*a(z)+a(y)*a(z)))
expected=4-16*(x*y+x*z+y*z)+42*x*y*z
assert s.factor((N-expected).subs(z,1-x-y))==0
schur=x**3+y**3+z**3+3*x*y*z-(x*x*y+x*x*z+y*y*x+y*y*z+z*z*x+z*z*y)
assert s.factor((expected-4*schur-6*x*y*z).subs(z,1-x-y))==0
assert s.expand(schur-((x-y)*(x*(x-z)-y*(y-z))+z*(z-x)*(z-y)))==0
pairnum=s.factor(10*x*z*(x+s.Rational(1,3))*(z+s.Rational(1,3))*(a(x)+a(z)))
assert s.expand(pairnum-((x+z)**2+(x+z)/3-(s.Rational(10,3)+2*(x+z))*x*z))==0
assert s.factor(t*t+t/3-(s.Rational(10,3)+2*t)*t*t/4-t*(1-t)*(3*t+2)/6)==0
print('Exact scalar global-order identities verified; positivity follows from displayed Schur and xz<=((x+z)/2)^2.')
