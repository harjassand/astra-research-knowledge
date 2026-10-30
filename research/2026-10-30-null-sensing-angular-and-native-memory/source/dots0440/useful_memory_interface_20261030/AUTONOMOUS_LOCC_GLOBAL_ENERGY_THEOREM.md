# Autonomous bilateral Bell protection in an explicit local-instrument/message model
2026-10-30. Constructed stochastic LOCC theorem, conditional only on the reviewed deterministic Tanner GPT density/confinement facts and the explicitly declared physical primitive class below. NOT a two-site-Hamiltonian/onsite-reset compiler theorem.

## Result first
There is a finite-state autonomous LOCC Bell buffer in a concrete broader Markovian jump model. It starts from physical Bell pairs with a small local source-fault envelope, not pre-encoded Bell states. It uses no persistent measured baseline, reliable classical records, external syndrome schedule, growing message identifiers or shared coherent quantum hub.

At fixed code degree, the apparatus has O(N) quantum/classical sites, fixed local dimensions, fixed message capacities and rates, and bounded graph-local supports. At sufficiently small exogenous local Poisson-CPTP fault rate it preserves k=Theta(N) encoded ebits for exponential physical time. A fixed ideal relative recovery gives known-Bell target trace error

    delta(t) <= 2 eta_source + C(1+t) exp(-cN).          (T)

The estimate is uniform for the allowed coherent syndrome gauge/reference states. It is a target-entanglement theorem, not an arbitrary-logical identity theorem on the joint two-party space. The resource can subsequently teleport an UNKNOWN already-encoded input using the separate full-physical-mask endpoint proved in SIGNED_BELL_ENCODED_TELEPORTATION.md.

The changed hardware scope is essential: quantum check/read/correction steps are atomic bounded-body LOCAL CPTP instruments, and interparty edges are finite-capacity measured classical FIFO channels. Their finite-duration two-site-gate implementation would need local locks and safe prefix/abort handling. This theorem does not assert that the original native coherent compiler already implements them.

## 1. Explicit autonomous machine and correction of one liveness ambiguity
Use AUTONOMOUS_LOCC_ARCHITECTURE_AUDIT.md together with the load-bearing FIFO_PROTOCOL_CLARIFICATION_AND_WORD_PROOF.md. The latter supplies the precise unconditional receive rule absent from an overly terse reading of the original protocol.

For every GPT hub h, allocate a Bob master/cache, an Alice worker, and private bounded-capacity FIFO request/reply paths. Alphabets are SYNC/READ and ACK/DATA(a). Every actual in-flight packet is one of the counted finite registers. Put G=C_req+C_resp+1, including the one possible worker-held reply.

After each local Bob watchdog, the master resets its cache and counter and obtains G+1 acknowledged SYNC probes before sending one READ. Alice responds to READ by an atomic local stabilizer measurement. When the reply arrives, one local Bob commit reads Bob's CURRENT relevant stabilizers, computes f_h(a+b), and applies the prescribed Pauli. It consumes its cache and begins another flush.

**Responses are dequeued in every master phase.** An ACK advances the counter only in FLUSH_WAIT; DATA is cached only in READ_WAIT; every other response is discarded. Without this rule, full request/reply queues and a master waiting to enqueue can deadlock. All unused physical basis encodings also have defined harmless transitions, or the registers are exact finite qudits.

The G+1 purge excludes every pre-reset READ/DATA by FIFO order. At most G old replies can exist or be generated. At least one accepted ACK is therefore fresh; every old request/reply precedes it. Leftover SYNC/ACK packets cannot generate DATA. No sequence tag or maximum packet delay is assumed.

Alice NEVER nominally changes her stabilizer syndrome. Bob obtains his own syndrome at the same atomic jump as his correction. Thus nominal transactions require no distributed locks or even Bob read locks in this primitive model. All quantum interactions remain within one laboratory. Every crossparty packet is measured/dephased before transmission.

Each operation is attempted by an independent fixed-rate Poisson clock; disabled attempts implement identity after the relevant classical basis read. Mathematically, each nominal term is lambda(Phi-id) for a specified bounded-body CPTP map Phi. Classical clocks are internal dynamics, not a fault-free external operating schedule. The favorable clock words below are proof events, never instructions sent by an external controller.

