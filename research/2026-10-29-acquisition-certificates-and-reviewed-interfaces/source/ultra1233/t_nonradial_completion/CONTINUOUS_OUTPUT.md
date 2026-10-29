# Positive continuous output: pay clipping exactly where it can occur

The exact finite-cell operation does not projectively refine to a full point;
REFINEMENT_BARRIER.md preserves that failure. A different positive consumer
does give ONE continuous normalized velocity law within an explicitly paid
total-variation error, uniformly in time. It is not exact f_t output and not
a claim about unvalidated floating or finite-bit errors.

## 1. General envelope operation

Suppose a probability density f is known to have a bounded unbiased query
H(v), E H(v)=[f(v)-M(v)]/W(v), |H(v)|<=L, with W integrable. Both M,W are
known and sampleable after normalization. Set G=M+L W, Z=int G=1+L int W.
Draw v with density G/Z, query H AT THIS SAME v and accept with probability

    max{0, [M(v)+W(v)H(v)]/G(v)}.                       (C1)

The upper bound1 is deterministic. Define the nonnegative clipping bias

    b(v)=E[-M(v)-W(v)H(v)]_+.

The accepted velocity has normalized continuous density

    g(v)=[f(v)+b(v)]/[1+B], B=int b,
    0<=b(v)<=[L W(v)-M(v)]_+.                          (C2)

Indeed max(x,0)=x+(-x)_+; conditional expectation proves the UNNORMALIZED
density f+b. Thus

    TV(g,f)<=B/(1+B)<=d/(1+d),
    d=int[L W-M]_+,                                   (C3)

and expected proposals are Z/(1+B)<=Z. This charges normalization, rather
than passing an unnormalized clipped estimator to the output. Correlation
between a proposal's cost and its acceptance causes no extra assumption:
independence of complete attempts gives mean total work=mean attempt work
divided by acceptance probability. A uniform query-cost bound therefore
gives total mean<=Z times that bound. No unknown f_t floor is used.

This is an ordinary clipping/rejection operation. The consequential interface
is that the constructed HARD-SPHERE query supplies it with a time-uniform
mark bound, and the near-equilibrium Gaussian envelopes make d fourth order,
not merely proportional to the source deviation. Generic signed sampling or
an unacquired pointwise density estimate would not supply this fact.

The same generic positive clipped-mean consumer is already constructed in
root_complex_collision/PROOF.md Section5 for its DIFFERENT Maxwell/rotation
input. It is credited, not reintroduced as a new positivity principle. Here
there is no Gaussian-mixture/Wild closure. The new hard-sphere row/query and
the explicit support of possible negative estimates supply the missing native
input; the one-query tail calculation avoids that earlier general1/epsilon^2
mean-estimation cost in this admitted small-deviation class.

## 2. Closed Gaussian tail bound, no tolerance oracle

For W=M^beta, beta=3/4, let L<M0^(1-beta), M0=(2pi)^(-3/2), and

    R^2=2 log[M0^(1-beta)/L]/(1-beta),
    T(x)=sqrt(2/pi) x exp(-x^2/2)+erfc(x/sqrt2).

The positive part is supported exactly on |v|>R. Therefore

    d(L)=L Z_beta T(sqrt(beta)R)-T(R).                 (C4)

Both terms are known initial Gaussian tail integrals. Their small difference
is evaluated outward; no finite plot or cancellation in binary64 is a proof.
Mills' expansion gives, as L tends to0 at fixed beta=3/4,

    d(L)~(4pi/3) R L^4.                               (C5)

Only(C4), not this asymptotic, is used for the actual error receipt. The
fourth-order suppression follows from the changed Gaussian density power;
it does not assert an exact fourth-order kinetic perturbation closure.

## 3. Actual nonradial input and full-cycle operation

Use H_t from NONRADIAL_PROOF, W=M^(3/4), L=D_eff=1/8000. Propose from the
known mixture proportional to M+L M^beta. Each component is an ordinary
3-normal with variance1 or1/beta, and its exact mixture probability is known.
Query at that actual full vector and apply(C1). All failed proposals and
all query kernel/factory work are charged. Ideal-real accepted velocities
are iid from ONE continuous normalized g_t; hence every measurable detector
is a pushforward of this same law, with the SAME TV error bound.

The sharper pointwise mark is |H_t(v)|<=D phi(|v|). On |v|<=5,
M(v)^(1-beta)>D_eff, while phi=1 outside5. Clipping can therefore occur only
in the far tail, where the mark bound is D=1/10000. Consequently(C4) with
L=D bounds the ACTUAL clipping bias, even though the simple proposal uses
the slightly larger D_eff. STATIC_CERTIFICATE.json retains both conservative
and sharper bounds as exact rational Arb endpoints. The theorem gives a
declared tolerance1e-12 with substantial slack, uniformly in all finite t.

The expected ideal-real query tree has<=400 nodes, and expected proposals
are<=1+D_eff Z_beta<1.001. The certified envelope/factory constants pay a
large finite primitive-work upper bound. They are independent of t, but not
claimed practical or optimal. This removes the radial symmetry and fixed
detector prerequisites simultaneously, at an EXPLICIT approximation target.
It does not solve exact full-law sampling or literal fair-bit acquisition.

## 4. Equal-information ordinary comparison

The ordinary normalized finite-time hard-sphere lineage operation receives
the SAME source sampler, exact moments and collision kernel; it gives exact
ideal-real f_t and therefore also meets the1e-12 target. Its full recursion
cost is retained, including failed final rejections and tilted source draws.
The underlying published Fournier recursion is the strong general weighted
incumbent; nonlinear LVDSMC and conservative Fourier/spectral solvers remain
strong approximate alternatives. No lower bound on THEIR best possible
same-input cost follows from one lineage comparison or this receiver.

All incumbents also receive the newly proved bound
TV(f_t,M)<=D_eff Z_beta exp(-nu0 t/400)/2. It qualifies cheap direct Gaussian
output once it reaches the requested tolerance. At initial time the exact
anisotropy-cell discrepancy is>8e-6, so substituting M does not automatically
meet1e-12 merely because the source is close. At intermediate times the
displayed bound must actually pay the requested tolerance; unqualified true
closeness cannot be substituted for it. A validated deterministic transient
solver may be stronger in practice; no absence or superiority is asserted.

Binary64 execution is a finite diagnostic of the implementation and cost,
not a claim that its numerical law is within1e-12. That contract belongs to
the proved IDEAL-REAL consumer until an interval/fair-bit evaluator is supplied.
Neither supplied source formulas nor ideal randomness establish physical
gas qualification. Historical priority of this specific hard-sphere operation
is UNKNOWN; clipping, rejection, weighted analysis and branching are prior.
