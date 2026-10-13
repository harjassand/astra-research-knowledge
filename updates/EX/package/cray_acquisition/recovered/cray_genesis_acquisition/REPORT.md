# CRAY GENESIS — Response-cell acquisition

**Research date:** 13 October 2026  
**Status:** Internally derived mathematics, exact finite tests, and synthetic executable experiments. Historical novelty, independent proof review, physical usefulness, and superiority to the strongest specialised methods are **not established**. This packet does not meet the civilisation-enabling completion criterion.

## 1. Outcome and scientific target

This investigation developed an information-acquisition candidate for effective linear response on a finite, known network. Rather than acquire every accurate microscopic coefficient and then solve the accurate global problem, it acquires selected coefficients—or selected local response cells—and returns a two-sided confidence enclosure for one macroscopic conductance.

The most useful derived structure is that a single nonnegative discrepancy controls both the width of the physical-response enclosure and the variance of the quantities that must be acquired. A local-cell construction can decrease this discrepancy without guessing the target global solution. However, the executed strong-mismatch experiment also exposes the unresolved cost: local repair only reached a narrow enclosure after all target coefficients were acquired.

The elementary edge enclosure is a direct consequence of established Dirichlet and Thomson principles. Variance-adaptive confidence estimation is also established. The possible research contribution is the particular acquired local-response interface, its joint discrepancy/variance control, and its resource tradeoff. A search of related literature did not establish priority. Independent derivation is not evidence of novelty.

### Independent screening

Four directions were screened before committing to this target:

| Direction | Relevant existing comparator | Reason not to claim a generic breakthrough |
|---|---|---|
| Correlated electronic structure | Selected configuration interaction with stochastic perturbative correction [1] | A sparse representation still does not furnish general, cheaply acquired, certified energy accuracy. No new mechanism resolving that issue was obtained here. |
| Rare molecular and chemical events | Weighted ensemble and optimised trajectory management [2] | Beating brute-force waiting would not establish an advance over these specialised methods. The cost of learning useful reaction coordinates remains relevant. |
| Experimental inference | Goal-oriented Bayesian optimal experimental design [3] | Acquiring a predictive quantity rather than every parameter is already an established objective. Merely renaming it would not be discovery. |
| Expensive coefficients underlying macroscopic response | Degree-of-rate-control analysis, local probabilistic conductivity methods, variational network methods [4–6] | The selected question is whether finite-error global certification can be coupled to a substantially cheaper *acquired* coefficient interface. |

These were literature-informed screening routes, not completed implementations or head-to-head evaluations. No theorem from the Astra or OpenAI mathematics repositories is used as a premise of the results below.

### Exact input/output contract

Inputs are a finite connected graph with positive reference conductances, a specified terminal pair, a way to obtain target conductances on requested edges, and certified ratio bounds on the reference-response support. The topology and reference model are not free. The algorithm outputs an interval for the conductance of the specified target graph, not a guarantee that this graph accurately models a real material.

Potential applications would be linear transport or reversible-network capacities built from expensive microscopic calculations. This packet does not establish a realistic atomistic network, ab initio rate accuracy, missing-path discovery, a nonequilibrium reaction-rate model, or a many-body state-space compression. A capacity-to-rate conversion can require additional stationary weights and modelling assumptions, which are not supplied here.

## 2. Reference response and the edge enclosure

Let an oriented incidence matrix be H; the choice of orientation is immaterial. Let c0_e>0 be reference conductances and c_e>0 target conductances on the same graph. Set h0(s)=1 and h0(t)=0, and let h0 be reference-harmonic at other vertices. Terminal sets can first be contracted into a single source and sink.

Write

\[
 d_e=(H^T h_0)_e,\qquad
 C_0=\sum_e c_e^0d_e^2,\qquad
 f_e^0=c_e^0d_e.
\]

The reference flux satisfies

\[
 Hf^0=C_0(\delta_s-\delta_t).
\]

