# Fresh reconstruction of the finite-energy logarithmic-tail entropy bridge

24 October 2026, Brisbane. W49. Exact target, read completely:

`work/workers/w38_fresh_inventory_critic/new_independent_epni_invention/FINITE_ENERGY_LOG_TAIL_ENTROPY_BRIDGE.md`,
SHA256 `2167da8029a740a937b5ae477a1bf984fd34d4f9b6c02ce001ee02c8bc191e6e`.

I also reopened the stated scalar dependency
`ARBITRARY_COVARIANCE_EXPONENTIAL_TAIL_HEAT_CLOSURE.md`, SHA256
`d0e95b062c7b6c3c02ff512fc2e17f0c41866444ec58a8bda0eb079fa7ce0334`,
especially Sections 3 and 5. Only its scalar entropy-target facts are
needed and are rederived below. I do NOT import its exponential-energy
source premise, moment expansion or multi-mode Gaussian theorem. No
other worker's verdict or numerical radial data was used as a premise.

**Verdict:** L2 and L3 reconstruct without a blocking mathematical defect,
under their precise supplied tail assumptions and actual heat. One
NONESSENTIAL literal sentence in Section 6 is false as written: a fixed
temperature shift need not change the relative density by `O(1/r)` when
the remainder is merely continuous `o(1/log r)`. An exact counterexample
is given in Section 9 below. The sufficient and valid statement is that
a fixed shift preserves the two-term expansion, with an `o(1/log r)`
remainder. With this explicit local correction, all the claimed
coefficients, normal quantum transfer and eventual positive gap follow.
The frozen source should be preserved and the correction recorded in a
separate mandatory clarification. No unheated/general finite-energy,
source-uniform threshold, novelty or hardware result follows.

All entropies and relative entropies below use NATURAL logarithms. An
entropy gap measured in bits is divided by `ln 2`.

## 1. Class, normalization and finite-entropy identities

Let the body of the probability law of R be arbitrary on a bounded
interval, and beyond some fixed r0 have continuous density

    f_R(r)=C r^-2 (ln r)^-p
              [1+d/(ln r)+epsilon(r)/(ln r)],
    C>0, p>1, epsilon(r)->0.                         A1

In particular the asymptotic error is uniformly small beyond a chosen
cutoff. The mean `a=ER` is finite, while `ER^(1+eta)` is infinite for
every eta>0. The body and its atoms are included in all normalizations.
An atom at zero causes no difficulty after positive heat.

Write `K_v(r)=v^-1 exp(-r/v)` for v>0. The actual heated thermal mixture
has coherent-amplitude squared-radius law

    h_t(r)=E K_(t+R)(r),
    q_t(r)=K_(t+a)(r), t>0.

These are normalized probability densities. Their radial KL is the same
as the full circular complex-amplitude KL. Convexity of KL, evaluated on
the exponential-radius laws, gives the useful GLOBAL finite bound

    D_cl(h_t||q_t)
      <= E[(t+R)/(t+a)-1-ln((t+R)/(t+a))]
       = ln(t+a)-E ln(t+R)
      <= ln(1+a/t) < infinity.                      A2

Log integrability follows from `ln(t+R)<=ln t+R/t`, so A2 uses only
finite mean. It licenses the positive integrand

    Phi(h,q)=h ln(h/q)-h+q >=0

without a difference of infinite entropy integrals or a global L2 norm.
The quantum states are normal, phase-invariant, unflagged thermal
mixtures with finite mean and finite entropy. For the thermal reference
of the same mean, its logarithm is affine in photon number. Thus exactly

    D_q(H_t rho_R || tau_(t+a))=g(t+a)-S(H_t rho_R),
    g(n)=(n+1)ln(n+1)-n ln n.                       A3

All terms in A3 are finite. This is an actual quantum relative entropy,
not the entropy of an accessible temperature flag.

## 2. Pre-crossover control and the retained omitted mean

Set `l=ln t`, `Y=l+(p+2)ln l`, `X=tY`, and fix delta in (0,1).
Elementary integration of A1 gives

    P(R>delta t)=O(t^-1 l^-p),
    E[R;R>delta t]=O(l^(1-p)),
    E[R^2;R<=delta t]=O(t l^-p).                   A4

The last assertion is a TRUNCATED second moment, not an assumed full
second moment. For example split its tail integral at sqrt(t); the
upper part is bounded by a constant times `t l^-p`, and the lower part
is smaller. The bounded body contributes a fixed finite constant.

