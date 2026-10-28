"""High-precision source-axis stationary well and exact first-order transverse data."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parents[2]/'capability_backward_bridge/code/vendor'))
import mpmath as mp
mp.mp.dps=70
m=mp.findroot(lambda t:mp.ellipk(1-t)/mp.ellipk(t)-mp.mpf('2.5'),(mp.mpf('.005'),mp.mpf('.008')))
k=mp.sqrt(m);K=mp.ellipk(m);KP=mp.ellipk(1-m);kap=2*KP/mp.pi
u0=mp.acosh(mp.sqrt(5)/mp.cosh(2*mp.pi/5));aa=mp.sinh(u0);PP=mp.cosh(u0)
def axis(z):
 dn=mp.ellipfun('dn',kap*z,1-m);A=1/dn+dn/k;D=PP**2-mp.sin(2*z)**2
 return A/mp.sqrt(D)
def deriv(z):return mp.diff(axis,z)
roots=[mp.mpf(0),mp.pi/4,mp.pi/2]
for i in range(20):
 a=mp.pi*i/40;b=mp.pi*(i+1)/40
 if deriv(a)*deriv(b)<0:
  q=mp.findroot(deriv,(a,b))
  if 0<q<mp.pi/2 and all(abs(q-r)>mp.mpf('1e-40') for r in roots):roots.append(q)
roots=sorted(roots);mins=[r for r in roots if mp.diff(axis,r,2)>0];z=min(mins,key=axis)
B=axis(z);D=PP**2-mp.sin(2*z)**2;tau=kap*z
sf=mp.ellipfun('sn',tau,1-m);df=mp.ellipfun('dn',tau,1-m)
T=1-(1-k)*sf**2;Huu=kap**2*(1-m)*T/df**2;Hvv=kap**2*(1-m)*T/k
bu=-PP*aa/D;bv=-aa*mp.sin(2*z)/D # relative ∂uB/B, ∂vB/B
S=mp.sqrt(2*(bu**2/Huu+bv**2/Hvv))
# Unit direction in(u,v) maximizing well-bottom variation on Δpsi=h².
du=mp.sqrt(2)*(bu/Huu)/mp.sqrt(bu**2/Huu+bv**2/Hvv)
dv=mp.sqrt(2)*(bv/Hvv)/mp.sqrt(bu**2/Huu+bv**2/Hvv)
Bss=mp.diff(axis,z,2)/D
# Vacuum curvature identity checked from the axis curve itself.
gamma=lambda t:mp.matrix([aa*mp.cos(t),aa*mp.sin(t),mp.sin(2*t)/2])
tan=mp.diff(gamma,z);acc=mp.diff(gamma,z,2)
cross=mp.matrix([tan[1]*acc[2]-tan[2]*acc[1],tan[2]*acc[0]-tan[0]*acc[2],tan[0]*acc[1]-tan[1]*acc[0]])
curvature=mp.norm(cross)/mp.norm(tan)**3
# Inverse transverse metric has diagP² and crossP E.
E=-mp.sin(2*z);normgrad=mp.sqrt((bu*bu+bv*bv-2*(E/PP)*bu*bv)/D)
assert abs(curvature-normgrad)<mp.mpf('1e-60')
out={'status':'PASS','scope':'High-precision stationary-well calculation and exact first-order derivatives; not a finite-radius confinement certificate.','m':str(m),'k':str(k),'u0':str(u0),'kappa':str(kap),'stationary_points_one_period':[{'zeta':str(r),'B':str(axis(r)),'B_second':str(mp.diff(axis,r,2))} for r in roots],'selected_min_zeta':str(z),'B_min':str(B),'B_ss_at_min':str(Bss),'axis_curvature_at_min':str(curvature),'relative_grad_B_uv':[str(bu),str(bv)],'psi_Hessian_uv':[str(Huu),str(Hvv)],'relative_half_well_bottom_spread_per_sqrt_DeltaPsi':str(S),'maximizing_flux_normal_direction_du_dv':[str(du),str(dv)],'DeltaPsi_for_linear10percent_action_variation_at1percent_deep_well':str((mp.mpf('.001')/S)**2),'DeltaPsi_for_linear_well_shift_equal1percent_depth':str((mp.mpf('.01')/S)**2)}
Path('results/reference_well.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