Define the reference dissipation probability and target/reference ratios

\[
 p_e=\frac{c_e^0d_e^2}{C_0},\qquad r_e=\frac{c_e}{c_e^0}.
\]

Only p-positive edges enter the following expectations. Let

\[
 A=\mathbb E_p r,\qquad B=\mathbb E_p r^{-1}.
\]

### Proposition 1: deterministic enclosure

\[
 \boxed{\frac{C_0}{B}\le C(c)\le C_0 A.}
\]

**Proof.** The reference potential is an admissible unit-drop trial potential for the target network, with energy

\[
 \sum_e c_ed_e^2=C_0A.
\]

The reference flow divided by C0 is an admissible conserved unit flow. Its target resistance energy is

\[
 \sum_e \frac{(f_e^0/C_0)^2}{c_e}=\frac{B}{C_0}.
\]

The Dirichlet minimum principle gives the upper bound. The Thomson minimum-resistance principle gives 1/C(c) <= B/C0, yielding the lower bound. These variational principles are established prior work [6].

### What does not need to be acquired

If p_e=0, both trial drop and trial flux vanish on that edge. Its positive target coefficient may be arbitrarily large or small without entering either bound. No target/reference ratio bound is required on such an edge for Proposition 1 or its sampling procedure.

This is not a claim that such edges never affect the true response. Under mismatch they may carry target current. Rather, the two trial witnesses already bound every possible effect they can have. When the witness interval is wide, that protection is correspondingly uninformative.

### Discrepancy and scale invariance

The ratio of the upper to lower deterministic bound is 1+D, where

\[
 D=AB-1
 =\frac12\mathbb E_{e,f\sim p}
       \frac{(r_e-r_f)^2}{r_er_f}\ge0.
\]

Thus a common multiplicative calibration r_e=rho gives D=0 exactly, even when rho is far from 1. Relative dispersion, not absolute common bias, is the relevant quantity. For ratios rho(1+small fluctuations), the gap starts at second order in the fluctuation amplitude.

There is also an information-theoretic identity. Define the target trial-energy distribution q_e=p_er_e/A. Then

\[
 D=\chi^2(p\Vert q),\qquad
 \frac{\operatorname{Var}_p(r)}{A^2}=\chi^2(q\Vert p).
\]

These are direct algebraic identities, not claims of a new divergence.

## 3. The response-cell operation

The edge construction cannot repair a poor witness. A stronger operation uses local target response solves while preserving globally compatible boundary data.

Partition the edges into disjoint cells K. Vertices can belong to more than one cell. A cell boundary consists of the terminals it contains and all its vertices incident to edges outside the cell. Other cell vertices are interior.

For each cell set

\[
 E_K^0=\sum_{e\in K}c_e^0d_e^2,\qquad
 b_K=H_K f_K^0.
\]

The vector b_K vanishes at cell-interior vertices. Its total is zero on each connected component of the cell.

Acquire the target coefficients inside the requested cell and compute two quantities:

\[
 D_K=\min_{h|_{\partial K}=h_0}
          \sum_{e\in K}c_e(H_K^Th)_e^2,
\]

\[
 N_K=\min_{H_K f=b_K}
          \sum_{e\in K}\frac{f_e^2}{c_e}.
\]

D_K is a local fixed-potential response. N_K is a complementary local fixed-flux response. These are two local problems, not a supplied exact macroscopic oracle. All acquired coefficients, local solves, and precision costs must be counted.

### Proposition 2: compatible global enclosure

\[
 \boxed{\frac{C_0^2}{\sum_K N_K}
       \le C(c)\le\sum_K D_K.}
\]

**Proof.** The local minimizing potentials agree at shared vertices because all shared vertices retain h0. Gluing them gives one globally admissible unit-drop potential. Its energy is the sum of D_K.

