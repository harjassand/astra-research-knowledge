#!/usr/bin/env python3
"""Independent algebra and universal power ledger, not a simulation or proof assistant.
Does not import an author module. Uses the installed SymPy exact algebra engine.
The tail domain is reparameterized T=t^4, r=u^2, 1<=u<=t.
"""
from pathlib import Path
from fractions import Fraction as F
import itertools,json
import sympy as S
here=Path(__file__).resolve().parent
counts={};details={}
def check(group,name,condition):
 if not bool(condition):raise AssertionError((group,name))
 counts[group]=counts.get(group,0)+1

def eq(name,x,y):check('symbolic_full_chain',name,S.expand(x-y)==0)
A,B,C,D,E,N=S.symbols('A B C D E N'); vars=(A,B,C,D,E)
a2=A*(A-1);h=A*E;L=A+(C+D)/2;Z=C-D;n=A+B+C+D+E;Q=L**2-C*D
# Literal stoichiometric vectors, not the derived jump table.
channels=[('imm',1,(1,0,0,0,0)),('death',A,(-1,0,0,0,0)),
 ('2A_AC',a2,(-1,0,1,0,0)),('AC_2A',A*C,(1,0,-1,0,0)),
 ('2A_AD',a2,(-1,0,0,1,0)),('AD_2A',A*D,(1,0,0,-1,0)),
 ('2A_AE',a2,(-1,0,0,0,1)),('AE_2A',h,(1,0,0,0,-1)),
 ('AE_CD',h,(-1,0,1,1,-1)),('CD_AE',2*C*D,(1,0,-1,-1,1)),
 ('CD_AB',C*D,(1,1,-1,-1,0)),('AB_CD',A*B,(-1,-1,1,1,0))]
def delta(p,d):return S.expand(p.subs({x:x+v for x,v in zip(vars,d)},simultaneous=True)-p)
u=[delta(L,d) for _,r,d in channels];v=[delta(E,d) for _,r,d in channels];w=[delta(h,d) for _,r,d in channels]
rates=[r for _,r,d in channels]
expectedu=[1,-1,-S.Rational(1,2),S.Rational(1,2),-S.Rational(1,2),S.Rational(1,2),-1,1,0,0,0,0]
expectedv=[0,0,0,0,0,0,1,-1,-1,1,0,0]
expectedw=[E,-E,-E,E,-E,E,A-E-1,E-A-1,-A-E+1,A+E+1,E,-E]
for i,(name,r,d) in enumerate(channels):
 eq(name+' L',u[i],expectedu[i]);eq(name+' E',v[i],expectedv[i]);eq(name+' h',w[i],expectedw[i]);eq(name+' mass',sum(d),(1 if i==0 else -1 if i==1 else 0))
 if i not in [1,2,3,4,5,6]:eq(name+' preserves imbalance',delta(Z,d),0)
