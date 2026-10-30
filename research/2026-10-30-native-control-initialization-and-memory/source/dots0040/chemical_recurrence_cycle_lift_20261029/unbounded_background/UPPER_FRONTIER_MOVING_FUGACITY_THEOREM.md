# Constructive two-dimensional upper-frontier recurrence theorem

29 October 2026. Candidate proof developed by the parent and independently reconstructed here. Not externally reviewed, not novelty-cleared, and not a solution of arbitrary-dimensional or general two-dimensional chemical recurrence. Unlike the finite-phase theorem, both populations are unbounded.

## Contract

Let the finite complex set be

    y_i=(a_i,b_i), i=0,...,m-1, m>=3,

with integer coordinates satisfying

    0=a_0<a_1<...<a_{m-1},
    b_0>b_1>...>b_{m-1}=0.

Assume every listed point is a strict vertex of the upper convex frontier and no three are collinear on that frontier. Equivalently the adjacent positive normal slopes

    r_i=(b_i-b_{i+1})/(a_{i+1}-a_i), i=0,...,m-2,

are strictly increasing. The reaction graph on these complexes is strongly connected, with arbitrary fixed positive rates on its edges. Self-loops may be removed and parallel edges aggregated. Stochastic rates are the exact falling-factorial mass-action rates.

No Lyapunov function, stationary law, gap, mixing estimate, conditional sampler, or finite background is supplied.

## Candidate theorem

There is an explicit finite construction of bounded C1 functions U,V of the logarithmic slope r such that

    mu(a,b)=exp[a U(r)+b V(r)]/(a!b!),
    r=log(a+2)/log(b+2),

is strictly positive, sum mu q<infinity, and L*mu<0 outside a finite set. Hence the CTMC is nonexplosive and positive recurrent on each nonabsorbing communicating class; absorbing singleton classes are trivial.

The construction varies only the smaller-coordinate fugacity: U is constant for r>1, V is constant for r<1, and both are constant on a neighborhood of r=1. They are also constant near r=0 and r=infinity. All choices come from finite graph/rate inequalities. The proof does not assume the existence of a favorable envelope.

## 1. Poisson-defect coefficients

Let k_ij be the aggregate rate from y_i to y_j, zero if absent, and k_i=sum_{j!=i}k_ij. Strong connectivity gives k_i>0. For a fixed fugacity c=(c_A,c_B)>0 define

    d_i(c)=sum_{j!=i}k_ji c^{y_j-y_i}-k_i.

The exact adjoint ratio of c^x/x! is sum_i d_i(c)(x)_{y_i}. We need strict negativity only at the complexes exposed in the population direction, not simultaneously at every complex.

## 2. Acquire a strictly negative fugacity for every exposed pair

For adjacent vertices u=y_i and v=y_{i+1}, the subgenerator on {u,v}, killed upon exit, is transient. Indeed, strong connectivity of a graph with at least three vertices gives a path from either vertex to outside the pair. In elementary terms,

    k_uv k_vu < k_u k_v

if both cross rates are positive; missing cross rates only simplify the inequality. Choose a positive number rho with

    k_uv/k_v < rho < k_u/k_vu,                     (1)

where a zero k_vu makes the upper endpoint infinite. At c^{v-u}=rho the within-pair contributions obey

    k_vu rho-k_u<0,
    k_uv/rho-k_v<0.                               (2)

Let w=(r_i,1). This exposes exactly {u,v}. Along a fugacity whose logarithm tends to infinity in direction w while keeping c^{v-u}=rho, every off-face incoming ratio c^{z-u} and c^{z-v} tends to zero. Hence for a sufficiently large such fugacity both d_u and d_v are strictly negative.

This step is finite and constructive. For rational rates choose a rational rho strictly inside (1); face normals and complex differences are rational/integer.

## 3. One common central fugacity and fixed dominant-coordinate bases

Choose a large scalar M. If the direction (1,1) uniquely exposes a vertex, take the central c_*=(M,M). If it exposes an adjacent pair, choose a fixed positive tangent adjustment c_*=(M,M t_*) satisfying the pair ratio (1), possible because that face has delta_a+delta_b=0. In either case, for sufficiently large M all complexes exposed at r=1 have strictly negative defects. Set

    S=log c_{*,A}, T=log c_{*,B}.

For every face normal r_i>1, keep c_A=c_{*,A} fixed and choose c_B to realize its previously selected rho. Its logarithm is

    log c_B=S/r_i+O(1),

with the O(1) fixed explicitly by rho and the complex difference. Thus as M increases, the fugacity approaches the correct face-normal direction and the off-face terms vanish. For each r_i<1 instead keep c_B=c_{*,B} fixed and solve for c_A; its logarithm is r_i T+O(1). Because there are finitely many faces, one sufficiently large M makes every pair strict inequality and the central inequalities hold simultaneously.

