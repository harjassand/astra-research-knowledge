# Native equilibrium closure without a force-derivative bound

29 October 2026. Independent construction and detailed challenge of root's
compact-occupation/Girsanov route. This reviews that route as supplied in
the task message, rather than claiming to have read a later root manuscript.

## 1. Result and physical scope

Fix a connected d-dimensional position torus, unit masses, damping
gamma>0, temperature tau>0, and a finite force-amplitude ceiling A. Consider
smooth periodic position-only forces F_j with ||F_j||_infinity<=A, with
no uniform derivative bound, and stationary sources

    dq=p dt,
    dp=[F_j(q)-gamma p]dt+sqrt(2gamma tau)dW.             (1)

All odd variables are the directly thermalized momenta; there are no odd
external fields or altered reservoir interpretations. Let sigma_j be the
stationary physical entropy production. Suppose sigma_j tends to zero.

**Theorem.** For every fixed finite horizon h, the stationary path laws
approach, in bounded-Lipschitz/weak path topology, the stationary Gibbs
sources having the SAME coordinates, bath and mass and smooth periodic
potentials with gradient norm at most A.

Equivalently, smooth conservative competitors can be chosen with

    dist_BL(P_j[0,h],P_Gibbs,j[0,h]) -> 0.              (2)

No hidden mixing rate, force-derivative ceiling, finite hidden dimension
inference, or identification of F_j is inserted into the proof. The
conclusion is an existence/stability theorem, not an algorithm acquiring
the competing potentials. The amplitude bound and full thermal source
class are physical information, not consequences of a fitted coarse law.

Full-path TV cannot replace the topology in (2), as the bounded shear
counterexample already proves. The compactness proof below gives a
particularly useful stronger intermediate fact: every vanishing-entropy
subsequence has a further subsequence converging SETWISE on the fixed
path space to a native Gibbs limit, which may initially have a Lipschitz
rather than smooth potential. Setwise convergence still differs from TV.

## 2. Thermal reduction of the initial stationary law

Let rho_j be the stationary density, nu_j its position marginal, and M
the centered Maxwell momentum density of covariance tau I. The exact
entropy-current square and conditional Gaussian logarithmic Sobolev
inequality give

    D(rho_j || nu_j M) <= sigma_j/(2gamma),
    TV(rho_j,nu_j M) <= epsilon_j:=sqrt[sigma_j/(4gamma)]. (3)

Each F_j is smooth and bounded, so the ordinary stationary kinetic
identities and integration by parts apply. The limiting force will be
only bounded measurable; it is identified through the martingale problem,
not by assuming a smooth stationary Fisher identity for that limit.

The product nu_j M is a mathematical comparison law, not an acquired
preparation. Its unknown nu_j is not supplied by (3).

## 3. A uniform L2 smoothing step with an explicit covariance

Let mu_0 be uniform position times M, the stationary free Kramers law.
Fix delta>0. Start FREE Kramers dynamics from ANY nu M, even singular nu.
Its terminal momentum is again M and independent of the initial q.
Write D_delta=integral_0^delta p_s ds. Conditionally on p_delta, D_delta
is Gaussian with mean

    [(1-exp(-gamma delta))/gamma] p_delta

and covariance v_delta I, where

    v_delta=(tau/gamma²)
        [2gamma delta-3+4exp(-gamma delta)-exp(-2gamma delta)]>0. (4)

Positivity follows because the bracket vanishes at zero and its derivative
in u=gamma delta is 2(1-exp(-u))²>0. Wrapping this nondegenerate Gaussian
around the torus gives a bounded density. Convolution with arbitrary nu
does not increase its supremum. Consequently the FREE endpoint density
relative to mu_0 is bounded by a finite C_delta, uniformly in nu.

Under a force with norm at most A, the Girsanov likelihood Z on [0,delta]
satisfies, uniformly in every initial state,

    E_free[Z² | Z_0=z] <= exp[A²delta/(2gamma tau)].       (5)

This follows by writing the square as the exponential martingale with
twice the drift integrand, times an exponential bounded by the right side.
Bounded drift ensures the required Novikov martingale property.

