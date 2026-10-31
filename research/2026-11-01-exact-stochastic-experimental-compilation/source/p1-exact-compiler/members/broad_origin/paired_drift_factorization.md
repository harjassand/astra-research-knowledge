# Paired drift can reveal an executable tensor factorization

Working construction and explicit prior-art qualification, 31 October 2026.

## Status and main result

This note constructs a reusable Clifford decoder from paired experimental
preparations whose individual-state average is maximally mixed. The paired
source changes from shot to shot, so it is not tomography of a fixed unknown
pure state. The construction is elementary, has a polynomial acquisition bound,
and is implemented in `twin_factorization.py`.

**This is not a claimed major new capability or a demonstrated advantage over
the strongest conventional method given the same paired observations.**
Aguilar, Jerbi, Eisert, and Bittel, arXiv:2609.27565v1 (September 2026), already
develop a polynomial Bell-quadratic-symmetry learner for Clifford-dressed
product pure states. Their quadratic lifting and algebra decomposition are the
strongest comparator. The source here is an ensemble of correlated twins,
rather than repeated copies of one pure state; its particularly simple
algebra admits an explicit kernel/image splitting implementation. This is a
useful constructive extension and experimental-interface observation, not a
substantiated claim of historical novelty. Ordinary adaptation of the published
method appears to deliver essentially the same operation on these observations.

The distinctive source property is that large shot-to-shot local drift can
coexist with exactly informative paired correlations. The quantitative result
uses the specified local two-design distribution; it does not cover every
possible drift law. The negative finding is
equally concrete: independent unheralded corruption of Bell outcomes destroys
the exact kernel. No general constant-noise robustification is established.

## Experimental input, including what is not acquired

There are n physical qubits and one fixed, unknown Clifford U. On shot t the
source draws independently Haar-random pure single-qubit states
|psi_(t,1)>,...,|psi_(t,n)> and produces **two preparations with the same draw**:

    U (tensor_i |psi_(t,i)>)  tensor  U (tensor_i |psi_(t,i)>).

Different shots have independent draws. The learner receives both registers
on an ordinary programmable Clifford processor, whose elementary gate and
measurement calls are charged. In particular it can perform the usual pairwise
physical Bell measurement and execute the acquired decoder. This standard
Clifford instruction set is supplied; the unknown decoding circuit is acquired.
The same processor is available to the conventional comparator. The learner does not
receive a classical description or preparation key for the latent local
states. The learner's own random seed is not being hidden from a comparator.
The absence of that classical key is part of the source access model.

Haar randomness can be replaced exactly by independent uniform choices among
the six Pauli eigenstates: these have the same two-copy average. Consequently
the source is not being credited with magic states or general quantum
computational power. It is a correlated preparation source with a hidden
Clifford frame.

This source does not clone an arbitrary supplied state: it makes two
preparations from a shared classical preparation choice. Such paired access
must be physically present; two independent samples of the averaged density
matrix are insufficient. No claim is made that a single nonresettable physical
specimen can provide these pairs. Bell gate errors must be absent, heralded,
or small enough for the explicit coupling bound below.

The output is a classical description of a Clifford decoder V and n logical
qubit factors, up to factor permutation and independent single-qubit Clifford
frames. This decoder also factorizes every subsequent state of the form

    rho = U (tensor_i rho_i) U^dagger,

regardless of the rho_i. The common hidden-frame promise for subsequent states
is an assumption about the source family; it cannot be certified for arbitrary
unobserved future preparations from the calibration record.

## Proposition 1: single-copy observations contain no frame information

For any U, averaging one register over the latent draws gives I/2^n. Hence any
number of independent one-register preparations, even with arbitrary collective
measurements, has the same density matrix for every U. It cannot identify the
hidden factors.

This is an information contrast between paired and unpaired input sources. It
is **not** a comparison against a conventional method that receives the same
pairs. The strongest same-pair comparator can use all the information below.

For one latent qubit, the paired average is

    E[|psi><psi| tensor |psi><psi|] = (I + SWAP)/6 = P_sym/3.

