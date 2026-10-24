# Adversarial check: block canonical observables, §§1–5

2026-10-24. Bounded derivation review of
../fermion/BLOCK_CANONICAL_OBSERVABLES.md §§1–5. This checks the inequalities
and their hypotheses, not the separately repaired interleaved shuffle
implementation. Graded signs are retained in every exact local activity;
absolute-value bounds below are applied only after that signed activity is
formed.

## Complex block norm, parity gain, and local activity

Given the asserted negative-root theorem and B_B(0)=1, write

    B_B(z) = product[j=1..d_B] (1 + z/beta_j),   beta_j > 0.

For z = rho exp(i theta), |theta| <= 2pi/3, and u = rho/beta_j,

    |1 + u exp(i theta)|^2 - (1+u)^2/4
      = 3(1+u^2)/4 + (2 cos(theta)-1/2)u >= 0.

At the worst angle 2pi/3, the right side is 3(u-1)^2/4. Multiplying over
roots proves (3), including degree zero. The factor 2^(-d_B) is tight when
every u=1 at the sector boundary.

The parity argument is genuinely local and survives a strongly resonating
reference. Each native block tensor is even. A nonzero bra/ket matrix element
therefore has an even total number of incident cross-edge creators or
annihilators on each active block, counted across both copies. An active block
needs at least two incidences; each selected edge factor contributes two
block incidences. Thus a component on s active blocks needs at least s
selected bra/ket edge factors. This does not claim either copy separately has
even incidence, and does not discard the sign of an interleaved fermionic
contraction. It only lower-bounds the number of weak factors after the exact
signed local term is assembled.

The real-radius estimate behind (5) is consistent with nonuniform internal
blocks: use the Hilbert norm ||Omega_B(rho)|| = sqrt(B_B(rho)), the operator
bound ||C_e^dagger|| <= 2, and 2 sqrt(R) lambda <= v. For an s-block
support, there are at most b Delta s/2 physical cross edges; their bra/ket
inclusion patterns are at most 2^(b Delta s). Each contributing term has at
least s selected factors, so v <= 1 allows v^s to be pulled out. In the
complex sector, division by actual analytic block denominators costs at most
2^(sum[d_B]) <= 2^(d_max s) by (3). Thus the stated h^s envelope follows with
the larger K=2^(d_max+2). The extra margin is harmless. I find no
counterexample from unequal block polynomials or large internal pairing
amplitudes, provided the exact block norm and negative-root premise hold.

One important scope distinction: (5) is a sector bound and must not be used
through a negative-axis zero of a block polynomial. The outer-arc proof does
not do that. It bounds every active component by its norm at the positive
radius B_B(rho), and leaves inactive factors as
u_B(theta)=|B_B(rho exp(i theta))|/B_B(rho). This avoids division by complex
block values, even when one is zero.

## Heterogeneous outer arc

For each block, negative-root factorization gives a Poisson-binomial
characteristic function. If p_Bj=rho/(rho+beta_Bj), then

    u_B(theta) <= exp[-2 V_B(rho) sin^2(theta/2)],
    V_B(rho) = sum[j] p_Bj(1-p_Bj) <= d_B/4.

The last inequality gives exp(2 V_B) <= exp(d_B/2) <= 3^d_max. Applying the
stated forest injection to absolute component activities bounded by h^|C|,
with inactive block weights u_B, yields the product in (8); component
activities need not be positive. Then

    product[B] (u_B + y)
      <= exp[-2 V_0(rho) sin^2(theta/2) + y 3^d_max M],
    y = (D+1)h.

For |theta| >= pi/2, 2 sin^2(theta/2) >= 1. Divide by the positive-real KP
lower bound Z(rho) >= Z_0(rho) exp(-M S). The exponent is at most

    -V_0(rho) + M[S+(D+1)h 3^d_max]
      <= -nu M/2 + nu M/16
      = -7 nu M/16,

throughout the factor-two tilt window. This is stronger than the claimed
-nu M/4. The proof is heterogeneous: it uses only sum[B] V_B >= nu M/2 and
the uniform degree bound. Negative-real reference zeros cause no singularity.

## Tilt bracket and strongly resonating example

For one root factor, V_Bj(rho)=rho beta/(rho+beta)^2, and

    V_Bj(2 rho)/V_Bj(rho)
      = 2(rho+beta)^2/(2 rho+beta)^2, which lies in [1/2, 2].

The same termwise bounds hold for sums, even when block roots and block
variances are very nonuniform. Therefore (7) implies V_0(rho) >= nu M/2 on
[r_0/2, 2r_0]. Since d mu_0/d log(rho)=V_0, endpoint mean displacement is at
least (log 2)nu M/2 - 1/64 >= nu M/4 - 1/64. Cauchy gives
|Q'| <= M S/s_0 <= nu M/128, so the full mean still brackets k for
sufficiently large M; the finite small range needs the stated exact
enumeration fallback. Also |Q''| <= 2 M S/s_0^2 <= nu M/8 for s_0=1/8, so
the full variance stays positive in the bracket, at least 3 nu M/8, under
these same tests.

The four-site example is an exact sanity check. Its polynomial
1+8z+4z^2 has roots -1 ± sqrt(3)/2, hence positive Bernoulli parameters
beta=1 ∓ sqrt(3)/2. At z=1/2 the tilted charge law is (1/6, 2/3, 1/6),
with mean 1 and variance 1/3. Repeating this non-product block M times gives
reference variance M/3 at target k=M, so any fixed nu<1/3 passes the
variance gate. An independent-dimer approximation is unnecessary.

## Bounded finding

I found no algebraic counterexample to (3)–(8) for nonuniform bounded blocks.
The safeguards are: use the negative-root theorem only for native block
references; keep exact graded signs in local activities; apply the h^|C|
envelope to their absolute values; and normalize outer inactive blocks at
positive real fugacity rather than dividing by B_B(z) on the outer arc. The
tilt margin is termwise stable under factor-two rescaling. The claims remain
conditional on the reconstructed negative-root theorem, the all-context
parity/local-norm derivation, KP tests (4)–(6), and exact finite-block
enumeration. This note does not audit the marked-observable extension in §6
or the known code-shuffle repair.
