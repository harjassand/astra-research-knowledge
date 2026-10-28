# Independent review: passive streaming erasure and causal memory

Reviewer: `producer-workspace/pulse_review`, 29 October 2026 Australia/Brisbane.

## Decision and accepted scope

**Accept the passive compression lemma, its causal iteration, and the complete refined-record erasure identity at the declared exact model scope.** For fixed finite arrival batches of known controlled-Weyl features with globally vanishing imaginary Gram matrix, the construction retains exactly

\[
r_t=\tfrac12\operatorname{rank}K_t,
\qquad K_t=\sum_{s\le t}\operatorname{Im}(F_s^\dagger F_s)
\]

canonical bosonic modes after cut \(t\). It uses passive mode mixing, destructive homodyne and local diagonal source feedback, without extra source-to-field interaction. Gaussian, vacuum, thermal and factorized input-state assumptions are unnecessary for the exact identity.

**Accept the matching lower bound within the explicitly declared noiseless linear Gaussian reconstruction class.** This is not a minimum over arbitrary non-Gaussian receivers, modular Weyl measurements, arbitrary Hilbert-space encodings, or approximate state-restricted recovery. All quantum ancillas, delay lines and bypasses crossing a cut must count.

Canonical-mode count is not finite Hilbert dimension, energy capacity, lifetime, record precision or total hardware cost. Live width includes incoming modes. Exact feature knowledge and ideal sharp homodyne remain supplied interfaces. The numerical compiler residuals are not physical channel-error certificates.

## Version pins and actual execution

Reviewed author files under `p2_mediator/causal/`:

| File | SHA-256 |
|---|---|
| `PASSIVE_STREAMING_ERASER.md` | `4b97f4ba41627855b2591a170b60b0714d3244b44b5181164840290a229e3d0f` |
| `passive_streaming.py` | `a028906b1e0e629fc100e5d28b89728ced9b2b7d213178d07e3eccb630dcd805` |
| `exact_feature_algebra.py` | `c37c0e819be1bdc65dc079335a785f7b1b6e2e4bbccf35a1f28b81426cb1acad` |
| `passive_streaming_results.json` | `2c0b8e819141bc3a73c8affe39d409f4e59d4b5c8abac385daa26b0e9f06abca` |
| `EXECUTED_CHECKS.md` | `34abe2717bd112d7f45c15296be0ac508ee1ab2da8734e9072cbb53e6db25d88` |
| `RESOURCE_DEFINITIONS.md` | `dd15952775bdeadc0f0ae7efd9eb8769cf5215c5c02a1ff8a768a542ae8373e1` |

I read the proof, both executable source files, execution report and resource definitions in full. I replayed copies under `reviews/causal_review/replay/`, preserving the author artifacts. The entire result JSON matched exactly, including all seven examples, stage matrices, exact prefix ranks, refined record modes and feedback coefficients.

The independent standard-library audit `exact_pair_audit.py` imports neither author module. It exercises seven source labels spanning five independent real feature directions, a non-saturated pair with \(\sigma=3/5\), a saturated pair with \(\sigma=1\), a radical direction, rational passive mode mixing and two arrival cuts. All assertions use exact rational arithmetic. Audit-script SHA-256:
`f9e47e8193c185b68838757617728a03863bdcf1923e394f1c6646006b6bca68`.

## 1. Passive compression is valid, including non-saturated pairs

The real inner product \(\operatorname{Re}\langle\cdot,\cdot\rangle\) is positive definite on the real feature span. Orthogonally reducing its restricted imaginary Gram matrix gives the stated real-orthonormal pairs and radical vectors. Their complex Gram matrix is positive, and each pair obeys \(0<\sigma\le1\).

For \(\sigma<1\),

\[
w=(v-i\sigma u)/\sqrt{1-\sigma^2}
\]

has unit complex norm, is complex-orthogonal to \(u\), and has real inner product \(\sqrt{1-\sigma^2}\) with \(v\). At saturation, equality in Cauchy–Schwarz gives \(v=iu\); no residual mode exists. Distinct pairs, their residuals and radical vectors are mutually complex-orthogonal in the combinations used by the construction.

For real \(\alpha,\beta\),

\[
\alpha u+\beta v=(\alpha+i\sigma\beta)u
 +\sqrt{1-\sigma^2}\,\beta w.
\]

