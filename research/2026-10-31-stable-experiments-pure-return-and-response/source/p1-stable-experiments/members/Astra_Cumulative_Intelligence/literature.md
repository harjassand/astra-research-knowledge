# Literature and mathematical constraints for cumulative operator learning

Internal research notes, 2026-10-31. These distinguish known results, elementary derivations, and an unproved extension target. They do not establish novelty or a superiority theorem over an equally capable learner retaining the same information.

## 1. Findings that should constrain the proposal

1. Shared compositional representations of sequence tasks are already explicit in vector-valued weighted automata. Ordinary Hankel-rank acquisition, shared transition matrices, and linear readout transfer are not a new mechanism.
2. Low rank does not make a useful basis discoverable. Exact membership access alone can require exponentially many queries. A counterexample/equivalence oracle can supply precisely the missing information.
3. Known modern PSR learning results impose both an observability/conditioning condition and known core tests (or known core action sequences). Finite representational dimension is different from efficient acquisition.
4. Generic lifelong representation expansion, including adversarial task order, has modern theory based on task-eluder dimension. A direction-count argument should be compared against this literature.
5. Exact positive Gram closure is closely related to Krylov/GNS constructions and flat-extension moment theorems. Robust extraction from nearly flat moment data also has prior work.
6. Rank growth is an incomplete measure of cumulative learning: a new task can require much more precision within the same two-dimensional representation.
7. If a baseline has the same source access, retained observations, hypothesis class, and compute allowance, it can run the proposed algorithm. A legitimate claim is a cost theorem or improvement over specified algorithms, not a universal separation from equally strong retained learners.

## 2. Closest known results and exact qualifications

### 2.1 Exact active automata learning

Angluin (1987), *Learning Regular Sets from Queries and Counterexamples*, learns a minimal DFA in time polynomial in its state count and maximum counterexample length. A minimally adequate teacher supplies exact membership answers and exact equivalence answers or a counterexample. The paper discusses replacing equivalence queries with random sampling for PAC guarantees. That replacement changes the guarantee to distributional approximation; it does not give free worst-case equivalence.

- Primary paper: https://homepages.math.uic.edu/~lreyzin/papers/angluin87.pdf
- Retrieved reference: `turn6view4`.

Beimel, Bergadano, Bshouty, Kushilevitz, Varricchio (2000), *Learning Functions Represented as Multiplicity Automata*, uses the equality between minimal linear representation dimension and Hankel rank for exact learning. It improves earlier query algorithms. Therefore discovering a linear realization from exact counterexamples is established prior work.

- DOI: https://doi.org/10.1145/337244.337257
- Authors' institutional record: https://cris.technion.ac.il/en/publications/learning-functions-represented-as-multiplicity-automata/
- Retrieved reference: `turn3search2`.

Kaznatcheev and Panangaden (2021), *Weighted Automata Are Compact and Actively Learnable*, gives a concise linear analogue of Angluin–Schapire for arbitrary fields. It maintains a nonsingular Hankel block, constructs transition matrices, and uses each counterexample to add an independent row and column. Section 4 describes binary counterexample processing. For complete accounting, include the source values needed to populate all shifted Hankel tables, execution of the queried words, field/bit arithmetic, and the teacher's own cost. A count of counterexample-processing queries alone is not the full acquisition bill.

- Primary paper: https://arxiv.org/pdf/2011.10498
- Retrieved references: `turn19view2`, `turn20view1`, `turn21view0`.

### 2.2 Multitask weighted automata

Rabusseau, Balle, Pineau (NeurIPS 2017), *Multitask Spectral Learning of Weighted Automata*, already defines a shared compositional feature map

\[
\phi(w)^\top=\alpha^\top A_w,\qquad
f_i(w)=\phi(w)^\top\omega_i.
\]

The vector-valued automaton has a matrix of final weights and shared initial weights/transitions. A tensor/matricization of task Hankel blocks recovers the shared representation. Task relatedness is expressed by the dimension of a minimal joint realization relative to separate dimensions. The spectral reconstruction requires a complete finite Hankel block; finite-sample conditioning matters. This is the main direct overlap with a proposed shared operator basis. The paper treats a batch multitask setting, rather than proving charged adaptive source discovery for unknown future tasks.

- Primary paper: https://papers.nips.cc/paper_files/paper/2017/file/e655c7716a4b3ea67f48c6322fc42ed6-Paper.pdf
- Abstract: https://papers.nips.cc/paper_files/paper/2017/hash/e655c7716a4b3ea67f48c6322fc42ed6-Abstract.html
- Retrieved references: `turn8view0`, `turn11view0`, `turn6view0`.

