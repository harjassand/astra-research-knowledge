# Ongoing Fock injection through a rotating quantum memory

Owner: retained persistent/non-Gaussian bath Sol. 2026-10-25.

New question: can continuously renewed NONCLASSICAL inputs pass through a
persistent, backacting quantum memory while still admitting an all-set
fault bound uniform in circuit duration? A scalar classical filter is not
sufficient: it omits the force-operator commutators and the resulting quantum
backaction. A global initial-state comparison of every incoming Fock bin
would also charge a constant for every clock tick, even for one marked fault.

The construction below closes this question for an EXACT DISCRETE
collision/finite-pulse model. It uses a new mark-dependent mode compression,
a finite-dimensional bosonic number-moment calculation, the already proved
soft joint-energy inequality, and the existing Ng-Preskill Gaussian receiver.
The physical bath is not replaced or measured in the protocol. No generic
continuous-input, nonlinear-bath, hardware, novelty, or cold-input advantage
is asserted.

## 1. Exact finite-horizon quantum protocol

For a circuit of L contacts, begin with one bus mode c_0 and L-1 fresh input
modes c_1,...,c_{L-1}. All states and propagators are ordinary finite-mode
Fock-space objects; there is no trace-class state with infinitely many occupied
incoming bins. Bounds below are uniform in finite L.

Between contacts the bus undergoes a phase rotation and a passive beam-splitter
collision with the next fresh mode. Its FREE Heisenberg recurrence is

    a_{t+1} = zeta a_t + sqrt(1-|zeta|^2) c_{t+1},
    a_0=c_0,                 |zeta|=rho<1.                 (1)

A passive unitary on bus plus input supplies (1), retaining the outgoing
mode as environment rather than assuming a reset. Write a_t=a(v_t), where
a(v)=sum_j conjugate(v_j)c_j. Then

    v_t = conjugate(zeta)^t e_0
          + sqrt(1-rho^2) sum_{j=1}^t conjugate(zeta)^{t-j} e_j,
    ||v_t||=1,
    <v_t,v_s> = zeta^{t-s} for t>=s.                      (2)

The physical data contact at clock t is a FINITE pulse. During that pulse,
injection, bus rotation, and the passive bus coupler are switched off. Its
angular-frequency Hamiltonian is

    K_t(u)=K_control,t(u)+gamma_t(u) S_t(u) X_t,
    X_t=a(v_t)+a(v_t)^dagger,
    ||S_t(u)||<=1,        integral_pulse |gamma_t(u)|du<=g. (3)

S_t is a bounded local data/ancilla operator. The ideal controls may be
noncommuting and may entangle data. All bath forces within this contact use
the SAME free mode v_t. Contacts have disjoint time windows. More than one
fixed free mode per location is possible with an explicit rank/contact cost,
but is not silently included in the constants below.

The finite collision, switching, and finite force pulse define the exact
model; no delta-kick approximation is needed. A continuously damped bus
throughout a finite gate can see an infinite-dimensional span of fresh modes
inside ONE location. It is not covered simply by writing r modes for r
marks. A switching implementation or an independently justified rank/error
approximation is required to connect that different model.

Initially the marginal state of all input modes, INCLUDING c_0, is diagonal
in the joint occupation basis, supported on n_j<=n0. Thus it can be any
convex mixture of product configurations |n_0,...,n_{L-1}>, including classical
correlations among inputs. Product Fock states with n0>=1 give a pure,
genuinely non-Gaussian and nonclassical example. For the usual computation
contract the source is prepared independently of the unknown logical input.
The mathematical estimate also holds for initial outside/reference
correlations whenever this same marginal and uniform support contract holds.

The bath is not required to stay below this cutoff after data interactions.
The actual interacting bus can be pumped and become entangled with the data.
Equation (1) is the FREE interaction-picture mode decomposition, not a claim
that the interacting bus ignores data backaction.

For Im(zeta)!=0 the force operators do not commute:

    [X_t,X_s] = 2i Im(zeta^{t-s}) I, t>=s.                (4)

For example the earlier contact exp(-ig S X_0) changes a later X_1 by
2g Im(zeta) S in the corresponding Heisenberg expression. This is an actual
retarded data-dependent disturbance. There is no joint exogenous classical
angle process representing these force operators.

## 2. The exact full marked operator

