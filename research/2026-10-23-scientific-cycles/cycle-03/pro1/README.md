# Astra Pro 1 coherent recurrent communication checkpoint

22 October 2026. Owner: Astra Pro 1. Recipients: Max and the evaluator.

## Strongest new result

For every fixed `0 <= beta <= 1/8`, the unchanged closed tree device with its actual fixed initializer `tau_pi` satisfies

`lim_n (1/n) max_rho I_c(rho^(tensor n), N_n^(tau_pi)) = 3/2`.

This is the **optimized iid (tensor-power) coherent-information value**. The marginal may be chosen separately for each horizon. Within a block every input factor is the same density. The explicit finite-horizon upper bound is `3/2 + (4/n)^(2/3)`; the unchanged critical density `diag(1/2,1/4,1/4)` gives the matching limit. Neither arbitrary correlated inputs nor independent nonidentically distributed products are included. This is not a general capacity converse.

The selected coherent seed at the fixed `beta=1/512` cannot stabilize the bath or sustain the intended high-entropy compression mechanism. More generally, every fixed iid qutrit density with entropy above `3/2` gives exponential escape from all sublinear-depth cutoffs for `beta<=1/4`, from every normal initializer. At `beta<=1/8`, starting from the actual `tau_pi`, bath entropy grows linearly and every asymptotically lossless bath projection has exponential rank, including non-coordinate projections.

## Why the result holds

An exact insertion resolvent on the two-seed binary Fock bath gives a bounded correction to depth. A cancellation controls its commutator uniformly near the critical bias, even though the resolvent norm can diverge. The root exchange remains in the calculation and is bounded by completion of a positive square. A qutrit spectral window covers every input of entropy above `3/2`.

A separate finite-band positive-tilt lemma turns the operator drift into an all-time escape estimate. Exact conservation of bath depth plus port color number then bounds the entropy of all outputs jointly, retaining their correlations. The actual initializer's normalized tails have explicitly controlled entropy, which upgrades bath entropy growth to the arbitrary-rank compression obstruction. Finally, purification of the initial bath and an explicit uniform corrector bound give the iid information ceiling, even for horizon-dependent marginals.

## Read in this order

1. `RESULTS.txt` for the claims and their exact quantifiers.
2. `output/pdf/COHERENT_INPUT_ESCAPE.pdf` for the complete mathematical account. Editable sources: `COHERENT_INPUT_ESCAPE.tex`, `FINITE_BAND_ESCAPE.tex`, `ENTROPY_AND_SCOPE.tex`, `IID_INFORMATION.tex`.
3. `REVIEW_STATUS.md` and the focused contributions for the algebra, spectral bridge, tilt, entropy/compression and iid-information challenges.
4. `CONTINUATION.md` for the selected two-call correlated input operation and its unresolved obligations.
5. `FAILED_ROUTES.md`, `REFERENCES.md`, `RESOURCE_RECORD.json`, and `VERIFY.md` for failure boundaries, comparison and observed costs.

`representation/exact_representation.py` is the unchanged exact infinite-bath algebra from Cycle2. The two substantive replay scripts check finite resolvent identities with their actual remainder, not a reflecting approximation or an all-time theorem. Analytical proofs carry the norm limit, domain, normality and uniformity obligations.

## Inherited result and live question

The completed capacity floor remains: for each fixed angle, one code sequence independent of the initializer works for every fixed normal bath, with vanishing full-diamond error at asymptotic rate at least `3/2`. This convergence is pointwise in the initializer. No terminal bath return or efficient compiler is claimed.

At the live fixed `beta=1/512`, the unchanged capacity interval is

`1.5 <= Q <= Q_backward_classical <= 1.58164276090312...`.

Strict gain versus plateau, and equality of assisted and unassisted capacity, remain open. The current result directs the next construction outside iid averages; it does not settle those questions. The owner selects a temporally correlated two-call family on the full nine-dimensional input space. This is not a restart of the balanced-only search.

## Preservation and private handoff

`preserved/Astra_Amplification_Cycle2_PRO1_20261022.zip` is unchanged: 2,041,187 bytes, SHA256 `1cb1b91c3c79e46d67d1686d7aa5d33ab889d28f826048710fa24ec6f81753c3`. It preserves the complete predecessor chain, including the exact whole-bath Dyck identity, inherited coding machinery, feedback/stopping results, earlier failures, and closed R1 source/provenance. No other owner's programme is reopened.

The immutable new ZIP and a UTF-8 base64 transport are delivered on the existing private Page route. The external `.delivery.json` receipt records exact native references, bytes, hashes and readback. Upload and byte verification do not assert that Max or the evaluator has read, accepted or integrated this checkpoint.
