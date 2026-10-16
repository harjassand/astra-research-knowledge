# Completed-sweep memory with coherent post-errors at every proposal

Date: 2026-10-15.
Status: constructed compositional theorem, with its quantum and classical interfaces independently reviewed internally. No counterexample was found under the hypotheses below. This is not formal verification, external referee validation, a numerical threshold, or a hardware demonstration. Historical novelty remains open.

## 1. Main statement

Fix a bounded family of memory fault patches attached to the primal and dual correction locations of the four-dimensional toric sweep model. The patches have diameter and incidence degree bounded independently of system size. Assume the stabilizer detection and no-local-logical conditions in Section 2.

There exist a fixed integer block size b, constants delta_0, eta_0, A, c>0, and a minimum size, depending on this fixed geometry and the ideal sweep rule but not on storage time, bath dimension, or system size, with the following property.

For sufficiently large compatible sizes L=bM, initialize the entire six-logical-qubit toric code space, allowing arbitrary logical-bath-reference entanglement. Use the completed sweep correction instrument at EVERY point of independent exogenous rate-kappa Poisson clocks at each primal and dual vertex. After each correction, apply the joint randomized post-error specified below, with a uniform coherent-strength bound delta<=delta_0. Allow independent single-face Pauli noise with rates lambda_X, lambda_Y, lambda_Z satisfying

    max(lambda_X+lambda_Y, lambda_Z+lambda_Y) <= eta_0 kappa.

