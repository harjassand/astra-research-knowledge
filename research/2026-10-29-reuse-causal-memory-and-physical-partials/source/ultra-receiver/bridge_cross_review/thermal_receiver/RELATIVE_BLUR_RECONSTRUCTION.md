# Independent reconstruction of the nonlinear finite-exposure bridge

This checks the mathematical dependency before final software intake.
It does not accept an unfinished budget or physical receiver. The
model is the fixed one-hidden-quartic, unit-mobility bath with known
SPD M-matrix K, connected p-to-v access g=R_pv>0 and zero force.
The two assigned paths satisfy that condition. If g=0 a claimed
strictly positive contrast must be declined.

## 1. Direct semigroup proof of the required positive correlation

There is a self-contained alternative to the finite-grid FKG passage.
Let P_t be the reversible Langevin semigroup at parameter a and
f(x)=x_p, g3(x)=x_v^3. Both have zero stationary mean. Integration by
parts and the gap imply

    E_pi[f P_t g3]
       =theta int_0^infinity
                      E_pi[partial_p P_(s+t) g3] ds.    (1)

Indeed differentiate E_pi[f P_(s+t)g3], integrate from zero to infinity,
and use its limit zero. Cooperative synchronous comparison makes
P_r g3 increasing. Equivalently the flow derivative J(r,0) is
entrywise nonnegative, and
partial_p P_r g3=E[3 X_v(r)^2 J_vp(r,0)]>=0.
The derivative is integrable: J<=exp(-Kr) entrywise and the stationary
second moment is Gaussian-dominated. Thus (1) proves exactly
h_a(t)=E[X_v(t)^3 X_p(0)]>=0, without an unexamined stationary
association limit or a Gaussian nonlinear law. Standard truncation/
Dirichlet-form closure covers the unbounded polynomial observables.
This is ordinary covariance/semigroup calculus, not a new correlation
principle. The original FKG/cooperative argument has compatible premises.

## 2. Relative covariance, rather than absolute blur bias

Let C_a(t)=E[X(t)X_p(0)]. It obeys
C_a'=-K C_a-a e_v h_a. The exact initial covariance difference is
eta g R_.v, eta=(theta d-v(a))/d^2>=0. Hence

    C_0(t)-C_a(t)
       =exp(-Kt)eta g R_.v
          +a int_0^t exp[-K(t-r)]e_v h_a(r)dr.          (2)

All entries are nonnegative. Its pp component is at least
s_a exp(-K_pp t), since exp(-Kt)_pp>=exp(-K_pp t).
Rectangular exposure integrates stationary covariance with triangular
weight, giving the stated relative retention

    contrast_exposure>=s_a*2(z-1+exp(-z))/z^2,
    z=K_pp delta.                                    (3)

At z=1 the factor is 2/e. Thus delta need not vanish with the tiny
signal s. This statement is nonlinear in a, valid against every
a>=Delta by scalar contrast monotonicity. Replacing it by an absolute
O(theta delta) blur error would impose an unnecessary resource debt.

## 3. A's longer-exposure input and its actual geometry

The first term of (2) gives the stronger survival retention
L(t)=(exp(-Kt)R)_pv/g. For a known endpoint tridiagonal path,
f(t)=exp(-Kt)_pv/g is a nonnegative normalized density with Laplace
transform det(K)/det(K+zI). Thus its travel variable has the sum-of-
independent-exponentials law with eigenvalue rates, and

    mu=Tr R, variance=Tr R^2,
    B_L(delta)=1-E[(1-T/delta)_+^2]
          >=2mu/delta-(mu^2+variance)/delta^2.           (4)

This matches A's accepted LONG_EXPOSURE_INTERFACE. The source's
particular scalar choice delta=3(mu^2+variance)/(2mu) gives retention
8mu^2/[9(mu^2+variance)]. No optimal-exposure claim follows. The
same continuant argument applies to either assigned endpoint chain,
but K2 must use ITS OWN traces and curvature, not the K3 numerical
packet copied across the changed shunt.

The exposure mean is not Gaussian at a>0. The small long-window
variance instead follows from the actual flow derivative. For
F=delta^-1 int X_p, initial and Wiener derivatives are nonnegative
and bounded entrywise by their harmonic counterparts. Product
Brascamp--Lieb/Wiener Poincare has form

    Ecal(F)=theta grad_0 F^T R grad_0 F
                                    +int |D_s F|^2 ds.

R is entrywise nonnegative, so Ecal(F)<=V_delta POINTWISE, where
V_delta is the harmonic exposure variance. Applying the SAME form
to F^2 gives

    Var(F^2)<=4 V_delta E F^2<=4V_delta^2.              (5)

Independent Gaussian detector variance sigma_delta^2 tensorizes,
so with S_delta=V_delta+sigma_delta^2,
Var[(F+eta)^2]<=4S_delta^2. Endpoint conditioning and the gap pay
correlations between nonoverlapping exposures; they are not IID.

For spacing h=delta+1/kappa the summed constant is bounded by
4+8/(e-1)<9 (e>8/3 suffices). The harmonic input may use

    V_delta<=min(theta R_pp,2theta(R^2)_pp/delta).      (6)

Equations (4)--(6) justify A's long-exposure packet under its exact
M-matrix, one-quartic, stationary bath/electronics conditions. The
K3 numerical values have already passed root whole intake; this
review does not rerun or widen their scope.

## 4. Initialization and physical gates

The zero-start contraction bound for passive squared scores survives
exposure averaging by Jensen, using the SAME electronics noise in
the comparison. Observation duration is t0+(Q-1)h+delta, safely
bounded by t0+Qh. Detector variance Sdet/delta assumes the warranted
white-output-noise convention; it is not constant when the exposure
is changed. Nonoverlap is needed for independent electronics.

The known harmonic reference covariance is a mathematical reference,
not an observed/calibrated baseline for free. Calibration errors must
be in the actual score units and cover both hypotheses. Colored
electronics, unknown metric/mobility, altered bath, other quartics,
unqualified geometry or temperature can invalidate this receiver.
No finite-Delta full-time-series likelihood optimum is supplied by
the correlation or Dirichlet bounds.
