# Coherent spin fusion: physical instrument and source-specific losses

This continues the exact homogeneous partial-SWAP task. The positive result here is a fully specified growing-spin CPTP receiver, with an efficient representation and an explicit execution bill. Its required recovery performance has **not** been proved and the natural fixed choice performs poorly in finite diagnostics. A second result proves an exact fourth-order payload loss when consecutive-pair fusion labels are made classical. Neither result is a general no-go for adaptive coherent fusion.

## 1. A genuine crossed-spin fusion instrument

Write u = cot(theta), and let Q_J be a spin-J memory. Let R be an additional qubit. Initialize R,Q_(1/2) in a singlet. This is equivalent to the Bell initialization in the crossed-source identity after a fixed Y basis change.

On Q_J tensor E, with E the current incoming carrier, let P_+ and P_- project onto total spins J+1/2 and J-1/2. The spin-J crossed Lax operator has the two eigenvalues

    v_+ = u + i(J-1/2),
    v_- = u - i(J+3/2).

Set

    g_J = u^2+(J+3/2)^2,
    K_J = (v_+ P_+ + v_- P_-)/sqrt(g_J).

Let C_+: Q_(J+1/2) -> Q_J tensor C^2 be the usual Clebsch-Gordan isometry onto P_+. Define the rectangular failure Kraus operator

    L_J = sqrt[2(2J+1)/g_J] C_+^dagger.

Then

    K_J^dagger K_J + L_J^dagger L_J = I.

On K, discard the current E and keep R,Q_J. On L, retain the fused spin Q_(J+1/2) coherently, keep R, and record the branch. This is a deterministic instrument when both outcomes are included. It never accesses the original source or bath purifiers. At J=1/2, K is precisely the normalized crossed partial-SWAP filter, in the singlet convention, and L retains its triplet complement.

The complete retained quantum system is R tensor Q_J, not the scalar J label. Its maximum dimension after N collisions is 2(N+2), so its quantum memory needs at most 1+ceil(log2(N+2)) qubits. One carrier and workspace are added during each update. J and the measurement history are classical and may be retained. This memory claim is about the specified physical instrument; it is not a recovery claim.

### Implementation cost

Use binary registers for J,m. A spin-J plus spin-1/2 Clebsch-Gordan transform consists of reversible arithmetic and controlled two-dimensional rotations. In that basis K_J is a two-value diagonal filter, implementable with a flag ancilla, phase shifts, and one controlled rotation. L_J is the upper-branch fusion isometry. With gate synthesis and arithmetic precision delta per step, the ideal-to-implemented channel distance is bounded by N delta via the ordinary hybrid bound. Choosing delta = O(epsilon/N) gives polynomial cost in log(N/epsilon) and the input bit length of theta per step, provided the binary-register encoded spin operations are compiled as stated. A conservative source-angle calibration requirement is absolute error O(epsilon/N); actual acquisition exposure for that calibration is not supplied by this mathematical construction.

Peak local Hamiltonian norms can remain bounded, but this requires an explicit service-time premise. If a compiled update has depth G and the receiver clock is Omega_R, the incoming spacing must be at least order G/Omega_R for the stated small-buffer serial realization. With a fixed faster stream spacing Delta and no ability to slow it, a single sequential memory update can accumulate order N(1-Delta Omega_R/G) waiting carriers. That backlog is quantum memory and would destroy the logarithmic-memory bill. If the source permits idle intervals between its unchanged weak encounters, they must be included in total collection time N Delta and protected-source exposure. Neither a native high-spin interaction nor arbitrarily fast arithmetic is granted.

Thus this instrument family has O(N polylog(N/epsilon)) elementary processing, O(log N) retained quantum memory plus arithmetic workspace, a prepared singlet, O(N) measured/reset flags, and O(N log N) or fewer classical history bits depending on the record format. Memory protection and gate errors remain physical resources. No native high-spin interaction is assumed free.

## 2. What symmetry makes tractable, and what it does not

Introduce the reference R0 maximally entangled with the source S. After conjugating R0 by Y, the Choi state is invariant under collective SU(2). For a receiver whose coherent memory is R tensor Q_J, the joint invariant state lies on

    R0 tensor S tensor R tensor Q_J.

For J >= 3/2 the total-spin multiplicities are

    J-3/2: 1,   J-1/2: 3,   J+1/2: 3,   J+3/2: 1.