### 2.3 Modern PSR learning already includes broad task transfer

Liu, Netrapalli, Szepesvári, Jin, *Optimistic MLE—A Generic Model-based Algorithm for Partially Observable Sequential Decision Making* (STOC 2023; arXiv v3, 2022), proves polynomial sample bounds for well-conditioned PSRs and includes reward-free learning. Section 4 assumes the candidate models share core tests known to the learner, permitting overparameterized tests. Its conditioning bounds future-error amplification. Proposition 4.2 gives an exponential-in-horizon sample lower bound even with constant observation, action, and core-test sizes when conditioning is absent. Section 7 already learns a model useful for all reward functions. Sample efficiency should not be conflated with polynomial-time optimization/planning.

- Primary full text: https://arxiv.org/html/2209.14997v3
- Key locations: §4.1 known tests; Proposition 4.2; Condition 4.3; Theorem 4.5; §7 reward-free learning.
- Retrieved references: `turn6view3`, especially `turn13view3`.

### 2.4 Lifelong representation learning is not only a static-rank story

Balcan, Blum, Vempala (COLT 2015), *Efficient Representations for Lifelong Learning and Autoencoding*, gives sequential algorithms for unknown shared linear and Boolean feature structure. The paper explicitly controls approximation-error propagation. Its linear-separator results use log-concave input distributions; Boolean results impose anchor conditions. It also treats a streaming setting retaining compact representations/hypotheses instead of all previous labeled data.

- Primary: https://proceedings.mlr.press/v40/Balcan15.pdf
- Retrieved reference: `turn12view2`.

Wang, Zhang, Vinayak (ALT 2026), *Bridging Lifelong and Multi-Task Representation Learning: An Algorithm and a Complexity Measure*, permits adversarially ordered tasks with a common representation and a well-specified noise model. The learner requests iid samples for the current task, tests whether its representation suffices, and invokes multitask ERM on stored failed tasks when necessary. Task-eluder dimension controls the number of costly updates. The theoretical algorithm assumes known Bayes risks/noise levels, Assumption 3. The representation and head classes are specified; generic ERM is a subroutine, not automatically a polynomial-time solver. This is a closer comparison than an independent-task baseline for any novelty-triggered representation expansion rule.

- Published primary page: https://proceedings.mlr.press/v313/wang26c.html
- Full arXiv text examined: https://arxiv.org/html/2511.01847v1
- Retrieved references: `turn12view0`, `turn13view1`, `turn17view0`, `turn19view3`.

### 2.5 Task-sensitive experimental design is established in observed dynamics

Wagenmaker, Simchowitz, Jamieson (ICML 2021), *Task-Optimal Exploration in Linear Dynamical Systems*, gives instance- and task-dependent local minimax bounds and a polynomial-time experiment-design method. The primary setting observes states in stable linear dynamics, with Gaussian process noise and an input-energy constraint; decision loss and its optimizer satisfy smoothness conditions. The result includes a finite-time burn-in and lower-order terms. It provides a strong comparator for claims that task-aware exploration buys only the information needed for a task. It does not itself solve unknown latent operator-basis discovery from scalar word moments.

- Primary: https://proceedings.mlr.press/v139/wagenmaker21a/wagenmaker21a.pdf
- Published page: https://proceedings.mlr.press/v139/wagenmaker21a.html
- Retrieved references: `turn19view0`, `turn20view2`, `turn17view1`.

### 2.6 Gram reconstruction and robustness have their own prior art

Burgdorf and Klep, *The Truncated Tracial Moment Problem*, studies finite-rank positive tracial moment matrices and flat-extension criteria for matrix representations. Klep, Povh, Volčič, *Minimizer Extraction in Polynomial Optimization Is Robust*, modifies GNS extraction for non-flat data and analyzes sensitivity under perturbations. These are warnings against presenting positive moment closure or robust finite operator extraction itself as a new theorem. A new result would need to concern acquisition access, costs, task dependence, or a genuinely stronger robustness guarantee.

- https://arxiv.org/abs/1001.3679 (`turn14academia50`)
- https://optimization-online.org/2017/10/6249/ (`turn17view2`)

## 3. Elementary lower bounds and checks

The arguments in this section are derived here, rather than claimed as novel research.

### 3.1 Rank-(L+1) singleton: why a counterexample oracle matters

Let an unknown secret string be \(s\in\{0,1\}^L\), and let

\[
f_s(w)=\mathbf 1\{w=s\}.
\]

