# Coherent tree perturbations: targeted primary comparison

Reviewer: `/root/stopping_literature`. Date: 21 October 2026.

Task: determine whether a general published continuity theorem already supplies the owner's proposed upper stability for the persistent-memory family `V_s = cos(s) U + i sin(s) I`, and identify a useful predecessor for lower stability. No broad historical-priority audit was undertaken. The quantitative history bound itself was assigned to other reviewers; it is not certified by this literature note.

## Conclusion

The retrieved standard continuity theorem does **not automatically imply** continuity of the present closed infinite-memory capacity. It concerns independently reusable channel maps. The actual device instead reuses the same reservoir coherently, without resetting it between blocks. An upper bound proved directly from its coherent histories therefore addresses an obligation not discharged merely by citing finite-channel continuity.

A plausible route to a matching lower limit is available: use the exact Dyck block as a bath-independent inner code, bound the perturbed block in operator norm uniformly over the bath, and apply an outer error-correcting code to sparse bad blocks. The relevant classical-independent quantum error-correction and coherent fault-path methods are old. Their combination with the exact universal bath-return code is the specific obligation to establish here.

## 1. Leung–Smith: close channels, independent uses

Debbie Leung and Graeme Smith, *Continuity of quantum channel capacities*, Communications in Mathematical Physics 292, 201–215 (2009).

Primary source: https://arxiv.org/pdf/0810.4931

Corollary 14 bounds the unassisted quantum-capacity difference of finite-output channel maps whose diamond distance is at most epsilon by `8 epsilon log(d_B) + 4 H(epsilon)`. Theorem 11 proves the underlying entropy estimate for tensor powers. Section VI separately establishes continuity of two-way and backward-classical-assisted quantum capacities in the interior of their nonzero-capacity regions using channel simulations.

This is not a theorem for arbitrary persistent-memory processes. Applying it to an `L`-slot block as one reusable channel would supply independent repeats of that block channel, including its initialization. The present contract does not grant those repeats. Closeness of the one-use reduced map is especially insufficient because it discards the memory-output correlations which affect subsequent uses.

Read: capacity definitions, Theorem 11, Corollary 14 and Section VI setup/argument. Useful retrieval refs: `turn70view0`, `turn72view1`, `turn72view3`.

## 2. Kretschmann–Werner: the memory hypothesis matters

Dennis Kretschmann and Reinhard F. Werner, *Quantum Channels with Memory*, Physical Review A 72, 062323 (2005).

Primary source: https://arxiv.org/pdf/quant-ph/0502106

Theorem 13 assumes finite-dimensional ports **and finite-dimensional memory**, together with forgetfulness, to obtain its coding formulas. The surrounding double-blocking construction suppresses the influence of earlier memory. Those assumptions are not supplied by a stationary density or by a small operator-norm perturbation of the present infinite tree unitary.

There is a direct model-specific reason not to import forgetfulness at `s=0`: the owned exact Dyck word sends every initial vertex back to itself. Repetition preserves the distinction between different initial bath states at arbitrary block boundaries. Hence the uniform loss of initial-memory information required by a forgetful-channel reduction is unavailable for this base device. Whether a particular nonzero perturbation satisfies some other suitable mixing condition would require proof.

Read: memory model, forgetfulness discussion and Theorem 13 hypotheses. Useful refs: `turn70view2`, `turn72view4`, `turn72view5`.

## 3. Coherent local-noise predecessor

Barbara M. Terhal and Guido Burkard, *Fault-Tolerant Quantum Computation For Local Non-Markovian Noise*, Physical Review A 71, 012336 (2005).

Primary source: https://arxiv.org/pdf/quant-ph/0402104

Lemma 6 bounds coherent fault-path norms by powers of a system–bath interaction strength. The paper separates correction of sparse fault sets from a norm bound on the sum of bad histories. Its recovery discussion explicitly allows syndrome and bath systems to retain arbitrary residual states while the logical state is restored.

