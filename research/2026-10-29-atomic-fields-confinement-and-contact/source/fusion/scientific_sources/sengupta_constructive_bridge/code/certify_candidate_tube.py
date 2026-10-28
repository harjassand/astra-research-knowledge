"""Complete candidate tube at exact rational sigma=1.34452, fixed iota=1/sqrt5."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parents[2]/'capability_backward_bridge/code/vendor'))
import mpmath as mp
mp.iv.dps=60;iv=mp.iv

def K(m):
 a=iv.mpf(1);b=iv.sqrt(1-m)
 for _ in range(14):a,b=(a+b)/2,iv.sqrt(a*b)
 return iv.pi/(2*iv.mpf([b.a,a.b]))
def sinh(x):return (iv.exp(x)-iv.exp(-x))/2
m=iv.mpf(['.01032','.01033']);sig=iv.mpf('1.34452')
lo=iv.pi*K(iv.mpf('.01032'))/K(1-iv.mpf('.01032'));hi=iv.pi*K(iv.mpf('.01033'))/K(1-iv.mpf('.01033'))
assert lo.b<sig.a and hi.a>sig.b
kap=2*K(1-m)/iv.pi;x=iv.sqrt(5)/((iv.exp(sig)+iv.exp(-sig))/2);u0=iv.log(x+iv.sqrt(x*x-1))
qcap=iv.mpf('.00001');xcap=iv.mpf('.0046')
# cd satisfies U'=-sqrt((1-U²)(1-mU²)); U=cos(theta) gives
# theta'>=sqrt(1-m), hence cd(x)<=cos(sqrt(1-m)*x).
cdhi=iv.cos(iv.sqrt(1-m)*xcap);assert cdhi.b<(1-qcap).a
radius=xcap/kap;margin=u0-2*radius;D=(sinh(u0-radius)-sinh(radius))**2
assert margin.a>0 and D.a>0 and xcap.b<K(m).a
out=dict(status='PASS',exact_sigma='1.34452',exact_iota='1/sqrt5',m_enclosure=['.01032','.01033'],profile_period_ratio_lower=str(lo),profile_period_ratio_upper=str(hi),u0=str(u0),kappa=str(kap),DeltaPsi_cap='1e-5',profile_coordinate_absolute_bound='.0046',cd_upper=str(cdhi),uniform_u_minus_abs_v_lower=str(margin),uniform_D_lower=str(D),scope='Full candidate tube and source regularity; no particle/coil performance assertion.')
Path('results/candidate_tube_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
