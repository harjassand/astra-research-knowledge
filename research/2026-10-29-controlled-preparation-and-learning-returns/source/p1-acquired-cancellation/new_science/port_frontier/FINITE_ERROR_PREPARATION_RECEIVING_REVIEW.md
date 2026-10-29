# Consequential review of finite-error receiving effects and preparation information

29 October 2026. Port-information agent independent review of NEW sections 4--6
of FINITE_ERROR_PREDICTIVE_PREPARATION.md, version
73dc022c7201803b1d4be7f2df48bca8f4ede443026e4432de781fabf16862c4.
An exact copy is preserved in reviewed_versions/. Sections 1--3 are used at
their already independently checked scope; they were not re-audited here.

## Decision and a needed execution-interface distinction

The recursive omitted-effect bound is valid for the explicitly stated stage
order: choose an operation from the already available history, execute its
kernel, THEN read a visible label. The joint-density bound K_joint^2<=BM and
the unconditional density-transport construction are valid. The continuous-time
constant-killing improvement is valid in the reversible generator's own L2
geometry at its stated domain.

For an execution interface that also permits an INITIAL fresh label read before
the first kernel call, the complete-record receiving bound requires one more
observation branching. A sufficient corrected bound is

    eta_initial,n <=min(1/2, sqrt(k) eta_n).                  (A)

Equation (7) without this qualification is not valid for that broader interface.
The exact four-state counterexample in section 3 attains the extra sqrt(k) factor
for one call. The fix is to use (A), or count the initial read as a separate
identity-kernel observation stage. An OLD label already in Z is different: it
is conditioned on under the joint initial-information contract, and is not a
new post-preparation state measurement.

Two physical/notation qualifications should also be explicit:

* Adjoint-word acquisition of preparation leakage needs an actual adjoint
  realization of every factor in W, such as the advertised forward
  weighted-reversible menu. Mere preservation of mu by a nonreversible kernel
  does not supply its adjoint operation or a squared-conditional-mean oracle.
* Equation (9) uses the baseline generator's invariant measure pi, including
  its norm and density q=d rho/d pi. It may instead use a different Q reversible
  for mu, but those geometries must not be silently mixed with section 1's
  biased reference mu. The derivation below states this explicitly.

These clarifications preserve the new finite-tolerance capability. No physical
sample, reset, hidden-state bound or unmodeled observation has been acquired
by this review.

## 1. Derivation of the recursive receiving bound

Fix any permitted past record and the policy's external randomization. At that
history node the next selected j is fixed. For a complete-record event with d
stages remaining, its effect has the form

    f=T_j g,       g=sum_a E_a f_a,

where f_a is the conditional event effect of the continuation given the newly
read label a. A stopped leaf has effect 0 or1, constant as a function of the
unobserved current state. All continuation effects satisfy 0<=f_a<=1; hence
0<=g<=1. They need not be the same function in different branches.

Because P commutes with each E_a, T_j1=1 and P1=1,

    (I-P)f=(I-P)T_jP(g-mu(g))
                 +(I-P)T_j sum_a E_a(I-P)f_a.

The first term has norm <=epsilon/2: orthogonal projection cannot increase
the centered L2 norm, and the variance of a [0,1] function is <=1/4.
For the second term, the label supports are orthogonal, so

    ||sum_a E_a(I-P)f_a||^2
        =sum_a ||E_a(I-P)f_a||^2
        <=k max_a ||(I-P)f_a||^2.

Consequently e_d<=epsilon/2+Gamma sqrt(k)e_(d-1), e_0=0, which proves

    e_n<=(epsilon/2) sum_(i=0)^(n-1)(Gamma sqrt(k))^i.

Independently, every actual event effect is in[0,1], so its omitted norm is
<=||f-mu(f)||<=1/2. This proves the cap in (7). Stopping before n stages only
reduces the induction depth. Randomized policies average conditional effects;
the norm bound survives convex averaging. If an independent random key is
part of the service record, condition on it and allow the event to depend on
its value. Correlated retained keys belong in the joint initial-information
contract instead of being declared independent.

