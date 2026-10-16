# Scheduled finite-duration memory with overlapping weak shared-bath pulses

Date: 2026-10-15. Status: composed theorem with independent internal end-to-end reconstruction completed. The quantum subset/support interfaces, classical local-stochastic interface, and their composition pass under the exact stated premises and named contour imports. See SCHEDULED_THEOREM_INDEPENDENT_AUDIT.md. This is not formal certification, independent external validation, or physical implementation qualification.

## 1. Statement

Consider the same sufficiently large compatible 4D toric-code family and fixed ideal decoder as in the reconstructed memory theorem. Replace instantaneous proposals by exogenous independent rate-kappa Poisson STARTS of fixed-total-duration tau gadgets. Each gadget consists of an exact bath-independent completed correction circuit, exact stabilizer-frame insertion, a finite weak local memory-bath pulse, and exact frame removal. Reserve its complete data/check/randomizer/private-ancilla patch throughout that total interval.

Under Sections 2-3 below there are positive small-parameter constants and A,c independent of L,T such that, for every deterministic T>=0, the recovered joint-input channel Gamma_(L,T) obeys

    ||Gamma_(L,T)-Id_logical tensor Lambda_(L,T)||_diamond
       <= min(2, A L^4(1+kappa*T) exp(-cL)),             (1)

for a CPTP bath/auxiliary comparison map Lambda_(L,T). The input is logical tensor the initially arbitrary finite persistent bath; an additional untouched reference is allowed. Tracing the retained bath gives the analogous comparison with Tr_B. A logical-only channel against identity follows with a fixed independent bath initialization.

The smallness requirements involve the external noise ratio nu/kappa, the conflict/latency ratio kappa*tau, and the full joint integrated pulse action a. They are specified through a local-stochastic contour budget in Section 3, NOT by invoking an iid-death theorem for correlated characters.

## 2. Exact physical/mathematical premises

### 2.1 Primitive schedules, patches, and clean classification

All start streams and external local Pauli-noise clocks are exogenous and independent of the quantum input. Durations and internal timing are fixed; neither the clocks nor future primitive increments are controlled by quantum outcomes. Starts include both CSS sectors. A fixed bounded number of correction gates and ideal frame operations is used per attempted gadget, independent of L. Every memory operation has a declared bounded data/ancilla support.

Each start s at location i reserves one bounded patch P_i for the entire interval [s,s+tau]. This includes the full support of syndrome checks, correction gates, error pulse, frame generators, and ancillary resets. Conflict neighbors are all locations with intersecting reserved DATA/ANCILLA resources, with degree at most D, including distinct attempts at the same location. Sharing only the persistent bath does not itself constitute a memory conflict.

An attempt is geometrically bad if another reserved memory/ancilla patch overlaps it during execution, or an external physical noise event touches its reserved resources. At a fixed readout T, every attempt unfinished at T, including unfinished frame removal, is additionally bad. Every skip or abort must belong to these charged bad attempts; arbitrary uncharged skips are excluded. Every actually clean attempt receives genuinely fresh reset local ancillas, with prior correlations removed, before execution.

Bad/conflicting/dirty/pending gadgets may contain arbitrary local operations and arbitrary persistent-bath interactions on their declared memory patches. Every such memory action remains within that attempt's declared total interval [s,s+tau]; no uncharged delayed tail or post-reset memory interaction is allowed. They are not collapsed into bounded overlap components. Their actual gates or continuous local interaction terms remain in chronological order and have locally finite, well-defined evolution. Any operation touching a supposedly clean reserved memory patch during its interval belongs to that clean gadget or invalidates cleanliness. Ancilla resets cannot secretly spread corruption outside their declared patches.

At time zero there are no in-flight attempts and local ancillas are reset. Different startup conventions require explicitly charged boundary strips and an admissible initialized prefix. At time T actual pending prefixes are retained; no correction, pulse, or frame removal is completed fictitiously.

### 2.2 Exact correction and exact frames

The clean correction is the original COMPLETED C_i, including its inactive Kraus branch. Its implementation is exact for every input entangled with exterior systems. Every internal correction gate acts only on data plus fresh private ancillas and acts as identity on the persistent bath. Private correction records are discarded/reset; no hidden retained correlation may later recouple outside the declared implementation. This is stronger than agreement of an isolated reduced-memory channel with C_i.

