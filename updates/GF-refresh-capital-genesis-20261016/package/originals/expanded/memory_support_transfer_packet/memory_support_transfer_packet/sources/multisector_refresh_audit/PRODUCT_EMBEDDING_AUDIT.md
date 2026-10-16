# Audit of auxiliary-label local-tester embedding

Date: 2026-10-16. Separate from the frozen singleton result. This is an explicit mathematical reduction, conditional on the binary unchanged-action tester simulation and causal positive-domination theorem cited in imperfect_refresh_product/PROOF.md.

## Conditions

There are commuting coarse good/bad parities A_i. Coordinate i has one fixed ordered node with projectors P_{i,0}=P_good_i and P_{i,1},...,P_{i,K_i} resolving its total bad sector. Every fine projector commutes with EVERY coarse parity. The node is exactly eta_i Id+(1-eta_i)sum_j Ad(P_{i,j}) on the full modeled state. Node environments are discarded and independent; controls cannot access them. Actual nodes have a prescribed chronological ordering. Simultaneous nodes may be handled by a specified sequential composition; an unspecified correlated simultaneous channel is not covered.

Between nodes, use the same broad-parity Hamiltonian contract and own-gap budgets as in the binary proof. A baseline need only preserve coarse parities. It need not preserve fine sectors.

## Exact encode / local pinch / decode channel identity

Fix coordinate i and omit its index. Let J have dimension K and orthonormal labels 0,...,K-1. Set ell(0)=0 and ell(j)=j-1 for 1<=j<=K. Let S_l be cyclic shift by l, and define

W=sum_{j=0}^K P_j tensor S_{ell(j)}.

W is unitary and preserves all coarse parities. With J initialized to |0>, define the tester-local projectors

R_0=P_good_A tensor I_J,
R_j=P_bad_A tensor |j-1><j-1|, 1<=j<=K.

Apply W, then the specified local channel eta Id+(1-eta)sum_j Ad(R_j), then W†. The identity branch is exactly identity with J restored to |0>. In a full-pinch branch, R_j W(|psi> tensor |0>)=P_j|psi> tensor |ell(j)>; decoding gives P_j|psi> tensor |0>. Consequently the total reduced channel is exactly the physical fine-pinch mixture, including on states entangled with any reference, and J is reset. Reusing label 0 for both good and first bad sector is safe because R_0 and R_1 distinguish the private coarse parity.

## Implementing W without exposing the private parity

When padding to equalize coarse-sector dimensions, extend each fine resolution to all added dimensions: good padding belongs to P_0, while added bad dimensions can be assigned to P_1 within each joint coarse sector. Simply zero-padding every bad projector would fail to resolve identity on the enlarged bad subspace. This extension preserves all coarse commutators and makes W unitary throughout the finite simulation. After equalizing coarse-sector dimensions, represent the physical state as coarse bits and a common prover bath B. Since every P_j commutes with all coarse parities,

P_j=sum_z |z><z| tensor Q_{j,z},

where for each z the Q_{j,z} form the appropriate orthogonal bath resolution (some are zero). Each local tester coherently copies its private bit into a fresh message C_i. The prover controls the bath/J version of W on the copied joint string. It returns copied messages unchanged; testers uncompute and discard them. J is returned specifically to tester i. The tester applies its local R-projector mixture and then sends J back in the next padded message round. The prover uses a fresh copy of the joint coarse string to implement W†. Copies are again returned unchanged and uncomputed. No actual Hamiltonian evolution is placed between these three simulation stages.

Thus both encode and decode are allowed joint-prover operations. Their possible action on fine bath labels costs no odd interaction action. Other testers can use identity operations in these extra rounds. Even noncommuting fine pinches for different coordinates can be embedded in their prescribed order, with separate message rounds.

## Why arbitrary prover strategies still have the singleton bound

The tester keeps its parity private. Its message copy/uncompute operations, initialization, discarding, and every induced prover intervention preserve that parity. The only odd operations remain its budgeted rotations. At its node the retained private A and received J have exactly one good block and K bad blocks. An arbitrary malicious choice of J, including entanglement with the prover or other systems, is already covered by SINGLETON_PROOF.md: purify the total state before the node, apply the rank-one block inequality there, and allow arbitrary parity-preserving operations after the node. Sending J away afterward is such an operation. The private noise environment is not sent away.

Therefore its individual optimum is at most F_K(a,b,eta). This is a bound against arbitrary interactive strategies, not merely the honest encoding strategy.

## Conditional product conclusion

The resulting local testers are genuinely independent: each has its own private parity, local rotations, received J interface, fixed local noise channel, and independent discarded noise environment. Common padded rounds permit the cited causal domination theorem to tensor their normalized dominating strategies. Hence all-pass probability is bounded by the product of their F_{K_i} values against an arbitrary joint prover, including shared bath and shared initial reference.

The physical model embeds into that game through the explicit label identity above and the inherited unchanged-action binary simulation. Therefore this gives the coordinate endpoint-bad product upper bound under the listed conditions. Tensoring the singleton witnesses shows uniform sharpness over unrestricted finite models with sufficient independent sector dimensions; sharpness is not asserted for every fixed family of overlapping fine projectors.

## Interaction-picture and scope cautions

If an interaction picture is used to remove a coarse-parity-preserving H0, each fine projector must be conjugated at its actual node. The conjugated projectors still commute with all coarse parities, have the same number of sectors, and are encoded by the same construction. Do not leave the original fine pinch unchanged unless the necessary commutation holds. Alternatively retain H0 in a partitionwise simulation and insert exact channel nodes.

This argument does not cover projectors that fail to commute with another coordinate's coarse parity, correlated joint node channels specified only by marginals, adaptive unqualified node schedules, noise-environment access, or literal generator-wise dephasing that is not the stipulated scalar fine-pinch mixture. Endpoint-bad products do not by themselves establish the older syndrome-history support/reservation theorem.

## Independent corroboration

The separate causal-tester reviewer independently checked the singleton proof and label embedding and supplied the full-resolution padding detail above. Exact rational label-interface checks supplied by the parent are in /workspace/scratch/57d8dd795b13/multisector_refresh_root/check_label_interface.py and interface_checks.json; they use two coarse bits with a shared bath qubit, Z-bath fine sectors for one coordinate and X-bath fine sectors for the other. Their fine projectors do not mutually commute, while all commute with both coarse bits. The checks establish unitarity and the encode/pinch/decode identities exactly.
