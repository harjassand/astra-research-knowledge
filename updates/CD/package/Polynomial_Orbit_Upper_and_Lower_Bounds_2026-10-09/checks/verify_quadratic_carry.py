#!/usr/bin/env python3
"""Exact finite checks of the explicit carry construction; no general complexity certification."""
from pathlib import Path
import json

def check(m):
    b=[0]*m
    c_tail=[0]*(m-1)
    z=0
    expected=2**(m+1)-2
    flips=[0]*m
    for t in range(expected+1):
        c=[1-sum(c_tail)]+c_tail
        assert all(x in (0,1) for x in b+c+[z]) and sum(c)==1
        if z:
            assert t==expected
            assert flips==[2**(m-i) for i in range(m)]
            return {'m':m,'dimension':2*m,'map_degree_at_most':2,'output_degree':1,'first_nonzero_index':t,'flips_by_bit':flips}
        for i in range(m): flips[i]+=c[i]
        bnew=[b[i]+c[i]-2*b[i]*c[i] for i in range(m)]
        cnew=[b[i-1]*c[i-1] for i in range(1,m)]
        znew=b[-1]*c[-1]
        b,c_tail,z=bnew,cnew,znew
    raise AssertionError('No overflow at expected endpoint')

payload={'status':'Exact sanity checks of an illustrative lower obstruction; no novelty claim','cases':[check(m) for m in range(1,17)],'checks_passed':True}
Path(__file__).with_name('quadratic_carry_checks.json').write_text(json.dumps(payload,indent=2)+'\n')
print(json.dumps(payload,indent=2))