## 2. Faults, source and initial classical states
Each primitive fault support has an exogenous Poisson clock of rate <=epsilon, with bounded physical support and bounded incidence. Its action is an arbitrary CPTP operation on that support and a retained bath. Faults may be correlated through the bath and depend causally on past records. Clock locations/times, however, have the stated positive dominating Poisson law independent of the protected state. No uncharged continuous bath coupling is included.

Faulty operation attempts may be included by Poisson thinning: the good nominal attempt retains a positive fixed rate, while failed attempts are additional charged arbitrary local maps. Thus local resets, measurements, messages and commits are not asserted to be physically infallible. This is a stochastic fault-location model, not a conversion of generic weak continuous coherent noise into sparse events.

A primitive event is charged its direct paired-column DATA support and the full bounded read footprints of every master/cache it can corrupt or make stale. Controller-only events receive a nonzero declared support mass even if their immediate DATA action is identity. This pays for service interruption as well as future marked commits. Let s_p bound this charged mass and b_p the number of affected hubs; both are fixed.

The initial Bell source has a common positive-record support majorant Z_source. On its good event Z_source<=z0 N, every local Pauli coefficient term has a relative error representative of weight <=z0 N. The bad source-instrument mass is <=eta_source, uniformly over allowed gauge/reference inputs. A bounded-depth physical Bell source with sufficiently weak local-stochastic faulty locations is one example. A promise of only high per-pair average fidelity with unrestricted correlations is insufficient. Sparse missing/replaced pairs can be included as local source faults; slow asynchronous acquisition is not solved by this condition.

No clean classical-controller initialization is necessary for the variant proved here. Controllers, workers and all finite channel slots may initially have arbitrary states, including correlations with the syndrome gauge/bath. Start their ANALYTICAL marks at one. The DATA input must still lie in the stated Bell-target/error span. The initially arbitrary controllers can cause local bad commits before their first watchdog; the rate choice in Section 4 makes their total mass small with an exponential tail.

## 3. Exact unmarked semantics and no taint propagation
A fault marks every hub whose full dependency patch it touches. In particular an Alice DATA fault marks each cached read it can invalidate. A nominal watchdog of h clears h's analytical mark immediately.

This clearing is sound: after the watchdog the actual master must pass the complete FIFO purge before any new commit. Regardless of all old finite channel contents, absent a subsequent relevant fault the used Alice reply is genuinely fresh and stays valid until commit. Bob reads his current syndrome at commit. Thus EVERY unmarked commit is exactly the ordinary GPT move on the current relative error.

No marked commit can create new stale Alice records: it acts on Bob only. It can create a bounded relative DATA error, already charged to its own full patch, but it does not propagate controller taint. Nominal Alice measurements commute with every stabilizer and only project/dephase the Bell gauge. The mark process is therefore a birth/reset process, not an unproved branching infection process.

All assertions are coefficientwise on one actual positive fault/clock record. Local fault operators may be expanded in Pauli/matrix-unit components with retained bath coefficients. Nominal basis-reading channels define ordinary finite classical histories for each component. Marks depend only on the actual record, not a sampled Pauli component or a hidden perfect physical flag.

## 4. Marked-commit moments, including arbitrary initial controller states
For one hub let a<=nu epsilon be its total mark-birth rate, mu its watchdog rate, and lambda its commit-attempt rate. Commit attempts are counted even when their guard is disabled. These three exogenous clock families are independent. Dominate the mark by a two-state process 0->1 at rate a and 1->0 at rate mu, starting at 1.

For any selected measurable time set A, let K_h(A) count commit attempts while marked. Set v=lambda(exp(theta)-1), and require mu>v. Conditional on the mark trajectory, the count has Poisson exponential moment exp(v integral_A m(t)dt).

The backward Feynman–Kac equations for g_0,g_1 are

    g_0'=a(g_1-g_0),
    g_1'=mu(g_0-g_1)+v 1_A g_1,
    g_0(0)=g_1(0)=1.

With x=g_1/g_0-1>=0,

    x'=v1_A+(v1_A-mu-a)x-a x^2
       <=v1_A-(mu-v)x.

Hence integral x<=v|A|/(mu-v), x<=v/(mu-v), and

    E_0 exp(theta K_h(A)) <= exp[a v|A|/(mu-v)],
    E_1 exp(theta K_h(A)) <= mu/(mu-v)
                                  exp[a v|A|/(mu-v)].   (4)

