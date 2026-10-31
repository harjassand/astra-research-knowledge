# Acquiring an economical frame by paying for return depth

Research continuation, 31 October 2026. Companion program:
`geometry_acquisition_check.py`; recorded output:
`geometry_acquisition_results.json`.

## Result and boundary

The old rank-two obstruction is a limitation of finite invariant polytope
coordinates. It is not a limit on learning compact predictive machinery.
Here is an operational escape: repeatedly lengthen an actual return word until
its orbit vector supplies a well-conditioned second coordinate, then use that
acquired coordinate to construct the missing sine measurement required by an
ordinary robust phase learner. No useful frame, quadrature probe, or small-angle
estimate is supplied. The complete experiment depth is paid.

For the explicit two-reflection circle family, all scalar predictions of words
of length at most H can be learned to additive epsilon with a model of dimension
at most two. The number of acquired moment types is O(log(H/epsilon)); the total
primitive execution cost, including sampling, is

    O(B^2 [H/epsilon + q log(H/epsilon)]
         log(log(H/epsilon)/delta)),

with fixed numerical constants stated below and q acquired adaptively. Either
q = O(min{1/dist(theta,pi Z), H/sqrt(epsilon)}) is found, or the task is already
indistinguishable, to the requested tolerance, from a one-coordinate signed
model. Preparations and readouts add their actual costs per sampled return.

This is a **family-promised construction**, not finite-data certification that
an arbitrary source has rank two. A separate measured closure check below gives
generic soundness if desired, at an explicitly higher precision cost. The
general question of polynomial acquisition in hidden rank r is not settled here.

The adopted algorithm is an ordinary retaining robust phase learner. The
multiscale phase method is established prior art. The contribution to this
investigation is to construct its prerequisite quadrature operation from the
actual Gram-return interface, and to account for the frame search, unsuccessful
attempts, preparation, depth, and precision. No advantage over that ordinary
learner is claimed.

## 1. Actual source and future task

On the circle with uniform stationary measure, let

    f(x) = sqrt(2) cos x,
    (A g)(x) = g(-x),
    (B g)(x) = g(theta-x).

Both primitives are self-adjoint Markov isometries with the same invariant
measure. Put f_k(x) = sqrt(2) cos(x-k theta). Then

    A f_k = f_(-k),   B f_k = f_(1-k),
    <f_k,f_l> = cos((k-l)theta).

Writing R = B A, an actual length-2n word prepares the orbit vector R^n f = f_n
in the operator convention. The established chronological adjoint-return
interface implements its moment with a fresh stationary preparation and total
primitive return length 2|n|. No hidden-state copy or normalized linear
combination is prepared.

The endpoint-product report is in [-2,2], because f has unit L2 norm but
pointwise bound sqrt(2). Its law is

    Z_n = 2 cos X cos(X-n theta)
        = cos(n theta) + cos(2X-n theta),  X uniform.

Thus E Z_n = c_n := cos(n theta), and the physical report bound is B=2.
One can instead use f=cos x and reports in [-1,1], then multiply the estimated
moments by two. That normalization has exactly the same effective variance
and sampling bill. Neither choice supplies a unit-range physical report for
the unit-L2 seed.

The family promise consists of these two reflections and this observable,
with theta unknown. In particular, all A/B words have responses

    <f,T_w f> = cos(k(w)theta),  |k(w)| <= ceil(|w|/2),

where k starts at zero and updates by k -> -k for A and k -> 1-k for B.
The construction below uses the deliberately conservative bound |k(w)|<=H.
For lower bounds, the primitive horizon must instead be respected explicitly:
index n is reached by B(AB)^(n-1), of length 2n-1.
The future task is to answer **every** such word up to horizon H, not merely
the sampled powers. Once acquired, the model also supplies two orthogonal
2-by-2 matrices, or a one-coordinate signed model at the requested resolution.

All supplied source structure is visible here. In a general unknown
contraction source, neither the trigonometric identities nor this complete
parameterization may be assumed.

## 2. Acquire the frame rather than invert a tiny pivot

Set

    eta = 1/64,
    a = acos(47/64) = 0.7460509236...,
    K = the least power of two >= max(1, a H/sqrt(epsilon)).

Estimate c_k to total error at most eta for k=1,2,4,...,K. Stop at the first
q with |c_hat_q| <= 3/4. On the simultaneous confidence event,

    |c_q| <= 49/64,
    G_q = [[1,c_q],[c_q,1]],
    lambda_min(G_q) >= 15/64,
    condition_2(G_q) <= 113/15 < 7.534.

