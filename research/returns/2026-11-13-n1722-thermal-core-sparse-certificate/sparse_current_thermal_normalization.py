from fractions import Fraction as F
import math,json
from pathlib import Path
rows=[]
q5=F(59,500);a=F(49999,50000)
for R in [4,8,20,40,80,200,1000,10000]:
 theta=4.;phi=theta/R;L=8*R;n=L*L;K=5*R*R;M=10*R;kappa=1.
 r=1
 while 6*n*q5**(2*r)/(1-q5)>F(1,100):r+=1
 u=6*n*q5**(2*r)/(1-q5)
 valid=3*(r+2)<=R and 4*r<L and M<K+1
 if not valid:
  rows.append(dict(R=R,L=L,r=r,valid=False,reason='explicit thermal-flow condition r+2<=R/3 fails'));continue
 gamma=8*theta*R/float(a)+8*theta
 logres=math.log(2*n)+gamma
 logres+=math.log1p(math.exp(-logres)) # kappa=1
 sparse=math.log(n)+2*math.log(M)+(M-1)*math.log(64)-8*theta*(math.sqrt(K+1)+math.sqrt(K+1-M))+2*phi*M
 logbound=sparse+logres-math.log1p(-float(u))
 rows.append(dict(R=R,L=L,r=r,valid=True,theta=theta,kappa=kappa,max_component_sites=M,core_error_upper_exact=str(u),Gamma_eff=gamma,log_current_fraction_upper=logbound))
Path(__file__).with_suffix('.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
