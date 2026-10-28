# Compatible-jet inverse from one global contact certificate

This receiver uses the ORIGINAL quartic F and k=p6/T^2, with k(0)=0.
It does not add epsilon T and does not use the calibrated70 primitive.
Its input data are five chosen minor-conjugate coordinates, not the four
physical Piola stresses. The compatible-state/noise promise is explicit.

## General receiver

Suppose a differentiable energy W has global scalar supports k(A) with

    P_A(X)=W(A+X)-W(A)-DW(A):X-k(A)detX>=0

for every base A and increment X. Put m(A)=(A,detA) and

    j(A)=(DW(A)-k(A)cofA,k(A)).

For the global receiver assume also P_B(X)>=beta|X|^4 for all B,X,
with a supplied beta>0. The original certificate gives beta=1/1600000.

No differentiability of k or C2 representative is needed. Given a candidate
A, suppose a GLOBAL contact certificate proves P_A(X)>=mu|X|^2, mu>=0.
The paid candidate certificate normally supplies a positive mu.
For any other compatible state B, adding the two support inequalities gives

    [j(B)-j(A)]:[m(B)-m(A)]>=mu|B-A|^2+beta|B-A|^4.    (1)

Let d=|B-A| and take rational c>=sqrt(1+|A|^2). The determinant identity
detB-detA=cof(A+(B-A)/2):(B-A) gives

    |m(B)-m(A)|<=d sqrt[1+(|A|+d/2)^2]<=d(c+d/2).

Hence a global bound for ANY residual rho>=|j(B)-j(A)| is the unique
nonnegative root dmax of

    dmax(mu+beta*dmax^2)/(c+dmax/2)=rho.                  (2a)

The left side increases strictly for dmax>0: its derivative numerator
is c*mu+3c*beta*dmax^2+beta*dmax^3>0. Rational bisection gives a rigorous
upper bound without a root oracle. This works even with mu=0, including
the flat candidate A=0. If rho<2mu, the simpler bound

    |B-A| <= c rho/(mu-rho/2)                            (2b)

also holds. These are GLOBAL localization bounds: B is not assumed to lie in a Newton
ball or a bounded prior set. For noisy data w with |w-j(B)|<=nu, any
proposal A may use rho=|j(A)-w|+nu. Exact l1 bounds may replace Euclidean
norms on the right. A poor proposal or excessive noise leaves the sharp
linear regime or gives a wide bound; no acquisition success is assumed. With only the
quartic margin, the receiver is Hölder near zero, as expected for a flat
quartic energy. The paid candidate quadratic margin supplies a much
sharper linear local regime while retaining the global guarantee.

The positive quartic margin beta alone proves injectivity by(1), including
comparison with A=0. For the continuous original rational jet,
the mu=0 bound at A=0 also proves properness, so j is a homeomorphism
onto its closed image. Thus this is a compatible-state
inverse receiver despite the proven absence of a C2 convex lift at zero.
It does not define an inverse on all of R5 or claim that arbitrary noisy
data lie in the four-dimensional image j(R4).

## Paid conditioning for the original rational-selector energy

At a rational nonzero A, specialize the frozen180-feature support identity
to obtain a14 by14 rational Gram in the features

    Z14(X)=(X_0,...,X_3, all ten X_iX_j).

If M_A substitutes the A monomials in Z180, then exactly

    P_A(X)=Z14^T R_A Z14,
    R_A=M_A^T R180 M_A/T(A)^2.

M_A has full14-column rank whenever A!=0. A useful mu can be proposed
from the4 by4 Schur complement of the quadratic block, then certified
by exact LDL of R_A-mu I_linear. The eigensolver only proposes mu; its
error is not trusted. This certifies a global increment bound, not a
local Jacobian bound extrapolated to all states.

The matched coarse receiver uses the SAME proposal and SAME five noisy
data, but retains only the original theorem's mu0=T(A)/2400000. The
new receiver pays the explicit14-Gram specialization and exact LDL to
improve that conditioning. This is an ordinary SOS contact/error-bound
composition, not a new universal nonlinear solver or a claimed historical
priority result.

## Executed discriminating attack

`inverse_experiment.py` uses exact data j(I) plus a fixed rational noise
vector with component magnitude10^-12 and known l1 bound5*10^-12.
The two frozen starts are a different exact-stress branch and a nearby
nondegenerate state. Least squares proposes states only. The same
proposals and data feed BOTH global receivers. Each proposed state is
rounded to46-bit rational coordinates before any claimed certificate.

The exact14-Gram identity and LDL prove mu=.000646578 at both resulting
proposals. The receivers return state-error upper bounds approximately
2.0013e-8 and2.0007e-8. The matched coarse bounds are approximately
1.5528e-5 and1.5523e-5, about775.9 times wider. Ground truth is used
only as an executed control: actual state errors are about3.6093e-10
and lie within both certificates. The flat A=0/mu=0 fallback also
returns a finite, deliberately weak global bound; it does not pretend
that a zero-Jacobian acquisition step succeeded.

Each14-Gram conditioning acquisition, including exact LDL, took about
.020s, and its independent literal coefficient identity check about
.015–.020s. Proposal acquisition took10 and7 function evaluations,
about.004s and.0006s. The module's final measured elapsed time was
about.77s excluding Python startup, with about.60s for imports/literal
setup and.073s for common jet/Jacobian compilation. The accepted180
input was not reacquired or declared free; its original costs remain
upstream. No large SDP or numerical inverse accuracy guarantee is used.

### A stress-only ambiguity exposed, rather than assumed away

Let t=d/a for diagonal A. Write

    P(t)=4p0+2p2 t^2+L(3t-t^3),
    R(t)=4p0 t^3+2p2 t+L(1-3t^2),
    Sa=P(1), Sd=R(1).

Exactly Sa R(t)-Sd P(t) has roots t=1 and the two roots of

    3931850000410343971 t^2
      -28131936792459066116 t-1207698022677591029=0.

For each real root set a^3=Sa/P(t), d=ta. The script supplies rational
root-isolation and cube-root boxes, verifies the ratio identity, and
checks the off-diagonal stresses vanish. The three actual states are
approximately

    diag(2.8692166856,-.1224445386),
    diag(1,1),
    diag(.3740476575,2.6922307608).

All have EXACTLY DF(I). The latter two have positive determinant.
Their rational jet intervals are disjoint; the normal components are
approximately.1376878646,.3452233542,.1141229011. Thus ordinary stress
inversion cannot uniquely recover these states, including within the
orientation-preserving class. The receiver's extra five-coordinate
contract is essential and is not an acquired physical measurement.

The new data are the ORIGINAL rational-selector jet, not DG70 data;
the energy and calibration differ. The775.9-fold comparison is only
between receivers for the SAME original five-coordinate data. This
operation is retained as a qualified mathematical branch certificate,
not evidence of a material inverse, a universal nonlinear solver, or
a70-specific entropy/PDE advantage.
