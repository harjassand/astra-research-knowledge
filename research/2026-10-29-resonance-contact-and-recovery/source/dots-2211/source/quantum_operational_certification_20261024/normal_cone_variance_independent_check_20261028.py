"""Independent exact variance sums and high-precision finite horizon checks."""
from fractions import Fraction as F
from math import comb,factorial
from pathlib import Path
import mpmath as mp,json
mp.mp.dps=90
for r in range(2,100):assert factorial(r)>=2*3**(r-2)
for k in range(1,12):
 L=3**(k+1);p=F(1,L)
 assert p*L*L==L
for ell in range(1,13):
 assert sum(comb(ell,k)*3**k*3**(k+1) for k in range(1,ell+1))==3*(10**ell-1)
 assert sum(comb(ell,k)*3**k*(3**(k+1)+1)**2 for k in range(1,ell+1))==9*(28**ell-1)+6*(10**ell-1)+4**ell-1
# Tail inversion algebra: s=sqrt(2Vt)+2bt/3 implies s²>=2t(V+bs/3).
import sympy as s
x,b,t=s.symbols('x b t',nonnegative=True)
S=x+2*b*t/3
assert s.expand(S*S-x*x-2*t*b*S/3)==2*b*t*x/3
z=mp.log(720)
def radius(N):return mp.mpf(3)/4*mp.sqrt(3)*(mp.sqrt(18*z/N)+20*z/(3*N))
assert radius(82201)>mp.mpf('.05')>radius(82202)
parent=mp.ceil(2*81*z/(mp.mpf(1)/30)**2);assert parent==959255
out={'status':'PASS_EXACT_VARIANCE_AND_90_DIGIT_THRESHOLD','source_outcomes':0,'h_82201':mp.nstr(radius(82201),80),'h_82202':mp.nstr(radius(82202),80),'minimal_variance_calls':82202,'parent_calls':int(parent),'scope':'Exact discrete identities and high-precision scalar check, not empirical confidence acceptance.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
