"""Exact rational operational reset fixture; no source shots or truncation proof."""
from fractions import Fraction as F
import sympy as s,json
from pathlib import Path
q=s.Rational(1,4);H=s.Matrix([[1,1],[0,q]]);P=s.Matrix([[1-q,q],[q,1-q]])
# Columns tau are physical pointer populations; future rows are trace and outcome1.
Tau=s.Matrix([[1,1-q],[0,q]]);C=Tau.inv()*P*Tau;m=s.Matrix([[1,1]]);E=s.Matrix([[0,1]]);W=s.Matrix([-1,1]);D=E*C*W
assert m*C==m and D[0]==s.Rational(1,2)
v=s.Matrix([-1,2]);assert C*v==v and Tau*v==s.Matrix([s.Rational(1,2)]*2)
K=sum(abs(x) for x in H.inv());assert K==9
checks=[]
for t in range(1,21):
 # Classical pointer perfectly correlated with a retained reference bit.
 A=(P**t)/2
 # Each column is joint probability of pointer value and reference label.
 target=s.ones(2,2)/4
 actual_half=sum(abs(x) for x in A-target)/2
 assert actual_half==s.Rational(1,2)*D[0]**t
 assert actual_half<=2*K*D[0]**t
 checks.append({'t':t,'actual_half_distance':str(actual_half),'certificate_unclipped':str(2*K*D[0]**t)})
# Interval certificate: all transfer entries uncertain by f; trace row by d.
f=s.Rational(1,1000);d=s.Rational(1,1000)
Dhat=C[1,1]-C[1,0]*m[1];B=f+f+abs(C[1,0])*d;c_cert=abs(Dhat)+B
assert c_cert==s.Rational(503,1000)<1
# Check every interval corner independently, including trace row uncertainty.
corner_count=0
for sign1 in [-1,1]:
 for sign2 in [-1,1]:
  for signm in [-1,1]:
   # true raw mass <=1; negative perturbation also covered; + corner is capped.
   mt=min(s.Rational(1),m[1]+signm*d)
   dt=(C[1,1]+sign1*f)-(C[1,0]+sign2*f)*mt
   assert abs(dt)<=c_cert
   corner_count+=1
out={'status':'PASS_EXACT_RATIONAL_FIXTURE','source_draws':0,'C':str(C),'trace_row':str(m),'fixed_coordinate':str(v),'core_bound_K':str(K),'true_contraction':str(D[0]),'interval_contraction':str(c_cert),'interval_corners':corner_count,'correlated_reference_checks':checks,'infinite_environment_argument':'Tensor every step with unilateral shift of an inaccessible counter. Counter sectors remain orthogonal and no stationary normal counter state exists. All future effects ignore counter, so same exact rank-two quotient and reset bound. This is analytic, not a truncation simulation.','limitations':'Supplied exact core fixture; does not bootstrap its acquisition from one uncontrolled trajectory or run hardware.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