One way to verify the identity without integrating is to average the six Pauli
eigenstates. The identity and pairwise Pauli second moments agree with
(I+SWAP)/6. Its Bell outcome is uniform over the three triplet states, and the
singlet never occurs. The n-factor paired source has this law independently
on each hidden factor before applying U to both registers.

## Proposition 2: an explicit classical observation law

Use interleaved Pauli coordinates (x_1,z_1,...,x_n,z_n) in F_2^(2n), and let J
be the block diagonal matrix with n copies of [[0,1],[1,0]]. In standard Bell
coordinates the singlet is (1,1). Define

    D = {(0,0),(1,0),(0,1)}.

The observed Bell label Y has the law

    Y = S X + a,    X uniform on D^n,

where S is symplectic, S^T J S = J, and a is a fixed affine shift determined
by U and the Bell convention.

Justification of the affine action: U tensor conjugate(U) permutes the Bell
basis by the symplectic action of U. For a Clifford U, U U^T is a Pauli up to
phase. This holds for the Clifford generators and is preserved under
multiplication: if V V^T is Pauli then U(V V^T)U^T is the product of a
Clifford-conjugated Pauli and U U^T. The difference between U tensor U and
U tensor conjugate(U) is therefore a Pauli translation of Bell labels.

Only S is needed for the tensor decomposition. The affine shift corresponds
to Pauli-frame information and does not alter the factor subspaces.

## Proposition 3: exact low-degree structure and its sample cost

Let Q_2 be the vector space of squarefree Boolean polynomials of degree at most
two in 2n variables, including constants. Its dimension is

    D_2 = 1 + 2n + choose(2n,2) = 2n^2+n+1.

The subspace of polynomials that vanish on D^n is exactly

    K = span{x_i z_i : i=1,...,n},

and has dimension n.

Proof: evaluation at zero forces the constant coefficient to vanish.
Evaluation at each coordinate vector forces every linear coefficient to
vanish. Evaluation at the sum of two coordinate vectors from different
factors forces every cross-factor quadratic coefficient to vanish. The only
remaining quadratic terms are x_i z_i, which indeed vanish. An invertible
affine map preserves the space of Boolean degree-at-most-two functions, so the
observed law also has an n-dimensional quadratic vanishing space.

Every nonzero class in Q_2/K is nonzero on at least 1/9 of D^n. More generally,
every nonzero reduced polynomial of degree at most k on D^n is nonzero with
probability at least 3^(-k). A reduced polynomial has no x_i z_i factor. If it
depends on block i, write it as A+x_i B+z_i C, where at least one nonzero B or
C has degree at most k-1. For every remaining input where that coefficient is
nonzero, the three evaluations A, A+B, A+C cannot all vanish. Induction gives
3^(-k). If the polynomial does not depend on the selected block, remove that
block and continue. A nonzero constant has probability one. For k=2 the bound
is 1/9 and can be attained by the product of two one-block point indicators.

Construct the m by D_2 evaluation matrix whose rows contain 1, the coordinates
of Y, and all squarefree pair products. Its nullspace contains the true K. A
false polynomial class survives all m observations with probability at most
(8/9)^m <= exp(-m/9). There are at most 2^(D_2-n)-1 nonzero classes, so

    Pr[empirical kernel differs from true kernel]
      <= 2^(2n^2+1) exp(-m/9).

In particular it suffices that

    m >= 9[(2n^2+1) ln 2 + ln(1/delta)].

This charges 2m prepared n-qubit registers and m Bell measurements, each using
O(n) pairwise elementary Clifford gates and measurements. It is polynomial,
not an uncharged exponential support enumeration. The raw record has O(mn)
classical bits. A naive dense F_2 elimination takes O(m D_2^2) bit operations;
better bit packing is possible but is not needed for polynomiality. The
prototype uses exact uint8 parity arithmetic; no continuous numerical
conditioning or estimated singular-value gap enters.

## Proposition 4: explicit recovery of the factor subspaces

For a quadratic q, write B(q) for its polar matrix: B is alternating and its
off-diagonal entries are the squarefree quadratic coefficients. Define

    T(q) = J B(q).

