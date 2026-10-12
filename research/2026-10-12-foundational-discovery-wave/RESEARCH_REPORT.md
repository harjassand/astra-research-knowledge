# Foundational discovery wave — 12 October 2026

## Verdict

This wave produced four substantive families of internally derived mathematics: a controlled action-state realization for resonant interactions; an affine rare-event hardness reduction and overlap bound; an explicit nonlinear inverse-tomography barrier with a restricted constructive inverse; and a two-sided minimax law for coarse-snapshot prediction of unforced two-dimensional flow. Complete arguments, counterexamples, source comparisons and executable diagnostics are preserved below. **None has established external correctness, literature priority, a general technological advantage, or a civilisation-level discovery.** The mission's highest ambition remains unachieved.

The strongest completed mathematical target is the fluid minimax law. The most promising mechanism to investigate beyond this wave is the real sign-pair cancellation in inverse tomography. The affine overlap inequality deserves a short focused priority and algorithmic audit. The resonant representation is exact on its stated model, but a matched amplitude solver was faster; it should not be promoted as a computational breakthrough.

Several attractive claims failed under stronger comparison. Low-width affine approximation is already covered by an established automata FPRAS. Loop products in resonant stars occur in older literature. Snapshot derivative nonclosure does not imply a persistent forecast barrier. Continuum inverse uniqueness does not supply finite, stable experimental recovery. A challenge-file `sorry` was initially mistaken for a solution admission, then correctly retracted. These corrections are research outcomes, not evidence for their opposite headline claims.

All new theorem statements in this package have status **internally derived candidate, full argument written, external correctness and novelty UNKNOWN** unless a narrower status is given. “Complete” describes the written argument within its contract. It does not mean independent scientific certification or a Lean proof. Source-reported Astra and OpenAI/math claims retain their original status.

## 1. Questions worth retaining

The [selection record](SELECTION.md) separates consequence, mechanism, decisive accessibility, feasibility and external dependence. The following eight questions survive; there is no aggregate score. Their ceilings differ substantially from the value already demonstrated.

| Question and exact target | Consequence and current obstruction | Decisive route, costs and present status |
|---|---|---|
| **Q1. Operational state for controlled resonances.** For a specified nonlinear interaction network and admitted control family, characterize the equivalence relation “all future requested actions agree under every common control,” and construct a regular finite realization of that quotient. | A successful general theory could support trustworthy physical reductions. Phase information can remain relevant at vanishing shared modes even when actions and individual triad products agree. | A star model is solved internally in S1. Extend only where an acquired sensor interface beats the existing amplitude representation; arbitrary networks, economical acquisition and advantage remain open. |
| **Q2. Structured rare failure beyond graphs.** For independently retained affine equations over F2, characterize supplied representations allowing relative approximation of inconsistency, with full construction and rational costs. | Rare failures matter in coding and reliability. Bounded arity alone does not control the representation: even distinct fair ternary rows inherit a #BIS approximation barrier. | S2 proves an overlap inequality and direct witness estimator. Existing #NFA methods already handle polynomial witness trellises. Seek a strict representation or runtime advantage under matched inputs, rather than renaming that boundary. |
| **Q3. Finite experiments for unknown media and geometry.** Under calibrated boundary control, noise, energy and bandwidth budgets, determine recovery risk for a specified smooth coefficient class and a specified gauge loss. | Would distinguish mathematical uniqueness from operational scientific inference. Elliptic propagation suppresses interior high frequencies exponentially; unrestricted gauge loss adds a separate obstacle. | S3/S5 give an explicit real nonlinear pair and adaptive resource bounds, plus D scalar probes for a small known D-shell prior. Quantitative separation in a genuine boundary-fixed gauge quotient and useful nonradial positive classes remain open. |
| **Q4. Resolution, delay and precision in nonlinear flow prediction.** Determine minimax prediction error from finite observations as output bandwidth, forecast delay, viscosity and sensor precision vary. | Could guide what trustworthy simulation must measure. An unresolved initial field can affect an expanding resolved band during an increasingly short initial layer. | S4 closes the zero-forcing 2D single-snapshot law. The next substantial target is a causal sensor/delay law with matched positive recovery, then carefully stated forcing and three-dimensional extensions. |
| **Q5. Blind synthesis transfer with redox and microstructure.** Can one charge-aware model predict held-out variable-valence phase paths, including measured microstructure, better than established kinetic simulators under equal training and acquisition? | A reliable affirmative result would expand materials synthesis. Thermodynamic endpoints omit kinetic clocks, charge state and morphology. Generic synthesis kinetics is already an active demonstrated capability. | Preregister a lineage of held-out redox-active pathways, including Na0.67CoO2, against the primary simulator in A2. Needed experimental/atomistic data were not acquired. No empirical advance is claimed. |
| **Q6. Minimal physical anchoring for a causal query.** Given an input/output-equivalent dynamical family, which calibrated interventions or observations identify one specified physical causal assertion, at what precision? | Could prevent false mechanism claims from accurate predictors. Similarity transformations preserve all input/output behavior while changing state-coordinate graphs. | A3 supplies an exact two-state counterexample and a sufficient full-rank anchor. The missing theorem is query-specific rather than blanket state identification; classical realization theory is a strong baseline. |
| **Q7. Intervention transport across evolved genotypes.** Under explicit restrictions on epistasis and environment, determine minimax assay requirements for predicting a fixed intervention in unseen lineages. | Consequential for biological engineering and intervention design. High-order interactions are invisible to lower-order panels; the application itself is already recognized. | A4 gives the exact product-interaction ambiguity. A credible escalation requires a transport theorem plus lineage-held-out data, with assay and prior-acquisition costs. Neither is supplied here. |
| **Q8. Paired approximation in nonlinear elasticity.** Does every 3D bi-W^(1,1) homeomorphism of the cube, fixed near its boundary, admit smooth diffeomorphisms converging simultaneously in forward and inverse W^(1,1)? | This is the highest-ceiling pure-mathematics reserve. It concerns deformations that control both stretching and collapse. One-sided approximation does not give inverse derivative control. | B2 isolates a paired source/target PL-mesh lemma controlling derivative and cofactor mass while preserving injectivity. A recent PL-to-smooth theorem supplies the next step, but the missing mesh mechanism has not been invented. No positive result on that gate is claimed. |

