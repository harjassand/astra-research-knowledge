#!/usr/bin/env python3
"""Small-field validation oracle for balanced cyclic two-quiver strings.

Exponential in matrix dimension. It is a conjecture-testing oracle, not a
claimed counting algorithm. A string (length, first_color) has arrows from
successive basis elements toward the previous element.
"""
from pathlib import Path
from itertools import combinations_with_replacement
import json,time
import numpy as np
from pair_spectrum_oracle import inverse,multiply,rank,transpose

def string_types(n):
    choices=[(l,c) for l in range(1,2*n+1) for c in (0,1)]
    dims=lambda p: ((p[0]+(p[1]==0))//2,(p[0]+(p[1]==1))//2)
    def rec(start,left,right,parts):
        if left==right==0:
            yield parts;return
        for i in range(start,len(choices)):
            x,y=dims(choices[i])
            if x<=left and y<=right:
                yield from rec(i,left-x,right-y,parts+(choices[i],))
    yield from rec(0,n,n,())

def matrices(parts,n):
    cnt=[0,0];A=B=0
    for length,c in parts:
        prev=None
        for j in range(length):
            col=(c+j)%2;i=cnt[col];cnt[col]+=1
            if prev is not None:
                oldcol,oldi=prev
                if col==1:A|=1<<(oldi*n+i)
                else:B|=1<<(oldi*n+i)
            prev=(col,i)
    assert cnt==[n,n]
    return A,B

def profile(A,B,n):
    L,R=A,B;out=[]
    for j in range(2*n):
        out.extend((rank(L,n),rank(R,n)))
        L,R=multiply(L,B if j%2==0 else A,n),multiply(R,A if j%2==0 else B,n)
    return out

def run(n=4):
    start=time.perf_counter()
    size=1<<(n*n)
    inverses=[(x,inverse(x,n)) for x in range(size)]
    pairs=[(x,y) for x,y in inverses if y is not None]
    xs=np.array([x for x,y in pairs],dtype=np.uint64)
    ys=np.array([y for x,y in pairs],dtype=np.uint64)
    parity=np.array([i.bit_count()%2 for i in range(size)],dtype=np.uint8)
    data=[]
    for parts in string_types(n):
        A,B=matrices(parts,n)
        signs=parity[xs & transpose(A,n)]^parity[ys & transpose(B,n)]
        value=len(xs)-2*int(signs.sum())
        data.append(dict(strings=parts,A=A,B=B,alternating_ranks=profile(A,B,n),K=value))
    result=dict(n=n,q=2,GL_size=len(xs),types=len(data),seconds=time.perf_counter()-start,data=data)
    Path(__file__).with_name(f'nilpotent_strings_n{n}.json').write_text(json.dumps(result,indent=2))
    print(json.dumps({k:v for k,v in result.items() if k!='data'}))
    for d in data:print(d['strings'],d['K']//(2**(n*(n-1)//2)))

if __name__=='__main__':run()
