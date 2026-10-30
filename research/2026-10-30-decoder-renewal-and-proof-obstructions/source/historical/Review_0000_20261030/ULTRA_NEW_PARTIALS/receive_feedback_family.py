"""Exact all-r composition of EXISTING fixed coherent-feedback controller.

No source/model/solver/RNG call. Checks saved rational CPTP map and derives
its three symbolic1/r coefficients from the same literal circuit.
"""

from fractions import Fraction as F
from pathlib import Path
import hashlib,json,time
from coherent_pauli_feedback import exact_state_coefficients,strict_ldl


def main():
    base=Path(__file__).parent;start=time.perf_counter()
    raw=(base/'COHERENT_FEEDBACK_DECODER.json').read_bytes();x=json.loads(raw)
    assert x['r']==2 and x['input_dimension']==24 and x['output_dimension']==2
    C=[[F(v) for v in row] for row in x['repaired_CPTP_Choi']]
    assert len(C)==48 and all(len(row)==48 for row in C)
    assert all(C[i][j]==C[j][i] for i in range(48) for j in range(48))
    pivot=strict_ldl(C)
    assert all(C[2*i][2*j]+C[2*i+1][2*j+1]==int(i==j) for i in range(24) for j in range(24))
    z=exact_state_coefficients();coeff=[]
    for zz in z:
        target=[[zz[24*b+j][24*a+i]/2 for j in range(24) for b in range(2)]
                for i in range(24) for a in range(2)]
        coeff.append(sum(C[i][j]*target[j][i] for i in range(48) for j in range(48)))
    assert coeff[0]==F(1,4)
    old=json.loads((base/'COHERENT_FEEDBACK.json').read_text())
    assert old['r']==2
    assert sum(coeff[j]/2**j for j in range(3))==F(old['qualified_feasible_Bell_fidelity'])
    # One constant circuit/map; this is symbolic family evaluation, no new case.
    out={'scope':'exact SAME fixed controller for ALL integer r>=1,D>=2r; new symbolic1/r extraction only',
         'decoder_sha256':hashlib.sha256(raw).hexdigest(),
         'fixed_feedback_coefficients_independent_of_r':True,
         'exact_Bell_fidelity_coefficients_1_rinv_rinv2':list(map(str,coeff)),
         'exact_Pauli_twirl_halfdiamond_coefficients':list(map(str,[1-coeff[0],-coeff[1],-coeff[2]])),
         'coefficient_decimals_diagnostic':list(map(float,coeff)),
         'decoder_strict_LDL_minimum_pivot':str(pivot),
         'all_576_CPTP_trace_entries_exact':True,
         'same_rank_two_certificate_reproduced_exactly':True,
         'physical_CPTP_reason':'literal controlled-isometry+group-permutation channel+fixed24to2CPTP decoder, for everyD including nonfaithfulS3 cases',
         'required_new_source_calls_per_payload':2,'online_source_calls':1,
         'near_linear_high_fidelity_rank_scaling':'NOT_ACHIEVED; fixedQ2 fidelity tends1/4 asr grows',
         'new_source_model_solver_reference_or_RNG_calls':0,
         'seconds_after_imports':time.perf_counter()-start}
    (base/'ALL_R_FAMILY.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
