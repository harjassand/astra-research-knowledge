# Literal polynomial locality bookkeeping for the all-cold bootstrap

29 October 2026. Companion to ALL_COLD.md Section6. All constants below
depend only on the fixed spatial growth nu,D, fixed decay/Gevrey exponents,
and fixed filters. They do NOT depend on volume, temperature, local Hilbert
dimension, a Gibbs eigenvalue, or an unspecified large-energy spectral gap.
Real powers with fixed denominators can always be enlarged to integer
powers in the final polynomial. No support-volume norm is inferred.

## 1. The scaled shell class and finite moment orders

Use Hermitian anchored balls with a declared majorant

    ||A_x,r||<=J exp[-(r/ell)^alpha], ell>=1, 0<alpha<=1.   (S1)

Pairing or scalar vacuum subtraction costs at most a constant. The elementary
sum/integral estimate gives, for every fixed integer k,

    sum_r (1+r)^k exp[-(r/ell)^alpha]
       <=C_(k,alpha) ell^(k+1),                           (S2)

where C_(k,alpha) can be bounded with Gamma((k+1)/alpha) and finitely many
endpoint terms. In the actual bootstrap take

    p_F=D+2, B=4D+10, M=8D+24,
    K=ceil((M+B+2)/alpha_min)+4.                         (S3)

Products, overlap commutators, martingale localization, and the final
relative-defect sum require spatial moments of order at most M; deliberately
loose filter/moment bounds may use time moments up to K. All these orders
are fixed. The proof propagates the pointwise shell envelope (S1), so it
does not iterate a moment loss indefinitely. Equation(S2) acquires each
needed finite moment after an envelope update.

For the explicit Gevrey2 choices here the source native interaction is
finite range; ground flow gives exponent1/2; the downward/thermal band
filters give exponent1/4; sech averaging preserves it; the parent ground
flow gives exponent1/8. Products and finite weak parameter flows keep that
exponent with a scale adjustment. Thus alpha_min=1/8 is a possible common
lower exponent. For D3, (S3) reads p_F5,B22,M48,K580. These are proof
orders, not additional SW order or a numerical native-gate qualification.

## 2. A convolution constant independent of the large scale

Let

    F_ell(r)=(1+r)^(-p_F) exp[-(r/ell)^alpha].             (S4)

Its summability and convolution constants obey

    sup_x sum_y F_ell(d(x,y)) <=2nu,
    sum_z F_ell(d(x,z))F_ell(d(z,y))
                            <=2^(p_F+2)nu F_ell(d(x,y)). (S5)

For the first inequality one can overcount the radius-r sphere by the
whole ball nu(1+r)^D, leaving sum_r(1+r)^(-2)<=2. For the second, use
d(x,y)^alpha<=d(x,z)^alpha+d(z,y)^alpha. At least one of the two distances
is >=d(x,y)/2; its polynomial denominator supplies2^p_F/(1+d(x,y))^p_F,
and summing the other polynomial denominator gives (S5). In particular
these constants do not become exp(ell) or exp(ell^D).

Convert a ball-profile interaction (S1) to the usual pair F norm. A ball
containing x,y has radius r>=d(x,y)/2 and at most nu(1+r)^D anchors.
Split its exponential into two equal factors, reserve one for distance,
and use (S2) for the root-count and polynomial factors. At scale

    ell_F=2*2^(1/alpha) ell

this gives

    ||A||_F <=C J ell^(D+p_F+1)=C J ell^(2D+3).          (S6)

The usual LR proof therefore gives a velocity parameter bounded by

    v<=C J ell^(2D+3).                                   (S7)

Any extra polynomial factors from Haar conditional expectations can be
overpaid by B in (S3). All estimates are in operator norm; no sum over a
local matrix basis or a dimension-dependent Hilbert--Schmidt inequality
appears in this conversion.

## 3. Filtering: explicit scale update rather than a free constant

Suppose A has envelope (J_A,ell_A,alpha_A), H has
(J_H,ell_H,alpha_H), and |f(u)|<=C_f exp[-(|u|/T)^zeta].
Set alpha=min(alpha_A,alpha_H), ell=max(ell_A,ell_H,1), and use v from
(S7). Conditional-expectation LR bounds, clipped by2||A||, then splitting
the time integral at u_c=c(r/ell)^alpha/(1+v), give a bound with output
exponent alpha*zeta and scale

    ell_out<=C ell[1+(1+v)T]^(1/alpha).                  (S8)

For completeness the two tail contributions are a fixed polynomial in
r,ell times exp[-c(r/ell)^alpha], and a fixed polynomial times
C_f T exp[-c{(r/ell)^alpha/((1+v)T)}^zeta]. The latter follows by a direct
tail integral of the time envelope. Absorb powers of r by halving their
exponential coefficient and applying (S2). A deliberately loose amplitude
update is

    J_out<=C J_A C_f(1+T)
                    [1+ell+ell_out+v+T]^B.              (S9)

