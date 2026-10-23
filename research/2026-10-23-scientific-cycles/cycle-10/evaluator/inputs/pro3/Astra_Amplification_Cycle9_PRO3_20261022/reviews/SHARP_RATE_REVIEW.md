# Independent source-bound challenge: sharp public-distortion rate

Reviewer: `/root/cycle9_rate_challenge`, independent of the constructive
upper and lower contributors. Review date: 22 October 2026, UTC.
Review started at the observed clock 09:14:18 UTC. This is an internal
mathematical challenge of the changed Cycle9 theorem, not an external
referee report or a new audit of the full historical programme.

## Verdict and exact binding

**ACCEPT the principal logarithmic-rate theorem and its explicit same-v
separation under the stated native assumptions. No mathematical repair
was required.** The review identified one notation collision and supplied
an elementary strict-constant comparison; the principal incorporated
both without changing the theorem or any construction.

The final source personally inspected and accepted is:

- `SHARP_DISTORTION_RATE.md`
- 26,911 bytes
- SHA256 `5f76de8b2e7567cadae8ae06d272de8e1bdbae1e6e29ddf1a34800f090e5ce2f`

The initially assigned source had SHA256
`7b74640d5c3eeecae04cd6bf0493327cecf48f54e4dccaa21f535a1d41428a34`.
An intermediate editorial version had SHA256
`fe2f50c9330481ebd4d5e120f0b080a0c18f776cc0d6ae5543356f559a6c74dc`.
The changes were: removal of a stray `+or`; renaming the accepted core
hazard to `g_core` so it cannot be confused with the index-zero value of
the sequence `g_i`; and replacing a terse strict-inequality check with
the elementary argument recorded in Section 7 below. The affected final
sections were reread. This verdict does not silently bind later edits.

The accepted statement is, for every deterministic public policy sequence
with v_n->infinity,

    -log R_n / min(loglog n, u_n c(D_n)) -> 1,

where D_n=|kappa_n-eta_n|A_n, u_n=eta_n log n,
v_n=u_n/(1+D_n), r=alpha exp(-K)/(1-alpha), and

    c(d)=inf_{a>=0,d+a>0} log(1+r exp(a))/(d+a).

This is a logarithmic equivalent for the native class supremum. It is
not a multiplicative risk equivalent, an endpoint amplitude, or a
practical sampler advantage. Those distinctions are correctly retained.

## Sources read and dependency scope

The review read the principal proof in full and the load-bearing source
interfaces below. The complete predecessor chain remains an accepted
dependency rather than being independently reproved here.

| Source | Bytes | SHA256 |
|---|---:|---|
| Cycle8 `ASYMMETRY_BUDGET_THEOREM.md` | 28,265 | `eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1` |
| Cycle4 `BRANCHING_SHARPNESS.md` | 18,093 | `119dfb8d0b8e77b3ce93fdef1f1450c01fc1d090a0f05c4dd7ae0ea7ada1d645` |
| Cycle7 `RECIPROCAL_PROPOSAL_THEOREM.md` | 21,709 | `584c2fcbedcead37578b91596ace85eeb75426537d564cdd646d44831f4dbc6a` |
| Contributor `STRONG_DISTORTION_UPPER.md` | 14,135 | `fc353cdd3a0d97af5eaf21b18ab0c2272170fa4f3f53c858371347f5d1e9c6c2` |
| Contributor `FINITE_DISTORTION_LOWER.md` | 14,146 | `413294034f5304445f106e9bb2ddf6b234d2ee3a40752461734142a3ba77cff4` |
| Contributor `GROWING_DEPTH_LOWER.md` | 16,677 | `b9868b2a1f25881af254cca84b2013341c053c934fe5b79eea00b0c7065434af` |

The constructive notes were used to locate obligations, not treated as
independent acceptance. The conclusions below follow from checking the
principal's finite inequalities and native construction directly.

## 1. Native assumptions and finite interface match

The new theorem keeps finite positive pi,q, one population forward-KL
budget, proposal initialization, fixed alpha, actual lazy mixture,
fixed-within-run public policy and target-independent reciprocal Q.
The local factors still multiply to the target Hastings ratio. The
target-corrected local kernel is reversible even if Q is asymmetric.
The proposal row budget, reverse-proposal evaluations, true rejection
diagonal and all original-chain returns remain present.

The finite certificate quoted in principal equations (6)-(11) matches
the actual Cycle8 source. Its scalar envelope is applied only with
theta<=eta and theta<=1/2. The local accepted-outflow subtraction and
the separate global q-density Jensen step are not replaced by a mere
off-diagonal comparison. The first-hit operator is not renormalized.
The full-return decomposition propagates each first hit using the
original C, and the one KL budget supplies both tail inequalities.

The chosen h, R, test cutoff and N are the valid predecessor cutoffs.
Their small errors are uniform in support, degree, minimum mass and Q.
No unstated lower bound on eta, upper bound on kappa, or bound on the
number of native states enters the new proof.

## 2. Scalar coefficient and all finite endpoints

With z=exp(-a), the inequality

    exp(dc) z^(1-c)-z <= r

