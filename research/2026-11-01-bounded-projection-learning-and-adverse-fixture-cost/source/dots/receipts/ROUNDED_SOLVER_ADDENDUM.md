# Independent rounded-FW finite-bit addendum — 2026-11-01

This independently audits the root's subsequent rounded-step proposal. I read and verified the actual author file ROUNDED_PROJECTION_SOLVER.md SHA256 972ee67b866093f791d11e8081d379bbdf27037f80549b92c8d29d690ca3640b, together with current main construction SHA256 4dd9265425b1ef0f78c487602c63e6cd8d78b429c1cf7bc67155981e8ad1632f; the acceptance below binds those bytes. It supplements, rather than retroactively changes, the original unrounded proof recorded in RECEIPT.md (original historical SHA256 c298209577337f2aae8fba8c1f16d55e8641c003ca67bf880c68962d32b8bae9; subsequently given a current-byte/update notice). That receipt's larger digital accuracy cost concerned its explicitly UNROUNDED solver. The rounded solver below has a different and better certified bit-work bound.

## Judgment

The rounded solver is sound. It preserves the exact gap stopping criterion and therefore all statistical projection, corrected-output, witness and lifetime proofs in the preceding receipt. It gives a sufficient full DIGITAL accuracy factor lambda^-2 up to logarithms, not merely the source-shot factor, while retaining large polynomial rank/horizon dependence. No implementation speedup, optimality, or novelty follows.

## Descent proof independent of coefficient conditioning

At size m, B=m, C=16mB^2, delta=B^2 alpha. Let the exact empirical gradient be g=2Gbar c-2Khat d and let s be the exact l1-ball minimizing vertex. When gap=<g,c-s> exceeds delta, form

    c'=(1-theta)c+theta s,  theta=delta/C.

Then round each coordinate TOWARD ZERO to a fixed dyadic grid h=2^-p satisfying

    h <= delta^2/(24CBm).

Both c' and its rounded version c'' remain in the l1 ball. The entire segment joining them lies in that convex ball. Binary sample means imply |Khat_ij|<=1. Also |Gbar_ij|<=2: off-diagonal entries are empirical means, and the diagonal shift m alpha<1. Thus on the whole ball

    ||gradient qbar||_infty <=2(2B)+2B=6B.

The rounding displacement has l1 norm at most mh, so integration of the gradient along that feasible segment yields

    qbar(c'')-qbar(c') <=6Bmh <=delta^2/(4C).

Curvature gives qbar(c')-qbar(c)<=-theta gap+(C/2)theta^2 < -delta^2/(2C). Therefore each nonterminal rounded step decreases the SAME exact empirical objective by at least delta^2/(4C). This is not an assumption that rounding preserves the FW gap; the gap is recomputed exactly at the new rounded iterate.

Using the conservative objective-range bound R=8mB^2, the cap

    N=1+ceil(4CR/delta^2)=1+ceil(512m^2/alpha^2)

forces a gap<=delta iterate before exhaustion. As before, exact PSD verification is required; if it fails, acquisition permanently fails. Binary bounds and this objective-range argument hold even off the simultaneous estimation event whenever the guard passes.

The chosen output is l1-feasible and has actual empirical FW gap <=delta. It consequently has exactly the empirical suboptimality guarantee used by the original projection proof. No new rounding allowance needs to be charged to the PHYSICAL projection/output certificate: the final objective-gap certificate already includes the effects of every rounded step. If instead an implementation stops merely after a heuristic count or uses an unverified approximate gap, this conclusion would not follow.

## Finite-bit bound

Choose p as the least nonnegative integer satisfying 2^-p<=delta^2/(24CBm), by exact rational comparisons. Since alpha>=lambda/(3072m^3), the step count is O(m^8lambda^-2), but

    p=O(log(m+1)+log(lambda^-1)+tolerance input bitheight).

Each stored coefficient has O(p+log B) bits, independent of N. Initialize every solve at zero; input d is the seed or a previous grid-valued solve. The intermediate unrounded step combines fixed-grid coefficients with rational theta, then immediately returns to the fixed grid by exact integer quotient toward zero. Computing that intermediate value also has only O(L_*) bits, where L_* is the input/confidence/word-size quantity defined in the preceding receipt. Empirical binary means share the epoch shot-count denominator; repairing the diagonal and adding fixed-grid products preserves polynomial O(L_*) bitheight, including logarithmic summation factors.

With naive schoolbook arithmetic, an exact dense gradient/gap step costs O(m^2L_*^2) bit operations. A solve therefore costs O(m^10lambda^-2L_*^2). At most O(H) solves per rejected/acquiring stage and W+1 stages give W-degree at most 11. Moment acquisition has degree at most 8; exact PSD tests, bilinear corrections and outward roots have smaller degree. For example a safe common DIGITAL envelope is

    C(k+H+1)^2(H+1)^5(W+1)^16(1+lambda^-1)^2 L_*^6.

Thus the previously recommended beta=delta_stat/(W+1)^64 is more than sufficient for polynomial unconditional expected acquisition. No unproved polynomial-QP blackbox, exact line search, or unknown Gram eigenvalue enters this bound. The iteration count and polynomial constants can nevertheless be enormous.

The same proof applies to candidate-prefix distance solves, with their target coefficient mass one and the same conservative delta, C, h and objective-range bounds. All preceding failure-latch, source encoding, actual-adjoint, horizon, and physical-cost qualifications remain in force.

## Exact rational check

rounded_descent_exact.py passed 350 exact rational one-step descent/feasibility checks at m=1,2,3, with a singular rank-one physical Gram plus diagonal repair and bounded empirical cross terms. Every tested nonterminal step preserved the fixed dyadic grid and l1 feasibility and decreased objective by at least delta^2/(4C). These are bounded-QP algebra checks, not a physical-source simulation or a run of the potentially enormous optimization cap. The proof above, not this finite diagnostic, establishes general convergence.

### Finite binary scheduler accepted; audit closed

Read and SHA-verified BINARY_SCHEDULER.md, SHA256 10cb212745356dff1f6b2d06a78fc26ad45979c3d87eaa1e6d0ba1b7fa7d217f. Its E=1+ceil_log2 W bounds all reachable precision epochs; each epoch has at most W1(W1+1)/2 unordered descriptor pairs, so Jmax=(E+1)(W1+1)^2 is conservative. Every required moment uses descriptors of length <=H+1. The shared binary shot count n_b=ceil[8alpha^-2 ceil_log2(2Jmax/beta)] more than ensures 2exp(-n_b alpha^2/2)<=beta/Jmax. Conditional unbiasedness makes this valid for each adaptively selected job conditional on its starting history; union over the finite job universe gives the required simultaneous event. Canonical symmetric caching, demand-only scheduling, current-epoch remeasurement, unique retention, and permanent failure preserve the preceding good-event source count and finite worst-event bound. The recurrence computes W and W1 without enumeration, and their confidence-log bit cost is already included in L_*. No further mathematical qualification or correction was found. This closes the requested audit; it does not claim integration or execution of the full receiver.
