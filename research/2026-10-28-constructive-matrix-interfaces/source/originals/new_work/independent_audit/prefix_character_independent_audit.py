#!/usr/bin/env python3
"""Literal one-character audit of the row-prefix sampler's core identity."""
from pathlib import Path
from collections import defaultdict
import json
import random
import sys
import time
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'affine_sampler'))
from affine_slice_prefix_sampler import (
    AffineMatrixSliceSampler, pack_vector, unpack_vector, matmul,
    trace_bit, dot, rank_field)
from raw_bilinear_product_checks import FixtureField


class RebasedF4:
    """The basis (omega,1), so the actual field identity is coordinate 2."""
    a = 2
    q = 4
    one = 2
    def __init__(self):
        self.base=FixtureField(7)
    @staticmethod
    def swap(value):
        return ((value & 1) << 1) | ((value >> 1) & 1)
    def mul(self,x,y):
        return self.swap(self.base.mul(self.swap(x),self.swap(y)))
    def inv(self,x):
        if not x:
            raise ValueError('zero inverse')
        return self.mul(x,x)


def decode(F, word, rows, columns):
    return [unpack_vector(F, word >> (F.a*columns*i), columns) for i in range(rows)]


def main():
    began=time.perf_counter()
    records=[]
    cases=[(FixtureField(3),2,2,2,True),
           (FixtureField(3),2,3,2,False),
           (RebasedF4(),1,2,2,False),
           (RebasedF4(),2,1,2,False)]
    comparisons=literal_pairs=0
    for case,(F,p,d,r,exhaustive) in enumerate(cases):
        if not hasattr(F,'one'):
            F.one=1
        width=F.a*d*r
        groups=defaultdict(list)
        for x in range(F.q**(p*d)):
            X=decode(F,x,p,d)
            for y in range(F.q**(d*r)):
                Y=decode(F,y,d,r)
                z=pack_vector(F,[v for row in matmul(F,X,Y,r) for v in row])
                groups[z].append(y)
                literal_pairs+=1
        if exhaustive:
            probes=[(z,D) for z in range(F.q**(p*r)) for D in range(F.q**(d*r))]
        else:
            rng=random.Random(779000+case)
            probes=[(0,0)]+[(rng.randrange(F.q**(p*r)),rng.randrange(F.q**(d*r))) for _ in range(31)]
        checked=0
        for z,dword in probes:
            Z=decode(F,z,p,r)
            D=decode(F,dword,d,r)
            truth=defaultdict(int)
            for y in groups[z]:
                Y=decode(F,y,d,r)
                phase=0
                for frequency,row in zip(D,Y):
                    phase^=trace_bit(F,dot(F,frequency,row))
                sign=-1 if phase else 1
                for size in range(width):
                    truth[size,y & ((1 << size)-1)]+=sign
            engine=AffineMatrixSliceSampler(F,Z,d)
            for size in range(width):
                t,used=divmod(size,F.a*r)
                for prefix in range(1 << size):
                    rows=decode(F,prefix,t,r)
                    bits=prefix >> (t*F.a*r)
                    alpha=rank_field(F,rows,r)
                    k=rank_field(F,rows+Z,r)-alpha
                    actual=engine._partial_signed(D,rows,bits,used,alpha,k)
                    assert actual==truth[size,prefix],(case,z,dword,size,prefix,actual,truth[size,prefix])
                    checked+=1
        comparisons+=checked
        record=dict(field_degree=F.a,identity_coordinate=F.one,p=p,d=d,r=r,
                    distinct_target_character_probes=len(probes),
                    exact_one_character_prefix_comparisons=checked,
                    factor_pairs_enumerated=F.q**(p*d+d*r))
        records.append(record)
        print(json.dumps(record),flush=True)
    result=dict(passed=True,records=records,literal_factor_pairs=literal_pairs,
                exact_one_character_prefix_comparisons=comparisons,
                seconds=time.perf_counter()-began)
    (HERE/'prefix_character_independent_audit_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))


if __name__=='__main__':
    main()
