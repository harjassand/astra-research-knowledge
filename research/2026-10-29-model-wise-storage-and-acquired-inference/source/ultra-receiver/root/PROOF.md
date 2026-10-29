# A stationary-state receiver for a full logical qubit

29 October2026. Root construction, under active independent peer challenge.
This is a conditional quantum-information receiver. It does not itself prove
the static quantum Peierls estimate, generator locality, a microscopic bath,
or efficient physical encoding. The proof uses ordinary CPTP contraction,
logical Pauli twirling and Gibbs calculus; historical novelty is UNKNOWN.

## 1. Exact algebra and positive encoding

Let H be finite dimensional. Supply Hermitian unitaries O_X,O_Z with
O_X O_Z=-O_Z O_X and let O_Y=i O_X O_Z. This is an exact M2 algebra, hence
there is a unitary identification U:H->C2 tensor K taking O_alpha to the
ordinary logical Pauli matrices tensor I. Supply a faithful density matrix rho.
Define the logical twirl

    sigma=(rho+sum_(alpha=X,Y,Z) O_alpha rho O_alpha)/4
         =U^dagger[(I2/2) tensor tau]U,
    tau=Tr_C2(U rho U^dagger).

The encoder and decoder are actual CPTP maps

    Enc(omega)=U^dagger[omega tensor tau]U,
    Dec(a)=Tr_K(U a U^dagger).

Thus Dec Enc=id exactly. No product form of rho itself is assumed. In a
stabilizer application these O_alpha must be the exact corrected logical
Paulis of ONE shared syndrome decoder. Their implementation and preparation
of tau are separate resource contracts; a mathematical map is not a native
initializer.

## 2. Stationarity gives a fidelity receiver without reversibility

Let T_t be any finite-dimensional CPTP semigroup, with T_t(rho)=rho. Write
L* for its Heisenberg generator and use the GNS norm

    ||A||_rho^2=Tr rho A^dagger A,
    epsilon=||sigma-rho||_1,
    delta_alpha=||L*(O_alpha)||_rho.

Unital complete positivity gives T_t*(A)^dagger T_t*(A)<=T_t*(A^dagger A).
Taking rho expectation and using stationarity proves GNS contraction. Hence

    ||T_t*(O_alpha)-O_alpha||_rho <= t delta_alpha.

For the decoded qubit channel Lambda_t=Dec T_t Enc, its entanglement fidelity
with the identity channel is the exact Pauli expression

    F_e(Lambda_t)=1/4 [1+sum_alpha Tr sigma O_alpha T_t*(O_alpha)].

The trace in this expression is real because sigma commutes with O_alpha.
Replacing sigma by rho changes each term by at most epsilon, since
||O_alpha T_t*(O_alpha)||<=1. Cauchy--Schwarz in the rho inner product then
proves the receiver

    F_e(Lambda_t) >= 1-[3 epsilon+t sum_alpha delta_alpha]/4.       (1)

Here F_e is initially the maximally mixed entanglement fidelity. The
independent retained peer supplied the following conversion, checked by root.
For any logical d-dimensional CPTP channel with Kraus operators A_k, center
B_k=A_k-Tr(A_k)I/d. Variance is invariant under that scalar shift, so

    1-F_e(omega,Lambda)=sum_k Var_omega(B_k)
       <=sum_k Tr B_k^dagger B_k
        =d[1-F_e(I/d,Lambda)].

For d=2 and e_t=[3 epsilon+t sum delta_alpha]/4, EVERY purified logical
input therefore has fidelity at least1-2e_t. The pure-state trace-distance
bound then gives ||Lambda_t-id||_diamond<=2 sqrt(2e_t), capped by2.
This supplies the explicit worst-case/reference conversion; (1) alone was
not already a statement of every-input entanglement fidelity.

This does not assume that L is self-adjoint in any detailed-balance inner
product, that its logical channel is Pauli diagonal, or that rho is diagonal
in syndrome sectors. It does require EXACT stationarity and a bound on the
FULL generator L*O, including its Hamiltonian part. A small dissipative
Dirichlet form alone would not control coherent logical rotation.

## 3. A Gibbs commutator pays the logical-twirl cost

Now let rho=e^(-beta H_g)/Z, beta>0, and define

    h_alpha=||[H_g,O_alpha]||_rho.

Duhamel's formula gives

    [O,sqrt(rho)]=-(beta/2) integral_0^1
       rho^(s/2) [O,H_g] rho^((1-s)/2) ds.

If K=[O,H_g], then K is anti-Hermitian. In a rho eigenbasis |K_ij|=|K_ji|.
Weighted AM--GM therefore proves, for0<=s<=1,

    sum_ij rho_i^s rho_j^(1-s)|K_ij|^2
       <=sum_ij rho_j |K_ij|^2 = h_alpha^2.

