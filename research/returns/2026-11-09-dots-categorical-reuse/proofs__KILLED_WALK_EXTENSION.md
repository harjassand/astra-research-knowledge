# Exact categorical reuse with a distribution-uniform latency tail

9 November 2026. New analytic extension; the original reviewed proof is preserved unchanged. No experiment, implementation, novelty claim or application acquisition.

## 1. Contract and parameter choice

Use exactly the finite-alphabet, actual stored X~P, independent fresh P/Q samples and independent fair-bit contract in PROOF.md (SHA256 851453442a734b44a033acb90079e1ad5e101718f9ed32dd15c7c25d483b7439). The alphabet size d is known. Fix rational 0<eta<=1/2 and define

    L = ceil(2/eta),
    b = the smallest nonnegative integer with 2^b >= 2d(L-1)/eta,
    beta = 2^(-b),
    C = 1+2d(L-1),
    D = 2^b + L C + 2,
    B = 2D.

These quantities use integer/rational arithmetic only. In particular beta<=eta/[2d(L-1)] and 1/beta<4d(L-1)/eta. Thus C=O(d/eta) and D=O(d/eta^2), with all constants displayed.

Modify every one-label factory in the original algorithm: immediately before each original query, independently kill the factory with probability beta. On killing, return UPPER, exactly as if the upper boundary had been reached. Otherwise make the original fair P/Q source choice and query, updating or holding the counter as before. A beta coin is exactly b fair bits with killing precisely when all are zero. At L=1 the original immediate-UPPER convention could still be used; the stated parameter choice has L>=4.

The top-level reuse and residual-rejection algorithm is unchanged. There is no timeout fallback and no discard based on observed elapsed runtime.

## 2. Why killing preserves the exact marginal

Let a_beta(p,q) be the probability of hitting LOWER before UPPER or killing, starting at counter 1, with upward label probability p and downward label probability q. For p+q>0 set

    d_beta(p,q)=p a_beta(p,q).

For every finite LOWER-terminating path, the number of downward steps is one greater than the number of upward steps. If there are u upward steps and h holding steps, multiplying that path's probability by the initial p gives a factor proportional to

    (pq)^(u+1) (1-(p+q)/2)^h (1-beta)^(2u+1+h).

The omitted power of 1/2 depends only on the number of nonholding moves. This expression is symmetric in p,q. The set of admissible counter paths depends only on the fixed boundaries, not p,q. Summing their nonnegative probabilities therefore proves

    p a_beta(p,q) = q a_beta(q,p).

The boundary cases with p=0 or q=0 give zero on both sides. For both zero set d_beta=0. The walk is killed almost surely if it has not already absorbed, so this finite-path sum accounts for its complete LOWER event.

Write d_i=d_beta(p_i,q_i), r_i=p_i-d_i, s_i=q_i-d_i and R=sum_i r_i=sum_i s_i. These are nonnegative and r_i-s_i=p_i-q_i. The first factory's UPPER-or-KILL probability conditional on X=i is r_i/p_i. The reversed factory after a Q proposal j accepts with probability s_j/q_j. Therefore the same exact coupling identity as before holds:

    Pr(X=i,Y=j)=d_i 1{i=j}+r_i s_j/R.

In particular the new marginal remains exactly Q. A killing event is not an arbitrary replacement by a fresh Q sample: it changes BOTH common-mass factories symmetrically, and the residual race restores the required column sums.

## 3. Retention loss caused by killing

Couple a killed factory with its original un-killed finite-interval walk, using the same query/source stream until killing. Denote original durations by tau_0(p,q) and the two original averaged costs by

    A_0=sum_i p_i tau_0(p_i,q_i),
    B_0=sum_i q_i tau_0(q_i,p_i).

The reviewed identity gives A_0+B_0=2s(L-1), where s<=d is union-support size. Let R_0 be the original residual mass and R_beta the new one. Lost common mass is nonnegative and equals R_beta-R_0. The probability that killing occurs among an original N-query walk's kill opportunities is 1-(1-beta)^N<=beta N. Summing first in the P representation and then in the Q representation gives

    0 <= R_beta-R_0 <= beta min(A_0,B_0)
                           <= beta s(L-1)
                           <= eta/2.

The symmetry proved in Section 2 is essential: both sums bound the SAME lost common mass. Together with the original R_0<=TV(P,Q)+(1-TV(P,Q))/L,

    Pr(Y!=X) <= R_beta <= TV(P,Q)+1/L+beta d(L-1)
                              <= TV(P,Q)+eta.

Also R_beta>=R_0>=1/L, so the residual acceptance rate remains bounded below without probability evaluation.

## 4. Expected source cost is not increased at a fixed L

Let A_beta and B_beta be the corresponding averaged killed-factory query costs. In the common-stream coupling the killed factory executes a prefix of the original queries, so A_beta<=A_0 and B_beta<=B_0. The residual proposal/renewal argument is unchanged and includes all rejections:

    E N = 1+A_beta+B_beta <= 1+2s(L-1) <= C.

