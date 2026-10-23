"""Audit published SI tables only. No chemistry/flow trajectories.
Each printed measurement is retained unchanged; derived EC follows main-paper Eq.2.
"""
from pathlib import Path
import json,re,hashlib,statistics
P=Path(__file__).resolve().parent
source=P/'2022_effusion_si.txt';t=source.read_text(); rows=[];table=None; runs={}
for line in t.splitlines():
    if line.startswith('Table S.') and 'Total flow' in line:
        table=line.split('.')[1].strip()
    if line.startswith('S.2.1 Diagnostic'): break
    m=re.search(r'(20/80|40/60|50/50|60/40|70/30|80/20)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)',line)
    if not m: continue
    mix,q,i,p,no,no2,ec=m.groups();q,i,p,no,no2,ec=map(float,[q,i,p,no,no2,ec])
    key=(table,mix);runs[key]=runs.get(key,0)+1
    calc=p*24*60*100/(q*(no+no2))*1e-6
    rows.append(dict(table=table,replicate=runs[key],mix=mix,flow_Lmin=q,current_mA=i,power_W=p,NO_percent=no,NO2_percent=no2,reported_EC_MJmol=ec,recomputed_EC_MJmol=calc,relative_difference=ec/calc-1))
assert len(rows)==72
(P/'2022_effusion_table_audit.json').write_text(json.dumps(rows,indent=2))
groups=[]
for table in ['1','2','3','4']:
 for mix in ['20/80','40/60','50/50','60/40','70/30','80/20']:
  r=[x for x in rows if x['table']==table and x['mix']==mix]
  p=statistics.mean(x['power_W'] for x in r);no=statistics.mean(x['NO_percent'] for x in r);no2=statistics.mean(x['NO2_percent'] for x in r);q=r[0]['flow_Lmin']
  groups.append(dict(table=table,mix=mix,n=len(r),mean_power_W=p,mean_NO_percent=no,mean_NO2_percent=no2,mean_NOx_percent=no+no2,recomputed_EC_from_means_MJmol=p*24*60*100/(q*(no+no2))*1e-6,mean_printed_EC_MJmol=statistics.mean(x['reported_EC_MJmol'] for x in r),mean_recomputed_EC_MJmol=statistics.mean(x['recomputed_EC_MJmol'] for x in r)))
a=[x for x in groups if x['table']=='2' and x['mix']=='80/20'][0];b=[x for x in groups if x['table']=='4' and x['mix']=='80/20'][0]
summary=dict(source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),number_rows=len(rows),flags_over_2p5percent=[r for r in rows if abs(r['relative_difference'])>.025],group_means=groups,dry_air_80_20_comparison=dict(with_nozzle=a,without_nozzle=b,relative_NOx_increase=a['mean_NOx_percent']/b['mean_NOx_percent']-1,relative_EC_reduction=1-a['recomputed_EC_from_means_MJmol']/b['recomputed_EC_from_means_MJmol']),notes=['Arithmetic means are a transparent reanalysis, not the authors weighted estimates.','P is discharge power, not total electricity.','NOx is NO+NO2 as printed, not captured fertilizer.','Two rows fail their own formula; printed data remain unchanged.','No controlled equal-power experimental comparison is inferred.'])
(P/'2022_effusion_audit_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary['dry_air_80_20_comparison'],indent=2))
