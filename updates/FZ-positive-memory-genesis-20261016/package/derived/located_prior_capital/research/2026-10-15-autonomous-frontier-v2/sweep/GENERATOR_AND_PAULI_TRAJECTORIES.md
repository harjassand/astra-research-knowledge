# Exact autonomous generator and code-initial Pauli representation

Status: supplied mathematical local generator. The monotone-envelope and transfer companions analyze this generator. Local jump engineering, energy/reset/calibration costs, and a physical 3D embedding are not acquired. Previous-campaign artifacts are not changed.

## 1. Code and local jumps

Take the cubical 4-torus of side L. Put one qubit on each positively based face (v;i,j), 1<=i<j<=4. There are six qubits per cell, so the cell Hilbert dimension is 64. The code has parameters [[6L^4,6,L^2]]. Its X checks A_e are products over the six faces incident to an edge e; its Z checks B_c are products over the six boundary faces of a 3-cube c. Error 2-chains are over F_2. Z errors have a primal closed edge syndrome, while X errors have a closed edge syndrome on the dual cubical lattice.

At a primal vertex v let incoming edges be e_i(v-u_i) and outgoing edges e_i(v), i=1,...,4. For each nonempty even subset O of {1,2,3,4}, define the local syndrome projector Pi_(v,O) onto the event:

- all four incoming A_e values are +1;
- the outgoing A_e value is -1 exactly for i in O.

There are seven such O: the six pairs and the full four-element set. Pair O in increasing order, and let F_(v,O) be the sum of the positively based faces p_ij(v) for these one or two pairs. The correction jump is

    L^Z_(v,O)=sqrt(kappa) Z(F_(v,O)) Pi_(v,O).

Use precisely the same construction on the dual lattice for X correction jumps L^X_(v*,O), using the dual-edge syndrome determined by B_c.

Each jump is supported on at most 24 qubits. For the primal jump these are the faces meeting v, which support all eight incident-edge checks and the correction faces. The dual count is the same by self-duality. Each jump writes at most two qubits. All support sizes, ranges, and operator norms are independent of L. Grouping faces by their positive base cell gives bounded cell interaction range (at most one in the cell l_infinity metric). The choice of sorted direction pairing is fixed and translation invariant.

The generator is

    L_total = sum_(v,O) D[L^Z_(v,O)]
            + sum_(v*,O) D[L^X_(v*,O)]
            + sum_faces (lambda_X D[X_f]
                       + lambda_Y D[Y_f]
                       + lambda_Z D[Z_f]),

where D[L](rho)=L rho L^dagger - {L^dagger L,rho}/2. No Hamiltonian is needed. All rates are constant in time and independent of L. The correction jump norm is sqrt(kappa), and the seven projector patterns at one vertex are mutually orthogonal, giving sum_O (L_(v,O)^dagger L_(v,O))<=kappa I.

In the classical representation below this is exactly an independent attempted vertex clock of rate kappa: at an active local syndrome apply its unique F_(v,O); otherwise do nothing. The null attempted clocks are an analysis representation, not additional physical operations.

## 2. Exact Pauli-trajectory lemma from any code state

This argument is included explicitly because the literal Definition 2.22 in Drechsler-Oreg-Aharonov 2610.05589v1 has jumps P_i f with a SINGLE-qubit Pauli P_i. Our four-outgoing-edge correction instead flips two face qubits simultaneously. Their single-bit formulation should not be cited as a black box containing this generator. The following elementary invariant-family proof covers local Pauli strings directly.

Let rho_0 be any density operator in the code space, possibly entangled with an arbitrary external reference. For error labels a,b in F_2^(faces), put

    rho_(a,b) = (X^a Z^b tensor I_ref) rho_0
                (Z^b X^a tensor I_ref).

Each such density operator is supported on a definite joint stabilizer-syndrome sector. For a local syndrome projector Pi, there is a scalar chi_(a,b) in {0,1} with Pi rho_(a,b)=rho_(a,b) Pi=chi_(a,b) rho_(a,b). For any Pauli string Q and jump L=sqrt(gamma) Q Pi,

    D[L](rho_(a,b))
       = gamma chi_(a,b) (Q rho_(a,b) Q^dagger-rho_(a,b)).

The same identity holds for unconditioned Pauli noise with Pi=I. Thus, if p_t(a,b) solves the finite classical forward equation with these syndrome-dependent Pauli-label transitions and starts at label (0,0), then

    rho_t = sum_(a,b) p_t(a,b) rho_(a,b)

solves the Lindblad master equation exactly. Finite-dimensional uniqueness proves the identity. Linear dependence among some rho_(a,b) does not matter: this constructs a valid mixture solving the equation. Event probabilities are independent of the encoded logical state and of its entanglement with the reference.

A Y_f noise event toggles both a_f and b_f, preserving the true cross-sector correlation. Marginally, the primal syndrome has independent face births at rate lambda_Z+lambda_Y and the dual syndrome at rate lambda_X+lambda_Y. Corrections in one CSS sector do not change the syndrome of the other. No independence of the two sectors is asserted or needed for the final union bound.

If a fixed final component-filling decoder leaves both corrected error chains homologically trivial, the remaining Pauli is a product of stabilizers up to a global phase. It acts as the identity on every encoded state, including reference-entangled inputs. Therefore any classical bad-path probability epsilon gives an exact logical-channel decomposition with an identity component of weight at least 1-epsilon, implying entanglement infidelity at most epsilon and diamond distance to identity at most 2epsilon.

## 3. Initialization, resources, and scope

Initialization is a supplied arbitrary code-space state. The physical memory carries only the six qubits per cell; there is no noiseless classical layer, coarse bit eta, sampled-time register, or globally scheduled operation. The auxiliary envelope, block scale b, slab duration Delta, LSS coupling, and contour witnesses are analysis objects.

The readout used in the theorem is a fixed ideal syndrome measurement plus the fixed decoder defined in HOMOLOGY_AND_SLAB_TRANSFER.md. Efficient or noisy implementation of this readout is not established. The theorem concerns the stated independent local Pauli births and exact conditioned jumps. Arbitrary coherent errors, arbitrary perturbations of jump projectors, or noisy processing hardware are outside its proved model.

Physical 3D realization of the supplied 4D graph, code preparation, conditioned-jump fabrication, reservoir acquisition, reset, energy, calibration, and imperfect readout costs remain UNKNOWN. No hardware or practical-rate advantage is inferred from a mathematical lifetime proof.

## 4. Competitor boundary checked in this campaign

- [Drechsler-Oreg-Aharonov, 2610.05589v1](https://arxiv.org/html/2610.05589v1), Sections 1.5.3 and 1.8, explicitly leaves the nonthermal time-independent asynchronous memory problem open. Its literal single-qubit-jump class is narrower than the two-face sweep event above.
- [Kubica-Preskill, 1809.10145](https://arxiv.org/pdf/1809.10145) supplies the sweep operation and static perfect-syndrome threshold. Our operation is an asynchronous specialization; the proposed new contribution is the ongoing-noise proof mechanism, not invention of sweep decoding.
- [Kumar-Weimer, 2602.19288v1](https://arxiv.org/html/2602.19288v1), Sections II.3 and III, studies continuous-time 2D toric dynamics coupled to a classical scalar field. Its field update includes a size-dependent penalty phi/L^2 and its phase diagram and memory evidence are numerical. It does not supply the fixed-resource rigorous lifetime theorem sought here. This comparison does not establish historical novelty of our proof mechanism.
