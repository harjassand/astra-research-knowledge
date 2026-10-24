#!/usr/bin/env python3
"""Exact finite marked-mode/number-PGF checks, not a bath experiment.

Cross-checks the normal-order expansion against full second quantization and
tests projection covariance with genuinely complex passive memory vectors.
"""
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial
from pathlib import Path
import json

from check_gaussian_envelope import G, eye, zeros, add, scale, mul, adj, trace


def inner(v,w):
    return sum((x.conj()*y for x,y in zip(v,w)),G())


def matvec(a,v):
    return [sum((x*y for x,y in zip(row,v)),G()) for row in a]


def permanent(a):
    n=len(a)
    if not n:
        return G.of(1)
    total=G()
    for mask in range(1,1<<n):
        value=G.of(1)
        for row in a:
            value *= sum((x for j,x in enumerate(row) if mask>>j&1),G())
        total += value*((-1)**(n-mask.bit_count()))
    return total


def repeated(a,occupations):
    indices=[j for j,n in enumerate(occupations) for _ in range(n)]
    return [[a[i][j] for j in indices] for i in indices]


def pgf_coefficients(p,occupations,n0,d):
    coeff=[Q(0) for _ in range(sum(occupations)+1)]
    for m in product(*(range(n+1) for n in occupations)):
        per=permanent(repeated(p,m))
        assert per.im==0 and per.re>=0
        weight=Q(1)
        for n,mj in zip(occupations,m):
            weight *= Q(comb(n,mj),factorial(mj))
        coeff[sum(m)] += weight*per.re
    for k,c in enumerate(coeff):
        assert c<=comb(d+k-1,k)*n0**k
    assert coeff[0]==1
    for t in (Q(1,8),Q(1,4)):
        # Exact full diagonal of Gamma(I+tP), independently of the normal
        # ordered coefficient sum. This equals <n|exp(beta N_P)|n>.
        b=add(eye(len(p)),scale(p,t))
        direct=permanent(repeated(b,occupations))
        direct /= G.of(__import__('math').prod(factorial(n) for n in occupations))
        expansion=sum((c*t**k for k,c in enumerate(coeff)),Q(0))
        assert direct==G.of(expansion)
        assert expansion<=(1-n0*t)**(-d)
    return [str(c) for c in coeff]


def main():
    count=4
    zeta=G(Q(0),Q(3,5))
    vectors=[]
    v=[G.of(1)]+[G() for _ in range(count-1)]
    for t in range(count):
        vectors.append(v)
        if t<count-1:
            v=[zeta.conj()*x for x in v]
            v[t+1] += G(Q(4,5))
    for t,v in enumerate(vectors):
        assert inner(v,v)==G.of(1)
        for s in range(t+1):
            expected=G.of(1)
            for _ in range(t-s):
                expected *= zeta
            assert inner(v,vectors[s])==expected

    marked=(1,3)
    columns=[vectors[t] for t in marked]
    gram=[[inner(v,w) for w in columns] for v in columns]
    det=gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]
    inverse=[[gram[1][1]/det,-gram[0][1]/det],
             [-gram[1][0]/det,gram[0][0]/det]]
    vmat=[[columns[j][i] for j in range(len(columns))] for i in range(count)]
    p=mul(mul(vmat,inverse),adj(vmat))
    assert p==adj(p) and mul(p,p)==p and trace(p)==G.of(2)
    kernel_checks=0
    for t in marked:
        assert matvec(p,vectors[t])==vectors[t]
        for s in range(count):
            assert inner(matvec(p,vectors[t]),matvec(p,vectors[s]))==inner(vectors[t],vectors[s])
            kernel_checks+=1
    # The analogous preservation statement for an unmarked first leg is
    # intentionally NOT required and is false on this fixture.
    assert inner(matvec(p,vectors[0]),matvec(p,vectors[0])) != inner(vectors[0],vectors[0])
    commutator=inner(vectors[1],vectors[0])-inner(vectors[0],vectors[1])
    assert commutator==G(Q(0),Q(6,5))

    fixtures=[]
    for n in ((1,1,1,1),(2,1,0,2),(2,2,2,2)):
        coeff=pgf_coefficients(p,n,max(n),2)
        fixtures.append({'input_occupations':n,'normal_order_coefficients':coeff,
                         'direct_second_quantization_agrees':True,
                         'thermal_coefficients_dominate':True})
    # Exact forbidden-class counterexample: the per-input cutoff and zero
    # field after a global +/- mixture do not bound bright-mode occupation.
    coherent_bins=8
    bright_population=Q(coherent_bins+1,4)
    assert bright_population>1
    q=Q(7,8)
    c=1/((1-(q**-2-1))*(1-q)**2)
    assert c==Q(1568,17) and c<=32*4
    output={
        'scope':'exact Gaussian-rational finite mode compression, normal-order photon PGF and marked covariance; not a full continuum bath or device simulation',
        'finite_input_modes':count,
        'rotation_attenuation':{'re':'0','im':'3/5','fresh_mode_amplitude':'4/5'},
        'marked_contacts':marked,
        'compressed_rank':2,
        'marked_first_leg_covariance_equalities':kernel_checks,
        'unmarked_first_leg_equality_false_as_expected':True,
        'noncommuting_force_commutator':{'re':str(commutator.re),'im':str(commutator.im)},
        'photon_moment_fixtures':fixtures,
        'coherent_cap_counterexample':{'bins':coherent_bins,'cap':1,
            'rank_one_bright_population':str(bright_population),
            'claimed_thermal_mean_if_contract_misused':1},
        'n0_one_q_7_over_8_comparison_constant':str(c),
        'status':'PASS'
    }
    Path(__file__).with_suffix('.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='photon_moment_fixtures'},indent=2))


if __name__=='__main__':
    main()
