# Transactional controller: actual terminal-or-abort reset tail

Date: 2026-10-29. Mathematical certificate for the explicitly monitored, noiseless generator specified below. Not a data threshold, and not a claim that a dirty terminal reset performs correct logical recovery.

## 1. The event and the killed CP instrument

For a specified owner h, designate ONLY its complete terminal and abort reset channels as events:

J_T,s = sqrt(kappa_T)|Q0,0><C_L,s|,
J_R,a,s = sqrt(kappa_R,a)|Q0,0><R_a,s|.

Workspace outcomes s are separate Kraus channels, with complete summed intensities kappa_T P_C_L and kappa_R,a P_R_a. Commitment A_k→C0 is NOT the event. Cleanup/ready resets and monitor emissions are NOT the event.

Let L be the actual full augmented generator, including the finite-rate clock monitors. Delete the designated gains, retaining ALL their anticommutator losses:

K_h = L - sum_(designated J) J(.)J*;  N_h(t)=exp(t K_h).

N_h is exactly the CP, trace-nonincreasing instrument for no designated event in [0,t]. It is not exp(t L) projected on a bad-clock subspace. The event probability is 1-Tr N_h(t)(rho), even if the initial state is entangled with an arbitrary reference. For any CP map, ||N_h||_diamond=||N_h^*(I)||_infinity. Consequently a uniform event probability is precisely the operator estimate needed for the diamond bound.

## 2. Required actual-generator facts

The alphabet has distinct A_k and C0, a complete one-way commitment reset A_k,s→C0,0, and NO coherent C→A transition. C_t↔C_(t+1) uses a unitary workspace/data gate and a projector onto h's ownership on its actual target resource. C_t claims every resource. ALL abort labels R claim every resource for the purpose of disabling cleanup: no h-cleanup edge is active in R. Terminal/abort reset moves to Q0 and completely overwrites workspace. Q cleanup and verification then release tags. A acquisition/reversal and Q cleanup/verification are as in the repaired no-epoch model.

Every inconsistent ordinary phase has a distinct enabled abort destination for every failed local ownership test. Each selected nonzero Hamiltonian block is unique and is g U times its eligible clock projector, with g≥g_min>0. Summed ordinary no-jump losses are clock diagonal. Reset intensities are positive uniformly on workspace. All local dimensions, circuit length L, support k, incident-owner bound d, and all local interaction/rate norms are fixed. Include ALL generator terms touching the proof patch in the norm budget, including boundary-crossing terms. No perturbative data noise is silently included.

Add the actual on-site two-level reset monitors of `ordered_lease_schedule_20261029/EXACT_RESET_MONITOR.md`, with fixed Omega,kappa_m>0. They resolve only clock/lock labels, never data or workspace. All main terms act trivially on monitors.

These are operator hypotheses, not a certification that a separately supplied implementation passes them. The new generator's regression receipt must check the unique blocks and complete reset losses. A coherently summed workspace reset is not a substitute.

## 3. Short path for computation sectors

After a joint clock/lock-label projection of h and its resources:

* An R label has a one-step direct abort reset, independently of locks and workspace.
* A C_t with a failed ownership test has the two-step path C_t→R_(C_t,j)→Q0.
* A C_t with every lock o_h has the forward circuit path C_t→...→C_L→Q0, of length at most L+1. Gates are unitary on the entire dirty workspace/data state, so this probability argument requires no clean-history premise.

Thus m_C=max(2,L+1) selected steps suffice from arbitrary C/R labels. Lock labels can be arbitrary initially. After projection, the relevant block is norm preserving, even on an arbitrary reference-entangled input. No path reverses into acquisition.

For iteration restricted to C/R inputs one must distinguish R_C from R_A or R_Q. Before the first designated reset, the span of C_t and their attached R_(C_t,j) is invariant. Therefore the short bound iterates there. An arbitrary R_(A_i,j) may return coherently to A_i without resetting; an R_Q can return to Q. The full-alphabet construction below removes this restriction and is needed for the phrase "arbitrary R" without qualification.

## 4. Full-alphabet bounded path

Set N_h to the other owners sharing a resource with h; |N_h|≤k(d−1). Let Gamma consist of these owners, h, and ALL of their resources. The number of complete physical sites is at most n≤[1+k(d−1)](k+1). A fixed larger bound is harmless.

ClearOwner(j), from a projected arbitrary local configuration:

1. If j is inconsistent, take one enabled abort edge then its complete abort reset to Q0. If already R, take its reset.
2. If j is consistent C_t, progress FORWARD to C_L and take terminal reset to Q0. (The old C rollback-to-A path is unavailable and must not be reused.)
3. From Q_i, remove all own o_j/z_j outside the verified prefix using o_j→z_j→free, then advance verification to Q_k and ready-reset to A0. Already verified resources have no own tags. These operations do not acquire any resource.
4. A consistent A_i instead reverses its acquisition prefix to A0. It has no own tag outside that prefix.

At termination j is A0 and has no own tags. No workspace refresh is needed for this probability result. A conservative bound is

M = L+3k+4

selected steps per owner. This dominates the bad→abort→Q path, the C-forward→terminal→Q path, and the A reversal path. During the selected record, suppress competing local transitions by the no-local-reset and projected-path construction; this is an event subset, not physical feedback.

First ClearOwner(h), then each j∈N_h. Any terminal/abort reset of h already counts as success and the analysis stops caring about future states. Otherwise after clearing all these owners every target resource is free. Acquire h's k resources, take its complete commitment reset, progress L circuit edges, and take its terminal reset. No outside owner can have a tag on a target resource: every incident owner is in this bounded patch. Clearing another owner never acquires resources, so it cannot re-block a cleared target lock.

