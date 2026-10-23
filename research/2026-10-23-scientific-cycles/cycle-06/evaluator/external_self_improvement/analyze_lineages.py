#!/usr/bin/env python3
"""Descriptive, common-task reanalysis of official released DGM metadata.

No execution of agent/source code, model calls or causal inference. Unknown task
outcomes stay unknown. Missing evaluations are not asserted to be failed science.
"""
from pathlib import Path
from collections import Counter, defaultdict
from fractions import Fraction
import csv, hashlib, json, sys, time

BASE = Path(__file__).resolve().parent

def stream_json(path):
    text = path.read_text(); decoder = json.JSONDecoder(); pos = 0; result = []
    while pos < len(text):
        while pos < len(text) and text[pos].isspace(): pos += 1
        if pos == len(text): break
        obj, pos = decoder.raw_decode(text, pos); result.append(obj)
    return result

def outcome(meta):
    p = meta.get('overall_performance') or {}
    yes = set(p.get('total_resolved_ids', []))
    no = set(p.get('total_unresolved_ids', [])) | set(p.get('total_emptypatch_ids', []))
    assert not yes & no, 'Contradictory task labels'
    return yes, no

def summary(rows):
    available = [r for r in rows if r['pair_fully_observed_10']]
    verified = [r for r in rows if r['verified_gain_10']]
    gain = sum(r['gain_tasks_10'] for r in available)
    loss = sum(r['loss_tasks_10'] for r in available)
    return {
        'attempts': len(rows),
        'native_archive_admissions': sum(r['native_admitted'] for r in rows),
        'child_performance_metadata_available': sum(r['child_performance_available'] for r in rows),
        'fully_observed_parent_child_pairs_10': len(available),
        'verified_improving_children_10': len(verified),
        'definitely_worse_children_10': sum(r['definitely_worse_10'] for r in rows),
        'ties_in_complete_pairs_10': sum(r['child_successes_10'] == r['parent_successes_10'] for r in available),
        'no_observed_verified_gain_10': len(rows)-len(verified),
        'unknown_child_outcome_pairs_10': sum(not r['pair_fully_observed_10'] for r in rows),
        'new_success_events_complete_pairs_10': gain,
        'lost_success_events_complete_pairs_10': loss,
        'sum_net_success_events_complete_pairs_10': gain-loss,
        'sum_parent_failed_tasks_complete_pairs_10': sum(10-r['parent_successes_10'] for r in available),
        'sum_parent_success_tasks_complete_pairs_10': sum(r['parent_successes_10'] for r in available),
        'mean_net_successes_complete_pairs_10': float(Fraction(gain-loss,len(available))) if available else None,
        'new_success_fraction_among_parent_failures_complete_pairs': float(Fraction(gain,sum(10-r['parent_successes_10'] for r in available))) if available and sum(10-r['parent_successes_10'] for r in available) else None,
        'lost_success_fraction_among_parent_successes_complete_pairs': float(Fraction(loss,sum(r['parent_successes_10'] for r in available))) if available and sum(r['parent_successes_10'] for r in available) else None,
    }