The local minimizing flows have exactly the same cell divergences as f0. Summing them over the edge partition gives global divergence Hf0. Dividing by C0 yields an admissible global unit flow with resistance energy (sum N_K)/C0^2. Apply the two variational principles.

### Proposition 3: the paired local response inequality

\[
 D_KN_K\ge(E_K^0)^2.
\]

**Proof.** For any admissible cell potential h and flow f,

\[
 \sum_{e\in K}(H_K^Th)_ef_e
 =h^Tb_K=h_0^Tb_K=E_K^0.
\]

The middle equality holds because b_K is zero in the interior, where h can differ from h0. Weighted Cauchy–Schwarz now gives the claim for the independently minimizing pair.

If E_K^0=0, h0 is constant on each connected component of that cell and f0 is zero there. Both local energies are zero for all positive target coefficients. Such a cell requires no query.

For positive-work cells define

\[
 w_K=E_K^0/C_0,\qquad
 u_K=D_K/E_K^0,\qquad v_K=N_K/E_K^0.
\]

Then w is a probability distribution, u_Kv_K>=1, and

\[
 \boxed{C_0/\mathbb E_wv\le C(c)\le C_0\mathbb E_wu.}
\]

### Coarsening is monotone, but is not free

Merging cells can only decrease sum D_K and sum N_K. The old glued potential is feasible for the merged Dirichlet problem, and the old combined flow is feasible for the merged Neumann problem. Each merged minimization therefore costs no more energy than its old trial.

Consequently the lower conductance bound increases and the upper bound decreases. Singleton-edge cells give Proposition 1. One whole-graph cell gives equality at both ends, provided terminal sets have first been contracted into one source and sink.

That exact endpoint is not a speedup: it acquires and solves the entire target network.

## 4. The same discrepancy controls response error and acquisition variance

Assume a certified 0<a<=r_e<=b on the positive reference-work support, and write R=b/a. Edges of zero reference work still need no such restriction.

The reference potential and flux are feasible local trials. They imply D_K<=bE_K^0 and N_K<=E_K^0/a. Combined with Proposition 3 this yields

\[
 a\le u_K\le b,\qquad b^{-1}\le v_K\le a^{-1}.
\]

Let

\[
 A=\mathbb E_wu,\quad B=\mathbb E_wv,\quad\Delta=AB-1.
\]

### Proposition 4: variance control

\[
 \boxed{\frac{\operatorname{Var}_w(u)}{A^2}\le R\Delta,
 \qquad \frac{\operatorname{Var}_w(v)}{B^2}\le R\Delta.}
\]

**Proof.** For a positive X with mean m and X<=b,

\[
 \mathbb E[(X-m)^2/X]
 =m(m\mathbb E[1/X]-1).
\]

Hence

\[
 \operatorname{Var}(X)/m^2
 \le (b/m)(m\mathbb E[1/X]-1).
\]

Apply this to u. Since v>=1/u, A E[1/u]-1<=AB-1. Also b/A<=b/a=R. This proves the first inequality. Swap u,v, using their reciprocal range, for the second.

This proof does not require independent or stationary coefficients in space. The target network can be arbitrary and fixed. Randomness is introduced by the acquisition algorithm sampling from w.

### Separating two reasons the certificate can remain wide

Let q_K=w_Ku_K/A. Then

\[
 \boxed{\Delta
 =\chi^2(w\Vert q)
  +A\mathbb E_w\left[v-\frac1u\right].}
\]

The first term is redistribution of work between cells. The second is the incompatibility between each cell's prescribed reference potential trace and prescribed reference flux. Both are nonnegative. This separates between-cell information mismatch from within-cell response mismatch.

More samples estimate these quantities more accurately but cannot make either intrinsic term vanish. A better reference or a better cell representation is required when Delta exceeds the desired accuracy.

## 5. Acquiring the enclosure with a stopping rule

