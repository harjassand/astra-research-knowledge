# Independent whole review: native stochastic LOCC rollback integration

2026-10-30. **PASS in the precise scope below.** This reviews the new physical compiler, live FIFO composition, delayed semantic taint, COUNT moment, actual service, and global assembly together. It does not promote an earlier atomic-instrument theorem or a finite regression into a native theorem.

## Frozen objects

All sources are in `producer-workspace/native_locc_rollback_integration_20261030`:

| Source | SHA-256 |
|---|---|
| `EXTENDED_MACHINE_AND_OPERATOR_PROOF.md` | `73e1b695d260dc3821ea39c4241bd33730cf5b393bf478c6ca512fbb4c9ab34b` |
| `DELAYED_ALICE_TAINT_AND_SERVICE.md` | `16ae051c86742c7bdc606e262aa1db7960f4e3afd7b3762ac1d91145dd46a7ef` |
| `DEPTH_TWO_EMISSION_COUNT_MGF.md` | `ac73de80c09d8789ee394bf5703c240de68e48bb9ab81b8514db0170697a5d76` |
| `ACTUAL_SUCCESS_SERVICE_AND_GLOBAL_ASSEMBLY.md` | `b3cbf9b11cbfc41a8c4f130527711f7875235dbc046bbda8fec8717bdc6eb810` |
| `EXPLICIT_LOCAL_PAYLOAD_GATES.md` | `e85cbcbaa20d3e789a55fd506708f7c4cd34ae2befa5d5c457534fe240a68df3` |

Exact imported dependencies, scripts, and independent snapshots are recorded in `SOURCE_MANIFEST.json` and `SOURCE_SHA256.txt`. Earlier challenge notes and available pre-freeze snapshots remain preserved. `FUTURE_SEMANTIC_FLAGS_NOT_GOVERNING.md` is excluded from this verdict.

The accepted result is a finite-rate **nominal LOCC Bell buffer** with local onsite/two-site Hamiltonians and onsite resets on fixed-dimensional grouped quantum sites, plus separately declared measured finite-capacity classical transport. With the stated clean native initialization, reviewed Tanner hypotheses and Bell-source envelope, sufficiently small exogenous local Poisson-CPTP fault rates give

`target trace error <= 2 eta_source + C(1+t) exp(-c N)`.

The output includes the explicit local forest inverse followed by fixed ideal relative recovery. Constants are fixed with N and may be extremely poor. The claim is for the known logical Bell target/common gauge-reference span, not arbitrary-logical identity protection of the enlarged bilateral space.

## 1. Actual quantum payload, not an atomic read oracle

The supplied gate lists implement the required instruments exactly. For a commuting stabilizer S_j, the hub Hadamard, resource-by-resource controlled Pauli factors, and final Hadamard implement coherent extraction of its syndrome. Commutativity gives the joint projector decomposition `sum_b Pi_b |b>`. Alice's actual workspace-resolved terminal resets write b into the physical HOLD register and implement `Pi_b rho Pi_b`.

Bob first executes the same extraction, then the explicitly defined onsite permutation `c -> c XOR enc[f_h(a XOR b)]`, then resource-by-resource controlled corrections. On a clean entry source its resolved Kraus operator is `Pauli[f_h(a XOR b)] Pi_b`. The table gate is a finite, completely specified permutation on the grouped hub, including nonzero input c. It is not an elementary-qubit locality claim. Gate counts, workspace dimensions and program dimension are bounded independently of N at fixed code degree.

These U_t appear only on the stated native rail edges. No timed external quantum pulse, coherent interparty bus, or instantaneous all-resource quantum measurement is left in the implementation. Measured classical transport remains an explicitly granted resource rather than a derived relativistic communication carrier.

## 2. Whole-alphabet forest and individual no-creation

For every actual owner mask, the deleted-edge forward forest is well defined. Each backward copy B_(j0,l) uses the same V_l, so every available inverse edge flattens. A C_t-to-B_(t,t) watchdog has equal source/target frame and cannot erase a live prefix. Every R leaf inherits its parent frame and claims all resources; this is important even when its parent is I/A/Q.

An F_h factor has nonidentity DATA action only on resources actually tagged o_h. Distinct owners' DATA actions are disjoint in each common tag sector, and their diagonal tag controls commute. All Hamiltonians flatten to controller-only operators. Acquisition, cleanup and other owners' tag transitions preserve a live owner's actual mask. The live C/B/R(C/B) region has no reset-free exit to reacquisition; a complete T_h retirement is unavoidable before that owner's usable DATA set can change.

