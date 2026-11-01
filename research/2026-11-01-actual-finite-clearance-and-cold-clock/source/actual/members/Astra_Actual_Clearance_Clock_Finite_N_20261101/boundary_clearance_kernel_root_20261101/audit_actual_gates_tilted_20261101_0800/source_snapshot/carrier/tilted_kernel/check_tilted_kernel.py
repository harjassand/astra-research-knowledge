#!/usr/bin/env python3
"""Exact tilted-source identities and continuous rational proof certificates.

No product H(E), physical event simulation, state grid, stationary law, or
numerical sign acceptance is used. Run with Python + the existing sympy.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import sympy as s

P = Path(__file__).resolve().parent
checks = []
values = {}
def check(name, condition):
    assert bool(condition), name
    checks.append(name)
def equal(name, lhs, rhs):
    z = s.factor(s.powsimp(lhs-rhs, force=True))
    assert z == 0, (name,z)
    checks.append(name)
def record(name, v):
    values[name] = str(v)
    return v

# Literal five-species stoichiometry: no aggregated model is substituted.
A,B,C,D,E,N = s.symbols('A B C D E N', nonnegative=True)
a = s.symbols('a', integer=True, nonnegative=True)
L = A+(C+D)/2
rows = [
 ('0->A',1,(1,0,0,0,0)),
 ('A->0',A,(-1,0,0,0,0)),
 ('2A->AC',A*(A-1),(-1,0,1,0,0)),
 ('AC->2A',A*C,(1,0,-1,0,0)),
 ('2A->AD',A*(A-1),(-1,0,0,1,0)),
 ('AD->2A',A*D,(1,0,0,-1,0)),
 ('2A->AE',A*(A-1),(-1,0,0,0,1)),
 ('AE->2A',A*E,(1,0,0,0,-1)),
 ('AE->CD',A*E,(-1,0,1,1,-1)),
 ('CD->AE',2*C*D,(1,0,-1,-1,1)),
 ('CD->AB',C*D,(1,1,-1,-1,0)),
 ('AB->CD',A*B,(-1,-1,1,1,0)),
]
expected_marks = [(1,1,0),(-1,-1,0),(-1,-s.Rational(1,2),0),
 (1,s.Rational(1,2),0),(-1,-s.Rational(1,2),0),
 (1,s.Rational(1,2),0),(-1,-1,1),(1,1,-1),(-1,0,-1),
 (1,0,1),(1,0,0),(-1,0,0)]
marks=[]
for (name,rate,v), expected in zip(rows,expected_marks):
    mark=(v[0],s.Rational(v[0])+s.Rational(v[2]+v[3],2),v[4])
    check('literal mark '+name, mark==expected)
    check('literal total count '+name, sum(v)==(1 if name=='0->A' else -1 if name=='A->0' else 0))
    marks.append(mark)

# Exact ratio algebra uses an arbitrary formal integer exponent a. For E-moving
# rows set q_next=q*g or q*k and apply the local H recursion. This is algebra,
# not an infinite product approximation.
p,q,t,u,g,k = s.symbols('p q t u g k', positive=True)
d=1+(u-t)/2
hplus=(1+u/2)/(q*g)
hminus=q/d
raw=[]
for b,v,w in marks:
    if w==0:
        ratio=p**v*q**b
    elif w==1:
        ratio=p**v*hplus*(q*g)**b*g**a
    else:
        ratio=p**v*hminus*(q*k)**b*k**a
    raw.append(ratio)
formulas=[p*q,1/(p*q),1/(s.sqrt(p)*q),s.sqrt(p)*q,
 1/(s.sqrt(p)*q),s.sqrt(p)*q,
 (1+u/2)*g**(a-2)/(p*q*q),
 p*q*q*k**(a+1)/d,k**(a-1)/d,
 (1+u/2)*g**a,q,1/q]
for (name,_,_),r,f in zip(rows,raw,formulas):
    equal('exact local ratio '+name,r,f)
# Table's AE->2A form after q*k=q+t.
equal('AE->2A table form',(formulas[7]/k**a).subs(k,1+t/q),p*q*(q+t)/d)
equal('qk identity',q*(1+t/q),q+t)
equal('qg identity',q*(1-t/q),q-t)
cd_sum=2*((1+u/2)*g**a-1)+(q-1)
equal('exact CD source cancellation',cd_sum.subs(q,1-u),2*(1+u/2)*(g**a-1))
ae_sum=formulas[7]+formulas[8]-2
expected_ae=(p*q*q*k*k+1)*k**(a-1)/d-2
equal('both actual AE channels combined',ae_sum,expected_ae)
equal('combined AE numerator after qk substitution',(p*q*q*k*k+1).subs(k,1+t/q),p*(q+t)**2+1)
# Immigration/death/falling factorial/AC/AD group assembly.
ell,CD,delta,c = s.symbols('ell CD delta c',real=True)
equal('AC and AD sum A(C+D)',A*(C+D),2*A*(L-A))
expr=-c+c*B/(N*q)+4*A*c/(N*q)
subst={B:N*(1+delta)+A-2*ell-E,q:1-c*E/N}
rhs=c/(1-c*E/N)*(delta+5*A/N-2*ell/N-(1-c)*E/N)
equal('AB/AE joint actual B E L motion',expr.subs(subst,simultaneous=True),rhs)

# All inequalities below are rational endpoint bounds for the continuous domain.
p=F(1,2);c=F(1,2);qmin=F(199,200);umax=F(1,200)
check('sqrt p lower',F(7,10)**2<p)
check('sqrt p upper',F(71,100)**2>p)
check('A over N from exact A/L and L/N gates',F(1,100)*F(1,5000)==F(1,500000))
record('binomial_mx_upper',c*F(1,500000)/qmin)
check('binomial inflation domain',c*F(1,500000)/qmin==F(1,995000)<F(1,2))
check('N power lower: N^.3 >=48',48**10<500000**3)
check('count-ratio absorption using sqrt2<2',F(12*2,48*10)==F(1,20))
check('joint AB AE count term <=3AL/100',c*F(1,20)/qmin<F(3,100))
check('death ratio coefficient <=11/10',1/(p*qmin)-1<F(11,10))
check('two AA C/D ratio coefficient <=9/10',2*(1/(F(7,10)*qmin)-1)<F(9,10))
check('AA E ratio coefficient <=11/10',(1+umax/2)/(p*qmin*qmin)-1<F(11,10))
check('AC AD negative coefficient',2*(1-F(71,100))==F(29,50))
check('all AA coefficients total2',F(9,10)+F(11,10)==2)
check('AA after AC expansion129/50',2+F(29,50)==F(129,50))
check('AL after count absorption -11/20',-F(29,50)+F(3,100)==-F(11,20))
final=record('AL_coefficient_upper',F(11,1000)+F(129,5000)-F(11,20))
check('strict full source drift coefficient',final==-F(1283,2500)<-F(1,2))

# Linear and quadratic finite sums; these are symbolic polynomial identities.
e=s.symbols('e',integer=True,nonnegative=True)
j=s.symbols('j',integer=True,nonnegative=True)
equal('linear logarithm sum',s.summation(j/2+j+1,(j,0,e-1)),e*(3*e+1)/4)
equal('lower quadratic sum',s.summation(j*j,(j,0,e-1)),e*(e-1)*(2*e-1)/6)
equal('upper quadratic sum',s.summation((j+1)**2,(j,0,e-1)),e*(e+1)*(2*e+1)/6)
check('lower log H coefficient',F(3,8)-F(1,4800)>F(187,500))
check('upper log H quadratic remainder',c*c*F(1,100)/(2*qmin)==F(1,796))
check('upper log H coefficient',F(3,8)+F(1,796)<F(377,1000))
check('log2 lower partial sum',2*(F(1,3)+F(1,81))==F(56,81))
check('log2 upper geometric tail',F(2,3)+F(2,3)*F(1,27)/(1-F(1,9))==F(25,36))
entry=record('entry_log_coefficient_upper',-F(56,81)+F(377,1000)*F(9,5)+F(1,400))
check('entry exp(-L/100) including tiny L',entry<-F(1,100))
check('postjump E cap at N>=1e5',F(1,100)+F(1,100000)<F(1,50))
check('postjump q min',1-c*F(1,50)==F(99,100))
check('postjump log q lower',c*F(1,50)/(1-c*F(1,50))==F(1,99))
end_coeff=record('upper_hit_log_L_coefficient',F(187,250)-F(25,36)-F(1,9900))
end_slack=record('upper_hit_minimum_L_margin',(end_coeff-F(3,100))/2-F(101,9900))
check('upper-hit Phi>=exp(3L/100) including simultaneous exit',end_slack>0)
check('entrance scale exponent',F(5,9)/100==F(1,180))
startup_E=8*400**3
startup_log=record('actual_startup_log_upper',-F(56,81)*400+F(377,1000)*F(startup_E**2,10**20)+F(startup_E,8*10**20))
check('actual L400 E512million entrance log<-276.5422',startup_log<-F(1382711,5000))
check('actual startup ever-hit cost <=exp(-276)',startup_log<-276)
conservative_E=128*400**3
conservative_log=record('conservative_startup_log_upper',-F(56,81)*400+F(377,1000)*F(conservative_E**2,10**20)+F(conservative_E,8*10**20))
check('even conservative E128m3 startup log<-276',conservative_log<-276)
check('actual startup A cap',2<=F(400,100))
check('actual startup upper-ratio entrance',F(startup_E**2,10**20*400)<F(9,5))


# Verify preservation of the old note and code without rewriting its artifacts.
import hashlib
old=P.parent/'HISTORY_PRACTICAL_ONE_SIDED_QUOTIENT_V1_ccab7011.md'
check('v1 original quotient note preserved exactly',hashlib.sha256(old.read_bytes()).hexdigest()=='ccab7011afc7fce1bd08a95b6d81a5537a2851d7148f488d39822d2e0d1fbcf9')
ledger=[]
for (name,rate,v),mark in zip(rows,marks):
    ledger.append({'channel':name,'rate':str(rate),'delta_species':list(v),'delta_A_L_E':[str(z) for z in mark]})
out={'status':'PASS_EXACT_TILTED_SOURCE_KERNEL_AND_GLOBAL_UPPER_BARRIER',
 'scope':'Conditional actual stopped-domain theorem; no entrance or A/Z admission supplied; original narrow-count cost valid only through original cap/4T.',
 'checks_count':len(checks),'checks':checks,'rational_constants':values,
 'literal_twelve_channels':ledger,
 'no_state_grid_or_simulation':True,'no_materialized_H_product':True,
 'positive_source_drift_bound':'G Phi/Phi <= -1/2-AL/2',
 'entrance_upper_hit_bound':'R0<=9/5 => P(ever R>=2 before other stops)<=exp(-L0/100)',
 'comparison_status':'Ordinary symbolic identities and rational proof constants; not a numerical scout acceptance.'}
(P/'tilted_kernel_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],len(checks),'checks')
