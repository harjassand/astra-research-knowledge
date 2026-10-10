# Independent geometric-mechanism investigation

Date: 2026-10-10. This record concerns independently proposed mechanisms, not an audit of another manuscript.

## Outcome at this stage

No new dimension-free theorem or universal sampling operation has been proved. Three initial directions were screened before a targeted literature check:

1. **Covariance-normalized fiber symmetrization.** Center each one-dimensional conditional fiber, then restore covariance, hoping for a bounded cumulative energy cost. The missing step is a comparison of all Dirichlet energies, not just covariance. Even the elementary half-disk centering map has unbounded differential. Repeated isotropic normalization does not remove this issue.
2. **Geometry-normalized line refresh.** Divide the conditional-variance Dirichlet form by the conditional variance of the line coordinate. This makes every affine test exactly Euclidean, including on simplices. A precise analytic proof obligation was derived. It passes every Gaussian with sharp constant one, but the same sharp constant is false on balls. A cube-padding limit recovers the full ordinary gradient energy, with no constant loss, so the original Poincare obstruction survives intact. Crucially, the proposed continuous-time normalization has infinite stationary expected jump rate on a square. No finite-cost universal sampler follows.
3. **Reverse convolution with a covariance/entropy defect budget.** Attempt to reverse central-limit smoothing with a summable, dimension-normalized defect. A single exponential coordinate tensored with arbitrarily many Gaussian coordinates defeats a trace-averaged entropy-to-spectral-defect estimate. Replacing the trace budget by a worst-direction quantity reintroduces the unresolved mechanism; no useful reverse comparison was proved.

The strongest concrete products are counterexamples preventing false shortcuts, an exact simplex computation, and exact Gaussian/non-Gaussian tests of the normalized line form. These are research-screening results, not a foundational discovery claim.

## Target-status correction

After the mechanisms were explicit, current primary sources were checked. Two October 2026 arXiv records now claim dimension-free KLS: Bizeul–Klartag–Lehec, arXiv:2610.05474, submitted October 4; and Song–Zhang, arXiv:2610.01447, initially October 1 and revised October 4. This investigation has **not independently checked those proofs** and does not use their conclusions. Their existence means that an alternative route to the same inequality alone is not a credible novelty target without a distinct capability.

The parent therefore narrowed continuation to asking whether the normalized line form supplies a new geometric mechanism or a distinct sampling capability. The explicit clock obstruction prevents the latter inference; the former remains an unproved inequality, with substantial overlap with established hit-and-run Dirichlet-form and divergence-certificate methods.

## Exact analytic proof obligation

For a full-dimensional log-concave probability measure \(\mu\) on \(\mathbb R^n\), let \(u\) be uniform on \(S^{n-1}\). Write \(Y=P_{u^\perp}X\), \(s_u^2(Y)=\operatorname{Var}(u\cdot X\mid Y)\), and define

\[
Q_\mu(f)=\mathbb E_u\mathbb E_Y\frac{\operatorname{Var}(f(X)\mid Y)}{s_u^2(Y)}.
\]

The obligation was to prove a universal positive \(c\) such that

\[
Q_\mu(f)\geq\frac{c}{n\|\operatorname{Cov}\mu\|_{op}}\operatorname{Var}_\mu(f).
\tag{NC}
\]

All conditionings here are mathematical disintegrations, not assumed unit-cost sampling oracles. For affine \(f=a\cdot x+b\), the identity \(Q_\mu(f)=|a|^2/n\) holds for every admissible measure; this identity does not prove (NC) on nonlinear functions.

One-dimensional log-concave Poincare inequalities imply, with a numerical universal constant \(C_1\),

\[
Q_\mu(f)\leq\frac{C_1}{n}\int |\nabla f|^2\,d\mu.
\]

Consequently (NC) would imply the ordinary dimension-free covariance-normalized Poincare inequality. It is not a proof to insert that conclusion, or a sampler already known to mix by it, into the argument for (NC).

## Tests and stopping boundary

- Arbitrarily anisotropic Gaussians: proved (NC) with \(c=1\), in the accompanying test report.
- Uniform balls: affine tests are exact, but a two-dimensional cubic test space gives \(c<1\). A separate block-refresh example has a dimension-sized nonlinear obstruction invisible to all linear tests.
- Cube-padded fixed-dimensional log-concave bases: \(nQ\) converges to the base gradient energy. In particular, an exponential base forces every possible universal constant in (NC) to satisfy \(c\leq1/4\). This does not disprove a smaller positive universal constant.
- Uniform simplices: exact ordinary chord-refresh affine energy is order \(n^{-2}\), even in isotropic position. Inverse conditional variance cancels this at the level of affine forms, at an unaccounted clock cost.
- Product exponentials: mean matrix control fails to control the operator norm of a random Stein metric; the loss is logarithmic or squared logarithmic in dimension, exactly.
- Apparent thin necks: disconnected mixtures, annuli and curved thin tubes are not valid counterexamples because they are not log-concave. The negative examples retained here are genuine convex/log-concave families.

The investigation stops without asserting (NC), an efficient sampler, novelty, or a solution of KLS. Further work would need either a non-circular proof that (NC) yields a distinct capability, or a finite-cost operation retaining its normalization with a proved universal convergence theorem.