Only the retained coefficient is complex. Homodyning the residual mode's \(Q\) quadrature commutes with every controlled feature and produces a known phase linear in the source labels. Radical coefficients are also real. Completing these vectors to a complex orthonormal basis is a passive interferometer, with no squeezing or physical gain hidden in the normalization.

The measured sector contributes only a real Gram matrix, so the retained imaginary Gram matrix is unchanged. Its rank is twice the number of retained pairs. Dependence among source features causes no difficulty: the full-row-rank real coefficient matrix relating them to their real span preserves the rank of the restricted skew form.

The non-saturated case is the decisive bridge. Two real feature directions can occupy two complex bright modes, while the receiver retains only one of them quantum mechanically. The residual mode may lie outside the original real feature span. Allowing the actual record to refine the minimal target measurement is what makes that passive reduction possible.

## 2. Causal iteration and arbitrary correlations

At stage \(t\), concatenating retained features and new arrival features produces imaginary Gram matrix \(K_t\). Previously measured contributions were real. Applying the lemma therefore gives exactly \(r_t\).

Every measured mode is complex-orthogonal to retained modes and future physical arrivals, and later receiver operations leave it untouched. Pulled back to the original input, the network defines commuting recorded quadratures \(Y_\ell\), with

\[
\Phi(F_i)=\sum_\ell b_{i\ell}Y_\ell,
\qquad b_{i\ell}\in\mathbb R.
\]

Each actual recorded quadrature commutes with every target feature. At the final globally isotropic cut no source-dependent quantum feature remains. Dark modes carry zero controlled feature and may be traced by the same baseline receiver.

Measuring a past mode can steer a correlated future mode. This does not invalidate the construction: it uses an operator/instrument identity, not a conditional covariance or independent-supply assumption. The same steering occurs in the common baseline receiver. Neither the proof nor the exact audit assumes fresh thermal marginals after a measurement.

## 3. Complete refined record and feedback

At a stage, measured and retained sectors are complex-orthogonal. Their Weyl factors therefore tensor-factor without a scalar source cocycle. In the spectral-measure sense,