Its Hankel matrix has rank exactly \(L+1\) over any field. The rows indexed by prefixes \(s_{1:i}\), and columns indexed by suffixes \(s_{j+1:L}\), for \(i,j=0,\ldots,L\), form an identity matrix: only equal split positions have total length \(L\), and those entries equal one. Every other nonzero row is a prefix row, giving the matching upper bound.

Nevertheless, until a membership query hits \(s\), all answers are zero. Each length-L query rules out at most one secret. Exact identification needs \(2^L-1\) queries in the worst case. Under uniform secret and at most q queries, any randomized learner has success at most \((q+1)/2^L\), by conditioning on its random seed and considering the all-zero path. Hence constant success needs exponential queries.

An equivalence query against the zero function immediately returns \(s\). This oracle grants exponentially valuable discovery information on this family. Reset does not remove the lower bound when all it permits is executing another chosen string.

Qualification: this is an exact/worst-case prediction obstruction. Under a distribution assigning mass \(2^{-L}\) to the exceptional word, the zero predictor is already good at constant PAC accuracy. The scoring distribution and task relevance must be specified.

### 3.2 Future readouts can expose previously invisible structure

Suppose \(f_i(w)=\alpha^\top A_w\omega_i\). The observable output subspace generated by existing tasks is

\[
V_t=\operatorname{span}\{A_w\omega_i: i\le t,\ w\in\Sigma^*\}.
\]

Old tasks identify only the quotient visible through this subspace. A new readout outside it can distinguish previously equivalent states. No learning rule can infer such a readout solely from old answers unless a relation tying it to old tasks is assumed or new source observations are allowed. Conversely, if a new task belongs to the established shared representation, readout fitting is ordinary transfer. Neither statement supplies an advantage over another learner retaining the same information.

### 3.3 Small closure defect does not certify arbitrary composition depth

Let \(A_\theta\) be a planar rotation, \(b=e_1\), and \(P=e_1e_1^\top\). Then

\[
\|(I-P)A_\theta P\|=|\sin\theta|,
\quad b^\top A_\theta^H b=\cos(H\theta),
\quad b^\top(PA_\theta P)^H b=(\cos\theta)^H.
\]

The one-step closure defect tends to zero with \(\theta\). For \(H\approx\pi/(2\theta)\), the true return tends to zero while the compressed prediction tends to one. Both operators are norm-nonexpanding. A small finite defect therefore needs an explicit horizon, discount, or stronger decay condition. Merely calling the system stable in the sense of bounded powers is insufficient.

With contractive generators and an orthogonal projection, the telescoping estimate gives a valid finite-horizon certificate. Write \(\widehat x_0=b\in\operatorname{ran}P\), \(\widehat x_j=PA_{a_j}P\widehat x_{j-1}\), and \(D_a=(I-P)A_aP\). Then

\[
\|A_{a_H}\cdots A_{a_1}b-\widehat x_H\|
\le \sum_{j=1}^H\|D_{a_j}\widehat x_{j-1}\|.
\]

Each squared term is a quadratic form in

\[
\Gamma_a=P A_a^*(I-P)A_aP.
\]

If accessible return-word moments determine this matrix, the bound can be evaluated on actual projected task trajectories, sometimes much more sharply than \(H\max_a\|D_a\|\). This is an elementary residual bound, related to established model-reduction error estimation; it is not the proposed novelty. Noise, adaptively selected basis, and moment-conditioning costs still need to be charged.

### 3.4 Stable rank can conceal new precision requirements

Consider noisy return-moment access

\[
Y_k=\cos(k\theta)+\xi,\qquad \xi\sim N(0,1),
\]

with independent noise and cost \(k\) for executing a length-k query. Let the requested task be estimating \(\cos(H\theta)\) to a fixed error below \(1/2\). Choose two alternatives

\[
\theta_0=\pi/(3H),\qquad \theta_1=2\pi/(3H).
\]

Both systems have Hankel rank two for sufficiently large H. Their task outputs are \(1/2\) and \(-1/2\). At any query length k,

\[
|\cos(k\theta_0)-\cos(k\theta_1)|
\le \min\{2,\pi k/(3H)\}.
\]

The Gaussian KL divergence of one observation is half the squared mean difference. Since \(\min\{1,x^2\}\le x\) for x≥0, this is at most \(Ck/H\). The chain rule applies to adaptive queries, so total KL is at most \(C\mathbb E[\sum k]/H\). Constant-success discrimination needs constant KL, hence expected acquisition cost \(\Omega(H)\). A constant number of queries at k=H achieves the matching order.

