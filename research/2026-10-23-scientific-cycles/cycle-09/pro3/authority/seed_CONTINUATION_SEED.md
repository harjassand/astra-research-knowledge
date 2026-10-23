# PRO3 current scientific continuation after Cycle8

Date: 22 October 2026, Australia/Brisbane.
Owner: Astra PRO3. This source supersedes the prior tentative budget question.
Preserve newer verified owner-local work if this checkpoint is later imported.

## Read first

1. REPORT.md
2. ASYMMETRY_BUDGET_THEOREM.md — complete principal proof
3. contributors/ASYMMETRY_ENERGY.md and ASYMMETRY_LOWER.md
4. reviews/CRITERION_REVIEW.md and its source-bound receipt
5. FAILED_APPROACHES.md, INFORMATION_AND_COST_CONTRACT.md, COMPARATOR.md
6. NUMERICS.md and the frozen executable inputs/results

The unchanged Cycle7 owner original is sources/Astra_Amplification_Cycle7_PRO3_20261022.zip,
2,410,386 bytes, SHA256
fede9a15e5d94efee2152b3527e05d78ce92d2a92c1160ed8a253346df42fdc9.
It recursively preserves all earlier accepted source. Do not restart those
programmes or re-audit their whole proof chain by default.

## Exact current contract

Finite labelled positive pi,q, fixed K>0 and alpha in (0,1), beta=1-alpha,
D(pi||q)<=K, initialization q. Public horizon policy 0<eta_n<1,
finite kappa_n>=0, finite A_n>=0. Q is fixed, target-independent,
row-stochastic with reciprocal off-diagonal support and actual
A(Q)=max |log(Q_yx/Q_xy)|<=A_n. No off-diagonal edges means A(Q)=0.

S_xy=(q_y/q_x)^eta (Q_yx/Q_xy)^kappa.
L_xy=Q_xy min(1,S_xy) min(1,[pi_y Q_yx/(pi_x Q_xy)]/S_xy).
The actual diagonal completes L. G is proposal-q independence MH.
C=(I+alpha G+beta L)/2. Every object stays fixed during each run.
Support grows across the supremum. TV is half l1 and logs are natural.

The sampler has no free target normalizer, target table, KL estimator,
absorbed simulator, or index/precision oracle. All native evaluation,
proposal, reverse-Q, caching and arithmetic costs remain real.

## Newly closed result

Let D_n=|kappa_n-eta_n|A_n, u_n=eta_n log n,
v_n=u_n/(1+D_n), and R_n=sup_admitted TV(q C^n,pi).

R_n->0 IFF v_n->infinity, equivalently u_n->infinity and D_n=o(u_n).

For fixed mismatched eta in (0,1), kappa>=0 this is exactly A_n=o(log n).
Fixed finite public asymmetry permits any fixed mismatch and leading
amplitude K. This does not contradict the unrestricted-Q mismatch floor.

Uniform finite upper, with constants depending only on K,alpha:
R_n <= K/[log n-4loglog n-1] + C/(log n)^2 + 2 exp(-c_0 v_n),
c_0=min(1/4,alpha exp(-K)/(8 beta))/4.
If v_n/loglog n->infinity, then (log n)R_n->K.
The latter condition is sufficient, not proved necessary for amplitude K.

## Load-bearing new upper operation

For theta<=eta,theta<=1/2,p=(1-theta)^-1,w>=1,
tau=p(1-theta/eta), U=w exp(D theta p/eta), define
H_w(D)=sup_{0<z<=1}(U z^tau-z).
This controls the powered accepted-flow bracket, INCLUDING its actual
outflow subtraction. Reverse-Q Jensen then gives local weighted energy
2^(p-1)[(1+H) E_A + E_E].

For A_low={W<h}, b=q(A_low), E subset its complement, e=q(E), the
absorbed multiplier is
Gamma(e)=1/2+2^(p-1)/2 [1+[beta H-alpha(1-b)]_+ +alpha w e].
First-hit mass <= (b/w)^(1-theta)e^theta Gamma(e)^(N/p).
Killed rows are never renormalized; all hit times accumulate in one vector;
each first hit is propagated by the original C with all returns.

