"""Finite arithmetic check: bounded spin energies with exactly dyadic coins.
Pseudorandom runs test the implementation. Mathematical exactness assumes fair
independent input bits, as for ordinary randomized algorithms.
"""
from fractions import Fraction
from pathlib import Path
import random,json
D=16
MASK=(1<<D)-1
K=20000

def energies(z):
    rotated=((z<<1)&MASK)|(z>>(D-1))
    walls=(z^rotated).bit_count()
    first=(z&255).bit_count()
    return walls//4+first//4,(D-walls)//4+(8-first)//4

hist={}
for z in range(1<<D):
    pair=energies(z)
    hist[pair]=hist.get(pair,0)+1
R=max(max(pair) for pair in hist)
S=1<<R
na=sum(n*(S>>ka) for (ka,kb),n in hist.items())
nb=sum(n*(S>>kb) for (ka,kb),n in hist.items())
ni=sum(n*(S>>max(ka,kb)) for (ka,kb),n in hist.items())
den=(1<<D)*S
sa,sb,I=Fraction(na,den),Fraction(nb,den),Fraction(ni,den)
sg=(sa+3*sb)/4
p=3*sb/(sa+3*sb)
assert I<=sg
rng=random.Random(20261105)

def coin(exponent):
    return exponent==0 or rng.getrandbits(exponent)==0

proposals=0
accepted=0
sum_b=0
while accepted<K:
    source_a=rng.getrandbits(2)!=0
    while True:
        z=rng.getrandbits(D)
        proposals+=1
        ka,kb=energies(z)
        if coin(ka if source_a else kb):
            break
    exponent=max(0,kb-ka) if source_a else max(0,ka-kb)
    if coin(exponent):
        accepted+=1
        sum_b+=int(source_a)
result={'dimension':D,'enumerated_states':1<<D,'maximum_energy_units':R,
        'sample_count':K,'s_A_exact':str(sa),'s_B_exact':str(sb),
        'overlap_exact':str(I),'p_B_exact':str(p),
        'race_theory_proposals':float(1/I),
        'race_observed_proposals':proposals/K,'race_p_hat':sum_b/K}
proposals=0
accepted=0
sum_b=0
while accepted<K:
    is_b=rng.getrandbits(2)!=0
    z=rng.getrandbits(D)
    proposals+=1
    ka,kb=energies(z)
    if coin(kb if is_b else ka):
        accepted+=1
        sum_b+=int(is_b)
result.update({'direct_theory_proposals':float(1/sg),
               'direct_observed_proposals':proposals/K,
               'direct_p_hat':sum_b/K})
(Path(__file__).parent/'finite_spin_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
