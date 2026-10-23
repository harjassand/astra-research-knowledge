"""Timescale-only closure diagnostic. No new ODE or mode-resolved trajectory.
The additive VT+VV screen pins VV acceptors to equilibrium as ideal sinks;
it is not a six-species mixture relaxation eigenvalue or exclusion bound.
"""
from pathlib import Path
import numpy as np,json,csv
D=Path(__file__).resolve().parent
f=D.parent/'restored_cross_width400um_N48_trajectory.npz'
d=np.load(f);N=int(d['N']);t=d['t'];s=d['state'];mu=d['mu'];Mhot=float(d['hot_mass_per_area'])
Y5=s[:5*N].reshape(5,N,-1);Y=np.concatenate([(1-Y5.sum(0))[None],Y5]);T=s[5*N:];W=np.array([28.0134,31.998,14.0067,15.999,30.0061,46.0055]);names=['N2','O2','N','O','NO','NO2'];X=Y/W[:,None,None];X/=X.sum(0)
P=101325.
# Park 1993 coefficients, reproduced by Jans et al SAND2025-12571J Appendix A.
A=np.array([221,229,180,72.4,225.]);B=np.array([.029,.0295,.0262,.015,.0293]);
# Product p*tau in atm s. These are VT parameters, not complete-mixture rates.
ptau=np.exp(A[:,None,None]*(T[None]**(-1/3)-B[:,None,None])-18.42)
rate=X[:5]/ptau # at 1 atm
# Jans et al updated fits to VV theory/measurements; Eq A2, Pa s.
ptau_O2=3.158e7*T**(-2.17)+1.31e-10
ptau_NO=1.644e5*T**(-1.82)+1.17e-11
ptau_NO_new=2.750e5*T**(-2.21)+2.568e2*T**(-.75)+.381
vvo2=P*X[1]/ptau_O2;vvno=P*X[4]/ptau_NO;vvno_new=P*X[4]/ptau_NO_new
vt=rate.sum(0)
combined_old=vt+vvo2+vvno;combined_new=vt+vvo2+vvno_new
# Compare pure nitrogen primary empirical fit as independent checkpoint.
primary_NN=10**(102*T**(-1/3)-11.24)
rows=[];ci=N//2
for target in [0,10e-6,25e-6,50e-6,80e-6,110e-6,.001]:
 j=int(np.argmin(abs(t-target)));temp=T[ci,j];pO=X[3,ci,j]
 r={'t_us':t[j]*1e6,'center_T_K':temp,'center_xO':pO,'center_xNO':X[4,ci,j],'center_xNO2':X[5,ci,j], 'pure_N2_MW_us':ptau[0,ci,j]*1e6,'pure_N2_primary_1963_us':primary_NN[ci,j]*1e6,'N2O_MW_partial_us':1e6/rate[3,ci,j],'N2O_measured_envelope_fast_us':.4/pO,'N2O_measured_envelope_slow_us':3./pO,'N2_total_VT_screen_us':1e6/vt[ci,j],'N2O2_VV_model_us':1e6/vvo2[ci,j],'N2NO_VV_older_model_us':1e6/vvno[ci,j],'N2NO_VV_2022_model_us':1e6/vvno_new[ci,j],'additive_VT_VV_old_NO_screen_us':1e6/combined_old[ci,j],'additive_VT_VV_new_NO_screen_us':1e6/combined_new[ci,j]}
 rows.append(r)
with (D/'center_timescale_table.csv').open('w') as ff:
 w=csv.DictWriter(ff,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
# The cooling e-folding timescale of equilibrium N2 vibrational energy.
R=8.314462618;theta=3395.;ev=R*theta/np.expm1(theta/T);cv=R*(theta/T)**2*np.exp(theta/T)/np.expm1(theta/T)**2
Tdot=np.gradient(T[ci],t);evdot=cv[ci]*Tdot
te=np.divide(ev[ci],abs(evdot),out=np.full_like(t,np.inf),where=abs(evdot)>0)
thermal={}
for target in [5e-6,10e-6,15e-6,25e-6,50e-6]:
 j=int(np.argmin(abs(t-target)));thermal[str(target)]={'t_us':t[j]*1e6,'T_K':T[ci,j],'dTdt_K_s':Tdot[j],'equilibrium_N2_energy_change_time_us':te[j]*1e6,'vt_vv_fast_screen_us':1e6/combined_old[ci,j],'ratio_screen_to_energy_change_time':1/(combined_old[ci,j]*te[j])}
# Frozen global N2 vibrational inventory compares energy, not parcel Tv. It
# remains unchanged under internal diffusion, unlike a parcel-only lag model.
Nmol=mu[:,None]*Y[0]/(W[0]/1000)/Mhot # mol per kg fresh, each cell
N2_Ev=(Nmol*ev).sum(0)
j50=int(np.argmin(abs(t-50e-6)))
out={'scope':__doc__,'trajectory':str(f),'pressure_Pa':P,'source_parameters':{'VT':'Park 1993, DOI 10.2514/3.431, as reproduced in Jans et al SAND2025-12571J App A Table A1','VV':'Jans et al SAND2025-12571J Eq A2 and Table A2. Older/fast NO fit and Streicher2022 alternative. All p*tau units Pa s, partial-pressure scaling used.','N2_N2_primary':'Millikan & White 1963 DOI 10.1063/1.1734039, 1900-5400 K. Values below1900 extrapolated.','N2_O_measurement':'Eckstrom1973 DOI 10.1063/1.1680410,1200-3000 K,p*tau0.8-2atm us ±50%. Broad entire-domain envelope0.4-3atm us, not temperature-resolved confidence interval.'},'timescales':rows,'thermal_timescale':thermal,'initial_center_heater_13ms_over_vt_time':.013*vt[ci,0], 'initial_center_heater_13ms_over_pure_N2_primary_time':.013/primary_NN[ci,0],'initial_global_N2_Ev_J_per_kg_fresh':N2_Ev[0],'eq_global_N2_Ev_near50us_J_per_kg_fresh':N2_Ev[j50],'difference_J_per_kg_fresh':N2_Ev[0]-N2_Ev[j50], 'critical_limitations':['No mode-resolved ODE/PDE integrated; no prediction of actual Tv or minimum T.','VV transfers energy into finite O2 and NO reservoirs and cannot simply be counted as independent VT losses. Additive rates are closure screens only.','The 2025 correlations do not state a formal low-temperature validity interval in their Appendix; any usage is illustrative, not a validated rigorous bound.','The 2022 NO experiments start at1900K; using that fit near1700K is extrapolation.','At <1900K pure-N2 1963 empirical measurement fit is extrapolated; Park/MW also empirical.','Eckstrom N2O1200-3000K covers hot cooling branch but not cold300K reservoir.','N2–NO2 energy-transfer data were not located for1700-2700K. It cannot silently be set to zero in a rigorous six-species rate bound.','Vibrational-mode conduction, species diffusion carrying internal energy, chemical production partition and non-Boltzmann distributions are not included here.','Does not alter the conserved fully equilibrated endpoint energy bound.']}
(D/'relaxation_diagnostic.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
