from fractions import Fraction as F
import json

def ar(m):
 a=(F(4,7)**m+F(2,7)**m+F(1,7)**m)/7-(F(2,3)**m+F(1,3)**m)/3+F(4,21)
 r=(F(4,7)**m+F(2,7)**m+F(-6,7)**m)/7-(F(2,3)**m+F(-2,3)**m)/3
 return a,r
rows=[]
for m in range(1,101):
 a,r=ar(m); det=a*a-F(1,2)**m*r*r
 assert a>=0 and det>=0
 rows.append({'m':m,'A':str(a),'R':str(r),'det_positive':det>0})
a1,r1=ar(1);a2,r2=ar(2)
assert a1==r1==0
assert a2+F(1,2)*r2==0
L=F(4,21)-(F(2,3)**4+F(1,3)**4)/3
U=F(1,4)*((F(4,7)**4+F(2,7)**4+F(6,7)**4)/7+F(2,3)*F(2,3)**4)
assert L>U
out={'gain':2,'rows':rows,'uniform_m_ge_4_A_lower':str(L),'uniform_m_ge_4_abs_C_upper':str(U),'uniform_margin':str(L-U),'scope':'Local e3 Hessian at product vacuum only; not global determinant or entropy inequality.'}
print(json.dumps(out,indent=2))
