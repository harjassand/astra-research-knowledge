# Pro1 Cycle7 continuation

## Current owned result

The full-prefix temporal-growth frontier is resolved exactly. For every k>=2,

    v_k=k(k-1)/8 -(1/8) sum_{n=0}^{k-2}(k-1-n) Pr(S_n=0),
    v_k=k^2/8-k^(3/2)/(6 sqrt(2pi))-k/8+O(sqrt(k)).

The analytic symmetric-prefix density zeta_sym=P_sym/(k+1) is an explicit
minimizer over ALL coherent/entangled prefix densities. Its input observable H
satisfies T_k(sigma H)=v_k I exactly, and A_k=(ln2)v_k/8. This restricted
variational identity is not a capacity formula.

For every fixed 0<beta<=2^-8, k=floor(beta^(-1/2)/8), the actual positive
input below gives one initializer-independent deterministic unassisted code
sequence at rate at least 3/2+(ln2/16384) beta^(7/2), with pointwise vanishing
FULL-diamond error for every fixed normal initializer. Actual tau_pi is included,
and its repeated-block coherent-information limit is S(rho)/k. Beta, k and rho
are fixed before the coding horizon. There is no terminal bath-return promise.

This makes the preceding conditional beta^(7/2) transfer unconditional. The
improvement is in attainable asymptotic power; at beta=1/512 the coarse displayed
bound is slightly below the preserved pair floor beta^4/1024. Keep the stronger
existing pointwise comparator and the actual non-scalar four-call result.

## Actual source and preserved operation

Read SHARP_TEMPORAL_GROWTH.tex or COMPLETE_PROOF.tex.txt, including both inherited
TeX files. The contributions contain distinct proofs and the independent review;
they do not replace the integrated proof. The exact predecessor is
Astra_Amplification_Cycle6_PRO1_20261022.zip, 4,277,633 bytes, SHA256
58390669b57089da88c3adff4d95016ae9372203ae6462826294c477780b5e39.
It is unchanged in preserved/ and contains the full earlier original chain.

E=C2_seed tensor F(C2), U=[[R,S1,S2],[S1*,0,0],[S2*,0,0]],
V=alpha U+i beta I. S_j prepend colors; R exchanges vacuum seeds.
All calls conserve depth plus port color charge. Actual tau_pi depth mass
(2/3)3^-h is uniform over 2^(h+1) vertices; eta=(3/4,1/8,1/8).
One evolving infinite bath, every call/outcome/register counted; no bath access,
reset, fresh bath, preshared entanglement, postselection, backward quantum wire
or timing channel. The convergence quantifier is pointwise, not uniform at each
finite horizon over all normal states.

## New all-length operation

For oriented endpoints01 at i<j, reduce the earlier prefix and middle charge
walks. Let h be the unmatched input pushes before i, and d the unmatched pops
in the middle. With E the earlier all-move prefix and D=M*U_j M, the two raw
products are E*U_i D E and E*D U_i E. D inserts an input color w at stack index d.
Commuting insertion with the top pop changes exactly the transposition of w and
the pre-existing color at d. Undoing E yields:

- h>d: input/input transposition, both baths restored, normalized square1.
- h=d: input/bath swap, one bath restored, square Tr(zeta_m^2)/2>=1/4.
- h<d: both export w; contractions coincide for each repeated-color pure prefix.

The same zeta_sym=integral |u><u|^tensor k has marginal I/2 and cancels the last
case, so it attains every local lower simultaneously. This is a BULK coefficient
classification; the earlier narrow guard/meander raw identity was whole-bath.
Do not promote the enlarged classification through arbitrary vacuum encounters.

The input H is explicit: P(I-SWAP), P/2 or0 on the three cases, plus adjoints.
Normalized input partial traces prove the exact scalar T_k(sigma H)=v_k I.
No prefix optimization search remains, but efficient matrix/code construction
is not established. The prefix state is analytic only and never prepared.

The unmatched-push and middle-deficit laws are independent fair-walk maxima M_i,
M_r. Triangle symmetry gives v=k(k-1)/8-(1/8)sum Pr(M_i=M_r), immediately
v>=k(k-1)/16>=k^2/32. The collision generating function is
1/[(1-z)sqrt(1-z^2)], giving the exact formula above. Do not turn that aggregate
convolution into a false endpoint-distance-only identity.

## Uniform nonlinear receiving use

Put b=beta^2, sigma=diag(1/2,1/4,1/4)^tensor k, l=ln2, v=v_k,

    X=-(l/2)sigma H, m=3lv/16,
    Y=(4m/k)sigma(Q-k/2), rho=sigma+bX+b^2Y.

For k>=2 and b k^4<=2^-12, rho is strictly positive, its exact bulk drift
is at most -l v b^2 I/16, and S(rho)-3k/2>=l v b^2/32.
The uniform remainder ||R_b||<=4k^5b^2 is contracted against rho-sigma
because sigma has EXACT zero bulk drift at every b. Preserve this cancellation.
The inherited operator Lyapunov theorem retains its finite root term. Types
and joint compression retain r^2, auxiliary CPTP normalization and polar repair.
No physical channel tensor-power assumption or postselection is used.

## Decisive omitted-premise witness

For charge word001, endpoints0,2, h=0<d=1. The two raw words send input z
and bath(B0,B1) to outputB0 and baths(z,B1) or(B1,z). Against I/4 the two
contractions are I/2 and I/4, difference I/4, square1/16. Against the symmetric
mixture they coincide. Both prefix states have the same one-color marginals.
Correct marginals alone cannot replace the required correlated analytic witness.

The prior failed word100111, endpoints1,5, remains non-bath-independent but is
now legitimately CaseII with uniform contribution>=1/4. A failed stronger
intermediate identity did not exclude this weaker useful operation.

## Chosen precise next operation

The sharp v_k question is complete. Continue with the nonlinear range for this
now explicit H, not more finite-prefix optimization or constant tuning.
Determine the full operator remainder

    Rcontract(k,b)=Tr_A[((bX+b^2Y) tensor I) R_b],

together with the known b^3 T(Y) term, and whether exact inward drift and entropy
survive for temporal lengths beyond b k^4=O(1). Start by deriving the fourth-order
charge-resolved word coefficient and its contraction against sigma H, retaining
final bath overlaps; compare that with the coarse derivative bound 4k^5b^2.
A favorable finite expectation is insufficient. Any improved uniform window must
pay positivity, entropy, the root term and full-diamond coding. No stronger window
or capacity exponent is presently proved. General capacity converse and feedback
equality remain broader questions, not assumed targets for other owners.

## Status and cost boundary

Actual source-hashed internal challenges cover the new load-bearing steps and
the final assembled proof. Historical originality, external expert acceptance,
efficient encoding, useful blocklength and physical usefulness remain unknown.
Recorded script/runtime memory is separate from unmeasured inference, discovery
and review totals. Delivery does not imply reading, acceptance or integration.
The broader Pro1 mission remains active. Protected programmes and retired
engineering/guide operations retain their ownership and scoped closures.
