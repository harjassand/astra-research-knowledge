#!/usr/bin/env python3
"""Separately entered full twelve-channel algebra and rational receiver margins."""
from fractions import Fraction as F
from pathlib import Path
import json, hashlib
import sympy as s
P=Path(__file__).resolve().parent; checks=[]; values={}
def ck(name,truth):assert bool(truth),name;checks.append(name)
def eq(name,lhs,rhs):ck(name,s.factor(s.expand(lhs-rhs))==0)
A,B,C,D,E,N=s.symbols('A B C D E N',nonnegative=True);species=(A,B,C,D,E)
channels=[('birth',1,(1,0,0,0,0)),('death',A,(-1,0,0,0,0)),
 ('AA_AC',A*(A-1),(-1,0,1,0,0)),('AC_AA',A*C,(1,0,-1,0,0)),
 ('AA_AD',A*(A-1),(-1,0,0,1,0)),('AD_AA',A*D,(1,0,0,-1,0)),
 ('AA_AE',A*(A-1),(-1,0,0,0,1)),('AE_AA',A*E,(1,0,0,0,-1)),
 ('AE_CD',A*E,(-1,0,1,1,-1)),('CD_AE',2*C*D,(1,0,-1,-1,1)),
 ('CD_AB',C*D,(1,1,-1,-1,0)),('AB_CD',A*B,(-1,-1,1,1,0))]
L=A+(C+D)/2;Z=C-D;UU=E-A/2
marks=[]
def dm(f,v):return s.expand(f.subs({x:x+d for x,d in zip(species,v)},simultaneous=True)-f)
def gen(f):return s.expand(sum(rate*dm(f,v) for name,rate,v in channels))
def bracket(f):return s.expand(sum(rate*dm(f,v)**2 for name,rate,v in channels))
for name,rate,v in channels:
 marks.append((name,dm(A,v),dm(L,v),dm(E,v),dm(Z,v),dm(UU,v)))
 ck('A unit mark '+name,abs(dm(A,v))==1)
 ck('L mark bound '+name,abs(dm(L,v))<=1)
 ck('Z mark bound '+name,abs(dm(Z,v))<=1)
 ck('U mark bound '+name,abs(dm(UU,v))<=s.Rational(3,2))
eq('GA',gen(A),1-A-3*A*(A-1)+A*(C+D)+3*C*D-A*B)
eq('GL',gen(L),1+A+A*L-3*A*A+A*E)
eq('qLL',bracket(L),1-A/2+A*A+A*L/2+A*E)
eq('GL-qLL',gen(L)-bracket(L),A*(s.Rational(3,2)+L/2-4*A))
eq('GZ',gen(Z),-A*Z)
eq('qZ',bracket(Z),2*A*(L-1))
eq('A up',sum(rate for name,rate,v in channels if v[0]==1),1+A*(C+D)+A*E+3*C*D)
eq('A down',sum(rate for name,rate,v in channels if v[0]==-1),A+3*A*(A-1)+A*E+A*B)
eq('E up',sum(rate for name,rate,v in channels if v[4]==1),A*(A-1)+2*C*D)
eq('E-up ceiling residual',2*L*L-(A*(A-1)+2*C*D),A*A+2*A*(C+D)+A+(C-D)**2/2)
eq('U drift',gen(UU),s.Rational(5,2)*A*A-2*A-s.Rational(1,2)+A*((B-C-D)/2-2*E)+C*D/2)
eq('U bracket',bracket(UU),s.Rational(1,4)+A/4+s.Rational(11,4)*A*(A-1)+A*(C+D)/4+s.Rational(5,2)*A*E+s.Rational(3,4)*C*D+A*B/4)
# Independent recurrence verification of all local Phi ratios for symbolic E,N
# and integer exponent representatives. Uniform exponent rules are in the review.
q=1-E/(2*N);t=1/(2*N);g=1-t/q;k=1+t/q;dd=1+(E-1)/(4*N)
hp=(1+E/(4*N))/(1-(E+1)/(2*N));hm=(1-E/(2*N))/(1+(E-1)/(4*N))
a=s.symbols('a',integer=True,nonnegative=True)
expected=[q/2,2/q,s.sqrt(2)/q,q/s.sqrt(2),s.sqrt(2)/q,q/s.sqrt(2),
 2*(1+E/(4*N))*g**(a-2)/q**2,
 q*(q+t)*k**a/(2*dd),k**(a-1)/dd,(1+E/(4*N))*g**a,q,1/q]
