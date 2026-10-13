# ASTRA FRONTIER — Payoff-certified exclusion under common experimental access

**Date:** 13 October 2026.  
**Status:** Mathematical construction, exact rational finite-device certificates and numerical falsification checks. No independent proof review, formal verification, historical-priority clearance or physical experiment. Quantum state exclusion, minimax measurement design, residual certification and Hamiltonian discrimination speed bounds are established ideas and are explicitly credited. The present contribution is a constructive, resource-accounted combination for an interacting control problem and a comparison against all acquisition protocols under the specified access budget.

## 0. Result and scope

The preceding result used one selected contrast that could not identify two model parameters. That did not bound a learner allowed to choose another measurement. This investigation changes the comparator: every learner may choose its preparation, ancillary systems, known controls, adaptive feedback and readout, but has the same total exposure to the unknown phase-sensitive Hamiltonian.

For the finite interacting four-site device below, a single interrogation of duration pi/4 followed by a three-outcome measurement selects a nominally optimal allowed control with probability at least 0.99819460749. With finite phase/drain actuation error, the same event has throughput regret below 0.000003085217. Worst-case expected regret is below 0.000094185535.

In contrast, no protocol with total unknown-link exposure at most pi/4 can identify the phase with uniform success probability 0.99. Its worst-case identification failure is at least 0.011031161767. This lower bound permits arbitrary known controls and ancillary processing; it is not a comparison restricted to one chosen contrast. It concerns acquisition before choosing the action. Subsequent operation of the device is not free retrospective sensing.

Every no-observation, possibly randomized choice from the same nine controls has worst-case expected regret at least 0.016009727377. This is a risk comparison, not a runtime or sample-complexity speedup factor.

The output is the stationary particle throughput of a driven four-site hard-core device, **not the previous infinite-chain coefficient D**. The smaller device permits a rigorous fair-access test; it does not make general macroscopic quantum matter tractable. The three-valued fresh phase-fault promise, finite nine-action menu, calibrated pure dephasing, finite control precision and preparation/readout requirements are load-bearing. A continuous unknown phase or an unrestricted actuator menu is not covered.

Six fresh robust response-family constructions, exact checking, probe compilation and decision checking took 6.2948 seconds including imports in the recorded process, with 135,588 KiB peak resident memory (about 132.4 MiB), one BLAS thread. The model and probe family were selected during exploration, excluded from that timing. The final response coefficients were computed from scratch. Later independent-of-optimizer rebuilding and tests took 12.2117 seconds. These are container observations, not hardware-independent complexity guarantees.

## 1. The mathematical object is not generally a partition of models

For model theta, let

    G_theta(epsilon) = {u : max_v J(v,theta) - J(u,theta) <= epsilon}

be its acceptable action set. A decision only requires choosing an action in the true model's set. It need not identify theta.

Pairwise sharing an acceptable action is not transitive in the sense required for a partition. Three models can have acceptable sets {1,2}, {0,2}, {0,1}: any two share an action, but all three do not. A model-equivalence quotient loses this overlap. The appropriate finite combinatorial object is the collection of **minimal incompatible families** of acceptable sets.

### Proposition 1 — minimal decision conflict equals state exclusion

Suppose a finite family G_1,...,G_q has empty intersection and every proper subfamily has nonempty intersection. Fix an allowed acquisition strategy and its output states rho_1,...,rho_q. Then the optimal worst-case probability of choosing an unacceptable action equals the optimal worst-case probability of mistakenly excluding the true state.

**Proof.** For every action u choose one index i(u) such that u is not in G_i(u). Such an index exists because the full intersection is empty. Any action-valued measurement can be coarse-grained by i(u). Under true model i, the probability that this coarse-grained measurement excludes i is at most the original probability of an unacceptable action. This proves that optimal exclusion error is no larger than optimal decision error.

Conversely, choose u_i in the intersection of all G_j with j different from i. Minimality guarantees existence. Necessarily u_i is not in G_i, or it would belong to the full intersection. On exclusion outcome i, choose u_i. Under true model j this action is unacceptable exactly when i=j. The two error vectors are identical. This proves the reverse inequality. The argument also applies after optimizing over a common set of acquisition strategies. QED.

This is a task reduction into known quantum state exclusion [1], not an invention of that measurement problem. The general family may have many incompatible subfamilies; finding and resolving all of them can itself be expensive.

