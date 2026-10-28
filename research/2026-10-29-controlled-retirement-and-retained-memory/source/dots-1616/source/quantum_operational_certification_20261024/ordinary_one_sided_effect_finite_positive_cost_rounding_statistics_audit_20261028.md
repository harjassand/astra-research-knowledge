# Independent receiving: finite positive-cost one-sided effects

28 October 2026. Reviewer: `producer-workspace/audit_count_pilot_fresh`.

**PASS for known rational data and a supplied feasible covariance.** Reviewed source: `ordinary_one_sided_effect_finite_positive_cost_rounding_20261028.md`. Final SHA-256 `8b5859b44e398d5d97d5b14580041bd9232b9fe59188a9c090634d6a4dbab0b6`. The previous source `9351f94187591fd20efd680f2d7ab3957d719f3dbdbfad6249b0f3c4ab57b49f` differs only by the requested logarithmic shorthand cleanup; this exact reverse-edit hash was verified. No source experiment, source-dependent spectral basis or moving-effect decoder oracle is included.

## 1. Covariance relaxation and finite rational basis

The rational Hermitian coordinate basis has Gram entries 1 or 2; therefore its covariance moment maps are rational and `Tr Z<=Tr rho<=k`. Rank-one covariance from an actual effect A has rho=A^2<=I and `Tr WA^2<=Tr WA`, so it is a valid relaxation. Scaling Z by 1/2 leaves at least half the fractional objective and creates the rho<=I/2 slack needed below. All quantities and scale choices are known classical data. The finite optimization contract is the received bounded, known-interior SDP contract; the theorem rounds any supplied feasible Z rather than claiming an exact optimal SDP output.

The gap-free Jacobi step is valid. A largest off-diagonal entry has squared modulus at least E/k^2, and an exact two-coordinate diagonalization removes twice that amount from E. Comparing two unitary conjugations of a matrix of operator norm at most 1/2 gives energy perturbation no more than the source's safe 2k d_ctrl. The recurrence has stationary error eta^2/128. At the displayed cap, its decaying initial contribution is at most eta^2/128, already below the required eta^2/16 threshold.

A complex 2-by-2 diagonalizing unitary can have determinant adjusted to one without changing its conjugation result, then overall sign chosen to put its scalar quaternion coordinate in the nonnegative hemisphere. Stereographic coordinates have bounded norm, rational approximations map to exact rational unitaries, and no spectral gap is assumed. While a rotation is needed, the chosen off-diagonal entry is at least eta/(4k), bounding the conditioning of its elementary formulas. The number of rotations depends logarithmically on 1/eta; precision and product denominator lengths are polynomial in the rational input bits. No fine unitary net is enumerated.

For R=Q*rho Q, the off-diagonal norm is at most eta/4. Thus `D=diag(R)+(eta/2)I` gives

`rho+(eta/4)I <= QDQ* <=rho+(3eta/4)I`,

which proves the source's weaker sandwich and strict 0<D<I. This also shows why repeated eigenvalues cause no difficulty.

## 2. Tail, every cross-block and total cost

Base-four bands use rational square-root scales. Discarding only coordinates below delta gives

`E||G-PGP||_F^2 <= 2 Tr[(I-P)rho] <=2k delta`.

The numerator's Hilbert-space triangle bound yields s_keep>=s/4 with slack. Every diagonal and Hermitian cross-block is retained. Their K-component Cauchy bound is valid even when the components are correlated. This is not a replacement by independent diagonal/cube coordinates.

For each pair orient the smaller scale toward i. Both row and column Gaussian variances are bounded by their corresponding covariance bands. Summing small-side moments over all pairs assigned to i gives at most `P_i rho P_i`; hence the crucial total `sum_pairs t_ij<=q_bar` holds without another ell factor. Positivity of W is essential here.

The diagonal costs sum to at most `(4/3)m+4q_bar`; pair baseline costs to `(4/3)ell m`; large-side costs to `8ell q_bar`; small-side costs to `48q_bar`. These imply the stated `(8ell+56)(m+q_bar)` envelope. Moreover `q_bar<=q+eta Tr W<=q+m/8`. Combining the retained numerator, component count and total cost proves the exact component-ratio lower bound. Choosing the maximum rational s_j/b_j is finite; a positive s forces a positive retained component.

## 3. Gaussian event and actual positive effect

