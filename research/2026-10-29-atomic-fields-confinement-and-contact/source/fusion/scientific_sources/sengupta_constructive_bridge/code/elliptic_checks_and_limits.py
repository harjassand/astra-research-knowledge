"""Independent high-precision checks of Jacobi identities plus geometric limit formulas."""
from pathlib import Path
import sys,json
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parents[2]/'capability_backward_bridge/code/vendor'))
import mpmath as mp
mp.mp.dps=65
errors=[]
for m in map(mp.mpf,['.006192','.1','.5','.9']):
 k=mp.sqrt(m);K=mp.ellipk(m);KP=mp.ellipk(1-m)
 for t in [mp.mpf('.13'),KP/3,KP/2]:
  dn=mp.ellipfun('dn',t,1-m);A=1/dn+dn/k
  direct=mp.ellipfun('sn',K+1j*t,m)+mp.ellipfun('sn',K+1j*(KP+t),m)
  dnshift=mp.ellipfun('dn',t+KP,1-m)
  errors.append(float(abs(direct-A)/A));errors.append(float(abs((1/dnshift+dnshift/k)-A)/A))
for g in map(mp.mpf,['.0294372515','.3','.8']):
 KT=mp.ellipk(1-g)
 for t in [mp.mpf('.2'),KT/3]:
  mu=mp.ellipfun('dn',t,1-g)**2;mushift=mp.ellipfun('dn',t+KT,1-g)**2
  errors.append(float(abs(mu*mushift-g)))
assert max(errors)<1e-60
r=json.loads(Path('results/reference_well.json').read_text());m=mp.mpf(r['m']);k=mp.sqrt(m);kap=mp.mpf(r['kappa']);u0=mp.mpf(r['u0']);R=mp.sinh(u0);P=mp.cosh(u0)
branches=[]
for v in r['stationary_points_one_period']:
 if mp.mpf(v['B_second'])<=0:continue
 for j in range(4):
  z=mp.mpf(v['zeta'])+j*mp.pi/2;t=kap*z;sf=mp.ellipfun('sn',t,1-m);dn=mp.ellipfun('dn',t,1-m)
  D=P*P-mp.sin(2*z)**2;T=1-(1-k)*sf**2
  hu=kap**2*(1-m)*T/(dn*dn);hv=kap**2*(1-m)*T/k
  bu=-P*R/D;bv=-R*mp.sin(2*z)/D
  S=mp.sqrt(2*(bu*bu/hu+bv*bv/hv));branches.append(dict(zeta=float(z),half_spread_coefficient=float(S)))
out=dict(status='PASS',maximum_relative_identity_error=max(errors),scope='High-precision identity checks accompany exact symbolic/general proofs; not a uniform numerical proof.',all_reference_axis_wells=branches,reference_axis_S_min=min(v['half_spread_coefficient'] for v in branches),reference_axis_S_max=max(v['half_spread_coefficient'] for v in branches),limiting_geometry=dict(R_definition='sinh(u0) forv0=delta=0,N=1',curvature_min='R/(R²+1)',curvature_max='sqrt(R²+4)/R²',necessary_circular_normal_tube_radius_upper='R²/sqrt(R²+4)',fixed_iota_R_upper='sqrt(iota^-2−1)',reference_R=float(R),reference_curvature_min=float(R/(1+R*R)),reference_curvature_max=float(mp.sqrt(R*R+4)/(R*R)),reference_normal_reach_upper=float(R*R/mp.sqrt(R*R+4)),warning='A circular normal-tube bound is not an arbitrary-shape plasma or coil engineering no-go.'))
Path('results/elliptic_checks_and_limits.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
