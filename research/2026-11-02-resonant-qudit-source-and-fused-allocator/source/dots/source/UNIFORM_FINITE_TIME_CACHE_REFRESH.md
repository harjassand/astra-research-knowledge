# Uniform finite-time cache refresh: CP/operator admission

Reconciled proof, 2026-11-01 17:36–17:40 UTC. Uses the proved two-body stage-completion bound, not independent quantum clocks. Parent supplied the last-window strategy. This derivation avoids needing a pair-activity factorization.

## 1. Explicit physical/instrument assumptions

For target check s and its at most Delta overlapping neighbors:
1. Each finite apparatus has a binary active label, conserved by its coherent stage Hamiltonians. A start pump can act only while idle, with rate r and a TP preparation map. Completion/readout is the only active->idle exit. All phase states are legitimate apparatus states; arbitrary initial partial phases are allowed.
2. Every active cycle, from ANY initial active stage and arbitrary joint quantum state/history, has survival bound
   P(active cycle not completed by t | past) <= S(t),
   where S is nonincreasing, bounded by 1, has an exponential tail, and tau=integral_0^infinity S(t)dt<infinity. Use a common envelope for freshly started and initially partial cycles. TWO_BODY_STAGE_COMPLETION_OBSERVABILITY.md supplies such an envelope for finitely many driven stages, once actual preparation/readout response stages are included.
3. Source evolution preserves every dressed true stabilizer. Cache s changes only on its completed readout, not during intermediate readout circuitry. A fully prepared, collision-free cycle has a correct QND cache overwrite as a CP-instrument identity. Finite preparation impurity has a convex bad-preparation branch of probability <=p; optional stochastic readout error may be included in p. No arbitrary coherent detector fault is silently replaced by p.
4. Start pumps are local channels with bounded attempt intensity r. Their Poisson attempt representations are independent. The quantum states, completion times and successful births need NOT be independent.

The claim below is for this ideal source plus the stated finite impurity. Other local physical noise remains separately priced.

## 2. Why classical activity histories are legitimate

The target observable e_s=(I-Z_cache,s Sbar_s)/2 is diagonal in apparatus active labels and in the classical cache. Hamiltonians commute with active labels; each jump maps a specified active-source block to a specified active-destination block. Hence the adjoint evolution/instrument preserves the block-diagonal observable algebra. Initial coherences BETWEEN active blocks do not affect these counting probabilities or the expectation of e_s. Coherence WITHIN a ground/excited stage is retained and was included in the completion theorem.

Thus, for this analysis only, dephase initial active labels and unravel their jumps without changing the quantity being bounded. An idle pump of rate r is represented by an independent rate-r Poisson ATTEMPT stream; an attempt starts a cycle iff idle. Null attempts while active are ignored. This is a mathematical uniformization of block populations, not a physical reliable controller. It does not assert an independent classical law for stage completion.

All conditional estimates below condition on PAST instruments/stopping times. No arbitrary postselection on future neighboring quantum measurement outcomes is used.

## 3. Uniform duty bound from survival and bounded births

Let A_q(t) indicate q active. An initially active cycle contributes at most S(t). Each subsequent birth has predictable intensity <=r and, conditional on that birth and all past history, residual survival bounded by S. Therefore
 E[A_q(t)] <= S(t)+r integral_0^t S(u)du <=S(t)+r tau.
This holds uniformly over the initial joint quantum state. No pair factorization is invoked.

## 4. Bad reports in a last window, including earlier-born cycles

Consider the observation window [B,B+L]. Conservatively call a target cycle bad if its active interval overlaps any neighbor's active interval, or its preparation/readout takes a bad impurity branch.

First, a cycle born before B may finish and overwrite the cache inside the window. All such cases are covered by
 P(A_s(B)=1)<=S(B)+r tau.
This explicitly prevents the common mistake of counting only cycles born during the window.

For a target cycle born inside the window, each collision is witnessed by one of:
(a) target birth while a neighbor is already active;
(b) a neighbor birth while the target is active.
Compensators, the bounded attempt intensity, and the duty bound give the expected number of such collision incidences at most
 2 Delta r integral_B^(B+L)[S(t)+r tau]dt
 <=2 Delta r integral_B^infinity S(t)dt+2 Delta r² tau L.
A bad target cycle can produce at most one readout; counting incidences overcounts, which is safe. Multiple collisions and correlated completion times do not invalidate this bound.

The expected number of bad impurity births inside the window is <=p r L. If p includes independent readout error, count readouts of newly born cycles; there are at most their births, while the single pre-window cycle is already covered above.

Thus
 P(any bad target report in [B,B+L])
 <=S(B)+r tau+2 Delta r integral_B^infinity S(t)dt
   +(2 Delta r² tau+p r)L.                                      (1)

