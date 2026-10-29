# Focused receiving review: action, approximation and physical scope

29 October 2026. Existing physical-mechanism role; no new helpers. Root files were not modified.

## Inputs and disposition

| Actual input | SHA256 |
|---|---|
| `CONTROLLED_MACROSCOPIC_ACTION.md` | `c15a789c95e8472531fd575a9f252f35d6345ea7f5d830d35c08a4a07ab3202e` |
| `IMPLEMENTATION_SYMMETRY_AND_RARE_EVENT_CONFIDENCE.md` | `a93e4af190a7aaa45ea2a65b6ad6cdfd1fa2f14440aabe603a63c3c2761f1d20` |

Exact snapshots and `REVIEW_INPUTS.json` are preserved alongside this review. The phase-replacement, scalar-current and ordinary hydrodynamic dependency files were also read for their initialization and clock scope.

**Disposition:** no counterexample or necessary correction was found in the assigned parts: current compact containment, exponential continuous tightness, finite-energy identification, full finite-action smooth approximation, and implementation/record/cost claims. These parts are accepted at their exact stated mathematical interface, **conditional on the separately reviewed occupation and weak-tilt hydrodynamic inputs** assigned to record-geometry. This is not acceptance of an apparatus, acquired uniform structural bounds, finite-N error rates, priority or practical speedup.

The full path action is stronger than the scalar-current result. The extra topology, compactness and approximation arguments are actually supplied; they are not inferred from a scalar LDP by assertion.

## 1. Current compact containment and topology

The finite conservation identity gives \(|J_i-J_j|\le N\) along an arc. Therefore, with \(w_i=J_i/N\), all values differ by at most one and

\[
\|W_t^N\|_{TV}=N^{-1}\sum_i|w_i(t)|
\le|N^{-1}\sum_iw_i(t)|+1=|Q_N(t)|+1.
\]

This prevents positive and negative spatial currents from escaping while their circulation stays bounded. It is a one-dimensional ring fact. Higher-dimensional divergence-free circulation would not obey this argument, and the theorem does not claim that extension.

On a total-variation ball, Fourier coefficients are uniformly bounded and the \(H^{-3}\) tail is summable. The strong \(H^{-3}\) topology thus agrees with weak measure convergence there, and the ball is compact in \(H^{-3}\). Exponential tightness of \(\sup_t|Q_N|\) supplies the needed current ball; no deterministic bounded-current assertion is made.

The finite density/current relation passes to limits in this topology. For a smooth test G, its discrete gradient differs from G_x by O(1/N) in H^3. Hence the discrete continuity error tends to zero on bounded H^{-3} current sets, not merely on states with bounded microscopic counters.

## 2. Exponential time tightness and interpolation

For a fixed smooth test, jumps are O(N^-2) and quadratic variation per macroscopic unit is O(N^-1). Applying the exponential martingale with multiplier bN yields the stated correction exp(Cb/N). The unmodulated test drift is bounded. An increment of the integrated phase remainder is at most twice its full supremum, so the already proved superexponential supremum estimate is enough; no instantaneous-small-current assertion is needed.

The exponential Ascoli step can be made explicit. Fix a target exponential level L. First restrict circulation to a cutoff whose complement has exponent below -L-2. On the resulting total-variation ball, truncate the H^-3 Fourier tail at each desired norm accuracy. Only finitely many smooth tests remain. Choose their time meshes so the modulus failures have probabilities below exp[-N(L+ell+2)], then intersect over ell. The closure is equicontinuous with compact spatial range. A standard diagonal construction can shrink each mesh further to handle its finitely many small N; this preserves the limiting bound. The summable union proves exponential continuous tightness.

Uninterpolated paths are not continuous. The text correctly uses a deterministic linear interpolation, which differs by at most one jump: 2/N in density TV and 1/N^2 in current TV. It is deterministically exponentially equivalent in the ambient path topology. No physical interpolation is assumed. The claim is continuous limiting support, not literal continuity of the finite-N jump paths.

## 3. Finite-energy identification and goodness

Scaling a smooth field in the finite variational supremum bounds its linear part in the weighted norm L2(chi(rho) dxdt). Riesz representation gives

\[
A=\partial_tW+D\rho_x,\quad
\int A^2/\chi(\rho)<\infty,\quad D=s/2.
\]

The boundary convention is correct: A vanishes where chi=0. Since chi<=1/4, A is also in ordinary L2. Singular temporal current cannot hide in this representation, because it would violate the bounded weighted linear functional.

Conservation yields the forced heat equation rho_t=D rho_xx-partial_x A. Regularizing and testing with rho-m gives the displayed energy inequality, hence rho_x and j=A-D rho_x lie in L2. With W_0=0 this identifies W_t=int_0^t j, rather than assuming that representation in advance.

Uniform action bounds give uniform L2 bounds for A, rho_x and j. Then

\[
\|W_t-W_u\|_{L^2}\le\sqrt{|t-u|}\,\|j\|_{L^2(dt dx)},
\]

and conservation gives the same modulus for rho in H^-1. Uniform spatial L2 bounds and compact embeddings into H^-3 prove compactness of action levels. The integrand A^2/chi(rho) is jointly convex by concavity of chi and the perspective inequality; lower semicontinuity supplies closure. These details validate the file's short good-rate-function argument.

