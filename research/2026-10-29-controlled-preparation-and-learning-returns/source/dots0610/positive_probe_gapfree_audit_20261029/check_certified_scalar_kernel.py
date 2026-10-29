from fractions import Fraction as F
import json,math
from pathlib import Path
# Fully rational scalar prototype, K=[1/2,1], density proportional exp(-2(x-1/2)).
# Alternating series provides rigorous rational exponential enclosures on[0,1].
def eb(t,k=16):
 term=F(1);total=F(1)
 for j in range(1,k+1):term*=-t/j;total+=term
 # k even: total upper, next term gives lower.
 return total+term*(-t)/(k+1),total
lo,hi=eb(F(1));Zlo=(1-hi)/2;Zhi=(1-lo)/2
muLo=((2-3*hi)/4)/Zhi;muHi=((2-3*lo)/4)/Zlo
Slo=((5-10*hi)/8)/Zhi;Shi=((5-10*lo)/8)/Zlo
W=(Slo+Shi)/2;err=(Shi-Slo)/2
assert err<=W/101 and F(99,100)*Shi<=W<=F(101,100)*Slo
T=8;d=1;gamma=4*((10*d*T-1).bit_length());eta=F(1,32*d*gamma**2);r=F(1,4)
assert 1/W<=F(3,2)*d*gamma**2 # G=K exactly in this prototype
N=2;records=[]
while True:
 xs=[F(1,2)+F(2*i+1,4*N) for i in range(N)]
 ws=[sum(eb(2*x-1))/2 for x in xs];z=sum(ws);ps=[w/z for w in ws]
 mu=sum(p*x for p,x in zip(ps,xs));M=sum(p*x*x for p,x in zip(ps,xs))
 meanerr=max(abs(mu-muLo),abs(mu-muHi));moment=M-F(50,99)*W
 records.append({'cells':N,'certified_mean_error_upper':str(meanerr),'moment_margin':str(moment)})
 if meanerr<=r/(4*T*T) and moment>0:break
 N*=2;assert N<=4096
# Positive linear loss ell=2/3; exact actual-discrete covariance estimator identity.
ell=F(2,3);est=sum(p*(ell*x)*x/M for p,x in zip(ps,xs));assert est==ell
# Stability against rigorously enclosed continuous S.
for x in xs:assert x*x*Shi/(M*M)<=8*d*gamma**2
out={'status':'PASS_EXACT_RATIONAL_INTERVAL_CERTIFICATES','cells':N,'gamma':gamma,'eta':str(eta),'continuous_mean_interval':[str(muLo),str(muHi)],'continuous_S_interval':[str(Slo),str(Shi)],'rational_W':str(W),'actual_M':str(M),'actual_mean':str(mu),'certified_mean_error_float':float(meanerr),'required_mean_tolerance':str(r/(4*T*T)),'exact_unbiased_estimator':str(est),'iterations':records,'scope':'Certified 1D finite rational law and real exponential interval comparison, not full35D controller execution; analytic integrals replace generic interval Riemann integration in this diagnostic.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2));print({k:out[k] for k in ['status','cells','certified_mean_error_float','required_mean_tolerance']})