A common length bound is

m = [1+k(d−1)] M + k + L + 2.

Pad shorter branches with idle checks before success, or unrestricted evolution after an absorbing *analysis event flag*. This flag records that a real designated jump already occurred; it is not an added physical transition. Paths and predicates are chosen from recorded clock outcomes only. Their union is a genuine subset of actual trajectories.

## 5. Finite-rate probability constants

Let B≥1 bound the sum of norms of all main Hamiltonian terms touching Gamma plus half the summed ordinary no-jump loss norm bound there. Ordinary includes commitment, terminal, abort, workspace, ready, and lock-cleanup instruments. Terms outside Gamma are retained as a CPTP semigroup. Let kappa_min>0 be the minimum intensity among selected reset steps, including commitment and cleanup/ready resets when used. Set

delta ≤ min(1/(16B), g_min^2/(16B^3)),
p0 = min(g_min^2 delta^2/4, kappa_min delta/4, 1/4),
epsilon ≤ min(1/(16B), p0^m/[8B(m+1)]).

The projected-path Dyson estimate supplies ≥p0 per Hamiltonian/reset/idle step, uniformly over the arbitrary conditional outside/reference state. The error replacing each ideal measurement by a finite sequential measurement window is ≤4B epsilon in diamond norm for the complete recorded instrument. There are m+1 such windows, hence normalized selected-record success ≥p0^m/2. This is the full instrument bound, not an outcome-by-outcome error multiplied by the number of labels.

For reset monitors define A=-i Omega X-(kappa_m/2)|1><1| and

F_u = integral_0^u kappa_m exp(A* s)|1><1|exp(A s) ||exp(A(u-s))|0>||^2 ds,
alpha(u)=lambda_min(F_u)>0.

Positivity follows from observability of (A,<1|): a vector annihilated for an interval has both components zero because Omega>0. Let

w = alpha(epsilon/n)^n exp[-kappa_m(n−1)epsilon],
T = m delta+(m+2)epsilon,
p = (p0^m/2) w^(m+2) exp[-kappa_m n m delta] >0.

The extra window flushes arbitrary initially entangled monitors, by one resolved reset per monitor. After the flush their timing process factors independently of the main system. Timing-density conditioning precedes the O(B epsilon) comparison, so there is no error division by w. Early designated resets during the flush or measurement windows are counted as success, not discarded. Equivalently use the absorbing event flag when comparing instruments. For the C/R_C-only theorem use Gamma={h and its resources}, m=m_C and its corresponding B,n.

Therefore, for EVERY full physical/reference state, P(at least one h terminal-or-abort reset by T)≥p. All constants depend only on fixed local parameters, not total graph size. The bound is deliberately very pessimistic.

## 6. Exponential diamond tail, with exact quantifiers

The uniform probability statement is N_h(T)^*(I)≤(1−p)I. Its validity on the full alphabet is what permits iteration after ANY previous no-event record. Complete positivity and semigroup composition give

N_h(t)^*(I) ≤ (1−p)^floor(t/T) I,
||N_h(t)||_diamond ≤ (1−p)^floor(t/T) ≤ C exp(−c t),
C=(1−p)^(-1), c=−log(1−p)/T.

This includes arbitrary initial C/R states with dirty workspace, malformed locks, arbitrary clock coherences, monitor entanglement, outside correlations and a reference. The short constant version holds on the invariant C/R_C sector. The full constant version holds even on A and Q, without assuming clean initialization.

No good/bad structural-clock projector enters this argument. A healthy computation branch that has not reset is still counted by N_h; forward terminal progress is the missing ingredient that a bad-weight contraction cannot supply.

## 7. Joint tails

Chronological nonoverlapping length-T windows assigned arbitrary owners have joint no-reset instrument norm at most (1−p)^r for r windows, by composition of the full-state bounds.

A stronger simultaneous, spatially extensive tail is proved in `JOINT_LOCAL_LYAPUNOV_TAIL.md`. The killed-generator integral is approximated by an anchored finite-support polynomial, yielding alpha I≤Z_h≤I and K_h*Z_h≤−r Z_h. For owners separated at the resulting witness radius (not merely disjoint original resource sets), the exact local product identity gives

||N_S(t)||_diamond≤min{1,alpha^(−|S|) exp(−r|S|t)}.

This works with an interacting exterior and arbitrary entangled initial states; no independence assumption or remote-record postselection is used. Bounded-degree packing extends it to arbitrary owner sets with a fixed weakened exponent. See the companion proof for constants and the essential actual-instrument restriction on optional perturbations.

## 8. Scope

This is a regeneration-clock/reset-instrument tail, not proof that any given dirty terminal branch implements intended recovery, not a bound on data-support spread, and not a fault-tolerance threshold. No numerical small-system decay fit substitutes for the uniform operator argument. The construction assumes the explicitly priced finite-rate monitors; removing them is not justified by this proof.

## 9. Regression receipt

The supplied transactional fixture was snapshotted without altering its source. `check_reset_paths.py` exhaustively validates 58,320 full-alphabet owner paths across all 29,160 arbitrary configurations; maximum length 25 versus the conservative bound 46. It also validates 44,550 C/R short paths; maximum length 4. This checks actual clock-edge eligibility, not finite-rate quantum probabilities or data-channel factorization. The latter probability assertion rests on the operator proof above and the explicit monitor hypotheses.
