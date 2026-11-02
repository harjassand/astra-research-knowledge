# Operational recovery on nonlinear transport trees: sharp tasks, transport duality, and an excitation frontier

**Research continuation, 2 November 2026.** An original synthesis and explicit conditional theorems/fixtures, **not** a claim of historical priority, a physical demonstration, a formal proof-assistant verification, or an advantage over equally informed established optimal recovery. This document builds on the completed [network-realizability opening](research_opening_network_realizable_interpolation.md) and retains its exact three-edge star counterexample.

**Astra pinned revision inspected:** [`c758c85713245fe853ef0fe00d4b18de691252b9`](https://github.com/harjassand/astra-research-knowledge/commit/c758c85713245fe853ef0fe00d4b18de691252b9). The connected Astra retriever was unavailable. Read the source/agent instructions, several current packets and selected governing proofs through the GitHub connector. No blanket repository review or status upgrade was made.

## 1. Scientific capability and strict source contract

**Goal:** For a *known rooted tree* of stationary passive nonlinear transport elements, use a finite, reusable record of controlled boundary injections and noisy boundary potential readings to decide future boundary operating tasks *sharply over all stationary constitutive laws consistent with that same record*. A task might be: will every terminal voltage remain below its rated level during a proposed first-time simultaneous demand? A decision is sound only when the entire compatible physical source family satisfies it.

Let ground be node 0, and ports 1,...,b be boundary nodes. Each edge e is oriented away from ground. Its unknown inverse constitutive relation is a single function φ_e: flow j -> voltage/pressure drop, held fixed across all experiments and requested future operations. Assume

- **Topology and conservation:** the known graph is a finite rooted tree; *every non-port internal node has zero external injection*, and the return/ground current balances the ports. No unobserved leakage, hidden injections or loop circulation.
- **Static edge class:** φ_e(0)=0; on its *certified finite flow interval* I_e containing 0 and every admitted historical/task edge flow, all secant slopes belong to [ℓ_e,u_e] with independently qualified 0<ℓ_e≤u_e<∞. Equivalently φ_e=m_e j+r_e(j), m_e=(ℓ_e+u_e)/2, r_e(0)=0, Lip(r_e)≤d_e=(u_e−ℓ_e)/2. No derivative oracle or edge-law coefficients are supplied. Global extensions can be constructed by continuing with legal slopes, but the physical qualification is only over I_e.
- **Experiments:** a record of k exact delivered port-current vectors p^h and selected terminal potential reports y_a, indexed by experiment h and port i. For each report there is a simultaneous deterministic measurement enclosure |y_a−x_i(p^h)|≤σ_a. Any uncertainty in actually delivered current must be charged separately; the exact LP below does **not** silently absorb uncertain inputs.
- **Future:** one or several exact planned port-current vectors p*, scalar task weights c, and a threshold in the same potential units. Joint future-task constraints can be appended to one LP. The source is not altered by past experimentation.

For a tree, define C_{ei}=1 if port i lies below edge e, else 0. Then Kirchhoff conservation **fixes**

\[
 j_e(p)=\sum_i C_{ei}p_i,\qquad
 x_i(p)=\sum_e C_{ei}\phi_e(j_e(p)).\tag{1}
\]

These are equations for the original physical tree, not an effective abstract gradient surrogate. The flows are known from the port currents independently of the edge-law values. Acyclicity is indispensable. In a looped network, conservation alone leaves circulation free, and equation (1) does not hold.

**Earned finite operating range/voltage containment.** Given a specified compact set of admissible injections P, the interval I_e can be chosen to contain {0}∪{∑_i C_{ei}p_i:p∈P}. For any admitted p,

\[
 |x_i(p)|\le\sum_{e:C_{ei}=1}u_e\left|\sum_jC_{ej}p_j\right|.\tag{2}
\]

Thus, under *independently established slope bounds over the known FLOW ranges*, the current-driven port potentials are bounded without requiring an unmeasured voltage solution. It would be circular to infer those slope bounds from this calculation; real calibration or physics must provide them. Sensor input resistance must be negligible or explicitly modeled.

### Physical scope

The most defensible prospective implementation is a branched quasi-static resistive/electrofluidic or microfluidic system, where sources and terminal pressure/voltage sensors can be commissioned. The result does not automatically transfer to AC electric grids, uncertain topology, pumps with internal control states, fluid inertia/capacitance, hysteretic devices, time-varying temperature/viscosity, or dynamic chemistry. Those cases invalidate one or more of the model premises.

## 2. Theorem A — exact source-complete finite LP for any rooted tree

Given k old injections and one future injection p*, collect for each edge e the sorted distinct flow levels

\[
 S_e=\{0,j_e(p^1),\ldots,j_e(p^k),j_e(p_*)\}.
\]

Introduce one real variable z_e(s)=r_e(s) per nonzero s∈S_e; set z_e(0)=0 exactly. For each pair of consecutive levels s<t in S_e impose

\[
 -d_e(t-s)\le z_e(t)-z_e(s)\le d_e(t-s).\tag{3}
\]

For every received terminal report a=(h,i), add the two linear inequalities

\[
 y_a-\sigma_a\le
 \sum_e C_{ei}\big[m_ej_e(p^h)+z_e(j_e(p^h))\big]
 \le y_a+\sigma_a.\tag{4}
\]

For task T=c^T x(p*) optimize its linear expression with the same variables:

\[
 T=\sum_e w_e\big[m_ej_e(p_*)+z_e(j_e(p_*))\big],
 \qquad w_e=\sum_i C_{ei}c_i.\tag{5}
\]

**Claim:** If the LP is feasible, its minimum and maximum are **exactly** the lowest and highest task outcomes of all stationary, monotone edge laws satisfying the stipulated flow-range bounds and all retained observation intervals. Any feasible LP point is realizable by the actual tree, and task endpoints are attained. Infeasibility is a falsification of the *joint* source/measurement/flow promises, subject to a sound exact numerical implementation.

**Proof.** Necessity: every actual φ_e gives z_e(s)=φ_e(s)−m_es satisfying (3), (4) and (5). Conversely, (3) implies the correct Lipschitz inequality for every pair of sampled levels by telescoping. Interpolate z_e linearly between consecutive levels; extend to the rest of I_e (and, if desired, globally) with any slopes in [−d_e,d_e]. Then φ_e(s)=m_es+z_e(s) has secant slopes in [ℓ_e,u_e], retains φ_e(0)=0, and visits *all* specified edge values under one shared physical law. Because the graph is a tree, the path-sum potentials constructed from these edge drops satisfy KCL, each edge's relation and the measured terminal enclosures. Therefore each LP feasible point is a physical source completion; an LP optimum is a physically attainable extremizer. The finite level value sets are bounded by the anchor and Lipschitz constraints, hence the objective extrema exist. QED.

For one task, there are at most |E|(k+1) nonanchor variables, ≤2|E|(k+1)+2M inequalities for M scalar observations, plus the linear model's sparse path summations. Sorting costs O(|E|k log(k+1)). Rational inputs have rational LP vertices. Ordinary LP theory gives polynomial bit-complexity bounds with rational coefficients; this is **not** a strongly-polynomial complexity theorem or a claim that the Python implementation is exact-certified. A conventional shape-constrained full finite-law identification LP with precisely the same information obtains **identical** sharp endpoints. The theorem replaces a nonessential full law parameterization, not an equally informed algorithm's attainable answer.

**Multiple future tasks** just add their future edge-flow values to each S_e and operate on one shared collection of z_e. Solving them as independent, disconnected histories would lose joint-source consistency. Task-dependent weights and thresholds may be chosen later from the existing record without reinstrumentation, as long as the same deterministic error enclosures and admitted source class remain valid.

## 3. Theorem B — task-specific operational information equals a one-dimensional transport dual

Subtract the known midpoint voltage contribution from every scalar observation:

\[
 \tilde y_a=y_a-\sum_e C_{e,i(a)}m_ej_e(p^{h(a)}),\quad
 \tilde T=T-\sum_e w_em_ej_e(p_*).
\]

Define one signed atomic measure on the **edge-flow line** for the future task and each observation:

\[
 \mu_e^*=w_e\delta_{j_e(p_*)},\quad
 \mu_{a,e}=C_{e,i(a)}\delta_{j_e(p^{h(a)})}.
\]

All unknown functions are anchored at zero. For a signed measure ν of finite support define its *balanced* form

\[
 \bar\nu=\nu-\nu(\mathbb R)\delta_0
\]

and the anchored KR norm

\[
 \|\nu\|_{\mathrm{KR},0}
 :=\int_{-\infty}^{\infty}|\bar\nu((t,\infty))|\,dt.
 \tag{6}
\]

This is the exact support value \(\sup_{r(0)=0,\operatorname{Lip}(r)\le1}\int r\,d\nu\). It is finite and equals a weighted sum of absolute cumulative atomic masses over consecutive sorted flow gaps. **The balancing atom at 0 is essential for negative flows and for nonzero-total measures.** An integral of *unbalanced* cumulative masses over all ℝ is generally infinite and is NOT the correct formula.

For every vector γ of linear coefficients on the measured readouts, write

\[
 \nu_e(\gamma)=\mu_e^* -\sum_a\gamma_a\mu_{a,e}.
\]

The sharp conditional extremal residual tasks are

\[
 \boxed{\begin{aligned}
 U_\mathrm{res}(\tilde y)&=\inf_\gamma\left[\gamma^T\tilde y+
 \sum_ed_e\|\nu_e(\gamma)\|_{\mathrm{KR},0}+
 \sum_a\sigma_a|\gamma_a|\right],\\
 L_\mathrm{res}(\tilde y)&=\sup_\gamma\left[\gamma^T\tilde y-
 \sum_ed_e\|\nu_e(\gamma)\|_{\mathrm{KR},0}-
 \sum_a\sigma_a|\gamma_a|\right].
 \end{aligned}}\tag{7}
\]

Add back the known midpoint task to obtain [L,U]. Equation (7) is valid whenever the observation fibre is nonempty. The upper expression has an actual finite minimum and the lower an actual finite maximum after quotienting irrelevant coefficient directions, or is approached as an equivalent LP dual if degeneracies arise; the task support values themselves are attained in the primal compact set. Numerically an accepted solver's primal/dual gap must be outward-certified before declaring a strict physical decision.

**Proof.** For any admissible edge family, the identity

\[
 \tilde T-\sum_a\gamma_a\tilde y_a
 =\sum_e\int r_e\,d\nu_e(\gamma)-\sum_a\gamma_a\varepsilon_a,
\]

with independent |ε_a|≤σ_a, immediately gives the two valid inequalities in (7) by the one-dimensional Lipschitz/Kantorovich–Rubinstein support identity. Conversely, Theorem A makes the unknown residual values a finite product of Lipschitz polytopes intersected with affine measurement strips. Finite-dimensional LP strong duality says the best coefficient bounds attain the primal source extrema. Eliminating each independent Lipschitz polytope produces (6), and eliminating the independent measurement-error box produces Σσ_a|γ_a|. Thus the infimum/supremum are exactly the conditional physical support functions, not merely generic upper/lower bounds. QED.

### Global, *pre-data* minimax radius

If only experiment locations/ports and sensor error budgets are known, the sharp globally worst-case error radius for estimating one scalar future task from the measured outputs, over all functions in the admitted symmetric centered residual class and all bounded errors, is

\[
 \boxed{\rho_*(p_*,c;\mathcal H)=\inf_\gamma\left[
 \sum_ed_e\|\nu_e(\gamma)\|_{\mathrm{KR},0}+
 \sum_a\sigma_a|\gamma_a|\right].}\tag{8}
\]

An affine prediction using an optimal γ attains this uniform bound. No nonlinear estimator can reduce that global worst-case radius: at the zero residual-data observation one can present two opposite allowed residual source/error pairs with the same reports and opposite task effects. Their task separation equals twice the optimal primal support, by strong duality. This is standard symmetric-convex optimal-recovery logic adapted to a network's exact flow-measure interface, not a newly invented abstract minimax principle. It does **not** say every actual-data fibre has radius ρ*: unusually informative observed values can yield a much smaller conditional interval.

In particular, with **zero sensor error** the future task is exactly recoverable from past scalar observations for *every* admissible physical network iff there exist coefficients γ satisfying, for each physical edge e,

\[
 \mu_e^* -\sum_a\gamma_a\mu_{a,e}
 \quad\text{is supported only at the anchor }0.
 \tag{9}
\]

Equivalently, all nonzero edge-flow atomic coefficients cancel. The condition can be checked by finite linear algebra without identifying even one edge law. If sensor noise is positive, the same algebra gives an exact functional identity plus a controlled noise amplification cost \(\sum\sigma|\gamma|\).

**Interpretation:** a new intervention is predicted from prior operations precisely when those operations span its *flow-evaluation signature*, even if the internal laws are nowhere uniquely identifiable. The signed-measure norm quantifies the *uncaptured* operation if exact cancellation is impossible.

This is related to the accepted Astra [N997](https://github.com/harjassand/astra-research-knowledge/blob/c758c85713245fe853ef0fe00d4b18de691252b9/knowledge/current/packets/N997.json) task-specific rank criterion, but N997 concerns a fixed exact-rational **linear** operator with full-vector responses. Its exact rank lower bound does not transfer as a theorem here: the present object is an infinite-dimensional product of nonlinear edge functions with scalar boundary mixing and an anchored-Lipschitz support norm. Astra [N1125](https://github.com/harjassand/astra-research-knowledge/blob/c758c85713245fe853ef0fe00d4b18de691252b9/knowledge/current/packets/N1125.json) supplies the qualified-task threshold discipline; the actual sharp observation-fibre extrema here meet its missing witness obligation.

## 4. Theorem C — an unavoidable *safe-excitation frontier*

Suppose every feasible training experiment keeps each edge flow within its *accessible* interval \(J_e=[a_e,b_e]\) containing 0, even if arbitrarily many perfectly measured experiments are permitted. A future task uses flow j_e*=j_e(p*). Define its outside-distance \(\Delta_e=\operatorname{dist}(j_e^*,J_e)\). Then there are two admitted source families with **identical full boundary responses on every allowed training intervention**, but a future scalar task gap equal to

\[
 \boxed{\sum_e |w_e|(u_e-\ell_e)\Delta_e.}\tag{10}
\]

To construct them, choose both inverse laws equal to the midpoint line m_ej throughout J_e. On each relevant outside segment toward j_e*, one law continues with slope ℓ_e and the other with slope u_e; choose which endpoint belongs to which system according to the sign of w_e and the direction of the excursion, so every edge contribution adds in the target difference. On other edges/functions, keep both systems equal. The laws are still stationary, anchored, continuous and monotone with the declared slopes. Every safe experiment sees exactly the same edge values, hence the same boundary reports. This proves an unavoidable **full task interval width of at least** the right-hand side even with unlimited perfectly precise safe experiments. Other ambiguities can make the interval wider.

Equation (10) prevents an exaggerated claim: if the intervention requires a genuinely new high trunk flow, no manipulation of previously low-flow observations removes its uncertainty. To close it, earn a rated/high-capacity reference operation, a stronger independently verified physical law, or accept the risk. A calibration port can expose that missing operation without simultaneously exercising the fragile service branches, **but it still exposes the shared trunk to the consequential current**.

## 5. Exact counterfactual composition, including an explicit decision reversal

For a one-trunk star with independent service branch drops f_i and a dedicated calibration branch, the target simultaneous injection p*=(q_1,...,q_n,0) has total S=Σq_i. The target terminal i is

\[
 x_i^*=f_0(S)+f_i(q_i).\tag{11}
\]

One calibration-only experiment injecting S into the rated calibration branch yields at any inactive service-port sensor the trunk contribution f_0(S), irrespective of the calibration branch's unknown nonlinear law. One single-port experiment injecting q_i into service branch i gives active voltage f_0(q_i)+f_i(q_i) and inactive voltage f_0(q_i). Consequently,

\[
 \boxed{x_i^*=y_{\mathrm{inactive}}^{\mathrm{cal}}+
 y_i^{\mathrm{single}(i)}-
 y_{\mathrm{inactive}}^{\mathrm{single}(i)}.}\tag{12}
\]

The equality holds for any nonlinear stationary independent edge laws, and even when each trunk/branch consists of arbitrarily many heterogeneous *series* components. It is not linear superposition of system responses: it is an exact elimination of repeated unknown *flow evaluations*. It uses only three scalar reports per terminal (one high-flow reading shared by all terminal decisions) and no function inversion. For n outputs, it uses n+1 controlled episodes and at most 2n+1 scalar voltage readings. Input currents are physically applied; their control accuracy and preparation are charged.

**Exact-rational five-port fixture.** Let S=12/25, q_i=3/25 for four equal service demands. On the target positive-current interval choose

\[
 f_0(j)=\tfrac3{25}j+\tfrac9{100}j^2,
 \qquad f_1(j)=\tfrac9{25}j+\tfrac7{100}j^2.
\]

They admit globally monotone extensions with trunk inverse slopes in [1/10,1/2] and branch slopes in [3/10,4/5] on the specified finite flow regime (the executable source uses tangent linear extensions outside ±1/2). The observations are exactly

\[
 y_{\rm cal,inactive}=\frac{1224}{15625}=0.078336,\quad
 y_{\rm probe,active}=\frac{936}{15625}=0.059904,\quad
 y_{\rm probe,inactive}=\frac{981}{62500}=0.015696.
\]

By (12) the *previously unperformed* joint service task is exactly

\[
 x_1^*=\frac{7659}{62500}=0.122544.
\]

For safety threshold c=0.15, no-history slope bounds give [0.084,0.336], so they **cannot** certify. Four single-service probes at ≤0.12 but **no high-flow calibration** give the physically sharp interval [0.095904,0.239904], which still straddles c. The two extremal source families in (10) produce the irreducible width (0.5−0.1)(0.48−0.12)=0.144. Adding the one high-flow calibration experiment collapses the ideal noiseless interval to [0.122544,0.122544], which certifies x_1^*<0.15. The control/information change, not an optimization trick, earns the decision.

**Bounded sensor and actuation errors.** With independent absolute voltage-report errors δ_v, exact currents give |error in (12)|≤3δ_v. If reference *delivered* flow differs from planned S by ≤η_ref and the single-service probe from intended q_i by ≤η_i, add u_0η_ref+u_iη_i. If the future joint operation itself has individual current errors ≤ζ_j, add

\[
 u_0\sum_{j=1}^n\zeta_j+u_i\zeta_i\tag{13}
\]

for terminal i. All realized flows must remain inside the independently qualified slope intervals. The branch reference must remain inactive during the service probe and the inactive sensor must not draw an uncharged current. (13) is a certified **outer** error budget, not an exact sharp current-uncertainty LP.

## 6. Large source-faithful execution and honest comparator outcomes

Saved executable: [`run_operational_tests.py`](run_operational_tests.py) with [`tree_operational_recovery.py`](tree_operational_recovery.py), producing [`operational_recovery_results.json`](operational_recovery_results.json). The code carries the original graph edges, individual heterogeneous inverse constitutive functions and all resulting flow/voltage calculations; the LP does *not* assume the producer's special source formulas. The model law for |j|≤1/2 is an odd quadratic \(a_ej+b_ej|j|\) with independent (distinct) coefficients around each series chain; it is tangent-line extended outside that domain to retain all global derivative bounds. The 40 heterogeneous series components sum to the declared nonlinear aggregate f_0 or f_i.

- 64 service branches and 1 calibration branch, each with 40 heterogeneous edges, plus 40 trunk edges: **2,640 physical edges**.
- 65 controlled single-branch episodes: one rated high-flow calibration at S=0.48 and 64 individual service current probes. The complete joint 64-port operation was never used in the training history.
- 129 scalar voltage readings (1 reference plus active/inactive service pairs). Every service current q_i is approximately 0.006–0.009 and sums to 0.48. Measurements use physically consistent terminal paths, no direct internal-edge voltage instrument.
- The exact mathematical stitching equality has a maximum floating residual 2.78×10⁻¹⁷ across all 64 ports. This is numerical checking of an exact symbolic identity, not 17 digits of laboratory accuracy.
- Model maximum service voltage during the target operation: **0.0818117471**; specified service limit **0.09**. No-history upper bound **0.2472105153** (does not certify).
- With δ_v=2×10⁻⁵ per voltage report, reference delivered-current error ≤2×10⁻⁴, single-port probe current error ≤10⁻⁵, and *each* future service port current error ≤5×10⁻⁶, equations (12)–(13) give a uniform error allowance **0.000332**, and hence an all-service upper **0.0821437471 <0.09**. Those error promises are supplied scenario assumptions, not acquired physical measurements.
- The original uncollapsed **2,640-edge** LP for a selected future terminal with three historical scalar readouts and each reading ±2×10⁻⁵ produced [0.0802614191, 0.0803814191]. It had 2,680 nonanchor variables and 5,366 inequalities; the two numerical HiGHS solves took about 0.02–0.04 seconds on this container. This is an executed software result and small allocated workload, not a benchmark across physical devices or broad source classes.
- Calibration **steady** power (current × calibration-port voltage) = **0.12828672** model units, while target simultaneous steady power is **0.03891828**. The calibration episode uses approximately **3.30 times the target's steady input power**, for equal time durations. Actual total energy also requires episode durations, ramping, apparatus overhead, measurement, resetting and losses. This substantially qualifies the practical benefit.

The native LP tests also covered a separate 8-port, 15-edge binary tree with 3–8 old episodes, mixed positive/negative edge currents, scalar tasks, and alternating exact/bounded **actually perturbed** observations. Across six independently constructed cases, the physical-primal conditional intervals contained the true task, their transport-dual upper/lower values agreed with the primal results to ≤2.8×10⁻¹⁷ in double precision, and all six conditional interval widths were smaller than the corresponding no-history widths. These are finite synthetic tests, not a statistical performance study or formal floating-point proof. Importantly, I also used each primal solution to **construct an entire original-edge piecewise-affine constitutive family**. Both the lower and upper families satisfy every historical observation enclosure and attain the respective future-task extremum in all six cases. This is the source-faithful conventional *full law identification* comparator run on the very same information; it ties the task-only bound while returning much more description than the task requires.

### Strong conventional optimization first

The companion [`conventional_network_milp.py`](conventional_network_milp.py) builds a standard mixed-integer finite-interpolation model for **arbitrary grounded connected graphs**, including cycles, with one shared unknown nonlinear conductance function per edge. It retains the original full state, Kirchhoff laws, old observations, future queries, anchor values and every pairwise secant slope obligation. One binary chooses the sign of each difference between edge voltage samples, with *valid a priori big-Ms* from the global positive-conductance band and grounded-Laplacian spectral gap. This is a reference formulation, not claimed optimal MILP engineering or exact symbolic verification.

On the original three-edge star with current history p=(0.2,0.2), measured terminal voltages (0.3,0.3), future p*=(0.2,0.4), conductance slopes in [1,5], the conventional HiGHS MILP reported bounds [0.3400000000,0.5000000000], a zero numerical MIP gap and one search node for each optimum. The separate *inverse-flow* tree LP with slopes [1/5,1] also recovers exactly 17/50 and 1/2, agreeing with the earlier independent rational star construction. The generic smooth-convex surrogate from that opening permits the physically impossible 0.26, a genuine but well-scoped structural relaxation gap.

On a separate six-edge cyclic diamond network, the same conventional MILP with two noisy historical response vectors and one future task reported [0.329915,0.391660] with 36 binaries and zero numerical relative MIP gap, exploring 68/34 nodes. This already handles the small cyclic regime. It would be incorrect to claim an exponential separator requirement or that a failed larger MIP run proves hardness. The special acyclic model is chosen for its exactly known internal flows and experimentally meaningful information signature, not as a performance victory over a strawman solver.

### Equally informed reconstruction/identification comparator

A conventional shape-constrained, full piecewise-linear identification approach applied to **the same knots and the same input/output/error constraints** is mathematically the primal Theorem A LP. It **ties** all our sharp bounds and decisions, and can produce explicit full candidate functions after each solve. A conventional optimal recovery expert using the same 1D Lipschitz supports can also adopt the transport dual and tie its error guarantee. Our gain is a verified *operational interface*: the query can be answered and its irreducible information diagnosed without choosing a unique microscopic description. It is not exclusive algorithmic superiority over an equally informed method. An arbitrary fitted single source cannot claim a robust decision when another compatible source produces the opposite result; the right conventional solution is to retain the whole compatible family as in Theorem A.

The no-history baseline uses exactly the same topology, known planned flow, slope bounds and anchor, but not the experimentally acquired voltage readings. Its sharp interval is

\[
 T_{\rm mid}\pm\sum_e |w_e|d_e|j_e(p_*)|.\tag{14}
\]

It ties the best possible answer when the prior supplies no more structure. In the positive large fixture, it correctly refuses the voltage threshold; the history-based task certificate passes. Equally informed identification ties the history-based decision, so there is **no claimed unique method win**.

## 7. Prior art and Astra inheritance, accurately delimited

**Physical mathematics already established:**

1. Will Johnson, [*Nonlinear Electrical Networks*](https://sites.math.washington.edu/~reu/papers/2014/will/directed-networks.pdf), source dated **16 August 2010**: nonlinear conductance/resistance networks, well-defined Neumann-to-Dirichlet response and edge-voltage uniqueness (Theorem 10.3). The present work does **not** claim to invent nonlinear resistance network existence or uniqueness.
2. A. van der Schaft, B. Besselink and A.-M. Huijzer, [*Kron Reduction of Nonlinear Networks*](https://research.rug.nl/en/publications/kron-reduction-of-nonlinear-networks/), *IEEE Control Systems Letters* **2024**: effective boundary reduction for static nonlinear networks. This supplies the strongest conventional physical reduction on general graphs.
3. H. Gernandt and J. Rohleder, [*A Calderón type inverse problem for tree graphs*](https://www.sciencedirect.com/science/article/pii/S0024379522001197), *Linear Algebra and its Applications* **2022**: exact tree metric/leaf-response reconstruction under a linear weighted model. The tree-additivity and series invariance are not claimed as novel structural identities.
4. A. Taylor, J. Hendrickx and F. Glineur, [*Smooth Strongly Convex Interpolation and Exact Worst-case Performance of First-order Methods*](https://arxiv.org/abs/1502.05666), *Mathematical Programming* **2017**: strong exact abstract interpolation baseline, which needs a physical realizability interface on the specified graph.
5. S. Foucart, [*Foundational Results of Optimal Recovery*](https://www.cambridge.org/core/books/abs/mathematical-pictures-at-a-data-science-exhibition/foundational-results-of-optimal-recovery/5CD2133E119A69F92E4331AF39EB6216), **2022**, and M. Ettehad & S. Foucart, [*Instances of Computational Optimal Recovery: Dealing with Observation Errors*](https://epubs.siam.org/doi/10.1137/20M1328476), **2021**: symmetric-convex optimal recovery and bounded observation uncertainty are established.
6. [Kantorovich–Rubinstein duality for 1D Lipschitz functions](https://mathematical-tours.github.io/book-sources/optimal-transport/CourseOT.pdf): anchored signed-atomic 1D norm is standard optimal transport/Lipschitz-free-space mathematics, not newly established abstract theory.
7. [SciPy HiGHS LP](https://scipy.github.io/devdocs/reference/optimize.linprog-highs.html) and [MILP](https://scipy.github.io/devdocs/reference/optimize.html) are legitimate standard optimization baselines. The numerical solves here are not exact rational proof receipts.
8. [*Hydraulic–electric analogy for design and operation of microfluidic systems*](https://pubs.rsc.org/en/content/articlelanding/2023/lc/d3lc00265a/unauth), *Lab on a Chip* **2023**, and [*Steady-State and Dynamic Behavior of Geometry-Tunable Microfluidic Passive Flow Regulators*](https://onlinelibrary.wiley.com/doi/full/10.1002/smll.74354), **2026**, document real applications but also the importance of dynamics and actual calibration. These papers do **not** validate the numerical present fixture as a fabricated physical device.

**Astra operations actually used or challenged:**

- [N1028 inverse-sector](https://github.com/harjassand/astra-research-knowledge/blob/c758c85713245fe853ef0fe00d4b18de691252b9/knowledge/current/packets/N1028.json): exact joint inverse consistent-family reasoning; crucial contrast, not a theorem that arbitrary globally monotone boundary maps are physically implementable by the specified network.
- [N1048 retained conservative cyclic-gradient interpolation](https://github.com/harjassand/astra-research-knowledge/blob/c758c85713245fe853ef0fe00d4b18de691252b9/knowledge/current/packets/N1048.json): reinforces one-source interpolation and warns that independently valid marginals do not form a common physical source.
- [N997 task-directed operator uncertainty](https://github.com/harjassand/astra-research-knowledge/blob/c758c85713245fe853ef0fe00d4b18de691252b9/knowledge/current/packets/N997.json): a **linear-operator** no-hidden-description task principle; the nonlinear functional interface here is separately earned by tree flow and Lipschitz structure.
- [N1125 qualified task decisions](https://github.com/harjassand/astra-research-knowledge/blob/c758c85713245fe853ef0fe00d4b18de691252b9/knowledge/current/packets/N1125.json): threshold logic requires actual qualified sharp bounds and endpoint witnesses, rather than treating a loose unresolved interval as proof of information impossibility.
- [N1077 planar matchgate tensor recognition](https://github.com/harjassand/astra-research-knowledge/blob/c758c85713245fe853ef0fe00d4b18de691252b9/knowledge/current/packets/N1077.json) and [N1615 common predictable rate Lyapunov](https://github.com/harjassand/astra-research-knowledge/blob/c758c85713245fe853ef0fe00d4b18de691252b9/knowledge/current/packets/N1615.json) were reviewed as alternate operations and **not** transferred into this network because their structural hypotheses are incompatible.

**No historical novelty exclusion:** the precise network task-flow signed-measure formulation may have antecedents not found in this targeted search. Claiming priority or a new fundamental physical law would be premature. The defensible result is the exact assembled conditional mechanism, executable physical-source checks and explicit information boundary.

## 8. What remains genuinely hard

The conditional mathematical service is complete **for rooted trees with known topology, exact delivered currents and independently qualified stationary edge-slope bands**. A powerful practical deployment still needs a physical specimen and repeatable method that confirms those premises under actual temperature, nonlinear pressure/current range, nonzero sensor loading, leak detection, apparatus drift and input/report uncertainty. The calibration reference can require substantially higher steady power and can stress the common trunk; this might make the method inferior to direct commissioning. An actual equal-budget experimental comparison is necessary, not implied by software runtimes.

For wider graph classes, the central new mathematical task is to replace the tree's known-flow signature with a representation that retains **unknown loop circulations jointly across old and future interventions**, while still producing sharp task-recoverability and intrinsic safe-excitation lower bounds. The conventional MILP is already a valid competitor; the open problem is *whether informative, source-faithful task experiments and efficient exact inference survive when branch currents are not determined by conservation.* Failure of a solver on one instance is not a hardness theorem. A meaningful mathematical next theorem would cover bounded independent cycle rank with a specified complexity and produce matched ambiguity witnesses, then demonstrate an informative task family that is not solved as well by ordinary certified optimization.

**The most immediate physical falsifiers** of the present capability: a branch whose constitutive curve drifts between individual and joint experiments, unexpected leak flow at an intended inactive sensor, a calibration exposure that damages the common trunk, or a measured edge outside its certified slope/flow range. A very high-information mathematical certificate cannot repair those missing source truths.

## 9. How to reproduce

The package includes original previous note and exact star code; the additional scripts use Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0 (HiGHS), with NumPy/scipy version flexibility subject to ordinary numerical tolerance.

```bash
python exact_stitch_fraction.py
OPENBLAS_NUM_THREADS=1 python conventional_network_milp.py
OPENBLAS_NUM_THREADS=1 python tree_operational_recovery.py
OPENBLAS_NUM_THREADS=1 python run_operational_tests.py
```

`run_operational_tests.py` regenerates `operational_recovery_results.json`. Its tests check the exact star regression, noiseless and bounded-noisy branched-tree primal/dual equivalences, a constructed information floor, the 2,640-physical-edge 64-port source identity and full-edge primal LP. Actual numerical result JSON includes each case and 64 individual terminal predictions. `conventional_network_milp.py` implements the ordinary big-M comparison rather than silently comparing with factorial enumeration.

**Finite-output scientific status:** The physical tree LP theorem, task-transport support identity and counterfactual/source-law constructions are derived here with explicit proofs and software checks. Their antecedent mathematical ingredients have substantial prior art. Physical-source qualification, historical priority, numerical outward validation and practical advantage have *not* been established.
