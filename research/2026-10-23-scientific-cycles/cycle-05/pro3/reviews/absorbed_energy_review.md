# Source-bound acceptance: critical-window endpoint theorem

Reviewer: `/root/critical_budget`. Scientific date: 22 October 2026,
Australia/Brisbane. Complete source read and final decision recorded at
2026-10-21 22:20 UTC (2026-10-22 08:20 Australia/Brisbane).

## Exact reviewed source and decision

Principal proof: `CRITICAL_ENDPOINT_THEOREM.md`

- Bytes: **18,790**.
- SHA256: **4a459d8ee78253564a849b3033abc25e548224dc695fbb819cd9860e3a5c9014**.

**Decision: accept the new finite absorbed-energy lemma, finite TV certificate,
and critical-window upper without repair.** Combined with the unchanged,
already accepted Cycle4 lower dependency, the stated exact critical amplitude
follows in the declared native finite class with `alpha exp(-K)/beta<1`.
No gap was found in the complete source. This is an internal mathematical
review, not formal verification, historical-priority adjudication, external
acceptance or an implementation-performance claim.

The full proof was read, with focused reconstruction of Sections 3--7. The
historical branching lower was not re-reviewed. Its unchanged accepted status
is an explicit dependency.

The reviewer previously supplied the joint information lemma independently
on a separate assigned obligation. Consequently this is an independent
challenge to the principal's **new absorbed-boundary construction and its
use of the lemma**, not an independent second discovery or independent
review of the reviewer's own budget contribution. The principal separately
owns acceptance of that contribution. The provisional review
`contributors/critical_budget_absorption_review.md` is preserved unchanged;
this document binds the final verdict to the actual complete source.

## 1. Absorbed process is the correct first-hit object

Rows in A retain their original C entries into A union E and lose the actual
mass sent to B\E. E rows absorb. No killed row is normalized. The identity
`P^E=(I+alpha G^E+beta L^E)/2` gives exactly this proof process, including
absorbing E rows. Initial mass is the restricted subprobability q 1_A,
explicitly distinguished from the conditional distribution q(.|A).

Equation (7) is therefore exact: E mass at horizon N counts all first B-hits
in E by N, and only those hits. Absorbing after the hit is legitimate for
this event calculation. Equation (17) later propagates the original first-hit
submeasures by the full C, so the proof never substitutes absorption for the
sampler's actual later trajectory.

## 2. Weighted independence inequality

Because W_x<h<=W_y for x in A,y in B, all independence proposals from A to B
are accepted. The actual G[A,A] row mass is b, including the true rejection
diagonal. In particular G_yy<=b for y in A.

For the absorbed G^E, row masses are b+e on A and 1 on E. The q-density
column on y in A is at most `b+(b-q_y)<=2b`. The column on y in E is exactly
`1+b`: the absorbing row contributes 1 and incoming A rows contribute their
q mass b. Both are at most 2. Weighted Jensen in the unnormalized q measure
gives equation (13) with no support or minimum-probability factor. The
identity between the weighted density norm and the transformed counting
p-norm uses `p(1-theta)=1` and is exact.

## 3. Local inequality retains rejection and survives absorption

For theta=c eta with 0<c<1, the actual local acceptance bounds every
transformed off-diagonal entry by Q_xy. For a downward proposal-mass ratio,
the positive transformed row change is at most
`Q_xy[v^(1-c)-v]<=Q_xy F(c)`; upward-ratio changes are nonpositive. Keeping
the original rejection diagonal gives the A-row bound 1+F(c). Absorbed
E rows have sum exactly 1.

The transformed columns are at most 2. This remains true in E, where the
new diagonal 1 is combined with incoming A off-diagonal entries bounded by
Q_xy. Symmetry/stochasticity supplies their sum bound. The proof correctly
uses counting-measure Jensen for this local matrix and weighted Jensen for G;
these are different representations of the same transformed input energy.

Equation (12), including its different A/E energy coefficients, follows.
It would have been too coarse to replace them by a common row maximum before
combining the mixture, but the delivered proof does not do that.

## 4. Mixture convexity and capture coefficient

The three convexity weights 1/2,alpha/2,beta/2 sum to one. Their A coefficient
is exactly

`1/2 + 2^(p-1)/2 [1 + beta F(c) - alpha(1-b) + alpha e]`.

