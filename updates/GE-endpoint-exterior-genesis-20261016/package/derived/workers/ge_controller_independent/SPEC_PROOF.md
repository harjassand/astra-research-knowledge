# Repeated encoded transactions with local bank movement

16 October 2026. Independent construction. Internal mathematical status only.

This is a **fixed-size, periodic, noninteracting-cell theorem** in an ideal engineered-jump plus onsite-Poisson-noise model. It supplies finite A/B reuse, total damaged-control retirement, a reference-uniform quantum contract, and an elementary all-set bad-epoch estimate at that scale. It does not supply a noisy circuit implementation of recovery, interactions between cells, an arbitrary program stream, a recursive controller, or a threshold. In particular, the fixed-support recovery jump below is an explicit remaining physical interface.

## 1. Alphabet and geometry

A cell has five physical sites, indexed i=1,...,5. Each site contains two qutrit banks A_i,B_i and a three-valued classical phase r_i in {0,1,2}. A qutrit is span{|0>,|1>,|v>}, with |v> vacancy. Thus the local Hilbert-space dimension is 27 if the classical phase is represented by dephased quantum sectors. Arrange the five sites in any fixed bounded region of a two-dimensional lattice; all maps below then have a fixed finite range. There are no dynamically stored program symbols. The repeated word is hardwired into the local jump types.

Use the [[5,1,3]] code C in the qubit subspace of A_1...A_5, with stabilizers

    XZZXI, IXZZX, XIXZZ, ZXIXZ.

Let P be its rank-two projector, and take X_L=X^tensor5, Z_L=Z^tensor5. Put

    C = (I - i(X+Y+Z))/2,
    W_0=I, W_1=X, W_2=CX,
    U = C^tensor5 X^tensor5 restricted to C.

C cyclically sends X to Y, Y to Z, and Z to X. Its transversal action preserves C; the four stabilizer images are g_3g_4, g_1g_2g_3, g_2g_3g_4, g_1g_2. Consequently U is a genuine logical unitary. The logical channels of C^tensor5 and X^tensor5 do not commute: C_L sends logical X to logical Y. This is not only a commuting correction cycle.

Initially all r_i=0, all B_i are |v>, and A carries an arbitrary state on C, including entanglement with an arbitrary reference. One output event, called a commit, means one application of U. The same ten banks and five phases are reused after every commit.

All listed maps and rates are fixed in time. The ideal autonomous generator is

    L_0 = lambda sum_i(Phi_i-id) + kappa(T-id)
          + nu sum_i(Reset_i-id) + mu(R_*-id),

with either optional rate allowed to be zero. A CPTP-map-minus-identity is the generator of its Poisson-jump semigroup. Thus this is a time-independent, bounded-support generator on the stated fixed alphabet, not an externally timed schedule.

## 2. Explicit local maps

For a qubit unitary V, let V^sharp=V direct-sum 1_v. Define M^AtoB_V on A tensor B by: discard B, apply V^sharp to A, transfer A isometrically to B, and prepare A in |v>. Its Kraus operators are

    D_b = sum_(a,c=0,1,v) (V^sharp)_(c,a) |v,c><a,b|,
    b=0,1,v.

Then sum_b D_b^dagger D_b=I_(A B). Define M^BtoA_V by interchanging A and B. These are total CPTP maps, including on vacancy or doubly occupied inputs. They transfer rather than copy the selected source. They do not ask whether a bank is occupied.

Each track has an independent rate-lambda proposal Phi_i. It first dephases its phase sectors and performs:

| Phase before | Quantum map | Phase after |
| --- | --- | --- |
| 0 | M^AtoB_X | 1 |
| 1 | M^BtoA_C | 2 |
| 2 | identity | 2 |

The gate and phase update in each row are one onsite CPTP jump. A correct track has A as its selected bank at phases 0 and 2, and B at phase 1. Both an omitted gate and a wrong-bank selection are allowed after a local phase fault; they will be treated as an error on that track rather than guessed away.

Optionally each site has a rate-nu reset proposal. It dephases r_i and resets the unselected bank: B at phases 0 or 2, A at phase 1. It does not read occupancy. If a faulty phase causes it to erase live information, this is a local track error. The recovery proof below explicitly includes such arbitrarily many subsequent ideal wrong-bank resets.

