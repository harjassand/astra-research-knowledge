#!/usr/bin/env python3
"""Exact sharpness of degree-promised deletion and tail-detection gaps."""
from bisect import bisect_left
from fractions import Fraction
import json
from pathlib import Path
from recognition_fixture import anf_degree,exact_prefix_rejection

HERE=Path(__file__).resolve().parent


def lis(values):
    tails=[]
    for x in values:
        i=bisect_left(tails,x)
        if i==len(tails):tails.append(x)
        else:tails[i]=x
    return len(tails)


def main():
    rows=[]
    prefix_rows=[]
    for n in range(3,10):
        N=1 << n
        for d in range(1,min(4,n-1)+1):
            # The high d bits control an LSB flip. This is a degree-d
            # triangular bijection and a product of disjoint adjacent swaps.
            monomial=((1 << d)-1) << (n-d)
            p=[x ^ int((x&monomial)==monomial) for x in range(N)]
            assert len(set(p))==N
            mismatches=sum(p[x]!=x for x in range(N))
            deletion=N-lis(p)
            assert Fraction(mismatches,N)==Fraction(1,1 << d)
            assert Fraction(deletion,N)==Fraction(1,1 << (d+1))
            rows.append(dict(n=n,d=d,moved_items=mismatches,adjacent_transpositions=deletion,
                exact_tail_mismatch_probability=str(Fraction(mismatches,N)),
                exact_deletion_distance=str(Fraction(deletion,N)),
                model='identity vs x_LSB + product(high d bits); all other outputs unchanged'))
            low=n-d-1
            width=1 << low
            midpoint=(1 << d)-1
            def block_swap(x):
                top=x >> low
                if top==midpoint:top+=1
                elif top==midpoint+1:top-=1
                return (top << low)|(x&(width-1))
            block=[block_swap(x) for x in range(N)]
            assert len(set(block))==N
            degrees=[anf_degree([(block[x] >> (n-i-1))&1 for x in range(N)],n)
                     for i in range(n)]
            assert max(degrees)==d
            for h in (1,n):
                rejection=exact_prefix_rejection(block,n,h)
                assert rejection==Fraction(1,h*(1 << (2*d)))
                prefix_rows.append(dict(n=n,d=d,h=h,block_width=width,
                    exact_prefix_probe_rejection=str(rejection),all_output_degree=d,
                    model='swap midpoint adjacent values of high d+1 bits; preserve every lower bit'))
    out=dict(status='PASS',scope='explicit bounded-degree bijections attain both internal degree-gap bounds',
             cases=len(rows),records=rows,prefix_probe_sharp_cases=len(prefix_rows),prefix_records=prefix_rows)
    (HERE/'sharp_degree_gap.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',cases=len(rows),prefix_probe_sharp_cases=len(prefix_rows))))
if __name__=='__main__':main()
