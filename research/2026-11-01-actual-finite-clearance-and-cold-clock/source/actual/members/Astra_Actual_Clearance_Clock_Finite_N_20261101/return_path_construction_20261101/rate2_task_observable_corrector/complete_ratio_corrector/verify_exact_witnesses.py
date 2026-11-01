#!/usr/bin/env python3
"""Reproducible rational witnesses for the canonical complete cubic correction."""
from fractions import Fraction as F
from pathlib import Path
import pickle,json,hashlib,sys
import sympy as S
sys.set_int_max_str_digits(0)
P=Path(__file__).parent
ob=pickle.load(open(P/'complete_algebra.pkl','rb'))
r,u,t,a,z,s=ob['vars']
def code(ex):
 if isinstance(ex,S.Symbol):return str(ex)
 if isinstance(ex,S.Rational):return f'F({int(ex.p)},{int(ex.q)})'
 if isinstance(ex,S.Add):return '('+'+'.join(code(q) for q in ex.args)+')'
 if isinstance(ex,S.Mul):return '('+'*'.join(code(q) for q in ex.args)+')'
 if isinstance(ex,S.Pow):return '('+code(ex.base)+'**'+code(ex.exp)+')'
 raise TypeError(ex)
def make(ex):return eval('lambda r,u,t,z,s:'+code(ex),{'F':F})
hf=[make(x) for x in ob['chi_power'][1:]]
cf=[make(x) for x in ob['fall_coeff']]
# Emit a pure-Fraction evaluator independent of SymPy and the pickle after generation.
evaluator=['from fractions import Fraction as F']
for i,ex in enumerate(ob['chi_power'][1:],1):evaluator+=['def h%d(r,u,t,z,s):'%i,'    return '+code(ex)]
for i,ex in enumerate(ob['fall_coeff']):evaluator+=['def c%d(r,u,t,z,s):'%i,'    return '+code(ex)]
(P/'exact_fraction_coefficients.py').write_text('\n\n'.join(evaluator)+'\n')
rows=[(1,1,0,0,1),(-1,-1,0,0,-1),(-1,F(-1,2),0,1,0),(1,F(1,2),0,-1,0),(-1,F(-1,2),0,-1,0),(1,F(1,2),0,1,0),(-1,-1,1,0,0),(1,1,-1,0,0),(-1,0,-1,0,0),(1,0,1,0,0),(1,0,0,0,0),(-1,0,0,0,0)]
names=[v[0] for v in ob['rows']]
def coeff(x):rr,uu,tt,aa,zz,ss=x;return [f(rr,uu,tt,zz,ss) for f in hf]
def chi(x):rr,uu,tt,aa,zz,ss=x;return sum(q*aa**j for j,q in enumerate(coeff(x),1))
def val(x):rr,uu,tt,aa,zz,ss=x;return rr*(1-aa*uu)+chi(x)
def rates(x):
 rr,uu,tt,aa,zz,ss=x;cd=(1-aa)**2-zz*zz/4
 return [tt*tt,aa*tt,aa*(aa-tt),aa*(1-aa+zz/2),aa*(aa-tt),aa*(1-aa-zz/2),aa*(aa-tt),aa*rr/uu,aa*rr/uu,2*cd,cd,aa*(ss*rr/uu**2-2+aa-rr/uu)]
def moved(x,j):
 rr,uu,tt,aa,zz,ss=x;da,dl,de,dz,dn=j;ch=1+de*uu*tt/rr;lh=1+dl*tt
 return rr*ch**2/lh,uu*ch,tt/lh,(aa+tt*da)/lh,(zz+tt*dz)/lh,ss+dn*uu**2*tt/rr
def mean(x):
 rr,uu,tt,aa,zz,ss=x;K=ss-uu+2*uu**2*(1-tt)/rr;Lam=3-3*zz**2/4+tt**2
 mu=uu**2*Lam/(rr*K);et=tt*uu/K;M=[F(1),mu,mu*(mu+et),mu*(mu+et)*(mu+2*et)]
 return 4-3*rr-rr*tt*tt/uu+sum(f(rr,uu,tt,zz,ss)*mm for f,mm in zip(cf,M))
def certificate(fr):
 st=str(fr.numerator)+'/'+str(fr.denominator)
 return {'numerator_sign':(fr>0)-(fr<0),'numerator_bits':abs(fr.numerator).bit_length(),'denominator_bits':fr.denominator.bit_length(),'fraction_sha256':hashlib.sha256(st.encode()).hexdigest(),'decimal_approx':float(fr)}
