# A specified full-qubit storage model for the native clock endpoint

29 October 2026. This composes the all-clock static theorem in PROOF.md
with the already whole-reviewed root logical receiver and Gaussian CKG
admission. It does not reopen those modules or run new dynamics. The
Hamiltonian is the actual two-body Pauli-clock endpoint, without arbitrary
additional physical Hamiltonian errors. The thermal generator is the exact
algorithmic quasilocal one specified below, not an inferred native bath.

## 1. Exact full logical algebra and the real Gibbs environment

Let U be the exact finite-depth prefix gauge. In that gauge the full
Hamiltonian is Delta H'(lambda;S), at EVERY clock energy. Supply the primary
shared-decoder corrected logical Paulis OX,OZ, and OY=i OX OZ. They are
Hermitian unitaries forming M2, and commute with every source stabilizer.
Thus they commute EXACTLY with H'(lambda;S). In physical coordinates put

    Oalpha_sim=U^* (Oalpha tensor I_clock) U.

They retain the whole logical algebra and commute with Hsim. Consequently
rho_beta=exp(-beta Hsim)/Z commutes with all of them. In its exact logical
tensor identification rho_beta=(I2/2) tensor tau_beta. The encoder and
decoder are the root's CPTP maps

    Enc(omega)=omega tensor tau_beta, Dec=logical partial trace,

in that identification. Logical twirl cost and Hamiltonian logical drift
are both ZERO. This is stronger than checking a single classical logical
observable. Physical acquisition/preparation of tau_beta is NOT supplied.

## 2. Every operator on a physical patch has a common good projector

For a physical patch X, the finite-depth gauge sends any operator on X
to an operator on X^+ with radius enlarged by a fixed RU. Its data portion
A contains at most qA qubits. The clock portion may be arbitrary. On the
gauged side expand only the data part in the full Pauli algebra on A,
retaining arbitrary clock-matrix coefficients.

The primary sufficient bad projector Pbad0 is syndrome-diagonal. Take the
union of its conjugates under the 4^qA data Paulis, as in the accepted
whole-support receiver. Its complement is a COMMON good sector for EVERY
data-clock operator on X^+. Clock matrices commute with the data logical
algebra, so their dimension introduces no Pauli coefficient cost in this
commutator statement. The corresponding physical good projector is its
conjugate by U.

Under the thermal gate of PROOF.md, the full syndrome free-energy change
under ANY Pauli-induced flip of tau checks is at most

    |Delta F_beta| <= (3/2) beta |tau|.                    (1)

The ground remainder contributes beta|tau|/4 and the thermal remainder
at most beta|tau|/4, in addition to the bare defect term. A qA-qubit Pauli
flips at most r qA supplied checks. Syndrome translation is a bijection
on the actual admissible set. Hence the full native-clock Gibbs state has

    p_bad(X) <=4^qA exp[(3/2)beta r qA] p_bad0
              <=4 exp[chi qA-c0 s_k],                    (2)
    chi=ln4+(3/2)beta r, c0=(ln2)/2, s_k=2^k.

Here the factor 4 and exponent c0 s_k are the supplied source two-sector
Peierls bound. There is no free replacement of a quantum Gibbs state by
its ground band: (2) used the FULL clock trace.

For a radius-R physical patch, the admitted source density and the fixed
gauge range give qA<=rhoU(1+R)^3, for example
rhoU=rho_data(1+RU)^3. Choose

    a=[c0/(2chi rhoU)]^(1/3),
    R_k=floor(a s_k^(1/3))-1.

Eventually R_k>=a s_k^(1/3)/2 and includes every fixed seed support. Then

    p_k<=4 exp[-(c0/2)s_k].                               (3)

This is a common projector bound for a WHOLE coherent jump on that patch,
including arbitrary clock operators, not just separate jump summands.

## 3. The actual admitted generator

For every data qubit take the three one-site Pauli seeds. For each L=8
clock take the 63 nonidentity three-bit Pauli matrices acting on its ONE
eight-level Hilbert space. This notation does not convert the Hamiltonian
to a two-body-qubit model. Every seed A is Hermitian unitary of norm one.
There are

    Nseed=3Ndata+63Nclock <=(3+63r)Ndata                    (4)

seeds, and a constant number per physical cell. The inequality follows
because every nonidentity supplied check contains at least one data qubit.

