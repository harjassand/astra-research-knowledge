# Independent proof and review: bounded Markov intervention closure

29 October 2026. Physical-frontier branch.

Exact reviewed root file: `BOUNDED_MARKOV_FORCE_INTERVENTIONS.md`.
Reviewed SHA256:

    db1dcfba5eda825e3ba6465736072bc2e0761681c95ef732d6fc2c24075a24ca

**Review outcome:** the root theorem is valid at its declared scope,
including full phase-space Markov controls, the order infimum over one
Gibbs explanation before supremum over interventions, fixed-record TV,
and finite-window Wasserstein consequences. No load-bearing gap was
found. This file supplies an independent ordinary argument and a further
static-law reuse corollary. There is no empirical test or acquisition claim.

## 1. Interface and conclusion

Keep the fixed torus, d, unit masses, gamma,tau>0, baseline force ceiling
A, intervention ceiling B and finite T. Baseline F(q) is smooth with
||F||<=A, stationary law rho_F and the already specified physical entropy
sigma(F). The control u is a bounded Borel function of time and CURRENT
full native state, ||u(t,q,p)||<=B. It adds through the noisy momentum
force port:

    dq=p dt,
    dp=[F(q)+u(t,q,p)-gamma p]dt+sqrt(2gamma tau)dW.       (1)

Let P_F^u start from baseline rho_F. For smooth periodic U with
||grad U||<=A, let Q_U^u use baseline Gibbs initialization mu_U and the
same protocol u. Neither controlled law is presumed stationary.

The conclusion is

    sup_(F: ||F||<=A, sigma(F)<=s)
      inf_(U: ||grad U||<=A)
        sup_(u: ||u||<=B) d_BL(P_F^u,Q_U^u) ->0.         (2)

The first supremum is over the stated smooth baseline source class and
the infimum over smooth Gibbs potentials. d_BL uses the bounded uniform
path metric. The same Gibbs potential serves every admitted intervention.
The theorem also holds in every finite W_p for the unbounded uniform path
metric, and in output TV for each fixed record kernel of the types stated
by the root theorem.

These hypotheses specify a conditional physical interface. They do not
acquire the microscopic state readout, calibrated port, initial preparation
or equilibrium potential. Low BASELINE entropy does not imply low heat or
work during the applied intervention. Apparatus entropy is not inferred.

## 2. Full-state free kernel: explicit calculation

The reference is stationary free Kramers motion with invariant measure
mu_0=uniform position times Maxwell M_tau. For h>0 put a=exp(-gamma h).
Conditional on p_0=x, the endpoint momentum has mean a x and covariance
tau(1-a^2)I. Its density relative to M_tau is the OU Mehler kernel m_a.

Conditional on p_0, the displacement noise and endpoint momentum noise
have covariances

    Var(p_h)=tau(1-a^2)I,
    Var(displacement)=(tau/gamma^2)
                       [2gamma h-3+4a-a^2]I,
    Cov(displacement,p_h)=tau(1-a)^2 I/gamma.             (3)

The Schur complement therefore gives the displacement conditional on
BOTH endpoints p_0=x,p_h=y:

    mean=[(1-a)/(gamma(1+a))](x+y),
    covariance=v_h I,
    v_h=(2tau/gamma^2)[gamma h-2tanh(gamma h/2)].          (4)

The function z-2tanh(z/2) has derivative tanh(z/2)^2 and vanishes at zero,
so v_h is strictly positive for every h>0 and increases with h. Its
small-h value is tau gamma h^3/6 to leading order.