The mean number of residual proposals is still exactly one overall, because that stage is entered with probability R_beta and takes 1/R_beta proposals conditionally. Thus the mean number of factory invocations is exactly two. Source choices during queries remain conditionally fair, yielding

    E N_P = (A_beta+B_beta)/2,
    E N_Q = 1+(A_beta+B_beta)/2.

This is the cost at the larger L needed to allocate half the slack to killing. Compared with the earlier eta-only choice L=ceil(1/eta), the distribution-uniform latency repair can increase the certified mean by approximately a factor of two, not a new inverse-eta power.

## 5. Uniform remaining-work and tail bounds

In any currently running factory, regardless of its label, counter, p or q, the remaining number of source queries before either killing or absorption is dominated by the number of failures before an independent beta success. Its conditional mean is at most 1/beta.

At the start of the residual race, the expected remaining query count is

    (1+B_beta)/R_beta <= L(1+B_beta) <= L C.

At any other internal state, at most one currently running factory and a possible future residual race remain. A fresh proposal, when required, adds at most one query. Therefore the expected remaining source-query count, conditional on the complete current state and transcript, is bounded by D as defined in Section 1. This includes arbitrary midway counter states, not merely averaged initial states. Fresh independent killing/source randomness is required at all such states.

Reveal free internal bits up to the next source query or termination. This defines an embedded stopped process indexed by source-query count. The preceding bound applies at every reachable nonterminal embedded state. Markov's inequality over a block of B=2D queries, followed by the strong Markov/conditional iteration, yields

    Pr(N>mB) <= 2^(-m)                    for every integer m>=0,
    Pr(N>mB) <= (C/B) 2^(-(m-1))         for every integer m>=1.

The second bound uses the sharper initial mean E N<=C for its first block. Hence all moments are finite with constants uniform over P,Q, even when individual atoms approach zero.

A conservative explicit second-moment ledger is

    E N^2 <= 12 B C = 24 D C = O(d^2/eta^3).

Indeed, use E N^2=sum_(n>=0)(2n+1)Pr(N>n). The first block contributes at most 2BC by the mean bound. For block j>=1 use the second displayed tail: its contribution is at most BC(2j+1)2^(-(j-1)). The sum of those coefficients is 10.

For any latency-failure tolerance delta>0, these formulas supply an explicit source-query quantile. One may choose an integer m>=1 with (C/B)2^(-(m-1))<=delta, then mB queries suffice except on probability delta. This is a latency statement for the exact untruncated algorithm, not a claim that forcibly stopping preserves its marginal. If a hard stop with fallback is imposed, the marginal/retention changes by at most its overrun probability under the same coupling as in the earlier proof.

## 6. Exact finite-bit work

Each kill test uses exactly b fair bits, and each executed source query inside a factory uses one further fair bit for its named source. Every nonterminal kill test is followed by a query. At most one terminal kill test occurs per factory invocation. Since the expected number of invocations is two,

    expected kill tests <= E N + 1 <= C+1,
    expected fair bits <= b(C+1)+(C-1).

Pathwise the number of factory invocations is at most the number of residual proposals plus one, and proposals are counted in N. Therefore the total random-bit count is at most (2b+1)N+b. The same distribution-uniform tail applies after this deterministic cost conversion. Auxiliary state consists of two labels, a counter in [0,L], and counters for the b-bit test; a conservative memory bound is O(log d+log L+b), apart from source state and optional logging.

Arithmetic parameters can be computed from rational eta by exact integer comparisons. All subsequent decisions use only integer counters, label equality, and bits. There is no irrational coin, underflow, numerical normalization or hidden Bernoulli-factory compiler. Actual oracle runtime is separately paid under the existing conditional cost contract; a query-count tail is not a wall-time tail if the underlying oracle lacks one.

## 7. Prior and limits

The repair uses established independent killing/resolvent and Bernoulli-factory ideas. Its narrow operation is preserving a common retained mass under killing, then using the exact residual race to keep Q unchanged while obtaining a uniform remaining-work bound. No historical novelty claim is made.

Fixed-batch empirical coupling already supplies exact Q and a deterministic O(d/eta^2) query cap. The new result is an O(d/eta) mean together with a uniform exponential tail on the broader O(d/eta^2) scale. It is not an O(d/eta) hard-cap theorem or an exponential tail on the mean scale. The independent binary moment obstruction is being developed separately and is not assumed here.

For d=16, eta=1/100, the explicit choices are L=200, b=20, C=6,369, D=2,322,378 and B=4,644,756. These are conservative analytic bounds, not runtime measurements. High-confidence worst-case latency remains expensive. The original downstream work-ratio test must use the new actual disagreement/call costs; no real application satisfying it has been acquired. The exact-input, conditional-history and response-independence restrictions of the earlier proof remain unchanged.
