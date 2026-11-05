# Schur analysis of the homogeneous tracial partial-SWAP stream

## Status and scope

This note proves a boundary on the ordinary Schur compression route. It does **not** prove a general memory lower bound for the homogeneous source, and it does **not** construct the requested causal decoder. The accepted partial-SWAP acquisition and inverse-dummy theorem is used without revalidation.

Source: one unknown qubit S, possibly entangled with an arbitrary reference; independent incoming carriers E_i = I/2; U_i = exp(i theta SWAP_{S,E_i}); chronological access to E_1,...,E_N; final S discarded; no purifiers, preparation labels, or return link. Error is half the diamond norm.

## 1. Ordered collisions are not permutation symmetry

Define bath payload operators

    B_N^a = (1/2) Tr_S[U_N ... U_1 (sigma_a^S tensor I) U_1^dagger ... U_N^dagger].

For rho = (I + sum_a r_a sigma_a)/2, the output is

    C_N(rho) = 2^(-N) [I + sum_a r_a B_N^a].

All U_i commute with collective SU(2), so B_N^a is a vector under collective rotations. They do not commute with arbitrary permutations of the bath: changing bath order changes the chronological circuit.

For two carriers, c = cos(theta), s = sin(theta), and the cross product is (sigma_1 cross sigma_2)_a = sum_bc epsilon_abc sigma_b^1 sigma_c^2. Direct conjugation gives

    B_2^a = s^2 [sigma_a^1 + c^2 sigma_a^2 + c s (sigma_1 cross sigma_2)_a].

The z component has eigenvalues

    +/- s^2 (1+c^2),  +/- s^3 sqrt(4-3s^2).

In the singlet/triplet-zero basis, its inter-sector block is

    s^2 [s^2 X + 2 c s Y].

Thus even at N=2, dephasing total spin changes the acquired channel. For larger N, a vector operator in Schur form can connect J to J and J +/- 1, with operators on the permutation multiplicity spaces. SU(2) covariance supplies no reason for those multiplicity operators to be scalar or mutually commuting.

## 2. A general obstruction to discarding multiplicities

Let C be **any** SU(2)-covariant qubit-to-N-qubit channel satisfying C(I/2)=I/2^N. Let T be the bath permutation twirl. Standard Schur compression that records J, keeps the spin-J representation Q_J, and discards the permutation multiplicity P_J has exactly the same recoverable information as T C: the discarded maximally mixed multiplicities can be reattached.

Write

    (C^2)^(tensor N) = direct_sum_J Q_J tensor P_J,
    dim Q_J = 2J+1,
    mu_J = binom(N,N/2-J) - binom(N,N/2-J-1),
    w_J = (2J+1) mu_J / 2^N.

Binomial coefficients outside their integer range are zero. The classical J distribution w_J is independent of the input. Covariance and the permutation twirl imply the conditional channel

    C_J(rho) = [I_(2J+1) + beta_J r dot J]/(2J+1).

The absence of inter-J terms follows from inequivalent symmetric-group representations; within Q_J the rank-one irreducible tensor occurs once.

Complete positivity is equivalent to

    -1/(J+1) <= beta_J <= 1/J          (J > 0).

To see this, conjugate the normalized Choi matrix on the input qubit by Y. Its nonconstant part is -beta_J sigma dot J. The latter operator has eigenvalues -beta_J J on total spin J+1/2 and beta_J(J+1) on total spin J-1/2.

Any recovery may be averaged over SU(2), without increasing its distance to the identity. A covariant decoder from spin J to a qubit has Heisenberg form

    D_J^*(sigma_a) = gamma_J J_a,
    -1/(J+1) <= gamma_J <= 1/J.

The composition is depolarizing with coefficient

    t_J = beta_J gamma_J J(J+1)/3 <= (J+1)/(3J).

The J=0 branch has coefficient zero. Consequently, even the optimum recovery after the multiplicities are discarded satisfies

    t <= t_bar_N := sum_(J>0) w_J (J+1)/(3J),

and its half-diamond error obeys

    epsilon >= (3/4)(1-t_bar_N)
            = 1/2 + w_0/4 - (1/4) sum_(J>0) w_J/J.

This statement includes arbitrary later processing and unlimited classical memory of J. It is independent of theta. For large N,

    sum_(J>0) w_J/J = sqrt(8/(pi N)) + O(1/N),
    epsilon >= 1/2 - 1/sqrt(2 pi N) + O(1/N).

It rules out the standard logarithmic-register Schur compression at one-percent error. It does not rule out retaining an appropriate coherent part of multiplicity data, nor a receiver using a different representation.

In particular, the theorem does **not** cover a coherent J register with a carefully aligned multiplicity basis. Adjacent irreducibles Q_(K-1/2) direct_sum Q_(K+1/2) are unitarily equivalent, as SU(2) representations, to a qubit tensor a spin-K gauge. Thus inter-J coherence can carry a noiseless qubit. Measuring J would destroy that possibility. At N=43,462 the exact combinatorial bound for the measured-J compression is 0.498074876985 in half-diamond error; this is an analytic sum, not a simulation of that many qubits.

