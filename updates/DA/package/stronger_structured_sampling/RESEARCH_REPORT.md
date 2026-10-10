## Stronger result

**I derived a finite-size sampling guarantee that permits arbitrarily strong—and exact hard—structured constraints, with no penalty-strength dependence in the mixing bound.** I also extended the mechanism from nested count constraints to quadratically interacting matroid bases, including spanning trees.

This is substantially more usable than the previous small-\(rd\) regime. However, it is **not** a stronger theorem for arbitrary \(U\): it trades unrestricted interaction geometry for explicitly exploitable constraint structure.

The proofs are complete internal derivations, not independently verified. The implementations and benchmarks are completed, but use floating point rather than certified numerical arithmetic. The originality of the combined results remains unresolved.

01_stronger_regimes_proof.md[Full mathematical derivation](sandbox:/mnt/data/astra_quadratic_continuation/01_stronger_regimes_proof.md) · 02_evidence_and_limits.md[Evidence, benchmarks and limitations](sandbox:/mnt/data/astra_quadratic_continuation/02_evidence_and_limits.md) · astra_stronger_regimes_handoff_2026-10-11.zip[Complete reproducible handoff](sandbox:/mnt/data/astra_stronger_regimes_handoff_2026-10-11.zip)

## 1. The change that removes the strength restriction

The previous approach tried to prove that individual-coordinate updates mix despite the negative quadratic constraints. Its sufficient condition required an extremely small aggregate parameter and controlled Fourier tails. 01_main_proof

The surviving approach does something different:

> **Sample the strongly constrained part exactly, and use a Gaussian auxiliary variable to incorporate the remaining weak interactions.**

This avoids asking a single-site chain to cross barriers created by constraints—or to move outside an exactly constrained support.

Consider binary variables \(x\in\{-1,+1\}^n\). Let \(\nu\) be a tractable constrained distribution, and write its linear tilts as

\[
\nu_a(x)
=
\frac{e^{a^\top x}\nu(x)}
{\sum_z e^{a^\top z}\nu(z)}.
\]

The target is

\[
\mu(x)\propto
\nu_h(x)\exp\!\left(\frac12x^\top Kx\right),
\qquad K=B^\top B\succeq0.
\]

Here \(\nu\) contains the strong constraints. \(K\) contains the interactions not already handled by the constrained sampler.

### General contraction theorem

Suppose a fixed matrix \(C\succeq0\) satisfies

\[
\operatorname{Cov}_{\nu_a}(X)\preceq C
\qquad\text{for every }a\in\mathbb R^n.
\]

Define

\[
\theta=\|BCB^\top\|_{\mathrm{op}}.
\]

If \(\theta<1\), one complete round of

\[
Y\mid X=x\sim N(Bx,I),
\qquad
X'\mid Y=y\sim\nu_{h+B^\top y}
\]

satisfies the relative-entropy contraction

\[
\boxed{
D(\rho P\|\mu)\le \theta\,D(\rho\|\mu).
}
\]

The second step samples the **whole constrained configuration**, not one coordinate.

For the two concrete classes developed below,

\[
\operatorname{Cov}_{\nu_a}(X)\preceq2I,
\]

so a sufficient condition is simply

\[
\boxed{\|K\|_{\mathrm{op}}<\frac12.}
\]

The strength of the constraints inside \(\nu\) does not appear.

### An explicit initialization and round count

Initialize from the constrained base itself:

\[
X_0\sim\nu_h.
\]

With \(\kappa=\|K\|_{\mathrm{op}}\), the initial relative entropy is bounded by

\[
D(\nu_h\|\mu)\le \frac{n\kappa}{2}.
\]

Therefore

\[
\boxed{
\|\nu_hP^t-\mu\|_{\mathrm{TV}}
\le
\sqrt{\frac{n\kappa}{4}(2\kappa)^t}.
}
\]

For the implemented \(n=256\), \(\kappa=0.36\) models, this gives

\[
t=38
\quad\Longrightarrow\quad
\|\nu_hP^t-\mu\|_{\mathrm{TV}}
\le0.009345.
\]

**That is a usable finite number of full rounds, not an asymptotic guarantee whose first certified instances are astronomically large.** It is a bound for the ideal mathematical kernel; the floating-point implementation has not been certified to that total-variation tolerance.

## 2. First strong regime: nested count constraints, including hard constraints

Let

\[
N_A(x)=\sum_{i\in A}\frac{x_i+1}{2}
\]

count the selected variables in a subset \(A\). Consider a base distribution

\[
\nu_h(x)\propto
e^{h^\top x}
\prod_{A\in\mathcal L} f_A(N_A(x)).
\]

The family \(\mathcal L\) must be **laminar**: two sets are either disjoint or one contains the other. This includes hierarchical quotas and nested groups.

