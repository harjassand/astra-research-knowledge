# Rounded fixed-step solver: no growing coefficient denominators

Root author addendum to BOUNDED_PROJECTION_ACQUISITION.md, pending independent review.

All means are exact rationals in[-1,1]. At dictionary size m>=1 use B=m, alpha as in the main construction, delta=B²alpha, and Gbar=Ghat+m alpha I. Check Gbar PSD by an exact rational procedure; otherwise latch failure. Its entries have absolute value<=2. The target linear term is Khat*d with ||d||_1<=B, or a prefix cross vector with entry bounds1. Constant target terms do not enter optimization.

Let q(c)=c*Gbar c-2c*k on ||c||_1<=B. Then ||gradient q(c)||_infty<=6B. A safe Frank-Wolfe curvature bound is C=16mB²: along any feasible segment q(c+theta(s-c))<=q(c)-theta gap+(C/2)theta². Set theta=delta/C<1.

Choose a fixed dyadic h=2^-p satisfying

 h<=delta²/(24 C B m).

Start EACH solve at c=0. At each iteration find the exact signed l1-ball vertex s minimizing the empirical gradient. Compute the exact FW gap. If gap<=delta, return c and that certificate. Otherwise compute z=(1-theta)c+theta s, then round EACH coordinate of z toward zero to a multiple of h, giving the next c.

Rounding preserves ||c||_1<=B. It changes l1 distance by at most m h, so it can increase q by at most6Bmh<=delta²/(4C). Before rounding, gap>delta guarantees decrease at least delta²/(2C). Thus a nonterminal rounded step decreases q by at least delta²/(4C).

A safe full-domain objective range is R=8mB². Consequently

 N=1+ceil(4 C R/delta²)

is a deterministic sufficient iteration cap whenever the PSD guard passes, even on a statistical bad event. Exceeding the cap latches failure. No limiting iteration or uncharged exact optimizer is assumed. The same exact FW gap certifies objective suboptimality<=delta by convexity; no rounding allowance needs adding to the final returned objective-gap certificate.

Every retained iterate has coordinates in h*Z and absolute values<=B. Its bit height is therefore O(log B+log(1/h)), NOT linear in N. Each temporary exact update uses only the fixed rational theta and a grid point, and is immediately rounded. Mean denominators, input tolerance bit height, and exact rational gradient arithmetic are all charged; their sizes are polynomial in log m, log(1/lambda), and the encoded confidence/tolerance parameters. The target coefficient vector is also on a fixed grid for that solve epoch. There is no iterated chain of uncontrolled rational denominators.

With alpha proportional to lambda/m³, the conservative N is O(m^8 lambda^-2). Each iteration uses O(m²) rational arithmetic operations of the bounded bit height above, so an explicit elementary solver has lambda^-2 accuracy dependence up to logarithmic bit factors, with a larger polynomial in m. This is digital work as well as source sampling; it is not a statement of a useful numerical constant or laboratory runtime. A stronger established convex solver may improve the m dependence and is a legitimate comparator/component.

Worst-event requirements remain: fixed finite word horizon/alphabet, cache by precision epoch, refuse duplicate retained descriptors regardless of estimated leverage, and permanently latch a rejected task that cannot supply a fresh admissible witness. These ensure that acquisition stages are bounded by the finite descriptor universe even on bad data. Future accepted-query evaluation work is charged separately and may grow with the number of requested tasks.

The complete explicit unconditional expectation envelope and integration with the source job scheduler are delegated for independent verification. No code execution or historical novelty is asserted by this author note.