Then the same type of fixed perfect final syndrome-recovery decoder as in the reconstructed ideal sweep theorem gives a decoded joint-input channel Gamma_{L,T} satisfying, for all T>=0,

    || Tr_{B'} Gamma_{L,T} - Tr_B ||_diamond
       <= min(2, A L^4 (1+kappa T) exp(-c L)).                (1)

The domain of both maps is logical tensor bath; arbitrary additional untouched reference systems are included by the diamond norm. With a fixed independent bath initialization, (1) also gives the usual logical-channel bound against identity. More strongly, for each horizon there exists a CPTP bath map Lambda_{L,T} such that Gamma_{L,T} is within the same stated bound of Id_logical tensor Lambda_{L,T}.

The finite-dimensional bath can persist across proposals and distant patches. Constants do not depend on its dimension. This statement does not cover an unbounded retained classical output register or an infinite-dimensional bath without additional analysis.

Operational consequence: under the explicit joint-frame and uniform-norm assumptions, a bounded coherent memory-bath post-error at EVERY correction proposal reduces to a controlled marked-Poisson SUPPORT probability problem. This remains true when there is no common bath-channel CP minorant and hence no independent physical rare-fault mixture.

## 2. Exact model hypotheses

### 2.1 Completed correction, not the original seven-jump generator

At each proposal, the ideal memory channel is

    C(X)=sum_{j=1}^7 Q_j Pi_j X Pi_j Q_j^dagger + Pi_0 X Pi_0,
    Pi_0=I-sum_{j=1}^7 Pi_j.

The active projectors select the seven prescribed sweep patterns; Q_j are their prescribed Pauli corrections. Q_0=I. The projectors are functions of commuting code stabilizers. Every proposal executes this complete instrument, including the inactive branch. A bad post-error does not suppress or replace the correction.

The original seven-active-jump Lindbladian differs from kappa(C-Id) by the absent inactive-projector dephasing. They agree on the original definite-syndrome Pauli trajectories, not on arbitrary full-input coherences. The present theorem is expressly for completed proposals.

### 2.2 Exogenous clocks, fixed patches, and ordering

Correction clocks have independent homogeneous rate-kappa laws, independent of the initial joint quantum input. Neither their rates nor future realizations can be changed or anticipated by the protocol. Each clock type carries a fixed bounded patch A_i, or an adaptively chosen patch enclosed in that fixed patch. The within-attempt order is

    old-state ideal correction, THEN joint randomized post-error.

Both intermediate states are included in the support-history certificate. Independent external Pauli clocks retain their stipulated laws.

### 2.3 Local detectability and absence of local logicals

For each patch A_i, choose a subgroup G_i of code stabilizers such that a Pauli supported in A_i commutes with G_i exactly when it commutes with all code stabilizers. Require that every such zero-syndrome patch Pauli is itself a stabilizer up to phase. Equivalently, there is no nontrivial logical Pauli supported in A_i.

For the toric family and sufficiently large L, a fixed contractible bounded patch meets the latter condition. Geometrically local checks intersecting A_i supply a detection-complete G_i supported in a bounded neighborhood. This neighborhood must be counted if the physical randomizer is implemented by pulses. Bounded error support does not imply bounded randomizer support for arbitrary nonlocal-check codes.

No refined syndrome measurement is imposed. In particular, Pi_0 is not assumed to resolve the full local syndrome.

### 2.4 Actual joint twirl and uniform coherent strength

At each proposal, conditional on every admissible genuine causal physical history, there is a joint unitary U_i on A_i tensor B and a bath-only unitary V_i such that

    || U_i-I_{A_i} tensor V_i || <= delta.                 (2)

The bound is operator norm on the full joint patch-bath space and is uniform in current bath state and all admissible histories. A bound for one prepared bath state, an averaged calibration value, or average fidelity does not suffice.

The actual post-error joint channel is

    T_i(X)=|G_i|^-1 sum_{g in G_i}
              (g tensor I) U_i (g tensor I) X
              (g tensor I) U_i^dagger (g tensor I).       (3)

A fresh frame must be sampled independently of the current input and U_i. Its explicit randomization register is discarded or inaccessible to all future dynamics. Any indirect bath correlations arising through the stipulated U_i are already modeled; an additional accessible frame leak is not. A memory-only marginal twirl does not establish (3).

Paired stabilizer frames around the completed correction and its fixed post-error realize (3) algebraically because the completed correction is stabilizer covariant. This observation does not certify noisy physical pulse implementations. Gate/frame-dependent errors require their own justification of (2)-(3).

U_i may depend on genuine available past physical records, and on the observed clock prefix, provided every such choice obeys these hypotheses. Mathematical character labels introduced in the proof are not controller-accessible records unless that instrument is actually implemented. Bath-only evolution is harmless. No uncontrolled memory interaction between proposals is included.

## 3. Quantum reduction: an instrument, not a rare-fault mixture

For one proposal, let

    U_chi=|G|^-1 sum_g chi(g)^* (g tensor I)U(g tensor I).

Character orthogonality gives T(X)=sum_chi U_chi X U_chi^dagger and sum_chi U_chi^dagger U_chi=I. These operators define a legitimate Kraus instrument, even when its character labels are only mathematical.

Set D=U-I tensor V. Conjugation averaging E_G yields

    sum_{chi != 0} U_chi^dagger U_chi
       =E_G(D^dagger D)-E_G(D)^dagger E_G(D)
       <=delta^2 I.                                      (4)

Thus a nontrivial character has conditional probability at most p=delta^2 for every normalized current joint state, after every feasible prior record. The inequality is global; it does not require refinement or an encoded input.

Expand each U_chi in patch Paulis with bath-operator coefficients. Equal characters imply that the corresponding Paulis differ by a patch-supported stabilizer. Therefore, for a representative P_chi on A,

    U_chi=(P_chi tensor I) sum_M M tensor B_{chi,M}.

For a full-code encoding V_code and any physical Pauli E,

    U_chi(E V_code tensor I)
        =P_chi E V_code tensor A_{chi,E}.                 (5)

The coefficients A_{chi,E} are arbitrary ordered bath operators. Their stabilizer eigenvalue signs depend on the syndrome of E, not on the logical vector. Equation (5) holds on entangled logical-bath inputs. Choose P_0=I: the zero character preserves each Pauli orbit, though its bath operation may depend on the syndrome.

The completed correction similarly maps E V_code either to Q_j E V_code or to zero. Consequently every fixed complete Kraus record follows one legal Pauli history: every correction occurs; a nonzero character subsequently introduces one bounded-patch Pauli; the zero character adds no support. The aggregate inactive projector is scalar on each full-syndrome orbit, which is why no additional measurement is needed here.

This construction supplies a uniformly bounded conditional bad-label probability. It does NOT give an input-independent classical distribution of actual fault locations or a common-bath-channel CP minorant.

## 4. Classical marked-proposal comparison

Verified classical module:

    ../classical/SAME_ATTEMPT_LABEL_COMPARISON.md

Condition on all exogenous correction clock locations/times h over a finite horizon. Causality and the pointwise bound (4) imply

    Pr(actual bad label at i | h, previous labels)<=p.

A sequential uniform-variable coupling dominates these actual labels by iid Bernoulli(p) reference marks ON THE SAME correction clocks. The coupling can depend on the initial quantum input; its independent-reference marginal and its bounds do not. It is used only for analysis.

The robust support envelope and block-failure events are increasing in the bad marks for fixed clocks. This concerns the universal auxiliary envelope, not an assertion that adding errors makes the actual correction dynamics monotone. The reference keeps every original correction time and attaches a possible post-correction birth at that exact attempt.

All original slow-certificate and structural-fast-word estimates therefore retain rate kappa. If N_guard bounds the number of correction streams whose fixed patches touch one primitive guard and Delta is the slab duration, the new guarded-birth contribution is

    1-exp(-kappa p N_guard Delta)
      <= kappa delta^2 N_guard Delta.                    (6)

Both primal and dual attempts able to affect a sector must be counted. Add the previously established external Pauli birth contribution. There is no factor (1-p) reducing the ideal correction rate in this instrument route.

Reference births and correction clocks at the same attempt are correlated. The primitive packet is the clock PLUS its independent mark. Spatially separated packets and disjoint deterministic slabs are independent; the robust flags have bounded dependence. The stopped torus-to-lift replay must copy each packet jointly, never resample its clock and birth independently.

Choose fixed geometry, guards, forcing constants, dependence target, and block size first. Then choose delta_0>0 and external rate ratio eta_0>0 sufficiently small that (6) and the external birth term fit the positive bad-flag budget. The reconstructed product-domination/eroder/torus-homology chain then gives a uniform bad-record probability

    epsilon_{L,T} <= C L^4(1+kappa T)exp(-c L).           (7)

Its good-event rule is a fixed, input-independent function of clock/support records, and certifies every admitted bounded-patch Pauli history with the same final decoder. Both pre-correction and post-correction/pre-birth states are covered. Enlarged patch geometry changes constants and the required minimum L.

## 5. Trace-nonincreasing good map and compositional diamond bound

Verified quantum module:

    ../bridge/BATH_QUANTUM_AUDIT.md

For every good complete record, equation (5), the completed correction identities, and the common-decoder homology statement give a recovered Kraus operator I_logical tensor B_alpha. Summing all good records and averaging exogenous clocks gives

    G=Id_logical tensor Lambda_g,

where Lambda_g is CP and trace-nonincreasing. Conditioning on a good label record does not produce a CPTP channel, and is not used as though it did.

Write the full decoded CPTP channel as Gamma=G+H with H CP. Trace preservation gives

    H^*(I)=I_logical tensor D_B,
    D_B=I_B-Lambda_g^*(I),  0<=D_B<=I_B.

The input-uniform probability estimate (7) implies D_B<=epsilon_{L,T} I_B. Choose any fixed bath output density matrix sigma and define

    Lambda_b(X)=Tr(D_B X) sigma.

Then Lambda_g+Lambda_b is CPTP. Since the diamond norm of a CP map equals the operator norm of its adjoint effect,

    ||Gamma-Id_logical tensor (Lambda_g+Lambda_b)||_diamond
       <= ||H||_diamond+||Id_logical tensor Lambda_b||_diamond
       <=2 epsilon_{L,T}.                               (8)

Tracing the bath and absorbing 2C into A proves (1), with the trivial maximum distance 2. The bath completion is a mathematical comparison map, not a proposed physical intervention. Uniformity over every initial bath state is necessary for this joint-input norm claim.

## 6. Distinction from the refined fixed-unitary theorem

The separate REPORT.md Sections 2-4 prove a full-input CP mixture for a memory-only fixed U after a refined correction C_ref, with a state-independent coefficient q>=||U-I||^2. Its independent-stream representation has clean correction rate kappa(1-q), and its bad event includes the whole correction-plus-fault gadget.

The present theorem instead uses the original completed C, no additional refinement, and a joint bath instrument. All rate-kappa corrections remain. Its actual bad labels may be input- and bath-correlated. Only a dominating reference has independent Bernoulli marks.

The distinction is necessary. With measured stabilizer Z_A and U_AB=exp(-i theta Z_A tensor Z_B), every character is trivial, yet the two syndrome sectors apply different bath unitaries exp(+/-i theta Z_B). Their rank-one Choi supports have no nonzero common CPTP minorant for generic small nonzero theta. The orbit/instrument argument still applies, while a full-input mixture with one common bath channel fails.

Neither theorem claims arbitrary coherent robustness of the original uncompleted active-jump generator.

## 7. Established ingredients, constructed connection, and imports

Previously reconstructed internal ingredients include the completed correction/Pauli-orbit identities; fixed full-code decoder and common-decoder homology condition; microscopic support envelope; uniform forcing; primitive slow/fast flag bounds; bounded-dependence product-domination replacement; stopped replay; and accumulated-homology transfer. Consolidated status and source pin:

    ../STATUS.md
    ../classical/QUANTUM_INTERFACE_VERIFICATION.md
    pin 3e8a972f2924272e1a89859d2f556b5b1f91d501.

The substantive external probability import remains Hartarsky-Toninelli, arXiv:2212.08437v2, Corollary 9.5, with its Toom-contour dependencies. Its applicability was reviewed; the entire external contour theory has not been independently reconstructed here.

The connection constructed here is: exact joint stabilizer twirl -> uniform bad-character effect plus encoded-orbit preservation -> same-attempt marked-clock domination retaining every correction -> TNI-good-map bath completion. The separate quantum and classical audits above support this composition under the listed hypotheses. No unclosed internal interface is currently identified within that stated ideal model. Formal certification and external scientific review remain outstanding.

Noise tailoring and stabilizer randomization are established prior art, including Wallman-Emerson (arXiv:1512.01098), Cai-Benjamin (arXiv:1807.04973), and Beale-Wallman (arXiv:2306.13752). Whether this particular completed-sweep marked-bath interface is historically new has not been established.

## 8. Exact handoff and remaining physical primitive tests

A proposed implementation must supply, for each correction location and every admissible genuine causal history:

1. A complete ideal correction instrument with the displayed active AND inactive Kraus branches; characterize any deviation separately.
2. A bounded attached error patch, its support incidence count, and a bounded detection-complete stabilizer randomizer.
3. An actual JOINT patch-bath channel satisfying (3), including fresh-frame independence and inaccessible frame records.
4. A uniform full-joint operator-norm bound (2), not merely average infidelity or a memory-only reconstructed marginal.
5. A demonstration that noisy randomizer pulses, reset operations, measurement ancillas, and idle latency are either included in that same justified channel or separately charged by an authorized noise model.
6. Verification of the correction-before-birth event order, unchanged exogenous clocks, and absence of unscheduled memory interactions.
7. Perfect encoded initialization and the stipulated final decoder, or a separate theorem addressing their imperfections.

The actual hardware challenge lies in these premises. This theorem supplies no useful numerical threshold, no empirical lifetime, no noisy-readout result, no 3D embedding or reservoir implementation, and no automatic extension to continuous system-bath Hamiltonians, leakage, or arbitrary faulty gates. It establishes an explicit bounded post-proposal coherent-error bridge once the required physical primitives are justified.

## 9. Exact rational bath-filter witness

The following compact illustration strengthens the distinction in Section 6. Let the memory be a stabilized ancilla A with stabilizer Z_A and an untouched logical subsystem L. Encode A in |0> and let C reset A to |0>. The patch A contains no logical Pauli. Let bath B be a qubit and set c=99/101, s=20/101. Use the joint unitary

    U=I_A tensor |0><0|_B
        +(c I_A-i s X_A) tensor |1><1|_B.

Twirl by {I,Z_A}. Its exact character Kraus operators are

    U_0=I_A tensor A_0,       A_0=diag(1,c),
    U_1=X_A tensor A_1,       A_1=diag(0,-i s).

They satisfy A_0^dagger A_0+A_1^dagger A_1=I and

    A_1^dagger A_1=diag(0,400/10201)<= (400/10201) I.

Also ||U-I||^2=4/101, consistent with the general bound. The good label preserves the encoded memory orbit but filters the bath rather than applying a trace-preserving bath channel.

There is no p>0 and CPTP Lambda_B for which this twirled reset/post-error channel dominates p(C tensor Lambda_B). Restrict the input ancilla to |0> and the output to its |0> block. The domination would require Ad_{A_0}>=_CP p Lambda_B. Its rank-one Choi support forces Lambda_B to be proportional to Ad_{A_0}, but no nonzero proportional multiple is trace preserving because A_0^dagger A_0=diag(1,c^2) has unequal entries.

Nevertheless the logical subsystem is preserved exactly for every initially correlated L-B input: tracing the ancilla gives Id_L tensor (Ad_{A_0}+Ad_{A_1}). The TNI good bath map Ad_{A_0} admits the CPTP completion supplied by the bad bath map Ad_{A_1}. This illustrates why the instrument proof covers cases excluded by an independent ideal/bath-channel mixture; it is not a large-code or hardware performance test.

Reproducible exact symbolic certificate:

    ../checks/check_bath_exact.py

The script checks joint unitarity, both character operators, completeness, the exact bad effect, and the rank-one/non-TP-filter obstruction using installed SymPy and rational arithmetic.

## 10. Additional non-Markovian prior art and correlated-input caution

Winick et al., *Concepts and conditions for error suppression through randomized compiling*, arXiv:2212.07500v1, already treats persistent ancillary systems in Section III.2 and discusses gate-dependent/non-Markovian limitations, including leaked frame information, in Section III.3. Primary source: https://arxiv.org/html/2212.07500 . Thus neither bath noise tailoring nor the need to protect the fresh frame information is claimed new here.

This theorem deliberately keeps the joint-input operator/instrument proof rather than substituting a reduced-system Pauli-channel formula for arbitrary correlated inputs. A short exact illustration: take joint Kraus operators K_0=I_S tensor |0><0|_B and K_1=X_S tensor |1><1|_B, and rho_SB=(|00><00|+|11><11|)/2. The output system is |0><0|, although the input reduced state is I/2 and every system-only Pauli channel would preserve I/2. Joint system-bath instruments cannot generally be replaced by a system-only Pauli channel acting on the reduced input for arbitrary correlations. This scope caution is not a refutation of the cited paper or of correlated-Pauli-process approaches. It explains why equations (4)-(8) are formulated on the full joint domain.
