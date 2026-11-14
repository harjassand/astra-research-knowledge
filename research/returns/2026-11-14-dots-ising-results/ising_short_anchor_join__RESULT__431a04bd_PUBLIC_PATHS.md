# Paid shorter-anchor to full-line transport join

Candidate restricted extension, submitted for independent review. This is not a general macroscopic-droplet theorem, and no novelty or advantage over direct mass has yet been established for its newly covered source subset.

## Exact source and two native stages
Retain original theta4,phi4/R,L8R, core A, soft clock kappa, voltage v, capacity C and majority target B. Let H_m contain non-target states with some horizontal or vertical consecutive PLUS segment of length m=ceil(9R/4). Fix one such anchor label (orientation and starting site, at most2n labels).

1. Starting from this actual anchor, fill the rectangle of width m and height L-1 immediately above it in a fixed row order, skipping initial plus spins. Stop at first actual B. If B has not been reached, the anchor and rectangle form m full plus columns.
2. Apply the previously reviewed fixed-full-column native growth order to the terminal configuration, again skipping existing plus sites and stopping at first actual B.

No equilibrium refresh is made at the join. Every flow weight starts from the ORIGINAL w(x), and both stages use physical upward single-spin edges. A full band is only a transport interface, not a new source/core/clock.

## Paid rectangle and terminal arrival density
Import bridge's open rectangular partition bound for bottom-plus/three-sides-minus boundary:

 Q_mh <= exp(mh exp(-8)) * m/(1-exp(-delta)) * P(exp(-8/R))^2 * coth(4)^(m-1),
 delta=8m/R-16>0, h=L-1.

Ferromagnetic ratio monotonicity lowers unknown exterior plus bits to minus. The top side actually identifies with the anchor, but treating its boundary incidences as minus is a valid ratio upper bound, not a physical change. Thus the full terminal fiber satisfies

 nu(y)=sum_{sources x ending at y} w(x) <= Q_mh w(y).

This is an UNNORMALIZED pushforward inequality for each exact terminal state, not a claim that arrivals are Gibbs. Restrictions excluding early-target sources only decrease the positive sum.

The existing partial-row comparison bounds stage1 pointwise positive congestion by2 exp(2phi m) Q_mh. Stage2 uses the fixed-column w-weighted flow and the domination nu<=Q_mh w, hence congestion at most2 Q_mh J_line. Here the safe existing one-line constant is

 J_line <=101n exp(16+(7/5)L+n/2397570000).

The exact conditional terminal distribution need not be sampled to establish this analytical domination; consequently this note does not claim a polynomial-time implementation of the arrival law.

## Composition without a hidden second entropy factor
For a fixed anchor, stage1 flips only sites within its width-m band. After stage1 that band is all plus, so stage2 never flips one of those sites. The two stages therefore use disjoint physical COORDINATES, not merely disjoint times. Their pointwise congestion bounds combine by maximum, not by product or by an unearned reset.

The displayed J_line upper bound also exceeds exp(2phi m) at the stated instances. Paying all2n anchor labels and n original coordinate-current cuts gives

 N_Hm <=4n^2 Q_mh J_line C.

One may choose a deterministic canonical anchor per source; positive overcounting all labels yields the same upper bound. The actual stopping target remains B throughout. This bounds an occupation numerator divided by ZA after importing C/ZA; it is not a complete mean estimator.

## Conservative exact finite receipt
Use exp8>2980, exp2>7, pi²<10, and
 log P(exp(-a)) <=pi²/(6a),
 log coth4 <=2/(exp8-1).
Since delta>=2,
 log Q_mh <=mh/2980+log m+1/6+5R/12+2m/2979.

check.py verifies all rational scalar decisions, including the logarithmic prefactor via positive Taylor certificates. At the existing capacity tuples:
- R80: N_Hm/ZA <=exp(-513).
- R200: <=exp(-1497).
- R1000: <=exp(-3760).
- R10000: the bound is vacuous; the loose rectangle pressure dominates.

## Limits and baseline gate
The source hypothesis is an ACTUAL solid segment; a large filled outer disk need not contain it because of shape or thermal holes. No such coverage implication is assumed. Existing full-line, dense4R-window, winding and Gibbs-mass results may already control important subsets of H_m. Before promoting this as substantive progress, identify a genuinely new high-mass source family or use the join as part of a broader paid source decomposition. Do not call a smaller geometric threshold alone a breakthrough.

## Critical-width solid specialization
The same proof works with m=2R+1. Now delta=8/R and its denominator is bounded by1+R/8, not by the earlier constant7/6. No hole-pattern factor is used. `solid_critical.py/json` pays the altered prefactor and gives exponents515,1521,4423 at R80,200,1000. Its R10000 bound remains vacuous. This is the solid event used in bridge's refined no-anchor complement, not the weaker earlier ceil(2.25R) threshold.
