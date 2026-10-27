"""Exact shared-clock polynomial and sign-propagation receiver. No numeric decisions."""
import sympy as S
import json,hashlib
from pathlib import Path
s,b,e,f=S.symbols('s b e f');w=s+b;A=2*(s+1)*w-b
A2=4*(s+1)**2*w*w-2*b*(s+1)*w+b*b*e
B2=(s+3)**2*w*w-b*(s+3)*w+b*b*e
N2=S.Poly(S.expand(3**18*s**5*A*A*A2*A2*(s+1)**6-64*w*(3*w+1)**3*(3*s+1)**15*B2),s)
A3=A**3+b*A*A+b*b*e*A+b**3*f
B3=(s+3)**3*w**3-b*(s+3)**2*w*w+b*b*e*(s+3)*w-b**3*f
N3=S.Poly(S.expand(3**27*s**9*A3*A3*(s+1)**12-64*(3*w+1)**3*(3*s+1)**24*B3),s)
assert N2.degree()==21 and N3.degree()==31
assert S.factor(N2.nth(0)+64*b**3*(3*b+1)**3*(e+6))==0
assert S.factor(N3.nth(0)+64*b**3*(3*b+1)**3*(3*e-f+18))==0
for N in [N2,N3]:
 assert N.LC()>0 and N.nth(3).subs(b,0)<0
 assert all(N.nth(j).subs(b,0)==0 for j in range(3))
# Receive that these are the original determinant ratios, not arbitrary polynomials.
x=1/s;y=1/w;z=y-x;h=1+x;v=1+3*x
out2=(h+z/2)*(h*h+h*z/2+z*z*e/4);ref2=v*v+v*z+z*z*e
rat2=out2**2*h**6/((1+y/3)**3*(1+x/3)**15*ref2)
assert S.factor(rat2-3**18*s**5*A*A*A2*A2*(s+1)**6/(64*w*(3*w+1)**3*(3*s+1)**15*B2))==0
q=1+x+z/2;out3=q**3-q*q*z/2+q*z*z*e/4-z**3*f/8;ref3=v**3+v*v*z+v*z*z*e+z**3*f
rat3=out3**2*h**12/((1+y/3)**3*(1+x/3)**24*ref3)
assert S.factor(rat3-3**27*s**9*A3*A3*(s+1)**12/(64*(3*w+1)**3*(3*s+1)**24*B3))==0
metadata=[]
# Closed e interval, including e=1/4: homogeneous h0,h1 coordinates.
h0,h1=S.symbols('h0 h1');co2={}
for j in range(22):
 P=S.Poly(N2.nth(j),e);co2[j]=S.Poly(S.expand(sum(P.nth(i)*h1**i*(h0+h1)**(2-i)/4**i for i in range(3))),b,h0,h1)
weights2={7:(182,718,98,1),8:(264,567,169,1),9:(308,456,235,2),10:(0,566,361,73),11:(0,412,502,86),12:(0,376,367,257)}
# Ordered Schmidt gaps: lambda proportional to(g0+g1+g2,g0+g1,g0).
g0,g1,g2=S.symbols('g0 g1 g2');l1=g0+g1+g2;l2=g0+g1;l3=g0;D=l1+l2+l3;E=l1*l2+l1*l3+l2*l3;F=l1*l2*l3;co3={}
for j in range(32):
 P=S.Poly(N3.nth(j),e,f);co3[j]=S.Poly(S.expand(sum(c*E**i*F**k*D**(6-2*i-3*k) for (i,k),c in P.terms())),b,g0,g1,g2)
weights3={13:(2249,6100,1642,10),14:(3390,4407,2193,10),15:(4136,2993,2861,10),16:(0,5709,2968,1324),17:(0,4300,4143,1557)}
for rank,N,co,weights,low,high,vs,deg in [(2,N2,co2,weights2,6,14,(h0,h1),2),(3,N3,co3,weights3,12,19,(g0,g1,g2),6)]:
 for j in range(low+1):assert all(c<0 for c in co[j].coeffs())
 for j in range(high,N.degree()+1):assert all(c>0 for c in co[j].coeffs())
 chains=[]
 for j,(aa,bb,cc,dd) in weights.items():
  P=S.Poly((cc*b+dd)*co[j+1].as_expr()-(aa*b+bb)*co[j].as_expr(),b,*vs)
  assert all(c>0 for c in P.coeffs())
  # Strict even on all closed-simplex faces: a pure gap monomial survives at b=0.
  for z0 in vs:assert P.coeff_monomial(z0**deg)>0
  coefficients=[{'powers':list(mon),'coefficient':str(c)} for mon,c in P.terms()]
  chains.append({'index':j,'weights_A_B_C_D':[aa,bb,cc,dd],'positive_coefficients':coefficients})
 print('rank',rank,'low/high signs and',len(chains),'strict positive chains PASS;',sum(len(c['positive_coefficients']) for c in chains),'chain coefficients',flush=True)
 metadata.append({'rank':rank,'degree':N.degree(),'low_negative_through':low,'high_positive_from':high,'source_coefficients':[str(N.nth(j)) for j in range(N.degree()+1)],'chains':chains})
Path(__file__).with_suffix('.json').write_text(json.dumps({'method':'exact shared-clock Descartes sign-propagation','cases':metadata},indent=2))
print('PASS: actual determinant ratios, closed Schmidt domains, all integer coefficient chains, endpoint signs.')
