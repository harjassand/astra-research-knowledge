#!/usr/bin/env python3
"""Independent full truth-table Walsh oracle for every binary 2x2 source."""
from collections import Counter
from pathlib import Path
import json
from matrix_kloosterman import (
    Field, all_matrices, mmul, mtrace, cubic_count_supported,
    cubic_zero_source_from_ranks, cubic_zero_source_sum)


def coefficient_mask(A):
    n=len(A)
    return sum(A[j][i]<<(n*i+j) for i in range(n) for j in range(n))


def matrix_from_bits(x,n=2):
    return [[(x>>(n*i+j))&1 for j in range(n)] for i in range(n)]


def main():
    F=Field(3)
    matrices=[matrix_from_bits(x) for x in range(16)]
    truth=[]
    for word in range(4096):
        X,Y,Z=(matrices[(word>>(4*j))&15] for j in range(3))
        truth.append((-1)**mtrace(mmul(mmul(X,Y,F),Z,F)))
    spectrum=truth[:]
    width=1
    while width<len(spectrum):
        for start in range(0,len(spectrum),2*width):
            for j in range(width):
                u,v=spectrum[start+j],spectrum[start+width+j]
                spectrum[start+j]=u+v
                spectrum[start+width+j]=u-v
        width*=2
    passed=[]
    unsupported=[]
    routes=Counter()
    for a,A in enumerate(matrices):
        for b,B in enumerate(matrices):
            for c,C in enumerate(matrices):
                mask=coefficient_mask(A)|(coefficient_mask(B)<<4)|(coefficient_mask(C)<<8)
                expected=(4096+spectrum[mask])//2
                try:
                    count,stats=cubic_count_supported(A,B,C)
                except ValueError:
                    unsupported.append([a,b,c,expected])
                    continue
                assert count==expected,(a,b,c,count,expected,stats)
                passed.append([a,b,c,count])
                route=stats.get('backend')
                routes['zero_source' if isinstance(route,str) else 'matrix_Kloosterman']+=1
    large=[]
    for n,a,rA,rB,rBA in [(32,4,0,0,0),(64,8,48,40,24),(64,8,64,0,0)]:
        signed,stats=cubic_zero_source_from_ranks(n,a,rA,rB,rBA)
        inputs=3*a*n*n
        count=((1<<inputs)+signed)//2
        large.append(dict(matrix_rank=n,field_degree=a,original_inputs=inputs,
            source_ranks=[rA,rB,rBA],signed_sum_hex=hex(signed),zero_count_hex=hex(count),
            count_bits=count.bit_length(),details=stats))
    data=dict(status='all supported source triples match full truth-table Walsh oracle',
              independent_truth_table_inputs=12,truth_table_points=4096,
              complete_source_spectrum=4096,accepted_source_triples=len(passed),
              accepted_by_route=dict(routes),unsupported_source_triples=len(unsupported),
              exact_accepted_cases=passed,unsupported_examples=unsupported[:20],
              growing_rank_zero_source_cases=large)
    path=Path(__file__).with_name('cubic_spectrum_results.json')
    path.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({k:v for k,v in data.items() if k not in
        ('exact_accepted_cases','growing_rank_zero_source_cases','unsupported_examples')}))


if __name__=='__main__':
    main()
