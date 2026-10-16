# Audit of auxiliary-label local-tester embedding

Date: 2026-10-16. Separate from the frozen singleton result. This is an explicit mathematical reduction, conditional on the binary unchanged-action tester simulation and causal positive-domination theorem cited in ../sources/binary_partial_refresh_PROOF.md.

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


## Positive causal domination and sharpness

For each padded local tester let T_i be its positive all-pass operator. Its optimum against every admissible prover is at most F_i=F_{K_i}. The causal domination theorem (Gutoski and Watrous, Toward a General Theory of Quantum Games, 2007, Theorem 9, printed pages 13-14, https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf) supplies a normalized positive causal operator R_i with T_i <= F_i R_i. In the matching message convention its prefix operators obey Tr_{Y_{i,k}}R_{i,k}=I_{X_{i,k}} tensor R_{i,k-1}, with scalar initial prefix 1. Tensoring these equations shows tensor_i R_i is normalized after regrouping common rounds. Positivity yields tensor_i T_i <= (product_i F_i) tensor_i R_i. Pairing with any compatible joint prover proves the claimed product bound. This invokes the published causal-domination theorem rather than deriving that theorem from axioms.

Tensor the independent singleton equality witnesses, with their own sector labels and orthogonal sinks, to attain the product for any prescribed node schedule and budgets. All dimensions and K_i are finite. This proves sharpness over arbitrary finite baths, not within every fixed constrained bath realization.

## Unchanged-action simulation detail

After padding coarse sectors to equal dimensions and removing the coarse-preserving baseline in its interaction picture, each normalized own-odd Hermitian interaction has a block off-diagonal contraction K between the two own-parity sectors, separately for each other coarse string. Write K=U H with H positive and 0<=H<=I, extending the polar partial isometry to a unitary U. Then W_plus=U(H+i sqrt(I-H^2)) and W_minus=U(H-i sqrt(I-H^2)) are unitaries whose average is K. The corresponding odd Hermitian generator is the average of two coarse-parity-diagonal conjugates of the private X rotation. Implement each conjugation as a free joint prover gate on copied coarse strings and bath. Alternating the two rotations with half the exposure gives, by Lie-Trotter convergence, the desired interaction with exactly the original own-coordinate action. Time-discretize bounded integrable generators and refine the partition, retaining every actual channel node; norm convergence of the finite products gives convergence of their effects. Equivalently keep the baseline as intervening free diagonal gates. Every node in the approximation is encoded exactly by the above auxiliary-label construction. Conjugating fine projectors when changing interaction picture preserves their coarse commutation and sector count. These operations introduce no extra own-odd action. The product inequality holds for every approximant and passes to the limit. The one-gap sine transition bound used by the singleton proof is the same bath-uniform good/bad transition estimate as in the included binary source.

## Reproducible interface check and scope

../checks/check_label_interface.py checks the encode/pinch/decode identities exactly over rational matrices for two coarse bits sharing a bath qubit. One fine resolution uses bath Z sectors and the other bath X sectors. The fine resolutions do not mutually commute, but both commute with all coarse bits. The script verifies unitarity and every projector intertwining and decoding identity. This is an interface check, not a substitute for the causal proof or a hardware qualification.

This result is separate from finite-width private-Z refresh analysis. Substituting F_K for F in a finite-width remainder formula is not justified without separately proving the physical multi-sector controller's channel, commutation, privacy and approximation bounds. One physical Z random phase supplies binary dephasing, not full-group pinching. Historical priority is not established. No new license grant is made for this analysis.
