#!/usr/bin/env python3
"""Generate NEW jointly retained pooled observations; never alter old files."""
from pathlib import Path
import gzip,hashlib,json,sys,time
ROOT=Path(__file__).resolve().parent;PARENT=ROOT.parent;sys.path.insert(0,str(ROOT))
from joint_source import TaggedPoolSource
from fractions import Fraction as F
BASE_SHA='dc7583f0aa94e06f7440a6109a2dbef128b1db35538664a1880f8a5c4c146568'

def run(output_dir=None):
    start=time.perf_counter();raw=(PARENT/'history_sensitive_4096_result.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==BASE_SHA
    model=json.loads(raw);n=model['n'];parts=model['partition'];r=len(parts);which=[0]*n
    for g,p in enumerate(parts):
        for i in p:which[i]=g
    q=TaggedPoolSource(n);b,e,den=q.public_task();assert (b,e,den)==(model['task_b'],model['task_ell_numer'],model['task_ell_denominator'])
    records=[];summaries=[]
    for turn,schedule in enumerate(model['cross_rounds']):
        N=schedule['outgoing_per_pooled_batch'];reps=schedule['outgoing_replicates']
        for a in range(model['m']):
            for g,p in enumerate(parts):
                for rep in range(reps):
                    record=q.batch(a,p,N,which,r);record.update({'turn':turn,'group':g,'replicate':rep});records.append(record)
        summaries.append({'prefix':turn,'logical_calls_cumulative':q.logical_calls,'individual_macro_reset_draws_cumulative':q.individual_macro_reset_draws,'row_multinomials_cumulative':q.row_batches})
        print(json.dumps(summaries[-1]),flush=True)
    data=json.dumps({'n':n,'r':r,'partition':parts,'records':records},separators=(',',':')).encode();compressed=gzip.compress(data,mtime=0)
    out={'status':'NEW_JOINT_SOURCE_DATA','records':len(records),'logical_source_calls':q.logical_calls,'actually_generated_macro_reset_destination_labels':q.individual_macro_reset_draws,'row_branch_and_local_multinomials_each':q.row_batches,'largest_macro_or_reset_owner_destination_array_length':q.allocated_macro_peak,'branch_argument_probabilities':[str(x) for x in q.branch_exact],'cumulative_prefixes':summaries,'transcript_uncompressed_bytes':len(data),'transcript_compressed_bytes':len(compressed),'transcript_sha256':hashlib.sha256(compressed).hexdigest(),'prior_discovery_column_and_coarse_calls':sum(x['logical_forward_calls'] for x in model['source_ledger'] if x['phase'] in ('column_bound','sparse_coarse')),'actual_old_acquisition_not_refunded':model['logical_forward_calls'],'historical_tags_reconstructed':False,'scope':'New joint source draws under original ordinary _row_counts ideal argument law. Reuses previously paid acquired partition and old column/coarse evidence, NOT historical pilot/incoming/outgoing outcomes. Statistics are correlated exactly as ordinary chosen-row transitions. No new external source calls or physical operation; logical simulated calls and actually generated labels are separately reported.','seconds':time.perf_counter()-start,'source_sha256':hashlib.sha256((ROOT/'joint_source.py').read_bytes()).hexdigest(),'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'base_model_sha256':BASE_SHA}
    if output_dir is not None:
        p=Path(output_dir);(p/'tagged_observations.json.gz').write_bytes(compressed);(p/'tagged_generation.json').write_text(json.dumps(out,indent=2)+'\n')
    return out,records
if __name__=='__main__':
    out,_=run(ROOT);print(json.dumps(out,indent=2))