An elementary boundary follows from Helly's theorem: for convex acceptable sets in p real control dimensions, any finite minimal incompatible subfamily has at most p+1 elements. For intervals, the minimal conflict has two models, and zero-error exclusion of two nonorthogonal pure states is impossible, just as zero-error identification is. Multiway overlap, or nonconvex/discrete action structure, can change the information requirement. This observation does not make general nonconvex global optimization easy.

### A constructive minimax measurement problem

Given computed losses L_(a,theta) and output states rho_theta, a decision measurement solves

    minimize t
    subject to E_a >= 0, sum_a E_a = I,
               sum_a L_(a,theta) Tr(rho_theta E_a) <= t for all theta.

The dual uses a probability distribution pi on models and a Hermitian Y satisfying

    Y <= sum_theta pi_theta L_(a,theta) rho_theta for every action a,

and maximizes Tr Y. Weak duality follows immediately by multiplying by E_a, tracing and summing. In finite strictly feasible instances, ordinary SDP duality gives equality. Interval losses and state errors must enlarge the constraints; they are not assumed exact.

The numerical package does not invoke a general-purpose SDP solver. The covariant example below is solved analytically, with its inequalities verified from the actual physical loss table. General decision-oriented experiment optimization and exclusion SDPs are prior work [1,4,5].

## 2. The interacting physical task

There are four hard-core sites 0,1,2,3. Each carries occupation n_i=|1><1| and lowering operator s_i. Let

    H_phi = -sum_(i,j) in {(0,1),(0,2),(2,3)} (s_i^+ s_j + h.c.)
            -(exp(i phi) s_1^+ s_3 + h.c.) + V_xi,

    V_xi = U_L n_0(n_1+n_2) + U_R n_3(n_1+n_2)
           + W n_1 n_2 + Z n_0 n_3.

The four unknown interaction coefficients obey

    xi=(U_L,U_R,W,Z) in (4,3,1,2)+[-1/25,1/25]^4.

They are neither set to zero nor treated as a small interaction perturbation about a free Hamiltonian. The robust local parameter expansion is about this strongly interacting center, and its entire error is verified.

The physical Schrödinger generator is

    L_(phi,kappa,xi)(rho) = -i[H_phi,rho]
       + (2/5) D[s_0^+](rho) + kappa D[s_3](rho)
       + (d/4) sum_(i=0)^3 D[Z_i](rho),      d=1/100,

where D[L](rho)=L rho L^dagger - {L^dagger L,rho}/2. The actual physical dephasing is retained; no artificial noise is added. Units have hopping t=1 and hbar=1.

The target is the steady throughput

    J(phi,kappa;xi)=kappa Tr(n_3 rho_ss).

The system is driven, and this is a finite-density nonequilibrium output. The all-charge-sector, number-neutral density-matrix space has dimension sum_q binomial(4,q)^2=70. A neutral steady state exists by twirling a steady state under the conserved global phase symmetry of the generator. The verified trace-normalized inverse below makes it unique within that space, so every steady state has the same throughput. No numerical gap promise is used.

At the nominal good setting, floating diagnostics put approximately 29.40% of the stationary probability at occupation number at least two. Approximately 0.0949785 of the 0.2282292 throughput arises from sectors with at least two particles. The same device with all diagonal interactions removed gives throughput about 0.2784894. These are diagnostics, not the exact bounds used for the theorem. They make explicit that the output calculation is not replaced by a one-particle model.

Interference-controlled transport and dark states in small quantum devices are established phenomena [6]. This model is a possible engineered excitation-transport device, not a validated description of a specific quantum-dot or material experiment.

### Fresh phase uncertainty and action menu

After common device characterization, a fresh, persistent phase fault is promised to be

    theta_j=2 pi j/3,  j=0,1,2.

The possible commands are

    alpha_a=pi-theta_a in {pi, pi/3, -pi/3},
    kappa in {2,4,8}.

There are nine allowed nominal controls. The actual flux is phi=theta_j+alpha_a. If a=j the flux is pi; otherwise it is plus or minus pi/3 modulo 2pi.

The fault is fixed during acquisition and later device operation. Pre-fault characterization does not identify the new fault. No unknown-phase-sensitive observations made after the fault may be omitted from the exposure budget.

