#!/usr/bin/env python3
"""Exact small-instance check of path/cycle fixed-filter identities.

Uses rational Gaussian arithmetic and direct permutation expansion. Finite
checks only; the general proof is stated in LEAD_RESULT.txt.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
import json
from pathlib import Path


def gadd(a,b): return (a[0]+b[0], a[1]+b[1])
def gneg(a): return (-a[0],-a[1])
def gmul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def gabs2(a): return a[0]*a[0]+a[1]*a[1]
ZERO=(F(0),F(0))
ONE=(F(1),F(0))

def det(a):
    n=len(a)
    z=ZERO
    for p in permutations(range(n)):
        inv=sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=ONE
        for i,j in enumerate(p): term=gmul(term,a[i][j])
        z=gadd(z, gneg(term) if inv%2 else term)
    return z

def minor(a,I,J): return [[a[i][j] for j in J] for i in I]

def direct_z(a,k):
    n=len(a); total=F(0); count=0
    for I in combinations(range(n),k):
        for J in combinations(range(n),k):
            if set(I).isdisjoint(J):
                total += gabs2(det(minor(a,I,J))); count+=1
    return total,count

def matching_poly(n,edges,weights,k):
    ans=F(0)
    def rec(pos,used,chosen,w):
        nonlocal ans
        if chosen==k:
            ans += w; return
        if pos==len(edges) or chosen+(len(edges)-pos)<k: return
        rec(pos+1,used,chosen,w)
        u,v=edges[pos]
        if u not in used and v not in used:
            rec(pos+1,used|{u,v},chosen+1,w*weights[pos])
    rec(0,set(),0,F(1))
    return ans

def build(n,cycle):
    a=[[ZERO for _ in range(n)] for _ in range(n)]
    edges=[(i,(i+1)%n) for i in range(n if cycle else n-1)]
    for i,j in edges:
        # Different rational complex amplitudes in both directions.
        a[i][j]=(F(i+2,3),F(j+1,5))
        a[j][i]=(F(j+3,7),F(i+1,4))
    return a,edges

def product(vals):
    x=ONE
    for v in vals: x=gmul(x,v)
    return x

def predict(a,edges,k,cycle):
    n=len(a)
    ws=[gabs2(a[i][j])+gabs2(a[j][i]) for i,j in edges]
    base=matching_poly(n,edges,ws,k)
    if cycle and n%2==0 and k==n//2:
        ev=tuple(range(0,n,2)); od=tuple(range(1,n,2))
        even=set(ev)
        ms=[edges[::2], edges[1::2]]
        excl=F(0)
        for M in ms:
            forward=[]; reverse=[]
            for u,v in M:
                if u in even:
                    forward.append(a[u][v]); reverse.append(a[v][u])
                else:
                    forward.append(a[v][u]); reverse.append(a[u][v])
            excl += gabs2(product(forward))+gabs2(product(reverse))
        d1=det(minor(a,ev,od)); d2=det(minor(a,od,ev))
        base=base-excl+gabs2(d1)+gabs2(d2)
    return base

def run_case(name,n,cycle):
    a,edges=build(n,cycle); out=[]
    for k in range(n//2+1):
        z,count=direct_z(a,k)
        p=predict(a,edges,k,cycle)
        assert z==p,(name,k,z,p)
        out.append({'k':k,'Z':str(z),'disjoint_pairs_checked':count})
    return {'case':name,'n':n,'identity_checks':len(out),'sectors':out}

def main():
    cases=[run_case('path6',6,False),run_case('odd_cycle5',5,True),
           run_case('even_cycle4',4,True),run_case('even_cycle6',6,True)]
    result={'status':'PASS','arithmetic':'exact rational Gaussian pairs',
            'cases':cases,'scope':'Finite evidence only; proof and bit costs are in LEAD_RESULT.txt.'}
    path=Path(__file__).with_name('nearest_neighbor_check.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','cases':len(cases),
                      'sectors':sum(x['identity_checks'] for x in cases),
                      'output':str(path)}))
if __name__=='__main__': main()
