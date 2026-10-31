# From classical samples to a reusable source representation
31 October 2026. This guide describes a restricted acquisition prototype. The full downstream quantum simulation algorithm remains mathematical, not implemented here.

## The exact access/model promise
The source has a complete, correctly observed n-bit state. A chosen-input one-step query at x returns

    F x XOR beta XOR eta,

where eta is fresh, independent and uniform on one unknown fixed binary subspace. F, beta and that subspace are unknown. The source is a classical exogenous process, and the same kernel is used during training and reuse. Each query requires whatever state preparation/reset and observation operations the real access interface entails; all are charged.

This is exact single-update access, including self-loops, not merely waiting for a label change. Passive trajectories, hidden states, unreliable readout, drift, nonuniform or correlated noise, and unknown nonlinear source updates are not covered. Finite data do not verify this promise against arbitrary unseen behavior.

The continuous-time consumer additionally needs its known independent Poisson clock/rate and the actual future system-coupling operations. Neither unknown quantum backaction, physical source-system coupling nor clock-rate calibration is learned from these label samples.

## What the prototype acquires
At zero input it learns the noise subspace from output differences. It then uses one query at each basis input to acquire the deterministic quotient dynamics. Under the promise, one high-probability event makes the inferred transition LAW exact on every input, not just on observed samples. Original private noise coordinates and a hidden physical implementation are not identified.

The query count is

    2n + ceil(log2(2/delta)) + 1.

Every call may need a chosen-state preparation/reset, and every returned label has n bits. Linear algebra, stored data, realization construction and future execution are additional paid work. The learning routines have no coherent sampling oracle and do not inspect the hidden implementation of the sampler supplied by a caller.

If the inferred kernel is controllable in the stated uniform-source class, compile_affine_source.py constructs a DIFFERENT quantum realization of the same classical label kernel. It uses explicit binary linear algebra and reversible gates, then checks it with the separate Clifford-source verifier. This can repair a naive quantum realization that retains unwanted coherence. It does not preserve arbitrary coherent operations on the original dilation or disclosed original random coins.

## Run the supplied transcript example
From this directory:

    python learn_affine_source.py examples/learned_history.transcript.json --output learned.json

The transcript lists outputs in the fixed query-plan order. The callable query_plan(n, delta) returns the exact input list. The callable sample_and_compile(n, delta, one_step) is provided for an independently authorized classical sampler; this package performs no device or network access on its own. All included tests use synthetic sources or exact finite enumeration.

The result contains the learned affine model, its law-preserving Clifford realization, a pure-return certificate, and explicit statistical scope. The verifier checks consistency of this inference and compilation with the supplied transcript; it does NOT prove the real source belongs to the model family or that this particular inferred model is correct.

To synthesize from an already known classical affine program instead:

    python compile_affine_source.py examples/xor_noise.affine.json --output realization.json

That input contains n, F_columns, G_columns and offset, as binary column masks. Controllability is checked. Rejection only means this uniform controllable class was not admitted, not that every other source representation or simulation is impossible.

## Do not lose the confidence when reusing a model
The failure bound is frequentist over acquisition transcripts for every fixed source satisfying the promise. The admitted-transcript bound is an average conditional on admission, NOT posterior certainty for each observed transcript and NOT a guarantee after arbitrary rare later postselection.

On the single successful acquisition event, the same exact law supports all finite future adaptive uses, even when the transcript is public. Statistical failure need not be charged anew for every use. Numerical simulation errors and real execution costs do still accumulate and need their own budget. Each downstream consumer retains its own prescribed-time and observable-algebra restrictions.

The deliberately preserved rare_wrong_admitted_transcript.json is a counterexample to overclaiming. Under the full-noise two-bit test source (F=0, beta=0, noise uniform over all four states), that transcript has positive probability. Its inference record verifies and the inferred source admits, yet the inferred law is wrong. Across the exact admitted-transcript experiment in the test, the wrong-law fraction is1/21 at requested delta1/4. This is consistent with the theorem and disproves a pointwise-posterior interpretation.

## Guarded coupling interfaces
acquire_affine_pauli_consumer.py accepts only source-diagonal sparse Pauli couplings after exact cancellation of duplicate terms. It rejects coherence-sensitive source terms, because preserving a classical kernel does not preserve an arbitrary original quantum task. It does not verify a future control-instrument program.

acquire_learned_pauli_consumer.py additionally carries the learning transcript digest and confidence/model-promise limitations into that guarded coupling output. It never converts the inference record into proof of the real source's truth. It emits classical mean/centering and circuit specifications; downstream simulation is not executed.

The nontrivial source-averaged Hamiltonian remains physical and must be priced. A generic mean BLOCK can be encoded by compressing the supplied coupling with prepared reference-state auxiliaries, but that does not calculate its classical numeric value or make its real dynamics free. The sparse-Pauli module computes numeric means only within its stated input class.

## Scope of the achievement
This is an executable acquisition-to-representation pipeline under an explicit finite-field model and chosen-state access. Its component linear-identification, tableau and deadbeat-control methods are established machinery. It is not model-free source learning, a new general theory of intelligence, a physical experiment, or a demonstrated practical advantage over strong learners/compilers using the same information and retained knowledge.

The exact-law theorem and the numerical/code audits have separate receipts. Statistical assumptions, mathematical compilation and executed code must not be conflated. New results and code files should be used only with their current source-bound review status.
