# Actual SSF tests of the barrier candidate

2026-10-29. These are finite structural diagnostics, NOT certified expander-family tests or memory-threshold evidence.

## Exhaustive degree-2 control

`test_ssf_animals.py` imports the exact atomic SSF rule from `online_ssf_stress_20261029/stress.py`, including the beta=1/2 decrease criterion and candidate support restriction. On the L=3 cycle-HGP code it enumerates all 256 syndromes, all 397 connected syndrome-check animals, and 81 parameter/cutoff choices. Every nontrapped syndrome had negative aggregate clean SSF drift for the softened-animal observable. This does not establish uniform constants or exclude bad traps. It also computes the exact local decoded-current boundary: some malignant single-qubit edges have a source representative of weight one, because distance is only three.

## Degree-3 actual SSF: exact per-move counterexample

`test_degree3_ssf.py` uses the explicit 5x5 binary matrix

    1 1 0 1 0
    0 1 1 0 1
    1 0 1 1 0
    0 1 0 1 1
    1 0 1 0 1

and its N=50 hypergraph-product code. Each classical degree is three. Stabilizer commutation is checked. SSF candidates obey 2|sigma(F)|>=3|F| and beta=1/2; each hub chooses maximum decrease with fixed tie breaking, exactly as the existing stress convention.

For error bit mask 8796109800448 (weight three), syndrome mask 19158272, hub 16 selects flip mask 8796095119360. The syndrome XOR is 3408128, and syndrome weight drops 7 to 5.

Nonetheless the softened connected-syndrome-animal observable with exp(a)=2, theta=1/32 and cutoff ell=4 rises EXACTLY from

    221205760 / 1048576

to

    248380608 / 1048576.

There are 3175 connected syndrome animals through size four. The exact numerator difference is 27174848>0; see `exact_nonmonotone_move.json`. Thus ordinary syndrome-count descent cannot be substituted for monotone barrier descent, even for a low-weight initial error and a valid non-degree-2 SSF move.

This is NOT a counterexample to an averaged generator-drift inequality: in 500 sampled states all aggregate clean drifts were nonpositive (trapped states attained zero). Nor are the strong expansion constants of the theorem certified for this tiny circulant graph. The proposed SSF Lyapunov inequality remains open rather than disproved.

## Resolvent alternative and its exact obstruction

One can define a clean potential on a finite transient basin by integrating a target observable until absorption, obtaining L0 V=-W (up to an absorbing baseline/boundary term) exactly. This fixes per-move nonmonotonicity. But global SSF has traps, so a global inverse need not exist; restricting to the small-error basin introduces boundary terms. More importantly, an inverse alone does not bound orbitwise oscillation under one local change: two initial syndromes may follow different cascades. A coupling/locality bound for that potential is still needed. It would be circular to assume it from finite total work.

The finite-rate stabilizer-dephasing construction avoids this particular obstruction for offdiagonal sectors: its local-source inverse is proved directly in `FINITE_DEPHASING_RESOLVENT.md` without any SSF absorption/mixing assumption. That is the current more concrete mechanism.
