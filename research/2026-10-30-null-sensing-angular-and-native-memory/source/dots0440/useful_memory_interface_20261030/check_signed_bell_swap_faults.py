#!/usr/bin/env python3
"""Independent exact integer matrix test of the swap's relative-error formula."""
import json, random
import numpy as np
n=4;dim=1<<n
I=np.eye(dim,dtype=np.int64)
def parity(x):return x.bit_count()&1
def pauli(x,z):
    a=np.zeros((dim,dim),dtype=np.int64)
    for j in range(dim):a[j^x,j]=-1 if parity(j&z) else 1
    return a
G=[pauli(15,0),pauli(0,15)]
P={(x,z):pauli(x,z) for x in range(dim) for z in range(dim)}
def syn(x,z):return parity(z&15)|(parity(x&15)<<1)
# Scaled syndrome projectors, Pi_s=Q_s/4.
Q={s:(I+(-1 if s&1 else 1)*G[0])@(I+(-1 if s&2 else 1)*G[1]) for s in range(4)}
single=[(0,0)]+[(1<<i,0) for i in range(n)]+[(0,1<<i) for i in range(n)]+[(1<<i,1<<i) for i in range(n)]
rng=random.Random(20261030);cases=8192;negative=0
for j in range(cases):
    s=rng.randrange(4); p=(rng.randrange(dim),rng.randrange(dim))
    e1=rng.choice(single);e2=rng.choice(single);g=rng.choice(single)
    t=s^syn(*p)^syn(*e1)
    E1=P[e1];E2=P[e2];PP=P[p];F=P[g]
    # A raw physical Bell outcome P followed by the correct mask P.
    out=Q[s]@E1.T@PP@Q[t]@E2.T@PP.T
    target=4*Q[s]@E1.T@E2.T
    assert np.array_equal(out,target) or np.array_equal(out,-target)
    negative+=int(np.array_equal(out,-target))
    # Corruption of the reported mask adds a local output Pauli F.
    badmask=F@PP
    noisy=Q[s]@E1.T@PP@Q[t]@E2.T@badmask.T
    noisy_target=4*Q[s]@E1.T@E2.T@F.T
    assert np.array_equal(noisy,noisy_target) or np.array_equal(noisy,-noisy_target)
    forbidden=Q[s]@E1.T@PP@Q[t^1]@E2.T@PP.T
    assert not np.any(forbidden)
print(json.dumps({'code':'[[4,2,2]] CSS','seed':20261030,'exact_integer_trials':cases,
 'incoming_relative_error_formula':'passed','sparse_mask_corruption_formula':'passed',
 'forbidden_outcome_formula':'passed','record_dependent_negative_phase_cases':negative},indent=2))