For initial nu M, let r be the forced endpoint density relative to mu_0
and r_0 the free endpoint density. Conditional Jensen gives

    integral r² dmu_0
      =integral r_0² (E_free[Z|Z_delta])² dmu_0
      <= C_delta E_free Z²
      <= C_delta exp[A²delta/(2gamma tau)].              (6)

Apply this to nu_j M and F_j, and call the resulting endpoint law
tilde_rho_j=r_j mu_0. By stationarity and data processing,

    TV(tilde_rho_j,rho_j)<=epsilon_j.                    (7)

Thus there is a uniformly L2-bounded family of actual initial densities
whose future path laws are TV-close to the original stationary sources.
No claim that arbitrary hidden states mix in time delta is involved.

## 4. Compactness of the free occupation operator

Let P_0 be stationary FREE Kramers path measure on [0,h]. For a bounded
fixed measurable state function g, define

    (A_g f)(path)=integral_0^h f(q_t)g(q_t,p_t)dt,
    A_g:L2(uniform_torus)->L2(P_0).                      (8)

**Lemma.** A_g is compact. The same statement holds for a fixed bounded
time-dependent g, including restriction of the integral to [s,t].

The elementary bound ||A_g||<=h||g||_infinity follows from stationarity
and Cauchy--Schwarz. Consider its Gram operator A_g* A_g. In its double
time integral, retain only |s-t|>=eta. For such pairs the joint density
of q_s,q_t is bounded: their difference is a wrapped Gaussian with
covariance

    [2tau/gamma²][gamma|t-s|-1+exp(-gamma|t-s|)] I.

The conditional expectation of g_s g_t is bounded by ||g||_infinity².
Therefore the retained integral has a bounded kernel on the compact
torus squared and is Hilbert--Schmidt.

The discarded diagonal strip has bilinear norm at most

    2h eta ||g||_infinity² ||f||_2 ||k||_2.              (9)

Indeed each two-time expectation is bounded by the product of the
stationary L2 norms, and the strip has area at most 2h eta. Hence A_g*A_g
is an operator-norm limit of compact operators and is compact. The Hilbert
space implication that A*A compact implies A compact proves the lemma.

This is the missing spatial averaging statement. It does not assume that
F_j(q_t) converges pointwise or strongly in L2, and it does not infer a
Markov model merely from the limiting visible record.

## 5. Weak-star force convergence identifies the true native limit

By weak-star compactness of the L-infinity ball on a finite torus, after
subselection F_j converges weak-star to a bounded measurable F, ||F||<=A.
Since L1 is separable this subsequence can be chosen sequentially.
In particular F_j converges weakly in L2.

Start the forced source F_j from tilde_rho_j. Its full path density
relative to P_0 is

    R_j(path)=r_j(Z_0) Z_Fj(path).

The conditional bound (5), now over h, and (6) imply

    ||R_j||_L2(P0)^2
      <= C_delta exp[A²(delta+h)/(2gamma tau)].           (10)

Choose a weak L2 subsequential limit R. Positivity and pairing with the
constant function show R>=0 and E_P0 R=1, so Q=R P_0 is a path law.
Because every bounded path functional lies in L2(P_0), Q_j converges
setwise to Q. Equation (7) gives the same setwise limit for the original
stationary source paths.

For a smooth compact-in-momentum test phi, write the martingale problem
with L_j=L_0+F_j(q) dot grad_p. Fix a bounded past-measurable multiplier
Psi. All terms involving the fixed F can be passed using weak L2
convergence of R_j. The only moving term is bounded by

    |E_P0 R_j Psi integral_s^t (F_j-F)(q_u) dot grad_p phi(Z_u)du|
       <= ||R_j||_2 ||Psi||_infinity
          ||A_grad_p_phi(F_j-F)||_2 ->0,                (11)

by compactness of A and weak L2 force convergence. Thus Q solves the
martingale problem for the SAME kinetic equation with bounded Borel
position force F and the original bath.

That martingale problem is weakly unique. Bounded-drift Girsanov constructs
it from free Kramers dynamics, and inverse Girsanov turns any solution
back into the unique free source. No derivative bound or assumed hidden
Markov closure is required. The limiting Markov property is a consequence
of this identified native martingale problem and its uniqueness.

