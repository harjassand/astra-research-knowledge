# Verification, replay and observed resources

## Proof versus diagnostics

FEEDBACK_AND_STOPPING.tex contains the new universal arguments. The preserved owner archive supplies the prior full tree proof and the exact finite-error-set coding lemma, derived from operator compression, affine Tverberg and Knill–Laflamme conditions. This lemma is an existence result, not an efficient synthesis claim.

The supplied feedback proof was read as source. The limited new replay checks representation and arithmetic; no old recurrence/tree audit was rerun.

With Python 3 and NumPy, run:

    python run_replay.py

This rewrites its receipt and diagnostic outputs with new timings. Preserve the original receipt if needed. Absolute paths in the original receipt record the producer invocation; the script itself locates sources relative to its own directory.

The independent scalar certificate uses standard-library exact rationals:

    python reviews/history_exponent_certificate.py

To compile the proof with pdfLaTeX and its listed standard packages:

    python build_pdf.py

To verify content before replay changes any receipt:

    python verify_package.py

## Observed producer costs

| Operation | Observed result | Wall time |
|---|---|---:|
| Supplied two-slot feedback factorization | Frobenius discrepancy 1.1210126175528405e-16; TP discrepancy 8.3203732140461555e-16; input-dependent outcome difference 0.012639000613812382 | 0.2310454 s |
| New frontier/arithmetic diagnostic | All assertions passed | 0.7968434 s process; 0.6784409 s body |
| Independent exact exponent certificate | Strict gap and negative tail enclosed by rational intervals | 0.00123281 s |

Principal environment: Python 3.12.14, NumPy 2.3.5, x86_64. Runner peak child RSS was 23,264 KiB; the new diagnostic reported 22,656 KiB; the scalar certificate reported 8,320 KiB. These are process peaks, not a sum or total research-session memory.

No GPU job, hardware experiment, purchase or outreach. Inference, search energy, total scientific labor and total monetary cost were not independently metered. File size and agent count are not productivity metrics.

## Physical and computational contract

The exact code uses n_K=(2/3)log2 K+O(log log K) qutrit calls. Its stopping version uses one backward coin bit and expected cost p n_K. Both branches remain in the error calculation. The converse allows unlimited normal measurable classical feedback.

The perturbed lower code uses exactly LN calls on the same bath, with no feedback. Local external decoder syndromes and recovery registers are explicit. A syndrome dimension 3^L per inner block is a sufficient loose finite choice for an isometric decoder extension. Local memory and encoding/decoding complexity can grow rapidly; no circuit, energy or practical-scale advantage is established.

The ideal inner block is identity on all of E, which prevents bath errors propagating through ideal packets. The actual perturbed protocol can change the bath; full logical diamond error <=4T'_N, half error <=2T'_N. Uniform logical transmission is not bath return.

## Conventions and limits checked

- State cutoff: half-trace <=sqrt(1-q); full trace <=2sqrt(1-q).
- Lottery: half-diamond=(1-p)(1-K^-2); full diamond is twice that.
- Unequally normalized coherent history sums use a full trace estimate.
- Stopping compares a bounded event, not an unbounded expected value.
- Coherent upper bound fixes the vertex cutoff before the horizon limit.
- Lower continuity fixes inner length and device before growing outer block count.

Archive integrity, manifest hashes and unchanged owner bytes are checked before upload. Private upload and readable UTF-8 transport verification do not establish receiver download, scientific acceptance or repository integration.
