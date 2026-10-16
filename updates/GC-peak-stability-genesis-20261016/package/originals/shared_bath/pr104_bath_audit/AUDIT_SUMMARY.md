# PR104 shared-bath audit

Pinned revision: 9dbe934e5475f415c2d160a6c0715534aafa546b.

## Finding

The load-bearing new mathematical operation is an exact change of unraveling: the specified dephasing generator is represented by independent complete parity pinches at intensity 2γ. Applying the old deletion-null measured-cell lemma to every latent inter-pinch gap and averaging the scalar gap-action certificates closes the formerly open sharp subset-product question. A separate virtual-seed construction imports this improvement into the existing qualified private-sign Fourier interface, replacing mB by mε. It does not establish a new microscopic physical generator or generic memory theorem.

Source: https://github.com/harjassand/astra-research-knowledge/blob/9dbe934e5475f415c2d160a6c0715534aafa546b/updates/GB-dots-capital-genesis-20261016/package/derived/root/SHARP_SUBSET_PROOF_RECONSTRUCTION.md

## Analytic audit outcome

No defect found in the sharp endpoint proof under its literal finite-dimensional, deletion-preserving, independent-clock assumptions. The argument can be reconstructed without importing any numerical PASS label:

1. D=(Id+Ad Z)/2 gives γ(Ad Z−Id)=2γ(D−Id), including a simultaneous noncommuting Hamiltonian via the exact jump expansion.
2. Fix the Poisson cut times and retain an isolated record at every pinch. Deleting the own interaction on one gap forces its two record labels to agree on every input, regardless of other selected interaction strengths. Other parity pinchings preserve this identity because the parities commute.
3. Project onto one mismatching gap for each selected parent. Repeated fundamental calculus eliminates all coordinate-boundary terms. The mixed Duhamel derivative contains all insertion orders, whose time domains partition the Cartesian product of gap intervals. Its norm is at most the product of gap actions, with no factorial. Squaring gives a positive effect bound on the whole admitted joint input domain.
4. Union over witness gaps gives the product of each parent's sum of squared gap actions. The quantum records need not be independent. Only the scalar clock partition families need be independent. Their averages factor, and the probability that two times share a gap is exp(−2γ|t−s|).
5. The endpoint all-flip event is contained in the every-parent latent-mismatch event. Dropping constraints with factor above one justifies the product of individually capped factors. No normalized conditioning on a bad outcome is used.

This yields ε=J²/γ[T−(1−e^(−2γT))/(2γ)] for a constant norm bound. The whole-input effect inequality is stronger than testing one bath state. The private-sign lift has the correct Walsh normalization 2^(−k), and the virtual seed parity meets the one-selected-parity-per-term premise. It depends on coefficients and baseline being independent of all selected signs and paths.

“Sharp” here identifies the proposed ε factor rather than a claim that the bound equals the physical error at finite parameters. The source itself distinguishes certificate and actual error.

## Independent finite checks, separate from the analytic audit

The newly authored check_sharp_product.py executes no acquired code. Twelve two-data-qubit/shared-qubit-bath instances use complex parity-dependent couplings and syndrome-preserving noncommuting bath blocks. Each test computes the largest eigenvalue of the endpoint Heisenberg effect compressed to the initial syndrome, optimizing over bath inputs. All twelve satisfy the sharp product; maximum ratio is 0.4579195381. Independent quadrature reproduces the Poisson-gap identity within 2×10^(−17).

A deliberate forbidden cross-parity term J X1 X2 produces actual joint-flip probability 0.000381918346 against an invalid singleton product 0.000000152747163, a ratio of 2500.33. This is a falsifier of dropping the locality assumption, not of the theorem. Finite checks do not prove universality or external correctness.

## Missing microscopic proof and remaining gates

UNIVERSAL_PAIR_CLOCK_ENVELOPE.md and the quantum-stability-genesis20261016 path do not occur in PR104's changed-file list. Repository search for UNIVERSAL_PAIR_CLOCK_ENVELOPE returns no results. Thus this PR does not supply that specifically named missing microscopic pair-clock source. Search indexing is not an exhaustive proof about every byte of repository history; this conclusion concerns the inspected PR and available search evidence.

The exact stipulated Markov generator, private controller independence, full support/completion imports, real boundary operations for spatial-memory transfer, finite-duration/noisy implementation, and matched physical cost remain distinct requirements. A finite-rate memory-only randomizer still does not uniformly repair arbitrary continuous joint-bath coupling. The new latent records are mathematical dilation outputs, not newly acquired experimental data.

## Additional bounded result

PEAK_RATE_CERTIFICATE_ADDENDUM.md closes the source's unresolved constant-action peak-rate-constrained certificate regime. Its global optimum is proved by a measure lower bound and potential/KKT argument; check_peak_cap.py independently verifies potential integrals, energy formulas and matching boundaries. This is an extension to a sufficient certificate optimizer only, not a physical-error lower bound or a hardware result.

All work is internal mathematical review, not external validation or historical-priority certification. No canonical edits or outreach were performed.
