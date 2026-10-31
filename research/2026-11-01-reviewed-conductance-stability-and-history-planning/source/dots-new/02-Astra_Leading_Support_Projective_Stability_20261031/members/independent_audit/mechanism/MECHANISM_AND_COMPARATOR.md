# Pending polynomial-angular mechanism: independent derivation and comparator

This file concerns a new pending extension. It does not alter or inherit acceptance from any earlier package. All assertions below are ordinary mathematical derivations; no general stability completeness or novelty is claimed.

## 1. Raw mediated pair-conversion family and all-rate quadratic witness

Use rates

    2B -> B+C : p,       B+C -> 2B : q,
    B+C -> 2C : r,       2C -> B+C : s,
    B+C -> A+B : u,      A+B -> B+C : v,

with all six rates positive, and the open core `0->A` at lambda and `A->0` at delta. Internal channels conserve `N=A+B+C`.

Let

    H=A N+eta BC,
    eta=min(1, u/[2(p+q+u)], u/[2(r+s)]).

Its degree-two Bernstein coefficients are `(c_AA,c_AB,c_AC,c_BB,c_BC,c_CC)=(1,1/2,1/2,0,eta/2,0)`, all in `[0,1]`. The leading cubic part of `L_internal H` has coefficients

    B^3: eta p,                   C^3: eta s,
    B^2 C: u+eta(-p-q+r-u),
    B C^2: u+eta(q-r-s),
    A^2 B: -v,
    A B^2: -v(1-eta),
    A B C: u-v.

The two mixed boundary coefficients are at least `u/2`, and the pure boundary coefficients are positive. Thus the proposed degree-two cone contains a positive certificate for every positive rate choice, with `beta=eta min(p,s)`.

The exact lower-order remainder is

    eta[-2p B^2-2s C^2+(p-q-r+s)BC+pB+sC].

In particular, a coefficient-absolute-value bound is

    C_R=eta[3p+3s+abs(p-q-r+s)].

The negative A-containing leading coefficients sum to

    K=v(2-eta)+max(0,v-u).

All of these formulas are finite raw-rate computations.

## 2. The general degree-d construction is sound algebraically

Let `d>=1`, and write the homogeneous polynomial in multinomial/Bernstein coordinates:

    H_d(x)=sum_(|alpha|=d) binom(d,alpha)c_alpha x^alpha,
    c_(d e_A)=1,  0<=c_alpha<=1.

These coefficient bounds imply `0<=H_d<=N^d`, nonnegative coordinate increments, and `partial_A H_d<=d N^(d-1)`.

For a finite conservative unary/binary internal reaction list, `L_internal H_d` is a polynomial of degree at most `d+1`. Its exact leading part `G_(d+1)` is linear in the unknown coefficients. If every boundary coefficient is nonnegative and each pure satellite coefficient is at least beta positive, then

    G_(d+1)>=beta sum_j B_j^(d+1)-K A N^d,

where K is the sum of absolute values of its negative A-containing coefficients. Each such monomial is at most `A N^d`. If the sum of absolute coefficients of the lower-degree remainder is `C_R`, that remainder is at least `-C_R(N+1)^d` for every nonnegative integer state.

For rational `t>1`, put

    D=delta(1-1/t),
    epsilon=min(1/2,D/(4K)) if K>0, else 1/2,
    h=1-epsilon H_d/(N+1)^d,     W=t^N h.

Then `1-epsilon<=h<=1`. Conservation gives the exact internal quotient

    L_internal W/W=-epsilon L_internal H_d/[(N+1)^d h].

Immigration contributes at most `lambda[t/(1-epsilon)-1]`. For an A death at `A>=1`,

    h(x-e_A)-h(x)
       =epsilon[H_d(x)/(N+1)^d-H_d(x-e_A)/N^d]
       <=epsilon[H_d(x)-H_d(x-e_A)]/N^d
       <=epsilon d/N.

After multiplication by `delta A/[t h]`, the positive death correction is at most `delta epsilon d/[t(1-epsilon)]`. The negative exponential death term is `-D A`. This proof also covers N one; at N zero death is absent.

Combining these inequalities gives

    LW/W <= C0-(D/2)A-epsilon beta b^(d+1)/[m^d(N+1)^d],
    C0=lambda[t/(1-epsilon)-1]
          +delta epsilon d/[t(1-epsilon)]
          +epsilon C_R/(1-epsilon),

where `b=sum_j B_j` and `m` is the number of satellites. For N at least one, split `A>=N/2` versus `b>N/2`. In the second case,

    b^(d+1)/(N+1)^d >= N/2^(2d+1).

Thus the proposed positive radial dissipation

    kappa=min(D/4,epsilon beta/[2^(2d+1)m^d])

is valid. At N zero the immigration contribution is also bounded by C0. Standard explicit Foster constants and the earlier stopped-semigroup moment argument then apply. No stationary-fiber premise appears.

The univariate notation `d` must not simultaneously denote polynomial degree and the death rate; this note uses delta for the latter.

