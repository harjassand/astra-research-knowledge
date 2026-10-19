> Public selected edition of the 19 October audit. Original review SHA-256: `1822ec8316b3f8811add6b6965fe45ff4463645cdbd63ec4d053ea8b40040ff6`. Original scientific inputs are retained unchanged. Navigation and historical-receipt pointers are adapted to the selected public subset; mathematical statements, caveats and attribution are retained. Unselected ancillary source critiques and printed-matrix diagnostics are omitted, together with their nonessential checker branches. The main counterexamples, theorem-version pin, prior comparison and all limitations are retained. Past private-audit statements describe that audit, before approved publication. Current reproduction and retained-file hashes are in the release README and FILES.json.

# Independent embedding and prior-art audit

Audit date: 19 October 2026 (Australia/Brisbane). Public-source downloads were made on 19 October 2026 UTC. This review concerns exact finite, time-homogeneous continuous-time chains on the same observed states, with the sampling interval absorbed into the generator.

**Material verdict:** the implication (1) to (2) in **Theorem 3.16 of arXiv:2511.22800v1 is false as printed**. Both the private rational example and a construction from the integer generator printed in a 2020 public precursor satisfy its assumptions. They admit ordinary Markov generators but no reversible Markov generator. This conclusion follows from explicit spectral-block algebra below, with numerical exponentials serving only as diagnostics. The broad separation is therefore **not a first-example novelty claim**. The particular family, its closed feasibility boundary, and its quantitative entropy optimization require a much narrower novelty assessment.

This is a model-generated mathematical audit, not external peer review, a proof-assistant certificate, or a claim of community acceptance. No authors were contacted. No private manuscript text or private constants were sent to external services. All local output is confined to this review directory.

## Reading order and version boundary

I first retrieved the original v1 HTML, its definitions and the complete proof of Theorem 3.16 from arXiv. Only then did I read the private `reconstructed_markov_proof.md`, including sections 5–6. I did not import or execute either archive checker. The independent checker in this directory was written from spectral projectors and the public integer matrix.