Sample cells independently with probabilities w_K. Query/cache their target coefficients and obtain u_K,v_K. Repeated cells do not require repeated expensive coefficient acquisition, although repetitions are retained in the statistical sample.

For n>=2 observations X_i in an interval of width W, use the one-sided empirical Bernstein bound [7]

\[
 \mathbb EX\le\bar X+
 \sqrt{\frac{2s_n^2\log(2/\delta)}n}
 +\frac{7W\log(2/\delta)}{3(n-1)}
\]

with probability at least 1-delta. Here s_n^2 is the unbiased sample variance.

At dyadic stage k, allocate failure probability

\[
 \delta_k=\frac{\alpha}{2k(k+1)}
\]

to each of the two upper moment bounds. The sum of failure probabilities over all stages and both moments is alpha. Intersect the resulting intervals

\[
 [C_0/B_k^+,\ C_0 A_k^+]
\]

with previous intervals. Stop when U/L<=1+epsilon. With probability at least 1-alpha the reported interval contains C(c). Its geometric midpoint, if computed accurately, has multiplicative error at most sqrt(1+epsilon)-1.

If no such interval is obtained within the budget, return failure and the current wider interval, not a spurious answer.

### Query scaling, with the crucial qualification

A standard Bernstein calculation for relative moment error eta gives the sufficient sample count

\[
 n\ge\left(\frac{2R\Delta}{\eta^2}
       +\frac{2(R-1)}{3\eta}\right)\log(4/\alpha).
\]

This statement bounds relative errors of the two sample means; it is not the exact stopping count of the implementation. Empirical-variance stopping can adapt without knowing Delta beforehand, at the cost of additional logarithmic factors [7,8].

For a family with Delta<=epsilon/4 and fixed R, the count to reach an epsilon-width certificate is of order

\[
 \widetilde O\bigl((R/\epsilon)\log(1/\alpha)\bigr).
\]

Outside that favourable-discrepancy regime, this is **not** an epsilon-accuracy algorithm. Infinite samples only converge to the intrinsic interval ratio 1+Delta.

### Complete resource accounting

A realistic cost expression is

\[
 T_{\rm graph}+T_{\rm reference}+T_{\rm weights}
 +T_{\rm sampling}+T_{\rm statistics}
 +\sum_{K\ \mathrm{queried\ distinctly}}
  \left(\sum_{e\in K}T_{\rm acquire}(e)
       +T_D(K)+T_N(K)+T_{\rm precision}(K)\right).
\]

For a fixed partition, cells are edge-disjoint. When changing partitions adaptively, edge caching must prevent double-counting; new local solves still cost time. A statement about n sampled cells is not a statement about n acquired coefficients.

The expected distinct-cell acquisition cost after n draws is

\[
 \sum_K \left[1-(1-w_K)^n\right]T_K,
\]

where T_K includes that cell's coefficients and local computation. This formula, not a graph-size-independent draw count alone, determines whether the operation is practically useful.

Building an explicit categorical sampler costs O(number of cells) storage/setup; inverse cumulative sampling then costs logarithmic time per draw. The special grid demonstration has a simpler exact factored sampler.

## 6. Precision and the implemented finite-bit case

The original large comparison in experiment.py uses float64. It is not a rigorously outward-rounded certificate, even though the underlying probability theorem is rigorous under its premises.

The separate finite_bit_demo.py removes that particular arithmetic issue for an analytically solvable reference grid. It uses an implicit 256 by 256 grid, exact integer channel weights, a cached lazy rational target-coefficient oracle, and integer inverse-cumulative sampling. It does not generate all target coefficients before acquisition.

Sample first and second moments are enclosed using fixed-point integers. Logarithms in the probability bound are bounded above using the positive series

\[
 \log z=2\sum_{j\ge0}\frac{t^{2j+1}}{2j+1},
 \qquad t=(z-1)/(z+1),
\]

after scaling z into [1,2]. A geometric tail bound is included. Square roots are rounded upward by integer square roots. All stored interval endpoints and stopping comparisons are rational/integer.

