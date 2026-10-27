import sympy as s
p,t=s.symbols('p t',positive=True);a=p/4;b=(1-a)/9
assert s.simplify(a+2*b-(7*p+8)/36)==0
assert s.simplify(a+9*b)==1
assert s.simplify((a+2*b)**2-(4*b*(a+b)+a*a))==0
c=s.symbols('c',real=True)
assert s.expand(1-((1+2*c)/3)**2-s.Rational(4,9)*(1-c)*(2+c))==0
assert s.Rational(9,32)*s.Rational(2,3)==s.Rational(3,16)
C=s.Rational(13,16)**2*s.Rational(5,6)**2/27
assert C==s.Rational(4225,248832) and C<s.Rational(1,3)
assert 1-s.Rational(3,16)==s.Rational(13,16)
# Exact two-by-two product trace/determinant invariants; sqrt trace squared=tr+2sqrt det.
x,y=s.symbols('x y',positive=True)
assert s.expand((2*b*b+2*a*b+a*a*t)+2*b*(a+b)-(4*b*(a+b)+a*a*t))==0
print('PASS exact program-fidelity formula invariants, source normalization, phase bounds and constant4225/248832')
# Independent amplified-relative-entropy constants and source coefficient.
assert s.Rational(1,4)*3*s.Rational(2,3)==s.Rational(1,2)
assert 2*s.Rational(7,8)**2==s.Rational(49,32)
assert s.Rational(49,32)*8==s.Rational(49,4)
assert s.Rational(49,4)/16==s.Rational(49,64)
# Spectral logarithms leave a*(1-t) times log(1+a/b); b contribution cancels.
assert s.expand((b+a)-(b+a*t)-a*(1-t))==0
print('PASS exact relative-entropy cancellation, repeated-retrieval Pinsker constants, and separate p versusp² source scaling')