If a face normal equals 1, use the central fugacity for it. Choose a small central slope neighborhood containing no other face normal. On that neighborhood the same central fugacity is valid for whichever of its one or two exposed vertices dominates.

## 4. Interpolate without losing the acquired coefficient margins

For fixed c_A, the function t -> d_i(c_A,exp t) is a finite sum of positive multiples of exponentials in t, minus k_i, so it is convex. If it is negative at two endpoint values, it stays at most the larger of the two negative endpoint values along the entire interval between them. The same fact holds when c_B is fixed and log c_A varies.

On the right of the central neighborhood keep U=S. At each exposed face use a small constant plateau V equal to its acquired face value. Between successive plateaus interpolate V smoothly, only inside the unique-vertex cone. The relevant vertex coefficient is negative at both endpoints (each endpoint face contains it), so convexity supplies a uniform negative margin throughout. The first interpolation from the central plateau has the same property. Extend the final face value constantly to r=infinity.

On the left keep V=T and analogously interpolate U, extending the first face value constantly to r=0. Use C1 cubic interpolants with derivative zero at each plateau endpoint. The finite construction yields bounded U,V and bounded derivatives, and it keeps every nonconstant interpolation interval compactly inside either r<1 or r>1 and inside a unique-vertex cone. All face plateaus have strict margins at both exposed complexes.

## 5. Exact bounded shifts track the selected fugacity

Write F(a,b)=a U(r)+b V(r). On a right interpolation interval U=S is constant and r>=1+epsilon. Its derivative formulas give

    partial_a F = S + b V'(r)/[(a+2)log(b+2)],
    partial_b F = V(r)-[b/(b+2)]r V'(r)/log(b+2).

Since a is much larger than b, these differ from (U(r),V(r)) by o(1), uniformly on each fixed compact interpolation interval. On a left interval r<=1-epsilon,

    partial_a F = U(r)+[a/(a+2)]U'(r)/log(b+2),
    partial_b F = T-a r U'(r)/[(b+2)log(b+2)],

and a is much smaller than b, again giving a uniform o(1) error. Plateaus have exact constant gradients except near their endpoints, where the same bounded-derivative estimates apply.

Thus for each fixed reaction shift z, uniformly in all nonconstant and finite interior plateau strips as a,b grow,

    F(x+z)-F(x)=z_A U(r(x))+z_B V(r(x))+o(1).       (3)

Factorial cancellation in the exact adjoint therefore gives local coefficients d_i(exp U,exp V)+o(1), not a diffusion approximation.

## 6. Monomial dominance supplies the actual tail sign

Cover the finite slope interval between the two endpoint plateaus by the face plateaus and unique-vertex interpolation regions chosen above. On each face plateau, the two exposed monomials have coefficients bounded strictly below zero; every other monomial has a uniformly smaller logarithmic exponent. On each unique-vertex region the exposed monomial has a uniform negative coefficient and dominates every other monomial by a positive power of b. The o(1) errors in (3) therefore preserve strict negativity for sufficiently large b, uniformly over that region.

At the left endpoint plateau the pure-B complex y_0=(0,b_0) has a negative coefficient and uniquely dominates. The ratio of any other monomial to it is bounded by a negative power of b throughout the endpoint slope region. This remains true when a is bounded or zero because falling factorials are at most their monomials, while (b)_{b_0} is comparable to b^{b_0}. Bounded shifts remain inside the constant endpoint plateau outside a finite set. The pure-A endpoint gives the symmetric argument for large a and possibly bounded b.

Hence the exact adjoint is strictly negative outside one finite set K, including all boundary strips; no unbounded disabled-reaction staircase is discarded. All cutoffs arise from fixed coefficient margins, finite monomial gaps, bounded shifts and derivative bounds. They can be computed with certified elementary estimates for rational input rates, but no useful or polynomial encoded cost bound is asserted.

## 7. Summability and actual recurrence

Bounded U,V give mu(a,b)<=exp[C(a+b)]/(a!b!) for some finite C. This implies both sum mu<infinity and sum mu q<infinity for the polynomial rates. The exact embedded-chain dual argument from `MOVING_FUGACITY_DUAL.md`, Section 5, now applies: finite nu=mu q and negative adjoint defect outside finite K imply finite expected embedded excursions, positive recurrence on every closed irreducible class, and nonexplosion. Nonzero enabled mass-action rates are bounded below by the smallest positive reaction constant. Pure-axis endpoint complexes ensure all absorbing states lie in a finite box.

## Boundaries of the theorem

This is an upper-frontier, strongly connected, two-species class with pure-axis endpoints and no three collinear exposed complexes. It does not cover interior complexes, general boundary strata, a face containing a whole closed linkage class, or three-plus collinear exposed complexes. The strict two-vertex face inequalities would fail for a closed neutral face; a growing-shell analysis or another representation would then be needed. In dimensions above two, both the face-internal dynamics and the integrability of moving fugacities require new arguments. No claim of historical novelty is made.