For a specified set F of r contacts, let U_J be the FULL joint propagator
with the data-bath terms in the marked contacts F\J switched off, and all
other contacts, ideal controls, passive collisions, and outputs unchanged.
Define

    A_F = sum_{J subset F} (-1)^(r-|J|) U_J.              (5)

This is the sum of all perturbative paths with at least one noise insertion
in every marked contact. It is bounded, ||A_F||<=2^r, regardless of the
unbounded individual fields. Its positive effect A_F^dagger A_F is the SAME
operator for every initial-state comparison below. It is not an observed
syndrome or an ordinary probability effect. In a purification,
||Psi_bad(F)||^2=Tr(rho_initial A_F^dagger A_F).

## 3. Compress the marked fields, not the entire source history

For this F let T be the one-particle span of {v_t:t in F}, let P_T be its
orthogonal projector, and let d=dim T<=r. Fock space factors canonically as
F(T) tensor F(T^perp), with a fixed passive change of mode basis. This
factorization is a PROOF representation; no physical mode sorter is assumed.

In the free interaction picture split every field, at ALL contacts, as

    X_t = X_T,t + X_perp,t,
    X_T,t=a(P_T v_t)+a(P_T v_t)^dagger.                   (6)

At each marked contact X_perp,t=0 exactly. All T-perpendicular terms at
unmarked contacts can therefore be absorbed, along with data controls and
outside registers, into a unitary enlarged-system background. They cannot
fault a mark. In this background interaction picture the T-field couplings
at every time, including every unmarked contact, remain explicit. Their
bounded system factors have unchanged operator norm under conjugation.
No selected unmarked interaction is discarded.

The original free evolution need not preserve T as a physical cavity
subsystem. Equation (6) uses fixed INITIAL interaction-picture modes, with
their full time-dependent coefficients. This is why infinitely many past
contributors do not require selecting infinitely many source bins at once.

## 4. A passive-compression photon-number bound

Lemma. Let P be an orthoprojector of rank d in a finite one-particle input
space, N_P=c^dagger P c, and let the input occupation configuration obey
n_j<=n0. For beta>0 with n0(e^beta-1)<1,

    <n|exp(beta N_P)|n>
       <= [1-n0(e^beta-1)]^(-d).                         (7)

The same bound holds for arbitrary convex mixtures of these occupation
configurations, including classically correlated mixtures.

Proof. Put t=e^beta-1. Since P is a projection, diagonalizing it gives the
normal-order identity exp(beta N_P)=:exp(t c^dagger P c):. Let Z be an
auxiliary proper complex Gaussian vector of covariance P. Normal-ordered
Gaussian integration, or expansion into creation/annihilation monomials,
gives the exact finite-occupation identity

    <n|:exp(t c^dagger P c):|n>
       = E_Z product_j L_{n_j}(-t |Z_j|^2),               (8)
    L_n(-x)=sum_{m=0}^n binom(n,m) x^m/m!.

One way to verify (8) term by term is that
E product_j |Z_j|^(2m_j)=per(P[m]), where P[m] repeats row/column j m_j
times. On the operator side the same term has coefficient
product_j binom(n_j,m_j)/m_j!. The Gaussian integral here is mathematical,
not a physical Gaussian assumption about the input or its evolved state.

For x>=0 and n<=n0, binom(n,m)<=n0^m gives L_n(-x)<=exp(n0 x).
Consequently (8) is at most E exp(n0 t ||Z||^2). The nonzero eigenvalues
of P are exactly d copies of 1, so this integral equals (1-n0 t)^(-d).
This proves (7). Convexity gives its mixture extension.

This is a mode-count, not a total-source-energy bound. There can be n0 L
photons supplied across the complete history, but a rank-d passive
compression has the uniform exponential moment (7). Photon bunching can
still produce very large occupancies with small probability; the lemma
does not assert a hard cutoff on N_P.

The number-diagonal premise is necessary for this uniform argument. For
example the product (|0>+|1>)/sqrt(2) over L input modes has, in the uniform
bright mode, <N_P>=(L+1)/4 although every input is supported on n<=1.
A common +/- phase mixture makes its mean field zero without removing
this extensive population. Hard per-mode supports or zero first moments
alone do not establish (7) for coherent input states.

## 5. Initial joint order after compression