An arm swap 1<->2 followed by the gauge exp(i phi n_3) maps H_phi to H_-phi. It preserves all four interaction templates, injection, drain dissipation and dephasing. Consequently J(phi,kappa;xi)=J(-phi,kappa;xi), uniformly in the full uncertainty box.

Write g_kappa=J(pi/3,kappa;xi), b_kappa=J(pi,kappa;xi). The two nonmatching phase commands have the same ideal payoff. Exact calculations below establish that g_4 is the largest of all six payoff types throughout the box. Hence each phase model has two equally best allowed actions, and the three acceptable sets form the minimal conflict in Section 1.

This is an optimum **within the stated nine-action menu**. Nothing here asserts that pi/3 is globally best among all continuous fluxes, or that drain rate 4 is globally best among all positive rates.

## 3. Constructing the robust physical loss table

A guessed loss function would defeat the purpose. The physical loss table is constructed with a finite rational residual certificate.

Vectorize all |a><b| with equal occupation number. Replace one generator row with the trace equation. The resulting square matrix A(theta) has dimension 70 and right-hand side e_0. It includes all number sectors, not just the single-excitation sensor subspace.

For each of the six phase/drain types, the program computes a total-degree-six trial polynomial in six variables: four interaction deviations, phase actuation error, and drain actuation error. There are binomial(12,6)=924 coefficients, each a 70-component complex vector. The allowed actuator deviations are

    |zeta_phi| <= 1/4096,    |zeta_kappa| <= 1/4096.

The first four variables have radius 1/25. The phase exponential is retained to degree four, with an explicit fifth-order remainder; uncertainty in sqrt(3) at pi/3 is enclosed rationally. All matrices used by the exact checker are integer numerators over a common denominator.

A floating inverse R and polynomial trial x are proposals only. Their entries are rounded to rational dyadics. The checker proves

    ||R A(theta)-I|| <= q < 1

uniformly over the box. It uses an exact Frobenius upper bound on the reference residual, a joint 16-vertex norm bound for the four interaction perturbations, and explicit phase/drain/remainder bounds. Therefore

    ||A(theta)^-1|| <= ||R||/(1-q).

It regenerates the full residual r(theta)=A(theta)x(theta)-e_0, including every polynomial coefficient above the trial degree, and obtains a uniform norm bound. Then

    |J(theta)-J_trial(theta)|
       <= 3 (kappa+1/4096) ||R||/(1-q) ||r(theta)||.

The coefficient 3 bounds the Euclidean norm sqrt(8) of the drain-occupation functional. This is an inverse bound derived and paid for on this finite device, not a supplied many-body gap or a scalable large-system theorem.

The resulting q bounds range from about 0.469 to 0.828. The largest uniform scalar error among the six cases is below 2.404e-7. The small trial errors do not imply that different parameter values have the same current; the actual parameter variation is retained in the polynomial.

### Exact uniform payoff ordering

Shared polynomial coefficients are subtracted before bounding them, retaining common parameter dependence. Certified lower differences from the best allowed type are:

| Comparator | Lower bound for g_4 - comparator |
|---|---:|
| b_2 | 0.04165675588 |
| g_2 | 0.03914286006 |
| b_4 | 0.04802918213 |
| b_8 | 0.07161991547 |
| g_8 | 0.00320605179 |

For G(xi)=g_4-b_4,

    0.04802918213346 < G(xi) < 0.05046011753683.

The full robust good/drain4 current, including the specified actuator errors, lies in

    0.22589600877950 < J_good,4 < 0.23056231751457.

For the same nuisance coefficients, phase/drain actuation can change the selected good/drain4 payoff by at most 3.085216432e-6. The bound compares correlated polynomial values; it is not the entire width of the uncertain-current interval. The bad/drain4 variation is smaller.

This finite full-state approach is feasible at four sites. It does not outperform general many-body methods by avoiding exponential dimension. Certified steady-state observable methods for much larger systems already exist [7]; no head-to-head superiority over them is claimed.

## 4. Constructing an experiment without a supplied decision Jacobian

The nuisance operators are known templates with unknown coefficients. The compiler enumerates the four occupation-state pairs connected by the unknown link 1-3. For a pair |a>,|b>, it evaluates all four template eigenvalue differences. Only one connected pair has zero difference in every nuisance direction:

    |0100>, |0001>.

