# Ordinary canonical-MDP comparator (post-freeze, not yet independently reviewed)

This addendum strengthens the ordinary baseline, not an exclusive capability
claim. It does not amend the reviewed resolvent-control archive. Its input is
EXACTLY the already received small Bhat,hhat,eta,delta_h,gamma and partition hash;
it receives the same retained observations and source-event certificate.

## 1. Raw reset factorization is a real known-model alternative

Suppose exact known matrices satisfy A_a-A0=Z D_a W, with D0=0 and D_a 1=0.
Let Dmin[j,k]=min_a D_a[j,k], K=A0+Z Dmin W, R_a=D_a-Dmin.
For microscopic i in block j and l in block k,

 K[i,l]=min_a A_a[i,l]>=0.

Consequently K is substochastic, R_a>=0, and A_a=K+Z R_a W. Write
s=-Dmin 1, so R_a1=s independently of a and K1=1-Zs. This is a genuine common
background plus controlled reset decomposition. It is not fair to compare
against repeatedly solving all n-state tasks when these probabilities are known.

For completeness, a conventional embedded decision model can be constructed
for common state rewards f=(1-gamma)Zg. Assume first s_j>0; zero-reset blocks
have no control effect and can be eliminated or retained as nondecision states.
Let G_K=(I-gamma K)^-1, S=diag(s), and D=diag(1-Zs). A reset decision occurs in
block j with probability s_j; the reset destination law is R_a[j,:]W/s_j.
If u is the value at a reset decision and v the ordinary microscopic value,
conditioning on reset versus common-background continuation gives

 v=G_K[ZS u+D f],
 u_j=max_a { f_j + gamma [S^-1 R_a W v]_j }.

Here f_j denotes the common reward in block j. Therefore the r-state decision
operator has nonnegative coefficients

 T_a=gamma S^-1 R_a W G_K ZS,
 b_a=(1-gamma)g+gamma S^-1 R_a W G_K D f.

Because G_K Zs<=1 (apply the positive resolvent to Zs<=1-gamma K1),
T_a1<=gamma 1. Thus this is an ordinary discounted decision model, possibly
with a zero-value cemetery state. Precomputing the needed resolvent products
costs ambient work once, but every later g uses the retained small matrices.
This paragraph covers common state rewards; it is not an unproved claim that
arbitrary action-dependent rewards can be deferred to reset epochs.

The weak resolvent condition in the reviewed work is strictly broader: its
saved nullspace-perturbed example has (A_a-A0)H=ZB_a but NOT raw ZD_aW structure.
Also R=WH can be singular, so B_a does not generally permit recovery of D_a by
R inversion. Neither fact prevents the ordinary hidden-K route below.

### Only row samples do not give a free exact common-part sampler

Even two Bernoulli rows expose a standard Bernoulli-factory obstruction. Their
pointwise-minimum common mass is 1-|p-q|; exposing an exact reset event would
produce a Bernoulli(|p-q|) output from independent unknown p- and q-coins.
There is no such almost-surely finite algorithm valid for every p,q in (0,1).
If output 1 has positive probability at p!=q, some finite-time output-1 event has
positive probability. Every finite transcript has a strictly positive likelihood
ratio at an interior diagonal p=q, including adaptive choice of input coin and
independent internal randomness. Thus the same event has positive probability
at p=q, contradicting the required zero. This is the familiar interior-zero
Bernoulli-factory obstruction, not a new general classical-computation lower
bound. A parameter/probability oracle, supplied coupling, separated parameter
promise, approximate sampling or confidence-qualified lower common part changes
the question. Strong approximate reset learners must receive the same metadata
and may be cheaper on their applicable class.

Primary context: Dughmi et al., *Bernoulli Factories and Black-Box Reductions*,
Section 2.2, gives the ordinary oracle formulation and credits Keane--O'Brien.
The finite-transcript argument above is included rather than relying on an
unstated sampling primitive.
https://www.cs.cornell.edu/~rdk/papers/stoc17-rad.pdf

## 2. The SAME acquired signed coefficients admit an ordinary canonical MDP

Use t=gamma/(1-gamma). Form the horizontal r by mr matrix A with column (j,a)

                       A[:,(j,a)]=(e_j-t Bhat_a[j,:]^T).

Representative submatrices are M_pi^T. The reviewed acquired margins imply
all randomized M_pi nonsingular, and hhat M_pi^-1 strictly positive. Continuity
along the baseline-to-policy segment gives positive representative determinants.
Hence this is exactly the hidden-K / positive-basis setting, not a new generic
complementarity solver.

