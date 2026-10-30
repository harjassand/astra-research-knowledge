# Correctness with bad ports left open

2026-10-30. Exact multilinear lemma, primary receiver check, and remaining physical premise.

## 1. This replaces causal straightening for the correctness step

The separate Bell-link note gives a possible dimension-cost norm conversion. It is unnecessary if the actual good circuit satisfies the stronger open identity below and rarity is controlled by the original global inclusive expansion. In particular, a retained bad comb need not be assigned an artificial circuit-time order.

## 2. Exact open identity

Fix an encoded input map V_enc, an intended logical isometry U, a good-circuit tensor network T, and a decoder isometry D that retains syndrome and all measurement/reset dilation outputs. Let S be a specified finite set of missing local operation/wire tensors. Every local input/output leg of these holes, including quantum ancillas and relevant classical records, is included. Choose a product matrix-unit basis {B_a} for the amplitude tensors at S.

Suppose for every basis assignment a the actual circuit's correctness proof supplies

    D T(B_a) V_enc = U tensor W_a.                 (2.1)

This is an equality on the logical input and the allowed ancillary/syndrome input space, not merely equality of one measurement distribution. Then the uncontracted tensor itself obeys

    D T_open V_enc = U tensor W_open.             (2.2)

Proof: both sides are multilinear in the open entries, and equality on a product basis is equality of tensors. No norm estimate is involved.

For a doubled tensor network, an arbitrary retained process C has operator-valued coefficients C_ab on the hole indices. Substituting (2.1) on ket and bra gives

    (D tensor id) [T_open * C](V_enc rho V_enc^dagger)
        = U rho U^dagger tensor Gamma_C.          (2.3)

All arbitrary correlations, feedback order and retained-bath dependence occur in Gamma_C, not in the logical factor. More generally, Gamma_C is a linear map on an arbitrary allowed ancillary input, and (2.3) is reference-stable. C need not be a product of fault maps, CP, positive, causal in circuit order, or small in a matrix-unit coefficient norm. Its contraction must, of course, actually be the physical network under analysis.

This is a common-correctable-span identity. It does not claim that an arbitrary bad comb is an ordinary gate fault.

## 3. How to get the open identity from an actual fault-tolerant gadget

It is NOT enough to know that one CPTP noisy implementation has the right reduced output. The required premise is correctness for every allowed Pauli/operator word at the marked locations, with a common decoder, common logical U, and retained syndrome/dilation outputs.

For a Pauli word P at allowed locations, the completed circuit is physical. If its decoded logical channel is exactly the unitary U for every logical input, then any Stinespring dilation on the allowed input span factors as U tensor W_P. One elementary proof applies the dilation to a logical basis: purity gives U|i> tensor |w_i>; applying it to superpositions forces all |w_i> equal. With arbitrary ancillary/syndrome input, the same argument gives an ancillary map W_P. This prevents hidden logical information in a retained measurement record.

Pauli operators span local operator space. Matrix units and general hole tensors are linear combinations of these operators (include the fixed local ideal gate or its finite Stinespring isometry when converting an input/output hole to an operator insertion). Thus Pauli-word factorization extends to (2.1) by multilinearity. If an erased tensor has larger arity than the original gate, every additional port must be counted; it cannot be hidden in the word 'fault'.

## 4. Primary-source check

Aliferis–Gottesman–Preskill, arXiv:quant-ph/0504218v3, Section 5.2.2, Eq. (14), uses the retained-syndrome factorization of a good rectangle. Section 11.4 explicitly extends correctness to nonphysical fault sums via Pauli expansion and linearity. Section 9, Lemma 5, supplies the higher-distance exRec criterion. These are the right algebraic ingredients. The source's final classical-decoding qualification remains in force; it does not grant reliable physical feedforward or record capture in our apparatus.

Primary URL: https://arxiv.org/abs/quant-ph/0504218v3

For a concrete check, check_open_tensor_correctability.py constructs the [[5,1,3]] perfect-code decoder and verifies the open matrix-unit identity for every one-qubit insertion. It also contracts an arbitrary signed, non-Hermitian 16 by 16 coefficient tensor across correctable Pauli errors and verifies exact logical tensor factorization. This demonstrates the algebra with arbitrary coherent cross terms, but the ideal recovery cut in that test is not a native fault-tolerant recovery circuit.

## 5. Application to static destructive-transfer modules

If the physical execution outside a damaged module set really reduces to the designated ideal DAG with only its bounded boundary ports open, Section 2 applies to each gadget whose enlarged marked-port set lies within its actual fault-tolerance budget. Fresh-output overwrite and consumed-input reset are what remove pre-production and post-consumption contacts from the quantum boundary. A poisoned/false DONE does not need to be interpreted as a causal gate map; its entire boundary tensor is simply contracted into the open holes.

Native partial transactions touched by a damaged actuator must also be marked. It is not legitimate to call such a neighboring transaction an exact good gate just because its eventual label was SUCCESS. Full-footprint ownership, forest semantics, and the cavity buffers must establish that every retained gate is the exact intended tensor. Similarly, online classical records and commands that affect retained operations must be inside the counted boundary or proved correct. A sparse set of classical source faults does not establish this physical open-DAG premise by itself.

## 6. Combination with global inclusive norms

Keep the complete original expansion E = sum_R E_R. Suppose every coefficient term called globally good satisfies the SAME logical factorization after the fixed decoder, established by the open identities, and let B be the total globally bad part with ||B||_diamond <= delta. No norm bound on individual boundary tensor coefficients is needed for this correctness step.

For a fixed logical-independent initialized ancillary state, the decoded good part has the form c U_channel, with a scalar c independent of the logical input. It need not be CP. Since the actual decoded channel is trace-preserving,

    |1-c| <= ||D B||_diamond <= delta.

Consequently

    ||D E - U_channel||_diamond <= 2 delta.        (6.1)

If ancillary outputs are retained, use the corresponding U_channel tensor Gamma factorization before taking the desired output marginal. The good part's auxiliary map need not separately be a physical channel. Equation (6.1) concerns the actual physical CPTP total map.

Rarity can therefore be handled in the closed global Boolean expansion, while correctness is handled as an open tensor identity. This avoids assuming a small OPEN-comb norm. It does not provide the remaining Gács-to-physical-actuation semantic contract or active-wire exposure theorem.
