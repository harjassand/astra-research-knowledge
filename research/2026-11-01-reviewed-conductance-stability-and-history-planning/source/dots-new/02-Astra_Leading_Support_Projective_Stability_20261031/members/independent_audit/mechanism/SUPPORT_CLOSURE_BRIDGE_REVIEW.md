# Independent mathematical review of the top-order support/positive-cone bridge

## Verdict and boundaries

The proposed equivalence is mathematically sound under the definitions and norms below:

1. Every singleton top-order support closure reaches the open species A.
2. At some finite degree there is a homogeneous polynomial in the Bernstein coefficient box `[0,1]` whose top-order Lie derivative has all boundary monomial coefficients nonnegative and all pure boundary coefficients strictly positive.

The true direction is an explicit Euler-polynomial plus coefficient-elevation construction; the false direction has a finite invariant-face obstruction. This is **exact acquisition completeness for a fixed-top-order certificate hierarchy**, not recurrence completeness. No implementation or frozen receiver is accepted by this mechanism-level note. No earlier accepted file is changed.

The full stochastic conclusion also retains one open immigration/death coordinate, total-conservative internal reactions, `n>=2`, and full weak reversibility if every initial state's communicating class is claimed recurrent. Support closure alone does not imply closed state classes: `0<->A` plus irreversible `2B->2A` has transient states despite top-order reachability.

## 1. Definitions

Let p at least two be the designated raw maximum internal source order. Let

    v(y)=sum_(|u|=p) kappa_(u,w) (w-u)y^u

be the homogeneous top-order vector field. Conservation gives `sum_i v_i=0`. A support set S is closed if every top-order reaction whose source support lies in S has target support in S. Starting from a singleton and repeatedly adding such targets produces its finite closure.

Use

    C=max(1,p^3 sum_(top-order channels) kappa),
    T=1/(4C),
    h=T/M,

where M is a positive multiple of n. Zero-increment channels may be discarded. Positivity of rates and a successful support test ensure a nonempty set of relevant top-order channels; let `kappa_min` be their minimum rate.

## 2. Uniform rational support propagation

On the nonnegative unit simplex, every negative coordinate term is bounded below by `-C y_i`: if a channel decreases coordinate i, its source contains i, so `y^u<=y_i`. Thus the Euler map

    E_h(y)=y+h v(y)

satisfies `E_h(y)_i>=(1-hC)y_i`, remains nonnegative, and conserves the sum. Across the entire horizon, every retained mass contribution is multiplied by at least

    (1-hC)^M >=1-MhC=3/4.

An initial coordinate is at least `1/n`, so it remains at least `l_0=3/(4n)` throughout. A singleton support path to A needs at most `n-1` species-addition stages. Divide the M steps into n equal blocks. If every source species in a chosen reaction is at least l throughout its block, the newly produced coordinate receives at least `h kappa_min l^p` per step and retains at least three quarters of that production to the terminal time. Consequently

    l_(r+1)=min(l_r,T kappa_min l_r^p/(4n)),
    delta=l_n>0

is a conservative uniform lower bound on `(E_h^M(y))_A`, independent of M. The factor one quarter is weaker than the three-quarter survival bound. The induction records lower bounds valid through the remaining horizon, not only at block endpoints. If the initial large coordinate is already A, direct survival suffices.

This is a continuous-simplex leading-field argument. It does not assert that one literal stochastic molecule can fire a p-molecular channel.

## 3. Derivative estimates with rational constants

Use the vector infinity norm, induced row-sum matrix norm, and the tensor norm equal to the maximum, over output coordinates, of the sum of absolute second-derivative entries. On the simplex,

    ||v|| <=p sum kappa <=C,
    ||Dv|| <=p^2 sum kappa <=C,
    ||D^2 v|| <=p^2(p-1)sum kappa <=C.

These follow by summing all first or second partial derivatives of a degree-p monomial and bounding each remaining monomial by one.

