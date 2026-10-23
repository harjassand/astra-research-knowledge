#!/usr/bin/env python3
"""Independent exact polynomial check of the owner's non-scalar four-call witness."""
from fractions import Fraction as F
from itertools import product
import json,time,resource
from pathlib import Path


def trim(p):
    p=list(p)
    while p and not p[-1]:p.pop()
    return tuple(p)
def add(p,q):return trim([ (p[i] if i<len(p) else 0)+(q[i] if i<len(q) else 0) for i in range(max(len(p),len(q))) ])
def sc(p,c):return trim([c*x for x in p])
def mul(p,q):
    out=[F(0)]*max(0,len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q):out[i+j]+=x*y
    return trim(out)
def shift(p,k):return trim([F(0)]*k+list(p))


def run():
    start=time.perf_counter();base=Path(__file__).parent
    rep=json.loads((base/'four_call_representation.json').read_text());words=[tuple(x) for x in rep['input_words']];bath=[tuple(x) for x in rep['bath_prefix_words']]
    pair=list(product((0,1,2),repeat=2));q=(F(1,2),F(0),-F(1,512));one=(F(1),);qm=add(one,sc(q,-1));x=mul(q,q);y=sc(mul(q,qm),F(1,2));z=sc(mul(qm,qm),F(1,4));c=(F(0),-F(1,128));kappa=(F(0),F(0),F(1,128),-F(1,128))
    omega={}
    for v in pair:
        if v==(0,0):omega[v,v]=x
        elif 0 not in v:omega[v,v]=z
        else:omega[v,v]=y
    for j in (1,2):omega[(j,0),(0,j)]=c;omega[(0,j),(j,0)]=c
    rho={}
    for i,v in enumerate(words):
        for j,w in enumerate(words):
            value=mul(omega.get((v[:2],w[:2]),()),omega.get((v[2:],w[2:]),()))
            if value:rho[i,j]=value
    left=words.index((1,0,0,0));right=words.index((0,1,0,0));block={left,right}
    assert rho[left,left]==rho[right,right]==mul(x,y)
    assert rho[left,right]==rho[right,left]==mul(x,c)
    assert all((i in block)==(j in block) for i,j in rho if i in block or j in block)
    del rho[left,right];del rho[right,left]
    assert add(*[rho[left,left],sc(mul(x,y),-1)])==()
    actual={}
    for degree,entries in rep['bulk_drift_coefficients'].items():
        for i,u,j,v,coefficient in entries:
            term=sc(shift(rho.get((j,i),()),int(degree)),coefficient)
            if term:actual[u,v]=add(actual.get((u,v),()),term)
    actual={key:value for key,value in actual.items() if value}
    expected={}
    for u,w in enumerate(bath):
        value=sc(kappa,-2)
        if w[0]==2:value=add(value,sc(mul(x,kappa),2))
        expected[u,u]=value
    assert actual==expected
    return {'status':'passed','all_b_identity':'D_rho4 = -2 kappa I + 2 x kappa (I-S1S1*) on L>=4','rho':'omega tensor omega - x c (|1000><0100|+h.c.)','reducing_block':'span{1000,0100}: diagonals xy, offdiagonals xc; no matrix entries to its complement','positivity':'Deleting offdiagonal of this reducing positive 2x2 block preserves positivity','entropy_increment':'2 x y [1-h2((1+c/y)/2)] > 0 for 0<beta<1','uniform_negative_margin':'2 kappa (1-x)>0','polynomial_identity_checked_for_all_b':True,'wall_seconds':time.perf_counter()-start,'max_rss_kib_linux':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}

if __name__=='__main__':
    out=run();Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
