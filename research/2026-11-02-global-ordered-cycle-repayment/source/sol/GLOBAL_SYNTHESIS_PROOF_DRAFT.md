# Global synthesis proof under construction

Earlier working derivation. The final complete argument and claim scope are in GLOBAL_ORDERED_CYCLE_THEOREM.md and REPORT.md; no independent review is claimed.

This is an ordinary working scientific proof. Completed source directories are unchanged. All new conclusions require the arguments here; no independent audit is claimed.

## Raw family and facts

Let k>=3. Set y0=0, y1=(1,1,0), yj=(j,j−1,j−1) for 2<=j<=k. Channel i is yi->yi+1 for i<k, with constant kappa_i>0; channel k is yk->0, constant kappa_k>0. Growth increments are u0=(1,1,0), u1=(1,0,1), and ui=(1,1,1) for i>=2. The last decrement is v=(k,k−1,k−1). Let M=A+B+C and W=exp(theta M).

Every state communicates with zero. Actual deletion words are: remove B using [0,1,1,3,4,...,k] (the symbols 3..k−1 are omitted if k=3); remove C using [0,0,1,3,4,...,k]; remove A using [0,1], then channel 2 repeated 2k−3 times, then channel k twice. The first two require respectively B>=1 and C>=1, the third A>=1. They decrement ONLY that coordinate. All intermediate sources are enabled under those conditions. Weak reversibility reverses each word. Thus the actual class is N^3, rather than a ray through different classes.

Complex balance holds exactly when kappa_j follows the geometric continuation forced by j=2,3: kappa_j=kappa_3^(j−2)/kappa_2^(j−3) for j>=4. A positive balance point, when these relations hold, is

    a=kappa_0 kappa_3/kappa_2^2,
    b=kappa_2^2/(kappa_1 kappa_3),
    c=kappa_1 kappa_2/(kappa_0 kappa_3).

This makes k=3 an ordinary deficiency-zero baseline, while k>=4 includes arbitrary deficiency and generic non-CB rates. The terminal-gap cone fails for every k: take divergent coordinates I={B,C}, outside coordinate A and weight w_B=w_C=1/2. Allowed s_A<=c_A forces the source index not to exceed the terminal index, so w.(s−c)<=0. I is admissible since the full stoichiometric span is R^3. No claim of general weak-reversibility completeness is made.

## 1. Universal actual normalizer off the slow section

Let Z={A=0} union {B=C=0}. From any off-Z state define an episode stopping at the first channel-k degradation or after k genuine jumps, whichever is earlier. It has at most k jumps, increases M by at most 3k on any branch, and includes all actual competitors.

CLAIM TO COMPLETE IN FULL DETAIL: along ANY escaping off-Z sequence, with probability tending to one this episode ends with M reduced by at least one. Then for any theta>0, outside a finite head

    E W(X_sigma) <=rho W(x),     rho<1.                         (N)

The finite case proof is as follows.

* If A->infinity, nested source counts give q_i/q_j<=C/A for every i<j at a state whose largest enabled source is j, throughout a bounded prefix. With probability tending to one all selected sources are maximal. A maximal growth raises the largest enabled index by at least one, so indices are visited at most once before degradation. If ALL indices 0,...,k occur, then the initial state must satisfy (A=0 or B=0) and (A=0 or C=0), exactly Z. Off Z at least one growth is omitted, so the total growth is componentwise below v and M strictly falls. At most k jumps occur.
* If A is bounded, extract A=a>=1. If B,C both diverge, all lower/maximal source ratios tend to zero and the preceding argument applies.
* If B->infinity and C is bounded, with probability tending to one channel 0 is avoided until degradation: channel 1 has rate kappa_1 AB, while q_0 is constant. Every other growth raises BOTH A and C by one. Within at most k−1 such growths the terminal source is present; once present its extra B degree makes degradation beat all growth with probability tending to one. Hence at most k−1 growths occur, each adding at most three particles, and the terminal removes 3k−2: M falls by at least one.
* If C->infinity and B is bounded, allow at most one initial growth to reach A>=2,B>=1. This is always possible and every available initial channel (0 or 1) does it; if B=0 only 0 is enabled. Thereafter physical ABC growth beats channels 0,1 by a C factor. Within at most k−2 more growths the terminal source is present, and its extra C degree makes degradation overwhelmingly likely. Again at most k−1 growths occur and M falls by at least one.

All rate statements concern the actual bounded prefix, where the divergent coordinates change by only O(k^2). The countable-sequence extraction proves a single finite exceptional head rather than supplying an unproved uniform mixing parameter. This normalizer is global over the complement, including high-A and low-B/C landings.