for aa in [0,1,2,3,7]:
 for ix,(name,rate,v) in enumerate(channels):
  if s.simplify(rate.subs(A,aa) if hasattr(rate,'subs') else rate)==0:continue
  da,dl,de=marks[ix][1:4]
  qp=1-(E+de)/(2*N)
  hr=hp if de==1 else hm if de==-1 else 1
  direct=2**(-dl)*hr*qp**(aa+da)/q**aa
  eq('tilted literal ratio '+name+' A='+str(aa),s.cancel(direct),s.cancel(expected[ix].subs(a,aa)))
# Formal source group identities with independent symbols.
x,y,pp,aa=s.symbols('x y pp aa',real=True)
eq('CD cancellation',2*((1+x/2)*y**aa-1)+((1-x)-1),2*(1+x/2)*(y**aa-1))
sumAE=expected[7]+expected[8]-2
combined=((q+t)**2/2+1)*k**(a-1)/dd-2
ck('AE combined exponent identity',s.simplify(s.powsimp(sumAE-combined,force=True))==0)
ell,delta=s.symbols('ell delta',real=True)
expr=(-s.Rational(1,2)+B/(2*N*q)+2*A/(N*q)).subs(B,N*(1+delta)+A-2*ell-E)
want=(delta+5*A/N-2*ell/N-E/(2*N))/(2*q)
eq('AB AE actual motion identity',s.cancel(expr),s.cancel(want))
# Exact scalar proof margins.
qmin=F(199,200);p=F(1,2)
for name,truth in [
 ('sqrt half lower',F(7,10)**2<p),('sqrt half upper',F(71,100)**2>p),
 ('At/q',F(1,2)*F(1,500000)/qmin==F(1,995000)),
 ('N^.3 lower',48**10<500000**3),('count absorption',F(1,2)*F(1,20)/qmin<F(3,100)),
 ('death scalar',1/(p*qmin)-1<F(11,10)),
 ('AA CD scalar',2*(1/(F(7,10)*qmin)-1)<F(9,10)),
 ('AA E scalar',(1+F(1,400))/(p*qmin*qmin)-1<F(11,10)),
 ('full AL coefficient',F(11,1000)+F(129,5000)-F(11,20)<-F(1,2)),
 ('lower log H coefficient',F(3,8)-F(1,4800)>F(187,500)),
 ('upper log H coefficient',F(3,8)+F(1,796)<F(377,1000)),
 ('log2 lower',2*(F(1,3)+F(1,81))==F(56,81)),
 ('log2 upper',F(2,3)+F(2,81)/(1-F(1,9))==F(25,36)),
 ('entry margin',-F(56,81)+F(377,1000)*F(9,5)+F(1,400)<-F(1,100)),
 ('exit margin',(F(187,250)-F(25,36)-F(1,9900)-F(3,100))/2-F(101,9900)>0),
 ('rho uniform',F(4904,10000)/F(9,10)+F(2,9*10**19)<F(545,1000)),
 ('U barrier generator',-F(1,20)+F(9,800)*F(40,37)<0),
 ('poststartup CD floor',(1-F(1,100))**2*200**2-F(1,4)*F(1,100)**2*200**2>4),
 ('poststartup E/B',F(1,100)/F(9,10)<F(1,5)),
 ('poststartup L/B',F(1,5000)/F(9,10)<F(1,10)),
 ('root E-cap seed',F(199,4*10**6)>F(1,10**6)),
 ('root L-cap seed',F(199,10**6)>F(1,10**6)),
 ('T5 count mass headroom',12*10**4<=F(10**20,16)),
 ('T5 min population',10**20>=2000*10**6),
 ('T5 horizon threshold',10**20>=160),
 ('clearance target comparison',F(13,16)<F(15,16))]:ck(name,truth)