The other two sites are empty. Thus the protected two-level subspace is found from the operator support tables, not from fitted response sensitivities or a supplied low-rank inverse. All interaction products vanish in this one-excitation subspace. The physical interactions remain fully active in the subsequent stationary transport problem.

Prepare |0100>, disable the other hopping edges and the injection/drain, and keep the original dephasing. Expose the pair to the unknown link for T=pi/4. In the pair basis the Hamiltonian is

    H_theta=-cos(theta) X+sin(theta) Y.

The two different occupations acquire relative dephasing at rate d. Solving the 2x2 Bloch equations gives

    rho_j = [I+s n_j.sigma+z Z]/2,
    n_j=(sin theta_j,cos theta_j,0),
    Omega=sqrt(4-d^2/4),
    s=(2/Omega) exp(-d T/2) sin(Omega T),
    z=exp(-d T/2)[cos(Omega T)+d/(2Omega) sin(Omega T)].

This state is calculated from an actual specified preparation and evolution; it is not a freely supplied state oracle. The interaction coefficients do not enter it because of the exactly verified nuisance-null subspace.

The chosen exposure is simple and feasible within the common budget. A general globally optimal preparation/control search was not performed. The all-adaptive identification lower bound below is nevertheless stronger: it allows competitors arbitrary preparations and intermediate controls.

## 5. Derive the action readout from the physical payoff

For fixed drain4, regret is G(xi) when a=j and zero otherwise. The task is therefore to avoid reporting the true phase label. The minimizing POVM is

    E_a=[I-n_a.sigma]/3,  a=0,1,2.

The effects are positive and sum to I. The three outcomes are physical actions, not positive statements about the model: outcome a rules against phase a, after which command alpha_a is safe under the remaining phases.

The ideal bad-action probability under each true phase is

    p_bad=(1-s)/3.

### Optimality over every POVM on this prepared probe

For uniform phase prior, the exclusion SDP has dual matrix

    Y=[(1-s)I+zZ]/6.

Indeed rho_a/3-Y=(s/6)(I+n_a.sigma)>=0. Thus every POVM has average bad probability at least Tr Y=(1-s)/3. The displayed E_a attain it, with equal error for every phase. They are minimax-optimal, not merely better than two chosen quadratures. This is an explicit state-exclusion SDP certificate in the established framework [1].

The drain choice is not silently fixed before this comparison. For action (a,k), its mean payoff operator is

    W_(a,k)=(2g_k+b_k)(I+zZ)/6 + (b_k-g_k)s n_a.sigma/6.

The exact physical polynomial bounds prove W_(a,4)-W_(a,k)>0 for k=2,8 throughout the nuisance box. Conservative positive eigenvalue margins are respectively above 0.0041278 and 0.0014977. Therefore any effect assigned to k=2 or k=8 can be reassigned to drain4 without lowering average payoff, for every xi. Covariance then converts average optimality into minimax optimality.

The construction is thus minimax-optimal over the full nine-action POVM set on the constructed probe, uniformly in xi. It is not asserted globally optimal over all preparations, exposure schedules, coherent multipass strategies or hardware implementations.

### Physical realization and a nonzero noise budget

Each E_a has rank one and eigenvalue 2/3. A 3x2 isometry has row a equal to sqrt(2/3)<v_a|, where n_a.sigma |v_a>=-|v_a>. An unused occupation channel supplies a Naimark extension. A known number-conserving 4x4 unitary and occupation measurement implement the readout, with the unknown link switched off. This is a constant-size operation; no second phase-dependent interrogation is concealed in the readout.

There is a demanding bandwidth condition. One conservative compilation uses at most six two-level Givens rotations, each routed through the known spanning tree 1-0-2-3 with at most five adjacent rotations, plus onsite phases. With known complex hopping and onsite control scale Gamma, a safe readout time is 20pi/Gamma. Original dephasing causes total-variation error at most d times this time on four sites. Gamma=4096 makes this contribution less than 0.000154. This is a sufficient theoretical implementation budget, not a pulse sequence tested on hardware. Slower native-only readout is not automatically covered.

