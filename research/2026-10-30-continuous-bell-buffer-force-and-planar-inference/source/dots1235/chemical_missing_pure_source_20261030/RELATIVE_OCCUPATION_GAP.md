# Beyond pure-source coverage: an actual relative occupation gap
Status: NEW PERSONAL DERIVATION, unreviewed, separate from the frozen family theorem. No new global recurrence conclusion is asserted.

## Why the frozen theorem does not automatically extend
Take composition A,C, N=A+C, and a strongly connected fast cubic graph on A+2C,2A+C,3A, with positive rates and common qB catalyst. The graph omits3C. At A=0 the entire fast subsystem and clearing are disabled, for arbitrarily large N. Thus a uniform fast-clearing theorem over every composition is false. Even from active A=1, startup is autocatalytic and its natural time is logarithmic over N^2, rather than a strict power faster than N^-2. This is not a constant-adjustment issue.

Nevertheless the full connector's immigration physically seeds A. The potentially useful quantity is the RELATIVE occupation gap, not an assumed fast equilibrium.

## Concrete killed fast chain
For clarity use the bidirectional chain

    A+2C <-> 2A+C <-> 3A,

with arbitrary fixed positive constants. Removing the common (B)_q factor, A is a birth-death chain on {1,...,N}, with

    b_a=k_1 a(C)_2+k_2(a)_2 C,
    d_a=l_1(a)_2 C+l_2(a)_3,

and clearing kill k_D(a)_3. The active class never reaches0 through fast moves. Define

    T(a)=E_a tau,        U(a)=E_a integral_0^tau A_t dt.

Claim: for all large N and every active starting a,

    T(a)<=C (log N)/N^2,
    T(a)<=C (log N)/N^(1/3) * U(a).                       (1)

The same ratio holds when immigration and activation are added as competing killing events, with B>=q fixed and the common catalyst factor restored. These are actual killed-path estimates.

## 1. Logarithmic drift earns the mean
For a<=epsilon N, b_a>=c a N^2 and d_a<=C a^2 N. Since log(1+1/a)>=c/a and |log(1-1/a)|<=C/a for a>=2 (d_1=0), choose epsilon small to obtain

    L_fast log a >=cN^2.

Globally |L_fast log a|<=CN^2, using total rates<=CaN^2 and the O(1/a) logarithmic jump bound. Let W(a)=2 log(N+1)-log a. It is positive and O(log N). On the low-a region the killed generator gives KW<=-cN^2. On a>=epsilon N the clearing rate is >=cN^3 and dominates the O(N^2) possible positive fast drift. Thus KW<=-c'N^2 everywhere on the active class. Finite-state killed Dynkin proves the first bound in (1), without stationarity or mixing.

## 2. Reach a mesoscopic A level before killing
Set K=floor(N^(1/3)). The same log drift before the fast hitting time sigma_K gives

    sup_(a<=K) E_a sigma_K <= C log N/N^2.

Before sigma_K, clearing rate is at most CK^3, so the probability of clearing before reaching K is at most C K^3 log N/N^2=O(log N/N). Hence every a<=K reaches K before clearing with probability at least1/2 for large N.

Starting at K, stop if A leaves [K/2,2K]. During a time interval c/N^2, the expected number of fast jumps before that stop is <=C c K. Choose c small so Markov's inequality makes the probability of enough jumps to leave the interval at most1/4. Clearing during this interval has probability <=C K^3 c/N^2=o(1). Therefore with probability at least1/2, A remains >=K/2 and alive for c/N^2, giving

    U(K)>=c' K/N^2.

Strong Markov at sigma_K yields the same lower bound for every a<=K. Combining it with the uniform T upper bound gives T(a)/U(a)<=C log N/K on that range.

For a>K, stop at clearing or the first hit of A<=K. Before that time A>=K, so U_pre>=K T_pre. The birth-death jump hits exactly K; applying the already proved bound to the remaining path gives

    T(a)<=max(1/K,C log N/K) U(a).

Thus (1) holds uniformly over all active starting compositions, not merely A=1.

## 3. Actual competing events and catalyst
With factor (B)_q, all fast times scale down by it. Add killing at rates k_I and k_T A B for immigration and activation. The mean/log-drift upper bound only improves. Before reaching K, the added birth hazard is bounded by C(1+KB), and its integrated expectation is at most

    C(1+KB) log N/[N^2(B)_q]=o(1)

uniformly over B>=q. The mesoscopic dwell argument has the same small additional hazard. Therefore the relative occupation proof remains valid for the process stopped at the FIRST clearing or competing birth.

Writing T_*(a),U_*(a) for those stopped occupations,

    P(immigration first)=k_I T_*(a),
    P(activation first)=k_T B U_*(a),

so their ratio is at most C log N/[B N^(1/3)]. Also the clearing-output inverse cubic moment is bounded by C(B)_q T_*(a). This is a relative actual-event comparison; no averaged activation rate is substituted.

## Possible consequence requiring a separate proof
At the N-directed section B=q, the frozen theorem used an absolute reset bound p=o(N^-2) and a crude activation probability lower bound cN^-2. Here only p_0=O(log N/N^2) is available, but the relative T_*/U_* gap is stronger than that crude comparison.

A refined low-phase walk can keep the FIRST reset law separate from later worst-case resets. Its escape bound should have terms

    sum_(ell=1)^3 [T_*(a)]^(ell/3) p_0^(1-ell/3).

Since U_*(a)>=cN^-2 by pointwise activation/clearing hazard comparison, and T_*(a)<=C N^-1/3 log N U_*(a), each term divided by U_*(a) is at most C N^-1/9 log N. This suggests a replacement upward/downward power gap even without pure3C. The refined reset-walk estimate, initial inactive seeding, and full global feedback have NOT been proved here. They remain the exact next obligations; this file does not enlarge the frozen theorem.

## Refinement: the first-reset walk bound can be proved from the existing lemma
Let t be the first clearing law's inverse m-th moment, and p_0 the worst-case moment for later resets. Start at B0, take its compulsory immigration, and inspect the FIRST positive-phase immigration run from b=1. A zero-length run activates directly into the section B=q and is safe. A run of length at least m has probability O(t). For 1<=ell<m, its probability is O(t^(ell/m)); activation then launches from b=ell+1. A bad fast immigration has probability O(p_0), and a good reset lands at phase <=ell, whose subsequent escape is bounded by the already proved phase-dependent reset lemma:

    O(p_0^(min(q-ell,m)/m))
       <= O(p_0^((m+1-ell)/m)),  q>=m+1.

Thus actual upward/bad escape is bounded by

    C t + C sum_(ell=1)^(m-1) t^(ell/m) p_0^((m+1-ell)/m). (2)

This keeps the first law separate; it does not multiply correlated marginals. It is sharper than the provisional loose expression above. With m=3, p_0=O(log N/N^2), t<=C N^-1/3 log N U_*, and U_*>=cN^-2, every cross term divided by U_* is even smaller than the direct O(N^-1/3 log N) term. Indeed the extra p_0^(1/m) is the cost of the necessary downward reset before the path can climb again.

Equation (2) is a local kernel comparison. It still does not by itself verify arbitrary initial inactive seeding, the uncapped complementary value, or the full actual global repair for this missing-pure-source graph.
