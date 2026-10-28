"""Resolve the finite preview's quadrature uncertainty without new sources.

Re-evaluate exactly the same 49 correlations at degree32. Agreement remains
a numerical diagnostic, not a rigorous quadrature enclosure.
"""
from pathlib import Path
import json,time
from bilocal_time_preview import Physical,ROOT

def main():
    start=time.monotonic();models={};checks=[]
    raw=json.loads((ROOT/'results/bilocal_time_source_inputs.json').read_text())
    aug=json.loads((ROOT/'results/frozen_span_new_inputs.json').read_text())
    cases=[]
    for x in raw:cases.append((x['n'],1.,x['left_delta'],x['right_delta'],x['C_projected_degree16']))
    for x in aug:cases.append((x['n'],x['old_fugacity'],None,x['new_delta'],x['C_projected_degree16']))
    for n,r,left,right,old in cases:
        key=n,r
        if key not in models:
            edges=(3*r,)if n==2 else(3*r,)+(3.,)*(n-2)
            models[key]=Physical(n,edges=edges)
        value,pieces=models[key].source_integral(left,right,32)
        relative=abs(value-old)/max(1.,abs(value));assert relative<5e-12
        checks.append({'n':n,'old_fugacity':r,'left_delta':left,'right_delta':right,
                       'degree16':old,'degree32':value,'relative_difference':relative,'pieces':pieces})
    out={'status':'PASS_SAME_SOURCE_DEGREE16_VS32_NUMERICAL_STABILITY',
         'same_correlations':len(checks),'maximum_relative_difference':max(x['relative_difference']for x in checks),
         'new_family_members':0,'checks':checks,'seconds':time.monotonic()-start,
         'time_ordered_trace_calls':sum(x.trace_calls for x in models.values()),
         'scope':'Checks the unresolved quadrature approximation only. No rigorous source, quadrature or floating-point interval follows.'}
    (ROOT/'results/quadrature_stability.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items()if k!='checks'},indent=2))

if __name__=='__main__':main()
