import math
from fractions import Fraction as F
n=8; a=F(1,2); d=F(2); t=1; eps=F(1,100); afail=.01
sig=F(1,128); ah=F(36); smax=F(17,2); M=ah+smax
R=2/sig+(1+(smax+ah)/sig)**2/d
print('R=',R, float(R))
for label,delta,count in [('source',eps/(4*16807935),10),('resolvent3',eps/(4*17),3),('positive1',F(1,425),1)]:
 lam=delta/(8*a*R**2); B0=n/lam
 logN=math.log10(128)+2*math.log10(B0)-2*math.log10(delta)+math.log10(math.log(2*count/afail))
 print(label,'node delta',float(delta),'lambda',float(lam),'log10 N',logN)
# One-node, generic hypocoercive time cutoff. Allocate delta/4 each to tail,
# statistical error, numerical error, with spare error left.
delta=F(1,425); eta=d/(2*ah**2+M**2+2*d*ah); beta=min(eta*sig**2,d)/3
T=math.log(float(4*a*math.sqrt(3)/(beta*delta)))/float(beta)
B=n*T
N=32*B*B/float(delta)**2*math.log(2/afail)
print('Hypocoercivity eta',float(eta),'beta',float(beta),'T',T,'B',B,'log10 N',math.log10(N))
# Exact elementary certificates of continuation claims
import sympy as s
r=s.symbols('r'); rates=[F(1,8),F(3,16),F(1,4)]
weights=[math.prod((-z/(q-z)) for z in rates if z!=q) for q in rates]
print('weights',weights,'W',sum(abs(x) for x in weights),'bias',F(1,4)*math.prod(q/(1+q) for q in rates))
c=F(9,8); bias=F(1,4)*(c-1)/(2*(c+1)); print('one-node bias',bias,'total',bias+c*delta)
y=s.symbols('y',nonnegative=True); ca=s.Rational(9,8)
gap=(ca**2-1)*y/((1+y)*(ca**2+y)); cert=s.factor((ca-1)/(ca+1)-gap)
print('kernel gap max certificate=',cert)
assert cert==s.factor((ca-1)/(ca+1)*(y-ca)**2/((1+y)*(ca**2+y)))
