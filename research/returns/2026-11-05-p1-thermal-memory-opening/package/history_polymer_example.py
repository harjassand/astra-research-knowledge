#!/usr/bin/env python3
"""Exact finite check of a hierarchical syndrome-history polymer representation.

Synthetic linear-code example, not the 3D BDL code or a physical memory.
At each internal vertex: a xor b = c xor d = parent; root=0.
Only leaf defects cost energy. Eliminating the unique history produces
growing-weight metachecks; keeping it gives a bounded-degree local model.
"""
from fractions import Fraction
from itertools import combinations
from math import log10
import json
from pathlib import Path

def tree(depth):
    count = (4**(depth+1)-1)//3
    internal = (4**depth-1)//3
    children = {v:tuple(4*v+i for i in range(1,5)) for v in range(internal)}
    adj = [set() for _ in range(count)]
    for v,ch in children.items():
        for a,b in combinations((v,)+ch,2):
            adj[a].add(b); adj[b].add(a)
    return count,internal,children,adj

def valid_history(bits,children):
    return not bits[0] and all((bits[a]^bits[b]) == bits[v] == (bits[c]^bits[d])
                              for v,(a,b,c,d) in children.items())

def from_leaves(mask,count,internal,children):
    bits=[0]*count
    for i in range(count-internal): bits[internal+i]=(mask>>i)&1
    for v in reversed(range(internal)):
        a,b,c,d=children[v]
        left,right=bits[a]^bits[b],bits[c]^bits[d]
        if left != right: return None
        bits[v]=left
    return tuple(bits) if not bits[0] else None

def components(bits,adj):
    unseen={i for i,b in enumerate(bits) if b}; result=[]
    while unseen:
        stack=[unseen.pop()]; piece=set(stack)
        while stack:
            v=stack.pop(); near=adj[v]&unseen
            unseen.difference_update(near); piece.update(near); stack.extend(near)
        result.append(frozenset(piece))
    return result

def partition_functions(depth,x):
    z=[(Fraction(1),x)]
    for _ in range(depth):
        a,b=z[-1]; z.append(((a*a+b*b)**2,4*a*a*b*b))
    return z

def generated_probability(bits,v,height,children,z):
    if height==0: return Fraction(1)
    a,b,c,d=children[v]; probability=Fraction(1)
    for u,w in [(a,b),(c,d)]:
        p0,p1=z[height-1]
        denominator=p0*p0+p1*p1 if bits[v]==0 else 2*p0*p1
        probability *= z[height-1][bits[u]]*z[height-1][bits[w]]/denominator
    for u in (a,b,c,d): probability *= generated_probability(bits,u,height-1,children,z)
    return probability

def check(depth=2,x=Fraction(1,10)):
    count,internal,children,adj=tree(depth); leaves=count-internal
    histories=[]; polymers=set()
    for mask in range(1<<leaves):
        bits=from_leaves(mask,count,internal,children)
        if bits is None: continue
        assert valid_history(bits,children); histories.append(bits)
        pieces=components(bits,adj); polymers.update(pieces)
        for piece in pieces:
            isolated=tuple(int(v in piece) for v in range(count))
            assert valid_history(isolated,children)
            assert from_leaves(sum(isolated[internal+i]<<i for i in range(leaves)),
                               count,internal,children)==isolated
            assert len(piece)<=2*sum(isolated[internal:])
        product=Fraction(1)
        for piece in pieces: product*=x**sum(v>=internal for v in piece)
        assert product==x**sum(bits[internal:])
    pair_checks=0
    for first,second in combinations(polymers,2):
        if first.isdisjoint(second) and all(not(adj[v]&second) for v in first):
            union=first|second; bits=tuple(int(v in union) for v in range(count))
            assert valid_history(bits,children)
            assert set(components(bits,adj))=={first,second}
            pair_checks+=1
    z=partition_functions(depth,x)
    enumeration_z=sum((x**sum(bits[internal:]) for bits in histories),Fraction(0))
    assert enumeration_z==z[depth][0]
    total=Fraction(0)
    for bits in histories:
        actual=generated_probability(bits,0,depth,children,z)
        assert actual==x**sum(bits[internal:])/enumeration_z
        total+=actual
    assert total==1
    ratio_values=[]
    for level,(a,b) in enumerate(partition_functions(6,x)):
        r=b/a; assert r <= (4*x)**(2**level)/4
        ratio_values.append({'level':level,'leaf_count':4**level,
                             'log10_ratio':log10(r.numerator)-log10(r.denominator)})
    return {'status':'all exact Fraction checks passed','physical_trials':0,
            'model':'synthetic hierarchical linear syndrome constraints, not the BDL quantum memory',
            'depth':depth,'leaves':leaves,'history_variables':count,
            'valid_histories':len(histories),'distinct_polymers':len(polymers),
            'compatible_polymer_pair_checks':pair_checks,
            'max_host_degree':max(map(len,adj)),'fugacity':str(x),
            'partition_function':str(enumeration_z),
            'properties':['unique history','component deletion','component recombination',
                          'additive physical energy','history size <= twice leaf defects',
                          'recursive sampler equals target distribution exactly'],
            'coarse_defect_ratio':ratio_values}

if __name__=='__main__':
    result=check()
    Path(__file__).with_name('history_polymer_example.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
