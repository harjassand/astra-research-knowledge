# Conditional clean-spectator curvature: operator-integral proof

26 October 2026. Original analytic proof. Two independent full-chain analytic audits PASS (attack_clean_spectator_core and derive_schur_inertia_principle).

## Statement

For all positive definite 2x2 matrices A2,H2 and h>0, let

    D(t)=det(A2+tI), N(t)=tr(H2 adj(A2+tI)),
    R(t,h)=(1+h/t)D(t)+N(t), L(t)=2D(t)+N(t),
    Q0(h)=integral_0^infinity [1/R(t,h)^2-2/L(t)^2]dt.

Let Ip(h) be the determinant-gradient integral in the clean-spectator
source, equivalently

    Ip(h)= integral_h^infinity du/det[H2+uI+2u A2/(u-h)]
           - integral_0^infinity du/det[H2+uI+3A2].

Then

    Ip(h)=0  ==>  Q0(h)<0.

In fact the proof establishes an explicit positive gap between a lower
bound for the unique Ip-zero and a sufficient threshold for Q0<0.
Commutativity of A2,H2 is not assumed.

Write A=tr A2, B=det A2, C=tr H2, delta=2-sqrt(3), and define

    h_cert = B/[A+C+sqrt(C^2+2AC+4B)].

The key quantitative conclusions are

    h_star > 4delta B/[A+C/3+2sqrt(B)] >= 4delta h_cert > h_cert,
    h>=h_cert ==> Q0(h)<0.

Here 4delta=8-4sqrt(3)>1.

## 1. Curvature transport

Write N(t)=Ct+E. Under t=2u,

    R(2u,h)-L(u)=2u^2+(C+2h)u+hA-B+hB/(2u)
                >=2u^2+hA-B+sqrt(2hB(C+2h)).

The increasing expression hA+sqrt(2hB(C+2h)) equals B at h=h_cert.
Consequently h>=h_cert gives R(2u,h)>L(u) for every u>0 and therefore

    Q0(h)=2 integral_0^infinity [1/R(2u,h)^2-1/L(u)^2]du<0.

## 2. A scalar integral inequality

For c>=2sqrt(d)>0,

    K(c,d)=integral_0^infinity x^2/(x^2+cx+d)^2 dx
            >=1/(c+sqrt(d)).

Equality holds only for c=2sqrt(d). To verify this, factor the quadratic
as (x+r)(x+s), r>=s>0. For r>s,

    K=(r+s)/(r-s)^2-2rs log(r/s)/(r-s)^3.

The desired bound is equivalent, for z=sqrt(r/s)>=1, to

    2log z <= (z^2-1)(z^2+4z+1)/(2z(z^2+z+1)).

The difference vanishes at 1 and has derivative

    (z-1)^4(z+1)^2/[2z^2(z^2+z+1)^2]>=0.

The equal-root limit is K=1/(3r).

## 3. Haar reduction and a weighted lower bound for h_star

Use normalized Haar measure on complex unit vectors psi in C^2 and put
alpha=<psi,A2 psi>, beta=<psi,H2 psi>, sigma=beta+3alpha.
The identity E<psi,M psi>^(-2)=1/det M gives, by applying Tonelli to
both nonnegative terms separately and then setting x=u-h,

    Ip(h)=E[K(beta+h+2alpha,2alpha h)-1/sigma].

Because beta>0, c=beta+h+2alpha>2sqrt(2alpha h), so the scalar bound
is strict. Put n=alpha-h-sqrt(2alpha h); then c+sqrt(d)=sigma-n>0.
The reciprocal tangent inequality is the exact identity

    1/(sigma-n)-1/sigma-n/sigma^2
       =n^2/[sigma^2(sigma-n)]>=0.

Thus, with X=E[alpha/sigma^2], Y=E[1/sigma^2],
Z=E[sqrt(alpha)/sigma^2],

    Ip(h)>X-hY-sqrt(2h)Z
          >=X-hY-sqrt(2hXY),