Thus ||[O,sqrt(rho)]||_2<=(beta/2)h_alpha. Factoring the difference of the
two positive squares and using Holder gives

    ||rho-O rho O||_1 <=2||sqrt(rho)-O sqrt(rho)O||_2
                      <=beta h_alpha.

Consequently

    epsilon <= (beta/4) sum_alpha h_alpha.                         (2)

No inverse minimum eigenvalue of rho, volume-dependent condition number,
or modular-time locality oracle enters this estimate. The Duhamel identity's
overall sign has no effect on the norm inequality.

## 4. Decoder-stable local algebras control arbitrary coherent jumps

For each native support X and logical O_alpha, supply an orthogonal projector
P_good^(alpha,X) such that

    [O_alpha,A_X] P_good^(alpha,X)=0

for EVERY operator supported on X. Define p_(alpha,X)=Tr rho(I-P_good).
This is an actual decoder-stability hypothesis, not inferred merely from
code distance or from a passing trajectory. Linearity can establish it from
the full local Pauli algebra, without summing Pauli coefficient norms.

For every such A_X,

    ||[O_alpha,A_X]||_rho <=2||A_X|| sqrt(p_(alpha,X)).             (3)

Indeed the commutator has a right P_bad factor and its square is bounded
above by4||A_X||^2 P_bad. This remains true for a coherent rho.

Write the actual Heisenberg generator as

    L*(O)=i[K,O]+sum_a (L_a^dagger O L_a
                       -(1/2){L_a^dagger L_a,O}).

If L_a is supported on X, the EXACT identity

    D_(L_a)*(O)=L_a^dagger[O,L_a]+(1/2)[L_a^dagger L_a,O]

uses only commutators of operators on the SAME support X. Since L_a^dagger
L_a is also supported on X, (3) yields

    ||D_(L_a)*(O_alpha)||_rho
       <=3||L_a||^2 sqrt(p_(alpha,X)).                            (4)

This avoids a faulty estimate which would move an uncontrolled L_a through
rho or silently replace one coherent jump by independent Pauli jumps.

If K=H0+sum_X K_X with [H0,O_alpha]=0, then

    delta_alpha <=2 sum_X ||K_X|| sqrt(p_(alpha,X))
                   +3 sum_a ||L_a||^2 sqrt(p_(alpha,supp L_a)).    (5)

Likewise (3) bounds h_alpha when H_g=H0+sum_X V_X. K may include an admitted
coherent correction in addition to H_g. Stationarity of the resulting full
generator is a separate premise, never inferred from its local appearance.

Combining (1),(2),(5) turns a static rare-bad-projector bound into an explicit
entanglement-fidelity bound for ALL qubit inputs and their entanglement.
For bounded per-site Hamiltonian/jump strengths and p_bad<=poly(n)e^(-c n^a),
the receiver yields an exponentially long (in n^a) memory interval, with a
possibly halved exponent and polynomial prefactors. This consequence remains
CONDITIONAL on the actual static estimate and generator admission.

## 5. Quasilocal jumps retain their cross terms

If a jump L has a local approximation L_R with ||L-L_R||<=r_R, it is NOT
legitimate to replace D_L by a sum of dissipators of its support pieces.
Instead for ||O||<=1 use the operator-norm bound

    ||D_L*(O)-D_(L_R)*(O)|| <=4||L|| r_R+2 r_R^2.                 (6)

Apply (4) to the full local approximation L_R and add (6). Similarly a
Hamiltonian truncation costs at most twice its omitted norm. The chosen
radius, decoder stability for that whole support, jump-integral weights,
number of terms and tail constants must ALL be paid. An exact weak-coupling
Davies spectral component for a noncommuting H is not automatically local.

Established quasi-local exact Gibbs samplers are relevant candidate model
classes, not already qualified microscopic baths. For example the primary
Chen--Kastoryano--Gilyen construction arXiv:2311.09207 states exact detailed
balance and quasilocal lattice jumps. Its actual coherent correction,
frequency integrals and tail bounds would have to be checked against (5)--(6).
No rapid mixing or efficient memory initialization is inferred from the name
'efficient Gibbs sampler'; its mixing time can be the long memory timescale.

## Research scope

The root proof above was constructed directly. Its ordinary ingredients are
not claimed new. An independent retained peer is checking the full encoding,
normalizations, GNS/Duhamel estimates and local-jump support logic. The active
RX/RZ researcher owns the separate static quantum Peierls construction.
Neither source correctness nor a physical memory is established by this
receiver alone. No finite numerical example is needed for these identities.
