# Acquiring a pure-return realization of a known affine stochastic program

31 October 2026. Mathematical construction, pending separate independent review and implementation. This changes a quantum realization while preserving a specified classical process. It does NOT preserve an arbitrary originally supplied quantum dilation, its environment records, or arbitrary coherent source interventions.

## 1. Declared input and preserved task

Input is an explicitly known affine program over GF(2),

    y = F x + G r + b,

with n>=1 state bits, fresh independent fair random bits r at each event, and

    rank [G, F G, ..., F^(n-1) G] = n.

Only the state process is part of the declared source output; the original random tape and dilation environment are private. Events may occur at an independently specified Poisson rate. No unknown transition law is learned. All matrices and their bit dimensions are supplied, and all rank tests below are exact finite binary computations.

Let g=rank G. Compress the redundant random bits to a basis of im G; this preserves the conditional state transition, because G r is uniform on im G. Controllability implies g>=1 and rank[F G]=n: a row annihilating F and G would annihilate the whole controllability matrix. Hence the uniform distribution is stationary. After n events, the random contribution has full support and is uniform, so P^n is the uniform-reset stochastic matrix. Affine offsets do not change these rank statements.

The goal is a polynomial-size Clifford Stinespring realization of exactly this P whose quantum channel has the stronger property Phi^n=Reset_(|+>^n), rather than merely diagonal mixing.

## 2. Exact reverse fibres and their feedback freedom

Choose a full-row-rank quotient matrix R with kernel im G, and set H=R F. H has n-g independent rows: if u H=0, the row uR annihilates both F and G, hence is zero; R has independent rows, so u=0.

Choose an n by n matrix A0 with H A0=R (for example, a right inverse of H multiplied by R), and an n by g basis matrix B for ker H. With the uniform stationary law, the reverse transition from y samples uniformly from

    x = A0 y + B z + A0 b,       z uniform in GF(2)^g.

Indeed these are exactly the solutions Hx=R(y+b), with unique z for each solution. For every g by n matrix L, replacing A0 by A=A0+B L leaves H A=R. Thus

    x = A y + B z + A b

has the SAME reverse conditional law. The feedback is a change in how private random bits select a point in a fibre, not a change in the Markov transition matrix.

The pair (A0,B) is controllable. One short finite proof uses the already established uniform stationary law: the reverse stochastic matrix is P^T, so its nth power is also uniform reset. Iterating its displayed affine update has random support equal to the image of [B,A0B,...,A0^(n-1)B]. Uniform reset forces that image to be all GF(2)^n. This argument uses no spectral or asymptotic mixing assumption.

## 3. Polynomial deadbeat feedback, proved over GF(2)

Write b1 for the first, nonzero column of B. Construct independent vectors v1,...,vn as follows. Set v1=b1. Given v1,...,vi with i<n, choose u_i from the finite list 0,e1,...,eg such that

    v_(i+1)=A0 v_i+B u_i

lies outside their current span S_i. Such a choice always exists. If every candidate lay inside S_i, subtraction of the zero candidate would put every column of B in S_i. The previous recurrences would then imply A0 v_j in S_i for j<i, and the zero candidate gives this also for j=i. Thus S_i would be a proper A0-invariant subspace containing im B, contradicting controllability.

Put u_n=0, T=[v1 ... vn], U=[u1 ... un], L0=U T^(-1), and A1=A0+B L0. Then A1 v_i=v_(i+1) for i<n. Consequently T is the cyclic controllability matrix [b1,A1 b1,...,A1^(n-1)b1]. All choices require only polynomially many rank tests.

Define

    w=e_n^T T^(-1), k=w A1^n,
    L=L0+e1 k, A=A0+B L=A1+b1 k.

Here e1 in L has g coordinates. To prove nilpotence without any assumption about an infinite field, let O have rows w A1^j for 0<=j<n. The product O T has zero entries whenever row index plus column index is less than n-1 and has ones on that anti-diagonal. Thus O is invertible. Moreover w A1^j b1=0 for j<n-1 and equals 1 for j=n-1. Therefore multiplying each row of O by A shifts it to the next row, except the last row, which becomes

    w A1^n + k = 0.

It follows that O A O^(-1) is the nilpotent shift and A^n=0. This is the ordinary cyclic-reduction/deadbeat feedback construction, here checked directly in characteristic two. Independently verify H A=R, A^n=0 and all matrix ranks before emitting a certificate.

## 4. Acquired reversible fibre circuit and orientation

The n by (n+g) matrix [A B] has full row rank. Applying H maps its A columns onto im R=GF(2)^(n-g), while the B columns span ker H. Complete these n rows to an invertible (n+g) by (n+g) matrix M using binary elimination. Define the affine inverse circuit by

    (x,r_new) = M (y,z) + (a,0),     a=A b,

whose first n output bits are x=A y+Bz+a. Let U be its inverse permutation. An explicit CNOT/SWAP network and X translations implement U in polynomial size by reversible binary elimination. The arbitrary remaining rows of M are private-environment conventions, not extra physical assumptions.

For a fixed x, feed U a uniform g-bit r_new. Each allowed y in F x+b+im G occurs exactly once: Hx=R(y+b) is the necessary and sufficient fibre condition, and the full-column-rank B then determines a unique z. Thus the FORWARD transition is precisely the original affine program, not its time reversal. Original redundant random bits have only been reparameterized privately.

