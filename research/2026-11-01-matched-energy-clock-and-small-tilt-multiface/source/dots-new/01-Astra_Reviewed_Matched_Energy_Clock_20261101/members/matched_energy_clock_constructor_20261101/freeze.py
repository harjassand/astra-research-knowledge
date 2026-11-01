"""Explicit source/evidence allowlist; no recursive archival discovery."""
from pathlib import Path
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parent
own=['README.md','COSTS_COMPARISONS_AND_FAILURES.md','POSITIVE_GRID_MATCHED_CONSTRUCTION.md','positive_integrals.py','acquire_derivative.py','shifted_current.py','receive_matched_clock.py','check.py','check_boundaries.py','compare_same_task.py','freeze.py','production_raw.json','small_raw.json','original_physical_task.json','matched_certificate.json','matched_producer_stdout.txt','small_certificate.json','author_checks.json','author_stdout.txt','boundary_checks.json','boundary_stdout.txt','same_task_comparison.json','positive_prices_1024_256.json','positive_prices_1024_256_stdout.txt','positive_prices_128_64.json','assembly_probe.py','assembly_probe_result.json','assembly_probe_stdout.txt','diagnostic_positive_ceiling.py','diagnostic_positive_ceiling_before_analytic_J.py','diagnostic_positive_ceiling_results.json']
for f in ['AUDIT_SHA256.json','CHECK_RESULTS.json','INPUT_SHA256.json','REVIEW.md','SOURCE_BOUND_ACCEPTANCE.md','check_positive_grid.py','received_candidate.md']:own.append('audit_positive_grid_20261101_0153/'+f)
def desc(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
old=json.loads((R/'retained_state_renewal_clock_20261101/FROZEN_SHA256_RECOVERY_V4.json').read_text());deps=dict(old['dependencies'])
for k,v in deps.items():assert desc(R/k)==v,k
for name in ['GLOBAL_ODD_MODE_AND_RENEWAL_CANDIDATE.md','FINITE_RATE_AND_SHARP_VECTOR_COROLLARY.md','CONCRETE_COMMITTOR_DOMAIN_JOIN.md','NO_GLOBAL_GAP_NOTE.md','COSTS_PRIORS_AND_BOUNDARIES.md','receive_clock.py','results.json','FROZEN_SHA256_RECOVERY_V4.json','audit_global_odd_renewal_recovery_20261101_0118/SOURCE_BOUND_ACCEPTANCE.md']:
 key='retained_state_renewal_clock_20261101/'+name;deps[key]=desc(R/key)
for key in ['audit_retained_clock_whole_recovery_20261101_0119/WHOLE_REVIEW.md','audit_retained_clock_whole_recovery_20261101_0119/AUDIT_SHA256.json','retained_clock_primary_comparison_20261101/ADDITIONAL_DISCOVERY_AND_ACCESS_BOUNDARY.md']:deps[key]=desc(R/key)
for name in ['FROZEN_FIBER_VARIATIONAL_ROOT.md','COAREA_DERIVATIVE_PRICE_ROOT.md','ODD_SLAB_SOURCE_ROOT.md','SHIFTED_BARRIER_WELL_CURRENT_ROOT.md']:
 key='matched_energy_clock_pending_20261101/'+name;deps[key]=desc(R/key)
for directory,files in [('audit_coarea_paid_trial_20261101_0131',['AUDIT_SHA256.json','CHECK_RESULTS.json','INPUT_SHA256.json','REVIEW.md','SOURCE_BOUND_ACCEPTANCE.md','check_independent.py','received_COAREA_DERIVATIVE_PRICE_ROOT.md','received_FROZEN_FIBER_VARIATIONAL_ROOT.md','received_ODD_SLAB_SOURCE_ROOT.md']),('audit_shifted_well_20261101_0137',['AUDIT_SHA256.json','CHECK_RESULTS.json','INPUT_SHA256.json','SOURCE_BOUND_ADDENDUM.md','check_shifted.py','received_candidate.md'])]:
 for name in files:
  key='matched_energy_clock_pending_20261101/'+directory+'/'+name;deps[key]=desc(R/key)
manifest={'schema':'matched_energy_clock_author_freeze.v1','status':'1036 author assertions and50 UNKNOWN checks; two additional actual production refusals; full raw production and fresh full verify PASS. Theorem receipts accepted; primitive/whole executable audit PENDING. Earlier accepted freezes unchanged.','files':{k:desc(D/k)for k in own},'dependencies':deps}
out=D/'FROZEN_SHA256.json';out.write_text(json.dumps(manifest,indent=2)+'\n');print(len(own),len(deps),desc(out))
for k,v in manifest['files'].items():assert desc(D/k)==v
for k,v in deps.items():assert desc(R/k)==v
