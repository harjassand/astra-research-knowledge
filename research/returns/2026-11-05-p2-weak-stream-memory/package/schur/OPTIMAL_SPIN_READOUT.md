# Exact optimal final readout from a qubit and one spin representation

This supplies the final quantum operation for a covariant fusion receiver. It does not assert that any proposed acquisition policy achieves the required state. It removes a final-decoder approximation from that question.

## Theorem

Let F map one input qubit to memory M = C^2 tensor Q_J and be SU(2)-covariant, with the receiver qubit and Q_J transforming in their usual representations. A classical history label may be retained: apply the construction separately to each history. The probability of an invariant history is independent of the input.

Let rho be the normalized Choi state of F, in reference-qubit/memory order. Conjugate the reference by Y, so the Choi state is invariant under collective SU(2). Couple the memory qubit with Q_J to K_- = J-1/2 and K_+ = J+1/2, then couple that memory representation to the reference qubit. For J>=1 the total-spin blocks are

    L=J-1:  a I_(2J-1),
    L=J:    I_(2J+1) tensor B,
    L=J+1:  c I_(2J+3),

where a,c>=0 and B is a positive 2x2 matrix in K_-,K_+ order. These are per-magnetic-state coefficients; normalization is

    (2J-1)a + (2J+1)Tr(B) + (2J+3)c = 1.

Put d_-=2J, d_+=2J+2. Then the maximum entanglement fidelity over **all** CPTP decoders M->qubit is

    F_opt = (1/2) max_(0<=x,y<=1) {
         d_- a(1-x) + d_+ c(1-y)
       + d_- B_-- x + d_+ B_++ y
       + 2 sqrt(d_- d_+) |B_-+| sqrt(x y) }.

The optimum payload error in the half-diamond convention is exactly

    epsilon_opt = 1-F_opt.

For an unnormalized history Choi state of trace p, the same expression returns p times that history's optimum fidelity. Sum these contributions across the retained classical histories before taking 1-F_opt.

## Finite evaluation, without a large SDP

Define

    A=d_-(B_---a),  C=d_+(B_++-c),
    H=sqrt(d_-d_+) |B_-+|,
    r=sqrt(x), t=sqrt(y).

The nonconstant objective is A r^2 + C t^2 + 2 H r t on the square [0,1]^2. Its maximum occurs at a corner or at one of the two possible edge stationary points

    (r,t)=(1,-H/C)  if C<0 and -H/C in [0,1],
    (r,t)=(-H/A,1)  if A<0 and -H/A in [0,1].

Thus at most six elementary evaluations suffice. A nonzero interior stationary point is homogeneous and has value zero, already obtained at (0,0).

At J=1/2 the L=J-1 block is absent and x is forced to1; optimize only t. At J=0 the memory is one qubit: the transformed Choi has a singlet scalar a and a triplet scalar b, and F_opt=max(a,b).

## Proof of optimality

Average any decoder over SU(2). This preserves its entanglement fidelity and cannot increase its diamond distance to the identity after F. Its Choi operator can consequently be taken invariant after conjugating the memory input by its spin time-reversal unitary.

Write the decoder's invariant blocks as a_D,B_D,c_D in the same coupling scheme. Partial trace over the output qubit gives precisely

    (2J-1)a_D + (2J+1)(B_D)_-- = d_-,
    (2J+1)(B_D)_++ + (2J+3)c_D = d_+.

Complete positivity is a_D,c_D>=0 and B_D>=0. Parameterize

    (B_D)_-- = d_- x/(2J+1),
    (B_D)_++ = d_+ y/(2J+1).

The maximum magnitude of its off-diagonal is sqrt(d_-d_+)sqrt(xy)/(2J+1). Choose its phase to align the Choi objective. Positivity allows this magnitude to be saturated, so no relaxation is involved. Substitution into the Choi fidelity pairing gives the theorem's expression.

For every decoder, diamond error is at least its loss of maximally entangled fidelity. The averaged optimal decoder composed with F is a qubit depolarizing channel; for that channel half-diamond error equals 1-F_e. The lower bound is therefore attained.

## Explicit physical decoder

The decoder may be dilated using environment spins J-1,J,J+1. Coherently transform the memory R,Q_J into K_-,K_+ registers. Do **not** measure K: its coherence is part of the resource.

For K_- choose amplitudes sqrt(1-x) into environment spin J-1 and sqrt(x) into environment spin J. For K_+ choose sqrt(y) into environment spin J and sqrt(1-y) into environment spin J+1. Apply the unique Clebsch-Gordan isometry from each K to output qubit tensor its selected environment spin. The shared-J alternatives retain their relative phase, chosen from B_-+. The images belonging to different K are orthogonal irreducible subspaces, so the map is an isometry. Trace the environment to obtain the decoder.

Equivalently, a concrete positive TP decoder Choi matrix is constructed in covariant_spin_readout.py. That implementation fixes all time-reversal and phase conventions; it directly verifies fidelity from the original (untransformed) Choi state.

## Resources and errors

This readout uses coherent CG transforms, a constant number of controlled amplitude rotations, and O(log(J+1)) initialized work qubits. Binary-register CG compilation and reversible arithmetic give cost polynomial in log(J+1) and log(1/delta) for implementation error delta. No native extensive spin coupling is assumed. The environment is discarded only after the final isometry. A protected output qubit and any protection used during the operation remain charged resources.

The six block parameters are computed from the known physical acquisition model and the actual classical history; no measurement or tomography of the arbitrary payload is performed. Calibration and model error are separate from the exact readout theorem. If the implemented memory channel differs from its declared channel by eta in half diamond and this decoder is implemented to delta, total error is at most (1-F_opt)+eta+delta.

## Executed finite checks

covariant_spin_readout.py generates 48 random covariant Choi states for J=0,1/2,1,3/2,2,3, constructs their optimal decoder Choi operators, and checks positivity, trace preservation and the exact fidelity formula. It also checks the identity channel with an independent maximally mixed spin gauge for each J. Maximum formula/direct-fidelity residual was 2.22e-16; maximum TP residual was 8.86e-16. These verify the finite implementation and conventions, not any acquisition performance claim.

The representation-theoretic reduction and coherent CG implementation reuse the standard Schur/Clebsch-Gordan machinery of Bacon, Chuang and Harrow, arXiv:quant-ph/0407082. The optimization and explicit phase convention are derived here for the receiver memory under consideration.