records=[]
for q,rr,ss,aa0,lo,hi in [(6,F(2),F(99,100),F(1,100),F(6),F(7)),(8,F(1,2),F(101,100),F(1,100),F(-47),F(-46)),(6,F(199,100),F(9901,10000),F(99,10000),F(5),F(7)),(8,F(51,100),F(10099,10000),F(99,10000),F(-49),F(-46))]:
 LL=10**q;uu=F(1,10**q);NN=rr*LL/uu**2;EE=uu*NN;AA=aa0*LL;ZZ=0;SS=ss*NN;CC=DD=LL-AA;BB=SS-AA-CC-DD-EE
 assert all(v.denominator==1 for v in (NN,EE,AA,SS,CC,DD,BB))
 x=(rr,uu,F(1,LL),aa0,F(0),ss)
 assert F(99,100)*NN<=SS<=F(101,100)*NN and EE/NN<=F(1,100)
 assert AA<=F(LL,100) and abs(ZZ)<=F(LL,100) and F(1,2)<=rr<=2 and EE**5>=32*NN**3 and LL>=100
 # Reference inverse check at this exact rational state and several actual A values.
 for aaa in (F(0),F(1,100),F(2,100),F(3,100)):
  y=(rr,uu,F(1,LL),aaa,F(0),ss);cv=chi(y);up=list(y);down=list(y);up[3]+=y[2];down[3]-=y[2]
  K=ss-uu+2*uu**2*(1-y[2])/rr;Lam=3+y[2]**2
  qc=((Lam+aaa*rr/uu)*(chi(tuple(up))-cv)+(aaa*rr*K/uu**2+aaa*rr/uu)*(chi(tuple(down))-cv))/(uu*y[2])
  # Full residual direct at the same algebraic A (whether or not all rates positive).
  f1=lambda xx:xx[0]*(1-xx[3]*xx[1])
  gf1=sum(rate*(f1(moved(y,j))-f1(y))/(uu*y[2]) for rate,j in zip(rates(y),rows))
  assert qc+gf1==mean(y)
 f=val(x);ch=chi(x);g=F(0);param=F(0);bracket=F(0);jumpmax=F(0)
 for name,rate,j in zip(names,rates(x),rows):
  assert rate>=0
  xx=moved(x,j);jump=val(xx)-f
  g+=rate*jump/(uu*x[2]);bracket+=rate*jump*jump/x[2]**2;jumpmax=max(jumpmax,abs(jump))
  frozen=list(x);frozen[3]+=x[2]*j[0]
  param+=rate*(chi(xx)-chi(tuple(frozen)))/(uu*x[2])
 up=list(x);dn=list(x);up[3]+=x[2];dn[3]-=x[2];aa=x[3]
 fast=((aa*aa-4*aa)*(chi(tuple(up))-ch)+(4*aa*aa-4*aa)*(chi(tuple(dn))-ch))/(uu*x[2])
 mn=mean(x);assert g==mn+fast+param
 assert lo<g<hi
 assert abs(f-rr)<F(1,10**6)
 record={'counts':{key:int(v) for key,v in zip(['N','A','B','C','D','E','S','L','Z'],[NN,AA,BB,CC,DD,EE,SS,LL,ZZ])},'R':str(rr),'exact_drift_interval':[str(lo),str(hi)],'normalization_uL':str(uu*LL),'normalized_full_drift':certificate(g),'normalized_reference_mean':certificate(mn),'normalized_frozen_mismatch':certificate(fast),'normalized_parameter_motion':certificate(param),'F2_minus_R':certificate(f-rr),'jump_max':certificate(jumpmax),'bracket_density':certificate(bracket),'domain_checks':'PASS','generator_and_reference_decomposition':'EXACT_EQUALITY_PASS'}
 records.append(record)
 print('WITNESS',rr,'full drift in',lo,hi,'mean',float(mn),'fast',float(fast),'parameter',float(param),flush=True)
report={'status':'EXACT_COUNTEREXAMPLES_TO_UNIFORM_INWARD_DRIFT','gauge':'chi(A=0)=0, complete cubic Qc inverse','reference_law_assumed':False,'witnesses':records,'scope':'Canonical complete cubic corrector fails requested inward sign on the stated full domain; this does not rule out different gauges, extra correctors, a tighter domain, or an occupation-integrated admission argument.'}
(P/'exact_counterexamples.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'witness_count':len(records)},indent=2))
