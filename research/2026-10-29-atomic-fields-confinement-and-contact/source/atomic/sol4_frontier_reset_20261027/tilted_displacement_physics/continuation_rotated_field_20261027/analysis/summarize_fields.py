from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
prefixes=['oblique_768_analytic_finite_dz1','onaxis_768_analytic_finite_dz1','oblique_768_vacuum_dz1','oblique_896_large_finite_dz1','oblique_1024_finite_dz05']
data={p:json.loads((ROOT/'outputs'/f'{p}.json').read_text()) for p in prefixes}
def row(prefix,controller,metric='point_bilinear'):
 return next(m for q in data[prefix]['results'] if q['controller']==controller for m in q['metrics'] if m['metric']==metric)
base=prefixes[0];on=prefixes[1];fine=prefixes[-1];names=['ideal32','coherent08','incoherent08'];comparison=[];trade=[];gain=[]
for model in names:
 for metric in ['point_bilinear','disk_r02','disk_r04']:
  ob=row(base,'parked_'+model,metric);ref=row(on,'parked_'+model,metric);src=row(on,'plus_b_'+model,metric);fi=row(fine,'parked_'+model,metric)
  gain.append(dict(model=model,metric=metric,oblique_over_source_scan_target_fluence=ob['target_density_per_e_per_A2']/src['target_density_per_e_per_A2'],oblique_over_source_scan_Cr_fraction=ob['target_over_all_Cr']/src['target_over_all_Cr'],refined_oblique_fraction=fi['target_over_all_Cr']))
  vals={}
  for label,r in [('onaxis_parked',ref),('source_scan',src),('oblique',ob)]:
   I=r['target_density_per_e_per_A2'];vals[label]=dict(other_Cr=r['species_density_sums']['Cr']/I-1,S=r['species_density_sums']['S']/I,Br=r['species_density_sums']['Br']/I)
  d={s:vals['oblique'][s]-vals['onaxis_parked'][s] for s in ['other_Cr','S','Br']};threshold=-d['other_Cr']/(d['S']+d['Br'])
  trade.append(dict(model=model,metric=metric,fluence_per_unit_target=vals,oblique_minus_onaxis_parked=d,equal_S_Br_relative_weight_crossover=threshold,interpretation='A conditional linear weighted-fluence frontier, not an acquired hazard or damage coefficient.'))
for p,d in data.items():
 for q in d['results']:
  for m in q['metrics']:comparison.append(dict(run=p,controller=q['controller'],metric=m['metric'],fraction=m['target_over_all_Cr'],target_density_per_e_per_A2=m['target_density_per_e_per_A2'],species_sums=m['species_density_sums']))
convergence=[]
for model in names:
 for metric in ['point_bilinear','disk_r02','disk_r04']:
  b=row(base,'parked_'+model,metric);r=row(prefixes[3],'parked_'+model,metric);f=row(fine,'parked_'+model,metric)
  convergence.append(dict(model=model,metric=metric,base=b['target_over_all_Cr'],larger=r['target_over_all_Cr'],refined=f['target_over_all_Cr'],larger_relative_fraction_change=r['target_over_all_Cr']/b['target_over_all_Cr']-1,refined_relative_fraction_change=f['target_over_all_Cr']/b['target_over_all_Cr']-1,refined_relative_target_density_change=f['target_density_per_e_per_A2']/b['target_density_per_e_per_A2']-1))
manifest=[]
for p in [ROOT.parent/'REPORT.md',ROOT.parents[1]/'empirical_operation_invention/sources/CrSBr.cif',ROOT.parents[1]/'empirical_operation_invention/.venv/lib/python3.12/site-packages/abtem/multislice.py',ROOT.parents[1]/'empirical_operation_invention/.venv/lib/python3.12/site-packages/abtem/potentials/iam.py',ROOT.parents[1]/'empirical_operation_invention/.venv/lib/python3.12/site-packages/abtem/integrals.py']:
 manifest.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
