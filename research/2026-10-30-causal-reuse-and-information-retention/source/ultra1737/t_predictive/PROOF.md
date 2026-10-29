# Proposed teacher-free compiler by asymmetric signed KL projection

30 October 2026. This is a COMPLETE PROPOSED MATHEMATICAL CONSTRUCTION, pending
independent whole challenge. Neither the engineering execution nor this label is
an internal acceptance. The astronomical polynomial is not a practical advantage.

This file governs the theorem. ASYMMETRIC_OPERATION, FRESH_SPANNERS and
RESOURCE_QUALIFICATION retain the derivation history. JOINT_RESTRICTIONS supplies
the improved support-safe cache, replacing normalized child queries in the
engineering prototype. No other scientific branch is modified or imported.

## 1. Input, output and the precise probability oracle

Let P,Q be distributions on [O]^T, O>=2, T>=1. At every cut the conditional
future distributions p_h=P(.|h), h in support(P), have linear span dimension at
most r>=1. The input consists of independent FULL P trajectories, conditional Q
samples at positive-Q prefixes, and next-token Q probability VALUE queries at
such prefixes. A value query returns a warranted interval at a requested number
of bits. Its actual computation cost, denoted C_Q(T,bits), is not free. A GIVEN
warranted rational upper bound Delta<infinity on D(P||Q) is supplied, in nats.
It is neither estimated nor verified by compilation; the theorem is not
Delta-oblivious. No P conditional or likelihood oracle is supplied.
Q can have arbitrary predictive rank. There is no target spectral/positivity gap.

For accuracy epsilon and failure probability delta in(0,1/4), put
A=ceil[1000(r+O+T+1/delta)]. The proposed algorithm has polynomial numbers of P
samples, Q calls, stored bits and inference arithmetic operations in
A,1/epsilon. It asks polynomially many probability BITS; multiply each service
cost in. If that primitive is polynomial-time in these arguments, the entire
operation is polynomial-time. Conditional draws alone do not in general simulate
the precision required here with polynomially many samples.
The ordinary encoded bit length L_in of the supplied rational numerical inputs
is also charged in total input/arithmetic time. Output size has no dependence on
an unnecessarily tiny supplied Delta beyond the accuracy choice below.

With probability at least1-delta the finite returned autoregressive model obeys

    TV(P,P_hat) <= epsilon +128 A^3 Delta^(1/16384).       (1)

It retains no Q evaluator and makes ZERO Q calls during inference or sampling.
The right side can be vacuous at any realistic misspecification. Its significance
is a horizon-independent Holder exponent and a condition-free finite compiler,
if the proposed proof survives whole challenge. This does not assert an efficient
positive-HMM realization, practical forecasting, novelty or physical acquisition.

## 2. Ordinary geometric acquisition, separately at each cut

