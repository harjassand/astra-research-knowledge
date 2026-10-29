# Correlated-input extension: accepted ideal memory instrument, not scalar acceptance
2026-10-29. New separate extension, pending independent review. It does not silently change v1's product-input scalar-pass theorem.

Retain the same exact private-pad boundaries, same-source role condition, weighted witness, finite guard, and total Clifford/Pauli outer decoder. Initial user payload, apparatus memory and external reference may now be arbitrarily correlated.

## Factorized complete branches
The retired-key service identity is an operator identity on arbitrary joint inputs, not only products. Test probes are freshly prepared independently of payload and memory. Refine the protocol mathematically by each Pauli service label and each Kraus/test/controller branch, WITHOUT conditioning on retired pad keys. Every branch before outer decoding is therefore a tensor product of a Pauli pattern on the outer data and a memory Kraus operator A_h. The actual outer Clifford decoder, measured initialized ancillas and deterministic Pauli correction/fallback turn ANY physical Pauli pattern into a logical Pauli L_h and a syndrome determined by the pattern. Thus an accepted branch has the form
L_h tensor A_h,
possibly with a classical history flag included in the memory output. If the service fault count is≤t, L_h=I exactly. No payload-dependent decoder record is retained outside this stated Clifford/Pauli construction; more general decoders would need their own analysis.

Let B_h(σ)=A_h σ A_h†, summing nuisance Kraus labels if desired. Define
B_acc=Σ_{h accepted} B_h,
B_bad=Σ_{h accepted,F>t} B_h.
For an arbitrary memory marginal σ, tracing a logical unitary from the data leaves the same updated memory marginal. The finite hazard/NB argument therefore gives
Tr[B_bad(σ)]≤epsilon_NB for EVERY density operator σ.
Equivalently its memory effect satisfies
E_bad=B_bad†(I)≤epsilon_NB I_M.
This operator bound can also be obtained by applying v1 to every product payload/memory input; since branch weights are algebraically the same, it is a state-independent consequence.

## Correct accepted ideal and diamond bound
The real accepted joint map is
A_acc=Σ_{h accepted} Ad_Lh tensor B_h.
Define the ideal accepted joint map as
I_acc=id_payload tensor B_acc,
with the SAME accepted memory/transcript instrument. Good branches agree. For the bad branches, first apply the CP flagged memory instrument
B_bad,flag(σ)=Σ_bad |h><h| tensor B_h(σ).
Its diamond norm is ||E_bad||∞≤epsilon_NB. The real bad map then applies L_h to user data conditional on h, while the ideal bad map applies identity; both postprocessings are CPTP. Their half-diamond distance is at most1. Composition yields
(1/2)||A_acc−I_acc||diamond≤epsilon_NB.
This holds on arbitrary payload–memory–reference inputs. It also holds when any allowed output history/source memory is included. The flag can be traced out if not retained. Summing separate branch operator norms would be unnecessarily weak; the bound uses the aggregate effect E_bad.

## What is NOT implied
B_acc is generally trace-decreasing and not a scalar multiple of a TP map. It can filter the initially correlated memory and thereby steer the user/reference conditional state. Such steering is present in the ideal id_payload tensor B_acc as well. Therefore this extension does NOT assert a constant input-independent acceptance scalar for arbitrary correlated joint inputs, nor that the accepted user marginal equals the original marginal after normalization. In v1's product-input case, B_acc(σ_M) has scalar trace p_acc independent of payload, recovering that theorem.

No security is asserted conditioned on a retained/disclosed pad key. No arbitrary payload-dependent outer decoder/fallback is substituted for the explicit Clifford/Pauli code. Endpoint isolation, current setting privacy, complete control budgets and lack of guaranteed yield remain unchanged. This is a simulator-style accepted-instrument statement, not a novel general quantum-authentication definition or superiority over existing composable authentication schemes.