Its complete threshold theorem has spatial/locality and computational-model assumptions that are not automatically the tree's assumptions. It should be cited for the mechanism, not imported wholesale as a proof of tree capacity. The current setting is simpler in one respect: ideal external encoders/decoders are already allowed, so an outer transmission code need not establish noisy-gate fault tolerance.

Read: model assumptions, interaction-picture sparse-error argument, Lemma 4 and Appendix Lemma 6. Useful refs: `turn70view1`, `turn71view2`.

## 4. Outer codes need not assume independent errors

A. R. Calderbank and Peter W. Shor, *Good quantum error-correcting codes exist*, Physical Review A 54, 1098–1105 (1996).

Primary source: https://arxiv.org/pdf/quant-ph/9512032

Theorem 1 corrects arbitrary decoherence on at most `t` qubits, including a joint environment. The existence argument culminating in Eq. (30) gives asymptotic rates at least `1 - 2 h_2(2t/n)`. Thus a fixed packet size `k` can be handled with ordinary binary codes on `Nk` qubits: correcting `k floor(delta N)` qubit errors also corrects arbitrary errors supported on `floor(delta N)` whole packets. No q-ary code theorem is needed just to make the outer rate approach one as delta tends to zero.

Read: definitions, Theorem 1 with environment, Section V concluding counting argument/Eq. (30). Useful refs: `turn73view0`, `turn74view0`, `turn74view2`.

## 5. Constructive lower-stability seed (not a completed review)

The following argument was sent to the owner as a proposed next construction. It is stated here to distinguish literature input from an already accepted theorem.

1. Fix an even inner length `L`. Choose a `D=2^k` subspace of the exact Dyck code, with `k/L` as close to `3/2` as desired by first taking `L` large. Its ideal block acts as a known output isometry on that subspace tensor the identity on the entire bath, for every bath vector, including vectors entangled with earlier packets.

2. Extend the ideal inverse decoder to a local isometry on all block outputs, retaining its auxiliary output as an external environment. Telescoping the `L` unitary calls gives a uniform encoded-and-decoded isometry difference no larger than `epsilon=L ||V_s-U||`. The ideal decoded block is `I_D` tensor a fixed decoder auxiliary state tensor `I_E`.

3. For `N` such packets, expand each block into its ideal part and its difference. Because each ideal block leaves **every** bath state unchanged while transmitting its own packet, a history with bad packet set `J` acts nontrivially only on those logical packets plus the bath and their local decoder environments. Its operator norm is at most `epsilon^|J|`. The crucial mathematical check is this support statement; ordinary one-use channel closeness would not suffice.

4. An outer code correcting arbitrary errors on `t=floor(delta N)` packets corrects the coherent span of all histories with at most `t` bad packets. The bath coefficients can be correlated and noncommuting. The bad part has norm bounded by `sum_{j>t} binom(N,j) epsilon^j`, in particular by `2^N epsilon^(t+1)` when `epsilon<1`. It decays if `delta log2(1/epsilon)>1`.

5. One still has to prove that the recovered sum of good histories acts as identity on the logical code tensor a logical-input-independent environment vector, despite that sum not being normalized. Standard error-correction linearity should give this. Normalization of the actual full isometry then supplies the final error estimate from the bad norm. This step should be written, not replaced by a statement that each history is corrected separately.

6. Binary outer codes can have rate approaching `1-2h_2(2delta)`. First choose fixed `L` for the desired inner rate; then sufficiently small fixed `s` permits small delta with the decaying tail; finally take `N` to infinity. This would yield lower continuity at zero without fresh baths. The construction would establish approximate logical transmission, **not exact bath return** for the perturbed device.

If completed, the result would be a model-specific robustness theorem built from existing coherent-error correction. It should not be described as a new fault-tolerance principle, a general continuity theorem for all infinite-memory channels, or a practical code implementation.

## Limits and observed effort

Two focused search queries were issued in one search call. Four relevant primary PDFs were opened and their named theorem/proof passages inspected. No search absence establishes priority. No numerical calculation, hardware operation, external compute job or outreach occurred. Total inference cost, energy and monetary cost were not measured.
