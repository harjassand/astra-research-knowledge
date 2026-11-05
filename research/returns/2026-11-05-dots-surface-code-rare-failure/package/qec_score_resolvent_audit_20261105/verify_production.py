"""Independent production readback, confidence proof and instrumented exact replay."""
import sys,json,time,random,hashlib,math
from pathlib import Path
from fractions import Fraction as F
import numpy as np
from scipy.stats import beta
root=Path(__file__).resolve().parents[1];src=root/'qec_score_resolvent_20261105';sys.path.insert(0,str(src));from exact_sampler import FoldedProposal
start=time.perf_counter();r=json.loads((src/'production_100k.json').read_text());meta=json.loads((src/'certificate_N64.json').read_text());G=json.loads((root/'canonical_qec_circuit_gate_20261105/d13_r13_p1_1000_graph.json').read_text());checked=[]
for line in (src/'PRODUCTION_SHA256SUMS').read_text().splitlines():
 expected,path=line.split(None,1);actual=hashlib.sha256((root/path).read_bytes()).hexdigest();assert expected==actual;checked.append(path)
assert sum(r['counts'].values())==r['shots']==100000 and r['seed']==202611051864
assert r['counts']['not_failure']+r['counts']['other_witness']+r['counts']['accepted']==r['decoder_calls']
assert r['normalizer_exact']==meta['Z_exact'];Z=F(meta['Z_exact']);bias=F(meta['conversion_TV_upper_exact']);lo,hi=map(F,r['interval']['acceptance_exact']);L,U=map(F,r['interval']['failure_probability_exact']);assert L==max(F(0),Z*lo-bias) and U==min(F(1),Z*hi+bias)
assert [float(L),float(U)]==r['interval']['failure_probability_float'];assert float(Z*r['counts']['accepted']/r['shots'])==r['point_estimate']
# Independently recompute the model conversion budget.
TV=sum(abs(F(k,1<<64)-F(e['p_mid']))+F(e['p_radius']) for k,e in zip(meta['q_numerators'],G['errors']));assert TV==bias
# Independently verify each exact CP root inequality with reverse binomial sums,
# not the production helper's recurrence or numerical proposal.
n=r['shots'];x=r['counts']['accepted'];D=1<<24;den=D**n;jl=int(lo*D);ju=int(hi*D)
def rcdf(k,j):
 term=math.comb(n,k)*j**k*(D-j)**(n-k);total=term
 for ell in range(k,0,-1):
  term,rem=divmod(term*ell*(D-j),(n-ell+1)*j);assert rem==0;total+=term
 return total
assert (den-rcdf(x-1,jl))*2000<=den
assert rcdf(x,ju)*2000<=den
assert (den-rcdf(x-1,jl+1))*2000>den
assert rcdf(x,ju-1)*2000>den
reflo=beta.ppf(.0005,x,n-x+1);refhi=beta.ppf(.9995,x+1,n-x);assert float(lo)<=reflo and float(hi)>=refhi
confidence_time=time.perf_counter()-start
print(json.dumps({'stage':'exact confidence and budgets verified','seconds':confidence_time}),flush=True)
# Replay without writing into the production directory. Instrument every decoder
# call to verify zero residual syndrome and the original L0 event independently
# of the gauge-cut implementation. No extra randomness is consumed.
P=FoldedProposal();original_decode=P.model.decode;original_witness=P.model.witness;colmask=[]
for e in G['errors']:colmask.append(sum(1<<j for j in e['detectors']))
original_labels=[e['logical'] for e in G['errors']];event_count={'decode_calls':0,'original_L0_failures':0,'zero_syndromes':0};last=[None]
def checked_decode(e):
 c=original_decode(e);res=e^c;s=0;logical=0
 for i in np.flatnonzero(res):s^=colmask[i];logical^=original_labels[i]
 assert s==0;assert logical==int(res[P.model.cut].sum())%2
 event_count['decode_calls']+=1;event_count['zero_syndromes']+=1;event_count['original_L0_failures']+=logical;last[0]=logical
 return c
