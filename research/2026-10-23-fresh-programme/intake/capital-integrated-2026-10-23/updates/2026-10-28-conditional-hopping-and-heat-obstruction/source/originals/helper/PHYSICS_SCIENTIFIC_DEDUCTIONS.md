## 1. Acquired equilibrium-response sensing

### What Astra contributes

Route **N712-local-readout-thermal-information-loss-and-variance-certificate** gives a useful structural change: bound the *difference* between covariances rather than the long-range covariance itself. For

`H(h) = H_bg + sum_a h_a P_a`,

canonical nonidentity Pauli dictionary support at most `k`, candidate incidence at most `Delta`, full Hamiltonian interaction support at most `ell`, per-site incident operator norm at most `g`, and a full-rank unrestricted Gibbs state at known `beta`, use parameter-independent uniformly randomized single-qubit Pauli readout. Independently calibrated sign noise has visibility at least `eta > 0` and is independent across sites and copies. Quantum outcome correlations can be arbitrary.

If `C` is BKM covariance, `V` the covariance of the corrected local shadow features, and

`nu = [1+k(Delta-1)] [(3/eta^2)^k-1] + beta*g*k*(k+ell)*Delta/3`,

then the source proves

`0 <= V-C <= nu I`,

`beta^2 C(C+nu I)^(-1) C <= F_M <= F_Q <= beta^2 C`,

`0 <= F_Q-F_M <= beta^2 nu I`.

Consequently any direction with `u^T F_Q u / ||u||_2^2 -> infinity`, at fixed local bounds and temperature, is asymptotically completely readable by the fixed product detector. A scalar statistic suffices. With `f=u.Y`, `V_u=Var(f)`, and `a=nu ||u||_2^2`, the record-only certificate is

`beta^2 (V_u-a)_+^2/V_u <= F_mom <= u^T F_M u <= u^T F_Q u <= beta^2 V_u`.

This does not require a partition function or complete background Hamiltonian. It *does* require the Gibbs-family and locality/strength premises and detector calibration.

### Exact governing passages

All paths below are relative to the pinned published root.

Source **src-EC-n712-4952291bbb26**:
`updates/EC/package/local_readout_information/recovered/astra_local_readout/local_readout_information.tex`.

- Lines 64–83: parameter dictionary and full Hamiltonian assumptions; “There is no lattice, clustering, commutativity, gap, or mixing-time hypothesis.”
- Lines 93–107: precise product POVM, independent-noise correction, and explicit acknowledgement that the measurement primitive is established shadow methodology.
- Lines 125–160: independent main theorem and constants.
- Lines 162–201: the measurement covariance defect vanishes between disjoint supports; this is why long-range correlations cancel in the *difference*.
- Lines 203–279: Brooks–Harris inequality and the coefficient-space double-commutator bound.
- Lines 281–327: score Schur complement and noncommuting matrix identity completing the information bound.
- Lines 338–391: enhanced-direction consequence and local estimator; “Calibration acquisition and a neighborhood in which a linear approximation is accurate must be paid for.”
- Lines 393–448: variance-only certificate, finite-copy confidence interval, explicit arithmetic/readout/independent-Gibbs-copy costs.
- Lines 498–528: a common detector flip destroys the additive information-loss claim despite positive marginal visibility.
- Lines 554–583: finite displacement, nuisance fitting, generic preparation and physical speedup remain separate obligations.

The current packet status is `source_derived_unreviewed`. Notice **SN-EC-N711-N712-INDEPENDENT-READOUT-CONDITIONAL-COROLLARY** says that the main additive theorem is independent of N711; only the all-directions constant-factor corollary imports N711's covariance floor, and only in its dictionary-only Hamiltonian scope. I do not import that corollary.

### Completed scoped proof reconstruction in this helper

I reconstructed the independent finite-dimensional chain at the cited version: unbiased product features; the positive-operator covariance defect; overlap row bounds; the spectral Brooks–Harris inequality with its `beta/12` factor; both row and column sums in the double-commutator estimate; thermal differentiation; the moment-score Schur complement; and

`C(C+R)^(-1)C - (C-R) = R(C+R)^(-1)R >= 0`.

I found no gap in that chain under the exact stated assumptions. I also reconstructed the scalar variance certificate and its paired Hoeffding confidence bound. This is an actual single-helper derivation check of those statements, not code replay, a review of N711, a novelty clearance, or physical validation. The correlated-detector limitation is substantive and preserved.

### Fresh connecting result A: approximate state preparation does not certify sensing derivatives

A preparation error bound at one operating point cannot establish the physically acquired Fisher information, even if its trace-distance error is zero at that point. Let the ideal smooth family be `rho_t`, with positive ideal directional information at `t0`. A preparation map that outputs `rho_t0` throughout a sufficiently small neighborhood has zero derivative and zero acquired information there, while remaining arbitrarily close to `rho_t` throughout that neighborhood. A smooth plateau and cutoff can make the approximation uniformly epsilon-close on a larger parameter interval while keeping zero derivative at `t0`.