The execution stopped after 2,048 draws and 2,014 distinct target-coefficient queries, with interval

\[
 [2.1503171602351814,\ 2.2339888389129205],
\]

whose endpoint ratio minus one is 0.03891131979. Exact rational endpoints, every sampled edge, and every acquired rational coefficient are recorded in finite_bit_results.json. There are no transverse coefficient queries; the mathematical enclosure applies to every positive assignment of those coefficients.

The data are synthetic. The target axial ratios are, by construction, between 0.95 and 1.05; the confidence procedure deliberately uses only the broader certified range [0.5,2].

The statistical theorem assumes independent uniform random bits. The stored run uses a seeded pseudorandom generator for reproducibility; this is not a verification of the generator. An OS-backed option is provided. The arithmetic implementation has been inspected and executed, not formally verified.

### General reference fields remain a separate cost

For any admissible potential h and exactly conserved unit flow j, even if they are not matched reference optimizers, define

\[
 U_0=\sum c_e^0(dh)_e^2,\quad
 R_0=\sum j_e^2/c_e^0,
\]

and separate energy distributions proportional to those two summands. Then

\[
 \frac1{R_0\mathbb E_q[r^{-1}]}
 \le C(c)\le U_0\mathbb E_p[r].
\]

This permits approximate reference solves with valid feasible witnesses. However, their initial product U0 R0 contributes an additional gap. Constructing an inexpensive, low-energy exactly conserved correction and enclosing its arithmetic for an arbitrary large graph is not implemented here. The analytically solvable reference is a deliberate restriction of the demonstrated backend.

## 7. Executed experiments

### 7.1 Large synthetic comparison

The grid has 65,536 vertices and 130,560 edges. Reference conductance varies between axial channels but is constant along each channel, so the reference potential is explicitly known. Of the edges, 65,280 have positive reference dissipation. Transverse target/reference ratios span approximately eight orders of magnitude, but those edges have zero reference work.

The stopping target is U/L<=1.05, with alpha=0.01. Both statistical procedures use the same graph, reference weights, samples, broad active ratio range [0.5,2], and confidence-budget schedule. The Hoeffding comparator is a matched range-only statistical baseline, not the strongest possible specialised transport algorithm.

| Target case | Exact-moment intrinsic gap (float calculation) | Bernstein distinct reads | Hoeffding distinct reads | Bernstein outcome |
|---|---:|---:|---:|---|
| Common axial scale 1.6 | 0, up to rounding | 2,014 | 24,506 | 3.599% width |
| Heterogeneous small axial mismatch | 0.4186% | 2,014 | 24,506 | 4.951% width |
| Axial ratios randomly 0.5 or 2 | 56.2477% | 51,380 | 51,380 | Budget exhausted; 58.727% width |

The successful runs use 2,048 draws, versus 32,768 draws for Hoeffding. Caching changes the draw ratio of 16 to a distinct-read ratio of approximately 12.17. Compared with reading all 130,560 edge coefficients, the count is approximately 64.83 times smaller. An optimised full-input solver could omit some edges between fixed terminal vertices; this count is not a lower bound on every specialised comparator's acquisition cost.

All displayed successful intervals contained the float64 full-network reference solve. Across 100 additional seeded runs of the heterogeneous case, all reported intervals contained that comparator; 99 runs stopped at 2,048 draws and one at 4,096. This is a finite diagnostic, not independent proof of 99% coverage.

The full sparse target solves took approximately 0.27–0.30 seconds each in this environment. No expensive physical oracle was executed. Therefore these data establish reduced synthetic coefficient reads, **not an ab initio wall-clock speedup**. The synthetic small-mismatch response is already close to the reference response; the achievement is a narrower acquired certificate, not a newly discovered large physical effect.

