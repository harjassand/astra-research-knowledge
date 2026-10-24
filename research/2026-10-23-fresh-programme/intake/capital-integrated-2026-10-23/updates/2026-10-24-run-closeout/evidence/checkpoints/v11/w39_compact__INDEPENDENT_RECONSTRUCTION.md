# Independent full-data proof reconstruction

W39, 24 October 2026. Exact lower source45421a5832a0453574a2251c9bb9c3c6c5ef6c7e7ae7e493236d69343aeaab2c
and two-round source2220c100071a2f0009d9b671564dffd0a1d13b11a48ff9642014a9bb8f51e17e.
No W73 producer replay, output, report/result, earlier Gaussian proof,
peer verdict or root development argument was read. The independently
derived pre-diagnostic argument is retained separately at SHA37f7fc19....
All subsequent finite controls use new code with no producer/peer imports.

## 1. Precisely which experiment is proved hard

Fix even n>=4, a,sigma>0, q>=1 and a finite nominal row budget B>=0.
A full action returns n Gaussian-noisy coordinates of Lx. Under a
nonadaptive design, write s_i=(x_1i,...,x_qi), with ||s_i||^2<=B for
EVERY realized design. Designs, including all their real coordinates,
are chosen independently of the unknown graph/weights. Decoder
randomization and unlimited computation are allowed. The observation
includes the entire nq-dimensional action transcript, not only two
selected vertices. Noise is independent N(0,sigma^2) at every acquired
coordinate/action and independent of graph and design.

Before design randomization, sample ordered hubs U,V uniformly and a
uniform balanced partition A,C of the n-2 remaining vertices. Independently
sample n-2 weights with the stated cos-squared density. Under hypothesis0
the graph is two stars; hypothesis1 adds a hub edge of exact weight a.
Both are forests, all nonzero weights lie in [a,3a], and connectivity
is exactly the hypothesis. This same metadata M may be revealed AFTER
the design is irrevocably committed. Its law is common to both hypotheses.
The proof does not reveal metadata before design or choose a graph after
seeing the random design.

The strengthened side-information statement means exactly that common
M from this experiment. It does not grant arbitrary answer-encoding
metadata. A guarantee with side information must hold for every admissible
fixed graph/metadata description (or its stipulated common metadata law).
Without side information the lower bound applies directly, and the
metadata convention cannot affect it.

## 2. Endpoint score regularity, including its unbounded score

Set w=a(2+u), u in[-1,1]. The probability element is
cos^2(pi u/2)du. Its integral is1; its density on the real line, extended
by zero, is C1. At each endpoint p=O(distance^2), p'=O(distance), so
boundary terms vanish. On the open interval its score is

    rho(w)=-(pi/a)tan(pi u/2).

The score is unbounded but is square integrable under p. Indeed

    E rho=integral p'=0,
    J=E rho^2=(pi^2/a^2)integral_-1^1 sin^2(pi u/2)du
             =pi^2/a^2.

The endpoints themselves have probability zero; no score value there
is required. Neither a bounded score nor a twice continuously
differentiable zero extension is needed for the IBP below.

An optional consistency observation: among densities on an interval of
length2a with sqrt(p) in H_0^1, J=4 integral|(sqrt p)'|^2>=pi^2/a^2 by
the first Dirichlet eigenvalue. The cos-squared density attains equality.
This is the standard one-dimensional Poincare calculation, not a claim
that the overall graph lower-bound constants or prior are minimax optimal.

## 3. Full-data conditional scores without Gaussian-conjugacy assumptions

Fix a real D-by-m matrix H and independent W coordinates with this prior.
Let Z be independent N(0,sigma^2 I_D), Y=HW+Z and f its density.
The Gaussian convolution has a smooth positive density even when H is
rectangular, rank deficient, or zero. For every compact smooth test g,

    E[g(Y)rho_j(W_j)]
       =-E[H_j^T grad g(Y)]
       =E[g(Y)H_j^T grad log f(Y)].

The first identity is ordinary compact-support IBP; boundary p=0 is
load bearing. Gaussian IBP similarly gives
E[g(Y)rho_Z(Z)]=E[g(Y)grad log f(Y)]. Consequently in the weak and
conditional L2 sense,

    E[rho_W(W)|Y]=H^T grad log f(Y),
    E[rho_Z(Z)|Y]=grad log f(Y).

