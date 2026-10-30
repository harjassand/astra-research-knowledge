# Bounded-deadline single-shot channel cells: exact instrument and honest threshold interface

2026-10-29, begun21:25 UTC. This is a **scheduled** implementation interface, not an autonomous computer. It changes the failed successful-update timing contract by terminating every cell after a fixed physical exposure time.

## 1. Exact single-shot channel, without an unnecessary Feynman chain

For a bounded-support CPTP map Phi(rho)=sum_s K_s rho K_s^dagger, use clock states |0>, |s> (s=1,...,m), and a dark |D> (DONE). Define

    V=sum_s K_s tensor |s><0|,
    H=g(V+V^dagger),
    L_s=sqrt(kappa) I_data tensor |D><s|.

DONE is not coupled by H. Thus a terminal emission cannot initiate another application. Start the clock in |0>. With an arbitrary entangled data/reference/bath input, the clean no-emission isometry at time t is

    M_0(t)=a(t) I tensor |0> + b(t) sum_s K_s tensor |s>,
    a'=-ig b,  b'=-ig a-(kappa/2)b,  a(0)=1,b(0)=0.

The amplitudes are scalar and independent of the data. The no-emission survival is

    q(t)=|a(t)|^2+|b(t)|^2.

At the fixed deadline tau, measure DONE versus not-DONE and trace/reset the private clock. The exact complete data/flag instrument is

    SUCCESS: (1-q) Phi,
    MISS:    |a|^2 Id + |b|^2 Phi =q R,
    R=(|a|^2/q)Id+(|b|^2/q)Phi.

This includes the genuine pending-operation state on the MISS branch; it is not silently replaced by the ideal output. Both normalized branches are CPTP, their traces are input-independent, and the sum is trace preserving. If Kraus labels are retained, the successful instrument resolves the corresponding K_s branches. A missed cell can conservatively be treated as an arbitrary local fault; no postselection is used.

For example, at g=kappa/4,

    q(t)=exp(-kappa t/2)[(1+kappa t/4)^2+(kappa t/4)^2].

No resonant pulse-area deadline is required: any sufficiently late deadline makes q small. The exact Phi still depends on the intended ratios/operators in the K_s coupling. Calibration error in those operators is physical noise, not cured by waiting. Exact critical damping is only a convenient formula, not a requirement: every g,kappa>0 gives q(t)->0 exponentially, uniformly on compact positive parameter ranges.

## 2. Finite-rate preparation, not a perfectly prepared clock assumption

A private clock can be prepared during a separate fixed window sigma using the one-body replacement generator

    kappa_p (R_0-Id),  R_0(rho)=|0><0| Tr(rho).

It has bounded one-clock Lindblad operators sqrt(kappa_p)|0><j| for every clock basis label j, including j=0. The total jump intensity is kappa_p I. Its exact instrument is: no replacement with probability q_p=exp(-kappa_p sigma), or at least one replacement with probability1-q_p, after which the clock is ready and uncorrelated with all data/baths in the clean model. This works for arbitrary initial clock states and clock-bath correlations.

Keep the preparation-failure tag as part of the analysis instrument; it need not be used for postselection. On the successful-preparation branch the preceding cell instrument applies. Charge preparation failure as an arbitrary local fault, with clean intrinsic bad probability

    q_0=q_p+(1-q_p)q(tau).

A failed preparation need not have bounded effects unless the cell is physically disabled at its deadline; that requirement is explicit below. This preparation primitive is an ideal supplied one-body reservoir operation subject to the same additional bounded local noise as the other clock operations. It is not a microscopic derivation of a reservoir.

## 3. Spatial/circuit interface that must actually be provided

Use conventional bounded-support FT circuit locations. Within a layer, active cells have disjoint data+private-controller supports. All controller/data interactions belonging to a cell are disabled at the common deadline, regardless of the private clock state. The next layer starts after the prescribed preparation/operation/output windows. Ancillas are not allowed to carry an uncharged active interaction into future cells. Storage/idling qubits are circuit locations too, exposed for the same fixed cycle duration Delta.

This hard exposure bound is what prevents the marching-soldier delay cone. A MISS does not postpone the rest of the circuit. Every intended gate location has duration at most Delta, independent of system size, previous successes, or computational runtime.

