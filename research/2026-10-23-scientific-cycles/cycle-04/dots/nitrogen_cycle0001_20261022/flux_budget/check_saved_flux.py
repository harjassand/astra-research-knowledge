"""Read-only thermal-path reaction-flux diagnostic; not a nonequilibrium trajectory.
N accounting: added NO+NO2 = -2 Delta N2 - Delta atomic N.
Gross N2 destruction gives a conditional upper envelope along this GIVEN path,
not a bound for paths with different state-resolved kinetics.
"""
from pathlib import Path
import sys,importlib.util,json,time,resource,hashlib
T0=time.monotonic();D=Path(__file__).resolve().parent;R=D.parents[1]
s=importlib.util.spec_from_file_location('signed',R/'nitrogen_finite_cycle_20261021/signed_trial_helper/helper.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);K=m.SignedTrialKernel()
import numpy as np
p=R/'nitrogen_lamella_20261022/restored_cross_width400um_N48_trajectory.npz';d=np.load(p);N=int(d['N']);t=d['t'];ii=np.flatnonzero(t<=150e-6);t=t[ii];state=d['state'][:,ii];mu=d['mu']/float(d['hot_mass_per_area']);yy=state[:5*N].reshape(5,N,-1);Y=np.concatenate([(1-yy.sum(0))[None],yy]);T=state[5*N:];rawmin=Y.min();yp=np.maximum(Y,0);yp/=yp.sum(0)
y=yp.reshape(6,-1);temp=T.reshape(-1);rho=101325/(K.R*np.sum(y/K.W[:,None],axis=0)*temp);net,f,b,lk=K.signed_rates(temp,rho*y/K.W[:,None]);fr=(f/rho*1000).reshape(7,N,-1);br=(b/rho*1000).reshape(7,N,-1)
# R1=N2+M->2N+M, R3=N2+O->NO+N. Each forward event destroys one N2.
forw=np.einsum('i,rit->rt',mu,fr);rev=np.einsum('i,rit->rt',mu,br);g=2*(forw[0]+forw[2]);aN0=float(np.dot(mu,Y[2,:,0])/(K.W[2]/1000));integ=float(np.trapezoid(g,t));rows=[]
for tt in [0,10e-6,25e-6,50e-6,70e-6,110e-6,150e-6]:
 j=int(np.argmin(abs(t-tt)));rows.append({'time_s':float(t[j]),'gross_N2_dissociation_mol_kgfresh_s':float(forw[0,j]),'gross_N2_O_exchange_mol_kgfresh_s':float(forw[2,j]),'reverse_N2_O_exchange_mol_kgfresh_s':float(rev[2,j]),'twice_gross_N2_destruction_mol_kgfresh_s':float(g[j])})
# Independent cap coefficient from source NASA at1700K, no borrowed displayed quotient.
cp,h,ss=K.thermochemistry(np.array([1700.]));hm=h[:,0]*K.R*1700/1000;a=float(hm[4]-(hm[0]+hm[1])/2)
cert=json.load(open(R/'nitrogen_lamella_20261022/exact_endpoint_certificate.json'));loss=next(v['float_for_display_J_kg_fresh'] for v in cert['rows'] if v['contract']=='enthalpy_isobaric' and v['NOx_cap_factor']=='1' and v['O_radical_cap_mol_per_kg_fresh']=='3/1000');needed=loss/a
out={'scope':__doc__,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'raw_saved_min_Y':float(rawmin),'coefficient_composition_policy':'negative roundoff clipped and unit sum restored only for this positive reaction diagnostic','last_time_s':float(t[-1]),'trapezoid_twice_gross_N2_destruction_mol_kgfresh':integ,'initial_atomic_N_mol_kgfresh':aN0,'conditional_NOx_creation_envelope_mol_kgfresh':integ+aN0,'extra_NOx_needed_for_zero_export_relaxed_1700_cap_mol_kgfresh':needed,'ratio_needed_to_thermal_gross_plus_N_inventory':needed/(integ+aN0),'NO_increment_enthalpy_coefficient_J_mol':a,'point_rows':rows,'limits':['Thermal path is already known to be physically unqualified during rapid cooling.','No rigorous quadrature or unsampled-time error bound; this is a diagnostic threshold.','Changed mode kinetics changes temperatures, concentrations, rates and trajectory; ratio is not a universal required enhancement.','Initial atomic N counted favorably; reversible turnover and later loss discarded in upper envelope.','Relaxes old NOx cap to ask how much NEW NOx could store the recombination energy; not the retention-only contract.','No pump, heater, product or full-cycle advantage follows.'],'elapsed_s':time.monotonic()-T0,'RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
(D/'saved_flux_diagnostic.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
