# A finite parity instrument with a retained quantum source

Working construction, 31 October 2026. This is a structural information/control
result with a derived microscopic interaction geometry. It is not a claim of a
completed semiconductor resource cycle. It retains the earlier charge-leakage
instrument as a separate operation: logical parity does not diagnose arbitrary
physical charge or orbital leakage.

## The useful operation determines the interaction

For two valid logical qubits, let Pe=(I+Z1 Z2)/2 and Po=(I-Z1 Z2)/2.
The useful consumer is an offline Bell resource. Measuring their parity after
preparing |++> produces a maximally entangled pair. Thus precise accumulation
of a pi/4 entangling phase is not necessary if a coherence-preserving parity
instrument and its actual controls can be supplied. Parity-based entanglement
and measurement reversal are established methods; the contribution here is the
retained-source, finite-stopping guarantee and the microscopic symmetry route.

Place three identical charge cells at z=-R,0,+R. The middle cell is the meter.
Within the unique dressed orbital ground state for each valid charge pattern,
global x reflection changes all three logical signs and eliminates every odd
Boolean energy term. Outer-cell interchange makes the two meter couplings
equal. Therefore, including every Coulomb pair,

    H_ground = E0 + J_DD Z1 Z2 + J_MD (Z1+Z2) ZM.

The direct data-data interaction has not been dropped. It is constant inside
each measured parity sector. The interaction operator follows from the spatial
representation and symmetry; it is not inserted as a native logical handle.

The companion microscopic calculation includes all fifteen Coulomb pairs.
At R=sqrt(2)d it gives J_MD=0.05244243313 K/d and J_DD=0.00311607562 K/d
with four modes/site. At R=1.7d, a three-mode calculation gives J_MD=0.0264288130
and J_DD=0.00134845133. These are ordinary numerical points, not certified
intervals. An analytic positivity/min-max argument gives a longitudinal
compartment orbital gap at least 20.20710 K/d for R>=sqrt(2)d. Bare-product
orbitals still differ from the dressed states by approximately .0037-.0043.
No six-electron finite-time return error is inferred from the earlier two-cell
cycle. See microscopic/THREE_CELL_PARITY_GEOMETRY.md.

## Quantum source and a path-dependent gain envelope

The qualified interrogation Hamiltonian is

    H = H_E + Z1 Z2 tensor C_E + (Z1+Z2) tensor B_E tensor ZM.

E includes the retained source, old records, and gauge. None of H_E, C_E, and
B_E need commute. The first two terms give different source evolution in the
two measured sectors, which is legitimate. They give the same evolution to the
two logical orientations inside either sector.

For one interrogation prepare the meter in +X and read X. The click has a
known Z1 byproduct. After correcting or tracking it,

    C_e = Pe tensor F_e,
    N_e = Pe tensor G_e + Po tensor V_e,

where V_e is source-unitary and F_e^dagger F_e+G_e^dagger G_e=I.

The gain need not be constant over an approach/dwell/return trajectory. Suppose
the actual operator has deterministic bounds

    b_minus(t) I <= B_E(t) <= b_plus(t) I.

Put b0=(b_plus+b_minus)/2 and dB=(b_plus-b_minus)/2. Require

    integral b0(t) dt / hbar = pi/4,
    D = integral dB(t) dt / hbar < pi/4.

The interaction-picture source branches are U_E exp(∓i pi/2) R_±.
The relative unitary R_-^dagger R_+ has angular path length at most 4D.
The unitary chord bound therefore gives

    ||G_e|| <= sin(2D),
    F_e^dagger F_e >= p I,       p=cos^2(2D).

If A_±=integral b_±dt/hbar and r=A_+/A_-, then p=sin^2(pi/(r+1)).
Zero-coupling portions are allowed. A long remote parking interval does not
artificially force r to infinity if its small or zero interaction action is
properly included. Arbitrary forward source evolution is retained throughout.
This is a bound on the full uncertain action, not a claim that travel is free.