Put `a=1+hC`. The kth Euler iterate has Jacobian norm at most `a^k`. For `khC<=1/4`, the binomial/geometric comparison gives

    a^k <=1/(1-khC)<=4/3.

If B_k bounds its Hessian tensor norm, the chain rule gives

    B_(k+1)<=a B_k+hC a^(2k),    B_0=0.

Unrolling and bounding each factor by `4/3` yields

    B_k <=(4/3)^3 Ckh <3Ckh.

For

    F_M(y)=h sum_(k=0)^(M-1) (E_h^k(y))_A,

we therefore have `||D^2 F_M||<=3CT^2` (indeed the simple sum gives a stronger factor one half). The exact discrete coboundary is

    F_M(E_h(y))-F_M(y)=h[(E_h^M(y))_A-y_A].

Taylor's theorem along the segment inside the simplex gives

    v(y) dot grad F_M(y)
       >=delta-y_A-3 C^3 T^3/(2M).

Choosing M, still a multiple of n, so that `M>=3 C^3 T^3/delta` proves

    v dot grad F_M >=delta/2-y_A.

Every constant is rational and acquired from the raw list and finite support paths. No favorable function or fluid-return oracle is assumed.

## 4. An actual boxed homogeneous polynomial, not a supplied oracle

The homogeneous Euler map of degree p is

    Ehat_i(y)=y_i N^(p-1)+h v_i(y),   N=sum_i y_i.

For a degree-p monomial involving i, the coefficient in the first term is a positive integer at least one. Its total adverse correction is no more than `h p sum kappa<=hC<=1/4`. A monomial not involving i has no negative contribution to coordinate i. Thus every coefficient of every Ehat_i is nonnegative. Also

    sum_i Ehat_i=N^p.

Each component therefore has normalized Bernstein coefficients in `[0,1]`. Homogeneous compositions have the same property and sum to the corresponding power of N. Elevating the coordinate iterates to common degree `D=p^(M-1)` and taking their average gives a rational homogeneous H_D which equals `F_M/T` on the simplex, again with every Bernstein coefficient in `[0,1]`.

There must be **no forced pure-A coefficient equal to one** for this completeness argument: the acquired time average need not have that normalization. Nonnegativity and the upper box bound are sufficient for the subsequent stochastic estimates.

Because `v dot grad N=0`, homogenization does not change the tangential Lie derivative on the simplex. Consequently the homogeneous polynomial

    g=v dot grad H_D

is at least `delta/(2T)>0` on the whole face `A=0,N=1`.

## 5. Elementary coefficient elevation

Restrict g to the boundary variables, where it is homogeneous of degree `q=D+p-1`, and write its ordinary monomial coefficients as g_alpha. For integer `r>=q`, the normalized coefficient of `N^(r-q)g` at multiindex gamma is exactly

    sum_alpha g_alpha (gamma)_alpha/(r)_q.

The value at the corresponding simplex point is

    g(gamma/r)=sum_alpha g_alpha (gamma/r)^alpha.

There is a simple finite probability proof of a uniform difference bound. On r labeled objects with category counts gamma, the two monomial factors are probabilities of a specified category word under sampling without versus with replacement. Couple the two sampling procedures; they agree unless a repeated labeled object appears among q with-replacement draws. A union bound gives discrepancy at most `q(q-1)/(2r)` for each word. Therefore, with `S=sum_alpha |g_alpha|`,

    |normalized coefficient-g(gamma/r)|
       <=S q(q-1)/(2r)
       <=2S q(q-1)/r.

The proposed constant is conservative. A finite explicit r makes the latter error smaller than half the uniform positive minimum `delta/(2T)`. All boundary coefficients then become strictly positive.

Multiplying H_D by the matching power of N preserves its Bernstein box. Its top-order Lie derivative is multiplied by the same power of N, so it is a member of the claimed coefficient hierarchy. Classical positive-coefficient elevation/Pólya reasoning is an ordinary baseline; the displayed elementary bound is proved here rather than imported from an uninspected quantitative source.