I independently read [Tropp's primary Theorem 4.1 and Corollary 4.2](https://tropp.caltech.edu/papers/Tro11-User-Friendly-preprint.pdf), printed pages 14–15. The Hermitian variance is the squared-coefficient sum; the rectangular variance is the maximum of row and column sums, with dimension-sum prefactor. Those are exactly the component variances used here. Together with the Gaussian quadratic second moment and cost Markov bound, the source's event intersection is at least 1/24, without an independence assumption between norm, cost and numerator.

The received finite Gaussian coupling loses at most 1/96. Its precision inequalities give the stated numerator/cost perturbation bounds. Sampling in the known rational block basis, or projecting a rational approximation onto its known support, keeps support exact without increasing Frobenius error. The result is a finite vector coupling, not continuous/discrete total variation. Small p,m,s_j affect bits, not the number of independent trials.

For a diagonal block, `A_±=(P_i±T_i)/2` are effects after the exact norm certificate. Parity retains one quarter of the T_i numerator, yielding `s_i/(128R0^2 b_i)` after scaling.

For a pair, the two polynomial completions are Hermitian and their `A-A^2` is block diagonal with blocks `BB* -4(BB*)^2` and `B*B-4(B*B)^2`. Thus the norm certificate guarantees both effect inequalities. For any PSD two-block W,A,

`Tr(WA)<=2[Tr(W_i A_ii)+Tr(W_j A_jj)]`.

This follows from positivity, Cauchy-Schwarz for the cross trace and `2sqrt(ab)<=a+b`. It pays the off-diagonal W contribution; it does not discard it. The returned cost is consequently bounded by twice b_ij/p_j. The odd numerator after scaling is at least `s_ij/(128R0^2 p_j)`, giving the stated `1/(256R0^2)` component ratio. Unequal actual costs of the two signs cause no problem because both obey the same upper envelope and both actual ratios are evaluated.

Combining the covariance factor 2, selection factor `8K(8ell+56)` and rounding factor `256R0^2` gives exactly

`F_Z/[4096R0^2 K(8ell+56)]`.

Repeated trials fail with probability at most beta. Every returned effect is feasible even off the favorable event. The finite formula governs small k and small scale ratios; asymptotic logarithmic shorthand is read with the usual additive 1 (equivalently log(2ak/m)). This notation does not change the finite guarantee.

## 4. Affine numerator and scope

For affine N(A), let b=||c||^2/m. The homogeneous candidate with ratio h satisfies `h<=2N(A)/u(A)+2b`, so the larger actual affine ratio at A or zero is at least h/4. Conversely every target affine ratio is at most `2b+2h_opt`. A homogeneous kappa-approximation therefore gives the displayed factor `2+8kappa`. No favorable offset or sign is presumed.

The input-dependent factor is genuinely polynomial-logarithmic in the supplied rational precision parameters; it is not a reciprocal-cost sampling budget. If F_Z>=1, then s>=m/2 after scaling, so the number of retained bands is bounded by a constant plus log(ak/m). Without that design-level restriction, the algorithm is still finite polynomial in the full input bit length, including log(1/s), but the shortened m-only logarithm is not asserted.

This supplies the canonical one-sided-effect branch. Combining it with the fixed-slice odd construction is not yet a finite global full-CPTP decoder oracle: the arbitrary polar/square-root interface and optimization of the actual moving effect remain unpaid. No acquisition exponent, source saving or conventional-learner separation is received.

## 5. Independent evidence

`fixed_effect_and_one_sided_rounding_statistics_check_20261028.py/.json` independently verifies two rational Jacobi runs (one repeated-eigenvalue input), exact unitarity and energy/sandwich certificates, all six components of a three-band rational covariance, 90 two-sign completion cases (180 actual PSD effects) and their ratios, and 72 cases with a nonzero cross-block W contribution. It also includes 18 extreme-scale precision inequalities, 100 rational Gaussian-tail constants and the companion full-CPTP checks. Computation is exact rational/complex algebra except for selecting a high-precision proposed 2-by-2 rotation; all its returned rational certificates are checked exactly. No RNG, source calls, sampled Gaussian success-frequency test, SDP execution or hardware claim occurs.

The accepted finite-coupling receipt's manifest was reverified. No unresolved load-bearing objection remains at this known-matrix, finite-output scope.