Thus even a uniform finite epsilon approximation to the state family, by itself, does not justify a *local* Fisher lower bound. A genuine acquisition contract must control the relevant response derivative, or switch the theorem to a finite-displacement decision/risk target at an explicitly charged resolution. This is not repaired by a source hash, high state fidelity, or many repetitions.

There is a useful but weaker robustness statement. If the actual common output law `Q` has total variation at most epsilon from the ideal operating-point law `P`, and `|f|<=L`, then

`|Var_Q(f)-Var_P(f)| <= 4 L^2 epsilon`.

Proof: `Var(f)=min_c E[(f-c)^2]`; both minimizing means lie in `[-L,L]`, and the squared loss lies in `[0,4L^2]`. Bound its expectation difference by its range times TV, in both directions. Therefore the ideal variance interval can be widened by `4L^2 epsilon`. This certifies the *ideal* Fisher interval only. It still does not certify the actual parameter derivative.

For `L=O(n)` and an ideal enhanced variance `Theta(n^(1+alpha))`, a small relative variance bias requires `epsilon=o(n^(alpha-1))`. This explicitly exposes a preparation-accuracy cost that the record-only certificate does not acquire.

### Fresh connecting result B: a full-cycle obstruction for ordinary reversible local refresh

Consider a classical diagonal Gibbs family `pi_t(x) proportional to exp[-beta(H0(x)+t M(x))]`, `M=sum_i x_i`, `x_i=+-1`. Suppose equilibrium refresh uses an irreducible reversible continuous-time single-spin generator, with each site's flip rate at most `gamma`. Write `L` for that generator, `V=Var_pi(M)`, and

`E(M,M) = <M_c, -L M_c>_pi`.

Every jump changes `M` by 2, so

`E(M,M) = (1/2) sum_x pi(x) sum_i c_i(x)[M(x^i)-M(x)]^2 <= 2 gamma n`.

For a stationary trajectory, the asymptotic variance of its time-averaged magnetization is

`(2/T) <M_c,(-L)^(-1)M_c>_pi`.

Spectral Cauchy–Schwarz gives

`<M_c,(-L)^(-1)M_c>_pi >= V^2/E(M,M)`.

Since `d E_pi M/dt = -beta V`, the local error-propagation information rate of this mean procedure is at most

`beta^2 V^2 / [2 <M_c,(-L)^(-1)M_c>] <= beta^2 E(M,M)/2 <= beta^2 gamma n`.

This already grants stationary preparation and noiseless readout. Superextensive per-copy equilibrium information cannot improve the scaling of this ordinary local-refresh magnetization-mean procedure per unit time. The relaxation bound `gap <= E(M,M)/V <= 2 gamma n/V` gives the same slowing-down warning.

Scope: this does not bound every path-likelihood estimator, quantum bath, nonreversible drive, nonlocal reset, coherent preparation, or dynamic metrology protocol. It blocks a tempting acquisition route; it is not a universal no-go and not a solution of the broader destination.

## 2. Acquired, model-robust macroscopic transport design

### What the corpus already supplies

**N747** develops population-balanced current witnesses for infinite one-dimensional hopping chains with arbitrary bounded finite-range real density interactions and physical on-site dephasing `d>0`, under infinite-temperature product trace. **N765** certifies the original macroscopic second-moment transport coefficient and its control derivatives by complete response residuals, without a supplied relaxation gap or normwise inverse approximation. **N768** already closes a restricted sensor-to-control chain over an uncertain `(U,d)` box. Repeating N768 as a new acquisition invention would be wrong.

At `t=1,U=4,d=2`, N765 reports a unique global optimum for `V in [0,3]` and regret below `2.978e-6` at `V=1109/512`, while its absolute transport interval is much wider. The output-specific mechanism is consequential: certify the decision error rather than first solve the whole interacting inverse to the same accuracy. The source's `86.44` comparison is a ratio of same-data certified regret bounds, not runtime speedup.

N768 allows `U in [3.9,4.1], d in [1.9,2.1]`; one local Ramsey contrast drives a control policy with source-reported regret below `4.3428e-5` at `2^20` decision shots, with greater than 99% confidence conditional on the physical/bias contract. Its optional coarse-box stage itself costs `2,097,152` shots and can return inconclusive. Preparations, reset, switching and readout are additional costs. All observations in the source are synthetic.

### Exact source routes

- **N747**: `updates/EO/package/frontier_balanced_transport/recovered/astra_frontier_balanced_transport/research_note.md`, lines 15–117 for the changed active interface; 118–243 for exact balance; 337–466 for second-moment thermodynamic transfer; 527–616 for local Ramsey access and costs. Notice **SN-EO-N742-N747-CHANGED-ACCESS-AND-OUTPUT** explicitly forbids importing a passive rare-Gibbs-copy escape.
- **N765**: `updates/EX/package/frontier_residual/recovered/astra_frontier_residual_response/research_note.md`, lines 8–31 for actual scope/cost; 33–56 for exact model and supplied physical assumptions; 66–120 for parity/balance/residual identity; 122–185 for derivative errors; 187–235 for thermodynamic transfer; 351–379 for incumbents and the still-open general output-cost theorem.
- **N768**: `updates/EY/package/frontier_decision/recovered/astra_frontier_decision_calibration/research_note.md`, lines 8–35 for outcomes; 37–65 for physical inputs; 67–122 for observation fibres and regret; 124–246 for mixed residual derivatives; 292–326 for the actual six-site preparation/switching assay; 403–438 for bias, shot and globality contracts; 492–520 for acquired coarse-box certification and costs; 553–579 for matched prior art and unresolved general constructive decision complexity.

