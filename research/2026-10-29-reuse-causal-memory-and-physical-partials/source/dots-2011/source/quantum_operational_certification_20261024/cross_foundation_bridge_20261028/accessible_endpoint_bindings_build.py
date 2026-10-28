#!/usr/bin/env python3
"""Bind local scientific endpoint sources, received imports and exact checks."""
from pathlib import Path
from hashlib import sha256
import json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
def digest(p):return sha256(p.read_bytes()).hexdigest()
names=[
'ACCESSIBLE_ENDPOINT_RATIONAL_SDP_AND_COMPILER.md',
'ACCESSIBLE_ENDPOINT_RATIONAL_SDP_AND_COMPILER_initial.md',
'ACCESSIBLE_ENDPOINT_RATIONAL_SDP_AND_COMPILER_pre_explicit_qr.md',
'accessible_endpoint_exact_checks.py','accessible_endpoint_exact_checks.json',
'accessible_endpoint_exact_checks.log','accessible_endpoint_exact_checks_initial.py',
'accessible_endpoint_exact_checks_initial_failure.log','accessible_endpoint_bindings_build.py',
]
deps=[
'SIGNED_CORE_COMPLETE_SERVICE_PREDICTION.md',
'SIGNED_CORE_COMPLETE_SERVICE_INDEPENDENT_AUDIT.md',
'SIGNED_CORE_COMPLETE_SERVICE_INDEPENDENT_RECEIPT.json',
'IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY.md',
'IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY_INDEPENDENT_AUDIT.md',
'IC_PORT_SHORT_DEPTH_COMPLETE_RECOVERY_INDEPENDENT_RECEIPT.json',
]
outer=[
'ordinary_local_mixed_gauge_cptp_erm_addendum_20261028.md',
'ordinary_local_mixed_gauge_cptp_erm_addendum_20261028_independent_audit.md',
'ordinary_local_mixed_gauge_cptp_erm_addendum_20261028_independent_receipt.json',
'ordinary_local_mixed_gauge_cptp_erm_addendum_controls_audit_20261028.md',
'ordinary_local_mixed_gauge_cptp_erm_addendum_controls_receipt_20261028.json',
'single_copy_pair_pauli_finite_operation_budget.md',
'single_copy_pair_pauli_finite_operation_budget_independent_audit.md',
'single_copy_pair_pauli_finite_operation_budget_independent_receipt.json',
'ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md',
'ordinary_one_sided_effect_finite_positive_cost_rounding_statistics_receipt_20261028.json',
]
check=json.loads((HERE/'accessible_endpoint_exact_checks.json').read_text())
assert check['source_sha256']==digest(HERE/names[0])
assert check['script_sha256']==digest(HERE/'accessible_endpoint_exact_checks.py')
assert digest(HERE/'accessible_endpoint_exact_checks.json')==digest(HERE/'accessible_endpoint_exact_checks.log')
files={str((HERE/n).relative_to(ROOT)):digest(HERE/n) for n in names+deps}
files.update({n:digest(ROOT/n) for n in outer})
out={
 'status':'AUTHOR_CONSTRUCTION_AND_CHECK_BINDINGS_NOT_AN_INDEPENDENT_RECEIPT',
 'date_utc':'2026-10-28',
 'source_sha256':digest(HERE/names[0]),
 'scientific_scope':'Finite rational accessible p-to-k service projection, k-to-p unrestricted CPTP recovery, explicit rounded-ellipsoid separation interface, exact rational repair and finite-bit known decoder synthesis.',
 'core_source_role':'Application/dependency reference only; this endpoint theorem starts from rational signed service Choi data and its certified complete error.',
 'selective_received_imports':'Known Choi/Kraus and gap-free finite matrix arithmetic; no acquisition/rate theorem imported from these decoder-control sources.',
 'source_calls':0,'episode_starts':0,'random_draws':0,'hardware_executions':0,
 'generic_ellipsoid_solver_executed':False,
 'generic_SDP_solver_executed':False,
 'restricted_exact_Pauli_endpoint_optimizer_executed':True,
 'exact_small_QR_completions_executed':True,
 'finite_gate_compiler_executed':False,
 'source_edited_by_reviewer':False,
 'known_corrections_preserved':[
  'Initial source and pre-explicit-QR source snapshots.',
  'Initial diagnostic used SymPy structural Hermiticity equality; corrected to exact simplified difference. Initial script and failure log preserved.',
  'Explicit QR/precision mechanism replaces unsupported quantitative completion import.',
  'SK compressed recursion counts are distinguished from expanded output and from finite-bit arithmetic; guarded finite-bit proof supplied separately.',
 ],
 'primary_sources':[
  'https://ir.cwi.nl/pub/10046/10046D.pdf',
  'https://cs.uwaterloo.ca/~watrous/Papers/SimplerSDPforCBnorm.pdf',
  'https://arxiv.org/pdf/quant-ph/9503016',
  'https://arxiv.org/pdf/quant-ph/0505030',
 ],
 'files':files,
}
target=HERE/'accessible_endpoint_source_bindings.json'
target.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'file':target.name,'sha256':digest(target),'bindings':len(files),
                  'source_sha256':out['source_sha256']},indent=2))