## 3. Efficient basis change does not close the causal normalization step

Bacon, Chuang, and Harrow construct an efficient Schur transform by sequential Clebsch-Gordan steps. Each step produces the new total spin and a coherent branching-path bit. Those path bits constitute the multiplicity register. Keeping the transform unitary retains them; discarding them invokes the obstruction above.

The payload operators also have constant-bond matrix-product descriptions. A locally purified matrix-product Choi state can be generated with a bounded virtual system, but this does not establish a channel consuming the physical inputs in chronological order. A state-generation tensor only obeys

    sum_(a,f) T_(a,f)^dagger T_(a,f) = I.

A channel tensor that consumes an arbitrary input a requires the stronger identity

    sum_f T_(a,f)^dagger T_(b,f) = delta_(a,b) I

(up to the chosen Choi normalization). Bell contraction of a state-preparation tensor otherwise gives a postselected map. For the straightforward Choi-state teleportation implementation, the all-identity Bell branch has probability 4^(-N), which cannot be hidden in a near-linear execution claim.

## 4. Crossed-source tensor: an exact causal filter with an explicit exponential cost

There is a sharper algebraic reformulation than teleporting all N inputs. Let

    W = U_1^dagger ... U_N^dagger,
    V_j = (U_j^dagger)^(T_S) = c I - 2 i s Phi_(A,E_j),
    V_total = V_N ... V_1 = W^(T_S).

The equality of products holds because the bath factors belonging to different sites commute, while partial transpose reverses the shared source matrix multiplication. Prepare an accessible Bell pair R,A. For every bath input Y, including inputs entangled with a reference,

    Tr_(A,E)[ V_total (Phi_(R,A) tensor Y) V_total^dagger ] = D_N(Y),

where D_N is the accepted inverse-dummy/Petz channel. This identity follows by writing V_(a,r)=W_(r,a) in source matrix blocks. The receiver tensor order is now chronological.

This is not a deterministic implementation: V_j has singular values c on the Bell-orthogonal subspace and sqrt(1+3s^2) on Phi. With g=1+3s^2, the physical success Kraus operator K_j=V_j/sqrt(g) is a contraction. Its complement can be chosen

    L_j = (2 |s|/sqrt(g)) (I-Phi).

The instrument {K_j,L_j} acts on the two currently available qubits A,E_j. Keep R,A and one incoming carrier; stop with failure on any L outcome. On N successive K outcomes the normalized acquired channel is exactly D_N C_N, and the success probability is exactly g^(-N), independent of the input/reference. At N of order theta^(-4) log(1/epsilon), the probability is exp[-Theta(theta^(-2) log(1/epsilon))]. Repetition would require fresh unknown payload copies, which are not supplied; even with such copies, the execution bill is exponential in theta^(-2). It therefore fails the requested operation.

A related deterministic local instrument is available. For the four Bell projectors Phi_p, the Kraus operators

    A_p = (c/2) I - i s Phi_p

obey sum_p A_p^dagger A_p=I. The outcome p is retained classically. This supplies a concrete weak Bell instrument for a two-qubit-memory receiver search, but its other branches have not been shown to recover the same logical channel. Correcting both memory halves in the naive way implements a Bell twirl and erases earlier payload information. A useful adaptive completion remains an unproved possibility, not a result of this note.

The finite matrix checks in check_schur.py verify the two-carrier formula, its spectrum, the crossed-filter singular values, and the weak-Bell instrument normalization. They do not test or establish a successful long-stream receiver.

## Primary references

* D. Bacon, I. L. Chuang, A. W. Harrow, Efficient Quantum Circuits for Schur and Clebsch-Gordan Transforms, Physical Review Letters 97, 170502 (2006), arXiv:quant-ph/0407082. https://arxiv.org/abs/quant-ph/0407082 ; full text https://arxiv.org/html/quant-ph/0407082v4 .
* A. Bisio, G. M. D'Ariano, P. Perinotti, M. Sedlak, Memory cost of quantum protocols, Physical Review A 85, 032333 (2012), arXiv:1112.3853. https://arxiv.org/abs/1112.3853 . The comb normalization and globally compatible decomposition conditions are material; a small Schmidt or MPO rank is not itself their realization criterion.
* M. Ziman, P. Stelmachovic, V. Buzek, M. Hillery, V. Scarani, N. Gisin, Diluting quantum information: An analysis of information transfer in system-reservoir interactions, Physical Review A 65, 042105 (2002), arXiv:quant-ph/0110164. https://arxiv.org/abs/quant-ph/0110164 . This is the quantum homogenizer setting; the present note does not claim that setting is new.

The boundary in section 2 is derived here. The general causal receiver problem remains open in this note.