To respect the hard exposure cap with a finite timer, the package commands a downward-rounded duration slightly below pi/4, with jitter at most 2^-18. The actual duration remains below pi/4; its state error is separately bounded at about 1.16e-5. Other preparation, loading, freezing, readout and calibration effects must fit the remaining allowance in `experiment_construction.json`. Their aggregate total-variation allowance, including the two specified contributions, is 1/2000.

The procedure selects a control for stationary throughput; the time for a real device to settle after changing that control is not bounded or included. A fixed-deadline transient recovery claim would need another theorem.

The model does not offer free state preparation. Emptying/loading sites, freezing known edges, switching the reservoirs and occupation readout have time, energy and calibration costs. These operations occur with the unknown link off; their phase-independent cost is additional to the charged unknown-link exposure. No numerical device energy or laboratory runtime is invented. A device that cannot meet the stated error and bandwidth requirements cannot use this guarantee.

### Optional acquisition of the four interaction intervals

The four-dimensional uncertainty box is not declared experimentally measured merely because it appears in the model. An optional explicit interval procedure starts from each coefficient in [0,8], with known physical d=0.01. All hopping and reservoirs are frozen. To probe U_L, prepare a Ramsey coherence on site0 with site1 occupied and others empty; use site3 with site1 occupied for U_R, site1 with site2 occupied for W, and site0 with site3 occupied for Z. These operations use calibrated single-site coherent controls, or a charge-reference ancilla if number-superselection constraints require one. The mean pair is exp(-d tau/2)(cos(c tau),sin(c tau)). No unknown phase-sensitive hopping occurs.

At stage one, tau=1/8 and 2^18 shots per quadrature give statistical radius 0.01. At stage two, tau=2, rotate the known readout reference by twice the first estimate, and use 2^16 shots per quadrature with radius 0.02. A per-quadrature mean-bias bound 0.0001 is additional to those radii. Half-angle arctangent, rational square-root and series intervals handle conversion without a phase-wrap assumption outside the admitted range. The first coefficient error is below 0.126; the second is below 0.016. The latter interval is accepted only if it lies entirely within its required center plus or minus 0.04. Otherwise the procedure is inconclusive.

The complete optional characterization costs **2,621,440 shots and 1,310,720 native interrogation-time units**, plus preparation, switching and readout. Exact exponential inequalities bound the probability of accepted false parameter coverage by 0.000064977852. Combined with the decision assay, the probability of accepting the characterization and selecting a bad phase control is below 0.001870371. This is an unconditional soundness-of-acceptance bound, not a conditional-on-rare-acceptance claim. Acceptance is not promised for every broad-prior model.

`calibration.py` implements rational data-to-interval conversion and the concentration certificate, and tests it on explicitly labelled synthetic nominal quadrature inputs. No shots were acquired from a device. The required preparation and mean-bias calibration are not validated by those synthetic tests. The main sensing comparison is conditional on correct characterization; both decision and identification competitors have that common information, and the identifier lower bound even grants the exact four interaction values. The substantial characterization cost can only be shared across fresh faults if the interaction parameters remain stable; amortization is not assumed for free.

## 6. Uniform decision risk, without repeated phase estimation

Exact rational pi, square-root and exponential bounds give

    s > 0.99608382248296,
    p_bad < 0.00130539250568.

An aggregate total-variation error eta=1/2000 raises the bad-action probability by at most eta, hence

    P(bad action) < 0.00180539250568.

On the complementary event the selected command is ideal-menu optimal, and the actual actuation has regret below

    3.085216432e-6.

The bound applies to every phase label and every xi in the four-dimensional box. There is no prior averaging in this high-probability statement. If the command is bad, its additional ideal loss is at most G_max. Thus

    E[regret] <= (p_bad+eta) G_max + actuation_allowance
               < 9.418554e-5.

Regret is measured against the best nominal control in the nine-action menu, at the same actual xi. The positive part may be taken if an actuation error happens to improve the nominal optimum.

No postselection on the measurement outcome is used and no outcome is discarded. One probe is prepared, exposed and read. Repetition could improve a different protocol, but it would spend a different total exposure budget.

### No-observation comparator, including randomized controls

Give any policy only the common uncertainty box. For fixed xi and a uniform phase prior, every phase command at drain k has average payoff (2g_k+b_k)/3. Exact polynomial checks prove that drain4 maximizes this quantity across k=2,4,8. Thus every no-observation randomized policy has average regret at least G(xi)/3, and hence worst-case regret at least

    G_min/3 > 0.01600972737782.