Each \(f_A\) must be a nonnegative log-concave sequence with interval support. Examples include

\[
f_A(k)=
\exp\!\left[-\frac{\gamma_A}{2}
(2k-|A|-b_A)^2\right],
\]

with **arbitrary \(\gamma_A\ge0\)**, and exact constraints such as

\[
f_A(k)=\mathbf 1_{\{k=q_A\}}.
\]

Multiple levels can be constrained simultaneously, provided the combined support is nonempty.

### The covariance lemma

I derived

\[
\boxed{
\operatorname{Cov}_{\nu_h}(X)\preceq2I
}
\]

uniformly over every field \(h\), every constraint strength, and every feasible coordinate conditioning.

The proof is elementary but depends on the nesting structure.

Upward subtree count distributions remain log-concave because convolution and multiplication preserve log-concavity. Increasing a subtree’s total count increases each leaf’s conditional inclusion probability. Conversely, log-concavity makes sibling counts compete: conditioning one sibling to have a larger count stochastically decreases the other.

Writing \(Z_i=(X_i+1)/2\), these facts give

\[
\operatorname{Cov}(Z_i,Z_j)\le0
\quad(i\ne j),
\qquad
\operatorname{Cov}\!\left(Z_i,\sum_j Z_j\right)\ge0.
\]

Thus, for \(\Sigma=\operatorname{Cov}(Z)\),

\[
\sum_j|\Sigma_{ij}|
=
2\Sigma_{ii}-\sum_j\Sigma_{ij}
\le2\operatorname{Var}(Z_i)
\le\frac12.
\]

Consequently \(\Sigma\preceq I/2\), and

\[
\operatorname{Cov}(X)=4\Sigma\preceq2I.
\]

The all-field quantifier is what permits the Gaussian algorithm to resample under its changing random fields.

### Why this is stronger than the earlier regime

In the 256-variable benchmark, the strong core contains **32 independent quadratic directions**, each of magnitude \(200\) when \(\gamma=25\). Larger \(\gamma\) is permitted without changing the mixing bound. Exact quotas are permitted directly.

The previous criterion fails dramatically on these inputs: even after allowing rank reduction, its \(\sqrt{rd}\) term exceeds \(28\), versus the required total error parameter of at most \(10^{-4}\).

This also returns to the original negative-quadratic setting. For a weak residual penalty

\[
\exp\!\left(-\frac12\|Vx\|^2\right),
\]

choose \(\tau\ge\|V\|^2\) and set

\[
K=\tau I-V^\top V.
\]

Since \(\|x\|^2=n\), the diagonal shift changes the energy only by a constant. Hence the method handles

\[
\text{arbitrarily strong nested negative constraints}
\;+\;
\text{an arbitrary negative residual with }\|V\|^2<\frac12.
\]

The number of strong constrained directions can grow proportionally to \(n\).

### The constrained sampler is not an oracle

For every random field, the count law is sampled by explicit tree dynamic programming: compute subtree count weights upward, draw the root count, and recursively draw child counts.