where the second step is Cauchy-Schwarz, Z^2<=XY.
Since delta+sqrt(2delta)=1,

    h<=delta X/Y ==> Ip(h)>0.

Ip is strictly decreasing in h in its original t-integrand and has a
unique positive zero (also follows from the earlier elementary operator
bracket). Hence

    h_star>delta X/Y.

## 4. Determinant lower bound for the weighted matrix mean

Set S=A2+H2/3, T=tr S=A+C/3, V=det S. Define

    M=V E[psi psi*/<psi,S psi>^2].

Then tr M=1, and the factors of 3 cancel to give X/Y=tr(A2 M).
The identity

    E[1/<psi,S psi>] = integral_0^infinity du/det(S+uI)

follows by diagonalizing S (both sides are the divided logarithm).
Differentiating in S yields the positive-matrix integral

    M=V integral_0^infinity adj(S+uI)/det(S+uI)^2 du.

Minkowski's determinant inequality for positive 2x2 matrices, in its
integral form (sqrt(det) is concave and homogeneous), implies

    sqrt(det M)
       >=V integral_0^infinity du/det(S+uI)^(3/2)
       =2sqrt(V)/(T+2sqrt(V)).

The last elementary integral is

    integral_0^infinity (u^2+Tu+V)^(-3/2)du
       =2/[sqrt(V)(T+2sqrt(V))].

The 2x2 trace-determinant inequality applied to A2^(1/2) M A2^(1/2)
now gives

    X/Y=tr(A2 M)>=2sqrt(B det M)
                    >=4sqrt(BV)/(T+2sqrt(V)).

Since S>=A2>0, V>=B. The function x/(T+2x) is increasing for x>0,
so

    X/Y>=4B/(T+2sqrt(B))=4B/(A+C/3+2sqrt(B)).

Finally

    A+C/3+2sqrt(B) <= A+C+sqrt(C^2+2AC+4B),

so X/Y>=4h_cert.

## 5. Conclusion and stationary-source receiver

Combining Sections 3 and 4,

    h_star>delta X/Y>=4delta h_cert>h_cert.

Section 1 gives Q0(h_star)<0. The mixed invariant Hessian direction
(delta p,delta s)=(-3,1) has integrated curvature

    Q=Q0-2 integral_0^infinity (k-1)^2/[D(t)^2 V_active(t)^2]dt
      <=Q0<0,

where V_active=p+(k+2)(s+k+2)>0 and k=h/t. Therefore at any genuine
noncommuting stationary source where the invariant directions are
locally available, the Hessian cannot be positive semidefinite. This
excludes a stationary minimum of that clean-spectator core, subject to
the established source-to-invariant local-coordinate interface.

## Audit notes / elementary form of the matrix inequality

The integral Minkowski step can be verified without invoking an external
theorem. For positive 2x2 matrices P,Q,

    tr(P adj Q)>=2sqrt(det P det Q).

This is the arithmetic-geometric mean inequality for the eigenvalues of
Q^(-1/2) P Q^(-1/2), multiplied by det Q. For an integrable positive
matrix-valued function P(u), polarization of the 2x2 determinant gives

    det(integral P)=1/2 integral integral tr(P(u) adj P(v))du dv
                  >=(integral sqrt(det P(u))du)^2.

Apply this with P(u)=V adj(S+uI)/det(S+uI)^2. Positivity and integrability
justify the passage from finite sums, or Tonelli entrywise after using
the nonnegative mixed-discriminant expression.

The zero h_star exists without any numerical premise. The original
Ip t-integrand is strictly decreasing in h. Its positivity for
h<=delta lambda_min(A2) follows already from Section 3, and for
h>=lambda_max(A2), the strict elementary upper bound K(c,d)<1/c gives
Ip<0 because c=beta+h+2alpha>=beta+3alpha. Continuity and strict
monotonicity then establish the unique positive zero.

Exact symbolic check: `clean_core_conditional_curvature_operator_check.py`
passes transport expansion, scalar log-inequality derivative, delta
identities, reciprocal tangent identity, determinant integral, and
threshold quadratic. No floating quadrature is used in that checker.