An invariant density operator therefore needs only 1^2+3^2+3^2+1^2 = 20 real Hermitian-block parameters, including its trace. This is a representation of the known conditional Choi state for each classical history. It does not replace the physical quantum memory or turn an arbitrary compression into a CPTP channel.

General SU(2)-covariant controls on R,Q_J,E have constant-size multiplicity blocks. Hence adaptive policies in this receiver family can be specified through small matrices plus Clebsch-Gordan arithmetic. The physical state may retain coherence between the two irreducible sectors inside R tensor Q_J. Measuring that internal sector is not licensed by the small parameter count.

The implemented diagnostic fusion_probe.py propagates the complete finite-dimensional reference/source/receiver state, not just source marginals. It supports the crossed instrument and projective upper/lower Clebsch-Gordan fusion, and can retain every classical branch history at small N. For the fixed crossed instrument with only the current J record, theta=.6 gives Petz entanglement fidelities about .351 at N=3 and .273 at N=20. Projective fusion with the full classical history gives about .397 at N=5 and .354 at N=12. These are performance diagnostics of those choices, not proofs about all controls in the family. The general adaptive policy has not been solved.

### Coherent completion is not yet compression

In a Stinespring implementation of K_J,L_J, the lower fused sector has one flag state and the upper fused sector has a different, generally nonorthogonal flag state. Within each sector the flag amplitudes are fixed numbers, independent of the vector in that sector. A controlled unitary can therefore uncompute this flag while preserving upper/lower coherence. What remains is precisely an isometric retention of both Clebsch-Gordan branches, with dimension (2J+2)+(2J)=2(2J+1), the full incoming dimension. It has not erased an input degree of freedom. Iterating coherent CG fusion in general creates path multiplicities; keeping a spin label alone is not a unitary implementation of that iteration. The actual source family could permit a further approximate reduction, but that is the missing theorem, not an implication of the flag completion.

### A single large irrep is mostly a classical frame for this joint family

There is also an exact representation-level approximation bound. Let rho be any SU(2)-invariant state on A tensor Q_J with dim A=8 and A carried by the three qubits R0,S,R. Then rho contains only tensor multipoles l<=3 on Q_J and rho_Q=I/(2J+1). The spin-coherent measure-and-prepare channel on Q_J multiplies multipole l by

    lambda_l = (2J)! (2J+1)! / [(2J-l)! (2J+l+1)!].

Here B_J(X)=(2J+1) integral |J,n><J,n| <J,n|X|J,n> dOmega/(4pi). The multiplier follows by evaluating a highest-weight matrix element of B_J((J_+)^l): with n=2J the remaining integral is integral_0^1 x^n(1-x)^l dx=n!l!/(n+l+1)!. This supplies the displayed formula without a classical-noise assumption.

For J>=3/2,

    (1/2)||rho - (id_A tensor B_J)(rho)||_1
        <= 4 max_(0<=l<=3)(1-lambda_l) = O(1/J).

Proof: the channel is diagonal in the orthogonal multipole basis. The operator inequality rho <= 8 I_A tensor rho_Q gives ||rho||_2 <= sqrt[8/(2J+1)]. Applying the Hilbert-Schmidt multiplier bound and then ||X||_1 <= sqrt[8(2J+1)]||X||_2 yields the displayed constant. This says that a large single-J register, with only a qubit companion, is close to a classical orientation register on the relevant invariant family. It does not prove an efficient implementation of that classicalization, or a no-go for a qubit plus arbitrary classical feedback.

A full quantum frame instead retains coherent multiple J sectors and growing right multiplicities, for example direct_sum_(J<=Jmax) Q_J tensor Q_J with dimension O(Jmax^3). The simple fixed-unitary frame operations in rotor_probe.py retain these coherences but have not exhibited recovery. At theta=.3, J=0,...,3, sine-weight frame initialization, and the actual carrier interaction exp[i theta (L dot sigma_E + I/2)], the best sampled receiver-only Petz fidelity through N=600 is .2831389233 at N=10. No bath random-unitary unraveling is used in this calculation.

## 3. Same-angle physical collisions do not supply the ordinary integrable fusion condition

Let W_12 swap two bath qubits, P_s=(I-W_12)/2 and P_t=(I+W_12)/2. For two homogeneous source collisions,

    U_2 U_1 = c^2 I + i c s (W_(S,1)+W_(S,2)) - s^2 W_(S,2) W_(S,1).

