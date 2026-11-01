# Acquired baseline action-effect closure for reusable optimal control

New work, NOT independently reviewed. Ordinary successor features, policy
improvement, linear programming and Bellman residual bounds are components.
The question is whether their particular acquisition/constraint-compression
join earns useful repeated planning without predictive aggregation. No novelty
or consequential empirical advantage is asserted.

## 1. Task and actual observation interface

There are n named states, m finite actions including baseline action 0, and
unknown stochastic row matrices A_a. A forward call at a chosen (i,a) returns
one iid next-state label; every choice and outcome is available for retention.
The baseline can be run from the resulting label. No reverse access, common
noise coupling, optimal policy, latent basis or transition probabilities are
input to the statistical learner. Fix a rational 0<gamma<1.

The task family starts from explicit native reward features psi_i. The learner
reads these features and initially groups equal rows; this is a task-description
operation, not an assumption that the resulting partition predicts dynamics.
Later tasks assign rewards in [0,1], constant on the FINAL acquired partition.
In particular all admitted bounded linear combinations of the native features
remain representable. If native feature rows are all distinct, this opening
already has n classes; there is no claimed dimensionality reduction.

Let an acquired partition have r nonempty blocks, indicator matrix Z, uniform
block averaging W, WZ=I. No balance assumption is needed. Define for ANALYSIS

 H=(1-gamma)(I-gamma A0)^(-1)Z,   C_a=(A_a-A0)H,
 R=WH,   u=(1/r)1^T,   mu=uW,   h=mu H=uR.

H is a nonnegative row-stochastic n-by-r matrix of full column rank, and h is
a probability row vector. R need NOT be invertible. The learner will acquire
only low-dimensional endpoint statistics needed below, not query H or invert R.
A stationary output table chooses one action per acquired block. Implementation
requires the retained n-label partition map and a current microscopic-label
sensor/simulator interface each step; it is not hidden-state inference.

Use normalized value V^pi=(1-gamma)E sum_t gamma^t reward(X_t), so 0<=V^pi<=1.
The normalized Bellman operator is T(V)=(1-gamma)Zg+gamma max_a A_a V.
It is a gamma-contraction in sup norm on the ORIGINAL n-state process.

## 2. Exact action-effect closure, not predictive closure

The exact success condition for this partition is

             C_a=Z B_a for every a.                         (C)

Here B0=0 and B_a 1=0. (C) does not say A_a Z is block constant, nor that the
block process is Markov. In particular the common passive dynamics may fail
predictive aggregation badly. Raw factorization A_a-A0=Z D_a W implies (C),
but is stronger; arbitrary row perturbations annihilating H leave (C) intact.

A nontrivial existence join is necessary: (C) alone does not make T map range(H)
into itself. For a BLOCK policy pi, let B_pi select one row from B_a per block.
Then

 (I-gamma A_pi)H = (1-gamma) Z [I-t B_pi],
             t=gamma/(1-gamma).

I-t B_pi is invertible: otherwise Hx is a nonzero null vector of the invertible
I-gamma A_pi. Therefore the policy value lies in range(H), specifically
V^pi=H [I-t B_pi]^(-1)g. Starting with baseline pi=0, ordinary exact policy
improvement chooses actions by B_a w and so remains blockwise. At every strict
improvement at least one state value increases, and a finite discounted MDP
has finitely many deterministic policies; retaining old actions on ties gives
finite termination at an optimal policy. This is an EXISTENCE proof, not a
proposal to enumerate m^r policies as the downstream algorithm.

Consequently V*=H(g+y*) with

 y*_j=t max_a [B_a(g+y*)]_j,     0<=y*<=t 1.             (1)

The last bounds use baseline action 0 and the fact that V* is in [0,1]:
B_a(g+y*)=(A_a-A0)V* is between -1 and 1.

Solve instead the r-variable, mr-constraint ordinary linear program

 minimize h y,
 y_j >= t [B_a(g+y)]_j   for every j,a.                 (2)

Every feasible y gives V=H(g+y)>=T(V), hence V>=V*. The true y* is feasible.
Since mu has full microscopic support, equality in mu V>=mu V* forces V=V*;
H has full column rank, so the minimizing y is y*. No componentwise-minimal-y
claim or arbitrary-positive-objective substitution is used. Coefficients are
signed; the reduced fixed-point iteration need not contract. The efficient
consumer is the polynomial-size rational LP, not an assumed dynamics model.

