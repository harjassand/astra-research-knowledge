#!/usr/bin/env python3
"""Joined no-reset physical-protocol illustration; see execution_limits in JSON.
ODE quadratures are numerical diagnostics. The learner receives only rounded
reports. Its final rational positive model is independently checked exactly.
"""
from fractions import Fraction as Q
import importlib.util, json, sys, argparse
from pathlib import Path
from math import ceil, exp, log, sqrt
from time import perf_counter
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp, quad
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('positive_fit',P.parent/'independent'/'passive_certified_fit.py')
fit=importlib.util.module_from_spec(spec);sys.modules[spec.name]=fit;spec.loader.exec_module(fit)
MU=B=T=1.;CUBIC=.15
def vp(x):return MU*x+CUBIC*x**3
def vpp(x):return MU+3*CUBIC*x*x
def S(t):
 t=np.clip(t,0,1);return t**3*(10+t*(-15+6*t))
def dS(t):
 t=np.clip(t,0,1);return 30*t*t*(1-t)**2
zero=lambda t:(0.,0.)

def integrate(rates,weights,state,duration,k,command=zero,forcing=None,drive=None):
 mass=sum(weights)
 def rhs(t,s):
  stiffness=k(t) if callable(k) else k
  u,du=command(t)
  force=stiffness*(u-s[0])+du if forcing is None else forcing(t)
  if drive is not None:force+=drive(t)
  return np.r_[force-vp(s[0])+weights@(s[1:]-s[0]),rates*(s[0]-s[1:])]
 def jac(t,s):
  stiffness=k(t) if callable(k) else k
  if forcing is not None:stiffness=0.
  a=np.zeros((len(state),len(state)));a[0,0]=-stiffness-vpp(s[0])-mass
  a[0,1:]=weights;a[1:,0]=rates
  a[np.arange(1,len(state)),np.arange(1,len(state))]=-rates
  return a
 sol=solve_ivp(rhs,(0,duration),state,method='BDF',jac=jac,dense_output=True,rtol=2e-10,atol=2e-12)
 if not sol.success:raise RuntimeError(sol.message)
 return sol

gx,gw=leggauss(24)
def integ(fun,a,b):return (b-a)/2*np.dot(gw,fun((a+b)/2+(b-a)*gx/2))
def report(sol,a,w,k,u):
 """Only visible x, applied trap force, and known V'(u) enter."""
 x=lambda t:sol.sol(t)[0]
 force=lambda t:k*(u-x(t))
 xl=integ(x,a,a+w)/w;xr=integ(x,a+w,a+2*w)/w
 ft=integ(lambda t:(t-a)*force(t)/w**2,a,a+w)
 ft+=integ(lambda t:(a+2*w-t)*force(t)/w**2,a+w,a+2*w)
 return ft-vp(u)-(xr-xl)/w

