## Governing transport evidence

Paths are relative to the pinned published snapshot in the sibling `published_repo` directory.

- **N747**, `updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/research_note.md`: §§2–3 (lines 33–181) define the infinite-temperature, number-conserving, physically dephased model and prove the balanced two-sided finite response theorem; §4 (lines 199–243) identifies the population operator as weighted classical exclusion. §§7 and 10 give the thermodynamic second-moment transfer and actual local-intervention contract. The general supplied-graph population Poisson solve is already in the source; it is not the new operation here.
- **N765**, `updates/EX/package/frontier_residual/recovered/astra_frontier_residual_response/research_note.md`: lines 33–56 give the physical input/output; lines 66–120 the exact balance and corrected-residual identity; lines 122–185 the complete response-error derivative bound; lines 187–235 the finite-packet and thermodynamic transfer. The source explicitly assumes exact local coefficients/structure and does not infer physical acquisition from numerical certificates.
- **N768**, `updates/EY/package/frontier_decision/recovered/astra_frontier_decision_calibration/research_note.md`: lines 37–65 and 292–326 give the preparation/switching/readout premises; lines 403–438 the bias, shots and globality conditions; lines 492–520 the already existing optional coarse-box assay. Its quoted observations are synthetic. Repeating that rule would not be a new acquisition result.

N765's source supplies an a posteriori instance-specific decision result, not an affordable full-class inverse theorem. In particular, its `86.44` factor compares regret-envelope widths at the same witness data; it is not a runtime speedup. General high-precision polynomial closure and quantitative full hydrodynamics remain open (N747 §13, G1/G2).

## New construction: local coherence-edge retargeting

### Exact enlarged model contract

Let

`H_a(V) = -sum_i a_i(n_env) (sigma_i^+ sigma_(i+1)^- + sigma_i^- sigma_(i+1)^+) + H_diag(V)`.

Here each `a_i` is the translate of a real finite-range diagonal function of sites **excluding the hopping pair**. Assume `0<a_min<=a_i<=a_max`; its environment values may be unknown interval parameters. `H_diag` is a real bounded finite-range diagonal interaction, with the selected control `V` entering affinely and diagonally. Preserve the physical generator

`L_a O = i[H_a,O] + (d/4) sum_i (Z_i O Z_i - O)`, `d>0`,

and the normalized infinite-temperature product trace. Locality, translation invariance, time invariance, Markovianity, the noise model and the specified hopping graph are physical premises, not inferred from finitely many successful assays. Complex configuration-dependent phases, additional transition edges, nonunital noise and finite-temperature reference states are outside this theorem.

The actual bond current is

`j_i(a) = (a_i/2)(X_i Y_(i+1)-Y_i X_(i+1))`.

It obeys the actual continuity equation. Distinct bonds flip different occupation pairs, so their tracial cross terms vanish on sufficiently large rings. Therefore

`b_J = ||j_a||_#² = (1/2) E_env a_i² <= a_max²/2`,

and `S j_a=d j_a`. This replaces the special source constant `t²/2`; it must not be reused unchanged.

### Retargeting theorem and proof

Take a nominal constant hopping `t0>0`, any diagonal nominal interaction, and an explicitly represented odd Hermitian translation-covariant local witness `f0` in the admitted even-X/Y-parity sector with

`P A0 f0=0`, where `A0=-i[H0,.]` and `P` is complete occupation dephasing.

For each edge `i`, let `E_i f0` retain exactly its matrix elements between configurations differing by the allowed nearest-neighbor occupation exchange on that edge. Different `E_i` have disjoint off-diagonal supports. Define

**`f_a = f0 + sum_i (t0/a_i - 1) E_i f0`.**

This is a real-linear operation on the imaginary matrix entries of `f0`. The ratio is equal at both endpoints of an exchange because its environment excludes the pair. Hence odd Hermiticity is preserved.

For a direct-hop configuration pair `(eta,xi)`,

`(H_a)_(eta,xi) (f_a)_(xi,eta) = (-a_i)(t0/a_i)(f0)_(xi,eta) = (H0)_(eta,xi) (f0)_(xi,eta)`.

