#!/usr/bin/env python3
"""Exact integer-amplitude Steane sanity checks, not the general proof."""
import itertools, json
H=[int(s,2) for s in ('1111000','1100110','1010101')]
N=7; ONES=(1<<N)-1
par=lambda a:a.bit_count()&1
# Generators first Z, then X. Pauli convention X^x Z^z (real unitary).
gens=[(0,h) for h in H]+[(h,0) for h in H]
def synd(x,z):
    return sum((par(x&gz)^par(z&gx))<<j for j,(gx,gz) in enumerate(gens))
def pauli(v,x,z,side):
    out={}
    for (a,b),amp in v.items():
        c=a if side==0 else b
        key=(a^x,b) if side==0 else (a,b^x)
        out[key]=amp*(-1 if par(c&z) else 1)
    return out
def add(a,b,f=1):
    out=dict(a)
    for x,v in b.items(): out[x]=out.get(x,0)+f*v
    return {x:v for x,v in out.items() if v}
def common(v,x,z): return pauli(pauli(v,x,z,0),x,z,1)
# Any syndrome preimage suffices; minimum weight is convenient for the test.
reps={}
for weight,x,z in sorted(((x|z).bit_count(),x,z) for x in range(128) for z in range(128)):
    reps.setdefault(synd(x,z),(x,z))
assert len(reps)==64
C={0}
for h in H: C|={c^h for c in list(C)}
omega0={(c^(ONES if l else 0),d^(ONES if l else 0)):1
        for l in range(2) for c in C for d in C}
assert len(omega0)==128
omegas={s:common(omega0,*reps[s]) for s in range(64)}
raw={(x,x):1 for x in range(128)}
raw_from_gauge={}
for v in omegas.values(): raw_from_gauge=add(raw_from_gauge,v)
assert raw_from_gauge=={x:8*v for x,v in raw.items()}
# Complete ideal syndrome projection on A gives Omega_s / 8.
for s,v in omegas.items():
    projected=raw
    for j,(x,z) in enumerate(gens):
        projected=add(projected,pauli(projected,x,z,0),-1 if (s>>j)&1 else 1)
    # Projector denominator 2^6; normalized Omega_s factor 8.
    assert projected=={x:8*a for x,a in v.items()}
    for j,(x,z) in enumerate(gens):
        sign=-1 if (s>>j)&1 else 1
        assert pauli(v,x,z,0)=={i:sign*a for i,a in v.items()}
        assert pauli(v,x,z,1)=={i:sign*a for i,a in v.items()}
    assert common(v,ONES,0)==v and common(v,0,ONES)==v
single=[(1<<i,0) for i in range(N)]+[(0,1<<i) for i in range(N)]+[(1<<i,1<<i) for i in range(N)]
common_cases=0;relative_cases=0
for s,v in omegas.items():
    for x,z in single:
        assert common(v,x,z)==omegas[s^synd(x,z)]
        common_cases+=1
        # Relative error flips only B's syndrome; exact recovery restores target.
        er=pauli(v,x,z,1)
        for j,(gx,gz) in enumerate(gens):
            sign=-1 if ((s^synd(x,z))>>j)&1 else 1
            assert pauli(er,gx,gz,1)=={i:sign*a for i,a in er.items()}
        recovered=pauli(er,x,z,1)
        # XZ convention may square to -I, physically irrelevant.
        phase=-1 if par(x&z) else 1
        assert recovered=={i:phase*a for i,a in v.items()}
        relative_cases+=1
# An uncorrected weight-one Z flips the logical paired X observable.
er=pauli(omega0,0,1,1)
assert common(er,ONES,0)=={i:-a for i,a in er.items()}
print(json.dumps({'code':'[[7,1,3]] Steane','signed_sectors':64,
 'raw_Bell_equals_uniform_coherent_gauge':True,
 'complete_local_projection_and_syndrome_checks':'exact',
 'common_single_Pauli_cases':common_cases,
 'relative_single_Pauli_recovery_cases':relative_cases,
 'separate_decoder_without_relative_recovery_counterexample':True},indent=2))
