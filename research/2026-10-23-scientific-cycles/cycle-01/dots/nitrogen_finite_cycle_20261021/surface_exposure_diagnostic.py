"""Frozen-trajectory Maxwellian NOx collision exposure, not a surface-rate bound.
Gamma denotes net fixed-N destruction per incident NOx molecule, NOT adsorption,
NO-to-NO2 conversion or mere NO disappearance. No measured zirconia gamma supplied.
"""
import sys,time,json,resource,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import simpson
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R));import reacting_heater_signed as m
p=R/'heater_H4_signed_T11_blow_10.npz';z=np.load(p);t=z['t'];s=z['state'];vals=[];negative=0;start=time.monotonic();area_density=6*(1-m.por)/m.dp
for v in s.T:
 q,rho,U,r=m.props(v);den=q[np.ix_([4,5],m.ids)];negative+=int(np.count_nonzero(den<0));c=np.maximum(den,0)/(m.K.W[[4,5],None]/1000)
 speed=np.sqrt(8.31446261815324*r['T'][m.ids]/(2*np.pi*(m.K.W[[4,5],None]/1000)))
 vals.append(float(np.sum(c*speed)*area_density*m.dx))
I=float(np.trapezoid(vals,t));Is=float(simpson(vals,x=t));n=float(s[-m.nc+5,-1]-s[-m.nc+5,0]);ratio=I/n
out={'scope':__doc__,'source_file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'interval_s':[float(t[0]),float(t[-1])],'two_bed_surface_area_m2_per_m2_bed_crosssection':2*area_density*.1,'integrated_NOx_collision_mol_m2':I,'simpson_collision_mol_m2':Is,'quadrature_difference_relative':abs(I-Is)/I,'net_export_NOx_mol_m2':n,'incident_NOx_collisions_per_net_export_molecule':ratio,'frozen_first_order_gamma_for_5percent_change':.05/ratio,'frozen_first_order_gamma_for_1percent_change':.01/ratio,'negative_NOx_density_entries_clipped_only_in_postprocessing':negative,'missing':['No measured dryair zirconia net fixed-N destruction rate','No surface coverage/storage or catalytic gas feedback','No heater/header surfaces','Not a complete periodic trajectory or rigorous loss/error bound'],'wall_s':time.monotonic()-start,'rss_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss};(R/'surface_exposure_diagnostic.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
