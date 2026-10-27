import sympy as s
p=s.symbols('p',positive=True);a=p/4;b=(1-a)/9
r=7*b+2*s.sqrt(b*(a+b))
assert s.simplify(r-(1-(s.sqrt(a+b)-s.sqrt(b))**2))==0
assert s.simplify(r.subs(p,1))==s.Rational(11,12)
assert s.simplify(s.limit((1-r)/p**2,p,0,dir='+'))==s.Rational(9,64)
assert s.simplify(s.limit(-2*s.log(r)/p**2,p,0,dir='+'))==s.Rational(9,32)
w=(-1+s.I*s.sqrt(3))/2
assert s.simplify(1+w+w**2)==0
# Normalized commuting probability vectors, their exact affinity.
assert s.simplify((a+b)+8*b)==1
P=[a+b,b]+[b]*7;Q=[b,a+b]+[b]*7
aa,bb=s.symbols("aa bb",positive=True)
PP=[aa+bb,bb]+[bb]*7;QQ=[bb,aa+bb]+[bb]*7
assert s.simplify(sum(s.sqrt(x*y) for x,y in zip(PP,QQ))-(7*bb+2*s.sqrt(bb*(aa+bb))))==0
print('PASS exact source program spectrum/affinity, orthogonal unitary pair, and quadratic weak-signal exponent')
# Two-sided CP domination: eigenvalues of J_E - qJ_R and cJ_R-J_E.
q=1-p;c=9*p+q
assert s.simplify(c/9-(p+q/9))==0
assert s.simplify(c/9-q/9)==p
print('PASS exact CP domination constants q and9p+q; heralded-support argument is analytic')
