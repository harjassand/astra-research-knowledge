"""Read-only current-checkpoint receipt. No integration or physical acceptance."""
from pathlib import Path
import json,hashlib,time,resource
import numpy as np
R=Path(__file__).resolve().parent;t0=time.monotonic();p=R/'heater_H4_signed_N24_T11_blow_10.npz';z=np.load(p);N=int(z['N']);H=int(z['NH']);M=2*N+H;dx=.1/N;v=np.full(M,.4*dx);v[N:N+H]=.1/H;s=z['state'];a=s[:,0];b=s[:,-1];nc=9

def inv(y):
 q=y[:6*M].reshape(6,M);return {'mass':float(np.sum(q@v)),'energy_MJ':float(np.dot(v,y[6*M:7*M])+2.5e6*dx*1000*np.sum(y[7*M:7*M+2*N])/1e6)}
ia,ib=inv(a),inv(b);d=b[-nc:]-a[-nc:];er=ib['energy_MJ']-ia['energy_MJ']-d[0]+d[1]-d[2]+d[3];mr=ib['mass']-ia['mass']-d[4]
q=b[:6*M].reshape(6,M);W=np.array([28.014,31.998,14.007,15.999,30.006,46.005]);ph=8314.46261815324*2700*np.sum(q[:,N:N+H]/W[:,None],axis=0)
out={'scope':__doc__,'source':p.name,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'N':N,'NH':H,'interval_s':[float(z['t'][0]),float(z['t'][-1])],'incremental_energy_residual_MJ_m2':er,'incremental_mass_residual_kg_m2':mr,'header_pressure_spread_Pa':float(np.ptp(ph)),'NOx_export_mol_m2':float(d[5]),'heater_positive_MJ_m2':float(d[0]),'observed_quotient_MJ_mol':float(d[0]/d[5]),'min_saved_rho_species_kg_m3':float(s[:6*M].min()),'ledger_check_pass':abs(er)<1e-6 and abs(mr)<1e-7,'complete_cycle_or_capability_admitted':False,'reason':'One blow only; no periodic reset or asymptotic discretization convergence. Unqualified transport, surfaces, actuation/capture and campaign boundary remain.','wall_s':time.monotonic()-t0,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};print(json.dumps(out,indent=2))
if not out['ledger_check_pass']:raise SystemExit(1)
