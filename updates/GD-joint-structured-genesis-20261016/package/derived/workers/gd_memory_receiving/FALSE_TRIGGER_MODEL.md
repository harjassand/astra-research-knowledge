# A concrete signed error in an actual two-check correction element

16 October 2026. New local derivation using the acquired ideal correction geometry. This is an explicit mathematical error model, not an acquired calibration or hardware noise bound.

## 1. Ideal and imperfect jumps

Fix one CSS sector and one direction pair at a vertex. Let `S_1,S_2` be its commuting, independent outgoing edge stabilizers, and let the written face Pauli `Q` anticommute with both. Put

`Pi=(I-S_1)(I-S_2)/4`, `A=Q Pi`, `B=I-Pi`.

The ideal completed correction has generator `kappa(D[A]+D[B])=kappa(C-Id)`. Its active-only original has generator `kappa D[A]`. They agree on definite-syndrome Pauli density operators and differ on syndrome coherences.

Consider a bounded real false-trigger amplitude in the active jump,

`A_epsilon=Q(Pi+epsilon I)`, `|epsilon|<=a`,

while the inactive completion `B` is retained exactly. When the predicate is inactive, the active jump now has an unconditional face-flip amplitude `epsilon`; this changes the actual dissipator and is not a mere Hamiltonian or a Pauli rate perturbation. No smallness of `a` is assumed in the following algebra; memory admission will require the resulting rate budget to be small.

The signed error is

`E_epsilon=kappa(D[A_epsilon]-D[A])`.

It need not be Lindblad by itself. It is the difference of two legitimate local Lindblad dissipators.

## 2. Exact sparse coefficient matrix

Use four Hermitian, traceless Pauli representatives

`P_0=Q`, `P_1=iQS_1`, `P_2=iQS_2`, `P_3=QS_1S_2`.

These are distinct and orthonormal under normalized Hilbert-Schmidt inner product. Phases are fixed as displayed; in particular `P_1,P_2` are Hermitian because `Q` anticommutes with the corresponding stabilizer. Then

`A=(P_0+iP_1+iP_2+P_3)/4`,

so `c=(1,i,i,1)^T/4` and the imperfect coefficient vector is `c+epsilon e_0`. Consequently

`C(epsilon)=kappa[epsilon(e_0 c^dagger+c e_0^dagger)+epsilon^2 e_0 e_0^dagger]`.

In full, the only nonzero entries are

`C_00=kappa(epsilon/2+epsilon^2)`,

`C_01=C_02=-i kappa epsilon/4`, `C_03=kappa epsilon/4`,

and the conjugate entries `C_10,C_20,C_30`. The Hamiltonian coefficient is zero. This is an actual signed GKSL coefficient expansion of an acquired correction element; it does not assume `C>=0`.

For `epsilon!=0`, the `0,1` principal coefficient minor has determinant `-kappa^2 epsilon^2/16<0`. Since this is a traceless orthonormal Pauli representation, the signed error alone is not a Lindblad generator. Thus silently using the compiler's positive-coefficient improvement on this concrete replacement error would be false, although the actual imperfect dissipator is of course legitimate.

For every `|epsilon|<=a`, preselect the bounds

`M_00=kappa(a/2+a^2)`, `M_0j=M_j0=kappa a/4` for `j=1,2,3`.

Thus the ordered coefficient sum satisfies

`sum_ab M_ab=kappa(2a+a^2)`.                                                (F1)

The identity `D[A_epsilon]-D[A]` is exact on all local inputs and references. There is no truncation in `epsilon`; the quadratic term is retained.

## 3. One fixed seven-Pauli floor

Apply the supplied compiler's diagonal and correlated-edge constructions to the star of coefficient positions above. The Hermitian products of `P_0` with `P_1,P_2,P_3` are, up to irrelevant signs/phases, `S_1,S_2,S_1S_2`. The fixed physically installed floor is

`F_a = kappa(5a/4+a^2) D[Q]`

`    + (kappa a/4) ( D[P_1]+D[P_2]+D[P_3]`

`                         +D[S_1]+D[S_2]+D[S_1S_2] )`.                      (F2)

It is independent of the unknown `epsilon`. Each term is a genuine positive Lindblad dissipator. Its total displayed floor coefficient is

`kappa(11a/4+a^2)`.

