# Independent audit: robust finite-policy certificate and infinite-fiber lift

Reviewer: finite_phase_drift_challenge, 2026-10-30. Internal mathematical review; no literature novelty certification. Reviewed ROBUST_PHASE_INFINITE_FIBER_LIFT.md.

## Verdict

The common-resolvent lemma, policy-independent offsets, eventual fixed policy, and forward-shift infinite-fiber lift pass. No switching, averaging, or common quadratic premise is hidden. The concrete application needs a nonneutral halo specified explicitly; an arbitrary tiny halo can be neutral. Choosing a consecutive corner J={0,...,K} with K≥3 suffices and removes that qualification for the intended hard-network use. Global matching, A/N→0, and outer-halo feedback remain open.

## 1. Finite-policy lemma

For a maximizing policy pi, G_pi v=-1. If one alternative row violates the desired inequality, the changed policy G' obeys 1+G'v=d e_i with d>0. Its resolvent vector satisfies

    w-v=(-G')^−1(1+G'v).

Hurwitz Metzler stability gives a nonnegative inverse with strictly positive diagonal, so w-v is nonnegative and has a strictly positive i coordinate. This contradicts maximality of the sum. Irreducibility is unnecessary. The conclusion extends to every rowwise convex combination because each row inequality is linear.

It is important that independent row replacement stays inside the family whose every policy is Hurwitz. Here each reaction coefficient affects only its source-phase row, so endpoint choices do have this rectangular property. Enlarging originally shared physical rate parameters to independent interval choices is safe: every enlarged endpoint still has the same positive weakly reversible reaction graph.

## 2. Policy-independent residual coordinate

The maximum degrees of the finite stationary-tree polynomials depend on available source orders and trees, not on their positive coefficients. Leading contributions are positive and cannot cancel. Fixed translations n=r−beta_j do not change these degrees. Therefore one beta vector and one set of integer residual increments work for all endpoint choices. Whether a projected component is neutral is also policy-independent.

The previously audited growing-tilt theorem applies separately to every finite endpoint policy with the SAME rational alpha<1/2. Its quadratic weights may depend on policy; no common quadratic form is needed. Taking the maximum of finitely many eventual thresholds establishes all endpoint Hurwitz assumptions simultaneously. The common-resolvent lemma then supplies the inequality for the entire interval family, without assuming interior-policy stability in advance.

## 3. One fixed maximizing policy eventually

All endpoint matrices are Laurent-polynomial in z=r^(1/q), with real or rational coefficients according to the rate endpoints. Their inverse vectors are rational in z and positive at all sufficiently large r. A difference of two objective sums is either identically zero or has only finitely many positive zeros and poles. Beyond all such exceptional points, the pairwise ordering is fixed. A single maximizer pi_* therefore works throughout the tail. Ties cause no difficulty.

Its positive rational entries have nonzero positive leading asymptotic terms. Hence v_j(r+delta)/v_j(r)=1+O(1/r) for each fixed shift. No discontinuous policy switching is hidden in the final V.

## 4. Forward shift and arbitrary state-dependent coefficients

At source residual r, a projected reaction has rate kappa_e(x,j)(r−beta_j)_(a_e) and target residual r+delta_e. The actual positive forward term differs from the inflated tilted term only by the Gamma ratio and v_k shift ratio. Their product is r^(alpha delta_e)(1+O(1/r)); fixed inflation 2^|delta_e| absorbs it eventually for every nonzero delta_e. For delta_e=0 the comparison is exact.

The coefficient is evaluated only at the SOURCE state and multiplies both sides. No derivative or fixed-shift comparison of kappa_e is required. Thus arbitrary hidden-state or time dependence within the fixed intervals is allowed for this local generator inequality. This is specifically a primal argument; an adjoint construction with arbitrary coefficient shifts would need different justification.

Transitions preserving both N and j contribute identically zero to the globally defined function V(N,j), even if they cross the boundary of the cone where coefficient comparability was checked. Target compositions need not satisfy the source cone condition. The local inequality requires that condition only at the source. No infinite-fiber mixing or spectral-gap assumption appears.

## 5. Concrete cone factorization

On A≥epsilon N with N=A+C and N sufficiently large, A/N lies in [epsilon,1], and

    (A)_3/(N)_3 lies in [epsilon³/8,1]

for example once epsilon N≥4. The factors B and (B)_4 are fixed positive coefficients on each relevant phase-specific reaction; channels with insufficient B are absent from the lifted graph. Immigration has coefficient one. All A/C redistribution channels preserve N and B exactly and can be omitted as null projected transitions.

The halo agreement is genuine on the chosen B-corner: every physical connector outgoing there is represented with its exact bounded-coordinate coefficient. The process may leave the cone or halo, but this does not invalidate the local generator calculation.

## 6. Neutral-halo qualification and clean application choice

An arbitrary finite halo need not have a nonzero residual increment. For J={B=0}, the connector halo phases {0,1,4} admit beta=(0,−1,−3) and all delta=0, so the Hurwitz part cannot be applied to it directly. The note's neutral-component exclusion is essential; its concrete application should not be read as bypassing it.

For the intended consecutive corner J={0,...,K}, K≥3, the halo contains translated connector cycles for z=0,1,2,3. If all residual increments were zero, their immigration edges would give beta_4=beta_0−4, whereas clearing in the z=0 cycle gives beta_4=beta_0−3. Contradiction. The projected halo graph is connected by overlapping complete cycles and hence strongly connected. This explicitly supplies a nonneutral component for the concrete robust construction, at any chosen fixed width K≥3.

Alternatively, a neutral component that exits J admits an analogous affine policy lemma: prescribe exterior value one and maximize the resolvent vectors (-Q_II,pi)^−1[1+Q_IO,pi 1]. The same row-improvement proof works for the affine residual Q_II v+Q_IO 1. This would require an explicit separate statement; the existing fixed-coefficient killed solve alone should not silently be treated as robust.

## Scope

The proof constructs a common pointwise generator certificate from finite positive endpoint policies, not from an assumed favorable composition law. It does not establish nonexplosion for arbitrary invisible dynamics, uniformity as coefficient lower bounds vanish, or any outer-region feedback contraction. In the mass-action application the fixed-N fibers are finite, but that fact alone does not close the remaining global matching problem.

Reviewed source hash:
e99ead0d10beba50ff18ef924f9f538df6f2764da7e61290fc9c0cd12d89ddfc  producer-workspace/ROBUST_PHASE_INFINITE_FIBER_LIFT.md
