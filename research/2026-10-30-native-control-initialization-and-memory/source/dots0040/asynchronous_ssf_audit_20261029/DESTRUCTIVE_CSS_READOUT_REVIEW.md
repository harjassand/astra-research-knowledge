# Independent hostile review: controlled destructive CSS readout
2026-10-29. Additive review; frozen transactional-memory results are unchanged.

Reviewed source:
`producer-workspace/DESTRUCTIVE_CSS_READOUT_CANDIDATE.md`
SHA256: 41b91064864638c848fdd7bd14adbf025b41866c84872b7801a650b7388a46b2.

## Verdict
**The single-D0-root suffix and measurement-compatible-span argument are valid under the candidate's explicit controlled-readout assumptions, interpreted precisely below.** No counterexample was found to the pointer-fault reduction, positive effect argument, or removal of the O(N) artificial-block factor.

One operational premise must be made completely unambiguous: the nominal terminal process must actually implement U_copy F^dagger, including the transition into readout mode. Every native term incompatible with that circuit must be suppressed or explicitly included and compensated in its prescribed constant-depth nominal implementation. Merely disabling visibly DATA-affecting terms is not sufficient if residual controller evolution changes the frame while F^dagger gates are being applied. Arbitrary residual dissipative evolution cannot be conjugated backward as a unitary. This is an extra controlled-stage assumption, not a consequence of the autonomous memory theorem.

With that premise, the theorem is a controlled destructive logical-Z (or logical-X) measurement with a certified classical-output diamond bound. It does not retrieve an arbitrary quantum state, make classical processing autonomous/reliable for free, or cover general coherent drift.

## 1. Exact CSS output POVM
For a physical Z-basis outcome x, let s=H_Z x, c(s) be the deterministic X-sector SSF correction, and f(x)=L_Z[x XOR c(H_Z x)]. The output effects are diagonal sums over the strings with a given f(x).

They are invariant under X stabilizers: an X stabilizer changes neither H_Z x nor L_Z x. Hence these effects commute with X-stabilizer syndrome measurements. Z corrections commute with the product-Z outcome effects and cannot change f(x). This proves that discarding the unused X-syndrome extraction and Z-error correction from a full terminal CSS decoder preserves its logical-Z output POVM. X-sector candidate choices must use their relevant syndrome, as in the accepted sectorwise SSF implementation.

The statement applies to the entire classical-output channel with an untouched reference, not merely to diagonal inputs. Equality of the POVM effects gives equality of the reference-conditioned output states after the unobserved DATA are traced.

## 2. Relocating readout faults: exact channel algebra
The nominal frame and copy circuits are unitary on their declared DATA/controller/pointer registers. A fault inside the frame circuit can be moved forward through its remaining nominal gates by conjugation. A fault inside the copy circuit can be moved backward through its preceding nominal gates. Keeping their chronological order produces ideal F^dagger, a sequence of conjugated CPTP events, then ideal U_copy and observation.

These moves do not invert faults, measurements, or native dissipation. CPTP character is preserved, common-bath coefficients are retained, and a bounded-depth local circuit enlarges each support only by a bounded light cone. Fixed-range primitive supports and bounded incidence remain bounded after this enlargement. The relevant DATA graph must include all such enlarged effective support cliques; its counting constants must be recomputed for this enlarged graph, although the deterministic SSF arguments remain valid.

Fresh pointer preparation is an ideal baseline resource whose modeled local preparation/write errors must enter this same CPTP event model. An unmodeled detector error after ideal observation is not covered by the quantum bound; the separate p_cl interface must cover it if claimed.

## 3. Pointer faults do not need a false DATA-only quantum channel
Expand each relocated local Kraus operator in DATA and pointer Paulis, with arbitrary controller/bath coefficients. All pointers start in |0>. The product of pointer Paulis therefore leaves a definite pointer basis string a on a fixed Pauli term, up to a coefficient phase. Ideal copying then produces observed string x=y XOR a when the corresponding DATA Z string is y.

If the memory-plus-readout DATA term has bit-flip mask e_X, the relevant effective error is

  e_eff=e_X XOR a.

For an encoded logical-Z basis input z, any compatible y obeys H_Z y=H_Z e_X and L_Z y=z XOR L_Z e_X. Thus

  H_Z x=H_Z e_eff,
  f(x)=z XOR L_Z[e_eff XOR c(H_Z e_eff)].

On a certified safe branch, the final effective X error is an X stabilizer, so f(x)=z. DATA-Z and pointer-Z factors can change phases/coefficient vectors but cannot violate this support implication. This is the required measurement statement. It does not assert preservation of the whole logical quantum state by arbitrary pointer faults.

Each local relocated insertion contributes only a bounded effective mask; mapping a pointer to its paired DATA coordinate preserves bounded geometry. Identity or canceling masks only make the support-mass upper bound looser.

