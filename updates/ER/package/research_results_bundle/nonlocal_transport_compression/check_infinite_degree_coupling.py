#!/usr/bin/env python3
"""Compact cycle witness: every odd k>=3 balanced degree-k space couples to k+2.
Integer Pauli/graph edge coordinates on the infinite translation quotient.
This is an invariant-subspace obstruction, not growth of the physical seed at all m.
"""
from collections import defaultdict

def edge(i,S): return tuple(sorted(s-i for s in S))
def vertex(S): return tuple(sorted(s-min(S) for s in S))
def add_term(d,key,c):
    d[key]+=c
    if d[key]==0:del d[key]
def square(S,a,b):
    S=set(S);out=defaultdict(int)
    assert a in S and b in S and a+1 not in S and b+1 not in S
    A=S-{a}|{a+1};B=S-{b}|{b+1}
    for i,U,c in [(a,S,1),(b,A,1),(a,B,-1),(b,S,-1)]:
        add_term(out,edge(i,U-{i}),c)
    return out

def divergence(f):
    d=defaultdict(int)
    for S,c in f.items():
        add_term(d,vertex((*S,1)),c)
        add_term(d,vertex((*S,0)),-c)
    return dict(d)
def raise_degree(f):
    d=defaultdict(int)
    for S,c in f.items():
        if -1 not in S and 2 not in S:
            add_term(d,tuple(sorted((*S,-1,2))),c)
    return d

for k in range(3,16,2):
    spectators={6+3*j for j in range(k-2)}
    q=square({0,3}|spectators,0,3)
    w=square({-1,0,2,3}|spectators,0,6)
    assert not divergence(q) and not divergence(w)
    r=raise_degree(q)
    pairing=sum(c*r.get(S,0) for S,c in w.items())
    assert pairing==1
    assert sum(c*c for c in q.values())==sum(c*c for c in w.values())==4
    print('k=',k,'div(q)=div(w)=0, <w,R+q>=',pairing)
    if k==3:
        print('q=',dict(q));print('w=',dict(w));print('R+q=',dict(r))
