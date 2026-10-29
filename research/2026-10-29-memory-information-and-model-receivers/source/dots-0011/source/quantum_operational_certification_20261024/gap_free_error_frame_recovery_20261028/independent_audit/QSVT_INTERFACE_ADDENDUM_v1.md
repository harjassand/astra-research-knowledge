# QSVT interface, normalization and finite-operation error

28 October2026. Independent implementation-scope addendum; original governing source is unchanged. A complete application must still supply its frame-access circuits and a finite compiled sequence.

## Primary implementation passages inspected

Gilyén–Su–Low–Wiebe, arXiv:1806.01838v1, Corollary18, Eq(33), implements a bounded real parity-matched polynomial by a control ancilla prepared/projected in |+>, coherently combining U_Phi and U_(−Phi). Their half-amplitudes add to the real polynomial; there is NO extra factor1/2 on the resulting desired block. Reverse this construction, with input/output projectors exchanged, for the adjoint singular-value map. Lemma19 and Figure1 require degree-many uses of U/U†, projector-controlled flips and phase gates. Theorem3 supplies a quadratic-arithmetic-count phase recurrence, while the subsequent completion uses polynomial roots. These passages alone do not prove a stable finite-bit implementation.

Source inspected: https://arxiv.org/pdf/1806.01838v1 , pp9,19–21 (PDF numbering). This is the2018v1 returned by the primary PDF, not an inferred later theorem numbering.

Haah, arXiv:1806.10236v4, Sections3.1 and4.1–4.2, gives finite-precision Laurent-product preprocessing in O(q³ polylog(q/tau)) time, using O(q log(q/tau)) arithmetic precision. Its initial contraction/rounding is part of the approximation error. This closes the abstract finite-bit existence issue for suitable QSP polynomial input; no claim of ordinary-double-precision stability follows.

Source inspected: https://arxiv.org/pdf/1806.10236v4 , pp1–2,5,8–14.

## How the present polynomial enters

For the real odd degree-q polynomial f_m, form the Laurent expression f_m((z+z^(−1))/2). Its rational coefficient list has length O(q) and polynomial bit length, obtained by the binomial theorem. Its values on the unit circle are real and bounded by1. A small controlled contraction/approximation allowance can provide room for finite-precision completion without changing the desired success block by more than the declared tolerance. The parity/reciprocity conditions must be kept when converting the resulting QSP factors into the alternating projected-unitary convention; a phase list for a different signal convention must not be silently substituted.

The exact Corollary18 construction and the finite-precision preprocessing theorem provide an algorithmic route, not an executed phase compiler in this package. In particular, this receipt does not certify a particular list of q angles, approximate block encoding, Schur branching circuit or polynomial normalization alpha. The central missing access obligation is unchanged.

## What must actually be available

One needs a coherent unitary U whose projected block is M/alpha with the stated domain and codomain, coherent inverse U†, implementable checks/reflections for both projectors, required clean ancillas and their preparation, classical phase synthesis at the paid precision, and a deterministic measurement/failure-reset interface. Efficient access to the source channel is not equivalent to these reversible operations. A physical cost bound must include projector checks and phase gates, not merely count U queries. No exponential matrix may be hidden inside a claimed constant-cost oracle.

## Robustness statements that can be used without a spectral gap

1. Suppose an actually implemented contraction A_tilde differs from the exact target A by operator norm at most tau, and BOTH are completed to total channels by keeping success and preparing a fixed state on failure. The same purification comparison gives

       1−F_e(D_(A_tilde) E_S) <= (20/9)b+2alpha epsilon+2tau.

Indeed the new overlap differs by at most tau: the original source purification after M has norm1 and the ideal target vector has norm1. This avoids a singular-value perturbation argument and does not assume the square roots of failure effects are close. It requires A_tilde itself to be a physical contraction, as a unitary block is.

2. If the entire ideal sequence W and its physical approximation W_tilde obey||W−W_tilde||<=xi, with identical input ancillas and identical success/failure processing, the resulting decoder channels have half-diamond distance at most xi. Purification vector distance is at most xi for every reference input, pure-state trace distance is at most that vector distance, and postprocessing is contractive. Thus xi adds directly to the Bell-infidelity bound. Additional ancilla-preparation, measurement, reset or postprocessing errors need their own channel allowances.

3. For products of unitary gates, telescoping gives||W−W_tilde||<=sum_l||V_l−V_tilde_l||. Therefore approximate base queries, projector controls and phase gates accrue errors proportional to their actual number of uses. Degree-q circuits do not inherit a degree-independent primitive-error tolerance. For phase rotations the local bound is at most the absolute phase error. To reach total xi, allocate the primitive errors across the actual compiled sequence.

These bounds distinguish polynomial-target approximation from whole-circuit approximation; do not count one twice. A source-channel mismatch or incorrect defect premise is neither of them and requires a separate estimate. All statements retain the original one-use/closed-operation scope.