## 5. A uniform conditional clean-report word

Choose F such that S(F)<=1/[8(Delta+1)], and assume
 (Delta+1)rF<=1/8,   p<=1/4.
Every block of length W=3F has a conditional probability at least q=rF/8 of containing a clean target report, regardless of the quantum state and active stages at block start.

Proof:
* First F: require no start attempts in the closed neighborhood and completion of all initially active cycles. Union bounds give failure <=(Delta+1)rF+(Delta+1)S(F)<=1/4, so this flush succeeds with probability >=3/4. It flushes arbitrary initially wrong/partial probes without claiming those flush reports are correct.
* Next F: from all idle, the probability that the first neighborhood attempt is the target's and occurs within F is [1-exp(-(Delta+1)rF)]/(Delta+1)>=rF/2.
* At that target birth (a stopping time), take the good-preparation branch, probability >=3/4. Within the next F, completion fails with probability <=S(F), and a neighbor birth occurs with probability <=Delta rF. Their union has probability <=1/4. Thus completion without collision has probability >=3/4 conditional on the good preparation and past.
The product is at least 27rF/128, so q=rF/8 is conservative. All events finish by 3F. For separate readout error, include its good branch in p or lower q by its actual factor.

A clean report need not remain the last report in its block. We do not pretend it does: equation (1) separately accounts for ALL subsequent bad reports.

Iterating the conditional lower bound gives
 P(no clean report in [B,B+L]) <=(1-q)^floor(L/(3F))
 <=exp[-(rF/8)floor(L/(3F))].                                  (2)

## 6. Upgrade to the required Heisenberg operator inequality

If the last window contains a clean report and contains no bad report, then that clean report sets e_s=0 as a CP-instrument identity. All subsequent source dynamics either preserves e_s or performs another correct overwrite. Hence the contribution of this collection of trajectory instruments to final mismatch is zero, for EVERY initial density operator, not merely for a fixed syndrome eigenstate.

Every remaining trajectory contribution is bounded by its probability because 0<=e_s<=I. Combining (1) and (2), for T=B+L,
 Tr[rho exp(T L*)e_s] <= delta(B,L)
for all initial joint rho, where
 delta(B,L)=exp[-(rF/8)floor(L/(3F))]
            +S(B)+r tau+2 Delta r integral_B^infinity S(t)dt
            +(2 Delta r² tau+p r)L.
Therefore the exact desired CP/operator admission is
                 exp(T L*) e_s <= delta(B,L) I.                (3)

This is uniform in total memory size. It prices reports that overwrite earlier good ones and reports from pre-window bad cycles. It uses no independent quantum-state assumption or global-in-time approximation.

## 7. Small-error regime and boundaries

For fixed bounded Delta and fixed local stage hardware, let z=(Delta+1)r tau+p. Choose B large enough that S(B) and its tail integral are suitably small, and choose L of order r^-1 log(1/z), with a sufficiently large fixed constant (the bound above allows approximately 24, plus a block-rounding margin). Then
 delta=O(z log(1/z))+vanishing initial-tail terms,
so delta->0 as r tau,p->0. The flushing restriction rF(Delta+1)<=1/8 eventually holds. T is finite and size independent, although it grows as the desired error shrinks.

The bound may be conservative and does not assert practical constants. A source with a non-TP reset, unbounded detector latency, intermediate cache writes, or a noncommuting omitted data bath does not satisfy these hypotheses automatically. Nor does (3) itself prove a finite-patch generator closure: it is the uniform refresh premise the parent's separate local corrector construction can consume.

## 8. Explicit apparatus discharges the response/cache premises (17:49 UTC)

EXPLICIT_TWO_BODY_QUDIT_SOURCE.md now supplies an actual 8w+6-level apparatus generator satisfying the source assumptions: onsite readout jumps have total hazard gamma Pi_final, keep the cache unchanged until the completed overwrite, and preserve its classical block algebra. Its explicit active survival envelope is S(t)=min(1,C exp(-theta t)), with C=M_stage^w gamma/(gamma-theta) and tau<=(log C+1)/theta. Thus no unspecified finite detector-response premise remains for THAT stated GKSL architecture. The distinct physical requirement of engineering those onsite reservoirs—including collective which-b-indistinguishable decay—and pricing their perturbations remains explicit.


## 9. Independent-audit asymptotic correction (17:52 UTC)

Section 7 now uses z=(Delta+1)r tau+p rather than the earlier z=Delta r tau+p. The +1 retains the pre-window r tau term for an isolated check (Delta=0), including perfect preparation p=0. The core displayed finite-time bound and operator inequality (3) are unchanged. This records the superseded shorthand rather than implying the original asymptotic parameter covered that boundary case.
