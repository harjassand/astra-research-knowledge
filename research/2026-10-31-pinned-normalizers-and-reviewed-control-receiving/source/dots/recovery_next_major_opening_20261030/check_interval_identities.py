from fractions import Fraction as F
from itertools import product
import json, math, pathlib, hashlib
pmf={1:F(1,10),2:F(1,5),3:F(3,10),5:F(2,5)}
lam=F(2,7)
def C(r): return lam*sum(p*max(l-r,0) for l,p in pmf.items())
checks=[]
for k in range(1,5):
    total=F(0)
    for xs in product(range(-4,5),repeat=k-1):
        pts=(0,)+xs
        total+=C(max(pts)-min(pts))
    rhs=lam*sum(p*l**k for l,p in pmf.items())
    assert total==rhs
    checks.append({'cumulant_order':k,'sum':str(total),'moment':str(rhs)})
for r in range(1,8):
    assert C(r-1)-2*C(r)+C(r+1)==lam*pmf.get(r,F(0))
    assert C(r)-C(r+1)==lam*sum(p for l,p in pmf.items() if l>=r+1)
for L in range(1,8):
    explicit=lam*sum(p*sum(a<=1 and a+l-1>=L for a in range(-8,9)) for l,p in pmf.items())
    assert explicit==C(L-1)
    a=math.exp(-float(C(0)))
    b=math.exp(-2*float(C(0))+float(C(L-1)))
    assert abs((1-a*a/b)-(1-math.exp(-float(explicit))))<1e-14
# Taylor coefficient check, not formal proof (proof in note).
a=.7
P0=[a*a,a-a*a,a-a*a,(1-a)**2]
ratios=[]
for h in [1e-3,1e-4,1e-5]:
    b=a*a*math.exp(h); P=[b,a-b,a-b,1-2*a+b]
    kl=sum(p*math.log(p/q) for p,q in zip(P,P0))
    ratios.append({'h':h,'KL_over_h2':kl/h**2})
out={'status':'exact finite-support identities passed','pmf':{str(k):str(v) for k,v in pmf.items()},'lambda':str(lam),'cumulants':checks,'binary_pair_KL_diagnostic':ratios,'KL_limit':a*a/(2*(1-a)**2),'scope':'Exact rational checks support formulas for this finite law, not a physical inference or general proof.'}
path=pathlib.Path(__file__).with_name('CHECKS.json');path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