resources={p:dict(seconds=d['elapsed_seconds'],atoms=d['atoms'],grid=d['args']['gpts'],slices=d['slices'],modes=sum(q['coherent_modes'] for q in d['controllers']),peak_resident_memory_bytes=d.get('peak_resident_memory_bytes')) for p,d in data.items()}
frozen=json.loads((ROOT.parent/'outputs/artifact_manifest.json').read_text());oldsha=next(q['sha256'] for q in frozen if q['path']=='REPORT.md');newsha=hashlib.sha256((ROOT.parent/'REPORT.md').read_bytes()).hexdigest();assert oldsha==newsha
output=dict(accepted_preceding_report_unchanged=True,accepted_preceding_report_sha256=newsha,status='COMPUTATIONAL_FLUENCE_ADVANTAGE_ONLY',transition_capability='NOT_ACHIEVED',comparison=comparison,gains=gain,weighted_fluence_tradeoffs=trade,convergence=convergence,resources=resources,total_main_propagation_seconds=sum(q['seconds'] for q in resources.values()),source_manifest=manifest,limits=['Static neutral-atom IAM, no thermal ensemble or changed defect potential','Nominal-site point and disk measurements are upstream slice-plane diagnostics','Actual nuclear-position and reactive transition kernels not acquired','No measured layer hazard, retained write, all-species damage rate or reset inferred'])
(ROOT/'outputs/COMPARISON.json').write_text(json.dumps(output,indent=2))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,2,figsize=(13,9));colors=['#225ea8','#d95f0e','#6a3d9a'];probe_labels=['Ideal 32 mrad','Coherent 0.8 A','Incoherent 0.8 A'];controllers=[(on,'parked_','On-axis parked'),(on,'plus_b_','Source +b scan'),(base,'parked_','Oblique parked')];x=np.arange(3);w=.24
for j,(model,color,label) in enumerate(zip(names,colors,probe_labels)):
 vals=[row(p,c+model)['target_over_all_Cr'] for p,c,_ in controllers];absvals=[row(p,c+model)['target_density_per_e_per_A2'] for p,c,_ in controllers]
 axs[0,0].bar(x+(j-1)*w,vals,w,color=color,label=label);axs[0,1].bar(x+(j-1)*w,absvals,w,color=color)
axs[0,0].set(xticks=x,xticklabels=[c[2] for c in controllers],ylabel='Target / all Cr nominal-site intensity',ylim=(0,1));axs[0,0].legend(frameon=False,fontsize=9)
axs[0,1].set(xticks=x,xticklabels=[c[2] for c in controllers],ylabel='Target point intensity per incident electron (1/A^2)')
for model,color,label in zip(names,colors,probe_labels):
 yy=[row(p,'parked_'+model)['target_over_all_Cr'] for p in [prefixes[2],base,prefixes[3],fine]];axs[1,0].plot(range(4),yy,'o-',color=color,label=label)
axs[1,0].set(xticks=range(4),xticklabels=['Vacuum','IAM base','Larger crystal','Finer grid/slices'],ylabel='Oblique nominal-site fraction',ylim=(0,1))
t=next(q for q in trade if q['model']=='incoherent08' and q['metric']=='point_bilinear')
for j,(s,color) in enumerate(zip(['other_Cr','S','Br'],['#225ea8','#999','#d95f0e'])):
 vals=[t['fluence_per_unit_target'][key][s] for key in ['onaxis_parked','source_scan','oblique']];axs[1,1].bar(x+(j-1)*w,vals,w,color=color,label=s.replace('_',' '))
axs[1,1].set(xticks=x,xticklabels=[c[2] for c in controllers],ylabel='Non-target site-intensity sum / target intensity');axs[1,1].legend(frameon=False,fontsize=9)
fig.suptitle('Incoming fluence in static native CrSBr: matched beams and explicit collateral',fontsize=14)
fig.text(.5,.015,'Nominal-site intensity is sampled before each atom-containing slice. Point and disk kernels are diagnostics; no write probability is inferred.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.04,1,.95]);fig.savefig(ROOT/'outputs/field_comparison.png',dpi=180);fig.savefig(ROOT/'outputs/field_comparison.pdf');plt.close(fig)
print(json.dumps(dict(resources=resources,gains=gain,convergence=convergence,tradeoffs=trade),indent=2))
