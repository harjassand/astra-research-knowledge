# Removing the spectral compiler from the bath coupling

29 October 2026. NEW construction under challenge. The accepted all-cold
circuit packet is frozen. No physical bath, quantum state, new Hamiltonian
instance or dynamics is executed here.

The operation sought is conditional-clock preparation. A replacement
controller may have the same Gibbs target and a useful gap without having
the exact same short-time trajectory as the rank-one algorithmic controller.
That distinction matters for stationary reservoirs.

## 1. Bare local seeds suffice; vacuum dressing can be proof-only

Let H=N+lambda V be the conditional gauged clock Hamiltonian, with its
known small-coupling uniform ground gap. The accepted exact ground frame
W has

    K=W H W^*-E=N+D,  ||D||_local=O(lambda),
    (1-a)N<=K<=(1+a)N, a<=1/4.

Choose the BARE conditional-frame onsite Hermitian seed
A_j=a_j+a_j^*, rather than W^*A_jW. In the vacuum frame it is

    Abar_j=W A_j W^*=A_j+O(lambda)

in every fixed spatial moment, with temperature-independent tails. The
fixed negative band filter therefore gives L_j,-=a_j+O(lambda). It still
annihilates the exact product vacuum because its energy support is strictly
negative. Thus G_--N has O(lambda) interaction tails and annihilates the
vacuum. The same vacuum-CP martingale yields

    (1-b)N<=G_-<=(1+b)N, b<=1/4

at a potentially smaller FIXED lambda gate. Every subsequent positive-sech,
parent-coercivity and stability step of ALL_COLD.md is unchanged. Hence the
all-cold parent gap applies to bare local seeds as well. W is a proof device,
not an external Hamiltonian-dependent seed compiler or implemented unitary.

This paragraph concerns the conditional GAUGED Hamiltonian H. For the actual
ungauged two-body Pauli-clock endpoint, a syndrome-preserving coupling is
the fixed-prefix pullback U^* A_j U. Its support/body order/spatial range
are bounded independently of n, but it is generally not an onsite or
two-body system-bath coupling. It is specified by the local prefix Pauli
table, not by the many-body spectrum. Independent onsite clock baths can
change corrected source syndromes; they cannot silently replace it.

The physical realization of these constant-body local couplings remains a
separate resource gate. The storage Hamiltonian is two-body; this text does
not assert the full preparation controller is two-body.

## 2. Positive time-translation averaging NEVER loses the parent gap

Suppose a KMS generator L for H has Gibbs state sigma and Hermitian parent

    P >= g(I-|sqrt(sigma)><sqrt(sigma)|).

For any probability measure mu on real s, conjugate L by system time
translations and average. The resulting generator is GKLS and has the
same stationary sigma. In doubled Hilbert space its parent is

    P_mu=integral U_s P U_s^* dmu(s),
    U_s=exp[is(H tensor I-I tensor H^T)].                 (1)

Since U_s sqrt(sigma)=sqrt(sigma), averaging the displayed operator
inequality gives EXACTLY

    P_mu>=g(I-|sqrt(sigma)><sqrt(sigma)|).                (2)

No locality, spectral separation, numerical fixture or optimization is used
in this gap-preservation principle. Ordinary complete positivity and
operator order supply it. The new input is the acquired weak-product gap.

For the band-filtered generator, the Gaussian measure

    dmu_T(s)=exp(-s^2/T^2)ds/(sqrt(pi)T)

