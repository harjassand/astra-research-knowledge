from pathlib import Path
from fractions import Fraction as F
from collections import Counter
import hashlib,json,math,sys,time,importlib.util
import numpy as np
ROOT=Path(__file__).resolve().parent;P=ROOT.parent/'qec_design_direct_20261105';start=time.perf_counter()
spec=importlib.util.spec_from_file_location('direct_cs',P/'sequential_decision.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
manifest=[]
for line in (P/'PRECOMMIT_SHA256SUMS').read_text().splitlines():
 h,p=line.split(None,1);assert hashlib.sha256((ROOT.parent/p).read_bytes()).hexdigest()==h;manifest.append(p)
# Independent interval condition using rational powers, not producer integer predicate.
def outside(n,k,p):
 return F(n+1)*math.comb(n,k)*p**k*(1-p)**(n-k)<=F(1,3000)
unit=0
for n in range(1,51):
 for k in range(n+1):
  a,b=m.confidence_sequence(n,k)
  assert 0<=a<=F(k,n)<=b<=1
  assert k==0 or outside(n,k,a)
  assert k==n or outside(n,k,b)
  unit+=1
# Exact finite-horizon crossing probabilities under simple rational Bernoulli laws.
cross=[]
for p in [F(1,2),F(1,10),F(9,10),F(1,1000)]:
 paths=[F(1)];absorbed=F(0)
 for n in range(1,129):
  nxt=[F(0)]*(n+1)
  for k,v in enumerate(paths):nxt[k]+=v*(1-p);nxt[k+1]+=v*p
  for k,v in enumerate(nxt):
   if outside(n,k,p):absorbed+=v;nxt[k]=F(0)
  paths=nxt
 assert absorbed+sum(paths)==1 and absorbed<=F(1,3000)
 cross.append({'p':str(p),'horizon':128,'crossing_probability':float(absorbed)})
reports=[]
for d in [19,23]:
 file=P/f'd{d}_decision.json'
 if not file.exists():continue
 r=json.loads(file.read_text());proposal=m.FaultTupleProposal(P/'qec_fault_tuple_20261105'/f'd{d}');G=json.loads((P/'qec_fault_tuple_20261105'/f'd{d}'/'input_graph.json').read_text())
 Z=F(r['normalizer_exact']);tv=F(r['conversion_TV_upper_exact']);assert Z==proposal.Z and tv==F(proposal.meta['conversion_TV_upper_exact'])
 records=r['inspection_records'];previous=0
 for rec in records:
  n,k=rec['n'],rec['k'];a,b=m.confidence_sequence(n,k);L=max(F(0),Z*a-tv);U=min(F(1),Z*b+tv)
  assert [str(L),str(U)]==rec['failure_interval_exact']
  assert k==0 or outside(n,k,a)
  assert k==n or outside(n,k,b)
  status='pass' if U<=F(1,10**12) else 'reject' if L>F(1,10**12) else 'inconclusive'
  assert rec['decision']==status
  assert n-previous==250;previous=n
 assert all(rec['decision']=='inconclusive' for rec in records[:-1])
 # Replay entire stopped trajectory and validate syndrome and L0 on every decode.
 original_decode=proposal.model.decode;original_witness=proposal.model.witness;calls=[0];fail=[0];last=[None]
 masks=[sum(1<<j for j in e['detectors']) for e in G['errors']];labels=[e['logical'] for e in G['errors']]
 def decode(e):
  c=original_decode(e);res=e^c;sy=l=0
  for j in np.flatnonzero(res):sy^=masks[j];l^=labels[j]
  assert sy==0 and l==int(res[proposal.model.cut].sum())%2
  last[0]=l;calls[0]+=1;fail[0]+=l;return c
 def witness(e):
  w=original_witness(e);assert bool(w)==bool(last[0])
  if w:assert sum(G['costs'][j]*(2*int(e[j])-1) for j in w)>=0
  return w
 proposal.model.decode=decode;proposal.model.witness=witness
 rng=m.CountedBits(r['seed']);counts=Counter();steps=decoded=0;prefix=[]
 for i in range(r['shots']):
  value,kind,length,dc,score=proposal.trial(rng);assert value==int(kind=='accepted');counts[kind]+=1;steps+=length;decoded+=dc
  if (i+1)%250==0:prefix.append([i+1,counts['accepted']])
 assert dict(counts)==r['counts'] and steps==r['fault_steps'] and decoded==r['decoder_calls']==calls[0]
 assert prefix==[[x['n'],x['k']] for x in records]
 assert rng.summary()==r['requested_random_bits'] and dict(proposal.prefix.counters)==r['endpoint_selection']
 assert fail[0]==counts['accepted']+counts['other_witness']
 reports.append({'distance':d,'status':'PASS exact CS checks, complete stopped-trajectory replay, syndrome and original L0 check on all decodes','shots':r['shots'],'accepted':counts['accepted'],'decision':r['decision'],'interval':r['failure_interval_float'],'decodes_checked':calls[0],'source_sha256':hashlib.sha256(file.read_bytes()).hexdigest()})
out={'status':'PASS: mixture confidence sequence and available production runs','manifest_files_checked':len(manifest),'exhaustive_endpoint_unit_cases':unit,'finite_horizon_crossing_checks':cross,'production':reports,'elapsed_seconds':time.perf_counter()-start,'scope':'Tests support implementation; all-time statistical coverage follows the uniform-beta nonnegative likelihood-ratio supermartingale and Ville bound, conditional on IID indicators.'}
(ROOT/'sequential_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
