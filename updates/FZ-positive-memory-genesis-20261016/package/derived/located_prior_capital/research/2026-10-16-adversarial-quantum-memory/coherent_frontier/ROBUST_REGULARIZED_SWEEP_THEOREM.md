# A regularized autonomous sweep memory with an open local-generator tolerance

16 October 2026. Reserved worker Sol 7. No agents were spawned.

**Verdict:** there is a constructive extension beyond positive Pauli
trajectories. Complete the sweep into CPTP proposal maps and add a sufficiently
weak, fixed local depolarizing floor. The resulting time-independent,
constant-range family tolerates an open ball of arbitrary local
Hermiticity-preserving, trace-annihilating generator perturbations, including
Hamiltonian drift, non-Pauli Lindblad noise and imperfections of the correction
jumps themselves. The lifetime conclusion is conditional on the exact LSS/HT
imports and deterministic sweep-envelope/torus/homology arguments in the root
reconstruction. It is not a proof of robustness of the original unmodified
generator. External correctness and historical originality are unestablished.

The argument does **not** replace coherent faults by positive Pauli faults.
It retains the Kraus sums and their phases, and uses exact correction of their
span on each good proposal schedule. The probability estimate concerns the
proposal schedule, independently of the quantum state and the Kraus record.

## 1. Precise theorem

Fix a finite cell radius q >= 1, independently of L. In the 4D cubical toric
code with one qubit per face, let R_(q,x) consist of all six face qubits based
at cells y with ||y-x||_infinity <= q. For large enough L this patch contains

    m_q = 6(2q+1)^4 qubits,       d_q = 2^m_q.

Let D_(q,x) be complete depolarization of this patch, acting as the identity
superoperator outside it:

    D_(q,x)(rho) = (I_R/d_q) tensor Tr_R(rho).

For each primal/dual vertex v, define the completed local sweep channel C_v
in Section 2. There are constants beta_q,delta_q,A_q,c_q > 0 and an integer
b_q, independent of L,T and of the perturbation, such that the following holds.
One can take delta_q = beta_q/d_q^2. Define

    G_(reg,L) = kappa sum_(v,sector) (C_v-Id)
                 + beta_q kappa sum_x (D_(q,x)-Id).           (1)

At each cell allow an arbitrary linear map E_x on operators on R_(q,x),
extended by the identity superoperator outside, satisfying

    E_x is Hermiticity-preserving,
    Tr(E_x(A)) = 0 for every local operator A,
    ||E_x||_diamond <= delta_q kappa.                         (2)

The maps and their coefficients are time independent. They may vary with x
and L. Put E = sum_x E_x. Then G_(reg,L)+E is a local Lindblad generator.
For all sufficiently large M and L=b_q M, a single fixed perfect final
syndrome-recovery decoder Dec_L satisfies

    || Dec_L exp[T(G_(reg,L)+E)] Enc_L - Id ||_diamond
       <= min(2, A_q L^4 (1+kappa T) exp(-c_q L)),  T >= 0.   (3)

All six logical qubits, arbitrary logical density operators and arbitrary
external references are covered. The constants are uniform throughout (2).
No physical auxiliary envelope, synchronized clock or classical register is
introduced. The base generator (1) is translation invariant; the permitted
perturbations need not be. Rates, range, terms per cell and cell Hilbert
dimension remain independent of L. The depolarizing terms can have very large
but fixed support for a given q.

The deliberate floor is present even when E=0. A positive existence threshold
is obtained, with no claim that its value is practical. This theorem is not a
claim about arbitrary non-Markovian baths or size-growing interaction range.

## 2. Complete each corrector into a CPTP proposal

At a primal vertex let s run over all 2^8 sign patterns of its eight incident
commuting edge stabilizers. Let Pi_(v,s) be the corresponding spectral
projector. Some projectors can be zero because of code relations; nevertheless

    sum_s Pi_(v,s) = I.

For an active trailing pattern, set Q_(v,s) to the original Pauli on the one
or two paired positively based faces. For every inactive pattern set Q_(v,s)=I.
Define

    K_(v,s) = Q_(v,s) Pi_(v,s),
    C_v(rho) = sum_s K_(v,s) rho K_(v,s)^dagger.               (4)

Since Q is unitary,

    sum_s K_(v,s)^dagger K_(v,s) = I.

Thus C_v is CPTP, with the same at-most-24-qubit support as the original local
corrector. On the dual lattice use the identical construction for X correction.
In Lindblad notation,

    kappa(C_v-Id) = sum_s D[sqrt(kappa) K_(v,s)].              (5)