For the canonical q_i=x_i z_i, T(q_i)=P_i is the rank-two coordinate projector
onto the ith factor. Under the observed affine symplectic change of variables,

    B(q_i') = S^(-T) B(q_i) S^(-1),
    T(q_i') = S P_i S^(-1).

The linear and constant parts introduced by the affine shift disappear upon
polarization. The span of the T(q_i') is a Boolean algebra: every element is
idempotent, all elements commute, and the primitive idempotents are the n
rank-two projectors S P_i S^(-1).

An explicit decomposition avoids searching the 2^n elements of this algebra.
Start with W=F_2^(2n). For each basis matrix T of the acquired algebra, split
each current invariant subspace W into

    ker(T restricted to W) direct-sum im(T restricted to W).

Idempotence gives the direct sum. Commutativity preserves the subspaces already
constructed. Since a basis spans all coordinate projectors, distinct primitive
factors have distinct joint eigenvalue patterns. At termination there are
exactly n two-dimensional subspaces W_i=S span(e_i,f_i).

The symplectic form is nondegenerate within each W_i and vanishes between
different W_i. Any ordered independent pair in W_i has pairing one over F_2.
Concatenating these pairs produces a symplectic matrix S_hat whose inverse
decodes the hidden factors, up to local symplectic transforms and permutation.
This splitting requires only polynomial-size linear algebra. It does not
assume a supplied solver for the physical many-body system.

The implementation checks kernel dimension, idempotence, commutation, the
dimensions of the joint eigenspaces, and symplecticity. These checks are useful
failure detectors. For arbitrary source misspecification they do not establish
that a finite record certifies the promised source model.

## Proposition 5: the acquired representation is executable

The code emits at most 4n symplectic transvections whose action is S_hat^(-1).
A transvection with vector v acts as

    T_v(x) = x + [v,x] v.

It is realized, up to irrelevant Pauli phases, by a pi/4 rotation about the
Pauli labeled by v. One such rotation compiles to O(n) elementary Clifford
gates using single-qubit basis changes and a parity accumulation. Thus the
decoder has an O(n^2)-gate implementation. This is an actual construction of
the learned operation, not just an existence claim about a change of basis.

For completeness, the sequential reduction used in code is constructive.
Suppose earlier symplectic pairs are fixed. To map the next current first
column a to the target e: if [a,e]=1, use T_(a+e). Otherwise, if a differs
from e, choose w in the remaining symplectic complement with [a,w]=[e,w]=1
and use T_(a+w), T_(w+e). Such w exists because a and e are distinct nonzero
vectors, and can be found by two linear constraints. To map the second column
b to f while fixing e, use T_(b+f) when [b,f]=1. Otherwise use intermediate
w=e+f and T_(b+w), T_(w+f). These transvections fix e because [e,b]=[e,f]=1.
All transvection vectors stay in the complement of previously fixed pairs.
At most four transvections are used per pair. The code verifies the resulting
product is exactly the desired inverse over F_2.

## What later calculations this actually enables

The decoder addresses a representation bottleneck: future states in the same
hidden product family can be decoded into individually measurable factors.
Then ordinary local tomography can acquire their product descriptions. This
supports reusable operations including global Pauli expectations, entropies,
purities, fidelities between two such product states, and response calculations
under Hamiltonians verified to be local in the decoded factors. Larger fixed
blocks would replace single-qubit algebra by small-block algebra, but the
present proof and implementation concern single-qubit factors.

Each later operation must pay for its own local parameter acquisition and
precision. In particular the calibration source does not reveal the rho_i of
a later preparation, nor any unknown subsequent Hamiltonian. It does not make
arbitrary physical-basis measurement sampling, arbitrary interacting dynamics,
postselection, or generic tensor-network contraction efficient. A concise
Clifford-times-product description can still lead to hard measurement
distributions. No universal classical many-body simulator is claimed.

If a later Hamiltonian is supplied as an explicit Pauli list, conventional
algebraic analysis of that list may already reveal the same factors without
using the calibration source. A fair downstream comparison must include that
route. The strongest defensible reuse case is decoding fresh members of a
common unknown source family for subsequent factorwise measurement and
computation, not claiming that an explicit new query is intrinsically hard.

## Imperfection: a useful success regime and a real failure

Finite sampling and the specified two-design **shared pure-state drift** are
handled by the construction above. Other drift ensembles require their own
diversity/anticoncentration analysis. Heralded erased shots can be discarded; the
acquisition count must include their cost. If each actual Bell distribution is
within total variation nu of the ideal distribution, coupling gives an added
failure probability at most m nu for m shots. Thus unheralded noise as small
as O(delta/m) can be included in the theorem. This is not constant-noise
robustness.

For any fixed positive uniform contamination probability eta, the population
law has full support on F_2^(2n). Its degree-at-most-two vanishing kernel is
zero. Therefore taking more samples eventually destroys every exact quadratic
constraint, rather than improving the ideal reconstruction. One cannot repair
this by replacing an exact kernel with the same larger-sample exact kernel.

Recovering approximate parity constraints needs a different algorithm and a
different analysis. Related noisy linear-parity and stabilizer-learning
problems have computational barriers, but **this note does not prove an LPN
hardness reduction for the specific ternary-product source**. A blanket claim
that all constant-noise recovery here is LPN-hard would be unjustified. Newer
noise-robust stabilizer methods also need to be included in any further
conventional comparison.

## Executed diagnostic

`python twin_factorization.py` generates synthetic Bell-law observations,
recovers the factors, emits a decoder, and verifies its symplectic action.
The diagnostic uses arbitrary affine shifts, a harmless enlargement of the
subset of shifts physically induced by applying one Clifford to both twins.
The script never constructs a 2^n-dimensional state. Results are saved in
`twin_factorization_results.json`.

Twelve ideal fixtures were run: n=2,4,8,12 and seeds 7,19,31. All recovered the
correct factor subspaces and passed exact decoder checks. The conservative
sample counts at delta=0.01 were 98,248,847,1845 respectively. Three additional
n=8 fixtures used 2% independent uniform corruption. They contained 16,19,19
corrupted labels; all had empirical quadratic kernel dimension zero and were
rejected. These finite diagnostics support the implementation and illustrate
the failure; they do not certify novelty, device performance, or a general
noise theorem.

## Primary sources and exact comparison

1. Gerard Aguilar, Sofiene Jerbi, Jens Eisert, Lennart Bittel,
   *Efficient learning of Clifford disentanglers and typical t-doped unitaries
   with exponentially more T gates*, arXiv:2609.27565v1, 23 September 2026.
   https://arxiv.org/html/2609.27565v1
   Relevant sections: 2.1 quadratic Bell symmetries; 3.1 lifted-kernel retrieval;
   4.1 finite-algebra simultaneous block diagonalization; Theorems 2 and 4.
   This is the strongest conventional route and substantially anticipates the
   mechanism used here. Its stated learning source is one fixed pure state,
   with a stabilizer-gap promise. The paired drifting ensemble here permits a
   simpler Boolean-algebra proof, but that difference is not a claim that the
   general method cannot process the same observations.

2. Letian Tang and Thomas Steckmann, *Learning Noise-Robust Stabilizer Structure
   via Bell Sampling*, arXiv:2610.03307, 2 October 2026.
   https://arxiv.org/abs/2610.03307
   Its finder-verifier construction is a necessary comparator for further
   noise claims. The present note used only its abstract; it does not import
   its theorems or claim they solve the hidden tensor problem here.

3. Takanori Maehara and Kazuo Murota, *Algorithm for Error-Controlled
   Simultaneous Block-Diagonalization of Matrices*, SIAM J. Matrix Anal. Appl.
   https://doi.org/10.1137/090779966
   Existing commutant-algebra decomposition already handles numerical common
   block structure when matrices are available. Mere invocation of a learned
   block decomposition is not a new operation.

4. Adrian Chapman and Steven T. Flammia, *Characterization of solvable spin
   models via graph invariants*, Quantum 4, 278 (2020).
   https://quantum-journal.org/papers/q-2020-06-04-278/
   Its line-graph recognition route already earns exact free-fermion structure
   from a supplied Pauli anticommutation graph. That route was considered and
   not promoted as a new learned compiler here.

The older Astra resource was read selectively at commit
cb87e72296824ae2a677ccd337025d02d20cbb0a, beginning at `00_START_HERE.txt`.
No theorem from that repository is a premise of the paired-drift construction.

