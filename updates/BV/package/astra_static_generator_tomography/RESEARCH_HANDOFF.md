# ASTRA INDEPENDENT INVESTIGATION — STATIC GENERATOR TOMOGRAPHY

**Record date:** 2026-10-10 (Australia/Brisbane)  
**Status:** Independent analytic derivation, numerical self-checks, **unreviewed**, no established publication priority. **Not a 9–10/10 breakthrough.**  
**Key claim scope:** Elliptic continuous-state Itô diffusion; fully observed state; unknown common drift, unknown **constant** symmetric positive-definite diffusion, **known additive drift controls**; exact stationary distributions. Efficient sample-based full-drift recovery in large dimension **not established**.

## 1. Question and research opportunity

Can one recover irreversible stochastic dynamics from independently sampled, *time-unlabelled* stationary states under controlled perturbations, without trajectories or known rates?

One invariant distribution is insufficient: distinct nonreversible diffusions can have the same invariant law. Contemporary work already studies interventions and steady-state SDE identifiability, so the *general topic* is absolutely not new. The investigation sought an exact, mechanistically informative statement with explicit requirements and a genuinely executed implementation.

Competing problems initially considered: NP-hard worst-case fermionic-sign computation; rare-event simulation; nonparametric SDE system identification. The last was chosen because a specific identifiability obstruction could be attacked algebraically rather than proposing an unsupported general speedup.

## 2. Model and exact weighted static-response identity

Let \(\Omega=\mathbb R^d\) (with vanishing boundary flux/integrability) or a flat torus \(\mathbb T^d\). Consider

\[
 dX_t=(b(X_t)+u_i(X_t))dt+\sqrt{2D}\,dW_t,\quad i=0,\ldots,m-1.
\]

The unknown \(b:\Omega\to\mathbb R^d\) is common to all interventions. The unknown \(D=D^\top\succ0\) is a **constant** matrix, and the \(u_i(x)\) are *known* smooth control vector fields. In all numerical experiments the controls are constant vectors (so their divergences vanish). Assume strictly positive stationary \(C^2\) densities \(p_i\), smooth enough for the calculations, and stationary currents

\[
J_i=(b+u_i)p_i-D\nabla p_i, \qquad \nabla\cdot J_i=0.
\]

For any ordered pair, define \(r=p_i/p_j>0\), \(w=\nabla\log r\), and \(\delta u=u_i-u_j\). Then **for every admissible scalar test function \(q:(0,\infty)\to\mathbb R\)**,

\[
\boxed{\qquad
D:\underbrace{\mathbb E_{p_i}[q(r)ww^\top]}_{M_{ij,q}}
=\underbrace{\mathbb E_{p_i}[q(r)\,\delta u(X)\cdot w]}_{g_{ij,q}}.
\qquad}\tag{1}
\]

The density-gradient matrix \(M\) and right-hand side \(g\) are static observables of the controlled stationary laws and controls; the unknown drift \(b\) and stationary currents do not enter. \(q\equiv1\) is already useful; level-selective \(q\)'s yield more equations **from the same two conditions**.

### Proof

The exact current decomposition is

\[
J_i=rJ_j+p_i\bigl(\delta u-D\nabla\log r\bigr).
\]