For EACH seed use the primary Gaussian Chen--Kastoryano--Gilyen generator
built from this SAME Hsim and beta, with

    f(t)=exp(-t^2/beta^2)/sqrt(beta sqrt(pi/2)),
    Ahat(omega)=(1/sqrt(2pi)) integral f(t)e^(-iomega t)
                                  exp(itHsim)Aexp(-itHsim) dt,
    gamma(omega)=exp[-(beta omega+1)^2/2],
    L_A(rho)=-i[B_A,rho]+integral gamma(omega)D_Ahat(omega)(rho)domega.

The coherent correction B_A is EXACTLY the double-time kernel in the
primary Eq11; it is retained. Sum all these one-seed generators at
constant per-site rate, and optionally add -i[Hsim,rho]. Every summand is
exactly stationary at rho_beta. Seed normalization is applied separately
before summing; there is no hidden 1/N slowdown.

This is the already admitted ordinary [CKG2311.09207v2, TheoremI.1/
Eqs7--12](https://arxiv.org/html/2311.09207v2) construction. Its complete
strength and tail receiver is root_quantum_receiver/CKG_ADMISSION.md.
The source Hamiltonian here is genuinely two-body and finite range, with
fixed but potentially enormous Delta and Delta lambda. Its ordinary LR
constants C0,mu,v_LR are independent of N, and may be correspondingly
terrible. No small or physically calibrated velocity is inferred.

In the notation of that admitted receiver,

    d_R=C0 exp(-mu R/2)+2 exp[-R^2/(4v_LR^2 beta^2)],
    rB(R)=6C0 exp(-mu R/2)
         +2C1 exp[-pi R/(4v_LR beta)]
         +6 exp[-R^2/(4v_LR^2 beta^2)],
    C1=8sqrt(2)exp[(1+pi^2)/8].

Its frequency-integrated jump strength is <=1 per seed. Its coherent
correction has norm <3. The WHOLE-jump truncation, including cross terms,
and its Hamiltonian truncation give, for all three logical observables,

    ||L_phys^*(Oalpha_sim)||_rho
       <=Nseed[9sqrt(p_k)+2rB(R_k)+4d_Rk+2d_Rk^2].          (5)

The optional Hsim drift contributes exactly zero. All uses of R_k are
analytical truncations; the actual generator remains the exact quasilocal
one. No fixed-radius implementation or infinite-resolution Davies jump
is silently substituted.

## 4. Quantum storage consequence and its clock

For R>=1 choose fixed Ctail,ctail>0 from the displayed formulas so

    2rB(R)+4d_R+2d_R^2<=Ctail exp(-ctail R).

Put uk=s_k^(1/3), b=min(c0/4,ctail a/2)>0 and
CD=(3+63r)(18+Ctail). Equations(3)--(5) imply

    max_alpha ||L_phys^*(Oalpha_sim)||_rho
          <=CD Ndata exp(-b uk).                          (6)

Apply the accepted root stationary-state receiver with zero twirl cost:

    1-Fe(I/2,Dec exp(time L_phys) Enc)
          <=(3/4)CD Ndata time exp(-b uk).                 (7)

This is in the parallel per-site-rate clock of (4). The source size bound
Ndata,k<=5(g^2)^k with fixed admitted g makes Ndata polynomial in uk.
Beyond a fixed onset, for every

    0<=time<=exp(b uk/4),

(7) is <=exp(-b uk/2). The root's Kraus-variance conversion gives fidelity
at least 1-2exp(-b uk/2) for EVERY purified logical-qubit input, and diamond
error at most 2sqrt(2)exp(-b uk/4). Thus a stretched-exponential-in-size
storage interval follows for this specified model. No mixing-time bound
or rapid thermal initialization is claimed.

## 5. Exact boundary

This closes a MODEL-WISE finite-temperature storage composition for the
unperturbed native two-body-QUDIT clock endpoint under an established,
exactly stationary, quasilocal algorithmic thermal generator with a full
known logical algebra. It includes noncommuting physical seed errors on
data and clocks; it is not a clock-only noiseless-subsystem example.

It does not prove a native Davies bath theorem, microscopic finite-coupling
thermal storage, strictly finite-range dissipative dynamics, robustness to
unknown changes of Hsim, fixed-controller robustness, efficient encoder
implementation or physical fabrication. Arbitrary added local Hamiltonian
errors were handled at ZERO T in the separate parameter-qualified package;
they are not imported into the present finite-T syndrome expansion.

The extremely conservative penalty and the Hamiltonian-dependent spectral
filters/coherent controller are real resources, not hidden prerequisites.
No practical memory, comparative advantage or historical priority is inferred.
