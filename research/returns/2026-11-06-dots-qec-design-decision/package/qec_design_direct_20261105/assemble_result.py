import json,sys,time,hashlib
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'canonical_qec_witness_20261105'))
from confidence_fast import exact_cp
started=time.perf_counter()
old=json.loads((ROOT/'inherited_d21/production.json').read_text())
meta=json.loads((ROOT/'inherited_d21/parameters.json').read_text())
lo,hi=exact_cp(old['counts']['accepted'],old['shots'],F(1,3000),bits=24)
Z=F(old['normalizer_exact']);eps=F(meta['conversion_TV_upper_exact']);a,b=max(F(0),Z*lo-eps),min(F(1),Z*hi+eps)
d21={'distance':21,'rounds':21,'shots':old['shots'],'accepted':old['counts']['accepted'],'alpha_exact':'1/3000','method':'exact fixed-shot Clopper-Pearson on specific archived precommitted sample','source_sha256':hashlib.sha256((ROOT/'inherited_d21/production.json').read_bytes()).hexdigest(),'acceptance_interval_exact':[str(lo),str(hi)],'failure_interval_exact':[str(a),str(b)],'failure_interval_float':[float(a),float(b)],'decision':'reject' if a>F(1,10**12) else 'inconclusive','recomputation_seconds':time.perf_counter()-started,'provenance':'Prior result known. This sample was precommitted n=10000,seed=202611052921; the original alpha=1/1000 interval is not substituted as a familywise interval.'}
(ROOT/'d21_decision.json').write_text(json.dumps(d21,indent=2)+'\n')
results=[json.loads((ROOT/f'd{d}_decision.json').read_text()) for d in [19,21,23]]
for d in [19,23]:
    G=json.loads((ROOT/'qec_fault_tuple_20261105'/f'd{d}'/'input_graph.json').read_text());assert set(G['costs'])=={4,5}
    A=json.loads((ROOT/'canonical_qec_circuit_gate_20261105'/f'd{d}_r{d}_p1_1000_acquisition.json').read_text());assert A['circuit_p_exact']=='1/1000';assert A['exact_projection_hyperedges']==0
selected=None
for r in results:
    if r['decision']=='pass' and all(v['decision']=='reject' for v in results if v['distance']<r['distance']):selected=r['distance'];break
resources=[json.loads((ROOT/f'd{d}_pipeline_resources.json').read_text()) for d in [19,23]]
priorcost=json.loads((ROOT/'inherited_d21/complete_cost_accounting.json').read_text())[1]
phys=json.loads((ROOT/'inherited_d21/independent_circuit_counts_and_d21_audit.json').read_text())['circuits']
out={'candidate_set':[19,21,23],'familywise_confidence_at_least_exact':'999/1000','target_exact':'1/1000000000000','selected_smallest_in_candidate_set':selected,'decisions':[{k:r[k] for k in ['distance','rounds','shots','decision','failure_interval_exact','failure_interval_float','method']} for r in results], 'physical_resource_counts_independent_audit':phys,'new_pipeline_wall_sum_seconds':sum(x['full_pipeline_seconds'] for x in resources),'new_pipelines_ran_concurrently':True,'concurrent_elapsed_is_not_sum':True,'new_pipeline_largest_sampled_tree_rss_bytes':max(s['sampled_process_tree_peak_rss_bytes'] for x in resources for s in x['stages']),'d21_prior_complete_stage_sum_seconds':priorcost['sum_separately_measured_complete_stage_seconds'],'historical_plus_new_operational_stage_sum_seconds':sum(x['full_pipeline_seconds'] for x in resources)+priorcost['sum_separately_measured_complete_stage_seconds']+d21['recomputation_seconds'],'cost_caveats':'d19/d23 individually continuously timed from acquisition through output, running concurrently on shared host. d21 historical cost is a sum of separate complete measured stages, not a fresh replay in this gate. Review/development/provenance assembly excluded and disclosed. RSS is sampled process-tree, not kernel-enforced bound.','audit_status':'Independent new-input review requested; see separate audit artifact before release.'}
(ROOT/'DECISION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
