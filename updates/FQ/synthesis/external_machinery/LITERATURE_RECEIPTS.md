# Selective primary-source proof receipts

Read date: 15 October 2026. Reconstructed conclusions are in `HEAT_TO_CRITICAL_TRACE.md`; source claims below are not silently promoted to externally verified mathematics. Acquired source hashes are in `source_manifest.json`.

## A. Bruno-Pasqualotto: actual planar quartic heat proof

Primary source: Giuseppe Bruno and Federico Pasqualotto, [Quasiconvexity for the Dacorogna-Marcellini Energy, arXiv:2608.06367v1](https://arxiv.org/html/2608.06367v1).

Read: Section 2, Lemma 3 and its proof; Section 3, exact-form construction and corrected quadratic blocks; Appendix A, the three-coefficient invariant cone and displayed square identity. In the web rendering these are approximately lines 132-190, 191-346, 347-422. The local HTML source is retained.

The source proves the Dacorogna-Marcellini threshold and the distinct class with both left and right rotational invariance. Its mechanism adds the pullback of an exact matrix-space two-form to the integrated heat second variation. It does not state a theorem for all nine coefficients with left rotational invariance alone. N794 already applies this method to a different explicit energy. The current transfer uses N794's strict margin, not the three-coefficient theorem as a substitute for the full cone.

## B. OpenAI Math: actual matrix heat proof, not a title analogy

Repository primary source: [openai/math at 1581d4cbdd69a0faf34b2089614fe2a814316a6a](https://github.com/openai/math/tree/1581d4cbdd69a0faf34b2089614fe2a814316a6a).

Read actual proof files in `preprints/The-maximal-triangular-Hilbert-transform-at-the-symmetric-point-September-24-2026/build/sections/`:

- [`matrix.tex`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-maximal-triangular-Hilbert-transform-at-the-symmetric-point-September-24-2026/build/sections/matrix.tex), lines 1-170: supported matrix Hessian and operator-order proof.
- [`heat.tex`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/The-maximal-triangular-Hilbert-transform-at-the-symmetric-point-September-24-2026/build/sections/heat.tex), lines 1-291: Gaussian-weighted stars, support preservation, heat identities, neighbor comparison, integrated dissipation proof.

The energy is `Phi(P)=tr(P^(3/2))` on PSD Grams. Its Hessian is the supported inverse of `L_sqrt(P)+R_sqrt(P)`. Neighbor costs are compared by PSD order, then Gaussian centers are integrated on `p0+p1+p2=d`. This is a specific finite-matrix entropy calculation, not a rank-one-convex-gradient theorem. The named positive-Gram representation transfer to `Fstar` is explicitly refuted by its negative value at the identity. No conclusion about the full triangular-Hilbert manuscript's external correctness is claimed from this selective read.

The full `trace.tex` file was acquired but not used as a premise. Its complete mixed-trace theorem was not independently audited here.

## C. OpenAI Math: actual recursive-potential proof

Read [`Midpoint-convexity-from-two-recursive-potentials-September-27-2026/build/sections/energy.tex`](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Midpoint-convexity-from-two-recursive-potentials-September-27-2026/build/sections/energy.tex), lines 1-75.

The two-field lemma uses nonnegative fields `P,Q,P',Q'` whose squares dominate child sums, a common nonnegative defect `d=P'-P=Q'-Q`, and one tight unprimed field at each internal node. Its proof sets a cubic-defect energy to the power `2/3`, applies Holder to two child sums, and telescopes to boundary leaves. These hypotheses were not constructed from arbitrary profile gradients. The lemma cannot be transferred merely because both problems use a word such as potential or compensation. The representation remains an incompatible interface, not a refutation of the source lemma.

Related constrained/free-root/linear tree files and the foundations/obstruction files were acquired for navigation. Their full proofs were not used.

## D. CLMS primary manuscript and the missing quartic closure

Primary source: R. Coifman, P.-L. Lions, Y. Meyer and S. Semmes, [Compacite par compensation et espaces de Hardy](https://www.numdam.org/item/SEDP_1989-1990____A16_0/), Seminaire EDP, expose XIV (28 November 1989), especially Theorem 1 on printed page XIV-2 and the proof sketches on XIV-4--XIV-5. This is an early primary account; the later journal article is not falsely reported as fully read.

Theorem 1 places the Jacobian in real Hardy space under Sobolev exponent summability. The scanned formula was visually checked on PDF page 5 (zero-based page 4), rather than trusting the incomplete OCR. The integration-by-parts/div-curl proof sketch was read. Section 10 of the report gives an independent scaled counterexample to the extra global `H^1`-BMO norm-product closure. It does not challenge the primary theorem.

## E. Flow interchange: exact applicability premises

Primary author manuscript: D. Matthes, R. J. McCann and G. Savare, [A family of nonlinear fourth order equations of gradient flow type](https://www.math.utoronto.ca/mccann/papers/MattesMcCannSavare.pdf), Theorem 3.2 and proof, printed page 17, equations (3.19)-(3.27).

The formula and proof were visually checked on PDF page 17 (zero-based page 16). The key comparison uses an actual minimizing-movement minimizer and its competitor evolved by an auxiliary EVI flow. Those assumptions do not follow from convexity in profile velocity. The result is background on method, not a positive premise of the trace theorem here.

## F. Trace topology

Primary source: Anatole Gaudin, [Homogeneous Sobolev and Besov spaces on special Lipschitz domains and their traces, arXiv:2305.01441v2](https://arxiv.org/html/2305.01441v2), Theorem 1.1 and discussion of the bounded-domain case.

The stated trace of `H^(1,4)=W^(1,4)` is `B^(3/4)_(4,4)=W^(3/4,4)` in the admitted bounded Lipschitz setting. Periodic cylinder charts give the same local trace scale. The report supplies its own elementary convolution-extension upper estimate, so it does not rely on a homogeneous whole-space quotient convention or on an unspecified Poisson calibration. No priority claim is made for this standard trace scale.

## G. Repository status and acquisition scope

The OpenAI repository README says its manuscripts have varying verification status. Its source descriptions and proof artifacts are not an independent correctness or novelty stamp. The complete acquired preprints tree and contents map provided navigation. Selective reading found no valid theorem that closes the full nine-coefficient destination obligation. That is a statement about the inspected transfers, not exhaustive absence of useful mathematics in the repository.

The positive transfer is consequently stated with the strict certificate from the pinned Astra source, whose algebra was replayed, and an explicit analytic proof supplied in this worker's report. Other collected texts are not counted as proofs read. No remote messages, repository changes, or publication actions were taken.
