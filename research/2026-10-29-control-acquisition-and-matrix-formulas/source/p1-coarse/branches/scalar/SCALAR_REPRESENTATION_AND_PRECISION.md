# Scalar response: useful closure, a stable compression certificate, and the precision obstruction

28 October 2026. New branch construction in the P1 successor investigation.
These are ordinary mathematical arguments and exact synthetic witnesses.
They do not claim a measured instrument, an independently audited whole proof,
a novel general convex principle, or civilisation-level practical capability.

## Research decision

Keep P1's bounded-error scalar acquisition and continuous-control certificates
as a component. Do not make recovery of a complete static port Gram the main
scientific agenda merely because it eliminates the microscopic state dimension.
Current Astra N1082 already acquires that exact operational quotient, including
a generic positive reference to illuminate relevant dark actuators. Existing
multiport identification provides a strong external comparator. The hard
remaining issue is observable conditioning, not a missing Woodbury identity.

The additional calculations here provide (i) an exact local derivative closure
for rank-one actuation, (ii) a residual-to-response error bound for an actual
projected model, valid even for signed arithmetic displacements, and (iii)
explicit witnesses showing why generic illumination does not acquire precision.
The first and second are useful coordinates/certificates. Neither includes a
complete noise-aware acquisition algorithm for the required global quotient.

## 1. Exact two-jet closure for rank-one actuation

Consider the retained P1 class with scalar residuals:

    J(u) = c0 + min_y [||y||² + sum_i u_i (g_i + b_i^T y)²].

Let x be a feasible anchor, Mx=I+sum_i x_i b_i b_i^T, and yx its minimizer.
Define

    r_i = g_i + b_i^T yx,
    c_i = Mx^(-1/2) b_i,
    C = [c_1 ... c_n],
    K = C^T C.

For any other feasible physical command u, set d=u-x and D=diag(d). Some d_i
may be negative; only u and x are physical commands. Completing the square
in the old objective gives the exact shifted problem

    J(x+d)-J(x) = min_z [||z||² + sum_i d_i (r_i+c_i^T z)²].       (1)

Its Hessian I+C D C^T is positive definite because it is congruent to M(u).
Solving the quadratic and applying Woodbury yields

    J(x+d)=J(x)+r^T D (I+K D)^(-1) r.                            (2)

This identity does not require an invertible K or an invertible D.
Sylvester's determinant identity ensures I+K D is invertible whenever the
physical quadratic in (1) is positive definite.

The envelope theorem and differentiated stationarity give

    p_i := J_i(x)=r_i²,
    H_ij := J_ij(x)=-2 r_i r_j K_ij.                            (3)

If every p_i>0, the scalar response's value, gradient and Hessian determine
its entire allowed nonlinear response law. Let s_i=sqrt(p_i)>0 and define

    Kplus_ij = -H_ij/(2 s_i s_j).                               (4)

The sign gauge on the unknown r conjugates K by a diagonal sign matrix,
which commutes with every D. Consequently

    J(u)=J(x)+s^T D (I+Kplus D)^(-1) s.                         (5)

This identifies an operational port-level model, not microscopic vectors.
It is a representation theorem with an exact two-jet premise. It does not
supply that jet from finitely many noisy scalar values without additional
acquisition and conditioning work. The Hessian contains O(n²) entries, so a
local two-jet is not the old O(n) tangent oracle.

### Third-order differential closure

At any point where p_i>0, write H=Hessian(J). Differentiating (3), using

    partial_k r_i = -K_ik r_k,
    partial_k K_ij = -K_ik K_kj,

gives, with repeated indices allowed,

    J_ijk = H_ij H_ik/(2p_i)
          + H_ij H_jk/(2p_j)
          + H_ik H_jk/(2p_k).                                  (6)