is equivalent to exp[c(d+a)]<=1+r exp(a) for every a>=0. Therefore
the variational coefficient is exactly the largest permitted proof
exponent c. At d=0, the excluded a=0 term imposes no missing constraint.
At c<1 the z=0 endpoint is zero, which is strictly below r>0; thus
c<c(d) gives a genuine strict margin H_d(c)<r.

The derivative numerator of phi_d(a)=log(1+r exp(a))/(d+a) is

    B(a)=(d+a) r exp(a)/(1+r exp(a))-log(1+r exp(a)).

Its derivative is positive for d+a>0 and its limit is d-log r.
This proves all three stated regimes:

1. If r>=exp(d), the infimum is one, approached at infinity.
2. Otherwise a finite positive minimizer gives F(c)=r exp(-d).
3. The minimizer reaches a=0 exactly at
   d_*=(1+r)log(1+r)/r; beyond it c(d)=log(1+r)/d.

At the second/third junction c=r/(1+r), so the formulas agree.
The capped first case also joins continuously at d=log r. These
checks include r=1 and r>1; no interior-only premise has been carried
across an endpoint. Positivity and continuity imply that g(d)=(1+d)c(d)
is bounded above and away from zero on the extended half-line, with
limit log(1+r) at infinity. This fact is essential to the final
subsequence argument and is established, not assumed.

## 3. Both uniform upper regimes pay accumulated errors

For D_n->d<infinity and v_n=O(loglog n), eta_n=O(loglog n/log n).
With fixed c<c(d), theta=c eta_n gives p->1, tau->1-c and
U->exp(dc). The finite scalar maximum converges to H_d(c)<r.
The actual positive part therefore vanishes eventually, uniformly
over native instances. Accumulation costs N theta=O((loglog n)^2/log n),
which tends to zero. The resulting tail plus exp[-c u_n+o(1)] bound
is valid even if v_n/loglog n tends to zero.

For D_n->infinity, theta=gamma eta_n/D_n tends to zero because eta_n<1.
Now U tau>1 eventually, so the exact finite branch is
H=exp(gamma p)-1. The positive part need not vanish. Its bound

    Delta=O(theta+(loglog n+1)/(log n)^2)

is correct: beta(exp(gamma)-1)=alpha exp(-K), while the finite low-set
KL cutoff changes 1-b by the second stated error. After N iterations,
all theta terms are paid relative to theta log n. The remaining terms
tend to zero. This proves the principal's general bound (16), not just
its bounded-v/loglog n specialization.

In particular, the proof never reasons that Gamma->1 implies Gamma^N->1.
In the general large-v case it retains the multiplier explicitly.
There is no endpoint substitution into a strict old norm theorem.

## 4. Native realization, multiplicity and moving signs

I independently checked the proposal rows and both orientations. On an
M-ary tree, each internal row has M child probabilities 1/(M+R_A)
and one parent probability R_A/(M+R_A), summing exactly to one.
Boundary rows have their actual completing diagonals. Every edge has
absolute log proposal asymmetry A_n.

The ceiling choices yield chi~(v_n+1)^2 and f=chi/(1+chi)->1.
For coalescence, kappa>=0 gives A_n>=D_n/eta_n. In the finite positive-d
case and the diverging-D case this grows much faster than log(v_n+1),
so R_A exp(-h_n)->infinity and the ceiling error is harmless. This
remains true under alternating mismatch signs. Positive mismatch
allows A_n to approach zero: expansion rounding still works because
R_A>=1 and exp(h_n) diverges.

The exact per-vertex screen calculation is decisive. In expansion,
z/M=R_A^(-kappa/eta)exp(-a/eta). In coalescence,
zM=R_A^(kappa/eta)exp(-a/eta). With the respective reverse-Q ratios,
both produce S=exp(-a). The target Hastings ratio is n^2/chi in both
orientations. Thus forward acceptance is sigma=exp(-a), reverse
acceptance is chi sigma/n^2, and after counting native multiplicities
the local aggregates are f sigma and f sigma/n^2. No factor of M is
missing. The true diagonal is retained.

The level partition is strongly lumpable by the actual native symmetries.
The q start is uniform within levels, as are all subsequent laws, so
quotient TV equals native TV. This is not an oracle-access assumption.

## 5. Information, actual global exits, capture and retention

The integer depth J=ceil[(ell+6 log ell+log b)/V] gives simultaneously

    n ell^2 <= W_J < n ell^2 exp(V),
    W_(J-1) < ell^2/n.

Consequently every transient weight is below the core weight, proving
the premise that was absent from the old arbitrary-distortion lower.
The complete KL upper is log(1/q_star)+ell^-4(ell+2 log ell+V), which
tends to -log(1-b)<K. The proof has established V=o(ell), so the
fixed terminal target mass ell^-4 is legitimate in this new regime.

For a transient level i, the exact global out-of-level probability is

    q_star + sum_(j>i) q_j + (sum_(j<i) pi_j)/W_i.

The first two terms are at most 1-b. The last term equals
q_i sum_(k=1)^i n^(-2k), at most b/(n^2-1). This justifies the
improved competing-exit constant alpha(1-b)/2. It is not the
probability of all global attempts. Rejections and global moves within
the current level are correctly retained as holds.