The broad transverse contrast should not be described as solving arbitrary hard high-contrast transport. The favourable geometry gives those edges zero reference work. The strong active-mismatch case was intentionally retained as a failure.

Initial attempts at a larger three-dimensional sparse comparator did not complete within the execution limits and produced no reported three-dimensional result. The successful benchmark is two-dimensional.

### 7.2 Local repair under strong mismatch

cell_probe.py uses a separate 64 by 64 strong-mismatch network. Terminals are contracted before applying the cell construction. All 7,938 retained target coefficients are acquired for this diagnostic.

| Nominal cell side | Cells | Largest cell, edges | Enclosure gap |
|---:|---:|---:|---:|
| 1 | 4,032 | 2 | 56.244% |
| 2 | 1,024 | 8 | 47.413% |
| 4 | 256 | 32 | 30.141% |
| 8 | 64 | 128 | 16.179% |
| 16 | 16 | 512 | 6.217% |
| 32 | 4 | 2,016 | 2.102% |
| 64 | 1 | 7,938 | approximately 1.14e-11 |

This confirms the predicted monotone gap reduction numerically. It does not establish acquisition savings: every row uses the entire target coefficient set. At the first tested scale below 5%, a cell can already contain 2,016 coefficients. The repair mechanism survives, while the hoped-for simultaneous cheap-acquisition result remains unproved and undemonstrated.

### 7.3 Exact finite checks

exact_checks.py uses rational arithmetic on 32 generated connected graphs, with multiple nested edge partitions per graph. It tests global conductance containment, local paired inequalities, ratio ranges, discrepancy/variance bounds, monotonic coarsening, and equality for a whole-graph cell. An additional balanced-diamond test has an exactly zero-work transverse edge with target conductance 10^12.

All 3,223 counted assertions passed. These finite checks are not a formal proof of the general propositions or a historical-priority review.

## 8. Failure boundaries and acquisition lower checks

### Scalar moments cannot generically close their own gap

The edge enclosure is sharp across graphs. For a chosen distribution p and ratios r, a parallel network can attain C/C0=A, while a series network can attain C/C0=1/B, by choosing their reference conductances appropriately. An interface retaining only these moments and C0 cannot distinguish the two outcomes in general.

For p=(1/2,1/2) and r=(1/2,2), A=B=1.25. The two endpoints are 0.8 C0 and 1.25 C0. A method using the topology or additional local responses can do better; this is not a lower bound on all algorithms.

### Some coefficient-tail information is indispensable

Without an acquired or otherwise justified upper tail restriction, an unqueried parallel edge can have arbitrarily large conductance. Without appropriate lower control, a missed weak series edge can dominate resistance. Good agreement on sampled edges cannot itself certify a global ratio envelope.

This is an input-information obstruction. It is not removed by the concentration inequality. In a physical application, validating an inexpensive envelope is one of the most consequential unresolved tasks.

### The favourable 1/epsilon scale has an elementary lower check

Consider equal-reference parallel edges. Compare a target with all r=1 to a target with a uniformly hidden fraction p=80 epsilon of edges having r=1.05, all others 1. Assume epsilon is sufficiently small and choose a graph size making the fraction integral.

The conductance changes by 4 epsilon, while

\[
 D=p(1-p)\frac{0.05^2}{1.05}<0.191\epsilon.
\]

Thus the example remains in a small-discrepancy regime. Before hitting a changed edge, coefficient-query transcripts are indistinguishable. A constant-success guarantee requires order 1/p, hence order 1/epsilon, distinct queries when the graph is large enough. This is an elementary restricted-model scaling check, not a full minimax theorem with optimal constants or a novelty claim.

### Why this is not a sublinear graph-input miracle

The graph/reference model and sampling weights are already acquired and charged. Known adjacency-query lower bounds for effective resistance concern a different input model [9]. No contradiction or general evasion of those bounds is claimed.

## 9. What remains before a consequential capability exists