Writing w_v for the wrapped Gaussian density relative to normalized
uniform position, the full free transition kernel is exactly

    k_h((q,x),(q',y))
      =m_a(x,y) w_(v_h)[q'-q-((1-a)/(gamma(1+a)))(x+y)].  (5)

For h>=epsilon, the wrapped factor is bounded uniformly by a finite
C_epsilon. On the side-2pi torus one may take

    C_epsilon=sum_(n in Z^d) exp[-v_epsilon |n|^2/2].

Direct Gaussian integration gives

    int m_a(x,y)^2 M_tau(dx)M_tau(dy)=(1-a^2)^(-d).      (6)

In one normalized coordinate, the Gaussian precision matrix after
squaring the density is

    (1-a^2)^(-1) [[1+a^2,-2a],[-2a,1+a^2]],

which has determinant one; the prefactor is (1-a^2)^(-1). Dimensions
multiply. Consequently

    ||k_h||_L2(mu_0 x mu_0)^2
       <=C_epsilon^2(1-exp(-2gamma epsilon))^(-d)
       for h>=epsilon.                                (7)

There is no unsupported pointwise bound on the full momentum kernel.
Its Gaussian-weighted Hilbert--Schmidt bound is sufficient.

## 3. Compact occupation on time times full phase space

For a fixed bounded measurable g(t,z), define

    A_g f=int_0^T f(t,Z_t)g(t,Z_t)dt,
    A_g:L2(dt mu_0)->L2(P_0).                           (8)

Stationarity and time Cauchy--Schwarz give

    ||A_g f||_2<=sqrt(T)||g||_infinity||f||_L2(dt mu_0).

In A_g* A_g, the off-diagonal kernel for s<t is
g(s,z)g(t,z')k_(t-s)(z,z'); for t<s it uses the transpose transition
kernel. Equation (7) makes its restriction to |s-t|>=epsilon
Hilbert--Schmidt on the time-state product.

For the omitted strip, set a(s)=||f(s,.)||_L2(mu_0) and
b(t)=||h(t,.)||_L2(mu_0). The bilinear form is bounded by

    ||g||_infinity^2 int int_(|s-t|<epsilon) a(s)b(t)dsdt
       <=2epsilon||g||_infinity^2||a||_L2||b||_L2.       (9)

The first inequality uses the two stationary marginals and ordinary
Cauchy--Schwarz. The second is Young convolution after extending the
time functions by zero. Thus A_g* A_g is a norm limit of compact
operators, and A_g is compact. In particular,

    f_j weakly ->f in L2(dt mu_0)
          implies ||A_g(f_j-f)||_L2(P_0)->0.             (10)

Restriction to any fixed time interval and vector-valued force fields
is handled by the same argument componentwise. Time-position protocols
are a special case, independent of p.

## 4. Controlled native limit with a moving protocol

For sigma(F_j)->0, use the already independently proved baseline
construction. Along a subsequence it supplies

    F_j weak-* ->F=-grad U,
    U periodic Lipschitz, ||grad U||<=A,
    rho_j close in TV to r_j mu_0 with error tending to zero,
    sup_j ||r_j||_L2(mu_0)<infinity,
    r_j weakly ->r,  r mu_0=mu_U=nu M_tau.               (11)

The positive Gibbs position density nu is bounded above and below. The
one-step smoothing used to obtain r_j is mathematical, not an executed
reset or an acquired hidden mixing estimate.

Let u_j be ANY sequence of admitted bounded Markov protocols. Since
L1(dt mu_0) is separable, weak-* compactness supplies a subsequence
u_j ->u in L_infinity(dt mu_0), with ||u||<=B. A bounded Borel version
can be chosen. F_j+u_j then converges weakly in L2(dt mu_0) to F+u.

Start the controlled paths temporarily from r_j mu_0. Their likelihoods
R_j relative to the common stationary free path law satisfy

    ||R_j||_2^2
       <=exp[(A+B)^2 T/(2gamma tau)] ||r_j||_2^2.        (12)

This follows from the conditional Girsanov second-moment estimate before
averaging the square of r_j. A weak L2 likelihood limit is nonnegative
and normalized. Every bounded measurable path function belongs to L2 of
the reference law, so convergence to that limiting path law is SETWISE.

For a smooth compact-momentum-supported test phi and bounded past
multiplier, the only changing generator term is

    int_s^t [(F_j+u_j)-(F+u)](a,Z_a)
                                      dot grad_p phi(Z_a) da.

It tends to zero in free L2 by (10). Cauchy--Schwarz with (12) handles
the changing physical law. All remaining martingale terms are fixed
bounded measurable path functions. The limit therefore solves the
native kinetic martingale problem with force F+u and initial mu_U.

Forward bounded Girsanov constructs that bounded Borel force law. For
any competing martingale-problem solution, coordinate localization
identifies its momentum Brownian motion; inverse bounded Girsanov
removes the entire added force and gives the unique free law. Reweighting
gives uniqueness. Degeneracy of position noise does not interfere because
the changing drift lies in the directly noisy momentum range.

Finally, initial TV in (11) contracts through each controlled path
kernel, uniformly in its particular u_j. The actual rho_j-start laws
have the same setwise limit, namely P_(F+u)^mu_U.

## 5. The one-potential quantifier order

Choose smooth periodic mollifications U_j of the limiting U with
epsilon_j->0. They preserve ||grad U_j||<=A, converge uniformly, and
their gradients converge strongly in L2(position). Their Gibbs initial
DENSITIES converge in L2(mu_0), and in TV, to dmu_U/dmu_0.

These potentials are selected before any separating protocol u_j.
For the same arbitrary protocol sequence, the controlled Gibbs drifts
-grad U_j+u_j have weak L2 limit F+u. Their likelihoods are uniformly
L2 and their initial laws converge to mu_U. Section 4 therefore identifies
the very same limiting path law as for the controlled physical sources.
Both controlled sequences converge weakly to this common law.

If (2) failed, select a low-entropy source sequence for which every smooth
Gibbs potential has some separating bounded protocol. Use the preceding
single U_j sequence and select such bad u_j. Their weak-* subsequence
has the common controlled limit just proved, contradicting separation
in d_BL. This verifies inf_U sup_u, rather than only sup_u inf_U.

The root notation mu_Uj->mu_U in L2(mu_0) is correctly interpreted as
convergence of their Radon--Nikodym densities. No substantive correction
is needed; spelling out "densities" would only make that notation explicit.

## 6. Record TV and all finite Wasserstein orders

For a fixed countable-output kernel K, setwise convergence gives each
output probability, and discrete Scheffe gives output TV convergence.
For a fixed dominated kernel whose density is bounded in the path
variable at almost every output, the same argument uses ordinary Scheffe.
Apply this to both controlled sequences in the separating-protocol
argument: the uniform-in-u record theorem follows. A finite specified
collection of such consequences can be enforced by the same potential.

Uniformly TV-Lipschitz readout families are controlled directly by d_BL.
The constants must include every reported channel, including command
values if they are reported. A ceiling on |u| alone does not bound the
state sensitivity of its exact command trace.

The initial baseline stationary moments satisfy

    ||p_0||_Lr<=A/gamma+sqrt(tau)c_(d,r).

During control, the mild force integral is bounded by (A+B)/gamma.
The Brownian maximal argument of the separate Wasserstein proof gives

    ||sup_(t<=T)|p_t|||_Lr
       <=(2A+B)/gamma+sqrt(tau)c_(d,r)
           +2sqrt(2gamma tau T)[r/(r-1)]c_(d,r), r>1.    (13)

The same bound covers Gibbs starts. Adding the torus diameter gives a
uniform r-th path-distance moment M_(r,T,B). For r>p, the established
coupling interpolation reads

    W_p(P,Q)^p <=d_BL(P,Q)
       +(2^r M_(r,T,B))^(p/r) d_BL(P,Q)^(1-p/r).         (14)

It upgrades (2) uniformly over u to every finite W_p. The same sequence
of Gibbs explanations works for all fixed p. The controlled experiment
can have substantial work; (13) is a force-and-bath moment estimate, not
a claim of low controlled dissipation. No unbounded hitting-time mean
is established without an additional time-tail argument.

## 7. Additional corollary: reuse of a static-law Gibbs explanation

The argument actually yields a stronger model-selection consequence.
Suppose sigma(F_j)->0 and U_j are ANY smooth potentials with
||grad U_j||<=A whose baseline Gibbs POSITION laws fit the original
baseline position laws weakly:

    d_BL^position(nu_Fj,nu_Uj)->0.                      (15)

Then, for every fixed B,T,

    sup_(||u||<=B) d_BL(P_Fj^u,Q_Uj^u)->0.               (16)

The fixed-record TV and finite W_p conclusions also hold for those same
U_j. A baseline path fit is sufficient but not necessary for this premise;
the complete position marginal (15) is enough within the native class.

Proof: work along any allegedly bad subsequence. The baseline theorem
identifies a further limit F=-grad U and nu_Fj weakly tending to nu_U.
Normalize U_j by an additive constant. The common gradient ceiling on
the compact torus makes them uniformly bounded and equi-Lipschitz, so
Arzela--Ascoli gives U_j->U_* uniformly along a further subsequence.
Their Gibbs position densities converge uniformly to nu_U*. Assumption
(15) forces nu_U*=nu_U. Both are positive, so the Gibbs formula gives
U_*=U up to a constant. Distributional differentiation and the uniform
gradient bound give -grad U_j weak-* tending to F. For any allegedly bad
u_j, Sections 3--4 now identify the same controlled limit on both sides.
This proves (16) by contradiction. The record and moment upgrades apply
unchanged.

Equivalently, the controlled discrepancy tends to zero uniformly when
BOTH the baseline entropy ceiling s and the full-position-law fitting
tolerance e tend to zero, for every candidate Gibbs potential in the
bounded-gradient class satisfying those tolerances. No effective
two-parameter modulus is obtained.

This is a stability statement for ordinary Boltzmann inversion, not a
new inversion formula or free acquisition of a high-dimensional density.
The position law is the complete native configuration, not an arbitrary
coarse observable. The bath, entropy premise, coordinate completeness
and force ceilings remain warranted inputs. Additional coarse observation
or hidden degrees of freedom require their own information argument.

## 8. Memory and physical preparation boundary

The uniform control class consists of functions of (time,current native
state). It has no separately varying internal history state. Its spatial
or momentum sensitivity need not be bounded: the free kinetic occupation
compactness handles that variation at the declared path/readout topology.

The proof does not establish uniformity over arbitrary varying
history-dependent controllers. Such a controller can retain a fine path
test and later issue a bounded command based on that stored information.
That memory is not represented by the current-state function u(t,q,p),
and the compactness lemma is not a theorem on arbitrary history spaces.

A SINGLE fixed bounded causal controller with a commonly initialized
independent random seed is also approachable by bounded path-dependent
Girsanov on the augmented reference: its feedback drift is fixed, so
only F_j moves in the martingale argument. That observation does not
extend the uniform theorem to arbitrary changing memory strategies.

A retained warm-up or calibration transcript cannot silently be placed
in an independent seed. It needs its actual joint initialization or an
explicit augmented-state approximation. The native bath, baseline
preparation, force-port and observation requirements are not supplied
by visible fitting. No physical operation was performed or requested
in this proof review.
