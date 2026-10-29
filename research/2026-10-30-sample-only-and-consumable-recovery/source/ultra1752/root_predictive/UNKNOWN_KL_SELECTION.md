# Removing both supplied likelihood values and a supplied KL bound

30 October 2026. **PROPOSED full composition; independent whole challenge pending.**
Root develops the selection argument and constants. T develops the support-safe
empirical-teacher fixed-tau operation; A challenges the entire composition.
The original accepted value-oracle theorem is not retrospectively changed.

## 1. Target theorem

Let P,Q be laws on [O]^T, O>=2,T>=1, and let every P predictive cut have rank<=r.
The algorithm receives iid full P trajectories and iid conditional Q futures at
positive-Q prefixes. It has NO Q probability-value service, NO P conditional
service, NO supplied or verified KL bound and NO target conditioning parameter.
Let d=D(P||Q), allowing infinity for a vacuous guarantee. Set

    A0=ceil[10000(r+O+T+1/delta)],
    kappa=1/131072.

The proposed operation returns, with probability>=1-delta, a finite teacher-free
autoregressive law H satisfying

    TV(P,H) <= epsilon +256 A0^2 d^kappa.                 (1.1)

Its sample, arithmetic, stored-bit and inference costs are fixed polynomials in
A0,1/epsilon, including all returned teacher-future strings, empirical sampling,
candidate evaluations and random-bit work. Source/conditional-service physical
acquisition is an additional paid primitive. Constants and powers are enormous;
(1.1) is generally vacuous at realistic misspecification. This is a theorem-level
access improvement, not useful model distillation or a practical advantage.

The proof below is conditional only on the fixed-tau operation established in
T's new owned proof passing whole review. That operation itself uses the accepted
asymmetric compiler and the ordinary Liu--Moitra empirical-tree primitive, with
the positive-Q support escape and KL transfer reconstructed in SAMPLE_TEACHER.md.

## 2. A fixed-tau operation which needs no actual value of d

At confidence gamma let

    A_gamma=ceil[1000(r+O+T+1/gamma)], x=A_gamma/tau.

For 0<tau<=1/(100 A_gamma), construct the consistent empirical law Qbar with
rho=alpha=x^(-8192), conceptual tree confidence beta, support-safe uniform escape,
and R=(1-alpha)Qbar+alpha Uniform. The empirical tape is independent of the P
sample/feature/algorithm randomness. Generate its rows once, lazily.

On its all-node event, for d<=x^(-16384), the KL transfer gives

    D(P||R)<=d+TO rho+2alpha
                  +(TO rho+sqrt(d/2))[TlogO+log(1/alpha)]
             <=x^(-4096).                              (2.1)

The powers have ample slack: for x sufficiently large, the bracket is<=x^2 and
the right side before the last inequality is<=5x^(-8188). All x here exceed the
required fixed numerical cutoff because tau<=1/(100 A_gamma) and A_gamma>=1000.

Run the accepted fixed-tau acquisition/projection algorithm on R with its known
synthetic upper promise x^(-4096). Its algorithm does not use the actual d. If
the promise happens to hold, the accepted proof gives, with failure<=gamma,

    D(P||H_tau)<=x^(-4096)+40T(B+1)tau.                 (2.2)

If the promise fails, it still returns a valid finite rational autoregressive
law: cap every acquisition/geometry/solver procedure at its deterministic known
polynomial work bound; on a detectable failure return Uniform. Finite feature
positivity has the known uniform Slater point independently of d. Normalize the
cached nonnegative rational token rows, impose exact coefficient sum1, and clamp
each actual output token at b before normalizing. All inference histories then
have actual positive rational token probabilities. The geometry filter either
finds its prescribed rational gap/rank<=r or returns the fallback. Correctness
of a bad candidate is not an additional approximation guarantee.

The old global proof's log bound is B=log[K/(theta a^T)], where
C=8(r+1), a=tau/(2O), theta=tau/[4(r+1)], and K=(r+1)C/a+2.
Using r,O,T<=A0 and tau<=1/(10000 A0), direct expansion gives

    B+1<=100 A0^2 log(1/tau).

Since x>=1/tau, (2.2), Pinsker, T<=A0 and
tau log(1/tau)<=sqrt(tau) give the convenient coarse bound

    TV(P,H_tau)<=64 A0^2 tau^(1/4).                    (2.3)

A0 here is a bound on the scientific parameters, not A_gamma; this distinction
keeps a grid-confidence logarithm out of the noise coefficient.

## 3. Grid confidence without an epsilon-dependent noise factor