Relative to the original generator, (5) adds the inactive-pattern dephasing
terms kappa D[Pi_(v,s)]. For a Pauli error P_E applied to an arbitrary code
state, each Pi is scalar 0 or 1 on P_E times the code. The added terms vanish
on that density operator. The original code-initial Pauli trajectory law is
therefore exactly unchanged. This does **not** establish equality of the two
generators on cross-syndrome coherences.

A smaller completion using one lumped inactive projector is also possible,
but (4) fixes the construction used in this theorem.

## 3. The intermediate theorem: arbitrary local CPTP Poisson faults

Replace the floor and perturbation in (1) by

    sum_(x,a) nu_a (N_(x,a)-Id),                             (6)

where every N_(x,a) is an arbitrary CPTP channel supported in R_(q,x),
there are finitely many types a per cell, and sum_a nu_a <= nu uniformly.
For sufficiently small nu/kappa, the conclusion (3) holds for the completed
sweep. The channels may be spatially nonuniform. This includes nonunitary
fault proposals and coherent unitary rotations at rare proposal times.

For a finite lattice the semigroup of (5)+(6) is exactly an average over
independent rate-kappa correction proposals and rate-nu_a fault proposals.
Conditional on the ordered proposal times and locations, compose the full
CPTP maps at those locations. Averaging gives the generator, either by the
first-event equation or by the convergent Poisson/Dyson series. The conditional
map is trace preserving. One must not condition on a quantum Kraus outcome
and then presume its probability is independent of the logical input.

Equivalently, using Kraus jumps for all proposal maps, the sum of J^dagger J
at each proposal location is its rate times I. The full no-jump operator is
scalar, and the no-jump factors yield precisely the ordinary Poisson law.
This treats no-jump terms exactly rather than deleting them.

### 3.1 One common support envelope, for all Pauli choices

At a fault proposal centered at x, set both CSS envelopes to one on the fixed
vertex box B_infinity(x,a_q), where a_q=q+3 is a conservative choice accounting
for primal and dual face conventions. This box contains the syndrome vertices
of every Pauli operator on R_(q,x), including Pauli products with many factors.
At the correction clocks use exactly the old-state monotone map in the saved
MONOTONE_ENVELOPE.md. Each Pauli branch of any Kraus expansion has its actual
syndrome support inside this *same* envelope at every event. No Pauli branch
selection appears in the envelope or its probability space.

The local-burst version of the forcing argument has the same five halfspace
sets, same eroder phi, same clearance certificates and same correction-clock
fast-chain count. Only the birth hazard changes. With

    Delta = C b/kappa,   m = floor(Rb/2),   a = a_q,

a valid single-sector primitive bad-flag bound is

    delta <= 2b^4 exp[(5 log(8)-C/2)b]
              + b^4 (35 kappa Delta)^m/m!
              + nu Delta [ (2R+5)b + 2a + 3 ]^4.            (7)

For the third term count proposal centers whose affected vertex box meets
the radius-(R+2) primitive guard. Summing the finitely many proposal types
uses their total rate nu, rather than treating multiplicity as free.

Choose C=10log(8)+2 and R >= ceil(280eC)+10. Fix the dependence guard to coarse
radius R+5. Choose the HT death tolerance and the LSS marginal tolerance
delta_* for these already fixed radii. Next choose b >= 2a+4 sufficiently
large that each of the first two terms in (7) is <=delta_*/3. The enlarged
birth-center guard is then contained in the fixed coarse radius R+5, so this
dependence choice is valid independently of b. Finally require

    nu/kappa <= delta_*
      / { 3 C b [ (2R+5)b + 2a + 3 ]^4 }.                   (8)

This order is noncircular, and the right-hand side is strictly positive.

All flags use fresh local primitive increments. Their fields are independent
between slabs and finitely dependent in space. Apply exactly the saved
infinite-volume LSS domination and HT spacetime-component tail, followed by
the fixed-anchor stopped finite-torus replay. The enlarged local birth guard
only changes constants. Consequently, with probability at least

    1 - A'_q L^4 (1+kappa T) exp(-c'_q L),                  (9)

both envelopes stay below the first macroscopic-component escape up to T.
This one event controls **every** supported Pauli history on that proposal
schedule. Sector independence is not required: the same fault proposal can
change both sectors, and their exceptional events are union-bounded.

### 3.2 Accumulated homology for a local burst

