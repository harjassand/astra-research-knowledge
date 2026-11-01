# Independent audit: energy-injection jump-count exponential tail

**Verdict:** The ordinary operator/positive-evolution proof is valid under the explicitly normalized actual-generator assumptions, with the recordwise control and count-accounting qualifications below. It proves a conditional theorem for specified actual counting channels, not a hardware/dilation construction, coherent simulation algorithm, thermodynamic work theorem, or all-selected-location fault admission. No novelty conclusion follows.

## 1. Source binding and scope

- Original requested source: `centered_mixing_fault_admission_20261031/ENERGY_JUMP_MGF_ROOT_CANDIDATE.md`, SHA-256 `bc401a320c086bdd0bd32e4de0293343962639dab41142223f008ddbfe4f540e`.
- Immutable local copy: `SOURCE_FROZEN.md` (read-only).
- Clarified source independently reread: SHA-256 `f77cadc6f3c55af024c11f6cff1938ada088878f7804505e55a38be802008d50`; immutable copy `SOURCE_CLARIFIED_FROZEN.md`.
- The clarification explicitly supplies `L = lambda(G tensor id) - i[sqrt(lambda)V+K(t), .]`, `[K(t),H]=0`, counted channels `sqrt(lambda)L_j`, deterministic history-uniform C(t), and instrument contraction for every prior record. These repair ambiguity, not the algebra.
- This audit does not edit root sources. Final root files were subsequently read and hash-verified; see section 10 for the binding and acceptance of all three files. Section 8 was first checked from the supplied formulas and then checked against the frozen extension file.

The proof needs well-defined bounded finite-dimensional joint generators (or separately justified infinite-dimensional domain/propagation hypotheses). An arbitrarily large finite quantum data system, with arbitrary initial correlations, is permitted. A genuinely infinite-dimensional/unbounded-control data extension is not established merely by saying “arbitrary data.”

## 2. Operator proof, independently reconstructed

Set `J*(X)=sum_j L_j^* X L_j`, `q=e^s-1`, `a=4q/(kappa-4hq)`, `W=I+aH`, and `r=2aC^2/kappa`. Here `q>=0` and `4hq<kappa` imply `a,r>=0` and `W>=I`.

1. `J*(W) <= (1+ah) J*(I) = 2(1+ah)H`, by positivity and `W <= (1+ah)I`. This is a complete joint-system operator inequality: the source inequalities tensor with identity on the data.
2. For any joint density matrix rho, Hilbert–Schmidt Cauchy–Schwarz applied to `sqrt(H)V sqrt(rho)` and `sqrt(H)sqrt(rho)` gives `|Tr(VH rho)| <= C sqrt(Tr(Hrho))`. Its adjoint term has the same bound, so `|Tr(i[V,H]rho)| <= 2C sqrt(E)` without product-state assumptions.
3. Young's inequality gives `2a sqrt(lambda) C sqrt(E) <= lambda a kappa E/2 + 2a C^2/kappa`. Since this holds for all joint density matrices, it implies the claimed Loewner-order commutator bound. Signs of the adjoint Hamiltonian term are correct for the stated Schrödinger generator.
4. `L_s^*W <= lambda[-a kappa/2+2q(1+ah)]H+rI = rI <= rW`. The cancellation is exact algebraically.
5. The tilted generator has positive weights on all jump terms and the original no-jump propagator, hence its Dyson expansion is completely positive, though not trace preserving. If `rho_s(t)` is its positive, unnormalized tilted state, then `w(t)=Tr(W rho_s(t))` satisfies `w'(t)<=r w(t)`. Also `Tr(rho_s(T))=E[e^{sN_T}]<=w(T)`. Gronwall yields `(1+aE0)e^{rT}`.

This forward weighted-state argument also avoids any ambiguity about time ordering in a nonautonomous adjoint comparison. `E[e^{sN_T}W_T]` should be understood as the scalar trajectory expectation of the terminal state's W expectation, not as an unspecified quantum random operator.

No reset, stationarity, product initial state, or adiabatic elimination is used. Retaining the full tilted propagator includes all no-jump histories.

## 3. Controls, instruments, and full-history costs

