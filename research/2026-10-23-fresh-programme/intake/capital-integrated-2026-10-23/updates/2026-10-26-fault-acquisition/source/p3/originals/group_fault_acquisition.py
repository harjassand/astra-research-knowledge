"""Robust reconstruction when faults affect entire measurement instruments.

Exactly five independently fallible devices; each reports 11 relative
contrasts. Two devices may corrupt ALL their reported scalars without bounds.
A matching 55-output lower bound holds for universal recovery when exactly
five device groups are available under this observation grammar.
"""
from fractions import Fraction as F
from pathlib import Path
import json
from fault_tolerant_acquisition import (ROOT,N,physical,Envelope,future_tests,enc,
    graph,group_fault_failure)

NDEV=5
BAD={1,4}

def execute():
    exact=[physical(v)-physical(0) for v in range(1,N)]
    data=[]
    for dev in range(NDEV):
        reports=[]
        for v in range(1,N):
            q=exact[v-1]
            if dev==1:q+=F(7*v+11,3)
            if dev==4:q-=F(13*v+3,5)
            reports.append(q)
        data.append(reports)
    assert all(data[g]!=exact for g in BAD)
    out=[F(0)]*N
    for v in range(1,N):
        vals=sorted(data[dev][v-1] for dev in range(NDEV))
        out[v]=vals[2]
    assert all(out[v]==physical(v)-physical(0) for v in range(N))
    env=Envelope(out,[F(0)]*N)
    env.validate()
    tasks=future_tests(env,'five independently fallible instrument groups, two arbitrary bad groups')
    return {'physical_instrument_group_calls':NDEV,
            'returned_scalars_per_call':N-1,'total_returned_scalars':NDEV*(N-1),
            'arbitrarily_corrupt_instrument_groups':sorted(BAD),
            'synthetic_report_groups':data,'exact_recovered_relative_values':out,
            'per_port_median_of_five_device_reports':True,
            'future_tasks':tasks,
            'information_optimum_for_exactly_five_devices':'Any cut must be crossed by at least five distinct device groups. With only five groups, each group subgraph must cross every cut and hence be connected; therefore at least n-1=11 readings per group, 55 total. Five anchored spanning stars attain this bound.',
            'scope':'Requires entire group fault status shared across one instrument and at most 2 of 5 instrument groups faulty. Independent instruments, stable source and genuine difference sensors are externally supplied.'}

def group_corruption_counterexample():
    """A five-edge-connected graph is not robust when one device owns 5 edges."""
    g=graph();example=group_fault_failure(g)
    delta=example['adversarial_single_group_shift']
    actual0=[F(0)]*N
    actual1=[F(0)]*N;actual1[0]=delta
    # Every nonincident edge has identical readings under both sources.
    incident={tuple(sorted(e)) for e in g.edges(0)}
    readings={}
    for u,v in g.edges:
        e=tuple(sorted((u,v)))
        readings[e]=actual1[e[1]]-actual1[e[0]]
        if e not in incident:
            assert readings[e]==actual0[e[1]]-actual0[e[0]]
    return {'one_bad_group_edges':sorted(incident),
            'first_source_zero_vector':actual0,'second_source_shifted_root_vector':actual1,
            'same_reports_achievable_with_one_corrupt_group_or_zero_corrupt_groups':True,
            'latent_relative_separation':delta,
            'correctness_boundary':'Five edge-disjoint paths do not protect against one hardware fault shared by every path.'}

def run():
    case=execute();counter=group_corruption_counterexample()
    result={'group_robust_operation':case,
            'edge_connectivity_insufficient_for_group_faults':counter,
            'conditional_minimum_sensor_channels':5,
            'minimum_scalar_readings_for_exactly_five_independent_groups':55,
            'group_robustness_requiring_2f_plus_1_independent_groups':True,
            'same_information_alternative':'Median-of-five independent device batches is standard robust aggregation and ties this procedure.'}
    (ROOT/'group_fault_acquisition_results.json').write_text(json.dumps(enc(result),indent=2)+'\n')
    print('Group-robust exact recovery:',case['physical_instrument_group_calls'],'calls,',case['total_returned_scalars'],'scalars',flush=True)
    print('Faulty groups:',case['arbitrarily_corrupt_instrument_groups'],
          'later tasks:',case['future_tasks']['count'],
          'mean radius:',float(case['future_tasks']['mean_certified_radius']),flush=True)
    print('Five-edge connectivity not enough for one grouped failure: certified counterexample',flush=True)
    return result

if __name__=='__main__':run()