External enable/disable, clock preparation, DONE sensing, and any flag routing are additional scheduled local operations. Their target actions and perturbation budgets belong in the same circuit location or explicit neighboring control locations. If a small fault in an internal enable bit can leave an O(g) interaction running forever, the promised block interface is false and the threshold transfer below is not established. Calling that controller 'equally noisy' is not a proof of fail-safe disabling. A trusted external schedule, or an independently fault-contained classical control implementation, is still a resource.

## 4. Exact mixed fault-map contract: cell-contained local noise

Here is a clean sufficient version, with its locality restriction stated rather than hidden. Each physical noise term during a layer has system support inside one active cell (or one idle location); its bath operators may act on an arbitrary shared retained bath. Include Hamiltonian terms -i[h_e(t),.] and added bounded Lindblad terms. Multiplying any subset of their strengths by numbers in[0,1] must leave CPTP dynamics. Let

    epsilon_j=integral_cell j sum_e ||N_e(t)||_diamond dt <=eta Delta.

The diamond norm is on the augmented system+bath space. No bath reset or Markov approximation for that bath is used.

Expand the actual complete instrument in physical noise insertions. A location is bad if it contains at least one physical noise insertion, or, with no such insertion, its clean preparation/operation instrument has an intrinsic failure. A good location implements exactly Phi, accompanied by its clean private-clock/record state, with its scalar clean success weight. This is an ordinary coherent superoperator fault expansion, not a probability assertion about the signed insertion terms.

For every fixed set S of marked circuit locations, the inclusive map summing all paths bad at each j in S satisfies

    ||F_bad(S)||_diamond <= product_(j in S)(q_0,j+epsilon_j).      (1)

### Proof of the mixed bound

Partition the marked set into A (locations with physical insertions) and B=S\A (locations with no insertion but intrinsic failure). Set the perturbation groups at B to zero, impose their clean failure instruments, and leave all unmarked perturbations present. The sum with at least one insertion in every location in A is the multivariate finite difference in the A noise strengths. Its Duhamel mixed derivative inserts one N_j at an arbitrary physical time for every j in A, with full CPTP interpolated evolution between insertions, as in PHYSICAL_TIME_FAULT_INSERTIONS.md.

Every clean B failure instrument has induced completely bounded trace norm at most q_0,j, independent of its incoming data/bath state. Because no insertion touches that cell, the scalar input-independent clean-clock factor can be pulled out even in the presence of arbitrary outside/bath dynamics. Clean cells in the same layer have disjoint system support; the only outside evolution acting on their entanglement partners commutes with their clean local dynamics. Earlier/later circuit operations are norm-one CPTP propagators. Repeatedly contracting these complete clean cell instruments therefore supplies product_B q_0,j. The remaining time-ordering integrals supply product_A epsilon_j, with no volume/runtime factor. Sum over all A subset S to obtain (1).

This proof retains the final SUCCESS/MISS records and all bath correlations. It never conditions/renormalizes on a rare clock history. Intrinsic clock failure and physical noise need not be assumed statistically independent. If only a perturbation norm but not a physical CPTP interpolation is available, use a separately proved expansion bound instead; the root's broader signed-generator controller theorem does not automatically imply (1).

For a single cell an entirely elementary fallback is

    ||E_actual-G_ideal||_diamond <=2q_0+eta Delta,

where G_ideal is the intended channel with SUCCESS flag. This follows from the exact convex clean instrument and Duhamel contraction. Equation(1) is the stronger inclusive multi-location statement under the displayed support/interface assumptions.

## 5. General finite-range noise: do not omit cross-cell supports

A physically local Hamiltonian term may touch several simultaneous gate cells. Such an insertion must be charged to **every** touched location, or to one bounded-size correlated location. The cell-contained theorem above does not cover it by relabeling the term as one-cell noise. Bounded geometric range/degree limits the number b of touched cells, but a complete threshold statement must use a bounded-spread correlated-location version of the FT theorem (and the corresponding packing/cluster bound), or redesign spacetime buffers so noisy interaction supports fit the chosen rectangles. The scalar expression q_0+eta Delta per arbitrary marked gate is not justified unchanged when b>1.

## 6. Consequence and limits

For the cell-contained model, choose fixed sigma,tau so q_0 is below a conventional FT local-noise tolerance, then choose fixed eta so q_0+eta Delta is below that tolerance. All rates and window lengths are constants independent of system size and runtime. Every controller is included in the noise budget; success does not certify that physical noise was absent, and is not treated as heralded perfect computation. A conventional FT circuit with the requisite local-noise theorem can then use these cells as its noisy locations. Storage noise is charged for the entire Delta, not just for the random successful operation time.