GL=sum(r*x for r,x in zip(rates,u));GE=sum(r*x for r,x in zip(rates,v));Gh=sum(r*x for r,x in zip(rates,w))
rh=E-3*E*Q+2*A*C*D+A*(A-1)**2+2*C*D+h*(N-B+2*L+2-7*A)
eq('GL',GL,1+A+A*L+h-3*A**2);eq('GE',GE,a2-2*h+2*C*D)
eq('Gh',Gh,-N*h+3*E*L**2+rh);eq('Q',Q,2*A*L-A**2+Z**2/4)
eq('count coefficient',N-B+2*L+2-7*A,N-n+E+4*L+2-8*A)
qLL=1+A+S.Rational(3,2)*a2+A*(C+D)/4+h
qEE=a2+2*h+2*C*D;qLE=-(a2+h);sL=1+A+2*a2+A*(C+D)/2+h
qhh=E**2*(1+A+2*a2+A*(C+D)+C*D+A*B)+a2*(A-E-1)**2+2*h*((E-1)**2+A**2)+2*C*D*(A+E+1)**2
for name,found,want in [('qLL',sum(r*x*x for r,x in zip(rates,u)),qLL),('qEE',sum(r*x*x for r,x in zip(rates,v)),qEE),('qLE',sum(r*x*y for r,x,y in zip(rates,u,v)),qLE),('sL',sum(r*abs(x) for r,x in zip(rates,u)),sL),('qhh',sum(r*x*x for r,x in zip(rates,w)),qhh)]:eq(name,found,want)
# Product identity for general pre/post values is exact, including z-neutral fast channels.
f,fp,g,gp,hh,ww,tt=S.symbols('f fp g gp hh ww tt')
eq('product increment',(fp+(hh+ww)*gp/tt)-(f+hh*g/tt),fp-f+ww*g/tt+(hh+ww)*(gp-g)/tt)
for i in [10,11]:eq('fast slow increment '+str(i),u[i]**2+v[i]**2,0)
# Rate-2 is essential: changing it leaves an uncancelled CD source.
eq('rate1 counterexample',Gh-C*D*(A+E+1)-(-N*h+3*E*L**2+rh),-C*D*(A+E+1))
check('symbolic_full_chain','rate1 mismatch nonzero',S.expand(C*D*(A+E+1))!=0)

# Supplementary exact finite-jump tests; no continuum conclusion comes from samples.
for aa,cc,dd,ee in itertools.product(range(6),repeat=4):
 for bb in [0,1,7,100]:
  ll=F(2*aa+cc+dd,2);nn=aa+bb+cc+dd+ee;qq=ll*ll-cc*dd;hh=aa*ee
  rr=[1,aa,aa*(aa-1),aa*cc,aa*(aa-1),aa*dd,aa*(aa-1),hh,hh,2*cc*dd,cc*dd,aa*bb]
  check('finite_jump','Q nonnegative',qq>=0)
  check('finite_jump','omitted intensity',aa+3*aa*(aa-1)+aa*(cc+dd)<=(1+5*ll)*aa)
  for i,((name,_,d),rrr) in enumerate(zip(channels,rr)):
   if not rrr:continue
   state=(aa,bb,cc,dd,ee);out=tuple(x+y for x,y in zip(state,d))
   check('finite_jump','enabled endpoint',min(out)>=0)
   hp=out[0]*out[4]
   check('finite_jump','post hplus',0<=hp<=(aa+1)*(ee+1))
   check('finite_jump','h mark bound',abs(hp-hh)<=aa+ee+1)

# Independent positive Laurent-polynomial ledger in a different domain parameterization.
t,u0=S.symbols('t u',positive=True);T=t**4;rr=u0**2;NN=T**5;mm=T*rr;ww=T**3*u0
H=10000*ww/NN;duration=16*ww/mm**2;J=mm*H
U=duration+H+S.Rational(5,2)*mm*H+2*ww*H
W=J+2*ww*H;VE=J+4*ww*H+8*mm**2*duration;VL=duration+H+4*mm*H+2*ww*H
Qh=4*ww**2*(duration+H+6*mm*H+4*mm**2*duration+2*NN*H)+16*ww**2*J+40*ww**3*H+128*ww**2*mm**2*duration
Rh=2*ww*duration+24*mm*ww*H+9*mm**2*H+8*mm**2*duration+2*ww*H*(10*T+2*ww+8*mm+2)
def terms(expr):
 out=[]
 for term in S.Add.make_args(S.expand(expr)):
  pd=term.as_powers_dict();p=pd.get(t,S.Integer(0));q=pd.get(u0,S.Integer(0));c=S.cancel(term/t**p/u0**q)
  assert c.is_Rational and p.is_Integer and q.is_Integer
  out.append((c,int(p),int(q)))
 return sorted(out,key=lambda x:(x[1],x[2]))
def dominate(name,expr,target):
 terms0=terms(expr/target);total=S.Integer(0)
 for c,p,q in terms0:
  check('universal_tail',name+' positive coefficient',c>=0)
  check('universal_tail',name+' exponent',p+max(q,0)<=0)
  total+=c
 details[name]={'coefficient_sum':str(total),'ratio_terms':[[str(c),p,q] for c,p,q in terms0]}
 return total
