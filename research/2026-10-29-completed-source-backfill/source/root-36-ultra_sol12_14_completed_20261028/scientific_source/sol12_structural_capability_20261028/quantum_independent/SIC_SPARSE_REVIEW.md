# Independent review: Bell/SIC reduction and support-five receiver

Status: **ACCEPTED, including the quantitative1/128 bound.** I whole-read
the producer's current `../quantum_composition/SIC_SPARSE_PROOF.md`, its
literal channel replay, its certifier, and the primary entropy-envelope
theorem cited below. This is a substantive mathematical review; the
saved arithmetic consumer imports none of the producer's functions.

## Exact channel and probability conventions

The labels p are Bell eigenvalues and SIC **preparation weights**, not
SIC measurement probabilities. In the declared permutation
`|u,d> -> |u+d,u+2d>`, applying W3 on the first qutrit to each Bell
projector gives `I3/3 tensor S_ab`, with
`s_ab=(|a+1>-omega^(-b)|a+2>)/sqrt2`. Thus
`S(Nrho)=log3+S(Mp)`, `S(rho)=H(p)` and `Erho=I9/9`.
The exact defect is `Delta=2S(Mp)-H(p)` and
`Tr Mp^2=(1+3sum p_i^2)/4`. Our alternative field representation
Q[sqrt(-3)] checks all729 component equalities,81 pair overlaps,
idempotence, and the tight-frame identity exactly.

## Equally informed sharp entropy/purity comparator

Harremoes--Topsoe2001 Theorem2.5(16),(17), together with their
information-diagram boundary description, supplies the sharp maximum
entropy of a five-vector at purity s and the sharp minimum entropy of
a three-vector at purity q. The upper extremizer is
`(z,(1-z)/4,...,(1-z)/4)`,
`z=(1+sqrt[4(5s-1)])/5`. The lower qutrit extremizer is
`(a,a,1-2a)` up to q1/2, and binary above q1/2. Padding supports smaller
than5 is allowed. Both extremal entropy curves decrease with purity,
which justifies using the opposite endpoints of each interval.

This primary theorem was read in the author-uploaded full text at
https://www.researchgate.net/publication/3080552_Inequalities_between_entropy_and_index_of_coincidence_derived_from_information_diagrams .
It is credited prior, not a new extremizer theorem here. The original
author PDF endpoint timed out; this review does not claim those PDF bytes
were acquired. The numerical purity diagnostic alone would not suffice.

## Independent full cover and analytic tail

Our `replay_reviews.py` re-evaluates **every one of the39 saved cells**
using80-bit directed rational square roots and24 atanh terms, instead of
the producer's60 bits/16 terms. It checks contiguity from1/5 to63/64 and
independently proves that every saved lower bound is valid and is at
least `(1-lo)/128`. Because s>=lo this pays `(1-s)/128` throughout the
whole cell, not only at sampled endpoints. The arithmetic trust boundary
is elementary integer isqrt, Fraction operations and a geometric positive
series tail; no approximate entropy or eigenvalue is a proof premise.

For the missing tail put u=1-s<=1/64 and eta=1-z. Then
`u=2eta-5eta^2/4`, `eta<=256u/507`, and the output binary small eigenvalue
nu satisfies `3u/8<=nu<=3u/4`. The monotonicity of x log(1/x) on this
range and the elementary logarithm bounds in the source yield

    Delta >= [11/3-(85/12)(256/507)]u
           = (137/1521)u >= u/128.

I checked the constants and the direction of every bound. At u0 the
source is a point mass with zero defect. This proves
`Delta >=(1-sum p_i^2)/128` for every at-most-five mixture, with equality
only at a point mass. The argument uses only output dimension3 and
pairwise pure overlaps squared1/4, so the same result holds for any such
equiangular subset; Hesse phases are not required.

The same scalar relaxation fails already at support6. That is a
relaxation failure, not an entropy counterexample. `ALL_NINE_PROOF.md`
now supplies a different full-frame majorization proof for all9 labels,
with equality at point masses and the full uniform vector. The sparse
1/128 stability bound remains separately useful and does not extend in
that form to all9 (the uniform vector has zero defect).

The joint exact source/cell/old-bath replay took about0.19s. The producer's
39-cell acquisition was separately paid at about0.063s. This review
does not establish historical priority, unrestricted WH3/CLR, or a
physical implementation.