The Gaussian score alone bounds directional Fisher by ||v||^2/sigma^2,
so all needed L2 objects are finite. Scores of different W coordinates
and Z are independent, centered, with variances J and sigma^-2.
For H alpha+beta=v, conditional Jensen gives

    I_Y(v)<=J||alpha||^2+sigma^-2||beta||^2.                (R1)

Define C=sigma^2 I+J^-1HH^T, positive definite regardless of rank H.
The minimizing pair can be verified directly, rather than inferred
from an assumed covariance:

    alpha*=J^-1 H^T C^-1v, beta*=sigma^2 C^-1v.

Their constraint is exact. Their objective equals
v^T C^-1(sigma^2 I+J^-1HH^T)C^-1v=v^T C^-1v. Strict convexity of the
alpha objective, whose Hessian is positive JI+sigma^-2H^TH, proves the
minimum. Thus R1 implies

    I_Y(v)<=v^T C^-1v.                                   (R2)

C is only a score-comparison matrix. In general Var(W) is not J^-1 I,
and the actual conditional variance Var(W|Y=y) depends on y. Neither
the actual non-Gaussian posterior nor its covariance was identified
with C or a Gaussian Schur complement. This distinction is sufficient
to remove the apparent conjugate-posterior risk in the argument.

The Fisher-convolution/score-projection method is classical. I directly
read [Dembo--Cover--Thomas, Section III-C, Theorem13 and the matrix-version
pointer](https://isl.stanford.edu/~cover/papers/transIT/1501demb.pdf).
That primary theorem supplies provenance for the general method; it
does not by itself state this exact rectangular-H or forest conclusion.
R1--R2 above are the independent proof of that specific application.

## 4. Full observation geometry and its exact comparison Schur blocks

Condition on a supported design and M. For a leaf l at hub h, let
r_l=s_l-s_h. The column of H for its weight is r_l at vertex l,
-r_l at h, and zero at every other vertex. With vertex-major ordering,
H is nq by n-2, and the complete observation at hub-edge weight t is

    Y(t)=HW+Z+t v,
    v=(e_U-e_V) tensor(s_U-s_V).                          (R3)

The independent leaf prior gives HH^T as a SUM of these edge-column
outer products. Distinct leaf blocks have no cross block. Each leaf
diagonal block of C is sigma^2 I+c r_l r_l^T, c=J^-1. Its cross block
with its hub is -c r_l r_l^T. The full hub diagonal is
sigma^2 I+c sum r_l r_l^T. Rank-one inversion gives

    c-c^2 r_l^T(sigma^2 I+c r_l r_l^T)^-1r_l
       =1/(J+||r_l||^2/sigma^2)=b_l.

Eliminating every observed leaf leaves two uncoupled blocks

    S_U=sigma^2 I+sum_A b_l r_l r_l^T,
    S_V=sigma^2 I+sum_C b_l r_l r_l^T.

Since v has zero leaf coordinates, the block inverse identity EXACTLY
gives, for r=s_U-s_V,

    v^T C^-1v=r^T(S_U^-1+S_V^-1)r.                       (R4)

Every leaf readout was retained in C and was eliminated algebraically
only AFTER establishing a full-data Fisher bound. The formula is not
a lower-data Fisher bound in disguise, and no independence of the
actual posterior leaf variables is assumed.

## 5. The hidden-label average and exact row-budget constants

Every supported design has ||s_i-s_h||^2<=4B, by the triangle or squared
two-vector inequality. Thus

    b_l>=b*=(J+4B/sigma^2)^-1,
    S_U>=b*[lambda I+sum_A r_l r_l^T],
    lambda=sigma^2/b*=sigma^2 J+4B.

For fixed arbitrary vectors r_i of squared norm <=R^2, use the exact
sampling equivalence: choose j uniformly and a d-subset A excluding j,
or choose a uniform(d+1)-set T followed by uniform j in T. For
G=lambda I+sum_T r_i r_i^T, put h_j=r_j^T G^-1r_j and
t_j=r_j^T(G-r_jr_j^T)^-1r_j. Then

    0<=h_j<1,
    t_j=h_j/(1-h_j)=h_j(1+t_j),
    t_j<=R^2/lambda,
    sum_T h_j=tr(I-lambda G^-1)<=q.

Hence the average t is <=(1+R^2/lambda)q/(d+1). It requires neither
generic position nor full rank of the r_i. The multiplicative factor
cannot simply be removed; the exact negative control with two scalar
vectors r_1=r_2=1 and lambda=1/100 has t=100/101>1/2.

Conditional on U, set r_i=s_i-s_U for the n-1 other labels. The actual
sampling chooses V uniformly, then a uniform d-subset A excluding V,
exactly the preceding law. With d+1=n/2 and R^2=4B,

    E[r^T S_U^-1r]
       <=b*^-1(1+4B/lambda)q/(d+1)
       =(J+8B/sigma^2)2q/n.

The symmetric V expression has the same bound. R2--R4 therefore imply

    E_M I_{Y|design,M}(v_M)<=(4q/n)(J+8B/sigma^2).          (R5)

The design seed is independent of this prior. Averaging over that seed
preserves R5, without choosing favorable labels after seeing a design.
A metadata distribution dependent on the realized design would be a
different experiment; it is not used.

## 6. Fisher path to TV: no finite-shift KL claim

For each fixed design,M, let f_t(y)=f_0(y-tv), t in[0,a]. Its Fisher in
direction v is invariant under translation. FTC and Tonelli imply

    (1/2)||f_a-f_0||_1
       <=(1/2)integral_0^a ||partial_t f_t||_1 dt
       <=a sqrt(I_Y(v))/2.                               (R6)

The derivative has integrable L1 norm by Cauchy--Schwarz and finite
Fisher. Compact prior support plus Gaussian convolution permits the
needed differentiation and domination. No inequality of the form
D(f_a||f_0)<=a^2 I_Y(v)/2 is invoked. A bound valid only infinitesimally
would not by itself justify such a KL statement.

The joint transcript includes common design and metadata. TV for these
joint laws is the average conditional TV; Jensen and R5 give

    TV(P1,P0)<=sqrt[(q/n)(a^2J+8a^2B/sigma^2)]
             =sqrt[(q/n)(pi^2+8a^2B/sigma^2)].             (R7)

Only t=0 and t=a enter the testing guarantee. The intermediate edge
weights are an analytic LOCATION PATH, and may violate the promise
that a present edge is at least a. That does not affect R6: it never
assumes that the algorithm succeeds at an intermediate t.

A test having risk <=delta at every fixed promised input has Bayes
equal-prior risk <=delta under the two endpoint priors. Optimal Bayes
risk is (1-TV)/2; random postprocessing cannot improve it. Thus
TV>=1-2delta. Combining with R7 proves exactly

    q[pi^2+8a^2B/sigma^2]>=n(1-2delta)^2.                  (R8)

Violation produces a fixed hard promised input, since the prior is
sampled independently before the algorithm's randomness. Support recovery
implies connectivity and inherits R8. q=0, noiseless sigma=0, or designs
depending on responses lie outside this stated proof. B=0 is allowed;
R8 is a weak necessary condition there, not a claim of achievability.

## 7. Separate reconstruction of the two-round upper

The second source assumes only the two-hidden-star family, optional hub
edge exactly a, arbitrary fixed leaf weights in[a,3a], delta in(0,1/2),
and its explicit three finite conditions(A). No hub/leaf metadata is
given to its adaptive learner.

For action1 x_i=b_i/2, independent fair b_i, every term at a positive
Laplacian row has the same sign as every other nonzero term at that
row. The optional hub edge therefore cannot cancel its leaf currents.
Conditional on a hub's own bit, the number of opposite leaves is
Binomial(d,1/2). With probability at least1-exp(-d/8) that number is
>=d/4, giving hub signal>=ad/8. Every leaf signal is <=3a/2.

With t=sigma sqrt(2ln(8n/delta)), all n first-action sensor errors are
bounded by t except with probability <=delta/4. The two binomial failures
sum to <=2exp(-d/8)<=delta/4. The strict condition
d>12+16t/a ensures the two hub observations outrank all leaves in
absolute value. Thus the ACTUALLY acquired hub set is correct with
probability >=1-delta/2; it is not supplied by a degree or topology oracle.

In action2, set one selected hub U to1/2 and every other vertex to0.
If the hub selection was correct, all leaf neighbors of the other hub
V have the same zero input as V. Its exact noiseless response is0 or
-a/2. Thresholding its fresh independent Gaussian readout at-a/4 has
error <=exp[-a^2/(32sigma^2)]<=delta/2. Conditional on the first-action
event the same bound holds; there is no selection bias in the new noise.
The total worst-case error is <=delta for every fixed graph/weight input.

The pathwise row budget is <=1/4 in action1 plus <=1/4 at at most one
selected vertex in action2, so B<=1/2 even on WRONG selection paths.
There are exactly2 complete actions and2n acquired scalar readings,
n initial fair bits, two preparations, and O(n) real arithmetic/selection.
This proves connectivity, not all leaf memberships/weights or general
forest support.

## 8. The correctly matched new combination

For fixed delta in(0,1/2), choose a fixed ratio r=sigma/a>0 satisfying
r<=1/sqrt(32ln(2/delta)). The other two finite conditions hold for all
sufficiently large even n. Comparing at the SAME B=1/2, R8 gives

    q_nonadaptive>=n(1-2delta)^2/(pi^2+4/r^2),
    q_adaptive=2.

Thus this specialized positive-star connectivity model has linear-in-n
versus constant full-action counts at fixed small scalar noise and
matched nominal row energy. It is equivalently an Omega(n^2) versus2n
scalar-acquisition comparison. The lower remains true even if its decoder
is given the common hub/partition metadata after commitment; the adaptive
upper does not use such metadata. There is no claim of separation for
every small n, full support, vanishing delta at fixed noise, or an
unrestricted physical measurement interface.

For example, my rational finite guards use delta=1/10 and r=1/20 at
n=258,4098,65538,1048578. Replacing pi^2 by10 only WEAKENS the lower.
At n=65538 this gives q_nonadaptive>=524304/20125>26, hence at least27
integer actions, against2 adaptive actions. These are model deductions,
not measured sample performance or a guarantee of hardware operation.

## 9. Finite controls, negative controls, and physical boundaries

The new checker passes210 exact rectangular minimization cases including
zero/rank-deficient H;735 full nq-observation inverse/Schur equalities;
11916 hidden-metadata forms in27 exhaustive average cases;2262 exact
Sherman--Morrison/ridge identities and84 average cases. Separate exact
upper controls cover10656 first-action graph/bit/weight cases,
15840 conditional hub-signal checks,63360 pathwise energy checks for
EVERY possible selected vertex, and360 second-action signal cases.
The all-size proof is R1--R8, not extrapolation from these cases.

Floating Gauss--Legendre quadrature covers36 actual full n=4 conditional
score cases and12 scalar non-Gaussian convolution Fisher/TV pairs, each
with a higher-order refinement. Maximum score residual is1.74e-13;
maximum score refinement is2.81e-13 and scalar refinement1.99e-13.
These are NOT interval certificates or acquired unknown-data samples.

Negative controls detect: omitting the ridge factor; replacing the
non-Gaussian posterior by the fixed comparison variance (actual posterior
variances .119434 and .106064 versus comparison .0919997); and ignoring
nonvanishing prior boundary terms (uniform-prior score identity residual
1.5953). They establish that the code distinguishes these invalid
shortcuts, not that all possible mathematical errors have been excluded.

The ideal sensing model grants exact controls and independent Gaussian
full readout. Nominal row-squared-control B is not Joules or duration.
The adaptive action1 can create O(an) hub currents and requires that
dynamic range. Under actual coordinate preparation errors bounded by
kappa, the stated ||L||_infinity<=6a(d+1) allows an O(an kappa) bias.
Keeping it below a fixed fraction of the second-action hub signal
requires kappa=O(1/n), despite the nominal0/1/2 control alphabet. Sensor
laws under this loading, quantization, finite impedance, reset and
calibration remain external physical obligations. No hardware/noise
calibration or physical trial was carried out.

Correctness is positive under the exact stated experiment. Source-method
priority, a complete comparison to prior graph-sensing results and
hardware advantage are separate UNKNOWN/NOT_ACQUIRED questions.

