# Receiving review: conserving common clock and independent zero-rate gates

29 October 2026. Existing physical-mechanism role. Root files were not edited. No additional helper or numerical fixture was used.

## Actual inputs and disposition

| Input | SHA256 |
|---|---|
| `COMMON_CLOCK_FAILS_ON_THE_CONSERVING_RING.md` | `4609f636ea4b0291d929efe19000e84556cbdc4218bb8b2ff34d85e026d02572` |
| `INDEPENDENT_CONTROL_OPENS_ZERO_RATE_GATES.md` | `42b0e66f96e12059613cd6fccda9e05f03e2d3e21f836c109a5b43fcea383db3` |
| `record_geometry/PHASE_ENERGY_SUPPLIES_EXCHANGE_COERCIVITY.md` | `7bcaa5f294219055b598f69e605ee285b5083e01db1fe1f8f2052511d3fe7189` |

Exact snapshots and input metadata are preserved alongside this review. The earlier common-clock version `34c56ffb5dfe4fddb239d3828ea0bd45d9902a56ee5679f70acd889b842d7621` was also read and preserved before the zero-gate extension. The finite rational identity checker and its output were read; they check generator algebra, not the asymptotic probability bounds.

**Accepted at the declared joint Markov interface:** the current decomposition; speed-N exponential equivalence; strict rare-current upper bound for fixed alpha below one; separate canonical stationary final-time CLT; superexponential suppression of nonzero circulation when alpha_N tends to one; and the independent-control form repair and full-action receiving extension at exact amplitude one.

**One record-scope wording correction is requested.** The sentence permitting an arbitrary retained initial record should require that the *entire future conditional native-and-clock generator* remains the displayed one. Fresh common-clock innovations alone do not suffice if that record exposes future native innovations. This does not change the unconditioned theorem or the proof under the intended Markov interface.

No full common-clock LDP, general necessity threshold, practical speedup, apparatus realization of parity-dependent coefficients, or fixed-resource comparison is accepted or claimed.

## 1. Admissible family and exact current martingale

For even N, every active exchange, including the periodic wrap bond, reverses both p and delta_i. Therefore alpha p delta_i is own-swap invariant. At fixed sigma the native rates are reversible in uniform occupancy, and common sign flips are reversible in the fair sign. Uniform canonical occupancy times a fair sign is stationary in every conserved sector.

Inactive bonds must not be counted as parity-changing attempts. The text and checker explicitly exclude them. On active bonds delta_i is plus or minus one, and around the ring sum_i delta_i=0. Consequently

\[
\sum_{i\,\mathrm{active}}r_i=cA,\qquad
\sum_{i\,\mathrm{active}}r_i(\delta_i-\alpha u)=0,
\]

and

\[
\sum_{i\,\mathrm{active}}r_i(\delta_i-\alpha u)^2
=cA(1-\alpha^2).
\]

Thus M is the uncompensated sum of zero-drift increments, not a current martingale with a missing order-N drift. Its jumps are bounded by 1+alpha, and it does not jump at common-clock events.

Every native jump and every common-clock jump reverses u, so pathwise

\[
\sum_{\mathrm{native}}u_{v-}
=\frac{u_0-u_t}{2}-\sum_{\mathrm{clock}}u_{v-}.
\]

Substitution of the compensated clock count proves the stated decomposition, including the negative signs on both clock terms. Simultaneous events have probability zero under the declared continuous-time law.

## 2. Exponential equivalence has the correct speed

The clock martingale estimate is uniform in its predictable integrand u. Its exponential compensator is at most

\[
\gamma_NN^2T[e^{|b\alpha|/N}-1-|b\alpha|/N]
=O_b(\gamma_N).
\]

The multiplier is exactly the one associated with speed N and N^-2 current normalization. This part needs no stationary initialization.

Normalize the one-sign form by
\(D_\sigma(f)=\tfrac12\mathbb E|f(\eta,-\sigma)-f(\eta,\sigma)|^2\).
Oddness in sigma gives

\[
|\langle\alpha\gamma_N\sigma p,f^2\rangle|
\le\sqrt2\,\alpha\gamma_N\sqrt{D_\sigma(f)}
\]

for unit L2 norm. Discarding the nonnegative native form, the top numerical range of the macroscopic generator plus the potential is bounded by

