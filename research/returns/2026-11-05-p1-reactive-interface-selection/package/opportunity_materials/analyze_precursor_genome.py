import json,collections
from pathlib import Path
p=Path(__file__).parent;d=json.loads((p/'precursor_genome_ledger.json').read_text()); ss=d['samples'];s=ss[0]
sc=s['characterization']['xrd']['scans'][0]
r={}
r['samples']=len(ss)
r['unique_precursors']=sorted({x['formula'] for s in ss for x in (s.get('precursors') or [])})
r['precursor_pair_counts']=dict(collections.Counter(len(s.get('precursors') or []) for s in ss))
r['duplicate_unordered_pairs']=len(ss)-len({tuple(sorted(x['formula'] for x in s.get('precursors') or [])) for s in ss})
r['null_synthesis']=sum(s.get('synthesis') is None for s in ss)
r['null_outcome']=sum(s.get('outcome') is None for s in ss)
r['categories']=dict(collections.Counter((s.get('outcome') or {}).get('reaction_category') for s in ss))
r['holding_times']=dict(collections.Counter((s.get('synthesis') or {}).get('heating_time') for s in ss))
r['temperatures']=dict(collections.Counter((s.get('synthesis') or {}).get('heating_temperature') for s in ss))
r['has_actual_temperature_profile']=sum(bool((s.get('synthesis') or {}).get('temperature_profile')) for s in ss)
r['negative_mass_for_xrd']=[s['sample_id'] for s in ss if ((s.get('synthesis') or {}).get('mass_for_xrd_mg') or 0)<0]
r['negative_recovered_mass']=[s['sample_id'] for s in ss if ((s.get('synthesis') or {}).get('mass_recovered_mg') or 0)<0]
scs=[sc for s in ss for sc in ((s.get('characterization') or {}).get('xrd') or {}).get('scans',[])]
cs=[c for sc in scs for c in sc.get('refinement_cases',[])]
r['number_scans']=len(scs);r['number_refinements']=len(cs)
r['scan_counts_per_sample']=dict(collections.Counter(len(((s.get('characterization') or {}).get('xrd') or {}).get('scans',[])) for s in ss))
r['accepted_case_counts']=dict(collections.Counter(str((c.get('verification') or {}).get('is_accepted')) for c in cs))
r['rwp_missing']=sum(c.get('rwp') is None for c in cs)
r['rwp_min']=min(float(c['rwp']) for c in cs if c.get('rwp') is not None);r['rwp_max']=max(float(c['rwp']) for c in cs if c.get('rwp') is not None)
r['quality_score_counts']=dict(collections.Counter(str((c.get('verification') or {}).get('human_quality_score')) for c in cs))
r['multiple_active_scans']=sum(sum(bool(sc.get('is_active')) for sc in ((s.get('characterization') or {}).get('xrd') or {}).get('scans',[]))>1 for s in ss)
print(json.dumps(r,indent=2));(p/'precursor_genome_summary.json').write_text(json.dumps(r,indent=2))
