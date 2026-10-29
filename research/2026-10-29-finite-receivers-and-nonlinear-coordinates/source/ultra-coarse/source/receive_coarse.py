"""One acquired baseline predicts three unseen simultaneous interventions.

Coarse receiver reads only adsorption counts, vacancy-residence histogram,
bounded endpoints and known adsorption coefficients/graph envelope. It
NEVER reads the exact pair activity. The latter is used in a separately
labeled richer-access ordinary Girsanov comparator.
"""
import hashlib,json,math,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'root_vacancy_envelope'


from bounded_confidence import interval


def main():
    tic=time.perf_counter()
    model=json.loads((HERE/'COARSE_CONTRACT.json').read_text())
    graph=json.loads((ROOT/'ENVELOPE.json').read_text())
    assert graph['input_sha256']==hashlib.sha256((HERE/'PAIR_GRAPH.json').read_bytes()).hexdigest()
    rows=np.genfromtxt(HERE/'BASELINE_COARSE.csv',delimiter=',',names=True)
    rich_rows=np.genfromtxt(HERE/'BASELINE_HIST.csv',delimiter=',',names=True)
    n=len(rows);M=model['sites']
    H=np.column_stack([rows[f'Tv{v}'] for v in range(M+1)])
    v=np.arange(M+1)
    kco=model['gas_activity_upper']['CO']/M
    ko=graph['common_pair_rate']
    Aco=kco*(H@v)
    intervals={'degree':(ko*(H@np.maximum(0,4*v-2*M)),ko*(H@(2*v))),
               'exact_graph_DP':(ko*(H@np.array(graph['min_empty_edges'])),
                                  ko*(H@np.array(graph['max_empty_edges'])))}
    # Audit only: exact pair activity does not enter either coarse estimate.
    exact_pair=rich_rows['AO2']
    assert np.max(abs(Aco-rich_rows['ACO']))<1e-12
    for lo,hi in intervals.values():
        assert np.min(exact_pair-lo)>-1e-12 and np.min(hi-exact_pair)>-1e-12
    outputs=['COcoverage','Ocoverage','CO2hit']
    designs=[('HELDOUT_080_090',.8,.9),('HELDOUT_090_080',.9,.8),('HELDOUT_080_080',.8,.8)]
    reports=[]
    baseline={o:interval(rows[o],1.) for o in outputs}
    for name,a,b in designs:
        held=np.genfromtxt(HERE/(name+'.csv'),delimiter=',',names=True)
        logcount=rows['NCO']*math.log(a)+rows['NO2']*math.log(b)
        C=((1-a)*model['gas_activity_upper']['CO']+(1-b)*model['gas_activity_upper']['O2'])*model['horizon_seconds']
        B=math.exp(C)
        weights={label:(np.exp(logcount+(1-a)*Aco+(1-b)*lo),
                         np.exp(logcount+(1-a)*Aco+(1-b)*hi))
                 for label,(lo,hi) in intervals.items()}
        rich=np.exp(logcount+(1-a)*Aco+(1-b)*exact_pair)
        values={}
        for o in outputs:
            f=rows[o]
            value=dict(direct=interval(held[o],1.),full_activity=interval(f*rich,B))
            for label,(wl,wu) in weights.items():
                low=interval(f*wl,B);high=interval(f*wu,B)
                value[label]=dict(lower=max(0.,low['lower']),upper=min(1.,high['upper']),
                      lower_estimator=low,upper_estimator=high,
                      acquired_structural_mean_gap=high['mean']-low['mean'])
            value['DP_width_improvement_factor']=(value['degree']['upper']-value['degree']['lower'])/(value['exact_graph_DP']['upper']-value['exact_graph_DP']['lower'])
            values[o]=value
        reports.append(dict(name=name,CO_multiplier=a,O2_multiplier=b,
             deterministic_weight_bound=B,mean_full_activity_weight=float(np.mean(rich)),
             effective_sample_size_diagnostic=float(np.sum(rich)**2/np.sum(rich**2)),outputs=values))
    result=dict(status='ACQUIRED native-model finite-pulse predictions; not physical-data/stationary/global-regret certificate',
       baseline_episodes=n,held_out_episodes_total=3*n,baseline=baseline,queries=reports,
       coarse_input_contract='NCO,NO2 and total-vacancy residence histogram plus bounded endpoint output; graph and two adsorption coefficients; no microscopic states, exact pair activity, background rates or learned generator at receiver',
       ideal_sampling_confidence=dict(t=14,scalar_statistics=57,
             failure_upper=8*57*math.exp(-14),
             condition='exact IID native Gillespie paths and exact recorded statistics; joint union bound, no independence across query functions required'),
       numerical_scope='binary64 application/seeded PRNG diagnostic; NOT a formal finite-bit distribution or physical-model confidence certificate',
       parent_graph_cost=dict(acquisition_seconds=graph['acquisition_seconds'],verification_seconds=graph['verification_seconds']),
       seconds=time.perf_counter()-tic,
       source_sha256={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest()
                    for n in ['COARSE_CONTRACT.json','PAIR_GRAPH.json','BASELINE_COARSE.csv']},
       parent_graph_sha256=hashlib.sha256((ROOT/'ENVELOPE.json').read_bytes()).hexdigest(),
       full_information_comparator='ordinary Girsanov given exact vacancy-pair activity; extra information labeled. SAME coarse-information ordinary partial-likelihood/graph optimization reproduces our receiver exactly.',
       physical_qualification='NOT_ACQUIRED: adsorption additivity/destination invariance, event-resolved total coverage, site graph, calibrated adsorption coefficients, initial ensemble, timing and model discrepancy')
    (HERE/'COARSE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'seconds':result['seconds'],'conditional_joint_failure_upper':result['ideal_sampling_confidence']['failure_upper'],
      'queries':[{'name':q['name'],'oxygen_interval':q['outputs']['Ocoverage']['exact_graph_DP'],
                  'direct_oxygen':q['outputs']['Ocoverage']['direct'],
                  'CO2_interval':q['outputs']['CO2hit']['exact_graph_DP']} for q in reports]},indent=2))


if __name__=='__main__':main()
