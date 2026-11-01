#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import json

def check(parts,n,cap=4):
    hubs=[(i,j) for left,right in parts for i in left for j in right]
    edges=[]
    def vec(i,j=None):
        v=[0]*n;v[i]+=1
        if j is not None:v[j]+=1
        return tuple(v)
    for h,(i,j) in enumerate(hubs):
        H=vec(i,j)
        edges.append((vec(0,0),H,F(h+1), 'forward_seed'))
        edges.append((H,vec(0,0),F(h+2), 'reverse_seed'))
        for x in range(1,n):
            edges.append((vec(0,x),H,F(h+x+1), 'forward_arm'))
            edges.append((H,vec(0,x),F(h+x+2), 'reverse_arm'))
    def R(x):return x[0]+sum(min(sum(x[i] for i in L),sum(x[j] for j in D)) for L,D in parts)
    def enabled(x,u):return all(a>=b for a,b in zip(x,u))
    def rat(x,u,k):
        for a,b in zip(x,u):
            for j in range(b):k*=a-j
        return k
    kx={i:sum(e[2] for e in edges if e[3]=='forward_arm' and e[0][i]) for i in range(1,n)}
    kmin=min(kx.values());kmax=max(kx.values())
    amin=sum(e[2] for e in edges if e[3]=='forward_seed')
    bmin=min(e[2] for e in edges if e[3]=='reverse_seed')
    jumps=states=0
    for x in product(range(cap),repeat=n):
        r=R(x);a=x[0];z=r-a;N=sum(x)
        neutral=bad=seed=F(0);any_enabled=False
        for u,v,k,kind in edges:
            if not enabled(x,u):continue
            any_enabled=True
            y=tuple(a-b+c for a,b,c in zip(x,u,v));dr=R(y)-r
            q=rat(x,u,k)
            assert r>=1 and R(y)>=1
            if kind=='forward_arm':
                assert dr in (-1,0)
                if dr==0:
                    neutral+=q
                    assert F(y[0],(R(y)+1)**2)-F(a,(r+1)**2)==-F(1,(r+1)**2)
                else:bad+=q
            if kind=='forward_seed':
                assert dr==-1;bad+=q
            if kind=='reverse_seed':
                assert dr==1;seed+=q
            assert abs(F(y[0],(R(y)+1)**2)-F(a,(r+1)**2))<=F(11,(r+1)**2)
            jumps+=1
        if r==0:assert not any_enabled
        assert neutral>=kmin*a*(N-2*r+a)
        assert bad<=(amin+2*kmax)*a*r
        assert seed>=bmin*F(z*z,len(parts))
        product_sum=sum(x[i]*x[j] for i,j in hubs)
        assert product_sum==sum(sum(x[i] for i in L)*sum(x[j] for j in D) for L,D in parts)
        states+=1
    return {'parts':parts,'species':n,'states':states,'enabled_jumps':jumps,'status':'passed'}

def main():
    result=[check([([2,3],[4,5])],6),check([([2],[3]),([4],[5])],6)]
    # Bipartite but not complete: missing edge(2,4), stock only those endpoints.
    missing_edge_graph=[(1,3),(1,4),(2,3)]
    x={1:0,2:1,3:0,4:1}
    assert sum(x[i]*x[j] for i,j in missing_edge_graph)==0
    assert min(x[1]+x[2],x[3]+x[4])==1
    return {'scope':'pending geometry only; no full Lyapunov/receiver acceptance',
            'fixtures':result,'incomplete_bipartite_negative_control':'passed'}
if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
