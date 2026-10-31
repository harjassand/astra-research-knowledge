#!/usr/bin/env python3
"""Compare acquired clocks on the exact previous two-inactive network, not just dimensions."""
from verify_protected import *
import time

def main():
    old_path=HERE.parents[1]/'stochastic_nonlinear_boundary_20261031/independent_audit/two_inactive_results.json'
    old=json.loads(old_path.read_text());raw=[(tuple(s),tuple(t),F(k)) for s,t,k in old['raw_reactions']]
    start=time.monotonic();rec,cert,row=run_case('same_previously_audited_two_inactive_network',old['raw_species'],raw)
    elapsed=time.monotonic()-start
    assert cert['activation_clock']['clock_linear_system_dimension']==4
    assert cert['R']==old['case']['R']==3 and len(cert['head_states'])==old['case']['inactive_head_states']==6
    print(json.dumps({'exact_same_raw_network':True,'prior_receipt_sha256':hashlib.sha256(old_path.read_bytes()).hexdigest(),
       'candidate_source_sha256':hashlib.sha256((HERE/'frozen_protected_boundary.py').read_bytes()).hexdigest(),
       'case':row,'previous_clock_dimension':old['clock_dimension'],'protected_clock_dimension':4,
       'previous_clock_fraction_bits':old['clock_fraction_bits'],'protected_clock_fraction_bits':cert['activation_clock']['largest_clock_fraction_bits'],
       'protected_clock_means':cert['activation_clock']['clock_hitting_means'],
       'protected_uniform_activation_bound':cert['activation_clock']['uniform_activation_mean_upper'],
       'elapsed_seconds_observed':elapsed,'not_a_uniform_complexity_benchmark':True},default=p.encode,indent=2))

if __name__=='__main__':main()
