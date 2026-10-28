# Three displayed identities reconstructed from the P1 native return

This is an intake-owner mathematical reconstruction dated 2026-10-28, after
reading the completed native response. It is not an acquired producer proof,
independent-at-start review, execution of the reported 31 checks, novelty
assessment, or verification of the unavailable PDF/ZIP. The whole wave programme
remains source report only. The following three precise subresults have complete
proofs here and can be accepted at their own conditional mathematical scopes.

## A. An affine lift of a supplied transported density

Let K(t) be a C1 real symmetric d by d matrix on an interval. Write
x=(q,v,W) in R^(2d+1), and set

    B = [[0,I,0],[-K,0,0],[0,0,0]],
    M = [[K,0,0],[K',K,0],[0,0,0]].

On (t,x), use the torsion-free affine connection whose only nonzero
coefficients are Gamma^i_00=(Mx)^i for spatial i. Let mu be a supplied C1
nonnegative density satisfying

    partial_t mu + (Bx).grad_x mu = 0.

Then V=(1,Bx) is geodesic, A=mu V tensor V is positive semidefinite as a
contravariant quadratic form and div_nabla A=0. For constant Lambda>=0,
b=Lambda W^2/2 has H_nabla b=Lambda dW tensor dW and A:H_nabla b=0.

Proof. Direct block multiplication gives B'+B^2=-M and tr B=0. Thus
(V.grad)V=(0,(B'+B^2)x) and the connection adds (0,Mx), proving
nabla_V V=0. The coordinate connection trace Gamma^a_ab vanishes: the only
possible nonzero symbols have two lower time indices and spatial upper index.
Consequently div_nabla V=tr B=0. The tensor product rule gives

    div_nabla(mu V tensor V)
      = [V(mu)+mu div_nabla V] V + mu nabla_V V = 0.

Positivity is A(alpha,alpha)=mu [alpha(V)]^2>=0 for every real covector alpha;
this is not a Lorentzian metric positivity assertion. The W row of M is zero,
so the connection correction to the coordinate Hessian of b vanishes. The
ordinary Hessian is Lambda dW tensor dW; V(W)=0 proves zero pairing.
For the associated flow q'=v, v'=-Kq,
U'=(q^T Kq-|v|^2)/2, differentiating W=U+q.v/2 also gives W'=0.

Scope. No construction of mu from a quantum field is proved here. This is the
auxiliary affine connection, not the physical Brinkmann Levi-Civita connection.
It supplies no Monge-Ampere existence theorem, boundary energy identity,
physical projection, sharp local smoothing, measurement or device.

## B. A trace-class positive majorant of a Hilbert curve

Let h:[0,ell]->H be an absolutely continuous unit-norm curve in a real or
complex Hilbert space, with ||h'(s)||<=1 almost everywhere and finite ell>=0.
Extend h constantly through ell+1, with derivative zero on the added tail. Then

    Gamma = 2 integral_0^(ell+1) (|h><h|+|h'><h'|) ds

is positive trace class, dominates |h(s0)><h(s0)| for every s0 in [0,ell],
and has tr Gamma<=2+4ell. Integrals are Bochner integrals in trace norm; the
integrands have integrable trace norm. The ell=0 case means a supplied constant
unit vector and the same constant extension.

Proof. For any z in H, put f(s)=<z,h(s)>. For each t in [s0,s0+1], absolute
continuity and Cauchy-Schwarz imply

    |f(s0)|^2 <= 2|f(t)|^2 + 2 integral_s0^(s0+1) |f'(r)|^2 dr.

Integrate over that unit interval. Both integrands are nonnegative, and the
interval is contained in [0,ell+1]. The resulting inequality is
|<z,h(s0)>|^2<=<z,Gamma z>, which proves operator domination simultaneously
for all z. Taking traces gives

    tr Gamma = 2[(ell+1)+integral_0^ell ||h'||^2] <= 2+4ell.

Scope. The orbit and its arclength are supplied, not acquired. This accepts the
abstract majorant, not the native's Gaussian speed formula, field calibration,
1+NT lower bound, physical recovery or practical advantage. Reparametrizing an
actual orbit and paying its length remain application obligations.

## C. A singular positive moment tensor controls its residual

On a measure space let a,b be measurable Hilbert-valued functions, and let
w be real n-vector valued with finite n. Assume

    integral ||a||^2 |w|^2 < infinity,   e=integral ||b||^2 < infinity.

Define the real symmetric matrix T=integral ||a||^2 w w^T and real vector
R=2 Re integral <a,b> w. Then R lies in range T and

    R^T T^+ R <= 4e,

where T^+ is the Moore-Penrose pseudoinverse. No positive lower eigenvalue is
assumed. The stated integrability makes each component of R well-defined.

Proof. For every real xi, Cauchy-Schwarz gives

    |xi^T R| <= 2 sqrt(xi^T T xi) sqrt(e).

Every xi in ker T therefore annihilates R. Since T is finite dimensional and
symmetric, (ker T)^perp=range T, proving the range claim. Put xi=T^+R and
y=R^T T^+ R>=0. The identities TT^+R=R and T^+TT^+=T^+ give
y<=2 sqrt(y e). If y=0 the conclusion holds; otherwise square and divide by y
to obtain y<=4e. This also covers T=0, when R=0.

Scope. The algebraic inequality needs no transport equation. The native's
additional Da+A a=b and A*=-A may supply an application, but deriving div T=R
needs that application's transport, measure and boundary identities. The
positive divergence-free completion, choice of d0, face flux and determinant
energy are not proved by this inequality. No infinite-dimensional closed-range
assertion, physical residual acquisition or small error in every tensor
component is inferred.

## Completed source-exposed internal review

The intake owner checked the displayed native formulas against each proof above,
including the C1 connection product rule, vanishing connection trace, covector
positivity, the unit interval at either endpoint, constant-tail derivative,
trace-class integrability, complex inner-product real part, zero tensor and
singular range cases. All three arguments close at the exact stated scopes.
Decision: ACCEPTED INTERNALLY VERIFIED for A, B and C only at the source and
unit versions bound by the review overlay. This is a completed substantive
owner review, not a claim of a second independent reviewer. No external or
specialist review is required for this scoped acceptance.

The unavailable governing wave files leave the coherent field construction,
auxiliary energy, wall estimates, Gaussian calibration/lower bound, quadratic
background classification, beyond-quadratic completion and physical energy
counterexample at source-report scope. Reported independent derivations and 31
checks were not read or replayed. Mathematical acceptance of A-C supplies no
acquired field, measurement, working device, historical priority or advantage.