Rescale `r=ty` and use

    k_x(y)=(1+x)^-1 exp[-y/(1+x)],
    H_t(y)=E k_(R/t)(y), Q_t(y)=k_(a/t)(y).

Taylor through first order on x in [0,delta] has remainder bounded by
`C x^2(1+y)^2 exp(-cy)`, `c=1/(1+delta)>1/2`.
The small-temperature contribution, minus the reference expansion, is

    -P(R>delta t)k_0(y)
    -E[R;R>delta t] k'_0(y)/t
    + the two Taylor remainders.

The SECOND term is retained. Omitting it would wrongly replace the full
matching mean by the truncated mean. The remaining large-temperature
integral has, from A1, the uniform upper bound

    C t^-1 l^-p integral_delta^infinity
          x^-3 exp(-c_delta y/x) dx
      <= C t^-1 l^-p (1+y)^-2.                    A5

Here `1+x` and x are uniformly comparable for x>=delta. For y>=1 use
the substitution y/x; for y<=1 use the total integral. Combining A4-A5
with the first-order centering yields the source's L5, uniformly in y:

    |H_t-Q_t| <= A_t+B_t,
    A_t=C t^-1 l^(1-p)(1+y)^2 exp(-cy),
    B_t=C t^-1 l^-p(1+y)^-2.                      A6

The reference's `O(t^-2)` term is smaller than A_t for each fixed p.
Also `Q_t>=c0 exp(-y)` for all large t. The pointwise inequality
`Phi(h,q)<=(h-q)^2/q` therefore gives

    integral_0^Y Phi(H_t,Q_t)dy
      <= C t^-2 l^(2-2p)
          +C t^-2 l^(-2p) integral_0^Y e^y/(1+y)^4 dy
      <= C t^-2 l^(2-2p)+C t^-1 l^(-p-2)
       =o(t^-1 l^-p).                              A7

The first integral converges because `2c-1>0`; its polynomial is
harmless. For the second integral split at Y/2. The last half is bounded
by `C e^Y/(1+Y)^4`, and the first is smaller by an exponential factor.
The denominator fourth power is essential: dropping it destroys the
claimed borderline order. A7 is LOCAL to the pre-crossover range and
does not imply finite global chi-squared divergence.

## 3. Uniform entropy heat removal in the remote region

Define h0 away from zero using the unheated kernels, omitting only a
possible delta mass at the origin. It need not be a globally normalized
ordinary density; it will be used ONLY for r>=X.

Restricting the temperature integral to R in [r,2r] gives common lower
bounds `c r^-2(ln r)^-p` for h_t and h0 there. The upper bounds are
`h_t<=1/t` and `h0<=1/(er)<=C/t`. The same holds for every positive
convex combination of the two. Since

    r/t >= ln r for r>=X and large t,

these lower/upper bounds show that the absolute log-ratio to q_t is at
most `C r/t` throughout that segment. The mean-value theorem in h,
whose derivative is `ln(h/q_t)`, reduces the entropy replacement error
to

    C integral_X^infinity (r/t)|h_t-h0| dr.         A8

I independently reconstructed each of its three temperature ranges.

SMALL, `R<=t/l^2`: the heated kernel is bounded by
`t^-1 exp[-r/(t(1+l^-2))]`. The unheated kernel is bounded by its value
at `R=t/l^2`, since r exceeds that temperature, namely
`(l^2/t)exp(-r l^2/t)`. After r=ty, A8 is bounded by
`C Y exp[-Y/(1+l^-2)]=O(t^-1 l^(-p-1))`, with a negligible unheated term.
The factor `exp[O(Y/l^2)]` is bounded and tends to one.

MEDIUM, `t/l^2<R<=delta t`: its probability is
`O(t^-1 l^(2-p))`. Its two kernels are bounded by
`t^-1 exp(-cr/t)` and `(delta t)^-1 exp[-r/(delta t)]`.
The A8 contribution is at most
`C t^-1 l^(2-p)Y exp(-cY)=o(t^-1 l^-p)`.
The extra factor `exp(-cY)=t^-c` dominates every fixed logarithmic power.

LARGE, `R>delta t`: differentiate K_(R+u) in u and use
`R<=R+u<=(1+1/delta)R`. Then

    |K_(R+t)(r)-K_R(r)|
       <=C_delta t R^-2(1+r/R)exp(-c_delta r/R).

