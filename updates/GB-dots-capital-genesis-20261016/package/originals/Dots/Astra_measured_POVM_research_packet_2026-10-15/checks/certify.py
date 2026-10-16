import numpy as np,sympy as s,json
from pathlib import Path
root=Path(__file__).resolve().parent.parent/'certificates';data=Path(__file__).resolve().parent.parent/'data'
Eraw=np.load(data/'huang_theta_pi_over_4_printed.npy')
def rational_matrix(A,den):return s.Matrix(np.rint(A.real*den).astype(int))/den+s.I*s.Matrix(np.rint(A.imag*den).astype(int))/den
E=[rational_matrix(e,1000) for e in Eraw]
# A separately constructed candidate, never used as a silent replacement.
H=(Eraw+Eraw.conj().transpose(0,2,1))/2;F=[]
for h in H:
 d,U=np.linalg.eigh(h);F.append((U*np.maximum(d,1e-5))@U.conj().T)
F=np.array(F);d,U=np.linalg.eigh(F.sum(0));W=(U/np.sqrt(d))@U.conj().T;F=W@F@W
Fc=[rational_matrix(f,10**8) for f in F[:3]];Fc.append(s.eye(4)-sum(Fc,s.zeros(4)))
maxdiff=0
for a,e in zip(Fc,E):
 assert a==a.conjugate().T
 assert all(a[:k,:k].det()>0 for k in range(1,5))
 for v in a-e:
  assert abs(s.re(v))<=s.Rational(1,1000) and abs(s.im(v))<=s.Rational(1,1000)
  maxdiff=max(maxdiff,float(abs(s.re(v))),float(abs(s.im(v))))
def encode(A):return {'real_numerators':[[int(s.re(x)*10**8) for x in row] for row in A.tolist()],'imag_numerators':[[int(s.im(x)*10**8) for x in row] for row in A.tolist()]}
(root/'physical_candidate.json').write_text(json.dumps({'denominator':10**8,'effects':[encode(a) for a in Fc],'meaning':'one constructed physical POVM inside declared componentwise tolerance 0.001; not the actual calibrated POVM','max_component_difference':maxdiff},indent=2))
# Exact rational local unitaries and algebraic physical states.
I=s.eye(2);X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1);Ps=[X,Y,Z]
nums=[[20,-27,-16],[-471,-263,-453]];Us=[]
for ns in nums:
 t=[s.Rational(n,1000) for n in ns];v=sum(x*x for x in t);qq0=(1-v)/(1+v);qq=[2*x/(1+v) for x in t];Us.append(qq0*I-s.I*sum([a*P for a,P in zip(qq,Ps)],s.zeros(2)))
 assert (Us[-1]*Us[-1].conjugate().T-I).applyfunc(s.simplify)==s.zeros(2)
U=s.kronecker_product(*Us);b=9*s.sqrt(2)/20;r=s.Rational(6,11);z=s.Rational(9,11)
R=[]
for ell in [-1,1]:
 rho=sum([s.kronecker_product((I+b*Z+i*b*X)/2,(I+ell*i*r*X+z*Z)/2) for i in [-1,1]],s.zeros(4))/2
 R.append((U*rho*U.conjugate().T).applyfunc(s.expand))
scores=[s.Rational(n,1000) for n in [-719,646,-270,149]]
Ls=[sum([(ell-score)**2*rho/2 for ell,rho in zip([-1,1],R)],s.zeros(4)) for score in scores]
# Freeze a rational common loss center, from componentwise median for the bound only.
Ynum=np.load(root/'frozen_arrays.npz')['center'];Yc=rational_matrix(Ynum,10**9)
assert Yc==Yc.conjugate().T
base=s.expand(s.trace(Yc)+sum(s.trace(e*(l-Yc)) for e,l in zip(E,Ls)))
coef=0
for l in Ls:
 for val in l-Yc:
  for part in [s.re(val),s.im(val)]:
   part=s.simplify(part)
   if part!=0:
    if float(part)>0:
     assert part>0
     coef+=part
    else:
     assert part<0
     coef-=part
coef=s.simplify(coef);base=s.simplify(s.re(base))
assert base<s.Rational(864558,10**6)
assert coef<s.Rational(3187,1000)
rawrisk=s.simplify(s.re(sum(s.trace(e*l) for e,l in zip(E,Ls))))
source45=1-s.Rational(45,100)*r*r;source43=1-s.Rational(43,100)*r*r
bound43=s.Rational(1)-s.Rational(43,100)*r*r-s.Rational(864558,10**6)-s.Rational(1,1000)*s.Rational(3187,1000)
assert bound43>s.Rational(4321,10**6)
result={'physical_candidate_exact_PSD_complete_box':'PASS','physical_candidate_max_component_error':maxdiff,'raw_fit_risk':float(rawrisk),'base_upper_exact':'864558/1000000','error_coefficient_upper_exact':'3187/1000','base_decimal':float(base),'error_coefficient_decimal':float(coef),'q45_source_risk_exact':str(source45),'q43_source_risk_exact':str(source43),'q45_raw_gap':float(source45-rawrisk),'q43_raw_gap':float(source43-rawrisk),'q43_gap_lower_at_declared_tolerance_001_exact':str(bound43),'q43_gap_lower_decimal':float(bound43),'all_assertions':'PASS'}
(root/'certificate.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
