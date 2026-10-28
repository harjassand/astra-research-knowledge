# Independent receiving of the local index27/4 and full condition-number24 theorem

27 October 2026. PASS for the theorem and quantitative bound in local_variance_index_27_over_4_root_theorem.md. The audit checks the abstract hypothesis replacement, singular receiving, original-source embedding, and whole spectral path, not only the scalar constant.

## 1. Same-pencil identities and the local hypothesis

The positive-part moment identities require positive U,V and Uψ=ψ, not a global upper bound on V. In the signed-kernel comparison the only former use of V≤I is the estimate <(I−V)²>≤1−y. The stated local premise <V²>≤y supplies exactly that estimate. It also implies0≤y≤1 by scalar Cauchy–Schwarz. The signs of k on the three intervals and the orientation of the tail inequality are correct.

Independent symbolic reconstruction gives a=23/4,b=23/13,ρ=23/54,z0=23/14 and the same partial fractions. The sum of their logarithmic coefficients is zero, so the endpoint at infinity cancels without a discarded constant. The exact bracket is

c=23/54+(529/5832)log(115893504/10604499373).

The original exact Taylor certificate was rerun and passes c>253/29160. An independently written rational-log receiver, local_index_twenty_seven_fourths_certificate.py, additionally proves c>1/64. Neither proof uses a floating-point sign premise.

## 2. Singular abstract extension is justified

The regularization Uε=(1−ε)U+εI, Vε=(1−ε)V+εI preserves Uεψ=ψ and the local cap:

yε−<Vε²>=(1−ε)²(y−<V²>)+ε(1−ε)(1−y)≥0.

A precise supported-log receiver is available. Because Uε is an effect with eigenvector ψ at eigenvalue one, Uε≥Pψ. Thus Bε≥Pψ/n and Cε≥(n+3)Pψ/(4n), with constants independent of ε. The rank-one Schur test then bounds <ψ,Bε^(-1)ψ>≤n and similarly for Cε. If μ is the ψ-spectral measure, its small-eigenvalue log tail satisfies, for0<δ<e^(-1),

∫_(0,δ)|logt| dμ(t)≤const·δ|logδ|.

Hence these tails vanish uniformly. Away from zero, norm convergence and continuous functional calculus apply. This supplies the claimed supported-log limit even though V need not be globally bounded by one. Finite dimension and bounded regularization ensure no upper-tail problem.

## 3. Original-source positivity and local cap

For n=27/4, δ0=1−n/9=1/4. The pure rank-one Schur test has the correct form Σr_i/[(n/3)r_i+δ0]≤1, by scalar concavity over at most three Schmidt weights. The operator nE(Pχ)−Pχ has at most one negative eigenvalue; effect duality therefore gives nE(A)−A≥−δ0I for every effect A, in every finite reference dimension.

Writing U=εI+(1−ε)A with ε≥1/24 gives nE(U)−U≥0 exactly at that threshold. No rank restriction or false global upper bound on V is used.

The nine qutrit Weyl terms are the actual conditional expectation. Since (I−U)ψ=0, one of the nine vectors in their average vanishes. Cauchy–Schwarz on the other eight gives the exact factor8/9. The bound ||I−U||≤23/24 then gives ||E(I−U)ψ||²≤(23/27)<E(I−U)>. With Vψ=ψ−(27/23)E(I−U)ψ this is precisely <V²>≤<V>. All constants and directions agree.

## 4. Actual entropy gradient and quantitative clipping

The identities B=E(U) and C=N²(U) are exact for the physical WH3 channel. Operator-log Jensen gives N(logN(U))≤logN²(U), so the actual entropy gradient is bounded below in the stated direction. Scale-linear trace constants cancel, and logU vanishes on the top vector.

For the clipping path, E is a self-adjoint orthogonal projection in Hilbert–Schmidt space. Therefore

Q′=2TrP_t(X_t−E(X_t))
  =2(m+t)[TrP_t−TrP_t E(X_t)/(m+t)].

The bracket is nonnegative since E(X_t)≤(m+t)I. Summing the received scalar score across a degenerate maximal eigenspace is legitimate. The condition-number floor is preserved as the top level decreases, and the path begins at a scalar white source with zero deficit and zero Q. Piecewise integration gives27c/(46M) times Q, hence the claimed11/(2160M) coefficient. If m,M are nonsharp external bounds, one may first use the actual extrema and then weaken the final denominator to M; this avoids describing a flat terminal clipping segment as having top norm m+t.

The quantitative coefficient is positive, so equality forces X=E(X); the converse follows because N fixes E's range.

## Received scope

PASS: every positive definite X on C3⊗C^d, finite d, with condition number at most24 satisfies the stated quantitative entropy comparison and equality classification. This is not an unrestricted/singular-source theorem. The old rank-six example remains a correct obstruction to a GLOBAL-effect embedding; it does not contradict this source-local variance construction. No hardware, decoder, or publication claim is acquired.