That exact recursive-cardinality machinery is established prior art, not an invention of this investigation. [arXiv](https://arxiv.org/abs/1210.4899)

The implemented stable, naive-convolution version costs \(O(n^2)\) arithmetic operations in a general tree. Independent blocks of size \(m\) cost \(O(nm)\). Matrix multiplication and factor construction are additional, charged costs. No normalizer, learned representation, or conditional-sampling oracle is supplied for free.

## 3. Why the Gaussian round actually contracts

The useful identity is an exact joint distribution:

\[
\pi(x,y)\propto
\nu_h(x)
\exp\!\left(-\frac12\|y\|^2+y^\top Bx\right).
\]

Its \(X\)-marginal is the target \(\mu\). Its two conditionals are exactly the two sampler steps.

The auxiliary marginal satisfies

\[
\nabla^2\log q(y)
=
-I+
B\operatorname{Cov}_{\nu_{h+B^\top y}}(X)B^\top
\preceq-(1-\theta)I.
\]

It is therefore strongly log-concave. The proof uses the established strong-log-concavity logarithmic Sobolev inequality; this analytical ingredient is not new. [arXiv](https://arxiv.org/abs/1807.09845)

The remaining argument converts that curvature into a **discrete sampler** guarantee. For \(f=d\rho/d\mu\), let

\[
g(y)=\mathbb E[f(X)\mid Y=y].
\]

The all-tilt covariance bound gives a sub-Gaussian moment bound and then

\[
\frac{\|\nabla g(y)\|^2}{g(y)}
\le
2\theta\,\operatorname{Ent}_{\nu_{h+B^\top y}}(f).
\]

The entropy chain rule decomposes the initial error into conditional and auxiliary contributions:

\[
D(\rho\|\mu)
=
\mathbb E_q\operatorname{Ent}_{\nu_{h+B^\top Y}}(f)
+
\operatorname{Ent}_q(g).
\]

Combining these relations bounds the auxiliary contribution by \(\theta D(\rho\|\mu)\). Returning from \(Y\) to \(X'\) cannot increase relative entropy.

This is why **constraint strength disappears while residual coupling remains**. There is no approximation of the strong constrained law in the proof.

## 4. A broader transfer: interacting matroid bases and spanning trees

The mechanism is not restricted to nested counts.

A matroid abstracts the exchange structure of linear-algebraic bases; spanning trees are a principal example. Let \(Z\) indicate a weighted random basis, and put \(X=2Z-1\).

Established matroid polynomial log-concavity implies

\[
\operatorname{Cov}(Z)\preceq\operatorname{diag}(\mathbb EZ).
\]

Apply the same theorem to the **dual matroid**, whose bases are complements. This gives

\[
\operatorname{Cov}(Z)
=
\operatorname{Cov}(1-Z)
\preceq
\operatorname{diag}(1-\mathbb EZ).
\]

Adding,

\[
2\operatorname{Cov}(Z)\preceq I,
\qquad
\boxed{\operatorname{Cov}(X)\preceq2I.}
\]

The deep matroid log-concavity theorem is imported from existing work, not claimed as an Astra discovery. [arXiv](https://arxiv.org/abs/1811.01816)

It follows that the same Gaussian sampler handles

\[
\mu(S)\propto
\exp\!\left[
h^\top(2\mathbf1_S-1)
+
\frac12(2\mathbf1_S-1)^\top K(2\mathbf1_S-1)
\right],
\]

where \(S\) is a basis and \(\|K\|<1/2\).

This is more than assigning independent weights to selected elements: the quadratic term couples their selections.

### The complete computation

For a general matroid, each inner weighted-basis sample can be approximated using the established basis-exchange walk. Its entropy contraction is supplied by Cryan–Guo–Mousa’s result. [arXiv](https://arxiv.org/abs/1903.06081)

The handoff explicitly charges the independence queries. Starting each inner walk at a maximum-weight basis gives initial entropy at most \(n\log2\), avoiding dependence on a potentially tiny minimum state probability. For rank \(k\), the resulting overall reduction uses

\[
O\!\left(
(t+1)nk\log\frac{n(t+1)}{\varepsilon}
\right)
\]

independence queries, plus arithmetic and numerical-precision costs.

For a finite-field matrix representation, those queries can be implemented by Gaussian elimination. **The generic matroid reduction is proved algorithmically but not implemented in the packet. The spanning-tree specialization is implemented.**

An additional check matters here: I enumerated a rank-4 binary matroid whose uniform basis law has a **positive pair covariance**. Thus this extension genuinely uses the primal–dual argument; it does not silently assume that all matroids have pairwise negative correlations.

## 5. Practical consequences: completed benchmarks

### Matched 256-variable experiment

The target combined 32 count-constrained blocks of eight spins with a dense residual of squared operator norm \(0.36\).

I compared the Gaussian/core sampler against single-site updates, a swap-plus-single-site method, and exact block updates. Every method received the same explicit model and started from the constrained base.

Each case used three seeds and 3,000 recorded sweeps or full rounds per seed.

The table reports the **median minimum estimated effective samples per second across four recorded observables**. These are autocorrelation-based empirical diagnostics, not convergence certificates.

| Constraint strength \(\gamma\) | Gaussian/core | Single site | Swap + single | Exact block |
|---|---:|---:|---:|---:|
| \(0.5\) | 9,074 | **12,842** | 11,645 | 1,994 |
| \(5\) | **9,162** | 53 | 6,088 | 1,538 |
| \(25\) | **6,592** | 0 | 5,532 | 1,364 |
| \(1000\) | 7,543 | 0 | **7,774** | 1,452 |
| Exact hard quotas | 8,229 | 0 | **8,853** | 1,839 |

The findings are specific.

**The penalty-strength failure of single-site updates is visible.** At \(\gamma=5\), they made only 262 recorded flips across all three traces. At \(\gamma=25\) and \(1000\), they made none. In the hard-constrained case, single-site moves cannot change a feasible configuration at all.

**The Gaussian/core method remains effective across the strength range.** Its median time for 3,000 correlated returned states was approximately \(0.177\)–\(0.246\) seconds.

**The stronger baseline prevents a universal speedup claim.** Constraint-preserving swaps remain competitive and outperform the implementation slightly at \(\gamma=1000\) and in the hard limit. Ordinary single-site updates win in the weak case.

The result is therefore a strength-independent guarantee and a working implementation—not evidence that Gaussian augmentation dominates every appropriate sampler.

The warmed timings do not hide compilation: a separate fresh-cache measurement recorded **10.47 seconds** for the six compiled benchmark primitives, excluding imports and process startup. Raw traces, parameters, timings and the interrupted earlier benchmark attempt are preserved.

### Larger nested constraints

The implemented nested-tree cases completed:

- **256 variables:** 38 burn rounds plus 1,000 recorded rounds in \(0.534\) seconds.
- **1,024 variables:** 42 burn rounds plus 1,000 recorded rounds in \(7.644\) seconds.

These cases contain strong constraints at multiple nested levels. They have no matched baseline, so they establish execution and scaling evidence, not superiority.

### Interacting spanning trees

For the complete graph on four vertices, I enumerated all 16 spanning trees and compared the exact interacting target with **4,000 independent sampler restarts**. The empirical histogram was consistent with finite-sample fluctuation; every output was a tree.

For an \(8\times8\) grid—64 vertices and 112 edges—the implementation completed 36 burn rounds and 1,000 recorded rounds in **0.518 seconds**, with every output connected and cycle-free.

The graph core uses established projection-determinantal sampling, not a new tree-generation primitive. Its QR and projection-update costs are included in the implementation. There is no matched interacting-tree baseline in this experiment.

## 6. Validation and the strongest falsifications

The proof was tested against **90 exhaustively enumerated core models** and **16,543 feasible coordinate conditionings**. The largest tested conditional covariance eigenvalue was approximately \(1.999644\), consistent with the bound \(2\).

A separate finite-kernel audit used Gaussian quadrature to test stationarity, reversibility and entropy contraction on hard-pair, nested-count and matroid examples. All tested entropy ratios satisfied the bound, including residual norms approaching \(1/2\). These checks support the derivation but do not replace it.

Two counterexamples sharply delimit the result.

### Arbitrary overlap is not covered

Consider

\[
\mu_\gamma(x)\propto
\exp\!\left[
-\frac{\gamma}{2}
\bigl((x_1+x_2)^2+(x_2+x_3)^2\bigr)
\right].
\]

The sets \(\{1,2\}\) and \(\{2,3\}\) overlap without nesting.

In the hard limit the support is

\[
\{(1,-1,1),\,(-1,1,-1)\}.
\]

Its covariance is \(ss^\top\), where \(s=(1,-1,1)\), so

\[
\lambda_{\max}(\operatorname{Cov}(X))=3>2.
\]

Thus the laminar covariance theorem cannot simply be extended to arbitrary intersecting constraints. This does not make the three-variable example computationally hard; it refutes the proposed general covariance mechanism.

### The \(1/2\) boundary is not merely a loose constant

Impose hard pair constraints

\[
x_{2j}=-x_{2j-1}
\]

and couple the remaining pair orientations through

\[
K=\kappa vv^\top,
\qquad
v=\frac{(1,-1,\ldots,1,-1)}{\sqrt n}.
\]

The auxiliary log-density has second derivative

\[
-1+2\kappa
\]

at the origin. The uniform Gaussian-convexity argument therefore breaks at \(\kappa\ge1/2\).

Again, this is a limitation of the mechanism, **not** a lower bound against all samplers. The example reduces to a count-structured Curie–Weiss model.

The handoff also preserves the failed Gaussian-smoothing shortcut that preceded this construction.

## 7. What is genuinely established—and what is not

The strongest defensible advance over the previous packet is:

> **A computable constrained part can absorb arbitrarily stiff interactions without imposing their stiffness on the mixing bound, provided its covariance is uniformly controlled under linear fields.**

The practical consequences demonstrated here are constrained binary sampling and quadratically interacting spanning trees. The matroid argument supplies a broader algorithmic transfer.

The novelty assessment remains restrictive. Gaussian augmentation and semi-log-concavity are established machinery. More importantly, Anari–Koehler–Vuong already proved a closely related result for a **single arbitrary-strength total-count penalty**, with the same \(1/2\) perturbation threshold, using polarized walks. Neither that special case nor the threshold itself is new here. [arXiv](https://arxiv.org/html/2407.16104v1)

The precise originality of the laminar extension, short entropy-contraction derivation and combined matroid transfer has not been cleared.

The unresolved mathematical obligation is now more specific: **obtain similarly chargeable computation for broad overlapping strong constraints, or cross the residual-coupling boundary using a mechanism that does not rely on uniform Gaussian convexity.** The present results do not establish either.

The packet includes the proofs, a usable generic laminar-sampling API, raw experiments, failed mechanisms, resource accounting, source dependencies and file hashes.

astra_stronger_regimes_handoff_2026-10-11.zip[Download the complete stronger-regimes handoff](sandbox:/mnt/data/astra_stronger_regimes_handoff_2026-10-11.zip)

**No GitHub commit or pull request was created. The outcome is a substantially stronger structured sampling capability with finite demonstrations—not an independently verified historic computational principle.**