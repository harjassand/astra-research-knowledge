#!/usr/bin/env python3
"""Independent literal-species algebra and exact source-charge arithmetic.
No author checker, evaluator, derivative solver, simulation, or external source.
"""
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
import hashlib,json,math
import sympy as s
ROOT=Path(__file__).parent
checks=[]
def ck(ok,label):
 assert ok,label
 checks.append(label)
def eq(x,y,label):ck(s.expand(x-y)==0,label)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source_bindings={
 '../../return_path_construction_20261101/rate2_task_observable_corrector/TASK_OBSERVABLE_CORRECTOR.md':'02e55555d845f7f3060e23500cb36934fbfd4709eb8755c9b1ebf2cfa7002a94',
 '../REMAINING_CLOCK_OBSERVABLE.md':'3738ec11751d5e094e70c5f32d7dedfe2ff978403cd7b4b6be18816bbf0cf555',
 '../CLOCK_WINDOW_REMAINING_CLOCK_INDEPENDENT_REVIEW.md':'136ad45a73828823abbdeeeff8fbb32948ece44577682390c96e97a3b291f470',
 'source_snapshot/full/FULL_CORRECTED_CLOCK_BRACKET.md':'f64bc7cf924af8f6c4ffd1a58b236763b49c874d9c2ac5cf5be80e95a133edf4',
 'source_snapshot/main/MAIN_WEIGHTED_CLOCK.md':'7f1d8341f515a29e4b55880ac327949599238e39ec1bb2c5f3e8ef030538ef61',
 'source_snapshot/residual/ACTUAL_CLOCK_RESIDUAL_BUDGET.md':'2ceb7e685692bfa2ae26e42b4080c074d009dad5320132c4a127b677898e8d07',
 '../GLOBAL_L_WEIGHTED_CLOCK_DERIVATIVES.md':'20dff0a1775870b93aa81a12bb88125892f242a0986438b3ce9e63e0c4d83ccb',
 '../REGULARIZED_WEIGHTED_SOURCE_BUDGET.md':'38973f8baacbadb5c8fdf63cac93e2aed49b7831883cd4c3943aff3e3ac10b2b',
 '../audit_global_derivatives_regularized_storage_20261101/REVIEW_RECEIPT.json':'e1c1eb76b8592a098bdad9f6188b7f7f08e7d0e75ce153bc9a06aa53950dcae8'}
for p,h in source_bindings.items():ck(digest(ROOT/p)==h,'hash '+p)
A,B,C,D,E,N=s.symbols('A B C D E N'); species=(A,B,C,D,E)
channels=[(1,(1,0,0,0,0)),(A,(-1,0,0,0,0)),
 (A*(A-1),(-1,0,1,0,0)),(A*C,(1,0,-1,0,0)),
 (A*(A-1),(-1,0,0,1,0)),(A*D,(1,0,0,-1,0)),
 (A*(A-1),(-1,0,0,0,1)),(A*E,(1,0,0,0,-1)),
 (A*E,(-1,0,1,1,-1)),(2*C*D,(1,0,-1,-1,1)),
 (C*D,(1,1,-1,-1,0)),(A*B,(-1,-1,1,1,0))]
L=A+(C+D)/2;Z=C-D; h=A*E;Q=L*L-C*D

