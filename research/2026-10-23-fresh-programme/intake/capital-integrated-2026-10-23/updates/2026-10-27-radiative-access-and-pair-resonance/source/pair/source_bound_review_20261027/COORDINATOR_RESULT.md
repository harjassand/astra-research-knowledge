# Result: a comparator needs the same controls, not just the same hardware

## Decision

The Pro 2 source's faster-CZ comparison is valid **when arbitrary local single-qubit rotations are available**. Its label “equal-resource” is not established by the phase-only controls declared for the fourth-order echo. This is a qualification of the comparison, not a rejection of either mathematical construction. Preserve Pro 2's productive warm context; this test authorizes no branch retasking.

Two fresh, separately dispatched workers read the same full frozen P2_2134 proof. Neither inherited coordinator history or saw the other's output. Both were explicitly asked to distinguish phase-only from arbitrary local controls; the coordinator had already suspected that distinction. This is a source-exposed diagnostic, not a blind trial or a prompt-policy comparison.

## Accepted mathematical scope

Both workers independently derive that exchange `XX+YY` plus local `ZI,IZ` preserves equality of the two parity-block determinants. CZ violates that closed invariant, even up to global phase. Thus ideal exchange plus phase controls cannot synthesize or arbitrarily approximate this same two-qubit target.

Both also construct an exact CZ once transverse local gates are supplied. In the normalization `H_ex=J(XX+YY)/2`, two partial exchange intervals total `pi/(2|J|)`. With the source's `J_g=g^2/8+O(g^4)`, exchange time is `4pi/g^2[1+O(g^2)]`. The construction worker additionally supplies an ideal zero-duration-local-control optimality argument; no hardware time optimum follows.

The coordinator read both complete arguments and scripts, then replayed unchanged script copies in separate reviewer directories: all **13 audit checks and 12 construction checks pass**. Original worker outputs remain unchanged. This completed internal mathematical review accepts the stated finite-dimensional control conclusions. It does not audit the producer's infinite-volume spectral theorem, acquire physical pulses, or prove a lower bound for the full SSH Hamiltonian. The proposed fourth-order interaction lies outside the exchange-only model.

## Existing knowledge and physical relevance

The determinant distinction is established matchgate theory, not a new Astra theorem: [Jozsa and Miyake](https://arxiv.org/html/0804.4050v2). [Brod and Galvão](https://arxiv.org/html/1106.1863v1) explain related parity-preserving resources with further circuit assumptions; no many-qubit universality claim is inferred for this device.

Absence from a model is not absence from plausible hardware. The relevant [Kim et al. experimental SSH waveguide](https://doi.org/10.1103/PhysRevX.11.011015) has individual excitation-drive and flux-control lines. That makes broader controls a substantive comparator to investigate, not a capability to assume impossible. It does not establish the controls, error budget or gradient-port geometry of Astra's exact model. Existing [hard-core Green-function machinery](https://doi.org/10.1103/PhysRevResearch.6.043264) also remains prior art; no model-specific priority was established here.

## Method learning and next question

I could have rejected a useful construction by comparing its limited controls with a conventional method granted extra operations. The corrective method is to construct the competing operation explicitly and check its resource assumptions before allocating effort. The reverse error is also possible: withholding controls that a real platform already supplies can manufacture apparent novelty.

This case supports that concrete correction. It establishes no general superiority of fresh workers, a staffing mix, or a prompting policy. Both fresh workers received the resource distinction in their question; they did not independently discover the coordination hypothesis.

The next discriminating scientific question is whether a physically motivated implementation supplies transverse control cheaply and accurately, and whether the intrinsic interaction has a useful finite-coupling regime after memory decay and pulse errors. No new branch experiment or message was issued. The proof remains worth preserving independently of a speed advantage; civilisation-level capability remains unestablished.

## Reproduction and original sources

- Producer proof: `.astra-dispatch/sources/P2_return_2134_20261026/ASTRA_SSH_EMBEDDED_PAIR_RESONANCE_AND_CZ_20261027.md`, SHA256 `c44fcc6b9e0f51d0c7fe79e621a727c6165f8e39553bb6e9e07a94cb60ae6af3`.
- Independent arguments/scripts/results: `audit/CONTROL_RESOURCE_ASSESSMENT.md`, `audit/exact_control_check.py`, `audit/exact_control_check.json`; `construction/RESULT.md`, `construction/verify_exact.py`, `construction/exact_check_results.json`.
- Coordinator replay: `coordinator_replay/SUMMARY.json`, separate copied scripts/stdout/stderr under each worker name. Runtime `/usr/local/bin/python3`; scripts are standalone apart from SymPy and the unchanged producer-proof path.
- `QUESTION.md` records exposure and that this written note followed the first interim result; it is not a preregistration.
