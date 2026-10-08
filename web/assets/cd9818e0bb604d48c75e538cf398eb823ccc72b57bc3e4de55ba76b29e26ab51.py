#!/usr/bin/env python3
"""Finite falsification tests for the HF encoding, not a proof of its theorem."""
import itertools, json
from pathlib import Path
from functools import lru_cache

class HF:
    __slots__=('index','atom','members')
    def __init__(self,index,a,m): self.index,self.atom,self.members=index,a,m
    def __iter__(self): return iter(self.members)
    def __contains__(self,x): return x in self.members
    def __hash__(self): return self.index
# Exact hash-consing preserves HF equality while avoiding exponential tree comparisons.
_pool={}
def atom(i):
    key=('atom',i)
    if key not in _pool: _pool[key]=HF(len(_pool),i,None)
    return _pool[key]
def hfset(xs=()):
    ms=frozenset(xs); key=('set',ms)
    if key not in _pool: _pool[key]=HF(len(_pool),None,ms)
    return _pool[key]
def is_atom(x): return x.atom is not None
def op(a,b): return hfset((hfset((a,)), hfset((a,b))))
@lru_cache(None)
def ordinal(i): return hfset(ordinal(j) for j in range(i))
def closure(xs):
    out=set(xs); todo=list(xs)
    while todo:
        x=todo.pop()
        if not is_atom(x):
            for y in x:
                if y not in out: out.add(y); todo.append(y)
    return out

def classes(D, eta):
    parent=list(range(len(D)))
    def root(i):
        while parent[i]!=i: i=parent[i]
        return i
    for i,j in eta:
        ri,rj=root(i),root(j)
        parent[ri]=rj
    return [frozenset(D[i] for i in range(len(D)) if root(i)==r) for r in set(root(i) for i in range(len(D)))]

def code_stage(D, eta, j):
    Cs=classes(D,eta)
    payload=[hfset(op(*p) for p in C) for C in Cs]
    codes=[op(ordinal(j),S) for S in payload]
    assert len(set(payload))==len(Cs)==len(set(codes))
    return Cs,payload,codes

@lru_cache(None)
def permute(x, p):
    if is_atom(x): return atom(p[x.atom])
    return hfset(permute(y,p) for y in x)

stats={}
# Ordered-pair injection includes atom/set mixtures and coinciding arguments.
objects=[atom(0),atom(1),hfset(),ordinal(1),ordinal(2),hfset((atom(0),)),hfset((atom(0),atom(1)))]
enc={}
for a,b in itertools.product(objects,repeat=2):
    e=op(a,b)
    assert e not in enc or enc[e]==(a,b)
    enc[e]=(a,b)
stats['ordered_pair_injection_cases']=len(enc)
# Exhaust every directed generating relation for every subset of a 2-atom pair domain.
A=[atom(0),atom(1)]; pairs=list(itertools.product(A,repeat=2)); cases=0
for dm in range(1<<len(pairs)):
    D=[p for i,p in enumerate(pairs) if dm>>i&1]; k=len(D)
    for mask in range(1<<(k*k)):
        eta=[(i,j) for i in range(k) for j in range(k) if mask>>(i*k+j)&1]
        Cs,payload,codes=code_stage(D,eta,1)
        # Independent bounded path definition used in the source.
        link={(i,i) for i in range(k)}|set(eta)|{(j,i) for i,j in eta}
        reach=set(link)
        for t in range(4):
            reach |= {(i,j) for i in range(k) for j in range(k) if any((i,z) in reach and (z,j) in link for z in range(k))}
        assert all(((i,j) in reach)==any(D[i] in C and D[j] in C for C in Cs) for i in range(k) for j in range(k))
        # Several non-class-invariant relations, using existential quotient semantics.
        for pred in (lambda a,b:a[0]==b[1], lambda a,b:a[1]==b[0] and b[0]==b[1]):
            rel={(i,j) for i,C in enumerate(Cs) for j,E in enumerate(Cs) if any(pred(a,b) for a in C for b in E)}
            reconstructed={(i,j) for i,C in enumerate(Cs) for j,E in enumerate(Cs) if any(pred(a,b) for a in D for b in D if op(*a) in payload[i] and op(*b) in payload[j])}
            assert rel==reconstructed
        fam=closure(A+codes+[ordinal(1)])
        B=max(2,len(A),len(codes),1)
        assert len(fam)<=9*B**3
        cases+=1
stats['exhaustive_domain_directed_eta_cases']=cases
print('Exhaustive quotient cases finished:', cases, flush=True)
# Arbitrarily nested symmetric quotients, and empty-state transitions.
run_tests=0; maxrank=0; max_family=0
for n in (2,3,4):
    for h in (1,2,4,8):
        for empty_after in (None,2):
            A=[atom(i) for i in range(n)]; U=A[:]; allcodes=[]; stages=[]
            for j in range(1,h+1):
                D=[] if empty_after and j>=empty_after else list(itertools.product(U,repeat=2))
                eta=[(i,k) for i,a in enumerate(D) for k,b in enumerate(D) if a[0]==b[0] and a[0]==a[1]]
                Cs,payload,U=code_stage(D,eta,j); stages.append(len(U)); allcodes.extend(U)
            fam=closure(A+allcodes+[ordinal(h)])
            B=max([2,n,h]+stages); T=n+h+sum(stages)
            assert len(fam)<=9*B**3
            assert len(fam)<=3*T*T
            perms=list(itertools.permutations(range(n)))
            for p in perms:
                assert {permute(x,p) for x in fam}==fam
            S=max([n]+stages)
            for x in fam:
                assert len({permute(x,p) for p in perms})<=S*S
            max_family=max(max_family,len(fam)); run_tests+=1
stats['symmetric_multistage_and_empty_run_cases']=run_tests
stats['largest_tested_transitive_family']=max_family
stats['all_recursive_individual_orbits_at_most_max_state_squared']=True
# A minimal finite example showing why molecule counts alone are not object counts.
for n in (2,3,4,5):
    A=[atom(i) for i in range(n)]; val=hfset(A)
    values=[val for a in A]
    assert len(values)==n and len(set(values))==1
stats['naive_molecule_count_negative_controls']=4
stats['all_assertions_passed']=True
Path(__file__).with_name('encoding_test_results.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