The conjugate term has the same identity. Non-edge coherences have zero Hamiltonian matrix element in both hopping models; diagonal Hamiltonians contribute no diagonal commutator. Summing the diagonal commutator edge by edge proves

**`P A_a f_a = P A0 f0 = 0`**

for every allowed amplitude assignment and every sufficiently large periodic volume. There is no inverse population operator and no relaxation-gap denominator.

This operation is local. If a Pauli density has support `W`, `E_i` merely selects terms with the direct pair coherence and diagonal factors elsewhere; it does not require the full many-body matrix. Multiplication by the local function `1/a_i` expands support by the fixed hopping environment. Its Walsh/diagonal-projector expansion has up to `2^m` coefficients for `m` environment bits; that representation and arithmetic cost are charged. Other higher-coherence terms of `f0` are retained unchanged. They cannot contribute to `P A_a f_a` when the Hamiltonian graph has only the specified direct nearest exchanges.

For `|a_i-t0|<=epsilon`, the Hilbert-Schmidt orthogonality of the edge sectors also gives

`||f_a-f0||_# <= (epsilon/a_min) ||sum_i E_i f0||_#`.

This bounds the witness change. It does not by itself bound a macroscopic transport change; full commutator residuals must be generated.

### Full response and derivative certificates

Choose an even local `g0` in that same invariant sector, set `A=A_a`, use the **actual** current `J_a`, and generate every commutator output. The inherited N747 theorem applies to `f_a,g0`:

`L_a = 2<J_a,f_a>-<f_a,S f_a>-<A_a f_a,S^+ A_a f_a>`,

`U_a = <J_a-A_a g0,S_odd^(-1)(J_a-A_a g0)>+<g0,S g0>`,

`L_a/n <= kappa_a,n <= U_a/n`,

`U_a-L_a = ||S f_a+A_a g0-J_a||_(S^+)² + ||S g0+A_a f_a||_(S^+)²`.

The population part is exactly zero before `S^+` is used. Discarding the population defect of the original unretargeted or midpoint-retargeted witness is invalid.

If `f0(V),g0(V)` are finite polynomial trial jets in the diagonal control, apply the same retargeting to every coefficient of `f0`. It preserves `P A_a(V) f_a(V)=0` for every real `V`. The varied commutator `A1=-i[dH_diag/dV,.]` remains diagonal-sector preserving, so the N765 normalized bound `w=4 J_*(H1)/d` and its complete error-jet formula survive:

`|D_a^(m)(V)-Dhat_a^(m)(V)| <= 4 m! sum_(r+s+c=m) q_r(a,V) q_s(a,V) w^c/(r!s!)`.

All `q_k` are the actual complete residual derivatives, including order `M+1` and outputs outside the discovery dictionary. No hopping derivative is being bounded by the source's diagonal perturbation theorem.

Finite-range locality and the product trace give fixed-time thermodynamic current correlations. Positive rates keep each charge-sector swap graph connected; the only undamped finite zero modes remain functions of charge. Realness preserves the parity Schur argument and `S_odd>=d`. With `b_J` as above, N765's bounded Poisson transforms, positive spectral measure and continuity-equation argument therefore transfer to the same **infinite-chain second-moment coefficient** `D_a=4 kappa_a`. This imports the source's stated analytic transfer, with its hypotheses checked for the enlarged class. It does not establish a Gaussian profile, a physical-time convergence rate, or a complete independent re-audit of the inherited source.

### Finite-shot intervals are symbolic parameters

For acquired intervals `a_sigma in I_sigma` with a common positive lower bound, keep `f_a` as a rational function of **all** exact parameters. The unknown physical point is covered by this one explicitly generated family. Never insert interval midpoints or rounded coefficients and then assert exact balance for the physical point.

The finite residual coefficients are rational functions with poles bounded away by `a_min`. Interval arithmetic or exact denominator clearing and polynomial bounds can enclose their covariances uniformly over the box. Those bounds, together with control-cell bounds in `V`, can certify a global actual regret. Source nominal regret numbers do not transfer without this recomputation.

More explicitly, writing `delta f_k=f_a,k-f0,k` and `Delta A=A_a-A0`, the residual changes are

