## Result: an extension to hard, densely overlapping assignment constraints

**I derived and implemented a sampling guarantee for quadratically interacting assignments with exact row-and-column constraints.** Every conditional sampling operation is explicitly implemented and charged. The result does not assume a permanent oracle or an efficient inner sampler.

The decisive change is that **covariance control is needed only inside a computable region of auxiliary fields—not under every possible field**. Outside that region, the chain stays at its current assignment. This preserves the original target distribution while avoiding the obstruction that stopped the previous proof.

The derivation is complete internally, but it has not been independently or formally verified. Historical originality remains unresolved.

01_guarded_overlap_proof.md[Full mathematical derivation](sandbox:/mnt/data/astra_overlap_frontier/01_guarded_overlap_proof.md) · 02_evidence_and_limits.md[Evidence and limitations](sandbox:/mnt/data/astra_overlap_frontier/02_evidence_and_limits.md) · astra_overlapping_assignment_handoff_2026-10-11.zip[Complete reproducible handoff](sandbox:/mnt/data/astra_overlapping_assignment_handoff_2026-10-11.zip)

## 1. The overlapping system now covered

Let \(z_{ij}\in\{0,1\}\), with

\[
\sum_j z_{ij}=1 \quad\text{for every row }i,
\qquad
\sum_i z_{ij}=1 \quad\text{for every column }j.
\]

Thus \(z\) is a permutation matrix: exactly one selection in each row and column.

These are **hard constraints**, not weak penalties. Every row constraint intersects every column constraint. Their constraint-incidence graph is \(K_{n,n}\), rather than a laminar tree. There are \(n!\) feasible assignments.

The target law is

\[
\boxed{
\mu(\pi)
\propto
\exp\!\left(
h^\top z(\pi)+\frac12\|Bz(\pi)\|^2
\right).
}
\]

Here \(B\) is an explicitly supplied matrix, or an explicitly constructed factor with charged evaluation costs. The quadratic term couples different assignment decisions. It is generally **not** equivalent to merely assigning a separate weight to each selected cell.

This is a substantive departure from the previous packet, whose concrete guarantees relied on laminar constraints or matroid bases and a covariance bound under every linear tilt. 01_stronger_regimes_proof

### Why the previous assumption fails here

Choose two permutations whose union is one long alternating cycle. External fields can make these two assignments dominate all the others.

Their incidence vectors differ in \(2n\) coordinates. An equal mixture therefore has covariance

\[
\frac14(z_1-z_2)(z_1-z_2)^\top,
\]

whose largest eigenvalue is

\[
\boxed{\frac n2.}
\]

Consequently, a dimension-independent covariance bound under **all fields** is unavailable for assignments. The new argument does not pretend otherwise.

## 2. The mechanism: restrict the update, not the target distribution

Write

\[
\nu_a(\pi)\propto e^{a^\top z(\pi)}
\]

for an ordinary weighted-assignment law. Introduce a Gaussian auxiliary variable through

\[
Y\mid z\sim N(Bz,I).
\]

The familiar Gaussian augmentation identity makes the conditional assignment law

\[
z'\mid Y=y\sim \nu_{h+B^\top y}.
\]

