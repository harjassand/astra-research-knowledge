# Direct weight-13 route: exact Gibbs conjugacy, not a cone approximation

2026-11-02. Governing concrete geometry input: the companion boxed/exterior star certificate in `concrete_stars/`. The complete source-binding audit now passes for the declared atlas; see FRESH_DIRECT_K13_AUDIT.md. Governing baseline: the same geometry proves the UNCHANGED source K≤15, so this K13 construction is an optional modest re-encoding, not a large gain over the strongest now-available method.

## 1. Physical star budget and a reusable rank bound

Let Q_v=Σ_(e∋v) dim F_e, counting distinct abstract edge germs even if their embeddings overlap. Every actual vertex X generator is supported on these Q_v physical qubits, irrespective of the chosen vertex basis or edge-stalk bases.

The source exterior rule permits, in each lattice unit-segment direction outside exceptional boxes, either one edge of face degree≤3 (stalk dimension≤2), or two edges each of degree≤2 (total stalk dimension≤2). There are six directions. Therefore Q_v≤12 for every exterior vertex. No injectivity of coincident edge germs or simple octahedral link is needed.

For a complete regular polygon star, every incident face bit occurs in exactly two distinct edge-germ restrictions. Take the uniform random section a∈F_v. The entropy chain rule gives

 2 dim F_v = 2 H(a) ≤ Σ_(e∋v) H(a|faces(e)) ≤ Σ_(e∋v) dim F_e = Q_v.

This is the elementary twice-covered Shearer inequality, not an independence assumption. To see the first inequality, order the face variables: conditioning each variable on all preceding variables can only decrease its conditional entropy relative to conditioning on the preceding variables in one restriction; sum the restrictions, which count every variable twice. Hence the exterior stalk rank is at most6.

The finite exceptional-star calculation gives Q_v≤13, with rank≤4, for doubled T boxes; Q_v≤12/rank≤4 for recursive T boxes; Q_v≤11/rank≤4 for glued-cross boxes; and Q_v≤7/rank≤2 for free-cross boxes. Thus **every X generator has weight≤13 without changing its vertex-generator basis**. The rank bound gives q_X≤12, since an edge qubit is acted on only by its two endpoint stalks, each of rank≤6.

## 2. One global physical edge-basis rule

For every red edge, order its incident abstract face IDs by a fixed deterministic global rule. For degree d use the path basis

 f_1+f_2, f_2+f_3, ..., f_(d−1)+f_d

of Par_d. Use the repetition all-ones basis for every blue edge; degree2 has its unique basis. This assigns ONE physical basis per edge, shared by both endpoints. No vertex chooses its own incompatible edge basis.

Each face occurs in at most two columns of a parity path basis, and in one column of a repetition basis. Every actual polygon has at most five boundary edges. Therefore **w_Z≤10**. Each edge has at most four incident faces, so q_Z≤4. Thus

 w_max≤13, total qubit degree q_X+q_Z≤16,
 native overlap D≤1+13(16−1)=196,
 clock length K_a=max(3,w_a)≤13.

All physical data qubits, faces, vertex-generator coordinates, check energies and geometric positions are retained. Only the representation of at most three qubits within each existing edge stalk changes. The K≤12 optional route would optimize some vertex generator bases and require a distinct thermal argument; it is deliberately NOT used here.

## 3. Exact whole-spectrum local-Clifford identity

Let E_old and E_new be the old and path bases of one edge stalk, and let A_e be the invertible binary matrix with E_new=E_old A_e. Set A=⊕_e A_e. With the vertex check coordinates unchanged, the old and new cochain matrices obey

 d0_new=A^(-1) d0_old,    d1_new=d1_old A.

There is a Clifford W_A supported separately on the ≤3 qubits of each edge such that

 W_A X_new(u) W_A†=X_old(Au),
 W_A Z_new(v) W_A†=Z_old(A^(-T)v).

