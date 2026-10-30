# Independent scoped review: nonbalanced dormant extension
30 October 2026. Reviewer `producer-workspace/review_dormant_extension`.

## Verdict
**Scoped PASS** for the local theorem in the frozen V1 manuscript, with the completing details below. Acceptance covers the stated six-reaction operational model, deficiency-one/unit-rate non-complex-balance calculation, finite-shell absorption, geometric creation budget, small dormant-return probability, incoming inverse-power profile, incoming physical-time bound, and extra inverse-power dormant-return gain. It does not cover a full connector-cycle recurrence theorem, the dormant exponential Green operator, all exponential moments, general weakly reversible recurrence, or historical novelty.

Frozen manuscript SHA256: `89f583e4513d2ab8d55b5119dd75bf593cecba8001c50c927cf0a620ec0109dc`.
Source: `recovery_chemical_boundary_20261030/NONBALANCED_DORMANT_EXTENSION_V1.md`. A copy is preserved under `frozen/`. The current theorem remains explicitly unreviewed in its original text; this separate receipt records the review without editing it.

## 1. Exact network and ordinary-theory boundary
In species order (A,C,D,B), the four translated fast complexes are

- (a0+2,0,0,q),
- (a0+1,0,1,q),
- (a0,1,1,q),
- (a0,0,2,q).

Adding zero and (1,0,0,1) gives six complexes in one strongly connected linkage class. The fast changes span two independent directions preserving A+C+D and B. Connector changes supply independent A/B directions because q>m=a0+2. Thus full rank is four and deficiency is six minus one minus four, namely one. This was independently checked by exact rational ranks for three parameter pairs, in addition to the general argument.

For unit fast rate constants, deterministic complex balance at the non-anchor C+D and 2D complexes forces c=a and d=a, respectively. The A+D balance then equates inflow a^2+cd+d^2=3a^2 with outflow 2ad=2a^2. Positive solutions are impossible. The common A/B catalyst monomial cancels and connector rates do not enter these three equations. This rules out the usual complex-balanced product-Poisson route at these rates, not every possible product-form invariant law or recurrence theorem.

The official abstract of Anderson, Cappelletti and Kim (2020) was independently read. Its displayed sufficient conditions require a binary full network and a species-multiple complex for each species. The translated network is high-molecularity and has no C-only complex, so those stated conditions do not settle it. This is a narrow source comparison, not a literature-exhaustiveness claim. No denied Wisconsin PDF route was retried.

## 2. Active shells and creation marks
Every enabled complex can be transported to 2a along at most two fast edges, retaining all spectator molecules; clearing is the third event. The 2d route is 2d→a+d→2a. Rates of enabled prescribed edges have a positive constant lower bound, while all shell propensities are O(n^2). Three-event trial success is therefore at least c n^-6. Each trial has bounded mean duration since some active rate is bounded below, and fast jumps preserve activity. The claimed C n^6 clearing-mean bound follows without assuming shell irreducibility.

Clearing and both creation reactions have the same (a)_2 factor. Their combined event marks have constant clearing probability p=k0/(k0+k1+k5). The total creation count before clearing has a geometric tail. Each creation raises d by at most two and lowers a+c by at most two; every other reaction lowers d by one or leaves it fixed. The double-step creation changes constants and the upper-exit count, not the mechanism.

## 3. Seeded probability estimate
For a<K and 1<=d<J, c>=n/2 for sufficiently large n. The positive c+d→a+d contribution is k4 c d; adverse a drift is at most C(a^2+ad). Thus the unkilled chain has Qa>=c n. Stop that chain before a reaches K or a d boundary, and use its bounded terminal a to obtain CK/n by stopped Dynkin. Adding a clearing hazard afterward shortens the interval; assigning zero cemetery a before applying the positive drift would be invalid.

Only a+d→2a at d=1 enters d=0. Its low-strip rate is at most C K, so the sharper low-strip loss estimate CK^2/n is valid. Clearing has rate O(K^2), giving CK^3/n.

In the high strip a>=K/2,d<J, clearing has rate at least cK^2. Its compensator bounds the expected integral of (a)_2, hence the integral of ad by CJ/K. A drop of K/2 in a requires either many creation losses, with geometric-tail probability, or an a+d→c+d loss. Even bounding the latter by the expected total number CJ/K is sufficient. Reaction 6 is favorable and cannot introduce an additional negative-a event.

Conditional stage restart sums are finite for large n. Reaching d>=J from d=1 requires at least (J-1)/2 creations and has exponentially small mass. Any later return from that exceptional upper exit is bounded by its entire mass; no favorable continuation is assumed. Every path from arbitrary d>=1 to zero must first visit d=1 because all negative d jumps are exactly minus one. This proves the uniform C n^-1/8 return-probability claim. It does not prove that the complete connector is recurrent.

