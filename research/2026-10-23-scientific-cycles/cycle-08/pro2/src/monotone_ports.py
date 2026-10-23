"""Existence-preserving flag dominance on the exact active-port algebra.
Guarantees use realized flags bounded ABOVE by each requested profile.
"""
from active_ports import *
from collections import defaultdict

def base(s):return s[0],s[1],s[2],s[4]

def below(a,b):
    return base(a)==base(b) and (a[3]&b[3])==a[3] and (a[5]&b[5])==a[5]

@lru_cache(128)
def groups(states):
    out=defaultdict(list)
    for s in expanded(states):out[base(s)].append(s)
    return dict(out)

def reduce(states):
    out=set()
    gr=defaultdict(set)
    # Candidate output sets are transient. Do not retain their full color
    # expansions in the global basis caches.
    for s in states:
        for t in orbit(s):gr[base(t)].add(t)
    for ss in gr.values():
        for s in ss:
            if not any(t!=s and below(t,s) for t in ss):out.add(canonical(s))
    return frozenset(out)

@lru_cache(512)
def covers(realizers,targets):
    gr=groups(realizers)
    return all(any(below(t,s) for t in gr.get(base(s),())) for s in targets)

def covering_witness(realizers,target):
    return next(s for s in groups(realizers).get(base(target),()) if below(s,target))