def step(f,v):return s.expand(f.subs(dict(zip(species,[x+y for x,y in zip(species,v)])),simultaneous=True)-f)
def gen(f):return s.expand(sum(lam*step(f,v) for lam,v in channels))
u=[step(L,v) for lam,v in channels];ev=[v[4] for lam,v in channels]
qll=s.expand(sum(channels[i][0]*u[i]**2 for i in range(12)))
qee=s.expand(sum(channels[i][0]*ev[i]**2 for i in range(12)))
sl=s.expand(sum(channels[i][0]*abs(u[i]) for i in range(12)))
wle=s.expand(sum(channels[i][0]*abs(u[i]*ev[i]) for i in range(12)))
eq(gen(L),1+A+A*L-3*A*A+A*E,'actual GL')
eq(qll,1-A/2+A*A+A*L/2+A*E,'actual qLL')
eq(gen(L)-qll,A*(s.Rational(3,2)+L/2-4*A),'actual GL-qLL')
eq(sl,1-A+A*A+A*L+A*E,'actual sL')
eq(qee,A*(A-1)+2*A*E+2*C*D,'actual qEE')
eq(wle,A*(A-1)+A*E,'actual wLE')
rh=E-3*E*Q+2*A*C*D+A*(A-1)**2+2*C*D+A*E*(N-B+2*L+2-7*A)
eq(gen(h),-N*h+3*E*L*L+rh,'full actual Gh identity')
ck(u[10]==u[11]==ev[10]==ev[11]==0,'fast rows have exactly zero slow increments')
# Main continuous constants: monotonic R(T) reduces these to endpoints.
R=F(10,9)**5;RR=F(10000,9999)**5
ck(R<2 and R*R<3,'main T>=10 R bounds')
ck(RR<F(1001,1000) and RR*RR<F(1003,1000),'main T>=10000 R bounds')
ck(F(5,2)*F(1001,1000)<3,'aT>=.9997T for T>=10000')
ck(F(5,4)**2/(2*(15+F(5,12)))>=F(1,20),'main 5/T Freedman exponent')
ck(4-F(5,4)-F(25600,17100)>=F(5,4),'main 8/T drift threshold')
ck(F(5,4)**2/(2*(24+F(5,12)))>=F(1,32),'main 8/T exponent')
ck(F(9997,10000)*F(3,2)-F(5,4)-F(25600,171*10000**2)>F(1,5),'main practical threshold')
ck(F(1,25)/(2*(F(3009,2000)+F(1,15)))>F(1,80),'main practical exponent')
# Derivative-domain padding checks, with irrational powers squared exactly.
ck(81*F(200,199)**7<100,'all-segment F20 inflation')
ck(13*F(200,199)**3<14,'all-segment F11 inflation')
ck(148**2*F(200,199)**5<150**2,'all-segment F02 inflation')
ck(F(401,10000)<=F(1,2),'startup l rectangle')
ck(F(512000001,10000**3)<F(1,1000),'startup e rectangle')
ck(F(200)-3-F(1,50)-F(1,10000**5)>0,'post-startup complete cone padding')
ck(F(2349,16)<148,'startup b_ee bound')
ck(F(3,2)+(F(3,2000)+2)*8<18,'rectangle l>=1/2 b_ee')
ck(sum(F(1,math.factorial(k)) for k in range(12))+F(1,math.factorial(12))/(1-F(1,13))<3,'exact exp1 upper')
# Polynomial coefficients independently expanded before assigning dimensions.
a,x,y,z=s.symbols('a x y z');K=F(800,171);J=F(404,17)
groups={
 'l drift':(a+2*a*x,F(5,2),1),
 'e drift':(30*a*x+12*a*y,F(2),3),
 'Gh remainder':(y+10*a*y*x+3*a*x*x+2*z+a*y*y+2*a*y,F(5,2),6),
 'count remainder':(12*a*y,F(5,2),5),
 'll Taylor':(5+s.Rational(15,2)*a*x+5*a*y,F(7,2),2),
 'le Taylor':(14*a*x+14*a*y,F(3),4),
 'ee Taylor':(75*a*x+150*a*y+150*z,F(5,2),6),
 'll product':(10*(a+1)*(y+1)*(1+2*a*x+a*y),F(7,2),7),
 'le product':(14*(a+1)*(y+1)*(a*x+2*a*y+2*z),F(3),9)}
coefs=defaultdict(F);ledger=[]; by_group={}
for name,(poly,p,k) in groups.items():
 subtotal=defaultdict(F)
 for powers,c in s.Poly(s.expand(poly),a,x,y,z).terms():
  aa,xx,yy,zz=powers;c=F(int(c.p),int(c.q));ck(c>0,'positive monomial '+name+str(powers))
  # Retain one A for its source clock; CD terms instead pay their own source.
  if zz:
   ck(zz==1,'CD degree one '+name+str(powers)); lp=xx+aa
   ck(p>=1+lp+F(yy,2),'weighted CD decay '+name+str(powers))
   source='CD_phi';constant=6*J*F(3,2)**yy;tp=lp+3*yy+3-k
  elif aa:
   lp=xx+aa-1
   if p>=1+lp+F(yy,2):
    source='A_phi';constant=6*K*F(3,2)**yy;tp=lp+3*yy-2-k
   else:
    ck(p>=lp+F(yy,2),'unweighted A decay '+name+str(powers))
    source='A_plain';constant=F(3,2)**yy;tp=lp+3*yy-k
  else:
   ck(p>=xx+F(yy,2),'horizon decay '+name+str(powers))
   source='time';constant=4*F(3,2)**yy;tp=xx+3*yy+1-k
  subtotal[-tp]+=c*constant;coefs[-tp]+=c*constant
  ledger.append({'group':name,'powers_A_L_E_CD':powers,'source':source,'weight_power':str(p),'coefficient':str(c*constant),'inverse_T_power':-tp})
 by_group[name]={str(k):str(v) for k,v in sorted(subtotal.items())}