This is a bound for arbitrary events of the COMPLETE discrete endpoint record,
not just additive rewards or terminal observables. It does not acquire unseen
between-call paths, retained random durations, or extra state-dependent sensor
kernels that fail to commute with P.

## 2. Geometry and acquired norms

Let H=L2(mu), mu=w pi/pi(w), and let actual T_j be reversible for pi w_j.
Write r_j=w_j/w. Since the invariant measures differ by this bounded positive
multiplier, Markov contraction in L2(pi w_j) gives

    ||T_j||_H<=sqrt(max r_j/min r_j)=Gamma_j.

The scalar normalization cancels. The adjoint is

    T_j^*=M_(r_j)T_j M_(r_j)^-1 in H.

Thus the relevant leakage Gram F^*T_j^*(I-P)T_jF in the H geometry can be
acquired by the actual weighted forward-word protocol. This is not T_j^2 unless
T_j is self-adjoint in H. The source text correctly requires the appropriate
adjoint Gram rather than deriving leakage from Gamma alone.

A product W of available mu-reversible factors has an available reverse-word
adjoint in H even if W itself is not reversible. If W is instead only assumed
mu-preserving with arbitrary nonreversible factors, its contraction proof may
still hold mathematically, but this acquisition route is not supplied without
additional adjoint access. Keeping the factors inside the actual acquired
operation menu resolves that physical-interface issue.

## 3. Exact initial-read counterexample and correction

Take four states with uniform mu, labels A={1,2}, B={3,4}, and
V=span{1_A,1_B}. Let

    T_1 = [[1/4, 0,   3/8, 3/8],
           [0,   3/4, 1/8, 1/8],
           [3/8, 1/8, 1/2, 0  ],
           [3/8, 1/8, 0,   1/2]],

    T_2 = [[1/2, 0,   3/8, 1/8],
           [0,   1/2, 3/8, 1/8],
           [3/8, 3/8, 1/4, 0  ],
           [1/8, 1/8, 0,   3/4]].

Both are symmetric Markov kernels, so both are reversible for the same mu and
Gamma=1. P averages within each label. Direct exact calculation gives

    ||(I-P)T_jP||^2=1/8,       epsilon=1/(2sqrt(2)).

If a FREE initial label is read, select T_1 in A and T_2 in B. Consider the
event that the final label differs from the initial label. Its true effect is

    f=(3/4,1/4,3/4,1/4),
    Pf=(1/2,1/2,1/2,1/2),
    ||(I-P)f||=1/4.

The n=1 bound (7) would give epsilon/2=1/(4sqrt(2))<1/4. The additional initial
read has therefore changed the interface. Its required factor sqrt(k)=sqrt(2)
is attained here.

In general, an initial read produces effect sum_a E_a f_a, where each f_a has
the ordinary n-call bound eta_n after its history is fixed. Orthogonality gives
||(I-P)sum_a E_a f_a||<=sqrt(k)eta_n, proving (A). It is also legitimate to
count the read as an identity-kernel stage, with its ZERO leakage and the
additional branching cost. No actual microscopic freeze is needed for that
bookkeeping; the stage is just a nondemolition observation.

## 4. Constructive joint initial-information bound

Assume q_X=dP_X/dmu<=B and the entire retained old record Z has at most M values.
Let h_z=dP_(X,Z=z)/dmu and p_z=P(Z=z)>0. Nonnegative joint densities satisfy
0<=h_z<=q_X<=B. Therefore

    E_Z ||dP_(X|Z)/dmu||^2
       =sum_z ||h_z||^2/p_z
       <=sum_z B int h_z dmu/p_z <=BM.

There is no hidden independence assumption between X and Z. Rare branches are
weighted by their actual probabilities in this JOINT bound. A separately
postselected branch instead has K_z^2<=B/p_z, as the root text states.

Finite M constrains a posterior information quantity only after the marginal
density bound B and the actual retained-record interface are supplied. It is
not a statement that acquiring an M-valued statistic was cheap. All discarded
measurements and actions may still affect B through the real preparation
protocol, and their physical costs remain charged. Continuous records cannot
be called one finite-valued observation. A continuous independent seed can be
handled by a direct joint-density argument, but a seed used to steer the
source may become correlated and must be analyzed accordingly.

