# Native path composition and the exact critical phase law

Astra PRO3, Cycle11. Principal construction and integration: /root.
Scientific date: 23 October 2026, Australia/Brisbane.

## 1. New result and structural consequence

This paper closes the arbitrary-geometry gap left by Cycle10. In the strict
zero-attenuation regime, the periodic depth penalty is the asymptotic value
of the **unrestricted native supremum**, not merely a feature of one tree.
Merging, cycles, nonreversible proposals, heterogeneous paths and all original
returns do not fill its troughs.

The new finite operation is a path-composition bound. Small proposal mass at
a first-hit boundary forces substantial cumulative proposal likelihood
progress on all but a paid exceptional mass. Progress need not be a function
of the current state: it can have circulation around proposal cycles. The
actual global exits then charge that progress through the already proved
history-dependent killed control. A reverse reference matrix is allowed to
have row sums up to 3/2, and its entire finite-time growth is paid.

This replaces the unproved demand for a deterministic progress coordinate.
It also extends the sharp finite-space law to arbitrary bounded
antisymmetric log-screen distortions, not only mismatched powers of the
forward/reverse proposal probabilities. That extension is an exact-real
robustness statement, not a floating-point or practical-sampler claim.

### 1.1 Exact native contract

Fix K>0 and 0<alpha<1, with beta=1-alpha. At horizon n, the public policy
has finite A_n>=0, 0<eta_n<1 and kappa_n>=0. They and all kernels remain
fixed throughout the run. The admitted instance has finite labelled strictly
positive probability vectors pi,q, population D(pi||q)<=K, initialization q,
and target-independent row-stochastic Q with reciprocal off-diagonal support
and max |log(Q_yx/Q_xy)|<=A_n over its off-diagonal edges.

G is proposal-q independence Metropolis-Hastings with target pi. All proposal
ratios and local screens below are defined only on edges x!=y with Q_xy>0;
set L_xy=0 on absent off-diagonal edges. On a present edge,

    r_q(x,y)=q_y Q_yx/(q_x Q_xy),
    r_pi(x,y)=pi_y Q_yx/(pi_x Q_xy),
    S_xy=(q_y/q_x)^eta (Q_yx/Q_xy)^kappa,
    L_xy=Q_xy min(1,S_xy) min(1,r_pi(x,y)/S_xy),
    C=(I+alpha G+beta L)/2.

Every completing rejection diagonal is the actual one. Let

    R_n=sup_admitted ||q C^n-pi||_TV,

with TV half l1 and all logs natural. Supports may grow with n. The sampler
does not receive a normalizer, target table, population-KL estimator, free
reverse-proposal evaluation, proposal label, exact-arithmetic service or
absorbed simulator. Native preparation, proposals, target calls, labels,
precision, indexing and caching retain their actual costs.

For fixed d>0 and s real, assume

    |kappa_n-eta_n| A_n=d,
    ell=log n, L=log ell, u_n=eta_n ell,
    c(d) u_n=L+s+o(1).

Write

    b0=1-exp(-K), r=alpha exp(-K)/beta,
    h_r(a)=log(1+r exp(a)), gamma=log(1+r), t=r/(1+r),
    d_star=gamma/t,
    c(d)=inf_{a>=0} h_r(a)/(d+a).

### Theorem A — exact unrestricted phase law

Suppose d>d_star. Define the continuous function on the unit circle

    Psi(x)=min{(d t-gamma)x, gamma(1-x)}, 0<=x<=1,
    Psi(0)=Psi(1)=0,
    phi_n={u_n/d}.

Then under every public policy sequence above,

    ell R_n - max{K, b0 exp[-s-Psi(phi_n)]} -> 0.       (1)

In particular,

    limsup ell R_n=max{K,b0 exp(-s)},                  (2)
    liminf ell R_n=
       max{K,b0 exp[-s-gamma(1-d_star/d)]}.            (3)

The limit exists exactly when b0 exp(-s)<=K; in that case it is K.
When b0 exp(-s)>K, the unrestricted minimax risk has the nonconstant
phase modulation in (1). This is a statement about the class supremum,
not just an oscillating witness family.

The earlier complete branches are preserved unchanged:

* r>=exp(d): ell R_n -> max{K,b0 exp(d-s)/r}.
* r<exp(d), d<=d_star: ell R_n -> max{K,b0 exp(-s)}.

They are not reproved as new results here.

### Theorem B — finite transport operation