Choose \(f\) with \(f'(r)=q(r)/r\). Stationarity gives

\[
0=\int_\Omega f(r)\,\nabla\cdot J_i
=\int f(r)J_j\cdot\nabla r + \int f(r)\nabla\cdot[p_i(\delta u-Dw)].
\]

The first integral vanishes: \(f(r)\nabla r=\nabla F(r)\) and \(\nabla\cdot J_j=0\). Integrating the second by parts yields

\[
0=-\int_\Omega p_i f'(r)\nabla r\cdot(\delta u-Dw)
=-\int_\Omega p_i q(r)\,w\cdot(\delta u-Dw),
\]

proving (1). This is an elementary current-cancellation identity; whether the precise formulation is already published remains unverified.

### Identifiability of \(D\) from the identities

Represent \(D\) in \(p=d(d+1)/2\) symmetric-matrix coefficients. Form \(A\in\mathbb R^{L\times p}\) by vectorizing \(M_{ij,q}\), including factor 2 on off-diagonal entries, and \(g\in\mathbb R^L\) by the corresponding \(g_{ij,q}\). **If \(\operatorname{rank}A=p\), then \(D\) is uniquely determined by \(A\theta=g\).** Neither a known initial drift nor trajectory data is needed.

For \(d+1\) regimes, the \(d(d+1)/2\) **unweighted pairwise equations** can already form a square full-rank system. Alternatively, two regimes can provide more equations through different \(q\)'s when their *conditional Fisher tensors* vary sufficiently across level sets of \(r\). Full rank is an **assumption to check**, not a universal property. In two-regime numerical experiments, this formulation was substantially less stable than using three regimes.

### Stability, assuming exact observable features

If the true design has smallest singular value \(\sigma_{\min}(A)>0\), and the learned design/right-hand side have operator errors \(\delta A,\delta g\), then for square invertible \(A\) (or suitably stable least squares), with \(\|\delta A\|<\sigma_{\min}(A)\),

\[
\|\hat\theta-\theta\|\le
\frac{\|\delta g\|+\|\delta A\|\|\theta\|}{\sigma_{\min}(A)-\|\delta A\|}.
\]

This is algebraic perturbation stability **only**. It does not bound the statistical errors in estimated density-ratio gradients, the time to achieve stationarity, or experimental intervention error.

## 3. Reconstruction of arbitrary nonlinear drift under a pointwise rank hypothesis

Set \(s_i=\nabla\log p_i\) and \(T_i=\nabla^2p_i/p_i\), and use \(p_0\) as reference. For \(i=1,\ldots,d\), subtract the stationary Fokker–Planck equations:

\[
(s_i-s_0)^\top b
=D:(T_i-T_0)-\nabla\cdot u_i-u_i\cdot s_i+\nabla\cdot u_0+u_0\cdot s_0.\tag{2}
\]

Define \(W(x)=[s_1-s_0,\ldots,s_d-s_0]\in\mathbb R^{d\times d}\) and \(h_i(x)\) as the right side of (2). Wherever \(W(x)\) is invertible,

\[
\boxed{\quad b(x)=W(x)^{-\top}h(x).\quad}\tag{3}
\]

**Theorem (conditional exact stationary generator identifiability).** Suppose there are \(d+1\) experiments sharing the same smooth drift \(b\) and constant diffusion \(D\), with known controls, exactly known positive stationary densities, an invertible pairwise matrix-feature system for \(D\), and \(W(x)\) invertible for almost every \(x\). Then \(D\) and \(b(x)\) a.e. are unique and given by (1)–(3), among all admissible generators in this model class.

**Proof:** Any compatible \(D\) satisfies the exact linear identities (1), so feature rank forces the same \(D\). Any compatible \(b\) satisfies (2), so pointwise rank forces (3). QED.

This is not a universal constructive high-dimensional solution. Evaluating (3) nonparametrically requires density scores and second derivatives and division by poorly conditioned \(W\).

### Lower bound / invisible currents

On \(\mathbb T^2\), **even two complete stationary densities and known \(D\) cannot uniquely identify general \(b\)**. For any positive \(p_0,p_1\), write \(r=p_1/p_0\) and choose a nonzero constant skew matrix \(S\). Set

\[
v(x)=p_0(x)^{-1}S\nabla r(x).
\]

Since \(\nabla\cdot(S\nabla r)=S:\nabla^2r=0\) and \(\nabla r\cdot S\nabla r=0\), both \(\nabla\cdot(p_0v)=0\) and \(\nabla\cdot(p_1v)=0\). Consequently \(b\) and \(b+\varepsilon v\) produce **exactly the same two stationary laws**, with identical \(D,u_0,u_1\), but different currents. Compactness ensures the perturbed field is smooth/bounded for smooth positive densities. This defeats the stronger claim that two static populations can determine full arbitrary drift.

## 4. Affine density-ratio regime: estimator needing no density derivatives to recover \(D\)

On \(\mathbb R^d\) assume the observed perturbed-to-baseline density ratios are **exact exponential tilts**

\[
p_i(x)=Z_i^{-1}p_0(x)e^{a_i^\top x},\quad i=1,\ldots,d,
\]

with \(A=[a_1\ \cdots\ a_d]\) nonsingular, and constant applied forces \(u_i\) with \(U=[u_1\ \cdots\ u_d]\). Set

\[
B=UA^{-1},\qquad D_*=(B+B^\top)/2,\qquad K_*=(B-B^\top)/2.
\]

**Corollary.** If these stationary laws are consistent with the model and constant positive-definite \(D\), then **necessarily**

\[
\boxed{D=D_*,\quad b(x)=B\nabla\log p_0(x).}\tag{4}
\]

Conversely, if \(D_*\succ0\) and the tilted densities normalize, (4) is a stationary generator with rotational current \(J_i=K_*\nabla p_i\).

**Proof:** For every pair, \(w_{ij}=a_i-a_j\) is constant; taking \(q=1\) in (1) gives

\[
(u_i-u_j)\cdot(a_i-a_j)=(a_i-a_j)^\top D(a_i-a_j).
\]

Including the baseline \(a_0=u_0=0\), diagonal and cross-pair equations imply \(A^\top U+U^\top A=2A^\top D A\). Thus \(D=\operatorname{sym}(UA^{-1})\). The score difference matrix in (3) is constant \(W=A\). Substitution into (2) gives \(b=UA^{-1}\nabla\log p_0\). Conversely \(b+u_i=B\nabla\log p_i\), hence \(J_i=(B-D)\nabla p_i=K_*\nabla p_i\), whose divergence vanishes since \(K_*\) is skew and Hessians are symmetric. QED.

The formula recovers **nonreversible** circulation \(K_*\), not just equilibrium gradient dynamics, and permits arbitrarily nonlinear \(\log p_0\). Under this exact structure, density-ratio logistic regressions on labelled independent stationary samples estimate \(a_i\) parametrically; estimating \(D,K\) does **not** require learning \(\nabla\log p_0\). Estimating \(b\) or entropy production *does*.

**Sharp worst-case intervention count within this family:** If fewer than \(d\) independent tilt directions have been observed, choose \(E\ne0\) with \(Ea_i=0\) for each observed \(i\). For small \(E\), \(\operatorname{sym}(B+E)\succ0\). Then the generator \(b'=(B+E)\nabla\log p_0\), \(D'=\operatorname{sym}(B+E)\) yields the same observed tilted stationary laws and applied forces. Thus fewer than \(d+1\) total regimes cannot ensure full generator identification even in this restricted family. In three dimensions, the code constructs such a second generator with \(\|B-B'\|_F=0.18\).

When \(A\) is estimated as \(\hat A=A+E\), the standard inverse perturbation inequality gives, if \(\|A^{-1}E\|_2<1\),

\[
\|\hat B-B\|_2\le \frac{\|B\|_2\|E\|_2\|A^{-1}\|_2}{1-\|A^{-1}E\|_2}.
\]

The experimental *force amplitudes*, condition number of \(A\), and density overlap determine whether this is useful with finite samples.

## 5. Recovering stationary irreversibility, conditional on score acquisition

For the baseline generator in the affine case, \(J_0=K\nabla p_0\). Under the usual overdamped stochastic thermodynamics convention with natural logarithms, stationary entropy production per unit time is

\[
\sigma=\int\frac{J_0^\top D^{-1}J_0}{p_0}\,dx
=\mathbb E_{p_0}\left[s^\top K^\top D^{-1}Ks\right],\quad s=\nabla\log p_0.
\]

The experiment `entropy_production_experiment.py` first estimates \(B\) by logistic stationary density ratios. It separately estimates the unknown symmetric quadratic potential coefficients and the quartic coefficient \(\lambda\) by **score matching on baseline position samples**, then plugs \(\hat s\) into the equation above. The quartic family is **known a priori**, an important supplied-information advantage. The reference sigma is estimated from 750,000 additional *exact independent* baseline draws, with 1,050,000 rejection proposals, not an analytical known value.

No direct measurements of entropy production or irreversible current were used to build the estimator. Nevertheless, without the known potential family, the expensive task of learning high-dimensional scores remains unresolved. Physical time-reversal semantics, observability of the full state, and model appropriateness must be verified for any application.

## 6. Reproducible calculations, failures and comparisons

All scripts are local and runnable. Environment: Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, scikit-learn 1.8.0; thread-limited BLAS used for tests.

### A. Three-dimensional exact-i.i.d. sampling, 25 repetitions per N

`stationary_tilt_experiment.py` generates four stationary laws with a **non-Gaussian quartic base potential**, \(D\) anisotropic and \(K\ne0\), by exact Gaussian-proposal rejection sampling. The quartic acceptance factor is \(\exp[-(0.35/4)\sum x_j^4]\le1\); all proposals are counted, and each accepted draw is independent. Controls \(u_i=0.9e_i\), log ratios \(a_i=B^{-1}u_i\); both the potential shape (in the ratio-estimation step) and \(B\) are treated as unknown.

| Stationary draws/condition | Total accepted | Relative error \(B\): classifier | Relative error \(D\) | Relative error \(K\) | Relative error \(B\): Gaussian-moment baseline |
|---:|---:|---:|---:|---:|---:|
| 500 | 2,000 | 12.53% | 12.72% | 11.70% | 14.51% |
| 2,000 | 8,000 | 7.23% | 7.63% | 6.26% | 8.99% |
| 8,000 | 32,000 | 3.80% | 3.84% | 3.47% | 5.31% |
| 32,000 | 128,000 | **1.70%** | **1.71%** | **1.52%** | 3.93% |

Mean over 25 seeded replications; relative Frobenius errors. At N=32,000, mean proposal count ~201,000 (acceptance fraction 63.6%); generation+fitting averaged **0.221 seconds on this local machine**. This time excludes any physical dynamics/relaxation, instrument costs, generator equilibration or preparation. The comparator is a **finite-force Gaussian-moment linear-response approximation**, not the strongest possible model-aware semiparametric competitor; the classifier estimates the exact log-density ratio family.

`proof_checks.py`: max absolute continuous Fokker–Planck residual at 1000 random points in four regimes was \(4.55\times 10^{-13}\); max pairwise Fisher identity residual \(4.44\times10^{-16}\). These are finite floating-point consistency tests only. For a second \(B'\) hiding from the first two controls, \(\|B-B'\|_F=0.18\) and \(\lambda_{\min}(D')=0.4475>0\).

### B. Two-dimensional periodic nonlinear irreversible model (no affine density ratios)

`general_identity_torus.py` solves the forward equation with a conservative second-order consistent **positive-rate, centered** Markov discretization of an explicitly specified 2D smooth non-gradient drift and \(D=\left[\begin{smallmatrix}.65&.12\\.12&.50\end{smallmatrix}\right]\). It never assumes linear density-ratio slopes. Solved stationary law arrays and central-difference score/Hessian fields are numerically acquired on successively refined periodic grids. The 3-regime \(D\) estimator uses one unweighted Fisher equation per pair; the 2-regime version uses seven level-selective weights of \(\log(p_1/p_0)\).

| Grid side N | Three-regime relative \(D\) error | Two-regime relative \(D\) error | Two-regime condition number | Drift relative RMS error, rank-stable cells |
|---:|---:|---:|---:|---:|
| 24 | 1.552% | 153.3% | 104 | 30.05% |
| 40 | 0.625% | 73.4% | 157 | 12.93% |
| 64 | 0.254% | 31.75% | 182 | 4.92% |
| 96 | 0.114% | 14.64% | 192 | 2.08% |
| 128 | 0.0647% | 8.34% | 195 | 1.18% |
| 192 | **0.0287%** | **3.74%** | 198 | **0.527%** |

At every grid size, roughly 89.7–89.8% of cells met the **predeclared local rank filter** \(\operatorname{cond}W<20\), \(\sigma_{\min}(W)>0.08\). The two-regime equations were **mathematically full rank but badly conditioned**. Their finite-grid error was large, decreased on refinement, and must be treated as a practical negative finding, not evidence of a useful reduced-intervention algorithm.

**Critical distinction:** These grid calculations used nearly exact deterministic solutions of a discretized stationary equation, not \(O(N^2)\) random observed stationary samples. They do **not** demonstrate that the full nonlinear drift can be learned statistically at the reported accuracy or cost. The grid itself scales exponentially with state dimension, and the calculations incur sparse stationary linear solves plus dense difference operations.

### C. Entropy production with learned potential, 12 repetitions

With the same 3D quartic model, potential coefficients are estimated from baseline samples using Hyvärinen score matching. \(\hat B\) is estimated from four labelled stationary populations. End-to-end static EPR estimates are compared with independent-sample reference \(\sigma_{\mathrm{ref}}\approx2.29734\) (nats per model time unit).

| Accepted draws/condition | Total accepted | Mean \(\sigma\) relative error: classifier + score matching | Mean \(\sigma\) error: finite-force moment comparator |
|---:|---:|---:|---:|
| 2,000 | 8,000 | 6.94% | 10.67% |
| 8,000 | 32,000 | 3.66% | 6.48% |
| 32,000 | 128,000 | **1.63%** | 6.19% |

Reference acquisition is a separate evaluation cost. The potential *family* is supplied; the coefficients are learned. The result is neither biological experimental proof nor a matched state-of-the-art evaluation.

## 7. Hard failure modes and open gates

1. **Stationarity is costly:** 4 independently prepared steady regimes in 3D, not 4 instantaneous reads. Unknown mixing times, slow metastability, perturbation calibration and instrument time can dominate all CPU work.
2. **Model misspecification:** If the force is not additive, the drift changes with intervention, the diffusion depends on state or condition, or observations omit latent variables, identifiability claims do not apply as stated.
3. **High-dimensional density-score acquisition:** A generic smooth \(p_i\) requires estimating \(\nabla p_i\) and \(\nabla^2p_i\); absent structural assumptions, this is statistically and computationally costly. The affine logistic shortcut does not extend to arbitrary \(p_i/p_j\).
4. **Feature-rank failures:** Pairwise matrices may fail to span \(\mathrm{Sym}_d\), or \(W\) may have zero singular values on physically relevant regions. Tiny singular values amplify observational error.
5. **Two-regime conditional-Fisher instability:** The numerical experiment found condition numbers 100–198 and poor finite-grid recovery compared with 3 regimes; obtaining theoretical rank is not equivalent to usable experimental inference.
6. **Invisible solenoidal currents:** One population never determines \(K\); two populations cannot determine arbitrary 2D drift, even if \(D\) is known (explicit gauge above).
7. **Finite sampling:** No nonasymptotic theorem from raw labelled samples to \(D\) and \(b\) in arbitrary dimension or low regularity has been proved. Logistic \(N^{-1/2}\) behaviour needs overlap and Fisher information assumptions.
8. **Numerical regularization/robustness:** No documented noise-corruption, partially observed system, force calibration drift or unknown relaxation stress-test; no physical validation.
9. **Priority:** The broad stationary inverse problem, Fokker–Planck algebra, nonreversible skew perturbations and SDE identification under interventions are already researched. Our exact identity might be well known in a different form, and this investigation did not establish novel priority through a complete primary-paper proof audit.

## 8. Prior literature, scope and novelty cautions

- Zweig, Lin, Azizi, Knowles (2026), *Towards Identifiability of Interventional Stochastic Differential Equations*, UAI/PMLR 337: https://proceedings.mlr.press/v337/zweig26a.html — tight linear SDE intervention results and nonlinear small-noise identifiability, explicitly using stationary snapshots. **Overlapping broad question**, different stated scopes; only accessible abstract/HTML summary was checked here, not every proof in the PDF.
- Salehkaleybar (2026), *One Intervention per Component is Enough*, ICML/PMLR 306: https://proceedings.mlr.press/v306/salehkaleybar26a.html — OU model, intervention structures and covariance methods. **Overlapping static identifiability**, not claimed superseded.
- Lund, Halter, Hubbard (2014), *Nonparametric Estimates of Drift and Diffusion Profiles via Fokker–Planck Algebra*, J. Phys. Chem. B 118:12743: https://www.nist.gov/publications/nonparametric-estimates-drift-and-diffusion-profiles-fokker-planck-algebra — algebraic estimates from evolving density snapshots, including reported experiment. **Direct precedent for density-based inverse techniques.**
- *Inversions of stochastic processes from their ergodic measures* (2026): https://doi.org/10.1515/jiip-2025-0098 — related inverse ergodic-measure identifiability, including distinctions for drift/diffusion. Detailed mathematical scope not audited here.
- *Accelerated Diffusion-Based Sampling by the Non-Reversible Dynamics with Skew-Symmetric Matrices* (2021): https://pmc.ncbi.nlm.nih.gov/articles/PMC8394571/ — familiar \(D+K\) nonreversible invariant-law construction, so the existence of stationary skew currents is **not itself original**.
- Troyer & Wiese (2005), *Computational Complexity and Fundamental Limitations to Fermionic Quantum Monte Carlo Simulations*, Phys Rev Lett 94 — alternative sign-problem frontier was passed over because existing worst-case hardness cannot be bypassed by a generic positive-weight trick.

**Novelty verdict:** Exact equations, conditional reconstruction theorem, affine special case, and explicit gauge falsifiers are independently derived and internally checked. They are **not** an externally validated discovery or priority-certified unpublished theorem. Recent published work means no appropriate historic-significance claim can presently be made.

## 9. Astra integration and revision-pinned research capital

GitHub connector used directly. **No repository writes were made**; this record resides in the output bundle.

- Astra: `harjassand/astra-research-knowledge` default branch `main`, accessed commit **`8aed7fd74eb14622ed5a0a3635a799374296e32a`**. Task-first router [`00_START_HERE.txt`](https://github.com/harjassand/astra-research-knowledge/blob/8aed7fd74eb14622ed5a0a3635a799374296e32a/00_START_HERE.txt), blob SHA `40a1421816ac0d651cff4bff1cb729d01d78e759`; [`agent/topics.txt`](https://github.com/harjassand/astra-research-knowledge/blob/8aed7fd74eb14622ed5a0a3635a799374296e32a/agent/topics.txt); [`agent/RESEARCH_WORKFLOW.txt`](https://github.com/harjassand/astra-research-knowledge/blob/8aed7fd74eb14622ed5a0a3635a799374296e32a/agent/RESEARCH_WORKFLOW.txt); current `frontier/PRIORITIES.md`. Searched selectively for stationary/SDE/Fokker terminology; not a full card audit.
- Read reviewed wrapper `N186-charged-EP-confidence-sequence` at this commit, blob SHA `e7ae3221633dc685fd91c184748cbe36ebabdba4`: existing research needs *charged stationary-start/mixing access* and controlled reversals; its external proof/priority remain unreviewed. **Bridge:** a future joint methodology could compare trajectory-based EP lower confidence bounds with snapshot-predicted EP only when model acquisition and intervention/equilibration are charged. Do not use this new conditional theorem to bypass those acquisition costs.
- Read reviewed wrapper `N498-dissipative-radial-material-clock`, blob SHA `118c7883b33bf75406752d18055e260bd8a7a25e`: source-derived 2D driven diffusion admits a reversible radial projection despite nonzero full-system entropy production. **Bridge:** losing state coordinates can destroy the matrix feature rank, directly falsifying naïve snapshot tomography from an observed projection. Existing N498 source remains unreviewed.
- Read reviewed wrapper `N340-fixed-stable-flow-undecidable-lifetimes`, blob SHA `30a9cb92a834d1f2267572f66776d7fe9af37221`: an unreviewed scoped claim about stochastic lifetime complexity despite fixed deterministic drift, unrelated to the current proof's direct premises. No dependency inferred.
- OpenAI comparative corpus `openai/math` accessed default commit **`fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb`**, [`CONTENTS.md`](https://github.com/openai/math/blob/fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb/CONTENTS.md), blob SHA `2c68c086fff36a5806c936ad1659cf1a8d0b6dd9`. Targeted code search for `Fokker Planck` found an unrelated heat-equation analysis section, not a directly comparable constant-force generator identification theorem. **Absence from this targeted search is not evidence of novelty.**

Potential Astra destinations: **Applied branch** (a conditional snapshot-tomography algorithm); **Natural Sciences branch** (design and physical calibrations of controlled perturbations, microscopic EP); **Primitive Genesis/Theoretical branch** (invariants \(\{M_{ij,q}\}_q\), invisible-current gauge, rank/identifiability lower bounds); **Ultra** (priority collision review and matched empirical testing). No branch has independently reviewed this work.

## 10. Decisions and handoff

**Delivered:** algebraic theorem and proof for static-response identities, sufficient generator-identification conditions, exact special affine family, explicit nonidentifiability constructions, four executable numerical experiments and deterministic proof checks. Tests include resource and failure reporting and preserve failed two-regime numerical recovery.

**Not delivered:** a fundamentally new universal high-dimensional scientific/computational capability, biological experiments, formal Lean proof, independent expert mathematical referee check, comprehensive publication priority clearance, or a matched benchmark against contemporary neural identifiability systems.

**Decisive remaining blocker:** Find an acquisition-complete estimator from *finite, noisy, correlated stationary samples* that reconstructs an unrestricted high-dimensional stochastic generator without prior low-complexity density structure, with controlled error and **subexponential dependence on dimension**, while preserving known irreversibility. The current exact equations do **not** address this information/statistics barrier.

### Reproduction commands

```bash
python proof_checks.py
OPENBLAS_NUM_THREADS=1 python stationary_tilt_experiment.py --sizes 500 2000 8000 32000 --reps 25 --seed 25016 --output results.json
OPENBLAS_NUM_THREADS=1 python general_identity_torus.py --sizes 24 40 64 96 128 192 --output torus_results.json
OPENBLAS_NUM_THREADS=1 python entropy_production_experiment.py --n 2000 8000 32000 --reps 12 --output entropy_production_results.json
```

Dependencies `numpy`, `scipy`, `scikit-learn`. Results are stored alongside the scripts. The generated evidence does not alter or upgrade source claim statuses in Astra.

## 11. Additional acquisition-complete restricted-model test: weak generator moments

Because the density-score acquisition in (2)–(3) is a major obstacle, I tested an alternative that avoids density derivatives **when a finite basis for the drift is supplied**. With \(b(x)=\sum_{k=1}^{P}\theta_k\psi_k(x)\) and known test functions \(\varphi_\ell\), the weak stationary identity is

\[
\boxed{\qquad
\sum_k\theta_k\,\mathbb E_{p_i}[\psi_k\cdot\nabla\varphi_\ell]
+D:\mathbb E_{p_i}[\nabla^2\varphi_\ell]
=-\mathbb E_{p_i}[u_i\cdot\nabla\varphi_\ell].\qquad}
\]

Every feature on both sides is a direct empirical average of known functions evaluated on stationary positions. No densities or score functions are estimated. However, the **choice of drift basis is privileged information** and need not be obtainable cheaply for unknown natural systems.

`weak_stein_torus.py` uses the same 2D nonlinear nonequilibrium periodic diffusion, with eight *supplied* Fourier drift coefficients and three unknown entries of \(D\), hence **11 unknown physical parameters**. It samples independent positions from the same 128-by-128 numerically stationary simulator under three controlled forces; 48 sine/cosine generator tests per condition produce 144 empirical linear equations. The estimator solves overdetermined least squares on exactly these observations. No trajectory order or stationary-density grid is passed to the estimator.

| Accepted draws per regime | Total accepted | Relative error of 8 drift coefficients | Relative error of \(D\) | Mean CPU sample-and-fit |
|---:|---:|---:|---:|---:|
| 1,000 | 3,000 | 52.7% | 73.1% | 0.020 s |
| 5,000 | 15,000 | 28.4% | 39.9% | 0.100 s |
| 20,000 | 60,000 | 11.0% | 14.6% | 0.390 s |
| 80,000 | 240,000 | **4.01%** | **5.50%** | 1.80 s |

Means from 12 seeded repetitions. Time excludes acquiring physical stationary distributions and simulator PDE solves, and the inferred generator carries discretization error from the synthetic source.

**Prior-art collision:** This is a familiar weak-form Fokker–Planck/Stein strategy, **not an original foundational invention**. Relevant direct precedents are:

- Bleile, Lumpp & Drton (AISTATS 2026), *Efficient Learning of Stationary Diffusions with Stein-type Discrepancies*: https://proceedings.mlr.press/v300/bleile26a.html — generator-based kernel Stein stationarity objectives with efficiency comparisons.
- *Weak collocation networks: A deep learning approach to reconstruct stochastic dynamics from aggregate data* (2025): https://www.sciencedirect.com/science/article/pii/S1007570425007695 — weak Fokker–Planck regression with aggregate data.
- Kuntz, Ottobre, Stan & Barahona (2016/2017), *Bounding Stationary Averages of Polynomial Diffusions via Semidefinite Programming*: https://doi.org/10.1137/16M107801X — polynomial stationary generator moment equalities and convex constraints.

The **specific pairwise current-elimination identity** in Section 2 might remain an independently interesting derivation, but neither the elementary Stein/moment estimator nor the generic problem of stationary SDE identification can be called novel. The strongest experimentally demonstrated advance remains conditional inference under carefully supplied models, not a new general computational capability. This test changes the research decision: the acquisition barrier *can* be avoided for a given low-dimensional generator basis, but obtaining/validating that basis and retaining a well-conditioned empirical design becomes the true difficulty.

## 12. Matched-information adversarial comparator: parametric score means

The affine density-ratio logistic estimator has **no demonstrated dominance** over competing estimators that exploit the same model's structure. A direct competitor uses the exact score identity, valid for \(p_i\propto e^{a_i^\top x}p_0\),

\[
a_i=-\mathbb E_{p_i}[\nabla\log p_0(X)].
\]

Indeed, \(\mathbb E_{p_i}[\nabla\log p_i]=0\), and \(\nabla\log p_i=\nabla\log p_0+a_i\). This gives a simple **score-moment estimator**: fit the baseline quartic potential coefficients by score matching from the same \(x_0\) samples and estimate each \(a_i\) by minus the perturbed sample mean of that fitted baseline score. Invert the resulting slope matrix to recover \(B\). It uses *exactly the same baseline and intervention sample populations and known controls as logistic regression*. It also exploits the **supplied quartic potential family** that the ratio method does not require; no true hidden parameter is passed in.

`matched_stein_comparator.py` executed 25 *paired* sample draws per size and compared this score-moment estimator, the ratio logistic estimator, and a finite-force Gaussian-moment baseline, charging every sample-generation proposal and fitting cost.

| Samples/condition | Total accepted | Relative \(B\) error: logistic ratio | Relative \(B\) error: fitted score-moment | Relative \(B\) error: Gaussian moment |
|---:|---:|---:|---:|---:|
| 500 | 2,000 | 14.46% | **13.68%** | 15.63% |
| 2,000 | 8,000 | 7.36% | **6.28%** | 8.44% |
| 8,000 | 32,000 | **3.27%** | 3.48% | 4.83% |
| 32,000 | 128,000 | 1.78% | **1.62%** | 3.84% |

The *paired* difference \(\mathrm{error}_{\mathrm{logistic}}-\mathrm{error}_{\mathrm{scoremoment}}\) at 2,000/condition was +1.08 percentage points, with descriptive Student-t 95% interval [+0.30,+1.86] percentage points. At 32,000/condition it was +0.156 percentage points with descriptive interval [−0.048,+0.360] percentage points, **including zero**. These intervals describe Monte Carlo replications of one synthetic distribution; they are not population-science uncertainty estimates.

**Decision:** The fitted score-moment baseline competes closely, and with its additional (supplied) potential-family structure can be better. Thus the logistic algorithm is a workable model-robust route to tilt slopes—not a new statistically dominant or generally transformative estimator. Further incremental optimization against this comparator is unlikely to clear Astra's historic-breakthrough threshold. The strongest surviving research object is the *exact current-cancellation identity and its structural identification boundary*, with practical high-dimensional acquisition still open.

Reproduce:

```bash
OPENBLAS_NUM_THREADS=1 python matched_stein_comparator.py --sizes 500 2000 8000 32000 --reps 25 --output matched_comparator_results.json
```