The first two terms preserve the bath singlet/triplet decomposition. The product term does not. Exactly,

    || (I_S tensor P_s) U_2 U_1 (I_S tensor P_t) || = (sqrt(3)/2) s^2.

This follows by reducing the three-spin space into total spin 3/2 and the two copies of spin 1/2. On the latter multiplicity space, the two source/bath transpositions are reflections with off-diagonal entries +/- sqrt(3)/2; their product has off-diagonal magnitude sqrt(3)/2.

For two real angles theta_1,theta_2, the squared leakage norm is

    (3/4) [sin^2(theta_2-theta_1) + sin^2(theta_1) sin^2(theta_2)].

It cannot be canceled by choosing two nonzero real weak angles. Standard rational R-matrix fusion instead uses a string of shifted spectral parameters. That algebraic fusion premise is not supplied by the homogeneous once-through physical source. A receiver may attempt to create an effective shifted representation with measurements and feedback, but must prove and pay for that physical conversion.

## 4. Exact payload obstruction for classical consecutive-pair fusion labels

Consider the following preprocessing of the actual source output. After each consecutive pair E_(2k-1),E_(2k), measure its singlet/triplet label and keep both representation blocks and the complete classical result. Retain all of these processed bath systems and allow an arbitrary final decoder. This gives strictly more quantum storage than any scheme that subsequently compresses those blocks. Nevertheless its asymptotic acquired channel cannot approach perfect recovery.

Set x=sin^2(theta). Use normalized Hilbert-Schmidt inner products. For one input source Pauli, after the two collisions and the pair-label dephasing, the squared norm exported to source identity is

    b = x^2 (2-x)^2 / 2.

The squared norm still carried by source-traceless terms is

    h = (1-x)^2 (1+2x) = 1-3x^2+2x^3.

The total is

    q = b+h = 1-x^2+x^4/2.

### Derivation

The bath-identity part is

    [x(2-x)/2] (sigma_a^1+sigma_a^2),

whose norm squared is b. The source-traceless part has three mutually orthogonal Pauli-weight groups. Their squared norms are

    (1-x)^4,
    4(1-x)^3 x,
    3(1-x)^2 x^2.

Their sum is h. SU(2) covariance makes the same scalar identities hold for all three Pauli directions and all cross-inner-products. They therefore extend to arbitrary operator coefficients on all previous outputs; no independence of old outputs is assumed.

Previously exported source-identity information persists. Each new exported contribution has a traceless fresh-pair factor and is orthogonal to older exports. Consequently, after K pairs,

    p_K = b (1-h^K)/(1-h)

is the exact Gram coefficient of the channel to the processed bath. The normalized-adjoint/Petz recovery has depolarizing coefficient p_K. The all-decoder Cauchy-Schwarz bound gives

    epsilon_opt >= (3/4) (1-sqrt(p_K)).

In particular,

    p_K <= p_infty = (2-x)^2/[2(3-2x)] <= 2/3,
    epsilon_opt >= (3/4)(1-sqrt(2/3)) = 0.1376275643...

The source is discarded here as in the target task. Even if the true source is additionally granted at the end, the Gram coefficient is p_K+h^K and has the same asymptotic limit. A single pair-label measurement already causes an irrecoverable full-source-plus-output loss of order x^2 = theta^4: its best-recovery error is at least (3/4)(1-sqrt(q)).

This proves that the measured labels in this simple fusion construction are not redundant for the arbitrary input/reference payload. The information they erase appears at precisely the fourth-order acquisition scale. It does not exclude a receiver preserving their coherence in another representation, or an adaptive multiplicity rotation before measurement.

## Primary sources and scope of reuse

* D. Bacon, I. L. Chuang, A. W. Harrow, Efficient Quantum Circuits for Schur and Clebsch-Gordan Transforms, PRL 97, 170502 (2006), https://arxiv.org/abs/quant-ph/0407082 . Supplies efficient CG/Schur circuitry, not permission to discard this source's path registers.
* W.-L. Yang, R. I. Nepomechie, Y.-Z. Zhang, Q-operator and T-Q relation from the fusion hierarchy, Physics Letters B 633, 664-670 (2006), https://arxiv.org/abs/hep-th/0511134 , equation (3.1), full text https://arxiv.org/html/hep-th/0511134v2 . States fusion with successively shifted spectral parameters. The physical leakage and payload formulas above are derived here for the rational partial-SWAP setting.

The target operation remains open in this note. The growing-spin instrument has a complete physical definition and execution bill; its target recovery theorem is the unresolved part.