def analyze():
    start = time.perf_counter()
    subsets = {n: set(json.loads((BASE/'official_repository/swe_bench/subsets'/f'{n}.json').read_text())) for n in ('small','medium','big')}
    assert [len(subsets[n]) for n in ('small','medium','big')] == [10,50,140]
    assert not (subsets['small'] & subsets['medium'] or subsets['small'] & subsets['big'] or subsets['medium'] & subsets['big'])
    small = subsets['small']; sixty = small | subsets['medium']
    allrows=[]; results={}; file_bindings=[]
    for run in sorted((BASE/'released_metadata').iterdir()):
        if not run.is_dir(): continue
        metas={p.parent.name:json.loads(p.read_text()) for p in sorted(run.glob('*/metadata.json'))}
        for p in sorted(run.rglob('*')):
            if p.is_file(): file_bindings.append({'path':str(p.relative_to(BASE)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        gens=stream_json(run/'dgm_metadata.jsonl'); rows=[]; known_archive={'initial'}; seen_ids=set(); anomalies=[]
        native_parent_scores={}
        for node, meta in metas.items():
            perf=meta.get('overall_performance') or {}; yes,no=outcome(meta)
            native_parent_scores[node]=perf.get('accuracy_score')
            if perf and perf.get('total_submitted_instances') != len(yes|no):
                anomalies.append({'node':node,'declared_submitted':perf.get('total_submitted_instances'),'enumerated_task_ids':len(yes|no)})
        for gen in gens:
            scheduled=Counter(tuple(x) for x in gen['selfimprove_entries'])
            matched=Counter()
            previous_best=max(len(outcome(metas[n])[0]&small) for n in known_archive if len((outcome(metas[n])[0]|outcome(metas[n])[1])&small)==10)
            for node in gen['children']:
                assert node not in seen_ids; seen_ids.add(node)
                assert node in metas, ('Missing child metadata',node)
                meta=metas[node]; parent=meta['parent_commit']; assert parent in known_archive
                matched[(parent,meta.get('entry'))]+=1
                cy,cn=outcome(meta); py,pn=outcome(metas[parent]); cy10=cy&small; py10=py&small
                cu=small-(cy|cn); pu=small-(py|pn)
                depth=0; ancestor=node; visited=set()
                while ancestor!='initial':
                    assert ancestor not in visited; visited.add(ancestor); depth+=1; ancestor=metas[ancestor]['parent_commit']
                rows.append({
                    'run':run.name,'attempt_ordinal':len(rows)+1,'generation':gen['generation'],
                    'child':node,'parent':parent,'depth':depth,'entry':meta.get('entry'),
                    'native_admitted':node in gen['children_compiled'],
                    'child_performance_available':bool(meta.get('overall_performance')),
                    'parent_native_accuracy':native_parent_scores[parent],
                    'child_native_accuracy':native_parent_scores[node],
                    'parent_successes_10':len(py10),'child_successes_10':len(cy10),
                    'parent_unknown_10':len(pu),'child_unknown_10':len(cu),
                    'pair_fully_observed_10':not (pu or cu),
                    'verified_gain_10':len(cy10)>len(py10)+len(pu),
                    'definitely_worse_10':len(cy10)+len(cu)<len(py10),
                    'gain_tasks_10':len(cy10-py10) if not (pu or cu) else None,
                    'loss_tasks_10':len(py10-cy10) if not (pu or cu) else None,
                    'prior_archive_best_10':previous_best,
                    'verified_record_10':len(cy10)>previous_best,
                    'parent_successes_60':len(py&sixty),'child_successes_60':len(cy&sixty),
                    'parent_unknown_60':len(sixty-(py|pn)),'child_unknown_60':len(sixty-(cy|cn)),
                    'verified_gain_60':len(cy&sixty)>len(py&sixty)+len(sixty-(py|pn)),
                    'observed_child_passes_absent_from_reported_parent_passes_10':sorted(cy10-py10),
                    'lost_task_ids_10':sorted(py10-cy10) if not (pu or cu) else [],
                })
            assert matched == scheduled, ('Unmatched scheduled attempt',run.name,gen['generation'],scheduled,matched)
            known_archive.update(gen['children_compiled'])
            assert known_archive == set(gen['archive'])
        unused=set(metas)-seen_ids-{'initial'}; assert not unused, unused
        byscore={str(s):summary([r for r in rows if r['parent_successes_10']==s]) for s in sorted({r['parent_successes_10'] for r in rows})}
        bydepth={str(s):summary([r for r in rows if r['depth']==s]) for s in sorted({r['depth'] for r in rows})}
        best_native=max(sorted(known_archive),key=lambda n:native_parent_scores[n])
        lineage=[]; node=best_native
        while node!='initial':
            row=next(r for r in rows if r['child']==node)
            lineage.append({k:row[k] for k in ('child','parent','generation','depth','parent_native_accuracy','child_native_accuracy','parent_successes_10','child_successes_10','child_unknown_10','gain_tasks_10','loss_tasks_10','prior_archive_best_10','verified_record_10')}); node=metas[node]['parent_commit']
        lineage.reverse()
        results[run.name]={
            'scheduled_attempts':sum(len(g['selfimprove_entries']) for g in gens),
            'returned_children':len(rows),'generations':len(gens),
            'all_attempts':summary(rows),'first_80_attempts':summary(rows[:80]),
            'parent_score_strata_10':byscore,'lineage_depth_strata':bydepth,
            'attempt_half_strata':{'first_half':summary(rows[:len(rows)//2]),'second_half':summary(rows[len(rows)//2:])},
            'declared_vs_enumerated_task_count_discrepancies':anomalies,
            'native_score_max_admitted':native_parent_scores[best_native],
            'native_best_agent':best_native,'native_best_lineage':lineage,
            'native_admitted_children_count':len(known_archive)-1,
            'unique_10_task_successes_ever_observed':len(set().union(*(outcome(m)[0]&small for m in metas.values()))),
            'max_observed_10_successes':max(len(outcome(m)[0]&small) for m in metas.values()),
            'initial_successes_10':len(outcome(metas['initial'])[0]&small),
            'verified_gains_60':sum(r['verified_gain_60'] for r in rows),
            'children_with_at_least_57_known_60_task_outcomes':sum(60-r['child_unknown_60']>=57 for r in rows),
        }; allrows.extend(rows)
    out={'scope':'Retrospective descriptive reanalysis; no new DGM execution or causal identification.',
         'common_task_set':'Official small.json, 10 exact IDs; initial scores are 3/10 in each run.',
         'missingness':'Unenumerated outcomes remain unknown. No observation of a verified gain is not proof of no true gain.',
         'comparison_limits':'Adaptive parent/task selection, shared ancestry, uneven evaluation tiers, single run per condition, producer/workspace confounding and unmeasured per-attempt total cost.',
         'runs':results,'source_bindings':file_bindings}
    (BASE/'ROOT_LINEAGE_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    with (BASE/'ROOT_ATTEMPT_ROWS.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(allrows[0]));w.writeheader()
        for row in allrows:
            w.writerow({k:json.dumps(v) if isinstance(v,list) else v for k,v in row.items()})
    (BASE/'ROOT_ANALYSIS_COST.json').write_text(json.dumps({'elapsed_seconds':time.perf_counter()-start,'counted_attempts':len(allrows),'model_calls':0,'paid_services':0,'discovery_inference_time':'unmeasured'},indent=2)+'\n')
    print(json.dumps({n:{'all_attempts':r['all_attempts'],'first_80_attempts':r['first_80_attempts'],'parent_score_strata_10':r['parent_score_strata_10'],'native_best_lineage':r['native_best_lineage']} for n,r in results.items()},indent=2))

if __name__=='__main__': analyze()
