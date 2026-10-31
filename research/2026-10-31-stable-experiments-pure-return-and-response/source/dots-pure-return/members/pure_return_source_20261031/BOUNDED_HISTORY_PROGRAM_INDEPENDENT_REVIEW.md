# Independent review: bounded-history program corollary

31 October 2026. Scoped concrete mathematical PASS, receiving the separately reviewed abstract compiler and stronger-input addendum.

## Source binding

I read all five sections, including the prescribed-label-snapshot receiving subsection and comparison boundaries, of `BOUNDED_HISTORY_PROGRAM_COROLLARY.md`, 11,571 bytes, and verified SHA-256 `1ea1ec3379a3e46ea6d09d8c3e71e247f2032ff059a0e891350383942209d4dc`.

This receives the final base source `1a097458af52e4b89746b2f5e38e8ba4ea9f8a835db731daef39b8e9ea71e032` and its review `62b766cb45cd243c2e0c75402a8f91aa311c940436d2d2c739b4d3e2b705962f`; where stronger inputs/controls or the near-linear schedule are used, it also receives the final addendum `39cfffcb2c38bf13da46a380760a994787caada7ecc99f43cc93e6953fc95069` and review `3d48ca120041a8a0dd37da86b5b5a08c40e9d16b10fa643e29e4c4e31ca798ef`. The low-rate per-window repair in that final addendum remains load-bearing.

## 1. Exact operation and source direction

The map transfers the oldest bit to a fresh environment, shifts the other bits, and inserts |+>. Preparing that fresh bit and permuting wires gives the promised acquired unitary extension and controlled inverse; no data are erased. Its adjoint on diagonal observables averages the two possible appended bits, so it realizes exactly the oldest-to-newest convention in the source, not the reverse shift.

After n applications all original source data, including entanglement with a reference, have been transferred out. The remaining source is |+>^n. Thus Phi^n is exactly the reset channel, (Phi†)^n Q=0, and the overlap A obeys A^n=P. With a reference the reset identity means P tensor the partial trace of the original source; it does not erase the reference. All binary strings are valid, so there is no hidden invalid-codeword extension assumption.

The pure fixed state, coefficient vector, and reflection have explicit polynomial circuits. The return horizon m=n is an exact operation certificate rather than a spectral or stationary-distribution inference.

## 2. Coupling access and signed centering

The controlled history-output block is explicitly an input circuit with paid cost. A table-generating classical program by itself is not treated as coherent operator access. The optional fair sign reset creates a separately specified centered physical model; it is not a transformation preserving arbitrary unsigned noise. Its tensor reset still gives Phi^n=Reset, now with two fresh event-output qubits, and PKP=0 follows exactly from the sign expectation.

The displayed Boolean benchmark is correct: conjugating (X+Z)/sqrt(2) by Z^f X^g gives [(-1)^f X+(-1)^g Z]/sqrt(2). Squaring yields identity because X and Z anticommute. Reversible evaluation and uncomputation of f,g therefore acquire the normalization-b unitary without enumerating 2^n histories. Taking f=x_1 and g=0 indeed gives noncommuting values, but does not prove classical hardness or exclude a smaller specialized model.

## 3. Classical controlled-process receiving, including observations

The system-valued source-diagonal observable algebra is invariant under both the channel adjoint and the Hamiltonian commutator. Restricting the adjoint dynamics therefore yields the intended classical-history/system generator. Equality of the initial state's diagonal restriction suffices for all observables in this algebra, even though the stationary quantum preparation is coherent.

A prescribed computational-label measurement with its classical outcome retained preserves this algebra in the Heisenberg picture. So do the specified classical updates and label-dependent system instruments when their FULL outcome-retaining maps have that property. Backward composition consequently gives equality of the accessible multitime output law. The qualification about the full instrument is essential: an unconditional algebra-preserving map could have coherence-sensitive individual outcomes.

The stronger-input compiler pays for these source-changing instruments using its enlarged count cap and updated budgets. It can also receive an actually sampled nonstationary classical history law, or an acquired correlated classical-history/system ensemble. No coherent square-root distribution preparation is needed, but the actual sampler, conditional state preparation and their errors remain paid. Known psi is still needed for internal reflections, not as the physical initial state.

These statements expose only the prescribed physical label snapshots and their allowed feedback. They do not expose private dark-emission times, colors, seeds or the full microscopic physical path. Arbitrary coherent source interventions remain a different quantum-source experiment.

## 4. Resource and comparison scope

Substituting m=n in the reviewed receiver gives the stated polynomial program/register dependence and logarithmic switching-rate/compilation-precision dependence, with all supplied operations charged. The stronger-input fixed-window schedule gives the optional near-linear extensive envelope only with its completed low-rate window scan. If the number of requested snapshots scales with the physical event count, the observation cost can itself be linear in that count. Statistical estimation and repeated execution costs are not removed.

The honest ordinary comparator is already an n-bit trajectory program, not necessarily a 2^n-state density table. Endpoint histories can be sampled from the capped Poisson count and at most n fresh bits. This does not automatically give the chronologically ordered coupled system evolution, but neither proves it hard. Known special functions may allow much smaller exact descriptions.

I checked the accessible primary abstracts for [OQuPy](https://arxiv.org/abs/2406.16650) and [Jorgensen–Pollock](https://arxiv.org/abs/1902.00315). They support treating process-tensor/multitime tensor-network methods as genuine memory-aware competitors. This receipt makes no general complexity comparison or lower bound against them, and does not turn their specific applicability conditions into a universal simulator promise.

## Verdict

No load-bearing gap found in the concrete program-to-acquired-interface map or its separately stated classical observation receiving. It applies to known finite histories of iid fair bits with the explicit optional sign process, not arbitrary n-bit state machines, learned sources, free path disclosure, or an unproved practical/complexity advantage. The reviewed whole machinery is being instantiated, not re-proved or generalized by the corollary.
