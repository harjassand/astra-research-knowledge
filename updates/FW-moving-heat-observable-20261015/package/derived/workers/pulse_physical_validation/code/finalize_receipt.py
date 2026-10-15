from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parents[1]
def read(name):return json.loads((BASE/'results'/name).read_text())
a=read('acquisition_audit.json');g=read('paired_gate.json');h=read('hybrid_baseline.json')
l=read('joint_lp.json');q=read('joint_target_queries.json');c=read('check_results.json')
receipt={'worker':'pulse_physical_validation','date':'2026-10-15',
 'mission_status':'NOT_ACHIEVED',
 'original_data_acquisition':'SUCCESS_MD5_VERIFIED',
 'physical_validation':'NOT_PERFORMED_CURRENT_AND_INITIAL_STATE_INTERFACE_INCOMPLETE',
 'conditional_model_transfer':'REJECTED_FOR_ALL_92_CELLS_UNDER_EXPLICIT_PREMISES',
 'incumbent':'PINNED_ORIGINAL_HYBRID_DRT_EXECUTED; NO_SUPERIORITY_CLAIM',
 'new_operation':'Paired opposite-pulse increment ordering/concavity gate independent of unknown common current amplitude and full positive relaxation continuum',
 'original_measurement_bytes':a['original_data_total_bytes'],
 'supplied_EIS_row_verified_against_original':a['supplied_first_EIS_row_exactly_matches_original'],
 'acquired_current_trace':False,'acquired_capacity_reference_Ah':False,
 'actual_initial_relaxation_controlled':False,'noise_budget_calibrated':False,
 'cell_001_gate_error_floor_mV':g['cell_001']['minimum_per_endpoint_uniform_error_mV'],
 'all_92_gate':g['all_92'],
 'gate_premises':g['premises'],
 'gate_error_meaning':'Error of baseline-referenced endpoint voltage increments under the listed ideal-current/common-state assumptions. Not an instrument-voltage error confidence bound.',
 'full_band_ordering_cell_001':read('fullband_ordering.json')['cell_001'],
 'joint_LP_runs':l['runs'],'joint_LP_elapsed_s':l['elapsed_s'],
 'joint_target_queries':q,
 'actual_upstream_runs':h['runs'],
 'upstream_hybrid_commit':'e01dba1bf5f02fa6b63c82169c0652a5a695344d',
 'upstream_mittag_leffler_commit':'6e875fa3e124d25420fd791e4e742d67599d94a7',
 'upstream_source_modified':False,
 'heldout_caveat':'Discharge voltage excluded from parameter fitting, but used for switching-bracket alignment and its baseline. Current amplitude inferred from positive training data; not a prospective physical test.',
 'verification':c,
 'novelty':'UNESTABLISHED',
 'disposition':'Retain acquired data and conditional transfer gate; do not promote a validated scientific response operation.',
 'artifacts':{'report':str(BASE/'REPORT.md'),'figure':str(BASE/'results/paired_pulse_boundary.png'),
   'gate':str(BASE/'results/paired_gate.json'),'incumbent':str(BASE/'results/hybrid_baseline.json'),
   'verification':str(BASE/'results/check_results.json')},
 'resource_scope':'Original data+source archives below40MB. Library downloads, acquisition elapsed, full-pipeline peak memory and instrument collection costs not measured together.'}
(BASE/'RECEIPT.json').write_text(json.dumps(receipt,indent=2,allow_nan=False))
entries=[]
for p in sorted(BASE.rglob('*')):
 if not p.is_file() or p.name=='MANIFEST.json':continue
 rel=p.relative_to(BASE)
 if any(x in ['__pycache__','build'] or x.endswith('.egg-info') for x in rel.parts):continue
 b=p.read_bytes();entries.append({'path':str(rel),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'algorithm':'SHA256','excluded':'MANIFEST itself, Python caches, upstream local build directories and egg-info',
          'files':entries,'file_count':len(entries),'total_bytes':sum(r['bytes'] for r in entries)}
(BASE/'MANIFEST.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({'receipt':str(BASE/'RECEIPT.json'),'manifest_file_count':len(entries),
                  'manifest_bytes':manifest['total_bytes'],'status':receipt['mission_status']}))
