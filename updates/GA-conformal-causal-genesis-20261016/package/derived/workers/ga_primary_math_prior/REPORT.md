# Primary proof and priority audit: conformal cubic compensation

Date: 16 October 2026, Australia/Brisbane.

**Outcome.** The outstanding full-proof comparison with Stefan Müller's MiS 19/1998 is completed at the preprint level. Cubic compensation for a differential constraint with varying rank is established prior mathematics, including an estimate with the same \(L^4\)-\(L^2\) scaling. That paper does not state the packet's operator-specific 18-dimensional classification, and its nonresonance mechanism does not directly prove that classification or the sharp quartic inequality. The classification is a short algebraic consequence of classical mixed-derivative interpolation once the correct transverse jet is identified. Exact historical originality remains UNKNOWN.

Selected actual OpenAI Math proofs were inspected at a current immutable pin. Their matrix/heat mechanism supplies a concrete design pattern, with a missing transfer stated below. It does not close the sharp bound.

The authored [weighted-jet extension](DERIVED_JET_EXTENSION.md) proves a larger finite-constant classification, gives a simpler compatible necessity carrier, and derives an explicit higher-integrability decay rate for the target cubic. These internally derived consequences retain the critical concentration obstruction. No all-gradient sharp quasiconvexity theorem or compatible negative Jensen field is produced here.

## Source context and proof scope

The supplied packet is frozen at
../../originals/conformal_packet/RESEARCH_REPORT.md and SOURCES.json.
The parent supplied Astra checkout pin
f80a8f15137575133ad2c9af975513b32e8fa93e.
I read its current AGENTS.md, 00_START_HERE.txt, and complete N880 dossier. The dossier's scoped open gates are retained; its navigation metadata is not a proof premise.

OpenAI Math was freshly pinned through the GitHub commit API at
1581d4cbdd69a0faf34b2089614fe2a814316a6a.
All selected source links below use that pin. The first whole-repository recursive tree response was truncated; I then acquired the root tree and the complete untruncated preprints subtree. Catalogue screening is not an exhaustive proof audit.

Acquisition times, URLs, byte counts, SHA-256 values, HTTP failures, and the HTML soft failure from an initial AMS URL are preserved in ACQUISITION_RECEIPTS.json and the individual acquisition receipt files. Downloaded external PDFs, repository sources, rendered proof pages, and extracted text stay under external_excluded_from_publication. They must not be copied into the public research package. Authored reports, source metadata, and the exact derived receipt may be published subject to the parent's ordinary integration checks.

## 1. What Müller's actual proof establishes

