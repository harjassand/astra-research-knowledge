# Finite-error predictive preparation in the physically prepared geometry

29 October 2026. Root construction following the smoothing obstruction and the
complementary finite-error biased preparation proof in noise_frontier. The target
is a COMPLETE later observable record at finite tolerance. Exact finite closure
and hidden mixing are not assumed. The initial-information contract has a
constructive sufficient interface below.

## 1. Actual operations and acquired geometry

Let pi be the baseline law on a standard Borel state space, with noninvasive
visible partition E_a, a=1,...,k. For a known positive visible weight w bounded
above and away from zero, define the genuine reference law

    mu(dx)=w(Y(x)) pi(dx)/pi(w).

An ACTUAL fixed preparation word W is composed of kernels preserving mu. It may
be one reversible biased kernel or a product sharing that weight; the product
need not be reversible. No preparation of mu or hidden convergence to mu is
assumed. Execution time, switches and randomization are paid. No new conditional
reset record is retained for service unless its full instrument is represented.
Every factor must additionally have an ACTUAL adjoint realization for the stated
acquisition, as the available weighted-reversible menu does. Mere invariance of
mu by an arbitrary nonreversible kernel supplies the contraction proof but does
not supply its adjoint experiment or its squared-conditional-mean information.
An adaptive reset with discarded observations is not automatically a fixed
mu-preserving word; its combined operation would need a separate certificate.

Let V be a finite label-local space of bounded acquired future features,
containing1. Its L2(pi) projection P commutes with E_a and multiplication by w;
therefore P is also its orthogonal projection in H=L2(mu). Weighted Gram moments
and pi(w) are acquired by chronological experiments with their finite errors.
Put B=P W|V and V0=V intersect ker(mu). B preserves1 and mu|V. Suppose certified
true weighted-Gram bounds give

    ||B|V0||_H<=kappa<1,       ||(I-P)WP||_H<=e.             (1)

Use an operator norm, not merely eigenvalue modulus. For non-self-adjoint W,
the acquired leakage Gram is <WF,WF>_mu-K*G_mu^(-1)K, K=<F,WF>_mu. The
actual adjoint-word experiment acquires it; a single future's squared report
does not. Clock, sensing, conditioning, statistical and matrix errors are paid.

## 2. A saturating preparation bound

Let actual rho have density q relative to mu with mu(q)=1, ||q||_H<=K. Then
||q-1||<=sqrt(K^2-1). For every v in V and m>=0,

    |rho W^m v-mu(v)| <=sqrt(K^2-1)b_m ||v-mu(v)||_H,
    b_m=kappa^m+e(1-kappa^m)/(1-kappa).                      (2)

Proof. W is Markov and preserves mu, so Jensen gives ||W^n||_H<=1. Put
E=WP-PB; E1=0 and ||E||<=e. Discrete Duhamel is

    W^m P-PB^m=sum_(j=0)^(m-1) W^(m-1-j) E B^j.

On centered V, ||B^j||<=kappa^j. Thus the difference has norm at most
e(1-kappa^m)/(1-kappa)||v-mu(v)|| and zero mu mean. Pair it, and the remaining
centered B^m term, with q-1. This proves(2). Markov contraction also permits
capping b_m at1 in the resulting bounds.

For a genuine event effect v in V, ||v-mu(v)||<=1/2. If e<1-kappa, repetitions
decrease this bound toward sqrt(K^2-1)e/[2(1-kappa)]. More execution cannot
be claimed to erase that floor. The exact bounded-density example in
noise_frontier/FINITE_ERROR_BIASED_PREPARATION.md retains a response of order
e/(1-kappa) forever. If the ratio is large, this certificate is unhelpful.

## 3. Every later service event, including the retained old record

Let f_A(x)=P_x(A) be the ACTUAL effect of any event in any admitted service
program's complete record. Suppose a uniform receiving bound is certified:

    sup_(program,A)||(I-P)f_A||_H <=eta_service.              (3)

