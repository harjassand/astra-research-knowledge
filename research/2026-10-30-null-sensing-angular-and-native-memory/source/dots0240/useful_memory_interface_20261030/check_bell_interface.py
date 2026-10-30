#!/usr/bin/env python3
"""Exact small-code sanity check; not a replacement for the general proof."""
import itertools, json
H=[int(s,2) for s in ('1111000','1100110','1010101')]
C={0}
for h in H: C|={c^h for c in list(C)}
assert len(C)==8
ones=127
parity=lambda x:x.bit_count()%2
results=[]
for a,b in itertools.product(range(2), repeat=2):
    after={}
    for l in range(2):
        for c in C:
            u=c^(ones if l else 0)
            for d in C:
                v=d^(ones if l^b else 0)
                after[u,v^u]=after.get((u,v^u),0)+(-1 if a*l else 1)
    observed={}
    for (u,v),amp in after.items():
        for x in range(128):
            observed[x,v]=observed.get((x,v),0)+amp*(-1 if parity(x&u) else 1)
    nz=[((x,z),amp) for (x,z),amp in observed.items() if amp]
    assert nz
    for (x,z),amp in nz:
        assert all(parity(h&x)==0 for h in H)
        assert all(parity(h&z)==0 for h in H)
        assert parity(x)==a and parity(z)==b
    results.append({'a':a,'b':b,'nonzero_fine_outcomes':len(nz),'logical_labels_exact':True})
for xa,xb,za,zb in itertools.product(range(2), repeat=4):
    assert bool(xa or xb)==bool(xa or (xa^xb))
    assert bool(za or zb)==bool((za^zb) or zb)
print(json.dumps({'steane_bell_cases':results,'paired_column_support_check':'all 16 Pauli patterns passed'},indent=2))
