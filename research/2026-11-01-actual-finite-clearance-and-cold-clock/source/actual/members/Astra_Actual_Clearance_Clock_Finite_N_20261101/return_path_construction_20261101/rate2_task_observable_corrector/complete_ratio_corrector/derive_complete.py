#!/usr/bin/env python3
"""Exact normalized complete cubic construction; algebra only."""
import sympy as S, json, pickle, time
from pathlib import Path
r,u,t,a,z,s=S.symbols('r u t a z s')
cd=(1-a)**2-z*z/4
# q=rate/L^2; increments in A,L,E,Z,total n
rows=[('0->A',t*t,(1,1,0,0,1)),('A->0',a*t,(-1,-1,0,0,-1)),
('2A->AC',a*(a-t),(-1,-S.Rational(1,2),0,1,0)),('AC->2A',a*(1-a+z/2),(1,S.Rational(1,2),0,-1,0)),
('2A->AD',a*(a-t),(-1,-S.Rational(1,2),0,-1,0)),('AD->2A',a*(1-a-z/2),(1,S.Rational(1,2),0,1,0)),
('2A->AE',a*(a-t),(-1,-1,1,0,0)),('AE->2A',a*r/u,(1,1,-1,0,0)),('AE->CD',a*r/u,(-1,0,-1,0,0)),
('CD->AE',2*cd,(1,0,1,0,0)),('CD->AB',cd,(1,0,0,0,0)),('AB->CD',a*(s*r/u**2-2+a-r/u),(-1,0,0,0,0))]
coeff=[S.Integer(0)]*4
for name,q,j in rows:
 da,dl,de,dz,dn=j
 c=1+de*u*t/r;h=1+dl*t
 f0=r*(c*c/h-1)-r*u*t*da*c**3/h**2
 f1=-r*u*(c**3/h**2-1)
 pp=S.Poly(S.expand(q*(f0+f1*a)/(u*t)),a)
 for i in range(4):coeff[i]+=pp.nth(i)
D0=4-3*r-r*t*t/u
coeff[0]-=D0
coeff=[S.factor(S.cancel(x)) for x in coeff]
print('coeff sizes',[(i,len(str(x))) for i,x in enumerate(coeff)],flush=True)
K=s-u+2*u*u*(1-t)/r
Lam=3-3*z*z/4+t*t
mu=u*u*Lam/(r*K);et=t*u/K
c=[coeff[0],coeff[1]+t*coeff[2]+t*t*coeff[3],coeff[2]+3*t*coeff[3],coeff[3]]
scale=u**3/(r*K)
d3=S.factor(S.cancel(scale*c[3]/3))
d2=S.factor(S.cancel(scale*c[2]/2+S.Rational(3,2)*(mu+2*et)*d3))
d1=S.factor(S.cancel(scale*c[1]+2*(mu+et)*d2))
print('falling chi sizes',list(map(lambda x:len(str(x)),[d1,d2,d3])),flush=True)
# Coefficients in powers of a. chi=h1*a+h2*a^2+h3*a^3.
h=[S.Integer(0),S.factor(S.cancel(d1-t*d2+2*t*t*d3)),S.factor(S.cancel(d2-3*t*d3)),d3]
# Mean is calculated in factored form; avoid giant expansion for interval proof.
M=[1,mu,mu*(mu+et),mu*(mu+et)*(mu+2*et)]
mean=D0+sum(c[j]*M[j] for j in range(4))
print('ordinary chi sizes',list(map(lambda x:len(str(x)),h)),flush=True)
# Cancel normalized mean: needed to remove spurious 1/u poles.
mean=S.factor(S.cancel(mean))
print('mean size',len(str(mean)),flush=True)
path=Path(__file__).parent
obj={'vars':(r,u,t,a,z,s),'rows':rows,'coeff':coeff,'fall_coeff':c,'chi_falling':(d1,d2,d3),'chi_power':h,'K':K,'Lam':Lam,'mu':mu,'et':et,'mean':mean,'D0':D0}
with open(path/'complete_algebra.pkl','wb') as f:pickle.dump(obj,f)
(path/'exact_formulas.txt').write_text('\n\n'.join([f'p{i} = {x}' for i,x in enumerate(coeff)]+[f'chi_a{i} = {x}' for i,x in enumerate(h[1:],1)]+[f'mean_normalized = {mean}'])+'\n')
(path/'construction_metadata.json').write_text(json.dumps({'residual_degree':3,'coefficient_expression_lengths':[len(str(x)) for x in coeff],'chi_expression_lengths':[len(str(x)) for x in h[1:]],'mean_expression_length':len(str(mean)),'status':'EXACT_FORMULAS_ONLY_NOT_YET_UNIFORM_CERTIFICATE'},indent=2)+'\n')