Apply the already proved soft joint-energy inequality to A=F(T), with
K_A=N_T and the entire T-perpendicular bath/data/reference as O. If

    Q=exp(-beta N_T/2), Z=Tr Q=(1-q)^(-d), q=e^(-beta/2),
    Omega_O=Tr_T[exp(beta N_T/2) rho exp(beta N_T/2)],

then, for M=Tr Omega,

    rho <= M Z^2 tau_T tensor sigma_O,
    tau_T=(1-q)^d q^N_T,      sigma_O=Omega_O/M.           (9)

This follows by weighted Cauchy-Schwarz on each energy block and permits
arbitrary initial T-O entanglement created by the passive basis change.
In general sigma_O is tilted and is NOT the original outside marginal.
Only the physical initial marginal enters M in (7).

For n0>=1 choose any q satisfying sqrt(n0/(n0+1))<q<1. Equations (7)-(9)
give a per-selected-mode cost

    rho <= C(q,n0)^d tau_T tensor sigma_O,
    C(q,n0) = 1/{[1-n0(q^(-2)-1)](1-q)^2}.              (10)

Because d<=r and C>=1, this costs at most C^r per specified fault set,
independently of L or the number of contributing incoming bins. A simple
rational choice is q=1-1/[4(n0+1)], for which

    C<=32(n0+1)^2,
    2 n_ref+1=(1+q)/(1-q)<=8(n0+1),
    n_ref=q/(1-q).                                       (11)

For n0=0 the physical bath is vacuum, and rank-one support forces product
with the outside. Take tau_T vacuum and C=1 directly rather than using
the loose n0>=1 choice.

Neither the compressed physical state nor its future dynamics is Gaussian.
The Gaussian state in (9) is only an initial comparison state for the same
positive effect in (5). There is no per-clock-step comparison factor.

## 6. Marked-first-leg covariance and full unmarked resummation

Under tau_T the free selected fields are centered Gaussian with

    Delta_T(t,s) = (n_ref+1)<P_T v_t,P_T v_s>
                   + n_ref<P_T v_s,P_T v_t>.             (12)

For every first leg t in F, P_T v_t=v_t. Thus (12), even when s is an
arbitrary UNMARKED contact, equals the corresponding full-mode thermal
covariance. In particular,

    |Delta_T(t,s)| <= (2n_ref+1) rho^|t-s|, t in F.        (13)

There is no assertion of a useful bound of this form for every unmarked
first leg after projection. It is not needed by the Gaussian skeleton proof.

Here is the necessary localization of that proof. In the squared bad norm
there are 2r earliest insertions, one in every mark on each Keldysh branch.
Every skeleton contraction has at least one of these earliest marked
vertices. The other leg is another earliest marked vertex or an arbitrary
legal insertion. The complete sum of remaining dressing is resummed into
norm-at-most-one hybrid system strings. It therefore suffices to bound

    E_F = max_{t in F} integral_first_leg_in_contact_t
                         integral_second_leg_all_contacts |covariance|,

with the coupling envelopes included. The other leg includes the ENTIRE
finite computation, all selected unmarked contacts, and both contour
choices (the latter supplies the familiar factor 2 in the skeleton sum).
Ng-Preskill Eqs. (59)-(63) explicitly use E(i) only for these marked first
legs; no recursive unmarked-first envelope is inserted. Their full-time
Gaussian Wick equalities still hold here for tau_T, not for the physical
Fock source. The enlarged background remains unitary and all its dressed
system operators have the same norm bounds.

Using (3) and (13) gives the uniform estimate

    E_F <= E0 = g^2 (2n_ref+1) (1+rho)/(1-rho).            (14)

When 2E0<=1, the standard skeleton count yields

    Tr[(tau_T tensor sigma_O) A_F^dagger A_F]
       <= (2 e E0)^r.                                    (15)

For completeness the count is the same finite marked calculation as in the
core note: k internal contractions among 2r marked vertices give at most
(2r E0)^k/k! times (2E0)^[2(r-k)]; summing k=0,...,r and using 2E0<=1
gives (2eE0)^r. All full-time unmarked evolution is already included in the
hybrid resummation, rather than bounded by its Dyson absolute sum.

This step is precisely where replacing physical non-Gaussian moments by
termwise Wick upper bounds would have been insufficient. We use an actual
Gaussian comparison on the complete finite marked span, so the required
resummation is exact under the comparison state.

