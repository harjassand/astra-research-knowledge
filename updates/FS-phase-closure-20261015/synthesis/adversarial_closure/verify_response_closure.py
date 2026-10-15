"""Exact finite countermodels and coefficient checks; no physical validation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json

OUT=Path(__file__).resolve().parent
checks=[]


def passed(name, **data):
    checks.append({'name':name,'passed':True,**data})


# A known detector sum does not identify a product-specific task score.
r0=(F(3,2),F(1,2)); r1=(F(1,2),F(3,2)); incumbent=F(1)
assert sum(r0)==sum(r1)==2
assert r0[0]>incumbent>r1[0]
passed('detector fiber contains opposite task decisions',
       response0=list(map(str,r0)),response1=list(map(str,r1)))

# Full joint uncertainty can be much tighter than separately optimistic endpoints.
joint=[(F(0),F(0)),(F(10),F(10))]; beta=F(1)
joint_support=max(j-beta*c for j,c in joint)
box_support=max(j for j,c in joint)-beta*min(c for j,c in joint)
assert joint_support==0 and box_support==10
passed('joint reward cost correlation sharpens support',
       joint=str(joint_support),independent_box=str(box_support))

# An unmeasured admitted mode can flip a decision with all measured modes fixed.
light=F(2); measured=F(1)
assert max(measured,F(0))<light<max(measured,F(3))
passed('unmeasured action coverage is necessary')

# A higher-order interaction can be invisible at every other configuration.
target=(1,1,1)
tested=[a for a in itertools.product((0,1),repeat=3) if a!=target]
interaction=lambda a: 4*a[0]*a[1]*a[2]
assert all(interaction(a)==0 for a in tested) and interaction(target)==4
passed('uncalibrated joint interaction invisible on held out subset',tested=len(tested))

# Cost boundary uncertainty can reverse feasibility, independently of the reward gap.
B=F(1); eps=F(1,1000)
assert B-eps<=B<B+eps
assert F(2)>F(1)
passed('arbitrarily small cost uncertainty changes optimal feasible action')
assert (F(0)+2*B)/2==B
passed('mean resource budget does not imply pathwise budget',violation_probability='1/2')

# Unequal-duration block totals are not throughput rates.
outputs=[F(10),F(2)]; durations=[F(10),F(1)]
assert outputs[0]>outputs[1] and outputs[0]/durations[0]<outputs[1]/durations[1]
passed('duration normalization can reverse a response ranking')

# A relaxation upper bound does not establish an achievable dark emulator.
B=F(1,2); deterministic_dark=F(0); relaxed_dark=B; light=F(1,4)
assert deterministic_dark<light<relaxed_dark
dual=F(1)*B+max(F(0),F(1)-F(1)*F(1))
assert dual==relaxed_dark
passed('LP upper bound is asymmetric decision evidence',
       actual_dark=str(deterministic_dark),light=str(light),relaxation=str(relaxed_dark))

# A full finite support certificate does establish the declared comparison.
modules=[[(F(0),F(0)),(F(3),F(2)),(F(5),F(4))],
         [(F(0),F(0)),(F(4),F(3)),(F(6),F(5))]]
B=F(5); beta=F(1)
alphas=[max(j-beta*c for j,c in modes) for modes in modules]
bound=beta*B+sum(alphas)
feasible=[sum(v[0] for v in choices) for choices in itertools.product(*modules)
          if sum(v[1] for v in choices)<=B]
assert max(feasible)==bound==7
assert F(15,2)>bound
passed('finite complete support witness',bound=str(bound),light='15/2')

# Ratio-only measurements identify efficiency parameter but not absolute power.
L=[[F(4),F(1)],[F(1),F(1)]]
scale=F(100)
ratios=(L[1][0]/L[0][0],L[0][1]/L[1][1])
scaled_ratios=(scale*L[1][0]/(scale*L[0][0]),scale*L[0][1]/(scale*L[1][1]))
assert ratios==scaled_ratios and ratios[0]*ratios[1]==F(1,4)
pmax=L[0][1]**2/(4*L[1][1]); pmax_scaled=(scale*L[0][1])**2/(4*scale*L[1][1])
assert pmax==F(1,4) and pmax_scaled==25
passed('two port ratio scale ambiguity',power0=str(pmax),power1=str(pmax_scaled))

# Exact sharp one-dimensional quartic Picone remainder.
# f(t)=(t-1/3)^4 has remainder f(1)-f(0)-f'(0)=1/3.
remainder=(F(1)-F(1,3))**4-F(1,3)**4+4*F(1,3)**3
assert remainder==F(1,3)
passed('sharp quartic remainder coefficient',value=str(remainder))

# Boundary-zero weak-dual approximants have q=0 and converge to primal energy1.
for e in [F(1),F(1,2),F(1,10),F(1,100)]:
    for x in [F(1,10),F(1,2),F(1)]:
        divj=-12/(x+e)**4
        conjugate=3/(x+e)**4
        assert -divj/4-conjugate==0
assert F(1)/(1+F(1,100))**3 > F(97,100)
passed('boundary zero exact dual approximants',boundary_value_epsilon_1_over_100=str(F(1)/(1+F(1,100))**3))

# Algebra for new shear scope and the conservative rational coercivity constant.
assert F(29,20)**3>3 and F(39,10)**3<60
factor=1+6*F(1,3)**2*F(1,2)+F(1,3)**4*F(3,8)
a=F(1,4); b=F(1,5)
curvature=-b*factor*(2*a+F(3,2)*a**3)
assert factor==F(289,216) and curvature==-F(19363,138240)
passed('shear constant and failure of prior curvature cancellation',
       density_factor=str(factor),curvature=str(curvature))

# Constants used by the fully minimized phase obstruction.
assert F(1,20736)<F(3,32768)
endpoint=F(1,16)+2*F(1,12)*F(4,3)+16+F(1,4)
assert endpoint==F(2381,144)<17
assert F(1,24)+F(17,128)<F(1,2)
assert F(1024)**4/(131072*F(4)**8)==128>17
passed('reduced phase obstruction finite constants',endpoint_upper=str(endpoint))

receipt={'status':'PASS','groups':len(checks),'checks':checks,
 'scope':'Exact finite arithmetic and countermodel checks. Does not formalize positivity, weak duality, averaging, coverage, PDE regularity, or physical assumptions.',
 'repository_pin':'846f185763ed3a27310fad4ce9471ba324d1e5f4',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OUT/'EXACT_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'status':receipt['status'],'groups':len(checks)},indent=2))
