#!/usr/bin/env python3
"""Independent literal spin-2 construction, all signed M sectors retained.

Does not import the producer or reuse its base-5 indexing. Rebuilds moments
0..6 of both new six-cycles and193 four-cycle controls modulo one modulus.
This is a bounded data/control-flow check, not regeneration of all25 CRT runs.
"""
from pathlib import Path
from itertools import product
from collections import defaultdict
import json,time
import numpy as np
from scipy.sparse import coo_matrix,eye

HERE=Path(__file__).resolve().parent
WORK=HERE.parents[1]
PRIOR=WORK.parent/'sol8_opportunity_selection_20261027/obstruction_first/continuation/data'

def all_blocks(n,twist):
    groups=defaultdict(list)
    for state in product(range(-2,3),repeat=n):groups[sum(state)].append(state)
    for total,states in sorted(groups.items()):
        lookup={s:i for i,s in enumerate(states)}
        rr=[];cc=[];vv=[]
        for col,s in enumerate(states):
            diagonal=0
            for i in range(n):
                j=(i+1)%n;diagonal+=2*s[i]*s[j]
                phase=-1 if twist=='P' and i==n-1 else 1
                for delta in (-1,1):
                    t=list(s);t[i]+=delta;t[j]-=delta
                    if min(t)<-2 or max(t)>2:continue
                    value=phase*(2-delta*s[i])*(2+delta*s[j])
                    rr.append(lookup[tuple(t)]);cc.append(col);vv.append(value)
            if diagonal:rr.append(col);cc.append(col);vv.append(diagonal)
        h=coo_matrix((np.array(vv,dtype=np.int64),(rr,cc)),shape=(len(states),len(states))).tocsr()
        yield total,states,h

def short_moments(n,kind,maxprime):
    answer=[0]*7;dimensions={};checks=[]
    for total,states,h in all_blocks(n,kind):
        d=len(states);dimensions[total]=d
        row=int(np.asarray(abs(h).sum(axis=1)).max(initial=0))
        col=int(np.asarray(abs(h).sum(axis=0)).max(initial=0))
        radius=max(row,col)
        assert d*radius**6<2**62
        assert row*maxprime<2**62 and d*maxprime<2**62
        h2=h@h;h3=h2@h
        values=[d,int(h.diagonal().sum()),int(h2.diagonal().sum()),int(h3.diagonal().sum()),
                int(h2.multiply(h2.T).sum()),int(h2.multiply(h3.T).sum()),int(h3.multiply(h3.T).sum())]
        answer=[a+b for a,b in zip(answer,values)]
        checks.append({'M':total,'dimension':d,'row_abs_max':row,'int64_control':True})
    assert sum(dimensions.values())==5**n
    assert all(dimensions[m]==dimensions[-m] for m in dimensions)
    return answer,dimensions,checks

def four_control(kind,prime):
    residues=[0]*193;maxdim=0
    for total,states,h in all_blocks(4,kind):
        d=len(states);maxdim=max(maxdim,d)
        assert int(np.asarray(abs(h).sum(axis=1)).max(initial=0))*prime<2**62
        assert d*prime<2**62
        power=np.eye(d,dtype=np.int64)
        for k in range(193):
            residues[k]=(residues[k]+int(np.trace(power)))%prime
            if k<192:power=(h@power)%prime
    return residues,maxdim

def four_analytic():
    energies=defaultdict(int)
    for a in range(5):
        for b in range(5):
            for j in range(abs(a-b),a+b+1):
                E=(j*(j+1)-a*(a+1)-b*(b+1))//2;energies[E]+=2*j+1
    assert sum(energies.values())==625
    return [sum(d*(2*e)**k for e,d in energies.items()) for k in range(193)]

def run():
    start=time.perf_counter()
    six=json.loads((WORK/'thermal/results/cycle6_moments_exact_degree192.json').read_text())
    rows=[]
    for rec in six['records']:
        rebuilt,dims,checks=short_moments(6,rec['twist'],max(rec['CRT_primes']))
        assert rebuilt==list(map(int,rec['trace_2H_powers'][:7]))
        rows.append({'twist':rec['twist'],'moments_0_to_6':list(map(str,rebuilt)),
                     'all_signed_M_dimensions':dims,'max_dimension':max(dims.values()),
                     'overflow_checks_all_signed_M':checks})
    old=json.loads((PRIOR/'twisted4_moments_exact_degree192.json').read_text())
    pold=next(r for r in old['records'] if r['twist']=='P')
    prime=six['records'][0]['CRT_primes'][0]
    controls=[]
    for kind,expected in [('I',four_analytic()),('P',list(map(int,pold['trace_2H_powers'])))]:
        got,dim=four_control(kind,prime)
        assert got==[v%prime for v in expected]
        controls.append({'cycle':4,'twist':kind,'moments_0_to_192_modulus':prime,
                         'all_193_match':'PASS','max_dimension':dim})
    result={'status':'INDEPENDENT_LITERAL_CYCLE_CONTROLS_PASS','cycle6':rows,'cycle4_controls':controls,
            'scope':'all physical states included; full6-cycle25-modulus degree192 acquisition reviewed rather than regenerated',
            'seconds':time.perf_counter()-start}
    (HERE/'CYCLE_CONTROL_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'cycle6_first7':[r['moments_0_to_6'] for r in rows],
                     'cycle4_controls':controls,'seconds':result['seconds']},indent=2))

if __name__=='__main__':run()