Q8 is retained despite low immediate accessibility, so a familiar solvable finite model does not displace every speculative high-ceiling direction. It was not assigned a deep worker because the scout exposed a precise missing construction without a positive opening. Q5 and Q7 require physical evidence; mathematical prose cannot substitute for those experiments.

## 2. Deep investigation: a sharp flow-prediction contract

The full proof is [S4](deep/S4.md). On the normalized two-torus, let u be a real, smooth, mean-zero, divergence-free solution of unforced 2D Navier–Stokes with viscosity ν>0 and ||u(0)||2≤E. Let P_K retain the square Fourier band |j|∞≤K. An algorithm receives exactly P_Ku(0), K,E,ν,T, and returns a predicted P_K trajectory. Computation is unrestricted. Define the worst-case path error

\[
\mathcal E_K(T;E,\nu)=\inf_{\mathcal A}\sup_{u_0}\sup_{0\le t\le T}
\|P_Ku(t;u_0)-\mathcal A(P_Ku_0)(t)\|_2.
\]

For integer K≥16, the internally proved bounds are

\[
10^{-8}E^2\min\{K^2T,(\nu+E)^{-1}\}
\le\mathcal E_K(T;E,\nu)
\le10E^2\min\{K^2T,(\nu+E)^{-1}\}.
\tag{F}
\]

The lower already holds when the entire supplied snapshot is zero. The upper handles every mean-zero snapshot through the explicit heat predictor z(t)=exp(νtΔ)P_Ku0. For an arbitrary observed mean m, subtract m and use a Galilean frame: evaluate exp(νtΔ)(P_Ku0−m) at x−mt and add m, with the same constants. S1's final internal reconstruction prompted this explicit scope extension; the pre-audit report is preserved as S4_initial.md.

**Upper argument.** Compare u to the full heat evolution v and set w=u−v. With X=||u||2² and Z=||∇u||2², energy gives X′=−2νZ. The elementary periodic inequality ||u||4²≤10√X√Z yields

\[
\tfrac12(\|w\|_2^2)' +\nu\|\nabla w\|_2^2
\le10\sqrt{XZ}\|\nabla w\|_2
\le\tfrac\nu2\|\nabla w\|_2^2+50XZ/\nu.
\]

Since ∫XZ≤E⁴/(4ν), ||w||2≤5E²/ν. Energy also gives 2E. The individual nonlinear Fourier coefficient is at most |j|X, so projection and integration give 4K²E²T. Although v uses the unknown tail in this proof, P_Kv uses only the supplied snapshot. Taking the minimum and splitting E≤ν versus E≥ν proves the upper of (F). This distinction prevents an uncharged full-state input from entering the actual predictor.