for name,expr,target in [('U',U,mm),('W',W,mm),('VE',VE,ww),('VL',VL,mm),('Qh',Qh,ww**3)]:
 check('universal_tail',name+' C0',dominate(name,expr,target)<=10**7)
bases=[NN/mm,mm**2,mm**2*ww/NN,ww,mm*ww];charges=[S.Integer(0)]*5
for c,p,q in terms(Rh):
 candidates=[]
 for i,base in enumerate(bases):
  _,bp,bq=terms(base)[0]
  if p-bp+max(q-bq,0)<=0:candidates.append(i)
 check('universal_tail','Rh dominates a base',len(candidates)>0)
 # Choose minimum worst exponent, independently of the author's greedy exact-match rule.
 i=min(candidates,key=lambda i:(p-terms(bases[i])[0][1]+max(q-terms(bases[i])[0][2],0),i));charges[i]+=c
for value in charges:check('universal_tail','Rh C0',value<=10**7)
details['Rh_alternative_base_coefficients']=list(map(str,charges))
g0=S.Rational(1,32);kle=g0**-3+S.Rational(9,14)*g0**-4+S.Rational(3,14)*g0**-6;kee=S.Rational(3,10)*g0**-3+(S.Rational(3,2)+1/(2*g0**2))*kle
constants=[3**5/(5*g0**3),3**4/(2*g0**2),3**8/(7*g0**4),3**6*kle,3**5*kee]
for value in constants:check('universal_tail','derivative common D',value<10**14)
details['exact_derivative_constants']=list(map(str,constants))
D0=10**14;fl=D0/u0**5;fe=D0/u0**4;fll=D0/u0**7;fle=D0/u0**6;fee=D0/u0**5;hp=3*mm*ww
r1=fl*(1+4*mm)*H/T;r2=fe*(J+4*ww*H+8*mm*H)/T**3;r3=fl*Rh/(NN*T)
taylor=fll*U/(2*T**2)+fle*W/T**4+fee*VE/(2*T**6)
product=fll*hp*VL/(NN*T**2)+fle*hp*VE/(NN*T**4)
lo=dominate('all_nonTaylor_residuals',r1+r2+r3+product,T**-2/rr)
check('universal_tail','nonTaylor exact sum',lo==131059200000000000000);check('universal_tail','nonTaylor ceiling',lo<10**23)
ty=dominate('Taylor',taylor,T**-1/u0**5);check('universal_tail','Taylor ceiling',ty<10**23)
aa=fl/T+hp*fll/(NN*T**2);bb=fe/T**3+hp*fle/(NN*T**4);cc=fl/(NN*T)
br=dominate('full_bracket',2*(aa**2*U+2*aa*bb*W+bb**2*VE)+2*cc**2*Qh,1/(T*rr**4))
check('universal_tail','bracket exact sum',br==71293440000000000000000000000000000);check('universal_tail','bracket ceiling',br<10**40)
jump=dominate('jump',aa+bb+4*cc*ww,1/(T*u0**5));check('universal_tail','jump ceiling',jump<10**16)
ep=dominate('endpoint',2*mm*ww*fl/(NN*T),T**-2/rr);check('universal_tail','endpoint ceiling',ep<10**16)
om=dominate('omitted_compensator',11*mm*H,T**-1*u0**3);check('universal_tail','omitted geometric ceiling',2*om<400000)
# Whole-segment padding and post-jump endpoint h use actual A<=m/16.
for name,condition in [('L lower',F(1,2)-F(1,100)>=F(1,3)),('E upper',2+F(1,100)<=3),('cone',F(1,3)>=9*F(1,32)),('h endpoint',(F(1,16)+F(1,100))*(2+F(1,100))<2),('hplus',(F(1,16)+F(1,100))*(2+F(1,100))<3),('h mark',F(1,16)+2+F(1,100)<4),('clock tail',F(512,3)<200),('decreasing bracket geo',F(1,1)/(1-F(1,16))<2),('increasing omission geo',F(1,8)<F(1,4))]:check('geometry_and_clock',name,condition)
# Sharp finite endpoints not zeroed: at initial l=1/T the sensitivity bound gives O(T^-1).
# Compact power ledger with arbitrary positive fixed constants; no growing-K estimate used.
x,k,ec,hc,dc=S.symbols('x k ec hc dc',positive=True)
cm=k*x;cw=ec*x**3;ch=hc/x**2;cd=dc*x
cu=cd+ch+S.Rational(5,2)*cm*ch+2*cw*ch
cve=cm*ch+4*cw*ch+8*cm**2*cd
cvl=cd+ch+4*cm*ch+2*cw*ch
cqh=4*cw**2*(cd+ch+6*cm*ch+4*cm**2*cd+2*x**5*ch)+16*cw**2*cm*ch+40*cw**3*ch+128*cw**2*cm**2*cd
crh=2*cw*cd+24*cm*cw*ch+9*cm**2*ch+8*cm**2*cd+2*cw*ch*(10*x+2*cw+8*cm+2)
chp=(cm+1)*(2*cw+1)
def compact(name,expr,power):
 pp=[]
 for term in S.Add.make_args(S.expand(expr)):
  exponent=term.as_powers_dict().get(x,S.Integer(0));check('fixed_compact',name+' exponent',exponent<=power);pp.append(str(exponent))
 details['compact_'+name]={'largest_exponent':str(max(map(S.Rational,pp))),'bound_exponent':str(power)}
