# Growing caps and subexponential tilts replace summable fiber absorption

Status: NEW PERSONALLY DERIVED CANDIDATE, not reviewed. This is a separate v2 mechanism; it does NOT alter the frozen global-proof bundle currently under separate review.

## Purpose
The v1 complementary trace used the strong absorption estimate E tau_clear<=C N^(-9/4)/(B)_4 to sum an infinite composition tail. That special exponent is unnecessary for global gluing. An explicitly growing cap, with its actual incoming feedback controlled, allows the much cruder polynomial bound C N^12/(B)_4 instead. No truncated domain is assumed closed.

## 1. Earn the crude bound without mixing or a special profile
On the conservative N-shell, N>=3, remove the common (B)_4 factor. Every state reaches clearing in at most three A-increasing fast jumps followed by clearing. Each required enabled rate is bounded below by a positive constant; all rates are at most C N^3. Thus the prescribed path has probability at least c N^(-12). Total holding rates are bounded below, so four-jump blocks have bounded mean duration. Repeated attempts yield

    sup_A E tau_clear <= C N^12/(B)_4.

This is the old bounded-path estimate, not the sharper boundary-layer theorem.

## 2. A growing domain with fully accounted exits
Retain s=B−g_N from the complementary trace. Fix

    p=1/8,   delta=1/16,   L(s)=floor(s^p),
    D={s>s0, N<=L(s)}.

Choose s0 large enough that L(s0)>=12. Define the stopped process to exit D both at the residual threshold and at the composition cap. Cap exit is an actual stopping event, not a deletion of its physical transitions.

At fixed s during a neutral tail excursion, B=s+g_N>=s. Competing births have rate at most1+NB. The crude absorption estimate gives

    P(birth before next clearing) <= C s^(-3) N^13,
    E(time stopped at birth/clearing) <= C s^(-4) N^12.

Sum over the decreasing N→N−3 ladder, only up to N<=L(s):

    P(any birth before the finite head) <= C s^(-3)L(s)^14
                                       <= C s^(-5/4),
    E(stopped tail time) <= C s^(-4)L(s)^13
                         <= C s^(-19/8).

A neutral birth restarts the tail if still inside D; otherwise it is a cap exit. Its restart probability is O(s^(-5/4)), so geometric closure is uniform. The previously certified fixed N<=8 head still has up-exit probability O(1/s) and neutral-tail probability O(s^(-3)). Thus the actual first nonzero residual exit OR cap exit satisfies

    P(up and still alive) <= C/s,
    E(excursion time) <= C s^12.

Cap exits have terminal value zero in the value construction below; they cannot worsen contraction.

## 3. A finite stopped-cost value with a subexponential tilt
Put

    phi(s)=exp(s^delta) Gamma(s+1)^alpha,

where the same bulk-admissible 0<alpha<1/2 is used. Since delta<1, fixed-shift exponential ratios tend to1, and the trace still contracts:

    E[phi(s_next) 1_alive]/phi(s)
       <= C s^(alpha−1)+C s^(−alpha) ->0.

As in the v1 value lemma, define

    W_cap(x)=E_x integral_0^T phi(s_t)dt   inside D,
    W_cap=0                              outside D.

Here T is the actual exit from D. The earned trace bounds prove finiteness and stopped nonexplosion, with

    W_cap<=C(1+s)^12 phi(s),
    L W_cap=−phi(s) inside D.

No derivative of L(s), no frozen phase, and no invariant cap is used.

## 4. The actual outer-cap forcing is exponentially dominated
For the hard network, a state outside the cap can jump into it only by clearing, apart from finitely many threshold states. Indeed fast moves preserve N,s; immigration increases N and does not increase s; activation raises N by2 and raises s by at most1, while L(s+1)−L(s)<=1. Clearing lowers N by3 and leaves s unchanged.

Therefore every large-s incoming boundary state lies in the collar

    L(s)<N<=L(s)+3.

Its positive W_cap generator contribution is at most poly(s) phi(s). This follows from the polynomial clearing rate and the uniform value bound at its target.

On this collar, N is of order s^p and B=s+g_N is of order s. The already earned F is strictly negative for every composition there: N→infinity and B→infinity, so either the extreme-composition estimate or the balanced bulk estimate applies. Also r=N−h_B is very negative, so W_r and all its nearby target values are zero.

Most importantly,

    log[phi(s)/F]
       <= s^delta −alpha log(B!/s!)
       <= s^delta −c alpha N log s
       <= −c' s^p log s

for large s, because g_N=B−s is a positive linear function of N up to a bounded error and delta<p. Thus the ABSOLUTE outer-cap forcing is smaller than the earned negative F margin by more than any polynomial factor. The discontinuous/growing cutoff is not hidden: its entire incoming jump term is included and dominated.

At s<=s0, any jump into D has bounded s and bounded N<=L(s0+1), so the threshold leakage has finite support.

## 5. Close the same remaining cylinder
For fixed bounded N and B→infinity, eventually N<=L(s), and

    phi(B−g_N)/F >= exp(s^delta) B^(-C).

This dominates every polynomial multiple of F. Hence the negative W_cap drift closes the bounded-N/large-B cylinder just as W_s did in v1. Elsewhere W_cap is nonpositive in drift except at the explicitly absorbed cap collar.

Therefore the SAME global conclusion for the hard network follows from

    V_v2=F+W_r+W_cap,

using only the crude polynomial fiber absorption bound, not N^(-9/4). This remains a candidate until the cap, value, and interface arguments are reviewed.

## 6. General certificate rule exposed by the construction
Suppose a killed conservative fiber of size N has mean absorption at most C N^ell z^(-q), competing births have rate at most C z^a N^b, q>a, and each killing decreases N by a fixed positive amount while preserving a residual s with z>=s. On a cap N<=s^p,

    tail birth risk <= C s^(-(q-a)+p(ell+b+1)).

Choose p>0 so u=(q-a)−p(ell+b+1)>0, and choose the factorial exponent below the earned first-up exponent. A subexponential tilt exp(s^delta), 0<delta<p, still dominates every fixed polynomial on bounded-N cylinders while allowing the factorial loss at the cap to absorb all outer forcing.

Thus ANY earned polynomial absorption estimate can suffice when there is a positive resource-order gap. The former summability condition on the entire infinite fiber is not fundamental. This is not a claim that arbitrary weakly reversible networks satisfy the required resource gap, finite-head exit bias, or outer-collar F inequality. Those remain explicit structural obligations, not supplied global barriers.
