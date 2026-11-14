from pathlib import Path
import sys,json,time,math
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'deps'))
import numpy as np
from scipy.integrate import quad
start=time.perf_counter()
# A damped causal oscillator h(t)=exp(-gamma*t)*sin(Omega*t), t>=0.
# Transform convention H(w)=integral h(t)*exp(i*w*t) dt.
# Its absorption is Im H and its time L2 energy is analytic below.
w=np.linspace(20,72,10401);Omega=100.0
osc=[]
for gamma in (1.,.1,.01,.001,.0001,.00001,.000001):
 H=Omega/((gamma-1j*w)**2+Omega**2)
 osc.append({'Omega':Omega,'gamma':gamma,'max_abs_imag_in_band_20_72':float(np.max(abs(H.imag))),'max_abs_real_in_band_20_72':float(np.max(abs(H.real))),'time_L2_energy_exact':Omega**2/(4*gamma*(gamma**2+Omega**2)),'passive_positive_absorption':bool(np.all(H.imag>=0))})
# Exact bright amplitude for i bdot = g*d; i ddot = g*b+Delta*d.
g=.7;Delta=1.1;R=math.sqrt(Delta**2+4*g*g)
def b(t):return np.exp(-.5j*Delta*t)*(np.cos(.5*R*t)+1j*Delta/R*np.sin(.5*R*t))
def bd(t):
 return np.exp(-.5j*Delta*t)*(-.5j*Delta*(np.cos(.5*R*t)+1j*Delta/R*np.sin(.5*R*t))-.5*R*np.sin(.5*R*t)+.5j*Delta*np.cos(.5*R*t))
errors=[]
for t in np.linspace(.05,8,25):
 integrand=lambda s:np.exp(-1j*Delta*(t-s))*b(s)
 I=quad(lambda s:integrand(s).real,0,t,epsabs=1e-12)[0]+1j*quad(lambda s:integrand(s).imag,0,t,epsabs=1e-12)[0]
 errors.append(float(abs(bd(t)+g*g*I)))
out={'purpose':'Analytic countermodel checks, not physical validation or novelty evidence.','finite_band_causal_oscillator':osc,'bright_dark_elimination':{'g':g,'Delta':Delta,'n_test_times':len(errors),'max_derivative_vs_memory_integral_residual':max(errors),'claim':'Explicit unobserved-state dynamics and its eliminated causal-memory representation predict identical bright response; representation is not a distinct physical mechanism.'},'wall_seconds_measured':time.perf_counter()-start,'model_tokens':'UNAVAILABLE','physical_experiment_performed':False}
(ROOT/'CAUSAL_AMBIGUITY_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