For record-adaptive controls, each prior record must admit the same operator inequalities, with a deterministic envelope `C(t)>=||sqrt(H)V_record(t)||`. Then replace `rT` by `int 2a C(t)^2/kappa dt`. A path-dependent random integral cannot simply be pulled outside expectation unless a deterministic bound or an appropriately weighted supermartingale formulation is supplied.

An intervention with outcome maps Phi_o may be inserted if, for each prior record, `sum_o Phi_o^*(W)<=W`. Summing the **unnormalized** branches then preserves the comparison. Future branchwise generators must obey the uniform hypotheses. Postselecting a favorable outcome and renormalizing is not covered by the unconditioned bound; a conditional bound must pay its conditioning probability. Assume causal, well-defined, non-Zeno interventions or justify their limiting propagation separately.

**Count-accounting qualification:** the displayed aggregate W contraction is for interventions that add no counted emissions. If an intervention itself emits photons/clicks included in N, it needs a count-tilted instrument inequality, e.g. `sum_o e^{s n_o} Phi_o^*(W)<=W`, or a separately charged factor. A cooling/reset map can contract W while producing many physical photons. Its unweighted map does not make those photons free.

Initial source preparation contributes E0; subsequent drives contribute their full exposure integrals. Waiting, switching, readout, and failed/retried operations during which admitted coupling remains active must be included. Detector/control/reset errors and engineering overhead are not bounded by this count certificate unless separately modeled. For backward time-window weights (section 8), past exposure is paid at its propagated influence rather than simply discarded.

## 4. Finite tilt and derivative

At zero tilt the two sides both equal one. Taking the right derivative is legitimate in the finite bounded model and gives

`E N_T <= 4E0/kappa + 8 C^2 T/kappa^2`.

For time-varying C, replace `C^2T` by its integral. The zeroth-order equality is necessary for differentiating an upper bound in this way; it holds here.

The condition `4h(e^s-1)<kappa` is a sufficient domain for this particular lambda-uniform Lyapunov certificate, not the actual finite-model MGF domain. Since the conditional total specified jump intensity is at most `2lambda h`, the ordinary bounded-intensity argument gives, for every finite s>=0,

`E e^{sN_T} <= exp(2lambda h T (e^s-1))`.

One can take the minimum of applicable bounds. Unlike the energy-flow estimate, that Poisson envelope grows with lambda. Section 8 also sharpens the Lyapunov tilt range without changing the zero-tilt constants.

## 5. Actual-count and thinning semantics

The count depends on the specified physical instrument/unravelling. An abstract GKLS representation is not evidence that its jump record is observed in a device; other representations or displaced detection schemes can give different counts for the same unconditional master equation. The theorem applies once the actual counted channels and any approximation error are established.

For ordinary non-disturbing independent marking, split each physical channel into missed and detected maps `eta J_j` and `(1-eta)J_j`. Tilting only missed marks replaces q by eta q. If outcomes trigger feedback, use this local branchwise marked-generator argument; the eventual M conditional on the eventual total N need not be binomial, because feedback can change future N.

A sufficient operator form for history-dependent thinning is: on every record, the actual missed jump CP maps M_j satisfy `sum_j M_j^*(I)<=2eta H`, the aggregate unmarked physical generator remains admitted, and missed post-jump/control effects obey the admitted W bound. Since `W<=(1+ah)I`, this implies `sum_j M_j^*(W)<=2eta(1+ah)H`, the exact estimate needed by the proof. The familiar scalar split `M_j=eta_{j,record}J_j`, with `0<=eta_{j,record}<=eta`, is sufficient. An average detector efficiency for a preferred input is insufficient. Dead time can have conditional miss probability one.

## 6. Structural scope and no all-selected overclaim

In finite dimension, every stationary source state sigma satisfies `0=Tr(G^*H sigma)<=-kappa Tr(Hsigma)`, hence is supported in ker H. Each counted L_j annihilates that support. If the source has a faithful stationary state, the hypotheses force H=0 and all counted jumps to vanish. Thus the nontrivial certificate concerns a dark/draining source driven externally, not generic stationary thermal emission.

Also H is, from these hypotheses alone, a positive Lyapunov/activity observable proportional to jump intensity. Identifying it with actual thermodynamic energy, and C^2 exposure with work or joule cost, needs additional physics.