multiplies the jump coefficient between frequencies omega,omega' by
exp[-T^2(omega-omega')^2/4]. It multiplies the canonical tanh coherent
coefficient by the same factor. Therefore EVERY finite Gaussian coarse
average has the same gap lower bound, independently of T. The infinite
time average deletes unequal-frequency cross terms and B; it is the usual
Davies generator with local coupling operators A_j and rates |h_b(omega)|^2.
This proves its FORMAL gap, not the physical validity/rate of a Davies limit.

An exact rank-one band controller is generally not time-translation
covariant. Already in the product reference, L=a+exp(-b/2)a^* has the
phase-sensitive terms exp(-b/2)(a rho a+a^*rho a^*). A stationary-bath
Davies limit omits these cross-frequency terms. Thus we use the averaged
preparation operation instead of claiming identical microscopic trajectories.
This is not a no-go for finite-coarse-grained physical thermalization.

## 3. A strong EXISTING microscopic mechanism matches the finite average

[Scandi--Alhambra, PRX16,011040(2026)](https://doi.org/10.1103/sfp3-3sqf),
[arXiv2505.20064](https://arxiv.org/html/2505.20064), Theorem15, already derives
the Gaussian-averaged KMS rates

    gamma_(omega,omega')=exp[-T^2(omega-omega')^2/4]
                       ghat(-omega)ghat(-omega'),
    S_(omega,omega')=i tanh[b(omega-omega')/4] gamma

from a microscopic Gaussian thermal bath, with a renormalized system H*.
For independent baths choose C_hat(-omega)=|h_b(omega)|^2. Then their
ghat(-omega)=h_b(omega), and the effective generator is exactly the finite
average above, evaluated at H*. This physical coarse-graining mechanism is
PRIOR, not an invention of this packet. It avoids a rotating-wave or
smallest-Bohr-gap assumption, and its trace error grows linearly in time.

Their exact hypotheses include initially factorized system/bath state,
thermal Gaussian bath/Wick correlations, zero bath mean, and finite absolute
correlation/square-root-correlation moments Gamma0,Gamma,tau0,tau,K0,K.
Their paper explicitly notes that these infinite-time moments require an
infinite reservoir. A finite hardware bank is not admitted merely by citing
that theorem. Finite bath replacement, thermal initial-state acquisition,
local geometry, and coefficient precision are being separately investigated.

## 4. Lamb renormalization can be handled globally at polynomial bath coupling

Use b for inverse temperature, u for rescaled dissipative evolution time,
and alpha for the microscopic system-bath coupling. Their physical time
is u/alpha^2. The data Hamiltonian's lambda is NOT changed with volume.
From the time-domain Lamb-shift formula and ||A_j||<=1,

    ||H*-H|| <= alpha^2 Gamma0/2.                        (3)

We need not assume this small but increasingly spread correction passes
an N-uniform local-interaction threshold. Instead pay its GLOBAL norm.
The band parent has a polynomial operator-norm Lipschitz modulus that
does not involve Gibbs condition numbers. Let C0(b),C1(b) bound the time
filter L1 and first absolute moments of BOTH h_b and its symmetrized q_b.
They are explicit polynomials in b by the existing scalar-filter proof.
For m seed operators and delta=||H'-H||,

    ||P(H')-P(H)||
       <=m[8 C0 C1+2b C0^2]delta,
    ||P(H)||<=2m C0^2.                                  (4)

Indeed filtered jumps change by at most2 C1 delta. The normalized sech
kernel has first absolute moment<=b; Duhamel then controls its change in
the loss term. The tensor jump products use the same elementary product
bound. All imaginary-time factors have already canceled before this estimate.

Gaussian averaging also changes its conjugating Hamiltonian, but this adds
only4T delta||P(H)|| because E_mu|s|=T/sqrt(pi)<=T. Consequently

    ||P_T(H')-P_T(H)||
       <=m[8 C0 C1+2b C0^2+8T C0^2]delta.               (5)

For the source's observation window T=O(poly(n,b)/alpha), equations(3)--(5)
are O(alpha poly(n,b)). Thus inverse-POLYNOMIAL bath coupling alpha is
enough for ordinary Weyl stability of the already constant parent gap.
There is no need to resolve close Bohr frequencies or to apply the weak
product theorem anew to H* with a potentially bad local norm.

Their Theorems11,13,17 bound microscopic/coarse-graining/renormalization
errors with the same polynomial bath moments and inverse powers of T;
Theorem18 gives ||sigma_H*-sigma_H||_1<=alpha^2 b Gamma0.
Composing these bounds at u=O(n(1+b)+log(1/epsilon)) is the proposed route
to a polynomial-time microscopic preparation theorem. Its full resource
receiver, finite reservoir and calibration are NOT yet closed here.

The coherent drift -i[H*,rho]/alpha^2 does not spoil the L2 contraction:
it is anti-Hermitian in the same similarity and fixes sigma_H*. The
dissipative parent lower bound controls the real part. This is a formal
mathematical statement, not a physical Markov approximation by itself.
