# Calculations, comparison and numerical limitations

## What was actually computed

The principal implemented `code/uniform_certificate.py` using only Python's
standard-library Decimal arithmetic. The frozen grid has 30 horizon rows,
24 accuracy-policy rows and 516 scalar certificate evaluations per run.
The full outputs are in `results/uniform_certificate_80.json` and
`results/uniform_certificate_120.json`. Their comparison is in
`results/uniform_precision_comparison.json`. These are rounded numerical
evaluations of rigorously proved inequalities, not outward-rounded interval
certificates and not simulations of exponentially many transitions.

Proof choices were frozen before those calculations: K=1, alpha=1/2,
h=0.01, and a=0.95 a_h*. They give

    a=0.2729655610161550...,
    S=287.12045716399948...,
    Lambda_*=3.3129027137733123....

The large S and fixed a make the finite upper certificate conservative.
No choice was optimized after seeing a favorable output. Vacuous bounds are
retained in full, including their raw values above one.

The lower contributor independently implemented the actual finite matrices,
not only the event bound. Sixteen laws q C^n were calculated by deterministic
matrix powers. The horizon is an exact power of two, up to 2^1000; this is
not a trajectory run of that length. All input pi,q,Q, resulting C, propagated
law, KL, event bound, TV, row sums and balance residuals are saved in the
two lower JSON files. The higher-precision run has 30 extra reserved digits.
Maximum working precisions are 392 and 422. The measured largest absolute
TV difference is about 1.073e-91; these are diagnostics, not a proof of the
asymptotic theorem or an interval arithmetic guarantee.

## Stable evaluation of the principal finite bound

The code selects x=log horizon and n=ceil(exp(x)), x>=16, but never builds
that enormous chain or integer. It uses R=exp(x)/x^4. In Theorem A,
Jbar<=2/(alpha n)<=2 exp(-x)/alpha and

    N=floor(n/2)>=(exp(x)-2)/2>=(x^2-2)/2.

Therefore replacing the survival term by
exp[-kappa_h(x^2-2)/2] is a conservative upper relaxation. It is not an
underflow-to-zero approximation. The five evaluated terms are

    A= min(1,K/(x-4log x-1)),
    survival=exp[-kappa_h(x^2-2)/2],
    high=S exp[theta(log A-x+4log x)],
    core=S exp[theta(log(M/h+1)+log(2/alpha)-x)],
    stationary_core=sqrt[(2/alpha)(M exp(-x)+x^-4)].

At fixed eta these nonnegative terms decrease for x>=16. The integer search
brackets and bisects the first x for which their sum is <=0.95 epsilon.
It verifies that the preceding integer fails this margin. The resulting
ceil(exp(x)) is a sufficient horizon for the exact inequality; the printed
numbers approximate that certificate. No inference about actual optimal
mixing time follows from the size of this sufficient horizon.

## Ordinary pure IMH comparator with the same error contract

The ordinary comparator uses q and the same unnormalized target oracle,
starts at q, permits complete caching, and performs one ordinary nonlazy
IMH proposal per update. It already has the sharp minimax coefficient K.
For a finite sufficient comparison use the following elementary coupling.

Couple a q-start chain and a pi-start chain with the same iid candidates and
acceptance uniforms. Until they meet, whichever chain currently has the
larger W stays at that initial larger weight whenever the chains do not
coalesce. If the larger chain accepts a candidate, so does the smaller;
otherwise a move of the smaller chain keeps it below the unchanged larger
weight. When both initial weights are at most R, the probability of
coalescence in each step is at least

    integral_{W<=R} min(1,W(y)/R) q(dy)=pi(W<=R)/R.

The exceptional initial event has probability at most
a_R+q(W>R)<=a_R(1+1/R). Consequently

    TV(q G^n,pi)<=a_R(1+1/R)+exp[-n(1-a_R)/R].        (P)

Use the same forward-KL envelope a_R<=min(1,K/(log R-1)). In the comparator
code R=exp(x)/x^2 and n=ceil(exp(x)), giving the valid sufficient bound

    A(1+exp(-x+2log x))+exp[-(1-A)x^2],
    A=K/(x-2log x-1)<1.

Both algorithm certificates use the same 5 percent error margin. Their
cutoff choices are explicit and not jointly optimized. This compares two
sufficient certificates; it is not a ratio of actual runtimes. Pure IMH
remains the strongest established ordinary method needed for this claim.

