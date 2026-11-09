# Exact categorical reuse with capped local factories

9 November 2026. This is a simpler continuation of KILLED_WALK_EXTENSION.md, not an alteration of the original reviewed theorem. It needs no additional killing coins. Analytic result only; no run, practical timing or novelty claim.

## 1. Algorithm and explicit parameters

Assume the same exact independent sample-oracle contract as PROOF.md. The actual stored X has law P, and Q is fixed independently of its realized value under that contract. The alphabet [d] is known. Given rational 0<eta<=1/2, set

    L=ceil(2/eta),
    K=ceil(2d(L-1)/eta),
    C=1+2d(L-1),
    D=K+L C+2,
    B=2D.

In every one-label factory of the original algorithm, count its source queries. Run the original counter walk until a boundary is hit OR K queries have been executed. If query K hits LOWER, return LOWER. Any upper hit or an interior state after K queries returns UPPER. Thus LOCAL TIMEOUT is treated like UPPER.

The outer algorithm is unchanged: run this capped factory on X with P upward/Q downward; on LOWER return X. Otherwise repeatedly propose J~Q and run the same capped factory with Q upward/P downward. Accept J on UPPER, including its local timeouts, and repeat on LOWER. The number of residual attempts is NOT capped.

This is not the invalid global operation of timing out the whole coupling and substituting an independent Q sample. Both common-mass factories and the residual rejection law are changed consistently.

## 2. Exact common mass survives the local cap

Let a_K(p,q) be the probability of reaching LOWER by query K before reaching UPPER, from counter 1. In every such path, downward moves exceed upward moves by one. If it has u upward moves and h holds, multiplication by the initial probability p makes its probability proportional to

    (pq)^(u+1) [1-(p+q)/2]^h.

All omitted factors depend only on the path, and the permitted path set (including its length<=K condition) is unchanged when p,q are exchanged. Therefore

    d_K(p,q):=p a_K(p,q)=q a_K(q,p).

This also holds when one probability is zero; both sides vanish. Set d_K(0,0)=0. Define d_i=d_K(p_i,q_i), r_i=p_i-d_i, s_i=q_i-d_i and R=sum r_i=sum s_i. The actual complete joint law is

    Pr(X=i,Y=j)=d_i 1{i=j}+r_i s_j/R.

Its new marginal is exactly Q. The selected old sample is not replaced in proving its first marginal. No probabilities are evaluated by the algorithm.

## 3. Error and expected queries

Compare with the original uncapped finite-interval factory at the SAME L. Let tau_0(p,q) be its mean source-query duration and

    A_0=sum_i p_i tau_0(p_i,q_i),
    B_0=sum_i q_i tau_0(q_i,p_i).

The original reviewed identity gives A_0+B_0=2s(L-1), s<=d. The local cap only removes LOWER events with original duration exceeding K. Since the lost common mass is symmetric, Markov's inequality in both representations gives

    0<=R_K-R_0<=min(A_0,B_0)/K<=d(L-1)/K<=eta/2.

Consequently

    TV(P,Q)<=Pr(Y!=X)<=R_K
                       <=TV(P,Q)+1/L+d(L-1)/K
                       <=TV(P,Q)+eta.

Also R_K>=R_0>=1/L. Let A_K,B_K denote the averaged capped-factory query counts. Each capped duration is the minimum of K and the original absorption time. Thus A_K<=A_0, B_K<=B_0. The complete residual-race normalization cost is still paid by the same first-step identity:

    E N=1+A_K+B_K<=C,
    E N_P=(A_K+B_K)/2,
    E N_Q=1+(A_K+B_K)/2.

The overall expected number of residual proposals is exactly one. Attempt duration may be correlated with acceptance; the renewal argument uses fresh independent attempts and does not assume otherwise.

## 4. Distribution-uniform tail and second moment

From the beginning of the residual stage the expected remaining number of source queries is

    (1+B_K)/R_K <= L C.

From ANY internal state of a current factory there are at most K further queries before that factory terminates. Afterward the algorithm either stops or starts the residual race. A possible fresh proposal costs one query. Therefore the conditional expected remaining source-query count is at most D at every reachable state, independently of P,Q, their support, and their smallest atom.

Let F_n be the transcript/state after n queries and deterministic internal processing. On {N>n}, at least one more query will occur and the conditional expected remainder is at most D. Markov iteration in blocks B=2D gives

    Pr(N>mB)<=2^(-m),                        integer m>=0,
    Pr(N>mB)<=(C/B) 2^(-(m-1)),             integer m>=1.

The second expression uses E N<=C for the first block. These are distribution-uniform exponential tails for the EXACT, untruncated outer algorithm.

There is also a sharper elementary second-moment identity than the conservative block-sum estimate:

    E[N(N+1)]/2
      =sum_(n>=0) E[(N-n) 1{N>n}]
      <=D sum_(n>=0) Pr(N>n)
      =D E N.

Tonelli justifies the nonnegative sums; the finite right side then establishes finite second moment. Hence

    E N^2 <= (2D-1) E N <= 2DC = O(d^2/eta^3).

No unknown atom floor or uniform conditional cost at the old uncapped input is assumed. The LOCAL cap supplies the uniform internal-state bound.

## 5. Bits, memory and actual runtime

Every source query within a factory uses one exact fair bit. Residual Q proposals use none. Thus expected fair bits are A_K+B_K<=C-1 and pathwise their number is at most N. No additional random coin is needed for local timeouts. Counter storage is O(log d+log L+log K), with ordinary exact integer comparisons and updates. Conservative expected local bit work is O(C[log d+log L+log K]), plus actual source-oracle work. Parameter acquisition from rational eta is ordinary exact integer arithmetic.

The tail counts source queries, not arbitrary external wall time. If the oracles have bounded per-call work c, local work can be combined with c to obtain a wall-work tail. If only conditional mean source costs are supplied, only an expected work bill follows without a separate source-tail contract. Retained responses and conditional histories still need the original independence requirements and COST_AND_RESPONSE_CLARIFICATION.md.

The overall sampler has unbounded retries. Forcibly imposing a global cap plus arbitrary fallback produces an approximate-Q interface with TV error at most the displayed overrun probability; it is not the exact theorem. Exact fixed-batch empirical coupling remains available when a deterministic hard cap matters more than mean cost.

## 6. Finite resource gate

At d=16, eta=1/100:

    L=200, K=636,800, C=6,369,
    D=1,910,602, B=3,821,204.

Thus the exact algorithm uses at most 6,369 expected new queries. The displayed uniform tail bound gives an explicit, but potentially large, high-confidence latency allowance. The original eta-only unmodified factory bound was 3,169 mean queries without a uniform second moment. The repair pays a constant-factor mean increase for a uniform tail on a broader scale. None of these are measured runtimes or application gains.

The asymptotic distinction is:

- original factory: O(d/eta) mean; no distribution-uniform second moment;
- local-cap factory: O(d/eta) mean, O(d/eta^2) uniform tail scale, O(d^2/eta^3) second moment;
- fixed-batch empirical coupling: O(d/eta^2) deterministic source-query count.

Strong primary prior already covers gambler's ruin, residual coupling, Bernoulli factories and races. The current operation is the symmetric local-cap modification and complete outer-law/cost accounting. No priority claim is made. A separate binary moment/hard-cap obstruction is under independent development and is not assumed as an input to this proof.

The practical application gate remains unpassed. There is no measured real workload satisfying both exact sampling access and a sufficiently large downstream/source cost ratio. Common applications with known probabilities, accessible common randomness, or expensive upstream sampling may favor stronger existing methods.