This is an acquired constant condition bound for the actual word frame
(f,R^q f). The original short frame (f,Bf) can have condition tending to
infinity. Waiting for a useful orbit direction, at its physical cost, avoids
normalizing that original almost-invisible difference.

### Why doubling cannot skip the useful direction

Let phi = dist(theta,pi Z), chosen in [0,pi/2]. At integer k,
|cos(k theta)| = |cos(k phi)|. If phi >= a, k=1 already has
|cos phi| <=47/64. Otherwise, the first dyadic k with k phi >= a has

    a <= k phi < 2a < pi-a,

because 3a<pi. Hence |cos(k phi)| <=47/64 and the noisy acceptance test
must pass. Therefore q <= max(1,2a/phi) whenever the cap reaches that scale.

If no q has been accepted through K, then phi<a/K. The sign s of cos theta
is unambiguous from the first estimate. Since theta=m pi +/-phi,

    cos(n theta) = s^n cos(n phi),
    |cos(n theta)-s^n| <= n^2 phi^2/2
                       <= a^2 H^2/(2K^2) <= epsilon/2.

The learner may return the one-dimensional model A=1, B=s. This conclusion
uses the reflection-family promise. Failed dyadic trials do not certify an
arbitrary source to have dimension one. They also are not free: every sampled
word through K appears in the bill.

## 3. The acquired frame constructs a quadrature operation

Suppose an anchor q was accepted. For every integer n,

    [c_(n-q) - c_n c_q] / sqrt(1-c_q^2)
       = sign(sin(q theta)) sin(n theta).

Thus two scalar cosine returns and the retained anchor measurement construct
the sine quadrature, up to a single orientation sign sigma. The denominator is
bounded below by sqrt(1695)/64 > 0.643. These are bounded numerical
coefficients, not a physically prepared synthetic state. Negative n-q causes
no source complication: c_(-j)=c_j, so the experiment uses |n-q|.

Use clipped estimates c_hat in [-1,1], which cannot increase their error.
Since the accepted value satisfies |c_hat_q|<=3/4, its computed denominator
is at least sqrt(7)/4. If all three moment errors are at most eta, elementary
subtraction and square-root perturbation give

    |quadrature_hat - sigma sin(n theta)| <= 6 eta,
    ||(c_hat_n,quadrature_hat)
       -(cos(n theta),sigma sin(n theta))||_2 <= 7 eta.

For completeness, the numerator perturbation is at most
(2+|c_hat_q|)eta <=2.75eta. The square-root perturbation is at most

    (|c_hat_q|+|c_q|)eta /
      [sqrt(1-c_hat_q^2)+sqrt(1-c_q^2)] < 1.163eta.

Dividing their sum by sqrt(7)/4 gives less than 6eta. The angular error is
therefore at most asin(7eta)<0.110 radians. Numerical evaluation can consume
an additional pi/48 radians while staying below

    b = pi/12 = 0.261799... .

The sign sigma does not affect any future scalar word response:
cos(k sigma theta)=cos(k theta). It merely chooses the orientation of the
learned Euclidean coordinates. Near theta=pi, the signed one-coordinate
fallback retains the correct parity. The program checks both issues.

## 4. Ordinary robust phase unwrapping, now constructively available

For n_j=2^j, estimate the phase a_j=atan2(quadrature_hat,c_hat_nj).
Its circular distance from 2^j gamma is at most b, where gamma=sigma theta.
Start with gamma_hat_0=a_0. At level j>0 choose the value

    (a_j+2 pi l)/2^j,  l integer,

nearest the previous estimate. This choice is computable by one integer
rounding, not a search oracle. If the previous error is at most b/2^(j-1),
the correct candidate lies within 3b/2^j of it. Other candidates are spaced
2pi/2^j apart. Since 3b<pi, the correct lift is uniquely nearest, so the new
error is at most b/2^j. The induction is unaffected by crossing the principal
branch at +/-pi: one keeps a consistent real lift, then takes cosine.

Take N=2^J to be the least power of two at least max(1,2bH/epsilon).
Then the final phase error, modulo its irrelevant orientation, is at most
b/N <=epsilon/(2H). Every requested word obeys

    |cos(k(w)theta)-cos(k(w)gamma_hat)|
       <= H b/N <=epsilon/2.