The obstruction persists at fixed representation dimension. It is a precision/information demand, not a new-rank event. With bounded short queries k≤L, each observation has at most \(O(L^2/H^2)\) KL under the displayed Lipschitz bound, so at least \(\Omega((H/L)^2)\) repetitions are necessary; near zero the cosine-only difference is even smaller. These are lower bounds for the stated noisy access model, not universal costs for exact arithmetic or different oracles.

For tasks encoded as compact exponents, retained precision can make many later evaluations cheap. If the input itself spells out a unary length-H word, reading that input already costs H; keep task description costs separate from physical experiment costs.

### 3.5 Pairing source replicas can identify reducible error without known noise risk

For independent repeated outcomes Y,Y′ at the same x, with conditional mean m(x), and a predictor f fit independently of the validation pair,

\[
\mathbb E[(Y-f(x))(Y'-f(x))\mid x]=(m(x)-f(x))^2.
\]

This standard double-sampling identity removes the need to know intrinsic noise variance in a squared-error sufficiency test. It is not free: repeatability, independence, replay/reset cost, and concentration cost must be stated. In a stochastic dynamical system, reproducing the same observable history may require rare-event conditioning; repeating an action sequence alone need not recreate the same conditional hidden state.

## 4. A defensible extension target

### Task-restricted statistical realization with charged source acquisition

The strongest opening identified here is to combine latent compositional model discovery with task-specific information acquisition, rather than propose another exact span certificate.

**Setting.** A stationary unknown finite-dimensional operator process is accessed only through explicitly allowed noisy scalar word moments. Query q costs c(q), including word execution, reset/replay and repetitions. Tasks arrive sequentially and specify bounded-horizon or discounted functionals \(F_t\) and error tolerances \(\epsilon_t\). The algorithm keeps all learned structure, uncertainty, and source data. Comparators receive the same access and retention rights.

**Representation uncertainty has two parts.** First, whether the model's observable quotient omits a task-relevant direction. Second, whether already represented directions have enough precision. An acquisition criterion must cover both.

In a locally identified smooth model \(\theta\), define source Jacobians \(\psi_q=\nabla_\theta\mu_\theta(q)\) and accumulated information

\[
M=\sum_q n_q\psi_q\psi_q^\top/\sigma_q^2.
\]

For a scalar task gradient \(g_t=\nabla_\theta F_t\), local variance is governed by \(g_t^\top M^\dagger g_t\), with infinite uncertainty if \(g_t\notin\operatorname{ran}M\). Parameterization must quotient out similarity/gauge directions of the latent realization. The local design benchmark is

\[
\min_{n_q\ge0}\sum_q n_q c(q)
\quad\text{subject to}\quad
g_t^\top M^\dagger g_t\le\epsilon_t^2
\quad (t\le T).
\]

This expression is standard experimental design locally. It is a comparison target, not a new theorem. A rigorous global method must also distinguish structurally different models consistent with old data; a local Fisher matrix alone can entirely miss the singleton obstruction.

**Nontrivial theorem to pursue.** Under explicit, source-testable coverage/conditioning assumptions, give a computationally efficient algorithm that (a) discovers a task-sufficient latent basis without a free equivalence oracle, (b) produces valid adaptive finite-noise confidence certificates, (c) reuses both basis and precision as tasks arrive, and (d) bounds total physical query and numerical cost against a clearly stated sequential or offline experimental-design comparator. Arbitrary task families may forbid a constant competitive ratio; restrict the family or prove the unavoidable dependence.

The work not supplied by the cited results is the bridge from raw allowed source access into the identifiable local regime, with global validity and explicit acquisition/conditioning costs. Existing spectral/GNS extraction starts later; generic task-eluder algorithms abstract away the operator identification solver; fully observed task-optimal system identification does not discover a latent realization.

## 5. Minimal evidence requirements for any experiment

- Same source interface, task stream, old data, memory budget, and compute budget for competing retained learners.
- Acquisition cost includes failed probes, teacher/counterexample search if used, source word length, resets, repetitions, matrix construction, precision/bit arithmetic, and fitting.
- Record prediction/decision quality on new compositions, not only reconstruction of acquired moments.
- Include the hidden-singleton family to test undisclosed discovery assumptions.
- Include long-horizon rotations or weakly coupled hidden modes to test precision and horizon validity at fixed rank.
- Include task-order shifts exposing previously invisible output directions.
- Use known shared-WFA learning, a retained multitask learner, and a task-aware acquisition baseline; independent relearning is a useful ablation but not the strongest baseline.
- Report ties as ties. A compact learned representation is useful even when another equally informed learner acquires the same one; that outcome cannot support an exclusivity claim.
