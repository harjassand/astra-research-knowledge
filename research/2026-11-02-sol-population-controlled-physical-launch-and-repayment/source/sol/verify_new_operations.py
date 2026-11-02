#!/usr/bin/env python3
"""Exact geometry/kernel checks; numerical signs remain finite diagnostics."""
from pathlib import Path
from itertools import product
from collections import deque
from fractions import Fraction as F
from math import factorial,prod
import json,sys
import mpmath as mp
from conservative_fiber_kernel import canonical,bounds,shift,raw_network,acquire,W
from collapsed_physical_dp import run

P=Path(__file__).resolve().parent
OLD=Path('producer-workspace/astra-sol-joint-activation-20261102')
sys.path.insert(0,str(OLD))
import neutral_source_compiler as neutral

def main():
    checked=0
    # Compare exact factorial products, not approximate convex values.
    for b,c,e,f in product(range(6),repeat=4):
        x=(1,b,c,1,e,f);lo,hi=bounds(x);opt=canonical(x)
        value=lambda y:prod(factorial(a) for a in y)
        assert value(opt)==min(value(shift(x,k)) for k in range(lo,hi+1))
        assert all(canonical(shift(x,k))==opt for k in range(lo,hi+1));checked+=1
    raw=raw_network();C=sorted({v for s,u,k in raw for v in [s,u]});I=[1,2,4,5]
    profile=[{'coordinate':0,'kind':'exact','value':0},{'coordinate':3,'kind':'exact','value':0}]
    root=neutral.make_node((0,)*6,profile);seen={root};todo=deque([root]);gaps=[];edges=0
    while todo:
        node=todo.popleft()
        for a in C:
            if neutral.source_available(node,a,profile):
                gap=tuple(a[i]-node[0][i] for i in I);gaps.append(gap)
                assert sum(gap)<=0
        for r in range(len(raw)):
            dest=neutral.neutral_step(node,r,I,profile,raw)
            if dest is not None:
                edges+=1
                if dest not in seen:seen.add(dest);todo.append(dest)
    assert len(seen)==7
    assert all(neutral.neutral_step(node,r,I,profile,raw) in seen or neutral.neutral_step(node,r,I,profile,raw) is None for node in seen for r in range(len(raw)))
    # Exact primary terminal-gap dual on the normal linkage.
    pairs=0
    for t in C:
        if t in [raw[8][0],raw[8][1]]:continue
        for a in C:
            if a[0]<=t[0] and a[3]<=t[3]:
                assert sum(a[i]-t[i] for i in I)<=0;pairs+=1
    x=(1,11,10,1,11,10);t=(0,0,0,1,1,0)
    kernel=acquire(x,t);dp=run(x,t,max_h=1)
    first=mp.mpf(kernel['physical_time_plus_power_change_over_2V'])
    second=mp.mpf(dp['rows'][0]['physical_time_plus_coarse_power_change_over_2V'])
    assert abs(first-second)<mp.mpf('1e-65') and F(kernel['time_exact'])==F(1,24)
    result={'exact_quotient_minimization_and_orbit_checks':checked,
            'closed_neutral_obstruction':{'divergent_coordinates':I,'outside_profile':profile,'nodes':len(seen),'edges':edges,'dual_weight':['1/4']*4,'terminal_gaps':sorted(set(gaps))},
            'ordinary_terminal_cone_dual_pairs_checked':pairs,
            'finite_kernel_and_actual_feedback_operator_agree':True,'exact_joint_active_exit_time':'1/24',
            'scope':'Same-principal exact operation checks; no independent audit or global coupled recurrence conclusion.'}
    (P/'results/new_operation_checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
