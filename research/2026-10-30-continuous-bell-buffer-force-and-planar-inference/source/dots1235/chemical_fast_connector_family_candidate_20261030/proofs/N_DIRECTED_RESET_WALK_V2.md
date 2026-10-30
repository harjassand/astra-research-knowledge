# N-directed first exit from an actual fresh-clearing section
Status: V2: unreviewed probability-kernel candidate; actual continuation handled separately. This earns a candidate regeneration estimate, not yet the full globally defined N-directed stopped value.

## Setting and exact residual
Use homogeneous degree-m fast chemistry containing all pure mX_i, common qB catalyst, q>m>=2, connector0->A+B->mA+qB->0. Let h=q-m. For B>=1 write B-1=a(q-1)+v-1, 1<=v<=q-1, and define

    H(0)=0, H(B)=a(m-1)+v, r=N-H(B).

Activation is always r-neutral. Immigration is neutral except at B positive divisible by q-1, where it raises r by h. Clearing is neutral except at B>=2q-1 with B≡1 mod(q-1), where it lowers r by h. In particular clearing B=q->0 is neutral. Fast transitions preserve r exactly.

Assume the independently earned strict clearing estimate, uniformly over active compositions,

    E tau_clear <=C N^{-(m-1+epsilon)}/(B)_q,

for some epsilon>0. Set p(r)=r^{-(m-1+epsilon)}. Throughout an r-neutral excursion, N=r+H(B)>=r.

## 1. Actual fast-episode bounds and output moments
Until the next connector birth, N,B stay fixed. Hence immigration before clearing has probability <=Cp(r)B^-q; activation before clearing has probability <=C r^{-(m-2+epsilon)}B^{1-q}. Both tend to0 uniformly for B>=q.

At actual clearing, A_after=A_before-m. The elementary inequality

    (A_before)_m/(1+A_after)^m <=C_m

and the killing compensator imply

    E[(1+A_after)^-m ; clearing before a competing birth]
        <=C (B)_q E tau_clear <=Cp(r).                    (1)

This is an actual output-law bound, not a claim that A_after is typically proportional to N.

A fast episode starts after a low-phase activation at B=b+q-1, 1<=b<=q-1, and ends on reaching B<q, a downward r exit, or an immigration (the last is counted as a bad event regardless of its own r increment). Additional activations preserve B mod(q-1). With no immigration, at most q-1 clearings lead to either a downward exit or B<q; the latter terminal phase is at most b-1. The probability of a competing activation per clearing stage is o(1), so geometric restart gives a uniformly bounded expected number of stages. Consequently:

- bad immigration probability <=Cp(r);
- if the episode returns low, it goes to some phase b'<=b-1;
- its terminal A law, conditional on low return, has E(1+A)^-m<=Cp(r).

The normalization in the last assertion is legitimate: the FIRST clearing before ANY birth returns directly to b-1 and has probability1-o(1), uniformly in the incoming composition. Correlation between terminal b' and A is allowed; only the joint inverse-moment bound is used.

## 2. Finite low-phase reset-walk lemma
Consider phases0,...,q, with0 a return target and q an upward escape. At phase b in1,...,q-1, immigration raises b by1 and A by1; an activation launches the fast episode above, which either exits safely/downward, has a bad event, or resets to some phase <=b-1 with the joint inverse-moment bound (1). Immigration versus activation satisfies

    P(next jump immigration | A,b)<=C/(1+A),

uniformly in positive b. Thus the probability of ell consecutive immigrations before activation is <=C_ell(1+A)^-ell. For a fresh reset law with E(1+A)^-m<=Cp, Hölder gives

    P(ell consecutive immigrations)<=C_ell p^{min(ell,m)/m}.

Put beta=p^(1/m). Group the path into immigration runs followed by fast resets. Each reset lowers the phase by at least one. A run of length at least m has probability O(beta^m); the expected number of runs before hitting0 or q is uniformly bounded by a q-step SUBSTOCHASTIC KERNEL argument. Index transitions at fast-episode ENTRANCES, before observing the joint reset output. Each episode followed by the next activation has probability O(beta) of any intervening immigration, uniformly in its full entrance state. If q successive transitions have no immigration, launch phase decreases to absorption. Hence the q-step kernel has row mass at most q C beta<1/2, and positive kernel iteration gives O(q) expected runs. No inverse-moment or drift bound is conditioned on the observed post-reset A or phase.