Current packet statuses for these records are source-derived/unreviewed; N768 has selected same-implementation reruns, not an independent physical or general algorithmic validation. I reconstructed the additional bridge below, not the complete inherited thermodynamic proof or numerical packets.

### Fresh connecting result: uniform diagonal-model-error and regret transfer

Retain exactly the hopping, uniform dephasing, trace reference and translation-invariant finite-range structure of the N747 class. Let the actual diagonal Hamiltonian differ from the nominal one by

`Delta H = sum_X Delta H_X`, all real and diagonal,

with acquired per-site incident operator-norm bound

`sup_i sum_(X contains i) ||Delta H_X|| <= epsilon`.

This allows unspecified diagonal interactions beyond the fitted `U,V` form, rather than treating the nominal model as exact.

For two occupation configurations differing on `q` sites, their perturbing energy difference is at most `2 epsilon q`. Physical dephasing on the associated off-diagonal matrix element is `d q/2`. Consequently, for every positive proof regularizer lambda,

`|| (S+lambda)^(-1/2) Delta A (S+lambda)^(-1/2) || <= 4 epsilon/d`,

where `Delta A=-i[Delta H,.]`. It annihilates populations and creates no population output. Both nominal and perturbed normalized resolvents are accretive and have inverse norm at most one. The normalized current has squared per-site norm at most `t^2/(2d)`. The resolvent identity therefore gives, uniformly in ring size and lambda,

`|kappa_actual-kappa_nominal| <= 2 t^2 epsilon/d^2`.

Using `D=4 kappa` and the same finite-range diagonal-class limit,

**`sup_V |D_actual(V)-D_nominal(V)| <= 8 t^2 epsilon/d^2`.**

Thus a nominal global regret certificate `r`, valid for the data-driven selected control, transfers as

**`regret_actual <= r + 16 t^2 epsilon/d^2`.**

Use a common lower bound `d_min` when dephasing is uncertain. This is a mathematical bridge with explicit constants, not a physical acquisition or historical novelty claim. It preserves the full macroscopic observable and original physical dephasing; it does not replace them with an auxiliary rate model or Hodge energy.

The original observation-law bias must still be satisfied. Unknown diagonal interactions can also bias the Ramsey contrast. Under the source's hopping-freeze preparation, terms touching the central two sites have total norm at most `2 epsilon`, so the conservative Duhamel estimate at interrogation time `1/2` adds at most `2 epsilon` to the contrast-mean bias. Reserve this inside the declared `1e-4` budget, or regenerate the finite-shot policy certificate with the enlarged bias; reusing a table whose entire bias budget is already spent would be invalid.

This bound shows how severe the acquisition gate is: at `t=1,d_min=1.9`, merely keeping the added regret near `4e-5` needs an incident diagonal-error bound of order `1e-5`. That is a sufficient bound, not a necessary physical tolerance or a demonstrated calibration. An improved decision-correlated perturbation theorem could be substantially less conservative.

### Decisive obstacle and unchanged destination

Exact population balance is structural. A small unspecified non-diagonal Hamiltonian or nonunital/memory noise does not inherit the normalized perturbation bound: it can act on the zero-damping population sector, and `S^+` cannot charge that residual. Ordinary coefficient closeness is therefore insufficient to promote the model prediction into a robust physical controller.

The high-leverage research target is a constructive, acquisition-inclusive decision-complexity theorem: generate conservation-safe response residuals, realizable low-dimensional assays, model-error certificates and global regret bounds at controlled total cost across a consequential interacting class. The unresolved obstruction is not just finding a nice local fit; it is acquiring a sufficiently strong physical class/error contract and proving adequate residual cost. Matched comparisons must include modern tensor-network/backflow methods, ordinary optimal experimental design and Hamiltonian learning with the same raw data. The existing fixed-control comparator is insufficient for an ordinary-method superiority claim.

### Wider primary research checked

- Han and Hartnoll, **Locality Bound for Dissipative Quantum Transport**, PRL 121, 170601 (2018), [author preprint](https://arxiv.org/abs/1806.01859), [accepted manuscript](https://link.aps.org/accepted/10.1103/PhysRevLett.121.170601). It already bounds diffusivity using microscopic quantities and local nontransport measurements; that broad idea is prior art. It does not establish the specific decision-regret certificate above.
- Mendoza-Arenas et al., **Dephasing enhanced transport in nonequilibrium strongly correlated quantum systems**, PRB 87, 235130 (2013), [publisher](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.87.235130), [author preprint](https://arxiv.org/abs/1302.5629). Strong-interaction dephasing enhancement and matrix-product simulation are established. Neither noise-assisted transport nor an interacting chain alone distinguishes this opportunity.