## 3. A universal candidate receiver under approximate observations

Suppose rational Bhat_a are row-zero-sum with Bhat_0=0 and an acquired event gives

 eta >= max_(a,i in j) || C_a[i,:]-Bhat_a[j,:] ||_1.     (3)

For ANY task g in [0,1]^r and rational candidate y, put w=g+y and

 rho=max_j | y_j-t max_a [Bhat_a w]_j |.

Choose the nominal greedy action in each block, with deterministic tie rule.
For both the actual Bellman residual and the residual of this chosen policy,

 ||H w-T(H w)||_infinity,
 ||H w-T_pi(H w)||_infinity
       <= (1-gamma)rho + gamma eta ||w||_infinity.

The two original-process contraction bounds give the complete pointwise regret

        0<=V*-V^pi <= 2[rho+t eta ||w||_infinity] 1.     (4)

This does NOT assume (C), LP optimality, R invertibility, a reduced contraction,
or accuracy of an objective vector. An arbitrary heuristic candidate is safe
only when its externally requested tolerance passes (4). Failure means UNKNOWN,
not a false model certificate. Since (3) is uniform in w, the same event supports
arbitrarily many adaptively chosen admitted tasks/candidates with no new union
bound. It does not support a new gamma, action set, partition, or reward language.

## 4. A feasible/stable finite-data consumer, not only refusal

A small noisy LP can be inconsistent with any process. The following robust
bounded LP both protects acceptance and proves eventual success on class (C).
Suppose also ||hhat-h||_1<=delta_h, hhat>=0, hhat 1=1. Set

 q=t eta; require q<1;    M0=1/(1-gamma),
 c=2 q M0/(1-q),   Y=t+c,   M=1+Y=M0+c,   s=q M.

For a task g in [0,1]^r solve

 minimize hhat y,
 0<=y<=Y 1,
 y_j >= t[Bhat_a(g+y)]_j+s    for all j,a.              (5)

If a solver fails or cannot supply a checked candidate, return UNKNOWN.
If true closure (C) holds and (3) holds, y*+c1 is feasible: Bhat_a 1=0, and
its constraint gap is at least c-t eta M0=s. It lies in the declared box.
Every feasible candidate has ||w||<=M and is a TRUE Bellman supersolution,
since its robust slack s covers t eta M. Thus V=Hw>=V*.

Let y minimize (5). Comparing to y*+c1 and using the objective error gives

 Delta:=mu(V-V*)=h(y-y*) <= c+delta_h Y.                (6)

Indeed hhat(y-y*)<=c and ||y-y*||_infinity<=Y. This uses the acquired h, not
an unearned arbitrary positive objective. Now define qnom_j=y_j-t max_a Bhat_a w,
so qnom>=s>=0. The actual normalized residual is
qtrue_i=(V_i-T(V)_i)/(1-gamma), and |qtrue_i-qnom_j|<=s.
Since V>=V*, monotonicity gives 0<=V-T(V)<=V-V*. Hence

 (1/r)sum_j qnom_j <= Delta/(1-gamma)+s,
 rho=max_j qnom_j <= r[(c+delta_h Y)/(1-gamma)+s].       (7)

The measured receiver (4) therefore has the a priori success bound

 regret <= 2r(c+delta_h Y)/(1-gamma)+2(r+1)s.            (8)

The loss is r, not the ambient n or an inverse microscopic occupancy. It comes
from block-constant nominal residuals and the artificial full-support objective
mu=uW. R can be singular. This is a sufficient polynomial success schedule,
not a sharp sample bound. Approximate optimality gap zeta in (5) adds zeta to
the right side of (6), and correspondingly 2r zeta/(1-gamma) to (8).
The posterior measured (4) remains valid even if class (C) is false.

## 5. Direct endpoint acquisition, finite stopping and confidence

Fix the proposed partition BEFORE a fresh batch. For each (i,a), execute N iid
episodes: one A_a step, then baseline steps until an independent geometric
stopping time T with P(T=t)=(1-gamma)gamma^t, capped at K. Record the final
microscopic label and its acquired block. All chosen source rows, intermediate
labels and action metadata remain available to strong retaining competitors;
keeping extra metadata costs memory/time, not extra forward observations.