def covariance(starts,w,sf,sx):
 """Shared white-meter covariance, integrated as piecewise polynomials."""
 def val(t,a):
  if a<t<a+w:return (t-a)/w**2,1/w**2
  if a+w<t<a+2*w:return (a+2*w-t)/w**2,-1/w**2
  return 0.,0.
 out=np.zeros((len(starts),len(starts)))
 for i,a in enumerate(starts):
  for j in range(i+1):
   b=starts[j];knots=sorted(set([a,a+w,a+2*w,b,b+w,b+2*w]));v=0.
   for lo,hi in zip(knots[:-1],knots[1:]):
    mid=(lo+hi)/2
    if not(a<mid<a+2*w and b<mid<b+2*w):continue
    for g in [-1/sqrt(3),1/sqrt(3)]:
     t=mid+(hi-lo)*g/2;p,dp=val(t,a);q,dq=val(t,b)
     v+=(hi-lo)/2*(sf*sf*p*q+sx*sx*dp*dq)
   out[i,j]=out[j,i]=v
 return out

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--reuse-fit',action='store_true',
                     help='Reuse and exactly reverify an existing fit only if every report matches.')
 args=parser.parse_args()
 start=perf_counter();plan=fit.make_plan(Q(1,32));eta=float(plan.delta)*B
 nodes=np.array([float(t)*T for t in plan.nodes])
 rates=np.r_[0.,np.geomspace(1e-8,1e6,63)]
 weights=.6+np.cos(np.arange(64)*.71)**2;weights[0]*=5;weights/=weights.sum()
 hidden=.21*np.sin(np.arange(64)*.37)+.08;hidden[0]=.28
 state=np.r_[0.,hidden];E0=.5*(weights@hidden**2);G0=sqrt(2*B*E0)
 A,h,w=.2,.004,.004;L=vpp(A+.01);delta=eta*A/(64*(B+L))
 Xinitial=G0/MU;Xhistory=max(Xinitial,A+delta);G=G0+B*Xhistory
 D=G+B*delta+2*B*A+vp(A)
 k=max(2*D/delta,4*(G0+B*Xinitial)/delta)
 tau_ramp=.1;tau_center=log(max(1.,2*Xinitial/delta))/(k+MU+B)
 Hcal=2*w+8*G*(h+T+4*w)/(exp(1)*A*eta)
 init=integrate(rates,weights,state,tau_ramp,lambda t:k*S(t/tau_ramp))
 cent=integrate(rates,weights,init.y[:,-1],tau_center,k)
 aged=integrate(rates,weights,cent.y[:,-1],Hcal,k)
 baseline=report(aged,Hcal-2*w,w,k,0.)
 pulse=integrate(rates,weights,aged.y[:,-1],h,k,lambda t:(A*S(t/h),A*dS(t/h)/h))
 post=integrate(rates,weights,pulse.y[:,-1],T+2*w,k,lambda t:(A,0.))
 values=np.array([report(post,t,w,k,A) for t in nodes])
 sf,sx=1e-8,1e-11;alpha_acq=alpha_init=.005
 cov=covariance(np.r_[-2*w,h+nodes],w,sf,sx);ev,vec=np.linalg.eigh(cov)
 rng=np.random.default_rng(20261105);noise=vec@(np.sqrt(np.maximum(ev,0))*rng.normal(size=len(ev)))
 measured=(values+noise[1:]-baseline-noise[0])/A
 reports=[fit.nearest_dyadic(Q(float(v/B)),plan.bits_y) for v in measured]
 Fread=k*delta;n=ceil(16*Fread/(A*eta));bf,bx=1e-8,1e-11
 components={
  'old_force_drift':G*(h+T+4*w)/(exp(1)*(Hcal-2*w)*A),
  'tracking_and_nonlinearity':(4*B+2*L)*delta/A,
  'finite_force_bins':2*Fread/(n*A),
  'meter_bias':2*(bf+2*bx/w)/A,
  'joint_noise':sqrt(2*(4*sf**2/(3*w)+4*sx**2/w**3)/A**2*log(2*len(nodes)/alpha_acq)),
  'finite_reporting':2.**(-plan.bits_y-1)*B}
 acq_bound=sum(components.values())
 if acq_bound>eta:raise RuntimeError('Acquisition error budget not closed')
 old=P/'physical_bridge_results.json'
 if args.reuse_fit and old.exists():
  olddata=json.loads(old.read_text())
  assert olddata['acquisition']['reports']==[str(q) for q in reports]
  assert olddata['declared_B']==B and olddata['horizon']==T
  result=olddata['fit']
  mass=sum(Q(m['weight']) for m in result['model'])
  assert 0<=mass<=1 and all(Q(m['weight'])>=0 and Q(m['pole'])>=0 for m in result['model'])
  residual=Q(0);bits=fit.ceil_log2(128/plan.delta)
  for t,r in zip(plan.nodes,reports):
   lo=hi=Q(0)
   for m in result['model']:
    low,high=fit.exp_neg_bounds(t*Q(m['pole']),bits)
    lo+=Q(m['weight'])*low;hi+=Q(m['weight'])*high
   residual=max(residual,abs(lo-r),abs(hi-r))
  assert residual<=Q(result['max_verified_report_residual_exact'])
  assert plan.a+16*fit.pow2(-plan.n)+plan.L*(residual+2*plan.delta)<=Q(result['certified_L1_bound_exact'])
 else:
  result=fit.fit_certified(plan,reports)
 smoothing=B*(h/2+w);zeta=B*T*result['certified_L1_bound']+smoothing
 returned=integrate(rates,weights,post.y[:,-1],h,k,lambda t:(A*(1-S(t/h)),-A*dS(t/h)/h))
 gamma_target=.002;wi=.01;F=.4;tau_release=1e-6
 Hi=2*wi+2*G*(T+2*wi)/(exp(1)*gamma_target)
 guard=integrate(rates,weights,returned.y[:,-1],Hi,k)
 si=sqrt(2*sf**2/(3*wi)+2*sx**2/wi**3)
 c=-(report(guard,Hi-2*wi,wi,k,0.)+rng.normal()*si)
 c=float(np.clip(c,-G-2*B*delta,G+2*B*delta))
 delta_release=delta+(G+F+abs(vp(0.)))*tau_release
 gamma=G*(T+2*wi+tau_release)/(exp(1)*(Hi-2*wi))+2*B*delta+B*delta_release+si*sqrt(2*log(2/alpha_init))+Fread/n+bf+2*bx/wi+L*delta
 mr=np.array([float(Q(m['pole']))/T for m in result['model']])
 mw=np.array([float(Q(m['weight']))*B for m in result['model']])
 Dstate=max(abs(c)/MU,F/MU);xmax=abs(c)/MU+Dstate
 Dvel=F+(vpp(xmax)+2*B)*Dstate;bound=max(delta_release,(zeta*Dvel+gamma)/MU)
 tests={'dc':lambda t:.35,'sinusoid':lambda t:.4*np.sin(2*np.pi*t),
        'smooth_pulse':lambda t:.4*np.sin(np.pi*t)**2,
        'two_tones':lambda t:.25*np.sin(6*np.pi*t)+.15*np.cos(2*np.pi*t)}
 ts=np.linspace(0,T,1501);traces={'time':ts.tolist()};checks={}
 for name,f in tests.items():
  release=integrate(rates,weights,guard.y[:,-1],tau_release,
                    lambda t:k*(1-S(t/tau_release)),
                    drive=lambda t:f(0.)*S(t/tau_release))
  truth=integrate(rates,weights,release.y[:,-1],T,0.,forcing=f)
  small=integrate(mr,mw,np.zeros(len(mr)+1),T,0.,forcing=lambda t:f(t)+c)
  tx=truth.sol(ts)[0];sy=small.sol(ts)[0]
  checks[name]={'sampled_maximum_error':float(max(abs(tx-sy))),
               'analytic_bound_without_numerical_solver_budget':bound,
               'true_rhs_calls':truth.nfev,'model_rhs_calls':small.nfev,
               'actual_initial_x_after_finite_release':float(release.y[0,-1])}
  traces[name+'_true']=tx.tolist();traces[name+'_model']=sy.tolist()
 factors=np.array([integ(lambda s:30*(s/h)**2*(1-s/h)**2/h*np.exp(-r*(h-s)),0,h) for r in rates])
 read=np.ones_like(rates);nz=rates>0;read[nz]=(-np.expm1(-rates[nz]*w)/(rates[nz]*w))**2
 actual=np.exp(-np.outer(nodes,rates))@(weights*factors*read)
 diag_report=float(max(abs(np.array([float(q) for q in reports])*B-actual)))
 def diff(t):return abs(weights@np.exp(-rates*t)-mw@np.exp(-mr*t))
 knots=sorted(set([0.,T]+[min(T,1/r) for r in rates if r>0]))
 diag_l1=sum(quad(diff,a,b,epsabs=2e-10,limit=100)[0] for a,b in zip(knots[:-1],knots[1:]))
 out={'seed':20261105,'source_modes_diagnostic_only':64,'source_rates_diagnostic_only':[0.,1e-8,1e6],
  'declared_B':B,'mu':MU,'horizon':T,'initial_energy':E0,'amplitude':A,
  'hidden_force_envelope':G,
  'finite_control':{'stiffness':k,'tracking_allowance':delta,'ramp_time':h,
   'initial_stiffness_ramp_time':tau_ramp,'centering_time':tau_center,
   'command_speed':15*A/(8*h),'command_acceleration':10*sqrt(3)*A/(3*h*h),
   'trap_speed_bound':15*A/(8*h)+10*sqrt(3)*A/(3*h*h*k),
   'trap_acceleration_bound':10*sqrt(3)*A/(3*h*h)+60*A/(h**3*k),
   'initial_force_bound':k*Xinitial,'probe_force_bound':15*A/(8*h)+k*delta,
   'hold_force_bound':Fread,'finite_release_time':tau_release,
   'release_stiffness_slew_bound':15*k/(8*tau_release),
   'release_trap_force_bound':k*delta_release,
   'moving_viscous_support_speed_bound':F,
   'support_acceleration_during_initial_drive_ramp':15*F/(8*tau_release),
   'support_travel_release_and_deployment_bound':F*(T+tau_release)},
  'acquisition':{'quiet_hold':Hcal,'half_bin_width':w,'nodes':len(nodes),
   'force_bins_per_half_window':n,'force_average_count':2*n*(len(nodes)+2),
   'position_average_count':2*(len(nodes)+2),'sigma_force':sf,'sigma_position':sx,
   'report_error_allowance':eta,'closed_error_bound':acq_bound,'components':components,
   'diagnostic_max_report_error':diag_report,'reports':[str(q) for q in reports]},
  'fit':result,'kernel_L1_certificate':zeta,'smoothing_budget':smoothing,'diagnostic_kernel_L1':diag_l1,
  'initialization':{'hold':Hi,'half_bin_width':wi,'measured_bath_force':c,
   'force_forecast_error_bound':gamma,'actual_guard_exit_x_diagnostic':float(guard.y[0,-1]),
   'deployment_initial_coordinate_bound':delta_release,'hidden_reset':False},
  'deployment':{'force_amplitude_bound':F,'velocity_bound':Dvel,'uniform_bound':bound,'checks':checks},
  'physical_duration':tau_ramp+tau_center+Hcal+2*h+T+2*w+Hi+tau_release+T,
  'wall_seconds':perf_counter()-start,
  'execution_limits':[
   'BDF and Gaussian-quadrature readouts are floating numerical illustrations, not interval-validated physical data.',
   'Fine force bins are fully costed and their error charged, but are represented by sufficient statistics rather than individually materialized.',
   'The fitter receives rounded reports and mass/horizon bounds, never microscopic source rates or weights.',
   'Four simulated deployment alternatives replay the same saved bath state; no physical reset or repeatability is claimed.',
   'Each deployment includes a finite stiffness release and finite rise to its initial force. The movable viscous support and switchable stiffness are explicit additional physical resources.',
   'The source-model theorem and exact model verifier establish the conditional certificate, not sampled diagnostic errors.',
   'The deployed BDF simulation is not the separately proved residual-certified digital compiler; certified deployment must add its numerical residual budget.']}
 (P/'physical_bridge_results.json').write_text(json.dumps(out,indent=2)+'\n')
 (P/'trajectory_traces.json').write_text(json.dumps(traces)+'\n')
 print(json.dumps({'modes':len(mr),'kernel_bound':zeta,'kernel_diagnostic':diag_l1,
  'trajectory_bound':bound,'max_sampled_trajectory_error':max(v['sampled_maximum_error'] for v in checks.values()),
  'physical_duration':out['physical_duration'],'force_average_count':out['acquisition']['force_average_count'],
  'wall_seconds':out['wall_seconds']},indent=2))

if __name__=='__main__':main()
