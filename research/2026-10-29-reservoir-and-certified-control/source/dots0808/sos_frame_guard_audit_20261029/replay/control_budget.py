import sys,json,numpy as np
from pathlib import Path
P=Path(__file__).parent;Q=P/'received_dependencies';sys.path[:0]=[str(Q/'compiled_payload_outer_bridge_20261029'),str(Q/'outer_grs_distillation_20261028')]
from direct_outer_checks_v1 import outer_encoder
from grs_wrapper_v1 import GF,construct
from algebra_compiler_v1 import gate_rows
g=GF(5,37);c=construct(g,31,6);gs,gram=outer_encoder(g,c);counts={k:sum(x[0]==k for x in gs) for k in ['CX','SW','H','S']};cn=counts['CX']+3*counts['SW'];labels=np.eye(310,dtype=np.uint8)
for gate in gs+gs[::-1]:gate_rows(labels,gate,155)
assert np.array_equal(labels,np.eye(310,dtype=np.uint8))
rows=[]
for candidate in json.loads((P/'results.json').read_text())['rows']:
 for r in candidate['guard_results']:
  # Matching can use the same completed logical Pauli service; conservative raw good
  # subbranch retained for its soundness ledger. No extra physical permutation charge.
  percall=r['s']*16+(1-r['s'])*(4 if r['test']=='matching' else 16)
  inner=percall*r['expected_native_calls'];outer=cn*(1+r['acceptance'])
  rows.append({'candidate':candidate['candidate_policy'],'test':r['test'],'expected_inner_CNOT':inner,'outer_encoder_CNOT_per_attempt':cn,'outer_decoder_CNOT_on_accept':cn,'expected_inner_plus_outer_CNOT':inner+outer,'accepted_payload_per_expected_CNOT':r['expected_accepted_payload']/(inner+outer)})
res={'scope':'Ideal circuit accounting, no hardware error/latency guarantee. Eight-CNOT four-spin encoder and inverse, matching singlet prepare/read4CNOT/test; all controllers can use cheap logical Pauli service twirl. Four learned local frame singles per direction additional. Outer encoded beforeguard, inverse only onaccept. Exact source exposure and gatecount are different metrics.','outer_encoder_gates':len(gs),'outer_encoder_counts':counts,'outer_encoder_CNOT_after_SWAP_expansion':cn,'data_buffer_qubits':155,'active_service_peak_ignoring_classical_controls':158,'active_test_peak_with_buffer':159,'inverse_binary_action_checked':True,'rows':rows}
(P/'control_budget.json').write_text(json.dumps(res,indent=2)+'\n');(P/'outer_circuit.json').write_text(json.dumps({'encoder':gs,'inverse_decoder':gs[::-1],'trace_gram':gram},indent=2)+'\n');print(counts,cn)
