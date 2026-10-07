#!/usr/bin/env python3
"""Exact boundary/ambiguity replays for the reusable normal and root components."""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result
normal=module('normal',HERE/'certified_normal.py')
root=module('root',HERE/'certified_psd_root.py')
start=time.perf_counter()
normal_reports=[]
for L,ell in [(F(1),16),(F(4),24),(F(8),16)]:
    bits=ell+normal.ceil_fraction(L*L)+8
    D=1<<bits
    for name,u in [('left_tail',0),('zero',D//2),('interior',D*8//9),('right_tail',D-1)]:
        normal.base.ledger=normal.base.Ledger()
        t0,c0=time.perf_counter(),time.process_time()
        data=normal.generate(L,ell,u)
        assert F(data['ideal_clipped_normal_coupling_error_upper'])<F(data['h'])
        if name=='zero':
            assert F(data['output_rational'])==0
            assert data['termination']=='TOLERANCE_INTERIOR_STOP'
        if name=='left_tail': assert F(data['output_rational'])==-L
        if name=='right_tail': assert F(data['output_rational'])==L
        data['costs']={**normal.base.ledger.snapshot(),'wall_seconds':time.perf_counter()-t0,
                       'cpu_seconds':time.process_time()-c0}
        path=HERE/'evidence'/'normal_boundary'/f'L{L}_ell{ell}_{name}.json'
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(data,indent=2)+'\n')
        normal_reports.append({'output':str(path.relative_to(HERE)),
                               'termination':data['termination'],
                               'coupling_bound':data['ideal_clipped_normal_coupling_error_upper'],
                               'cdf_calls':data['cdf_request_count'],
                               'max_integer_bits':data['costs']['max_observed_integer_bits']})
root_reports=[]
for name in ['zero','rank1','rank2','tiny','negative']:
    root.base.ledger=root.base.Ledger()
    t0,c0=time.perf_counter(),time.process_time()
    data=root.root(root.FIXTURES[name],12)
    if name=='negative': assert data['status']=='REFUTED_PSD_INPUT'
    else:
        assert data['status']=='CERTIFIED_GAP_FREE_PSD_ROOT_COLUMNS'
        q=F(data['target_root_operator_error'])
        assert F(data['squared_residual_operator_upper'])<=q*q
        # Independently recompute the delivered squared residual from its root.
        X=[[F(x) for x in row] for row in data['certified_root_matrix']]
        C=root.FIXTURES[name]
        independent=[[sum(X[i][k]*X[k][j] for k in range(3))-C[i][j]
                      for j in range(3)] for i in range(3)]
        delta=max(sum(abs(x) for x in row) for row in independent)
        assert delta==F(data['squared_residual_operator_upper'])
    data['costs']={**root.base.ledger.snapshot(),'wall_seconds':time.perf_counter()-t0,
                   'cpu_seconds':time.process_time()-c0}
    path=HERE/'evidence'/'root_boundary'/f'{name}.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2)+'\n')
    root_reports.append({'fixture':name,'output':str(path.relative_to(HERE)),
                         'status':data['status'],'working_bits':data.get('working_dyadic_bits'),
                         'steps':data.get('newton_steps'),
                         'max_integer_bits':data['costs']['max_observed_integer_bits']})
report={'status':'NORMAL_AND_ROOT_COMPONENT_AUDITS_PASS',
        'normal_cases':normal_reports,'root_cases':root_reports,
        'wall_seconds':time.perf_counter()-start,
        'limits':'Boundary and exact-residual checks support implemented components; not an end-to-end growing-N sampler.'}
(HERE/'evidence'/'primitive_audit.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':report['status'],'normal_cases':len(normal_reports),
                  'root_cases':len(root_reports),'wall_seconds':report['wall_seconds']}))
