# Finite rational-Poisson minimum atlases do not suffice

29 October 2026. New internal structural obstruction, not independently reviewed. This is not a counterexample to chemical recurrence. It rules out a specific broad proposed certificate class, even with exact minimum patching.

## Network

Use two abstract species A,B and the directed four-complex cycle

    y0=(0,72) --2--> y1=(3,60) --1--> y2=(5,36)
           --1--> y3=(6,0) --1--> y0.

It is weakly reversible. Rates are stochastic mass action k_i (x)_{y_i}. No physical implementation or biological experiment is proposed.

## Claimed obstruction

For this network there is no positive tail measure of the form

    mu(A,B)=min_{ell=1,...,L}
       [a_ell R_ell(A,B) c_{ell,A}^A c_{ell,B}^B/(A!B!)]

with finite L, fixed positive a_ell and c_{ell,A},c_{ell,B}, and positive rational functions R_ell, that satisfies L*mu<=0 outside a finite set on the full state space. Rational functions are assumed defined, finite and positive on the sufficiently large integer points under discussion. The same obstruction applies on any communicating class containing the large sublattice described below.

The failure includes constant prefactors (R=1), arbitrary finite rational corrections, and exact selector-aware minimum patching. It does not include arbitrary nonlinear envelopes, an infinite atlas, state-dependent bases, or rational functions with inadmissible poles/zero values.

## 1. Exact Poisson-base adjoint defect

For mu_c(x)=c^x/x!, the adjoint ratio is exactly

    L*mu_c(x)/mu_c(x)=sum_i d_i(c)(x)_{y_i},
    d_i(c)=k_{i-1} c^{y_{i-1}-y_i}-k_i,

with cyclic indices. Hence

    sum_i c^{y_i} d_i(c)=0.                         (1)

If every d_i(c)<=0, (1) and positivity force every d_i(c)=0, which is exactly complex balance around this directed cycle.

## 2. All four necessary inequalities occur in the same ordering sector

Along logarithmic rays A=t^u, B=t^v, u>v>0, the source monomial exponents divided by v are

    72, 3r+60, 5r+36, 6r, where r=u/v>1.

The unique maximizer is respectively y0, y1, y2, y3 on the four nonempty open intervals

    (1,4), (4,12), (12,36), (36,infinity).           (2)

Thus every complex is uniquely exposed along a ray in which A grows strictly faster than B.

## 3. Every finite atlas uses the same base throughout these rays

Let c_* be the lexicographically smallest pair (c_A,c_B) among the finitely many bases. On every ray with u>v>0, the exponential ratio of any base with larger c_A to c_* tends to infinity faster than every rational function; if c_A ties and c_B is larger, the B exponential has the same property. Therefore only candidates having the same base c_* can attain the minimum at large t, both at x and at any of its finitely many fixed reaction shifts.

Choose a rational exponent ratio inside each interval in (2), avoiding the finitely many Newton-weight ties of all numerators and denominators of the R_ell. Write u=p,v=q with positive integers p>q and use integer points A=n^p,B=n^q. Each rational function then has one leading monomial on that ray and satisfies

    R_ell(x+z)/R_ell(x) -> 1

for every fixed integer vector z. The same ratio property holds for the minimum of finitely many positive such functions: bound each shifted function between (1-o(1)) and (1+o(1)) times its unshifted value, then take the minimum.

Consequently the actual atlas measure satisfies

    mu(x+z)/mu(x)=[mu_{c_*}(x+z)/mu_{c_*}(x)](1+o(1))

on each chosen ray. Exact bounded shifts of falling factorials have the same leading monomials. At a ray uniquely exposing y_i, the leading adjoint coefficient is therefore d_i(c_*). Eventual L*mu<=0 forces d_i(c_*)<=0. All four inequalities follow from (2).

This argument does not incorrectly require a single rational correction to remain the minimum at neighboring states: the finite minimum itself has the needed shift-ratio property.

## 4. Contradiction to the rate cycle relation

The four complexes have the affine integer relation

    y0-3y1+3y2-y3=0,
    1-3+3-1=0.

Complex balance would make F_i=k_i c^{y_i} equal for all i. Taking the product with powers (1,-3,3,-1) would then give

    1=F0 F2^3/(F1^3 F3)=k0 k2^3/(k1^3 k3)=2,

a contradiction. Thus the finite atlas cannot be an eventual dual supersolution.

## Communicating-class version

The first two reaction vectors are nu0=(3,-12) and nu1=(2,-24). They generate

    2nu0-nu1=(4,0),
    2nu0-3nu1=(0,48).

Weak reversibility realizes each negative reaction vector by a fixed finite return path. Therefore both signs of these two sublattice moves are executable whenever the population has a sufficiently large fixed buffer. Their finitely many paths have bounded excursions. A single communicating class consequently contains all sufficiently large points in one translated (4Z)x(48Z) sublattice, connected by these coordinate moves without leaving the buffered region. Taking n to be sufficiently large multiples of 48 places all four families of generic integer rays in that same class (choose the untranslated large sublattice class). The coefficient contradiction therefore is not merely an artifact of combining unrelated communicating components.

## Consequence for the multidimensional program

The minimum-patching inequality itself is valid. The unavailable step is acquiring local envelopes with the correct selector regions. A finite family of fixed Poisson bases cannot adapt to distinct logarithmic monomial-dominance regimes that share one ordering of coordinate growth. Rational prefactors do not alter this failure. More adaptive geometry or a genuinely different positive resolvent representation is required; deterministic inward geometry by itself does not provide such an atlas.