The current arXiv landing page lists only v1, submitted **27 November 2025, 23:15:28 UTC**. The versioned PDF, current unversioned PDF, and Bielefeld institutional PDF downloaded in this audit are byte-identical: SHA-256 `26e25ea7cb52bc4ed9a2108e715f43fceb9adbcf94e2eb8c292f33ced1441af5` (457207 bytes). The retrieved PDF has 20 pages; its landing-page comment says 10 pages. Theorem 3.16 is on PDF page 12 and its proof continues on page 13. A focused title/identifier search and the current arXiv/institutional records did not reveal a replacement, erratum, withdrawal or retraction. That is a bounded search finding, not proof that no correction exists anywhere. The verdict here is pinned to v1; it does not attribute the v1 assertion to a hypothetical later revision. [Original v1 full text](https://arxiv.org/html/2511.22800v1), [current history](https://arxiv.org/abs/2511.22800), [institutional PDF](https://www.sfb1283.uni-bielefeld.de/preprints/sfb25065.pdf).

Other substantive version pins are:

| Source | Version inspected | Publication boundary |
|---|---|---|
| Casanellas, Fernández-Sánchez, Roca-Lacostena, open-set paper | arXiv:2005.00821v1, 2 May 2020; full HTML and 12-page PDF | DOI 10.1080/03081087.2020.1854165; online 17 December 2020; *Linear and Multilinear Algebra* 70(19), 3768–3779 (2022) |
| Baake–Sumner, dimensions at most four | arXiv:2311.02596v2, 19 June 2024; full HTML and PDF; publisher full HTML | DOI 10.1007/s00285-024-02112-w; published 2 July 2024 |
| Casanellas et al., general embedding problem | arXiv:2005.00818v2, 22 June 2021; full HTML; publisher PDF | *Publicacions Matemàtiques* 67(1), 411–445 (2023), DOI 10.5565/PUBLMAT6712308 |

The open-set paper's publisher metadata and Crossref record agree on its DOI and dates. An institutional accepted-manuscript PDF dated 15 January 2021 is indexed with the same integer generator, but direct retrieval returned 403/418, so it is not represented here as a downloaded full-text pin. The complete older mathematical reconstruction uses the successfully retrieved arXiv v1. [Open-set v1](https://arxiv.org/html/2005.00821v1), [publisher metadata](https://www.tandfonline.com/doi/abs/10.1080/03081087.2020.1854165), [accepted-copy record](https://upcommons.upc.edu/entities/publication/a8299721-188e-4b42-bf19-0209ec442db9), [Baake–Sumner v2](https://arxiv.org/html/2311.02596v2), [Baake–Sumner publication](https://link.springer.com/article/10.1007/s00285-024-02112-w), [general paper publication](https://mat.uab.cat/pubmat/articles/view_doi/10.5565/PUBLMAT6712308).

Complete fetched-file hashes, URLs and retrieval times are in `public_source_manifest.json`.

## Exact scope of the disputed theorem

In v1, a Markov matrix is row stochastic, a generator has zero row sums and nonnegative off-diagonal entries, and reversibility means detailed balance for some **strictly positive** probability vector. Positive spectrum permits multiplicities. Theorem 3.16 asserts, for a reversible matrix, equivalence of: (1) ordinary embeddability with positive spectrum; (2) embedding with a generator reversible for that same probability vector; and (3) positive spectrum with a principal logarithm that is a generator. It does **not** assume simple spectrum, irreducibility, symmetry, or a normal embedding generator. Its earlier Proposition 3.12 has the simple-spectrum restriction; Theorem 3.16 attempts to remove it. [Definitions and Theorem 3.16, v1](https://arxiv.org/html/2511.22800v1#S3.Thmtheorem16).

The legitimate reversible-embedding criterion is narrower: for reversible positive-spectrum \(P\), a reversible generator exists exactly when its principal logarithm is a generator. This does not decide existence of arbitrary nonreversible generators. Uniqueness of a reversible embedding was already treated by Jia in 2016. [Jia, Theorems 1–2](https://arxiv.org/html/1605.03502).

For clarity, the uniqueness argument needed below can be proved directly. If an irreducible sampled matrix \(P\) has stationary vector \(\rho>0\), any reversible generator \(Q\) with \(e^Q=P\) must be reversible for \(\rho\): a reversible distribution of \(Q\) is stationary for \(e^Q\), and \(P\)'s stationary distribution is unique. Then \(D_\rho^{1/2}QD_\rho^{-1/2}\) is symmetric. A symmetric logarithm of a symmetric positive definite matrix is unique, because its real eigenvalues are uniquely determined by exponentiation on every eigenspace. Hence \(Q=\log P\). A negative off-diagonal entry of \(\log P\) excludes every reversible generator, not merely a particular parametrization.

## Independent rational counterexample

Let

\[
J=\mathbf1\mathbf1^T/4,\quad
v=(1,-1,0,0)^T/\sqrt2,\quad
u=(1,1,-1,-1)^T/2,\quad
w=(0,0,1,-1)^T/\sqrt2.
\]

These vectors, together with \(\mathbf1/2\), are an orthonormal basis. Set \(V=vv^T\), \(E=uu^T+ww^T\), \(a=8\log2\), \(b=18\log2\), \(t=2\pi/\sqrt7\). Rebuilding the sampled matrix from the projectors gives

\[
P=J+2^{-8}V+2^{-18}E
=\frac1{1048576}
\begin{pmatrix}
264193&260097&262143&262143\\
260097&264193&262143&262143\\
262143&262143&262147&262143\\
262143&262143&262143&262147
\end{pmatrix}.
\]

It is strictly positive, symmetric and row stochastic, with spectrum \(1,2^{-8},2^{-18},2^{-18}\). Its stationary distribution is uniquely uniform. Its principal logarithm is \(L=-aV-bE\), and

\[
L_{12}=a/2-b/4=-\tfrac12\log2<0.
\]

Define, entirely within the repeated eigenspace,

\[
R=t(uu^T-ww^T)+2\sqrt2t(uw^T-wu^T),\qquad Q_0=L+R.
\]

In the \(u,w\) basis the \(R\)-block is

\[
\begin{pmatrix}t&2\sqrt2t\\-2\sqrt2t&-t\end{pmatrix},
\qquad R^2=-7t^2E=-4\pi^2E.
\]

It vanishes on the other two eigenspaces, commutes with \(L\), and has exponential equal to the identity. Thus \(e^{Q_0}=e^L e^R=P\) **exactly**. The generator is

\[
Q_0=\frac14\begin{pmatrix}
-2a-b+t&2a-b+t&b+3t&b-5t\\
2a-b+t&-2a-b+t&b+3t&b-5t\\
b-5t&b-5t&-3b-t&b+11t\\
b+3t&b+3t&b-5t&-3b-t
\end{pmatrix}.
\]

All row and column sums vanish. The only nontrivial positivity tests are \(b>5t\) and \(2a-b+t>0\). Exact elementary estimates suffice: \(\log2>2/3\) implies \(b>12\); \(\pi<22/7\) and \(220^2<84^2\cdot7\) imply \(5t<12\). Also \(\pi>3>\sqrt7\) gives \(t>2>2\log2=b-2a\). Thus every off-diagonal entry is strictly positive. Its spectrum is

\[
\{0,-8\log2,-18\log2+2\pi i,-18\log2-2\pi i\}.
\]

Therefore \(P\) satisfies condition (1) of v1 Theorem 3.16 but not (2) or (3). The no-reversible-generator conclusion follows from the direct uniqueness argument above; it does not use the disputed theorem. \(Q_0\) is visibly not symmetric, since \(q_{13}-q_{31}=2t\ne0\).

Independent numerical diagnostics at 100 decimal digits gave

\[
\min_{i\ne j}(Q_0)_{ij}=0.1506362832104390\ldots,
\quad \max_{ij}|(e^{Q_0}-P)_{ij}|=1.79\times10^{-102}.
\]

The exact block identity, not this residual, proves the exponential equality.

## Independent older-work construction

The public v1 Example 3.2 prints the integer matrix

\[
H=\begin{pmatrix}
-21&4&16&1\\7&-9&1&1\\1&1&-9&7\\1&16&4&-21
\end{pmatrix}
\]

as \(4/\pi\) times a Markov generator. Its off-diagonal entries are all positive integers and its row sums are zero, so \(\pi H/4\), and also \(\pi H\), are generators directly from their entries. The following is a fresh derivation from \(H\); the paper does not need to have stated the resulting reversible consequence. [Casanellas et al., Example 3.2, PDF pages 4–5](https://arxiv.org/pdf/2005.00821v1).

Exact calculation gives

\[
\det(zI-H)=z(z+28)((z+16)^2+36),\qquad
\rho=(1/7,5/14,5/14,1/7).
\]

The stationary vector was reconstructed from \(H^T\rho^T=0\), not assumed. An eigenvector for \(-28\) is \(r=(-5,2,2,-5)^T\). Its spectral projectors, with \(D=\operatorname{diag}\rho\), are

\[
E_1=\mathbf1\rho,
\quad E_{28}=\frac{r(r^TD)}{r^TDr}
=\frac1{14}\begin{pmatrix}
5&-5&-5&5\\-2&2&2&-2\\-2&2&2&-2\\5&-5&-5&5
\end{pmatrix},
\]

\[
E_{16}=I-E_1-E_{28}
=\frac12\begin{pmatrix}
1&0&0&-1\\0&1&-1&0\\0&-1&1&0\\-1&0&0&1
\end{pmatrix}.
\]

Set

\[
T=-28E_{28}-16E_{16}
=\begin{pmatrix}
-18&10&10&-2\\4&-12&4&4\\4&4&-12&4\\-2&10&10&-18
\end{pmatrix},
\]

\[
C=H-T=\begin{pmatrix}
-3&-6&6&3\\3&3&-3&-3\\-3&-3&3&3\\3&6&-6&-3
\end{pmatrix}.
\]

Direct rational identities show that the projectors are pairwise orthogonal, \(TC=CT\), \(CE_{16}=C\), \(C^2=-36E_{16}\), and \(DT=T^TD\). Consequently \(e^{\pi C}=I\), and

\[
P_{\rm old}:=e^{\pi H}
=e^{\pi T}
=E_1+e^{-28\pi}E_{28}+e^{-16\pi}E_{16}.
\]

This is a strictly positive Markov matrix because it is the exponential of an irreducible generator; its spectrum is \(1,e^{-28\pi},e^{-16\pi},e^{-16\pi}\). The displayed weighted symmetry of \(T\), or that of both projectors, proves \(DP_{\rm old}=P_{\rm old}^TD\). Thus it is reversible for \(\rho>0\). Its principal logarithm is exactly \(\pi T\), since \(T\) is diagonalizable with real eigenvalues \(0,-28,-16,-16\). Its \((1,4)\) entry is \(-2\pi<0\). The direct uniqueness argument again excludes every reversible embedding, while \(\pi H\) supplies an ordinary embedding.

Equivalently, define \(M_*=e^{\pi H/4}\). Then \(P_{\rm old}=M_*^4\). This establishes the broad separation from a public 2020 integer generator without attributing a new theorem to the older paper. Its published open-set result concerns general four-state matrices and complex eigenvalues; the reversible positive-spectrum consequence above is our explicit mathematical corollary.

The independent 100-digit residual was \(6.43\times10^{-101}\) for \(e^{\pi H}\) against the projector formula, and \(6.07\times10^{-101}\) for \(e^{\pi T}\). The minimum off-diagonal entry of \(\pi H\) is exactly \(\pi\). These diagnostics corroborate the rational identities.

The older-work proof uses the exact integer H and projectors, never a rounded transition matrix.

## The invalid inference in the v1 proof

The v1 proof combines ambient density of simple-spectrum embeddable matrices with reversible row/column deformations. The cited results establish the two properties separately: Davies's Theorem 7 gives density **inside all embeddable matrices**, by perturbing generators; Brill et al.'s Theorem 3.1 preserves **reversibility** under the specified modifications of transition matrices. Neither states that these latter modifications preserve embeddability or that Davies's approximants can be chosen reversible. Their combination does not justify the simultaneous simple + reversible + embeddable approximants required by the proof. [Davies, Theorem 7](https://arxiv.org/html/1001.1693), [Brill et al., Theorem 3.1](https://arxiv.org/html/1806.10154).

Here is a direct obstruction, stronger than merely identifying an unsupported step. The principal matrix logarithm is continuous in a neighborhood of the rational \(P\), whose spectrum avoids the nonpositive real axis. Since \((\log P)_{12}<0\), this entry remains negative throughout a sufficiently small neighborhood. Every reversible matrix there has real positive spectrum. If it also has simple spectrum, its only real logarithm is its principal logarithm, so it cannot be ordinarily embeddable. Therefore **no** reversible, simple-spectrum, embeddable sequence can approach this \(P\), irrespective of how its stationary distributions are chosen. The crucial approximating sequence is impossible, rather than just unproved.

An explicit family illustrating the obstruction is

\[
P_\epsilon=J+2^{-8}V+2^{-18}(1+\epsilon)uu^T
+2^{-18}(1-\epsilon)ww^T,\qquad0<\epsilon<1.
\]

These matrices are symmetric, strictly positive and stochastic; their four eigenvalues are positive and distinct. But

\[
(\log P_\epsilon)_{12}
=-\tfrac12\log2+\tfrac14\log(1+\epsilon)
<-\tfrac14\log2<0.
\]

They approach the embeddable \(P\) while being nonembeddable themselves. Conversely Davies's embeddable simple approximants must leave the reversible class near \(P\). This is fully compatible with ambient density.

The implication (2) to (1), equivalence (2) with (3), and the simple-spectrum statement do not fail for this reason. An additional normality/commutation hypothesis on an embedding generator and its time reversal can also support symmetrization; the rational \(Q_0\)'s repeated-eigenspace block is nonnormal, so that repair would not cover it.

## Strongest earlier results and novelty limits

The 2023 general four-state paper treats the exact spectral type \(\operatorname{diag}(1,\lambda,\mu,\mu)\). Its Theorem 5.11 exhausts real logarithms with zero row sums; Corollary 5.14 and Algorithm 5.16 decide generator feasibility by intersecting linear inequalities with a two-sheet hyperboloid, with finitely many winding indices to consider. Thus the general logarithm classification and the existence of an embedding decision procedure for this family are prior results, rather than a new general solution in the private reconstruction. [General paper, Case III](https://arxiv.org/html/2005.00818v2), [published full text](https://mat.uab.cat/pubmat/fitxers/download/FileType:pdf/FolderName:v67(1)/FileName:6712308.pdf).

Baake–Sumner v2 Fact 2.10 and Corollary 2.11 parametrize real logarithms of scalar two-dimensional blocks. Its Lemma 4.5 applies them precisely to a simple unit eigenvalue, one other simple real eigenvalue and a repeated real eigenvalue; positive spectrum does not force the principal logarithm to be a generator. These results agree with the block mechanism reconstructed here. The same statements are present in the publisher version. [Baake–Sumner v2, Lemma 4.5](https://arxiv.org/html/2311.02596v2#S4.Thmtheorem5), [publisher version](https://link.springer.com/article/10.1007/s00285-024-02112-w).

| Proposed contribution | Audit status |
|---|---|
| Reversible positive-spectrum sampled matrix with ordinary but no reversible same-state embedding | Already a short, exact corollary of the public 2020 \(H\). No first-example claim is warranted. |
| Parametrizing every logarithm by a real two-dimensional rotation block and winding number | Prior general machinery, including an exhaustive four-state treatment. |
| Ordinary embedding implies reversible embedding for arbitrary positive multiplicities | False in v1 Theorem 3.16; valid with the earlier simple-spectrum restriction. |
| Explicit symmetric rational \(P\) and all-positive \(Q_0\) | Correct, useful exact example. The stronger symmetry/rational presentation is a narrower distinction, not evidence of first discovery of the broad phenomenon. |
| Closed boundary \(b\le2a\), or in the nonprincipal regime \(b\ge10\pi/\sqrt7\) and \(a\ge b-\sqrt{(b^2-4\pi^2)/2}\) | A concrete analytic elimination of a known general feasibility problem. The displayed block inequalities support it; originality of the closed form remains unestablished. |
| Positive stationary entropy for every same-state generator | Follows from absence of reversible embeddings and the entropy definition. |
| Existence of a strictly positive finite global entropy minimum | Also an elementary consequence of the old example plus compactness, as shown next. |
| Complete one-variable entropy objective, monotonicity in winding and block imbalance, strict convexity, unique minimizer up to transpose, certified numerical value | Potential narrower contribution. The inspected embedding sources do not supply this optimization. This audit is not an exhaustive entropy-literature search and does not certify novelty or independently certify the private entropy interval. |

For the penultimate entropy row, fix an irreducible \(P\) and its stationary vector \(\rho\). For every generator with \(e^Q=P\),

\[
\sum_{i\ne j}q_{ij}=-\operatorname{tr}Q=-\log\det P.
\]

All off-diagonal rates are nonnegative and individually bounded by the fixed total. The feasible set is closed (generator inequalities and \(e^Q=P\) are closed) and bounded, hence compact. The usual stationary entropy

\[
\sigma(Q)=\sum_{i<j}(\rho_iq_{ij}-\rho_jq_{ji})
\log\frac{\rho_iq_{ij}}{\rho_jq_{ji}}
\]

is lower semicontinuous as an extended nonnegative function, with zero exactly at detailed balance, counting a one-way edge as infinite. It attains its minimum. If no reversible generator exists, that minimum cannot be zero. For \(P_{\rm old}\), the all-positive generator \(\pi H\) gives a finite entropy value. Thus a strictly positive finite floor is already a consequence of the older example. What may add content is the exact quantitative optimization across all generators for a specified family.

The present review leaves novelty **UNKNOWN**, not confirmed. Specialist review should compare the family-specific closed form and entropy minimization against the strongest prior four-state algorithms, reversible-embedding criteria, and inverse entropy-production literature. Hidden-state enlargements and time-dependent generators change the admissible model and are outside these conclusions.

## Reproduction and evidentiary limits

Run the selected `independent_embedding_audit.py` in a disposable copy, as documented in the release README. It uses SymPy and mpmath and imports no source-archive checker. The public edition retains only the rational-P and older-H identities and their numerical diagnostics. Its freshly generated receipt gives the selected check count; these finite identities supplement the mathematical arguments above. Unselected ancillary source critiques and diagnostics are omitted.

No original source file, shared repository file, or another reviewer's output was edited. The archive's section 6 broad counterexample assessment is substantiated; its wording should retain the version-specific theorem pin and the distinction between a new family calculation and an older-work corollary. The entropy number and its claimed exact certification remain for the separate entropy audit.
