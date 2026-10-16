"""Read text count data only; no author code imports, no fitting."""
from pathlib import Path
import re,json,csv
base=Path(__file__).parent;p=base/'rgst/data'
def read(fn):
 d={}
 for line in fn.read_text().splitlines():
  if line.startswith('#') or not line.strip():continue
  s,*c=line.split();assert s not in d;d[s]=tuple(map(int,c));assert len(d[s])==2 and sum(d[s])==1000 and min(d[s])>=0
 return d
def length(s):
 if s=='{}':return 0
 s=re.sub(r'\(((?:G[ixy])+)\)\^(\d+)',lambda m:m[1]*int(m[2]),s)
 s=re.sub(r'\(((?:G[ixy])+)\)',lambda m:m[1],s)
 toks=re.findall('G[ixy]',s);assert ''.join(toks)==s,s
 return len(toks)
data={(a,i):read(p/f'{a}_{i}.gst') for a in ['gst','rgst'] for i in range(1,8)}
keys=list(data['gst',1]);assert all(list(d)==keys for d in data.values())
ls=[length(k) for k in keys]
summary={'files':14,'circuits_per_file':len(keys),'shots_per_circuit':1000,'total_shots':14*len(keys)*1000,'identical_key_order_all_files':True,'min_clifford_count':min(ls),'max_clifford_count':max(ls),'physical_pulses_per_clifford_paper':2,'pulse_width_ns_paper':50,'actual_per_shot_pauli_seeds_present':False,'waveform_schedules_present':False,'author_randomizer_example_seed':'0xcafe; not verified as actual acquisition seed'}
(base/'contract_validation.json').write_text(json.dumps(summary,indent=2));print(summary)
rows=[]
for s in ['(Gx)^32','(Gy)^32','(Gi)^128','(Gx)^1024']:
 for i in range(1,8):
  a=data['gst',i][s];b=data['rgst',i][s]
  rows.append({'experiment':i,'nominal_circuit':s,'cliffords':length(s),'physical_pulses_each_arm':length(s)*2,'active_pulse_time_us_each_arm':length(s)*.1,'gst_minus_count':a[0],'gst_plus_count':a[1],'rgst_minus_count':b[0],'rgst_plus_count':b[1],'delta_minus_probability':(b[0]-a[0])/1000})
with (base/'direct_count_examples.csv').open('w') as f:
 w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
for s in ['(Gx)^32','(Gy)^32','(Gi)^128','(Gx)^1024']:
 a=[r for r in rows if r['nominal_circuit']==s];print(s,'GST', [r['gst_minus_count']/1000 for r in a], 'rGST',[r['rgst_minus_count']/1000 for r in a],'delta range', min(r['delta_minus_probability'] for r in a),max(r['delta_minus_probability'] for r in a))

# Predeclared exploratory set: exact bare pure powers, never padded/fiducial keys.
# Accept a bare literal run or a parenthesized single gate to a power.
def bare_power(s):
 m=re.fullmatch(r'\((G[ixy])\)(?:\^(\d+))?',s)
 if m:return m[1],int(m[2] or 1)
 m=re.fullmatch(r'(G[ixy])(?:\1)*',s)
 if m:return m[1],len(s)//2
 return None
selected=[]
for s in keys:
 z=bare_power(s)
 if z and (z[0]=='Gi' or z[1]%4==0):selected.append((z[0],z[1],s))
selected.sort()
rows=[]
for gate,n,s in selected:
 for i in range(1,8):
  a=data['gst',i][s];b=data['rgst',i][s]
  rows.append({'gate':gate,'n':n,'nominal_circuit':s,'experiment':i,'ideal_return_label':'minus','physical_pulses_each_arm':2*n,'active_pulse_time_us_each_arm':n*.1,'gst_minus_count':a[0],'gst_plus_count':a[1],'rgst_minus_count':b[0],'rgst_plus_count':b[1],'shots_each_arm':1000,'delta_return_probability':(b[0]-a[0])/1000})
with (base/'all_pure_power_return_counts.csv').open('w') as f:
 w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
summary=[]
for gate,n,s in selected:
 rs=[r for r in rows if r['nominal_circuit']==s]
 summary.append({'gate':gate,'n':n,'nominal_circuit':s,'paired_runs':7,'gst_return_fraction_mean':sum(r['gst_minus_count'] for r in rs)/7000,'rgst_return_fraction_mean':sum(r['rgst_minus_count'] for r in rs)/7000,'mean_paired_delta':sum(r['rgst_minus_count']-r['gst_minus_count'] for r in rs)/7000,'min_paired_delta':min(r['delta_return_probability'] for r in rs),'max_paired_delta':max(r['delta_return_probability'] for r in rs),'positive_pairs':sum(r['delta_return_probability']>0 for r in rs),'zero_pairs':sum(r['delta_return_probability']==0 for r in rs),'negative_pairs':sum(r['delta_return_probability']<0 for r in rs)})
with (base/'all_pure_power_return_summary.csv').open('w') as f:
 w=csv.DictWriter(f,summary[0].keys());w.writeheader();w.writerows(summary)
(base/'pure_power_selection_validation.json').write_text(json.dumps({'exact_keys_selected':len(selected),'paired_rows':len(rows),'selected':selected,'no_fiducial_substitution':True,'count_label_evidence':'pyGSTi v0.9.3 std1Q_XYI: prep 0, effect E0=1, plus E0, minus remainder','no_model_fit':True},indent=2))
print('ALL PURE POWERS',len(selected),'keys;',len(rows),'paired run rows')
for s in summary:print(s)
