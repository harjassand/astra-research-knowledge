"""Reproducible two-component acquisition; native source separated from learner."""
import json,time,hashlib
from pathlib import Path
from fractions import Fraction as Q
from acquisition import plan,propose,certify
from native import fixture,acquire


def write(path,value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def main():
    root=Path(__file__).resolve().parent
    output=root/'results';output.mkdir(exist_ok=True)
    summary=[]
    for which,label in enumerate(['component_A','component_B']):
        begin=time.perf_counter()
        contract=plan(3,Q(1),Q(2),Q(1,4),Q(1,8))
        source=fixture(which)
        record,native_cost=acquire(contract,source)
        native_seconds=time.perf_counter()-begin
        write(output/(label+'_port_record.json'),record)
        write(output/(label+'_native_cost.json'),native_cost)
        # Only the public contract and paid port record enter these calls.
        fitting_start=time.perf_counter()
        model=propose(record)
        proposal_seconds=time.perf_counter()-fitting_start
        checking_start=time.perf_counter()
        certificate=certify(record,model)
        checking_seconds=time.perf_counter()-checking_start
        model['certificate']=certificate
        model['record_sha256']=hashlib.sha256((output/(label+'_port_record.json')).read_bytes()).hexdigest()
        write(output/(label+'_model.json'),model)
        row={'component':label,'native_seconds':native_seconds,
             'proposal_seconds':proposal_seconds,'checking_seconds':checking_seconds,
             'native_dimension':native_cost['native_dimension'],
             'trials':contract['real_trials'],'scalar_readouts':contract['scalar_readouts'],
             'frequencies':contract['frequency_count'],
             'retained_states':certificate['state_dimension'],
             'certificate_error':float(Q(certificate['operator_error'])),
             'sample_error_max':float(Q(certificate['sample_error_max'])),
             'coverage_error':float(Q(certificate['all_frequency_coverage_error'])),
             'residue_trace_mass':float(Q(certificate['residue_trace_mass'])),
             'inverse_error_max':float(Q(certificate['inverse_error_max'])),
             'candidate_variables':model['proposal_variables'],
             'candidate_inequalities':model['proposal_inequalities'],
             'general_SDP_fallback':'proved, not executed'}
        summary.append(row)
        print(json.dumps(row),flush=True)
    write(output/'acquisition_summary.json',summary)


if __name__=='__main__':main()
