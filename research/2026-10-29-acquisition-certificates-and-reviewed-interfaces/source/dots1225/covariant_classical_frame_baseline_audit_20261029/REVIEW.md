# Independent review: covariant classical frame baseline

2026-10-29. Reviewer `producer-workspace/review_history_program_bounds`.

**ACCEPT the frozen governing theorem and finite-interface addendum, at their stated single-use averaged-channel/IID scope.** The MSE proof, bi-covariance, half-diamond conversion, finite positive quadrature, bounded-random-bit approximate twirl, additive precision budget, and ordinary-source-call cap are sound. The numerical scalar proxies are not certified diamond norms of the finite Monte Carlo channels.

An independent tightening gives `halfdiamond <= 704/(9 m g_L^2) = 3520/(N g_L^2)`, where `N=45m`; the submitted weaker constant432 remains valid. This refinement is proved separately in `TIGHTER_CONSTANT.md`, without changing the author's immutable source.

## 1. Estimation and the bad event

The specified minus record is the real symmetric density matrix `sigma_R=alpha I-g cc^T`, with `c=vec(R)/sqrt(3)`, `g=(1-eta)/(8+eta)>0`. Its minimum eigenspace is the ray of c and its eigengap is exactly g. No knowledge of eta is needed by the eigenvector estimator; a valid lower bound g_L is needed for its resource guarantee.

Each diagonal projector outcome is Bernoulli. Measuring `|i><j|+|j><i|` and halving its outcome gives an unbiased estimate of the real entry sigma_ij, with outcomes `-1/2,0,1/2`. Thus every scalar estimate has variance at most1/(4m). There are nine diagonal and36 off-diagonal settings, while the latter appear twice in the squared Frobenius norm. The resulting `81/(4m)` bound and `45m` record count are correct.

Write `E=||sigmahat-sigma||op`. The perturbed minimum eigenvalue is at most `alpha-g+E`. Projecting its eigenvalue equation onto c-perp gives `sin(theta)<=E/(g-E)`. On `E<=g/4`, the ground eigenvalue is simple and this is at most1/3. The sign-aligned scaled vector is within `sqrt(6)sin(theta)<1` in reshaped Frobenius distance of R. Since R has smallest singular value1, its determinant cannot change sign inside this operator-norm ball. The determinant sign rule therefore selects the correct projective sign. Nearest-SO3 projection doubles the distance at most, yielding precisely `(128/3)E^2/g^2` for squared rotation error.

Any two SO3 rotations have squared Frobenius distance at most8. Markov's bound on `Pr(E>g/4)` then gives the submitted `3456/(m g^2)` unconditional MSE bound. The argument does not assume that a typical eigenvector perturbation guarantee holds on every sample.

For an explicit computable tie convention, one may return I when the minimum eigenvalue is repeated or the reshaped eigenvector is singular; otherwise choose its positive-determinant sign and use the unique polar factor. Both exceptional cases are outside the good event. At fixed m the count matrices are rational and there are finitely many possible count tuples. Eigenvectors, determinant tests and polar factors can be specified by real-algebraic operations, then approximated with certification. Thus a measurable but noncomputable tie convention is not needed. This is a finite computability statement, not an efficient native implementation or an endorsement of uncertified floating eigensolver output.

## 2. Covariance and the genuinely matched metric

The known nine-dimensional label action maps `sigma_R` to `sigma_(A R B^T)`. It acts on acquired label registers, not by querying or inverting an unknown physical gate. For independent Haar A,B, the estimator returns S and the implemented Bloch rotation is `A^T S B`.

For `R'=L R H^T`, set `C=A L`, `D=B H`. Haar invariance leaves the joint law of C,D unchanged, and the corrected output is `L[C^T S D]H^T`. Therefore `M(L R H^T)=L M(R)H^T`. At I the stabilizer L=H forces `M(I)=kappa I`, and hence `M(R)=kappa R`. Each branch implements a known unitary, so the average is unital; there is no unexamined affine translation term.

