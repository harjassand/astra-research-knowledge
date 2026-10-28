# Independent reconstruction of the finite-force mean inputs

This records analytical work while C's final receiver/budget remains
live. It is NOT acceptance of unfinished calibration, classification
or cost software. No model or quadrature was rerun. The functions
below are the inputs that a frozen receiver must use and qualify.

## 1. Actual finite-force response

For the stipulated SAME mechanical bath and force U at port p,
Gaussian conditioning at the one hidden quartic gives

    X_v=sqrt(theta d) Z,
    density Z proportional exp[-Z^2/2-beta Z^4/4+hZ],
    beta=a theta d^2, h=Ug/sqrt(theta d),
    E Y=U(b-g^2/d)+(g/d) E X_v.

For h>0 define the response ratio

    r_beta(h)=E X_v/(Ug)
      = E_beta[Z^2 sinhc(hZ)]/E_beta[cosh(hZ)],          (1)

where the expectations on the right use the even, zero-force
quartic-tilted law. The port mean decrease from harmonic reference
is exactly U g^2/d [1-r_beta(h)]. This is an actual finite-U
formula, not the FDT derivative substituted for a nonzero force.

For fixed h, write (1) as an expectation of
|Z|tanh(h|Z|)/h under the absolute density proportional to
exp[-Z^2/2-beta Z^4/4] cosh(hZ). This observable increases in |Z|.
Increasing beta multiplies the density by a decreasing function of
|Z|, so r_beta(h) decreases. Hence an a=Delta contrast lower endpoint
is uniform against every a>=Delta. This argument needs no small-a
assumption and remains valid at the high-force input.

## 2. Paid fixed-U=1 enclosure

Let m2=E_beta Z^2. Zero-force absolute quartic tilt is stochastically
dominated by the standard absolute Gaussian. Consequently

    1<=E_beta cosh(hZ)<=exp(h^2/2).

The elementary bound sinhc(t)<=1+t^2 cosh(t)/6 and Gaussian
absolute-moment domination give

    m2 exp(-h^2/2)<=r_beta(h)
       <=m2+(h^2/6)(h^4+6h^2+3) exp(h^2/2).            (2)

The upper uses E_G[Z^4 cosh(hZ)]=(h^4+6h^2+3)exp(h^2/2).
Thus the weak_field calculation can use the already acquired m2
interval with no new quadrature. At theta=1,U=1, h=g/sqrt(d) and
the contrast is g^2/d times 1-r. A positivity check must use the
UPPER endpoint of (2), as the source does.

## 3. High-force quadrature structure

At U=1/g and theta=1, Ug=1 and h=1/sqrt(d). Let

    J0=int_0^infinity exp[-z^2/2-beta z^4/4] cosh(hz)dz,
    J2=int_0^infinity exp[-z^2/2-beta z^4/4]
                                             z^2 sinhc(hz)dz.

Then r=J2/J0. In particular J2 is not the ordinary second moment;
the factor 1/h in z sinh(hz)/h is exactly what produces the correct
mean response. The source's z=0 branch has its continuous value.

The identity sinhc(hz)=int_0^1 cosh(thz)dt explains a common fourth-
derivative upper bound for both integrands. Starting from z^m,
iterate the POSITIVE coefficient recurrence

    P -> P'+(h+z+beta z^3)P, m=0 or 2.

On a positive panel [l,r] this polynomial at r times
exp[-l^2/2-beta l^4/4+hr] bounds the absolute fourth derivative,
including the integral over t in [0,1]. Thus the same h_panel^5/2880
Simpson remainder applies to the high-field integrals.

Dropping the negative quartic tail and completing the square gives,
for L>h, t=L-h,

    tail J0<=exp(h^2/2-t^2/2)/t,
    tail J2<=exp(h^2/2-t^2/2)
                                  [t+(1+h^2)/t+2h].    (3)

The second follows from sinhc<=cosh and integrating (t+h)^2 against
the shifted Gaussian. These are genuine infinite-tail bounds. The
reported high-force contrast must again use 1-r_UPPER.

## 4. Initialization, work and comparison boundaries

The force-shifted Gibbs law is still strongly log-concave, with the
same Hessian floor. Stationary fluctuation and mean-read bounds may
use that floor, but a zero-start burn-in cannot silently use the
UNFORCED stationary total second moment. It must include the force-
shifted mean/energy. For example, strong log-concavity gives
Cov_U<=theta R and ||E_U X||<=|U|/kappa, yielding the sufficient
total moment bound theta TrR+U^2/kappa^2. A concrete receiver must
state the initialization/admission bound it actually consumes.

U is a conservative mechanical force and Y a displacement. The work
is int U dY. Constant holding in stationary equilibrium need not
have a nonzero mean mechanical dissipation rate. The harmonic value
bU^2/2 is a quasistatic/reference loading-energy scale and can be
recovered on a reversible return; it is not automatically an
irreversible full-cycle joule lower bound or power U^2 times duration.
Peak force, displacement, preparation, squared-input proxies and
reference energy must be reported with their actual protocols.

The full SAME-bath Gaussian/nonlinear likelihood is allowed the same
record. A's stationary local near-Gaussian score result is not a
finite-Delta optimality theorem. Its finite-alternative continuous-
path bounds and C's finite-risk upper plans must retain their separate
starts, detector/geometry assumptions and quantifiers. A fixed-peak
mean plan and a high-peak plan are different resource contracts, not
an algorithmic proof of passive superiority or its negation.
