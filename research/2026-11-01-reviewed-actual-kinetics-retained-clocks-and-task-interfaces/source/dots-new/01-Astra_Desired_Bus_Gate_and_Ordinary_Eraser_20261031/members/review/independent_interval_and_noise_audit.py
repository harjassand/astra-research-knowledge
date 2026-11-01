"""Independent high-precision interval receiving and corrected variance-only noise tests."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
import mpmath as mp
import numpy as np
root=Path(__file__).resolve().parent;mp.mp.dps=130
cert=json.loads((root/'bus_certificates.json').read_text());out=[]
def frac(x):
 x=F(x);return mp.mpf(x.numerator)/x.denominator
def inside(name,v,r):
 lo,hi=map(frac,r['interval']);assert lo<=v<=hi,(name,mp.nstr(v,50));out.append(dict(name=name,value=mp.nstr(v,75),interval_width=mp.nstr(hi-lo,8)))
pi=mp.pi;T=2*pi;I=pi/8
inside('pi',pi,cert['pi']);inside('force_peak_bound',mp.sqrt(mp.mpf(17)/75),cert['force_peak_upper']);inside('force_slew_bound',mp.mpf(53)/(20*mp.sqrt(6)),cert['force_slew_upper'])
inside('integrated_drive_energy',I*(mp.mpf(4)/3+mp.mpf(1)/100),cert['integrated_drive_energy']);inside('local_Z_coefficient',50*pi,cert['local_Z_coefficient_requirement']);inside('unmonitored_diamond',1-mp.exp(-pi/5),cert['unmonitored_exact_bus_diamond'])
g=mp.mpf(477)/1000;K2=mp.mpf(13)/50;E=g*g*T;Imin=2*I*I/(E+mp.sqrt(E*E-4*K2*I*I))
inside('all_closed_minimum_I',Imin,cert['all_closed_fixed_B_minimum_I']);inside('all_closed_unmonitored_lower',1-mp.exp(-mp.mpf(8)/5*Imin),cert['all_closed_fixed_B_unmonitored_diamond_lower'])
for row in cert['rows']:
 p=row['parameters'];beta=mp.mpf(p['beta']);W=1/beta;D=beta*beta+1;r=mp.exp(-beta*T)
 Finf=(T*(1+beta*beta/(2*D))-(1-r)/(beta*D*D))/24;tail=(1-r)**2*mp.exp(-2*beta*W)/(48*beta*D*D);Fw=Finf-tail
 Ac=mp.mpf(999)/5000*Fw;L=I/5-Ac;a=mp.exp(-2*L);q=1-a**4;w=1-a
 vals={'integrated_bus_occupation':I,'captured_fraction':Fw/I,'captured_displacement_energy':Ac,'inaccessible_displacement_energy':L,'small_loss_margin':q-2*w,'exact_bus_diamond':q,'continuing_data_upper':mp.mpf(4)/10000*(T+W+mp.mpf(1)/100),'ADC_upper':4*mp.sqrt(Ac/2)/100000,'saturation_upper':2*mp.exp(-25)/(5*mp.sqrt(pi))}
 vals['complete_error_upper']=q+vals['continuing_data_upper']+vals['ADC_upper']+vals['saturation_upper']+mp.mpf(1)/1000
 for name,v in vals.items():inside(p['beta']+'_'+name,v,row[name])
 assert row['meets_0_01']==(vals['complete_error_upper']<=mp.mpf(1)/100)

# This is an extra channel-norm upper bound, not Gaussian identification.
B=np.array([2,0,0,-2]);rng=np.random.default_rng(6147);noise=[]
for values,prob,k in [(np.array([-.25,.25]),np.array([.5,.5]),1),(np.array([-.1,.9]),np.array([.9,.1]),.8),(np.array([-1,0,1]),np.array([.01,.98,.01]),.3)]:
 assert abs(prob@values)<1e-14;var=prob@(values*values);C=sum(p*np.exp(1j*k*x*(B[:,None]-B[None,:])) for p,x in zip(prob,values));bound=min(2.,8*k*k*var);maximum=0.
 for j in range(20):
  v=rng.normal(size=16)+1j*rng.normal(size=16);v/=np.linalg.norm(v);rho=np.outer(v,v.conj());diff=(rho.reshape(4,4,4,4)*(C-1)[:,None,:,None]).reshape(16,16);e=float(np.linalg.norm(diff,ord='nuc'));assert e<=bound+1e-12;maximum=max(maximum,e)
 noise.append(dict(noise_values=values.tolist(),probabilities=prob.tolist(),gain=k,variance=float(var),valid_extra_diamond_upper=bound,max_sampled_reference_error=maximum))
result={'high_precision_interval_checks':len(out),'interval_results':out,'corrected_non_Gaussian_noise_checks':60,'noise_results':noise,'scope':'Independent 130-digit interval checks are diagnostic; interval proof and generic centered-noise bound were also reviewed analytically.'}
(root/'independent_interval_and_noise_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='interval_results'},indent=2))