## Selected finite certificate outputs

Here eta=min(1,d epsilon log(1/epsilon)). Each x is the integer for which
the sufficient step count is ceil(exp(x)). These impractically large bounds
are shown honestly; they are not a proposed simulation budget.

| epsilon | d | Hybrid x | Hybrid epsilon x | Pure IMH x | Pure epsilon x |
|---|---|---|---|---|---|
| 0.01 | 0.25 | 3530 | 35.30 | 116 | 1.16 |
| 0.01 | 1 | 901 | 9.01 | 116 | 1.16 |
| 0.01 | 4 | 246 | 2.46 | 116 | 1.16 |
| 0.01 | 16 | 128 | 1.28 | 116 | 1.16 |
| 0.001 | 0.25 | 28341 | 28.341 | 1068 | 1.068 |
| 0.001 | 1 | 7163 | 7.163 | 1068 | 1.068 |
| 0.001 | 4 | 1892 | 1.892 | 1068 | 1.068 |
| 0.001 | 16 | 1084 | 1.084 | 1068 | 1.068 |

These outputs establish no hybrid advantage. For example at log n=10^6,
lambda=4 in eta=lambda loglog n/log n, the computed raw bound multiplied
by log n is about 162.47, despite the proved eventual limit 1. The fixed
proof constants produce a long transient. At lambda=8 the same scaled
bound is approximately 1.0001037. Neither is an observed Markov-chain error.

The exact adverse path at lambda=1.08 has exponent 0.99429479028... .
The matrix diagnostics do not reach its eventual scaled divergence: at
n=2^1000 they give log(n) TV approximately 0.43074. Its rigorous asymptotic
obstruction comes from the explicit capture proof and the exact integer
inequality, not a favorable plotted trend. Integer path-length rounding and
the very small exponent gap matter. All unsuccessful numerical impressions
are retained rather than selecting more favorable examples.

## Physical and computational operation boundary

An n-step lazy hybrid makes alpha n/2 global proposals and beta n/2 local
proposals in expectation, plus initialization. Pure IMH makes n global
proposals plus initialization. Each local proposal first evaluates the
known q ratio. If that screen passes and the target value is not cached,
it evaluates the target, computes the reciprocal correction and tests a
second uniform. Global acceptance likewise uses cached target/q ratios.

Let c_q,c_Q,c_pi denote actual proposal/q-evaluation, local-proposal and
target-query costs under a specified recipient. The theorem bounds none
of them. Cached target calls are at most the number of distinct needed
states, and no more than 1 plus the number of proposals reaching a target
test. The full cache costs O(number of distinct cached states) entries.
There is no model-independent positive lower cost for a target call, or
uniform finite bound on precision needed for arbitrary log q and target
ratios. Log arithmetic avoids direct underflow but does not prove exact
Bernoulli decisions. Ideal-real mixing and approximate implementation remain
distinct.

Decreasing eta increases the local total acceptance and also weakens the
first rejection screen. It therefore does not reduce uncached target calls
for a fixed state/proposal pair. Different trajectories can change reuse,
so neither a total target-cost nor wall-time ordering follows. Maintaining
two acceptance stages, local proposals and their caching adds code and
maintenance requirements to pure IMH. No end-to-end efficiency measurement
or sampler speedup is claimed.

The adverse tables are supplied to the mathematical verifier. Were a
scientific recipient actually given the complete finite target table, direct
normalization and discrete sampling would be the ordinary method and cannot
be forbidden to favor this hybrid. The current theorem concerns the stated
ratio-oracle contract; it does not manufacture a downstream application.

## Failures and limits of execution

The initial principal script attempted mpmath, absent in both the default
and primary runtime. Both import failures occurred before any calculation.
The implementation was changed to standard-library Decimal, with no package
installation or external compute. A subsequent edit moved the principal
wall-clock measurement to include the variational-root calculation; both
precision outputs were then regenerated from the final source.

The lower contributor's first propagated-mass assertion incorrectly used
the full working precision after matrix-power amplification. The corrected
tolerance is based on reserved precision, with explicit extra log10(n)
digits. The failure and rationale are saved in
reviews/vanishing_lower_failed_checks.txt. This changed a diagnostic
tolerance, not the mathematical acceptance rule or a claimed observation.
