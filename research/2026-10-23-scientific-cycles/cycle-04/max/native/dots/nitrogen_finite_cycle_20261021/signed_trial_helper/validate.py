from pathlib import Path
import time,resource,json,hashlib,sys
import numpy as np
from helper import SignedTrialKernel,m,SOURCE
start=time.perf_counter();k=SignedTrialKernel();old=m.ThermoKernel();rng=np.random.default_rng(1021)
n=256;T=rng.uniform(201,3499,n);Y=rng.dirichlet(np.ones(6),n).T;P=rng.uniform(.51,1.99,n)*101325
b=old.evaluate(T,Y,P,strict=True,return_rates=True)
a=k.evaluate_rho_u(b['rho'],b['rho']*b['internal_energy'],Y,strict=True,return_rates=True)
err={}
for field in ['T','rho','cp','cv','Rmix','internal_energy','mass_production','forward_rates_of_progress','reverse_rates_of_progress','viscosity','conductivity']:
 scale=np.maximum(1,abs(b[field]));err[field]=float(np.max(abs(a[field]-b[field])/scale))
assert max(err.values())<1e-8,err
# Signed mixtures at fixed rho and prescribed T, and conservative inversions.
Ys=Y.copy();Ys[2]=-rng.uniform(1e-12,9e-4,n);Ys[0]+=1-Ys.sum(axis=0)
Rmix=k.R*(Ys/k.W[:,None]).sum(axis=0);rho=P/(Rmix*T)
cp,h,s=k.thermochemistry(T);es=(h-1)*k.R*T/k.W[:,None];U=rho*(Ys*es).sum(axis=0)
a=k.evaluate_rho_u(rho,U,Ys,return_rates=True)
assert np.max(abs(a['T']-T))<1e-7
assert np.array_equal(a['Y'],Ys)
assert np.max(abs(a['pressure']-P)/P)<1e-10
assert np.max(abs(a['conservative_energy_residual_J_m3']))<1e-5
# Exact integer element balance (independent N/O atom count).
E=np.array([[2,0,1,0,1,1],[0,2,0,1,1,2]],dtype=int)
assert np.array_equal(E@k.nu,np.zeros((2,7)))
assert np.max(abs(k.W@k.nu))<1e-13
mol=a['mass_production']/k.W[:,None];bal=E@mol
balance=float(np.max(abs(bal))/max(1,np.max(abs(mol))))
assert balance<1e-14
# Independently implemented ordinary polynomial rates and analytic N derivative.
t=np.array([2700.]);C=np.array([.002,.0006,0.,1e-5,1e-4,1e-6])[:,None]
# Derivative of fourth reaction: k4 C_O2 C_N - k4/Kc C_NO C_O.
# None of k4 or Kc depends on C_N at fixed T and other concentrations.
expected=np.exp(np.log(9.7e-21*k.A)+1.01*np.log(t)-3120/t)*C[1]
hstep=1e-12;cm=C.copy();cp_=C.copy();cm[2]-=hstep;cp_[2]+=hstep
rm=k.signed_rates(t,cm)[0];r0=k.signed_rates(t,C)[0];rp=k.signed_rates(t,cp_)[0]
dleft=(r0[3]-rm[3])/hstep;dright=(rp[3]-r0[3])/hstep
assert np.max(abs(dleft/expected-1))<1e-7
assert np.max(abs(dright/expected-1))<1e-7
# Negative N fourth-reaction forward flux must be negative, not clipped to zero.
assert k.signed_rates(t,cm)[1][3,0]<0
# All 7 polynomial rates, including actual signed third-body / Lindemann terms.
def algebra(t,C):
 A=k.A;M=k.third_body_efficiencies@C
 rates=np.stack([5e-14*A*np.exp(-113200/t)*(-np.expm1(-3354/t))*M[0],3.7e-14*A*np.exp(-59380/t)*(-np.expm1(-2238/t))*M[1],3e-16*A*np.exp(-38000/t),9.7e-21*A*t**1.01*np.exp(-3120/t),2.4e-15*A*np.exp(-74700/t)*M[2],4.9e-16*A*t**(-.4),5.5e-18*A*np.exp(188/t)])
 low=9.2e-40*A*A*t**(-1.6)*M[2];rates[5]=rates[5]*low/(rates[5]+low)
 _,h,s=k.thermochemistry(t);K=np.exp(-k.nu.T@(h-s))*(k.P0/(k.R*t))**k.delta_nu[:,None]
 f=np.stack([C[0],C[1],C[0]*C[3],C[1]*C[2],C[4],C[4]*C[3],C[5]*C[3]])*rates
 r=np.stack([C[2]**2,C[3]**2,C[4]*C[2],C[4]*C[3],C[2]*C[3],C[5],C[4]*C[1]])*rates/K
 return f-r,f,r
C=rho*Ys/k.W[:,None];direct,f,r=algebra(T,C);net=k.signed_rates(T,C)[0]
polyerr=float(np.max(abs(net-direct)/np.maximum(1,abs(f)+abs(r))))
assert polyerr<1e-12
# Independent analytic-polynomial complex-step Jacobian at zero atomic N.
C0=np.array([.002,.0006,0.,1e-5,1e-4,1e-6])[:,None]
cc=C0.astype(complex);cc[2]+=1e-30j
exact_j=(k.nu@algebra(t,cc)[0]).imag[:,0]/1e-30
cm=C0.copy();cp_=C0.copy();cm[2]-=1e-12;cp_[2]+=1e-12
left=(k.nu@(k.signed_rates(t,C0)[0]-k.signed_rates(t,cm)[0]))[:,0]/1e-12
right=(k.nu@(k.signed_rates(t,cp_)[0]-k.signed_rates(t,C0)[0]))[:,0]/1e-12
jerr=max(np.max(abs(left-exact_j)/np.maximum(1,abs(exact_j))),np.max(abs(right-exact_j)/np.maximum(1,abs(exact_j))))
assert jerr<1e-5,(exact_j,left,right,jerr)
assert exact_j[2]<0 # atomic-N source has the required restoring slope
# Rejections remain explicit: negative accepted state, excessive trial, bad sum,
# bad pressure, bad energy. Trial energy clamp reports both original/effective.
reject=[]
for label,rr,uu,yy,kw in [('strict_negative',rho,U,Ys,{'strict':True}),('excess_negative',rho,U,Ys+np.array([.002,0,-.002,0,0,0])[:,None],{}),('bad_sum',rho,U,Ys*.99,{}),('bad_pressure',rho*10,U*10,Ys,{}),('bad_energy',rho,U+1e10,Ys,{})]:
 try:k.evaluate_rho_u(rr,uu,yy,**kw)
 except ValueError:reject.append(label)
 else:raise AssertionError(label)
report={'scope':'Synthetic signed Newton continuation only; no physical acceptance or cycle claim','positive_states':n,'signed_states':n,'positive_relative_errors':err,'max_signed_temperature_error_K':float(np.max(abs(a['T']-T))),'signed_mass_element_relative_residual':balance,'all_seven_polynomial_gross_scaled_error':polyerr,'N_zero_reaction4_derivative':{'expected':expected.tolist(),'left':dleft.tolist(),'right':dright.tolist()},'N_zero_total_source_derivative':{'polynomial_complex_step':exact_j.tolist(),'left':left.tolist(),'right':right.tolist(),'max_relative_error':float(jerr)},'rejections':reject,'wall_seconds':time.perf_counter()-start,'peak_rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
Path(__file__).with_name('validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
