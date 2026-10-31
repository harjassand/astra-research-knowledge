# Large ambient space: positive replay, spectral discarded state

Working construction following the large-n challenge, 31 October 2026.
Not independently reviewed at this source freeze. A 4096-state executable
and saved-count replays now instantiate the construction. This note owns
the next hard step instead of treating the previous sufficient billion-sample
schedule as necessary. The methods of aggregation, sparse spectral learning,
randomized norm estimation and concentration are established tools; the exact
reusable composition and its all-cost utility still need assessment.

## 1. Mixed positive/L2 scalar certificate

Acquire a task-compatible partition, indicator Z and uniform within-block
average W. Put P=ZW and Q=I-P. P is both stochastic and orthogonal in the
uniform probability inner product H=I/n. No true invariant law is assumed.
Let K_a=W A_a Z and let B_a be stochastic with
||K_a-B_a||_infinity<=d. Require b=P b and ell^T=ell^T P.

Acquire bounds

    e_in >= max ||Q A_a P||_H,
    e_out >= max_g,a ||(W A_a Q)[g,:]||_(H^-1),
    alpha >= max ||Q A_a Q||_H.

With M=||b||_infinity, t_0=0, t_(j+1)=min(1,alpha*t_j+e_in),

    |ell^T A_w b - ell^T Z B_w W b|
       <= ||ell||_1 M [l*d+e_out sum_(j<l)t_j].                  (M1)

Proof: stochastic full trajectories have H norm at most M, and orthogonal Q
has norm one. The discarded-state H recurrence is therefore the same capped
recurrence as before. Retained coordinates W x have sup norm at most M;
their error is propagated by the stochastic B, with one-step discrepancy
d M plus e_out ||Q x||_H. Output uses ell^T Q=0 and
||ell^T Z||_1<=||ell||_1. Neither common stationarity nor global contraction
away from constants is needed. Only the discarded space must contract.

Words retain the explicit column-application convention of the other notes.

## 2. Fresh row and pooled-vector validation is linear in ambient dimension

Lock the partition before fresh per-row batches of N transitions. Let C be
their empirical stochastic matrix, Rhat=C Z and That=W C. Write
pi_g=|block_g|/n and G=diag(pi_g).

For N independent categorical vectors (not necessarily identically
distributed) with mean p, their average phat satisfies

    E||phat-p||_2 <= 1/sqrt(N),
    Pr(||phat-p||_2 > (1+sqrt(K))/sqrt(N)) <= exp(-K).            (M2)

The expectation follows from the sum of coordinate variances <=1/N.
Changing one categorical outcome changes the norm by at most sqrt(2)/N;
McDiarmid's inequality gives the displayed deviation. The number of labels
does not enter this Hilbert-norm bound.

Let rho_R=(1+sqrt(K_R))/sqrt(N) with K_R>=ln(mn/delta_R).
For all rows, ||(A Z-C Z)[i,:]||_2<=rho_R simultaneously. Since Q is
H-orthogonal, a valid incoming bound is

    e_in <= ||Q Rhat G^(-1/2)||_(H,F) + rho_R/sqrt(min pi_g).     (M3)

The first term is just a weighted sum of rational squares, so no irrational
basis need be stored. Indeed QAP is isometric to the retained input map
QAZ G^(-1/2), and Frobenius dominates its induced norm.

Each pooled row That[g,:] averages |block_g|N independent categorical vectors,
possibly with different row laws. Applying (M2) with K_T>=ln(mr/delta_T),
then using that right multiplication by Q contracts the dual H norm, gives

    e_out <= max_g ||(That Q)[g,:]||_(H^-1)
              + max_g sqrt(n/(|block_g|N)) (1+sqrt(K_T)).        (M4)

Thus balanced acquired blocks of mass at least 1/(kappa r) need
N=O(kappa r log(mn/delta)/theta^2) per row to price both cross blocks to
O(theta). Total validation samples are O(m n r polylog(n)/theta^2), not
fine estimation of every one of n^2 transition entries. Counts can be stored
sparsely by observed edges. Actual support size, sorting/lookups and every
count update are paid. A large dense support can still make storage large.

For a finite candidate family fixed after training, include its size in the
confidence union bounds as in FINITE_CANDIDATE_ACQUISITION.md. This is not
free optimization over arbitrary partitions chosen after validation.

## 3. Acquiring the discarded spectral norm from a sparse observed matrix

