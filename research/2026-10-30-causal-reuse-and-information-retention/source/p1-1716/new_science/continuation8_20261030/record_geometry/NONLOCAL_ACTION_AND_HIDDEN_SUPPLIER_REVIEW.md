# Actual-file receiving review: nonlocal action and compatible hidden kinetics

30 October 2026. Complementary Astra P1 mathematical review. Exact reviewed inputs are preserved alongside this file.

| Input | SHA-256 |
|---|---|
| `NONLOCAL_ACTION_FROM_EVENT_MEMORY.md` | `9ac12fa8af633308446e3e18d2421d286c1fed43f96496353e052fce18532be8` |
| `HIDDEN_KINETICS_AND_DESIGNED_MEMORY.md` | `39d23c21bc8cd7bdc1f52ca82a7d00be3a51de0ef74ccc977de4145111dc1a27` |

**Disposition:** accepted as a proved receiving construction at the explicit stated interface, conditional on the retained weighted-corrector, occupation, and round7 topology/smoothing dependencies. I found no substantive correction needed in these actual versions. This is a mathematical review, not formal verification, experimental validation, or a historical-priority verdict. No new optional numerical fixture was run for this review.

The weighted-corrector supplier was authored in this complementary role and independently read by root. The present review reconstructs the remaining root receiver and action proof; it does not purport to be an independent re-authorship of that supplier.

## 1. Clean actual-process receiver

The corrected increment `d_E=E_i delta_i-alpha u A_E/A` is uniformly bounded. The comparison tilt therefore has the required second-moment likelihood bound `exp(O(N))` even though `d_E` is not an antisymmetric native edge increment. Girsanov's jump likelihood needs predictability and the true compensator, not antisymmetry or a tilted invariant law. Equation (13) uses the correct base martingale compensation `cS_E`.

The covariance expansion and its factor of two are correct: the microscopic coefficient is `c`, canonical/local activity supplies `2 chi`, and the resulting mobility coefficient is `s=2c`. The nonlocal ratio can be replaced without cutting off small activity because `be/a`, extended by zero, is Lipschitz on the cone `a>=0`, `|b|<=||H||a`, `|e|<=||E||a`. Its derivatives are bounded there, and the cone is convex. Occupation replacement first supplies the three moments in time `L1`; this cone property then supplies their quotient. The stronger assertion is continuity of the covariance ratio, not of the unweighted average `A_E/A` at zero activity.

The limiting weak equation has enough energy to justify the positivity and difference tests. For each candidate solution, regard its bounded scalar `q_E(rho)(t)` as a given measurable time coefficient. It has no spatial derivative. The constant subsolution `m exp(-s||E_x||t)` satisfies the required sign inequality; applying the same comparison to holes gives the upper bound. Both density and holes remain strictly positive on the finite interval. Thus `C_rho` has the claimed lower bound, and the ratio map has the displayed `L1` Lipschitz constant. The `L2` difference energy estimate and Gronwall identify a unique limit. There is no missing assumption of a local kinetic amplitude or a phase-factorized evolving density.

Existence comes from the tight stochastic subsequences and their weak equation. The proof does not need a separate unsupported global nonlocal-PDE existence result. The fixed flat interior initializer matters here: an arbitrary profile touching zero and one would not get the displayed positive constant by this argument.

## 2. Action, topology, and approximation

The likelihood sign is correct. The linear term is `int E j-c int rho E_x`, hence `int E(j+c rho_x)` after integration by parts. Inverting the rank-one mobility gives the displayed inverse field and positive extra action term. The inequalities `I_0<=I_alpha<=I_0/(1-alpha^2)` follow from homogeneity of the quadratic dual and its norm comparison, with extended-real conventions.

The reviewed file does not incorrectly infer lower semicontinuity from norm comparison alone. Its independent representation

`M_rho(E,E)/s = inf_b int chi(rho)[E^2-2 alpha b E+b^2]`

is correct. The bracket equals `(E-alpha b)^2+(1-alpha^2)b^2`, is nonnegative, and its minimizing scalar is `b=alpha int chi E/C`. For fixed `b` the density functional is concave and weakly upper semicontinuous; their infimum has these same properties. Bounded minimizing time coefficients can be approximated in ordinary time `L2`. This gives the required lower semicontinuity of the likelihood dual on bounded-density paths, and closed sublevels inside the accepted compact reference sublevels give goodness.

Current compact containment uses the exact ring conservation estimate, not an assumed bounded variation for all paths in the ambient Skorokhod space. Fixed smooth test moduli come from the actual weighted-current correction and bounded martingale jumps. The same deterministic negligible interpolation issue handled in round7 remains attached: finite-`N` paths have jumps; their limit support is continuous.