A total-count tail does not assign fault locations or prove local stochastic noise. Even source-local independent damping does not license multiplication of marginal probabilities for correlated warm initial states. For m sources, start in `(1-p)|0...0><0...0| + p|1...1><1...1|`, with no drive. Then

`P(each source emits by T)=p(1-e^{-2h lambda T})^m`,

whereas the product of marginal probabilities is `p^m(1-e^{-2h lambda T})^m`. For m=4,p=.02,h=.8,lambda T=10 these are approximately .019999991 and 1.5999993e-7. The proposed initial product-W expectation retains exactly the correlations that a product of means would lose. Shared physical events affecting multiple data patches and clustered cascades require further receiving hypotheses.

## 7. Numerical corroboration, not exact arithmetic certification

`check_tilted.py` / `check_tilted.json` use NumPy/SciPy double-precision matrix exponentials and Hermitian eigensolvers. They are **numerical finite-matrix checks**, not interval/rational certificates, Monte Carlo hardware evidence, or substitutes for section 2.

Model: TLS damping with `H=.8|1><1|`, `L=sqrt(1.6)|0><1|`, `kappa=1.6`; source tensor a qubit data system; entangled Bell and random correlated initial states; random Hermitian joint couplings. Across 720 cases with lambda=.1,1,20 and q=.05,.15,.35,.49:

- No numerical MGF or operator-inequality violation.
- Largest MGF/bound ratio: .9735177801.
- Largest eigenvalue of `L_s^*W-rW`: -.00079509196.
- Analytic no-drive Bernoulli MGF versus matrix propagation discrepancy <=8.9e-16.
- Explicit data instrument and outcome-adaptive future drive: MGF 1.17545877 <=2.53726254.
- Record-dependent thinning bounded by eta=.3: MGF 1.05169205 <=1.15347475.
- Augmented moment-generator mean: .48005919 <=1.13139480.

`check_backward.py` / `check_backward.json` additionally corroborate the terminal-zero time-window and optimized-split formulas. A q=.8 counted window exceeds the original stationary threshold .5, yet its finite-horizon backward certificate gives 1.05237394<=1.27271979. This has no lambda-uniform claim. All postwindow backward weights are zero. Optimized-split tests q=.1,.49,.7,.95 satisfy the expected numerical inequalities.

## 8. Separately earned extensions from root proposals

### 8.1 Optimized Young split

For `0<theta<1`, use `delta=theta kappa` in Young's inequality. If `D=kappa(1-theta)-2hq>0`, set

`a=2q/D`, `r=a C^2/(theta kappa)`.

The same coefficient cancellation proves the same MGF bound. Taking `g=kappa-2hq>0`, `theta=g/(2kappa)` yields

`a=4q/g`, `r=8q C^2/g^2`, valid for `q<kappa/(2h)`.

These algebraic formulas check; they improve both displayed coefficients relative to the half-split choice, but optimize the asymptotic rate r rather than necessarily the entire initial-prefactor-plus-time objective. Their zero-tilt derivatives are unchanged. This is an ordinary parameter optimization, not a novelty claim.

### 8.2 Backward counted-window weight

Let q(t)>=0 be a bounded deterministic counting tilt (e.g. nonzero only on selected time windows), and solve

`a'(t)=lambda[(kappa/2-2h q(t))a(t)-2q(t)]`, `a(T)=0`.

The explicit solution is

`a(t)=2lambda int_t^T q(u) exp{-lambda int_t^u[kappa/2-2h q(v)]dv} du >=0`.

With `W_t=I+a(t)H`, `r(t)=2a(t)C(t)^2/kappa`, direct substitution gives

`partial_t W_t + L_{q(t)}^*W_t <= r(t)I <= r(t)W_t`.

The resulting bound is

`E exp(int_0^T s(t)dN_t) <= [1+a(0)E0] exp(int_0^T r(t)dt)`,

where q(t)=exp(s(t))-1. The finite-horizon solution exists for bounded q even beyond the steady-state threshold, but can grow exponentially in lambda. Before a counted window, uncounted driving remains charged through a(t); after the final counted window, a(t)=0. Instrument conditions use the current W_t and still require count-tilted treatment if the instrument itself adds counted events.

### 8.3 Product weights, strictly source-local model

