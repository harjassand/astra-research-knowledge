import sympy as S
from functools import lru_cache
u,v,w,e,t=S.symbols('u v w e t', positive=True)
@lru_cache(None)
def mom(a,b,c):
 if (a+c)%2 or (b+c)%2:return S.Integer(0)
 out=0
 for j in range(c//2+1):
  n=(a+c-2*j)//2;m=(b+c-2*j)//2
  out+= S.binomial(c,2*j)*S.rf(S.Rational(1,2),n)*S.rf(S.Rational(1,2),m)*S.rf(S.Rational(1,2),j)*S.rf(e+S.Rational(1,2),j)/(S.rf(e+1,n+j)*S.rf(e+1,m+j))
 return S.factor(out)
def ev(p):
 return S.factor(sum(coef*mom(*powers) for powers,coef in S.Poly(S.expand(p),u,v,w).terms()))
H=u*v+u*w+v*w-u-v-w
for k in (1,2,3):
 f=ev(H**k);g=S.factor(f.subs(e,1/t-1));print('EH^',k,'eta=',f,'t=',g)
 if k==2:M2=g
 if k==3:M3=g
for a in (18,7,S.Rational(27,4)):
 P=S.factor(a*M2-M3)
 diff=S.factor(P.subs(t,1)-P)
 print('a',a,'diff=',diff,'derivative1=',S.diff(P,t).subs(t,1))
 for x in (S.Rational(99,100), S.Rational(49,50),S.Rational(199,200)):
  print('t',x,'gap=',S.factor(diff.subs(t,x)))
print('M3 diff factored=',S.factor(M3.subs(t,1)-M3))
print('M3 derivative',S.factor(S.diff(M3,t)),S.diff(M3,t).subs(t,1))