For each rotation estimate, squared Frobenius error is `6-2 Tr(R^T Rhat)`. Averaging gives `MSE=6(1-kappa)`. Complete positivity of the averaged qubit channel places kappa in `[-1/3,1]`. Its Pauli weights are `(1+3kappa)/4` for identity and `(1-kappa)/4` for each other Pauli. The triangle upper bound on half-diamond distance is the total nonidentity weight; a maximally entangled input gives the same Bell-diagonal trace-distance lower bound. Consequently

`halfdiamond = 3(1-kappa)/4 = MSE/8 <= 432/(m g_L^2)`.

This is a **single averaged channel**, including averaging the estimator and controller randomization outcomes, with calibration independent of the payload/reference input. It is not a per-estimate diamond guarantee, an outcome-resolved instrument guarantee, or a guarantee for inputs chosen adaptively from the calibration transcript. Reusing a single estimate coherently across many gates also needs a separate correlated-error analysis. Those distinctions match the stated scope rather than invalidate it.

The Monte Carlo file reports `MSE/8` only as a scalar proxy for the exactly twirled channel and separately reports finite-sample anisotropy. That qualification is correct and load-bearing. A coherent rotation by0.1 radians already supplies a counterexample: its `MSE/8` is about.002498, while its half-diamond error is about.049979. No finite-Monte-Carlo diamond certification is inferred from the proxy.

## 3. Exact finite positive quadrature

The nonlinear eigenvector/polar postprocessing does not make the overall quantum operation nonlinear in its input density matrix. For fixed m there is a finite measurement-outcome set, a fixed map from each outcome string to a known output gate, and therefore a fixed CPTP record-to-gate processor. The estimator's coefficients do not depend on A,B.

Each conjugated record density contributes degree at most2 separately in A and B. Its N-fold joint outcome probabilities have degree at most2N per factor; the Bloch corrective rotation contributes at most1 further degree per factor. Thus each averaged channel coefficient has separate degree at most2N+1. This concerns the unconditioned apparatus, not a normalized postselected outcome whose probability denominator could destroy polynomiality.

A product of at most L spin-one matrix entries decomposes into integer-spin matrix coefficients with spin at most L. For `2L+1` equally spaced alpha and gamma values, every nonzero magnetic frequency in that range sums to zero. The only survivors are `d^ell_(0,0)(beta)=P_ell(cos beta)`. `L+1` Gauss-Legendre nodes integrate these polynomials exactly, with strictly positive weights. Only the surviving zero-frequency Wigner terms need be polynomials; no erroneous assumption that every Wigner small-d entry is a polynomial in cos beta is required. Normalizing the product weights by Haar mass gives a positive probability distribution.

The chosen `L=4N+4` safely exceeds the needed degree. The node count is `(2L+1)^2(L+1)=O(L^3)` per SO3 factor, with a product of two such factors. This finite ideal construction exactly reproduces the Haar-averaged channel; its large table size is not hidden as a practical advantage. Gauss nodes/weights and Euler rotation entries are algebraic and can be approximated with controlled error.