Without capping, the endpoint block law is P_a=A_a H. With capping, coupling
on T<=K gives per-row L1 bias <=2 gamma^(K+1). Each episode uses at most K+1
actual source calls, with mean 1+gamma(1-gamma^K)/(1-gamma). Random stopping
coins, labels, mapping and count increments are execution costs, not a free
geometric-resolvent oracle. Rational gamma permits exact Bernoulli coins using
integer rejection sampling; its random-bit/rejection cost must also be paid.

Let Phat_a[i,:] be the empirical endpoint block law. For a fixed design and
fresh iid outcomes, a union over all subsets of r categories and nm rows gives
simultaneously, with failure<=delta,

 ||Phat_a[i,:]-P_a[i,:]||_1 <= epsilon,
 epsilon=sqrt_up(2 L/N)+2 gamma^(K+1),
 L>=ln(2^r n m/delta).                                 (9)

The subset union uses one-sided Hoeffding; complements include the other sign.
A paid rational upper bound ceil(log2(2^r nm/delta)) is sufficient. Store a
common dyadic outward square root and all count denominators explicitly.

Define Ehat_a=Phat_a-Phat_0, Ehat_0=0, Bhat_a=W Ehat_a, and

 eta_hat=max_(a,i in j)||Ehat_a[i,:]-Bhat_a[j,:]||_1,
 eta=eta_hat+2 epsilon,
 hhat=(1-gamma)u+gamma u W Phat_0,
 delta_h=gamma epsilon.                                (10)

Then (3) and the h-event hold on (9), even though all statistics share data.
There is no independence assumption between estimated coefficients and error
bounds. Under exact closure, eta_hat<=4 epsilon and eta<=6 epsilon. Thus (8)
tends to zero with a polynomial sufficient sample budget as epsilon decreases.
No full n-by-n transition matrix or n-by-r exact H is learned or retained.
The final count receiver reads O(nmr) counters. The reusable small matrices have
O(mr^2) rational entries, plus the n-state partition map and the proof/data
retention needed for independent receiving. Future core planning is independent
of n after that receiving; full re-audit of all observations is NOT free.

For successive attempts use externally fixed budgets delta_j with sum<=delta_total,
freeze each design before its batch, and retain ALL source calls, failures,
rounding and solver attempts. Adaptive outcome-dependent stopping at N is not
justified by this fixed-N concentration inequality. Count arrays alone do not
authenticate iid sampling, freshness, source identity or the stopping protocol.

## 6. Acquiring a useful partition instead of receiving good coordinates

For an EXACT-input structural theorem, start with the partition of equal native
reward-feature rows. At current partition Z_t, compute H_t and all C_a^t for
analysis/ordinary exact algebra. Refine each block by equality of the entire
row tuple (C_a^t[i,:])_a. Stop if there is no split. At most n-r0 strict rounds
occur, and the final partition satisfies (C). Baseline-only resolvent queries,
not optimal-control oracles, construct the row tuples.

If any stable target partition Z_* refines the native reward partition, then
no exact round can split a target block. Indeed while Z_t=Z_*L, H_t=H_*L and
C_a^t=Z_* B_a^* L, constant on each target block. Thus the final rank is <=r_*.
The same argument establishes monotonicity of the refinement operation and
that iteration finds the coarsest exact stable refinement of the starting
partition. The target partition is a SUCCESS property, never input advice.

For finite observations, in each current block join two states when their
empirical effect-row tuples differ by at most 4 epsilon in maximum-action L1
norm, and split into connected components. On (9), states from the same stable
target block are a clique, so components cannot split them, even if different
target groups are joined by noisy chains. Use a fresh batch after every proposed
partition change: relabeling old endpoints adaptively is not silently treated
as fresh evidence. If every distinct exact tuple at a round has separation
>8 epsilon, the components equal the exact-refinement classes. Without that
gap, no exact recovery claim is made; decrease resolution with a paid confidence
schedule, or accept only the posterior residual certificate at the current
partition. Chain merging may increase eta_hat and cause a legitimate refusal.

For a finite exact class the finitely many exact refinement rounds have a
positive minimum nonzero separation unless no split is needed. Sufficiently
small epsilon reproduces that route. This is an output-sensitive SUCCESS
statement with a potentially tiny separation and high bill, not a cheap universal
partition oracle. A single round can require all nm source preparations; rare
unqueried rows cannot be certified away under a pointwise optimality guarantee.