## 4. Full smooth approximation survives endpoint and boundary attacks

The flat initial density is materially used.

1. Mixing with the path (m,0) preserves continuity and the initial trace, makes the density strictly interior, and costs at most (1-delta)I. This follows from chi((1-delta)rho+delta m)>=(1-delta)chi(rho), with the squared numerator scaled by (1-delta)^2.
2. Spatial convolution preserves the constant initial density and continuity. Jensen applies to the jointly convex (rho,A) integrand.
3. Extending rho as m and current as zero before time zero introduces no delta source, because the density trace is m. Its action is zero there. A smooth kernel supported on past lags [epsilon,2epsilon] makes the path flat with zero current near time zero, while preserving the exact initial profile. Values beyond T are never needed.
4. A is convolved linearly with rho and j. Jensen plus the zero-cost past extension bounds the cost on [0,T]. For fixed positive delta the resulting E=A/[s chi(rho)] is smooth and bounded, including at the endpoints.
5. Convolutions converge in the stated L2 quantities; integrated currents converge uniformly in time in L2, and densities converge in the continuous weak path topology. Lower semicontinuity plus the upper cost bound gives convergence of costs, not merely a convenient lower-cost unrelated sequence.

I found no boundary-density or temporal-singularity finite-action path defeating this construction. It does not automatically extend to a nonconstant prescribed initial profile; the file claims only the flat-initial problem.

## 5. Upper neighborhoods and actual initial laws

The unsmoothed mobility term is not continuous in the weak density topology. The proof correctly smooths only this term at a fixed macroscopic block scale during the neighborhood upper bound, then removes the scale after the volume limsup. Bounded densities give space-time L1 convergence of smoothing. The occupation estimate uses the necessary order of limits, not an unsupported superexponential assertion at each fixed block scale.

The current martingale has mean one under the actual initial law. The lower bound uses the actual tilted comparison law with that same start. The active phase layer is used for superexponential estimates and typical hydrodynamics, not to transfer finite-action probabilities using an exp(hN) density ceiling. This distinction is present and essential.

Random initial profiles that are merely typically flat would need an initial LDP or an appropriately conditional statement. The inherited source interface explicitly preserves that limitation. Deterministic initial configurations converging to the flat profile are sufficient as stated.

## 6. Implementation error calculation

For a_i=(s/2)F_i e_i delta_i, own-swap invariance gives

\[
\langle\sum_i a_i,f^2\rangle
=\tfrac12\sum_i\langle a_i,(f-f^i)(f+f^i)\rangle.
\]

Using weights r_i/2, the first square factor is D_native. The second is at most (2/c_*)sum_i||a_i||_infinity^2. This proves the displayed coefficient s||F||d_N/sqrt(2c_*) multiplying sqrt(N D_native). No phase derivative of the error is required. Its dependence may be completely nonlocal provided exact own-swap invariance and the uniform bound hold.

Completing squares separately against native and phase energy gives the d_N^2+1/kappa_N budget. Thus reciprocal errors can vanish independently of N, without Nd_N->0. This remains a population structural theorem; it does not establish that an apparatus has such a vanishing uniform error.

The directional counterexample is correctly normalized. Rates multiplied by exp[c delta_i/N] give the flat-profile current s chi(m)cT. Thus an O(1/N) absolute perturbation can have an order-one macroscopic consequence when reciprocity is lost. The document does not infer a general biased action merely from this mean-current shift.

## 7. Calibration, records and physical resources

The calibration-mixture calculation is correct. A fixed nonzero chance of a second mean rate selects the minimum of its two rare-event exponents. A branch probability exp[-NJ+o(N)] adds J to that branch's cost. Fixed coverage confidence cannot be silently added to a speed-N claim. Conditioning on a retained branch label is a separate conditional question, and the text does not confuse it with the unconditional mixture.

The actual supplier is a continuous-time family with independent phase diffusion or local sign-reversal access. Endpoint calls, invariant weights, a reversible kernel or a logged seed do not manufacture those operations. The file does not claim that they do. Weak current fields are proof comparison laws, not assumed free physical actuators.

Conditional statements require the future conditional physical generator to remain the declared one. In particular future phase increments must be fresh. If an old record determines future native jump innovations as well, the same conditional native law would also fail. Retaining controller data as generated is compatible with the same joint execution law; arbitrary rare future-record conditioning is not supplied. This is a scope clarification, not an identified contradiction in the stated old-record interface.

The horizon N^2T and kick count gamma_N N^3T are correct. The order-N^3T native opportunity count is distinct from accepted swaps and from energy/work. Current sensing, conserved initialization, reciprocal control, known homogeneous mean, local independence, isolation and apparatus precision remain actual suppliers. No practical speedup or microscopic record-TV equivalence is claimed.

## 8. Scope of acceptance

The detailed occupation/two-block transfer and reconstructed weak-field hydrodynamics remain the separately reviewed dependency. Fabrication, acquisition of uniform error bounds, historical priority, finite-N rates, and a conserving-ring common-clock obstruction are not accepted by this review. The latter remains constructive work, not a consequence of the heat-bath example.

No numerical fixture substitutes for these analytic checks. The assigned core is accepted without extending the topology, finite macroscopic horizon, deterministic initial-profile interface, conditional future-noise law or physical ports.