`delta r_o,k = S delta f_k + Delta A g_k - 1_(k=0) delta j`,

`delta r_e,k = A0 delta f_k + Delta A f0,k + Delta A delta f_k + k A1 delta f_(k-1)`.

The complete even sum has zero population part by the proved identity. Its pieces must be combined before applying `S^+`. Local algebra gives finite, volume-independent bounds on these quantities. Insert `q_k(a)<=q_k(0)+||delta r_k||_(S^+)` into the source derivative theorem. For a fixed finite nominal certificate with strict margins, these rational bounds vary continuously as the hopping box shrinks to the nominal point. This is a constructive local robustness statement for a certificate; it is not a uniform bound on the size or acquisition cost of certificates over all interacting inputs.

## Acquisition recipe and costs, without assuming exact amplitudes

The retargeting theorem does not acquire coefficients by itself. Under a support-complete local switching and calibration contract, a finite recipe acquires every local amplitude value. For each of `M=2^m` environment patterns, freeze the relevant environment in its chosen Z state and disable every other hopping term whose full support can affect the probed pair or change an environment occupation affecting its amplitude/detuning. For conditional hopping this includes remote bonds whose coefficient depends on a probed occupation. Merely disabling the two adjacent bonds is insufficient.

With this isolation the one-particle pair has `H_pair=-a X+Delta Z/2` and Bloch generator

`K=[[-d,-Delta,0],[Delta,-d,2a],[0,-2a,0]]`.

Assume acquired bounds `a<=a_max`, `|Delta|<=Delta_max`, `d<=d_max`, and let `L=2a_max+Delta_max+d_max`, `tau=1/(4L)`. With calibrated preparation and measurement along all three logical axes, nine expectation values determine `T=exp(tau K)`. This is ordinary process tomography, not the scientific invention claimed here.

Dissipativity gives `||T||<=1` and `||T-I||<=tau L=1/4`. If every expectation has total error at most `delta`, then `||That-T||<=3delta`. Set `delta_total=min(tau epsilon/3,1/24)`, so both matrices lie within radius `R<1/2` of identity. The convergent matrix-log series and telescoping powers give

`||log That-log T|| <= ||That-T||/(1-R)`.

Since `a=-K_zy/2`, this guarantees `|ahat-a|<=epsilon`. Retain simultaneous intervals; no exact coefficient is returned. There is no frequency-alias assumption hidden in a fitted oscillation, because the small-time log is on its explicit convergence branch.

For independent ±1 observations and failure probability `alpha`, a sufficient number per setting is

`N >= 2 delta_stat^(-2) log(18M/alpha)`.

There are `9M` settings. Reserve preparation, switching, readout, timing and arithmetic biases `b` inside `delta_total`, with `delta_stat=delta_total-b>0`. If `b<=delta_total/2`, the sufficient bound is `N>=8 delta_total^(-2) log(18M/alpha)`. Total copies are `9MN`, plus every preparation/reset, waiting time and classical finite matrix-log/interval cost. The truncated log tail can be bounded by `R^(k+1)/[(k+1)(1-R)]`; charge enough terms and precision to fit the reserved arithmetic budget. Locality/translation/Markovianity/future invariance remain device-model premises; finite tomography does not prove them against arbitrary alternatives.

A weaker-access fallback prepares logical `+Y` and reads Z. Then `z'(0)=-2a` and `|z''|<=2a_max(Delta_max+2a_max+d_max)`. A paid finite-time slope estimator gives a conservative `epsilon^-4` shot bound. Three-axis tomography has the stronger `epsilon^-2` dependence at fixed local strength bounds and should be the informed comparator whenever that access is available.

The cost is not small by assertion. For diagnostic bounds `a_max=1.25`, `Delta_max=8`, `d_max=2.1`, `epsilon=0.01`, `M=4`, `alpha=0.01`, allocating the entire mean error budget to statistics gives `tau=0.01984127`, `delta=6.61376e-5` and **146,197,128,816** sufficient shots over 36 settings. This conservative guarantee is not a necessary cost, an acquisition or an efficient proposal. A matched optimal-design/Rabi-fitting method may be much better; it must be allowed the same isolation, preparations and readout. The continuation below establishes a particular interacting thermodynamic decision for a 1% amplitude box; affordable physical acquisition of that box is not established.