## 3. Cone acquisition and nesting

At fixed degree, all coefficient constraints are finite rational affine inequalities. Choose any explicit finite upper bound on beta obtained from the sum of absolute coefficients in the raw pure-boundary rows (and one if needed). This cannot exclude positivity. All coefficients one give `H_d=N^d` and internal generator zero, so beta zero is feasible. The polytope is compact; exact nonsingular active-basis enumeration therefore decides positivity just as in the earlier linear-coefficient cone. Finite work budgets must still return UNKNOWN, and input-size guards should precede generating large monomial/constraint lists.

Multiplication by N preserves the normalized coefficient bounds. Explicitly, the new coefficient at multiindex gamma is

    c'_gamma=sum_i gamma_i/(d+1) * c_(gamma-e_i).

This is a convex average and the pure-A coefficient remains one. Since internal reactions conserve N,

    L_internal(N H_d)=N L_internal H_d.

The leading polynomial is multiplied by N. Boundary signs and positive pure-ray coefficients are preserved. Hence positive-cone feasibility is nested by degree; this is a mathematical nesting claim, not an efficient computation claim.

The hierarchy remains incomplete for recurrence at every degree. For the stable unary network `0<->A, A<->B`, there is no degree-`d+1` internal leading term at all. Every member of this hierarchy has beta zero even though a conventional exponential Foster function exists. No general-WR or arbitrary-stability completeness follows from nesting.

## 4. A simpler nonsmooth ordinary comparator must be retained

The new family does not require a polynomial degree-two correction uniquely. Define the mediator-inventory function

    P=A+eta min(B,C),
    S=u+p+q+r+s,
    eta=min(1/2,u/(2S)),
    beta=eta min(p,s)/2.

This P is piecewise linear, satisfies `A<=P<=N`, increases exactly one under A immigration and decreases exactly one under A death. We claim

    L_internal P >= beta[(B)_2+(C)_2]-v A N.             (*)

Write `b=B,c=C` and consider three integer regions.

**b>=c+2.** The dominant `2B->BC` reaction increases min by one. Retain its positive contribution and discard other positive terms. The minority adverse quadratic contribution satisfies `(c)_2<=bc`, giving

    L_internal P >= eta p(b)_2
          +[u-eta(u+q+s)]bc-vab
       >= eta p(b)_2-vab.

Also `(b)_2+(c)_2<=2(b)_2`, yielding (*).

**c>=b+2.** Symmetrically retain the `2C->BC` contribution:

    L_internal P >= eta s(c)_2
          +[u-eta(r+p)]bc-vab
       >= eta s(c)_2-vab.

Now `(b)_2+(c)_2<=2(c)_2`, again giving (*).

**abs(b-c)<=1.** Every pair-conversion increment of min is at least minus one. The `BC->AB` weighted increment is at least `1-eta`, and the reverse increment is at least minus one. Here `(b)_2,(c)_2<=bc`, so

    L_internal P >= [u-eta S]bc-vab
       >= (u/2)bc-vab
       >= beta[(b)_2+(c)_2]-vab,

because `beta<=u/4`. Finally `ab<=aN` proves (*).

Consequently the already established normalized-P proof applies with `K2=v,K1=0`:

    W=t^N[1-epsilon P/(N+1)]

has a global negative-linear radial quotient bound and all finite exponential stationary moments. No smoothness of P is required: the internal quotient identity uses its exact discrete generator, not derivatives.

This is an ordinary completed finite-region proof. It does not make the acquired polynomial cone unsound, but it limits the claim of conceptual necessity: the polynomial hierarchy is one automatic smooth algebraic certificate language; a simpler explicit nonsmooth mediator-inventory function also resolves this particular network.

## 5. Precise obstruction to the old linear-coordinate family

For `P=A+v_B B+v_C C`, the internal weighted drift at pure B is proportional to `v_C-v_B`, while at pure C it is proportional to `v_B-v_C`. Strict positive pure-boundary production cannot hold on both rays. Even allowing nonnegative coefficients forces `v_B=v_C`; then all internal drift at either pure ray is invisible, while the bounded normalized correction's immigration quotient tends to `lambda(t-1)>0`. Thus the earlier bounded normalized linear-weight ansatz cannot yield global geometric Foster drift for this family.

The stronger aggregate no-go also transfers. At pure B, a putative positive normlike geometric Foster function `F(A,N)` obeys the same immigration inequality as previously. At `(1,n-1,0)`, the `AB->BC` channel loses A at rate `v(n-1)` and its destination has value `F(0,n)`; other internal channels preserve A,N. Dropping positive core destination terms produces the same scalar contraction contradiction. This statement requires that the compared states belong to the specified class; globally it is immediate, and a classwise formulation should explicitly supply the corresponding connecting paths rather than assume them.

No impossibility for all joint, nonsmooth, sampled-time, excursion, or additive Lyapunov methods is claimed. The nonsmooth comparator above is a constructive counterweight to any such overstatement.
