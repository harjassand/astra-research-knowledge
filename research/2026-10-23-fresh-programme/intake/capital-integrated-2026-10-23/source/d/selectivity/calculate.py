import json,math,time,resource,hashlib
from pathlib import Path
start=time.perf_counter();p=Path(__file__).with_name('inputs.json');d=json.loads(p.read_text());T=d['temperature_K'];R=d['R_J_mol_K'];fit=d['LiFeO2_Gf_fit_kJ_mol'];g=d['JANAF_1000K_Gf_kJ_mol'];s=d['silicate_carbonation_J_mol'];assert fit['range_K'][0]<=T<=fit['range_K'][1] and T>993.15
Gf=fit['intercept']+fit['slope_per_K']*T
DG_F=1000*(2*Gf+g['CO2_gas']-g['Fe2O3_cr']-g['Li2CO3_liquid'])
DG_S=s['solid_carbonate_intercept']+s['solid_carbonate_slope']*T+s['fusion_intercept']+s['fusion_slope']*T
pF=math.exp(-DG_F/(R*T));pS=d['bar_per_atm']*math.exp(DG_S/(R*T));ratio=pS/pF
# All atoms balance for the written reactions.
formula={'LiFeO2':{'Li':1,'Fe':1,'O':2},'Fe2O3':{'Fe':2,'O':3},'Li2CO3':{'Li':2,'C':1,'O':3},'CO2':{'C':1,'O':2},'Li2Si2O5':{'Li':2,'Si':2,'O':5},'SiO2':{'Si':1,'O':2}}
for sto in [{'LiFeO2':2,'CO2':1,'Fe2O3':-1,'Li2CO3':-1},{'SiO2':2,'Li2CO3':1,'Li2Si2O5':-1,'CO2':-1}]:
 for el in ['Li','Fe','C','O','Si']:assert sum(v*formula[k].get(el,0) for k,v in sto.items())==0
out={'input_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'T_K':T,'LiFeO2_Gf_kJ_mol':Gf,'ferrite_formation_DG_J_mol':DG_F,'disilicate_carbonation_DG_J_mol':DG_S,'ferrite_retention_upper_CO2_bar_unit_activities':pF,'silicate_carbonation_lower_CO2_bar_unit_activities':pS,'no_unit_activity_equilibrium_pressure_window':pF<pS,'required_activity_selectivity_ratio':ratio,'ferrite_activity_threshold_at_silicate_boundary_other_activities_unity':1/math.sqrt(ratio),'ferrite_activity_threshold_at_20bar_other_activities_unity':math.sqrt(pF/20),'ferrite_pressure_interval_from_reported_fit_plus_minus_only':[math.exp(-(DG_F+6000)/(R*T)),math.exp(-(DG_F-6000)/(R*T))],'seconds':time.perf_counter()-start,'peak_RSS_KiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'Pure-phase/reference-activity discriminator, not a molten-ore process exclusion or a complete uncertainty interval.'}
Path(__file__).with_name('results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
