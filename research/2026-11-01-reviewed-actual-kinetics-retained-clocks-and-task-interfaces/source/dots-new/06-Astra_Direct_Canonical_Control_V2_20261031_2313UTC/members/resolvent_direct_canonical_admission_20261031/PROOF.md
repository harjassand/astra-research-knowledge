# Directly acquired control geometry through an ordinary canonical LP

Separate post-freeze strengthening; no earlier receipt covers this file yet.
The earlier ordinary canonical-MDP comparator establishes the transformation.
Here it is used as the ADMISSION CERTIFICATE, replacing the conservative
source-derived inverse/objective-margin test. This is an ordinary hidden-K
method coupled to the actually received source-residual event, not a new generic
complementarity theorem or proprietary consumer unavailable to other learners.

## 1. Observation input and task scope remain unchanged

The completed forward-episode receiver provides rational Bhat_0=0,
Bhat_a 1=0 and a simultaneous event

 H=(1-gamma)(I-gamma A0)^-1 Z,
 max_a ||(A_a-A0)H-ZBhat_a||_(infinity->infinity) <= eta.

The probability, full-data receiving, partition acquisition/refinement, all
failed attempts, finite episode caps, fixed fresh sample counts, labels and
source preparation/sensing are paid exactly as before. We do not need h=mu H
or an estimate of h at all. Existing data may still contain hhat/delta_h; the
new consumer does not read or rely on their accuracy. One event supports every
later adaptive reward table g_a[j] in [0,1], constant on the acquired blocks.
The fully observed discounted source and pointwise microscopic/history comparator
are unchanged. No physical access, hidden-state inference or microscopic-reward
extension is implied.

Put t=gamma/(1-gamma) and A[:,(j,a)]=(e_j-t Bhat_a[j,:]^T). Acquire a rational
matrix X and positive scalar delta by the ordinary Morris canonical-form LP.
The receiver checks, for EVERY action column Y=XA,

 Y[i,(j,a)]<=0 for i!=j,
 delta<=sum_i Y[i,(j,a)]<=Y[j,(j,a)]<=1.                 (1)

These are finitely many exact inequalities on acquired coefficients, not a
supplied favorable norm or a promise about unknown source closure. Neither the
old kappa-q margin nor the old source-objective accuracy inequality is required.
A bad/nonpositive/backend proposal is UNKNOWN, never a proof of no structure.

## 2. Verified canonical geometry supplies a uniform value bound

The baseline columns of A are e_j. Hence X itself has nonpositive off-diagonal
entries and strictly positive column sums. It is nonsingular: X^T is a strictly
row-diagonally-dominant Z-matrix. Its inverse is nonnegative; e.g. normalize the
diagonal to write X^T=D(I-P), P>=0 with ||P||_infinity<1, and use the Neumann
series. In particular X_ jj>0 and X_ jj<=1.

The comparator's exact augmentation gives an (r+1)-state stochastic decision
model with discount beta=1-delta, original action rewards g_a[j], and dummy
reward zero. Its optimal (UNNORMALIZED) value obeys

                  0<=v_j<=1/delta,  v_dummy=0.

The unique original nominal solution is w=X^T v_original. Its baseline
constraints imply w_j>=g_0[j]>=0. Since the off-diagonal entries of X are
nonpositive,

  w_j=X_jj v_j + sum_(i!=j) X_ij v_i <= X_jj/delta.

Thus the cheaply computed constant

                C_X=max_j X_jj/delta

bounds ||w||_infinity for EVERY later allowed reward table, not merely the
currently tested goals. This is sharper than applying an arbitrary operator
norm to X^T, because it uses positivity of canonical values and the baseline
constraints. No source-derived lower singular bound for H is needed here.

Choose a nominal maximizing action in each block. The already proved source
Bellman-residual transport gives pointwise normalized policy regret at most

                 2 t eta ||w||_infinity <= 2 t eta C_X.             (2)

Therefore (1) plus 2t eta C_X<=epsilon_req is a uniform all-goal certificate.
The acquired X is data-dependent, but no new statistical union is needed: the
original event controls ALL action-effect rows, and the inequalities above are
deterministic consequences on that event. The witness is selected only from the
same retained Bhat; later goals can be fully adaptive.

## 3. Polynomial ordinary small-LP consumer, without source objective learning

One may plan in the canonical stochastic model, paying its actual iteration
cost and possibly poor discount. Alternatively construct the rational objective

                     h_c=(X^-1 1)^T>0.

For any representative selector M_pi=I-t Bhat_pi, Y_pi=X M_pi^T is a strictly
column-diagonally-dominant Z-matrix by (1). Thus

             h_c M_pi^-1 = 1^T (Y_pi^T)^-1 > 0.

The standard hidden-K grouped-dual/complementarity argument now makes

 min h_c w,   w_j>=g_a[j]+t[Bhat_a w]_j

a correct r-variable mr-constraint ordinary LP for every goal. The source
objective h is absent. Feasibility w=1, baseline w>=0 and positive h_c give
finite attainment. A checked primal/dual pair plus exact original residual
protects against solver failure. Generic rational LP supplies polynomial bit
complexity; executed SymPy simplex or exact policy iteration is NOT claimed
polynomial in the worst case. Canonical coefficient/witness bit lengths,
receiving, LP assembly/checks and deployment map/sensor work remain paid.

