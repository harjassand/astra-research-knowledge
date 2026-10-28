"""Independent rational two-dimensional contact/service certificate.

Directly excludes unsafe (radius,depth) boxes. Does not import the worker's
inverse, interval optimiser, square-root code or saved answer. All admitted
unknown finite populations reduce to the same single-crack inequality.
"""
from fractions import Fraction as F
from math import isqrt
from pathlib import Path
import json,time,sys


def atan_interval(x,n):
    s=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(n)),F(0))
    nextterm=(-1)**n*x**(2*n+1)/F(2*n+1)
    return min(s,s+nextterm),max(s,s+nextterm)


started=time.monotonic()
l5,u5=atan_interval(F(1,5),40);l239,u239=atan_interval(F(1,239),12)
pilo,pihi=16*l5-4*u239,16*u5-4*l239
declared_lo=F('3.1415926535897932384626433832795028841971')
declared_hi=declared_lo+F(1,10**40)
assert declared_lo<pilo<pihi<declared_hi
# In this file use the independently proved short enclosure.
scale=10**50
sqrtpi_lo=F(isqrt((declared_lo.numerator*scale*scale)//declared_lo.denominator),scale)
assert sqrtpi_lo**2<=declared_lo
mass_ratio_hi=1/(declared_lo*sqrtpi_lo)
case=sys.argv[1] if len(sys.argv)>1 else 'nominal'
assert case in ('nominal','matched_residual')
nuisance=F(1,50) if case=='matched_residual' else F(0)
U0,U2=(F(26,25)+nuisance)*mass_ratio_hi,(F(1,20)+nuisance)*mass_ratio_hi
beta=F(16,3)*(1-F(34,100)**2)/110_000_000_000
a_scale=F(1,10000);H=F(1,100)
k=F(2*10**15) if case=='matched_residual' else F(10**15)
residual_service=F(10_000_000) if case=='matched_residual' else F(0)
theta=beta*k*a_scale/declared_hi


def min_q(lo,hi):
    near=F(0) if lo<=0<=hi else min(abs(lo),abs(hi))
    return 1/U0+near**2/U2


def h(y):return theta*y**4/(1+theta*y)


def upper_K_squared(radius,depth):
    pc=500_000_000+250_000_000*depth+residual_service
    gradient=F(2,3)*2*250_000_000/H
    return 4*radius*(pc+gradient*radius)**2/declared_lo


pending=[(F(-4,5),F(4,5),F(0),F(5),0)]
safe=[];excluded=[];visited=0
while pending:
    lo,hi,yl,yu,depth=pending.pop();visited+=1
    demand_lower=h(yl)*min_q(lo,hi)
    if demand_lower>1:
        excluded.append([lo,hi,yl,yu,depth]);continue
    k2upper=upper_K_squared(a_scale*yu,hi)
    if k2upper<25*10**12:
        safe.append([lo,hi,yl,yu,depth,k2upper]);continue
    assert depth<32,('unresolved',lo,hi,yl,yu)
    if (hi-lo)/F(8,5)>=(yu-yl)/5:
        mid=(lo+hi)/2
        pending.extend([(lo,mid,yl,yu,depth+1),(mid,hi,yl,yu,depth+1)])
    else:
        mid=(yl+yu)/2
        pending.extend([(lo,hi,yl,mid,depth+1),(lo,hi,mid,yu,depth+1)])
area=sum(((x[1]-x[0])*(x[3]-x[2]) for x in safe+excluded),F(0))
assert area==8
out={'status':'INDEPENDENT_ALL_RADIUS_DEPTH_CONTACT_RISK_PASS',
 'pi_bracket_proved_by':'Machin formula, alternating rational arctan series40+12 terms',
 'case':case,
 'input':{'observed_Mref_triple':['1','0','.01'],'entrywise_error_Mref':'.02',
  'extra_nuisance_norm_Mref':str(nuisance),'contact_coercivity_lower_Pa_per_m':str(k),
  'service_residual_center_upper_Pa':str(residual_service),'radius_cap_m':'.0005'},
 'service_K_threshold_Pa_sqrt_m':5_000_000,
 'visited_boxes':visited,'safe_boxes':len(safe),'moment_excluded_boxes':len(excluded),
 'max_depth':max(x[4] for x in safe+excluded),
 'max_safe_leaf_K_squared':str(max(x[5] for x in safe)),
 'safe_leaves':[[str(v) for v in x] for x in safe],
 'excluded_leaves':[[str(v) for v in x] for x in excluded],
 'covered_rectangle_area':str(area),'seconds':time.monotonic()-started,
 'scope':'All feasible individual-radius/depth pairs under the supplied contact-weighted moment upper; exact rational finite covering. No acquired contact coercivity, measurement, physical component or advantage.'}
filename='MATCHED_BOX_CERTIFICATE.json' if case=='matched_residual' else 'BOX_CERTIFICATE.json'
(Path(__file__).parent/filename).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ('safe_leaves','excluded_leaves')},indent=2))