Correction occurs first. Then an ideal stabilizer frame g_i is inserted, held during the finite pulse, and removed before the gadget completes. Frame insertion/removal must be exact atomic operations or separately justified exact bath-independent local gates whose support/timing is included in the reservation. Generic correction gates need not be individually stabilizer covariant because the frame is inserted only AFTER the exact correction.

The finite abelian group G_i consists of code stabilizers detecting the full syndrome of all Paulis in the pulse error patch A_i. No nontrivial logical Pauli is supported in A_i. The error patch and full frame support are contained in P_i. Fresh frame seeds are independent and uniform, independent of the initial joint input and of the couplings being randomized. Their explicit registers are private and inaccessible to subsequent dynamics. The final Fourier labels introduced below are mathematical labels, not causal controller information.

### 2.3 Weak pulse and shared-bath model

Fix a finite horizon, the full EXOGENOUS primitive schedule/noise record h, and the seeds of all geometrically bad or pending attempts. Select only frames of geometrically clean completed attempts for the Fourier analysis. On one common finite-dimensional unitary dilation, the toggling-frame Hamiltonian has the additive form

    H_g(t)=H_0(t)+sum_(selected i) V_(i,g_i)(t),
    V_(i,g_i)(t)=(g_i tensor I_B) V_i(t) (g_i^dagger tensor I_B),
    integral sup_(g_i) ||V_(i,g_i)(t)|| dt <= a.

Each V_i is supported on A_i tensor the persistent bath during its own finite pulse interval. Pulses can overlap in time and have arbitrary noncommuting shared-bath coefficients. No bath operator is assumed to commute with another. Strong frame-independent bath-only evolution may remain in H_0. All OTHER memory-coupled terms must already be one of the declared ideal operations, external noise, or charged local bad/pending operations; an uncharged arbitrary memory Hamiltonian in H_0 is not allowed by the support premise.

The only explicit dependence on selected g_i is in its displayed term. Deleting or interpolating any selected terms must preserve this property in the SAME whole dilation. No controller, initialization, hidden seed readout, final projection, or changed feedback rule may retain an uncharged dependence on a deleted frame. Genuine outcome-controlled operations are allowed only if represented by fixed frame-independent controls on retained records in this common dilation, uniformly under all deletion/interpolation settings. A collection of separately conditioned or calibrated branch models does not suffice.

The action bound and locality statement hold uniformly in h, unselected seeds, and all initial joint states. Actual generated measurement/controller/dilation outcomes remain inside the common dilation and are SUMMED at the CP-effect level. One must never normalize a postselected endogenous branch and assert the same small-probability bound for it.

Finite-dimensional baths and local resources are assumed. Finite-horizon Stinespring environments can be discarded; no unbounded externally retained record register or infinite-dimensional bath extension is claimed.

## 3. Explicit coarse probability budget

Apply the following coarse construction separately to each CSS sector, taking worst-case constants and the smaller q_star where needed. Each sector counts starts/noise from BOTH sectors whenever they can affect its guarded support. The final escape event is the union of the two sector escapes; its factor of two is absorbed into A. Thus delta_ideal below is the per-sector slow+fast bound, not an implicitly uncharged joint-sector event.

Choose the enlarged geometry, attractive coarse rule, packet graph/connectivity and its coloring count Q before choosing the block size b. Q is uniformly bounded over L and b in the allowed range. Let Delta=Cb/kappa, with Cb>=1, and assume x=kappa*tau<=1. Let N count guarded gadget locations, F count all guarded elementary external-noise locations, and nu bound their aggregate rate per elementary location. Both sectors, all relevant data/ancillas, and every enlarged frame/pulse support are counted.

Let delta_ideal be ONLY the original slow-certificate plus fast-word bound at the unchanged original START rate kappa. No noise term is included in delta_ideal. A conservative base-flag marginal is

    d0 = delta_ideal
          + 2DN kappa^2 tau (Delta+2tau)
          + F nu (Delta+2tau)
          + N kappa tau.                              (2)

The last term is the bound for a LOCAL terminal flag: candidate starts in the slab's [t-tau,t+Delta] window intersected with [T-tau,T]. The event is empty in nonintersecting slabs. It is never one unrestricted global terminal event reused in every slab. Startup is free under Section 2.1; extra startup strips change (2).

