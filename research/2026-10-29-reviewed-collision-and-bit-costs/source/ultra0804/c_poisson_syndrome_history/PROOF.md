# Clockless restoration of syndrome coherence histories

29 October 2026. Constructed theorem. This supplies a restricted, all-orders
history-restoring operation with explicit physical-time cluster/exposure
bounds. It is **not yet a full autonomous memory theorem**: the residual
classical nonequilibrium Pauli-history persistence gate is separately named.
No source is assumed to have that gate merely because it has a static
Peierls bound or a synchronous decoder threshold.

## 1. Fixed register-free controller and actual model

Let S_a be commuting Pauli checks of a stabilizer code on n qubits, with
distance d. Redundant checks are allowed. Each qubit belongs to at most D
checks and every check has weight at most w. Every protected physical site
is covered by a check. In each admissible joint syndrome sector fix a Pauli
encoding E_s from the code sector. The initial encoder has the form

    Enc(omega)=sum_s p_s E_s omega E_s^dagger,

with p_s independent of omega; an arbitrary reference is allowed. This
includes the admitted nominal stabilizer-Gibbs module. It is not an
assumption about a noncommuting perturbed Gibbs stationary state.

The nominal recovery uses local, state-independent Poisson attempts. At
an attempt it measures a bounded set of checks, applies a deterministic
Pauli determined by their outcomes and, if desired, by an independent
classical coin, and discards the outcomes. These are bounded-support CPTP
update maps. The same-controller instantiation has no persistent clock
or classical controller registers. More generally, measured classical
controller bits can be included as trivial stabilizer ancillas with checks
Z_i; their noise is then included in the SAME CPTP-event class, rather
than declared noiseless. This unchanged theorem covers their measured
Boolean updates as syndrome-conditioned Pauli flips. See
CLASSICAL_CONTROLLER.md for the precise scope and the still-unpaid
classical restoring-history gate. A bounded-local Hamiltonian which is a
function of checks may run continuously. It is scalar in each syndrome
sector.

Add the fixed finite-rate check dephasers

    L_read=Gamma sum_a(M_a-id),
    M_a(rho)=(rho+S_a rho S_a)/2.                           (1)

This is an unmonitored local Lindbladian; equivalently it is the sum of
random stabilizer-kick generators of rate Gamma/2. No external repeated
measurement, accurate global timer or retained readout record is granted.
For analysis only, use the exactly equivalent unraveling in which M_a
attempts occur at independent rate-Gamma Poisson times and have the two
projective Kraus outcomes. The discarded environment carries these
records. Its microscopic realization and errors are physical obligations,
not laboratory resources acquired here.

Unknown errors are state-independent Poisson CPTP events on catalogue
supports X of size <=q with intensities k_X. The event maps are arbitrary
and can be nonunital and jointly coherent on X. By the preceding frozen
ballast theorem this class includes bounded unknown local Markov-generator
errors after an additional fixed, paid depolarizing ballast. It includes
small signed errors in the nominal measurement/update generators through
that same exact representation. No infinite-rate/Zeno limit is taken.

Put

    A(X)={a: supp(S_a) meets X},
    b=max_X |A(X)| <=qD,
    f=max_a sum_{X:a in A(X)} k_X,
    lambda_loc=max_v sum_{X containing v}k_X,
    Lambda=sum_X k_X <=n lambda_loc.                       (2)

Then f<=w lambda_loc. Below assume Gamma>=16bf and b>=1. Zero fault rate is
trivial. Gamma is a fixed constant chosen using a warranted error bound,
not using the unknown maps or observed trajectories. At bounded D,w,q,
this is a constant per-check rate, not a size-growing clock.

## 2. Exact nonpropagation of bra/ket syndrome difference

Consider a term E rho_s F^dagger, with E,F Paulis and rho_s supported in a
single joint syndrome sector. Its bra/ket syndrome difference is

    delta=syn(E)+syn(F).

A nominal Kraus operator has the form P f(S), where P is a Pauli fixed by
its local measurement/coin record. It shifts both syndromes by syn(P),
and multiplication by f(S) only changes a scalar. Thus every nominal
Kraus operation preserves delta. A check dephaser M_a kills the term if
delta_a=1 and fixes it if delta_a=0. Consequently on the delta band,

    L_read=-Gamma |delta|,

and this operator commutes with the entire nominal evolution. Its trace
norm, including an arbitrary reference, decays at least as
exp(-Gamma |delta|t). This is exact at finite Gamma, even if nominal
corrections spread the common classical error far from its origin.

The difference of the two Pauli histories does **not** spread under nominal
correction: a common Pauli conjugates other Paulis only by a phase. Only
actual CPTP fault events can add to its support. The argument is invalid
for arbitrary non-Pauli nominal data gates and is not asserted for them.