Multiplying by the tail density and putting R=rv gives

    |h_t^large-h0^large|
      <= C t r^-3(ln r)^-p.                        A9

For completeness, the logarithmic weight is uniform: if R,r>=e,

    [(ln R)/(ln r)]^-p
       <=C_epsilon max((R/r)^epsilon,(R/r)^-epsilon).

For R<=r, write `ln r=ln R+z`, use `ln R>=1` and
`(1+z)^p<=C_epsilon exp(epsilon z)`. For R>=r it is immediate.
With epsilon<1, the remaining integral of
`v^-4(1+1/v)exp(-c_delta/v)` times these powers is finite at both ends.
All temperatures in this range exceed the eventual-density cutoff for
large t, so no unaccounted body atoms enter A9. Its A8 contribution is
`O(X^-1(ln X)^-p)=O(t^-1 l^(-p-1))`.

Thus L9 is valid with an error `o(t^-1 l^-p)`. This is a direct remote
estimate, not a presumed inverse heat map or entropy continuity under
an uncontrolled infinite-dimensional norm.

## 4. Mellin coefficient, with a rigorous second-order remainder

Let `Lr=ln r`. The bounded-temperature body is exponentially small at
large r. For the continuous tail, the positive substitution z=r/R gives

    h0(r)=C r^-2 integral z e^-z [ln(r/z)]^-p
                  [1+d/ln(r/z)+epsilon(r/z)/ln(r/z)] dz.

A concrete way to justify the expansion is to split at
`z=r^-1/2` and `z=r^1/2`. In the middle,
`|ln z|<=Lr/2`, so Taylor's remainder is bounded by a constant times
`(ln z)^2/Lr^2`; its weighted integral is finite. Also
`sup_(R>=sqrt r)|epsilon(R)|->0`, controlling its remainder by `o(1/Lr)`.
The small-z complement has an integrable polynomial bound and mass of
order a negative power of r. The large-z complement has the e^-z bound;
the logarithmic-weight comparison from Section 3 controls its remaining
factor. The bounded body is handled separately. This proves a genuine
second-order expansion without using any higher R moment:

    h0(r)=C r^-2 Lr^-p[1+e/Lr+o(1/Lr)],
    e=d+p(1-gamma_E).                               A10

Indeed `integral z e^-z dz=1`, while differentiating
`Gamma(s+1)=s Gamma(s)` at s=1 gives
`integral z e^-z ln z dz=1-gamma_E`. The sign in A10 is PLUS p times
this derivative, because the logarithm in the kernel is `Lr-ln z`.

## 5. Complete remote integral and the second entropy term

Put `x=ln X=l+ln l+o(1)`. From the positive tail A10,

    I1=integral_X^infinity r h0(r)dr
      =C x^(1-p)/(p-1)+C e x^-p/p+o(x^-p),
    I0=integral_X^infinity h0(r)dr
      ~C X^-1 x^-p,
    Ilog=integral_X^infinity h0(r)ln r dr
      ~C X^-1 x^(1-p).                              A11

For I1 the integrated little-o is justified uniformly beyond X and the
integrable comparison `(ln r)^(-p-1)/r`. For I0 and Ilog, the change
r=Xu and logarithmic comparison give their standard first terms; no
second coefficient for those two integrals is needed.

The remote Phi integral decomposes EXACTLY into

    I1/(t+a) + integral h0[ln h0+ln(t+a)]dr
                     -I0 + integral q_t dr.          A12

The last two terms are `O(t^-1 l^(-p-1))` and
`O(t^-1 l^(-p-2))`. In the logarithm,

    ln h0=ln C-2ln r-p ln ln r+O(1/ln r).

The constant and ln-ln pieces contribute only
`O(t^-1 l^(-p-1)ln l)=o(t^-1 l^-p)`. The remaining part is

    l I0-2Ilog=-C t^-1 l^-p+o(t^-1 l^-p),

because `(l-2x)/Y->-1`. Replacing `t+a` by t changes only smaller terms.
Finally

    x^(1-p)/(p-1)
      =l^(1-p)/(p-1)-l^-p ln l+o(l^-p).

Combining A7-A12 yields the full CLASSICAL expansion

    D_cl(h_t||q_t)
     = C/t { l^(1-p)/(p-1)
                -l^-p[ln l+gamma_E-d/p] }
         +o(t^-1 l^-p).                             A13

