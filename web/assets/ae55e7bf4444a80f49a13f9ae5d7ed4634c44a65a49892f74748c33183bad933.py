#!/usr/bin/env python3
"""Exhaustive finite test of v2's scheduling/charging lemma only.

Random fixed local binary correction subspaces on overlapping syndrome
patches; neither GGJ geometry nor global expansion is assumed or tested.
"""
import json
import random
from pathlib import Path


def xor_span(gens):
    values=[0]
    for x in gens: values += [y^x for y in values]
    return sorted(set(values))


def test_system(rng,n=12,vertices=9):
    patches=[]; candidates=[]
    for _ in range(vertices):
        bits=rng.sample(range(n),rng.randrange(2,6))
        patch=sum(1<<b for b in bits)
        gens=[rng.getrandbits(n)&patch for _ in range(rng.randrange(1,4))]
        patches.append(patch); candidates.append(xor_span(gens))
    colors=[]
    for v,p in enumerate(patches):
        used={colors[u] for u in range(v) if p&patches[u]}
        color=0
        while color in used: color+=1
        colors.append(color)
    incidence=max(sum((p>>b)&1 for p in patches) for b in range(n))
    footprint=max(p.bit_count() for p in patches)
    constant=1+2*incidence*footprint

    def gain(v,s):
        choices=[(s.bit_count()-(s^c).bit_count(),c) for c in candidates[v]]
        g,c=max(choices,key=lambda x:(x[0],-x[1]))
        return (g,c if g else 0)

    for s0 in range(1<<n):
        initial=sum(gain(v,s0)[0] for v in range(vertices))
        s=s0; recorded=0
        for color in range(max(colors)+1):
            flip=0
            for v in range(vertices):
                if colors[v]==color:
                    g,c=gain(v,s); recorded+=g; flip^=c
            old=s.bit_count(); s^=flip
            assert s.bit_count()<=old
        decrease=s0.bit_count()-s.bit_count()
        assert recorded==decrease
        assert initial<=constant*decrease
    return {'syndromes':1<<n,'vertices':vertices,'colors':max(colors)+1,
            'max_patch':footprint,'max_incidence':incidence,'charge_constant':constant}


def main():
    rng=random.Random(20261009)
    systems=[test_system(rng) for _ in range(16)]
    out={'status':'PASS','scope':'fixed-color integer-gain charging only',
         'seed':20261009,'systems':16,
         'exhaustive_syndrome_cases':sum(x['syndromes'] for x in systems),
         'global_expansion_or_full_decoder_validated':False,'details':systems}
    print(json.dumps(out,indent=2))
    Path(__file__).with_name('finite_charging_v1.json').write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__': main()