## Actual checks and their scope

- `transport/edge_retarget_check.py` constructs exact rational configuration-cycle flows at periodic sizes 5,6,7,8. Changing to four environment-dependent amplitudes gives nonzero naive population divergences (maxima `13/28`, `19/56`, `33/56`, `33/28`); retargeted divergences are exactly zero. Arithmetic is `Fraction`. The all-size proof above, rather than extrapolation from these controls, establishes the operation.
- `transport/response_bounds_check.py` checks the inherited lower/upper bounds and residual-gap identity on actual correlated-hopping models at sizes 5 and 6, summing all charge sectors in the normalized trace. Naive defects reach `0.92857` and `0.67857`; repaired floating defects are below `4.5e-16`. Gap identities agree to `1.2e-16`. Trial bounds are deliberately broad; no quantitative design performance is claimed from these finite controls.
- `transport/acquire_hopping_check.py` checks the isolated-pair exponential/log and error bound on 1,000 parameter/noise cases. Maximum diagnostic amplitude error is `0.001788` under a proved sufficient `0.01` envelope. Statistical confidence comes from the analytic concentration bound, not random controls. No experimental observations were generated or represented as real.
- The one permitted Max helper independently reconstructed the new identity and checked Hermiticity, locality, actual-current normalization, symbolic intervals and support-complete isolation. Its finalized audit is `helper/conditional_hopping_retarget_audit.md`; acceptance applies at its actual stated scope.

## Preserved initial failed bridge: exact quartic separator

The initial full target was the nine-dimensional cone inclusion explicitly identified by **N794**, `updates/FE/synthesis/quartic/QUARTIC_AUDIT_AND_PROOF.md`, lines 185–189. The acoustic interface is at lines 61–65; compatible jets and closed heat certificates at lines 79–118. **N830**, `updates/FR-capital-mining-20261015/synthesis/higher_order_rigidity/PROOF.txt`, Theorems A–C, already proves that a universal smooth finite-jet local-storage repair cannot go beyond determinant-affine support/polyconvexity. This excluded simply adding more local storage derivatives as a universal mechanism.

With `u=a²+c²`, `v=b²+d²`, `w=ab+cd`, `q=ad-bc`, I constructed

`F=u²+v²+3w²+16q²+4q(u-v)`.

It is globally strictly rank-one convex. In N794's acoustic convention the integer skew completion is `(k01,k02,k03,k12,k13,k23)=(1,0,0,0,0,15)`. The 8×8 matrix is orthogonally equivalent to

`[[19,8],[8,4]]`, `[[5,16],[16,60]]`, `[[11,-8],[-8,6]]`, `diag(1,2)`.

Positive determinants give

`D²F(A)[h tensor b,h tensor b] >= (2/17)|A|²|h|²|b|²`.

The rational functional in `principal/EXACT_HEAT_SEPARATOR.json` acts on the 210 coefficients of the compatible biform in `(a,b,c,d)` and six second-jet variables. Its moment matrix on the 24 bilinear monomials is positive definite by exact rational LDL. It annihilates all 45 closed homogeneous-quadratic two-form directions, and satisfies exactly

`ell(E_I F)=-4049717/6250000`,

`ell(E_I q²)=80001/25000000 >0`.

Thus for **every** `gamma>=0`, `E_I(F-gamma q²)+omega` cannot be a bilinear sum of squares for any admitted closed quadratic two-form `omega`. This is an exact infeasibility proof, not an optimizer failure.

The symmetries `A->AS` (column swap) and `A->JAD`, with `J=D=diag(1,-1)`, preserve `F-gamma q²`. A finite group average takes any hypothetical constant SPD spatial diffusion matrix to `(tr M/2)I`; compatible jets transform linearly, closed forms by the determinant-weighted pullback, and SOS Grams by congruence. The same gamma survives. Hence the separator excludes **every constant-SPD spatial-diffusion certificate in that closed-quadratic-form/bilinear-SOS class**.