startupE=8*400**3
startup_log=-F(56,81)*400+F(377,1000)*F(startupE**2,10**20)+F(startupE,8*10**20)
ck('sharp actual carrier admission',startup_log<-276)
ck('raw startup R cap',F(64*400**6,10**20)<2)
ck('actual entrance R<=9/5',F(startupE**2,400*10**20)<F(9,5))
ck('actual entrance A cap',F(2,400)<=F(1,100))
values['startup_log_upper']=str(startup_log)
# Exact source/dependency readback; no dependency script import or cache experiment.
base=P.parent
spec=[('audit_cone_storage_20261101/REVIEW_RECEIPT.json',['UNWEIGHTED_SOURCE_STORAGE.md']),
 ('audit_count_band_buffer_20261101/REVIEW_RECEIPT.json',['ACTUAL_NARROW_COUNT_BAND.md','BUFFERED_PROGRESS_WITHOUT_LOWER_RATIO.md']),
 ('audit_global_derivatives_regularized_storage_20261101/REVIEW_RECEIPT.json',['REGULARIZED_WEIGHTED_SOURCE_BUDGET.md'])]
bindings={}
for manifest,names in spec:
 rr=base/manifest;data=json.loads(rr.read_text());bindings[str(rr)]={'sha256':hashlib.sha256(rr.read_bytes()).hexdigest()}
 for name in names:
  sha=data['accepted_sources'][name];file=base/name
  ck('accepted dependency bound '+name,hashlib.sha256(file.read_bytes()).hexdigest()==sha)
  bindings[str(file)]={'sha256':sha}
 for name,sha in data['review_artifacts'].items():
  file=rr.parent/name;ck('receipt payload bound '+str(file),hashlib.sha256(file.read_bytes()).hexdigest()==sha)
  bindings[str(file)]={'sha256':sha}
ck('regularized controlling receipt requested hash',bindings[str(base/'audit_global_derivatives_regularized_storage_20261101/REVIEW_RECEIPT.json')]['sha256']=='e1c1eb76b8592a098bdad9f6188b7f7f08e7d0e75ce153bc9a06aa53950dcae8')
workspace=base.parent
entropy=workspace/'return_path_construction_20261101/rate2_factorial_entropy_service'
for name,sha in [('FACTORIAL_ENTROPY_OUTPUT_SERVICE.md','bc5e25aacdeddf99d5e01a4429bd83dfad5b547a86b653cad0a1fcf161522bd9'),('audit_factorial_entropy_service_20261101_0721/SOURCE_BOUND_ACCEPTANCE.md','adffd448d1babea5af9f96fb7b5914d68d07859bc942cba0fea9ec83ae882414')]:
 file=entropy/name;ck('entropy accepted readback '+name,hashlib.sha256(file.read_bytes()).hexdigest()==sha);bindings[str(file)]={'sha256':sha}
(P/'DEPENDENCY_BINDINGS.json').write_text(json.dumps(bindings,indent=2)+'\n')
out={'status':'PASS_INDEPENDENT_LITERAL_CHANNEL_AND_RATIONAL_RECEIVER_CHECKS','check_count':len(checks),'checks':checks,'values':values,'marks':[{'channel':r[0],'dA':str(r[1]),'dL':str(r[2]),'dE':str(r[3]),'dZ':str(r[4]),'dU':str(r[5])} for r in marks],
     'scope':'Supporting exact checks; stopping-time and original-history proofs reviewed separately; no macro arrival certified.'}
(P/'INDEPENDENT_EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(checks))