For j=0,1,...,J put

    tau_j=2^(-j)/(10000 A0),
    beta_j=gamma_j=delta/[32(j+1)^2],
    A_j=ceil[1000(r+O+T+1/gamma_j)], x_j=A_j/tau_j.

Choose the first J such that

    tau_J <= tau_acc := [epsilon/(1024 A0^2)]^4.

All inputs may be dyadic/rational rounded down with declared factor-two slack;
the displayed exact rational grid is sufficient. The final point satisfies
tau_acc/2<tau_J<=tau_acc. J is O(log(A0/epsilon)).

From the definition of A0,

    A_j<=4 A0(j+1)^2.

The elementary inequality (j+1)^2<= (9/4)2^j for all j>=0 gives

    A_j tau_j <=9/10000<1/100,
    A_j <=9/(10000 tau_j)<=1/tau_j,
    x_j<=tau_j^(-2).                                  (3.1)

Thus the fixed-tau admissibility condition holds at every grid point. Moreover

    d<=tau_j^(32768) => d<=x_j^(-16384).               (3.2)

Tree and fixed-tau failure budgets sum to at most
2(delta/32)sum_(j>=0)(j+1)^(-2)<delta/8. Neither schedule nor computation needs d.
Allocate the remaining confidence to holdout/model sampling, empirical scores and
bounded random-bit implementation. Work is dominated by the smallest tau and
largest A_j, each polynomial in A0,1/epsilon; no hidden exponentially small step
comes from a supplied d.

## 4. Completely ordinary finite-family TV selection

Freeze all K=J+1 finite models before drawing fresh P holdout and fresh samples
from every model. Define A_ij={x:H_i(x)>H_j(x)}. Each point likelihood is a product
of the finite deterministic model's rational token probabilities, obtained by
its paid convex inference algorithm. Exact rational comparison fixes ties.
No unknown P likelihood, conditional P query, teacher evaluation or TV oracle is
used for those sets. All candidate evaluations and samples are teacher-free.

Take n>=log[4(K+1)K^2/delta]/(2e^2) samples from each of P and each H_k.
Hoeffding and a union bound make every empirical probability of each A_ij
accurate to e, except for at most delta/2. Choose k minimizing

    score(k)=max_(i,j)|P_emp(A_ij)-(H_k)_emp(A_ij)|.

For a minimum-TV candidate k*, write v*=TV(P,H_k*). Then score(k*)<=v*+2e.
For the selected k, the true discrepancy |P(A_kk*)-H_k(A_kk*)| is<=v*+4e.
Since A_kk* attains TV(H_k,H_k*),

    TV(P,H_k)<=3v*+4e.                                (4.1)

Set e=epsilon/16. Rational categorical samples have expected polynomial fair-bit
work. If a worst-case cap is desired, use progressive uniform-bit/CDF comparisons
and allocate a union-bound failure across all draws; after sufficiently many
polynomial bits, unresolved comparisons contribute at most the reserved delta.
This changes the failure budget, not which hidden teacher oracle is supplied.

## 5. The global unknown-d guarantee

Let s=d^(1/32768), first considering finite d. If s<=tau_J, the last grid point
qualifies by (3.2); by (2.3) its TV error is<=epsilon/16. If tau_J<s<=tau_0,
choose the smallest grid tau_j>=s. Then tau_j<2s and

    v* <=64*2^(1/4) A0^2 d^(1/131072)
        <77 A0^2 d^kappa.

Together, v*<=epsilon/16+77 A0^2 d^kappa. Equation(4.1) gives error at most
7epsilon/16+231 A0^2 d^kappa, hence (1.1).

If s>tau_0, the claimed noise term is already at least

    256 A0^2 tau_0^(1/4)
      =25.6 A0^(7/4)>1,

so any output law satisfies (1.1). Infinity d is likewise vacuous. For d=0 use
the first case. This is why no supplied KL bound or unknown-noise-dependent
output size is needed. It is not an empirical verification that any given d is
small, and does not estimate r or infer a hidden physical state.

## 6. Consequence and surviving obstacle

If whole review accepts the fixed-tau wrapper and this selection composition,
the acquired capability is condition-free compact acquisition from FULL-P samples
and conditional-SAMPLE access to a possibly arbitrary-rank misspecified teacher,
with no supplied KL bound. Existing same-target model stealing, empirical trees,
KL projection and Scheffe selection remain fully credited ordinary ingredients.

The enormous polynomial exponents and extremely weak Holder modulus remain the
central barrier to useful nonzero-noise acquisition. This operation alone does
not establish practical representation learning or civilisation-level success.
It does eliminate the former probability-VALUE and warranted-Delta suppliers at
the stated mathematical conditional-reset interface, if accepted. Conditional
reset access is still strong and its real acquisition cost is explicit.