The second line handles arbitrary initial controller states. It also bounds each later window conditional on an arbitrary earlier mark pattern by domination with all marks equal to one. The estimate works for disconnected A; it does not posit independent marks in successive windows.

For many hubs, color the bounded-overlap graph of their primitive-fault clock sets. Within one color the mark/watchdog/commit clock families are independent. Generalized Holder combines the colors; an additional Holder factor combines marked commits with direct primitive counts. Full patch weights add a further fixed dilation of theta. Perform ALL these dilations before choosing mu/lambda. For a fixed window T, the all-DATA bad support mass Q_j obeys a bound of the form

    log E exp(theta Q_j)
       <= N [b0(lambda/mu,theta)+epsilon b1(T,theta)],  (5)

where b0 tends to zero as lambda/mu tends to zero and b1 is finite at fixed rates/T. Direct primitive counts contribute their ordinary Poisson moment. This bound is uniform in j, including the initial window with arbitrary controller contents, and in all protected states/references.

Given q>0, first choose lambda/mu small enough that b0<theta q/4. After fixing T, choose epsilon small enough that epsilon b1<theta q/4. Chernoff yields

    Pr(Q_j>qN)<=exp(-theta qN/2).                       (6)

Rates may become impractical; they remain positive constants independent of N. Slowing commit attempts makes service rarer but does not destroy the uniform finite service word.

## 5. Real service and its actual-clock miss majorant
The FIFO clarification proves a finite universal word: fire the local watchdog, apply sufficiently many fixed round-robin attempts to every enqueue/dequeue/worker/hop clock, then fire the local commit. Unconditional reply draining prevents deadlock. Packet accounting bounds the required repetitions independently of payload values, quantum state and previous controller contents.

Place these finitely many required attempts in successive positive-duration boxes, excluding extra h-watchdogs and any other interfering private attempts within the word. Its probability p0>0 and duration T0<infinity depend only on the fixed local machine. The word contains a watchdog, so initially marked or corrupted masters are not an obstruction. No neighboring Bob commit needs to be prohibited: Bob's final snapshot is current. A neighboring move that changes an active candidate's raw dependencies already resolves that candidate in the energy accounting.

Repeat J independent clock-word trials in a window T=J T0. Define M_j^clock to count hubs with no successful clock word. Their miss probability is at most q_m=(1-p0)^J. Private hub clock families are independent; a finite conflict coloring would suffice if a particular physical layout shares boundedly many clocks. For any prescribed small m>0, choose J so q_m is small enough that

    Pr(M_j^clock>mN)<=C exp(-c_m N).                    (7)

A word spoiled by a primitive fault is not called a clean evaluation. It is paid instead by that fault's charged support: each fault can spoil at most b_p local word/candidate tests. This is why controller-only faults were included in Q_j. The word need not be conditioned to be fault-free when defining the independent miss majorant. Consequently no independence between Q_j and M_j^clock is needed.

## 6. Explicit energy contraction and first exit
Use the reviewed Tanner integer potential U from INTEGER_ENERGY_D0_D1.md. For each CSS sector it is stabilizer/syndrome invariant, U<=2|e|, a local Pauli mask f changes it by at most 2|f|, and every nontrivial unmarked commit lowers it by an integer >=1. Below a fixed linear reduced-weight radius,

    U>=h |R|,       number of active hubs >=kappa U.

Here R can be the fixed minimum same-syndrome representative used by the canonical proof. The same hypotheses hold in both sectors with common worst-case constants.

At the start of a safe window pack at least kappa_p U_j active candidates with disjoint full raw-syndrome dependencies. A clean accepted move resolves at most C_res candidates, a bad DATA mask resolves at most c_d times its charged mass, and a primitive service interruption resolves at most b_p candidates per charged event. Every remaining candidate with a successful unspoiled service word is correctly evaluated and forces a decrease. Therefore, for D_j the total clean decrease,

    kappa_p U_j <= C_res D_j+c_Q Q_j+M_j^clock,
    U_(j+1) <= U_j-D_j+2Q_j.

Thus, with fixed a=kappa_p/C_res in (0,1),

    U_(j+1) <= (1-a)U_j+A Q_j+B M_j^clock,
    A=2+c_Q/C_res, B=1/C_res.                         (8)

