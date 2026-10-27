# Exact source-native logdet interface for a possible peak2 receiver

27 October2026. Root-proposed route, independently derived here. The reduction is exact; the pointwise determinant and inverse-trace inequalities remain UNPROVED.

Let N=W3⊗id, τ=EX, D=X−τ, and0≤X≤2τ. Work on the actual product support so τ>0. For s>0 put

R_s=(τ+sI)^(-1/2), A_s=R_s D R_s.

Because τ is reference-only, E(A_s)=0, N(A_s)=R_s N(D)R_s, and

−I<A_s<I.

Indeed −τ≤D≤τ and R_sτR_s=τ(τ+sI)^(-1)<I. These are actual physical-qutrit matrices, not free input/output spectra.

## Exact Bregman logdet integral

For any faithful X and τ, the ordinary trace-entropy Bregman divergence is

TrXlogX−Trτlogτ−Tr[(logτ+I)(X−τ)]
=∫_0^∞ {Tr[(τ+sI)^(-1)(X−τ)]−logdet(X+sI)+logdet(τ+sI)}ds.

One verification differentiates in X: the resolvent difference integrates to logX−logτ, and the expression vanishes at X=τ. In our source the linear term is zero for every s, since E(D)=0 and(τ+sI)^(-1) is reference-only. Also TrD=TrDlogτ=0. Therefore

D(X||τ)=−∫_0^∞ logdet(I+A_s)ds.

Applying the same identity to NX, which has the same marginal, gives the exact original deficit

Δ(X)=∫_0^∞ {2logdet(I+N(A_s))−logdet(I+A_s)}ds.    (1)

No entropy is whitened. The reference congruences occur inside the determinant identity at each actual resolvent parameter, where they are exact.

For singular X or NX, regularize or pass directly at s>0. Near s=0 the finite-dimensional logdet singularity is at worst O(|log s|), which is integrable. At infinity the first-order terms vanish and the integrand is O(s^(-2)). Thus(1) has the same finite entropy-continuous limit and requires no arbitrary log value on a kernel.

## Unproved pointwise target

It would suffice to show, for every actual physical-qutrit Hermitian A with EA=0 and||A||<1,

F(A):=2logdet(I+N A)−logdet(I+A)≥0.

Since NA=−T_A A/2, this is equivalently

det(I−T_A A/2)^2≥det(I+A).

Both heads are positive in the strict norm ball by positivity and unitality of N. This pointwise statement is stronger than the desired integrated entropy conclusion; no inference from numerical tests to its truth is made.

## Stronger rational sufficient target

For the same actual A, define

R(A)=Tr(I+A)^(-1)−2Tr(I+NA)^(-1)+3d.

Along a radial path,

dF(rA)/dr=R(rA)/r, r>0,

because TrA=TrNA=0 and B(I+rB)^(-1)=[I−(I+rB)^(-1)]/r. Therefore R≥0 throughout the actual norm ball would imply F≥0 by integrating from r=0. This inverse-trace inequality is also unproved.

Diagnostic searches and exact family checks are recorded in relative_peak_two_logdet_search_status.md. Ordinary convexity and strict operator-norm contraction have explicit counterexamples there; neither may be assumed in proving the targets.
