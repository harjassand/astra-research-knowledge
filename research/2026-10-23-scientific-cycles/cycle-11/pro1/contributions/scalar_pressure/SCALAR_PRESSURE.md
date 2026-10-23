# Scalar pressure comparison: a valid pair control and a decisive higher-distance failure

**Cycle11 distinct contribution.** 23 October 2026, Australia/Brisbane.
Authoring branch: `/root/cycle11_scalar_pressure`.

## Scope and source

This contribution reads the actual Cycle10 `QUADRATIC_CAPACITY_FLOOR.tex` and
`contributions/hamming_response/FULL_HAMMING_RESPONSE.tex`. It studies a proposed
absolute-entry majorant for the new logarithmic-moment question. The conclusions
below are about that comparison, not a capacity converse, actual bath escape,
or a counterexample to a physical prefix log-moment theorem.

Let `b=beta^2`, `a=1-b`, `r=bk`. Let binary words x,y have equal Hamming weight
and distance 2m. The inherited physical block bound is

    ||P_y K_zeta P_x|| <= c_m (ab)^m,   c_m=m binom(2m,m),

and the diagonal blocks vanish. Prefix contraction preserves this bound.
The scalar comparison M on all 2^k binary words is defined by equality in this
bound for distinct equal-weight x,y and zero otherwise. It is entrywise
nonnegative and real symmetric. It retains no signs or color-wire constraints.

## Theorem 1: the full positive scalar comparison has divergent pressure

Fix r>0 and t>0. Set b=r/k and a=1-r/k, taking even k>r. Then

    log(2^-k Tr exp(t M))
      >= (3t/16) a^2 r^2 (k-2)^2 - k ln 2
      -> +infinity.

Consequently no uniform O(r^2) logarithmic-moment estimate can be proved by
this full positive comparator, even when r<=1/256. The failure already occurs
if all distances except four are deleted.

**Proof.** On the weight-q sector, every row has exactly
`binom(q,m) binom(k-q,m)` words at distance 2m. The constant vector in that
sector is therefore an eigenvector with eigenvalue

    Lambda_q=sum_{m>=1} binom(q,m) binom(k-q,m) c_m (ab)^m.

For q=k/2, keeping only m=2 gives, since c_2=12,

    Lambda_q >= 12 binom(k/2,2)^2 (ab)^2
             = (3/16) a^2 r^2 (k-2)^2.

One eigenvalue contributes `exp(t Lambda_q)` to the positive spectral trace.
Dividing by 2^k and taking the logarithm proves the claim. The same argument
applies to the distance-four-only matrix M_2, whose central row sum is exactly
the displayed quadratic expression. QED.

**Why this does not refute the actual programme.** The physical displacement
satisfies `||G_beta||<=k`, and its diagonal part has norm at most ak. Thus the
actual charge-offdiagonal K_zeta has norm at most (1+a)k. The scalar comparator
already violates this elementary physical restriction at sufficiently large k.
It is an upper comparison too loose to settle the physical logarithmic moment;
its rare Perron sector cannot be reinterpreted as a valid physical input.

The example identifies a genuine method failure: summing all endpoint-distance
bounds with positive signs loses all-order unitary cancellations. A second-
moment bound does not detect this issue: the inherited row-square calculation
also gives `2^-k Tr M^2 <= r^2 exp(4r^2)`, despite the divergent exponential
moment. The scalar M therefore supplies an explicit all-k distinction between
second and exponential moment control under exactly the block-size combinatorics.

## Theorem 2: the pair-only comparator has a uniform all-k pressure bound

Let J be the adjacency matrix of distance-two equal-weight binary words, on the
full binary Hilbert space, and let `M_1=2ab J`. For `theta=t a b k` in [0,1),

    log(2^-k Tr exp(t M_1))
      <= -theta-ln(1-theta)
      <= theta^2/[2(1-theta)].

This is a complete exponential-moment estimate, uniform in k; it is not inferred
from a variance or a finite spectral fit.

**Proof.** Write the Pauli spin operators

    S_x=(1/2) sum_i X_i,  S_y=(1/2) sum_i Y_i.

The exact spin identity is

    J=sum_{i<j}(s_i^+ s_j^-+s_i^- s_j^+)
     =S_x^2+S_y^2-kI/2.

Set `c=2tab`. The Golden--Thompson trace inequality gives

    2^-k Tr exp[t M_1]
      <= exp(-tabk) 2^-k Tr exp(c S_x^2) exp(c S_y^2).

Choose the full product X and Y eigenbases. Every squared overlap is 2^-k,
including across degenerate spin sums. Hence the last normalized trace factors
exactly into the product of the two normalized traces, which are equal:

    2^-k Tr exp(c S_x^2) exp(c S_y^2)
      = [ E_x exp( (tab/2)(sum_i x_i)^2 ) ]^2,