Final evaluation uses the other epsilon/2 budget. One convenient stable
representation is

    A_hat = [[1,0],[0,-1]],
    B_hat = [[cos gamma_hat,sin gamma_hat],
             [sin gamma_hat,-cos gamma_hat]],
    seed = e_1.

These are exact symbolic orthogonal matrices at the retained rational
approximation gamma_hat. Deployment can update the integer index k(w) and
evaluate cos(k gamma_hat), avoiding repeated unverified floating-point
matrix products. Trigonometric evaluation is to a stated numerical tolerance.

The phase learner, not the unstable short-basis inverse, is the strong
ordinary comparator. This construction adopts it completely.

## 5. Complete acquisition, preparation, depth, and precision bill

Number distinct moment requests in their adaptive order, i=1,2,..., and
allocate failure probability

    delta_i = delta/[i(i+1)].

The next moment index depends only on preceding data. Each new request takes
fresh conditionally unbiased bounded source reports. Hence conditional
Hoeffding and a union bound give a simultaneous event of probability at least
1-delta, without treating adaptively selected probes as predetermined.
All estimates and confidence allocations are retained and reused.

To reserve half of eta for statistical error and half for report and
arithmetic rounding, use

    M_i = ceil[8 B^2 eta^(-2) log(2 i(i+1)/delta)]

shots for the ith new moment. Round each report with deterministic error at
most eta/4 and compute its average with error at most eta/4. This makes total
moment error at most eta on the confidence event. The executable uses physical
range B=2 and reports rounded to ten fractional bits: bias at most 2^-11,
strictly less than eta/4. Grid reports sum as integers; accumulators require
O(log M_i + log B + log(1/eta)) bits. The final averages are rounded to the
specified tolerance. The simulator's float64 generation and checks are
numerical diagnostics; the theorem does not depend on float64 correctness.

Let Q be the number of distinct moments, M_max=max_i M_i. For a found anchor,

    Q <= 1+log2(q) + 2(J+1),
    stationary preparations <= Q M_max,
    endpoint evaluations <= 2Q M_max,
    primitive reflections <= M_max [4q+8N+2q(J+1)].

The last inequality pays for all failed anchor candidates, all positive-power
probes, and every offset probe |2^j-q|. Cache reuse can only reduce it.
For a failed anchor search through K, Q<=1+log2 K and the reflection bill is
at most 4K M_max. These caps apply even on a failed confidence event, so no
unbounded search or uncharged bad-event execution is hidden in an expected
cost statement. Each episode additionally pays the actual stationary
preparation cost and its readout costs. If those are P and C(b_report), the
total adds Q M_max[P+2C(b_report)]. If the preparation cost varies by request,
use its actual sum. Unknown or unavailable stationary preparation is not a
free premise supplied by this algorithm.

If the implementation reads the two bounded endpoint values separately,
their numerical precision must also be paid: absolute endpoint error at
most eta/(16 sqrt(2)) makes the product error less than eta/4. This changes
the readout bit count by a constant. The direct product-report specification
and the program's product rounding have the same constant-precision scaling.

For the phase and branch computations, O(log(N/epsilon)) fractional bits
suffice with guarded interval square roots, atan2, and pi. The denominator is
bounded below and the measured complex vector stays separated from zero, so
these computations have no hidden small-denominator requirement. Maintain
each unwrapped phase to absolute error substantially below b/(16N); this is
enough to preserve nearest-lift decisions and the stated angular margin.
Ordinary rational interval/Taylor or bisection algorithms implement these
elementary operations in polynomial time in that precision. Apart from
processing the source reports, there are O(Q) such scalar operations and
O(Q) retained moment entries. Word execution is not binary exponentiation:
the source actually pays all 2n primitive applications.

Deployment for a supplied word of length L<=H takes L elementary signed
integer updates, O(L log H) bit operations under elementary arithmetic, plus
one bounded-precision cosine evaluation. It uses no new source interaction.
For larger future horizons the retained moments and anchor remain available;
only missing dyadic and offset moments are acquired. The new maximum return
depth is still fully paid. Retention does not turn a precision upgrade into
a free prediction theorem.

### Bounded stationary reports are not the weighted adjoint interface

