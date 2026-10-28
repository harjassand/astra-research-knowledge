#!/usr/bin/env python3
"""Exponential small-case validation oracle for two-coefficient matrix sums.

Never used by the polynomial counter. An integer Walsh transform of the
inverse graph evaluates every binary source pair. Nilpotent cyclic-quiver
types are grouped by all alternating-product ranks for formula discovery.
"""
from collections import Counter
from pathlib import Path
import json
import numpy as np


def transpose(x,n):
    return sum(((x>>(i*n+j))&1)<<(j*n+i) for i in range(n) for j in range(n))


def multiply(x,y,n):
    mask=(1<<n)-1
    yr=[(y>>(n*j))&mask for j in range(n)]
    out=0
    for i in range(n):
        row=(x>>(n*i))&mask
        value=0
        while row:
            bit=row&-row
            value^=yr[bit.bit_length()-1]
            row^=bit
        out|=value<<(n*i)
    return out


def rank(x,n):
    rows=[(x>>(i*n))&((1<<n)-1) for i in range(n)]
    pivots={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p not in pivots:
                pivots[p]=row
                break
            row^=pivots[p]
    return len(pivots)


def inverse(x,n):
    rows=[((x>>(i*n))&((1<<n)-1))|(1<<(n+i)) for i in range(n)]
    for j in range(n):
        p=next((i for i in range(j,n) if rows[i]>>j&1),None)
        if p is None:
            return None
        rows[p],rows[j]=rows[j],rows[p]
        for i in range(n):
            if i!=j and rows[i]>>j&1:
                rows[i]^=rows[j]
    return sum((row>>n)<<(i*n) for i,row in enumerate(rows))


def spectrum(n):
    size=1<<(n*n)
    out=np.zeros(size*size,dtype=np.int64)
    units=0
    for x in range(size):
        y=inverse(x,n)
        if y is not None:
            out[transpose(x,n)|(transpose(y,n)<<(n*n))]=1
            units+=1
    width=1
    while width<len(out):
        for start in range(0,len(out),2*width):
            left=out[start:start+width].copy()
            right=out[start+width:start+2*width].copy()
            out[start:start+width]=left+right
            out[start+width:start+2*width]=left-right
        width*=2
    return out,units


def main():
    summaries=[]
    for n in (1,2,3):
        values,units=spectrum(n)
        size=1<<(n*n)
        mult=np.array([[multiply(x,y,n) for y in range(size)] for x in range(size)],dtype=np.int32)
        ranks=np.array([rank(x,n) for x in range(size)])
        groups={}
        I=sum(1<<(i*n+i) for i in range(n))
        nilpotent_pairs=0
        for A in range(size):
            for B in range(size):
                AB=int(mult[A,B]); power=I
                for _ in range(n):
                    power=int(mult[power,AB])
                if power:
                    continue
                nilpotent_pairs+=1
                pa=pb=I;profile=[]
                for _ in range(2*n):
                    pa,pb=int(mult[A,pb]),int(mult[B,pa])
                    profile.extend([int(ranks[pa]),int(ranks[pb])])
                key=tuple(profile)
                value=int(values[A|(B<<(n*n))])
                if key not in groups:
                    groups[key]=dict(alternating_ranks=profile,K=value,representative=[A,B],pairs=0)
                assert groups[key]['K']==value,(n,A,B,key,value,groups[key])
                groups[key]['pairs']+=1
        np.savez_compressed(Path(__file__).with_name(f'pair_spectrum_n{n}.npz'),K=values,n=n)
        summaries.append(dict(matrix_rank=n,source_pairs=size*size,GL_size=units,
                              nilpotent_pairs=nilpotent_pairs,cyclic_quiver_types=len(groups),
                              nilpotent_type_data=list(groups.values()),
                              value_distribution=dict(Counter(int(x) for x in values))))
    path=Path(__file__).with_name('pair_spectrum_results.json')
    path.write_text(json.dumps(summaries,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in x.items() if k not in
        ('nilpotent_type_data','value_distribution')} for x in summaries]))


if __name__=='__main__':
    main()