A guarded completion birth has a parent in a window of length at most Delta+2tau, so its expected candidate-parent count is bounded by

    mu = kappa N (Delta+2tau).

The joint subset effect theorem gives actual global-character subset probabilities at most a^(2|S|), conditional on ALL exogenous primitives and fixed unselected seeds, uniformly over initial inputs. Summing/averaging unselected seeds preserves that bound. The full-primitive version of the local-stochastic packet lemma therefore gives

    P(all B_v=1 for v in W) <= q^|W|,
    q=(d0+a^2 mu)^(1/Q)                               (3)

for every finite set W of distinct coarse spacetime sites. No sequential conditional-character bound or iid-mark coupling is used.

Let q_star be the sufficiently small death-subset tolerance of the correlated-death contour theorem for the fixed rule and connectivity. Require

    d0+a^2 mu <= q_star^Q.                            (4)

A simpler sufficient numerical recipe is

    delta_ideal+A0*(nu/kappa)+B0*(kappa*tau)+C0*a^2
        <= q_star^Q,
    A0=F(Cb+2), B0=N[2D(Cb+2)+1], C0=N(Cb+2).          (5)

First choose the geometry and q_star,Q; next choose b so delta_ideal fits a strict portion of (4); finally choose the physical ratios/action to fit the remainder. This order is noncircular. N,F and the displayed constants may be extremely large. For data-only original X/Y/Z rates, nu<=2sigma, where sigma=max(lambda_X+lambda_Y,lambda_Z+lambda_Y); ancilla noise must be added explicitly.

For fixed nu,tau,a, the two rate-dependent terms in (5) have unconstrained minimum 2sqrt(A0 B0 nu tau). The optimizing kappa must also satisfy all admissibility constraints. Thus this conservative recipe needs an adequate remaining budget after C0*a^2; its failure is not a device-impossibility theorem.

## 4. Proof chain, with the probability and support steps separated

### A. Exact corrections and arbitrary bad operations

Condition on h. Move ONLY clean exact correction-circuit gates to their parent starts by adjacent commutations. They are bath-independent and all intervening memory operations are disjoint from their reserved resources. Retain weak pulses and bad operations in their actual chronological positions; shared-bath channels are never commuted. At an omitted bad start the auxiliary support envelope uses the atomic update sat_(S_i) composed with F_i, which dominates the unchanged actual support. No arbitrary bad map is factored after a noninvertible C_i.

### B. Global Fourier subset effects

Fourier-transform the private selected frame tuple over the whole experiment. Its coefficients, refined by ordinary dilation output indices alpha, form a complete full-horizon Kraus family K_(h,chi,alpha). Here alpha also includes the unselected independent frame-seed record with the square roots of its averaging probabilities absorbed into the Kraus operator; equivalently one explicitly integrates those seeds. Completeness and the displayed effect inequality are asserted after that averaging and summing the dilation indices. For every specified subset S of selected distinct parents,

    sum_(chi: all chi_i!=0 on S) sum_alpha K^dagger K
       <= a^(2|S|) I.                                (6)

The audited proof uses mixed Duhamel derivatives, independent frame-coordinate L2 projections, and Parseval. The permutation simplices partition the insertion-time cube, so there is no factorial loss. Equation (6) is a joint effect bound, not a causal instrument or a bound conditioned on earlier character outcomes.

### C. Full-horizon support histories

For fixed h,chi and a fixed unnormalized dilation record, expand local interactions into memory Paulis with chronological auxiliary/bath coefficients. Move ONLY memory Pauli factors from a clean pulse to its completion; every intervening memory operation is disjoint by full reserved-patch cleanliness. Never reorder any bath factor. The product Pauli for that pulse has its selected character chi_i and lies in A_i. Detection completeness and no local logical permit replacement by a fixed representative P_(i,chi_i), up to a patch stabilizer and a syndrome-dependent scalar absorbed into the auxiliary coefficient. Choose P_(i,0)=I.

Every term of that global Kraus operator therefore has exact clean corrections at starts, charged arbitrary bad/pending local Paulis, omitted corrections at bad starts, and one representative birth at each nonzero clean character's completion. Its zero-character completions create no support. This is an operator expansion and universal support certificate, not a chronological local-channel factorization or physical Pauli mixture.

