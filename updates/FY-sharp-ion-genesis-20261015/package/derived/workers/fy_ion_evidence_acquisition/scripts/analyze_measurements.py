"""Reproducible analysis of primary publisher source-data values.

No new experiments, species reconstruction, thermal corrections, or kinetic fits
are implied. Conductance-to-inventory calculations are explicitly conditional.
"""
import csv
import json
import math
import pathlib
import statistics
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'analysis/local_plot_dependencies'))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PRIVATE = ROOT/'analysis/private_extractions'
OUT = ROOT/'analysis'

def sheet(file, name):
    b = json.loads((PRIVATE/file).read_text())
    return next(s for s in b['sheets'] if s['name']==name)['cells']

def column_pairs(c, xcol, ycol):
    out=[]
    for k,v in c.items():
        if k.startswith(xcol) and k[len(xcol):].isdigit() and isinstance(v['v'],(float,int)):
            row=int(k[len(xcol):])
            y=c.get(ycol+str(row),{}).get('v')
            if isinstance(y,(float,int)):
                out.append((row,v['v'],y))
    return sorted(out)

c=sheet('kautz_source_data_fig4_cells.json','Fig4b')
ed=column_pairs(c,'A','B')
ref=column_pairs(c,'C','D')
voltage=column_pairs(c,'E','F')
assert len(ed)==len(ref)==354 and len(voltage)==42877
assert [t for r,t,y in ed]==[t for r,t,y in ref]
minimum=min(ed,key=lambda p:p[2])
gaps=[{'after_row':a[0],'before_row':b[0],'start_hours':a[1],'end_hours':b[1],'duration_hours':b[1]-a[1]} for a,b in zip(ed[:-1],ed[1:]) if b[1]-a[1]>1]
row,tmin,gmin=minimum
ref_min=c['D'+str(row)]['v']
n0=1e-3*0.63e-3
nremoved=n0*(1-gmin)
crossings=[]
for left,right in zip(ed[:-1],ed[1:]):
    if left[2]>0.5>=right[2]:
        t=left[1]+(0.5-left[2])*(right[1]-left[1])/(right[2]-left[2])
        crossings.append({'left_cell':'B'+str(left[0]),'right_cell':'B'+str(right[0]),'linear_interpolation_hours':t})

slopes=[]
# Descriptive interior intervals chosen from source ON/OFF plot, not a fitted
# switch schedule. No pump-on timing or inferential confidence intervals.
for lo,hi,label in [(13,18,'ON interior'),(22,26,'ON interior'),(31,36,'ON interior'),(45,54,'OFF recovery interior')]:
    p=[x for x in ed if lo<=x[1]<=hi]
    x=np.array([x[1] for x in p]); y=np.array([x[2] for x in p])
    m,b=np.polyfit(x,y,1)
    slopes.append({'range_hours':[lo,hi],'source_state_interpretation':label,'n':len(p),'first_cell':'B'+str(p[0][0]),'last_cell':'B'+str(p[-1][0]),'normalized_conductance_per_hour':float(m),'conditional_kcl_removal_nmol_per_hour':float(-m*n0*1e9),'residual_rms':float(np.sqrt(np.mean((y-m*x-b)**2)))})

vc=sheet('kautz_source_data_fig3_cells.json','Fig3a')
jc=sheet('kautz_source_data_fig3_cells.json','Fig3b')
assert vc['M7']['v']==jc['M7']['v']==0.5
voc=vc['N7']['v']*1e-3
jsc=jc['N7']['v']*1e-6
area=0.32
isc=jsc*area
pin=0.215e-3
pmax=abs(voc*isc)/4
eff={'source_voltage_cell':'Fig3a!N7','source_current_density_cell':'Fig3b!N7','frequency_Hz':250,'duty_cycle':0.5,'electrolyte':'1 mM HCl','contacts':'Au-Au','active_area_cm2':area,'Voc_V':voc,'Jsc_A_per_cm2':jsc,'Isc_A':isc,'reported_input_power_W':pin,'maximum_matched_linear_load_power_W':pmax,'efficiency':pmax/pin,'reported_efficiency':1.96e-5,'scope':'maximum electrical output to a matched linear load; not measured ED separation free-energy efficiency'}

kc=sheet('kong_source_data_cells.json','Fig.5a')
ph=sheet('kong_source_data_cells.json','Fig.S9')
purities=[]
for r in range(3,16):
    li=kc['B'+str(r)]['v']; cl=kc['D'+str(r)]['v']; oh=kc['F'+str(r)]['v']
    purities.append({'row':r,'time_min':kc['A'+str(r)]['v'],'Li_mM':li,'Cl_mM':cl,'OH_mM':oh,'pH':ph['B'+str(r)]['v'],'purity_percent_from_equation6':100*oh/(oh+cl),'charge_residual_mM':li-cl-oh,'OH_mM_from_pH_assuming_pKw14':10**(ph['B'+str(r)]['v']-14)*1000})
costc=sheet('kong_source_data_cells.json','Fig.6b')
costs=[{'row':r,'assumed_electrode_lifespan':costc['A'+str(r)]['v'],'sum_B_to_G_USD_per_kg_LiOH_H2O':sum(costc[x+str(r)]['v'] for x in 'BCDEFG')} for r in [3,4,5]]

