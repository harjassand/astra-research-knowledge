"""Independent direct polynomial reconstruction; python independent_audit.py."""
import sympy as s
k,e,f,lam,r,C,S=s.symbols('k eta deta lambda r C S', real=True)
P=107*k**4-232*k**3+152*k**2-24
# In the positively rotating frame: DH = r^-1 [[4(f-k e)C,-9e S],[-3(f-k e)S,-5e C]].
A=s.Matrix([[r*k+lam/r*4*(f-k*e)*C,lam/r*(-9*e*S)],
            [lam/r*(-3*(f-k*e)*S),r+lam/r*(-5*e*C)]])
u=(A[:,0].T*A[:,0])[0];v=(A[:,1].T*A[:,1])[0];j=A.det()
G=s.expand(3*(u+v-2*j)**2+s.Rational(35,24)*u*u+j*j-s.Rational(5,2)*j*u)
def average(expr):
 out=0
 for (a,b),coef in s.Poly(expr,C,S).terms():
  if a%2 or b%2: continue
  i,j=a//2,b//2
  out+=coef*s.factorial(2*i)*s.factorial(2*j)/(4**(i+j)*s.factorial(i)*s.factorial(j)*s.factorial(i+j))
 return s.factor(out)
coeff=[average(G.coeff(lam,n)) for n in range(5)]
assert coeff[1]==coeff[3]==0
Q=s.expand(2*coeff[2]);alpha=Q.coeff(f,2);beta=Q.coeff(e,2);gamma=Q.coeff(e,1).coeff(f,1)
assert alpha==s.Rational(2033,4)*k*k-s.Rational(1653,2)*k+358
assert beta==s.Rational(2033,4)*k**4-2088*k**3+3541*k*k-2916*k+936
x=s.symbols('x', real=True);eta=(x+10)*(-x)
I2=s.integrate(Q.subs({e:eta,f:s.diff(eta,x)}),(x,-10,0))
lo=s.Rational(890923272145,10**12);hi=lo+s.Rational(1,10**12)
# Independent termwise interval box (all powers k^n positive).
low=upper=0
for (n,),co in s.Poly(I2,k).terms():
 low+=co*(lo**n if co>=0 else hi**n)
 upper+=co*(hi**n if co>=0 else lo**n)
assert upper < -16000
assert s.Poly(P,k).count_roots(lo,hi)==1
# x column <= 4*(10+.9*25)=130; y column <=9*25=225.
assert 130**2+225**2 < 260**2
bound=150*260**4*s.Rational(11,4)**36
assert bound<10**28
# Direct elementary pointwise |G| coefficient, using |det A| <= |A|^2/2.
assert 12+s.Rational(35,24)+s.Rational(1,4)+s.Rational(5,4)<15
root=s.RootOf(P,1)
c=s.Rational(107,24)*k**3-s.Rational(29,2)*k*k+19*k-12+3/k
# Conservative seed overhead from basic bounding on the isolated interval.
c_lower=s.Rational(107,24)*lo**3-s.Rational(29,2)*hi**2+19*lo-12+3/hi
assert s.Rational(137,120)-c_lower/4 < 2
assert -8000*s.Rational(1,10**32)+s.Rational(1,10**36)+2*s.Rational(1,10**36)<-s.Rational(7,10**29)
print('Independent direct quartic expansion: PASS')
print('alpha =',alpha);print('gamma =',gamma);print('beta =',beta)
print('I2 interval:',float(low),float(upper))
print('sqrt(130^2+225^2) =',float(s.sqrt(130**2+225**2)))
print('quartic bound =',float(bound))
print('root =',root.evalf(17))
