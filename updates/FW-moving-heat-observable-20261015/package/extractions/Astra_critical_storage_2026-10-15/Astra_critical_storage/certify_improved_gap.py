"""Exact certificate for L=6, lambda=2e-7, seed=1e-4."""
import runpy
import sympy as s
D=runpy.run_path(__file__.replace('certify_improved_gap.py','independent_audit.py'))
k,e,f,r=D['k'],D['e'],D['f'],D['r'];lo,hi=D['lo'],D['hi']
t=s.symbols('t',real=True)
L=s.Integer(6)
# x=-t, so d eta/dx = 2t-L.
Q=s.Poly(s.expand((D['coeff'][4]*r**4).subs({e:t*(L-t),f:2*t-L})),t).as_expr()
A=sum((-1)**j*s.diff(Q,t,j)/(4*k)**(j+1) for j in range(9))
assert s.simplify(s.diff(A,t)+4*k*A-Q)==0

def add(x,y):return x[0]+y[0],x[1]+y[1]
def mul(x,y):
 z=[a*b for a in x for b in y];return min(z),max(z)
def div(x,y):
 assert y[0]>0
 return mul(x,(1/y[1],1/y[0]))
def pol(expr):
 z=(s.S(0),s.S(0))
 for co in s.Poly(expr,k).all_coeffs(): z=add(mul(z,(lo,hi)),(co,co))
 return z
def rat(expr):
 nu,de=s.fraction(s.cancel(expr));return div(pol(nu),pol(de))
def expbox(x,N=120):
 # x is nonnegative rational; tail bounded by geometric ratios.
 terms=[s.S(1)]
 for j in range(1,N+2):terms.append(terms[-1]*x/j)
 v=sum(terms[:N+1]);tail=terms[N+1]/(1-x/(N+2))
 assert x<N+2
 return v,v+tail
Exp=(expbox(24*lo)[0],expbox(24*hi)[1])
a6=rat(A.subs(t,6));a0=rat(A.subs(t,0))
J=add(mul(Exp,a6),(-a0[1],-a0[0]))
assert J[0]>0 and J[1]<10**15
I=pol(D['alpha']*L**3/3+D['beta']*L**5/30)
assert I[1]<-173
lam=s.Rational(2,10**7);seed=s.Rational(1,10**4)
upper=lam**2*s.Rational(-173,2)+lam**4*10**15+2*seed**4
assert upper < -s.Rational(18,10**13)
# exp(6k) < 10^4 proves log(10^4)/k >6.
assert expbox(6*hi)[1]<10**4
print('EXACT STRONGER GAP: PASS')
print('I2 interval:',float(I[0]),float(I[1]))
print('JH interval:',float(J[0]),float(J[1]))
print('Rigorous coarse action excess upper bound:',upper, float(upper))
print('Gain is strictly greater than 1.8e-12.')
