"""Exact scalar/extreme-box acquisition; independent-set helpers disabled."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
import common_box as C
root=Path(__file__).resolve().parent

def path_box(n,lo,hi):
    m=n+1;z=lambda *ix:tuple(ix.count(i) for i in range(m))
    out=[(z(),z(0),lo,hi),(z(0),z(),lo,hi)]
    for i in range(1,n):
        out.extend([(z(0,0),z(i,i+1),lo,hi),(z(i,i+1),z(0,0),lo,hi)])
    for i in range(1,n+1):
        H=z(i,i+1) if i<n else z(i-1,i)
        out.extend([(z(0,i),H,lo,hi),(H,z(0,i),lo,hi)])
    return out

def disabled(*a,**kw):raise AssertionError('independent-set evaluation was called')
C.faces=disabled;C.multiplier=disabled;C.worst_scaled_drift=disabled
rows=[]
for n,lo,hi in [(2,F(1,2**200),F(2**200)),(7,F(1,17),F(29,3)),(30,F(1),F(2))]:
    raw=path_box(n,lo,hi);p=C.construct(raw);r=p['raw']
    assert p['M']>=12*r['s_hi']/r['b_lo']
    assert p['e']*r['mu_hi']<=r['mu_hi']**2*p['eps']/4
    assert p['H']-p['eps']*(1+p['Pbar'])==1
    assert p['Nstar']>=1+4*r['mu_hi']*p['H']/(p['g']*p['dA'])
    assert p['nu']<=r['lam_lo'] and p['D']==r['mu_lo']*(1-1/p['t'])
    assert p['independent_sets_enumerated']==0
    b=C.resource_budget(p,17,F(19,7),F(1,1000));C.receive_resource_budget(raw,b,initial_total_upper_bound=17,horizon=F(19,7),failure=F(1,1000))
    bad=dict(b);bad['count_level']-=1
    try:C.receive_resource_budget(raw,bad,initial_total_upper_bound=17,horizon=F(19,7),failure=F(1,1000))
    except C.Unsupported:pass
    else:raise AssertionError('mutated resource budget received')
    def scalars(o):
        if isinstance(o,(int,F)) and type(o)is not bool:yield F(o)
        elif isinstance(o,dict):
            for v in o.values():yield from scalars(v)
        elif isinstance(o,(list,tuple)):
            for v in o:yield from scalars(v)
    rows.append(dict(satellites=n,channels=len(r['channels']),lower_rate_bits=lo.numerator.bit_length()+lo.denominator.bit_length(),upper_rate_bits=hi.numerator.bit_length()+hi.denominator.bit_length(),
       M_bits=p['M'].bit_length(),Nstar_bits=p['Nstar'].bit_length(),max_scalar_numerator_plus_denominator_bits=max(x.numerator.bit_length()+x.denominator.bit_length() for x in scalars(p)),
       canonical_certificate_bytes=len(C.canonical_bytes(p)),independent_sets_enumerated=0,count_level=b['count_level'],selected_count_cap=b['selected_count_cap']))
result=dict(status='PASS_AUTHOR_EXTREME_SCALAR_ACQUISITION_NOT_INDEPENDENT',cases=rows,production_helpers='faces, multiplier and drift evaluation replaced by raising stubs',
    bindings={f:hashlib.sha256((root/f).read_bytes()).hexdigest() for f in ['common_box.py','COMMON_PREDICTABLE_BOX_THEOREM.md','check_scalar_extremes.py']})
(root/'scalar_extreme_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