This is the reviewed persistence argument with an explicit additional local-spoil constant; it is not an independent-scheduler assumption.

Choose r>0 strictly below both Tanner linear confinement cutoffs, with 2rN+s<d_N for large N; s bounds one local relative Pauli edge. Choose small source/mass/miss budgets z0,q,m and put

    v_star=max{2z0,(Aq+Bm)/a}.

Take them small enough that

    v_star+2q < h r/2.                                (9)

On the good source/window event, (8) gives U_j<=v_star N. Between boundaries clean moves decrease U and bad masks increase it by at most 2Q_j, so U<= (v_star+2q)N throughout.

If a canonical minimum-syndrome representative first reaches weight rN, the preceding representative has weight at least rN-s, remains below the confinement cutoff, and hence has U>=h(rN-s), contradicting (9). Candidate packing requires only the safe window start, so this first-exit induction is not circular.

Energy alone does not exclude a logical error. At the source, the small physical relative error and its minimum-syndrome representative differ by a zero-syndrome operator of weight <=2z0N<d_N, hence by a stabilizer. On each subsequent local edge f, consecutive canonical representatives satisfy

    sigma(R+f+R')=0,    |R|+|f|+|R'|<d_N.

Their difference is again a stabilizer. Therefore every safe coefficient history stays in the SAME correctable logical Bell class, not merely at low syndrome energy. Include both CSS sectors, choosing radius budgets so the combined physical representative is inside the final common recovery radius.

## 7. Quantum error bound and preparation consequence
Let L=ceil(t/T), and include the complete last window when bounding an intermediate observation time. Source failure and (6)-(7) give one positive bad-record instrument of mass

    delta_bad <= eta_source+C(L+1)exp(-cN).            (10)

This is an unconditional union bound over actual records. Temporal independence, conditional restart after observed outcomes, and a local-stochastic residual state are not assumed.

Every safe record maps the coherent Bell target/error span into the same relative-correctable span by Section 6. The fixed ideal decoder measures the final bilateral syndromes, corrects their difference, then uses matched signed-sector decoders. BILATERAL_SCHEDULED_CPTP_ADDENDUM.md Section 5 supplies the algebraic common-span factorization, which does not rely on a circuit schedule. It extracts the SAME pure logical Bell state from every safe Pauli coefficient, placing all syndrome phases, controller records and retained bath dependence outside that factor.

Positivity gives target trace error <=2 delta_bad, proving (T). Uniformly over gauge inputs and references this may also be written as a diamond bound from the gauge-input channel to a constant logical-Bell-output channel. It is NOT identity-channel protection for arbitrary unknown states in the enlarged joint stabilizer space.

Raw physical Bell pairs equal W|+>^(N-k), so the theorem needs no complete initial syndrome-measurement barrier or high-energy global Pauli-frame computation. The local source-support condition supplies the initial relative-error seed. The physical number of shared pairs and their acquisition remains a real entanglement resource.

## 8. Honest consequence and exact hardware boundary
This closes an actual AUTONOMOUS stochastic LOCC Bell-buffer architecture in the declared broader primitive class. It does not merely rename a joint coherent hub as classical. All channel slots, old replies, corrupted counters, reset delay, stochastic service and early bad commits are represented and charged. Reliable classical storage and a global error-correction schedule are absent.

The strong ordinary comparator remains the noisy fixed-iteration scheduled Tanner circuit in NOISY_CLASSICAL_ORDINARY_COMPARATOR.md. It uses the same physical Bell source and can implement the same purification, waiting and physical-mask teleportation. No asymptotic memory advantage or practical numerical threshold over that comparator is established here.

To claim the ORIGINAL native hardware scope, the next exact action is to replace the atomic Alice/Bob local instruments by finite local quantum gate modules while preserving local exclusion, prefix frames, safe abort/reset, and the classical-message purge. Crossparty communications must remain measured classical channels throughout, not just after a completed Stinespring unitary. That local quantum compiler problem has not been solved by this broader theorem.

Actual physical teleportation/swap also requires its declared finite-duration mode/control endpoint. Before applying its extensive raw mask, an ordinary zero-syndrome recipient cannot simply resume correction. Bare-state loading/output, arbitrary-delay message endpoints, magic states and universal quantum computation remain outside the claim.