compact('qLL',cu,1);compact('qEE',cve,3);compact('qhh',cqh,9);compact('rh',crh,4)
compact('h endpoint',cm*2*cw,4)
compact('h deterministic averaging',(cm*2*cw+crh)/x**6,-2)
compact('h averaging squared martingale',cqh/x**12,-3)
compact('full residual',(1+4*cm)*ch/x+(cm*ch+4*cw*ch+8*cm*ch)/x**3+crh/x**6+cu/(2*x**2)+(cm*ch+2*cw*ch)/x**4+cve/(2*x**6)+chp*cvl/x**7+chp*cve/x**9,-1)
compact('kappa squared',cve/x**6+cqh/x**12+cu/x**4+cve/x**12+chp**2*(cu/x**14+cve/x**18),-3)
compact('leading bracket',cu/x**2,-1)
compact('small leading rates',ch+cm*ch,-1)
compact('jump',1/x+1/x**3+(cm+2*cw+1)/x**6+chp*(1/x+1/x**3)/x**6,-1)
compact('scaled E bracket',cve/x**5,-2)
# Occupation-clock threshold remains a genuine exponential estimate at fixed K.
kk=S.symbols('k',positive=True)
check('geometry_and_clock','compact A-clock margin polynomial',S.expand(25*(kk+1)**2-9*kk**2-16*kk**2)==50*kk+25)
for name,exponent in [('omission',-1+F(3,2)*F(1,2)),('terminal b',F(1,2)-F(3,2)*F(1,2)),('actual macro duration',F(5,2)-F(3,2)*F(3,2)-F(1,2)),('compact scaled residual',F(1,2)-1),('tail scaled residual',F(1,2)-1),('tail lower residual',F(1,2)-2)]:
 check('limit_exponents',name,exponent<0)
 details['exponent_'+name]=str(exponent)
check('limit_exponents','growing cutoff below macro',F(3,2)<5)
check('limit_exponents','variance tail power',-5+1==-4)
out={'status':'PASS_INDEPENDENT_EXACT_ALGEBRA_AND_UNIVERSAL_LEDGERS','checks':sum(counts.values()),'groups':counts,'details':details,'scope':'Corroborates the accompanying ordinary mathematical review; no simulation, no numerical normal CDF, no proof-assistant claim.'}
(here/'INDEPENDENT_CHECK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='details'},indent=2))