The following statement is more general than the native target-corrected
model. Let q be a positive probability on a finite space and Q a stochastic
kernel with reciprocal off-diagonal support. Let 0<alpha<1, beta=1-alpha,
eta>0, d>0. Let L have off-diagonal entries Q_xy a_xy, where

    0<=a_xy<=min{1,exp(d) r_q(x,y)^eta},

and its actual completing diagonal. Let G be any stochastic kernel such that

    G_xy<=q_y for x!=y,
    G_xy=q_y for x in A, y in B=A^c,

where A is a set with b=q(A)<1. Set C=(I+alpha G+beta L)/2, with its actual
diagonal. Take E subset B, e=q(E), and start from the subprobability q1_A.
Let H_N(E) be the mass of first B hits by time N that land in E.

For r'>0 define

    M_{d,r'}(U)=min_{J>=1} J log(1+r' exp((U/J-d)_+)), U>0,
    V_{d,r'}(U)=exp[-M_{d,r'}(U)], U>0,
    V_{d,r'}(U)=1, U<=0.

The minimum is over positive integers. For every integer N>=1 and U>0,

    H_N(E)<=b V_{d,r_b}(U)
              +3 e (3/2)^N exp(U/eta),                (4)
    r_b=alpha(1-b)/beta.

Empty A or E has zero capture. There is no KL, stationarity, reversibility
or invariance hypothesis in this finite theorem. In particular Q need not
have an invariant probability supplied to the proof. The native application
retains all its stronger assumptions.

### Corollary C — arbitrary reciprocal screen distortions

Replace the native power screen by

    S_xy=r_q(x,y)^eta exp(xi_xy),
    xi_yx=-xi_xy, |xi_xy|<=d,

where the edge function is fixed and target-independent, and retain the
second Hastings factor, all real diagonals, G, alpha, the one KL budget and
q initialization. Its evaluations and representation are charged. Let the
supremum range over all finite such instances. At the same critical policy
the supremum satisfies (1), in addition to the two preserved branches.

Thus arbitrary spatial heterogeneity in a bounded reciprocal log-screen
distortion does not erase the discrete crossing cost. A concrete arithmetic
error model, its certified error and its evaluation cost are separate matters;
this corollary does not supply them.

## 2. Source dependencies and division of the argument

The unchanged predecessor is Astra_Amplification_Cycle10_PRO3_20261023.zip,
3,508,928 bytes, SHA256
55afc9d70013d8cc0332d6a03c51901876533d908412448d7d81b2b6f393e1c1.
Its CRITICAL_TRANSPORT_THEOREM.md is 24,570 bytes, SHA256
7d9aa025e15de176610b515a9deef9cd2fa9c84a60d315abd343235075e1b451.

We use three accepted interfaces, reproduced sufficiently below to expose
every new proof obligation:

1. Cycle10 Section 6: the exact finite killed-control value V and its
   Bellman inequality. This restricted model is closed; it is not the new
   result.
2. The full-return/anchored-smoothing decomposition, available in the
   predecessor's dependencies/CYCLE8_ASYMMETRY_BUDGET_THEOREM.md Section 4,
   SHA256 eba1595d9efec9c7dc8ac5c97257a9f0bf741f1f7931105114dc58faeae9e6c1.
   We replace only its bound on bad first-hit mass.
3. Cycle10 Section 5 and contributors/CRITICAL_NATIVE_LOWER.md: the actual
   two-sign native tree family and its full-law phase lower. Its exact
   acceptance, KL slack, strong lumping, retention, global moves and all
   returns remain unchanged. No old matrix suite is rerun.

The bounded contributor HETEROGENEOUS_TRANSPORT.md supplied the tagged-path
bridge and its proof. The principal checked that operation, derived the
uniform cutoff, one-budget asymptotic and larger screen class, and integrated
the complete argument here. A distinct contributor developed an exact
fixed-local-jump norm bound and independently challenged the bridge.
That supplementary norm result is not a premise of Theorems A-C.
A separate source-bound review checks the complete new argument.

## 3. Finite composition with all native path tags

We prove Theorem B. First record the accepted control inequality, for z>0
and x>0:

    sigma(x)[V(z-x)-V(z)]<=r_b V(z),
    sigma(x)=exp[-(x-d)_+],                            (5)

where V=V_{d,r_b}. V is nonincreasing. Equation (5) follows by prepending
one crossing to an optimal continuation. The preceding control proof
includes arbitrary randomized choices after any history of paid holds;
it does not require the action to remain fixed during a hold.

### 3.1 A reverse reference with a paid row budget

Resolve each off-diagonal transition of C into a local and global tag.
Their actual probabilities are beta Q_xy a_xy/2 and alpha G_xy/2.
Represent every stay, including all rejections, self proposals and laziness,
by one diagonal tag of probability C_xx. These tags sum exactly to C.

For the reference factors remove off-diagonal acceptances:

    B^local_xy=beta Q_xy/2, x!=y,
    B^global_xy=alpha q_y/2, x!=y,
    B^hold_xx=C_xx.

This reference matrix is not normalized. Its row sum at x is

    C_xx+beta(1-Q_xx)/2+alpha(1-q_x)/2<=3/2.           (6)

On a local tag put X(x,y)=-eta log r_q(x,y); on a global or hold tag put
X=0. For each labelled path x_0,...,x_j let Z be its signed sum of X.
Exact reversal of the reference factors gives

    q_x0 product B_forward
      =exp(Z/eta) q_xj product B_reverse.             (7)

Local factors supply r_q, global factors have
q_y B^global_yx/(q_x B^global_xy)=1, and the actual diagonal reverses
unchanged. No assumption that Z is a state potential is used.

Actual path mass is at most the left side of (7), because every removed
factor is at most one. Sum first-B-hit paths that end in E by time N and
have Z<U. After reversal their initial mass is q1_E. Dropping their
interior and first-hit restrictions only increases their reference mass.
By the ROW bound (6), their total actual mass is at most

    e exp(U/eta) sum_{j=1}^N (3/2)^j
      <=3 e exp(U/eta)(3/2)^N.                        (8)

This calculation includes branching multiplicity, shared terminals,
proposal circulation, repeated states and every stay. It neither asserts a
stochastic reverse kernel nor replaces its row bound by a column bound.

### 3.2 Positive progress and the real global killing rate

Until the first exit from A, define P as the sum of positive parts X_+ over
accepted local transitions. Clipping negative increments only enlarges
progress in this proof counter; it does not change the actual chain.

Every global transition from A into B has actual total probability

    g=alpha(1-b)/2=beta r_b/2.                        (9)

Regard all these global exits as killing, including global exits to E.
At a local edge with X>0 the acceptance bound gives a_xy<=sigma(X).

Before progress reaches U use the bounded potential V(U-P). Stop with
value 1 on reaching U, including when a local exit itself completes the
crossing. Stop with value 0 at an earlier global exit from A or at a local
exit that has not completed U. Native transitions within A with no positive
progress may change the physical state and future actions; they preserve
this potential. Actual stays also preserve it.

At every nonterminated history, with z=U-P>0, positive local drift is at most

    beta/2 sum_{y:X>0} Q_xy a_xy [V(z-X)-V(z)]
      <=beta/2 sum_{y:X>0} Q_xy sigma(X)[V(z-X)-V(z)]
      <=beta r_b V(z)/2 sum_{y:X>0} Q_xy
      <=g V(z).                                     (10)

Monotonicity of V justifies replacing a_xy by sigma. Equation (5) proves
the second inequality. The native proposal row budget proves the last.
Global killing subtracts exactly g V(z), and early local killing subtracts
additional nonnegative mass. The stopped potential is therefore a bounded
supermartingale. Finite iteration, without any unbounded optional-stopping
assumption, gives

    P_{q1_A}(progress completes by N before that killing)
       <=b V_{d,r_b}(U).                             (11)

A first-hit path into E with signed Z>=U belongs to this success event.
If its final tag is local, positive progress completes no later than that
tag. If its final tag is global, that tag contributes zero and completion
already occurred earlier, before the global killing tag. Thus direct
global hits are covered by (8) unless progress had already been paid.
Adding (8) and (11) proves (4).

The proof uses no fixed proposal label oracle: labels are a decomposition
of the probability law for analysis. It supplies neither a new sampler nor
a free absorbed operation.

## 4. Replacing only the first-hit term in the full-chain certificate

Return to the native model. With W=pi/q, choose hcut<1/2 and put
A={W<hcut}, B=A^c, b=q(A). For x in A,y in B, W_y>W_x, so native IMH
has G_xy=q_y. For every off-diagonal edge,

    log S_xy=eta log r_q(x,y)+xi_xy,
    xi_xy=(kappa-eta)log(Q_yx/Q_xy)<=d.

All hypotheses of Theorem B hold.

Here is the inherited full-return interface before inserting a first-hit
bound. Let n>=2, 1<=N<n, R>e, 0<xi_test<=1, and set

    M0=exp(2K+1), a=pi(W>R),
    J0=2/[alpha(2(n-N)+1)],
    rho=1-alpha(1-b)/2,
    ebar=min{1-b,a/R+(N+1)(M0/hcut+1)J0/xi_test^2}.

For each bounded test 0<=f<=1, the accepted anchored estimate applied to
g_j=C^(n-j)f, 0<=j<=N, supplies a set E=E(f) subset B with q(E)<=ebar.
It is the union of W>R and the N+1 sets where the anchored test deviations
exceed xi_test. If H_N(E) is the ORIGINAL first-B-hit mass into E, then

    |qC^n f-pi f|
      <=a+sqrt((M0+R)J0)+xi_test+ebar+b rho^N+H_N(E). (12)

The accepted identity behind (12) is

    qC^n=sum_{j=0}^N nu_j C^(n-j)+sigma_n,
    sigma_n(Omega)<=b rho^N,

where nu_j is the original unnormalized first-B-hit measure. Every hit is
propagated by the original C for all remaining steps. Initial bad hits cost
q(E); later bad first hits cost H_N(E). Thus replacing that single bound
does not remove any later exit, global attempt or return.

Combining (4) with (12), and using q(E)<=ebar, proves the finite certificate

    TV(qC^n,pi)
     <=a+sqrt((M0+R)J0)+xi_test+ebar+b rho^N
       +b V_{d,r_b}(U)+3 ebar (3/2)^N exp(U/eta).     (13)

It is uniform over every bounded test, support and native geometry.

### 4.1 The entire reverse growth is negligible at the critical scale

Put

    hcut=ell^-2, R=n/ell^4, xi_test=ell^-2,
    N=ceil[8L/(alpha exp(-K))].

The accepted binary KL bounds give

    a<=K/(ell-4L-1),
    k=-log(1-b)<=K+delta_h,
    delta_h=[K hcut+H2(hcut)]/(1-hcut)=O(L/ell^2).

For all sufficiently large n define the explicit positive bound

    E_n=K/[R(log R-1)]
          +(N+1)(M0/hcut+1)J0/xi_test^2.

Then ebar<=E_n, E_n=O(ell^6(L+1)/n), and

    sqrt((M0+R)J0)+xi_test+ebar+b rho^N=O(ell^-2).    (14)

Choose the proof threshold

    U_n=eta[log(1/E_n)-N log(3/2)-3L-log 3].          (15)

Since eta=Theta(L/ell) in the selected critical regime,

    U_n=u_n-O(L^2/ell)=u_n-o(1)>0,                  (16)
    3 E_n(3/2)^N exp(U_n/eta)=ell^-3.               (17)

The O-term in (16) can be understood as an absolute O-bound; no sign is
needed. The polynomial factor in E_n is explicit. In particular the
entire N log(3/2) is paid before the limit. No normalization of the reverse
matrix, no replacement of a deterministic horizon by an optional count,
and no inference that a one-step multiplier approaching one suffices is used.

Equations (13)-(17) yield the new uniform bound

    TV(qC^n,pi)<=a+b V_{d,r_b}(U_n)+O(ell^-2).        (18)

The constants depend only on fixed K,alpha,d,s and the eventual critical
policy bound, never on support, minimum atom or the actual geometry.

## 5. Stability and the single information allocation

For U>0 the minimizer defining M can be chosen with

    1<=J<=ceil(U/d),                                 (19)

because all larger J have cost J log(1+r') and the ceiling already has
zero attenuation. Every J-term is nondecreasing and 1-Lipschitz in U on
(0,infinity); its derivative when active is h_r'(U/J-d) in [0,1].
Taking the minimum preserves these properties:

    |M_{d,r'}(U)-M_{d,r'}(U')|<=|U-U'|, U,U'>0.      (20)

Also log(1+r' exp(a)) is 1-Lipschitz in log r'. Comparing minimizers and
using (19) gives, at a common U,

    |M_{d,r'}(U)-M_{d,r''}(U)|
       <=ceil(U/d)|log(r'/r'')|.                    (21)

No continuity at U=0 is asserted: V has the actual immediate-completion
boundary value there. Our thresholds tend to infinity.

Since r_b=alpha exp(-k)/beta>=r exp(-delta_h), monotonicity in r' and
(16),(20),(21) show, uniformly,

    V_{d,r_b}(U_n)
       <=exp[-M_{d,r}(u_n)+o(1)],                   (22)

because ceil(u_n/d)delta_h=O(L^2/ell^2)=o(1).

The finite control calculation already proved in Cycle10 gives, for d>d_star,

    M_{d,r}(u_n)=(gamma/d)u_n+Psi({u_n/d})+O(1/u_n)
       =L+s+Psi(phi_n)+o(1).                        (23)

It is uniform at integer phases and the tie of the two minimizing depths.
Equations (22)-(23) retain exactly the discrete cost that a best single
power-moment bound discarded.

We must not add a full K information tail to a full b0 transport term.
The accepted three-cell log-sum argument, for the SAME instance, gives

    k+a log R<=K+(hcut+a)(k+1)+hcut log(1/hcut),

and hence

    k+ell a<=K+o(1)                                 (24)

uniformly, using the binary bounds above.

Take any sequence of admitted instances, then a subsequence on which
k->k_infty in [0,K] and phi_n converges on the unit circle.

If k_infty=K, (24) gives ell a->0, b->b0, and (18),(22),(23) give

    limsup ell TV<=b0 exp[-s-Psi(phi_infty)].         (25)

If k_infty<K, then r_b stays eventually above a fixed r1>r.
There is a fixed c1>c(d)=gamma/d with

    h_{r1}(a)>=c1(d+a) for every a>=0.               (26)

For completeness: c(d)<1; choose a large finite cutoff beyond which the
ratio h_{r1}(a)/(d+a) is above (1+c(d))/2. On the remaining compact
interval it is strictly larger than the ratio for r, whose infimum is
c(d). Thus its infimum exceeds c(d). Choose c1 between the two.
Then for every J,

    J h_{r1}((U/J-d)_+)>=c1 U,

both when U/J>d and when U/J<=d. Consequently

    ell b V_{d,r_b}(U_n)
       <=exp[L-c1 U_n]->0.

Equation (24) now gives

    limsup ell TV<=K-k_infty<=K.                     (27)

These are the only cases. Choose finite-supremum approximate maximizers
within ell^-2 of R_n; no attainment is assumed. If the positive part of
ell R_n-max{K,b0 exp[-s-Psi(phi_n)]} failed to vanish, a subsequence and
(25)-(27) would contradict that failure. This proves the pointwise
asymptotic upper in (1) with the correct MAX allocation.

## 6. Native attainment and actual oscillation of the supremum

The accepted Cycle10 native family gives, under the same public policy at
EVERY sufficiently large n,

    ell TV(q_n C_n^n,pi_n)
       =b0 exp[-s-Psi(phi_n)]+o(1),                 (28)

with uniform phase error. Its Q is a true expanding/coalescing reciprocal
tree selected according to the mismatch sign, with native edge probabilities
and real row completion. All ratios use per-vertex masses. The construction
has explicit moving KL slack, W_terminal>=n ell^2, actual terminal escape
n d_T=o(1), a positive original global core hazard, and paid off-level
global/local-reversal errors. Its full-law equivalence includes all later
returns. Those source-bound obligations are preserved unchanged; this proof
does not infer (28) from the control value.

The separate Q=I information-tail family belongs to every policy class and
gives liminf ell R_n>=K. Combining these two admitted families by a MAX
with (28) proves the lower in (1). It does not combine their KL allocations
inside one instance.

All circle phases occur along integer horizon subsequences. For any fixed
x choose n_j nearest exp(exp[gamma(j+x)-s]). The critical policy gives
u_{n_j}/d=j+x+o(1). The continuity of Psi at the identified endpoints
handles the fractional-part convention. Its maximum is

    max Psi=gamma(1-d_star/d),

and its minimum is zero. Applying (1) proves (2)-(3). If b0 exp(-s)>K,
the phase-zero value is strictly larger than both K and the value at a
maximizer of Psi, so the unrestricted limit does not exist. If
b0 exp(-s)<=K, the expression in (1) is identically K. This proves every
claim of Theorem A.

## 7. Why the larger screen class has exactly the same law

For Corollary C, antisymmetry gives S_yx=1/S_xy and
r_pi(y,x)=1/r_pi(x,y). The elementary factorized Hastings identity

    min(1,S) min(1,r_pi/S)
      =r_pi min(1,1/S) min(1,S/r_pi)

proves detailed balance pi_x L_xy=pi_y L_yx. Thus C remains lazy and
pi-reversible and dominates alpha G/2 in Dirichlet form. These are the
only local-kernel facts used by the inherited anchored smoothing and
full-return decomposition (12). The upper screen bound in Theorem B
follows from xi_xy<=d, so the complete new upper applies.

For the lower, choose the original positive-mismatch public policy
A_n=d, kappa_n=eta_n+1 and its admitted native construction. Then
xi_xy=log(Q_yx/Q_xy) is a fixed-within-run, target-independent,
antisymmetric edge function with |xi_xy|<=d. That original family is
contained in the larger class. Its full-law phase lower and information
lower therefore remain available. This proves (1) for the larger class.

The other two critical branches also follow without new lower work. Their
accepted finite energy interface used only the upper screen inequality,
actual diagonal, reciprocal proposal rows and pi reversibility; all remain
valid here. The old admitted lower families are again a subclass. This is
an explicit consequence of the stated proof dependencies, not an unstated
extension to arbitrary nonreversible target kernels.

The new invariant formulation uses the reciprocal proposal FLOW r_q and
an antisymmetric bounded log-screen distortion. It does not give arbitrary
independent errors in forward/reverse target values, change the target, or
permit target-adaptive kernels during a run.

## 8. Comparison, significance, and boundaries

Ordinary independence MH retains the supplied-K minimax amplitude K under
the same proposal/target-ratio information. On the SAME native families
in (28), the accepted original-law estimate gives

    TV(q G^j,pi)
      <=p_T/(1-n^-2)+b_n z/[(1-b_n)(1-z)]+b_n^(j+1)
      =O(ell^-4), for j/n->t0>0,

including j=floor(alpha n/2), whereas the hybrid error is order ell^-1.
Analytic direct sampling is legitimate when the analytic target is actually
provided. There is no target-call, preparation, wall-time or useful-sampler
gain in this theorem.

The broader mathematical consequence is the finite composition principle
(4): rare-set probability, pathwise reciprocal-flow progress and genuine
killing can be combined without a deterministic progress coordinate or
acyclic reduction. It retains the integer crossing law that exponential
moments alone erase. Its present sharp consequence is an oscillating
UNRESTRICTED minimax risk and a wider bounded-screen class.

Path-probability reversal itself is established mathematics. Crooks,
"Entropy production fluctuation theorem and the nonequilibrium work relation
for free energy differences" (1999), Section II, equations (5)-(7), relates
forward and reverse path probabilities under its physical hypotheses.
Our reference has row sums up to 3/2 and is not a physical reverse process;
that fluctuation theorem is not applied here. Kevei, "Implicit renewal
theory in the arithmetic case," arXiv:1609.07339v1, Theorem 1 and Lemma 1,
establishes log-periodic tails for arithmetic renewal fixed-point problems.
Those are different observables and hypotheses; periodic asymptotics are
not newly claimed as a general phenomenon. Sherlock and Lee,
"Variance bounding of delayed-acceptance kernels," arXiv:1706.02142v4,
provides the relevant inheritance/failure and computational-comparison
context. It does not establish the supplied-K proposal-start minimax law.
Focused source details are in SOURCES.md. Historical novelty and external
acceptance remain unestablished.

All statements are exact-real finite mathematics. Neither a native enormous
graph nor a long Markov run was materialized. The new rational diagnostic
tests the labelled reversal and event interfaces at a small fixed horizon;
it is not an asymptotic proof. The admitted 32-state and failed-K=1
5,462-state historical fixtures remain unchanged and were not rerun.
The two-state precision boundary is preserved without a new numerical
campaign. Protected and retired programmes remain untouched.

## 9. Chosen continuation

The finite native critical phase problem is closed internally by this
checkpoint, subject to its recorded source-bound review. Do not reopen it
as another completion task.

The next question is whether the reciprocal-FLOW formulation and its sharp
composition law extend to standard Borel state spaces without a chosen
counting measure or atomic proposal density. State the flow
m(dx,dy)=q(dx)Q(x,dy), assume equivalence with its transpose on off-diagonal
proposal edges, and use r_q=dm^transpose/dm. With an antisymmetric
measurable distortion bounded by d, the target Hastings factor is
r_q W(y)/W(x). The desired theorem must handle singular/self transitions,
measurable path reversal, bad-set smoothing and all returns without
assuming a free density or evaluation oracle.

The finite lower is already contained in any class that permits atoms.
A meaningful non-atomic sharpness statement would additionally require a
native atomless realization with its actual proposal and target access;
it cannot be asserted by renaming a finite quotient. This is selected for
the representation-independent transport principle, not another numerical
prefactor. No claim for this continuation is made in the present theorem.