All these costs use a common stationary law and the fixed report bound B=2.
For a general weighted adjoint return with word-dependent report bound B_n,
the actual bill is a sum of M_i proportional to B_(n_i)^2 at each requested
word. The long phase probes can be exponentially expensive if those weights
grow exponentially with return length. Nothing here converts that broader
interface into the common-stationary bounded-report case.

## 6. Optional generic closure validation

Here is a sound way to distinguish the preceding family promise from a
generic acceptance certificate. Let V=(f,R^q f), and measure

    G=V*V, K_a=V*T_a V, L_a=(T_a V)*(T_a V)

for a in {A,B}. There are at most 17 distinct matrix entries before cache
reuse. With entrywise uncertainty zeta, each 2-by-2 matrix has operator
uncertainty at most 2zeta. Compute

    C_hat_a=G_hat^-1 K_hat_a,
    R_hat_a=L_hat_a-K_hat_a^T G_hat^-1 K_hat_a.

Accept only when all the following measured conditions hold:

    lambda_min(G_hat)>=1/6,
    ||C_hat_a||_2<=4,
    lambda_max(R_hat_a)<=64zeta,
    zeta<=1/4096.

Then true G>=I/8. The true squared residual at the fitted coefficients is

    R(C_hat)=L-K^T C_hat-C_hat^T K+C_hat^T G C_hat.

Its operator deviation from R_hat is at most
2zeta(1+||C_hat||)^2<=50zeta. Hence

    ||(I-P)T_a P||^2
       <= ||(T_a V-V C_hat)G^-1/2||^2
       <= 8(64+50)zeta <=1024zeta,

where P is the orthogonal projection onto span(V). This argument is valid
for arbitrary Hilbert contractions and does not assume rank two.

Choose zeta=epsilon^2/(4096 H^2). Projection then contributes at most
epsilon/2 to a length-H scalar prediction. Whitening K_hat using G_hat and
clipping singular values above one gives a learned contraction. In the true
whitened gauge, the Gram and cross-matrix errors are at most 16zeta; a
conservative bound is 256zeta per clipped operator and 32zeta per clipped
seed. Thus seed and operator estimation add at most

    64zeta+256H zeta <=5epsilon/64

for H>=1 and epsilon<=1. A remaining numerical budget of epsilon/4 is ample.
All the matrix operations are 2-by-2 with an acquired inverse bound, and
can be evaluated with interval error substantially below zeta.

On the exact circle family, the acquired true Gram condition is <=113/15,
so its exact coefficient matrices have norm <=sqrt(113/15)<2.745. The
estimated coefficient error is <48zeta. Exact closure gives true fitted
residual norm <=4608zeta^2, and the 50zeta perturbation bound makes the
64zeta test pass. Thus rank two is used only to prove successful closure
validation on this family; acceptance itself is generic.

The price is real: validation needs O(B^2 H^4 epsilon^-4 log(1/delta))
scalar shots, each of depth at most 4q+2, plus preparation/readout and
numerical costs. The family-specific phase theorem does not secretly include
this generic certification. If a generic test fails, its shots and words are
charged and no global-rank claim follows. The family-specific no-anchor
fallback likewise remains separate; a generic learner must measure and
validate a one-dimensional closure, or continue its search.

Subsequent refinement: `quadratic_leakage.md` proves that for self-adjoint
primitives and scalar tasks whose seed and readout lie in the acquired
subspace, projection error is quadratic in leakage. That permits validation
at zeta=O(epsilon/H^2), improving the above scalar-shot dependence from
epsilon^-4 to epsilon^-2. The displayed earlier bound remains valid for
generic forward-only contraction control, but is unnecessarily conservative
for the self-adjoint scalar task. In-span operator fitting error still needs
its separate first-order budget.

## 7. A genuine information-contract lower bound at rank one

Compact stable geometry does not eliminate source information cost. Consider
the reversible two-state Markov kernel

    P_theta = [[1-theta/2,theta/2],[theta/2,1-theta/2]],
    pi=(1/2,1/2), f=(1,-1), lambda=1-theta.

The reachable space is one-dimensional, the geometry is already perfectly
conditioned, and a length-l endpoint-product return is a +/-1 bit of mean
lambda^l. Preparations have the same law for all theta. One primitive
transition flips with probability theta/2.

For H>=4 and 0<epsilon<=1/16, compare

    theta_0=1/H, theta_1=(1+16epsilon)/H.