## 4. Measurement-compatible span and diamond distance
Fix a fine actual record and pointer outcome x. Every safe Pauli term annihilates logical-Z basis inputs other than f(x). Therefore its corrected restriction, and the coherent sum of all such terms, has the form

  K_x Enc=B_x <f(x)|.

A fixed mixed initial ancillary state can be purified or Kraus-expanded without changing the conclusion. After tracing unobserved output registers and grouping x by logical z, the safe classical-output map has effects a_z |z><z|. There is no need for the a_z to be equal. Replacing this by a scalar multiple of the full ideal measurement without proof would have been wrong; the candidate does not do so.

Completeness and positivity give 0<=a_z<=1. A uniform bad-record effect <=delta I implies

  0<=I-sum_z a_z|z><z|<=delta I.

The missing part of the ideal logical-Z measurement is itself a CP classical-output map with norm <=delta. Adding the bad CP map yields distance <=2delta, including entangled logical/reference inputs. Thus the final norm argument is sound.

For the additional 2 p_cl term, p_cl must be a certified uniform failure probability for the complete classical storage/computation/output process, not a per-bit marginal. Uniformity over input bit strings suffices for a genuinely classical local postprocessing channel. No independence from quantum readout faults is needed; one may union-bound the actual failure event.

## 5. Why one D0-only suffix is enough
The suffix contains the finite noisy readout circuit followed by ALL noiseless classical SSF scans. There is no need for a service guarantee or a D1 contraction statement inside it. In the effective one-sector Pauli history, the only bad insertions are the bounded readout masks. Each accepted classical SSF move lowers the relevant syndrome potential. Therefore the unconditional D0 work/footprint argument applies for the entire suffix regardless of its number of scans:

  |K|<=C_seed[|R_in intersect K|+Q_ro(K)].

A no-change scan is reached after at most n_Z+1 scans. If every enlarged suffix component is small, the final canonical representative has componentwise size below the FGL cutoff and is equivalent to the actual effective error. Nonzero syndrome would give an accepted candidate in one component, also globally accepted by read-footprint locality, contradicting the no-change scan. The final syndrome is zero, and the effective error is a stabilizer. This proves the actual computed classical output is correct without performing minimum-weight optimization.

Any failure consequently has a first cutoff-bad component in an earlier physical memory block or in this one suffix. At a suffix root, D0 gives either Q_ro density or a target in the preceding reduced representative. In the latter case the chain immediately enters prior genuine memory blocks. No no-service event in the noise-only interval is falsely assigned a small probability.

The direct readout count has the stated Poisson mean and Chernoff exponent. A suffix-root terminal has V=M; otherwise the existing geometric volume bound applies. The maximum of the memory and readout per-terminal-set bases safely bounds both types. Rooting at L+1 layers and retaining the conservative two-sector/R prefactors proves the displayed inequality, with constants computed on the enlarged graph.

## 6. Stronger than the earlier appended-scan theorem
This improvement is real. It replaces the O(N) appended proof-block factor by ONE root-only suffix, because D0 has no duration/service hypothesis. The earlier polynomial-time ideal mathematical decoder is the special case Q_ro=0 and can likewise use L+1 instead of L+J. This is an additive strengthening, not a revision of the previously accepted proof.

The classical work remains O(N^2) in a straightforward implementation, and the code/logical-parity description has polynomial size. The destructive protocol needs no quantum coherence during that work because the complete raw bit string has already been observed. It still needs reliable classical storage and processing for the entire latency.

## 7. Exact controlled-stage and finite-time boundaries
The bound as written is directly established for L completed memory blocks followed by the declared controlled suffix. For an arbitrary observation time inside a memory block, one may include the final partial memory interval in the same D0-only suffix. Its marked/direct fault mass must then be added to Q_ro and bounded using the accepted late-cell moment plus a Holder step. This preserves a constant-size root-tail parameter, but the pure-Poisson equation (3) alone does not bound that combined mass. Alternatively choose the observation time at an analysis-block boundary.

Unfinished clean or malformed transactions are handled only because the actual full-Hilbert F^dagger is included, not because their work was presumed complete. The circuit must act on the actual controls/workspaces and respect the full-Hilbert frame definition. No drain deadline is needed under this exact circuit premise.

All switching duration, readout gate durations, pointer/write stages and their modeled faults must lie inside the fixed tau_ro budget. A claimed bounded-depth schedule that leaves an incompatible native generator running is a different model and is not certified. The accepted memory proof supplies neither this external mode switch nor the classical fault-tolerant processor.

## Remaining external obligations
- Specify and implement the controlled nominal U_copy F^dagger stage, with compatible suppression/control of native terms.
- Supply the declared fixed-range Poisson-CPTP model for its gates, pointer initialization and pre-observation write circuitry.
- Supply a complete-record classical reliability bound p_cl with charged resources.
- Preserve the distinction from arbitrary quantum retrieval, general measurement bases, continuous coherent perturbations, passive thermal autonomy and fixed-dimensional high-rate geometric routing.

No accepted manuscript was edited. No denied access or external mutation occurred.
