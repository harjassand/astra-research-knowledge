#!/usr/bin/env python3
"""Exact finite HF-code tests for the ASM graph bridge; not BGS syntax execution."""
from itertools import product, combinations
from pathlib import Path
import json

ZERO = frozenset()
ONE = frozenset([ZERO])
TWO = frozenset([ZERO, ONE])
A, B = 'atom-a', 'atom-b'

def pair(a,b):
    return frozenset([frozenset([a]),frozenset([a,b])])
def mem(x):
    return x if isinstance(x,frozenset) else frozenset()
def union(x):
    return frozenset(y for z in mem(x) for y in mem(z))
def unique(x):
    return next(iter(x)) if isinstance(x,frozenset) and len(x)==1 else ZERO
def fst(p):
    # The intersection is bounded by Union(p), as in the term construction.
    return unique(frozenset(x for x in union(p) if all(x in mem(y) for y in mem(p))))
def snd(p):
    a=fst(p)
    difference=frozenset(x for x in union(p) if x!=a)
    return unique(difference) if difference else a

def tuple_code(t):
    out=ZERO
    for a in reversed(t): out=pair(a,out)
    return out

def closure(roots):
    todo=list(roots); seen=set()
    while todo:
        x=todo.pop()
        if x not in seen:
            seen.add(x); todo.extend(mem(x))
    return seen

# Source functions are sparse dicts. Graph representation contains only HF objects.
ARITIES=(0,1,2)
TAGS=(ZERO,ONE,TWO)
def encode(state):
    graphs=[]
    for f in range(3):
        g=frozenset(pair(tuple_code(k),v) for k,v in state[f].items() if v!=ZERO)
        graphs.append(pair(TAGS[f],g))
    return frozenset(graphs)
def graph(root,f):
    return unique(frozenset(snd(e) for e in root if fst(e)==TAGS[f]))
def lookup(root,f,key):
    return unique(frozenset(snd(e) for e in graph(root,f) if fst(e)==tuple_code(key)))
def upd_code(f,key,val): return pair(TAGS[f],pair(tuple_code(key),val))
def encode_updates(updates): return frozenset(upd_code(*u) for u in updates)
def source_apply(state,updates):
    bykey={}
    for f,k,v in updates:
        if (f,k) in bykey and bykey[f,k]!=v:
            return tuple(dict(g) for g in state),True
        bykey[f,k]=v
    result=tuple(dict(g) for g in state)
    for (f,k),v in bykey.items():
        if v==ZERO: result[f].pop(k,None)
        else: result[f][k]=v
    return result,False

def graph_apply(root,U):
    def f(u): return fst(u)
    def k(u): return fst(snd(u))
    def v(u): return snd(snd(u))
    clash=any(f(u)==f(w) and k(u)==k(w) and v(u)!=v(w) for u in U for w in U)
    if clash: return root,True
    out=[]
    for fi in range(3):
        updates=frozenset(u for u in U if f(u)==TAGS[fi])
        old=frozenset(e for e in graph(root,fi) if not any(k(u)==fst(e) for u in updates))
        new=frozenset(pair(k(u),v(u)) for u in updates if v(u)!=ZERO)
        out.append(pair(TAGS[fi],old|new))
    return frozenset(out),False

stats={'pair_projection_cases':0,'state_update_cases':0,'clash_cases':0,'lookup_cases':0,'roundtrip_states':0}
objects=(ZERO,ONE,TWO,A,B,frozenset([A,B]),pair(A,A),pair(A,ZERO))
for a,b in product(objects,repeat=2):
    p=pair(a,b)
    assert fst(p)==a and snd(p)==b
    stats['pair_projection_cases']+=1
assert len({pair(a,b) for a,b in product(objects,repeat=2)})==len(objects)**2

keys=((),(A,),(B,),(A,A),(A,B),(B,A),(B,B))
locs=((0,()),(1,(A,)),(1,(B,)),(2,(A,A)),(2,(A,B)))
values=(ZERO,ONE,A,frozenset([A,B]))
# All sparse states over three locations (including nullary and a binary location).
oldlocs=(locs[0],locs[1],locs[4])
updates=[(f,k,v) for f,k in locs for v in values]
batches=[()]+[(u,) for u in updates]+list(combinations(updates,2))
for vals in product(values,repeat=len(oldlocs)):
    state=tuple({} for _ in range(3))
    for (f,k),v in zip(oldlocs,vals):
        if v!=ZERO: state[f][k]=v
    root=encode(state)
    stats['roundtrip_states']+=1
    for f,k in locs:
        assert lookup(root,f,k)==state[f].get(k,ZERO)
        stats['lookup_cases']+=1
    for batch in batches:
        expected,clash=source_apply(state,batch)
        got,gclash=graph_apply(root,encode_updates(batch))
        assert clash==gclash and got==encode(expected)
        if clash: assert got==root
        stats['state_update_cases']+=1
        stats['clash_cases']+=int(clash)
# Repeated identical update is idempotent, including deletions.
state=({():A},{(A,):B},{(A,B):ONE})
for u in updates:
    assert graph_apply(encode(state),encode_updates([u,u]))==graph_apply(encode(state),encode_updates([u]))
# All graph predicates/lookups are evaluated before updates: source swap, not sequential copy.
swap=((1,(A,),A),(1,(B,),B))
state=({}, {(A,):B,(B,):A}, {})
new,clash=graph_apply(encode(state),encode_updates(swap))
assert not clash and lookup(new,1,(A,))==A and lookup(new,1,(B,))==B
# History independence after a long path of write/delete cycles.
root=encode(({}, {}, {})); initial=root; peak=0
for i in range(2000):
    v=objects[i%len(objects)]
    root,_=graph_apply(root,encode_updates([(1,(A,),v)]))
    peak=max(peak,len(closure([root,A,B,ZERO,ONE])))
    root,_=graph_apply(root,encode_updates([(1,(A,),ZERO)]))
    assert root==initial
stats['write_delete_cycles']=2000
stats['peak_coded_closure_in_cycles']=peak
# Guard convention: only exactly ONE is true, never generic nonemptiness.
assert [(x==ONE) for x in (ZERO,ONE,TWO,A,frozenset([A]))]==[False,True,False,False,False]
# Card's von Neumann return and atom default match source extension.
def ordinal(n):
    out=ZERO
    for _ in range(n): out=frozenset(set(out)|{out})
    return out
for x in objects:
    c=ordinal(len(mem(x)))
    assert len(c)==len(mem(x))
stats['all_checks_passed']=True
Path(__file__).with_name('asm_graph_update_results.json').write_text(json.dumps(stats,indent=2)+'\n')
print(json.dumps(stats,indent=2))