**Direct primary match:** Morris, *Efficient Computation of a Canonical Form for
a Matrix with the generalized P-property*, Theorem 2 and Section 3, gives the
positive representative-basis criterion, the following LP(A), and the one-extra-
state discounted-MDP construction. Klaus gives the broader Grid-LP/hidden-K/MDP
correspondence. We implement that ordinary construction, not relabel it.
https://math.gmu.edu/~wmorris/cubemdpmprev4.pdf
https://arxiv.org/pdf/1405.1827

Once per retained coefficient family, solve the ordinary rational LP

 maximize delta over X in R^(r by r), delta in [0,1],
 (XA)[i,(j,a)] <= 1  if i=j,
 (XA)[i,(j,a)] <= 0  if i!=j,
 1^T(XA)[:,(j,a)] >= delta.

The established hidden-K theorem guarantees a positive feasible delta. This
has r^2+1 variables and mr(r+1)+2 inequalities. A verified positive feasible
candidate suffices; numerical optimality is unnecessary for correctness.
Since baseline columns are e_j, every feasible X with delta>=0 has entries in
[-1,1]. The executable translates X=U-1 to nonnegative LP variables. It verifies
all original rational inequalities and nonsingularity afterwards. The diagonal
of each column Y=XA is positive, its off-diagonal entries are nonpositive, and
its sum s_ja obeys 0<delta<=s_ja<=Y[j,(j,a)]<=1.

Append a cemetery coordinate. For each original column put

 Q[:,(j,a)] = (Y[:,(j,a)], delta-s_ja),
 Q[:,dummy] = delta e_dummy.

Then every Q column sums to delta, has off-diagonal entries <=0 and diagonal
<=1. Set beta=1-delta. If beta>0, P[:,(j,a)]=(e_j-Q[:,(j,a)])/beta is a stochastic
column; transpose to the usual row transition convention. If beta=0, Q columns
are e_j and the decision is immediate reward maximization.

For ANY later action-dependent reward table g_a[j], give the canonical MDP those
rewards and zero dummy reward. Its ordinary discounted Bellman solution v has
v_dummy=0. Define w=X^T v_original. Then, exactly,

 Q[:,(j,a)]^T v=(e_j-t Bhat_a[j,:]^T)^T w.

Thus the canonical Bellman inequalities and their active actions are precisely
w_j>=g_a[j]+t[Bhat_a w]_j. Any optimal canonical action table is nominal-greedy
for the SAME w. The reviewed posterior bound 2(rho+t eta ||w||_infinity) therefore
certifies its true-source regret on the SAME learned event. No extra statistical
union, no full H, no raw D_a or R inverse, and no new source call is used.

This gives an ordinary positive stochastic COMPUTATIONAL DECISION MODEL. Its
transition matrix is not the law of the observed source blocks, its value v is
not the source's microscopic value, and its discount beta need not equal gamma.
Only the active-policy/nominal-constraint correspondence is asserted. Actual
source control still needs the retained n-label map and sensor interface.

## 3. Costs and failure receiving

Compile cost: one (r^2+1)-variable rational LP, O(mr^3) naive matrix arithmetic,
O(mr^2) retained stochastic coefficients plus X, and their full bit lengths.
Generic rational LP has polynomial bit complexity. Executed SymPy simplex does
not have an asserted polynomial worst-case guarantee. A failed proposal is
UNKNOWN, not proof that no canonical model exists. A small canonical gap may
make ordinary value/policy iteration expensive; no favorable discount is assumed.
The prototype uses exact policy iteration, reports evaluations and checks the
resulting Bellman equations. Its actual iterations, inversions and coefficient
bit growth are paid; no strongly polynomial claim follows from small dimension.
Primary r-variable LP remains available if compilation/iteration is unattractive.

The first free-variable SymPy formulation returned X=0,delta=0 as an allegedly
optimal proposal on an instance with an explicit positive witness. This was
caught/refused, not accepted as a no-structure conclusion. The standard bounded
translation avoids that observed backend defect. Its original source is
preserved in history; the corrected compiler still independently checks output.
This echoes the whole review's caught full-state LP error and underscores why
solver statuses are not scientific certificates.

No practical many-task speedup or historical novelty is inferred from this
comparator. Ordinary ALP/SF/hidden-K methods can adopt the acquired certificate
and obtain exactly the same useful decision model. The actual open contribution
question remains acquisition of a stable economical control-relevant interface
on important source families after all failed search and observation work—not
exclusive ownership of the downstream planner.