The identity `e/p-1=d/p-gamma_E` is responsible for the exact second
constant. There is no missed core contribution or a hidden ln C term
at this order; a constant times I0 is one logarithmic order smaller.

## 6. Actual normal quantum transfer

The coherent-state preparation channel maps h_t and q_t into the actual
quantum heated mixture and its matching thermal state. Heterodyne
measurement maps those two states to h_(t+1) and q_(t+1). Normal relative
entropy data processing gives

    D_cl(h_(t+1)||q_(t+1))
      <=D_q(H_t rho_R||tau_(t+a))
      <=D_cl(h_t||q_t).                              A14

The upper bound is finite by A2; hence no undefined relative entropy
or unbounded-log differentiation is needed. In particular this is not
a physical mixture flag made accessible to either party.

The explicit main term of A13 changes under t->t+1 by
`O(t^-2 (ln t)^(1-p))`, whereas its requested second-term scale is
`t^-1 (ln t)^-p`; their ratio is `O((ln t)/t)->0`.
Both classical little-o remainders remain little-o at that scale.
Squeezing in A14 proves L2 for the ACTUAL quantum relative entropy.
Only finite energy and the precise tail expansion were used.

## 7. Scaling, convolution and the permissible shift statement

For fixed c>0, a scaled temperature cR has parameters

    C'=cC, d'=d+p ln c.

This is the direct expansion of `c^-1 f_R(r/c)`. For two independent
laws with the same p, split their sum density at
`h(r)=r/(ln r)^2` and `r-h(r)`. In the first endpoint region the other
density's two-term expansion is uniform, since its argument lies in
`[r-h(r),r]`; the main power/log argument errors are `O(1/(ln r)^2)`
and its unspecified remainder is uniformly `o(1/ln r)`.
The endpoint probability omitted from the first law is

    O(r^-1 (ln r)^(2-p))=o(1/ln r).

The opposite endpoint gives the second law's corresponding term.
In the middle, at least one argument is at least r/2, giving its density
upper bound `O(r^-2(ln r)^-p)`; integrating the other variable above h(r)
then yields

    O(r^-3(ln r)^(2-2p))
      =o(r^-2(ln r)^(-p-1)).                         A15

Bounded body atoms are included in the endpoint integrals; no large-r
atoms remain. Thus convolution adds C and Cd at the specified order.

A FIXED shift also preserves these parameters. Its leading power/log
terms change by `O(1/r)`, and its remainder at r-shift is still
`o(1/ln r)` uniformly. The TOTAL relative density difference need not
be `O(1/r)`; Section 9 supplies a counterexample. The valid two-term
invariance is sufficient for all subsequent calculations.

For the actual independent-input amplifier, conditional thermal inputs
remain thermal with mean

    sT+W, W=lambda+G R_A+lambda R_B,
    lambda=G-1, s=2G-1.

Unflagged averaging is justified by the channel's linearity on the
independent product mixture. Consequently W is again in A1, with

    C_W=G C_A+lambda C_B,
    C_W d_W=G C_A(d_A+p ln G)
               +lambda C_B(d_B+p ln lambda).         A16

Its finite mean includes the fixed lambda shift. Neither independence
nor a temperature flag is created by a physical operation in this proof;
independence is an initial mathematical premise.

## 8. Scalar entropy target and exact cancellation

For one mode define the entropy target

    F(u,v)=g(G g^-1(u)+lambda[g^-1(v)+1]).

At the matching thermal inputs `n_i=T+a_i`, the output mean is
`n_C=G n_A+lambda(n_B+1)=sT+O(1)`, so the thermal baseline is EXACTLY
zero. Since `g'(n)=ln(1+1/n)` and `g''(n)=-1/[n(n+1)]`,

    F_u=G g'(n_C)/g'(n_A)=theta+O(1/T),
    F_v=lambda g'(n_C)/g'(n_B)=phi+O(1/T),
    theta=G/s, phi=lambda/s.

The Hessian is uniformly bounded on the intervening segment. For example

    F_uu=G^2 g''(n_C)/g'(n_A)^2
            -G g'(n_C)g''(n_A)/g'(n_A)^3,
    F_uv=G lambda g''(n_C)/[g'(n_A)g'(n_B)].

