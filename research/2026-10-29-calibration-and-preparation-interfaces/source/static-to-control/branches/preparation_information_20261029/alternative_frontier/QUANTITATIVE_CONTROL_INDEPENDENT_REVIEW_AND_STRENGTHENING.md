# Independent review and stronger endpoint estimate for quantitative control

29 October 2026. Ordinary analytic review by
producer-workspace/different_consequential_opening. No numerical test was used.

Exact reviewed root file: QUANTITATIVE_CONTROL_FROM_STATIC_INFORMATION.md.
SHA256 363af8817b0106ad7410107ace7ce14d1bbdab83aed616a9f0036157b1a88cf2.

**Verdict:** the displayed safe h^(-5/8) transition-TV estimate and the
resulting quantitative path bound pass, including bounded Borel common
feedback, all initial native states, the constants K_T and R_T, and uniform
time/geodesic interpolation. A further endpoint extraction proves the
stronger transition bound C eta h^(1/16), derived in section 6 below.

The derivation of eta and initial TV from entropy and acquired position
error is a separate causal-frontier construction. This review checked that
its equations (16)--(17) supply the inputs used here; it does not count as a
second full review of that construction.

## 1. Primary machinery and function-space scope

Primary: Issoglio, Pagliarani, Russo, Trevisani,
https://arxiv.org/html/2401.09165v2.
Actual new read scope: Definition 2.6; Example 2.7; Corollary 2.5 and the
derivative discussion; Proposition 2.9; Theorem 2.10; Definition 2.11 and
Proposition 2.13. These establish the anisotropic Besov conventions,
bounded-function embedding, product and free-semigroup estimates used here.
Their full foundational proofs were not re-audited.

Small bibliographic correction: item 2.9 is a PROPOSITION, not a lemma.

The precise embedding direction is L-infinity -> C_B^0.
The reverse direction is not valid and is not used by the safe proof.
For noninteger positive regularity, the supplied characterization gives
C_B^(3/2) -> L-infinity and
grad_p:C_B^(3/2) -> C_B^(1/2).
Bony's product with C_B^(-1/4) is legitimate because
1/2-1/4>0; its result has regularity -1/4.

A bounded Borel coefficient b can instead be multiplied pointwise by
grad_p v, using ||b.grad_p v||_infinity<=M C_D||v||_(3/2).
This is what makes the contraction independent of coefficient derivatives.

Fix the inhomogeneous dyadic norm and bath parameters once. The physical
noise sqrt(2gamma tau) can be handled by a fixed linear rescaling, with its
constants retained. Periodic q-functions are bounded tempered functions
on the Euclidean lift, with p unbounded. The free linear kinetic matrix
includes friction and satisfies the source's Hörmander condition. Its
Schauder bounds are global in state; no initial-momentum bound enters the
transition estimate.

## 2. Safe weighted a priori estimate, with constants

Write r=3/2, beta=1/4 and M=A+B. Use the root constants C_S0,
C_Sminus,C_E,C_D,C_M and h0 as defined there.

First restrict to smooth bounded coefficients with bounded derivatives and
smooth bounded terminal f with bounded derivatives. Their stochastic-flow
Feynman--Kac solutions have finite C_B^(3/2) norm on a compact time interval.
The standard free-semigroup variation-of-constants formula applies.
This is enough for an a priori estimate; no contraction theorem in a
nonseparable bounded-Besov-valued function space needs to be invoked.

Time reversal from a fixed terminal time gives

    v_b(t)=P_t f+int_0^t P_(t-s)[b_(h-s).grad_p v_b(s)] ds.

Let X_h(v)=sup_(0<t<=h) t^(3/4)||v(t)||_(3/2).
The elementary beta integral is

    t^(3/4) int_0^t (t-s)^(-3/4)s^(-3/4) ds
          =t^(1/4) Beta(1/4,1/4).

Thus the root h0 makes the feedback contribution at most X_h(v)/2,
giving X_h(v_b),X_h(v_c)<=2 C_S0||f||_infinity.

For w=v_b-v_c, set H=b-c=F-G and eta=||H||_(-1/4).
After retaining b.grad_p w as the absorbable term, Bony plus Schauder gives

    X_h(w)
      <=(1/2)X_h(w)
        +C_Sminus C_M eta h^(1/8)
                       Beta(1/8,1/4) X_h(v_c).

