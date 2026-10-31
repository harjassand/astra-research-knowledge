# Independent challenge of the finite-noise positive-rational compiler

2026-11-01. Constructor: complementary learning lane. This is a mathematical
challenge of the displayed theorem, not a historical-priority or physical audit.

## Pinned premises actually read

All Astra imports are at
`51ce47ce39f976517d60e2f87bbe280b651f6056` of
`harjassand/astra-research-knowledge`.

* N1152 governing source:
  `research/2026-10-29-control-acquisition-and-matrix-formulas/source/p1-dark/selection/inference_determinant_tail_theorem.md`.
  Read in full: positive principal-minor representation, coefficient boxes,
  one-sided truncation, and Section 7's already proposed LP outer family.
* N1150 governing source:
  `research/2026-10-29-control-acquisition-and-matrix-formulas/source/p1-dark/theory/SIMPLEX_LAW_ACQUISITION.md`.
  Path and SHA256 `279325cf5c9c90b8146c1bd3ea5e97485882aa1200d7b39f05ecdabc5212cf4f`
  were checked against the pinned packet; local
  supplied file `../physical/SIMPLEX_LAW_ACQUISITION.md` was read at the exact
  interpolation and noise-bound passage. Its degree-k simplex lattice norming
  constant is C_k=binom(2k-1,k), independent of n, with an ordinary rising-
  factorial proof. No new interpolation claim is made here.

## Checked statement

Let n>=1, delta>0, kappa>=0, G>=0, L=delta G^2, q=delta kappa.
Take r>=1,k>=1. Coefficients are indexed by subsets S of [n], |S|<=r:

    d_empty=1, n_empty=0,
    0<=d_S<=kappa^|S|,
    0<=n_S<=|S|^2 G^2 kappa^(|S|-1).

Interpret kappa=0 separately: D=1, N is linear. For physical N/D the
degree-r truncation error is one-sided, 0<=F-F_r<=E_r=L H_r(q), or E_r=0
when r>=n. At every degree-k barycentric simplex node v, let the calibrated
interval be F(v) in [y_v-eta,y_v+eta]. Fit the linear inequalities

    (y_v-eta-E_r)D(v)<=N(v)<=(y_v+eta)D(v).

The true truncated coefficient pair is feasible. An arbitrary feasible pair
need not be realizable by any PSD B,g. This relaxation is deliberate.

Set

    A_r(q)=sum_{j=0}^r q^j/j!,
    B_{r,k}(q)=L sum_{a=1}^r sum_{b=0}^r
                    1{a+b>k} a q^(a+b-1)/[(a-1)!b!],
    W_{r,k}=C_k A_r(q)^2(2eta+E_r)+(C_k+1)B_{r,k}+E_r.

Then the LP lower/upper response interval

    [ min_feasible N(u)/D(u), max_feasible N(u)/D(u)+E_r ]

contains every physically compatible F and has width <=W_{r,k} uniformly
on the entire dose simplex. All constants are finite rational operations
for rational source specifications. A source-wide hard cap [0,L] may be
intersected with the output, but arbitrary feasible ratios are not assumed
to satisfy it.

## Independent proof and sign checks

For a command u with total dose delta_u<=delta, elementary symmetric sums
satisfy sum_{|S|=a}u_S<=delta_u^a/a!. The coefficient boxes therefore give,
coefficient by coefficient in formal t,

    D(tu) <=coefficientwise sum_{b=0}^r (qt)^b/b!,
    N(tu) <=coefficientwise L t sum_{a=1}^r
                                a(qt)^(a-1)/(a-1)!.

For any two feasible pairs, put H=N D'-N'D. Each positive product has its
degree>k tail in [0,B_{r,k}] at every command. Thus the signed H tail lies
in [-B_{r,k},B_{r,k}]. There is no factor two: the difference of two numbers
in [0,B] has absolute value <=B.

At a lattice node, both ratios belong to the SAME interval
[y-eta-E_r,y+eta], so their difference is at most 2eta+E_r. There is no
second E_r. Multiplication by DD'<=A_r^2 shows
|H(node)|<=A_r^2(2eta+E_r). The total-degree<=k polynomial H_low therefore
has node magnitudes at most A_r^2(2eta+E_r)+B_{r,k}. The lattice norming
inequality bounds it everywhere by C_k times that quantity. Adding H_tail
and dividing by DD'>=1 gives rational-family diameter

    C_k A_r^2(2eta+E_r)+(C_k+1)B_{r,k}.

Only one final E_r is added in the physical upper enclosure. This proves
the stated W. This argument checks actual noisy acquisition convergence;
it does not estimate individual coefficients or invert a Gram matrix.

## Uniform convergence with r=k, including q>=1