Gaussian augmentation and covariance-based analysis of such representations are established tools; they are not the claimed invention. [arXiv](https://arxiv.org/html/2407.16104v1)

The new construction uses a convex region \(D\) of auxiliary variables:

1. Draw **one** \(Y\sim N(Bz,I)\).
2. If \(Y\notin D\), retain the current assignment.
3. If \(Y\in D\), draw a new assignment from \(\nu_{h+B^\top Y}\).

Call this the **guarded update**.

### General theorem

Suppose that throughout \(D\),

\[
B\operatorname{Cov}_{\nu_{h+B^\top y}}(Z)B^\top
\preceq \theta I,
\qquad \theta<1,
\]

and that every feasible assignment satisfies

\[
\Pr\{N(Bz,I)\in D\}\ge s>0.
\]

Then the guarded chain is reversible, has **exactly the original \(\mu\)** as its stationary distribution, and obeys

\[
\boxed{
\operatorname{gap}\ge s(1-\theta).
}
\]

“Exact target” means the stationary law is unchanged. A finite run still produces an approximate sample, with its error bounded through the spectral gap.

### Why the holding step is essential

Repeatedly drawing \(Y\) until it enters \(D\) is **not equivalent**.

Let

\[
p(z)=\Pr\{N(Bz,I)\in D\}.
\]

That repeated-redraw procedure has stationary law

\[
\mu_D(z)\propto \mu(z)p(z),
\]

which is generally biased. Holding on rejection supplies the state-dependent waiting time needed to restore \(\mu\).

The completed four-row test gives a concrete distinction: the repeated-redraw chain’s stationary distribution is approximately **0.194676 away from the desired distribution in total variation**. The guarded chain preserves the target.

### The proof of the gap bound

Condition the joint Gaussian-assignment law on \(Y\in D\). Its auxiliary marginal has

\[
\nabla^2\log q_D(y)
=
-I+B\operatorname{Cov}_{\nu_{h+B^\top y}}(Z)B^\top
\preceq -(1-\theta)I.
\]

A strongly log-concave Poincaré inequality on the convex domain \(D\), together with conditional variance decomposition, gives the conditioned chain a gap of at least \(1-\theta\).

The guarded chain \(Q\) and conditioned chain \(P_D\) satisfy

\[
Q(z,\cdot)
=
p(z)P_D(z,\cdot)+(1-p(z))\delta_z.
\]

Their Dirichlet forms obey

\[
\mathcal E_{Q,\mu}
=
\bar p\,\mathcal E_{P_D,\mu_D},
\]

while

\[
\operatorname{Var}_{\mu_D}(f)
\ge
\frac{s}{\bar p}\operatorname{Var}_{\mu}(f).
\]

Combining them gives \(s(1-\theta)\).

This uses established Markov-chain comparison ideas. General spectral-gap comparisons for hybrid Gibbs and data-augmentation chains already exist; the restricted-field construction and its complete assignment application need their own priority audit. [arXiv](https://arxiv.org/html/2312.12782v4)

## 3. A computable assignment theorem—not a covariance oracle

The application requires a covariance estimate that can be certified from the input.

### Bounded-field covariance lemma

For a positive \(n\times n\) weight matrix \(W\), suppose

\[
\frac{\max_{ij}W_{ij}}{\min_{ij}W_{ij}}\le R.
\]

Under the weighted-permutation law proportional to \(\prod_iW_{i,\pi(i)}\), the internal derivation proves

\[
\boxed{
\operatorname{Cov}(Z)
\preceq
\frac{2R^2(1+R^2)}{n}I.
}
\]

The important dependence is **\(1/n\)**, rather than the order-\(n\) covariance possible under unrestricted fields.

The proof constructs a coupling between assignments conditioned to use different cells. A discrepancy can be passed between a row and a column; at each stage it terminates with probability at least \(R^{-2}\). This bounds the expected number of differing entries and then the absolute covariance row sums.

Permanent-based probabilities appear in the *existence proof of the coupling*. They are **not evaluated by the algorithm**.

### Input quantities that suffice

Set

\[
K=B^\top B,\qquad
\kappa\ge\|K\|_{\mathrm{op}},
\qquad
d\ge\max_e K_{ee}.
\]

Compute a bound

\[
M\ge
\max_{e,\pi}|h_e+(Kz(\pi))_e|.
\]

For each fixed cell \(e\), this is a **linear assignment optimization**, not quadratic assignment. It can be computed by ordinary assignment algorithms. A cheaper sufficient bound is

\[
M=
\max_e\left(
|h_e|+\sum_i\max_j|K_{e,(i,j)}|
\right).
\]

Choose \(L>M\), and define

\[
D=\{y:\|h+B^\top y\|_\infty\le L\}.
\]

Then put

\[
R=e^{2L},
\]

\[
\delta
=
2n^2\exp\!\left[-\frac{(L-M)^2}{2d}\right],
\]

\[
\theta
=
\frac{2R^2(1+R^2)\kappa}{n}.
\]

Whenever \(\delta<1\) and \(\theta<1\),

\[
\boxed{
\operatorname{gap}
\ge
(1-\delta)(1-\theta).
}
\]

The Gaussian tail calculation gives \(s\ge1-\delta\); the bounded-field lemma gives the covariance estimate.

**This theorem applies to any explicit factor passing the certificate.** The structured construction below demonstrates that the certificate admits growing rank and growing interaction strength; it is not the theorem’s entire scope.

### Initialization is also paid for

A late audit identified an important cost issue: the exact mean bound \(M\) does not necessarily bound the initial field \(h\). An affordable initial weighted-assignment draw therefore cannot simply be presumed.

The general solution is to compute a permutation \(\pi_*\) maximizing the **linear** score \(h^\top z(\pi)\). Its target probability satisfies

\[
\mu(\pi_*)\ge \frac{e^{-n\kappa/2}}{n!}.
\]

Writing \(\gamma=(1-\delta)(1-\theta)\), a sufficient number of rounds from this explicitly computed state is

\[
\boxed{
t=
\left\lceil
\frac{
n\kappa/4+\tfrac12\log(n!)+\log(1/(2\varepsilon))
}{
-\log(1-\gamma)
}
\right\rceil.
}
\]

When the initial field is bounded, the implemented weighted-core initialization improves the bound by removing the \(\tfrac12\log(n!)\) term. All recorded benchmarks satisfy that bounded-initial-field condition.

## 4. The inner sampler is explicit and its rejection costs are bounded

For every accepted auxiliary field, the algorithm must sample a weighted permutation. I implemented the established **Huber–Law nesting-rejection algorithm** for this step. Its nesting bound is explicitly documented in the permanent-sampling literature. [NeurIPS Proceedings](https://proceedings.neurips.cc/paper/2021/file/01d8bae291b1e4724443375634ccfa0e-Paper.pdf)

The procedure recursively selects the row assigned to a column using computable upper bounds on the remaining assignment weights. Any unused probability causes rejection of the attempt. The upper bounds telescope, so a successful attempt has exactly the desired weighted-permutation law in real arithmetic.

No exact permanent or conditional marginal is supplied.

Matrix scaling improves the acceptance bound. Combining the nesting bound with the established van der Waerden lower bound for doubly stochastic permanents gives a polynomial expected number of attempts when \(R\) is fixed. The permanent lower bound is imported mathematics, not a new result here. [arXiv](https://arxiv.org/html/0711.3496v2)

The derived expected arithmetic cost per inner draw is

\[
O\!\left(
Rn^2\log(n+2)
+
A_R\,n^{(R^2+3)/2}
\right),
\]

where \(A_R\) is an explicit, conservative constant depending only on \(R\).

For \(L\le1/3\),

\[
R\le e^{2/3},
\qquad
\frac{R^2+3}{2}\le3.396834.
\]

Thus the inner operation has a proved polynomial cost, rather than an assumed sampling interface.

The complete accounting additionally includes reading and storing \(B\), computing the certificate, Gaussian generation, matrix products, initialization, and numerical precision. A generic stored factor costs \(O(rn^2)\) space; the simple generic mean-bound calculation costs \(O(rn^4)\) arithmetic operations.

**Fixed bounded \(L\) is a real restriction of this implementation guarantee.** Arbitrarily increasing the allowable field range would not preserve its stated uniform polynomial bound.

## 5. Growing rank and growing interaction strength

The theorem is not restricted to a fixed number of weak modes.

For primes \(n\ge7\) with \(n\equiv3\pmod4\), index cells by \((a,b)\in\mathbb F_n^2\). For each nonzero \(x\in\mathbb F_n\), use the real and imaginary parts of

\[
\frac{\sqrt{2\kappa}}{n}
\exp\!\left[
\frac{2\pi i}{n}(ax^2+bx)
\right]
\]

as two rows of \(B\).

Character orthogonality gives

\[
BB^\top=\kappa I_{2(n-1)}.
\]

Consequently,

\[
\operatorname{rank}K=2(n-1),
\qquad
\|K\|_{\mathrm{op}}=\kappa,
\]

and all those nonzero eigenvalues equal \(\kappa\).

The construction annihilates the fixed row-and-column directions. Its spectrum is therefore not being inflated by interactions placed only in deterministic constraint directions.

Explicit bounds are

\[
d=\frac{2\kappa(n-1)}{n^2},
\]

\[
M\le
\frac{2\kappa(n-1)(\sqrt n+2)}{n^2}.
\]

Taking

\[
\kappa=\frac{\sqrt n}{64},
\qquad L=\frac13,
\]

gives

\[
\delta\le2n^2e^{-c\sqrt n}\longrightarrow0,
\qquad
\theta=O(n^{-1/2})\longrightarrow0.
\]

Therefore:

\[
\boxed{
\begin{gathered}
\text{number of nonzero modes}=2(n-1)\to\infty,\\
\text{strength of every mode}=\sqrt n/64\to\infty,\\
\text{sampling cost remains polynomial.}
\end{gathered}
}
\]

The interaction is not constant on feasible assignments. For a uniformly random permutation and \(H=\|Bz\|^2/2\), the derivation gives

\[
\mathbb EH=\kappa,
\qquad
\operatorname{Var}(H)=\frac{\kappa^2}{n}.
\]

At the displayed scaling, the variance is \(1/4096\). This establishes nonconstancy; **it does not establish a dramatic distributional effect or a lower bound against every competing sampler**.

The factor is also computationally explicit. The implementation evaluates \(Bz\) in \(O(n^2)\) operations and \(B^\top y\) with \(n\) Fourier transforms in \(O(n^2\log n)\), using \(O(n^2)\) storage rather than materializing \(K\).

## 6. What actually ran

### Matrix-free overlapping-assignment runs

| Assignment size | Binary indicators | Interaction rank | Nonzero eigenvalue | Burn + recorded rounds | Sampler time |
|---|---:|---:|---:|---:|---:|
| \(131\times131\) | 17,161 | 260 | 0.5 | \(52+600\) | 2.48 s |
| \(523\times523\) | 273,529 | 1,044 | 1.2 | \(155+300\) | 30.70 s |

The larger run completed **4,804 inner rejection attempts** and **1,365 balancing iterations**. These costs are inside the reported sampler time. Every returned object satisfied every row and column constraint.

Its analytical parameters give

\[
\gamma\ge0.647266,
\]

and the ideal warm-start bound reaches total-variation error at most \(0.01\) after 155 rounds.

These qualifications matter: the program uses floating point, the recorded states are correlated, compilation occurred in earlier tests, and there is no matched baseline for these two matrix-free runs. The mathematical bound is **not a certificate for the exact executed floating-point distribution**.

### Matched comparison: transpositions were faster

I also compared against Metropolis random transpositions on exactly the same four generic models. Each case used three seeds and 1,500 recorded states per seed.

The table reports the median minimum estimated effective samples per second across four observables.

| \(n\) / rank | Guarded sampler | Transposition sampler |
|---|---:|---:|
| 32 / 4 | 11,535 | **196,500** |
| 64 / 4 | 2,994 | **96,312** |
| 128 / 8 | 562 | **31,287** |
| 128 / 32 | 454 | **3,211** |

**These measurements do not support a speedup claim.** They show an implemented, affordable sampler with a derived guarantee; the stronger baseline is substantially faster on the tested models. Effective-sample estimates are diagnostics, not convergence proofs.

### Falsification and correctness checks

The packet retains 160 completely enumerated covariance tests, 48,000 independent inner-sampler draws, and 12,000 independent end-to-end restarts against an enumerated target.

A finite transition-matrix audit found a numerical guarded-chain gap of \(0.237201\), above the proved lower bound \(0.091326\). Increasing Gaussian quadrature from 120 to 200 nodes changed the kernel by approximately \(2.22\times10^{-16}\). The same audit exposed the substantial bias of the incorrect repeated-redraw construction.

The late deterministic-initialization implementation was separately tested with 2,000 independent restarts.

All inputs, returned states or histograms, rejection counts, timings, and qualifications are preserved in the astra_overlapping_assignment_handoff_2026-10-11.zip[evidence report and raw packet](sandbox:/mnt/data/astra_overlapping_assignment_handoff_2026-10-11.zip).

## 7. What new capability follows—and what remains unresolved

The concrete extension is:

> **Hard, densely crossing assignment constraints can be combined with a certified class of dense quadratic interactions and sampled to arbitrary requested accuracy, without requiring covariance control under every field and without hiding the conditional assignment computation in an oracle.**

A polynomial approximate-counting consequence also follows by a charged annealing reduction. That consequence is proved internally but not implemented.

Ordinary permanent approximation is not new: Jerrum, Sinclair and Vigoda established a polynomial-time randomized approximation algorithm for arbitrary nonnegative permanents. This work must not be presented as discovering tractability of ordinary weighted assignments. [ACM Digital Library](https://dl.acm.org/doi/10.1145/1008731.1008738)

The candidate contribution is the **restricted-field, exact-target transfer and its fully costed quadratic-assignment application**. Targeted searches did not identify an exact matching theorem, but that is not evidence sufficient to claim that no existing method provides the same guarantees.

The remaining boundaries are explicit. The result does not cover arbitrary forbidden-edge patterns, unrestricted fields or quadratic interactions, three-dimensional matching, or arbitrary intersections of strong constraints. Nor does it solve worst-case quadratic-assignment optimization.

The principal mathematical advance within this continuation is removing the **all-field covariance requirement** while preserving the original target and retaining a computable worst-state guarantee. The principal unresolved assessment is whether this precise theorem and application are genuinely new relative to the full sampling literature.

The handoff contains the complete derivation, implementation, failed mechanisms, raw experiments, initialization correction, source dependencies, and file hashes.

astra_overlapping_assignment_handoff_2026-10-11.zip[Download the complete overlapping-assignment handoff](sandbox:/mnt/data/astra_overlapping_assignment_handoff_2026-10-11.zip)

**No GitHub commit or pull request was created. Independent correctness and historical significance remain unestablished.**