Primary source directly inspected: [Khalid et al., Gauss-Legendre Sampling on the Rotation Group, v2](https://arxiv.org/html/1508.03353v2), SectionsII-B andIII-B/C, equations2,14–18. It supplies the established Fourier/Legendre sampling context. The degree bound for this estimator apparatus and the zero-frequency-only proof above were checked independently; no quadrature novelty is accepted.

## 4. Bounded random bits and precision

The finite-interface addendum gives a useful alternative to constructing the exact quadrature table. Couple each b-bit midpoint draw to a uniform draw in its cell. With `h=2^-b`, each azimuth error is at most pi*h and the z=cos(beta) error at most h. The stated cosine inequality implies `|beta-beta'|<=pi sqrt(h/2)`. Telescoping the Euler factors yields an SO3 operator-norm difference below `9 sqrt(h)`. The tensor-product label actions differ by at most `18 sqrt(h)`.

A unitary channel's half-diamond distance is at most the operator-norm distance of its unitaries. Each of N label transformations therefore costs at most `18 sqrt(h)` in the hybrid bound. For qubit unitary channels represented by two SO3 rotations, half-diamond distance is exactly half their SO3 operator-norm distance, so the two corrective rotations cost at most `9 sqrt(h)` together. The estimator need not be continuous: both transformed inputs pass through the **same fixed CPTP estimator**, and contractivity controls that change. Output corrections are compared separately.

The result `(18N+9)2^(-b/2) <=32(N+1)2^(-b/2)` is valid. Six b-bit draws use exactly6b fair bits, with no rejection or Haar oracle. An even b satisfying the desired bound can be selected by integer comparisons. The implemented single-use channel obeys the stated additive budget

`432/(m g_L^2) + 32(N+1)2^(-b/2) + N(tau_label+tau_measure) + tau_process + 2 tau_gate`.

These tau values must bound the actual implemented channels, including classical-outcome registers where relevant; observed matrix residuals are not such certificates. The finite-count tie convention above makes a uniformly approximable ideal processor well defined. Arbitrary-precision arithmetic, compilation and routing are charged rather than presumed exact. Imperfections in the underlying coherent source-to-label acquisition are a separate dependency/error budget, not automatically included in the post-acquisition tau terms.

## 5. Ordinary calls and readiness

In the stipulated memoryless source, a minus branch is `q sigma_R` and its probability is `q=(8+eta)/18>=4/9`. For each waiting-flag string that produces N labels, the retained joint state is the same `sigma_R^tensorN`, multiplied only by the scalar probability of that flag string. Summing any accepted set of waiting strings leaves exactly that normalized product state. Thus acquisition completion-time selection, unlike the earlier antisymmetric-growth runtime selection, does not bias this estimator's label law.

The expected ordinary-call cost is at most9N/4. Capping a fresh attempt at `ceil(9N/2)`, discarding incomplete statistics/registers, and making at most r fresh attempts gives abort probability at most `2^-r` and a deterministic total call cap `r ceil(9N/2)`. A successful batch feeds the same estimator law. If aborts are replaced by an arbitrary fallback gate and the flag is discarded, the abort probability may additionally be charged as a bad-branch contribution; otherwise it is a separate flagged availability guarantee. Any statistical failure probability for a separately obtained eta/gap promise must likewise be paid, together with the calls used to establish that promise.

## 6. Independent evidence and decision

`independent_checks.py` verifies24 exact rational covariance-state/measurement-variance cases;800 eigenvector/projection perturbation fixtures; all2,002 entry monomials of degree at most5 against independently derived exact rational Euler integrals; a nontrivial actual binary record-measurement-to-gate twirl at four unknown rotations;5,000 midpoint couplings; nine exact negative-binomial cap cases; and exact Bell/Pauli metric identities. The operational twirl fixture has a nonzero analytically known kappa, so it is not merely checking that an uninformative average vanishes.

The author estimator replay agrees on every data field except elapsed runtime; its quadrature replay agrees exactly. These diagnostics supplement the mathematical proofs, not replace them. They are not native quantum measurement executions, certified Monte Carlo confidence intervals, or diamond-norm SDPs.

At fixed valid gap g_L>0 and one averaged gate use, this conventional estimate-and-apply route has `O(1/epsilon)` normalized-label and expected ordinary-call cost, plus explicit precision and readiness budgets. Therefore an approximate quantum-program advantage cannot be established by contrasting its averaged-channel error with a classical *high-probability per-estimate* inverse-square-error bound. This is a corrected matched-metric comparator, not a universal optimality/lower-bound theorem, a multi-gate reusable-calibration theorem, or evidence of a practical implementation. No approximate advantage for the quantum-program route is established by the reviewed packets.