For F_r=(1+q)exp(rM), one bounded episode has expected physical reward at most k(1+1/kappa_0)exp(r(M+3k)). Choose theta>r. After enlarging the finite head this reward is arbitrarily small relative to W. Given any finite profile f on Z with V_Z/W=1+O(1/M), (N) therefore constructs the actual Dirichlet normalizer in COMMON_CONTRACT.md with

    0<=V_off<=W.

This must be written as a nonnegative value-iteration/supermartingale argument with boundary V_Z, not as a supplied hitting law. Its first-holding reward is at least exp(rM), so it is normlike. The q reward gives finite expected genuine jump count; the 1 reward gives finite physical time. No explosion may be assumed in this construction.

## 2. Planned plane closure, using that same V_off

Choose a fixed cutoff B_*=C_* large enough for an interior A-return excursion. Set V_Z(0,b,c)=exp(theta(b+c))[1+f_b/(b+c+1)], where f_b decreases to zero at B_*.

Low B, large C: first fire 0. At A=1 both 0 and 1 are allowed. The 0 branch then follows maximal sources 2,...,k and returns (0,b+1,c−1); the 1 branch follows the same later sources and returns (0,b,c). Their actual first choice has p_b=kappa_0/[kappa_0+kappa_1(b+1)]. At phases j>=2, every unexpected source costs O(1/C), by the exact nested factorial ratio. Abort at its actual off-Z landing and receive V_off<=W. The finite decreasing f must be chosen so p_b(f_b−f_(b+1))/(b+c+1) pays this entire O(1/C) output budget. Constants can be acquired from finite raw ratios. No neighbor-profile law is a premise.

Low C, large B: follow 0 then 1. At A=2 allow either 1 or 2, then maximal sources 3,...,k. The first alternative removes one B, the second returns the same B,C. For finitely many c<C_* the negative alternative has a fixed positive probability. All other branches cost O(1/B), aborting at V_off. Both good endpoints have f=0 for large B.

Interior: before an upward step out of A=k, exactly k growths precede the degradation. The first two growths have nonanchor size one; later ones have size at most two. Thus every no-overrun A=0 return has Delta(B+C)<=0; equality occurs only for the ordinary or B-increasing/C-decreasing branch. The B-deletion word has probability >=d/(C+1). An overrun at A=k has probability <=C/(BC). Stop at A=0 or first B<K or C<K, retaining all unbounded A excursions. For a>=k,B,C>=K,

    q_growth/q_degradation
      <= [sum_(i<k) kappa_i/kappa_k]
         /[(a−k+1)(B−k+2)(C−k+2)].

After an overrun start A=k+1. Let U be high-A upward steps, D degradations, L low-A upward steps. L<=(k−1)D and nonnegative terminal A imply D<=k+1+U; hence T<=(k+1)U+k(k+1). This acquires the ENTIRE exponential jump and output tail, including all real low-B/C exits. V_off<=W and V_Z<=2W outside a finite head fit its output contract. On no-overrun returns a decrease of B+C absorbs f/M for large M; zero radial change has nondecreasing B and hence nonincreasing f. There is no circular choice of cutoff and profile: the factor 2 is fixed by enlarging the head AFTER f is acquired.

## 3. Planned axis repayment, with all aborts received globally

Start (a,0,0), a large. Follow maximal sources. Permit one first source mismatch whose index gap is exactly one, then follow the maximal-source normalization. The exact finite classifications are:

* at phase 1, channel 0 repeats AB: maximal completion returns the same axis point;
* at phase 2, channel 1 repeats AC: maximal completion returns the same axis point;
* at phases 3,...,k−1, the preceding channel has the SAME ABC physical increment, so completion is unchanged;
* at phase k, channel k−1 causes an ABC overrun: maximal completion returns (a−1,0,0).

Each completion uses at most 2k+2 jumps and bounded count overshoot. A first gap >=2 has probability O(a^−2). Any second mismatch after a gap-one first mismatch also has total probability O(a^−2). Abort either at its actual off-Z state and receive V_off<=W. All prefixes have A>=a−O(k^2), so the nested rate ratios are uniform; no protected-region exit is omitted. The negative overrun has probability >=d/a, while all other good paths return the same axis value. Thus the full output drift is <=−d_theta W/a+O(W/a^2), paying physical F_r for theta>r.

## 4. Closure still to be fully checked

With the preceding constructions completed against this SAME function, every large section state has a finite actual episode (plus the earned normalizer on an abort) whose output and F_r reward are strictly below its V_Z. Repeated section episodes hit a finite head with finite accumulated physical time, activity and exponential count reward. A finite trace closes a genuine return cycle. This would prove nonexplosion, positive recurrence and all stationary exponential total-count moments for the whole C_k family, including non-CB k>=4, while leaving general weak reversibility open.

No exponential RETURN-TIME moment is presumed. On large translated zero-cells the normal cycle has first-mismatch probability tending to zero; the degree-seven Poisson calibration already rules out a uniform exponential-return contract. That constraint must be proved explicitly in the correction/calibration file.