## 7. Finite-bit planning, execution and strongest baselines

All actual LP coefficients from counts, outward radii and rational gamma/g are
rational. Forming (5) costs O(mr^2) arithmetic; its size and bit length are
explicit. Ordinary polynomial-time rational LP algorithms supply a polynomial
bit-complexity downstream consumer. This is an established algorithmic component,
not a supplied optimal teacher. A practical simplex/floating implementation
has its actual attempts charged and must produce a checked rational candidate;
no polynomial worst-case runtime is asserted for simplex. The posterior check
(4) is O(mr^2), and can safely accept a nonoptimal candidate if its bound passes.
An exact primal/dual certificate additionally earns the success theorem for (5).

Storage includes n ceil(log2 r) partition bits, mr^2 coefficient numerators and
common denominators, hhat, confidence/radius strings, all retained count evidence,
and any optional source metadata. A later task reads its reward coefficients,
constructs g, solves/checks the LP and emits r action labels. Deployment observes
and maps the current state at every step. For a finite implementation of the
normalized discounted objective, a truncation after J steps loses at most
gamma^J in [0,1] rewards and pays all J transitions/sensor/map operations.

Strong ordinary ALP with the same implicit successor basis has nm constraints;
condition (3) certifies their replacement by mr robust constraints. Conventional
ALP/constraint aggregation can adopt this certificate and then has the SAME
consumer. Ordinary successor features, generalized policy improvement, successor
feature sets, value-equivalence learning, reward-free exploration and on-demand
policy evaluation receive identical endpoints, task labels, failed attempts and
retained work. The question is whether this particular acquisition and robust
constraint-compression ingredient is already supplied by prior theory, and
whether real repeated-task workloads amortize its bill. No exclusive advantage
can be inferred by withholding the learned ingredient from a comparator.

## 8. Informative limitations to test exactly

- R can be singular although H is full column rank; no division by R is legal.
- The baseline may have severe predictive aggregation error while (C) holds.
- (C) can hold when raw action differences do not factor through the partition.
- Signed reduced fixed-point iteration may fail contraction; use/check the LP.
- Incorrect objective coefficients can spoil the exact-LP optimality argument;
  (4) protects acceptance, and (5)--(8) pay acquired objective errors.
- Arbitrary perturbations remove exact closure; (3),(4) remain valid but may fail
  to certify useful regret. No empirical count dataset proves exact equalities.
- Gamma near one can make the sufficient horizon/sample bill prohibitive.
- Initial task labels, refinement rank and separation can be unhelpful. Exact
  refinement may end at n and solve no reusable compression problem.
- Pointwise control scope costs all rows. A one-goal/on-demand policy evaluation
  can be much cheaper; retained policy portfolios must remain strong baselines.

## 9. One explicit sufficient finite observation schedule

For exact closure, eta<=6 epsilon. If epsilon<=1/(12t), then q<=1/2,
c<=24 gamma epsilon/(1-gamma)^2, M<=3/(1-gamma), and
s<=18 gamma epsilon/(1-gamma)^2. Also delta_h Y<=3 gamma epsilon/(1-gamma).
Consequently (8) is at most

                   126 r gamma epsilon/(1-gamma)^3.    (11)

For desired normalized regret e_req>0, it is sufficient to choose

 epsilon_target <= min{1/(12t), e_req(1-gamma)^3/(126r gamma)}.

Choose cap K with 2 gamma^(K+1)<=epsilon_target/2, root bits b with
2^-b<=epsilon_target/4, and N>=32 L/epsilon_target^2. Then the unrounded
statistical root is <=epsilon_target/4, its outward rounding adds at most
another epsilon_target/4, and (9) has epsilon<=epsilon_target. This is a
finite, explicit, conservative schedule, not an empirical result or a lower
bound. Expected source calls are at most nmN/(1-gamma), worst-case calls
nmN(K+1), plus all partition discovery/refinement attempts and audits. A small
nonzero true closure defect adds to eta and may prevent the target guarantee.
The high inverse-discount exponent may make this schedule unattractive; no
constant tuning or another tiny benchmark is offered as a consequence claim.
