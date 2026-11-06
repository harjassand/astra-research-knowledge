"""Later tasks and modular composition without any new source observations."""
from fractions import Fraction as Q
from pathlib import Path
import json,time
from flow import build,propose_path,certify


def skew(n,edges):
    a=[['0']*n for _ in range(n)]
    for i,j,v in edges:a[i][j]=str(Q(v));a[j][i]=str(-Q(v))
    return a


def term(n,degree,weight,entries):
    v=['0']*n
    for i,value in entries:v[i]=str(Q(value))
    return {'degree':degree,'weight':str(Q(weight)),'direction':v}


def main():
    output=Path(__file__).resolve().parent/'results'
    models=[json.loads((output/(x+'_model.json')).read_text()) for x in ['component_A','component_B']]
    records=[json.loads((output/(x+'_port_record.json')).read_text()) for x in ['component_A','component_B']]
    init=[Q(row['channel']['initial_bound_at_start']) for row in records]
    cases=[
        {'name':'later_coupled_quartic','components':[0],
         'attachment':{'dimension':0,'damping':[],
                       'skew':skew(3,[(0,1,'3/2'),(1,2,'-2/3')])},
         'load':[term(3,3,'3/4',[(0,1),(1,1)]),
                 term(3,3,'2/5',[(1,1),(2,-1)]),
                 term(3,1,'1/3',[(0,1),(2,1)])],
         'segments':[{'duration':'1','input':['1','-1/2','1/3']},
                     {'duration':'1','input':['0','1','-1/2']}]},
        {'name':'later_two_added_states','components':[0],
         'attachment':{'dimension':2,'damping':['5/4','3/2'],
                       'skew':skew(5,[(0,3,2),(1,4,'-3/2'),(2,3,'1/2'),(3,4,'3/4')])},
         'load':[term(5,3,'1/2',[(0,1),(3,1)]),
                 term(5,3,'1/3',[(1,1),(2,-1),(4,1)]),
                 term(5,1,'1/4',[(2,1),(3,-1),(4,1)])],
         'segments':[{'duration':'1','input':['1','0','-1/2','0','1/3']},
                     {'duration':'1','input':['-1/2','1','0','1/2','0']}]},
        {'name':'later_composed_network','components':[0,1],
         'attachment':{'dimension':2,'damping':['5/4','3/2'],
                       'skew':skew(8,[(0,3,'5/2'),(1,4,'-3/2'),(2,5,2),
                                      (0,6,1),(4,7,'-4/3'),(6,7,'1/2')])},
         'load':[term(8,3,'2/5',[(0,1),(3,-1),(6,1)]),
                 term(8,3,'1/3',[(1,1),(4,1),(7,-1)]),
                 term(8,3,'1/4',[(2,1),(5,-1)]),
                 term(8,1,'2/3',[(0,1),(2,-1),(5,1),(7,1)])],
         'segments':[{'duration':'1','input':['1','-1/2','0','0','1/3','1/2','0','1/4']},
                     {'duration':'1','input':['0','1','-1/3','1/2','0','-1/2','1/4','0']}]}
    ]
    summaries=[]
    for case in cases:
        components=[models[i] for i in case['components']]
        initial=[init[i] for i in case['components']]
        matrix,R,alpha,error,groups,weights=build(components,case['attachment'])
        start=time.perf_counter()
        path=propose_path(matrix,case['load'],R,case['segments'],steps_per_unit=32,node_bits=44)
        proposal_time=time.perf_counter()-start;start=time.perf_counter()
        cert=certify(components,case['attachment'],path,initial)
        cert_time=time.perf_counter()-start
        payload={'task':case,'path':path,'certificate':cert}
        (output/(case['name']+'.json')).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
        row={'task':case['name'],'components':len(components),'observed_dimension':R,
             'model_dimension':len(matrix),'new_dynamic_states':case['attachment']['dimension'],
             'terminal_observed':[float(Q(v)) for v in cert['terminal_observed']],
             'certified_uniform_radius':float(Q(cert['uniform_observed_error_radius'])),
             'numerical_residual_L2':float(Q(cert['effective_numerical_residual_L2'])),
             'source_uncertainty_L2':float(Q(cert['source_uncertainty_contribution_L2'])),
             'initial_state_radius':float(Q(cert['initial_state_radius'])),
             'intervals':cert['intervals'],'field_evaluations':path['proposal_field_evaluations'],
             'residual_coefficient_bits_max':cert['max_residual_coefficient_bits'],
             'additional_source_calls':0,'proposal_seconds':proposal_time,'certificate_seconds':cert_time}
        summaries.append(row);print(json.dumps(row),flush=True)
    (output/'later_task_summary.json').write_text(json.dumps(summaries,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':main()