where the x_i are independent fair signs. The equality follows by expanding
both functions in the complete product eigenbases, so degeneracy causes no
change. With theta=tabk and a standard real Gaussian g,

    E_x exp[theta (sum_i x_i)^2/(2k)]
      = E_g [cosh(sqrt(theta/k) g)]^k
      <= E_g exp(theta g^2/2)
      = (1-theta)^(-1/2).

Here `cosh u <= exp(u^2/2)` follows, for instance, from
`(ln cosh u)'=tanh u<=u` for u>=0 and evenness. The Gaussian integral is finite
precisely for theta<1. Combining the estimates gives
`exp(-theta)/(1-theta)`. Finally

    -theta-ln(1-theta)=sum_{n>=2}theta^n/n
                       <=theta^2/[2(1-theta)].

QED.

**Receiving use.** Any sound full trace-moment comparison to M_1 inherits this
bound. It is a strong ordinary all-to-all XY control with the same complete
binary sector weights. It is not a bound on the actual full K_zeta, because
higher endpoint coherences are present there. No silent pair truncation is
permitted. The full M failure proves that simply adding their absolute block
bounds destroys the useful comparison, even when every fixed-distance
coefficient is small.

## Lemma 3: an exact physical cancellation on a restricted color subspace

Choose the analytic prefix `zeta=|1^k><1^k|` and restrict the input to
`C_1=span{|0>,|1>}^tensor k`. On this subspace, the compressed actual
charge-offdiagonal response is identically zero:

    P_C1 K_zeta P_C1=0.

This statement is a deep-bulk identity, not an identity at the root and not
`K_zeta=0` on all qutrit inputs.

**Proof.** Take any initial bath word beginning with h>=k copies of color 1,
with an arbitrary untouched tail w and seed. Only 0 and color 1 occur in the
restricted input, so each U call flips the input bit and moves the bath depth
by +1 for bit 1 or -1 for bit 0. Every accessed bath color is 1. No root
exchange is called because at most k moves occur from initial depth >=k.
With `v=alpha X+i beta I`, the exact history sum is

    W_k |x> |1^h,w>
      = sum_y (v^tensor k)_{yx} |y> |1^{h+|x|-|y|},w>.

The exponent is nonnegative. For two input words of the same total charge,
each common output y has exactly the same final bath vector on both sides.
Consequently the input matrix of `W_k^* Q W_k`, restricted to such a charge
block, equals that of `(v^tensor k)^* Q v^tensor k`. The latter is a sum of
one-site terms. Each term has diagonal `a(1-q_i)+b q_i` and charge-changing
offdiagonal terms. Total-charge pinching kills every such offdiagonal term.
Thus the compressed G is exactly `a(2Q-kI)`, proving the claimed zero K.
The first k colors alone determine the bulk representation, so the arbitrary
untouched tail and h choice do not affect this conclusion. QED.

**Limit.** Inputs containing color 2 were excluded. There is no assertion that
one can choose this prefix to make the full physical K vanish. This exact
restriction illustrates the cancellations erased by the positive scalar M:
M has many positive endpoint transitions even where the actual operator's
entire offdiagonal response is zero.

## Necessary-premise examples

- Deleting all higher endpoint terms yields a tractable true pair comparator,
  but does not preserve the actual physical full response.
- The full positive comparator obeys the same useful second-moment row bound
  yet its log moment diverges, so that row bound alone cannot settle the new
  entropy question.
- The all-color-1 zero-response lemma requires both the input color restriction
  and the deep-bulk condition. It is not a whole-qutrit or vacuum statement.

## Proof status, costs and receiving consequence

Theorems 1 and 2 and Lemma 3 are analytic arguments. The accompanying script
only verifies exact finite formulas and the limiting diagnostic at declared
parameters; its runtime is not discovery cost. No actual channel matrix is
formed by the script. No finite fit, field-priority claim, efficient physical
implementation or communication-rate conclusion is asserted.

The receiving consequence is to reject the all-distance positive scalar
majorant as a route to the desired log moment, while retaining an all-k
pair-only exponential-moment baseline and an exact physical cancellation
example. A successful full-response bound must preserve additional signs,
unitarity, or color/prefix structure. Main Pro1 owns that remaining construction.

## Primary mathematical dependency

The pair-pressure argument uses the finite-dimensional Golden--Thompson
inequality `Tr exp(A+B)<=Tr exp(A)exp(B)` for Hermitian A,B. Its original
primary comparison is Sidney Golden, *Lower Bounds for the Helmholtz Function*,
Physical Review 137, B1127--B1128 (1965),
https://doi.org/10.1103/PhysRev.137.B1127. The publisher abstract was read and
confirms the trace-product/partition-function inequality; the full article is
behind a subscription wall and was not obtained. This contribution does not
claim novelty for Golden--Thompson, the Gaussian integral, the spin identity,
or the mean-field control. The new use here is to delimit the absolute-entry
comparison available from the actual physical block bound.
