# Independent audit: strict three-root moment map

Scope: audit the strict three-root Jacobian, its local inverse, finite
two-mass realization, and the global moment-image argument in
`FIRST_FAMILY_CONSTRUCTION.md` and `FAMILY_THEOREM.md`. This is a proof audit,
not an independent reproof of every spectral resource theorem.

## Jacobian and orientation

Let the three simple roots be `x1<x2<x3` and assume the sign pattern
`F<0,+,-,+` across the four intervals. Thus
`epsilon=(+1,-1,+1)` and `sign(F'(xi))=epsilon_i`. The two moments are

`ell=ln(x1)+ln(x3)-ln(x2)`,
`A=x1^2+x3^2-x2^2`.

Implicit differentiation of `F(xi)=0` gives

`dxi=-(d lambda+2 xi^2 d mu)/F'(xi)`.

Consequently, with `u_i=(1/xi,2xi)^T` and `w_i=epsilon_i xi/F'(xi)>0`,

`D_(lambda,mu)(ell,A) = -sum_i w_i u_i u_i^T`.

The constants and signs in the supplied formula are correct. For any
nonzero `v=(v_lambda,v_mu)`,

`v^T J v = -sum_i w_i (v_lambda/xi+2 xi v_mu)^2 < 0`.

Strictness follows because two distinct roots make the two linear forms
linearly independent. Hence `J` is negative definite and nonsingular. Its
two-dimensional determinant is positive; explicitly,

`det(J)=4 sum_(i<j) w_i w_j (xj^2-xi^2)^2/(xi^2 xj^2) > 0`.

The map is locally analytically invertible wherever the roots remain simple.
The inverse derivative is `J^(-1)`; this proves finite local conditioning at
each strict point, not a uniform condition-number bound near boundary or
degenerate resource limits.

## Unit convention

There is one notation correction for the global map statement. If `xi` are
dimensional frequencies, `ln(x1 x3/x2)` is not dimensionally defined and
`exp(2 ell)` cannot equal a dimensional `B=4K/M`. The result is unchanged
after making the frequency normalization explicit. At fixed `theta`, set
`zi=xi/theta`, `ell_bar=ln(z1 z3/z2)`, and
`A_bar=(x1^2+x3^2-x2^2)/theta^2`. Then

`exp(2 ell_bar) = (4K/M)/theta^2`,
`A_bar = (4K/m0)/theta^2`,

and the image cone is `A_bar>exp(2 ell_bar)>0`. Equivalently, choose any
fixed reference frequency in place of `theta` and scale both moment
coordinates by it. In these dimensionless variables the same Jacobian formula
holds with roots `zi` and dimensionless dual variables
`lambda/theta`, `mu*theta`.

## Exact positive two-mass realization

For any three ordered positive frequencies `b<a<c`, define

`A=b^2+c^2-a^2`, `B=b^2 c^2/a^2`.

Then

`A-B=(a^2-b^2)(c^2-a^2)/a^2>0`.

Given any backbone lower bound `m0>0`, set

`K=m0 A/4`, `M=m0 A/B`,
`M_side=m0(A-B)/B`
`=m0(a^2-b^2)(c^2-a^2)/(b^2c^2)`,
`k=a^2 m0 M_side/M`.

All are finite and positive. For the within-cell two-mass spring matrix
`k[[1,-1],[-1,1]]` with mass matrix `diag(m0,M_side)`, the squared
frequencies at `q=0` are `0,a^2`. At `q=pi`, mass normalization adds
`4K/m0=A` to the backbone diagonal. The two resulting squared frequencies
have sum `a^2+A=b^2+c^2` and product
`(4K/m0)(k/M_side)=4K a^2/M=B a^2=b^2c^2`. They are therefore exactly
`b^2,c^2`, and the passbands are `[0,b] U [a,c]`.

This realization formula applies to any ordered positive triple. For
temperature-optimality, the triple must additionally be the roots of the
corresponding dual `F`; arbitrary triples need not satisfy that root
condition.

## Global image and boundary

For each fixed positive `theta`, Sections 4–9 of `FAMILY_THEOREM.md` give an
attainable one-resonator curve for every physical pair `A_phys=4K/m0` and
`B_phys=4K/M` with `A_phys>B_phys>0`. The finite interior minimum exists;
each stationary member supplies the three-root dual; the root-count/sign
argument makes that dual globally certifying. The strict certificate also
forces equality of any second optimum's band indicator, so the optimum
spectrum and its root triple are unique.

These facts support surjectivity of the strict moment map onto the
dimensionless cone `A_bar>exp(2 ell_bar)>0`. The same strict optimality
certificate supports injectivity: two dual pairs with the same moments
certify the same physical resources and hence the same unique optimal
passbands; those passbands determine the three ordered roots, and two roots
then determine `lambda,mu` uniquely. Combined with the nonsingular Jacobian,
the bijection and its analytic inverse follow.

There is no missing interior resource region in this argument. The sharp
finite-resource boundary is `A_phys=B_phys`, equivalent to `M=m0` and
`M_side=0`; it is excluded by the strict positive-side-mass/three-root
assumptions. `B_phys=0` is another non-finite limit, not an interior point.
The proof gives no uniform conditioning estimate as these boundaries are
approached.
