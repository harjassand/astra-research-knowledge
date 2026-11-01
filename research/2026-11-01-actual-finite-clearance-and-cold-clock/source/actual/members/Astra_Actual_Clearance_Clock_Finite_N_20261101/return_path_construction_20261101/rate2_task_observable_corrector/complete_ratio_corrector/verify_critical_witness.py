#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,sys
from exact_fraction_coefficients import h1,h2,h3,c0,c1,c2,c3
sys.set_int_max_str_digits(0)
P=Path(__file__).parent
rows=[('0->A',(1,1,0,0,1)),('A->0',(-1,-1,0,0,-1)),('2A->AC',(-1,F(-1,2),0,1,0)),('AC->2A',(1,F(1,2),0,-1,0)),('2A->AD',(-1,F(-1,2),0,-1,0)),('AD->2A',(1,F(1,2),0,1,0)),('2A->AE',(-1,-1,1,0,0)),('AE->2A',(1,1,-1,0,0)),('AE->CD',(-1,0,-1,0,0)),('CD->AE',(1,0,1,0,0)),('CD->AB',(1,0,0,0,0)),('AB->CD',(-1,0,0,0,0))]
def chi(x):rr,uu,tt,aa,zz,ss=x;return h1(rr,uu,tt,zz,ss)*aa+h2(rr,uu,tt,zz,ss)*aa*aa+h3(rr,uu,tt,zz,ss)*aa**3
def val(x):rr,uu,tt,aa,zz,ss=x;return rr*(1-aa*uu)+chi(x)
def moved(x,j):
 rr,uu,tt,aa,zz,ss=x;da,dl,de,dz,dn=j;c=1+de*uu*tt/rr;h=1+dl*tt
 return rr*c*c/h,uu*c,tt/h,(aa+tt*da)/h,(zz+tt*dz)/h,ss+dn*uu*uu*tt/rr
def rates(x):
 rr,uu,tt,aa,zz,ss=x;cd=(1-aa)**2-zz*zz/4
 return [tt*tt,aa*tt,aa*(aa-tt),aa*(1-aa+zz/2),aa*(aa-tt),aa*(1-aa-zz/2),aa*(aa-tt),aa*rr/uu,aa*rr/uu,2*cd,cd,aa*(ss*rr/uu**2-2+aa-rr/uu)]
def mean(x):
 rr,uu,tt,aa,zz,ss=x;K=ss-uu+2*uu*uu*(1-tt)/rr;Lam=3-3*zz*zz/4+tt*tt
 mu=uu*uu*Lam/(rr*K);et=tt*uu/K
 mm=[1,mu,mu*(mu+et),mu*(mu+et)*(mu+2*et)]
 return 4-3*rr-rr*tt*tt/uu+sum(fn(rr,uu,tt,zz,ss)*m for fn,m in zip([c0,c1,c2,c3],mm))
def cert(x):return {'approx':float(x),'sign':(x>0)-(x<0),'sha256':hashlib.sha256((str(x.numerator)+'/'+str(x.denominator)).encode()).hexdigest(),'numerator_bits':abs(x.numerator).bit_length(),'denominator_bits':x.denominator.bit_length()}
records=[]
for rr,aa,lo,hi in [(F(1,2),F(1,100),F(-57),F(-56)),(F(51,100),F(99,10000),F(-59),F(-56))]:
 LL=10**8;uu=F(128,LL*LL);NN=rr*LL/uu**2;EE=uu*NN;AA=aa*LL;CC=DD=LL-AA;SS=NN;BB=SS-AA-CC-DD-EE;ZZ=F(0)
 assert all(v.denominator==1 for v in [NN,EE,AA,CC,DD,SS,BB])
 assert NN==SS and EE/NN<=F(1,100) and AA<=F(LL,100) and abs(ZZ)<=F(LL,100) and F(1,2)<=rr<=2 and EE**5>=32*NN**3 and LL>=100
 x=(rr,uu,F(1,LL),aa,F(0),F(1));f=val(x);g=F(0);param=F(0);perchannel={};bracket=F(0);jmax=F(0)
 for rate,(name,j) in zip(rates(x),rows):
  xx=moved(x,j);jump=val(xx)-f;g+=rate*jump/(uu*x[2]);bracket+=rate*jump*jump/x[2]**2;jmax=max(jmax,abs(jump))
  frozen=list(x);frozen[3]+=x[2]*j[0]
  pp=rate*(chi(xx)-chi(tuple(frozen)))/(uu*x[2]);param+=pp;perchannel[name]=cert(pp)
 up=list(x);down=list(x);up[3]+=x[2];down[3]-=x[2]
 fast=((aa*aa-4*aa)*(chi(tuple(up))-chi(x))+(4*aa*aa-4*aa)*(chi(tuple(down))-chi(x)))/(uu*x[2])
 mn=mean(x);assert g==mn+fast+param
 assert lo<g<hi and 2<mn<3
 assert perchannel['AE->2A']['sign']==-1
 assert abs(f-rr)<F(1,10**14)
 records.append({'counts':{k:int(v) for k,v in zip(['N','A','B','C','D','E','S','L','Z'],[NN,AA,BB,CC,DD,EE,SS,LL,ZZ])},'R':str(rr),'u':str(uu),'E5_over_N3':str(EE**5/NN**3),'normalization_EL_over_N':str(uu*LL),'exact_normalized_drift_interval':[str(lo),str(hi)],'full_normalized_drift':cert(g),'reference_mean':cert(mn),'frozen_mismatch':cert(fast),'parameter_motion':cert(param),'parameter_motion_by_channel':perchannel,'F2_minus_R':cert(f-rr),'bracket_density':cert(bracket),'max_jump':cert(jmax),'domain_and_generator_decomposition':'EXACT_PASS'})
 print('CRITICAL EXACT',rr,'full drift in',lo,hi,'mean',float(mn),'AE->2A parameter',perchannel['AE->2A']['approx'],flush=True)
report={'status':'EXACT_LOWER_FACE_FAILURE_EVEN_AT_S_EQUALS_N','gauge':'canonical complete cubic inverse, chi(A=0)=0','witnesses':records,'scope':'Pointwise inward drift fails on the requested A<=L/100 domain even after a perfect total-count ledger. This is not a refutation of an occupation-integrated admission proof or the actual fixed-corner capability.'}
(P/'critical_exact_counterexamples.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'])
