# Exact anytime design decision from an acquired circuit kernel

## Statistical construction

For candidate j, the acquired integer-certified tuple sampler yields IID indicators Y_i with P(Y_i=1)=theta_j=P_{q,j}(F_j)/Z_j. Z_j is an exactly represented rational, not an estimated normalization. The graph probabilities q approximate the exact rational-input circuit marginal in total variation by at most epsilon_j. Thus |P_circuit(F_j)-Z_j theta_j| <= epsilon_j.

Under a putative Bernoulli theta, for every alternative u in [0,1], the likelihood ratio product L_n(u,theta) is a nonnegative martingale (with standard endpoint conventions). Integrating u against uniform measure gives

M_n(theta) = integral_0^1 (u/theta)^k ((1-u)/(1-theta))^(n-k) du
            = 1 / [(n+1) binom(n,k) theta^k (1-theta)^(n-k)].

M_0=1, so Ville's inequality gives P_theta(there exists n: M_n(theta)>=1/alpha)<=alpha. Hence C_n={theta:M_n(theta)<1/alpha} covers the true theta at all inspected times simultaneously. Its log-likelihood is concave, so C_n is an interval around k/n. The implementation proposes its endpoints numerically and verifies outward enclosure with exact integer comparisons. A failed proposal falls back to exact bisection. No floating result alone can authorize a decision.

For a dyadic p=a/D, outside the confidence set is certified by

(n+1) binom(n,k) a^k (D-a)^(n-k) alpha_den <= D^n alpha_num.

The lower endpoint is verified on the left of k/n, the upper on its right. At k=0 or k=n, the corresponding parameter endpoint is 0 or 1. Multiplying the enclosing interval by Z and expanding it by epsilon gives an anytime-valid circuit-model probability enclosure.

The candidate decision is pass iff U<=10^-12, reject iff L>10^-12, otherwise inconclusive. In particular, a strict equality cannot produce a false reject. Stopping times, batch inspection, and sample/resource caps preserve validity. A process cap that prevents interval output produces a blocked/inconclusive result, never a fixed-shot interval from partial counts.

For the historical d21 sample, the originally fixed shot count permits a fixed-shot exact Clopper-Pearson interval at alpha=1/3000. No optional-stopping rule is retroactively applied to it. Its provenance and prior result were known. d19 and d23 each receive alpha=1/3000 for their entire confidence sequences. A union bound gives simultaneous coverage >=1-3/3000=.999 for the three fixed candidate events. Independence across candidates is unnecessary.

The smallest-feasible selection checks every smaller candidate in {19,21,23}; it never infers monotonicity of failure probability from code distance. This is a finite design-set decision, not a theorem that no other code/decoder/round count is cheaper.

## Circuit and arithmetic accounting

The exact input law is p=1/1000 independently at each of the four specified types of physical noise channel in Stim's generated rotated-memory-Z Clifford circuit, not Stim's literal floating probability law. Acquired symbolic propagation computes the selected detector/observable marginal, factors each projected depolarizing channel exactly using its image-group Fourier transform, and encloses irrational factor rates with directed 192-bit dyadic arithmetic. Merging independent factors and rounding to q_den=2^64 is charged in the explicit sum-of-coordinate TV bound. Printed DEM floating values are diagnostic only.

The retained observable is the original generated memory-Z L0. The selected syndrome marginal is sufficient for this specified single-basis decoder and preserves its law, including common local projected effects. It does not preserve the unused detector family or claim the full joint logical Pauli channel. Reset/preparation and final readout occur in the circuit. No probability is relabeled as per-cycle or arbitrary-state quantum-memory failure.

The inherited tuple operation uses a rational positive supersolution checked over every finite state and residue with exact integer inequalities. Capped shortest-gap bounds relax the proposal; canonical decoding and terminal exact correction restore the target law. Repeated underlying fault edges are killed; no finite-length truncation is introduced. The integer-cost MWPM decoder contract and canonical tie rule remain explicit assumptions. The code's cost list is checked to be precisely {4,5}.

Statistical precision, numerical conversion error, and hardware-model uncertainty are separate. The operation charges the first two; it cannot estimate unmodeled coherent, leakage, crosstalk, drift, or correlated faults. Exact channel p is a model input, not measured hardware calibration. Python's Mersenne Twister supplies reproducibility, not a proof of ideal independent random bits; the finite-confidence theorem assumes ideal IID bits as in the acquired operation.

## Physical resource objective

For each candidate report data qubits d^2, used data-plus-ancilla qubits 2d^2-1, d rounds, and gate/reset/readout counts from its actual flattened circuit. Select the smallest candidate distance satisfying the target, which also minimizes these qubit counts in this prescribed family. There is no claim about a global architecture optimum or wall-clock quantum execution time: gate and measurement durations were not supplied.

## Prior art and alternative

This construction uses ordinary mixture-martingale confidence sequences and union-bound multiple-comparison control. Certified sequential QEC profiling, including ScaLERQEC, is directly relevant prior art. The novelty claim is deliberately empty: the deliverable is the executed decision, with model and arithmetic costs exposed.

Strong applicable alternatives include circuit-level splitting/MCMC (Mayer et al., Quantum 10, 2237, 2026; arXiv:2509.13678) and fault-subset/importance sampling with finite-confidence accounting. Their ability to reach probabilities far below 10^-12 already exists. The acquired comparison's fixed subregion heat-bath/BAR experiment reached only 13/31 rungs before 1,200 s, but this is not a tuned time-to-accuracy victory. No optimized matched ScaLERQEC or splitting execution has been supplied for this d19/d21/d23 decision. Runtime superiority over those incumbents remains unresolved.

Sources: acquired surface_code_rare_failure_release_20261105.zip; qec_fault_tuple_20261105/{THEOREM.md,SAMPLER.md,RESULT.md,PRIOR_ART_AND_SCOPE.md}; https://arxiv.org/abs/2509.13678 ; https://doi.org/10.22331/q-2026-10-15-2237 ; https://arxiv.org/abs/1308.6270 .
