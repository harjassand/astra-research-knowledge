# A finite rational witness below the exact reverse threshold

This construction makes the endpoint proof effective without a matrix-log
oracle. It uses the SAME supplied channel; no new channel, state search or
numerical case is acquired here. It is independently derived in this
challenge, with ownership separate from the producer's main theorem.

Let n>=2, choose a label i, and put

`B=(1/(n-1))sum_(j!=i) tau_j`,
`S=supp(B+tau_i)`, `P=projector ker(B) within S`,
`r=Tr tau_i P`.

All operators below are restricted to S. Take rational certified bounds

`0<a<=min(1,lambda_min(B+tau_i))`,
`0<b<=min(1,lambda_min^+(B))`.

These need no eigenvalue oracle for rational matrices: one may use
`a=min(1,1/Tr[(B+tau_i)^+])`,
`b=min(1,1/Tr[B^+])`, where + means the ordinary Moore--Penrose inverse
on the known exact support. The trace of an inverse is at least the
reciprocal of its smallest positive eigenvalue. Kernel bases and rational
orthogonal projectors give those pseudoinverses by rational elimination.

## 1. Uniform block lower bound

For `0<e<=ab/8`, define `B_e=(1-e)B+e tau_i`. Split S=P+Q with Q=I-P.
For vectors p in P and q in Q, use `||tau_i||<=1` and

`P tau_i P>=aP`, `QBQ>=bQ`.

Since e<=1/2,

`<(p,q),B_e(p,q)>
 >= e a||p||^2-2e||p||||q||+(b/2)||q||^2
 >= (e a/2)||p||^2+(b/2-2e/a)||q||^2
 >= (e a/2)||p||^2+(b/4)||q||^2`.                     (1)

The middle inequality is ordinary scalar Young. Thus, in operator order,

`B_e >= (e a/2)P+(b/4)Q`.                             (2)

This is also valid if P=0; no private-direction compression inverse was
used. Operator monotonicity of log, Tr(tau_i log tau_i)<=0, and (2) give

`D(tau_i||B_e)
 <= r log(1/e)+r log(2/a)+(1-r)log(4/b)
 <= r log(1/e)+log(8/(ab))`.                           (3)

All these relative entropies are finite: B_e is positive on the total
support S. If r=0, the formula still applies and supplies a finite
constant upper bound while the input divergence diverges.

## 2. A literal rational violating pair

Let c>=0 be any rational claimed reverse factor with `c r<1`. Compute
an integer h>=1 such that `2^h>=8/(ab)`, using integer comparisons only.
Put

`k=max(h, floor(c h/(1-c r))+1)`, `e=2^(-k)`.

The scalar-reference input hypotheses are

`p_i=1, p_j=0 (j!=i)`,
`q_i=e, q_j=(1-e)/(n-1) (j!=i)`.

They are exact rational probabilities with q strictly positive. Their
input divergence is `k log2`. Equation (3) yields

`D_in-c D_out
 >=[(1-c r)k-c h]log2 >0`.                            (4)

Consequently they are a finite exact witness to failure of any such c,
including the full conditional comparison since the reference is
scalar. No numerical evaluation of D, no asymptotic oracle, no unknown
reference and no sampling are needed. The first hypothesis is a valid
boundary state with finite divergences; if strict faithfulness is
additionally required, common faithful mixing preserves this strict
inequality for sufficiently small rational mixing. That optional
faithful-mixing precision is not quantified by the above k alone.

## 3. Costs must not be confused

For exact rational input preparations, computing P,r,a,b and the exact
coefficient1/rmin has polynomial bit cost in the explicit matrix input.
This does NOT imply that every explicit entropy witness has polynomial
length in the bit length of c or the threshold gap. The chosen rational
e has denominator2^k and requires k+1 denominator bits in an ordinary
binary rational representation. The bound on k contains
`c/(1-c r)`; both rare priors and precision can therefore cost a great
deal. Compressed exponent notation is a different output contract and
does not erase the eventual state-preparation cost.

This finite witness compiler is a mathematical operation. It does not
acquire a physical preparation with that rare prior, a calibrated
rank-deficient channel, or practical discrimination performance.