## 5. Density transport through actual weighted-reversible feedback

For a fixed kernel T_j, positivity, T_j1=1 and the preceding adjoint formula
give, when q<=B,

    T_j^*q=r_j T_j(q/r_j)
               <= B max(r_j)/min(r_j)=B rho_j.

Consequently a fixed open-loop word gives B<=B_0 product_j rho_j. From the
actual baseline pi, B_0=pi(w)/min w, with uncertainty in the visible mean
propagated at acquired confidence. No hidden value of pi(x) is required.

For arbitrary causal selection among s available operations, let h_j be the
unnormalized density of the state AND the selected operation immediately before
execution. Then h_j>=0 and sum_j h_j=q, irrespective of how much retained past
information the policy used. The physical Markov kernel contract gives the
unconditional next density as sum_j T_j^*h_j. Since each h_j<=q<=B,

    sum_j T_j^*h_j <= B sum_j rho_j.

This proves the stated conservative feedback update. Its validity requires the
choice to precede the kernel's fresh transition randomness and the kernels to
act on the full declared native state. A dependent unmodeled bath or an
operation-dependent hidden kick would change that kernel contract.

Noninvasive measurement averaged over outcomes leaves q unchanged. Retaining
its outcome changes the joint information and must be charged through Z or a
direct version of (5). Feedback among individually mu-preserving kernels need
NOT preserve mu: with two visible states, choosing identity at state0 and flip
at state1 concentrates a uniform source at state0. Both kernels are individually
uniform-reversible. The factor s in the general feedback density ceiling is
therefore not automatically removable.

This also distinguishes the FIXED preparation word W in sections 1--3 from an
adaptive observation-driven reset. Discarding an adaptive reset's observations
afterwards does not make its combined kernel mu-preserving. A combined adaptive
operation needs its own warranted invariance and acquired adjoint/leakage
interface before being substituted for W.

The construction supplies a sufficient initial-information budget without
hidden-state readings. It continues to rely on the actual original baseline
preparation and physical weighted-reversibility promises; those are not learned
from a finite visible fit.

## 6. Constant-killing continuous-time improvement

Use H0=L2(pi), q=d rho/dpi, a bounded reversible generator Q, an orthogonal
P containing1, A=PQP|V, and d=||(I-P)QP||. All norms and densities in this
paragraph use THAT invariant measure. The same proof works with mu in place
of pi if the chosen Q is actually reversible for mu. It is not a free change
of geometry for a Q reversible only for pi.

Let P0=P-1 tensor1 and E=QP-PA=(I-P)QP. Since Q1=A1=0, E1=0. Duhamel gives

    exp(tQ)P-P exp(tA)
       =int_0^t exp((t-s)Q) E exp(sA) ds.

The centered compression gap yields ||E exp(sA)P0||<=d exp(-lambda s).
The full Q semigroup is a contraction. The difference also annihilates the
constant part, so its full operator norm is bounded by

    (d/lambda)(1-exp(-lambda t)).

Taking adjoints gives the same norm for P exp(tQ)-exp(tA)P. Apply it to q-1,
whose norm is <=sqrt(K^2-1), and add the centered compressed evolution term:

    ||P(exp(tQ)q-1)||
      <=sqrt(K^2-1)[exp(-lambda t)
                     +(d/lambda)(1-exp(-lambda t))].

Thus (9) is correct, and the previous t d estimate is a coarser alternative.
The saturation floor does not require hidden mixing. If the generator is
unbounded, V must lie in its domain and the Duhamel use needs its domain
justification. Sharp diffusion indicators do not acquire that domain condition
from a Gram matrix. The bounded-kernel construction avoids this issue and is
correctly retained as the applicable finite-error route in that setting.

## 7. Scope of the completed review

The new receiving recurrence, joint-density budget and physical density
transport are sufficient at the actual declared stage/record interfaces.
They connect acquired omitted norms to complete finite service records even
when exact finite rank is unavailable. They do not guarantee small residuals,
affordable rank/depth, cheap acquisition, unbounded mean-lifetime control,
or microscopic regeneration. The initial-read correction (A), adjoint-factor
access and invariant-measure geometry should travel with the result.