For the quantum source, initialize these g environment qubits in |+>^g, apply the same affine permutation U, and discard its environment output z. If the frontend expects |0> ancillas, include g actual Hadamards in the program. No amplitude oracle is supplied implicitly.

## 5. Exact quantum return and phase-safe reference

The Kraus operator labelled by the discarded z is

    K_z = 2^(-g/2) sum_y |y><f_z(y)|,
    f_z(y)=A y+Bz+a.

This formula remains valid when f_z is not injective; the full affine permutation guarantees that (y,z) has a unique input pair. After n events, composition of the inverse maps has linear part A^n=0. Hence for every environment word z_1,...,z_n its Kraus product is

    2^(-ng/2) sum_y |y><x_root(z_1,...,z_n)|.

Every such branch has output proportional to |+>^n. Trace preservation of the full channel therefore proves, on every source/reference input,

    Phi^n(rho_SR)=|+><+|^n tensor Tr_S(rho_SR).

Equivalently, each root occurs equally often; this also follows from controllability, but is not needed as a separate normalization assumption. There are no hidden Pauli signs: U is an affine computational-basis permutation with positive unit entries.

The pure fixed state is psi=|+>^n. Since U preserves the uniform superposition on all n+g bits, its actual Stinespring satisfies W psi=psi tensor |+>^g exactly. Thus c=|+>^g with its correct circuit phase, preparation and reflection are explicit, and m=n is a full-input return certificate. Running the existing raw Clifford finder/verifier on this emitted circuit provides an independent finite check; mathematical validity does not depend on a lucky test outcome.

## 6. Preserved classical controlled process, not arbitrary quantum replacement

For every diagonal source observable diag(f), the new adjoint channel obeys

    Phi^dagger(diag(f)) = diag_x E_r f(Fx+Gr+b).

The same identity holds with system-operator-valued diagonal entries. A Hamiltonian controlled by source labels, sum_x |x><x| tensor B_x, preserves that algebra under its commutator, including when the B_x do not commute with one another. Backward composition therefore preserves the full system process and public source-label statistics for any initial classical source law and outcome-retaining prescribed interventions whose adjoints preserve this algebra. Rates and event timing are unchanged. Arbitrary nonstationary classical laws may be supplied by their actual sampler; no coherent square-root preparation is required for that interpretation.

This does NOT equate the new quantum source to a previously supplied dilation on coherent source inputs, to arbitrary quantum source controls or outputs, to disclosed original random bits, or to disclosed simulator emission timestamps. The accepted arbitrary-source-input compiler can simulate the newly chosen quantum realization as its own task, but it cannot be used to claim those stronger classical replacement equivalences.

The distinction is already visible for x'=x xor r on one bit. A direct CNOT from a |+> environment to the source gives Phi(rho)=(rho+X rho X)/2 and retains X information forever, although its classical transition is immediate uniform reset. The construction above may choose A=0, B=1 and a SWAP realization, giving Reset_|+>. These have identical classical state kernels but different coherent-source channels. Repairing the classical task is legitimate; replacing an arbitrary quantum task is not.

## 7. Receiving and limits

The acquired program now has the inputs of the accepted pure-return compiler without a supplied exponential state table or guessed stationary state. Source acquisition, the deadbeat feedback, circuit synthesis and exact certificate checks cost polynomial(n, number of supplied random bits, input length). The emitted circuit uses n+g bits and polynomially many gates; m=n. Source-only stabilizer expectations and future sparse-Pauli centering use the separately reviewed consumer interface.

A future coupling still needs an actual acquired circuit and exact or independently certified centering. The uniform stationary expectation of an arbitrary Boolean-program output is not obtained for free. Nontrivial mean Hamiltonians retain their real square-root-rate action; the existing identity-phase exception remains unchanged. No claim about unknown-source learning, arbitrary finite-state nonlinear programs, classical hardness, or practical advantage follows.

## 8. Ordinary primary comparison and access boundary

The multi-input-to-cyclic-input reduction and pole assignment are established control theory. [Heymann's 1968 primary correspondence, Comments on Pole Assignment in Multi-Input Controllable Linear Systems](https://csaws.cs.technion.ac.il/~heymann/Heymann%27s%20papers/Pole%20Assignment%20in%20Multi-Input%20Linear%20Systems.pdf) states and constructively proves the cyclic feedback lemma in its real-matrix setting. The proof above checks the specific finite-field algorithm directly rather than transferring real spectral arguments silently. Binary elimination, affine reversible circuits and stabilizer simulation are ordinary acquired tools; [Aaronson–Gottesman](https://arxiv.org/abs/quant-ph/0406196) is the existing primary stabilizer comparator.

An independently located NASA record titled 'Controllability and pole assignment for discrete time linear systems defined over arbitrary fields' was bibliographically relevant, but its page https://ntrs.nasa.gov/citations/19710042768 returned 403. It was not retried and no alternate copy was sought. Its theorem is not used as evidence. No novelty conclusion is drawn from this bounded comparison.

The prospective scientific operation is a verified realization-synthesis frontend: modify inaccessible coherence while retaining the entire declared classical diagonal process, thereby acquiring a certificate that a naive dilation can fail. This is more than assuming a mixing promise, but remains a known-program compiler construction awaiting separate code and conjunction review.
