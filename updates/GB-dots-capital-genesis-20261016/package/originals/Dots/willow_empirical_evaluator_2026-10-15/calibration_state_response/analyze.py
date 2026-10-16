import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import resource
resource.setrlimit(resource.RLIMIT_CPU,(120,120))
resource.setrlimit(resource.RLIMIT_AS,(1024**3,1024**3))
import numpy as np
from scipy.stats import fisher_exact
import json,re,pathlib,hashlib,csv,time
start=time.time(); O=pathlib.Path(__file__).parent
D=(pathlib.Path(__file__).resolve().parent.parent / 'measured_syndrome_acquisition/data/google_105Q_surface_code_d3_d5_d7/d5_at_q8_7/X/r13')
R=(pathlib.Path(__file__).resolve().parent.parent / 'measured_syndrome_audit/r13_raw_reference_structure.json')
ref=json.loads(R.read_text()); ms=ref['measurements']; coords={}; meas=[]; det=[]
for line in (D/'circuit_ideal.stim').read_text().splitlines():
 m=re.fullmatch(r'(\w+)(?:\(([^)]*)\))?\s*(.*)',line)
 assert m,line
 op,args,rest=m.groups()
 if op=='QUBIT_COORDS':coords[int(rest)]=list(map(float,args.split(',')))
 elif op=='M':meas.extend(map(int,rest.split()))
 elif op=='DETECTOR':
  inds=[len(meas)+int(v) for v in re.findall(r'rec\[(-?\d+)\]',rest)]
  det.append({'detector_index':len(det),'coordinates':list(map(float,args.split(','))),'raw_indices':inds})
assert len(meas)==337 and len(det)==312
assert all(q==r['qubit'] for q,r in zip(meas,ms))
selected=[]
for d in det:
 c=d['coordinates'];t=c[2]
 if 2<=t<=12:
  assert len(c)==6 and c[:2]==c[3:5] and c[5]==t-1
  a,b=d['raw_indices'];j=a%24;q=meas[j]
  assert a==24*int(t)+j and b==24*(int(t)-1)+j
  assert meas[a]==meas[b]==q and coords[q]==c[:2]
  d.update(time=int(t),first_measurement_index=j,qubit=q)
  selected.append(d)
assert len(selected)==264
assert sorted((d['time'],d['first_measurement_index']) for d in selected)==[(t,j) for t in range(2,13) for j in range(24)]
assert len(ref['first_round_random_indices'])==len(ref['first_round_determined_indices'])==12
(O/'verified_mapping.json').write_text(json.dumps(selected,indent=2))
# No measured bytes were opened above this line.
def read(name,width):
 a=np.fromfile(D/name,dtype=np.uint8)
 assert a.size==50000*((width+7)//8),(name,a.size)
 return np.unpackbits(a.reshape(50000,-1),axis=1,bitorder='little')[:,:width]
raw=read('measurements.b8',337);sw=read('sweep_bits.b8',25);bits=read('detection_events.b8',312)
tags=[];types=[]
for j in range(24):
 r=ms[j]
 if r['random_variables']:
  assert j in ref['first_round_random_indices'] and r['introduces_fresh_random_variable']
  tags.append(raw[:,j]);types.append('actual_first_raw_bit_noisy_gauge_proxy')
 else:
  assert j in ref['first_round_determined_indices']
  tag=np.full(50000,r['constant'],dtype=np.uint8)
  for s in r['sweep_indices']:tag^=sw[:,s]
  tags.append(tag);types.append('ideal_constant_xor_known_sweep_parity')
# Independently simulated reference terms must cancel all gauge variables.
for d in selected:
 expected=np.zeros(50000,dtype=np.uint8);random=set()
 for i in d['raw_indices']:
  r=ms[i];expected^=raw[:,i];expected^=r['constant']
  for s in r['sweep_indices']:expected^=sw[:,s]
  random.symmetric_difference_update(r['random_variables'])
 assert not random
 assert np.array_equal(expected,bits[:,d['detector_index']]),d
results=[]
for d in selected:
 j=d['first_measurement_index'];tag=tags[j];b=bits[:,d['detector_index']]
 n0=int(np.sum(tag==0));n1=50000-n0
 e0=int(np.sum(b[tag==0]));e1=int(np.sum(b[tag==1]))
 odds,p=fisher_exact([[e1,n1-e1],[e0,n0-e0]],alternative='two-sided')
 r0=e0/n0 if n0 else None;r1=e1/n1 if n1 else None
 results.append(dict(**d,tag_type=types[j],tag_constant=ms[j]['constant'],tag_sweep_indices=ms[j]['sweep_indices'] if not ms[j]['random_variables'] else [],n_tag0=n0,n_tag1=n1,detector1_tag0=e0,detector0_tag0=n0-e0,detector1_tag1=e1,detector0_tag1=n1-e1,detector1_total=e0+e1,detector0_total=50000-e0-e1,risk_tag0=r0,risk_tag1=r1,risk_difference=r1-r0 if n0 and n1 else None,odds_ratio=float(odds),p_two_sided=float(p),p_bonferroni=min(1.,float(p)*264),significant=bool(p<=.01/264),informative=bool(n0 and n1)))
(O/'all_results.json').write_text(json.dumps(results,indent=2))
with (O/'all_results.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
sig=[r for r in results if r['significant']];ranked=sorted(results,key=lambda r:r['p_two_sided'])
summary={'shots':50000,'tests':264,'family_alpha':.01,'per_test_threshold':.01/264,'significant_tests':len(sig),'significant_checks':len(set(r['qubit'] for r in sig)),'significant_by_tag_type':{t:sum(r['significant'] for r in results if r['tag_type']==t) for t in set(types)},'min_p':ranked[0]['p_two_sided'],'all_264_mapping_and_detector_reconstruction_checks_passed':True,'top_10':ranked[:10],'significant_results':sig,'runtime_seconds':time.time()-start,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'sha256':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [O/'PROTOCOL_FROZEN.md',O/'analyze.py',R,D/'circuit_ideal.stim',D/'measurements.b8',D/'sweep_bits.b8',D/'detection_events.b8']}}
(O/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({k:v for k,v in summary.items() if k not in ['sha256','significant_results','top_10']},indent=2))
print('TOP',json.dumps([{k:r[k] for k in ['qubit','time','tag_type','n_tag0','n_tag1','detector1_tag0','detector1_tag1','risk_difference','odds_ratio','p_two_sided','p_bonferroni']} for r in ranked[:5]],indent=2))