For k>=1 the finite positive cross-tail is bounded by

    B_{k,k} <= L exp(2q)[T_k(2q)+q T_{k-1}(2q)],

where T_j is the Poisson tail. To verify the index: total degree s=j+1 has
the universal coefficient L (1+j/2)(2q)^j/j!, and s>k means j>=k.
This is an algebraic domination; no physical Poisson detector is assumed.
For fixed finite q it decays factorially. Since C_k<4^k and A_k<=exp(q),
both C_k E_k and (C_k+1)B_{k,k} tend to zero. Consequently a finite k and
a positive finite eta achieve any requested additive tolerance. The
measurement count is binom(n+k,k), with no dependence on hidden source
dimension, small nonzero g_i, or eigenvalue gaps. It is still combinatorial
in the number of controls n and effective degree k.

## Boundary cases and limits

* q=0: for r>=1, D=1,N linear,E=B=0. The theorem is sound. At k=1 its
  width is 2eta. This agrees with direct simplex interpolation.
* r>=n: actual physical truncation error is zero. Outer polynomial degrees
  are <=n too, so use min(r,n) in the sums; k>=2n gives B=0.
* G=0: F identically zero and no response learning is needed after the
  baseline contract; the general bound is merely conservative.
* A common uncertain baseline must be carried as a correlated variable or
  paid separately. Independent node error eta is a valid conservative route.
* Fixed adversarial eta cannot be driven to zero by repeated measurements.
  Convergence requires a warranted precision service. For conditionally
  unbiased bounded noise, simultaneous confidence intervals can acquire eta
  with explicit repetitions; this is an additional statistical interface.
* The feasible ratios need not be concave or physical. A consumer cannot
  call their direct numerical optimization a convex program merely because
  the true F is concave. Uniform error does permit an approximate value-
  oracle consumer, or a separately charged concave-envelope construction.
* No claim of superior model-identification or rational-fitting algorithm
  follows. Ordinary positive-denominator rational approximation and
  set-membership LP adopt exactly this construction and its new source-
  specific finite-noise convergence guarantee.

## Verdict

The r/k cross-product theorem survives this independent algebraic challenge,
with the one-sided E_r, one positive-tail B, and one final physical E_r
accounted correctly. Finite exact checks are a supplement. Practical cost,
historical novelty, actual measurement qualification, and any superiority
over equally informed ordinary rational fits remain separate questions.

The supplementary program `check_rational_norming.py` completed 4,572 exact
rational outer-model-pair/command checks. It includes nonphysical feasible-
box pairs, q=0, r>k, k>r, and k=2r. It checked interpolation reproduction,
the Lagrange l1 bound, both separate positive tails, the signed-tail bound,
and the final ratio bound. Every check passed. Receipt:
`rational_norming_results.json`. These finite cases do not prove the theorem.

## Two interface consequences

For a gain task, separate r0 and c0 calibration can be avoided. Because
R(u)=r0+c0+F(u) and F(0)=0, one actual zero-dose reading gives
F(u)=R(u)-R(0). Its uncertain offset is shared across every difference and
must be retained or bounded; fixed-source/fixed-gain assumptions remain.
Absolute J tasks still require the appropriate offset information.

No theorem can evade the required precision. Even n=1,B=0 gives F_a(u)=a u
on [0,1]. Two slopes separated 2eta admit a common midpoint report satisfying
the adversarial eta error contract at every command. Hence uniform error
less than eta is impossible. For a bounded unbiased example let
Z=4(B-1/2), B~Bernoulli(1/2+a u/4), so E Z=F_a(u), Z in[-2,2].
Take a_plus/minus=1/2 plus/minus epsilon, 0<epsilon<=1/2. The two Bernoulli
probabilities lie in[1/2,3/4], and their difference is epsilon*u/2. Therefore
each query has KL at most (4/3)epsilon^2. The chain rule covers adaptive
commands. Bretagnolle-Huber testing then gives total calls

    T >= (3/(4 epsilon^2)) log(1/(4 alpha))

for any estimator accurate enough to distinguish these two response laws
with each error probability <=alpha. This is an elementary accuracy lower
bound, not a lower bound on the compiler's combinatorial command count.

## Retained exploratory failure

I considered extending N1202's all-rate lifetime resolvent bounds to full
rare-event lifetimes. That is not automatically a new mechanism: reversible
chain potential theory, quasistationarity and Lanczos/Gauss-Radau methods
already supply strong constructions when given the appropriate gap or
operator access. Furthermore, multiplicative resolvent accuracy does not
give multiplicative survival accuracy: Exp(1) and Exp(1+epsilon) have
resolvents whose ratio stays in [1,1+epsilon], while their survival ratio is
exp(epsilon t), unbounded as t grows. This candidate was deprioritized.
