# Independent review: present-channel singlet Dirichlet certificate
Reviewer: independent child `review_current_channel_symmetry`; 2026-10-29 UTC.
Disposition: **accepted at the stated mathematical and finite-block statistical scope**, subject to the explicit operational assumptions below. This is a new theorem, not an extension of the earlier exact-noise-model review by implication. No novelty, hardware, optimality, or generic noise-learning acceptance.

## Governing material
`../THEOREM_v1.md`, `../check_v1.py`, `../check_v1.json`; exact SHA-256 identities are in `RECEIPT_v1.json`. The author's program was independently rerun and output matched its JSON byte for byte. The separately written `check_certificate.py/.json` does not import author code. Numerical tests supplement the derivations below; they are not proofs or large-system execution.

## Independently checked load-bearing argument
Write M=n(n-1)/2. The transposition class sum in partition lambda has content eigenvalue c_lambda. Among nontrivial partitions the largest content is that of (n-1,1), equal to M-n: repeatedly transferring a lower-row removable box to the first row increases content until this shape is reached, without reaching (n). Thus the complete-graph Laplacian has nonzero eigenvalues at least n in every unitary representation. The representation on matrices is unitary in Hilbert-Schmidt norm, so its orthogonal invariant projection G obeys

    sum_a ||K_a-GK_a||_F^2 <= (1/n) sum_edges sum_a ||[S,K_a]||_F^2/2
                            = (D/n) sum_edges delta_S.

The last equality uses only sum K_a^dagger K_a=I; it does NOT assume unitality, random-unitary noise, reversibility, locality, or an environment model. Independent exact-integer checks enumerate all partitions for n=2 through 24 and recover gap n.

G(K_a) acts as scalar alpha_a on the whole spin-zero sector by its one-dimensional SU(2) representation factor. For arbitrary specified K-dimensional subcode E, let Psi=(E tensor I)Phi_K. The squared norm of the component of (K_a E tensor I)Phi_K orthogonal to Psi is at most ||(K_a-GK_a)E||_F^2/K. Summing uses trace preservation and gives physical Bell loss at most D/(Kn) times sum delta. The TP decoder adds nonnegative Bell overlap from its leakage replacement. This proves the claimed bound for its actual completed logical channel.

Important checked pitfall: Tr(E^dagger K_a E)/K is NOT generally alpha_a when the chosen power-of-two subcode is a proper subspace of the singlet multiplicity. The manuscript correctly does not assume this. Our independent n=6 reflection example has alpha=0.6 versus restricted trace scalar 0.5; the orthogonal-component bound still holds.

The code rate is k=floor(log2 Catalan(n/2))=n-(3/2)log2 n-O(1). K>d0/2, hence D/K=O(n^(3/2)); the random-edge witness coefficient C=(D/K)(n-1)=O(n^(5/2)). Even n>=4 gives nontrivial K>=2. The theorem excludes n=0 and odd n; n=2 has K=1 and is not a useful quantum memory.

## Physical test and logical metric
An actual controlled-S, channel-on-data-only, controlled-S circuit from |+><+| tensor I/D has off-diagonal ancilla block N(S)S/(2D). Its minus probability is [1-Tr(S N(S))/D]/2=delta/2, including for nonunital channels. Independent density-matrix simulation confirms the equality. Uniform independent edge sampling gives q=sum delta/(2M), without estimating each edge or multiplying confidence costs by M.

A full logical Pauli twirl of the completed encoded channel makes its normalized Choi state Bell diagonal and preserves Fe. Its identity probability is Fe. The maximally entangled input gives half trace distance 1-Fe, while the Pauli-mixture triangle bound gives half diamond at most 1-Fe. Thus equality is exact. Independent K=2,4 Kraus-level twirls confirm Bell diagonality and the Choi equality numerically. This is a reference-complete statement for the averaged **retired-key logical service**, not untwirled service, disclosed-key service, or logical-plus-bath output. Access to the key can invalidate the stated metric.

## Finite-data/control audit
For a frozen frame and a prespecified fixed sample count, iid trials from the same CPTP channel make the stated upper Clopper-Pearson endpoint valid. The endpoint solves the lower-binomial-tail equation, with r=m handled by q_U=1. For r=0 it equals 1-beta^(1/m), so m>=C log(1/beta)/epsilon is sufficient for zero-defect certification. This is an acceptance-cost statement, not a promise that an arbitrary channel passes. Independent grid enumeration verifies upper-interval undercoverage is at most beta for tested m values. The mathematical validity follows from binomial-tail inversion, not the grid.

A learned frame must be frozen before validation. A new frame selected using the validation results needs fresh data and a new confidence budget. Repeating validation until a pass or adaptively stopping at arbitrary m is not authorized by this fixed-block interval; confidence spending or a valid confidence sequence is needed. This does not block the stated one-block theorem.

The additive test bias and service implementation budgets are correctly placed: error <= min(1,C(q_U+b_test)+b_service). These are separately warranted physical control bounds, not consequences of a small witness. If test errors vary by shot, a uniform conditional lower bound on each actual minus probability by q-b_test gives the same conservative upper inference by binomial stochastic domination; otherwise one must not call arbitrary drifting observations iid.

## Operational assumptions retained, not solved
- The tested object is the same reset-to-readout CPTP channel N as used for service, independent of the private test/twirl random seeds except through declared input. Hidden role-dependent noise or initial input-bath correlations are not covered.
- Validation calls have the declared independent/reset interface. Arbitrary retained bath memory is allowed inside one call, not silently across iid calls. An N_T certificate costs T exposures per trial and certifies that horizon, not all future times.
- Maximally mixed preparation uses independent uniform product bits. Preparation records must not produce unmodelled bath correlations. The control ancilla remains isolated/coherent through the channel and requires calibrated preparation/readout and controlled pair routing.
- Specified frame gates, controlled-SWAP synthesis, Schur/Dyck encoder, TP decoder, logical Paulis and key retirement must actually be available at paid precision. The theorem makes no claim that their finite-precision budgets or scalable hardware implementations have been demonstrated.
- The exact group average is proof-only; the protocol does not require n! operations. Conversely the dense small-n test implementations are not the scalable compiler.

## Comparators and significance accepted
This removes the earlier exact collective-noise promise for a **current-channel sufficient certificate** at a particular high-rate singlet code, using local controlled-pair probes and a retired-key service modification. It does not prove global channel-norm proximity or efficient discovery under arbitrary noise, and it may falsely reject channels excellent on the code.

The manuscript includes the strong equally informed comparator: direct encoded random logical state-2-design survival estimates Fe without a protected reference and without the polynomial witness sample penalty, but executes the code compiler/decoder every validation call. Consequently no unconditional shot, control, practical, or asymptotic advantage over that baseline is accepted. The potential trade is a simpler calibration circuit against larger shot and control-accuracy requirements.

## Independent executable coverage
`check_certificate.py/.json`: exact partition gaps n=2..24; independent random nonunital CPTP channels n=2,4,6; nonvacuous near-identity channels; explicit TP decoder; explicit controlled-SWAP density circuit; proper-subcode scalar counterexample; rare-sector controlled-Z stress case; K=2,4 logical Pauli twirls; binomial upper-interval coverage grids. All assertions passed. Results at generic strong noise are intentionally often vacuous bounds >1; the theorem clips them at one. No statistical or physical experiment was performed.