The saved final decoder fills each sufficiently small syndrome component in
its uniquely lifted coordinate box. Keep r=L/32 and rho=L/8. A local Pauli
fault in R_(q,x) gives a 2-chain F in a fixed radius-a box. Every affected old
syndrome component meets that box. If all component diameters are <r, the
affected old/new components, their fillings and F lie in a single embedded
box of side at most 2r+2a+O(1), which is <rho for sufficiently large L.
Unaffected fillings cancel. Therefore

    F + D(s) + D(s+boundary(F))

is closed and supported in a contractible box, hence a stabilizer boundary.
The whole-slab cover in the saved argument ensures the small-component
condition at every physical event, including transient/pre-jump syndromes.
Induction keeps the decoded homology of the **entire** accumulated Pauli
error equal to zero. Splits, merges, syndrome cancellations, and local closed
parts of F do not remove accumulated error from this induction.

### 3.3 Exact Kraus-span recovery on a good proposal schedule

Fix a good schedule H, including every correction and fault proposal up to T.
Choose a Kraus decomposition for each of its fault channels. Expand each
fault Kraus operator on its finite patch in the Pauli basis:

    N_j = sum_P alpha_(j,P) P.                             (10)

Also fix a full record r of the ideal-correction Kraus labels and the final
syndrome-recovery Kraus label. Expand the composite recovered Kraus operator
A_(H,r) using (10), preserving the complex coefficients and Pauli phases.
Write V_L for the encoding isometry, so Enc_L(rho)=V_L rho V_L^dagger;
A_(H,r) maps the physical Hilbert space to the recovered logical space.
On the encoded code space, an ideal factor Q Pi either kills a Pauli summand
or acts by precisely the legal classical sweep correction for its current
syndrome. Every surviving summand thus corresponds to a valid supported
Pauli history on H, and is covered by the common envelope.

By Section 3.2 and the fixed final recovery, each surviving recovered Pauli
summand restricts to a scalar phase times the identity on the **whole** logical
space. Hence

    A_(H,r) V_L = c_(H,r) Id_logical                       (11)

after identifying the final recovered code with the logical system. The
number c_(H,r) is the actual complex sum over surviving histories. Histories
can merge, reinforce or cancel. There is no sum of absolute Pauli coefficients
and no division by a potentially zero coefficient.

The conditional proposal circuit followed by final recovery is CPTP. Thus
sum_r |c_(H,r)|^2=1. Its logical channel is exactly Id, for every logical
operator and with any untouched reference. This conclusion follows from
operator equality (11), not from selected codeword fidelities.

Average over schedules. On the good event the channel is Id; the normalized
average over the bad event is another CPTP channel. Therefore

    Dec_L exp(TG) Enc_L = (1-p_bad) Id + p_bad B_T,
    ||Dec_L exp(TG) Enc_L-Id||_diamond <= 2 p_bad.           (12)

Equations (9)-(12) prove the intermediate theorem. The argument avoids a
global exp(constant L^4 T) absolute-weight loss because it never expands the
probability of the full proposal circuit into signed fault-path weights.

## 4. A local Choi-interior lemma absorbs arbitrary generator perturbations

Let a patch have Hilbert dimension d. Define normalized Choi matrices using
the unit maximally entangled vector |Phi_d>:

    J(F) = (F tensor Id)(|Phi_d><Phi_d|).

Complete depolarization D has J(D)=I/d^2. If E is Hermiticity-preserving and
trace annihilating, then J(E) is Hermitian and

    ||J(E)||_infinity <= ||J(E)||_1 <= ||E||_diamond.         (13)

For ||E||_diamond <= nu/d^2, the linear map

    N = D + E/nu                                          (14)

satisfies

    J(N) >= (1/d^2 - ||E||_diamond/nu) I >= 0.

It is trace preserving because D is and E is trace annihilating. Positivity
of the Choi matrix gives a Kraus decomposition (diagonalize it and reshape
the eigenvectors), so N is CPTP. This also proves the used Choi criterion
directly in finite dimension. The exact generator identity is

    nu(D-Id) + E = nu(N-Id).                               (15)

No perturbative truncation or large-time remainder appears in (15). The map
E itself need not be a Lindblad generator. In particular, differences of
two local Lindblad generators can be absorbed.

Set nu=beta_q kappa with beta_q strictly below the positive threshold (8).
Apply (13)-(15) to every E_x, with d=d_q. The total generator (1)+E becomes
the arbitrary-CPTP Poisson generator of Section 3 at total proposal rate nu
per cell. This proves (3), uniformly over (2), using fixed b_q and constants.

