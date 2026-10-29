# One nominal local controller under unknown energy-conserving coherent errors

29 October 2026. An exact, all-orders positive subcase of the fixed-controller
question. **Arbitrary energy-changing coherent perturbations are not solved.**
The general stationary-observable criterion is ordinary/previous machinery;
this file constructs an explicit strictly local fixed-controller admission
and an unknown coherent error class on the supplied recursive family.

## 1. Nominal data and exact local energy resolution

Take the accepted even RX/RZ family H0=sum_j(I-S_j)/2 with n=n_k physical
qubits, one encoded qubit, check weight <=w, qubit incidence <=D, and the
same corrected logical Pauli algebra O_X,O_Y,O_Z. Use the primary-qualified
geometry and beta>beta_c in the unit-defect-energy convention. All constants
below are independent of k. Let rho0=e^(-beta H0)/Z0.

If A is supported on q qubits, let J(A) be the checks touching that support,
m=|J(A)|<=Dq, and U(A) their union with the native support. Then

    |U(A)|<=q(1+Dw),
    e^(itH0) A e^(-itH0)=e^(itH_A) A e^(-itH_A),
    H_A=sum_(j in J(A))(I-S_j)/2.

Its possible energy differences are integers in [-m,m]. For M=2m+1 and
t_r=2pi r/M, the finite Fourier formula

    A_omega=(1/M)sum_(r=0)^(M-1)
              e^(-i omega t_r)e^(it_r H_A)A e^(-it_r H_A)   (1)

is EXACT: [H0,A_omega]=omega A_omega, A=sum_omega A_omega,
and ||A_omega||<=||A||. Every component has the same bounded support U(A).
For m=0 take A_0=A. This is finite nominal energy resolution, not an
infinite-resolution Davies component of the perturbed Hamiltonian.

In particular the zero-frequency map A->A_0 is an average of unitary
conjugations, is Hermiticity preserving, and contracts the operator norm.
If a globally energy-conserving local V=sum_i V_i satisfies [H0,V]=0, then

    V=sum_i (V_i)_0.                                      (2)

Thus global energy conservation does not require an initially termwise
conserving decomposition. Pinching expands each native support only to its
check neighbourhood and does not increase that term's norm. Its incidence
increases by at most the fixed factor (1+Dw). Formula (1) is a mathematical
local qualification/compiler, not a granted physical averaging actuator.

## 2. One fixed, strictly local nominal thermal controller

For each of the 3n one-site Pauli seeds P, use (1) and set

    gamma_beta(omega)=1/(1+e^(beta omega)),
    D0=sum_(P,omega) gamma_beta(omega) D_(P_omega),
    D_L(rho)=Lrho L†-(1/2){L†L,rho}.                       (3)

All jumps have support at most Q_b=1+Dw, and there are at most 2D+1
frequencies per seed. The controller is selected once from H0, before any
unknown V. It uses bounded per-site rates. Its complete finite-frequency
block G_P has diamond norm at most 2: sum_omega P_omega†P_omega=I by time
averaging P(t)†P(t)=I, so sum_omega gamma P_omega†P_omega<=I. The CP part
and anticommutator part each have diamond norm <=1. This uses the strongest
ordinary block budget, rather than needlessly charging a frequency factor.
A stabilizer-dephasing controller

    Gamma sum_j D_(S_j)

may be added at any finite, size-independent Gamma>=0. It is not needed
for the positive theorem below.

The exact Gibbs relation for [H0,F]=omega F is

    F rho0=e^(beta omega)rho0 F.

Since F†F and FF† commute with rho0, a direct calculation gives

    [gamma_beta(omega)D_F
        +gamma_beta(-omega)D_(F†)](rho0)=0.                (4)

For the Hermitian seed P, P_omega†=P_(-omega). Its frequency family therefore
fixes rho0. Equation (3), the nominal H0 drift, and the stabilizer dephasing
all fix rho0. This is the established commuting-Hamiltonian Davies/heat-bath
construction, with its actual local support and clock paid here.

## 3. Unknown coherent and dissipative errors admitted

Allow ANY unknown Hermitian V=sum_i V_i with:

* original native support size <=q and bounded physical range;
* at most nu supports per qubit and ||V_i||<=v0;
* the single exact structural condition [H0,V]=0.

The strength v0 may be any fixed finite constant; no perturbative smallness
or Zeno limit is used. Neither individual checks nor corrected logicals are
required to commute with V. Equation (2) pays an individually conserving
decomposition on supports of size Q_v=q(1+Dw).

Specify the dissipative-error class explicitly as local nominal-Gibbs-balanced
pairs. One may choose unknown local F, resolve it by (1), and add, at any
allowed nonnegative strength, the paired terms in (4). At omega=0, if F is
not Hermitian use the equal pair (D_F+D_(F†))/2. Coherent superpositions
within a frequency block are allowed. Require the full admitted error-jump
supports <=Q_e and their total square-norm budget <=J_e n, with bounded
local incidence. This is an explicit sufficient class, not all weak Lindblad
perturbations; unbalanced errors are excluded.

The actual storage generator is

    L_V=-i[H0+V,·]+D0+Gamma sum_j D_(S_j)+E.               (5)

Every allowed unknown V and E fixes the SAME rho0. The controller D0,
dephasing strength, corrected decoder, and nominal encoder are independent
of V and E. No adaptation to the actual H0+V or its Gibbs state is used.
The stationary state is generally NOT the Gibbs state of H0+V. Accordingly
(5) is an engineered fixed-controller model, not automatically a physical
thermal bath for the full Hamiltonian.

## 4. All-input memory from the ordinary trace/module route

Let Q=max(Q_b,Q_v,Q_e), chi0=ln4+beta D. The accepted source Peierls bound
and same-decoder Pauli-shift union, now at zeta=delta=0, give a COMMON good
projector for every support of <=Q qubits, with

    p_Q<=4 exp(chi0 Q) 2^(-2^(k-1)),
    sqrt(p_Q)<=2exp(chi0 Q/2) exp[-(ln2)2^k/4].             (6)

Precisely, EACH given support X has its own P_good,X, common to every
operator on X and the FULL shared logical algebra X,Y,Z. Its bad probability
has the SAME uniform upper bound p_Q. There is no single projector formed
by a union over all supports; such a union would incur another cost. The
trace estimate below is applied per stationary block and only then summed.

The nominal rho0 exactly factors as I_L/2 tensor tau0 in the corrected
logical representation. The full stationary GNS bound would give a valid
sqrt(p_Q) result. The strongest ordinary Bravyi--Terhal-style trace argument
does better here, because the decomposition consists of INDIVIDUALLY
rho0-stationary local blocks and the good sector covers the FULL support
algebra, including L†L. It must be admitted as a comparator.

Here is an explicit reference-uniform version. For a purified logical input
Psi with reference Schmidt rank r<=2, let

    pi=rho0 tensor I_R,
    B=2Psi_(LR) tensor I_K,
    F=Enc0(Psi)=B pi.

Then ||B||=2. For a common good P of a local block G_X, let Qbad=I-P and
p=Tr rho0 Qbad. Both P and pi commute with B. Full-algebra protection gives

    G_X(BPpi)=B G_X(Ppi)=-B G_X(Qbad pi),                  (7)

because G_X(pi)=0. To see the first identity, commute B across L P and
L†L P separately in every dissipator, and across H_X P in any Hamiltonian
term. This is precisely where a common full-algebra good projector is
stronger than checking a single jump on a separate sector.

Now ||B Qbad pi||_1<=4p and ||Qbad pi||_1=r p<=2p. Triangle inequality
and the diamond norm of G_X imply the safe bound

    ||G_X(F)||_1<=8||G_X||_diamond p.                     (8)

In fact the first norm equals p for these syndrome projectors, but that
sharper constant is unnecessary. This reference-uniform module argument is
an elementary specialization/extension of the ordinary trace proof, not a
claimed new generic memory criterion.

For the decomposition of (5), the nonzero-defect block norm sum is bounded by

    sum_X ||G_X||_diamond <=Jstar n,
    Jstar=2nu v0+6+2J_e.                                 (9)

