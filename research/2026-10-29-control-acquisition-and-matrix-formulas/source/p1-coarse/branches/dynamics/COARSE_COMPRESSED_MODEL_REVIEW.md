# Scoped review of the certified two-state coarse model

## Verdict

The new use of the accepted confidence cover in `core/coarse_compressed_model.py` is sound. The saved rational two-state candidate is a valid positive substochastic model, and its 84 deterministic checks certify every finite switching word from the declared preparation at absolute survival error at most

\[
15583954301/250000000000=0.062335817204.
\]

The maximum error bound at retained branch words is approximately 0.01676534263. This is a certificate for a finite approximation to the scalar response, not a claim that the physical source has two states or finite hidden rank.

This review checked only the new implication, exact candidate admissibility and saved node bounds. It did not repeat the accepted cover statistics, source acquisition, trajectory work or weak-Poincare review. No source queries or trajectories were generated.

## The cover-to-model implication

Let f(w) be the true survival response and g(w) the candidate's total survival after the same word. Condition on the already accepted simultaneous event that f(v) lies in the saved interval [l_v,u_v] for every selected node v. This event holds uniformly before selecting the fitted candidate.

If a word ends at a branch node v, then

\[
|f(v)-g(v)|\le\max\{|l_v-g(v)|,|u_v-g(v)|\}.
\]

If a word extends a terminal prefix v, write it as vs. Irreversible absorption gives 0≤f(vs)≤f(v)≤u_v. Candidate substochasticity gives 0≤g(vs)≤g(v). Therefore

\[
|f(vs)-g(vs)|\le\max\{u_v,g(v)\}.
\]

The larger of the two prefix survival uppers is sufficient; adding them would be unnecessarily loose. The accepted finite tree guarantees that every nonempty word either ends at a retained branch or extends a terminal prefix. The empty word is exactly one under both preparations. Taking the maximum of these finitely many bounds proves the all-word result.

The candidate may be chosen using the same observed data. On the simultaneous interval event, the displayed inequalities hold for **every** admissible candidate that passes their deterministic checks. Consequently fitting the proposal to early moments consumes no new confidence budget and needs no independent validation batch. The float-based moment calculation and rounding propose a rational candidate; they do not establish its validity or substitute for the exact final checks.

## Exact candidate checks

The saved maps are

\[
M_0=\begin{pmatrix}
0.632329&0.119580\\
0.119580&0.131730
\end{pmatrix},\qquad
M_1=\begin{pmatrix}
0.497697&0.070398\\
0.070398&0.112506
\end{pmatrix}.
\]

These decimal displays denote the exact finite rational values in the saved result. The initial distribution is (1/2,1/2), and the receiver sums its two live components.

Every entry is nonnegative and both matrices are exactly symmetric. Their row sums are respectively

\[
(0.751909,0.251310),\qquad (0.568095,0.182904),
\]

all strictly below one. The implementation evolves a column distribution. Symmetry is relevant here: the checked row sums are also the column sums, which ensures that total survival cannot increase under either matrix.

The independent replay additionally verifies strict operator positivity and strict contraction, by the positive principal minors of each M_i and I−M_i. The determinants of M_0 and M_1 are exactly

\[
6899732277/100000000000,
\qquad 25519010139/500000000000.
\]

Operator positivity is stronger than the entrywise positivity and substochasticity needed for the terminal-prefix argument. The actual candidate satisfies both meanings of positivity.

The replay multiplies the rational matrices independently and recomputes the scalar survival at every selected node. It verifies every saved prediction, every branch or terminal bound, the aggregate maximum and the exact empty-word value. All 84 checks pass. The accepted cover's content hash is checked against its earlier review receipt, without rerunning that review.

## Scientific scope

This closes the finite-absolute-accuracy obligation for a compact two-state model of the declared coarse survival experiment. The same approximation applies to every finite word of the two operations from the same initial distribution and receiver. The physical hidden dimension remains unbounded; no upper bound on it was inferred from the fitted dimension.

The certificate does not control normalized hidden states conditional on survival. Dividing a small unconditional probability by another small probability can amplify the error. It also does not control lifetime moments or an infinite sum of survival probabilities: a uniform absolute error need not be summable. Indeed the candidate's common row-sum cap is strictly below one, so its repeated-operation mean lifetime is finite, whereas the private countable fixture has an infinite mean lifetime. This is consistent with the certified absolute-response metric.

## Preserved check

The independent checker is `replay_coarse_compressed_model_review.py`, with saved receipt `COARSE_COMPRESSED_MODEL_REVIEW_RESULTS.json` in this directory.

Reviewed model result SHA256:

`ace0f538a2443817556e7556461e9dada47f2b0003914ea9627767283a2d80c4`

Accepted cover result SHA256:

`2431a4c2da4f7b17e24d96dfbe3613e657f7f2c731dd078bf7876093e0ee4a57`