The extra perspective term `(int j)^2/C_rho` is jointly convex because its numerator argument is linear and `C_rho` is concave. Spatial smoothing increases `C_rho` and preserves the spatial integral of current. Past-only time smoothing after the flat extension preserves continuity and the initial trace and does not increase either cost. Combined with the existing finite-energy/Riesz argument and lower semicontinuity, this is a cost-preserving density of smooth paths. The smoothly inverted field is bounded for each fixed approximating path, which is exactly what the weak-tilt receiver requires.

The circulation contraction stated in Section 6 also checks: spatial Cauchy–Schwarz bounds the first action term below by `(int j)^2/C_rho`; adding the second yields its factor `1/(1-alpha^2)`. Concavity gives `C_rho<=chi(m)`, and time Cauchy–Schwarz gives the scalar lower rate. The flat constant-current path attains it.

## 3. Combined physical supplier

The product rate in the second input is an explicit actual composition premise. Its joint-swap symmetry is precisely what is needed for reversibility. In coordinates `sigma=u p(eta)`, a native exchange holds `sigma` fixed, and the unknown amplitude is invariant under that visible exchange. Therefore the native form dominates the ordinary visible exchange form with constant `c(1-alpha)(1-b)` at each fixed phase and sign. The reference conditional on each frozen `z` is the stated canonical/sign/circle product law.

All additional drift, bracket, and endpoint-corrector terms are linear in the phase cosines with coefficients independent of every actuated phase. The true compensated martingale subtracts the true rate sum, as the file explicitly says. It is not silently called the clean martingale. The added drift `sum R_i d_i(H)`, bracket terms, and generator correction `sum u R_i Delta_i F_H` have coefficients bounded uniformly in state and size. Their `sum_i ||coefficient_i||_infinity^2=O(N)` bound is enough for the independent-phase Feynman–Kac estimate. The file explicitly avoids the invalid interchange of a supremum and a sum of state-dependent coefficients. The comparison tilt remains bounded by `K/N`, so all these superexponential estimates transfer to it.

The extension of the inverse-activity proof to compact phase coordinates is justified directly. The process is a bounded-rate jump process coupled to smooth autonomous diffusions on finitely many circles. Visible density tests have no diffusion derivative. Their martingale brackets, stationary forward/backward identity, and visible-form energy estimates are unchanged. The conditional canonical occupation inequalities integrate over the phase variables. No finite-state approximation or hidden spectral gap is used.

## 4. Arbitrary initial phases and complete records

The phase warmup density bound is valid without independence of visible and phase states. Autonomous heat evolution bounds the phase marginal by `K_v^N` for any starting phase vector or mixture; each visible/sign conditional mass is at most one. Multiplying by the reciprocal uniform visible/sign mass yields `2 binom(N,M_N) K_v^N` for the complete endpoint law. The initial native count is dominated at mean `O(N/kappa_N)`, so the density/current perturbation of this active initial layer is superexponentially negligible. The shared-bit count can be larger but does not change the visible density or current.

The density ceiling is used only to transfer superexponential estimates. The tilted receiver starts with actual visible association and retains its actual initial law; it does not assign a finite-action probability by multiplying a reference event by an exponential ceiling. This distinction is explicitly preserved.

Both inputs require the complete conditional future generator after retained records. They do not assert an arbitrary joint apparatus-record LDP. Random canonical visible starts would add a static initial-density cost to the full spatial action; the main result correctly uses associated deterministic starts and retains a common association modulus for uniform families.

## 5. Accepted limits and remaining questions

Accepted: fixed `alpha<1`; strictly positive combined native ellipticity; the positive shared-clock window `N gamma_N -> infinity`, `gamma_N/N -> 0`; independently supplied phase diffusion with `kappa_N -> infinity`; fixed macroscopic horizons; the stated actual rate/symmetry and initializer interfaces. The combined action is uniform over the admitted bounded, phase-independent frozen kinetic amplitudes because every estimate and receiving equation is uniform in those amplitudes.

Not supplied by these proofs: zero-external-clock full spatial action; the singular `alpha=1` full spatial action; independence from arbitrary hidden changes of the selected mean rates; inferred compatibility of unmeasured interventions; a finite-data acquisition certificate; finite-`N` convergence rates; a practical advantage or apparatus; a full fluctuation theorem merely by differentiating the LDP; or a priority claim for generic noise control.

The concrete receiving gap left in round7 is closed at the positive-clock interface. A small designed kinetic memory and an independent phase supplier now have distinct mathematically certified roles in this compatible physical family.
