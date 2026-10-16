"""Own standard-library audit. Reads publisher text; never imports/runs author code."""
from pathlib import Path
from fractions import Fraction
import json,re,csv,hashlib
P=Path(__file__).resolve().parent

def parse(s):
 if s=='{}':return []
 pos=0
 def seq(end=False):
  nonlocal pos
  gates=[]
  while pos<len(s) and s[pos]!=')':
   if s[pos]=='(':
    pos+=1;term=seq(True);assert pos<len(s) and s[pos]==')';pos+=1
    power=1
    if pos<len(s) and s[pos]=='^':
     pos+=1;start=pos
     while pos<len(s) and s[pos].isdigit():pos+=1
     assert pos>start;power=int(s[start:pos])
    gates+=term*power
   else:
    token=s[pos:pos+2];assert token in ['Gi','Gx','Gy'],(s,pos);pos+=2;gates.append(token)
  return gates
 result=seq();assert pos==len(s);return result
streams={};checks=[]
for arm in ['gst','rgst']:
 for run in range(1,8):
  f=P/'rgst/data'/f'{arm}_{run}.gst';lines=f.read_text().splitlines();assert lines[0].strip()=='## Columns = minus count, plus count';d={}
  for line in lines[1:]:
   if not line.strip() or line.startswith('#'):continue
   a=line.split();assert len(a)==3 and a[0] not in d
   c=tuple(int(v) for v in a[1:]);assert min(c)>=0 and sum(c)==1000;d[a[0]]=c
  assert len(d)==3505;streams[arm,run]=d;checks.append({'path':str(f.relative_to(P)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'rows':len(d)})
keys=list(streams['gst',1]);assert all(list(d)==keys for d in streams.values());expanded={k:parse(k) for k in keys};assert max(map(len,expanded.values()))==1030
selected=[]
for k,gates in expanded.items():
 if not gates or len(set(gates))!=1:continue
 # Literal repeated tokens, or a single parenthesized gate and exponent only.
 bare=(k==''.join(gates)) or bool(re.fullmatch(r'\(G[ixy]\)(?:\^[0-9]+)?',k))
 if bare and (gates[0]=='Gi' or len(gates)%4==0):selected.append((gates[0],len(gates),k))
selected.sort();assert len(selected)==27
expected={(gate,n,k,run) for gate,n,k in selected for run in range(1,8)}
with (P/'all_pure_power_return_counts.csv').open() as f:rows=list(csv.DictReader(f))
assert len(rows)==189;seen=set()
for r in rows:
 gate,n,k,run=r['gate'],int(r['n']),r['nominal_circuit'],int(r['experiment']);seen.add((gate,n,k,run));a=streams['gst',run][k];b=streams['rgst',run][k]
 assert [int(r[x]) for x in ['gst_minus_count','gst_plus_count','rgst_minus_count','rgst_plus_count']]==list(a+b)
 assert r['ideal_return_label']=='minus' and int(r['physical_pulses_each_arm'])==2*n and int(r['shots_each_arm'])==1000
 assert abs(float(r['active_pulse_time_us_each_arm'])-n/10)<1e-12
 assert abs(float(r['delta_return_probability'])-float(Fraction(b[0]-a[0],1000)))<1e-14
assert seen==expected
with (P/'all_pure_power_return_summary.csv').open() as f:summaries=list(csv.DictReader(f))
assert len(summaries)==27
for r in summaries:
 k=r['nominal_circuit'];aa=[streams['gst',i][k][0] for i in range(1,8)];bb=[streams['rgst',i][k][0] for i in range(1,8)];delta=[b-a for a,b in zip(aa,bb)]
 for name,value in [('gst_return_fraction_mean',Fraction(sum(aa),7000)),('rgst_return_fraction_mean',Fraction(sum(bb),7000)),('mean_paired_delta',Fraction(sum(delta),7000)),('min_paired_delta',Fraction(min(delta),1000)),('max_paired_delta',Fraction(max(delta),1000))]:assert abs(float(r[name])-float(value))<1e-14
 for name,value in [('positive_pairs',sum(v>0 for v in delta)),('zero_pairs',sum(v==0 for v in delta)),('negative_pairs',sum(v<0 for v in delta))]:assert int(r[name])==value
# Read-only static source checks for labels, truncation and compiler table.
convention=(P/'source/pygsti_v093_std1Q_XYI.py.txt').read_text();assert 'prepExpressions=["0"]' in convention and 'effectExpressions=["1"]' in convention and "'minus': ('rho0','remainder')" in convention
trunc=(P/'source/pygsti_v093_stdlists.py.txt').read_text();assert 'truncScheme="whole germ powers"' in trunc and 'Rfn = _gsc.repeat_with_max_length' in trunc
pulse=(P/'qgl_source/src/pulses.jl').read_text();section=pulse.split('function DiAC(q::Qubit, num)',1)[1].split('\nend',1)[0];triples=re.findall(r'\[\s*(-?\d+\.\d+),\s*(-?\d+\.\d+),\s*(-?\d+\.\d+)\]',section);assert len(triples)==24 and section.count('X90(q)')==2
with (P/'qgl_source/diatomic_angles.csv').open() as f:angles=list(csv.DictReader(f))
for i,(row,values) in enumerate(zip(angles,triples),1):assert int(row['clifford_index'])==i and [float(row[k]) for k in ['alpha_turns','beta_turns','gamma_turns']]==[float(v)/2 for v in values]
# Bounded independent parse of the simple released EDD count-record layout; no YAML execution.
edd=[]
for f in sorted((P/'edd_subset').glob('*rawData.yml')):
 text=f.read_text();parts=text.split('  - backend_name:')[1:];names=[]
 for part in parts:
  counts=[int(v) for v in re.findall(r"^        '0x[01]': (\d+)$",part,re.M)];shots=re.findall(r'^    shots: (\d+)$',part,re.M);name=re.findall(r'^      name: (.+)$',part,re.M)
  assert len(counts)==2 and len(shots)==len(name)==1 and sum(counts)==int(shots[0])==8192;names+=name
 assert len(parts)==(25 if '_free_' in f.name else 100)
 edd.append({'file':f.name,'circuits':len(parts),'date':re.search(r'^  date: (.+)$',text,re.M)[1],'names':names,'shots':8192})
prov=json.loads((P/'provenance.json').read_text());verified=0
for e in prov['files']:
 f=P/e['path']
 if f.exists():assert f.stat().st_size==e['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==e['sha256'];verified+=1
result={'status':'PASS','ware_files':checks,'ordered_keys_match':True,'circuits_per_file':3505,'outcomes_per_circuit':1000,'total_outcomes':49070000,'max_expanded_clifford_length':1030,'selected_keys':selected,'paired_rows':189,'all_exported_counts_and_means_recomputed':True,'minus_return_source_convention_verified':True,'compiler_24_angle_rows_verified':True,'edd_separate_count_contract':edd,'source_provenance_entries_verified':verified,'no_author_code_execution':True,'no_fitting_or_hypothesis_testing':True}
(P/'independent_audit_results.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ['ware_files','selected_keys','edd_separate_count_contract']},indent=2))
