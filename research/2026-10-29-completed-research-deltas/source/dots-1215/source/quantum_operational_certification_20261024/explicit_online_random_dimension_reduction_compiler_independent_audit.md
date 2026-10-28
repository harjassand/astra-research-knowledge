# Independent receipt: explicit polynomial online dimension reduction

2026-10-27. Auditor: `producer-workspace/audit_causal_dimension_reduction`.

**PASS, with the resource and interface scope below.** The canonical source is `explicit_online_random_dimension_reduction_compiler_20261027.md`, not the duplicate root draft. The previously received causal-existence audit and receipt are unchanged.

This audit accepts a known polynomial-size, finite-horizon sequential receiver compiler, with polynomially many memoryproducer-workspace/workspace **qubits**, for exact-reference common-unknown-support random dimension reduction and arbitrarily accurate complete/interactive approximation. The phase-safe Bell/CG/erasure/attenuation/amplification construction closes the earlier *existence-only* compiler gap. It does not close the separate rank-squared ordinary encoder-discovery or efficient classical optimization gap.

## 1. The phase and orientation issues are material, and are now repaired

Use `G_(λ,μ):Q_λ⊗C^k→Q_μ` for the forward CG **coisometry**, and `C=G†` for its embedding. Then the required map is

```
F_(λ,μ)[i,b;a] = sqrt(d_λ/d_μ) conjugate(G[b;a,i])
               = sqrt(d_λ/d_μ) C[a,i,b].
```

There is no conjugation on the embedding's coefficient in the second expression. An earlier root draft used the wrong embedding orientation; the canonical manuscript has corrected it. The actual Bell-plus-conjugate-forward-CG circuit implements this corrected formula.

A direct inverse dual-CG circuit is **not** received here merely because it has the correct representation types. Its reciprocity convention may add predecessor-dependent phases. Such phases alter the multiplicity register and can change the required arbitrary-operator law, even while preserving norms and prefix causality. The canonical compiler avoids this ambiguity by bending the same chosen ordinary CG coefficients literally.

Independent negative controls confirm that this is not cosmetic. For `k=s=2,n=3`, a relative sign on the `(1,1)` predecessor into `(2,1)` changes the Haar output of `|010><010|` by trace distance `1/sqrt(3)`, while leaving its two-output prefix unchanged. An incorrect conjugation in a complex edge gauge produces the same discrepancy. Correctly paired complex edge gauges cancel exactly.

## 2. Cross-dimension multiplicity conventions are supplied, not guessed