The first term is the pinched neutral Hamiltonian, the second is the 3n
nominal per-seed blocks of norm <=2, and the third is the admitted balanced
error blocks. H0 and the stabilizer-dephasing blocks fix F EXACTLY and
contribute zero, whatever the finite Gamma. Every included block fixes rho0.

CPTP Duhamel for the FULL actual generator, followed by Dec0, gives

    ||Lambda_t-id||_diamond <=8 Jstar n p_Q t
       <=Kdiamond n t exp[-a2^k],
    Kdiamond=32Jstar exp(chi0 Q), a=ln2/2.                (10)

Here Lambda_t=Dec0 exp(tL_V) Enc0. The trace contraction acts on the local
stationary defects in (8), not on a global arbitrary perturbation norm.
Every purified input has overlap infidelity <=half of (10). Thus

    T_eta,k=eta exp[a2^k]/(Kdiamond n_k)                   (11)

is a rigorous interval with diamond error <=eta and every-purified-input
infidelity <=eta/2, uniformly over the unknown error class. The encoder,
decoder and controller are all selected before those errors. This is exact
at arbitrary finite v0 and Gamma, not a finite-order classical rate plus
an O(nt) approximation remainder.

Using the paid n_k<=5g^(2k), the distance power is alpha0=ln2/(2ln g).
Beyond the onset Kdiamond n_k<=exp[a2^k/4], the interval t<=exp[a2^k/4]
has diamond error <=exp[-a2^k/2]. This interval is at least
exp[c n_k^alpha0], c=(a/4)5^(-alpha0). The stronger exponent relative to
the H-adapted quasilocal model comes from strictly bounded local support
and an individually stationary trace proof. The error class is different
and substantially restricted; this is not a practical tolerance comparison.

## 5. Nontrivial native coherent defect hopping exists

This class is not limited to stabilizer functions. Consider the qubit graph
joining two qubits when they share a check; its degree is at most D(w-1).
On a geodesic of length 3D choose the D+1 centres at positions 0,3,...,3D.
Their radius-one check stars are disjoint. At each centre choose a one-site
Pauli P_i which flips a nonzero number m_i in {1,...,D} of checks. Pigeonhole
gives two centres i,j with m_i=m_j=m. Their physical separation is bounded
by 3D times the supplied check range.

Let J_i be the checks anticommuting with P_i and define

    F_i=P_i product_(a in J_i)(I+S_a)/2.

Then [H0,F_i]=mF_i. For a ground state |g>, F_i|g>=P_i|g> and
F_i†P_i|g>=|g>. The two-star interaction

    V_hop=lambda F_j F_i†+conjugate(lambda) F_i F_j†.       (12)

is Hermitian, exactly energy conserving, and supported on at most
2(1+Dw) qubits of physical diameter at most (3D+2) times the check range.
It maps the one-defect-cluster state P_i|g> coherently to lambda P_j|g>.
It does not commute with the individual flipped checks. Couplings and phases
can be unknown to the fixed controller; ||V_hop||<=2|lambda| pays their
bounded local norm in v0.

The relevant large component of the code eventually has such a geodesic:
a bounded-degree component with diameter <3D has bounded size, whereas the
component carrying the one logical qubit has at least d_seed 2^k sites.
No assumption of independently assignable local syndromes was used in (12).

## 6. The exact boundary of this result

For beta>0, rho0 and H0 have the same commutant. With all other terms in
(5) nominal-rho0 stationary,

    L_V(rho0)=-i[V,rho0]=0 iff [V,H0]=0.                   (13)

No finite stabilizer-dephasing rate changes (11), since D_(S_j)(rho0)=0.
Thus energy-neutrality is the exact largest Hermitian error class preserving
this fixed reference state by this mechanism. It is NOT the largest class
for which a fixed controller could preserve memory: a nonequilibrium proof
may go beyond it. KERNEL_OBSTRUCTION.md shows why finite dephasing does not
automatically provide the needed Markov/sector reduction for charged errors.

No arbitrary-energy-changing-V guarantee, native bath admission, practical
strength threshold, robustness during noisy state preparation, or world
priority is claimed. The generic stationary-observable principle and the
nominal Davies construction are established tools; the explicit restricted
fixed-controller composition and its residual charged-error gate are the
scientific deliverables here.
