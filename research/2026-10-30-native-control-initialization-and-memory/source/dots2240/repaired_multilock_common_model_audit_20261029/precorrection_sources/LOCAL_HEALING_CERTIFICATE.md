# Arbitrary-state local healing from a two-step abort path

This is a conditional theorem for the no-epoch repaired generator described by the implementation worker. It closes the rate implication once the stated transition invariants are exhaustively/algebraically checked. It is not a claim about logical data recovery or dirty-history spread.

## Required exact generator facts

For each hub h let B_h be its local Boolean bad-clock projector, including abort phases. The supplied predicate is:

- acquisition A_i: a required prefix resource lacks exact O_h, OR an own O_h/Z_h appears outside that prefix;
- computation G_t: some required resource lacks O_h;
- verification Q_i: an own O_h/Z_h appears in the already verified prefix;
- every abort label is bad.

Q_0 is good regardless of outstanding own tags, because its verified prefix is empty.

Assume:

1. Every Hamiltonian term commutes with every B_h. Every individual reset J satisfies J(I-B_h)=(I-B_h)J(I-B_h) and [J^*J,B_h]=0, and has no selected off-diagonal clock loss block. These are OPERATOR conditions, not merely arrows between basis labels. Thus L^*(B_h)<=0 on the FULL physical Hilbert space, not merely a legal sector.
2. Every bad non-abort clock configuration has at least one enabled local test on h and one of its resource sites, giving a unique coherent transition p -> R_(p,j) with amplitude >=g_r>0. Distinct tests have distinct abort destinations, avoiding cancellation. The transition preserves data/workspace norm.
3. Every abort R has a bundled one-site reset to Q_0 with intensity kappa_r P_R tensor I_workspace, kappa_r>=kappa_min>0. Workspace outcomes must be separately resolved if needed so the summed loss is the full projector, not a rank-one coherent sum over workspace inputs.
4. Local dimensions, number of resource sites per hub, overlap degree, and local Hamiltonian/reset norms are bounded. Local losses have no off-diagonal block between a selected p and its R destination.
5. Add the explicitly priced clock-only monitoring from FINITE_RATE_PROJECTED_PATH.md or EXACT_RESET_MONITOR.md. Monitor projectors resolve clock position/ownership/abort labels, not data or syndrome/workspace. They commute with B_h.

## Bounded local healing path

Let Gamma be the COMPLETE physical sites consisting of h and its resource sites. After projecting their clock labels:

- if B_h=0, healing has already occurred and remains true;
- if h is in an abort phase, use its reset to Q_0;
- otherwise, choose any violated local test, follow p->R_(p,j), then reset R->Q_0.

There are at most TWO selected steps. No resource acquisition, wait-for recursion, rollback, legal-prefix premise, or global coloring is needed. The choice of a violated test is only a branch-dependent description of a successful event subset, not external feedback.

## Explicit finite-rate certificate

Let n be the number of monitored clock sites in Gamma. Let B bound the main Hamiltonian norms touching Gamma plus half the summed ordinary no-jump loss norm there; monitor timing dynamics is factored separately. Choose

 delta <= min{1/(16B), g_r^2/(16B^3)},
 p_0=min{g_r^2 delta^2/4, kappa_min delta/4, 1/4},
 epsilon <= min{1/(16B), p_0^2/(24B)}.

The CP-Dyson/projection estimates in FINITE_RATE_PROJECTED_PATH.md give success probability >=p_0^2/2 after replacing ideal joint measurements by three finite measurement windows. Early healing and abort-only inputs can be padded with harmless checks because B_h=0 is absorbing.

For direct one-site dephasing attempts sqrt(gamma)P_c, set

 w=exp(-n gamma epsilon)(gamma epsilon)^n/n!,
 T=2delta+3epsilon,
 c=(p_0^2/2) w^3 exp(-2n gamma delta)>0.

For literal label-resolved on-site reset monitors M_c=sqrt(kappa_m)P_c tensor |0><1| and H_mon=Omega I tensor X, use the exactly-one-event Gramian alpha(u)>0 from EXACT_RESET_MONITOR.md. A preliminary local flush removes arbitrary initial monitor entanglement. Set

 w_mon=alpha(epsilon/n)^n exp[-kappa_m(n-1)epsilon],
 T_mon=2delta+4epsilon,
 c_mon=(p_0^2/2) w_mon^4 exp(-2kappa_m n delta)>0.

Every constant is finite and independent of total graph size. All initial physical data/workspace/clock/reference states are allowed, assuming the generator facts above hold globally.

## Operator contraction, not just a basis-state statement

Let T_t^* denote the full augmented Heisenberg semigroup. Since L^*B_h<=0 and the semigroup is positive,

 0<=T_t^*B_h<=B_h.

Hence T_t^*B_h is supported entirely inside the bad subspace. The uniform healing probability for every state supported on B_h gives

 T_T^*B_h <= (1-c) B_h

(or the reset-monitor constants). This automatically handles arbitrary coherences between good and bad clock sectors. Iteration yields

 Tr[rho_t B_h] <= (1-c)^floor(t/T) Tr[rho_0 B_h].

This is an exponential bound on structural bad weight, equivalently on the probability that a B_h projective test at time t reports bad. Do not automatically identify it with a first-entry stopping time of arbitrary quantum-jump trajectories: jumps can in general leave coherent good/bad components. The explicitly selected abort-reset paths certify a definite good destination, but a general operational healing-time identification needs extra record/branch structure.

## Exact boundaries

- This conclusion depends on the global algebraic no-bad-creation property. If that property was checked only on legal basis states, the arbitrary-state theorem does not follow.
- A generic coherent sum of reset transitions can introduce off-diagonal no-jump loss even if its basis arrows look harmless. Individual jump-channel matrices must satisfy the stated operator conditions.
- The predicate B_h identifies structural clock consistency. Reaching B_h=0 need not mean data is uncorrupted or a workspace has undergone a logically correct recovery map. Those are separate dirty-history and data-fault questions.
- Physical faults that create B_h require a source/propagation analysis on top of this unperturbed healing contraction.