Their horizon-H predictions differ by more than 2epsilon. Indeed, throughout
this interval the magnitude of the derivative of (1-theta)^H is at least
H(1-2/H)^(H-1)>=H/8, and the interval has length 16epsilon/H. The integral
is strictly larger than its endpoint lower bound.

The KL divergence of one full primitive transition under theta_0 versus
theta_1 is at most

    (theta_1/2-theta_0/2)^2 /
      [(theta_1/2)(1-theta_1/2)]
       <=256 epsilon^2/H.

A length-l endpoint is a function of the full l-step trajectory, so its
relative entropy is at most l times that amount. Conditional chain rule
handles adaptive queries and stopping: if C is the total number of primitive
applications, the complete transcript satisfies

    KL(transcript_0 || transcript_1)
       <=256 epsilon^2 E_0[C]/H.

A predictor correct within epsilon under both models with failure at most
delta must distinguish them. Binary data processing therefore gives

    E_0[C] >= H/(256epsilon^2) kl(1-delta,delta).

This lower bound permits arbitrary return lengths, arbitrary adaptive
experiments, retained observations, and a supplied perfect rank-one
representation. It is a limitation of this actual information contract,
not of a chosen finite dictionary. Preparation and readout costs only add.

An ordinary retaining estimator matches the order. Take independent one-step
returns and retain the number of flips. For theta in [1/H,2/H],
24H epsilon^-2 log(2/delta) shots suffice by multiplicative Chernoff to
estimate theta within epsilon/H and therefore all lambda^h, h<=H, within
epsilon. A Bernstein version with a larger universal constant gives
O(H epsilon^-2 log(1/delta)) uniformly over theta in [0,1]: its parameter
error is O(epsilon[theta+1/H]); for theta<=1/H use the horizon bound H,
and otherwise use the decaying derivative of (1-theta)^h. No conditioning
penalty or basis acquisition is necessary on this family.

This does not impose an epsilon^-2 cost on every isometric source. The next
bound shows why the reflection family has a different attainable law.

## 8. The phase scaling is also paid, not hidden free amplification

For the circle family, consider a legitimate bounded-return service that
randomizes each physical endpoint product z in [-2,2] to +/-2, with
P(+2|z)=(z+2)/4. It exposes only this randomized product. A return with
phase index d has P(+2)=(2+cos(d theta))/4 in [1/4,3/4].

For angles differing by Delta, its KL divergence is at most

    min(d^2 Delta^2,4)/3 <= (2/3)|d| |Delta|.

For any Gram query, |d| is at most its total primitive word length l.
Let n=ceil(H/2). The word B(AB)^(n-1) has length 2n-1<=H and response
cos(n theta). Choose theta_0=pi/(2n), theta_1=theta_0+4epsilon/n, with
epsilon<=1/8. These accessible task responses differ by
sin(4epsilon)>2epsilon. The same adaptive chain-rule argument proves

    E_0[C] >= 3n/(8epsilon) kl(1-delta,delta)
            >= 3H/(16epsilon) kl(1-delta,delta).

Thus the phase construction's nearly H/epsilon primitive scaling has the
right worst-case order, up to its logarithms, for this bounded-product
contract. It is not a lower bound for the more informative unrandomized
endpoint-product law or for a service exposing both endpoint values.

Together, the rank-one decaying mode and rank-two isometric mode explain why
linear dimension alone cannot specify the full price of predictive knowledge.
The way informative changes accumulate, and the information released by an
actual experiment, matter even after the best geometry is known.

## 9. Executed diagnostics and preserved limitations

The script samples the exact physical endpoint-product distribution, then
rounds reports to ten fractional bits. It numerically checks every integer
phase index 0<=n<=H; these cover all scalar outputs of A/B words up to H.
It also checks the elementary KL and task-separation inequalities on 15
rank-one parameter combinations, plus 16 phase lower-bound combinations with
explicit target-word reachability inside the primitive horizon. Hidden-theta
diagnostics run only after acquisition; the acquiring routine never reads
the simulator parameter. These are diagnostics alongside the proofs,
not substitutes for the proofs or a machine-checked interval certificate.

At H=256, epsilon=.02, delta=.01:

| Fixture | Acquired dimension | Anchor q | Moment types | Preparations | Primitive reflections | Largest numerical scalar error |
|---|---:|---:|---:|---:|---:|---:|
| theta=0 | 1 | none | 12 | 13,909,259 | 10,909,005,784 | 0 |
| theta=1e-5 | 1 | none | 12 | 13,909,259 | 10,909,005,784 | 3.28e-6 |
| theta=2 atan(1/64) | 2 | 32 | 25 | 32,993,880 | 98,499,424,956 | 1.86e-7 |
| theta=2 atan(1/16) | 2 | 8 | 25 | 32,993,880 | 98,951,906,406 | 1.76e-5 |
| theta=1.3 | 2 | 1 | 26 | 34,547,379 | 99,906,276,922 | 2.48e-6 |
| theta=pi/3 | 2 | 1 | 26 | 34,547,379 | 99,906,276,922 | 7.58e-6 |
| theta=pi-1e-5 | 1 | none | 12 | 13,909,259 | 10,909,005,784 | 3.28e-6 |
| theta=pi | 1 | none | 12 | 13,909,259 | 10,909,005,784 | 0 |

These conservative nonasymptotic constants are large. This is a constructive
finite-noise scaling result and a representation repair, not evidence of a
practical experimental advantage. The source simulator aggregates individual
reports on a workstation; its runtime is not those physical execution counts.

For theta=2 atan(1/64), horizon extensions 64 ->256 ->1024 retained the
anchor q=32 and added 21,4,4 moment types respectively. They added
23,450,132,796; 75,049,292,160; and 308,640,702,400 primitive reflections.
The retained dimension stayed two. This makes both cumulative reuse and the
continuing cost of finer predictive resolution visible.

Failed approaches and claim corrections retained:

* Inverting the original short Gram matrix is unnecessary on this family;
  it confuses an expensive coordinate choice with expensive prediction.
* Pure cosine dyadic measurements do not supply the signed phase required
  by the usual atan2 proof. The acquired offset anchor supplies it.
* A no-anchor result implies a signed rank-one task approximation only under
  the stated family promise. It is not generic global-rank certification.
* The frame search is not free: its longest word is O(H/sqrt(epsilon)) in
  the task-resolution fallback, even if the final model has one coordinate.
* Fixed moment precision does not mean fixed execution cost. Phase refinement
  moves to longer return words, reaching O(H/epsilon) depth.
* The physical circle report range is two, and generic weighted returns can
  be much more expensive. Neither is silently replaced by a unit-range oracle.
* Ordinary robust phase estimation wins the useful representation choice and
  is adopted. There is no claimed Astra-versus-retaining-learner separation.
* The initial phase lower-bound draft used cos(H theta) as though it were a
  primitive-length-H task. That was a factor-two horizon error: this response
  generally needs 2H-1 reflections. Section 8 now uses the reachable index
  n=ceil(H/2), exhibits its word, and states the corrected lower-bound
  constant. The scaling and the conservative positive construction are
  unchanged.

## 10. Primary research used constructively

1. Kimmel, Low, Yoder, *Robust Calibration of a Universal Single-Qubit Gate-Set
   via Robust Phase Estimation*, Phys. Rev. A 92, 062315 (2015), corrected
   arXiv v3 (2021): <https://arxiv.org/pdf/1502.02677>.
   The protocol has cosine and sine experiments and uses geometrically
   increasing powers with phase unwrapping. The corrected front matter warns
   that the original pi/2 branch-error condition was too weak; the correct
   analysis uses pi/3 and retains the scaling with changed constants. The
   proof here uses the stricter pi/12 margin and proves the branch choice
   directly. It constructs, rather than assumes, the quadrature operation
   from the bounded Gram-return source. The source's quantum gate experiment
   is not being equated with a generic hidden contraction oracle.

2. Levin and Peres, *Estimating the Spectral Gap of a Reversible Markov Chain
   from a Short Trajectory* (2016): <https://arxiv.org/pdf/1612.05330>.
   Their estimator doubles the skip length until the powered-chain gap is
   bounded away from zero, then transforms that estimate back. The source is
   an observed trajectory of a finite reversible chain; the theorem includes
   stationary minimum mass and spectral-gap costs. This is a strong ordinary
   example of acquiring a useful experimental time scale. It does not supply
   a general noisy hidden-Gram frame theorem. The elementary rank-one proof
   above is written independently for the actual endpoint-product interface.

The prior Astra operation-rule theorem, physical adjoint-return construction,
ordinary learner wins, invariant-polygon obstruction, and recovery-control
result remain unchanged. This note adds one fully paid compact construction
and two source-specific information bounds; it does not replace those results.
