# What the width changes, and what is not being inferred

30 October 2026. Analytical consequences of the proposed proof; no new source
instance or run. This note does not alter any frozen compiler or adapter bytes.

## 1. A per-cut probability-law interpretation

For cut t, let C_(r,t)(P) be the probability laws Z on[O]^T whose prefix marginal
at t equals the ACTUAL P prefix marginal, and whose joint flattening at ONLY
that cut has rank<=r. Then the proposed width is exactly

    w_r(P)=2 max_t min_(Z in C_(r,t)(P)) TV(P,Z).        (1)

To verify this, a probability row family s_h gives the law Z(h,f)=P(h)s_h(f).
The common prefix marginal is exact. Scaling the rows by their nonzero P(h)
does not change rank, and zero-prefix rows vanish. Conversely any such Z gives
these probability rows on positive-P prefixes. Its full-law L1 discrepancy is
sum_h P(h)||P(.|h)-s_h||1. The per-cut minimizations are independent and compact,
so minimizing their maximum is the maximum of their separate minima. This proves
(1), including its factor2. No Z is computed or sampled by the algorithm.

Thus each cut can have its own probability-valued low-rank explanation while
the emitted sequential model is ONE law. The proof uses the actual-P/teacher
KL dynamics to connect these cuts. It does not glue the explanatory matrices
into an unqualified positive tensor train or a hidden Markov model.

## 2. The relaxed source class is strictly broader than exact truth rank

The already used analytical copy-contamination family demonstrates the domain
change without a new empirical case. Let S be a mixture of two iid Bernoulli
sources on2n bits, and let C put uniform mass on repeated words(x,x). Set

    P_nu=(1-nu)S+nu C,  0<nu<1.

Rank(S)<=2 at every cut and TV(P_nu,S)<=nu, hence w_2(P_nu)<=4nu. At the middle
cut, the joint matrix of S is the sum of two positive outer products and that
of C is2^-n I. Therefore the middle joint matrix of P_nu is positive definite,
with minimum eigenvalue at least nu*2^-n, and true predictive rank2^n. This holds
for EVERY positive nu, however tiny. The new theorem is consequently an
approximate-structure statement for high-rank truth, not a rewording of exact
rank2. Its weak Holder guarantee may still be vacuous for practical nu.

## 3. Quantitative global realization remains separate

The proof pays w_r(P)<=4 eta_r(P), where eta_r is distance to a GLOBAL rank-r
probability law, including all null-prefix issues. It does not prove the reverse
with a dimension-uniform modulus, nor a strict separation between these two
approximate notions. Simultaneously fitting all cut matrices and preserving
global nonnegativity is an additional realization question. Ordinary signed
tensor-train rounding does not automatically pay that constraint.

The compact finite-domain sets share the same exact zero set, so some
instance-dependent continuity relationship exists. Such existence alone does
not provide a useful horizon/conditioning-independent bound. No new numerical
search is used to promote it. The full theorem and its global-shadow corollary
already follow without settling this reverse direction.

## 4. No logit or causal shortcut

Low mean-centered logit rank concerns a different family of matrices. Neither
the exact-rank separation nor (1) implies a useful small width for every such
source. Actual conditional-sample logit learning still needs its own mechanism.
Likewise the new bound is under P's actual observational prefix distribution;
it does not qualify arbitrary causal interventions or off-policy prediction.
The available operation is an autonomous predictive law with an all-P
approximation-dependent error bound, under paid conditional-Q sampling access.