The canonical LP maximizes delta subject to bounds on ALL transformed action
diagonals, not merely on diag(X). Consequently maximizing delta need NOT minimize
C_X=maxdiag(X)/delta. An independent exact actual-source counterexample is
preserved in GAP_OBJECTIVE_CORRECTION.md and its executable test: two witnesses
have the same optimal delta=3/5 but C_X=5/3 and 4/3. The former optimization
equivalence claim was false and is withdrawn; all v1 bytes are retained.
Correctness here needs only a feasible positive witness. The prototype checks
feasibility, not optimality, and computes its actual C_X. It can refuse despite a
better witness existing. No optimality of this sufficient bound is claimed.

## 4. A noisy-family success calculation: old discount penalties are not intrinsic

This is an asymptotic algebra check on the EXISTING four-state counterexample,
not a newly invented workload or performance experiment. Let two native blocks
be {0,1},{2,3}, P=ZW, J=11^T/4, and S the existing permutation exchanging states
1 and 2. Keep the SOURCE fixed:

                  A0=.9 S+.1 J, A1=.9 S+.1 P.

Let the TASK discount gamma vary in [9/10,1). The exact resolvent action effect
has

       t B1=p [[1,-1],[-1,1]],
       p=gamma/[20(1-(81/100)gamma^2)],
       450/3439<=p<5/19.

Write the actually acquired t Bhat1=[[p1,-p1],[-q,q]]. Under exact closure, the
same endpoint event with total row L1 radius e gives
||Bhat1-B1||_infinity<=2e and eta<=6e. Consequently each of p1,q differs from p
by at most 2te (a deliberately loose entry bound).

If 2te<=1/50, then 0<=p1,q<=3/10. Construct from these OBSERVED coefficients

 X=[[1,-q/(1-q)],[-p1/(1-p1),1]].

For baseline columns, the sums are (1-2p1)/(1-p1) and (1-2q)/(1-q), both >=4/7.
For action 1, off-diagonal entries are zero and diagonal entries are
(1-p1-q)/(1-q) and (1-p1-q)/(1-p1), again in [4/7,1]. Thus delta=4/7 is a
verified witness, C_X=7/4. This formula uses no unknown exact p or good basis.
It provides a deterministic small witness if an LP backend is unhelpful.
Equation (2) is bounded by

                         21 t e.

For 0<epsilon_req<=21/100, choose e<=epsilon_req/(21t). Then 2te<=1/50 and
uniform regret<=epsilon_req. Thus a sufficient endpoint accuracy is
O(epsilon_req(1-gamma)), while the earlier conservative source-objective-margin
success schedule was O((1-gamma)^3) at fixed requested accuracy and rank.
This compares SUFFICIENT proofs, not necessary sample complexity or a separation
from a strong ordinary learner. The new ordinary witness is equally available
to ALP/SF/reset learners using the same moments.

### Entire finite-observation schedule, not just exact coefficients

For fixed n,m,r and failure budget zeta, use L=ceil(log2(2^r n m/zeta)). Fix N,
cap K and rounding bits b BEFORE the fresh batch. A sufficient choice is

 N >= 32 L/e^2,
 2^(-b) <= e/4,
 2 gamma^(K+1) <= e/2.

The upward-rounded statistical radius is <=e/2, and truncation bias <=e/2.
Exactly nmN episodes are paid, each at most K+1 source calls; expected source
calls are nmN[1+gamma(1-gamma^K)/(1-gamma)]. Coin bits, all microscopic labels,
full count receiving and native partition storage remain as in the accepted
interface. At fixed confidence/rank/accuracy this sufficient expected-call bound
is O((1-gamma)^-3), with the stated confidence/accuracy factors, rather than the
former conservative O((1-gamma)^-7). The capped worst-case bill has an additional
log(1/e) factor. These are not measured empirical bills or lower bounds.

The successful large arrays in prior tests remain fabricated unit fixtures.
The actual saved 4,096-episode batch still REFUSES the requested .01 regret under
this improved rule. This calculation does not turn it into a successful experiment.

## 5. Successive acquisition/refinement and hard limits

The prospective full-trace receiver uses unchanged C.receive_counts for every
fixed batch, then computes/checks its canonical witness and all-goal bound. A
failed acquisition may propose the same connected-component refinement as before;
a changed partition still requires a fresh endpoint batch with a paid failure
budget. The external native features, source/gamma/actions, schedules, confidence
and tolerance are bound. A successful stop must be the last supplied record;
later paid attempts cannot be silently omitted. No historical tag or batch is
invented. Physical iidness/nonanticipation remains an external premise.

No cheap successful acquisition is guaranteed for arbitrary sources. eta can be
large, witness delta can be tiny or nonexistent, rank can grow to n, and native
row preparation/sensing may not exist in an application. The work proves a
stronger verifiable success condition, not that a consequential favorable
workload has been identified. Ordinary goal-specific algorithms may be cheaper.

Primary algebraic prior, directly implemented: Morris, Theorem 2 and Section 3,
https://math.gmu.edu/~wmorris/cubemdpmprev4.pdf ; related hidden-K/Grid-LP/MDP
correspondence https://arxiv.org/pdf/1405.1827 . The new local join is the
source-error transport and uniform C_X bound with an acquired witness; historical
novelty of that join has not been established.