The helper's separate `Fraction` sparse-polynomial checker imports none of my numerical maps. It independently checked 80 cubic-one-form exterior derivatives spanning all 45 closed directions, both pairings, all 24 positive dual pivots and all eight acoustic pivots. See `helper/independent_separator_check.py`, `helper/INDEPENDENT_HEAT_SEPARATOR_CHECK.json`, and `helper/n794_symmetric_bridge_audit.md`. This is a completed substantive internal audit at the exact stated scope. Historical priority is not established.

This does **not** refute quasiconvexity of F or the full planar implication. Unrestricted pointwise positivity can be larger than bilinear SOS; nonlinear/output-coupled/nonlocal flows are not excluded. Multiplier-SOS and joint-plane explorations produced no exact positive or negative results and remain numerical. Twelve local searches each for actual heat dissipation and Jensen energy, using eight compatible Fourier modes and analytically eliminated background, found no negative witness. Their best sampled values were 4 and 1.04694 at unit gradient L2 norm; these are not lower bounds. Finite differences checked the implemented gradients, and 9×9 versus 17×17 quadratures agree at `1.6e-14`. F's polyconvexity is not claimed either way; sampled determinant-support tests established neither outcome.

The heat strategy is already in [Bruno–Pasqualotto, §§2–3](https://arxiv.org/html/2608.06367v1), whose theorem covers the left-and-right rotationally invariant quartic class. Calderón's [binary biquadratic SOS theorem](https://www.sciencedirect.com/science/article/pii/0024379573900529) is prior machinery. The new object is the particular exact obstruction to the proposed larger bridge. Modern [polyconvex moment/SOS hierarchies](https://arxiv.org/html/2604.11124v1) are a stronger ordinary baseline than merely testing convexity; no claim that my finite searches dominate them is justified.

## What Astra enabled, the informed alternative, and the decisive obstacle

Astra supplied concrete mathematical interfaces: the acoustic/compatible-jet maps made a full-cone short-bridge hypothesis falsifiable by a portable rational object. In the changed physical route it supplied the degenerate-dissipation residual theorem, thermodynamic second-moment transfer and decision-error jets. These allow the edgewise repair to feed into an observable/regret certificate without solving a global population Poisson equation or assuming a mixing gap.

Equally informed alternatives can use the same model and assay: weighted-flow/Hodge methods, modern tensor-network transport calculations, primal-adjoint output estimation, interval arithmetic, optimal experimental design and local Hamiltonian/process tomography. None is ruled out here. [Han–Hartnoll](https://arxiv.org/html/1806.01859v2) already connects dissipative transport bounds to microscopic and local non-transport information. [Chuang–Nielsen](https://arxiv.org/abs/quant-ph/9610001) supplies the basic process-tomography framework. N765 credits established goal-oriented estimation. Novelty of the particular retargeting-to-macroscopic-regret composition has not been cleared, and practical superiority is not established.

The decisive remaining work is concrete. An actual useful target needs a physically warranted finite-range real hopping/noise class, sufficiently informative and affordable simultaneous coefficient intervals, and a finite nominal response witness whose robust full-control-cell residuals certify a meaningful decision. The final fixed-box continuation below certifies a common control with small global regret for the enlarged correlated-hopping class. It uses supplied finite source witnesses and does not establish affordable physical acquisition or uniformly economical witness construction across the broader class. General polynomial witness closure, finite-temperature/nonunital extension and quantitative full hydrodynamics remain separate problems.

The completed results are an exact audited failure of one foundational bridge, a constructive local repair of an off-diagonal model-error bottleneck, and an explicitly paid acquisition route with an unfavorable conservative cost control. They do not establish a civilisation-changing capability or a proof that one is now close.

## Continuation: current noise-profile comparator

The full author preprint of [Lawrence–Wang–Segal](https://arxiv.org/html/2604.23005v1), §§II–III, uses a single-particle tight-binding chain, finite extraction/reinjection flux, and separately controlled site dephasing. It optimizes log rates within `[1e-7,1]` using JAX/Adamax; ramp cases use 100 starts, disordered cases 500 landscapes, and runs stop by gradients, boundaries or 100,000 steps. Global maximality is not generally certified. Its main longer-chain examples have 12 sites. The [publisher](https://journals.aps.org/prb/abstract/10.1103/2h1t-vbqc) confirms the July 2026 publication.

This is a relevant informed optimization baseline and receiver for certificate ideas. It does not compute the interacting, all-charge-sector thermodynamic second-moment coefficient used here. Conversely, its extra local noise controls, finite single-particle solve and calibrated site data cannot be silently imported as free access. Broad noise-profile optimization and noise-assisted transport are not claimed as new. The ensuing test uses source witnesses to certify an actual interacting macroscopic decision over a nonzero conditional-hopping box; it does not substitute the paper's finite single-particle target.

## A nonzero-uncertainty interacting thermodynamic decision

The retargeting operation now has a quantitative construction beyond the preliminary finite controls. Reuse the explicit exact N765 footprint-eight witnesses at `V=3/2` and `V=0`, with `U=4,d=2`. Let the **four independent unknown amplitudes**, conditioned on `(n_(i-1),n_(i+2))`, lie in `[1-epsilon,1+epsilon]`. These are actual conditional hoppings in the many-body Hamiltonian, not a single-particle replacement or a supplied response coefficient.

`transport/robust_decision.py` imports no source compiler or optimizer. It expands the reflection-paired source fields into ordinary translation-orbit Pauli words, regenerates every commutator output, and exactly reproduces both source nominal endpoint values. It also checks all 20 population-block identities required by the parameter-family repair, using integer coefficients and their actual denominators.

A sharper identity makes the transfer useful: `⟨J_a,f_a⟩=⟨J0,f0⟩` exactly. Amplitude and inverse-amplitude factors cancel on every current-supported coherence. For `rho=epsilon/(1-epsilon)`, set

`c10=sum_sigma ||Q A0 E_sigma f0||_(S+)`,

`c01=sum_sigma ||Q A_sigma f0||_(S+)`,

`c11=sum_(sigma,tau) ||Q A_sigma E_tau f0||_(S+)`,

`b=rho*c10+epsilon*c01+epsilon*rho*c11`, `Q=I-P`.

The exact population identities are

`P A0 E_sigma f0=P A_sigma f0`,

`P A_sigma E_tau f0=1_(sigma=tau) P A0 E_tau f0`.

Their total coefficient is `r_sigma+e_sigma+e_sigma*r_sigma=0`. Consequently `||A_a f_a-A0f0||_(S+)<=b`, with no discarded imbalance. Orthogonality of edge/environment sectors gives the S penalty

`pS=[(1-epsilon)^(-2)-1]||E_edge f0||_S²`.

The inherited lower bound therefore gives

`D_a(3/2)>=D0_low-4[pS+2||A0f0||_(S+) b+b²]`.

For the fixed even witness at `V=0`, put `r0=J0-A0g0` and `cU=1/2+sum_sigma||A_sigma g0||_(S+)`. Since `||delta J||_(S+)<=epsilon/2` at `d=2`,

`D_a(0)<=D0_upper+4[2||r0||_(S+) epsilon*cU+(epsilon*cU)²]`.

All squared norms are exact rational sums; square roots are rounded upward as rational dyadics. At **epsilon=1/100**, safe outward decimals are

**`D_a(3/2)>=0.552042800224893174`,**

**`D_a(0)<=0.524990652212544690`,**

**`D_a(3/2)-D_a(0)>=0.027052148012348484`.**

These hold uniformly over the entire four-amplitude box for the actual thermodynamic second-moment coefficient, using the inherited transfer plus the audited model extension. A conservative analytic footprint bound also gives the same finite-response comparison for all rings `n>=27`; the regenerated fields have a smaller measured footprint. Exact fractions and input provenance are in `transport/ROBUST_INTERACTING_DECISION.json`. The helper's analytic and independent rational endpoint audit is `helper/robust_interacting_decision_audit.md`. It did not independently duplicate the principal's commutator regeneration; that verification scope is explicit.

The source witnesses are paid supplied mathematical artifacts, with 3,088/3,024 basis rows at each action. The new two-action compiler ran in roughly two seconds on these supplied fields; this is not a fresh inverse-construction or physical-acquisition benchmark. The repaired bounds allow the old source's enlarged even-X/Y sector: exact U(1) neutrality of every rounded trial is unnecessary, and the physical current/exact solution remain neutral. Actual S rates are retained.

To connect measurements to this box, the assay must return simultaneous intervals contained in `[0.99,1.01]`; otherwise this particular certificate is inconclusive or must be recomputed for the returned box. A confidence interval is not replaced by its midpoint. Finer assay radius, systematic-error reservation and source-class validation remain charged. The large conservative tomography count above is not an affordability result.

This two-control comparison is a constructive test of the uncertainty bridge, not the invention destination or a global optimum. The strongest inherited near-optimal control is much harder to distinguish from its previous neighbor; the ensuing correlated-jet test addresses that comparator rather than declaring success against a coarse control.

## Final fixed-box global certificate

At the single fixed box `a_sigma in [0.9999,1.0001]` for all four conditional hopping amplitudes, `U=4,d=2`, the common control **`V_c=1109/512` has global regret `<7.432e-6` over every `V in [0,3]`**. This is the actual interacting infinite-chain second-moment coefficient under the stated structural contract. A conservative full-footprint argument also covers finite periodic responses for `n>=47`.

The comparison to the previous informed near-optimal control is strictly resolved:

`D_a(1109/512)-D_a(71/32)>6.6398e-5`.

Larger-box rows with negative lower bounds are preserved as inconclusive certificate outcomes, not claims that physical improvement reverses. No more box refinement was undertaken.

The corrected-output perturbation follows from invariant current pairing and S/S+ Cauchy bounds. Its first and second derivatives have factors eight:

`|delta Dhat'|<=8m2 EF0 EF1+8(bA1 G0+bA0 G1)`,

`|delta Dhat''|<=8m2(EF2 EF0+EF1²)+8(bA2 G0+2bA1 G1+bA0 G2)`.

Here `m2=(1-epsilon)^(-2)-1`; all edge/witness norms and complete residual derivatives are uniformly enclosed. Order two includes the `2 A1 delta f^(1)` term. The central nominal/perturbation compiler checks 84 exact population identities and reproduces the exact source lower endpoint. The final residual order is retained.

Actual curvature is at most `-mu` on `[31/16,39/16]`, with `mu>0.065463115805586552114`. Uniform triangle bounds use radius `139/512`, covering both sides of the center. The chosen gradient is at most `0.000986417746969308826`. Seven upper witnesses exclude the outside domain: their exact convex quadratics bound whole rational cells by endpoints, with the hopping perturbation envelope added. **640 cells cover the entire complement**, not sampled centers. The outside-exclusion gap exceeds `0.001132260088125853605`. Every global maximizer is therefore inside the strictly concave interval and is unique. Strong concavity yields the rational regret bound `gradient_bound²/(2mu)`, safely at most **`0.000007431818357269293`**.

Authoritative artifacts are `transport/GLOBAL_ROBUST_HOPPING_CERTIFICATE.json`, `transport/CENTRAL_HOPPING_NORM_BOUNDS.json`, and `transport/GLOBAL_HOPPING_UPPER_ANCHORS.json`. `transport/verify_global_upper_polynomials.py` independently regenerated all three coefficients of all seven source upper quadratics; every coefficient matched exactly (`GLOBAL_UPPER_POLYNOMIAL_REPLAY.json`). The helper independently recomputed the central derivative formulas, five source residual-square bounds, all seven anchor polynomials, all 640 continuous-cell choices, exact coverage, curvature, exclusion and final regret with no principal-module imports and no overlapping Pauli regeneration. Its machine record is `helper/GLOBAL_HOPPING_INDEPENDENT_CHECK.json`; the final written audit `helper/correlated_global_transport_audit.md` retains its actual scope.

Central norm regeneration took about 214 seconds; an earlier near-optimal-only calculation took about 195 seconds and remains paid exploratory work. Upper-anchor perturbation regeneration took about 54 seconds. Source witnesses, their original construction/acquisition, all earlier exploration and physical calibration are additional inputs/costs. These times are not a fresh inverse solve from observations or a superiority benchmark. The supplied central fields have 53,088/53,024 basis rows per jet; finite-cost reuse of these valuable inputs is what this construction demonstrates.