**Lower construction.** Set L=floor(K/16), a=8E. Put vorticity a on ±A and ±a on ±B, where

\[
A=\{(40L+i,j):0\le i,j\le L\},\qquad
B=\{(-33L+i,8L+j):0\le i,j\le L\}.
\]

The two sign choices have energy at most E and identical zero snapshots. Every input lies above K. A target rectangle near (7L,8L), inside P_K, has order L² coefficients; each receives at least L²/4 same-sign interactions. The symmetrized vorticity coefficient

\[
(p\times q)(|q|^{-2}-|p|^{-2})>1/16
\]

on those pairs makes the second Picard term satisfy

\[
\|V_D(t)\|_2\ge a^2L^2t\,e^{-2852\nu L^2t}/960.
\]

An energy residual estimate for the exact PDE, including all modes generated after time zero, bounds its difference from that term by

\[
24a^3L^4t^2e^{16aL^2t}.
\]

At t=min{T,(6000νL²)^−1,(100000aL²)^−1}, the remainder is less than half the leading term. The two opposite leading outputs and the minimax triangle inequality yield (F). An earlier packet with −32L instead of −33L failed at K=31; that error and the corrected cutoff test are retained.

The interpretation is narrower than “fluid prediction is impossible.” The lower occurs at time of order K^−2 and at frequencies of order K. For any fixed output band P_J and zero snapshot,

\[
\sup_t\|P_Ju(t)\|_2
\le\frac{S_J E^2e^{50(E/\nu)^2}}{\nu(K+1)^2},
\quad S_J=(2J+1)\sqrt{2J(J+1)/3}.
\]

A four-mode sign pair gives the same K^−2 power below for one fixed low output at fixed E,ν and sufficiently large K. At a fixed terminal time T>0 the full zero-snapshot output also tends to zero, with upper E exp(25(E/ν)²)/((K+1)√(νT)). Thus growing output, initial transient, fixed output and positive delay are different tasks.

S4 also proves that fixed-bandwidth history with adversarial absolute error above the displayed P_J bound can have a common zero transcript, regardless of sampling rate. For the explicitly supplied two-packet family, one additional high-mode phase sign permits a certified second-Picard prediction. Its velocity precision is Θ(E/K), and an ordinary spatial grid acquisition costs O(K²) samples; the same grid already supports a full FFT baseline. There is no acquisition-inclusive advantage for general fields.