Suppose the FULL actual generator decomposes into source-local G_i and interactions V_i each commuting with all H_j, j!=i, with no shared-bath/cross-source term unless separately verified. Shared quantum data and initial correlations are allowed. Let `W_i(t)=I+a_i(t)H_i`, and use each local backward or static inequality. Because all other W_j commute with the i-th generator's operators,

`(partial_t+L_{q}^*) prod_i W_i <= sum_i r_i prod_{j!=i}W_j <= (sum_i r_i) prod_i W_i`.

Thus the multivariate MGF is bounded by

`Tr[(prod_i W_i(0))rho0] exp(int sum_i r_i dt)`.

For adaptive instruments, the needed contraction is for the **product W**, not merely each marginal W_i separately. Marginal contraction does not imply joint/product contraction. Do not factor the initial expectation absent an appropriate state condition. This is a valid multivariate count certificate under stronger locality assumptions, but not yet the fault-location theorem or error-suppression scaling needed by a receiving algorithm.

## 9. Prior-art placement (bounded primary-source pass)

The directly relevant prior located and inspected is Girotti, Garrahan and Guţă, *Concentration Inequalities for Output Statistics of Quantum Markov Processes*, Ann. Henri Poincaré 24 (2023), section 4/Theorem 6. It explicitly uses the quantum-count MGF identity with tilted generator `L+(e^u-1)J` and proves finite-time concentration using spectral/perturbative methods. Its continuous-time setup assumes a unique faithful stationary state. Those hypotheses differ from this supplied draining-energy inequality; the common tilted-generator machinery must be credited. [Primary paper](https://link.springer.com/article/10.1007/s00023-023-01286-1).

Earlier relevant work is Benoist, Hänggli and Rouzé, *Deviation bounds and concentration inequalities for quantum noises*, Quantum 6, 772 (2022), which gives finite-time deviation bounds via noncommutative Dirichlet forms and functional inequalities. This pass verified the primary journal abstract and its identification by the 2023 paper, not every theorem's applicability to the present singular-dark-source setup. [Primary journal page](https://quantum-journal.org/papers/q-2022-08-04-772/).

Garrahan and Lesanovsky's *Thermodynamics of Quantum Jump Trajectories* (2010) is established quantum-jump large-deviation background, including driven TLS photon trajectories. [Primary paper/preprint record](https://arxiv.org/abs/0911.0556).

This bounded search did not establish that the exact elementary Foster/Lyapunov specialization is new. No novelty clearance, exhaustive literature search, or hardware comparison is claimed. No denied source transfer was retried; no external agent, equipment, outreach, publication, purchase, or restricted-path read occurred.


## 10. Final frozen-source acceptance

The following three root files were read in full, their hashes independently verified, and immutable local copies made:

1. `ENERGY_JUMP_MGF_ROOT_CANDIDATE.md`: `cfb6610fbba434d955ba965aaaf5ab52d9e9444c31bb031d7be68d22c014ff39`; local `SOURCE_FINAL_BASIC_FROZEN.md`. **Accepted as the conditional specified-count theorem.** It correctly incorporates explicit generator normalization, recordwise envelopes, uncounted versus counted interventions, local detector marking under feedback, the ordinary all-s intensity envelope, and the distinction from thermodynamic energy/work.
2. `ENERGY_JUMP_MGF_EXTENSIONS_ROOT.md`: `3a064c7e14fc47d92be71634670dc46bf96acfc4c5f5dc620faf173a904dcfd7`; local `SOURCE_EXTENSIONS_FROZEN.md`. **Accepted under its stated full source-local decomposition and whole-product instrument hypotheses.** Section 8 gives the independently reconstructed proof. Its joint-dark initialization factor equals one even with arbitrary data entanglement; no factorization of warm source expectations is allowed.
3. `ENERGY_BURST_OBSTRUCTION_ROOT.md`: `31a5a85a6cd9354368a50e4e23a8ed7bf05700fdb04e0a712a706c7efa3e7733`; local `SOURCE_BURST_FROZEN.md`. **Its burst inequality and no-Poisson-domination consequence are accepted.** One wording correction was requested: “valid finite-dimensional Markov dilation” should mean a finite-dimensional source with a standard formal monitored Markov dilation, not a claim of an exact all-time finite-bath unitary implementation or acquired physical detector. Section 11 audits the actual argument.

These acceptances do not remove the assumptions and receiving/implementation boundaries listed above. No numerical result is used as the logical premise of acceptance.

## 11. Independent check of the cold three-level burst obstruction

For `H=diag(0,1,2)`, `L1=sqrt(2)|0><1|`, `L2=2|1><2|`, and `V=g(|2><0|+|0><2|)`:

- Direct multiplication gives `sum L_j^*L_j=2H`, `G^*H=-2H`, and `||sqrt(H)V||=sqrt(2)g`. The initially dark state has E0=0.
- No-jump evolution has amplitudes `a|0>-i x|2>` with `a'=-gx`, `x'=ga-2x`. Until a first falls to 1/2, x>=0, a<=1, and `x(t)<=gt`, so `a(t)>=1-g^2t^2/2`. For 0<g<=1 this prevents a crossing below 1/2 before t=1 and gives a>=1/2 through the closed interval.
- Therefore `x(t)=g int_0^t e^{-2(t-u)}a(u)du >=g(1-e^{-2t})/4`. Only L2 can be the first count while this no-jump state is present; its density is `4x(t)^2`.
- On t in [1/2,1], this density is at least `g^2(1-e^{-1})^2/4`. The first count leaves the normalized state exactly |1>. V is zero on |1>, and the next jump has waiting distribution Exp(2). At least one time unit remains before T=2, so its success probability is at least `1-e^{-2}`.
- Integrating over the half-unit first-jump window gives exactly `P(N_2>=2)>=g^2(1-e^{-1})^2(1-e^{-2})/8`.

Since C^2=2g^2, a Poisson dominating count with mean `K C^2 T=4Kg^2` at T=2 would have two-count tail O(g^4), contradicting the proved Omega(g^2) lower bound as g tends to zero for every fixed K. The obstruction is stronger than warm common-cause correlation because it starts dark, but it still is **not** a logical-error floor. Observed/corrected emissions, cancelling parity, or one receiver window may neutralize it.

`check_burst.py` / `check_burst.json` propagate separate zero-count, one-count, and at-least-two-count density blocks with floating-point matrix exponentials. The lower-bound coefficient is numerically .04318745194. At g=.001 the computed two-count probability is 8.4166171e-7, compared with the lower bound 4.3187452e-8. Across g=.001,.003,.01,.1,.5,1, all inequalities and total-probability checks pass numerically. This corroborates, but does not replace, the analytic derivation above.


## 12. Closed correction receipt and final three-source verdict

The burst wording correction was inspected as a diff and verified to leave all equations and the mathematical argument unchanged. The corrected final file states explicitly that the source is finite-dimensional, that its monitored Markov dilation is formal, and that this does not claim an exact finite-bath implementation or an acquired physical detector. Its immutable copy is `SOURCE_FINAL_BURST_FROZEN.md`.

**Final accepted source hashes (all independently rechecked together):**

| Root file | SHA-256 | Verdict |
|---|---|---|
| ENERGY_JUMP_MGF_ROOT_CANDIDATE.md | cfb6610fbba434d955ba965aaaf5ab52d9e9444c31bb031d7be68d22c014ff39 | Conditional actual-specified-count MGF theorem accepted |
| ENERGY_JUMP_MGF_EXTENSIONS_ROOT.md | 3a064c7e14fc47d92be71634670dc46bf96acfc4c5f5dc620faf173a904dcfd7 | Optimized-split, backward-window, and source-local product extensions accepted under stated premises |
| ENERGY_BURST_OBSTRUCTION_ROOT.md | 1c68a072b576ac766ad0b0e9c6eb521fe6340297ec57ea9f3d114082e26e4c0f | Cold-source two-count obstruction and precise no-low-rate-Poisson consequence accepted |

No requested proof check remains blocked or pending. Main acceptance evidence is the independent analytic operator/trajectory reconstruction, with floating-point checks only corroborative. Physical actual-channel realization, approximate-model error, algorithmic consumer construction, thermodynamic work, all-selected logical-fault admission, and novelty remain outside these accepted results, not secretly completed by them. No denied actions or uncertain external mutations occurred.