Fix a parameter0<tau<=1/(100A), write x=A/tau and d'=delta/(100T). Use the schedule

    C=8(r+1), b=tau/O, a=b/2, theta=tau/[4(r+1)],
    D=ceil(x^40), v=a tau, xi=tau,
    gamma0=d' tau/100,
    zeta=d' tau^2/[100 D(r+1)],
    N=ceil(x^60), M=ceil[(A N/zeta)^10],
    theta_geo=zeta/[100(r+1)N],
    eta=min{zeta/[100(r+1)], theta_geo d'/[100 N M]}.

At every nontrivial cut sample N fresh P trajectories. The sampled prefixes have
positive Q probability. Conditional chain rule and Pinsker give

    Pr_h(||p_h-q_h||_1>eta)<=2Delta/eta^2.

Thus all NT fresh queried rows are eta-close except with probability at most
2TNDelta/eta^2. No conditional closeness is asserted for their children.

There exists a subset of at most r sampled TRUE rows whose symmetric coefficient
parallelotope contains1-gamma0 of the P-prefix population. Indeed a maximum-volume
basis of all sampled true rows contains those samples with coefficients<=1. For
any fixed index subset I of size<=r, condition on its values. If its parallelotope
has population mass<1-gamma0, the other N-|I| samples all lie in it with probability
at most exp[-gamma0(N-r)]. Union over at most(r+1)N^r choices. This is an existence
witness, not a P query or computed basis.

To compute a basis, sample M features from
mu_geo=(U+sum_(i=1)^N q_(h_i))/(N+1), where U is the uniform future law. Put
u_i(j)=q_(h_i)(f_j)/(M mu_geo(f_j)). Unknown v_i formed with p_(h_i) have rank<=r.
On the good-row event, Markov plus a union bound gives

    |p_(h_i)(f_j)-q_(h_i)(f_j)|/mu_geo(f_j)<=theta_geo

at every queried pair, except with probability NM eta/theta_geo<=d'/100. Hence
||U-V||op<=sqrt(N/M)theta_geo. Retain singular directions above a threshold between
2 and4 times this known perturbation and compute a2-barycentric column spanner
there. At most r columns remain. Each original column has an l1 sketch residual
at most4(1+2r)sqrt(N)theta_geo<zeta/10 against these selected columns, coefficients
bounded by2. A small threshold gap and approximate SVD/volume swaps suffice:
no singular value of the UNKNOWN P basis is inverted. The retained-coordinate
condition is bounded by the known truncation threshold. To make finite arithmetic
literal, retain a rational approximate spectral subspace and perform exact
rational volume swaps on its coordinate columns. If the retained dimension is
d<=r, their initial volume is at least(delta_svd/sqrt(N))^d; with coordinate
norms<=R the selected-basis inverse can cost O(d log(d N R/delta_svd)) bits.
The factor d (hence r) is explicitly internal arithmetic cost, not a target
singular-value premise or a new teacher-precision oracle. Cache/subspace errors
enlarge the ideal residual constant4 to at most6; since N>=x^60 this is still
below zeta/10. See JOINT_RESTRICTIONS and A's independent fresh-side challenge.

Independently of any selected coefficients, a finite net for [-4,4]^N and
Hoeffding preserve the full L1 norm of EVERY teacher-row combination to zeta/10.
Consequently each sampled q_i is within zeta/2 of a combination of the selected
Q rows. Combine with the hidden true population spanner: outside gamma0 P-mass,
p_h is within r zeta of a combination of selected q's, coefficients<=2r. Its
mass differs from1 by at most r zeta. Normalize its coefficients by that mass:
the resulting signed density z0 has mass1, coefficients<=3r and

    ||p_h-z0||_1<=4r zeta.                            (2)

All selected rows are FRESH Q conditionals. Neither previous-basis children nor
their teacher error enter the selection or its importance measure.

## 3. Fresh features, positivity in measure and feasible proxies

Append a uniform row to the selected rows, R_1,...,R_S, S<=r+1, and set
mu=sum R_i/S. Then R_i/mu<=S and mu>=1/(S O^L), L remaining length. Draw D NEW
features from mu, independently after all basis choices. Coefficients satisfy
sum alpha=1, |alpha_i|<=C and finite-feature density z_alpha/mu>=tau. Uniform
coefficients are strictly feasible. At finite precision the implemented threshold
is2tau with slack, while the following statements concern exact virtual rows.

The full negative mass of every feasible state is at most v, simultaneously over
ALL possible inference choices. To see this, apply uniform Hoeffding/net bounds
to (-sum alpha_i R_i/mu)_+. Its empirical negative mass is0, its envelope<=SC,
and its coefficient sup-norm Lipschitz constant<=S^2. The sample count D pays
uniform error v (with half reserved for arithmetic). This is a negative-MASS
bound, not global pointwise positivity inferred from finitely many tests.

Pad the proxy (2) towards mu with weight4tau. It has mass1, coefficients<C and
L1 error e<=4r zeta+8tau<=9tau. If the unpadded density is>=-tau mu at a feature,
the padded density is>=3tau mu. Violating that condition has mu-probability at
most4r zeta/tau. Conditional on all acquired geometry, the expected P-prefix mass
without a feature-feasible proxy is at most gamma0+4D r zeta/tau<=d'tau/20.
Markov over the fresh features gives bad P-prefix mass<=tau except with
probability d'/20. This is P-weighted coverage of ACTUAL histories. It never
conditions on a previously selected basis prefix, avoiding the failed bias step.

## 4. Arbitrary child restrictions enter only a clipped logarithm

At the next cut cache V_(i,o)(f)=R_i(o,f), evaluated on that cut's features.
Each V is a subprobability density<=1. For a current state alpha and actual token
probability pi_o>=a, its reference is w_o=sum alpha_i V_(i,o)/pi_o. No normalized
Q(.|h_i o) query is needed. Bounds below allow every such child without any rank,
target-closeness or coverage promise. Its coefficient box is C/a.

Use delta_L=theta a^L and [z]_L=max(z,delta_L). The floor's total added mass is
at most theta. Every feasible state has excess k_z=int([z]_L-z)<=v+theta.
Let K=(r+1)C/a+2 and B=log[K/(theta a^T)]. Clipped densities lie between delta_L
and K, their pairwise log ratios have magnitude<=B, and their total clipped
masses are at most K.

Uniformly over bounded alpha0,alpha,beta, the function

    ((z_alpha0-z_alpha)/mu) log([z_alpha]_L/[w_beta]_L)

has envelope2SCB and coefficient sup-norm Lipschitz constant at most
2S^2 B+2SC(S+k)/delta_L, k<=r+1 for each token. A coefficient net followed by
Hoeffding therefore integrates it to error xi. Although the floor is exponentially
small in T, ONLY the logarithm of that Lipschitz constant enters the sample
count. No child-dominating importance measure is required. The features remain
independent of all bases; uniformity covers adaptive future coefficient choices.

For the current raw reference w, minimize the finite convex objective

    J(alpha)=D^-1 sum_j [z_alpha(f_j)/mu(f_j)
                         *log(z_alpha(f_j)/[w]_L(f_j))
                         -z_alpha(f_j)/mu(f_j)] .     (3)

Its first-order residual is at most xi. The minus-linear term is necessary
because normalization is in the FULL space, not the empirical feature sum.
Uniform integration gives int(z0-z)log([z]_L/[w]_L)>=-2xi. For a true p and a
feasible proxy z0 with ||p-z0||1<=e, put
Phi_L(p,z)=int p log(p/[z]_L), Z_w=int[w]_L. Then

    Phi_L(p,z)<=Phi_L(p,w)+log Z_w+2xi+B(e+2k_z).      (4)

Proof: insert z0, costing eB, and use the first-order inequality. Replacing z
by [z]_L costs Bk_z. Log-sum gives int[z]_L log([w]_L/[z]_L)
<=(1+k_z)log(Z_w/(1+k_z)). Subtracting log Z_w leaves at most Bk_z since
Z_w<=K. This establishes (4) without a pointwise-positive full signed state.

At bad histories, Phi_L(p,z)-Phi_L(p,w)<=B directly from the clipped log bound.

## 5. Exact transition normalization retains token KL

At a state of exact mass1 and negative mass<=v, let m_o=int z(o,f). Output

    pi_o=max(m_o,b)/M0, M0=sum_o max(m_o,b).

Here1<=M0<=1+v+O b<=2 and pi_o>=a. The raw child is w_o=z(o,.)/pi_o. As
pi_o delta_(L-1)>=delta_L, the exact unnormalized chain rule gives

    sum_o p(o)Phi_(L-1)(p(.|o),w_o)
       <=Phi_L(p,z)-D(p_tokens||pi).                 (5)

The child normalization is uniformly near1, independent of its coverage:

    Z_wo<=m_o/pi_o+v/pi_o+theta
          <=1+v+O b+v/a+theta,
    log Z_wo<=v+O b+v/a+theta<=4tau.                 (6)

The last direct bound is essential: a different Jensen normalization bound can
cancel the token KL and would not prove a compiler. Every projection resets the
parent negative mass to v, so v/a=tau never recurses through T. Token cache
rounding changes (6) by the explicit small terms in JOINT_RESTRICTIONS; (5)
holds for any actual positive pi and remains EXACT for that actual token rule.

Initialize with (1-tau)Q+tau U, whose Phi<=Delta+2tau and negative mass0. Its
required marginal/joint feature data are also cached. At the empty future the
only state is1 and Phi=0. Apply (4)-(6), average under the FIXED P prefix law,
and sum over cuts. The good-proxy error<=9tau, bad mass<=tau and floor/negative
errors give

    D(P||P_hat)<=Delta+2tau+T[6tau+12B tau].          (7)

The sum of token KLs is the KL of the ENTIRE output law by chain rule. There is
no selected-child coverage, P conditional oracle, inverse target-state matrix,
or recursively worsened teacher error in (7). With finite arithmetic, value-
oracle error, known Slater slack and convex-solve residual reserves, use

    D(P||P_hat)<=Delta+40T(B+1)tau.                  (8)

## 6. Explicit resource domination

For x>=1000 the schedule has d'>=x^-2, tau>=x^-1, a>=x^-1 and theta>=x^-1;
A,r+1,O,T,C<=x. It follows successively that D<=x^41, zeta>=x^-50,
N<=x^61, M<=x^1200, theta_geo>=x^-112 and eta>=x^-1400. Therefore
Delta<=x^-4096 makes the good-row failure at most2x^-1234, well inside delta.
The exact bound NM eta/theta_geo<=d'/100 pays the pointwise geometry error.

For sample-compression, gamma0>=x^-4 gives gamma0(N-r)>=x^56/2, while
log[(r+1)N^r/(d'/100)]<=x^3. Thus N pays its failure probability. For the full
L1 sketch a coefficient net gives a bound below10^9 N^7 zeta^-3 (including
confidence); (A N/zeta)^10 dominates it since A>=1000 and N>=1,zeta<=1.

For the gradient sketch use B<=A log x<=x^2, envelope<=x^5, parameter dimension
<=x^2, net log per coordinate<=x^2 and confidence log<=x. With half tolerances
and fixed constants the sufficient Hoeffding bound is below x^24. The negative-
mass bound has a smaller majorant because1/v<=x^2. D=ceil(x^40) pays both, and
the additional token/cut union only changes their confidence log. Across all
events the allocated failure is less than delta, including finite conditional-
sample implementation failures.

Geometry is computed at polynomial BIT accuracy around a known truncation
threshold. Inference (3) has bounded gradient and Hessian polynomial in S,B,1/tau;
the rational coefficient polytope has a known uniform Slater point. A linear-
minimization/Frank--Wolfe procedure decreases its bounded objective by a polynomial
multiple of the squared first-order gap. Ordinary rational LPs and warranted log
intervals therefore produce gap<=tau in polynomial time. No installed SVD or
CLARABEL run is presumed to certify these worst-case statements.

Each full row/joint density evaluation uses at most T next-token calls. The
compilation count is bounded by a fixed polynomial, for example a constant
multiple of T^2[NM+(O+1)(r+1)D+M+D], plus geometric/convex arithmetic. The output
stores O[T O(r+1)D] density/marginal scalars; optional feature-string provenance
adds O(T^2 D log O) bits and is not needed by inference. Scalar bit lengths
are polynomial in T log(O/a),logN,logM,logD,log(1/tau). During inference only
these finite arrays, a bounded rational coefficient vector and convex programs
are used. There is no hidden Q call. Its service cost is nevertheless fully paid
at compilation; probability VALUES, not sample-only access, are load-bearing.

## 7. Choose tau and derive the stated error

Take dyadic tau_acc between (epsilon/(1024A^2))^4 and twice that value. Start
tau=tau_acc and first compare the supplied rational Delta with (tau_acc/A)^4096.
If it is no larger, KEEP tau_acc: do not compute a tiny root of Delta. Otherwise
double tau until Delta<=(tau/A)^4096, or tau>1/(100A). This uses only
O(log(1/tau_acc)) exact rational comparisons, with the supplied input length
L_in charged. When nontrivial doubling occurs, tau<2A Delta^(1/4096).
All output parameters therefore have bit length controlled by tau_acc, not by
an arbitrarily tiny Delta denominator. If tau>1/(100A), return uniform independent
tokens. In this case the right side of(1) exceeds1: tau_acc cannot cause it and
the preceding unsuccessful comparison was at tau/2>1/(200A), so
Delta^(1/16384)>(1/(200A^2))^(1/4).

Otherwise Delta<=(tau/A)^4096 and all resource gates above apply. Since
B<=A log(A/tau), (8) and Pinsker imply the conservative bound

    TV(P,P_hat)<=sqrt(Delta/2)+10A^2 tau^(1/4).

Use tau<=max(tau_acc,2A Delta^(1/4096)) to obtain(1), with room for its
constants. Tau>=tau_acc bounds ALL sample counts and sizes by a fixed polynomial
in A,1/epsilon, regardless of how tiny Delta is. T does not appear in the
exponents of epsilon or Delta. No claim of useful moderate-Delta constants follows.

## 8. Source, execution and unsolved qualifications

Liu--Moitra2411.07536v1, §§3,5,6,7 is the strongest consumed constructive source:
same-target conditional queries, bounded barycentric geometry, density-mixture
sketches, robust truncation and KL convex inference are established machinery.
The new proposed interface is fresh-P acquisition under global KL to a different
arbitrary-rank teacher, coupled to signed full states and the asymmetric clipped-
log telescope. A same-target learner cannot be transferred merely by renaming Q.
Historical priority of this particular extension has not been established.

The retained T8 engineering run uses MUCH smaller budgets and floating tools.
It checks access separation and finite caching, not(1). The rank2 target/rank16
teacher diagnostic, all output probabilities, counts, first failed implementation,
corrected run and ordinary two-component EM comparison remain visible. The EM
model has narrower structural knowledge and no Q calls; it was dramatically
faster. No best-incumbent computational advantage is asserted. The proof itself
remains PROPOSED pending independent whole challenge.