Physical scope: equal scalar energies of two symmetric classical geometries
do not establish equal operator gains for independently fluctuating sources.
For H_int=(Z1 tensor B1+Z2 tensor B2) ZM, the odd sector responds to B1-B2.
Even the scalar example B1=b+e, B2=b-e falsely clicks on an odd input with
probability sin^2(2eT/hbar). Common operator gain needs a common source mode
invariant under outer-cell exchange, or an explicit mismatch bound. A source
coordinate entering a dressed orbital Hamiltonian also needs its actual
orbital motion/energy qualification; the abstract gain theorem does not supply
that qualification for arbitrary fast physical trap motion.

## Cover both outcomes, rather than waiting on a dark one

A single conclusive test has a dark parity. Repeating it on |++> leaves half
the ideal inputs consuming the whole cap. Its code-only stopped-error law
cannot be applied to that half. This is a real resource failure of the
one-sided Bell attempt.

Conjugate the native even test with an actual logical X2 to test odd parity:

    C_o = Po tensor F_o,
    N_o = Po tensor G_o + Pe tensor V_o.

The physical X2 sandwich and its finite duration belong to the implementation.
An even-then-odd sweep stops on its first click. Its conclusive operators are

    A_e = Pe tensor F_e,
    A_o = Po tensor F_o V_e,

and its all-inconclusive operator is

    N = Pe tensor V_o G_e + Po tensor G_o V_e.

If each targeted test has F^dagger F>=p I, then with q=1-p,

    N^dagger N <= q I_valid.

This contraction holds on every coherent superposition of the two valid
parities, not just on the sector sought by the first test. Noncommuting source
factors stay in their chronological order.

After M inconclusive sweeps the timeout operator is

    T_M = Pe tensor R_e + Po tensor R_o,      ||T_M||^2 <= q^M.

Add the two sector-projected timeout terms to their respective accepted
labels as a comparison instrument. Each sector's source map is then CPTP.
Consequently the comparison is a genuine parity Lüders instrument followed
by sector-dependent source channels. It preserves all quantum information
inside either parity sector.

For any input and reference let tau=T_M rho T_M^dagger. The actual-minus-
comparison instrument has three classical-label blocks:

    timeout: +tau;   even: -Pe tau Pe;   odd: -Po tau Po.

Their trace-norm sum is exactly 2 Tr(tau). Thus, when timeout has its own flag,

    D_diamond(actual ideal-capped, completed parity instrument)
        = ||T_M||^2 <= q^M,

where D_diamond is half the diamond norm. The completion is a comparison
channel, not a hidden physical parity measurement performed on timeout.
The finite device can report timeout. At p>=1/2, twenty sweeps make this
complete-instrument error less than 10^-6, including parity coherences and
arbitrary source/reference correlations.
This is a joint flagged-instrument guarantee. Conditioning additionally on a
particular rare parity label requires division by that label's actual
probability; no uniform normalized bound for arbitrarily rare labels follows.

### General finite-sector version

The argument is not limited to parity. Let {Pi_a} be an orthogonal resolution
of the valid logical space. Suppose each sector has an actually supplied
conclusive test C_a=Pi_a tensor F_a, with no-click operations that act only
on the retained source within every sector, and targeted success at least p.
A sweep testing each sector once has all-inconclusive norm at most sqrt(1-p).
The same completion, full-instrument q^M bound and stopped eta/p bound follow.
The essential condition is that every allowed outcome has a conclusive route.
Its implementation is a resource: s sectors generally cost up to s tests per
sweep, and the law does not make exponentially many sectors inexpensive or
supply tests for noncommuting observables. For a single parity bit s=2.

## Finite physical error and exposure

Let each complete physical sweep differ from its ideal instrument by
half-diamond distance at most eta_s, uniformly on valid two-qubit code tensor
every allowed retained source/reference history. Include its actual local X,
meter preparation, trajectory, analysis, readout, source evolution and renewal.
Any physical suffix is CPTP, including one after a fault creates a dark state.

The ideal-prefix/physical-suffix hybrid gives

    epsilon_M <= sum_j eta_j q^(j-1)
              <= eta_s (1-q^M)/p.

The complete parity-instrument comparison consequently obeys

    delta_M <= q^M + eta_s (1-q^M)/p.

The expected number of physical sweeps, even allowing absorbing faults, is

    E N <= g_M + (eta_s/p)(M-g_M),   g_M=(1-q^M)/p.