In this frame the good projector is DATA independent. Acquisition/unacquisition, verification, payload/rollback, consistency edges, monitors and each individual reset preserve its range. A failed-test edge has zero good source; its reverse cannot enter a consistent source under the same failed-test guard. Complete T_h outputs lie in the good Q0 range for every tag configuration. Scalar complete-erasure losses commute with the good projectors. These are individual Kraus/range statements, not merely averaged defect estimates.

Consequently DATA-Pauli expansion preserves good-source and regeneration inclusions coefficientwise. No Pauli coefficients are treated as probabilities. All nominal non-reset evolution remains controller-only; unmarked terminals are the actual intended instruments; dirty emissions and primitive faults have bounded DATA support. Clean rollback has no DATA Pauli even with an incorrect immutable program. For a mechanically clean but semantically marked Bob engine, therefore, only SUCCESS needs a bad DATA charge. Mechanically marked retirements can all be charged conservatively.

## 3. The three original integration objections are resolved

### Actual owned support, not worst-case footprint

A dirty Bob reset acts only on its actually owned DATA. Another mechanically clean committed Bob engine owns its entire raw-read footprint, so these supports are disjoint. A clean engine still acquiring has not yet taken a snapshot. This prevents Bob-to-Bob snapshot invalidation and is stronger than merely knowing that dirty actions have bounded worst-case support. Bob never changes Alice DATA; nominal request messages ask only for SYNC/READ.

### One ghost reply really means one

Alice can enqueue HOLD and process a new request only at engine I. In malformed C+HOLD, terminal overwrites HOLD before readiness, or abort preserves it. It cannot export the held value and then an additional old live-prefix result. Quantum phase coherence does not evade the argument: an actual enqueue gain has the I source projector and eliminates the C alternative. Pending REQUEST survives every cancellation until a successful read produces its single reply.

Thus `G=C_req+C_resp+1` counts all old queued, active and held reply capacity. Bob receives in every phase and accepts labels only in their designated wait phases. After G+1 accepted SYNC acknowledgments, one is fresh, and strict FIFO/worker serialization puts all older READ/DATA before it. The purge does not require a packet-delay bound or growing epoch identifiers.

### Native initialization cannot be arbitrary

Initially malformed quantum engines can each emit a fast DATA-changing reset even at zero external fault rate. Slowing SUCCESS does not suppress such dirty aborts. The concrete accepted initialization is engine I, initialized W/P, all owner tags free, and Bob master FLUSH_SEND(0) with empty cache. Arbitrary finite classical FIFO/Alice-worker contents are allowed behind this actual first purge. Arbitrary initial Bob WANT is not included. Sparse initial native-history variants require a separately quantified source/ancestry proof; they are not obtained merely from regeneration.

## 4. Delayed Alice corruption and exact bounded ancestry

The delayed Alice mechanism is real. A malformed A state missing an earlier resource can later acquire a different resource after a neighboring read has finished. It may then execute part of a stabilizer-read circuit before an ownership failure and dirty reset. This can change the Alice syndrome after Bob already retired and purged.

An independent two-DATA-qubit calculation in this audit directory checks the example with commuting XX and ZZ: starting in Phi+, a full XX read preserves ZZ, whereas stopping after the first controlled-X and resetting the ancilla makes the cached ZZ value wrong with probability 1/2. The finite monitored machine gives positive probability to this allowed acquisition/prefix/abort path. Primitive-only Bob marks are therefore insufficient.

The repaired passive mark process sets new Bob semantic marks at each mechanically marked Alice retirement, using a bounded superset of affected read/reply dependencies. Bob T clears the mark only after its emission and starts a compulsory purge. Delayed old packets cannot cross that future quarantine uncharged. Combined mechanical/semantic Bob births are assigned a unique LAST cause since the preceding T.

Each primitive root can parent at most b_A Alice retirements, at most b_B direct Bob retirements, and at most b_A c_AB secondary Bob retirements. Overwriting a cause cannot increase this fanout. The total charged descendant mass plus direct primitive mass is bounded by a fixed K. Depth is at most two. Under combined-LAST attribution, the second-layer Bob endpoint must include ALL charged T, including a dirty abort whose earlier mechanical defect survived a later Alice semantic birth. The final source includes this correction.

## 5. Actual retirement and service effects

The entire native alphabet has an explicit path to an actual complete retirement: I/A/Q/R have a direct watchdog; C can enter its equal-frame rollback copy; a consistent B can reverse to zero; an inconsistent B has an enabled distinct failed-test leaf and reset. A disconnected malformed rollback rail is not incorrectly declared absorbing at zero.

