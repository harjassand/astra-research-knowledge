# Independent proof: closing the same zero-good-support certificate over detector data

2026-10-15. Exact finite stabilizer-code algebra; no experimental data or unverified patch computation used.

## Statement
Let S be an abelian Pauli stabilizer group without −I on a finite qubit system. Let D be m qubits. Let G⊆S be a commuting measured subgroup **supported wholly on D**. Suppose the same zero-good-support certificate is required for arbitrary Pauli faults on all of D:

  Pauli(D) ∩ Centralizer(G) ⊆ phase × S.                    (1)

Then rank(G)=rank(S∩Pauli(D))=m, and the code factors as

  C(S)=|psi_D> ⊗ C_remaining,

where |psi_D> is one fixed pure stabilizer state on D. In particular D cannot be a nontrivially coupled, information-bearing patch of this stabilizer code under these assumptions. The rest of the code may still encode information; this is not a claim that the whole code is trivial.

## Dimension proof
Quotient Paulis by phases. The supported Pauli space V_D is a nondegenerate symplectic vector space over F_2 of dimension 2m. Let W=S∩V_D, with rank r. Because S is isotropic, W is isotropic and r≤m. Let g=rank(G), so g≤r.

The centralizer of G inside V_D is its symplectic orthogonal G^{perp_D}, with dimension 2m−g. Condition (1) says G^{perp_D}⊆W. Therefore

  2m−g ≤ r ≤ m,  and  g≤r≤m.

The only possibility is g=r=m. Hence G=W is Lagrangian in V_D and G^{perp_D}=W. Rank counts independent generators, not the number of measured check labels.

## Why rank m implies actual code factorization
For any global stabilizer s∈S, its restriction s_D commutes with all of W, because the elements of W are supported entirely on D. Thus s_D∈W^{perp_D}=W. There is consequently a D-supported stabilizer with that same Pauli restriction. Multiplying it into s cancels the D component and leaves a stabilizer supported on the complement D^c. It follows, modulo consistent signs, that

  S = W ⊕ (S∩V_(D^c)).

The m independent commuting stabilizers in W select a one-dimensional state on the m qubits of D. Their signs select |psi_D>; no −I ensures consistency. The remaining stabilizer constraints act only on D^c, proving the tensor-product codespace statement. It holds for every encoded state and external reference: there is no logical degree of freedom or encoded entanglement residing across this fixed factor.

## Consequence for physical detector closure
Suppose a theorem initially certifies a smaller noisy footprint A using checks G that extend outside A. Replacing A by the full detector **data** support D, keeping those checks within D, and demanding the unchanged certificate (1) against every Pauli on D is generally impossible for a nontrivial coupled patch. Repeatedly expanding the footprint is not a free repair: it forces the above fixed-state factor at closure.

This is a genuine obstruction to that particular sufficient certificate, not a no-go theorem for physical syndrome measurement or quantum error correction.

## Exact scope and escape routes not excluded
- If the perturbation family is restricted rather than all of Pauli(D), (1) need not be required. Restriction needs its own justification and stability under products; it cannot merely ignore possible detector-induced errors.
- If checks extend outside D, the support hypothesis for this argument fails. A smaller correctable error region A may be detected by larger check support without contradiction.
- Noisy/flagged measurement gadgets can charge detector faults as bad events, allow controlled nonzero good-branch support, use verified ancillas, or invoke a broader space-time decoder/support certificate. This result does not rule out any of those approaches.
- If part of D is a deliberately initialized ancilla stabilizer factor, that portion is already fixed and presents no contradiction. The theorem says all of D must be such a fixed factor under (1), including any data qubits put into D.
- Subsystem/gauge codes, noncommuting gauge measurements, or a certificate modulo a gauge group require a different algebra. This proof is for the stated commuting stabilizer/S_code condition.
- The result is independent of pulse/measurement duration. Charging finite time is still necessary, but cannot fix a logically impossible support certificate.

No H2 patch numbers or preliminary union-size computations are used in this proof. Those computations can illustrate the obstruction but are not needed to establish it.