An uncapped protocol can have infinite mean work under an arbitrarily small
absorbing fault. A real cap is essential. Fixed-deadline holding after early
success is charged for its full duration; the discount applies only to work
that actually stops.

For an ideal prepared |++>, every conclusive record produces the same Bell
state after known Pauli corrections. Its ideal timeout changes yield rather
than accepted Bell purity. With physical error epsilon_M,

    p_accept >= 1-q^M-epsilon_M,
    D(accepted new Bell marginal, Phi+) <=
        epsilon_M/(1-q^M-epsilon_M).

Older quantum information correlated with the source is a separate claim.
Selecting even one ideal fine record can steer it. Coarse acceptance over
all conclusive records differs from a source CPTP completion by a term q^M;
the joint reusable-history guarantee uses delta_M, with normalized conditional
bound delta_M/(1-delta_M). Exact purity of the new Bell does not erase this
distinction. These bounds telescope on joint instruments across uses; no
independent source resets or independent noise are inferred.

## Actual operations and cost consequences

For the parity-preserving instrument the odd test is X2/native-test/X2, with
the final X applied or tracked on every branch. For Bell preparation the
post-click undo X2 cancels the usual odd-Bell-to-even-Bell correction. Both can
be omitted together. Running native probes with one physical X2 between
successive probes implements this schedule, retaining the logical frame.
The raw click's known Z1 remains corrected or recorded.

In the ideal balanced protocol, expected sweeps are at most 1/p and expected
probes at most 2/p. For |++> with the first probe seeking even parity, the
uncapped bound improves to 2/p-1/2, and the number of intervening physical X
operations is one less than the number of probes. At p=1/2 this is at most
3.5 probes and 2.5 physical X operations, before adding preparation and
any physical charge-leakage checks. The hard cap is 2M probes. These counts
do not establish a duration advantage because the X and detector costs are
substantial.

The entire physical cycle still requires:

* six electrons loaded into the closed-rail dressed orbital domain, with
  unprepared spins only under the existing spin-independent qualification;
* actual local state preparation and finite logical X, rather than an abstract
  permutation of charge labels;
* a symmetric three-cell trajectory and return with a quantified orbital
  error, full source-force requirement and incident coupling sum;
* meter analysis/readout/renewal while coupled data remain protected, or a
  remote parked geometry whose residual action over their full duration is
  bounded;
* the separate coherence-preserving physical-leakage instrument when its
  domain is needed, and actual reset after resource rejection.

A prepared meter in a definite charge orientation can cause an unknown
within-parity data phase during analysis/renewal. Those intervals cannot be
silently classified as safe. Bringing the meter back to a qualified remote
location before analysis is a candidate supplied operation only when its
travel area, orbital return and finite remote tail are all included. The
two-cell meter return numbers are not the three-cell return numbers.

Weak probes also do not give arbitrary accuracy for free. For short duration
T, p=O(b^2 T^2). If a detected leading error gives eta=O(e^2 T^2), eta/p stays
O(e^2/b^2), while expected interrogation time grows as 1/(b^2 T). A fixed
preparation/readout error divided by p grows even faster. A first-order
unflagged duration error eta=O(kappa T) produces eta/p=O(kappa/(b^2 T)).
The organizing result is a finite error/exposure law, not elimination of
physical faults by repeated interrogation.

## Executable evidence and prior machinery

Root balanced_parity.py propagates the full data-source-meter Hamiltonian
through piecewise, noncommuting positive gains and large source Hamiltonians.
It includes the data-data sector source term. It verifies factorization,
instrument completeness, the exact timeout diamond expression, Bell purity,
and the distinct correlated-history steering term. It is a theorem witness,
not a microscopic controller simulation. The companion independent audit
checks the same law separately.

Relevant established constructions include the quantum-point-contact parity
meter (https://arxiv.org/abs/cond-mat/0602514), measurement reversal
(https://arxiv.org/abs/0906.3468), and degeneracy-preserving syndrome measurement
(https://arxiv.org/abs/1611.01219). Cavity dual-rail operations
(https://arxiv.org/abs/2212.12077) and physical erasure checks
(https://arxiv.org/abs/2406.14621) receive the same balanced/stopped-instrument
improvement if their actual operations furnish its hypotheses. No device
advantage is inferred merely from the number of ideal probes.
