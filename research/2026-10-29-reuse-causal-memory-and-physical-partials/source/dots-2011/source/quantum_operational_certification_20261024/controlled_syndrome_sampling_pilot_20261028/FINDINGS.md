# Sampled controlled-syndrome pilot: future coverage has a real cost

28 October 2026. AUTHOR numerical study; independent audit requested. This is a floating simulation of actual ordinary calibration calls and the resulting coherent receiver, not hardware, certified theorem-budget acceptance, or execution of the rational spectral-sign/compiler algorithms.

## Physical instance and actual learner information

One fixed unknown 8-by-8 output mixer V follows independent physical bit flips on a known three-qubit repetition encoding. The physical patch is known; support localisation is not part of this pilot. The learner knows the encoder, labels it prepared, the chosen injection label, and its local Pauli settings/outcomes. V and the physical flip probability p are used only by the simulator and posthoc evaluator, not by the fitted receivers.

Native calibration prepares the normal encoded logical state. Active calibration inserts uniformly one of I,X1,X2,X3 AFTER the known encoder and BEFORE the unknown physical channel, paying two random bits and at most one extra X pulse per call. This is an additional hardware port, not a free change at a logical black box or post-source depolarization. Payload scoring uses the NORMAL uninjected native channel in every arm. The fixed logical/gauge encoding U=V U_majority is common; probe and payload error weights differ.

Every simulated call individually draws logical X/Z axis/sign, active injection if applicable, three independent physical error bits, three output Pauli axes and the actual Born outcome. Stored count tensors retain all learner-accessible sufficient statistics. No conditional-success oracle, aggregate binomial replacement for those calls, or supplied Choi matrix is used by the estimator.

The primary estimators take finite-sample signed product-Pauli shadows, fit Hermitian matrix signs, and deploy the actual three-controlled-reflection coherent SWAP into an initially maximally mixed ancilla. All physical outputs are retained until that circuit ends. Native and active-unlabelled use the same estimator. Two additional active estimators reuse exactly the SAME active records: one weights by the sum of the three known injected computational-bit labels; the other fits three individual bit reflections and then the majority sign. These are equally informed conventional refinements, not independent acquisition runs or a claimed optimal estimator.

## What was executed

- Small budgets: N=512,2048,8192; p=0,.01,.1,.4;16 independent banks per arm/setting.384 calibration banks and1,376,256 per-call RNG simulations.
- Larger budgets: N=65536,262144; the same four p values;8 independent banks per arm/setting.128 banks and20,971,520 additional per-call simulations.
- Total:512 independent banks,22,347,776 simulated calibration BLOCK calls and1,024 decoder evaluations. Three active decoders share each active bank. Different N banks use different seeds and are not repeated prefixes.
- One fixed mixer V is used across all settings. These are not512 independent source models.
- Each block has three physical noise exposures and three output Pauli readouts, plus the actual encoded input preparation. The active variant adds the stated injection operation; those resources are not matched by pretending native calibration has the same port operation.
- No unknown terminal payload was sampled. Full receiver/native-channel Bell performance and the all-gauge virtual effect were computed analytically from the simulated model after learning. No nontrivial retained-memory dynamics were simulated. The all-gauge score is an operator diagnostic relevant to the theorem's future-memory guarantee, not acquired environmental information.
- Binary64 eigenvectors/matrix signs are used. Unitarity, effect normalization and the true-generator zero-error control passed numerically. This is NOT the received finite rational Jacobi compiler or physical gate synthesis.

## Results: distinct objectives must not be conflated

At N=262144, averaging8 banks:

* p=0: native current loss .000728, but its worst-gauge virtual loss .887902. Active-unlabelled current loss .002942, worst-gauge .006107. Active calibration substantially covers previously unexcited gauge sectors, while spending accuracy on sectors irrelevant to the current noiseless source.
* p=.01: native excess above the informed majority receiver .016081, worst-gauge .761094. Active-unlabelled excess .004202, worst-gauge .006836. Active label-triple excess .002896, worst-gauge .006235. The source-informed native majority loss is .000298 and is not included in these excess numbers.
* p=.1: native excess .007899, worst-gauge .055048. Active-unlabelled excess .004876, worst-gauge .009767. Active label-triple excess .003461, worst-gauge .009513.
* p=.4: native excess .013563, worst-gauge .073660. Active-unlabelled is WORSE: excess .047745, worst-gauge .223006. Label-triple improves on active-unlabelled but remains worse than native: excess .023161, worst-gauge .119347.

The smaller budgets are not ready-made practical memories. For p=.01,N=8192, active-unlabelled has current excess .106464 and worst-gauge loss .187295; native has smaller current excess .044940 but much worse all-gauge loss .886876. The full run-level results are retained, including these failures and variance across banks. The figures above are means, not empirical confidence certificates or proof of a uniform advantage.

The scientifically useful observation is the predicted tradeoff: deliberately informative probing can learn a reusable logical algebra when rare/no native syndromes leave its future action underdetermined. It can cost current-task accuracy and become worse near the high-noise boundary. The label-aware comparisons also show that available probe labels should not be discarded by an artificially weak benchmark.

This study does not establish novelty, a scalable fault-tolerance architecture, an advantage over every equally informed conventional estimator, or generic control under unknown noise. The iid bit-flip/fixed-mixer model is substantial. The separate deterministic-X1 counterexample shows that active injection can violate the required structural class for other otherwise correctable native sources.

## Reproduction and files

Run run_pilot.py and run_large_budget.py with the saved Python/NumPy environment; OPENBLAS_NUM_THREADS=1 was used for the original execution. Each results.json records versions, source matrix/seed, every bank seed, sample count, per-decoder scores and all summary rows. ordinary_counts.npz stores the actual sufficient count tensors; large_budget/ contains its separate continuation outputs. No earlier source/check file is modified by these programs.

Source references: ../ordinary_controlled_syndrome_excitation_witness_20261028.md and the received margin-free local-gap/complete CP-domination constructions. The label-aware variants are numerical candidates here and do not inherit a theorem receipt merely by appearing in a pilot.