The ratio of this lower bound to the acquisition-policy upper bound exceeds 169.98. It is a ratio of certified expected-risk bounds, not a runtime speedup, an optimal active sensing ratio or an asymptotic information complexity claim.

## 7. Same-access lower bound against every phase identifier

The experiment set is now specified independently of our chosen measurement. A competitor may use arbitrary known preparation, ancillas, coherent controls, measurements, resets, adaptive feedback and computation. Known controls may be strong. The unknown phase-sensitive link has instantaneous hopping magnitude at most one. The total summed exposure to that unknown interaction, across every specimen and every branch, is at most

    T_max=pi/4.

This is a hard total exposure bound, not just wall time for parallel copies and not an expected-time bound allowing rare arbitrarily long interrogations. Failed and discarded attempts count. Phase-dependent characterization after the fresh fault counts. Characterization before the fault is common information and cannot reveal the new label.

The phase changes only the displayed link. Other unknown coefficients can be given to the competitor exactly for this lower bound, strengthening its access. Additional independently phase-sensitive couplings, amplified unknown hopping, access to an external fault record or an uncharged phase-correlated reference are not in the interface.

For two different hypotheses and any common commanded phase alpha,

    ||H_(theta_i+alpha)-H_(theta_j+alpha)||=sqrt(3),

and the eigenvalue range of their difference is 2sqrt(3). All diagonal interactions cancel. This equality holds on the full four-site many-particle Hilbert space, not only on our probe subspace.

### Angular distinguishability bound

Let A_B denote the Bures angle of the two possible accessible states. During an infinitesimal unknown Hamiltonian exposure dt, their angular distance increases by at most half the spectral range of the Hamiltonian difference times dt, hence at most sqrt(3)dt. Known operations leave or decrease distinguishability. Common Markovian noise also contracts Bures angle. Ancillas do not change the norm of the Hamiltonian difference.

For a pure-state step, the bound follows by comparing the two infinitesimal propagators on the same input, removing a scalar phase, and using the Fubini-Study speed bound by half the spectral range; the triangle inequality propagates an existing angle. Purification and contraction give the mixed-state statement. Adaptive measurements can be stored in a record, and parameter-independent feedback implemented conditionally on that record. Discretizing the total exposure into native query slots, padding unused exposure with an empty-state query, and taking the limit gives the same bound for feedback and variable stopping under the hard total cap. Parallel probes are charged by the sum of their unknown exposures.

Therefore

    A_B(rho_i,out,rho_j,out) <= sqrt(3) T_max < pi/2,
    (1/2)||rho_i,out-rho_j,out||_1 <= sin(sqrt(3) T_max).

Binary equal-prior Helstrom error is at least

    [1-sin(sqrt(3)pi/4)]/2 > 0.011031161767.

Any uniformly successful three-label classifier yields a binary classifier on a chosen pair by coarse-graining its outputs. Consequently every allowed phase identifier has failure at least this amount on some phase. Uniform 99% phase identification is impossible in the common budget.

This reconstructs a standard Hamiltonian distinguishability/time bound [2,3]; it is not a new quantum speed limit. The novelty under investigation is its coupling to a payoff-certified decision that succeeds in that same access class.

The lower bound does **not** say that all estimate-then-act software must perform poorly. A decision-aware learner that does not actually identify the phase may implement our exclusion policy exactly. It also does not prohibit phase identification with more exposure, stronger phase-sensitive coupling or a different information source. The numerical exposure separation is finite and modest; no exponential sensing-time advantage is claimed.

## 8. Why this is more than a chosen-contrast nonidentifiability example

The previous contrast admitted two exactly identical observation laws, but another quadrature could distinguish them. That was an interface-specific statement about one selected experiment.

Here the successful method and competing learners share an acquisition budget and available phase-sensitive interaction. The lower bound holds even when competitors choose an arbitrary alternative preparation and readout and use feedback. It is therefore not invalidated merely by suggesting another quadrature.

The actual reason a decision is easier is overlap of physically certified good-action sets. Learning the true label would be unnecessary work: excluding one alternative is enough to select a control safe under the other two. The special three-way geometry is important. If the task instead required a unique phase correction encoding the true phase, decision and identification could coincide and this advantage would disappear.