The diagonal coefficient uses one fixed proposal clock at `2kappa(a/2+a^2)`. Each of the three correlated edges uses one fixed proposal clock at `4(kappa a/4)=kappa a`, with the supplied four-Kraus channel. Hence

`F_a+E_epsilon = sum_{j=0}^3 lambda_j(Phi_j(epsilon)-Id)`,

`sum_j lambda_j=kappa(4a+2a^2)`.                                          (F3)

The channels depend on the unknown but fixed scalar `epsilon`; their clock rates and patches do not. Zero-`a` terms are omitted. Singular boundary coefficients are admitted because the supplied edge Kraus construction remains valid at `|z|=M`.

This is a constructive sufficient rate, not a claim of globally optimal floors for this error family. It equals the general known-direction budget `4||A|| a+2a^2` when `||A||=1`, furnishing a concrete algebra check of that scaling without relying on the parent compiler proof.

## 4. The implemented generator is stated without changing models

For this element, the physical generator is

`kappa D[A_epsilon] + kappa D[B] + F_a`.

The same generator can be written exactly as the ideal completed correction `kappa(C-Id)` plus the fixed-rate CPTP fault proposals in (F3). The positive floor is present in the physical generator; it is not an analytical term added and subtracted at no cost.

Over all `12L^4` active pair correction elements, with independent fixed scalar amplitudes `|epsilon_e|<=a`, retain every inactive completion and install the respective floors. At each fine owner there are 12 such elements across both sectors. Therefore the total fault intensity per owner is at most

`nu_* = 12 kappa(4a+2a^2) = kappa(48a+24a^2)`.                              (F4)

Additional environmental noise clocks must be added to this budget. Keeping their rates absent in (F4) does not grant noise tolerance for them.

## 5. Body count and exact spatial box

An outgoing primal edge stabilizer contains six plaquettes. The two checked perpendicular edges share exactly the written positive plaquette, so their union contains 11 physical qubits. The seven floor labels have weights

`Q:1`, `P_1:6`, `P_2:6`, `P_3:11`, `S_1:6`, `S_2:6`, `S_1S_2:10`.

Every correlated proposal acts within that same 11-qubit union; there is no support enlargement beyond it for this family. To check geometry, represent a physical plaquette by its lower integer corner `u` and direction pair `{i,j}`. Its primal vertices are `u+epsilon_i e_i+epsilon_j e_j`; its dual vertices, indexed by hypercube lower corners, are `u-epsilon_k e_k-epsilon_l e_l`, where `{k,l}` is the complementary pair. The two primal edge-star union, and the corresponding dual edge-star union, both have all possible sector-boundary vertices in `v+{-1,0,1}^4`. Thus the boundary-reset radius in (G1) is exactly bounded by `q=1` for either CSS element in these owner conventions. The finite script checks all 12 pair/sector patches, rather than one picture.

For `b>=1`, insert (F4) and `q=1` in (G5). If the residual admissible owner-rate ratio from (G6) is

`tau = delta_* / {3 Cb [ (2R+5)b+2 ]^4}`,

then an explicit sufficient scalar-amplitude condition is

`48a+24a^2<=tau`, equivalently `a<=sqrt(1+tau/24)-1`.                         (F5)

This is a symbolic admission condition inside the conditional qualitative theorem. It gives no useful numerical hardware tolerance because `delta_*,C,R,b` have not been made operationally useful or measured.

## 6. Resources and retained limitations

Before merging duplicate Pauli labels, the physical Lindblad presentation has 12 perturbed active jumps and 12 retained inactive jumps per fine cell, plus at most 84 Pauli floor jumps: at most `108L^4` dissipators. The original completed ideal pair presentation had `24L^4`. The proof's alternative clock presentation has `12L^4` ideal correction streams plus at most `48L^4` fault streams, with at most `192L^4` Kraus dissipators when all four edge Kraus operators and both diagonal Kraus operators are retained. These are different presentations of the same new generator, not interchangeable hardware counts.

The floor strength, the 11-body operations, the static scalar bound `a`, ideal completion, 4D connectivity, memoryless Markov description, ideal initialization, fixed perfect decoder and all qualitative probability imports remain assumptions. No reset, reservoir, energy, noisy readout or acquisition mechanism is supplied. The result is not robustness of `kappa D[A]` alone, of the uncompleted active-pair generator, or of the 24-qubit whole-vertex generator.
