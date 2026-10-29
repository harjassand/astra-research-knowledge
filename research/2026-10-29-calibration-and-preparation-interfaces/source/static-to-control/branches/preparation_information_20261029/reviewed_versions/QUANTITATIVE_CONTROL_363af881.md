# Quantitative controlled prediction from static information and baseline heat

29 October 2026. New root construction, under independent challenge. Earlier
qualitative theorems remain established. This extension uses strong conventional
kinetic Schauder estimates and Besov products; those are not claimed inventions.
Its analytic constants must be retained, not replaced by assumed free accuracy.

## 1. Target and native interface

Fix the same native Kramers class, torus, complete coordinates, bath gamma,tau,
force ceiling A, control ceiling B and finite horizon T. A smooth bounded
position force F has stationary law rho_F, position marginal nu_F and warranted
physical entropy ceiling sigma(F)<=s. A smooth selected Gibbs potential U has
|grad U|<=A and W1(nu_F,nu_U)<=e. Put G=-grad U. Source and candidate receive
the SAME bounded Borel Markov force u(t,q,p), |u|<=B, through the momentum port.
They start from rho_F and nu_U M_tau respectively.

Let E0 bound initial full-state TV and put eta=||F-G||_(C_B^(-1/4)), using a
fixed kinetic anisotropic Besov norm, with momentum weight one and position
weight three. Periodic-position fields extend periodically to Euclidean space.
For a regular time mesh h=T/m<=h0 the ordinary proof below gives

    sup_(|u|<=B) d_BL(P_F^u,Q_U^u)
       <=2 E0+2 R_T(h)+2 C_tr m eta h^(-5/8),                    (1)

with explicit R_T(h)=O(sqrt(h log(T/h))). The constants depend only on fixed
native parameters, force ceilings and norm conventions, not force derivatives.
The force-information construction supplies

    E0<=sqrt(s/(4gamma))+(1/2)L(e),
    eta<=C_force [sqrt(s)+L(e)]^[1/(12(d+1))],                   (2)

where L(e)=O(e^(1/4)) is an explicit L1 density bound. It uses the selected
Gibbs density floor, not an inferred hidden source floor. New uses of (2)
are being checked separately. Physical acquisition of s,e, bath, complete
coordinates, preparations and actuation is not supplied by this formula.

## 2. Fixed analytic constants

For 0<t<=1 choose free-semigroup constants C_S0,C_Sminus and embedding/product
constants C_E,C_D,C_M such that

    ||P_t f||_(C_B^(3/2)) <=C_S0 t^(-3/4)||f||_infinity,
    ||P_t f||_(C_B^(3/2)) <=C_Sminus t^(-7/8)||f||_(C_B^(-1/4)),
    ||v||_infinity<=C_E||v||_(C_B^(3/2)),
    ||grad_p v||_infinity<=C_D||v||_(C_B^(3/2)),
    ||a.grad_p v||_(C_B^(-1/4))
                    <=C_M||a||_(C_B^(-1/4))||v||_(C_B^(3/2)).   (3)

The product is valid because grad_p v has regularity 1/2>1/4. Vector
dimension constants are included. A bounded coefficient b instead obeys
||b.grad_p v||_infinity<=(A+B) C_D||v||_(C_B^(3/2)). No reverse embedding
from C_B^0 into L_infinity is used; only L_infinity into C_B^0.

Primary: Issoglio--Pagliarani--Russo--Trevisani,
https://arxiv.org/html/2401.09165v2, Theorem 2.10, Lemma 2.9 and the positive
regularity characterization. Fixed bath scaling and periodic extension give
(3). These are known estimates for explicit free Gaussian kernels and a fixed
dyadic partition, not a hidden mixing premise. Their numerical values have
not been instantiated in this research.

With M=A+B choose

    h0=min{1,[2 C_S0 M C_D Beta(1/4,1/4)]^(-4)},
    C_tr=4 C_E C_S0 C_Sminus C_M Beta(1/8,1/4).                 (4)

Use h0=1 if M=0. C_tr is conservative for the TV normalization.

## 3. Short-time transition total variation

First take smooth bounded b(t,z),c(t,z), with |b|,|c|<=M and b-c=F-G,
and a smooth bounded terminal function f. Write v_b(r),0<r<=h, for its
backward Feynman--Kac solution, with time reversed from the terminal time.
Its mild equation is

    v_b(r)=P_r f+int_0^r P_(r-a)[b_(h-a).grad_p v_b(a)]da.      (5)

Smooth bounded-derivative approximations have finite weighted norm

    ||v||_h=sup_(0<r<=h) r^(3/4)||v(r)||_(C_B^(3/2)).            (6)

Apply (3) as an A PRIORI estimate on these Feynman--Kac solutions. The
linear perturbation contributes at most

    C_S0 M C_D h^(1/4) Beta(1/4,1/4)||v_b||_h<=||v_b||_h/2.

This follows by integrating (r-a)^(-3/4)a^(-3/4) and multiplying by
r^(3/4). Consequently ||v_b||_h,||v_c||_h<=2 C_S0||f||_infinity.
No nonseparable-function-space fixed-point assertion is needed.