## 3. An explicit total qutrit recovery

Define 26 maps on the code input:

    F_0 = I,
    F_(i,P) = P_i, P in {X,Y,Z}, i=1,...,5,
    F_(i,s) = sqrt(2) |v><s|_i, s in {0,1}, i=1,...,5.

The Pauli maps are restricted to their qubit sectors; their action on vacancy elsewhere is immaterial on P. The 15 weight-one Pauli syndromes are distinct and nonzero. Thus

    P F_a^dagger F_b P = delta_(a,b) P.                 (1)

For the leakage maps at the same site this follows from P |s><t|_i P=delta_(s,t) P/2, since every nonidentity weight-one Pauli has zero code compression. Different leakage sites have orthogonal vacancy patterns. Leakage and nonleakage images are orthogonal. These observations prove (1) exactly, including all cross terms.

Set J_a=F_a P and Q=sum_a J_a J_a^dagger. The J_a are isometries with orthogonal images; Q has rank 52 inside the 243-dimensional qutrit space. Prescribe

    R(sigma) = sum_a J_a^dagger sigma J_a
               + Tr[(I-Q)sigma] P/2.                 (2)

This is a total CPTP map into C. It corrects every one-site map from a qubit into a qutrit because the displayed 26 maps span all such error maps on C. In particular, if E_mu are arbitrary one-site Kraus maps, each E_mu P=sum_a alpha_(mu,a) J_a, then

    (R tensor id_ref)(sum_mu E_mu rho E_mu^dagger)
      = (sum_(mu,a) |alpha_(mu,a)|^2) rho             (3)

for any code/reference state rho. The scalar is independent of rho and its reference. An uncorrectable input is still sent into C; its logical state is unrestricted. No selective detector for all logical counterfeits is claimed.

## 4. Reusable commit

A rate-kappa commit proposal T dephases the five phases. In the all-2 sector it performs, in one fixed-support CPTP jump:

1. discard and prepare all B_i in |v>;
2. apply (2) to A;
3. prepare all r_i=0.

In every other sector it is identity after phase dephasing. Its enabled Kraus operators include the projector onto the all-2 sector; its disabled branch is the complementary phase projector. Both branches are CPTP in total. An enabled commit always leaves A in C, B vacant, and every phase zero, even on a completely malformed quantum input.

There is no terminal LIVE/SPENT flag, modulo epoch tag, delayed acknowledgment, or pending transfer object. Proposal clocks have no memory of an earlier bank choice. Each jump rereads the current phase atomically. After T the next Phi_i acts on A under phase 0 as the first operation of the next word. Before T, a phase-2 track cannot reexecute either operation. Thus T consumes the complete old phase vector and supplies the next finite authorization in the same jump.

## 5. Concurrent recovery at arbitrary asynchronous phases

There is also an explicit recovery that can run during a partially completed word. This strengthens the receiver without changing its phase/service graph.

For r in {0,1,2}^5 let V_r=tensor_i W_(r_i). Let L_r embed V_r C into the currently selected banks, with every unselected bank vacant. Define R_r by:

1. discard every unselected bank;
2. identify the five selected qutrits and apply (V_r^sharp)^dagger;
3. apply R from (2);
4. apply V_r^sharp and install the result in the same selected banks, with unselected banks vacant;
5. leave r unchanged.

Dephase r and use this map in each of its 3^5 finite sectors. The resulting total CPTP proposal R_* is always enabled and can have an independent rate-mu clock. On a legal L_r state it is identity. It corrects every one-track error relative to L_r, including a corrupted local phase which selected the wrong bank: selecting/tracing the wrong pair is still an arbitrary map on that one track before the code recovery. It changes no phase, so it cannot disable a local move or T.

This is a finite family of explicitly specified channels rather than an unspecified decoder oracle. It is nevertheless a five-site engineered recovery channel. Its noisy microscopic realization has not been supplied.

## 6. Quantum and ownership theorem