## 3. Physical-time Poisson-cut components

Work on a finite storage interval [0,t]. The initial encoder is already
syndrome diagonal. The final logical receiver may dephase all checks;
for a standard syndrome-based logical decoder that dephasing is already
part of its definition. This is one readout, not a repeated external clock.

On each check's time line insert its independent Poisson read times, plus
the two endpoints 0,t. They partition the line into read intervals. Make
a graph whose vertices are the actual fault events. Join two fault events
if they both touch a check a and fall in the same a-read interval. Connected
components of this graph are called coherence components. A fault may
touch several such intervals. Endpoint censoring can only shrink components
relative to the infinite stationary Poisson construction.

This graph depends only on event supports/timestamps and independent read
timestamps. It does not depend on the quantum state or hypothetical Born
outcomes. No such graph needs to be measured or stored by the controller.

## 4. Exact Pauliization on correctable components

Fix all fault/read times, all nominal attempt times/independent coins,
an initial syndrome s, all nominal environmental records and all fault
Kraus labels. Expand each fault Kraus operator in the Pauli basis on its
own X. A word of these Pauli insertions has, along the fixed nominal
record, a scalar amplitude times a final Pauli. Nominal decisions depend
on the fixed record, so their Paulis are common to every contributing word.
Check-Hamiltonian evolution changes only the scalar amplitudes.

Take two Pauli words with nonzero amplitude for this same record. At every
read cut their bra/ket outcomes agree. Therefore the sum of their fault
syndrome differences in every a-read interval is zero. All events touching
that check in that interval belong to the same coherence component.
Consequently, for **each individual component C**, the relative Pauli

    D_C=product_{e in C} P_e^dagger Q_e                    (3)

(ignoring Pauli phases) commutes with every check. Its physical support is
contained in Y_C=union_{e in C} X_e; nominal propagation does not enlarge
this relative support.

If Y_C is an erasure-correctable set, every such D_C is a stabilizer up to
phase, and hence is scalar on every syndrome sector. In particular this
holds when |Y_C|<d. If every component has this property, then all Pauli
words in the fixed record induce the SAME logical Pauli. Coherent sums
only change the positive probability of that record, independently of
the unknown logical input. This remains true with a reference.

For each record choose one contributing Pauli word. The exact conditional
logical channel is a convex mixture of these Pauli-labelled nominal
histories, all with fault labels supported on the original event supports.
No physical knowledge of the representative words is needed. The final
logical channel is therefore Pauli whenever all components are correctable.

### Causality boundary

This is an existence of an offline, support-respecting classical-history
representation. Its Pauli labels can depend on later cuts/records. It does
**not** assert a causal sector Markov process, a thermal rate formula, or
the original Pauli-twirled probabilities. A classical comparison must be
uniform over all Pauli labels on a given event pattern, or must separately
justify admitting this delayed adversary. A causal-only stochastic Pauli
threshold is not automatically sufficient.

For the nominal attempts conditioned above, measurement outcomes along a
Pauli history are deterministic. Any nominal random update choice is an
independent coin included in the schedule. This premise prevents quantum
interference from being silently used to reweight an unconditioned
state-dependent nominal jump process. General Pauli-times-function Kraus
maps alone do not establish that stronger path-law assertion.

## 5. Paid branching and multipoint exposure bounds

Here is an explicit deferred-decisions exploration; it is part of the
theorem, not a mean update-velocity assumption. Under the Palm law of a
fixed root fault, process discovered fault vertices in breadth-first order.
For each of its <=b touched checks, reveal that check's read interval if
it has not already been revealed, and reveal all previously unknown fault
events touching that check inside the interval.

Conditional on the past exploration, a fresh interval around its known
fault time extends left and right by independent rate-Gamma exponential
variables, truncated if it reaches an already revealed read boundary.
This follows from independent increments of each read process; the
unrevealed read process has not been consulted to choose that time.
Previously revealed fault-process portions are not counted again.
On fresh portions, the union of incident fault processes has intensity
<=f. Poisson independent increments/Palm deletion give its conditional
law. Overlaps only reduce new interval length or new discoveries.

Let L_i be the sum of fresh interval lengths exposed while processing one
fault and Y_i the number of newly discovered faults. The exact conditional
domination needed below is

    E[exp(theta L_i) z^{Y_i} | past]
       <=[Gamma/(Gamma-theta-f(z-1))]^{2b},                (4)

for theta+f(z-1)<Gamma. The right hand side is the gamma-Poisson
offspring bound, not an independent-errors assumption about accepted
updates. It remains valid with an arbitrary finite set of inserted root
faults; count those roots as initially discovered rather than offspring.