\[
\sup_{d\ge0}\{\sqrt2|b|N\alpha\gamma_N\sqrt d-N^2\gamma_Nd\}
=\alpha^2b^2\gamma_N/2.
\]

This verifies the factor one half in the Feynman--Kac estimate. A point mass on occupancy/common-sign states costs at most 2^(N+1) against the uniform product reference. Its normalized log cost is finite. For each fixed b, gamma_N/N tends to zero; afterwards b tends to infinity. This proves superexponential negligibility even from arbitrary initial points. It does not transfer a finite action probability through an initial density ceiling.

The conclusion here is terminal-current exponential equivalence. A uniform current-path version is unnecessary for the stated rare-current bound and has not been assumed.

## 3. Activity and the strict fixed-amplitude upper bound

The direct one-block upper argument in `RARE_TRANSPORT_WITHOUT_KINETIC_IDENTIFICATION.md`, Section 3, transfers to this common-clock model. Conditional on the autonomous common-sign path, each native generator is reversible in the same visible law and dominates c(1-alpha) times the ordinary exchange form. Global parity dependence does not enter this comparison.

The internal block activity has canonical conditional mean 2 chi(block density). Finite block Poincare controls its centered potential. Concavity of chi and conserved mass bound the sum of block means by 2 chi(global mass). Only this activity *upper* estimate is used; no unproved two-sided local equilibrium or independent per-bond sign law is needed.

The exact martingale compensator expands as

\[
\frac{B_N(b)}N
=\frac{b^2c(1-\alpha^2)}2
\int_0^T\frac{A(\eta_{N^2t})}{N}\,dt+O_b(N^{-1}).
\]

The remainder is deterministic: physical duration N^2, total intensity O(N), and exponent increments O(N^-1) give a raw cubic remainder O(1), hence O(N^-1) after normalization. The activity upper bound and mean-one exponential martingale yield

\[
-\frac{q^2}{2s\chi(m)(1-\alpha^2)T}.
\]

Exponential equivalence transfers this upper exponent from M to actual signed current J. It is strictly below the reference SSEP local-probability exponent for nonzero q. An upper bound suffices to contradict that reference LDP; a matching common-clock lower bound is unnecessary.

The matched positive comparison can use exactly the same deterministic flat initial configurations and all recorded initial orientations equal to plus one. Canonical equilibrium is not required for this rare-current obstruction.

## 4. Separate stationary variance diagnostic

For the CLT claim, uniform canonical occupancy times a fair common sign is an explicit initial premise. Counting adjacent and disjoint bonds gives Var(A/N)=O(N^-1). Stationarity and Jensen control integrated activity without any temporal mixing estimate. The normalized martingale bracket tends to s chi(m)(1-alpha^2)T and bounded martingale jumps vanish at scale N^-3/2.

The clock remainder has variance alpha^2 gamma_N T/N at that scale. The occupation remainder is centered in the stationary law. Inserting b=lambda/sqrt(N) into the exact Feynman--Kac estimate gives a sub-Gaussian variance proxy alpha^2 gamma_N T/N. Its second moment therefore vanishes as well. The boundary term is deterministic and negligible, proving the stated normal limit for actual J.

The file correctly does not infer an LDP from this CLT. The exponential decomposition and activity bound independently prove the rare-event obstruction.

## 5. The alpha_N to one extension needs no lost ellipticity

All algebra above remains valid for 0<=alpha_N<=1. In particular the remainder bound uses only the sign form and nonnegative native form, so its constant remains bounded at alpha_N=1.

For the native martingale, A<=N gives the deterministic bracket bound

\[
\langle M\rangle_{N^2T}\le c(1-\alpha_N^2)N^3T.
\]

The bounded-jump exponential estimate thus gives normalized log moment at most
\(c b^2(1-\alpha_N^2)T/2+O_b(N^{-1})\).
It tends to zero for each fixed b. Chernoff followed by b tending to infinity proves superexponential concentration of M/N^2 at zero. Together with the remainders it proves the stated concentration of actual circulation. No activity replacement and no lower bound on native rates were reused in this step.

At exact alpha=1, every positive-rate native exchange has delta_i=u_pre, so its corrected increment is zero and M is identically zero. The identity is therefore especially transparent at the endpoint. The assertion concerns a sequence of generators with fixed alpha_N during each execution, not an unprovided time-dependent alpha controller.