coefs[0]+=F(11,20000)
expected=[F(11,20000),20+45*K,6+F(537,2)*K+252*J,60+312*K+1164*J,24+936*K,2100*K+168*J,40+180*K+168*J,948*K,372*K,144*K,84*K]
ck(dict(coefs)==dict(enumerate(expected)),'independent full residual coefficient match')
ck(coefs[1]==F(4380,19),'exact residual T^-1 coefficient')
rem=sum(coefs[k]/10000**(k-2) for k in range(2,11))
ck(rem<F(1450753,200),'residual tail below7253.765')
ck(rem<7254,'residual advertised7254 coefficient')
ck(sum(x['source']=='A_plain' for x in ledger)==2,'exactly two unweighted A monomials')
ck(5000**3<355000**2,'macro L terminal constant')
ck(F(3,2)*100**3<3000000,'macro E terminal constant')
# Full corrected observable: formal exact partial derivatives and every actual row.
aa,LL,EE,TT=s.symbols('aa LL EE TT',positive=True); BB=s.Function('clock'); xx,yy=s.symbols('xx yy')
# A symbolic arbitrary second-order jet suffices: the full gradient uses exactly
# b_l,b_e,b_ll,b_le; independent coefficients avoid Subs canonicalization artifacts.
c00,c10,c01,c20,c11,c02=s.symbols('c00 c10 c01 c20 c11 c02')
jet=c00+c10*xx+c01*yy+c20*xx**2/2+c11*xx*yy+c02*yy**2/2
sub={xx:LL/TT,yy:EE/TT**3}; val=jet.subs(sub)
gradL=s.diff(jet,xx).subs(sub);gradE=s.diff(jet,yy).subs(sub)
hessLL=s.diff(jet,xx,2).subs(sub);hessLE=s.diff(jet,xx,yy).subs(sub)
corrected=val+aa*EE*gradL/TT**6
ck(s.expand(s.diff(corrected,aa)-EE*gradL/TT**6)==0,'full exact partial A arbitrary second jet')
ck(s.expand(s.diff(corrected,LL)-gradL/TT-aa*EE*hessLL/TT**7)==0,'full exact partial L arbitrary second jet')
ck(s.expand(s.diff(corrected,EE)-gradE/TT**3-aa*(gradL+EE*hessLE/TT**3)/TT**6)==0,'full exact partial E arbitrary second jet')
g0,g1,f0,f1=s.symbols('g0 g1 f0 f1')
for i,(rate,vv) in enumerate(channels):
 da=vv[0];de=vv[4];hp=(A+da)*(E+de)
 eq(hp-h,E*da+A*de+da*de,'full simultaneous product row '+str(i))
 eq(f1+hp*g1/TT**6-f0-h*g0/TT**6,(f1-f0)+(hp-h)*g0/TT**6+hp*(g1-g0)/TT**6,'full corrected product row '+str(i))
 ck(abs(da)==1 and abs(de)<=1 and abs(u[i])<=1,'full actual mark magnitudes '+str(i))
# Continuous l<=1 and l>=1 envelope reductions, exactly at worst T/cap values.
ck(F(243,10**4)<F(1,25),'coarse small-l L correction square')
ck(F(75,16000)<F(1,25),'coarse large-l L correction square')
ck(F(27,100)<F(3,10),'small-l E correction')
ck(F(9,4000)<F(9,100),'large-l E correction square')
ck(F(243,10000**4)<F(49,10000),'practical small-l L correction')
ck(F(75,16000)<F(49,10000),'practical large-l L correction')
phi_ratio=F(1000,999)**2
ck(phi_ratio<F(101,100),'full regularized weight segment ratio')
ck(24*phi_ratio<25,'full A gradient squared source coefficient')
ck(49*8*phi_ratio<400,'full E gradient squared source coefficient')
ck(F(36,25)*R<F(5,2),'full coarse L squared source coefficient')
ck(F(107,100)**2*RR<F(23,20),'full practical L squared source coefficient')
ck(F(21,20)*F(23,20)==F(483,400),'full asymmetric Cauchy L')
ck(42*(25+400)==17850,'full asymmetric Cauchy fast and E')
ck(F(21,19)<F(303,17),'full complete-rate source ratio maximum')
ck(F(4,100)+F(1212,17)<72,'full original-horizon source charge')
ck(F(483,400)*F(3,2)==F(1449,800),'full practical bracket coefficient T^-1')
ck(17850*72==1285200,'full practical bracket coefficient T^-3')
ck(F(107,100)+F(9,10000**2)<F(27,25),'full all-jump practical cap')
ck(F(6,5)+F(9,100)<F(13,10),'full all-jump coarse cap')
ck(F(1,5000)+F(1,100000)<=F(1,4000),'full L/N cap includes exit jump')
full_examples=[]
for t in (10000,100000):
 v=F(1449,800*t)+F(1285200,t**3);j=F(27,25*t)
 full_examples.append({'T':t,'v_exact':str(v),'j_exact':str(j)})
report={'status':'PASS_INDEPENDENT_MAIN_FULL_BRACKET_AND_RESIDUAL_EXACT_CHECKS','assertion_count':len(checks),'checks':checks,
 'source_bindings':source_bindings,'full_bracket_examples':full_examples,'residual_coefficients':{str(k):str(v) for k,v in sorted(coefs.items())},
 'residual_tail_exact':str(rem),'source_charge_ledger':ledger,'groups':by_group,
 'scope':'Ordinary analytic receipts supply continuous finite-jump and stopping proofs; no samples stand in for those proofs.'}
(ROOT/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],len(checks));print('residual T^-2 tail',float(rem))