Equations(S7)--(S9) are literal finite polynomial/algebraic updates, with
fixed exponents; they never exponentiate vT. An exponentially small factor
in J_A or C_f is retained LINEARLY before the polynomial update. The
normalized sech kernel has C_f=2/t,T=O(t),zeta1; using C_f<=2 for t>=1
is harmless. Thermal band filters have T=O(1+t), a fixed zeta=1/2 and
the amplitude factors in ALL_COLD Section5. The fixed ground-flow filter
has T=O(c^-1) and finite moments polynomial in c^-1.

The version with an arbitrary finite input shell radius is obtained by
first splitting that radius at r/2 and summing its own (S1) tail. It only
changes C and B. The input operator can be one rooted term or an interaction
evolved term by term. Thus there is no hidden sum over all volume anchors.

## 4. Products, commutators and the weak parameter flow

For two anchored balls of radii r,s, a commutator vanishes unless their
centers are at distance<=r+s. Assign the output to the first anchor; its
support lies in a ball of radius r+2s, and there are <=nu(1+r+s)^D possible
second anchors. Reserve part of the two exponential tails for that output
radius, then sum the remaining tails by(S2). This yields the conservative
finite updates

    alpha_out=min(alpha_A,alpha_B),
    ell_out<=C max(ell_A,ell_B),
    J_out<=C J_A J_B[1+ell_A+ell_B]^B.                   (S10)

The same bound, without the anchor overlap count, handles rooted products.
The onsite commutator with a number projector simply costs its declared
support volume, also within the finite moments(S3).

For the bootstrap path H(s)=H0+sV, all H(s) have a common (J,ell,alpha)
envelope up to a fixed factor. Filtering V by the fixed-gap flow filter
uses(S8)--(S9), giving an interaction generator with amplitude

    epsilon P1(J,ell,c^-1), scale ell1<=P2(J,ell,c^-1).    (S11)

Both P1,P2 are explicit finite compositions of (S7)--(S10) and the fixed
filter moment bounds. Its own LR velocity during parameter time s∈[0,1]
is at most epsilon C P1 ell1^(2D+3). Include that polynomial in the
smallness gate, so this velocity is<=1. The exponential LR factor for
this PARAMETER flow is then bounded by exp(1), rather than exp(poly(t)).
Conjugating V+[G_s,H(s)] retains a linear epsilon factor and polynomial
amplitude/range by(S10) and this bounded-velocity LR estimate. Integrating
over s of length1 gives precisely the interaction majorant claimed for
D(s) in ALL_COLD Eq(15). A possible scalar vacuum subtraction costs2.

There is no circular epsilon-independent exponential hidden here: the
native parent real-time velocity is polynomial and is clipped in(S8);
the parameter-flow velocity is SMALL because its generator is linear in
epsilon and we explicitly impose epsilon times a larger polynomial<=1.

## 5. Explicit polynomial into the relative-defect estimate

Let the preceding steps give amplitude epsilon J_D and scale ell_D,
with fixed exponent alpha_D>=alpha_min. The vacuum-CP martingale has
radial term bounds at most4 times the original rooted tail. At a fixed
cell, the number of possible anchors at radius r is<=nu(1+r)^D. The
remaining relative-form coefficient is bounded by

    4nu epsilon J_D sum_r(1+r)^(2D+2)
                              exp[-(r/ell_D)^alpha_D]
       <=C epsilon J_D ell_D^(2D+3).                    (S12)

This overpays both anchor/root localization counts. The exponent2D+2 is
less than M of(S3). Therefore a concrete choice for the stability polynomial
is the SUM of the weak-flow gate in(S11) and C J_D ell_D^(2D+3), enlarged
to include the finite moment and overlap constants above. J_D,ell_D are
the finite compositions(S7)--(S11); no unspecified function of temperature
or a dimension-dependent operator basis is left. The numerical coefficients
have NOT been evaluated for the native clock catalog.

If the all-cold input bounds give epsilon_t P(t)<=C0(1+t)^k exp(-t/4),
one may choose the entirely explicit final gate

    T0=max{1,64(k+1)^2,8 ceil(log2(4C0/c))}.              (S13)

Indeed log(1+t)<=sqrt(t): write x=sqrt(t) and differentiate
x-log(1+x^2), whose derivative is (x-1)^2/(1+x^2)>=0. For t>=T0,
k log(1+t)<=t/8 and log(4C0/c)<=t/8. This proves epsilon_t P(t)<=c/4
for EVERY real t>=T0, not merely at a sampled temperature grid.

The conclusion is a computable all-temperature gate from the derived
interaction/filter envelopes. It remains UNEVALUATED for the literal
native recipe. No additional finite Hamiltonian or quantum state has been
used as a substitute for these all-volume estimates.
