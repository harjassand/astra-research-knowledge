# Paid static hull ambiguity using existing magnetic moments

Status: a reusable STATIC envelope conditional on the same filled-domain/magnetic-walk injection used in the recovered global cut certificate. It is not a killed-duration congestion theorem. It avoids assuming arbitrary plus shapes are four Ferrers corners.

Fix a contractibly embedded filled domain D whose bounding rectangle has site widths W,H<=400. Put s=W+H, A=WH, P0=2s. The weight relative to the full rectangle is

 exp[-8(P(D)-P0)-.04(A-|D|)].

For every r in the existing moment tables, 1<=r<exp(.02). Let Z_P(r) bound the sum of r^(twice signed area) over all rooted nonbacktracking closed square words of length P (all four initial directions). The inherited contour injection, with P root choices, gives the fixed-bbox-anchor envelope

 K(W,H) <= sum_(even P>=P0) exp[16s-8P-2log(r)A] Z_P(r)/P.

Proof of the area replacement: exp(.04 |D|) = r^(2|D|) exp[(.04-2log r)|D|] <= r^(2|D|) exp[(.04-2log r)A]. Division by the rectangle's exp(.04A) leaves r^(-2A). Each valid compact boundary has P distinct rooted word encodings: a proper rotational period would have zero displacement and repeat an edge. Translation to its unique bbox anchor removes the global n factor. No arbitrary translation is free in a path-injection application; this is a FIXED rectangle bound only.

For each P take the minimum of the already certified moment envelopes for r=201/200,101/100,51/50,765151/750000 and the trivial r=1 count Z_P(1)<=4*3^(P-1). The latter includes all nonbacktracking words, even nonclosed ones. All moments through P1900 are retained. For P>1900 use the complete geometric tail with ratio3exp(-8), ignoring1/P and including odd perimeters harmlessly.

At fixed s, every term decreases with A. The minimum allowed A among W,H in[1,400] is s-1 for s<=401 and400(s-400) otherwise. Hence799 semiperimeter evaluations cover all160,000 rectangle dimensions; no aspect assumption is made.

## Executed numerical envelope
`hull_entropy_bound.py/json` uses directed Decimal conversion/log/exp enclosures and the saved upward moment tables. Runtime19.99 seconds. It finds

 log K(W,H) <=877.768274128277

uniformly. The worst envelope occurs at W400,H3 (s403,A1200). This is loose: it is not a claim the actual shape ambiguity is that large. The constant is too large for the previous log-duration budget~189, but could fit a stronger core-exit budget near1000 if every remaining reconstruction factor is paid.

## Internal holes: separate full-configuration factor
For spins inside a fixed filled outer domain D, with its outer boundary held plus, the relative weight of any internal minus pattern compared with all-plus D is

 exp[-8 P_internal -.04 N_minus].

Resolve every physical boundary pinch by a fixed deterministic convention. The internal boundary is an unordered collection of canonically rooted oriented square walks, each length>=4. All roots lie on at most401^2 vertices; at most4^P walk words per root suffice. Distinct boundary collections determine the spin pattern with the fixed outside plus phase, including nested plus islands. Discard compatibility and the nonnegative field cost. The exponential-gas bound is

 sum_internal_patterns weight <= exp[401^2 sum_(P>=4)(4exp(-8))^P] < exp(6e-7).

This factor must not be confused with a proof that an arbitrary augmented component has one raw outer walk: the outer-domain interface must be specified first. Nor does it encode ORIGINAL THERMAL COMPANIONS that the clearing algorithm has erased outside D.

## Missing path interface
To turn this into killed-duration congestion, an edge must recover the active rectangle, its stage, and the unchanged exterior, with a bounded number of rectangle/stage records. The original active hull and internal holes can then be weighted by the bounds above. Previously erased components must be encoded as a compatible Gibbs gas relative to the current exterior, not counted as2^n histories or silently discarded. Mergers and any active hull with a side>400 need a separate rule: this lemma does not cover them. Until this injection exists, no rho or native duration bound is established.
