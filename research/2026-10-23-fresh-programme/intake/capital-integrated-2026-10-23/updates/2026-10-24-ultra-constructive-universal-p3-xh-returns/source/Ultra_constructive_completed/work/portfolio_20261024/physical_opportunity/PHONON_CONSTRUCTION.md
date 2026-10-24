# Alternative owned construction: mass-constrained phonon spectrum design

## Question
Can a passive mass-and-spring material create a broad thermal stop spectrum without paying the inert mass/longitudinal stiffness penalty of an ordinary heavy chain? The consequential limitation is the coupling of thermal insulation to density and stiffness, including a possible thermoelectric backbone. No electronic performance is assumed or acquired.

## Exact representation
A 1D periodic mechanical cell has positive masses, internal passive springs and one backbone mass connected to adjacent cells by spring K. In mass-normalized coordinates,
D(q)=D0+s(q) v v^T, s(q)=4K sin²(q/2),
where D0 is PSD, has a rigid-translation zero mode z, and v is the backbone coordinate divided by sqrt(m_backbone). For one connected cell,
|z^T v|²=1/M_total.
The internal springs, all masses, all optical bands and the longitudinal K are charged. A strongest simple comparator rigidly binds the same total mass M_total to each backbone site and keeps K identical.

Because a rank-one positive update interlaces eigenvalues, each pass band is [sqrt(lambda_j(D0)),sqrt(lambda_j(D0+4Kvv^T))], with disjoint interiors. In the classical ballistic limit the conductance is proportional to their total width
W=Tr sqrt(D0+4Kvv^T)-Tr sqrt(D0).

## First derived theorem candidate
For every such finite passive cell,
W >= 2 sqrt(K/M_total).
The rigidly bound mass comparator approaches equality as internal spring frequencies tend to infinity. Thus counting the acoustic stop band alone can manufacture a high-temperature win: the optical branches pay it back.

Sketch: for t>0, the compliance resolvent q(t)=v^T(D0+tI)^-1 v >= |z^T v|²/t. Rank-one determinant lemma plus the scalar trace-square-root integral gives
W=(1/(2 pi)) integral_0^infty t^-1/2 log(1+4K q(t)) dt
>= (1/(2 pi)) integral t^-1/2 log(1+4K/(M_total t)) dt
=2 sqrt(K/M_total).
I will reconstruct constants and proof, test non-star passive cells and the exact finite-temperature Planck-weighted transport where bandwidth can be usefully moved above the thermal window.

## Positive construction direction
At finite temperature, a resonator can narrow the acoustic band below the rigid-mass cutoff while moving its compensating optical width above k_B T/hbar. A useful result must optimize the full Bose-weighted conductance rather than simply claim a band gap. The desired enabling framework is a sharp mass-constrained attainable thermal-spectrum body plus an actual passive cell realizing the useful edge, with strong global comparators and explicit stiffness/frequency resources.

For one backbone m and side mass M joined by spring k, the squared eigenfrequencies at s are roots of
m M lambda²-[M s+k(m+M)]lambda+s k=0.
For m=M=K=1, k=4, acoustic band is [0,1.236...], optical band [2.828...,3.236...]; total width1.644... exceeds the rigid-mass width sqrt(2), but optical transport can be thermally suppressed. This is not yet a demonstrated global finite-T advantage or novel physical operation.

Current status: owned mathematical model and theorem candidate, no physical specimen; nearest prior art and decisive finite-T/global optimization pending.