If all run lengths are <m, a path of n runs escaping from starting phase b requires at least q-b+n-1 immigrations. The joint probability is bounded by C^n beta^(sum run lengths), by iterated conditional reset-kernel bounds. Summing the at most m^n possible run-length strings gives a convergent geometric series. Adding the rare length>=m runs yields

    P(upward escape before return0) <=C p^{min(q-b,m)/m}.  (2)

Bad fast immigrations contribute only Cp times the uniformly bounded expected number of runs, and fit the same estimate. Correlation of terminal reset phase and A does not invalidate the argument: use the actual joint kernel and only the fact that its phase decreases by at least one; do not condition its inverse-moment estimate on a rare particular output phase. More precisely, one composite kernel consists of a fast reset followed by a specified immigration-run length; after summing ALL admissible output phases its total mass is bounded by C_ell beta^min(ell,m), uniformly in the full incoming state. Products of these positive-kernel sup-norm bounds control run-length strings. An auxiliary height drops by exactly one at each reset and therefore dominates the actual phase, which may drop farther. Its update is determined by prior run lengths, not by conditioning on the particular reset phase. This is the intended justification for the path enumeration; a conditional-on-observed-A marginal bound would be false.

## 3. Upward versus downward exit from a fresh B=0 section
A FRESH section means an actual clearing B=q->0; the output law satisfies (1), conditionally on the scalar incoming r/history before the final clearing attempt. At B=0, immigration is compulsory and neutral, producing B=1 and increasing A, so it preserves the inverse-moment upper bound. Applying (2) with b=1 and q-1>=m bounds upward/bad escape in one section-return cycle by Cp(r).

There is also a genuine downward opportunity of size at least c r^{-(m-1)} in each cycle. From B=1 after compulsory immigration, A>=1, so activation occurs before the next immigration with probability bounded below by a positive constant. This enters B=q. During the ensuing fixed-N fast episode, pointwise

    lambda_activation >= c r^{-(m-1)} lambda_clearing,

because A/(A)_m>=c N^{-(m-1)} when clearing is enabled and N=r+m is of order r. Integrating competing hazards gives activation-before-clearing-or-immigration probability at least c r^{-(m-1)} times the clearing-first probability, which is1-o(1). This activation moves B=q to2q-1 without changing r. The next clearing is a downward r exit; additional activations preserve that residue class, and immigration intervenes with probability o(1). Hence the claimed downward lower bound holds uniformly in the incoming composition.

Neutral returns to B=0 end with another actual clearing from B=q. Conditional on that final clearing-before-birth event, its probability is1-o(1) and the fresh inverse-moment bound remains valid. Mixtures over previous attempts and input compositions preserve it. The coarse history may retain r and completed section events, but must not silently condition on the newly observed A and then claim the same moment bound pointwise.

Iterating section cycles at fixed r gives the candidate estimate

    P(first nonzero r exit is up | fresh section law)<=C r^-epsilon,
    E(time to ACTUAL exit) remains pending bad-state repair. (3)

The time to the ARTIFICIAL cycle stop (which also declares every fast immigration bad) is uniformly bounded: low-phase waiting rates are bounded below by immigration, the expected number of reset runs is bounded, and fast stages have the earned finite mean.

## 4. Exact remaining step before a global N-directed value
Equation (3) is a law-of-actual-clearing-section estimate, not a pointwise bound from every composition. An arbitrary low-B state may first move upward with probability one, as already preserved in earlier counterexamples. A globally defined stopped value must pay the initial repair and the post-exit return to a fresh B=0 section.

A downward exit itself is a clearing and has a fresh inverse-moment law. Starting a low phase b<=q-1 with that law, (2) gives upward repair probability at most Cp^(1/m); typical repair returns to0 without increasing r. An upward exit enters an active fast phase and can be repaired through actual clearing; its initial cost may include the factor r^(alpha h). These observations suggest a weighted section-return contraction for alpha h<epsilon, but that full composition-sensitive value, including repeated repair events and nonexplosion, still needs a written proof. A neutral bad immigration is not a physical r exit. Its actual continuation and weighted cost are explicitly treated in UNCAPPED_N_DIRECTED_VALUE_CANDIDATE.md using a pointwise B=q section. No uncapped global recurrence conclusion is asserted by this file alone.
