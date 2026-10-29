"""Standalone promised-access receiver; no rich or held-out files read.

Only imports a data-free ordinary bounded-confidence helper. The graph is
an acquired geometry envelope, not a hidden kinetic generator.
"""
import argparse,hashlib,json,math,time
from pathlib import Path
import numpy as np
from bounded_confidence import interval

HERE=Path(__file__).resolve().parent
DESIGNS=[('HELDOUT_080_090',.8,.9),('HELDOUT_090_080',.9,.8),('HELDOUT_080_080',.8,.8)]
OUTPUTS=['COcoverage','Ocoverage','CO2hit']


def receive(contract,rows,graph,designs=DESIGNS):
    M=contract['sites'];assert graph['sites']==M
    assert graph['source_model_sha256']==contract['source_model_sha256']
    assert len(rows)==contract['row_count']
    assert set(rows.dtype.names)==set(['NCO','NO2']+OUTPUTS+[f'Tv{v}' for v in range(M+1)])
    H=np.column_stack([rows[f'Tv{v}'] for v in range(M+1)])
    assert np.min(H)>=0
    assert np.max(abs(H.sum(axis=1)-contract['horizon_seconds']))<1e-18
    v=np.arange(M+1);ko=graph['common_pair_rate']
    Aco=(contract['gas_activity_upper']['CO']/M)*(H@v)
    limits={'degree':(ko*(H@np.maximum(0,4*v-2*M)),ko*(H@(2*v))),
            'exact_graph_DP':(ko*(H@np.array(graph['min_empty_edges'])),
                              ko*(H@np.array(graph['max_empty_edges'])))}
    reports=[]
    for name,a,b in designs:
        assert 0<a<=1 and 0<b<=1
        count=rows['NCO']*math.log(a)+rows['NO2']*math.log(b)
        C=((1-a)*contract['gas_activity_upper']['CO']+(1-b)*contract['gas_activity_upper']['O2'])*contract['horizon_seconds']
        B=math.exp(C)
        weights={label:(np.exp(count+(1-a)*Aco+(1-b)*lo),
                        np.exp(count+(1-a)*Aco+(1-b)*hi))
                 for label,(lo,hi) in limits.items()}
        values={}
        for output in OUTPUTS:
            values[output]={}
            for label,(wl,wu) in weights.items():
                low=interval(rows[output]*wl,B);high=interval(rows[output]*wu,B)
                values[output][label]=dict(lower=max(0.,low['lower']),upper=min(1.,high['upper']),
                    lower_estimator=low,upper_estimator=high,
                    acquired_structural_mean_gap=high['mean']-low['mean'])
        reports.append(dict(name=name,CO_multiplier=a,O2_multiplier=b,
                            deterministic_weight_bound=B,outputs=values))
    oxygen=[q['outputs']['Ocoverage']['exact_graph_DP'] for q in reports]
    margin=oxygen[0]['lower']-max(z['upper'] for z in oxygen[1:])
    return dict(baseline={o:interval(rows[o],1.) for o in OUTPUTS},queries=reports,
          finite_candidate_oxygen_ordering=dict(candidate=reports[0]['name'],
                 conditional_lower_margin=margin,positive=margin>0,
                 scope='ONLY these three locked candidates and supplied surface-coverage output; not a CO2 product optimum or physical recommendation'),
          confidence_scope='exact IID clean-start law and exact coarse records; conditional union bound8*57*exp(-14)<.001 reserved for the combined57-stat comparison',
          implementation_scope='binary64 numerical application; no certified finite-bit law or measured-physical-data claim')


def main():
    a=argparse.ArgumentParser()
    a.add_argument('--contract',type=Path,default=HERE/'COARSE_CONTRACT.json')
    a.add_argument('--data',type=Path,default=HERE/'BASELINE_COARSE.csv')
    a.add_argument('--graph',type=Path,default=HERE.parent/'root_vacancy_envelope/ENVELOPE.json')
    a.add_argument('--out',type=Path,default=HERE/'COARSE_ONLY_RESULT.json')
    args=a.parse_args();tic=time.perf_counter()
    contract=json.loads(args.contract.read_text());graph=json.loads(args.graph.read_text())
    assert hashlib.sha256(args.data.read_bytes()).hexdigest()==contract['coarse_data_sha256']
    rows=np.genfromtxt(args.data,delimiter=',',names=True)
    result=receive(contract,rows,graph)
    result.update(status='EXECUTED with ONLY declared coarse inputs',seconds=time.perf_counter()-tic,
       input_sha256={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [args.contract,args.data,args.graph]},
       source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'seconds':result['seconds'],
                      'ordering':result['finite_candidate_oxygen_ordering']}))


if __name__=='__main__':main()