All effective means there stay of order T; these formulas are bounded
(their leading terms are theta phi and -theta phi). No exponential
source assumption is involved in this scalar assertion.

Let d_A,d_B,d_C be the actual quantum defects from the matching thermal
states. From A3 and the exact finite Taylor remainder,

    entropy gap
      =theta d_A+phi d_B-d_C
        +O((d_A+d_B)/T)+O((d_A+d_B)^2).              A17

By L2, `d_i=O(T^-1(ln T)^(1-p))`. Both errors in A17 are
`o(T^-1(ln T)^-p)` for every fixed p>1.

Apply L2 to W at heat sT. With `l=ln T`,

    F0(l)=l^(1-p)/(p-1),
    F0(l+ln s)=F0(l)-(ln s)l^-p+o(l^-p).

Also `(l+ln s)^-p=l^-p+o(l^-p)` and the shifted ln-ln difference is
smaller at this order. Put `Cbar=C_W/s=theta C_A+phi C_B`.
The leading `Cbar F0(l)/T`, common ln-ln and Euler terms cancel exactly.
The remaining coefficient in A17 is

    Cbar ln s
       +[theta C_A d_A,tail+phi C_B d_B,tail-Cbar d_W]/p
      =Cbar ln s-theta C_A ln G-phi C_B ln lambda
      =-theta C_A ln theta-phi C_B ln phi >0.         A18

Here `d_i,tail` denotes the supplied tail coefficient, distinguished from
the entropy defect notation in A17. Equation A18 is precisely L3 in
natural entropy units. Positivity is strict because the gain and sources
are FIXED, G>1 and both C values are positive. The little-o remainder
then gives an eventual sufficiently large FINITE T for each supplied
pair. No uniform quantitative crossover is asserted.

## 9. Exact ancillary-shift counterexample and limited diagnostic

For r>=e^2 choose

    f(r)=r^-2(ln r)^-2
                  [1+(ln r)^(-3/2)sin(2pi r)].       A19

Its tail mass is less than one: the bracket is below two and
`(ln r)^-2<=1/4`, giving tail mass at most `(1/2)e^-2`.
Put the remaining probability at zero. The density is positive,
eventually continuous, has finite mean and infinite every higher moment,
and satisfies A1 with p=2,C=1,d=0.

At `r_n=n+1/4`, its sine equals +1; after a fixed shift by one half the
sine is -1. Its smooth leading power/log ratio changes by `O(1/r_n)`.
Therefore

    f(r_n-1/2)/f(r_n)-1
         ~ -2(ln r_n)^(-3/2),                       A20

which is NOT `O(1/r_n)` but IS `o(1/ln r_n)`. This directly falsifies
the literal stronger sentence while demonstrating why the sufficient
tail-parameter invariance survives. The same construction can be scaled
to any nonzero fixed shift.

Own `check_fixed_shift_obstruction.py` uses Decimal160 arithmetic and
the exact sine signs at these points, without a peer implementation or
large-angle floating sine. Five n values from 10^3 through 10^60 exhibit
the normalized difference approaching -2 and unbounded r times the
relative change. Runtime was about 0.0008 seconds. These numbers target
only this exact local falsifier; they are not entropy quadrature, an
all-tail proof or quantum measurements. The formal proof is A19-A20.

## 10. Resource and scientific boundaries

The explicit original example with density `r^-2(ln r)^-p` on r>=e and
remaining mass at zero is valid: its tail mass is below e^-1 and mean
exactly `1/(p-1)`. Jensen on each thermal photon-number law proves
infinite photon moment of every order above one, so the class really
extends beyond finite-high-moment source premises.

The theorem still assumes a precise supplied tail expansion and common
p for the two independent sources. It applies ACTUAL equal heat T to
both inputs, adding T photons per input mode. It does not remove heat,
infer an unheated inequality, encompass arbitrary finite energy, acquire
a tail certificate from finite data, supply a useful source-uniform T,
or establish a source factory/advantage. The states are unflagged thermal
mixtures; temperature/amplitude records are not made accessible for free.

No physical heat, preparation, pumping, calibration, measurement, reset,
entropy acquisition or external communication was performed. General
UNHEATED finite-energy independent-input amplifier EPnI remains
NOT_ACHIEVED. Internal reconstruction succeeds with the explicit local
shift-sentence correction; external acceptance and special-case priority
UNKNOWN; hardware NOT_VALIDATED; practical advantage NOT_ESTABLISHED.