The exponent follows from
3/4+1-7/8-3/4=1/8. Therefore define

    K_w=4 C_S0 C_Sminus C_M Beta(1/8,1/4).

Then X_h(w)<=K_w eta h^(1/8)||f||_infinity.
Evaluating in C_B^(3/2) at h and using its L-infinity embedding gives

    ||w(h)||_infinity
       <=C_E K_w eta h^(-5/8)||f||_infinity.

This is exactly the root C_tr. Operator norm over |f|<=1 equals twice
TV in the usual probability convention; using the same constant for TV
is conservative.

## 3. Rough terminal tests and common Borel feedback

For smooth bounded feedback, every positive-time endpoint law is absolutely
continuous relative to the nondegenerate free kinetic endpoint Gaussian,
wrapped in q. This follows from bounded Girsanov, not from an assumption
that position itself receives white noise. A bounded Borel f admits smooth
bounded mollifications converging Lebesgue-almost everywhere, with no increase
of its supremum norm. Dominated convergence under both endpoint laws extends
the estimate to every bounded Borel terminal test.

For the feedback limit, extend u in time outside the interval in a bounded
way and mollify it jointly in time and phase space, periodically in q.
Positive averaging preserves |u_k|<=B and gives Lebesgue-almost-everywhere
convergence to u. Use the SAME u_k on both sides. The difference remains
exactly H; no new norm of H or derivative norm of u_k appears.

For each fixed initial z and either fixed baseline force, bounded drift
Girsanov yields

    D(P_(F+u)^z || P_(F+u_k)^z)
      =(1/(4gamma tau)) E_(F+u)^z int_0^h |u-u_k|^2dt ->0.

At every positive time the limiting process has a density relative to
Lebesgue measure, by its own equivalence to the free law. Fubini and
bounded convergence justify the limit despite the initially deterministic
state and despite only time-state a.e. convergence of the controls.
The t=0 slice is immaterial. Pinsker gives path-TV convergence for this
fixed z. The same applies to the candidate.

The approximating transition inequality has one constant for EVERY z.
Taking its limit separately at each z therefore leaves that same bound
valid for all z; uniform convergence of the approximations in z is not
required. Supremizing after this argument is valid. Weak uniqueness follows
by forward/inverse bounded Girsanov; strong pathwise uniqueness is unnecessary.

These steps also validate the stronger estimate in section 6.

## 4. Initial states, mesh and full-path constants

An initial complete-position W1 bound alone does not justify E0.
Here the causal-frontier construction explicitly supplies

    E0<=sqrt[s/(4gamma)]+(C_pos/2)e^(1/4),

using conditional Maxwell thermalization and the separately proved density
regularity estimate. The root correctly retains that initial-TV obligation.

At m equally spaced steps h=T/m, the ordinary product-kernel telescoping
bound gives skeleton TV<=E0+m delta_h. Each short-time kernel is compared
under the same Markov policy on its corresponding time interval.
Use an equal mesh, or choose m=ceil(T/h_target), so the last interval
cannot be arbitrarily shorter than the others.

The root momentum constant is correct. The initial source first moment is
at most A/gamma+sqrt(d tau), and the controlled deterministic convolution
is at most (A+B)/gamma. For the stochastic convolution,

    int_0^t exp[-gamma(t-s)]dW_s
       =W_t-gamma int_0^t exp[-gamma(t-s)]W_s ds,

so its supremum is at most 2 sup|W|. Doob's L2 estimate gives
E sup|W|<=2sqrt(dT). Therefore

    E sup|p|<=K_T
      =(2A+B)/gamma+sqrt(d tau)+4sqrt(2gamma tau dT)

for both initial laws. No controlled small-heat premise was inserted.

Let B_h be the maximum coordinate Brownian increment supremum over the
m intervals and d coordinates. Reflection and a union bound give
P(B_h>x)<=4dm exp(-x^2/(2h)). Put L=log(4dm). Integrating this tail at
x0=sqrt(2hL), using the Gaussian tail majorant h exp(-x0^2/(2h))/x0,
gives E B_h<=sqrt(h)[sqrt(2L)+1/sqrt(2L)].
A vector increment is at most sqrt(d) times the coordinate maximum.

