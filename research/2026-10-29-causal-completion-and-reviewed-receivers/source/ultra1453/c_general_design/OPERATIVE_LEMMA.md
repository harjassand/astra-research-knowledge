# One-sided Schur lift: keep every unknown denominator out

30 October 2026. Developing, not yet a completed general SDP theorem.

Let positive classical L have arbitrary rectangular shape, Q_i>=0 sum I,
and let T span the input zero-sum tangent. Put A_L=L T, A_K=K T,
W_y^A=sum_i A_yi Q_i. The universal free inequality is equivalent to

    R_L(K,c;Q) = [ c A_L^T diag(W^L)^-1 A_L   A_K^T ] >=0,
                 [ A_K                       diag(W^K)]

for every Q and reference dimension. This Schur lift is AFFINE in both
unknown K and unknown c. Crucially, every inverse is a fixed L denominator;
there is no inverse containing K. Thus a rational-positivity certificate
space can be fixed BEFORE optimizing K,c. This is stronger than observing
pointwise matrix-fractional convexity alone.

Rank deficiency has an exact linear gate: ker(L T) must be killed by K T.
Impose those equations and reduce T to an active complement; then the
nominal top block is positive definite, uniformly over Q. A constant
release is a strictly positive matrix-pencil baseline when c>0. No inverse
of L or state-dependent quotient is assumed.

Strong ordinary import already found and directly read: Volcic,
Hilbert's17th problem in free skew fields, arXiv2101.02314v2, Section4's
complexity tau and Theorem5.2/Section5.5. It gives an EXPLICIT truncated
rational quadratic module, not a hierarchy without a cutoff. Scalarizing
the matrix pencil with extra free Hermitian Y variables has tau<=4, hence
the published cutoff is9. The proposed common basis must handle all
coefficient choices, rational identities and domain/rank issues; those
are being derived, not waved away by citing the theorem. Its broad finite
reduction may already subsume the operation. No novelty or practical
efficiency claim follows from the reference alone.

The substantive question is now whether this yields a fully constructive
joint synthesis programme for ALL positive L, with a paid finite basis
and an actually executed genuinely rectangular/rank-deficient instance.
Polynomial conic description size, weak-SDP precision complexity, exact
decision, numerical acquisition and useful cost must remain distinct.