results={
 'analysis_scope':'Read-only source-data reanalysis; no new physical validation, no species-flux reconstruction, no lithium data from ratchets.',
 'kautz_ED':{
  'sheet':'Fig4b','conductance_points_per_cell':len(ed),'voltage_points':len(voltage),'time_range_hours':[ed[0][1],ed[-1][1]],
  'minimum':{'time_cell':'A'+str(row),'conductance_cell':'B'+str(row),'time_hours':tmin,'G_over_G0':gmin,'reference_cell':'D'+str(row),'reference_G_over_G0':ref_min,'ED_divided_by_reference':gmin/ref_min},
  'reference_range_to_min':[min(p[2] for p in ref if p[1]<=tmin),max(p[2] for p in ref if p[1]<=tmin)],
  'reference_full_range':[min(p[2] for p in ref),max(p[2] for p in ref)],
  'conditional_inventory':{'assumptions':['constant volume','KCl remains the only conductivity-relevant electrolyte','concentration proportional to normalized conductance','no uptake, leakage, contaminant, or solvent correction supplied'],'initial_mol_KCl':n0,'removed_mol_at_min':nremoved,'removed_umol_at_min':nremoved*1e6,'average_removed_nmol_per_elapsed_hour':nremoved*1e9/tmin,'average_removed_mol_per_m2_per_s':nremoved/(tmin*3600)/(0.16e-4),'50_percent_at_37h_umol':n0*0.5*1e6,'50_percent_at_37h_nmol_per_elapsed_hour':n0*0.5*1e9/37},
  'first_downward_half_crossing':crossings[0],
  'end':{'time_cell':'A356','conductance_cell':'B356','time_hours':ed[-1][1],'G_over_G0':ed[-1][2],'reference_G_over_G0':ref[-1][2],'conditional_remaining_depletion_nmol':n0*(1-ed[-1][2])*1e9,'fraction_of_maximum_depletion_recovered':(ed[-1][2]-gmin)/(1-gmin)},
  'descriptive_interval_slopes':slopes,
  'conductance_sampling_gaps_over_1h':gaps,
  'no_direct_pump_on_time':'source-data workbook has no ON/OFF state column; none reconstructed from output voltage',
 },
 'kautz_HCl_efficiency':eff,
 'grossman_peak_electrical_conversion':{'reported_J_uA_per_cm2':-5.17,'area_cm2':0.159,'current_uA':-5.17*0.159,'F_C_per_mol':96485.33212,'charge_equivalent_nmol_per_hour':abs(-5.17*.159)*1e-6/96485.33212*3600*1e9,'scope':'charge-imbalance equivalent only; cannot identify K, Cl, Li, Na flux or separation throughput'},
 'kong':{'source_rows':purities,'unweighted_mean_purity_percent':statistics.mean(p['purity_percent_from_equation6'] for p in purities),'sample_SD_across_timepoints_percent':statistics.stdev(p['purity_percent_from_equation6'] for p in purities),'range_percent':[min(p['purity_percent_from_equation6'] for p in purities),max(p['purity_percent_from_equation6'] for p in purities)],'reported_purity_percent':99.6,'reported_uncertainty_percent':0.2,'purity_boundary':'averaged figure source values are not underlying replicates; temporal SD is not measurement uncertainty; equation counts OH versus Cl, not all dry-solid impurities','cost_sums':costs}
}
(OUT/'MEASUREMENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
with (OUT/'kautz_deionization_derived.csv').open('w',newline='') as f:
    w=csv.writer(f); w.writerow(['source_row','time_h','dilution_G_G0','reference_G_G0','conditional_depletion_nmol_KCl'])
    for (r,t,g),(rr,tr,gr) in zip(ed,ref): w.writerow([r,t,g,gr,(1-g)*n0*1e9])
with (OUT/'kong_purity_recalculation.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(purities[0]));w.writeheader();w.writerows(purities)

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
def plot_gap_aware(ax, points, *args, **kwargs):
    x=[];y=[]
    for i,(_,t,v) in enumerate(points):
        if i and t-points[i-1][1]>1:
            x.append(float('nan'));y.append(float('nan'))
        x.append(t);y.append(v)
    ax.plot(x,y,*args,**kwargs)
fig,(ax,ax2)=plt.subplots(2,1,figsize=(9.4,6.4),sharex=True,gridspec_kw={'height_ratios':[2.0,1.1]})
plot_gap_aware(ax,ed,'.-',markersize=3,lw=1,color='#2166ac',label='Dilution cell')
plot_gap_aware(ax,ref,'-',lw=1,color='#d95f02',label='Reference cell')
ax.scatter([tmin],[gmin],color='black',zorder=4)
ax.annotate(f'Minimum {gmin:.4f} at {tmin:.3f} h',(tmin,gmin),xytext=(47,.66),arrowprops={'arrowstyle':'->','lw':.8})
ax.set_ylabel('Conductance / initial conductance');ax.legend(frameon=False,loc='upper right');ax.grid(alpha=.2)
plot_gap_aware(ax2,voltage,color='#444444',lw=.7)
for a in [ax,ax2]: a.axvspan(58.22870633388889,71.74454940388888,color='#cccccc',alpha=.2)
ax.text(64.9,.75,'No source\nsamples',ha='center',fontsize=9,color='#555555')
ax2.set_ylabel('RBIP output voltage (mV)');ax2.set_xlabel('Elapsed time (h)');ax2.grid(alpha=.2)
fig.suptitle('Kautz publisher source data, Fig. 4b',x=.1,ha='left',weight='bold')
fig.text(.1,.01,'Normalized conductance is measured. KCl inventory conversion is conditional; Li/Na flux is unmeasured.',fontsize=9)
fig.tight_layout(rect=[0,.035,1,.96]);fig.savefig(OUT/'kautz_deionization_reanalysis.png',dpi=180);plt.close(fig)
print(json.dumps({k:v for k,v in results.items() if k!='kong'},indent=2))
print(json.dumps({k:v for k,v in results['kong'].items() if k!='source_rows'},indent=2))