For an interval, distance of the actual q path from shortest-geodesic
endpoint interpolation is at most 2h sup|p|. This remains true when the
physical path winds around the torus: the chosen shortest geodesic is no
longer than the actual endpoint displacement. A fixed measurable tie rule
makes the interpolation a legitimate kernel of the skeleton.

Linear momentum interpolation has error at most twice the maximum increment,
bounded by 2[(A+B)h+gamma h sup|p|+sqrt(2gamma tau) B_h^vector].
Adding the position error gives exactly the stated R_T(h).
The interpolated path need not itself satisfy dq=p dt; it lies in the
ambient continuous-path space on which d_BL is defined, which is sufficient.

Each bounded 1-Lipschitz path test pays R_T(h) on each side and twice
the skeleton TV between interpolated laws. This verifies the root bound,
including its factors 2E0, 2R_T(h) and 2m delta_h.

## 5. Reach and numerical-constant boundary

The original choice h approximately eta^(8/17) gives the stated
O(E0+eta^(4/17)sqrt(log(1/eta))) bound. The equal-mesh rounding changes
only constants once eta is small. Uniform higher moments give the already
established finite-Wasserstein upgrades.

A uniformly TV-Lipschitz observation family inherits a quantitative bound.
A general measurable full-path kernel does not inherit one merely from
d_BL. The root correctly preserves only its earlier qualitative claim for
such records. This construction does not assert full continuous-path TV
convergence and does not contradict the earlier exact-path counterexample.

All analytic constants depend on the fixed free generator, dimension,
chosen norm partition, and force ceiling. The primary theorem guarantees
finite constants; their numerical values have NOT been computed here.
A quantitative rate in named analytic constants is established. A certified
numerical stopping schedule additionally needs usable upper bounds for those
constants and for the force-information conversion, plus the actual acquired
entropy/static-fit bounds. No operational precision is obtained for free.

## 6. Additional construction: stronger endpoint extraction

The estimate of w in C_B^(3/2) is stronger than needed for terminal TV.
After obtaining X_h(w), return to its Duhamel formula at the endpoint.

Introduce a fixed positive-order smoothing constant C_small satisfying

    ||P_t g||_infinity
        <=C_small t^(-3/16)||g||_(C_B^(-1/4)),  0<t<=1. (A)

This follows from Theorem 2.10 with output C_B^(1/8), followed by the
POSITIVE-order embedding C_B^(1/8)->L-infinity. The smoothing gain is
1/8+1/4=3/8, giving exponent 3/16. This intentionally avoids the invalid
C_B^0->L-infinity endpoint.

For the b.grad_p w term use only the Markov L-infinity contraction of
the free semigroup:

    ||int_0^h P_(h-s)[b.grad_p w(s)] ds||_infinity
      <=M C_D X_h(w) int_0^h s^(-3/4)ds
      <=4M C_D K_w eta h^(3/8)||f||_infinity.          (B)

For H.grad_p v_c, apply (A) and the same Bony product:

    ||int_0^h P_(h-s)[H.grad_p v_c(s)] ds||_infinity
      <=2 C_S0 C_small C_M eta ||f||_infinity
                    h^(1/16) Beta(13/16,1/4).          (C)

Indeed 1-3/16-3/4=1/16. For h<=h0<=1, (B)--(C) give

    sup_z TV(P_b(t,z;t+h,.),P_c(t,z;t+h,.))
                      <=C_imp eta h^(1/16),           (D)

    C_imp=4M C_D K_w
               +2 C_S0 C_small C_M Beta(13/16,1/4).

Again the same constant is conservative by a factor of two for TV.
The terminal/Borel limits of section 3 preserve (D), and the constant
does not depend on any control derivative.

Consequently the stronger full-path bound is

    sup_(|u|<=B) d_BL(P_F^u,Q_U^u)
       <=2E0+2R_T(h)+2 C_imp m eta h^(1/16)
        =2E0+2R_T(h)+2 C_imp T eta h^(-15/16).           (E)

Choosing h comparable to eta^(16/23), with the same uniform-mesh and
h0 restrictions, gives

    O(E0+eta^(8/23)sqrt(log(1/eta))).                   (F)

No exponent is claimed optimal. The safe root estimate remains valid;
(D)--(F) are a further consequence of exactly the same a priori argument
and the same admitted interface. A numerical value for C_small has not
been instantiated, just as for the other Schauder constants.

