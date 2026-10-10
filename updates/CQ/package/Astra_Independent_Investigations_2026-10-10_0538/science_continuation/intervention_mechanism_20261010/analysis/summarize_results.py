import sys,pathlib,json
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'python_packages'))
import numpy as np,pandas as pd
from scipy.stats import poisson
all=[]
for split in ['discovery','validation']:
 d=pd.read_csv(ROOT/f'results/{split}_off_memory.csv');all.append(d)
d=pd.concat(all,ignore_index=True);out=[]
for (split,frac,guard),a in d.groupby(['split','frac','guard']):
 pulse=a[a.group.str.contains('03_')];last=pulse.groupby(['cell','file']).tail(1)
 resolved=last[(last.category=='resolved_off')&(last.pulse>0)]
 risk=pulse[pulse.pulse>0];exposure=float((risk.exposure_early+risk.exposure_late).sum())
 base=a[a.group.str.contains('01_Without')];nbase=base.onset.notna().sum();tb=float((base.onset.fillna(base.end-base.start-.2)-guard).clip(lower=0).sum())
 out.append(dict(split=split,frac=frac,guard=guard,pulse_traces=len(last),pulse_unique_cells=last.cell.nunique(),resolved_postpulse=len(resolved),immediate_or_unresolved=int((last.category=='immediate_or_unresolved').sum()),ambiguous=int((last.category=='ambiguous').sum()),baseline_before_firstpulse=int(((last.category=='resolved_off')&(last.pulse==0)).sum()),at_risk_off_exposure_seconds=exposure,baseline_events=int(nbase),baseline_exposure_seconds=tb,baseline_observed_rate=nbase/tb,expected_off_events_at_baseline=exposure*nbase/tb,poisson_survival_descriptive=float(poisson.sf(len(resolved)-1,exposure*nbase/tb))))
s=pd.DataFrame(out);s.to_csv(ROOT/'results/summary.csv',index=False);print(s.to_string(index=False));(ROOT/'results/summary.json').write_text(s.to_json(orient='records',indent=2))
manifest=pd.read_csv(ROOT/'raw/selected_manifest.csv');print('selected',len(manifest),'unique cells',manifest.cell.nunique(),'splits',manifest.groupby('split').cell.nunique().to_dict());assert set(manifest[manifest.split=='discovery'].cell).isdisjoint(set(manifest[manifest.split=='validation'].cell))