## 7. Uniform ongoing-quantum-source fault theorem

Theorem. For the exact switched collision/finite-pulse model (1)-(3), with
the stated initial joint-number-diagonal source cutoff, for every marked
set F of r contacts,

    ||Psi_bad(F)|| <= epsilon_inj^r,
    epsilon_inj^2 = 2 e C(q,n0) g^2 (2n_ref+1)
                                      (1+rho)/(1-rho),    (16)

provided 2E0<=1. For n0>=1 the completely explicit sufficient bound is

    epsilon_inj^2 <= 512 e (n0+1)^3 g^2 (1+rho)/(1-rho).   (17)

Proof. Combine the same positive effect with (10), use d<=r, then (15).
No physical state is substituted during the actual circuit. n0=0 is the
vacuum Gaussian case with C=1. A chosen ordinary local-coherent
fault-tolerance receiver applies if (16) is below its threshold and all
its other complete-circuit/gadget/ancilla hypotheses are met.

The source renews a non-Gaussian Fock input every clock cycle. The memory is
quantum and backacting whenever (4) is nonzero. Nonetheless the sufficient
noise strength is independent of circuit duration. Long memory and large
input occupation are explicitly expensive; this is not an optimized constant.
The bound degenerates as rho approaches 1, and does not claim to certify an
undamped recurrent bus at arbitrary duration.

## 8. Operations, resources, and strongest conventional baseline

The supplied physical interface is a bounded local data-force contact,
passive bus rotation/beam splitter, a fresh number-diagonal Fock-cutoff input
per clock, and the ability to separate injection from force pulses. For L
contacts this consumes L incoming bosonic modes including initialization,
at most n0 L supplied excitations, L-1 passive collisions, their switching
time, and the total data-contact time. Old outgoing modes may be left
unmeasured. Coherent source preparation and exact occupation-tail/support
certification are NOT acquired from an observed mean photon number.

In a particular circuit-QED/phononic device the pulse waveforms, mode
orthogonality, phase stability, coupler loss/thermal inputs, qubit-mode
locality, injector duty cycle, source errors, and neglected Kerr terms all
need their own bounds. Likewise finite input pulse preparation and
readout/reset/control errors of the QEC computer must fit an additional
receiver budget. There is no claim of a demonstrated apparatus or a generic
continuous Markov input-field limit. Keeping one photon in every bin as the
bin duration tends to zero would also make the supplied flux diverge.

The strongest ordinary receiver is the SAME non-Markovian QEC framework
with exactly this source and control knowledge. Passive collision models,
linear bosonic mode transformations, normal ordering, Gaussian integration,
and Ng-Preskill are established methods. Merely writing a Fock collision
model is not new. A source-mode-by-source-mode initial domination would
charge the whole history or require truncating memory with duration-dependent
error. The closed mechanism here is instead the marked-span compression
plus a uniform compression moment bound and marked-first-leg resummation.
This is an explanatory/sufficient-theorem capability, not a new QEC code,
exclusive architecture, practical speedup, or proof of priority.

Cold vacuum inputs through the same passive coupling have n0=0 and a smaller
noise bound. If those inputs are equally available, they are a stronger
matched noise-suppression baseline. The present theorem is useful as a
tolerance certificate for an actual specified nonclassical source, not as
a reason to inject extra photons into a quantum computer.

Primary ancestry opened/read during this question:

- Ng and Preskill, *Fault-tolerant quantum computation versus Gaussian noise*,
  PRA 79, 032318 (2009), Sec. V, especially Eqs. (59)-(66), and Sec. VI,
  https://arxiv.org/html/0810.4953 .
- Ciccarello, Lorenzo, Giovannetti and Palma, *Quantum collision models: open
  system dynamics from repeated interactions*, Physics Reports 954 (2022),
  primary article abstract/model scope inspected via
  https://arxiv.org/abs/2106.11974 ; this is model ancestry, not a theorem
  used in (7) or (16).
- The normal-order/permanent calculation is rederived in (8); MacMahon's
  standard repeated-permanent generating identity is related, but no
  uninspected counting-oracle result is used.

The uniform finite-horizon statement is the owned endpoint. A limit with
infinitely many occupied incoming modes, arbitrary continuous force-mode
rank, source number coherence, or nonlinear bath dynamics needs its own
construction and is not inferred here.