## 6. Independent sign control really repairs the exchange form

For one bond put h=f^i-f, let h^flip denote its value after that independent sign flip, and write

\[
I=\int|h|^2,\quad J=\int|h-h^{\mathrm{flip}}|^2,
\quad W=\int(1+\beta_i\sigma_i)|h|^2.
\]

Since beta_i is sign independent, sign symmetry gives
\(|\int\beta_i\sigma_i|h|^2|\le\sqrt{IJ}\).
Therefore I<=2W+J. Native exchange commutes with the corresponding sign flip and preserves the reference measure, so
\(J\le4\int|f^{\mathrm{flip}}-f|^2\).
Summing and dividing by two yields exactly

\[
D_{\rm ex}\le(4/s)D_{\rm native}+4D_{\rm sign}.
\]

The constants agree with the displayed form conventions. Consequently gamma_N>=s implies
\(D_{\rm native}+\gamma_ND_{\rm sign}\ge(s/4)D_{\rm ex}\).
The phase-circle version was also checked directly: periodic integration by parts gives I<=2W+4J with J the phase-derivative norm; commutation of swaps and phase derivatives gives the coefficient eight in
\(D_{\rm ex}\le(4/s)D_{\rm native}+8D_\theta\).

These are joint-form comparisons. They do not assert positive instantaneous native rates or autonomous native mixing. Independent coordinate control is material: a single common derivative or flip cannot be summed in the same way without a volume factor.

## 7. Full-action receiving audit at exact zero native rates

The occupation comparison can use the full joint form after the inequalities above. The remaining phase-independent visible variational inequality is applied to f(.,phase) at each fixed phase, with its actual squared norm, and then integrated. This does not require factorization of the evolving joint law.

Phase-drift estimates already discarded the nonnegative native form, so their constants remain finite at amplitude one. The weak comparison tilt multiplies the same native rate by a positive bounded factor. Zero-rate transitions stay zero under both laws. The likelihood and its second-moment formula involve r_i(e^xi-1), not 1/r_i, so their use does not fail at a closed gate.

Current exponential tightness uses bounded rates, bounded jumps, continuity, and the phase-replaced drift. The active circle heat-layer density bound uses visible invariance conditional on the phase history, not strict native ellipticity. The finite sign reference dominates arbitrary starts as before. The tilted hydrodynamic receiver requires the transferred occupation form and vanishing phase drift, which remain available; its limiting diffusion coefficient stays s/2.

The finite-energy identification, good-action argument, and smooth finite-action approximation are unchanged macroscopic steps. On the already accepted underlying action and hydrodynamic dependencies, the full receiving extension to exact amplitude one is therefore sound. The file correctly withholds an automatic extension of arbitrary additive implementation errors at a closed gate: nonnegative actual rates and the replacement form comparison would need separate proof.

## 8. Physical and retained-record scope

The output is actual signed particle transport. Parity occurs only in admitted kinetic coefficients and need not be measured by the controller. Realizing those nonlocal coefficients has not been physically constructed; the conclusion is a mathematical separation within the permitted family.

One common Poisson pi clock and N independent local clocks are distinct suppliers. Every bond's marginal sign process can indeed have the same flip rate in both implementations, while their joint correlations differ. Their total event counts and actuation resources differ. The theorem establishes no superiority at fixed power, event count, wiring or fabrication cost.

After equation (10), require that conditional on any retained past record the full native jump intensities and clock law remain the declared joint law. If the record determines future native innovations, fresh common-clock increments alone do not restore Feynman--Kac or the martingale calculations. This is the only requested wording correction. A past record specifying just the initial state, frozen data, or initial orientation is harmless under the intended fresh-future interface.

No guarantee after arbitrary rare future-record postselection is supplied. Canonical stationary preparation for the CLT, nonlocal coefficient realization, timing, current sensing, independent actuation, and energetic costs remain actual external premises.

## Final receiving status

The common-clock counterexample and zero-rate extension survive the assigned attacks. The independent supplier can recover the nontrivial reference rare-current action at exact amplitude one, whereas the common supplier with gamma_N/N tending to zero suppresses every fixed nonzero circulation superexponentially. The stated mathematical consequence is accepted with the full conditional-generator clarification above. It does not need, and does not receive, an apparatus or historical-priority claim.
