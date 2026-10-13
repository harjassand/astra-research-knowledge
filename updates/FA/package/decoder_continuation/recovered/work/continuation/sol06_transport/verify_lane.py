#!/usr/bin/env python3
"""Artifact integrity/scope verifier, not a scientific validity test."""
from pathlib import Path
import hashlib
import json
import time

HERE=Path(__file__).resolve().parent
tic=time.perf_counter()
pins=json.loads((HERE/'SOURCE_PINS.json').read_text())['files']
for p in pins:
    copied=Path(p['copy'])
    assert copied.is_relative_to(HERE)
    assert hashlib.sha256(copied.read_bytes()).hexdigest()==p['sha256']
claims=json.loads((HERE/'CLAIMS.json').read_text())
for c in claims['claims']:
    for e in c['evidence']:
        assert (HERE/e).is_file(),(c['id'],e)
checks=json.loads((HERE/'decisive_checks.json').read_text())
for script,result,receipt in [('decisive_checks.py','decisive_checks.json','COMPUTATION_RECEIPT.json'),
                              ('pivot_checks.py','pivot_checks.json','PIVOT_RECEIPT.json')]:
    r=json.loads((HERE/receipt).read_text())
    assert r['script_sha256']==hashlib.sha256((HERE/script).read_bytes()).hexdigest()
    assert r['result_sha256']==hashlib.sha256((HERE/result).read_bytes()).hexdigest()
sources=json.loads((HERE/'sources/receipts.json').read_text())
for s in sources:
    if s['status']=='downloaded primary HTML':
        assert hashlib.sha256((HERE/'sources'/f"{s['name']}.html").read_bytes()).hexdigest()==s['sha256']
assert claims['mission_status']=='NOT_ACHIEVED' and not claims['physical_validation']
assert checks['corrected_low_flow_passive_W'] < .199
assert checks['mechanical_frequency_gate']['continuum_lower_bound_first_zero_reactance_hz'] > 64
assert checks['data_nonidentifiability_witness']['q_at_every_used_raw_source_frequency_exactly_one']
assert checks['data_nonidentifiability_witness']['q_at_all_standing_modes_exactly_zero']
costs={
    'scope':'Physical costs unacquired; no zero-cost substitutions. Counts are this lane only.',
    'physical':{'fabrication':None,'material_acquisition':None,'calibration':None,
                'full_loaded_pipe_measurement':None,'driver_idle_and_conversion_W':None,
                'support_impedance_and_fatigue_cost':None,'pump_electrical_efficiency_acquired':False,
                'film_preparation_and_maintenance':None,'clearing_and_product_quality_validation':None},
    'saved_conditional_device_W':{k:checks['preferred_saved_case'][k] for k in
          ['axial_fluid_power_W','cross_fluid_power_W','structural_loss_W','actuator_copper_loss_W','total_electric_before_idle_W']},
    'saved_assumed_pump_efficiency':.7,
    'saved_inventory_L':checks['passive_controls_at_same_flow'][0]['inventory_L'],
    '250L_cap_extra_loss_budget_W':checks['impedance_gate']['acceptance_gates'][1]['driver_extra_budget_at_saved_model_Z_W'],
    'source_html_downloads':len([s for s in sources if s['status']=='downloaded primary HTML']),
    'source_html_bytes':sum(s.get('bytes',0) for s in sources),
    'inherited_copied_files':len(pins),'inherited_copied_bytes':sum(p['bytes'] for p in pins),
    'final_bounded_fluid_and_comparator_run_seconds':checks['seconds'],
    'all_four_diagnostic_run_seconds_from_transcript':[1.3487160420045257,1.5035423329973128,1.5761913329770323,1.3852783750044182],
    'standing_mode_search_repeated':False,'hardware_runs':0,'paid_compute_jobs':0,
    'children_spawned':0,'commits':0,'external_messages':0,
    'source_acquisition_history':'Inherited PDFs/ZIP and original rheometer experiments are supplied inputs; their original acquisition/fabrication/experiment costs are unknown, not claimed free.'}
(HERE/'COSTS.json').write_text(json.dumps(costs,indent=2)+'\n')
receipt={'status':'passed','scope':'source-copy, JSON-reference and computation-receipt integrity only; not scientific validation',
         'claims':len(claims['claims']),'source_copies_checked':len(pins),
         'source_html_checked':len(sources),'seconds':time.perf_counter()-tic}
(HERE/'FINAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
