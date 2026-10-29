# Rigorous1D nonuniform exponential-potential certificate via exact Taylor remainder.
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import json
p=Path(__file__).parent;a=F(1,2);b=F(1);rate=4;order=40;T=8;d=1;gamma=4*((10*d*T-1).bit_length());r=F(1,4)
# |exp(-z)-sum_0^N(-z)^j/j!|<=z^(N+1)/(N+1)! for0<=z<=4.
rem=F(rate**(order+1),factorial(order+1));ints=[]
for k in [0,1,2]:
 val=sum((F((-rate)**j,factorial(j))*F(b**(j+k+1)-a**(j+k+1),j+k+1) for j in range(order+1)),F(0));err=(b-a)*rem;ints.append((val-err,val+err))
assert ints[0][0]>0
meanlo=ints[1][0]/ints[0][1];meanhi=ints[1][1]/ints[0][0];Slo=ints[2][0]/ints[0][1];Shi=ints[2][1]/ints[0][0];W=(Slo+Shi)/2;errS=(Shi-Slo)/2
assert errS<=W/101 and W>=F(99,100)*Shi and W<=F(101,100)*Slo
rows=[]
for n in [8,16,32,64]:
 pts=[a+(b-a)*F(2*i+1,2*n) for i in range(n)];ww=[sum((F((-rate)**j,factorial(j))*x**j for j in range(order+1)),F(0)) for x in pts];assert min(ww)>0
 total=sum(ww);mu=sum(x*w for x,w in zip(pts,ww))/total;M=sum(x*x*w for x,w in zip(pts,ww))/total;meanerr=max(abs(mu-meanlo),abs(mu-meanhi));assert M>=F(50,99)*W
 support=max(x*x/Slo for x in pts);assert support<=2*d*gamma*gamma
 # Exact unbiasedness for arbitrary rationallinearmeanell*x, hereell=1/2.
 ell=F(1,2);est=sum(w*(ell*x)*x/M for x,w in zip(pts,ww))/total;assert est==ell
 rows.append({'grid_n':n,'certified_mean_error_upper_float_display':float(meanerr),'target_tolerance':str(r/(4*T*T)),'mean_certificate_pass':meanerr<=r/(4*T*T),'covariance_and_leverage_certified':True,'estimator_unbiased_exact':True})
assert rows[-1]['mean_certificate_pass']
out={'status':'PASS_RIGOROUS_RATIONAL_EXPONENTIAL_QUADRATURE_CERTIFICATE','body':'[1/2,1]','density':'proportional exp(-4x)','taylor_order':order,'uniform_exp_remainder_bound_exact':str(rem),'continuous_second_moment_certified_interval':[str(Slo),str(Shi)],'scope':'Exact rational1D nonuniform kernel certificate; validates finite integration/error logic on this case, not35D runtime or an end-to-end learner. Float displays are not used for assertions.','rows':rows};(p/'certified_exponential_kernel_checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='continuous_second_moment_certified_interval'},indent=2))