### D. Local-stochastic contour and torus estimate

Apply the full-primitive packet lemma to (6), obtaining (3). The correlated-death contour proof uses distinct sinks in a disjoint contour family, whose joint occurrence probability is bounded by q to their total number. Exponential contour-chain enumeration yields anchored exponential spacetime zero-component tails. Its named deterministic imports remain SST arXiv:2202.10999v1 Theorem 7/Lemmas 13-14 and HT arXiv:2212.08437v2 Lemma 9.15; the iid Corollary 9.5 is not silently applied to correlated characters.

For each prospective torus first-crossing anchor, copy the native coarse death flags in its fixed injective witness patch and set all other flags to zero. This preserves the subset bound without an independent mark extension. The deterministic closed-ancestor replay, whole-slab cover, and bounded-event accumulated-homology argument then give

    P(no-escape predicate fails) <= C L^4(1+kappa*T) exp(-cL),

uniformly over initial joint states.

### E. Actual global-record good subchannel

Define G(h,chi) to be that fixed robust no-escape predicate, using the actual exogenous records, actual GLOBAL Fourier characters, all allowed bad-gadget patches, and skipped-start saturation. It is independent of the quantum input, bath coefficients, and any analysis coupling. It certifies EVERY Pauli term in each selected actual global Kraus record.

After the fixed final decoder, sum actual record maps with 1_G. This defines a CP trace-nonincreasing map Good=Id_logical tensor Lambda_g. Its complement Bad is CP. The uniform probability bound controls Bad^*(I); trace preservation implies this effect is I_logical tensor D_B. Add any CP bath map with effect D_B to Lambda_g to obtain a CPTP Lambda_(L,T). The CP-norm argument bounds the difference by twice the escape probability, yielding (1) after absorbing constants and imposing the trivial maximum 2.

No postselection is normalized in this argument. The global Fourier record is a legitimate final Kraus representation even though no small chronological character instrument exists.

## 5. What is finite-duration, what remains ideal

The clean syndrome-correction circuit and its weak error pulse have nonzero total reserved duration. Weak pulses can overlap in time on disjoint memory patches and interact through a common noncommuting persistent bath. Their net support histories are assigned at completions only in the proof.

Poisson START clocks, fixed timing/reservations, exact completed correction gates, exact private stabilizer frames, actual fresh reset, the qualified additive Hamiltonian/deletion structure, ideal encoding, and fixed perfect final recovery remain assumptions. The theorem supplies no autonomous finite controller, faulty-timer theorem, frame-error qualification, arbitrary continuous-bath robustness, leakage theorem, useful numerical threshold, practical 3D embedding, or physical time-independent Lindbladian realization. It makes no priority claim.

The readout guarantee is pointwise for each deterministic T. Pending classification changes with T. There is no asserted single physical Pauli/homology trajectory during coherent gadgets, no all-times escape event for actual intermediate coherent states, and no adaptive stopping-time guarantee.

## 6. Source and audit map

- Finite-duration serialization/flags: ../finite_duration_bridge/LIMITED_START_CLOCK_THEOREM.md and INDEPENDENT_BRIDGE_CHECK.md.
- Global joint effects and support locality: ../continuous_bath_obstruction/SUBSET_MOMENT_AND_LOCALITY_PROOF.md and SUBSET_CHARACTER_AUDIT.md, with COMPLETION_LOCALITY_AUDIT.md verifying the support bridge.
- Local-stochastic contour bridge: SUBSET_BOUND_CONTOUR_BRIDGE.md, including its explicit noninjective embedding/support-size conversion and cold-field convention; independent audit in INDEPENDENT_AUDIT.md.
- Base memory/common-decoder imports: ../memory_domination_review/GATE_STATUS.md and the named support, forcing, homology, torus and quantum-interface modules there.

The independent end-to-end composition audit is SCHEDULED_THEOREM_INDEPENDENT_AUDIT.md. It checks the full-primitive subset effect, enlarged supports, per-sector union, unselected-seed averaging, no delayed tails, contour budget, and CP completion. No remaining internal mathematical clarification is identified within these premises; the named imports and implementation qualifications remain explicit dependencies.
