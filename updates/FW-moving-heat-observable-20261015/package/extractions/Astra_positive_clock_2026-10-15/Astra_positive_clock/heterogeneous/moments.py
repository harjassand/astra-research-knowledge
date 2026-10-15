from pathlib import Path
import json
from fractions import Fraction as F
p=str(Path(__file__).resolve().parent)+'/'
j=json.load(open(p+'dyadic128_exact.json'));ks=list(map(int,j['rates']));cs=list(map(int,j['counts']));n=j['n'];base=ks[0];P=228;S=2**P;K=len(ks)
a=sum(c*base*S//k for c,k in zip(cs,ks));b=sum(c*base*base*S//(k*k) for c,k in zip(cs,ks));Al=F(a,S);Au=F(a+K,S);Bl=F(b,S);Bu=F(b+K,S);g=(1+F(1,2**(j['b']-1)))**(n+1)
# Compiled mean in units 1/base is C1. Compare at s=10/Au.
s=10/Au
# q cancels from Laplace denominator: phi=1/(1+s sum counts/(lambda+s)).
# Exact rational s numerator/denominator; interval sum with P fractional bits.
sn,sd=s.numerator,s.denominator
v=sum((c*base*sd*S)//(k*sd+base*sn) for c,k in zip(cs,ks));Vlo=F(v,S);Vhi=F(v+K,S)
phil=1/(1+s*Vhi);phiu=1/(1+s*Vlo)
q=F(1,2**n);expmax=q+(1-q)/(1+s*(Al/g)/(1-q))
out=dict(D_compiled_lower=float(Bl/Au**2),D_compiled_upper=float(Bu/Al**2),D_original_lower=float(Bl/Au**2/g**2),D_original_upper=float(Bu/Al**2*g**2),full_original_LT_lower=float(phil),atom_preserving_exponential_LT_upper=float(expmax),certified_LT_gap_lower=float(phil-expmax))
json.dump(out,open(p+'moment_certificate.json','w'),indent=2);print(out)