For a finite catalog of smaller patch types R_a, one may instead install a
floor nu_a(D_(x,a)-Id) for each type and require

    ||E_(x,a)||_diamond <= nu_a/d_a^2,
    sum_a nu_a <= the permitted per-cell proposal budget.

The single q-box construction proves existence without any catalog promise;
the catalog variant can drastically improve the finite dimension factor.

## 5. The perturbation class really includes coherent drift and faulty jumps

For arbitrary local H_x=H_x^dagger and local Lindblad operators V_(x,j),

    E_x = -i[H_x, .] + sum_j D[V_(x,j)],
    ||E_x||_diamond <= 2||H_x|| + 2 sum_j ||V_(x,j)||^2.    (16)

Thus (16) below delta_q kappa suffices. This covers continuous, unmarked
Hamiltonian drift, not just coherent rotations at rare physical times: (15)
is an identity of its continuous generator after the deliberate floor is
included. The original Hamiltonian is encoded in the Kraus operators of N.

If an engineered local jump J is replaced by J+Delta J, its contribution is

    E_J = D[J+Delta J]-D[J],
    ||E_J||_diamond <= 4||J|| ||Delta J|| + 2||Delta J||^2. (17)

Group these local differences and any Hamiltonians by their bounded support
patches; charge their total per-cell budget in (2). This allows arbitrary
changes of the correction's projector/action amplitudes and local Hamiltonian
miscalibration, subject to that budget. Small changes of the floor jumps
themselves can also be charged this way. A claim made in terms of per-jump
errors must include the finite number of jumps in the cell; it cannot discard
that multiplicity.

The tolerance is a local-generator norm tolerance. The total norm of E can
grow as L^4, which is allowed. There is no assumption ||E|| T << 1.

## 6. Why the two modifications matter

1. Original active jumps have syndrome-dependent total J^dagger J. Null
   correction proposals are a valid representation on code-initial Pauli
   mixtures, but are not automatically a state-independent CPTP proposal
   decomposition on arbitrary cross-syndrome coherences. Section 2 fixes that.
2. A Hamiltonian drift alone cannot be written r(N-Id) with a finite rate and
   N CPTP. Even an amplitude-damping Lindbladian generally lacks that form.
   Section 4 supplies a local CP interior by adding actual engineered noise.

The exact one-qubit falsifiers are in EXACT_COUNTERMODELS.md and the executable
check. They disprove those shortcuts, rather than proving that the original
memory cannot tolerate coherent errors. Without the regularization, a uniform
coherent fault-path/doubled-history estimate remains unproved here.

## 7. Resource and provenance boundaries

The code still has 6L^4 data qubits grouped into dimension-64 cells. Each
completed corrector has at most 2^8 Kraus terms with at most 24-qubit support.
Each depolarizing floor has m_q-qubit support and can be written with d_q^2
Pauli Kraus terms. These counts are fixed for q but can be enormous. One
floor proposal per cell has rate beta_q kappa, and its full hazard is charged
in (7). There is no noiseless classical layer and no manufactured schedule.

The proof inherits the exact envelope, block forcing, published LSS/HT
imports, stopped torus replay, whole-slab cover and component-filling decoder
from the saved reconstruction. Its additional deductions are the uniform
Kraus-span recovery and Choi-interior regularization. An independent review
must verify both these deductions and the inherited proof. Finite exact
matrix checks are sanity checks of specified identities, not certification
of an asymptotic memory theorem or novelty.

Engineering the many-body floor and dephasing channels, embedding the 4D graph,
preparing the code, reservoir/energy/reset costs, calibration within the very
small tolerance, and imperfect readout remain unacquired. No practical noise
threshold, hardware implementation or civilization-scale capability follows.

## 8. Primary sources read for the comparison

The source record is in SOURCE_REFS.md. Drechsler-Oreg-Aharonov 2610.05589v1
supplies the closest explicit Pauli/classical reduction and synchronous/Floquet
results; Section 1.8 discusses general Markovian noise and local-generator
stability. Those open questions motivate the scope but establish no novelty.
Pastawski-Clemente-Cirac 1010.2901v2 is the prior engineered static 4D toric
memory model with numerical local-memory evidence. Dünnweber-Styliaris-Trivedi
2601.20818v3 supplies a broader-noise discrete-time theorem and a static
continuous-time proposal-channel construction/threshold outline under local
unitary jump noise. Its Sections VII.2 and Discussion must be credited when
assessing prior autonomous constructions. The elementary CPTP proposal and
finite-dimensional error-span/Choi facts are not claimed to be new.