This is a strict scoped separation of decision and identification under shared access. It is not a complete information-complexity characterization for arbitrary physical experiments or high-dimensional models.

## 9. Evidence, reproducibility and resource accounting

The benchmark builds all six coefficient-family trials from the local model. It does not load previously solved responses. It uses ordinary floating inverses only for discovery, rounds all proposed trial and inverse entries to dyadic rationals, and checks every later inverse and residual bound with arbitrary-precision integer arithmetic. The accepted certificate is not based on a small floating residual.

Recorded benchmark:

| Stage | Seconds |
|---|---:|
| Six fresh robust response families and exact verification | 5.920287 |
| Probe construction, payoff ordering, POVM and risk/information checks | 0.194793 |
| Process clock including imports | 6.294814 |
| Later exact rebuilding and independent-coordinate checks | 12.211706 |

Peak process resident memory is 135,588 KiB. There are 388,080 complex trial scalars and 29,400 complex reference-inverse scalars across the six cases, explicitly stored. Those finite-state costs would grow badly with the number of sites. No scalable many-body inverse theorem follows.

The preparation space was enumerated from four link-connected occupation pairs. Its unique nuisance-null pair was selected exactly. The three-outcome readout was derived analytically from the certified loss structure. The nine-action menu, nominal device and simple pi/4 candidate exposure were selected during exploration; the timing is not an autonomous search from an unspecified set of scientific tasks.

### Tests

`checks.py --verify-witnesses` performed:

* Six exact certificate reconstructions without numerical optimization; zeroing a proposed inverse was rejected by the exact inverse-residual check.
* Six full 256-dimensional Kronecker-generator comparisons with the separately assembled 70-dimensional neutral matrices.
* 462 full finite-density steady-state polynomial checks, including every six-variable box corner for each case; all numerical discrepancies were below their exact residual bounds. The largest observed ratio was about 0.000883. The floating solves are diagnostics only.
* Thirty independent phase-reflection checks, and full Hamiltonian pair-difference norm checks.
* Thirty-six two-level physical-Lindblad probe comparisons over several times and original dephasing rates.
* One explicit 3x2 readout isometry and 120 arbitrary random POVM comparisons. Optimality comes from the analytic dual, not these random tests.
* Exact minimal-conflict set checks and finite-density occupation-sector diagnostics.

Rational bounds on pi use Machin's identity and alternating arctangent series. Exponential and sine remainders are explicit. Outward dyadic rounding prevents a huge serialization denominator from becoming a mistaken accuracy claim. An early attempt to serialize an unrounded large sine fraction hit Python's integer-string safeguard; the bound was outward rounded and all accepted results rebuilt. No physical sample is claimed.

The scripts and witness files are local conversation artifacts. No repository write was performed.

## 10. Prior-art comparison and attribution

State exclusion is established [1], including SDP formulations, optimality and worst-case variants. The anti-trine measurement and its distinction from minimum-error identification are not claimed as discoveries. The minimal-conflict reduction is an elementary decision-set formulation, not a claim that generic minimax quantum decision theory is new.

Experimental design already optimizes target decisions instead of complete parameter estimates. Fiez et al. give transductive linear-bandit lower bounds and near-matching algorithms under a specified measurement menu [4]. Estimate-then-optimize and semiparametric approaches similarly provide decision-relevant or nuisance-aware acquisition [5,8]. This run does not supersede those frameworks; it supplies an explicit quantum physical-control instance, a constructed nuisance-null experiment and a lower bound against all identifiers in its access class.

Strong active Hamiltonian learning is possible with controlled evolution and near-optimal time scaling [9]. That is why the comparator here is not tomography or one fixed quadrature. The lower bound is imposed by total unknown-interaction exposure and applies regardless of the learning algorithm's sophistication.

Certified steady-state observable algorithms already treat substantially larger systems than this four-site example [7]. Our finite exact residual compiler is a paid source of payoff guarantees, not a computational-speed claim over those methods. No independently optimized transport, reduced-order or Bayesian experiment-design implementation was timed head-to-head.

The new candidate contribution is the **payoff-to-exclusion construction plus a uniform interacting-device certificate and a fair total-exposure lower bound**. Historical priority of that combination remains unknown. It is not a civilisation-level scientific discovery, a new general quantum information principle, or a new solution of high-dimensional strongly interacting matter.

