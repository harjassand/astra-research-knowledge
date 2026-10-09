# Focused proof and primary-prior check

2026-10-09. One bounded AI check of the current candidate, its implementation, the existing comparison results, and nearest primary sources. This is not external review, formal verification, or priority certification. No extra reviewers or new large experiment were commissioned.

## Decision

**The exact finite-transform variance theorem and positive Hermitian realization survive this check.** I found no load-bearing mathematical error in Lemma 1 or Theorems 2–3. The specific moving-node, normalized-Pick endpoint result was not found in the primary sources inspected. This supports retaining a narrow research candidate; it does not establish publication-level novelty, numerical certification, or general practical superiority.

The practical claim should remain: with known atom count, exact reconstruction by a globally characterized scalar PSD boundary followed by a Hermitian eigensolve. Unknown-noise sparse free deconvolution, positivity/rank boundary estimators, and Loewner rational realization are established antecedents.

## Proof findings

1. **Strict backward feasibility is sound.** For delta=t-s>0, delta max K_ii(t)<1 gives absolute entrywise convergence of the geometric series. Schur powers are PSD. Positive diagonal makes the Gram vectors nonzero. If two Gram vectors coincided, inversion of u -> u/(1+t u) would force equal corresponding rows/diagonals in the original Cauchy Gram matrix, contradicting distinct z. A complex linear functional separates the finite set of nonzero vectors; tensor degrees 2 through m+1 give an invertible Vandermonde system. Equal transform values g_i are harmless.

2. **The finite endpoint theorem follows without a generic interpolation-sufficiency assumption.** At t0, actual atomic subordination gives S PSD of rank at most k-1. With m>=k it is singular. The backward lemma excludes every feasible t>t0 and includes all smaller t. The t0=0 case is covered.

3. **The realization extension is valid; expand its omitted row calculation.** Put H=K^(1/2), D=diag(w), and e=H^(-1)g. The identity DK-L=1g* becomes DH-HA=1e*. Thus row i of H is e*(w_i I-A)^(-1), since A is Hermitian and Im w_i>0. Multiplication by e gives g_i=e*(w_i I-A)^(-1)e. Moreover H^(-1)SH^(-1)=I-ee*: PSD and singularity imply ||e||=1. Spectral decomposition therefore gives a normalized positive measure. This uses K>0, not merely S>=0.

4. **m=k is the implemented realization regime.** At the true model K>0 by Cauchy invertibility and S has exactly one zero eigenvalue. For m>k, the variance theorem still holds but K is singular and the current realization routine needs rank reduction. Statements in PRIOR_BASELINE.md about “no atom-count input” should be qualified: the scalar theorem does not take k explicitly, but its guarantee requires sufficiently many nodes; the practical k-node estimator and comparisons use known k. They do not solve robust unknown-order selection.

5. **Normalized-Pick ancestry is especially transparent.** Define h_i=1/g_i-w_i. Then S_ij/(g_i conjugate(g_j))=(h_i-conjugate(h_j))/(w_i-conjugate(w_j)). Thus S is congruent to an ordinary half-plane Pick matrix for F(w)-w. This algebra reinforces the need to locate novelty in the particular moving-node path and endpoint theorem, rather than normalization or positivity by themselves.

## Narrow stability-note check

The load-bearing calculations in STABILITY_AND_FINITE_N.md are consistent: the uniform transform-to-S perturbation bound, simple-eigenvalue neighborhood, GOE Poincare constants, Gaussian concentration union bound, and integration-by-parts bias identity have the stated orders and constants. The derivative is S'=-(K Hadamard K). At m=k, strict positivity of K Hadamard K follows immediately from strict Schur positivity; the longer atomic divided-difference proof also works.

The statistical conclusion is conditional on fixed nonrandom nodes, exact empirical signal weights, t0>0, and eta^2>t0 for the elementary contraction/bias bound. It does not cover the data-dependent spectral-extent nodes used in the experiment. It is not a general Wigner local law or an atom/weight confidence theorem.

## Primary-source checks and scope