The marked-event calculation uses actual deterministic time windows.
From every vertex at a level the same local-forward probability and
same exit hazard apply, so conditional within-level motion does not
invalidate the geometric waiting identity. Iterating J windows uses
the Markov property and reaches the terminal union by n/2. No random
attempt count is replaced by its expectation.

At the terminal union the full-chain escape is exactly
alpha(1-p_T)/(2W_J)+beta f sigma/(2n^2), so n times this quantity tends
to zero. Global moves among terminal vertices remain retained. Paths
outside the selected event, including exits followed by returns, have
not been deleted from the actual chain; they only enlarge its final
terminal probability. Thus the finite lower (28) is sound.

For both finite positive d and infinite d, J=Theta(v_n), while
1-f=O(v_n^-2). Hence J(1-f)->0. The timing and retention corrections
are relative o(1), and log P_n=log b-J log(1+r_b exp(a))+o(1).
The b and a approximations are made only after the horizon limit.
Every actual instance has finite a and strict KL slack.

## 6. Universal quantifiers and the thin v/loglog n regime

This is the main extension beyond the finite-lambda contributor note.
The principal proves it directly. When D_n->d in (0,infinity),
v_n->infinity and v_n=O(L), the same calculations give

    V~(d+a)/eta_n,  J~u_n/(d+a)=Theta(v_n),
    -log P_n/u_n -> log(1+r_b exp(a))/(d+a).

No step requires v_n/L to be bounded away from zero. If v_n/L->0,
the capture logarithm is o(L), making ell^-4 negligible after subtraction.
This supplies the needed lower, rather than extrapolating from a
finite positive lambda theorem.

For D_n->0 the principal correctly switches lower constructions.
The actual Cycle4 source states its tree estimates for u->infinity,
u=O(loglog n), not only for a positive limiting ratio. I read its
finite construction, accumulated screen estimate, timing/retention
and strict parameter-order argument. It therefore covers u/L->0.
Every symmetric Q is admitted under every current asymmetry budget,
and its actual screen is independent of kappa. The dependency is used
by exact inclusion, not by assuming the coalescing rounding bound
continues to hold at d=0.

Finally, compactified subsequences D_n->d and v_n/L->x exhaust every
policy. If x=infinity, the accepted coarse upper and Q=I lower give
amplitude K. For finite x the new uppers apply. If x g(d)>=1, including
equality, the Q=I lower suffices. If x g(d)<1, strict approximation to
the appropriate capture coefficient keeps its exponent below one,
so the terminal target mass can be subtracted. When x=0 the same
argument uses normalization by v_n. Since g stays bounded away from
zero, the common denominator diverges and additive logarithmic
constants disappear. This proves the arbitrary-oscillation statement.

The proof never adds two separately saturated KL constructions. The
tail and transport lowers are alternatives in the class supremum.

## 7. Same-v statement and ordinary comparator

All three displayed policies have eta_n in (0,1) eventually, nonnegative
kappa_n, the same A_n=ell/L-2 and exactly v_n=L. The middle policy has
D=log4-1, and F(1/2)=1/4 implies c(D)=1/2 on the valid interior branch.
Its exponent is log2. The other two exponents are c(0) and
log(1+exp(-1)). These are genuinely distinct class-supremum rates.

The elementary ordering supplied during review is:
F(c)<=c gives c(0)>=exp(-1)>log(1+exp(-1)). Also
F(2/3)=2/(3 sqrt(3))>exp(-1), because
e>8/3>3 sqrt(3)/2; the latter follows from 256>243. Hence c(0)<2/3,
while log2=2 atanh(1/3)>2/3. Thus the separation does not rely on a
floating decimal or a fitted curve.

The same-input ordinary-IMH bound follows by first hitting the core
and then contracting under the original G. Its tail is O(ell^-4) on
the new transport witnesses at deterministic j/n->t>0. The proof
correctly retains the ordinary minimax amplitude K and allows direct
sampling of fully disclosed analytic targets. It does not equate
step counts with wall time or target-call budgets.

## Limits of acceptance and resources

The proof's frozen coalescence diagnostic exceeds K=1 and is explicitly
reported as an algebraic fixture only. It is not used in the universal
proof or its asymptotic admission argument. That failed finite admission
does not become positive evidence through a favorable TV number.
This review did not rerun the diagnostic or any old scientific suite;
its task was the new mathematical argument.

The review used local source reads, analytic derivations and source hashes.
No new simulation, native large graph, hardware, spending, paid credits,
outreach, public disclosure or other owner's investigation was used.
Observed clock bounds and file identities are in the accompanying receipt.
Total inference, token, design and discovery costs are unknown. The
short source-access operations are not claimed as research cost.

This acceptance is internal and conditional on the exact native model
and accepted finite-interface dependencies. Formal verification,
external mathematical acceptance and historical originality remain
unestablished. The theorem does not establish critical amplitudes,
fixed-support laws, finite-precision robustness or useful implementation
advantage. Integer-depth rounding is harmless for its logarithmic
equivalent and may matter at the selected next amplitude frontier.