Their E coefficient is `1/2+2^(p-1)/2`. Both are bounded by Gamma(e) as defined.
The initial transformed p-energy is b. Iteration followed by Holder on E
therefore gives exactly

`b^(1-theta) e^theta Gamma(e)^(N/p)`.

The first-hit times are accumulated in one absorbed vector. There is no
geometric sum of norms requiring endpoint strict contraction. Gamma may
exceed one, consistently with the previous strict-norm obstruction.

## 5. Finite TV certificate keeps all tests and returns

For j=0,...,N, the proof uses the actual bounded test `g_j=C^(n-j)f` and its
own anchor z_j. The single union set E lies in B and contains every high-W
point and every moderate-W point with anchor deviation above d_test at any
relevant j. The anchor gives its proposal mass at most bar e, uniformly in f.
The set's dependence on f is harmless because the finite hit bound applies
to every E subset B and the mass estimate is uniform.

For first hits into B\E, the accumulated test error is at most d_test times
a total mass at most one. Bad initial B mass contributes q(E); bad hits from
A contribute the absorbed probability. Every stationary comparison costs
at most `a+sqrt((M+R)J)`, weighted by the corresponding first-hit mass. The
remaining trajectories have mass at most b rho^N and are compared with an
equal-mass stationary measure. Thus equation (15) is valid with the actual a,b.
The monotone replacement e->bar e in the capture bound is legitimate.

## 6. Budget incorporation is exact

Section 5 correctly incorporates the contributor's finite log-sum lemma.
The entropy over H is bounded below by a log R. The remaining complement's
proposal mass is replaced by the larger 1-b in the direction that lowers the
bound. The derivative in d=pi(A) is nonpositive over the required interval
because `d<=hb<=b(1-a)` when h+a<=1. Substitution d=hb therefore gives a
valid lower bound. The handling of b=0 and the subsequent elementary
`(1-x)log(1-x)>=-x` bound are correct.

At the selected cutoffs the hypotheses hold eventually, and the remainder is
uniformly `O(u^-4 log u+1/log n)=o(u^-2)`. This supplies the joint allocation
`k_n+a_n log R<=K+o(u^-2)`. No independent second KL budget is introduced.

## 7. Uniform endpoint errors and class supremum

With `L=log n`, the proof has N=O(log L)=O(u), h=u^-4,
R=n/L^4 and d_test=L^-2. The second entry in the definition of bar e is
uniformly bounded above by `O(n^-1 L^4 u^5)` and below by a positive constant
times `n^-1 L^4`. The cap 1-b is eventually inactive because it is bounded
away from zero. Hence `log bar e=-L+O(log L)` uniformly.

At c=c_*, the energy deficit satisfies `Delta=O(h log(1/h))`. Consequently
`N theta`, `N Delta` and `N bar e` all tend to zero, giving
`Gamma(bar e)^(N/p)=1+o(1)` uniformly. Also
`bar e^theta=exp(-c_*u+o(1))`. The ordinary anchor errors are O(L^-2), and the
chosen numerical coefficient in N guarantees b rho^N<=L^-2 once
q(B)>=exp(-K)/2. The uniform continuity bound
`sup_b |b^(1-theta)-b|=o(1)` is valid even if b tends to zero. Equation (26)
therefore has genuinely uniform remainder terms.

For subsequences with k_n->k<K, a fixed c>c_* can be chosen with a strict
actual killing margin. Then Delta is eventually zero and the same finite
certificate makes transport o(1/L), yielding at most K-k. For k_n->K,
the joint budget forces L a_n->0 and b_n->b_K; the endpoint bound leaves at
most b_K exp(-c_*s). Near-maximizing finite instances exist to any prescribed
positive tolerance whether or not the supremum is attained. Subsequence
compactness of k_n then proves the full-class limsup. This argument does not
assume diagonal monotonicity or substitute a random count into a fixed-horizon
formula.

## Scope and resource record

The review covers the exact finite positive native model, fixed Q and eta
inside each run, and the stated nondegenerate critical regime r_0<1. It does
not extend the critical amplitude to r_0>=1, nonreversible/adaptive schedules,
empirical KL budgets or numerical implementation errors. Pure IMH remains the
stronger ordinary practical comparator; no speedup follows.

No numerical jobs, matrix searches, simulation, external data or historical
proof replay were used in this review. This is an analytic source inspection.
Active inference time, token counts, monetary costs and historical totals are
unknown. The timestamp records when final source inspection completed, not
an estimate of discovery cost.
