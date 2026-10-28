"""A complete reference tube, rather than a sampled cross-section.
Outward multiprecision AGM elliptic-integral and elementary-function bounds.
"""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parents[2]/'capability_backward_bridge/code/vendor'))
import mpmath as mp
mp.iv.dps=60
iv=mp.iv

def point(q):return iv.mpf(q)
def interval(lo,hi):return iv.mpf([lo,hi])
def K(m):
 a=point(1);b=iv.sqrt(1-m)
 for _ in range(14):a,b=(a+b)/2,iv.sqrt(a*b)
 return iv.pi/(2*iv.mpf([b.a,a.b]))
def sinh(x):return (iv.exp(x)-iv.exp(-x))/2
mlo=point('0.00619');mhi=point('0.00620')
rlo=K(1-mlo)/K(mlo);rhi=K(1-mhi)/K(mhi)
assert rlo.a>point('2.5').b and rhi.b<point('2.5').a
kap=2*K(1-interval('0.00619','0.00620'))/iv.pi
x=iv.sqrt(5)/((iv.exp(2*iv.pi/5)+iv.exp(-2*iv.pi/5))/2)
u0=iv.log(x+iv.sqrt(x*x-1))
# For Jacobi amplitude, sqrt(1-m)<=am'(x)<=1. Therefore
# cd(x|m)<=cos(sqrt(1-m)*x)/sqrt(1-m) while x<pi/2.
xmax=point('0.731');sq=iv.sqrt(1-mhi)
cd_upper=iv.cos(sq*xmax)/sq
assert cd_upper.b<point('0.75').a
# cd is decreasing on0<x<K; cd(xq)=1-q withq=1/4 impliesxq<xmax.
dmax=xmax/iv.mpf([kap.a,kap.b]);margin=u0-2*dmax
assert margin.a>0
Dmin=(sinh(u0-dmax)-sinh(dmax))**2
assert Dmin.a>0 and xmax.b<K(mlo).a
out={'status':'PASS','m_enclosure':['0.00619','0.00620'],'ratio_at_m_low':str(rlo),'ratio_at_m_high':str(rhi),'kappa':str(kap),'u0':str(u0),'profile_coordinate_absolute_bound':'0.731','cd_upper_at_bound':str(cd_upper),'coordinate_displacement_upper':str(dmax),'uniform_u_minus_abs_v_lower':str(margin),'uniform_D_lower':str(Dmin),'tube_delta_psi_max':'1/4','scope':'Complete smooth nested reference tube stays inside analytic profiles and regular u>|v| web. Global embedding follows separate explicit monotone inverse proof; not a particle or finite-coil theorem.'}
Path('results/reference_tube_certificate.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