The imported finite-rate monitor proof applies to these NEW blocks, complete scalar losses, finite alphabet and incident norm budget. It gives an integrated-window full-Hilbert contraction for deleting the actual T gains, including arbitrary workspace/program states and outside/reference entanglement. New parameters and local-polynomial witnesses are required; no old resolvent or numeric tail constant is reused. It does not assert a uniform instantaneous hazard on B.

For useful service, the old two-RETIREMENT certificate is invalid because clean native aborts occur. The new passive counter counts actual SUCCESS only. Its full-state contraction follows from a finite actual-record word: retire the target, retire/clean/park the finitely many competing owners, finish the finite FIFO purge, execute actual Alice READ and Bob payload macros, and take the actual terminal. All outcomes are retained. Parking selects no-LOAD/no-I-watchdog records while retaining their losses; it does not replace the running generator with halt mode. Every background Hamiltonian stays present and is charged in the local projected-path bound. The all-label finite word and actual monitor estimates therefore give a uniform positive effect, not just basis reachability.

Repeat the successful word if the counter starts at zero. This yields full alive-counter contraction even for artificial counter=1/dirty-physical inputs; their semantics are unnecessary for this operator estimate. The anchored polynomial construction gives a NEW finite-support positive witness for the genuine killed fewer-than-two-SUCCESS instrument. Buffered products and small additive Poisson-kick robustness yield

`Pr(all h in A have fewer than two successes in a length-T window) <= C_s^|A| exp(-gamma_s |A| T)`.

There is no independent-coin assumption. Uniformity over entering states permits any deterministic window location. Packing and a union over subsets then give an exponentially small tail for the total number M of owners missing two successes. A later success is a fresh correct evaluation unless a relevant primitive fault or dirty Alice retirement spoiled it; those are charged separately in Q. Previous-window marks are cleared by the first actual retirement, and any first bad emission in the current window is itself charged.

## 6. Independent derivation of the COUNT MGF bridge

The earlier occupied-cell ancestor theorem is insufficient for repeated emissions in one cell. The new proof instead counts DISTINCT primitive roots effective for a deterministic time set W. Let Y_W count roots that occur in W or have a charged descendant in W. Pathwise `Q_W <= K Y_W`.

For k distinct effective roots, choose just one witnessing descendant path per root. Unique canonical ancestry excludes sharing an intermediate Alice retirement between distinct roots. At any owner, successive selected intervals are separated by its preceding actual T, so their interiors are disjoint. There are at most 2k no-T intervals, 2k selected reset gains and k root insertions. This validity is established before any assignment restrictions are dropped.

For a deterministic valid family with total duration ell, choose the buffered spatial witness color carrying at least ell/P. The actual event is contained in the corresponding color's no-T event. The positive product-witness comparison, with all unselected faults retained, bounds its effect by

`alpha^(-m) D^q exp[-(rho/P) ell] I`.

Turning interval factors on/off costs at most alpha^{-1} per interval. A prescribed local CPTP insertion costs a fixed D, because it touches only boundedly many factors. A selected actual reset gain J satisfies `J*(I)<=kappa I`; dividing by kappa and adding the missing-effect Kraus operator gives a local CPTP completion for an UPPER bound. The physical generator is not changed into a Poisson reset-attempt model. These comparisons remain valid with a common retained bath because the witness factors are positive system operators and the maps are completely positive.

With beta=rho/P and a fixed C0, every selected root is bounded by the kernel

`g_W(tau)=C0[1_W(tau)+A1 kappa integral_W exp(-beta(v-tau))dv`

`                         +A2 kappa^2 integral_W (v-tau)exp(-beta(v-tau))dv]`,

where each integral has v>=tau. The second-layer intermediate time integration produces v-tau, because the Alice and Bob interval lengths add to that delay. Importantly C0 also multiplies the zero-edge term: such a root can still touch another path's larger witness support. The final source includes this repaired constant.

Tonelli gives `integral_0^t g_W(tau)dtau <= C1 |W|`, including disconnected W and old roots. Apply the exogenous Poisson factorial expansion over DISTINCT selected roots. Keep valid canonical domains while applying the killed comparisons, then enlarge to unrestricted nonnegative scalar kernels. The k-th term is bounded by

`[epsilon nu N C1 |W| (exp(theta K)-1)]^k/k!`.