Therefore W_A maps EACH new named stabilizer to its corresponding old named stabilizer, with its original coefficient. For the complete source Hamiltonians,

 H_new=W_A† H_old W_A,
 rho_new(beta)=W_A† rho_old(beta) W_A  for every beta,
 Pi_new(s)=W_A† Pi_old(s) W_A.

This is an exact full-spectrum identity. No generator products replace individual terms, no ancillary energy penalty or low-temperature approximation is introduced, and every thermal syndrome probability is identical. There is **zero cold-energy overhead** from this representation change.

The full-space decoded logical algebra is conjugated in the same way. Every new local Pauli error maps to a Pauli on at most three old qubits within the same edge stalk. Pauli products and their signs are transported exactly. Both error sectors and their canonical logical pairing follow from the same Clifford, not from two independently chosen non-symplectic maps.

## 4. Decoder, removable witnesses, filling and noise

The old syndrome labels and syndrome law are unchanged, so the entire original charged decoder/full-trace construction can be used in its old frame. The only physical input change is that a new one-qubit fault maps to a bounded old-edge Pauli word; this is already the type of bounded-local fault admitted by the source/native interface. Conjugate the final correction/logical readout back by W_A†. No new syndrome prepass or auxiliary trace leaves are needed. Consequently the code's contour entropy threshold is not multiplied by a vertex-basis rank or cone size.

New distances are at least old distances/3. A fine physical stabilizer of weight m maps to an old one of weight≤3m, and its old actual-generator filling conjugates back generator by generator. Radius and constant overhead are charged once at the final code, not multiplied at every recursive generation. Source maps may remain represented in the old frame; no false claim that every new-basis one-step projection still has column norm one is required.

Physical perturbations are still bounded-range operators on the new data/clock/bath sites. The edge Clifford has constant support and maps Pauli words to Pauli words, without a coefficient-norm expansion; a new data prefix of length≤13 maps to an old data word of support≤39. This keeps the old bounded-local full-trace and stabilizer-character consumer available with the actual enlarged input footprint.

The native two-body Hamiltonian is **recompiled** from the new weight≤13 checks. It is not asserted to be W_A† times the old native two-body Hamiltonian: conjugating a native data-clock term could make it act on several data qubits. Instead, the admitted all-K clock construction is applied anew in the new physical basis, where every hop still acts on one data qubit and one clock. Its exact thermal proof and perturbation dictionary then use K≤13 and D≤196, with the unchanged source syndrome traces and the charged three-qubit frame conversion.

## 5. Same-resource implementation ledger

No additional data qubits, spatial dimension, repeated syndrome measurements, active correction cycles, or source energy-scale increase are introduced. Clock dimensions, clock transition counts, and two-body peak coefficients change because the new certified maximum weight is13 rather than the previous conservative certificate180.

At the same effective coefficient J in −J S and the same eta, the resonant compiler's peak coefficient certificate changes as

 t_max=J K_max³/(2 eta²),
 t_max,new/t_max,old=(13/180)³≈0.0003767.

This is a comparison of sufficient designs, not proof that an optimized old device needed180. The violation energy is2J. Thermal wrap/tail conditions must be checked at the new K, rather than assumed monotone in K; the standard common bound for K≥3 with fixed cold beta J and sufficiently small eta supplies that check. Multi-rod overlap admission uses D≤196. The exact source Gibbs conjugacy itself holds at all beta, but the native memory conclusion retains its specified finite-temperature operating region.

For generic imperfection admission, K_max^(b_c) becomes13^(b_c), but any asserted improvement in v must retain the actual hook/dictionary/contact bounds and the new clock tail delta. The unchanged syndrome trace allows old conservative source constants to be reused only after verifying that the ≤39 old-frame prefix footprints and source contact degrees fit their previous envelopes. This is a finite dominance comparison, not a claim of automatically useful laboratory tolerances.

The equilibrium resource and ideal logical overwrite/terminal read assumptions are unchanged. There is no improved Gibbs preparation, noisy WRITE, autonomous loading, or physical access claim.