## 6. Vanishing dissipation makes the limiting force conservative

Initial marginalization of the setwise convergence, together with (3),
shows the limiting state law has the product form rho=nu M. Stationarity
passes because the approximating path laws are TV-close to stationary
laws. The position marginal nu is an ordinary probability measure;
the proof need not initially assume its smoothness.

Use the stationary martingale identity on phi(q)p_i, with momentum
cutoffs and the uniformly bounded moments to justify removing them.
The product Maxwell law gives

    tau integral partial_i phi dnu + integral F_i phi dnu=0,
    or grad nu=(F/tau)nu                                  (12)

as distributions. For a positive smooth torus approximate identity,
nu_epsilon satisfies

    |grad nu_epsilon| <= (A/tau)nu_epsilon.

Normalization and connected compactness bound its log density uniformly
above and below; those logs are equi-Lipschitz. Thus nu has a positive
Lipschitz density, bounded away from zero. Passing (12) distributionally
gives

    F=tau grad log nu almost everywhere,
    U=-tau log nu in W^(1,infinity), ||grad U||<=A.        (13)

The actual limiting native force is conservative. This conclusion did
not replace F_j nu_j by a guessed product of weak limits; equation (11)
is the required identification step.

## 7. Smooth conservative competitors and the claimed topology

Mollify U periodically. Then U_epsilon is smooth,
||grad U_epsilon||_infinity<=A, U_epsilon->U uniformly, and its force
F_epsilon converges to F in L2. Its Gibbs position density nu_epsilon
converges uniformly to nu. Bounded-drift Girsanov gives

    D(P_F^(nu M)[0,h] || P_Fe^(nu_e M)[0,h])
      =D(nu||nu_e)
          +[h/(4gamma tau)] integral |F-F_e|² dnu ->0.   (14)

The bounded positive Gibbs densities make all terms legitimate. Thus the
limiting source is itself a TV limit of smooth Gibbs sources within the
same force-amplitude ceiling. Combining the subsequential setwise limit
with this approximation proves (2) by the usual contradiction argument.

The proof also upgrades to weak convergence with second moments in the
uniform path metric. Bounded forces and the stationary OU representation
give uniform moments of every fixed order for sup_(t<=h)|p_t|. Weak path
convergence plus this uniform integrability gives Wasserstein-2 convergence
along each identified subsequence. Therefore the distance to the smooth
Gibbs class also tends to zero in that Wasserstein path metric. This is
still weaker than full path TV and is consistent with the shear example.

## 8. Consequence and limits

Force derivatives are unnecessary for equilibrium explanation at this
weaker topology. The source class itself supplies both a thermal
momentum coercivity and the compact occupation map that averages bounded
fine spatial variation in the weak experiment law. The earlier force
Lipschitz bound was a route to the stronger full-TV conclusion, not a
necessary hypothesis for every scientifically useful approximation.

The result is qualitative. It gives neither an effective uniform modulus
nor an acquisition procedure for F, nu or U. Every fixed finite-alphabet
passive path experiment respects the subsequential setwise limit. A
fixed bounded-gain, nonzero-noise Gaussian observation interface can also
use the Wasserstein coupling with the usual conditional Gaussian KL
argument. Uniformity over instruments with unbounded precision, gain,
timing resolution or force-dependent observation rules is not asserted.

Feedback that changes the physical dynamics is a separate theorem; passive
adaptive selection of observation times does not itself change the native
path law. Apparatus and preparation resources remain attached to whichever
observation consequence is invoked.

## 9. Independent challenge outcome

Every load-bearing step in the root-proposed route has a valid ordinary
argument above. The key checks were: conditional terminal Gaussian
variance remains positive; endpoint L2 uses one factor of the free density
ceiling and conditional Jensen; the full-path L2 likelihood bound is
conditional on the initial state; the occupation cutoff is compact even
for bounded signed g; moving force terms pass by compactness; and the
limiting Markov source is proved by Girsanov uniqueness rather than
assumed. No new empirical record or physical preparation was used.
