# Fixed circuit run

Written before examining counts from the exact folded sampler.

- Input: `canonical_qec_circuit_gate_20261105/d13_r13_p1_1000_graph.json`, SHA-256 `e7fba390da626d9698ab858502031f6099199b59ab297364fb4675a185f27a0d`.
- Distance 13, 13 rounds, physical circuit noise parameter 1/1000. The fixed projected single-basis law and fixed integer matching costs 4/5 are retained.
- Fold modulus 64. Exact 2^-64 rounded independent probabilities, with the full conversion total-variation bound added to the final interval.
- Exactly 100,000 trials, seed 202611051864, Python Random ideal-bit abstraction. No stopping based on observed estimates.
- 99.9% two-sided exact outward Clopper–Pearson interval for the Bernoulli count, multiplied by the exact certified normalizer. Add the conversion bias to both endpoints. No arbitrary path-length cutoff: stop on terminal, null, or repeated vertex.
- Pilot sanity tests may precede this run with different explicitly recorded seeds. If a law/code bug is found, preserve the affected run and document the correction before restarting; no selective sample replacement.
- Count full setup, sampling, confidence calculation, proposal steps, all rejection categories, decoder calls, and peak process memory. Shared-host runtime is illustrative, not a speed record.

The first comparison is the same input and fixed decoder with the original tilted and triangle-only covers. This does not establish superiority over optimized splitting/MCMC or remove the known canonical-overlap scaling obstruction.
