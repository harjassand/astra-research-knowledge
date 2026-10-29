"""Actual fixed-curve N=3 Toda input -> local Abel -> doubling -> physical decode.
NONCERTIFIED numerical bridge. Independent physical ODE is comparator only.
"""
from pathlib import Path
import json,time,hashlib
import sympy as s
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
import rounded_relative_doubling as r
mp.mp.dps=125
x=r.x;C=mp.mpf(6);p=lambda z:z**3-15*z+8

def decode(angles):
 pts=[r.point(j,a) for j,a in enumerate(angles)];mu=[P['x'] for P in pts]
 kappas=[]
 for P in pts:
  pp=p(P['x']);yy=P['y']
  ka=(pp+yy)/(2*C) if abs(pp+yy)>=abs(pp-yy) else 2*C/(pp-yy)
  kappas.append(ka)
 Gp=[mu[0]-mu[1],mu[1]-mu[0]]
 a3sq=-C*sum(1/(k*d) for k,d in zip(kappas,Gp));assert a3sq>0
 W=[-C/(a3sq*k*d) for k,d in zip(kappas,Gp)]
 assert all(w>0 for w in W)
 b1=sum(w*u for w,u in zip(W,mu));a1=mp.sqrt(sum(w*(u-b1)**2 for w,u in zip(W,mu)))
 b2=sum(mu)-b1;b3=-sum(mu);a3=mp.sqrt(a3sq);a2=C/(a1*a3)
 return mp.matrix([a1,a2,a3,b1,b2,b3]),dict(mu=list(map(r.outnum,mu)),kappa=list(map(r.outnum,kappas)),weights=list(map(r.outnum,W)))

def local_jac(angles):
 J=mp.matrix(2,2)
 for j,theta in enumerate(angles):
  P=r.point(j,theta);xx=P['x'];W=mp.sqrt(-mp.fprod(xx-e for k,e in enumerate(r.EDGES) if k not in [2*j+1,2*j+2]))
  J[0,j]=-1/W;J[1,j]=-xx/W
 return J

def local_abel(theta0,h):
 def f(j,u,k):
  xx=r.point(j,u)['x'];W=mp.sqrt(-mp.fprod(xx-e for l,e in enumerate(r.EDGES) if l not in [2*j+1,2*j+2]))
  return -xx**k/W
 return mp.matrix([sum(mp.quad(lambda u:f(j,theta0[j]+u,k),[0,h[j]]) for j in range(2)) for k in range(2)])

def initialize(theta0,tau):
 target=mp.matrix([0,-2*tau]);h=mp.matrix([0,0]);J0=local_jac(theta0);inv=J0**-1;records=[]
 # Fixed-J contraction, not a global Abel/period inversion.
 for iteration in range(80):
  displacement=local_abel(theta0,h);res=displacement-target
  records.append(dict(iteration=iteration,residual=r.outnum(mp.norm(res)),angle_step=r.outnum(mp.norm(h)),
    fixed_J_derivative_norm=r.outnum(mp.norm(mp.eye(2)-inv*local_jac([theta0[j]+h[j] for j in range(2)]),2))))
  if mp.norm(res)<mp.mpf('1e-70'):break
  h=h-inv*res
 else:raise RuntimeError('initializer did not converge')
 return [theta0[j]+h[j] for j in range(2)],records

def physical_rhs(tt,z):
 a=z[:3];b=z[3:]
 return np.array([a[i]*(b[(i+1)%3]-b[i]) for i in range(3)]+[2*(a[i]**2-a[i-1]**2) for i in range(3)])

def compare(t,physical):
 initial=[1,2,3,0,1,-1];answers=[]
 for tol in [2e-12,2.3e-14]:
  sol=solve_ivp(physical_rhs,(0,float(t)),initial,rtol=tol,atol=tol/10,method='DOP853')
  assert sol.success
  z=sol.y[:,-1];answers.append(dict(rtol=tol,nfev=sol.nfev,state=list(map(float,z)),max_coordinate_error=float(max(abs(float(physical[j])-z[j]) for j in range(6))),
   energy_drift=float(abs(sum(z[3:]**2)/2+sum(z[:3]**2)-15)),product_drift=float(abs(np.prod(z[:3])-6))))
 return dict(runs=answers,ode_refinement_difference=max(abs(a-b) for a,b in zip(answers[0]['state'],answers[1]['state'])))