**Physical acquisition.** A real scientific instance must supply or cheaply certify the graph, reference model, and error envelopes. Force-field or electronic-structure model bias is not corrected merely by calling a rate estimate “high fidelity.”

**Cost versus repair.** One needs a useful relationship between cell cost and discrepancy reduction for a consequential physical class. Monotonicity alone allows convergence only at the full-system endpoint, which can erase every saving. The strong-mismatch experiment illustrates this risk rather than resolving it.

**Specialised comparison.** The executed comparator is a matched Hoeffding certificate and a full sparse solve. Degree-of-rate-control selection, goal-oriented adaptive modelling, local probabilistic conductivity methods, multifidelity strategies, and specialised domain decomposition have not been beaten under matched total resources.

**Generality and precision.** The finite-bit backend covers a structured reference with lazy exact rational coefficients. It does not implement arbitrary-graph reference certification, noisy physical coefficient acquisition, interacting-state discovery, or a general verified local solver.

**Originality.** Variational principles, local response problems, targeted scientific acquisition, and empirical Bernstein stopping have substantial prior art. The combined construction may be useful, but fundamental novelty is unknown. A new label does not change that status.

The result worth retaining is a precise candidate interface and a testable tradeoff: acquire paired local responses, use their discrepancy to control both macroscopic error and sampling effort, and explicitly reject regimes where local repair consumes the full coefficient budget. The current evidence does not justify a civilisation-level breakthrough claim.

## References and priority boundaries

[1] Quantum Package documentation, “Selected Configuration Interaction.” Official project documentation. https://quantum-package.readthedocs.io/en/master/intro/selected_ci.html

[2] Ryu et al., “Reducing Weighted Ensemble Variance With Optimal Trajectory Management,” arXiv:2504.21663 (2025). https://arxiv.org/abs/2504.21663 . Relevant specialised rare-event comparator; not implemented here.

[3] Zhong et al., “Goal-Oriented Bayesian Optimal Experimental Design for Nonlinear Models using Markov Chain Monte Carlo,” arXiv:2403.18072 (2024). https://arxiv.org/abs/2403.18072 . Prior art for targeting predictive quantities rather than full parameter identification.

[4] Stegelmann, Andreasen, and Campbell, “Degree of Rate Control: How Much the Energies of Intermediates and Transition States Control Rates,” Journal of the American Chemical Society 131, 8077–8082 (2009), DOI 10.1021/ja9000097. https://doi.org/10.1021/ja9000097 . Prior art for directing accurate calculations toward rate-controlling quantities.

[5] Grigoriu and Papoulia, “Effective conductivity by a probability-based local method,” Journal of Applied Physics 98, 033706 (2005), DOI 10.1063/1.1993775. https://doi.org/10.1063/1.1993775 . Prior art for obtaining effective conductivity through local probabilistic information. Detailed equivalence with the present candidate was not established.

[6] Beard, Stefan, Viator, and Welters, “Effective operators and their variational principles for discrete electrical network problems,” Journal of Mathematical Physics 64, 073501 (2023); arXiv:2210.05761. https://arxiv.org/abs/2210.05761 . Established effective-network and complementary variational framework.

[7] Maurer and Pontil, “Empirical Bernstein Bounds and Sample Variance Penalization,” arXiv:0907.3740 (2009), Theorem 4 and sample-variance concentration results. https://arxiv.org/abs/0907.3740 . Imported concentration inequality; the constants were checked against the paper.

[8] Mnih, Szepesvari, and Audibert, “Empirical Bernstein Stopping,” ICML (2008), DOI 10.1145/1390156.1390241. https://doi.org/10.1145/1390156.1390241 . Adaptive variance-based stopping is prior art.

[9] Cai, Chen, and Peng, “Effective Resistances in Non-Expander Graphs,” arXiv:2307.01218 (2023). https://arxiv.org/abs/2307.01218 . Different graph-access model from the known-reference coefficient interface here.
