"""Exact independent algebra checks for ALL_BACKGROUND_REDUCTION.md."""
import json
from pathlib import Path
import sympy as S

a,t,p,z,r,ta,pi,eta=S.symbols('a t p z r ta pi eta')
alpha=2*(a+1)*(3*a+1); beta=12*(1-a*a); gamma=2*(a-1)*(3*a-1)
def W(t,p,z,r):
    T=t*t+r*r; P=p*p+z*z
    return alpha*T*T+beta*T*P+gamma*P*P
# Abstract moment functional, including determinant balance.
m,c1,c2,M11,M12,m1,m2,m31,m32,m41,m42,k=S.symbols('m c1 c2 M11 M12 m1 m2 m31 m32 m41 m42 k')
# Compute expected polynomial with independent raw moments, then collect cubic/fourth terms.
raw=S.Poly(S.expand(W(t+ta,p+pi,z+eta,r)-W(t,p,z,r)),ta,pi,eta)
mom={}
for ex,coeff in raw.terms():
    if sum(ex)==0: mom[ex]=1
    elif sum(ex)==1: mom[ex]=0
    else: mom[ex]=S.Symbol('E'+''.join(map(str,ex)))
Eg=S.expand(sum(co*mom[ex] for ex,co in raw.terms()))
subs={mom[(2,0,0)]:m,mom[(0,2,0)]:M11,mom[(0,0,2)]:m-M11,mom[(1,1,0)]:c1,mom[(1,0,1)]:c2,mom[(0,1,1)]:M12,
      mom[(3,0,0)]:m1,mom[(1,2,0)]:m2-mom[(1,0,2)],mom[(2,1,0)]:m31,mom[(2,0,1)]:m32,
      mom[(0,3,0)]:m41-mom[(0,1,2)],mom[(0,0,3)]:m42-mom[(0,2,1)]}
Eg=Eg.subs(subs)
const=Eg.subs({t:0,p:0,z:0,r:0})
Eg=Eg-const+k
c=S.Matrix([c1,c2]);M=S.Matrix([[M11,M12],[M12,m-M11]]);b=S.Matrix([p,z])
L=(3*a+1)*m1+3*(1-a)*m2;N=3*(1+a)*S.Matrix([m31,m32])-(3*a-1)*S.Matrix([m41,m42])
expected=k+24*m*(a+1)**2*t*t+48*(1-a)*(1+a)*t*(c.dot(b))+8*(1-a)*(b.dot((2*m*S.eye(2)-(3*a-1)*M)*b))+8*(a+1)*L*t+8*(1-a)*N.dot(b)+16*m*(a+1)*r*r
assert S.expand(Eg-expected)==0
D=2*m*S.eye(2)-(3*a-1)*M-3*(1-a)*c*c.T/m
# Exact square-completion identity, without matrix inverse simplification.
x=S.symbols('x');v=N-L*c/m
reduced=k-S.Rational(2,3)*L*L/m+8*(1-a)*(b.dot(D*b)+v.dot(b))
completed=24*m*(x+L/(6*m)+(1-a)*c.dot(b)/m)**2+reduced+16*m*(a+1)*r*r
assert S.cancel(expected.subs(t,x/(a+1))-completed)==0
# Covariance corners and robust positive denominator.
h0=S.Rational(99,200);s=S.symbols('s');mc=3*h0/2-25*s/4;cc=S.Matrix([15*s/4,h0-5*s]);MM=S.Matrix([[h0/2-9*s/4,3*s],[3*s,h0-4*s]])
DD=2*mc*S.eye(2)-(3*a-1)*MM-3*(1-a)*cc*cc.T/mc
corners=[]
for av,sv in [(-1,0),(1,0),(1,S.Rational(1,18)),(-1,S.Rational(1,18))]:
    mat=DD.subs({a:av,s:sv});res=mat-S.eye(2)/50
    assert res[0,0]>0 and res.det()>0
    corners.append({'a':str(av),'s':str(sv),'D':str(mat),'shifted_leading_minor':str(res[0,0]),'shifted_determinant':str(S.factor(res.det()))})
assert mc.subs(s,S.Rational(1,18))==S.Rational(1423,3600)
# Ball constant and covariance inputs.
As=S.Rational(9,7);Bs=S.Rational(9,140);Cs=S.Rational(27,560)
assert S.expand(As+4*a*Bs+(6*a*a-2)*Cs-(333+72*a+81*a*a)/280)==0
assert S.Rational(1,2)-S.Rational(1,30)*S.Rational(3,20)==h0
# Endpoint formulas.
assert S.expand(W(t,p,z,r).subs(a,-1)-16*(p*p+z*z)**2)==0
assert S.expand(W(t,p,z,r).subs(a,1)-16*(t*t+r*r)**2)==0
# Abstract degree bound for the scalar numerator.
h11,h12,h22,hh11,hh12,hh22,L0,L1,V01,V02,V11,V12,k0,k1,k2=S.symbols('h11 h12 h22 hh11 hh12 hh22 L0 L1 V01 V02 V11 V12 k0 k1 k2')
HH=S.Matrix([[h11+a*hh11,h12+a*hh12],[h12+a*hh12,h22+a*hh22]])
VV=S.Matrix([V01+a*V11,V02+a*V12]);LL=L0+a*L1;KK=k0+a*k1+a*a*k2
P=(3*m*KK-2*LL*LL)*HH.det()-6*(1-a)*(VV.dot(HH.adjugate()*VV))
assert S.Poly(P,a).degree()<=4
out={'passed':True,'checks':['exact full-background expansion','stable trace square completion','four exact robust D corners','ball coefficients','degenerate endpoints','quartic scalar numerator degree'],'corners':corners}
Path(__file__).with_name('all_background_algebra_receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