def main():
 start=time.perf_counter();path=Path(__file__).with_suffix('.json')
 # Derive monodromy exactly rather than insert a sheet sign by guess.
 aa=[s.Integer(1),s.Integer(2),s.Integer(3)];bb=[s.Integer(0),s.Integer(1),s.Integer(-1)]
 M=s.eye(2)
 for i in range(3):M=s.Matrix([[(x-bb[i])/aa[i],-aa[i-1]/aa[i]],[1,0]])*M
 assert s.expand(6*s.trace(M))==x**3-15*x+8
 G=s.Poly(x*x-x-1,x);M22=s.expand(M[1,1]);M11=s.expand(M[0,0]);ys=s.rem(s.Poly(12*M11-(x**3-15*x+8),x),G).as_expr();assert ys==5*x-9
 mu=[(1-mp.sqrt(5))/2,(1+mp.sqrt(5))/2];theta0=[]
 for j,u in enumerate(mu):
  angle=r.angle_of(dict(x=u,y=5*u-9),j)
  assert abs(angle.imag)<mp.mpf('1e-90');theta0.append(angle.real%(2*mp.pi))
 wrong_angles=[r.angle_of(dict(x=u,y=9-5*u),j).real%(2*mp.pi) for j,u in enumerate(mu)]
 wrong_state,_=decode(wrong_angles)
 z0,meta=decode(theta0);err0=mp.norm(z0-mp.matrix([1,2,3,0,1,-1]));assert err0<mp.mpf('1e-90')
 tau=mp.mpf(1)/64;angles,initialization=initialize(theta0,tau)
 ztau,_=decode(angles)
 data=dict(warning='Noncertified full physical bridge; floating analytic initialization/matching/projection/decoder. Exact rational curve/kernel algebra only.',
  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),prototype_sha256=hashlib.sha256(Path(r.__file__).read_bytes()).hexdigest(),
  fixed_curve=str(r.F.as_expr()),initial_a=[1,2,3],initial_b=[0,1,-1],exact_monodromy_M22=str(M22),exact_monodromy_M11=str(M11),exact_initial_y_mod_G=str(ys),
  rejected_M22_sheet_regression=dict(decoded_state=list(map(r.outnum,wrong_state)),expected_wrong_state=[1,3,2,1,0,-1],reason='For governing transfer convention kappa=psi_Nplus1=M11, while M22=1/kappa at Dirichlet roots'),
  initial_angles=list(map(r.outnum,theta0)),initial_decode_error=r.outnum(err0),initial_decode_metadata=meta,
  tau=r.outnum(tau),initializer=dict(method='fixed-J local Abel contraction using quadrature on original fixed curve, no physical ODE initialization',iterations=initialization,final_angles=list(map(r.outnum,angles)),ode_comparison=compare(tau,ztau)),records=[])
 path.write_text(json.dumps(data,indent=2));print('INITIALIZED '+json.dumps(dict(decode_error=r.outnum(err0),iterations=len(initialization),residual=initialization[-1]['residual'],ode_error=data['initializer']['ode_comparison']['runs'][-1]['max_coordinate_error'])),flush=True)
 A0=r.sumabel(theta0);bound=mp.norm(local_abel(theta0,mp.matrix([angles[j]-theta0[j] for j in range(2)]))-mp.matrix([0,-2*tau]))
 for step in range(1,12):
  rec=r.run_case('physical_time_doubling_'+str(step),theta0,angles,256,44,True)
  admitted=bool(rec.get('matching_below_quarter_input_separation') and rec.get('output_one_point_per_gap'))
  if not admitted:raise RuntimeError('Arithmetic admission failed at '+str(step)+': '+str(rec))
  angles=[mp.mpf(v) for v in rec['projected_output_angles']];time_t=tau*2**step
  direct=r.mod_period(r.sumabel(angles)-A0-mp.matrix([0,-2*time_t]))
  percall=mp.mpf(rec['abel_perturbation_norm'])+mp.mpf(rec['abel_perturbed_section_residual']['residual_norm']);bound=2*bound+percall
  physical,decode_meta=decode(angles)
  record=dict(step=step,time=r.outnum(time_t),admitted=admitted,direct_abel_error=direct['residual_norm'],accumulated_direct_error_budget=r.outnum(bound),below_budget=bool(mp.mpf(direct['residual_norm'])<=bound+mp.mpf('1e-27')),
   physical_state=list(map(r.outnum,physical)),decode_metadata=decode_meta,arithmetic=rec)
  if step in [1,6,10,11]:record['independent_physical_ode_comparison']=compare(time_t,physical)
  data['records'].append(record);data['seconds']=time.perf_counter()-start;path.write_text(json.dumps(data,indent=2))
  print(json.dumps({k:v for k,v in record.items() if k not in ['decode_metadata','arithmetic']}),flush=True)
if __name__=='__main__':main()