- **Ying (2025), Sparse free deconvolution under unknown noise level via eigenmatrix:** sections 3.1–3.2 use exactly z'=z-sigma^2 g; section 3.2 minimizes a singular-value objective, notes nonconvexity, and uses coarse-grid plus local search. Section 5 assumes known sparsity in the finite-N examples. This is the nearest same-model computational baseline. [Author PDF](https://web.stanford.edu/~lexing/fdc1.pdf), [DOI](https://doi.org/10.1016/j.acha.2025.101802).
- **Gautherat–Gayraud (2007 preprint), Parametric estimation in noisy blind deconvolution model:** equations (2.5)–(2.7) and section 3 explicitly use the first singular deconvolved moment matrix to identify Gaussian noise, followed by polynomial atom recovery and linear weight recovery. This decisively precludes a broad first-positivity-boundary/noise-identification claim. [Original preprint](https://arxiv.org/pdf/0711.0587).
- **Grabovsky (2022), Reconstructing Stieltjes functions from their approximate values:** Theorem 2.4 recalls Pick-matrix positivity and rational uniqueness on a singular boundary. Its half-line Stieltjes class is not literally the candidate's normalized real-line class. [Original preprint](https://arxiv.org/pdf/2101.02775).
- **Zhang–Gosea–Antoulas (2021), Factorization of the Loewner matrix pencil and its consequences:** section 2, Lemma 2.1, supplies the rational realization, Cauchy/Krylov factorization, rank, and pole-recovery mechanism. [Original preprint](https://arxiv.org/pdf/2103.09674).
- **Biane (1997), On the free convolution with a semi-circular distribution:** proves global semicircular subordination/conformal inversion and continuous density after positive semicircular convolution. Inference: an atomic signal cannot itself contain positive removable semicircular noise, so whole-law identifiability has a classical free-probability explanation. The candidate contribution is its finite-data criterion. [Original article, mirrored PDF](https://artefacts-discovery.researcher.life/full_text/DA-2/60/60545163c9ab3bc1acb346727b66d5b1/full_text/52e56cf77391d22ec0cea1d69b733e9f.pdf).
- **Arizmendi–Tarrago–Vargas, Subordination methods for free deconvolution:** Theorem 1.2 removes a known factor using inverse subordination at sufficient height; no finite unknown-variance Pick endpoint was identified. [Original preprint](https://arxiv.org/pdf/1711.08871).
- **Divisibility terminology warning:** the free divisibility indicator in Hasebe's section 7 is defined through the Belinschi–Nica/Boolean-power flow, not the maximum removable semicircular variance. It should not be silently identified with this estimator. Proposition 2.1 also recalls Im F(z)>=Im z. [Original paper](https://arxiv.org/pdf/1305.0924).

Bounded searches across free/semicircular deconvolution, divisibility, Pick/Nevanlinna, Loewner, normalized mass, and classical Gaussian moment boundaries did not locate an earlier exact version of this finite moving-node construction. Absence from this search is not proof of priority.

## Implementation and existing empirical evidence

I independently ran tiny checks, without changing the candidate code: k=1; t0=0; a standard k=3 exact case; m=5>k=3 feasibility; arbitrary finite probability-transform boundary realization; and a deliberate equal-g case. In the latter, z=(0.42i,1.92i), g=(-0.4i,-0.4i) recovered t=0.2, atoms (-1,1), and weights (0.5,0.5). Exact-case errors were approximately 1e-15. The arbitrary six-atom input sampled at three nodes produced a normalized three-atom boundary model with about 4e-15 interpolation error. These are implementation checks, not proof or robust error experiments.

The 16 matched N=1024 results have only four replicates per scenario. Pick's median W1 errors for (k,variance)=(3,.0625),(3,.5625),(5,.0625),(5,.5625) are approximately .000955,.0130,.00123,.1139. The 32-node fit has smaller median W1 in all four groups (.000514,.0125,.00107,.0984); the earlier short parent update said three, which was an arithmetic-reading slip. The same-node nonlinear fit can reproduce the Pick interpolant. High-noise k=5 has K condition numbers approximately 123,000–204,000. These results support speed/global-optimization advantages for the tested implementation, not a general accuracy advantage.

The prototype tests only negative imaginary parts and a diagonal upper bound. Its theorem-level input condition is still actual probability-transform data at distinct nodes. Arbitrary noisy complex values can violate S(0)>=0 and should not be treated as automatically covered. Floating eigenvalue signs, including near the true boundary, remain uncertified.


## Packaging clarification, 2026-10-09 13:40 UTC

The current prototype additionally checks S(0) for a materially negative eigenvalue and rejects it, without PSD projection. That guard was added during the work and is included in the final matched timing rerun. It does not replace the theorem-level actual probability-transform input assumption or certify floating-point PSD signs. The earlier paragraph describing only the imaginary-part/diagonal checks refers to the previously inspected prototype state. The atom-count wording in PRIOR_BASELINE.md has been corrected, and the current README reports lower median W1 for the 32-node fit in all four scenario groups. No extra audit was performed.