\[
K_xW\!\left(\sum_i z_i h_i\right)
=e^{i\sum_i z_i\theta_i(x)}
 W\!\left(\sum_i z_i g'_i\right)K_x.
\]

This is an instrument identity, not a claim that ideal homodyne has a bounded pointwise Kraus density. Iteration accumulates only phases linear in the source labels; product local \(Z_i\) feedback cancels them.

For arbitrary normal source/environment/reference input, including correlations, the corrected \((z,z')\) block at the full actual record is exactly

\[
g_z\overline{g_{z'}}\operatorname{Tr}_E[E_0(dy)\rho_{zz'}].
\]

This preserves the desired diagonal operation together with the assemblage of the **same refined receiver** on the common input. The common record can still contain preexisting source correlations; the theorem does not erase those correlations.

Keeping extra record coordinates is not the same instrument as keeping only the minimal feature record. Coarsening by the real map \(y\mapsto By\) recovers that smaller destructive measurement as an additional common processing step. The stated theorem correctly retains the actual record instead of silently coarsening it.

The final version correctly separates feedback schedules. Deferred feedback after the full declared operation suffices. Early feedback needs commutation with actual microscopic source controls, which a final diagonal dilation alone does not imply. Departed modes must not return before retirement. The earlier noncommuting contact and nonlinear sine leakage do not automatically satisfy this controlled-Weyl interface.

## 4. Lower bound: correct class, no universal claim

In the declared noiseless linear reconstruction class, the past target quadratures at a cut must have a representation

\[
A_{\le t}=B_tY_{\le t}+L_tR_{\rm mem}.
\]

The recorded variables commute with one another and with the retained register. Taking commutators using \([R_a,R_b]=2i(J_q)_{ab}\) yields

\[
K_t=L_tJ_qL_t^{\mathsf T},\qquad\operatorname{rank}K_t\le2q.
\]

The upper construction saturates this at every cut. A discarded unknown quadrature cannot provide an exact missing term later, and an independent noisy ancilla cannot provide a noiseless linear observable.

I directly read Holevo's primary [arXiv:2007.02340](https://arxiv.org/pdf/2007.02340), equations (3)–(4), Theorem 1 and the noiseless Type 3 discussion. Its Gaussian-observable characteristic function is a Weyl operator times a Gaussian noise multiplier. Exact reproduction of modulus-one Weyl factors forces zero variance in the required directions. This supports the author's noiseless-sector qualification. Gaussian-observable structure and Naimark machinery are existing results, not novelty established by this review.

The linear premise must not be promoted to arbitrary receivers. Modular measurements can handle finite Weyl lattices differently; a non-Gaussian encoding need not preserve canonical coordinates in this form; approximate energy-restricted recovery can discard weak directions. All retained ancillary quantum systems and bypasses count across cuts. These restrictions are essential to the lower bound.

## 5. Code and independent checks

The compiler's stacked real/imaginary SVD correctly forms a real-orthonormal basis. Real Schur reduction supplies the skew pairs. The residual formula, saturation branch, QR completion and phase alignment implement the lemma. Global mode tracking embeds retained modes and new arrivals into their proper input coordinates; previous measured modes remain orthogonal to later registers.

The exact helper supplies rational input Gram matrices, prefix ranks and a non-saturated-pair identity. The compiler uses floating SVD/Schur/QR and checks selected ranks against the exact example ranks. Its residuals are diagnostic, not outward enclosures or rank certificates for arbitrary ill-conditioned families. A weak nonzero direction can require a mode in the exact theorem even when floating thresholding drops it.

The independent replay covered the Bell case, repaired small-epsilon case, pointwise-real case, two dense rational families and two star families. Every stored result matched. The maximum residual below \(2.13\times10^{-15}\) is implementation evidence in those examples; it is not an operation-error allowance.

The separate exact audit gives:

| Quantity | Independent example |
|---|---:|
| Source labels | 7 |
| Independent real feature directions | 5 |
| Arrival mode counts | 4, 4 |
| Retained modes after cuts | 2, 0 |
| Live processing widths | 4, 6 |
| Actual record quadratures | 7 |
| Minimal feature-record dimension | 5 |

It verifies exact feature reconstruction, preserved prefix and vanishing final imaginary Gram matrices, passive orthogonal mode vectors, real feedback coefficients, and commutation of every actual record quadrature with every global target feature. Squared feature norms split without gain. The audit imports no author compiler.

## 6. Resources, useful failure and consequence

The rank formula concerns fixed arrival cuts. Grouping batches can lower between-batch rank while increasing capture/live width; batching cannot conceal buffering. Passive processing conserves total number before measurement but can concentrate energy. Unconditional retained energy is bounded by supplied arriving and ancillary energy; conditioned branches can be larger.

As clarified in `RESOURCE_DEFINITIONS.md`, `retained_mean_feature_photons` is \(\sum_i\|g_i\|^2\). It is a mean coherent-displacement photon number for vacuum background and independent uniform source signs. It is not a universal stored-state energy bound; the worst sign branch can reach up to \(n\sum_i\|g_i\|^2\). The one-mode star examples retain a growing feature-energy cost.

The actual record can contain many real outcomes. Collection, mode capture, interferometer calibration, local oscillator delivery, finite resolution, source coherence during feedback delay and receiver reuse/reset remain separate resources. Exact Weyl identities do not give uniform operator-norm robustness to feature miscalibration; a finite physical receiver requires state or energy contracts.

The block-partition completion dynamic program is valid within its stated independent-block architecture, conditional on the separate coherent isotropic-completion cost. It is not a universal storage/coupling optimum. This review does not certify that separate source-coupled operation or its physical interface.

The failed Darboux representation is correctly retained as a method failure. For features \((1,0)\) and \((i\epsilon,1)\), measuring \(Q_2\) and retaining mode 1 is passive and exact. A divergent \(1/\epsilon\) coefficient in a different representation is not a physical lower bound. The non-saturated lemma repairs precisely that issue.

Beyond a gate, the construction is a one-pass implementation of a jointly commuting family of field quadratures with the stated minimum retained canonical-mode count in the linear class. Local phase feedback turns that measurement instrument into a controlled-Weyl eraser. That reach follows from the proof. Historical priority and hardware advantage over an equally informed conventional receiver are not decided by this review.

## Final status

The author incorporated the residual-mode wording fix, persistent/live-width distinction, refined-record scope, energy interpretation and immediate/deferred-feedback distinction. The unavailable-SymPy execution failure is preserved, and the rational replacement and declared examples executed successfully.

No unresolved mathematical defect was found in the accepted passive construction or its declared linear-class lower bound at the pinned versions. This is an actual independent theorem/code review, not inherited acceptance from earlier memory or erasure work.