## 4. Paired profiles and the newly active corner
The reviewed triangle's three linear-in-d channels are unchanged. The paired-profile proof can be checked directly: choose epsilon=1-eta positive and small enough that the reverse-creation negative term in Q h_s dominates the epsilon-weighted adverse conversion term. Then Q_lin h_s<=-c d h_s whenever a+c>=1. For c large relative to 1+A, Q_lin f_s is itself strictly negative of order dc f_s/(1+A); on the complementary region f_s and h_s are comparable. A sufficiently large C2/C1 gives the stated common strict margins.

Reaction 6 increases both profile arguments by one. Finite-difference bounds for z^-s yield a negative contribution at least c_s(d)_2 F_s/(1+A+eta c). In particular, at a=c=0,d>=2 it supplies the missing strictly negative term. The lone d=1,a=c=0 state is inactive and is properly excluded.

The two creation jumps decrease the profile arguments by one or two but require a>=2. Their total positive drift is O(a F_s), uniformly in the shell. Clearing's actual physical terminal A is a-2, and its inverse-power reward is at most a fixed multiple of f_s(A). Scaling C1,C2 together makes F_s minus that reward at least F_s/2. For large a the resulting quadratic negative term absorbs O(aF_s). For bounded a and large n, the C-rich, D-rich with a+c>=1, and a=c=0 cases have the respective strict margins asserted in V1.

Small finite shells should be covered by finite-shell absorption and a finite maximum of the required value-function/profile ratios. Merely multiplying a Lyapunov function whose drift has the wrong sign would not fix that sign. The manuscript's finite-shell statement is accepted in this value-function sense; it is not an assertion that the same pointwise formula becomes superharmonic on every small shell by scaling alone.

## 5. Stopped kernel, return gain and physical time
At d=0 entry the A argument increases by one. Terminal profile rewards are bounded by the paired-profile boundary value. The same is true at either connector birth, which increases A; these are stopping events, not unpriced internal jumps. Stopped Dynkin therefore proves the joint profile bound. It is not conditioned on a selected output.

Applying the bound at exponent 2s and Cauchy–Schwarz with the small dormant-return probability gives C n^-1/16 times the incoming f_s. Both true seed outputs lower A by at most two and have bounded inverse-profile ratios because a>=2 and a0>=2. Their kernel is not small, but its product with the positive-to-dormant kernel is small for large n. Truncate the number of cycles before taking positive monotone limits. The finite-shell bounds established independently justify the remaining finitely many n.

Until the first connector event, B is constant and at least q. The fast clock multiplies every operational fast and clearing rate by (A)_a0(B)_q. For s=m, large-a negative drift times this factor is bounded below by c(A)_m F_m(B)_q, hence by c'(B)_q. On bounded-a large shells the strict paired/reaction6 margin likewise pays a fixed running-time cost. The dormant first-event waiting time has rate at least c(A)_m(B)_q. These facts and the same two-kernel iteration prove the incoming physical-time inequality. The condition B>=q cannot be dropped or replaced by division through a vanishing catalyst factor.

For the extra inverse power, use the paired profile at exponent s+1 with zero clearing reward. The actual dormant-entry forcing is k2 a 1_{d=1} f_s(A+1). At large a it is O(a^2 f_(s+1)), so a fixed scaling of the profile's negative clearing margin pays it. On bounded-a large shells the strict negative margins pay this bounded forcing. Killing at first dormant entry replaces the ordinary boundary F_(s+1) by the stated reward; dropping the negative subtraction of that ordinary boundary only weakens the desired inequality. This proves the extra-power bound without presuming the older unreviewed triangle gain.

## 6. Evidence and exclusions
Source finite-shell tests were replayed unchanged for n=8,16,32,64. An independently written generator constructed transitions from source/product complexes rather than copying the source delta list and tested n=2,5,12,24,40 (1,216 positive-d states total). It verified every dormant entrance is reaction 2 at d=1 and reproduced the expected finite profiles/time values. Maximum independent linear-system residual was 2.85e-14. The n=2 return probability can equal one, consistent with a large-constant asymptotic bound; it is not uniform smallness on all shells. These tests are diagnostics, not proof of asymptotic bounds or full recurrence.

No complete exponential-residual section drift, dormant Green norm, global Lyapunov function or full-network positive recurrence is accepted here. Local constants greater than one cannot replace the missing coefficient-one global margin. Neither the abstract comparison nor the numerical solver demonstrates novelty or a chemical device.

## Reference
Anderson, D. F., Cappelletti, D., & Kim, J. (2020). Stochastically modeled weakly reversible reaction networks with a single linkage class. Journal of Applied Probability, 57(3), 792–810. https://doi.org/10.1017/jpr.2020.28 . Official abstract inspected 30 October 2026: https://www.cambridge.org/core/journals/journal-of-applied-probability/article/abs/stochastically-modeled-weakly-reversible-reaction-networks-with-a-single-linkage-class/5E9F7DAE999525F8D4A3392F80B3F0C9 .
