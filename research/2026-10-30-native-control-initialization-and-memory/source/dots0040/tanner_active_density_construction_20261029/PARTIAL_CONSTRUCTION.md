# GPT active-hub density: a quantitative subclass result and exact open step
2026-10-29. New construction search, not a completed linear-distance memory theorem.

## Useful result
For the metastable, low-overlap, reduced-error regime of GPT Assumption 23, the proof yields

  g_active >= [alpha/(32 Delta^3)] U(e).

Here alpha is the positive constant in their Corollary 37. Constants depend on the fixed local-code degree, not blocklength. This does NOT yet hold for arbitrary small reduced errors by the argument below.

## Derivation
Let Y be the V1 vertices whose chosen nearest local codeword c_v is nonzero. Every error qubit touches Y: if both its endpoint codewords were zero, that qubit would be in BOTH endpoint minimum corrections. Flipping it would lower both local distances, contradicting metastability. Each local view has Delta^2 qubits, so

  |e| <= Delta^2 |Y|,  U(e)<=2|e|<=2 Delta^2 |Y|.

The case-3 expansion argument gives |Y|<=4 Delta |W|. Its Corollary 37 supplies at least alpha|W|/4 distinct special V0 vertices. The local analysis applies separately to each such vertex: either it supplies an improving flip within that local view, or it yields a stabilizer decreasing the assumed reduced error's weight, which is impossible. Therefore all those special vertices are active, proving the displayed constant.

This is an actual multiplicity extraction, not a transfer of FGL's mass theorem. It is usable componentwise only when the restricted component also satisfies the exact metastability/low-overlap assumptions and global/local read neighborhoods agree.

## Missing general quantitative lemma
GPT's cases 1 and 2 immediately finish the existence proof when there is a single-qubit improvement or a high-overlap local codeword. They do not establish that either defect type has positive density. One cannot infer that their complement occupies most of the system merely because the active set is small: the case-3 combinatorial lemmas use exact global metastability and low overlap.

A promising precise next target is a ROBUST case-3 estimate with defect penalties. Let A be the union of local neighborhoods of all single-qubit improving sites and all high-overlap V1 views. Prove a version

  number of special improving V0 views >= c U(e)-C |A|.

Each local defect certifies an active hub within bounded distance, so |A|<=C' g_active would then close g_active>=kappa U. The constants must be tracked through the disjoint-correction, R-flipping, exceptional-Y and local-codeword lemmas; this robust statement has not been established here. Merely deleting A or conditioning on its absence is not a proof, because it can change nearest codewords, reducedness and local potential.

## Primary sources and alternative route
Inspected GPT https://arxiv.org/html/2206.06557 , Theorem 10, Corollary 14, Definitions 16–24, the case split, and Corollary 37. Corollary 14 gives confinement only inside the proven correction radius, which is smaller than the raw existence radius.

The primary parallel-decoder literature https://arxiv.org/abs/2208.05537 and single-shot work https://arxiv.org/abs/2306.12470 give another route to constant-round contraction, but use mismatch-based decoder state. Their contraction must NOT be identified with density for GPT's syndrome-only U without a new decoder/interface construction. Search located these sources; their full proofs were not inspected in this short pass.

## Status
No counterexample to GPT active-hub density was constructed. General density, and consequently the proposed exp(N) continuous-noise memory upgrade, remain unproved. The metastable low-overlap constant above is the concrete new partial result. No accepted source was edited or externally published.
