# Independent exact audit: unrestricted static native-product obstruction

## Verdict

**PASS.** The supplied 324 positive rational actual-state weights give an exact native-product certificate on the actual capped eight-site Schlögl generator. The independent checker reconstructs every jump, verifies all 326 orbit-profile identities, and then averages the rows over four explicitly verified graph automorphisms to check all **1304 arbitrary site-profile identities**. No bound on any log factor, interpolation assumption, gauge normalization, or floating-point optimality claim is used.

For every positive static product V(n)=product_i h_i(n_i) and static exponential-prefactor upper envelope g(t,n)=exp(lambda(1-t))*V(n), with lambda>=0 and the SAME product formula on the target, the result is

    g(0,(50,...,50)) > 1-3*10^-22.

The boundary need only majorize one, not equal one. Factors need not be flat or nonnegative in logarithmic coordinates at low counts. The result applies to arbitrary site-dependent static factors, not only two symmetric profiles. It does not apply to products whose target values are separately overwritten to one, or to genuinely time-dependent local shapes.

This is a floor on candidate UPPER ENVELOPES, not a lower bound on the actual hitting probability. No interior probability solve or speedup follows.

## Inputs and replay

Frozen producer input:

    certificate/native_product_exact_dual.json
    SHA256 9a49ab628ce28c0006743bc49d76fb44646309d9de0219dcf64b06544d9e7e15

Independent verifier and receipt:

    certificate/check.py
    certificate/result.json

Replay command:

    python certificate/check.py

The script uses only the Python standard library. It reads rational weights as exact fractions, never executes producer code, reconstructs the physical graph from vertex coordinates, verifies the two degree classes, directly enumerates all reactions and directed diffusion jumps, and independently recomputes both mass and killing charge. Decimal outputs are descriptive only. The certificate inequalities are exact rational comparisons.

The 324 supplied states are distinct, are retained continuation states, and have strictly positive weights. Fifteen support rows have target-entering jumps; two have overflow jumps. The four-automorphism expansion may contain repeated rows, whose positive weights can be combined; uniqueness of expanded rows is neither needed nor claimed.

## Exact row semantics

Write Phi(n)=sum_i phi_i(n_i), phi_i=log h_i. At a retained continuation state x, let k(x) be the total rate of transitions creating count 163. Define the linear form

    q_x(phi)=sum_{x->y retained} rate(x,y)[Phi(y)-Phi(x)].

A retained destination includes target states, with their NATIVE product values. Overflow transitions have payoff zero. Thus

    QV(x)/V(x)
      = sum_{retained y} rate(x,y)[exp(Phi(y)-Phi(x))-1] - k(x)
      >= q_x(phi)-k(x),

using exp(z)>=1+z for all real z. A supercaloric exponential-prefactor envelope therefore satisfies the necessary linear inequalities

    q_x(phi)-lambda <= k(x).

A killed jump contributes the constant -rate and ZERO log-coordinate derivative. The checker deliberately omits both old and destination log derivatives on that jump while retaining its rate in k(x). Incorrectly treating this as an ordinary death of the source log value would invalidate the certificate.

## The exact identity and bound

For the two orbit profiles the supplied weights pi_x satisfy exactly

    4 phi_corner(50)+4 phi_inner(50)+sum_x pi_x q_x(phi)
      =4 phi_corner(15)+4 phi_inner(15).

To remove every profile-symmetry assumption, the auditor explicitly constructs the four grid automorphisms (independent row flip and column reversal), verifies that each preserves every directed edge, applies each to each weighted row with weight pi_x/4, and checks the resulting full-coordinate identity:

    sum_i phi_i(50)+sum_x expanded_pi_x q_x(phi)=sum_i phi_i(15).

All 1304 coefficients are checked exactly. This is a direct expanded dual certificate, not an appeal to an unverified symmetry reduction.

Let M be the total expanded weight and K its weighted overflow charge. The checker obtains

    M = 0.722505697953930089888877272923185980577280123... <1,
    K = 2.66741538755302118209247737765391230100290424...e-22 <3*10^-22.

The supplied fraction strings for M and K are also checked against these independently recomputed values. Their decimal renderings play no role in proof.

Multiplying the necessary inequalities by the positive weights and summing gives

    sum_i phi_i(50)+lambda
      >= sum_i phi_i(15)+(1-M)lambda-K.

The native target boundary at deadline requires

    V(15,...,15)>=1,

so sum_i phi_i(15)>=0. For lambda>=0 and M<1, log g(initial)>=-K>-3*10^-22. Finally exp(z)>=1+z gives

    g(initial)>1-3*10^-22.

**No gauge or low-coordinate nonnegativity is required:** the surviving term is the actual boundary value at the single target corner (15,...,15). The search's coordinate box bounds, lambda upper bound, and numerical zero objective have completely disappeared from this proof.

If one permits lambda<0 but requires the native boundary to majorize one for all t in [0,1], the same certificate also works. The t=0 and t=1 boundary conditions imply sum_i phi_i(15)>=max(0,-lambda). For negative lambda the displayed bound becomes log g(initial)>=-M*lambda-K>=-K. This extension uses the additional initial-time boundary explicitly; the principal statement above retains the simpler lambda>=0 convention.

## Scope and limitations

- Arbitrary 163-value positive static factors at each of eight sites are covered. The proof has no artificial magnitude bounds and no knot interpolation.
- Target slack is covered when the SAME native product defines target values. Only the all-15 target boundary enters the final dual.
- Target overwrite is NOT covered. On a jump into a separately assigned success payoff one, the ratio is 1/V(x), not V(y)/V(x); its tangent row changes. Fifteen positive-weight support rows enter the target, so this is a material limitation, not an ignorable endpoint detail.
- Genuinely time-dependent local factor shapes are not excluded. Earlier flat-low/exact-boundary results cover some of that different class, but this static dual must not be relabeled as a universal time-dependent theorem.
- Pair factors, sums of products, tensor trains and other non-product representations remain open.
- All states, rates, adjacency and overflow conventions are those of the actual eight-site instance supplied in the preceding audits. This is an exact finite certificate with same-team independent reconstruction, not external review or a claim of historical novelty.