A generic block diagonalization would not suffice. The relevant Schur family fixes the same Young–Yamanouchi matrices on the symmetric-group register for every physical dimension. [Burchardt et al., Section 2.2, equation (4), Theorem 1 and Section 6](https://arxiv.org/html/2509.22640) specify this basis and establish that the circuit reaches it. Therefore

```
Schur_s W^⊗n Schur_k† = ⊕_λ (W_λ ⊗ I_(P_λ))
```

follows by symmetric-group intertwining and Schur's lemma, not by assigning an arbitrary identification to multiplicity paths.

The canonical manuscript further selects the same sparse ordinary-CG family at `d=s` and `d=k`. In [Grinko–Yoshida, Appendix D, equations (115)–(138)](https://arxiv.org/html/2509.26623v2), the physical alphabet map is updated reversibly and the CG core acts on the compressed pattern. Restricting to alphabet `[k]` gives the same coefficients and path convention; register padding does not introduce edge phases. Appendix D describes an actual arriving-symbol update and cleaned workspace. Its stated complexity is polynomial in the step count and logarithmic in ambient dimension and inverse precision.

This receipt uses that **direct sequential primitive**. The optional full-Schur sandwich is not needed; any use of it must retain the manuscript's compatible-branching condition. The unrelated mixed/dual-CG phase convention is not imported as a substitute.

## 3. The co-CG normalization and coherent predecessor erasure check

For each valid `μ`, the partial trace of the CG range projector is a scalar on `Q_λ`; its trace fixes that scalar to `d_μ/d_λ`. Hence every `F_(λ,μ)` is an isometry. Distinct predecessors have orthogonal ranges, since they carry inequivalent conjugate irreducible representations in `C^k⊗bar Q_μ`. Thus the direct-sum map `F_μ` is an isometry **with the predecessor label consumed**.

Here is the audited successful block of the actual preparatory circuit:

1. A Bell pair contributes `1/sqrt(k)`.
2. Conjugate forward CG, conditioned on the old shape, contributes the literal conjugated `G` coefficient.
3. Matching its successor to target `μ` produces `sqrt(d_μ/(k d_λ)) F_(λ,μ)`.
4. Coherent projection of the old removable-row label onto a uniform register of size `m=2^ceil(log2 k)` contributes `1/sqrt(m)`.

Therefore its unattenuated singular amplitude is

```
α_(λ,μ)=sqrt(d_μ/(k m d_λ)).
```

The factor `m` is necessary. Retaining or tracing a which-predecessor record is not the desired map. Any reconstructed shape copy and dimension arithmetic must be uncomputed **before** the row-label projection. On the successful block the successor copy is erased using target `μ`. The target physical irrep is a spectator, not measured.

The Weyl product argument in the manuscript correctly gives `d_μ/d_λ≥1/k`, so `α≥1/sqrt(2k³)`. Computing these positive rational ratios requires polynomial bit length and arithmetic in the stated parameters. With

```
J=8k ceil(sqrt(k)),  θ=π/(4J+2),  c=sin θ,
```

the controlled attenuation `c/α` is bounded away from one. It yields the **same** successful block `cF` for every coherent shape and predecessor, with no relative phase change.

## 4. Amplification is a full isometry, not postselection

The input projector must include valid predecessor/GT encodings and initialized work registers. Reflecting only about fresh ancillas would not justify an unspecified completion on invalid padded inputs. The canonical source now explicitly supplies the valid-domain projector. The output projector tests all success conditions: attenuation, successor match, predecessor erasure, and cleaned workspace. All tests are on known representation labels or flags and are efficiently reversible.

Let `A` denote the preparatory unitary, `P` the valid initialized input projector, and `R` the successful-output projector. The audited identity is `RAP=cF`, with `F†F=I` on `P`. The failure component defines an isometry `B` orthogonal to `F`, so

```
Av = sin θ Fv + cos θ Bv
```

for every `v` in `P`, including arbitrary coherent superpositions and reference entanglement. With

```
Q = -A(I-2P)A†(I-2R),
```

the same two-dimensional rotation acts on every input direction. After `J` iterations the angle is exactly `π/2`, giving `Q^J AP=F`. All failure flags have zero amplitude in this ideal circuit. No input is measured, retried, discarded conditionally, or divided by an observed success probability.

This is a direct proof of the isometry-amplification step. It agrees with the isometry/projector form of amplitude amplification in [Gilyén et al., Theorem 28](https://arxiv.org/pdf/1806.01838), but the present exact angle choice does not require an additional unproved phase-synthesis routine.

## 5. Sequential correctness, forbidden inputs and finite precision

The physical forward CG update and `F_μ` yield the usual Schur-replacement dilation because the factors telescope to `1/sqrt(d_μ)`. Its emitted multiplicity path is unchanged, and its target irrep is maximally mixed after tracing the retained conjugate. This proves the supported identity on **all operators**, not only iid states. Cross-shape terms vanish only when the memory is traced; path coherences within a shape are preserved.

A forbidden crossing is routed coherently to a distinct memory sector. Storing the post-CG registers and emitting half of a fresh Bell pair is an explicit isometry; subsequent fallen steps store incoming registers and emit independent maximally mixed outputs. No original state must be cloned. Valid common-support inputs have zero ideal forbidden amplitude. Thus the full receiver is causal and CPTP on arbitrary physical inputs. It need not equal the earlier recursion on unpromised inputs.

Polynomial implementation must use the supplied padded gate circuits and simple reversible validity/failure routing, **not** synthesize an arbitrary dense completion on unused encodings. All these operations are receiver-known. The large physical alphabet is charged in register bits and reversible arithmetic, not treated as a free support oracle.

Finite approximation is applied to the complete deterministic gate sequence, including every amplification call and inverse. A uniform isometry operator error `e` bounds the resulting channel diamond error by `2e`. Summing per-step complete errors through an arbitrary external causal tester gives the claimed interactive error budget. Merely bounding acceptance probabilities or a parallel density-state discrepancy would not suffice. Leakage from approximate valid encodings is handled by the same globally defined CPTP gates; it is not postselected away.

The stated complexity is polynomial in `H,k,log s,log(1/ν)`. This is an asymptotic, representation-theoretic compiler theorem, not a gate-level execution, practical fault-tolerance estimate, constant-memory claim, or a polynomial bound on the **Hilbert-space dimension** of memory.

## 6. Independent numerical receiving

`explicit_online_rdr_compiler_independent_check.py/.json/.log` contains three independent checks:

- **Actual preparatory circuit:** a 64-dimensional unitary at `k=2, μ=(2,1)` includes both predecessors, padded irreps, Bell preparation, conjugate ordinary CG, uniform predecessor erasure, attenuation, valid-domain/success reflections, and the canonical `J=32` amplification. Successful-block error is below `7e-18`; full amplified-isometry operator error is `1.61e-14`; total failure-flag leakage operator norm is `1.04e-15`.
- **Sequential same-dimension circuit:** explicit `U(2)` CG/co-CG steps through `n=4` match Haar twirling on every matrix unit to below `1.7e-16`. Consistent complex edge gauges leave the isometry unchanged. Both wrong-phase and wrong-conjugation controls fail by trace distance `1/sqrt(3)`. Tracing instead of coherently erasing the predecessor fails by trace distance `1/2` on a coherent input.
- **Rectangular end-to-end circuit:** at `s=3,k=2,n≤4`, physical CG tensors are independently extracted from common Specht matrix units, with random complex physical-irrep basis gauges and a random complex embedding `W`. All multiplicity paths give the same physical CG tensors to `3.5e-16`. The full supported operator law holds to `4.2e-16`; the promised-subspace no-failure identity holds to `1.7e-15`.

The rectangular test executes finite representation algebra, **not** the imported high-dimensional gate implementation. Its choice of common Specht modules is explicit, so it tests tensor contractions and embedding transfer without silently identifying unrelated path bases. These floating-point tests support the general proof; they are not its replacement.

## 7. Operational payoff and stopping boundary

The received compiler supplies one retained quantum frame across calibration measurements and later source outputs. Equality of the entire supported operator maps is equality of the restricted combs, so arbitrary causal preparations/measurements may be linked between emitted ports. Later payloads can use this ongoing frame; simultaneous bank-plus-payload reduction or a new bank per payload is no longer imposed by the alignment primitive itself.

This receipt does not independently re-prove the Bures learner's rates, record-conditioned confidence, encoder-selection statistics, or classical decoder-net optimization. A fresh-bank theorem cannot simply be renamed a streaming conditional-confidence theorem. Memory must persist, the finite horizon must include its uses, all physical inputs must obey the same support promise, and retained-frame errors must be budgeted through the full interaction.

No external uploads, merges, or permission escalation occurred. No denied operation was retried. The original existence receipt is preserved.