def checked_witness(e):
 w=original_witness(e);assert bool(w)==bool(last[0])
 if w:assert sum(G['costs'][i]*(2*int(e[i])-1) for i in w)>=0
 return w
P.model.decode=checked_decode;P.model.witness=checked_witness
rng=random.Random(r['seed']);counts={k:0 for k in r['counts']};steps=0;decoders=0;maxsteps=0;maxscore=0;t0=time.perf_counter()
for i in range(n):
 value,kind,length,decoded,score=P.trial(rng);counts[kind]+=1;steps+=length;decoders+=decoded;maxsteps=max(maxsteps,length);maxscore=max(maxscore,score)
assert counts==r['counts'];assert steps/n==r['mean_path_steps'];assert decoders==r['decoder_calls']==event_count['decode_calls'];assert maxsteps==r['maximum_path_steps'];assert maxscore==r['maximum_true_score'];assert event_count['original_L0_failures']==counts['other_witness']+counts['accepted']
setup=json.loads((src/'fresh_setup_benchmark.json').read_text());tmp=Path(setup['temporary_directory']) if setup.get('temporary_directory') else None;freshgraph=tmp/'canonical_qec_circuit_gate_20261105/d13_r13_p1_1000_graph.json' if tmp else None;freshtable=tmp/'qec_score_resolvent_20261105/certified_table_N64.bin' if tmp else None
fresh_available=bool(tmp and freshgraph.exists() and freshtable.exists())
if fresh_available:
 assert hashlib.sha256(freshgraph.read_bytes()).hexdigest()==meta['input_sha256'];assert hashlib.sha256(freshtable.read_bytes()).hexdigest()==meta['table_sha256']
# Freeze ALL imported scientific runtime sources, not just the top-level script.
deps=['qec_score_resolvent_20261105/exact_sampler.py','canonical_qec_circuit_gate_20261105/tilted_pilot.py','canonical_qec_witness_20261105/sampler.py','canonical_qec_witness_20261105/confidence_fast.py','canonical_qec_witness_20261105/sampler_frozen_phenomenological.py']
hashes={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in deps}
out={'status':'PASS: exact production interval/budget and every fixed-seed category/event reproduced','shots':n,'counts_reproduced':counts,'decoder_event_checks':event_count,'mean_steps_reproduced':steps/n,'maximum_steps_reproduced':maxsteps,'maximum_score_reproduced':maxscore,'failure_interval_exact':[str(L),str(U)],'failure_interval_float':[float(L),float(U)],'CP_dyadic_numerators':[jl,ju],'CP_dyadic_denominator':D,'CP_beta_quantile_diagnostic':[reflo,refhi],'conversion_TV_exact':str(bias),'production_hash_entries_verified':len(checked),'runtime_source_hashes':hashes,'input_sha256':meta['input_sha256'],'table_sha256':meta['table_sha256'],'full_work_accounting':{'fresh_setup_seconds':setup['total_fresh_setup_seconds'],'production_loaded_run_seconds':r['total_seconds'],'sum_of_separately_timed_stages_seconds':setup['total_fresh_setup_seconds']+r['total_seconds'],'fresh_graph_and_table_bytes_match_frozen':True if fresh_available else None,'fresh_temporary_files_available_here':fresh_available,'fresh_setup_note':'A later portable replay may lack the original temporary rebuild directory; this does not skip production/certificate checks.','not_a_single_joint_timing':True},'audit_timing_seconds':{'confidence_and_readback':confidence_time,'instrumented_replay':time.perf_counter()-t0,'total':time.perf_counter()-start},'scope':'One-basis projected exact-rational circuit model, fixed integer-cost decoder, ideal iid random bits; no hardware or cross-decoder claim.'}
Path(__file__).with_name('production_audit_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