Section4 constructs it from acquired operation residuals. Since 0<=f_A<=1,
P contains1 and is orthogonal, ||P f_A-mu(f_A)||<=1/2. The prepared density
q_m=(W*)^m q satisfies ||q_m-1||<=sqrt(K^2-1). Splitting f_A into P f_A and
its omitted part, applying(2), and taking the supremum over ALL events gives

    TV(service after W^m from rho, service from mu)
       <=min{1,sqrt(K^2-1)[b_m/2+eta_service]}.               (4)

Both endpoints are genuine physical laws. No positive r-state realization or
simulated reduced law is needed. Microscopic memory may persist indefinitely.

For retained old record Z, permit the SAME Z-selected service policy on both
sides. A sufficient joint condition is

    E_Z ||dP_(X|Z)/dmu||_H^2 <=K_joint^2.                   (5)

Conditional application and Cauchy--Schwarz prove(4) jointly for (Z,service),
with K_joint replacing K and the same marginal law of Z. Unconditional density
control alone is not(5). New reset paths, clock realizations, random seeds and
apparatus memory cannot be silently retained after analyzing only averaged W.
Section5 constructs a sufficient bound from an explicit record interface.

## 4. Acquired leakage controls finite feedback programs

Actual service kernels T_j may have different known visible reversible weights
w_j relative to pi. Suppose the acquired records and physical weights give

    ||T_j||_H<=Gamma,     ||(I-P)T_jP||_H<=epsilon,
    T_j1=1,              Gamma>=1.                         (6)

Norm equivalence supplies
Gamma_j<=sqrt[max_a(w_j(a)/w(a))/min_a(w_j(a)/w(a))]. When all service calls
preserve mu, Gamma=1. Leakage in THIS geometry is acquired by the appropriate
adjoint-word Gram, including finite errors, not inferred from the norm bound.

A stage chooses j from the visible history, executes T_j, then reads a label.
For at most n stages, a uniform choice in(3) is

    eta_n=min{1/2,(epsilon/2)sum_(i=0)^(n-1)(Gamma sqrt(k))^i}. (7)

Proof. At a history node with d remaining stages, an event effect is
f=T_j sum_a E_a f_a, with continuation effects 0<=f_a<=1. Put
g=sum_a E_a f_a, so 0<=g<=1. Since P commutes with E_a and T_j1=1,

    ||(I-P)f||
      <=||(I-P)T_jP(g-mu(g))||
        +||(I-P)T_j sum_a E_a(I-P)f_a||
      <=epsilon/2+Gamma[sum_a||E_a(I-P)f_a||^2]^(1/2)
      <=epsilon/2+Gamma sqrt(k)max_a||(I-P)f_a||.

Leaves have constant effects0 or1 and zero residual; induction gives the sum.
Independently ||(I-P)f||<=||f-mu(f)||<=1/2 gives the cap. Randomized policies
average the bounds; retained independent keys can be conditioned on. No unseen
between-call paths, arbitrary new durations, or extra retained clock transcript
are supplied by this endpoint-program interface.

A FRESH INITIAL label read after preparation, before the first kernel choice,
adds observation branching. Its sufficient bound is

    eta_initial,n<=min{1/2,sqrt(k) eta_n}.                    (7b)

Indeed its effect is sum_a E_a f_a; orthogonal label supports give the extra
sqrt(k). Alternatively count it as an identity-kernel observation stage with
zero leakage. An old label already included in Z is different from a new state
read after preparation. The independent receiving review contains an exact
four-state counterexample attaining this additional factor; omitting it would
give a false guarantee for the broader interface.

This conservative bound can grow rapidly with the number of observations. It
controls a declared finite-tolerance full record, not an unbounded mean lifetime
or universally inexpensive long-horizon controller. It is useful when the
genuinely acquired residuals make(4) small.

## 5. Constructing initial information from the actual preparation program