**Theorem A.** Between two commits, allow an arbitrary finite number of onsite CP faults, all supported on one physical site i. A fault can act jointly on A_i, B_i, r_i and local reset controls, may leak data, and may correlate data with the phase. Allow arbitrary interleavings of Phi, reset, T proposals and optional R_* proposals. On the first next commit, the logical/reference output is exactly Ad_U on the previous commit's input. Each branch is a scalar multiple of this channel. All banks and phases are canonical afterwards. This statement holds for an arbitrary reference and for every i; the controller is not told i.

**Proof.** First omit R_*. Every other track j != i starts at phase 0, performs X_j then C_j exactly once, finishes at phase 2 with its result in A_j and B_j vacant, and waits. Its local reset proposals touch only vacancy. At site i all fault branches, wrong bank resets, repeated/skipped/reordered operations, source erasures and transfers are compositions of local CP maps. Terminal phase readiness may postselect such a branch, but does not alter its support. At T, discarding B_i leaves Kraus matrices from the original qubit A_i to the terminal qutrit A_i. Thus every terminal Kraus path is E_i U on the code, for an arbitrary one-site qubit-to-qutrit map E_i. Formula (3) gives the stated exact channel and input-independent scalar. The vacancy clears and phase preparation make ownership and control canonical. No copying or reconstruction of an unencoded unknown history was used.

With R_* present, maintain the stronger invariant that every branch is a one-track error after L_r applied to the intended logical state. A clean Phi_j updates r_j and its selected bank with precisely W_(r_j+1) W_(r_j)^dagger; a fault or wrong local reset stays on i. R_* corrects that invariant to L_r exactly by the same (3). At all-2, V_r=U preserves C; T yields the next canonical code state. This proves the theorem with arbitrary ideal recovery interleavings. The proof also covers faults at arbitrarily separated times on the same track, provided the first next commit occurs.

**Theorem B.** From every classical phase vector and every quantum/bank state, conditional on no further faults, the first next commit occurs with a clean service time dominated by

    S = max_(i=1,...,5) Gamma_i(2,lambda) + Exp(kappa). (4)

That commit returns a canonical cell. The logical output is unrestricted for a general damaged state. This is a general retirement statement for the finite cell, not an exact correction claim beyond Theorem A.

**Proof.** The rank d(r)=sum_i (2-r_i) lies in {0,...,10}. Every phase-changing local proposal lowers it by one, every pending track has its private rate-lambda proposal, and no reset or R_* action changes d. Thus each track needs at most two such arrivals. At d=0 the private rate-kappa T stays enabled. T then totalizes the quantum state by (2) and resets the controller. There is no raw occupancy predicate and no counter-surface consistency constraint that could trap malformed controls. This proves (4) independently of data and of activity in disjoint cells.

The same physical A/B registers are reused for any number of commits by induction. A fault may strand the real local share in the wrong bank; throwing away that share is permitted only inside the code-correctable track shadow. Uncorrectable damage is a bad logical cell output, followed by a clean controller. It cannot leave a surviving instruction source that changes arbitrarily many later gate locations at zero further fault cost.

The independence restriction is substantive. A finite collection of disjoint cells can retire any damaged set cell by cell, with local quantum errors on those cells. This does not give a growing-domain eroder on a coupled lattice, or a rendezvous rule for an intercell CNOT.

## 7. Physical time and all-set stochastic bound

Assume faults are exogenous independent onsite Poisson proposals of total rate at most rho in the cell (rho=5p for per-site rate p), with arbitrary onsite CP actions. Ideal gate, reset, commit and optional R_* clocks are independent. Faulty reset attempts may be represented by thinning reset proposals into ideal and arbitrary-onsite branches; their faulty rate is included in rho. Engineered T and R_* themselves are ideal fixed-support maps in this model; a faulty circuit decomposition of them is not covered.

Let m=E S. Exactly,

    m = 1/kappa + (1/lambda) sum_(j=1,...,5)
          (-1)^(j+1) binom(5,j)
          sum_(k=0,...,j) binom(j,k) k! / j^(k+1).    (5)

Also m <= 1/kappa + 2 H_5/lambda. For 0<theta<min(lambda,kappa),

    E exp(theta S) <= 5 (lambda/(lambda-theta))^2
                       kappa/(kappa-theta).         (6)

