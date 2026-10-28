# Odd history closure and the earlier signed filter

Let G_alpha=iS_alpha, so -h=sum_alpha G_alpha tensor G_alpha. Expand the
physical twisted n-cycle exponential in ordered bond events. Each event
inserts the same G_alpha at its two incident sites, with a proper rotation
at the closing leg. The absolute expansion is bounded by5^n exp(12 beta n),
so it may be regrouped by bond histories. At each site the resulting trace
is exactly the chronologically merged history kernel k_beta(x,y).

The product of these site traces is a cycle of n kernels. Its rotated
closing leg is the history U_g insertion. The Hilbert--Schmidt product trace
formula therefore gives

    Tr_history(K_beta^n U_g)=Tr_physical exp[-beta H_n(g)], n>=3.

No evenness entered. The spatial enumeration may be reversed to match index
conventions; this does not reverse the chronological operator words. Even
if words are transposed, each site gets(-1)^(its event count) because G^T=-G;
their product is(-1)^(twice the total event count)=1. There is no(-1)^n
factor and no time-reflection insertion.

For n2 the same construction means TWO PARALLEL physical bonds, one rotated.
It is not a single ordinary open pair. No assertion is made at n1. Since K
is Hilbert--Schmidt, K^n is trace class for every integer n>=2, and all odd
eigenvalue moments converge absolutely with their actual signs. The source
original proof explicitly notes that odd moments are useful for polynomial
estimates; evenness is needed for probabilities and purity, not this closure.

A5 character projectors remain linear at odd orders. The earlier p3/p5
values were therefore actual signed J=K/5 moments. The NEW literal physical
constructor independently reproduces the beta3 scaled triplet-list values

    M3/theta^3=-1.09136916937258,
    M5/theta^5=-.864361165066879.

Those negative signs were retained in the old Hankel matrix. Its failure was
not caused by absolute odd moments, a ferromagnetic cycle, a missing
reflection, or a cycle-parity error. `results/odd_moment_audit.json` records
the numerical check, including an independent analytic125-state triangle
spectrum. The closure conclusion follows from the derivation, not that
finite control. No new filter search was repeated in the audit.

The later TWO-atom test in `code/two_atom_moment_preview.py` is distinct:
for A=-J and its signed moment Hankel M, two eigenvalue occurrences x,y
require M-x^2v(x)v(x)^T-y^2v(y)v(y)^T>=0, v(x)=(1,x,x^2). With the new
projected Rayleigh lower, numerical feasibility gives a second-positive
edge around259608. It is not a certified global upper or physical input.