Suppose the UNCONDITIONAL initial density relative to mu obeys q_X<=B pointwise,
and Z is the ENTIRE retained old record available to service, with at most M
values. For h_z=dP_(X,Z=z)/dmu and p_z=P(Z=z)>0, 0<=h_z<=q_X<=B. Therefore

    K_joint^2=sum_z||h_z||_H^2/p_z
               <=sum_z B int h_z dmu/p_z <=B M.             (8)

This controls the joint law, not a rare postselected branch. A specified branch
of probability p_z may require K_z^2<=B/p_z. Continuous records require a
direct contract such as(5), or actual declared finite recording/erasure. Calling
a complete path one observation does not make M finite. Any retained key, clock
or apparatus memory that can influence service belongs to the interface.

One sufficient construction of B charges the complete actual protocol. Starting
at baseline pi gives q_0=pi(w)/w(Y), so B_0=pi(w)/min w, with the visible mean
bounded at acquired confidence. For an actual kernel T_j reversible for pi w_j,
let r_j=w_j/w and rho_j=max r_j/min r_j. Its H-adjoint is

    T_j*=M_(r_j) T_j M_(r_j)^(-1).

Thus q<=B implies T_j*q<=B rho_j. A specified open-loop word has
B<=B_0 product rho_j. If a stage selects among s operations using arbitrary
retained information, its unnormalized branch densities h_j sum to q and

    sum_j T_j*h_j <=B sum_j rho_j.

Noninvasive observation averaged over all outcomes leaves the state law
unchanged. Repeating this calculation gives a finite, possibly enormous B from
the complete operation/measurement program. Source postselection, new actuation,
sensor back-action or a dependent bath require their own physical analysis.
Operation choices precede the fresh native transition randomness; the declared
state/kernel contract must include all bath memory relevant to those transitions.

This is a sufficient acquisition/preparation bridge WITHOUT hidden-state reads.
It does not make acquisition cheap or infer it from stored bits. B depends on
the full actual protocol and M concerns all retained service information. Source
trials, discarded observations, timing, work, actuation and precision remain
paid even if the final controller retains a short statistic. Initial baseline
preparation remains a starting premise. A source density condition relative to
pi converts to this geometry with the genuine floor of w/pi(w), not for free.

## 6. Continuous-time corollary at its domain

For the bounded reversible baseline Q and true compression A=PQP from
OPERATIONAL_PREPARATION_AFTER_ACQUISITION.md, let its centered gap be lambda>0
and generator leakage d. In this paragraph ALL norms are in L2(pi) and
q=d rho/d pi. The same argument uses L2(mu) only when its chosen generator is
actually reversible for mu. Duhamel with constant-killing leakage improves the
earlier coarse t d estimate to

    ||P(exp(tQ)q-1)||
      <=sqrt(K^2-1)[exp(-lambda t)
                       +(d/lambda)(1-exp(-lambda t))].      (9)

Indeed ||(QP-PA)exp(sA)P0||<=d exp(-lambda s); integrate and take the adjoint
to bound projected density evolution. The earlier bound is still valid; its
optimized logarithmic factor came from the coarser estimate. This bound has a
floor d/lambda. Unbounded diffusion generators with sharp indicators do not
acquire the necessary domain condition. Their bounded-kernel version(1)--(7)
is appropriate and survives the exact-rank smoothing obstruction.

## 7. Scientific consequence

An ordinary smoothing diffusion may admit no exact finite sharp-readout model.
Nevertheless actual adjoint experiments still acquire omitted norms; an actual
known-weight operation supplies a genuine target; finite contraction controls
repeated preparation; and an explicit initial-information budget connects it to
later complete observable records. Standard projection, contraction, density
transport and Duhamel are the tools, not claimed new ingredients. Useful rank,
conditioning, residual size and affordable physical acquisition remain live
requirements. This construction makes their consequence precise rather than
silently replacing them by microscopic mixing or exact empirical closure.