Summing proves the asserted positive tilted-instrument/effect bound. It is uniform on positive subnormalized inputs and references, not a normalized rare-record argument. No independent delay distribution or independent Alice reset process is introduced. This establishes a global physical-time COUNT moment sufficient for the linear-radius energy theorem; it does not assert a new arbitrary spatial local-stochastic emission law.

## 7. One common record, parameters and logical endpoint

The enlarged Q includes immediate dressed faults, mechanically marked Alice/Bob retirements, semantic-only bad Bob SUCCESS, and bounded local service/semantic footprints. Every such footprint and its candidate incidence is fixed. M counts all physical owners missing two successes, so it majorizes any data-dependent packed candidate subset without applying a probability theorem to an adaptively selected set.

The no-creation and payload identities hold coefficientwise on one actual record. Unmarked terminals are current-syndrome GPT evaluations; unresolved candidates preserve their raw dependencies, so a later unspoiled success forces the reviewed integer decrease. Every clean move, bad mask or service spoil resolves only boundedly many packed candidates. Thus the reviewed deterministic counting argument gives, with enlarged fixed constants,

`U_(j+1) <= (1-a) U_j + A Q_j + B M_j`.

A noncircular choice is: fix code/read-footprint/circuit/FIFO/monitor/rate constants and new witnesses; choose a safe common radius and small source/mass/miss budgets; choose a fixed T large enough for the SUCCESS shortfall tail; then choose epsilon small enough for BOTH witness robustness inequalities and the COUNT Chernoff exponent at that T. Native clean initialization removes the old arbitrary-controller boundary term; it is not bounded by an unjustified fast-watchdog approximation.

For example require `v_star=max{2 z0,(Aq+Bm)/a}` and `v_star+2q < h r/2`, together with confinement and distance margins. For two CSS sectors the combined representative must fit the common recovery radius; equal radii can conservatively satisfy `4rN<d_N`, not merely the individual edge inequalities. Work at N>=N0 for these fixed margins.

Clean moves decrease U and bad masks increase it by at most twice their charged mass. The first-exit argument therefore bounds within-window energy before invoking confinement. A local Pauli edge changes canonical minimum weight by at most its bounded support. At a first radius crossing the preceding representative remains in confinement and contradicts the energy cap. Consecutive canonical representatives differ, after the local edge, by a zero-syndrome operator of weight below distance; hence they differ only by a stabilizer. Low energy alone would not establish this logical-class conclusion.

At observation t the final source uses completed service windows plus Q on the final PARTIAL interval only. No partial-window service event is needed, since `U(u)<=U(window start)+2 Q_partial`. Thus the safe/bad CP instrument uses only records available by t; no future quantum SUCCESS outcome is used to condition the t-output. The COUNT bound applies to the partial interval as well.

All Pauli coefficients of a safe record remain in the same correctable Bell-target span. The explicit `F_A^dagger tensor F_B^dagger` and fixed ideal relative decoder extract the same pure logical Bell factor, leaving syndrome gauge, bath and records outside it. A positive bad-instrument bound delta therefore gives target/reference trace error at most 2 delta. Union over completed windows and the partial mass yields the stated `2 eta_source+C(1+t)exp(-cN)` estimate without temporal independence or mark restarts.

## 8. Regression evidence and exact acceptance boundary

I reran independent copies of all four supplied regressions. The owner table checked 66,825 states and 449,190 transitions, including 357,957 live-ownership checks; FIFO tests found zero stale acceptance/dead states; the explicit payload Kraus error was at most 1.67e-16 and every prefix inverse error at most 6.67e-16. The ancestry bookkeeping tested 250,000 events and included 8,233 second-layer dirty-abort endpoints. The additional partial-Alice-read calculation was independently written here. These tests support finite algebra and record invariants; none substitutes for the operator probability arguments above.

The accepted noise model is additive sparse exogenous Poisson CPTP kicks with bounded support/incidence and arbitrary retained-bath actions at those locations. Actual nominal reset channels remain present and separately recorded. There is no uncharged continuous system-bath coupling, no arbitrary signed perturbation that removes the reset instrument, and no imported continuous-noise or topology-free corollary. The nominal apparatus is LOCC; adversarial shared-entangled-bath faults need not make the total faulty channel LOCC in the resource-theory sense.

The result still requires its common positive-record Bell-source support envelope, clean native apparatus, maintained reset/monitor resources, fixed-degree graph-local grouped-site architecture and declared measured classical communication. High average pair fidelity alone, arbitrary initially dirty native engines, bare DATA output at arbitrary time, efficient/physical ideal decoding, universal computation and practical threshold estimates are not certified. No external mutation or permission blocker occurred. Author sources were not edited by this audit.