The nearest primary comparisons are [Foias–Prodi determining modes](https://eudml.org/doc/107242), [continuous data assimilation](https://arxiv.org/abs/1304.0997), [negative-Sobolev continuous dependence](https://www.afit.edu/BIOS/docs/viscosity.pdf), and [a posteriori regularity certificates](https://arxiv.org/abs/math/0607181). Their observation and time contracts differ. Those differences establish compatibility, not novelty. The packet/minimax statement still requires specialist reconstruction and a targeted approximation-theory search.

## 3. Deep investigation: what finite boundary experiments cannot see

[S3](deep/S3.md) and [S5's alternative proof and constructive theorem](deep/S5_inverse_challenge.md) work with scalar conductivity on B1 in R^n, n≥3. Conductivity equals one near the boundary and lies between 1/2 and 3/2. The boundary norm ||f||E² is the energy of its harmonic background extension. It is an explicit excitation resource. Recovery loss is L2 in a calibrated coordinate chart.

Fix a smooth axisymmetric bump ψ supported inside Br, r<1, away from the rotation axis. For integer s>n/2 and small fixed a, define the real smooth pair

\[
\sigma_k^\pm=1\pm ak^{-s}\psi(\rho,z)\cos(k\theta).
\]

They lie in a fixed Hs ball and have exact separation Δ_k=√2 a||ψ||2 k^−s. Rotation by π/k exchanges them. Therefore their *nonlinear* DN difference D_k couples angular character blocks only when p−q is an odd multiple of k. Harmonic energy of weight p inside Br decays at least as r^(2|p|+n−2). A block Schur estimate gives

\[
\|D_k\|_{E\to E^*}
\le\frac{4t_k}{1-t_k^2}\frac{r^{k+n-2}}{1-r^{2k}}
\le C_{n,r}ak^{-s}r^k,
\quad t_k=ak^{-s}.
\tag{I}
\]

The sharper first constant is S5's alternative resolvent proof; S3 proves the same scaling with denominator (1−t_k)². In S5's notation, elimination of the zero-boundary correction gives

\[
\Lambda_t-\Lambda_0=tA-t^2J^*(I+tK)^{-1}J,
\]

so subtraction at ±t leaves

\[
\Lambda_t-\Lambda_{-t}=2tA+2t^3J^*K(I-t^2K^2)^{-1}J.
\]

Only odd scattering orders survive. This is the useful mechanism: comparing a real oscillation to zero would retain even nonlinear terms, whereas the rotated sign pair cancels them. The comparison and angular selection are exact; no linearization is passed off as the nonlinear theorem.

Two operational consequences follow. First, angular input bandwidth |p|≤L with 2L<k gives **exactly equal all permitted pairings**, even at unlimited amplitude or repetition. Second, let each scalar readout have bounded adversarial error ν and let ||f||E²≤Emax. If Emax||D_k||≤2ν, adaptive midpoint answers give identical transcripts under both media. The fixed-chart minimax error is at least Δ_k/2, yielding a logarithmic smooth-class precision floor.

For independent Gaussian readout noise of variance ν², a different argument charges repetitions. Include the algorithm's independent random seed in the transcript. Adaptive KL chain rule and Pinsker give, for success at least 3/4 below Δ_k/2 under both media,

\[
\mathbb E_+\sum_j\|f_j\|_E^4\ge\nu^2/\|D_k\|^2.
\]

With capped per-probe energy and target coefficient error ε, this entails

\[
mE_{\max}^2\gtrsim\nu^2\epsilon^{-2}\exp(c\epsilon^{-1/s}).
\]

This assumes a fixed absolute noise variance. A real detector's variance-versus-duration/energy law must be supplied separately. The original statistical wording was corrected: KL equality applies to the joint seed/data transcript; observations alone inherit an upper bound by data processing. The original saved report is retained as [S3_initial](deep/S3_initial.md).

**Positive restricted inverse.** Suppose instead that the unknown belongs to the supplied D-parameter radial family σ_c=1+Σc_jφ_j(|x|), where the nonnegative smooth φ_j have disjoint ordered shell supports [a_j,b_j]. Use D real scalar energy probes, normalized spherical harmonics of degrees 1 through D. Their response Jacobian at zero is

\[
M_{\ell j}=(2\ell+n-2)\int\phi_j(r)r^{2\ell+n-3}\,dr.
\]

Its determinant is an averaged Vandermonde determinant. With μ_j=∫φ_j(r)r^(n−1)dr,

\[
\det M\ge d_*=
\prod_{\ell=1}^D(2\ell+n-2)\prod_j\mu_j
\prod_{i<j}(a_j^2-b_i^2)>0.
\]

Set B=D/d_*. Disjoint supports give ||DF(c)−M||∞≤12||c||∞. On radius ρ=min{1/2,1/(24B)}, the inverse is Lipschitz with constant 2B, and the fixed-M update c←c+M^−1(y−F(c)) contracts by 1/2. For true parameters in radius ρ/2 and measurement plus certified forward error ζ+τ≤ρ/(4B), after N iterations the parameter error is at most 2B(ζ+τ)+2^−N||c*||∞. The conditioning B, potentially tiny radius, boundary bandwidth D, supplied profiles and D radial forward solves per iteration are all charged. A uniform bit-runtime claim for arbitrary black-box smooth profiles is not proved.

The positive theorem genuinely uses D scalar readouts, not D infinite-dimensional Neumann functions. It also shows exactly how a strong supplied prior evades the smooth-class obstruction. No useful general unknown-geometry recovery follows.

[Mandache](https://doi.org/10.1088/0266-5611/17/5/313), [Di Cristo–Rondi](https://arxiv.org/abs/math/0303126), [Isaev](https://arxiv.org/abs/1012.2193), and [Koch–Rüland–Salo](https://arxiv.org/abs/2012.01855) establish nearby or broader exponential-instability machinery. The precise real sign-pair priority is UNKNOWN. The radial positive argument is conventional finite-dimensional inverse machinery until a stronger novelty assessment says otherwise.

For geometry g=σ^(2/(n−2))δ the pair is inequivalent under the specified boundary-fixed conformal gauge, but isometric under a boundary-moving rotation. No positive separation in an unrestricted boundary-fixed diffeomorphism-quotient distance was proved. Fixed coordinate loss must not be silently promoted to that quotient loss.

## 4. Deep investigation: affine rare events and certificate overlap

The input is an explicit binary affine system a_e·x=b_e and independent rational retention probabilities p_e. Let U be its inconsistency probability. [S2](deep/S2.md) develops complete reductions, a directly specified estimator and bit costs. [S5](deep/S5.md), initially given the target and primary hardness premise without S2's construction, independently found a simpler flow reduction.

**Hardness with fair, sparse, distinct equations.** For a graph with terminals s,t, introduce binary edge-flow variables. Deterministic vertex parity equations impose divergence one at s,t and zero elsewhere. A failed edge adds the retained equation f_e=0. The system is consistent exactly when a surviving terminal path exists: a path gives a flow, and a disconnected component cannot have odd total divergence. Splitting long parity equations into private ternary chains preserves this equivalence.

Each deterministic helper is then replaced by repeated private-variable pairs z+Σ_Ax=0 and z+Σ_Bx=b. Both rows have arity at most three. If both fair-retained rows survive, they impose the helper; an incomplete pair imposes no projected constraint. With r copies, helper activation is 1−(3/4)^r. All rows are distinct. For D helpers, monotonicity and the independent event “all helpers active” imply

\[
[1-D(3/4)^r]U\le U'\le U.
\]

Thus r=O(log(D/ε)) suffices for relative approximation, **without any inverse-rarity precision floor**. Combined with [Feng–Fu–Guo, Theorem 3](https://arxiv.org/html/2608.02523v1), this gives: an FPRAS for inconsistency of distinct arity-at-most-three affine equations, all independently retained with probability 1/2, implies an FPRAS for #BIS. It is a conditional approximation-hardness implication, not an unconditional no-FPRAS theorem. S2's cographic proof provides a separate reconstruction. N715's proposed width-two rapid mixing is not a premise.

**An overlap bound that does not charge event rarity.** Let

\[
\mathcal C=\{c:A^Tc=0,\ b^Tc=1\},\quad
N(S)=|\{c\in\mathcal C:\operatorname{supp}c\subseteq S\}|.
\]

For inconsistent S, Gaussian elimination gives N(S)=2^(|S|−rank A_S−1). Put w(c)=Π_(c_e=1)p_e and Q=Σ_cw(c)=E N(S). Sample c proportional to w, force its support retained, and sample the remaining bits normally. The resulting set law is μ(S)N(S)/Q, so Q/N(S) is an unbiased estimator of U. This is the classical union-mixture estimator with an algebraic multiplicity count.

The internally proved inequality is

\[
Q\le U\prod_e(1+p_e),
\qquad
\frac{\operatorname{Var}(Q/N(S))}{U^2}
\le\min\{2^{m-\operatorname{rank}A-1},\prod_e(1+p_e)\}-1
\quad(U>0).
\tag{A}
\]

To prove the first inequality, order minimal contradictory supports and partition inconsistent sets by their first contained support C. No nonzero even-right-side dependency is supported inside C, or it would cancel part of C to give a smaller contradiction. Hence restriction of witnesses to S\C is injective, giving N(S)≤2^|S\C|. Conditional on retaining C, the outside bits remain a product measure. Avoiding earlier supports is decreasing; Harris correlation bounds the conditional mean of the increasing 2^|S\C| by Π_(e outside C)(1+p_e). Average over the partition. This proof also explains why an arbitrary DNF certificate family cannot be substituted without checking the injectivity premise.

A supplied-order syndrome trellis computes Q and exact rational witness samples in O(m2^w) states, where

\[
w=\max_j[\operatorname{rank}(u_1,\ldots,u_j)+
\operatorname{rank}(u_{j+1},\ldots,u_m)-\operatorname{rank}(u_1,\ldots,u_m)],
\quad u_e=(a_e,b_e).
\]

Representation construction, rank work, O(B+m)-bit integer tables, capped rational coin generation and output size are specified in S2. The explicit sample count is O(min{2^(nullity−1),Π(1+p)} ε^−2 log(1/δ)). Favorable order discovery is not free. Dependency blocks permit independent union composition without multiplying relative error by the number of blocks.

**The comparator changes the significance.** Nondeterministically choose c_e≤S_e along the trellis and accept at syndrome (0,1). This is a polynomial-size NFA recognizing inconsistent retention words. Rational probabilities can be encoded by dyadic threshold blocks, with monotone thinning controlling relative error. The established [#NFA FPRAS](https://doi.org/10.1145/3477045) therefore already gives an FPRAS for polynomial-size trellises **without** the small-retention-mass promise used in the direct estimator. The wave does not discover a new low-width tractability boundary. A practical advantage requires an implemented feasible-trellis compiler and a matched modern #NFA comparison. Exact priority of (A) and the fair distinct ternary restriction remains UNKNOWN.

A 32-row exact diagnostic had U≈6.84×10^−49 and 67,108,864 witnesses represented by 64 full-syndrome states per layer. Witness samples recovered its probability while raw product sampling would need about 1.46×10^48 draws per observed event. The toy also admits an exact dynamic program, so this contrast is an illustration of conditional sampling, not evidence of advantage over the strongest baseline.

## 5. Deep investigation: exact action dynamics through zero strata

[S1](deep/S1.md) studies complex amplitudes x_i,y_i,c satisfying

\[
i\dot x_i=k_i\bar y_i c,\quad i\dot y_i=k_i\bar x_i c,
\quad i\dot c=\sum_i k_ix_iy_i,\qquad k=Kv\in\mathbb R^r.
\]

Let a_i=|x_i|², e_i=|y_i|², n=|c|², b_i=x_iy_i, s_i=a_i+e_i,
p_i=Im(b_i\bar c), S_ij=Re(b_i\bar b_j), R=SK, P=K^Tp and L=K^T(k⊙s). The exact real polynomial state equations are

\[
\dot a_i=\dot e_i=-2k_ip_i,\quad\dot n=2k^Tp,
\quad\dot p_i=(Rv)_i-k_is_in,
\quad\dot R_{i\alpha}=-k_is_iP_\alpha-L_\alpha p_i.
\]

They use O(rd+r) coordinates and operations and never divide by a vanishing amplitude. Conservation of Σ_i(a_i+e_i)+2n supplies global physical factorization for locally integrable prescribed controls. Locally Lipschitz feedback also works; continuous square-root feedback has explicit nonunique waiting-time solutions. Arbitrary unphysical ambient coordinates can blow up, so global existence is asserted only on the realizable image.

If all K rows are nonzero and controls range over an open set, two amplitude states have identical all-action behavior under every common control exactly when their displayed states agree. Initial actions, first derivatives and second derivatives recover respectively (a,e,n), p and R. A generic continuous exact predictor needs at least 3r+1 real dimensions, or 2r with the r+1 conserved parameters supplied. The polynomial state is regular but redundant: for d=1 it has 4r+1 coordinates, close to the original 4r+2 amplitude coordinates.

The added-control criterion uses zero-diagonal symmetric differences D with DK=0 and positive/negative inertia at most two: a new real direction ℓ is determined by the old information exactly when every such D satisfies Dℓ=0. Equal-coupling stars with r≤3 reconstruct the whole real Gram matrix; r=4 has a concrete counterexample. Detuning breaks the half-real closure; the appropriate complex construction uses the span of K,DK,D²K,…, where D is the diagonal detuning matrix. Generic distinct detunings fill the full rank. This is a representation boundary, not an all-algorithm lower bound.

The root independently derived a larger complex collective-product closure; S1 sharpened it by discarding coordinates invisible to action experiments. Older [AA-star literature](https://arxiv.org/abs/1002.4994) already employs relevant loop products, and observation-algebra and PSD-recovery literature supplies nearby methods. Broad novelty fails. The matched implementation was approximately **1.67–4.69 times slower** than the amplitude implementation across the recorded cases. Action-jet acquisition requires repeated preparation, calibrated controls and charged derivative precision. No general sensing or runtime advantage is demonstrated.

## 6. What the representations actually accomplish

Three useful constructions emerged, each with a demonstrated but restricted consequence.

1. **Control-dependent action equivalence.** The resonance state retains precisely the correlations queried by an admitted control span and output task. It repairs a concrete zero-mode failure and proves exact behavior, but does not beat acquired amplitudes or automatically survive new controls.
2. **Contradiction-certificate multiplicity.** Gaussian rank computes the number of simultaneously valid witnesses. Combined with a supplied witness trellis, it makes reciprocal-overlap rare-event sampling executable. The operation is an algebraic instance of established union counting, with the additional inequality (A) as the candidate refinement.
3. **Rotated real sign-pair cancellation.** Nonlinear inverse responses at ±t cancel even orders and enforce an angular selection rule. This makes an explicit exponentially indistinguishable pair and exact bandwidth obstruction possible. Its consequence is an impossibility within a calibrated sensing contract, not a new physical law.

The root's synthesis is that predictive representation and experimental distinguishability must be checked together. In the star, admitting a control changes the behavioral quotient. In tomography, boundary bandwidth changes which pair can be distinguished. In flow, changing output bandwidth or delaying the target changes the minimax law. This is a useful organizing observation supported by these examples; it is **not** a proved universal meta-theorem or a newly discovered conservation principle. For any wider transfer, the exact interface and quantifiers must be rebuilt.

## 7. Major failures, obstructions and implications

| Tempting escalation | Decisive evidence | What would have to change |
|---|---|---|
| Any bounded-arity affine entailment problem inherits signed-graph tractability. | Distinct fair ternary compilation and the imported #BIS implication. | A genuinely restrictive supplied representation or a major approximation-complexity advance; arity alone is insufficient. |
| A witness partition function is the event probability. | It counts overlapping witnesses; connected rank-one examples give exponential Q/U. | Exact multiplicity correction or a different sampler, with construction cost charged. |
| A new small-mass/low-width FPRAS is a new complexity boundary. | Existing #NFA approximation applies without the mass promise. | Demonstrated matched performance or a strict representation enlargement. |
| Fixed low-mode derivative ambiguity gives persistent full forecast failure. | Viscous input lifetime is K^−2; fixed outputs and terminal-time upper bounds decay. | Specify growing output and initial layer, or construct a different persistent mechanism under a stronger physical contract. |
| Arbitrary finite probes inherit the quantitative continuous-transcript width bound. | Discontinuous adaptive policies need a different argument. | Root/S3 prove exact noninjectivity by regular-level induction, but uniform quantitative separation remains open for that general policy class. |
| Continuum inverse uniqueness supplies efficient sensing of arbitrary smooth geometry. | Explicit pair (I), finite-probe ambiguity, and energy/noise accounting. | A useful prior, stronger sensor access, or a specified gauge-sensitive stable-recovery theorem with real acquisition costs. |
| An exact resonance invariant reduction gives a practical speedup. | Nearly unchanged dimension, stronger amplitude baseline and slower matched implementation. | An acquisition interface that yields the reduced state more cheaply, or another task/network with a demonstrated advantage. |
| OpenAI/math challenge admission proves a solution gap. | Comparator metadata selects a separate complete solution source. | End-to-end solution compilation and obligation/axiom audit, not inspection of the challenge stub. Neither success nor failure was established here. |

The scouts also rejected broad new-primitive claims based on known channel postprocessing, GHZ marginal ambiguity, treewidth/min-plus composition, and gain-graph holonomy. B3's exponential rate-acquisition example does not refute a supplied-exact-rate algorithm. B5's H10(Q) and hyperbolic-group source claims remain unverified; the published-source scope conflict was not resolved by assertion. These are preserved in the fifteen original reports.

No result creates energy, improves a universal physical limit, solves a major open complexity or arithmetic problem, or validates a general scientific AI architecture. Conditional longer-term value is more specific: identifying unavoidable sensor requirements, constructing honest reduced experiments, and finding algorithmic representations whose acquisition is achievable. Civilisation-level consequences require a much broader independently verified capability than this package provides.

## 8. Research priorities and stop rules

**First: inverse sensing with explicit pairs and constructive priors.** Audit the real sign-pair theorem against the strongest nonlinear instability literature, then test whether its cancellation survives less symmetric known backgrounds. In parallel, implement certified radial-shell inversion with conditioning visible. Continue only if a new precise theorem or practically useful sensing tradeoff survives matched finite-prior methods. A quotient-distance lower bound would be substantive; merely translating fixed-chart notation would not.

**Second: a sensing-and-delay law for nonlinear flow.** Independently reconstruct (F), then choose one causal observation contract and seek matching positive and negative bounds in spatial resolution, delay and absolute precision. Avoid extrapolation to turbulence or 3D. Stop escalation if the result reduces to an already known continuity estimate without a new operational consequence. The corrected initial-layer construction gives a concrete starting point and falsifier.

**Third: affine overlap and executable rare-event comparison.** Conduct a focused priority audit of (A), build the feasible-trellis compiler, and compare with a modern #NFA FPRAS using the same matrices, rational probabilities and success criteria. Continue only for a demonstrated runtime/representation gain or a sharper theorem. The fair-ternary barrier is a reason to choose structure carefully, not a reason to abandon structured reliability.

Q8 remains the speculative high-ceiling reserve: search specifically for a paired mesh construction or an admissible counterexample. The important gate is derivative/cofactor control with injectivity, not another one-sided smoothing theorem. Resonant control stays lower priority until its acquisition disadvantage changes. Materials and biological questions should receive experimental partnerships or public data tests before more abstract orchestration.

## 9. Provenance, verification and durable handoff

The wave fetched and pinned [Astra](https://github.com/harjassand/astra-research-knowledge/tree/5fc72a144d77c31b400efc0768afd7833c702362) at `5fc72a144d77c31b400efc0768afd7833c702362`, and [OpenAI/math](https://github.com/openai/math/tree/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb) at `fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`. Before publication, Astra main advanced to `01eda4be0686e9fe4dc650af7137efc3c88ba0fb`; the private publication branch was rebased and incoming N720–N723 status/correction records checked. They do not change the mathematical source inputs used here and were not adopted as premises. Both research pins and the refreshed publication base are retained. Entry points and decisive mathematical ranges are recorded in [SOURCE_PINS.json](SOURCE_PINS.json), individual reports and [SOURCE_LINKS.md](SOURCE_LINKS.md). Navigation and repository formalization percentages are source descriptions, not verification results. The attempted logspace Lean build was interrupted while dependencies compiled; no successful end-to-end Lean check is claimed.

Actual orchestration used **15 gpt-6-luna workers at max effort**, five in each requested mode, followed by **four gpt-6.1-sol workers at max effort**, then a **fifth gpt-6.1-sol max worker** for independent hardness reconstruction and the interrupted inverse investigation. All were launched with fresh contexts (`fork_turns=none`). [SPAWN_RECEIPTS.json](SPAWN_RECEIPTS.json) exports actual accepted launch metadata. The root supplied independent derivations, selection, counterexamples and scope corrections; its underlying model identifier is not exposed here, so “principal investigator” is a role, not a claimed provisioned Ultra model.

The initial explorations were separated by assignments and context, including unanchored C-mode work, before root-mediated synthesis. Selection used substantive early streams while final scout reports were being completed; this is recorded rather than presented as a fully frozen sequential trial. The fifth worker received only the hardness target and imported premise before its alternative flow proof. Later cross-audits were deliberately informed and cannot be called blinded verification.

S3 suffered two capacity interruptions and a later stream disconnect despite same-configuration retries. Its saved main proof survived; S5 completed the alternative proof and positive shell refinement. Exact status and failure scope are in [EXECUTION.json](EXECUTION.json). No empirical laboratory work, external specialist review, paid cloud job or full formalization was performed. Platform token totals, billing, energy and per-result wall time are not available; they remain UNKNOWN rather than zero.

Reproducible finite evidence includes exact graph/mask checks, symbolic resonance identities, rational witness moments and packet convolution tests. Root diagnostics checked 11 exact polynomial identities, 759 graph/failure cases and 112 helper projections. S2 checked 4,880 affine instances, 50 cographic graphs/694 masks, block composition and a rare exact example. S5 checked its alternative flow/gadget and laminar-DP constructions. S4 checked exact Fourier interactions for L=1 through 8 and analytic constant inequalities. S1 includes symbolic, derivative and trajectory checks plus its matched benchmark. These are finite diagnostics and internal reconstruction; **agent agreement and passing tests are not independent proof or priority validation**.

[CLAIMS.json](CLAIMS.json) keeps proof, novelty, comparator and cost statuses separate. [MANIFEST.json](MANIFEST.json) hashes the frozen package. [README](README.md) gives replay commands and the original-path resolver. Original scout/worker outputs are retained; root corrections link rather than erase historical failures. No pre-existing claim, proof file, checkpoint or scientific status is upgraded.

Shared checkpoint registration is blocked by a pre-existing validator failure, `evidence path is absent at source_revision: updates/CR/README.md`, also present before this wave's additions. The wave's own checkpoint draft is validated separately and retained outside the immutable checkpoint tree. The exact attempt is preserved in [evidence/checkpoint_publication.json](evidence/checkpoint_publication.json). The report package can be reviewed through a draft PR, but **no shared branch checkpoint has been registered**. Historical records are left intact. The next session should begin from this report and its manifest, repeat only checks justified by changes, and retain the external-proof, novelty and acquisition gates.
