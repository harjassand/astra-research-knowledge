from fractions import Fraction as F
from pathlib import Path
import json
# Exact continuous-box witness: K={0,1}, phi(w)=min(0,w), alwaysreturn1.
# For -R<=G<=R, integral mean positive part is (R+G)^2/(4R).
continuous=[];finite=[]
R=F(3,2)
for j in range(-12,13):
 G=R*F(j,12);mu=(R+G)**2/(4*R);grad=(R-G)/(2*R);bias=1-grad
 assert bias*bias==mu/R
 continuous.append({'G':str(G),'expected_gap':str(mu),'bias':str(bias),'sqrt_bound_tight':True})
 for M in [2,4,16,64]:
  mid=[-R+F(2*k+1,M)*R for k in range(M)]
  em=sum(max(G+z,0) for z in mid)/M
  assert bias*bias<=(em+R/M)/R
  # Internal coin: half exact optimizer, half the constant action1.
  meanx=F(1,2)+sum(int(G+z<0) for z in mid)/F(2*M)
  erandom=em/2
  assert (meanx-grad)**2<=(erandom+R/M)/R
  finite.append({'M':M,'G':str(G),'mean_gap':str(em),'rounding_bound_pass':True,'extra_oracle_coin_pass':True})
# Exact Cauchy/Jensen composition with two possible actual histories.
q=[[F(1,4),F(2,3),F(1,2)],[F(1,3),F(1,5),F(3,4)]];prob=[F(2,5),F(3,5)];T=3
expected_sum=sum(prob[b]*sum(q[b]) for b in range(2));expected_squares=sum(prob[b]*sum(x*x for x in q[b]) for b in range(2))
assert expected_sum**2<=T*expected_squares
# Prior uniform tolerance reproduces <=720 approximate-optimization allowance.
for horizon in [1,2,10,1000]:
 M=1
 while M<140*horizon*horizon:M*=2
 gap_sum=R/F(4*horizon)
 squared_penalty_factor=F(horizon,R)*gap_sum+F(35*horizon*horizon,M)
 assert squared_penalty_factor<=F(1,2)
out={'scope':'Exact scalar sharpness, midpoint/private-oracle-coin checks and Cauchy composition; not a quartic optimizer or source experiment.','continuous_tight_witnesses':continuous,'finite_cases':len(finite),'all_finite_midpoint_and_private_coin_checks_pass':True,'expected_sum_bias':str(expected_sum),'cauchy_squared_bound':str(T*expected_squares),'uniform_tolerance_recovery_pass':True}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='continuous_tight_witnesses'},indent=2))
