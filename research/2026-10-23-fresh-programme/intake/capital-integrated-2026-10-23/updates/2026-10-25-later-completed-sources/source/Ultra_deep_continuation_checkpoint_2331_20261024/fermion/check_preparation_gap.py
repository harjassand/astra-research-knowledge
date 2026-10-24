#!/usr/bin/env python3
"""Finite complex hard-qutrit diagnostic of the local parent-gap lemma.

The three-site vacuum-reference triangle tests nonnormal-filter/kernel algebra.
It is not the large four-site-block preparation protocol, a gap proof, or a
physical execution. All reported eigenvalues are floating-point diagnostics.
"""
import sys
sys.dont_write_bytecode = True
from fractions import Fraction
from itertools import product, combinations
from pathlib import Path
import json
import numpy as np
from check_canonical_contraction import bond_create


def main():
    n=3
    masks=[sum((1 << (2*i+v-1)) if v else 0 for i,v in enumerate(o))
           for o in product((0,1,2),repeat=n)]
    index={mask:i for i,mask in enumerate(masks)}
    identity=np.eye(len(masks),dtype=complex)
    edges=[(0,1),(1,2),(0,2)]
    creators=[]
    for edge in edges:
        c=np.zeros_like(identity)
        for j,mask in enumerate(masks):
            for result,value in bond_create({mask:Fraction(1)},edge).items():
                if result in index:
                    c[index[result],j]=complex(value)
        assert np.max(np.abs(c@c))==0
        creators.append(c)
    for c,d in combinations(creators,2):
        assert np.max(np.abs(c@d-d@c))==0

    projectors=[np.diag([float(bool((mask>>(2*b))&3)) for mask in masks])
                .astype(complex) for b in range(n)]
    lam=1/1000
    coeff=[lam,1j*lam,-lam]
    e=2*lam; ell=2; degree=2
    delta=(1+e)**(4*ell)-1
    bound=1-delta*(1+3*degree*degree)
    results=[]
    for s in (.37,1.):
        factors=[identity+s*z*c for z,c in zip(coeff,creators)]
        inverses=[identity-s*z*c for z,c in zip(coeff,creators)]
        global_g=identity.copy()
        for factor in factors:
            global_g=global_g@factor
        terms=[]
        for b in range(n):
            local_g=identity.copy(); local_inverse=identity.copy()
            for j,edge in enumerate(edges):
                if b in edge:
                    local_g=local_g@factors[j]
                    local_inverse=local_inverse@inverses[j]
            a=local_g@projectors[b]@local_inverse
            assert np.linalg.norm(a@global_g-global_g@projectors[b],ord=2)<1e-12
            terms.append(a.conj().T@a)
        pair_nullities=[]
        for b,c in combinations(range(n),2):
            pair=terms[b]+terms[c]
            eigenvalues=np.linalg.eigvalsh(pair)
            original=np.linalg.eigvalsh(projectors[b]+projectors[c])
            nullity=int(np.count_nonzero(eigenvalues<1e-10))
            assert nullity==np.count_nonzero(original<1e-10)
            assert min(eigenvalues[eigenvalues>1e-10])>=1-2*delta-1e-12
            anti=(terms[b]@terms[c]+terms[c]@terms[b]
                  +3*delta*(terms[b]+terms[c]))
            assert np.linalg.eigvalsh(anti)[0]>-1e-12
            pair_nullities.append(nullity)
        h=sum(terms)
        spectrum=np.linalg.eigvalsh(h)
        assert sum(spectrum<1e-10)==1
        assert spectrum[1]>=bound-1e-12
        assert np.linalg.eigvalsh(h@h-bound*h)[0]>-1e-12
        results.append({"s":s,"pair_nullities":pair_nullities,
                        "floating_actual_gap":float(spectrum[1]),
                        "floating_max_local_delta":float(max(
                            np.linalg.norm(terms[b]-projectors[b],ord=2)
                            for b in range(n)))})

    # Exact integer tests of the separate four-site-family scalar example.
    assert 56*1001**16 <=57*1000**16
    assert 24**16<13**16*2**15
    output={"status":"PASS",
            "scope":"finite complex 3-site hard-qutrit parent lemma and exact scalar inequalities only; no large or physical preparation",
            "dimension":len(masks),"floating_certificate_delta":delta,
            "floating_certified_gap":bound,"path_checks":results,
            "four_site_family_exact_gap_inequality":True,
            "four_site_family_exact_secant_inequality":True}
    path=Path(__file__).with_name("PREPARATION_GAP_CHECK.json")
    path.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))


if __name__=="__main__":
    main()