## 11. What has changed, and the exact remaining problem

The earlier residual-derivative and measurement-fibre construction is preserved. Its selected-contrast nonidentifiability argument is not upgraded into a general lower bound. This investigation instead demonstrates a genuine all-permitted-identifiers separation for a different physical task.

The useful general lesson is operational: discover overlapping good-action sets from verified physics; synthesize an experiment and measurement that eliminate unacceptable actions; certify risk over every unresolved nuisance model. Neither curvature nor a fitted decision Jacobian is necessary for this construction. There is no need to reconstruct the complete model merely because it exists mathematically.

The remaining consequential theorem is to make that pipeline inexpensive for extended interacting devices: acquire certified loss inequalities and physically realisable probe codes for a manageable collection of decision conflicts, control approximation under continuous disorder and phase uncertainty, and bound the total experimental and computational cost without enumerating either all models or a full many-body Hilbert space.

Three actual obstructions remain explicit: loss certification can be many-body hard; good-action overlaps can vanish when controls are changed; and the required measurement may be physically inaccessible or too noisy. None is removed by naming a decision equivalence class, writing a small SDP, or providing an ideal output state.

In particular the previous infinite-chain inverse-rank, generic compact-certificate and general experimental-calibration problems remain open. This run does not replace them with a claim that the small-ring calculation completes the original North Star.

## 12. Provenance

The complete attached 595-line decision-calibration note and checkpoint were read. They explicitly distinguish one-contrast information from arbitrary active learning. No previous numerical response coefficient was used as a solver input here.

Astra main was fetched at commit `4ae225b0bf2a07e1ced2952a3e1399d4b45e039c` (13 October 2026). The current record includes N765 response-error design, N766 paired response acquisition and N767 chemomotor claims, all source-derived/unreviewed. This run did not independently audit or import those theorem claims. A targeted `Helly minimax` search in `openai/math` returned no applicable files; this is not an exhaustive novelty search. No Lean build or external write was made.

Original research was used to delimit prior art. Full HTML retrieval failed for the older exclusion and Hamiltonian-time papers; their primary abstracts were inspected and the specific algebra/time bound was derived directly here. No theorem was inferred from unavailable text.

## Primary references

[1] S. Bandyopadhyay, R. Jain, J. Oppenheim, C. Perry, *Conclusive Exclusion of Quantum States*, arXiv:1306.4683v3, Phys. Rev. A 89, 022336 (2014). https://arxiv.org/abs/1306.4683

[2] Y. Aharonov, S. Massar, S. Popescu, *Measuring Energy, Estimating Hamiltonians, and the Time-Energy Uncertainty Relation*, arXiv:quant-ph/0110004. https://arxiv.org/abs/quant-ph/0110004

[3] A. Acin, *Statistical distinguishability between unitary operations*, arXiv:quant-ph/0102064 (2001). https://arxiv.org/abs/quant-ph/0102064

[4] T. Fiez, L. Jain, K. Jamieson, L. Ratliff, *Sequential Experimental Design for Transductive Linear Bandits*, arXiv:1906.08399 (2019). https://arxiv.org/abs/1906.08399

[5] S. Tan, P. I. Frazier, *Regret Bounds and Experimental Design for Estimate-then-Optimize*, arXiv:2210.15576 (2022). Prior source reviewed in the attached continuation. https://arxiv.org/abs/2210.15576

[6] C. Emary, *Dark states in the magnetotransport through triple quantum dots*, arXiv:0705.2934, Phys. Rev. B 76, 245319 (2007). https://arxiv.org/abs/0705.2934

[7] L. Mortimer et al., *Certifying steady-state properties of open quantum systems*, arXiv:2410.13646v2, Phys. Rev. Research 7, 033237 (2025). https://arxiv.org/abs/2410.13646

[8] M. Tsang, F. Albarelli, A. Datta, *Quantum Semiparametric Estimation*, arXiv:1906.09871, Phys. Rev. X 10, 031023 (2020). https://arxiv.org/abs/1906.09871

[9] H.-Y. Huang, Y. Tong, D. Fang, Y. Su, *Learning many-body Hamiltonians with Heisenberg-limited scaling*, arXiv:2210.03030, Phys. Rev. Lett. 130, 200403 (2023). https://arxiv.org/abs/2210.03030
