# An explicit exact composition bound for CP, two-copositive maps

27 October 2026. Completed mathematical adaptation of a released proof. Internally reconstructed and audited at the exact scope below. Historical novelty and formal verification of the weakening are not asserted.

## Theorem

Let d>=2. For i=1,...,2(d-1), let Phi_i:M_d(C)->M_d(C) be complex-linear and completely positive. Suppose t composed with Phi_i is two-positive, where t is matrix transposition on the output. Then

    Phi_{2(d-1)} composed with ... composed with Phi_1

is entanglement breaking. The factors may differ, and trace preservation and unitality are not required. The conclusion quantifies over every finite reference dimension and every positive joint input. It concerns serial composition, not tensor powers or a network with a noiseless quantum bypass. The bound is sufficient, not claimed optimal.

## Proof and attribution

The released proof of Turturean–Bao, *Entanglement Breaking after 2(d-1) PPT Maps*, uses copositivity only on a two-dimensional reference in its pair lemma. For an input on C^2 tensor C^d, two-positivity of t composed with Phi makes the first output PPT. In the second-map block construction, the same condition on Psi makes both the pure two-reference output and its partial transpose positive. Their swapped average has equal diagonal blocks and is separable. The local filters and positive remainder in that construction then show that Psi composed with Phi is two-entanglement breaking. Complete positivity, retained throughout, permits the established arbitrary-reference Schmidt-number reduction. After d-1 pairs, the Schmidt number is at most one. No full copositivity beyond these two-reference tests is used.

The full singular-support, block, lifting and normalization argument is in `review/VERDICT.md`. This adaptation relies on PSI's key qubit construction; the iteration is the prior Christandl–Mueller-Hermes–Wolf technique, not an Astra invention. PSI's published theorem/fidelity file state full PPT. Its supplied Lean result should not be represented as formalising the weaker theorem here. No Lean build was performed for this adaptation.

Primary sources:

- [PSI paper at the inspected commit](https://github.com/physical-superintelligence/oqp-batch-2026/blob/da37af2ae174687403fbd97e9673c819edee71fd/ppt-composition-bound/paper/source/ppt_composition_prl_draft.tex)
- [PSI statement fidelity](https://github.com/physical-superintelligence/oqp-batch-2026/blob/da37af2ae174687403fbd97e9673c819edee71fd/ppt-composition-bound/lean/docs/FIDELITY.md)
- [Christandl–Mueller-Hermes–Wolf, Theorem II.1](https://arxiv.org/html/1807.01266v2)

## The class is strictly broader than PPT

For d>=3,

    Phi_d(X) = (2 tr(X) I_d - X^T)/(2d-1)

is CPTP and two-copositive, while its output-transposed Choi matrix has eigenvalue (2-d)/(2d-1)<0. Thus it is not PPT. The detailed exact verification is in the review. This standard Werner-form example was **already recorded** in Astra's later October 9 edition; it is not claimed new here.

## Correct Astra comparison

N574's later source `updates/CE/package/Uniform_CP_Cone_Composition_and_PPT_Applications_2026-10-09/nonstationary_ppt/TWO_COPOSITIVE_EXACT_WORD_EXTENSION.md` already claims some finite exact arbitrary-word length for the same class, without a practical numerical exponent. The present theorem supplies an explicit 2(d-1) bound and direct proof independently of that candidate's broad semialgebraic/cone argument. It does not newly discover the existence claim or validate the more general cone theorem. `review/VERSION_ADDENDUM.md` corrects the initial older-edition-only source comparison without overwriting its original bytes.

N577's effect-matched approximation is preserved. For words at least this exact cutoff, no EB approximation is needed; the word itself is EB. Earlier quantitative bounds may still describe shorter words or other useful quantitative questions. No universal quantum-computing, communication, distillability or practical advantage claim follows.

## Internal review scope

The coordinator traced the weaker assumption and checked the argument. A separate agent received the proposed theorem and governing sources, without the coordinator's derivation, and reconstructed the proof and strict-class example, then separately traced the later source edition. It knew the claim and common source; it was not blind. The completed audit covers the theorem stated here. It is not a broad audit of all N574 candidates or of every PSI result. No external-specialist approval is required for recording this completed internal audit at its actual scope.