At theta=0, choose z=Gamma/(4bf). By Bernoulli's inequality,

    E[z^{Y_i}|past] <=(1-1/(4b))^{-2b} <=16/9.

Let

    a=64bf/(9Gamma) <=4/9.                                (5)

If a root component has at least m vertices, the first m-1 processed
vertices must discover at least m-1 children. Iterated conditional (4)
and exponential Markov therefore give

    Pr(|C_root|>=m) <=a^{m-1}.                            (6)

This is an exponential tail with its small fault-rate dependence paid.

More importantly, use z=2 and theta=Gamma/(8b). Then

    E[exp(theta L_i)2^{Y_i}|past]
       <=(1-3/(16b))^{-2b} <=256/169 <2.                  (7)

During a breadth-first exploration with r initially inserted roots, the
nonnegative process exp(theta*total_exposure)*2^{queue_size} is a
supermartingale. Stop at the empty queue and use Fatou. The sum S of all
fresh exposed interval lengths obeys the **multipoint** bound

    E exp[Gamma S/(8b)] <=2^r,
    Pr(S>=u)<=2^r exp[-Gamma u/(8b)].                      (8)

Every component's temporal extent and its latest sealing delay relative
to its earliest fault are at most its exposed interval-length sum. Thus
(8) is a dimension-uniform physical-time restoring-history bound. It is
not obtained from a positive mean clock speed. No global quiet interval,
no noiseless register and no physical history log is used.

## 6. Logical consequences and the actual remaining gate

Set m0=ceil(d/q). Components with fewer than m0 vertices have support
strictly smaller than d. Mecke's identity (or a direct Poisson root union
bound) and (6) give

    P_bad_quantum <=Lambda t a^{m0-1}
                  <=n lambda_loc t a^{m0-1}.              (9)

On the complement the logical channel is Pauli by Section4. On the bad
timing patterns replace it by any Pauli channel. Since each pattern's
conditional evolution is CPTP and its law is input independent,

    distance_to_some_logical_Pauli_channel
       <=2n lambda_loc t a^{ceil(d/q)-1}                  (10)

in diamond norm. The Pauli channel is not asserted to preserve the input.
This result controls logical coherence, not classical logical flips.
It can depend on the horizon and the unknown error maps; the comparison
channels need not form a semigroup or a consistent causal process. No
efficient classical sampler, system identification, or computational
speed advantage is inferred from their existence.

Suppose separately one has a pathwise classical failure event B_cl for
the SAME nominal asynchronous controller/schedule, initial syndrome law
and final decoder: outside B_cl, EVERY Pauli assignment on the actual
fault event supports decodes to identity. This quantifier includes labels
chosen after the schedule is revealed. If Pr(B_cl)<=delta_cl, then the
all-input quantum logical memory error satisfies

    ||Dec exp(tL) Enc-id||_diamond
       <=2delta_cl+2n lambda_loc t a^{ceil(d/q)-1}.         (11)

No causal Markov model for the unknown noise and no perturbed Gibbs
stationarity enter (11). The unproved part for the actual nominal thermal
controller is delta_cl under ongoing arbitrary supported fault events.
Neither static Peierls nor the previous neutral-error stationary proof
delivers it. This package is a clockless quantum-history reduction and
quantitative coherence-restoration theorem, not a claim that this last
classical gate is already acquired.

## 7. Resources and strong ordinary comparison

At fixed D,w,q, the added per-check rate Gamma and support size w are
constants. There are O(n) check dephasers. No global clock, persistent
controller memory, external syndrome log, nor repeated ideal global
measurement is supplied. A final ideal receiver is still part of the
mathematical memory contract and must be implemented/qualified in a
physical claim. Unknown local implementation errors are admitted through
the preceding fixed-ballast Markov-generator reduction at its actual
support/rate cost. A microscopic finite-range reservoir is not acquired
by writing the local Lindbladian; that separate problem is not solved here.

Quantum-error-correction decoherence is an established principle:
Beale--Wallman--Gutierrez--Brown--Laflamme1805.08802v2 proves suppression
of logical coherence by stabilizer syndrome measurements. Tamiya--Koashi
2609.20708v1 gives a coherent-Z code-capacity threshold with ideal syndrome
measurement and noise-aware maximum-likelihood Pauli recovery. Neither
result is silently treated as a restoring threshold for this autonomous
continuous-time noisy controller. Classical reliable asynchronous
computation (Gacs) and localized topological clock repair
(Cook--Gacs--Winfree2008) are strong conventional alternatives; their
classical versus quantum-history and sustained-noise quantifiers matter.
Poisson graphical constructions and branching domination are ordinary
probability tools. World priority of the present composition is UNKNOWN.