Primary source: [MiS 19/1998 full PDF](https://files-www.mis.mpg.de/mpi-typo3/preprints/1998/preprint1998_19.pdf). The 11-page file contains article pages 1–7. All article pages were read; Lemma 2 and its proof on article pages 4–5 were visually checked. [The publisher record](https://doi.org/10.1017/S0308210500000214) identifies the journal publication as Proceedings of the Royal Society of Edinburgh A 130 (2000), 389–395. The publisher's online date is later. This audit read the full institutional preprint, not the publisher's final PDF.

For mean-zero periodic \(v:\mathbb T^3\to\mathbb R^3\), Müller uses
\[
\mathcal A(Dv)=(\partial_2v_1,\partial_3v_1,
 \partial_1v_2,\partial_3v_2,\partial_1v_3,\partial_2v_3).
\]
Lemma 2 gives, for \(1/p+1/q=1\), \(1<p,q<\infty\),
\[
\left|\int v_1v_2v_3\right|
\le C(p)\|v\|_{2p}^2\|\mathcal A(Dv)\|_{W^{-1,q}}. \tag{M1}
\]
Its second estimate controls the integrated quadratic polarization
\(D^2(v_1v_2v_3)(z)[v,v]\) by
\(C(p)|z|\|v\|_p\|\mathcal A(Dv)\|_{W^{-1,q}}\).
The proof splits each component into a narrow cone around its own coordinate axis and a remainder controlled by the defect. Three sufficiently narrow distinct cones cannot contain a nonzero zero-sum frequency triple. Expanding the product leaves a controlled remainder. At \(p=q=2\), gradient compatibility bounds the negative Sobolev defect by the \(L^2\) distance of the gradient from Müller's matrix subspace. Young's inequality then supplies a quasiconvex completion with an adjustable penalty.

There is a local sign typo in the acquired preprint's final cone-sum display on article page 5. The preceding three inequalities give
\[
(1-\delta^2)\sum_i|k^{(i)}|^2
\ \le\ 4\delta^2\sum_i|k^{(i)}|^2,
\]
although the summed display prints the reverse sign. The corrected sign gives the stated conclusion for \(\delta<1/\sqrt5\). This correction follows directly from the preceding inequalities and is not a missing analytic lemma.

### Exact comparison with the new packet

The following deductions are this audit's comparison, not claims made in Müller's paper.

| Interface | Müller's Lemma 2 | Packet's cubic theorem |
|---|---|---|
| Fields | Three free scalar components on \(\mathbb T^3\) | A compatible \(2\times2\) gradient on \(\mathbb T^2\) |
| Rank drop | Symbol rank three generically, two on coordinate axes | \(T_\sigma\) rank two off the vertical axis, one on it |
| Exceptional geometry | Three distinct axes | One repeated characteristic axis |
| Cubic | One trilinear product, plus its polarizations | All 20 homogeneous cubics, with exactly two exclusions |
| Cancellation | Signed integral; exact kernel products need not vanish pointwise | Admissible polynomials vanish on the exact pure-shear kernel |
| Analytic mechanism | Cone decomposition and absence of a zero-sum triad | Mixed-derivative interpolation and a second transverse jet |
| Constant | Finite, unspecified \(C(p)\) | Finite, unspecified \(K\); target constant remains missing |

A direct counterexample separates signed from absolute estimates in (M1):
\(v_i(x)=\sin(2\pi x_i)\) has \(\mathcal A(Dv)=0\),
\(\int v_1v_2v_3=0\), and \(\int|v_1v_2v_3|>0\).
Thus Müller's result cannot simply be relabelled as the packet's signed-absolute equivalence.

Near the packet's vertical characteristic, frequencies
\((1,N),(1,N),(-2,-2N)\) form an exact nonzero triad for every \(N\).
The distinct-cone nonresonance argument is therefore unavailable there.
Also, the small singular value of
\(\begin{psmallmatrix}\sigma\xi_x&\xi_y\\0&\xi_x\end{psmallmatrix}\)
near a unit vertical covector vanishes to second order in the angular displacement. The weights \(a:1,b:0,c:2,q:2\) in the authored extension encode that fact. There is no demonstrated linear coordinate transformation that turns this interface into Müller's three-axis problem.

**Priority adjudication:** the broad subject and finite cubic compensation beyond constant rank are old. The exact 18-dimensional statement was not found in this inspected paper. That limited nonmatch is not priority clearance.

## 2. Classical machinery already supplies the finite bound

The decisive analytic estimate is
\[
\|\psi_{xy}\|_t^2
\le C_{p,s}\|\psi_{xx}\|_p\|\psi_{yy}\|_s,\qquad
\frac1t=\frac12\left(\frac1p+\frac1s\right),
\quad1<p,s<\infty. \tag{H1}
\]
The packet provides a sound route to (H1): remove axis modes, use coordinate imaginary-power multipliers on the strip, and apply complex interpolation. The classical primary interpolation source [Stein, 1956, Theorem 1 and its proof](https://www.ams.org/journals/tran/1956-083-02/S0002-9947-1956-0082586-0/S0002-9947-1956-0082586-0.pdf), article pages 483–485, was acquired and read. Its scalar dual analytic-family argument supports the strip step. Periodic imaginary-power multiplier and Hilbert-transform bounds are standard additional inputs; they have not been re-proved from scratch in this audit.

With Hodge decomposition, (H1) gives
\[
\|a\|_{8/3}^2\le C_\sigma\|T_\sigma\phi\|_2\|D\phi\|_4.
\]
The rest of the cubic classification is algebra plus compatible necessity fields: membership in \((q,c,a^2)\), followed by Hölder, and exclusion of \(b^3,ab^2\).
The report should therefore distinguish an operator-specific characterization from invention of a new analytic interpolation theorem.

There is also a direct classical explanation for finiteness of the packet's horizontal-heat stresses. Its horizontal symbols have denominator
\[
D=(p+\ell)^2+p^2+\ell^2\ge p^2+\ell^2,
\]
and their rational degree-zero symbols are smooth away from \((0,0)\), with
\(|\partial^\alpha m|\le C_\alpha|(p,\ell)|^{-|\alpha|}\).
A smooth low-frequency cutoff preserves all nonzero integer frequency values.
The dyadic bilinear proof in [Coifman–Meyer, Astérisque 57 (1978), §13, Theorem 12 and proof, pages 54–58](https://www.numdam.org/item/AST_1978__57__1_0.pdf) was acquired and read. An explicit scaled-derivative formulation also appears in [Grafakos–Si's primary manuscript](https://grafakos.missouri.edu/preprints/Grafakos-Si-2011-01-12.pdf), equation (5). Their Theorem 1.1 applies directly with two scalar inputs, \(r=2,\gamma=2\), and input exponents \(4,4\): our smooth dyadic annulus symbols have a uniform \(W^{2,2}\) norm. I read that theorem and the proof setup, without auditing the entire later proof. The periodic Littlewood–Paley argument gives the same \(L^4\times L^4\to L^2\) estimate, and Hölder in the unsmoothed vertical variable supplies the two-dimensional estimate. This obtains another finite bound for the explicit cubic resolvent. Its constants do not establish the required budget \(4A_r\).

### Stronger older tools that were actually inspected

[Müller, MiS 29/1999](https://files-www.mis.mpg.de/mpi-typo3/preprints/1999/preprint1999_29.pdf) supplies Haar/Riesz interpolation and Jensen inequalities on directional Haar ranges. I read the main statements, the proof architecture, and the actual induction proof of Lemma 6. [Lee–Müller–Müller, MiS 7/2008](https://files-www.mis.mpg.de/mpi-typo3/preprints/2008/preprint2008_7.pdf), later published in 2011, extends this to finite \(L^p\): its Theorem 1.1 has sharp interpolation exponents \(1/2\) for \(p\ge2\), and \(1-1/p\) for \(p\le2\). The statement, the summation proof reducing it to the scale bounds, and the directional Jensen argument were read; the long scale-bound proofs were not fully audited. [Müller–Müller 2016](https://ems.press/content/serial-article-files/38608), pages 1137–1145, was read through the main theorem and its summation proof; the later wavelet operator estimates were not fully audited.

These sources offer a real-space/frequency-space decomposition followed by a valid Jensen inequality on a selected range. Their hypotheses have not been matched to \(T_\sigma\)'s repeated characteristic or to the exact quartic \(J_r\). Applying a sharp Haar exponent to a different derivative operator would be invalid. The carrier in the authored extension prevents a stronger uniform defect exponent for the entire missing derivative.

The 2020 Balashova paper on mixed derivative norms is a relevant exact-priority lead. Its primary indexed abstract identifies estimates on a multidimensional torus with different Lebesgue norms. Full-text acquisition failed through the documented MathNet/journal routes. It is not admitted as a theorem premise or an exact counterpart.

## 3. Selected OpenAI Math proof capital

Source pin: 1581d4cbdd69a0faf34b2089614fe2a814316a6a.

I inspected the actual sources of family 082:

- [Dyadic triangular Hilbert form](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/An-L3-bound-for-the-dyadic-triangular-Hilbert-form-October-5-2026/build/sections/03-trace.tex): complete matrix, trace, dyadic splitting, and summation sections.
- [Annular variation manuscript](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/preprints/Annular-variation-of-the-triangular-Hilbert-transform-at-the-symmetric-point-October-5-2026/build/sections/heat.tex): complete matrix section and Gaussian heat section. The frequency and preliminaries files were acquired, but no complete audit of the annular theorem's remaining proof is claimed.

The dyadic source constructs \(\Phi(P)=\operatorname{tr}(P^{3/2})\), with supported Hessian
\[
b_P(K)=\frac32\sum_{i,j}\frac{|K_{ij}|^2}{\sqrt{p_i}+\sqrt{p_j}}.
\]
It bounds a cyclic trace by three inserted Gram costs, handles singular supports, obtains a positive energy increment under the four XOR-compatible child choices, and telescopes. The annular source uses the same metric with Gaussian weights. Integrating center derivatives over a plane turns them into scale dissipation; nearby variance rates leave a positive dissipation margin. These are specific coupling and energy arguments, not just shared uses of the word heat.

**A useful design principle, with an unproved bridge.** A replacement construction should measure the coupled trilinear interaction in a positive Hessian cost before taking a norm. A matrix Gram budget can retain incident interactions that a separately bounded stress loses. The packet's explicit failure of its canonical stress contraction makes that distinction relevant.

For a valid transfer one must still construct, for every admitted compatible gradient, a matrix/semigroup representation whose cubic trace is exactly \(C_r\), whose defect insertion has cost \(Q_r\), and whose entire initial/terminal energy budget is at most \(A_r\) with the required constant. No such representation or budget was derived here. The source's \(L^3\) triangular operator, XOR geometry, cubic Schatten energy, and finite unspecified constants are different from the packet's \(L^4\) gradient/\(L^2\) defect quartic problem. Even treating its claimed theorem as true would not fill this bridge.

The repository explicitly records mixed verification status. I also read family 082's Lean scope note, comparator configuration, comparator statement, and actual [solution Main.lean](https://github.com/openai/math/blob/1581d4cbdd69a0faf34b2089614fe2a814316a6a/lean/OAI/Analysis/TriangularHilbert/Main.lean). The comparator statement contains a placeholder; the configuration points to a separate solution module whose main declaration has a proof body. A placeholder in the challenge file is not by itself a gap in the solution. I did not replay Lean, its dependency closure, comparator, or trusted-kernel export. No formal verification receipt is claimed.

## 4. Concrete consequences produced in this audit

The full proof is in DERIVED_JET_EXTENSION.md; JET_EXACT_RECEIPT.json checks only its specified algebraic fixtures and exponent identities.

1. For every homogeneous degree \(m\ge2\), finite \(p,s>1\) with \(1/p+(m-1)/s=1\), the exact signed/absolute finite-bound criterion remains
   \(P(a,b,0,-\sigma a)\) divisible by \(a^2\).
   Its dimension is \(\binom{m+3}{3}-2\).
2. More generally, for defect powers \(0<\theta\le1\) and
   \(\theta/p+(m-\theta)/s=1\), the exact criterion is divisibility by
   \(a^{\lceil2\theta\rceil}\). No signed-absolute equivalence beyond that range is asserted.
3. A single compatible travelling wave with profile
   \(\cos z+\cos2z\) proves necessity in every degree.
   It also proves the sharp normalization
   \(\|a\|_2^2\le\sigma^{-1}\|T_\sigma\phi\|_2\|D\phi\|_2\).
4. The target cubic's higher weighted order gives, for \(Q_r>0\),
   \[
   |C_r|/\sqrt{Q_r}\le K_r Q_r^{1/4}\|D\phi\|_6^{3/2}.
   \]
   The defect exponent \(3/2\) before division is optimal on uniformly bounded-gradient carriers. The analogous explicit rates hold for \(4<s\le6\).

The new \(L^6\) rate is a quantitative sufficient condition for the absence of near-kernel loss on a more regular family. It does not replace the packet's larger uniform-integrability class. Critical concentration makes \(\|D\phi\|_6\) grow as \(\varepsilon^{-1/6}\), exactly cancelling the apparent \(Q_r^{1/4}\) gain. That is a concrete retained boundary, not a concealed sharpness assumption.

## Adjudicated statuses

| Question | Status |
|---|---|
| Full Müller preprint proof acquired/read and exact mechanism compared | COMPLETE, scoped as above |
| Broad cubic compensation beyond constant rank is new | NO; contradicted by the primary predecessor |
| Exact 18-dimensional statement copied from Müller 1998/2000 | Not found in that source; no direct implication established |
| Exact historical priority of the classification/resolvent | UNKNOWN |
| Classical finite-constant machinery identified | YES; analytic interpolation and bilinear multipliers |
| Useful stronger consequences internally derived | YES; weighted-degree classification and explicit higher-integrability rate |
| OpenAI Math theorem formally replayed here | NO |
| Sharp unchanged \(C_r^2\le4A_rQ_r\), all gradients | OPEN |
| All-affine positive-core quasiconvexity or Morrey resolved | NO |

The highest-value remaining task is a cancellation-preserving sharp energy certificate, or a compatible negative field, for the exact original \(W^{1,4}\) class. Cone exclusion, a finite multiplier constant, an additional integrability promise, and a changed completion coefficient do not settle that task.