For w=v_b-v_c, retain b.grad_p w as the same absorbable term. The forcing
(b-c).grad_p v_c, followed by negative-to-positive Schauder smoothing,
has weighted norm at most

    C_Sminus C_M eta h^(1/8) Beta(1/8,1/4)||v_c||_h.           (7)

The kernel is (r-a)^(-7/8)a^(-3/4). Absorbing and evaluating at r=h gives

    ||v_b(h)-v_c(h)||_infinity
                     <=C_tr eta h^(-5/8)||f||_infinity.         (8)

This holds uniformly over initial phase states. Smooth bounded tests can
approximate every bounded Borel test almost everywhere. Both endpoint laws
are absolutely continuous relative to the full free kinetic endpoint Gaussian
(wrapped in position), by bounded Girsanov. Thus

    sup_z TV(P_b(t,z;t+h,.),P_c(t,z;t+h,.))
                                  <=C_tr eta h^(-5/8).         (9)

There is no full continuous-path TV claim in (9).

## 4. Bounded Borel feedback without a derivative cap

Choose COMMON smooth mollifications u_k with |u_k|<=B and almost-everywhere
convergence to u in time and phase space. Compare F+u_k with G+u_k: the
difference is exactly F-G, so eta is unchanged. No bound above uses Du_k.

For each fixed initial state and either baseline, bounded Girsanov gives

    D(P_(F+u)||P_(F+u_k))
      =(1/(4gamma tau)) E_(F+u) int_0^h |u-u_k|^2dt ->0.        (10)

At every positive time the law is absolutely continuous relative to the
free full-state Gaussian. Dominated convergence therefore applies to the
bounded integrand and its time-state almost-everywhere convergence. The
same holds for G. Thus (9) passes to each bounded Borel feedback for EVERY
initial state with the same constant; taking the supremum afterwards is
valid. Strong pathwise well-posedness of rough feedback is not assumed.

## 5. Complete finite-window path consequences

At grid times 0,h,...,mh=T, sequential kernel coupling gives

    TV(joint source grid,joint candidate grid)
                                  <=E0+m C_tr eta h^(-5/8).    (11)

Use a UNIFORM mesh so there is no arbitrarily short final interval. Put

    K_T=(2A+B)/gamma+sqrt(d tau)+4sqrt(2gamma tau d T),
    L=log(4dm),
    R_T(h)=2h[(A+B)+(1+gamma)K_T]
       +2sqrt(2gamma tau d h)[sqrt(2L)+1/sqrt(2L)].             (12)

The mild equation gives E sup_(t<=T)|p_t|<=K_T in both laws. Each position
increment is bounded by h sup|p|; each momentum increment is bounded by
(A+B)h+gamma h sup|p| plus its Brownian increment. The union/reflection bound

    P(max_(i,k) sup_(0<=r<=h)|W_k(ih+r)-W_k(ih)|>x)
                                           <=4dm exp[-x^2/(2h)]

gives expected vector increment maximum at most
sqrt(dh)[sqrt(2L)+1/sqrt(2L)]. Piecewise linear momentum and shortest-geodesic
position interpolation have expected uniform-path error at most R_T(h).
Resolve torus geodesic ties by a fixed measurable rule.

Each bounded 1-Lipschitz path test incurs at most R_T(h) under each
interpolation, and at most twice (11) between the reconstructed grid laws.
This proves (1). Controlled work can be large; the estimate uses force/bath
moments, not small controlled entropy. Infinite-time survival integrals are
not inferred from finite-window control.

Choosing h comparable to eta^(8/17), subject to h<=h0, gives the conservative
asymptotic bound O(E0+eta^(4/17)sqrt(log(1/eta))). Equation (1) retains
the actual finite-mesh constants. Higher moment interpolation gives every
finite Wasserstein order. A uniform TV-Lipschitz sensor family inherits a
quantitative output-TV bound. An arbitrary fixed measurable path sensor may
have no supplied quantitative modulus; its earlier qualitative theorem remains.

## 6. Acquisition and analytic constants

The finite native-position LP can certify e. A physical entropy UPPER bound
s requires its own calibrated bath, energy/heat observations and preparation
contract. Neither is acquired by the other. Substituting (2) in (1) produces
a mathematical bound in those errors and fixed analytic constants.

This is not an executed end-to-end predictor. Numeric bounds for the constants
in (3) and the force conversion have not been instantiated. They concern known
Gaussian operators, but their norm conventions and bit-cost evaluation must
be retained in any operational sample schedule. A fitted potential does not
prepare a physical Gibbs state. Actual intervention descriptions, state sensing,
numerical initialization and controlled solver accuracy/cost remain separate.
Arbitrary mathematical Borel protocols need not be computable.

Ordinary semigroup perturbation, Bony products, kernel coupling and Brownian
interpolation are the strong existing methods. The addition under challenge
is their connection to native baseline entropy and a reusable acquired static
position fit, uniformly across the stated intervention interface. No favorable
runtime, optimal exponent or historical priority is asserted.
