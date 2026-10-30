# Independent adversarial audit: genuinely leaky strip resolvent

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review, not novelty certification.

## Verdict

The local theorem passes this audit under its explicit finite lifted-graph leakage hypothesis and positive differentiable forcing assumption. No positivity-of-polynomial-coefficients shortcut is needed. The source/target orientation, generalized-monomial derivative bounds, normalized eigenvalue/determinant step, inverse path formula, and final exact adjoint estimate all check. Global feedback and parameter compatibility remain unproved, as stated.

## 1. Lifted coercivity and normalization

With p=1/alpha, z_(r,a)=f_r^p a_a gives

    z_(r,a)^(1−alpha) z_(s,b)^alpha
      =f_r^(p−1) f_s a_a^(1−alpha) a_b^alpha.

Thus summing the killed-complex functional is exactly sum_r f_r^(p−1)(M f)_r, including same-phase reactions. Every lifted vertex has an outgoing edge because it can reach killing, so the finite source out-degree coefficients yield cW≤D≤CW. Choosing epsilon after the coercivity constant yields

    sum f_r^(p−1)(Bf)_r≤−gamma sum D_r f_r^p

with a uniform gamma>0. Setting omitted coordinates to zero preserves this for principal restrictions; p>1 makes the zero-coordinate factors harmless.

For C_I=D_I^−1 B_I, the inequality is weighted ell-p dissipativity with weights D_I, exactly as claimed. An especially short rigorous spectral proof uses the nonnegative Perron eigenvector for the spectral abscissa of the finite Metzler matrix C_I, including reducible cases: substituting it into the inequality gives s(C_I)≤−gamma. Hence every eigenvalue has real part≤−gamma. The real determinant det(−C_I) is positive (real eigenvalues contribute positively and nonreal pairs contribute positive modulus squares), and its absolute value is at least gamma^|I|. Multiplying by det D_I yields the displayed determinant lower bound. This does not assume a phase stationary distribution.

## 2. Signed diagonals and determinant derivatives

For u_i above twice the largest relevant factorial offset,

    |partial_i log (u)_a|=sum_(ell=0)^(a_i−1)1/(u_i−ell)≤C/u_i.

Positive sums of fixed powers of these factorials inherit the same bound. Write T for all positive internal entries, including same-phase positive diagonal terms. Then B=T−(1−epsilon)D and

    d_r=−B_rr=(1−epsilon)D_r−T_rr.

Testing coercivity on a coordinate vector gives d_r≥gamma D_r. Also T_rr≥0 gives d_r≤D_r, and T_rr≤D_r. Differentiating this signed expression is therefore safe: |partial_i d_r|≤C(D_r+T_rr)/u_i≤C'd_r/u_i. No assertion that d_r is a positive-coefficient generalized polynomial is required.

Let N=diag(d)^−1 B_off. Since −B is a nonsingular M-matrix, rho(N)<1. Every directed cycle product of N is at most rho(N)^length<1. Each determinant permutation decomposes into disjoint cycles and fixed points, so its absolute weight is bounded by product d_r≤product D_r. Differentiation costs only a finite factor C/u_i per nonzero term, using the diagonal and off-diagonal bounds above. The determinant lower bound then controls its logarithmic derivative despite cancellation in its signed expansion. The same argument applies to every principal minor. Identically zero off-diagonal entries cause no difficulty.

## 3. Positive simple-path formula and forcing

The inverse orientation is correct: (−B)^−1_rs sums simple directed paths r→s, with product of B off-diagonal entries and the principal minor on the complement of all path vertices. The zero-length path for r=s gives the corresponding principal cofactor. Empty minors equal one. All summands are nonnegative and every nonzero principal minor is positive. The logarithmic derivative of each summand is O(1/u_i), hence the derivative of each positive inverse entry is bounded relative to itself. Structural zeros are identically zero throughout the high-count orthant.

For an everywhere-positive C1 forcing F obeying the stated relative derivative bound, v_r=sum_s(−B)^−1_sr F_s is positive because the diagonal inverse entry is positive. Its logarithmic derivative has the same bound. Integrating on a fixed-width neighborhood of u proves v_r(u−nu)/v_r(u)=1+O(1/min u) for every fixed reaction shift. Integrating along coordinate paths from a fixed interior anchor gives polynomial upper and lower bounds. Constants may depend on the fixed lifted graph and forcing derivative bound, not on u. There is no claim of uniformity for growing phase sets.

## 4. Exact incoming bound and adjoint closure within the block

The equation B^T v=−F gives the exact useful identity

    T^T v=(1−epsilon)Dv−F≤Dv,
    M^T v=−F−epsilon Dv.

Here T contains every positive ideal incoming contribution, including same-phase transitions, and the componentwise Dv means D_r v_r. Thus the factorial-ratio and v-shift errors, each relative O(1/min u) on individual incoming edges, sum to at most C D_r v_r/min u. Taking the count threshold large enough absorbs half the epsilon margin and yields precisely the displayed restricted adjoint inequality.

This statement concerns target states sufficiently far inside the high-count orthant that every incoming predecessor is also in the region where v is defined. Any arbitrary finite-width extension affects only another strip. Killing is an outgoing loss; prescribed external arrivals are added separately. If their normalized forcing admits the stated positive derivative-controlled majorant F, the negative −F term absorbs them. A fixed bulk fractional-factorial value shifted by finitely many reactions does produce such factorial-ratio expressions at high counts, and adding a positive constant handles zero forcing components. This does not establish that arrivals from subsequently modified neighboring strata retain compatible bounds.

Polynomial growth of v, combined with the positive fractional factorial exponent, ensures summability and polynomial-rate integrability. Neither fact controls flux sent back out of the solved strip.

## Unresolved obligations retained

- Every lifted complex must reach killing, not merely every frozen phase.
- The solved strip can overwhelm the bulk through reverse feedback.
- Selecting alpha from the strip after selecting its width from the bulk can be circular.
- Further small-coordinate strata require compatible joint choices, not just formal recursion.

Accordingly this is a valid local elimination result with supplied external forcing, not a global positive-recurrence certificate.

Reviewed source SHA-256: `45739dc21b3820d92a8608831ff8dbb5cb24a70e0c970c78cb4ca5800061d477`.