Every clean service state, including the state immediately after a fault, obeys the same bound. Declare an epoch bad if it contains at least two primitive onsite faults before its next commit. Theorem A makes every other epoch exact. A first-fault race followed by the uniform second-fault race gives

    Pr(bad epoch | arbitrary past) <= beta,
    beta = min(1,(rho m)^2).                          (7)

Indeed the first fault before clean completion has probability at most rho m; after it, without another fault, the total phase rule again completes within an S-dominated time, so the conditional second-fault probability is at most rho m. This deliberately counts two faults on the same track as bad even though Theorem A can correct them.

All commits occur almost surely even with ongoing noise. For any delta>0, a block interval of length delta has conditional probability at least

    q = exp(-rho delta)
        [1-exp(-lambda delta/2)(1+lambda delta/2)]^5
        [1-exp(-kappa delta/2)] > 0                  (8)

of completing a commit: no fault in the block, two local arrivals per track in its first half, and a T arrival in its second half. An earlier T already counts as completion. Thus Pr(T_next>k delta | arbitrary past) <= (1-q)^k and E T_next <= delta/q. Reset and R_* arrivals do not spoil this event.

Label epochs by the chronological commits of this cell. Every primitive fault belongs to exactly one epoch almost surely. There is no uncharged prehistory: faults while waiting, resetting, or doing local moves all belong to the current epoch. For any deterministic finite set J of epoch labels, repeated conditional use of (7) gives

    Pr(all labels in J bad) <= beta^|J|.             (9)

The inclusive bad-history maps are CP. Since the same bound holds for every quantum/reference input, their effects are bounded by beta^|J| I, hence their diamond norms are at most beta^|J|. This is a reference-uniform inclusive-subchannel estimate, not merely a statewise probability assertion. For the output immediately after the nth commit,

    ||actual_n - Ad_(U^n)||_diamond <= 2 min(1,n beta). (10)

The all-good part is an input-independent scalar multiple of Ad_(U^n) by (3); the bad union has CP norm at most n beta. These facts prove (10). This finite-cell estimate is not a level recursion.

## 8. What has and has not been removed

Removed at this fixed scale: one-use terminal authorization, permanent fresh output ports, stale finite tags, bank occupancy as a trusted oracle, a malformed local phase deadlock, and indefinite propagation of a controller discrepancy past a canonical commit. The corrected quantum word really is repeated on the same finite banks. Optional R_* supplies protected identity recovery during asynchronous partial progress in the same explicit model.

In a clean n-commit run, exactly 10n local gate/move events and n commits are accepted. The same ten qutrit banks are reused; no quantum bank or instruction token is permanently consumed. At unit rates, expected physical duration is n m. In that clean model the expected optional recovery count is mu n m and the expected optional reset-proposal count is 5 nu n m; disabled proposal attempts can also consume physical resources. Fault exposure during a run is bounded by rho times its full elapsed duration, including all such waiting and reset activity. A channel-level discard/preparation is specified, but reservoir entropy, work, engineering rates, calibration and actual dissipator cost are UNKNOWN.

The observation is the marked nth-commit cut. The model has no growing register storing n; an external mathematical observer may count the marked output events. At a deterministic physical time the number of commits and partial phase vector are random, so the theorem is a U^n transaction process rather than deterministic-time identity storage. Actual monitoring/readout hardware is outside the construction.

Not removed: a noisy local circuit for the five-site recovery/commit, control of faults inside such a circuit, interaction/rendezvous between cells, programmable nonperiodic universal computation, a recursive geometric eroder, level-uniform service and overlap, readout hardware, or a physical reset/energy/calibration demonstration. Treating an encoded growing block as one T or R_* jump would assume those missing operations. The model is a legitimate bounded-support bottom-scale generator; its physical engineering resources are unknown.

The supplied s03 finite receiver already used this code and its noncommuting X,C word. The independent change here is the total cyclic local phase/bank table, consumption and regeneration of the entire phase authorization at commit, and the phase-indexed recovery that can be concurrent with partial local progress. This is not a historical originality claim and is not a theorem about either cited paper's original generator.