This is a substantive **finite-rate, deadline-tolerant channel implementation contract**, but principally a corollary of ordinary CPTP/Stinespring synthesis, terminal-clock constructions and conventional fault tolerance. It trades precision pulse-area timing for fixed deadline controls, dissipative reset resources and calibrated channel couplings; it does not eliminate control, calibration, entropy export or fault-tolerant gadgets. Arbitrary whole-block recovery channels must not replace internally fault-tolerant gadgets: a single physical fault inside a large recovery cell can corrupt its full support.

No fully autonomous scalability theorem follows. The original autonomous memory/computation objective remains harder: it must acquire the hard deadline/control interface autonomously without reintroducing persistent uncharged controller faults, or prove a code tolerates actual physical-time delay clusters.

## Primary comparators

Conventional retained-bath FT: Terhal–Burkard, https://arxiv.org/abs/quant-ph/0402104; Aliferis–Gottesman–Preskill, https://arxiv.org/abs/quant-ph/0504218. Exact Stinespring/channel-cell semantics and the full-bath physical-time Duhamel contract are already present in the shared root/bridge files. This report makes no historical novelty claim for the single-shot damped cell or its scheduled threshold corollary.

## 7. Repair of section5: an explicit bounded-spread hyperedge fault bound

The following supplies the missing cross-cell accounting, rather than invoking it as a black box. Split physical noise into fixed slab/support groups e. Every group touches at most b circuit cells; every cell is incident to at most D such groups; and each group has integrated augmented diamond-norm budget <=epsilon. These are fixed constants under bounded range, bounded local degree and a fixed finite grouping of physical supports. All physical terms sharing one support can be grouped by summing their norms. Split a term crossing time-layer boundaries into separate time groups.

For a Dyson path write x_e=1 if it contains at least one insertion from group e. These are formal path labels, not classical noise probabilities. A marked cell is bad if some touching group has x_e=1, or if all its touching groups have x_e=0 and its clean intrinsic failure occurs. For every finite marked cell set S the inclusive bad map obeys

    ||F_bad(S)||_diamond
       <= [q_0+(2^D-1) epsilon^(1/b)]^|S|,   0<=epsilon<=1.  (2)

### Exact coverage bookkeeping

First partition S into B, the cells having no touching noise insertion but an intrinsic failure, and C=S\B, the cells touched by noise insertions. Set every noise group incident to B to zero and impose B's clean failure instruments. This is an exact restriction on Dyson histories, not conditioning by their probabilities. The groups still available to cover C have incidence at most D and size at most b.

The Boolean coverage indicator is

    f_C(x)=product_(j in C) [1-product_(e incident to j)(1-x_e)].

Expand and multilinearize using x_e^2=x_e. Before collecting coefficients there are at most (2^D-1)^|C| signed monomials. Every surviving/raw monomial selects a group set T that covers C, and therefore |T|>=|C|/b. A monomial product_(e in T)x_e selects exactly the inclusive physical fault sum for T, with all other allowed groups unrestricted. The mixed Duhamel proof, with the clean B failure instruments imposed, bounds its diamond norm by

    q_0^|B| epsilon^|T| <=q_0^|B| epsilon^(|C|/b).

The clean B factor is justified because all groups touching B were disabled, their private-clock failures have uniform input-independent instrument norm q_0, and outside dynamics cannot enter the clean cell during its fixed window. Shared retained-bath correlations do not alter that local clean instrument. Triangle inequality over the signed monomials then gives

    q_0^|B| [(2^D-1)epsilon^(1/b)]^|C|.

Finally sum over B subset S, giving (2). The argument never assumes norm monotonicity on dropping marked coherent faults; such a monotonicity would be false in general. It also never treats a multi-cell physical insertion as independent faults.

This is a conservative bounded-spread superoperator fault contract. The constants may be poor, but for fixed b,D and fixed deadlines its strength tends to q_0 as physical noise goes to zero. Choosing q_0 below a conventional circuit threshold and then epsilon sufficiently small yields a mathematical scheduled FT interface. The fault-tolerant gadgets and code must match the chosen bounded-size physical locations; large internally non-FT recovery hubs are still excluded. The externally enforced deadline/disable and output-control costs remain exactly as in section3.
