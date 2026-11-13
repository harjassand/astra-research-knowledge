"""PREDECLARED fixed1000-draw holdout, one frozen algorithm,99% one-sided abort bound."""
from pathlib import Path
from fractions import Fraction as F
import json,time,secrets,hashlib,statistics,sys
from frozen_component_v1 import sample,grid_layers
ROOT=Path(__file__).parent
sources=[ROOT/'frozen_component_v1.py',ROOT.parent/'bridge_dephasing/check.py']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
protocol=dict(version='frozen_component_v1',N=1000,n=1024,width=32,T=100,r='3/100',epsilon='1/50',component_entries=4096,integer_bits=20000,bridge_prune=True,terminal_measure=True,confidence='99% one-sided fixedN binomial upper',seed_policy='Fresh128bit OS seeds recorded, independent seeded pseudorandom streams',source_sha256=hashes,predeclared_before_samples=True)
(ROOT/'holdout_v1_protocol.json').write_text(json.dumps(protocol,indent=2))
setup=time.perf_counter();layers=grid_layers(32,32,100);setup=time.perf_counter()-setup
rows=[];start=time.perf_counter();cpu0=time.process_time()
for j in range(protocol['N']):
 wall=time.perf_counter();cpu=time.process_time();seed=secrets.randbits(128);output,s=sample(1024,layers,r=F(3,100),eps=F(1,50),seed=seed,cap=4096,bitcap=20000)
 s.update(index=j,seed=str(seed),output=str(output),total_wall_seconds=time.perf_counter()-wall,total_cpu_seconds=time.process_time()-cpu);rows.append(s)
 if (j+1)%25==0:
  (ROOT/'holdout_v1_progress.json').write_text(json.dumps(dict(completed=len(rows),aborts=sum(r['aborted'] for r in rows),elapsed=time.perf_counter()-start),indent=2));print('holdout',j+1,'aborts',sum(r['aborted'] for r in rows),flush=True)
 (ROOT/'holdout_v1_raw.jsonl').open('a').write(json.dumps(s)+'\n')
assert hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'Frozen dependency changed'
sys.path.insert(0,str(ROOT.parent/'mps_error'));from abort_confidence import upper
aborts=sum(r['aborted'] for r in rows);u=upper(len(rows),aborts,F(1,100))
summary=dict(protocol=protocol,completed=len(rows),aborts=aborts,abort_99pct_upper=str(u),abort_99pct_upper_float=float(u),mean_total_wall_seconds=statistics.mean(r['total_wall_seconds'] for r in rows),mean_total_cpu_seconds=statistics.mean(r['total_cpu_seconds'] for r in rows),max_component_entries=max(r['max_component_entries'] for r in rows),max_live_entries=max(r['max_live_entries'] for r in rows),max_amp_bits=max(r['max_amplitude_integer_bits'] for r in rows),max_live_payload_bits=max(r['max_live_payload_bits'] for r in rows),setup_seconds=setup,total_elapsed_seconds=time.perf_counter()-start,total_cpu_seconds=time.process_time()-cpu0,source_hashes_unchanged=True,limitations='Statistical99% abort confidence for this finite frozen setting, not a scaling theorem; ideal unbiased-randomness algorithm exercised with independent OS-seeded PRNG streams. Exact integer quantum evolution. Payload excludes Python overhead.')
(ROOT/'holdout_v1_result.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
