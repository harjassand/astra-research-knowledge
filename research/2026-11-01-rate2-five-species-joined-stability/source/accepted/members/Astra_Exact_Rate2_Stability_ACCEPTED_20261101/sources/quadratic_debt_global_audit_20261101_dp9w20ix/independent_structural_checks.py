"""Additional exact rational per-channel and uniform-margin checks; no author code."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json,hashlib
import independent_global_checks as G
PTH=Path(__file__).resolve().parent

def main():
 n=0;A0=0;arm=0;AE=0;forward=0;port=0;AB=0;poly=0
 for x in product(range(6),range(4),range(6),range(6),range(4)):
  A,B,C,D,E=x;c,d,H=G.coords(x);P,R=G.rec(x);dc=F(1,(c+1)*(c+2));dd=F(1,(d+1)*(d+2));DR=F(0)
  for rate,y,dn,name in G.trans(x):
   py,ry=G.rec(y);change=ry-R;DR+=rate*(G.r**dn*ry-R)
   if name.startswith('forward_'):assert rate*change<=1;forward+=1
   if name=='reverse_2':assert change==-F(D+1,(c+1)*(d+1)*(d+2))and change<=0;arm+=1
   if name=='reverse_3':assert change==-F(C+1,(d+1)*(c+1)*(c+2))and change<=0;arm+=1
   if name=='reverse_4':assert change<=dc+dd;AE+=1
   if name=='AE_CD':assert change==F(1,(c+1)*(d+1))and change<=F(3,4)*(dc+dd);AE+=1
   if name=='birth':assert change<=F(1,4);port+=1
   if name=='death':assert rate*change<=F(1,4)and(G.r**-1-1)*rate*ry<=G.delta;port+=1
  if not A:assert DR==-F(G.r,(C+2)*(D+2))-F(3*C*D,(C+1)*(D+1));A0+=1
  n+=1
 for A,C,D,t in product([1,2,3,1000],[0,1,1000000],[0,1,1000000],[F(0),F(1,10**6),F(4,5),F(1999,1000)]):
  c=A+C;d=A+D;z=F(1,2*c*d)
  upper=A*A*z*t*t+t*t+(A*A+1)*(2*t*z+z*z)
  assert upper<=F(3,2)*t*t+2*t+z;poly+=1
  for B in [A+1,A+2,10**9+A]:
   phase=5*t*t*(-A*(2*A-1)+F(A**3,B+1));assert phase<=-F(5,2)*(A*t)**2;AB+=1
 delta=G.delta;k=G.kappa
 margins={'both_diverge_zero_debt':delta-3*k,'both_diverge_positive_A':delta-1,'both_diverge_A_zero':delta-F(85,100),'one_coordinate_zero':-5+29*delta,'one_positive_coordinate_debt_zero':-F(3,2)*k+29*delta,'one_positive_coordinate_debt_positive':-F(7,30)+29*delta,'both_bounded_hub':-F(3,4)*k+29*delta}
 assert max(margins.values())==-F(721,10**6)<-F(1,2000)
 assert F(21,20)*9+20<30 and 30*F(1,60000)==F(1,2000)
 assert -F(15,100)+20*delta/7<=-F(4,100)
 assert -F(915,100)+(40+20*delta+k*(F(9,2)+delta))/7<=-F(4,100)
 assert F(5,8)*F(10287,4900)>F(162,137)and F(153,28)<6
 assert G.ex(F(4,5))[1]<F(9,4)and G.ex(F(1,2))[1]<F(5,3)and G.ex(F(1))[0]>F(8,3)and G.ex(F(2))[0]>7
 result={'status':'PASS_INDEPENDENT_EXACT_STRUCTURAL_AND_UNIFORM_MARGIN_CHECKS','states':n,'A_zero_exact_R_formula':A0,'forward_R_channel_checks':forward,'reverse_arm_R_identity_checks':arm,'AE_R_channel_checks':AE,'port_R_channel_checks':port,'AE_phase_polynomial_envelope_checks':poly,'AB_phase_damping_checks':AB,'escape_case_upper_bounds':{k:str(v)for k,v in margins.items()},'worst_common_upper_bound':'-721/1000000','strict_slack_below_minus_eta':'221/1000000','author_code_imported':False,'global_test_script_sha256':hashlib.sha256((PTH/'independent_global_checks.py').read_bytes()).hexdigest()}
 (PTH/'INDEPENDENT_STRUCTURAL_CHECKS.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