The closure is an exact model consequence. For one control it reduces to
J'''=3(J'')²/(2J'). A statistically significant violation can refute the
warranted rank-one quadratic source model at that point, provided the actual
derivative intervals and instrument errors support the comparison. Agreement
at finitely many points does not establish a global source class.

There is also a local converse. Suppose a C³ scalar J has p_i>0, a negative
semidefinite Hessian, and satisfies (6) throughout an open neighborhood. Put
s_i=sqrt(p_i), K=-diag(s)^(-1) H diag(s)^(-1)/2. Direct differentiation of
these definitions and (6) gives the same Riccati equations

    partial_k s=-K e_k e_k^T s,
    partial_k K=-K e_k e_k^T K.

Along a straight segment with displacement d these obey

    ds/dt=-K D s,       dK/dt=-K D K.

ODE uniqueness yields the solution underlying (5), until its denominator
ceases to be invertible. Therefore the differential identity supplies a
local rational realization. It does not by itself warrant extension across
a dark-gradient set, certify positivity on a larger command domain, or
supply an original nonnegative-dose source at a remote origin.

## 2. Dark derivatives defeat stable two-jet reconstruction

For a in {1/2,1}, take hidden dimension one, b_1=1, b_2=a, g=(1,0), c0=1.
Both actuators genuinely have rank one and obey ||b_i||²<=1. The exact law is

    J_a(u,v)=1+u-u²/(1+u+a²v).

At the zero command both laws have the identical jet

    J=1, gradient=(1,0), Hessian=[[-2,0],[0,0]].

At the admissible command u=v=1/2 on the radius-one simplex,

    J_1(1/2,1/2)-J_(1/2)(1/2,1/2)=3/104.                       (7)

Thus a zero second gradient does not establish an irrelevant actuator.
The missing interaction begins at third order.

The defect is not repaired by requiring merely strict positivity without a
quantitative lower bound. Replace g_2=0 by g_2=epsilon>0 in both sources:

    J_(a,epsilon)(u,v)
      =1+u+epsilon²v-(u+a epsilon v)²/(1+u+a²v).

For 0<epsilon<=2/3, the maximum entrywise difference between their two-jets
at zero is epsilon: the only leading difference is H_12. Yet their difference
at u=v=1/2 tends to 3/104 as epsilon tends to zero. All gradients at zero
are strictly positive. Hence there is no uniformly continuous inverse map
from these local two-jets to the global response law on this class without
an excitation/conditioning restriction. This is a limitation of that local
representation. The remote command itself immediately separates the sources
at fixed nonzero precision; no universal impossibility of control follows.

## 3. Even bright rank-two actuators are outside two-jet closure

One actuator of rank two can have

    f_A(u)= (1/2)u/(1+u/4)+(1/2)u/(1+3u/4),
    f_B(u)= u/(1+u/2).

Both have a rank-two realization with g=(1/sqrt(2),1/sqrt(2)). Their hidden
B^T B are diag(1/4,3/4) and diag(1/2,1/2), respectively. The actuator norms
are at most one. Both satisfy f(0)=0, f'(0)=1 and f''(0)=-1, but

    f_A(1)-f_B(1)=2/105.                                      (8)

Adding the same positive c0 places both in P1's retained class. Therefore
(5) and (6) are rank-one results, not consequences of arbitrary finite-rank
PSD actuation or of concavity. A finite-rank scalar ray generally contains
more spectral moments; general mixed interventions contain block/operator
information absent from the scalar two-jet.

## 4. A generic reference can hide a useful task signal by eight orders

Let m<=n. On m active actuators, choose the Gram K_m with diagonal one and
nearest-neighbor off-diagonal b=1/4; other off-diagonals are zero. This is SPD
by strict diagonal dominance, so it is B^T B for admissible rank-one actuator
vectors of norm one. Set g=e_1. Add n-m mutually orthogonal dummy actuators
with g_i=0. Set delta=kappa=1.

At the balanced reference x_i=1/(2n), half the dose remains available. Put
t=1/(2n). The active residual vector is

    r=(I+t K_m)^(-1)e_1,
    r_m=(-b t)^(m-1)/det(I+t K_m).                             (9)

The last formula follows by the tridiagonal cofactor expansion. Thus the
last port is nonzero (illuminated), but its local gradient is at most
(b/(2n))^(2m-2). Exact nonvanishing says nothing about a finite instrument.

Now prepare a task-directed reference with dose t*=1/[2(m-1)] on each of
the first m-1 active ports and zero on the last. Again half the dose remains.
The final residual is

    r_m*=(-b t*)^(m-1)/det(I+t* K_(m-1)).                      (10)

In each case add h=1/2 at the final port. The exact scalar response increase is

    DeltaJ = h r_m²/(1+h K^x_mm).                             (11)

For m=3,n=256, exact rational arithmetic gives

    balanced DeltaJ = 32768/1748538288356046129
                    = 1.874022445960166e-14,
    task-directed DeltaJ = 1/475608
                         = 2.102571865906377e-6.

The ratio is approximately 112,195,661. The same source, actuator, added dose
and norm bounds have very different required absolute resolution because
of preparation. The balancing strategy incurs the dilution, not a theorem
about the whole experimental problem. Adaptively locating and illuminating
active interactions remains possible; ordinary direct control may avoid
recovering the full model altogether. No shot count or photon lower bound is
inferred without a separate stochastic and physical instrument model.

More generally det(I+t K_m)>=1 and det(I+t* K_(m-1))<=exp(1/2), while
K^x_mm<=1. These give the lower bound

    DeltaJ_task / DeltaJ_balanced
      >= [n/(m-1)]^(2m-2) / [(3/2)e].                        (12)

This quantifies the dependence on intervention depth and dilution. It is not
a lower bound against every possible choice of anchor or acquisition strategy.

## 5. A residual certificate for a compressed global response

There is a useful way to retain approximate models without pretending a noisy
zero residual proves exact rank. In the actual shifted model (1), let Pi be
an orthogonal projection in whitened hidden coordinates. Its projected Gram
and residual energies are

    Khat_ij = c_i^T Pi c_j,
    rho_i = ||(I-Pi)c_i||².

Suppose these are known, or safely enclosed by a feasible family that really
has this PSD completion meaning. Let zhat minimize (1) over range(Pi), and
let Jhat(u) be the resulting restricted value. The vectors

    rhat = r+C^T zhat = (I+Khat D)^(-1)r

and Jhat are computable from r,Khat,D. The normalized physical Hessian obeys

    A(d)=I+C D C^T >= alpha I,
    alpha=1/(1+q), q=delta*kappa,

because M(u)>=I and M(x)<=(1+q)I. Its compression onto range(Pi) is also
positive definite, so signed arithmetic displacements cause no unproved
reduced-model singularity.

The residual of the restricted solution is

    e=A(d) zhat + C D r
     =(I-Pi) C D rhat.

Completing the square in the full quadratic yields the exact equality

    Jhat(u)-J(u)=e^T A(d)^(-1)e.

Cauchy-Schwarz on the residual columns now gives the operational error bound

    0 <= Jhat(u)-J(u)
       <= (1+q) [sum_i |d_i| |rhat_i| sqrt(rho_i)]².           (13)

The premise is an actual projection or a certified PSD residual completion,
not an arbitrary low-rank numerical approximation. Formula (13) has no
spectral-gap division and no need to call tiny eigenvalues exactly zero.
It also covers dark residuals algebraically. It is the ordinary Galerkin
residual argument expressed through scalar-response quotient data; it is
not claimed as a new general numerical-analysis principle.

This is a constructive piece for a global noisy compiler, but the hardest
obligation remains: acquire r,Khat,rho at useful precision and finite cost.
Intervals in those quantities require a verified bound over their joint
feasible family, including the sign gauge and positivity restrictions.
Simply substituting estimated values into (13) is not a certificate. The
P1 interval tangent controller remains the completed lower-information
route when a complete model cannot be acquired efficiently.

## 6. Existing constructions, actual addition, and source scope

The current N1082 capsule was retrieved at Astra commit
44b7e51f36b6dd4759a0227f23cc6b11671b1583. Its governing source
`ASTRA_PRO3_GLOBAL_RESPONSE_ACQUISITION.md` was read and verified with SHA256
`aebe53e9e530bc6bb3e1f30446ff4f942b9849303e992abaf5222f44a4a6a042`.
It already provides exact singleton/pair acquisition, PSD Nyström completion,
all-intervention response reuse, a generic illuminated reference, and an
explicit finite-noise/excitation caveat. Completed internal acceptance is
retained at that exact scope; this note does not reopen that review.

N1082's full quotient acquisition therefore precedes the present alternative
local-jet coordinates. The useful addition here is the explicit derivative
closure, its precise rank/darkness failures, the task-relative precision
witness, and (13) as a usable response error functional for projected data.
None establishes a new physical interface or broad economic superiority.

A primary external comparator is Philipp del Hougne, *Virtual VNA:
Minimal-Ambiguity Scattering Matrix Estimation with a Fixed Set of Virtual
Load-Tunable Ports*, arXiv:2403.08074v3 (14 February 2025),
https://arxiv.org/html/2403.08074v3 . Sections II and III formulate tunable
load/port reconstruction using a Schur complement, with closed-form and
intensity-only approaches. The article experimentally studies an eight-port
system. Its complex scattering observations and tunable-load contract are
different from the real SPD scalar P1 instrument, so their measurement counts
cannot be equated without translating the interfaces and calibration costs.
It nevertheless rules out presenting elimination of arbitrary microscopic
complexity through a finite port matrix as an untouched scientific opening.

The N1090 and N991 current capsules were inspected for comparison; their
specific results are not used as premises in any proof above. N1090's
monotonicity correction and operation-specific acquisition-count correction
remain in force. N991's first-capture probabilistic response is a distinct
instrument and does not justify importing a Laplace representation into P1.

## 7. Executable evidence

`jet_closure_checks.py` uses Python's standard library only. Its exact rational
formal power series computes a native scalar 3-jet independently of the
closure formulas, verifies all 27 ordered third partials in a nontrivial
three-actuator/two-hidden-coordinate instance, and verifies the reconstructed
law at four physical commands including signed displacement back to zero.
It also preserves the equal-jet dark and rank-two witnesses, exact chain
responses, and four exact checks of (13) at a nonzero reference with signed
displacements. The displayed residual certificates are conservative and are
not an executed economical model-acquisition result. Results are in
`JET_CLOSURE_CHECKS.json`.

These finite checks support the displayed arguments at their actual scope.
They do not validate a physical source model, imply successful noisy Gram
acquisition, or replace the ordinary proofs. The initial local environment
had no SymPy, so the final implementation was rewritten in exact
standard-library arithmetic; there is no runtime dependency to install.