Choose theta=eta epsilon_0/[2(1+D)], epsilon_0=min(1/4,r_0/8),
r_0=alpha exp(-K)/beta. Then H_1(D)<=3r_0/8 and actual global killing
pays the positive part uniformly.
Use h=(log n)^-2,R=n/(log n)^4,d_test=(log n)^-2,
N=ceil[8/(alpha exp(-K)) loglog n].
Keep N log Gamma=O(N theta)+o(1) in the combined exponent;
do not claim Gamma^(N/p)->1 for fixed eta and bounded D.
The first-hit exponent is -theta log n+theta O(loglog n)+o(1).

## New admitted lower operation

On a subsequence D_n/(eta_n log n)>=a>0 choose fixed integer J with Ja>1
and fixed b in (0,1-exp(-K)).
Use R_A=exp(A_n), M=ceil R_A and an actual M-ary tree plus core.

Positive mismatch: expand root to leaves, individual parent->child Q=1/(2M),
child->parent R_A/(2M), q-level ratio z=M R_A^(-kappa/eta).
Negative mismatch: coalesce leaves to root, reverse the progress orientation,
z=R_A^(kappa/eta)/M. Both native outgoing row budgets hold exactly.
All off-diagonal proposal ratios saturate the public bound.

V=-log z>=a log n-log2.
q_i=bz^i, pi_i=p n^[-2(J-i)], p=1/[(log n)^2(1+V)].
Native uniform splitting yields S=1 exactly; target Hastings completes
local forward f and reverse f/n^2, with f->1/2.
One whole-instance KL tends to -log(1-b)<K even for unbounded V.
Terminal W_J/n->infinity from monotonicity of (1+V)exp(-JV).
Whole-terminal-union escape is alpha(1-p)/(2W_J)+beta f/(2n^2).

Mark ALL global attempts and local backward moves as failures only in a
lower-bound event. Count actual local holds and deterministic windows.
This avoids any false assumption that transient W_i stay below the core.
The resulting liminf floor is >=b[beta/(2alpha+beta)]^J>0.
It is a lower bound, not an exact floor or full-law limit.

A symmetric three-state witness covers bounded eta_n log n. These two
branches exhaust every sequence with v_n not tending to infinity.

## Comparator

Pure G on the SAME multilevel instances has
TV(qG^j,pi)<=p/(1-n^-2)+bz/[(1-b)(1-z)]+b^(j+1)->0
for j->infinity, including any deterministic j/n->t>0.
General ordinary IMH amplitude K is preserved.
Direct target sampling remains allowed when its analytic structure is known.
No target-call or wall-time speedup follows.

## Actual validation and status

Principal proof SHA256:
eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1.
Principal accepts the theorem and both distinct incoming contributions.
A fresh source-bound reviewer found no load-bearing defect or required repair.
This is internal mathematical acceptance; no formal verification,
historical priority or external acceptance is claimed.

One frozen exact-rational principal run passed: 128 local and 128 mixture
energy checks, 384 first-hit identities, 16 full-return identities,
eight fourteen-state native configurations and 24 native/quotient law checks.
Every conservative finite TV lower was negative at the small frozen
fixture: preserve that limitation; do not retune to manufacture a plot.
The asymptotic lower is analytical.

Original diagnostic body ~0.797s wall, ~0.795s CPU, 14,080KiB peak RSS.
Replay/transfer times are separate. Total discovery and inference costs unknown.
No numerical jobs remain active.

## Precise next selected question

Determine the sharp reachable-transport rate in the convergent public-budget
class, focusing on v_n of order loglog n. First decide whether a sharp rate
can depend on v_n alone, or whether two policies with the same v_n but
different A_n and |kappa_n-eta_n| admit genuinely different minimax rates.

This is not an instruction to optimize the scalar envelope in isolation.
A complete answer needs actual native row budgets/multiplicity, fixed-within-run
policies, full rejection/return behavior, and one KL allocation.
The present finite H_w(D) and two-sign native construction are reusable.
A construction separating same-v policies would be a meaningful alternative
to a universal rate formula. No numerical asymptotic inference is permitted.

## Closed scope and continuity

Do not reopen the native/interior/global critical laws, first-order law,
fixed-screen, prefix/optional-prefix or one-step contraction searches.
Preserve the B3 pISO correction and failed full inference at its frozen
gate, closed metadata and R3/anMC operations, and retired thermal/TPV/
half-cell/molecular/GUIDE campaigns. Other protected programmes retain
their owners. The broader sampling mission stays active.

Delivery through the existing private Page route is source availability,
not evidence of Max/evaluator reading, acceptance or integration.
The final archive identity and actual transport receipt are separate
from these scientific files.

