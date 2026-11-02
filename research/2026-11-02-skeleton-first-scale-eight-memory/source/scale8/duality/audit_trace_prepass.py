"""Exhaustive tiny cancellation-gate test for the bottom linear prepass."""
import itertools
import numpy as np
cases=0
for mask in range(1<<9):
    L=np.array([(mask>>i)&1 for i in range(9)],dtype=int).reshape(3,3)
    for bits in itertools.product((0,1),repeat=3):
        s=np.array(bits);u=L@s%2
        active=set(np.flatnonzero(s));adj={j:set() for j in active}
        for i in range(3):
            contributors=set(np.flatnonzero(L[i]*s))
            if contributors:
                gate=3+i;active.add(gate);adj[gate]=contributors
                for j in contributors:adj[j].add(gate)
        comps=[]
        while active:
            stack=[active.pop()];comp=set(stack)
            while stack:
                for v in adj[stack.pop()]:
                    if v not in comp:comp.add(v);active.discard(v);stack.append(v)
            comps.append(comp)
        for choice in itertools.product((0,1),repeat=len(comps)):
            selected=set().union(*(c for c,b in zip(comps,choice) if b))
            tau=np.array([int(j in selected)*s[j] for j in range(3)])
            uc=np.array([int(3+i in selected)*u[i] for i in range(3)])
            assert np.array_equal(L@tau%2,uc)
            cases+=1
print('PASS:',cases,'whole-component selections over every binary 3x3 map/input.')
L=np.array([[1,1]]);s=np.array([1,1]);tau=np.array([1,0])
assert not (L@s%2).any() and (L@tau%2).any()
print('Negative control: dropping the zero-output gate separates [1,1], allowing invalid restricted output [1].')