Uniform-row coarse pairs give a sparse raw C with ||A-C||_2<=t under the
already derived matrix-Bernstein event, at a conditional O(n polylog(n)/t^2)
source budget when the acquired incoming-mass bound is constant. This event
is uniform over every subsequently acquired P. Hence

    alpha <= ||Q C Q||_2+t.                                    (M5)

Computing an n-by-n exact PSD decomposition would spoil the large-n goal.
Here is a paid randomized upper certificate that only uses sparse matvecs.
Fix F=Q C Q after all data/partition selection. Draw each coordinate of an
integer vector g independently uniformly from {0,...,J-1}, where J>=2/delta_N.
For any fixed unit vector v, choose a coordinate with |v_i|>=1/sqrt(n).
Conditioning on the other coordinates, the interval
|v^T g|<1/(2sqrt(n)) contains at most two possibilities for g_i. Therefore

    Pr(|v^T g|<1/(2sqrt(n))) <=2/J <=delta_N.

Apply this to a unit leading eigenvector of F^T F. On the complement event,

    ||F||_2^(2p) <= 2sqrt(n) ||(F^T F)^p g||_2.                (M6)

For p=O(log(n/delta_N)/log(1+xi)), the upper estimate from (M6) is within a
factor 1+xi of the actual norm, because ||g||_2<=J sqrt(n). This is a
standard randomized norm-estimation idea with an elementary exact-integer
anti-concentration proof; it is not asserted as new numerical linear algebra.

The probe must be fresh after fixing F. A maliciously chosen probe or an
outcome-adaptive stopping exponent does not inherit the fixed-design claim.
Several candidate matrices can share independent-of-data probes only with
the relevant finite union bound. Every failed power test is charged.

## 4. A bounded-bit sparse implementation route

Acquire a rational beta>=||C||_2 from
sqrt(||C||_1 ||C||_infinity), using outward rational rounding. Then Q and
C/beta, C^T/beta all contract Euclidean norm. Instead of forming huge exact
denominators in (M6), compute

    z approximately [(F^T F)/beta^2]^p g

with integer fixed-grid rounding after each of the five operations
Q, C/beta, Q, C^T/beta, Q per iteration. If the grid is 2^-b, accumulated
Euclidean error is at most 5p sqrt(n) 2^(-b-1), with no exponential inflation.
Therefore a valid rational norm admission test for candidate a is

    (a/beta)^(2p) >= 2sqrt(n)
        [||z||_2 + 5p sqrt(n)2^(-b-1)].                        (M7)

Use outward square-root bounds and exact rational comparison; also retain the
deterministic fallback beta. Sparse C has a known count denominator, and Q
uses the acquired integer block sizes. Each rounded sparse operation uses
fixed common-denominator integer accumulators whose bit sizes are paid. The
grid can be selected before the probe with b proportional to p plus the
source/count/task bit budgets. No n-by-n PSD check or exact invariant measure
is silently supplied. A conservative implementation still pays O(p(nnz(C)+n))
integer multiply-adds and O(n) live grid state, plus source storage and setup.

## 5. Downstream operation and executed scope

The concrete downstream operation is certified batch screening of Q
explicitly supplied routing/control schedules: output each terminal-event
probability and return the best among that supplied list. Uniform prediction
error epsilon gives a 2epsilon additive guarantee for the returned list-best
schedule. It does NOT solve unrestricted open-loop or feedback planning.
Reading the Q schedules, evaluating them, prefix storage, all acquisition and
all comparison methods are charged.

A relevant synthetic access model is packet motion on a large sparse network
with several routing regimes, source-region initial distribution and a target-
region terminal indicator. The partition must be learned from observed edges;
hidden generator coordinates are not learner input. Sparse community/spectral
methods, including retained ordinary baselines, get exactly the same graph
observations and this certificate. An asymptotic sample expression is not a
demonstration of practical utility. The current executable adds direct
quadratic-functional leakage tests (QUADRATIC_LEAKAGE_VALIDATION.md), an
acquired variance pilot, empirical Bernstein fine-action confidence, and
retained-data reuse. The 4096-state fixtures and cached/streamed integer
predictions are executed; logical forward calls are represented by aggregate
synthetic multinomials, not individually executed. Strongest general
variance/KL/goal-oriented comparisons and exact historical matching remain
open. See LARGE_PRIOR_AND_LIMITS.md.