This supplies eventual unbudgeted degree-search success, but its witness may be fantastically large. The degree `p^(M-1)`, its coefficients, and the later elevation are not materialized by merely writing this proof. Any actual implementation must distinguish this existence/termination recipe from the low-degree certificates it really executes, and must report finite-budget UNKNOWN honestly.

## 6. Exact converse via an invariant face

If a singleton closure misses A, its terminal support S is nonempty and disjoint from A. The simplex face supported in S is invariant under all sufficiently small Euler steps of the top-order field: channels with a source outside S vanish, and enabled channels cannot produce outside S by closure.

Any polynomial H attains a maximum at some y* on this compact face. Since `E_h(y*)` stays in the same face for small positive h,

    H(E_h(y*))<=H(y*),
    v(y*) dot grad H(y*)<=0.

But a strictly positive pure-boundary coefficient certificate would imply

    v(y*) dot grad H(y*)>=beta sum_j (y*_j)^(d+p-1)>0,

a contradiction. This converse does not need the coefficient box or homogeneity except to identify the proposed leading polynomial. The finite closed support is a checkable obstruction for **all degrees of this fixed-top-order strict boundary cone**.

## 7. Stochastic attenuation and essential scaling

Let `q0=d+p-2`. The leading generator polynomial has degree `q0+1`; all other exact terms have degree at most q0. With negative A-containing leading coefficient sum K and absolute remainder coefficient sum C_R,

    L_internal H_d >= beta sum_j B_j^(q0+1)-K A N^q0-C_R(N+1)^q0.

Use

    W=t^N[1-epsilon H_d/(N+1)^q0].

Because `p>=2`, `H_d<=N^d<=(N+1)^q0`, and the correction remains bounded between `1-epsilon` and one. A death correction is at most `epsilon d/N^(p-1)<=epsilon d/N`, so the earlier scalar death bound remains valid. The internal quotient is exact, and the pure-power inequality gives radial dissipation

    kappa=min(Ddeath/4,epsilon beta/[2^(2d+2p-3)m^(d+p-2)]).

The all-exponential stationary moments follow from this specific count-conservative, exact generator inequality, not from a generic fluid-stability theorem.

The power p matters. Catalyzing each quadratic internal channel by every species multiplies its entire discrete generator by exactly `N-2`. For the explicit boxed quadratic `H=2A(B+C)+BC`, the non-complex-balanced pair-conversion demo has leading drift `-3n^3` on `(4n,3n,3n)`, and its cubic lift has leading drift `-30n^4`. Dividing only by `(N+1)^2` creates an unpayable positive order-n-squared Lyapunov quotient there. Dividing by `(N+1)^3` reduces it to order n, which the acquired death absorption controls. The separate exact scaling-control script verifies these identities and both signs.

## 8. Restricted hierarchy, not a stability decision

A particularly simple full-WR stable counterexample is the all-rate-one network

    0<->A, A<->B, A<->C, 2B<->2C.

The top-order singleton closures are `{B,C}`, so the invariant-face obstruction rejects every degree. Nevertheless

    V=4^A 5^(B+C),       LV/V=3-A/4-(B+C)/5

is a direct conventional Foster proof. The top-order pair is exactly weight-neutral and lower-order channels restore the dissipative coordinate. Likewise earlier accepted higher-order-neutral certificates may remain valid when this new leading-only hierarchy fails. The sufficient architectures should be retained in parallel, not silently replaced.

For the particular opposing-pure-ray family, the nonsmooth inventory `A+eta min(B,C)` remains an ordinary explicit alternative, as proved in `MECHANISM_AND_COMPARATOR.md`. The polynomial hierarchy is an automatically acquired algebraic certificate language, not a claim that smooth high-degree polynomials are uniquely necessary.
