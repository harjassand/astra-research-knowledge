#!/usr/bin/env python3
import sympy as S,pickle,json
from pathlib import Path
P=Path(__file__).parent;o=pickle.load(open(P/'complete_algebra.pkl','rb'));r,u,t,a,z,s=o['vars']
A,L,E,Z,n,N,lam,k,beta=S.symbols('A L E Z n N lam k beta')
Q=lambda f:(lam+beta*A)*(f.subs(A,A+1)-f)+(k+beta)*A*(f.subs(A,A-1)-f)
checks=[]
def zero(x,label):
 assert S.cancel(x)==0,label
 checks.append(label)
fall=lambda j:S.prod(A-i for i in range(j))
for j in (1,2,3):zero(Q(fall(j))-(-j*k*fall(j)+j*(lam+(j-1)*beta)*fall(j-1)),f'branching reference factorial identity j={j}')
c0,c1,c2,c3=S.symbols('c0 c1 c2 c3');d3=c3/(3*k);d2=(c2+3*(lam+2*beta)*d3)/(2*k);d1=(c1+2*(lam+beta)*d2)/k
chi=d1*fall(1)+d2*fall(2)+d3*fall(3)
M1=lam/k;M2=lam*(lam+beta)/k**2;M3=lam*(lam+beta)*(lam+2*beta)/k**3
zero(Q(chi)+(c0+c1*fall(1)+c2*fall(2)+c3*fall(3))-(c0+c1*M1+c2*M2+c3*M3),'complete physical cubic inverse')
dp=A*A-4*A*L;dm=4*A*A-4*A*L
for j,expected in [(1,-3*A*A),(2,-6*A**3+5*A*A-8*L*A),(3,-9*A**4+15*A**3-24*L*A*A-3*A*A)]:
 actual=dp*((A+1)**j-A**j)+dm*((A-1)**j-A**j)
 zero(actual-expected,f'actual reference mismatch ordinary moment {j}')
D1,D2,D3=o['chi_falling'];h=o['chi_power'];scale=u**3/(r*o['K']);cc=o['fall_coeff'];mu=o['mu'];et=o['et']
zero(3*D3-scale*cc[3],'normalized inverse degree3')
zero(2*D2-3*(mu+2*et)*D3-scale*cc[2],'normalized inverse degree2')
zero(D1-2*(mu+et)*D2-scale*cc[1],'normalized inverse degree1')
zero(h[1]-(D1-t*D2+2*t*t*D3),'power/falling coefficient1')
zero(h[2]-(D2-3*t*D3),'power/falling coefficient2')
zero(h[3]-D3,'power/falling coefficient3')
zero(mu*D1/scale-(cc[1]*mu+cc[2]*mu*(mu+et)+cc[3]*mu*(mu+et)*(mu+2*et)),'mean centering identity')
# Critical-scale asymptotics are formal rational leading terms, not a numeric fit.
K=S.symbols('K',positive=True)
for j,minimum in [(1,3),(2,4),(3,6)]:
 x=S.cancel(h[j].subs({u:K*t*t,s:1,z:0}));num,den=S.fraction(x)
 np=S.Poly(num,t);dp=S.Poly(den,t)
 ni=min(m[0] for m,c in np.terms());di=min(m[0] for m,c in dp.terms());assert ni-di>=minimum
 if j==1:zero(np.nth(ni)/dp.nth(di)-r*K,'critical leading h1=r K t^3')
 checks.append(f'critical h{j} order at least t^{minimum}')
# Check arithmetic constants used to pad full physical exit jumps.
from fractions import Fraction as F
assert (1+F(1,5000))/(1-F(1,100))<F(51,50)
assert (1+F(1,5000))**2/(1-F(1,100))<F(51,50)
assert (1+F(1,100))/(1-F(1,5000))**2<F(51,50)
assert F(1,100)+F(1,5000)<F(11,1000)
checks.append('one-step segment ratio and count padding exact inequalities')
report={'status':'PASS','symbolic_and_exact_check_count':len(checks),'checks':checks,'scope':'Complete cubic algebra, all frozen moment discrepancies, critical obstruction asymptotics, and rational padding. Uniform drift/bracket certificates and witness files are separate.'}
(P/'complete_algebra_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
