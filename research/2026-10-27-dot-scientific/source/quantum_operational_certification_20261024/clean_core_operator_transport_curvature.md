# Clean-core operator/transport curvature bounds

26 October 2026. Initial exact sufficient conditions.

**Superseded for closure:** `clean_core_conditional_curvature_operator_proof.md`
now supplies the full conditional receiver by a weighted Haar mean and
a determinant integral inequality; the lemmas below remain valid.

Let A2>0 have eigenvalues a,b, let H2>0, and put A=a+b, B=ab,
C=tr(H2), D(t)=t^2+At+B, N(t)=Ct+E. The target is
Q0(h)=integral_0^infinity [R(t,h)^(-2)-2L(t)^(-2)]dt,
R=(1+h/t)D+N, L=2D+N.

## 1. Explicit sufficient threshold for negative curvature

Define

    h_cert = B/[A+C+sqrt(C^2+2AC+4B)].

Then h>=h_cert implies Q0(h)<0, with no restriction on E or det(H2)
beyond positivity.

Proof: change t=2u in the first integral. Direct expansion gives

    R(2u,h)-L(u)
      =2u^2+(C+2h)u+hA-B+hB/(2u).

AM-GM bounds the last expression below by

    2u^2+hA-B+sqrt(2hB(C+2h)).

The increasing function hA+sqrt(2hB(C+2h)) equals B at h=h_cert
(the displayed formula also holds when A^2=4B by continuity, or directly
by rationalizing the quadratic equation). Thus R(2u,h)>L(u) for every
u>0, and

    Q0(h)=2 integral [R(2u,h)^(-2)-L(u)^(-2)]du<0.

A proposed stronger receiver, still UNPROVED, is Ip(h_cert)>0. Since Ip
strictly decreases and has a unique zero, that would prove the desired
conditional curvature result.

## 2. Exact operator bracket for the Ip-zero

Let psi be Haar-uniform on the complex unit sphere in C^2 and write
alpha=<psi,A2 psi>, beta=<psi,H2 psi>. The elementary 2x2 identity

    E_psi <psi,M psi>^(-2)=1/det(M)

and Tonelli applied separately to the two positive integrals give

    Ip(h)=E_psi [K(beta+h+2alpha,2alpha h)-1/(beta+3alpha)],
    K(c,d)=integral_0^infinity x^2/(x^2+cx+d)^2 dx.

Here c>2sqrt(d). For every c>=2sqrt(d)>0,

    1/(c+sqrt(d)) <= K(c,d) < 1/c,

with equality in the left bound only at c=2sqrt(d).
To verify the lower bound, factor x^2+cx+d=(x+r)(x+s), r>=s>0.
For r>s,

    K=(r+s)/(r-s)^2-2rs log(r/s)/(r-s)^3.

The lower bound is equivalent, for z=sqrt(r/s)>=1, to

    2log z <= (z^2-1)(z^2+4z+1)/(2z(z^2+z+1)).

The difference vanishes at z=1 and has derivative

    (z-1)^4(z+1)^2/[2z^2(z^2+z+1)^2] >=0.

At r=s, K=1/(3r), giving the equality case. The upper bound follows
strictly by dropping d from the denominator of the integrand.

Put delta=2-sqrt(3). If h<=delta*lambda_min(A2), then for every psi,

    h+sqrt(2alpha h)<=alpha,

so K>1/(beta+3alpha) and Ip(h)>0. Conversely, if
h>=lambda_max(A2), c>=beta+3alpha and K<1/(beta+3alpha), so Ip(h)<0.
Consequently its unique zero satisfies

    (2-sqrt(3))*lambda_min(A2) < h_star < lambda_max(A2).

This bound does not use commutativity of A2,H2.

## 3. A certified parameter region

Combining the two statements proves Q0(h_star)<0 whenever

    h_cert <= (2-sqrt(3))*lambda_min(A2).

This is an explicit source-dependent condition, improving as tr(H2)
increases. In particular it holds for every H2>0 whenever

    kappa(A2) <= [sqrt(delta)/(1-sqrt(delta))]^2, delta=2-sqrt(3),

approximately 1.1516126864 (use the exact expression as the criterion).
This limited region does not settle the full anisotropic core.

Writing a=max(a,b), b=min(a,b), the source-dependent condition above
is equivalently

    tr(H2) >= a-(3-sqrt(3))*b+(2-sqrt(3))*b^2/(2a).

In particular tr(H2)>=lambda_max(A2) always suffices. The equivalence
uses (1-delta)^2=2delta and the positive quantity B-delta*b*A.
