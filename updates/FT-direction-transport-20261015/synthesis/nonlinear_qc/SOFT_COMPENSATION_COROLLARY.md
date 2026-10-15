# The full compatible G cubic-quartic inequality

Date: 15 October 2026. Internal proof consequence; external review and priority
UNKNOWN. Premise: the exact all-background G quasiconvexity proof in
`G_QUASICONVEXITY_PROOF.md`, using the rational closed heat certificate.

Let v be any real smooth periodic scalar function on the planar torus. Write

    p=v_xx,    q=v_xy,    r=v_yy,
    P=<p^2>,    T=<q(9p^2+4q^2)>.

Let K be the complete quartic

    1944 K(p,q,r)
      =8667p^4+18792p^3r+576p^2q^2+16416p^2r^2
        +1440pq^2r+6912pr^3+56q^4+576q^2r^2+1152r^4,
    D=<K(p,q,r)>.

Theorem. For every such v,

    D>=0,
    T^2 <= (8748/5) P D.                                (1)

Consequently, for every real s,

    (5s^2/12) P -(5s^3/162) T+s^4 D >=0.                (2)

All resonances and the complete v_yy dependence are retained. No Fourier
support restriction, smallness condition or assumption that K is pointwise
nonnegative is present.

Proof. Take the actual compatible perturbation

    phi_s=((2s/3)v_y,s v_x),
    I+Dphi_s=[[1+(2s/3)q,(2s/3)r],[sp,1+sq]].

The exact expansion retained in FS is

    G(I+Dphi_s)-G(I)
      =-(5s/18)q+(s^2/12)(5p^2+4pr-4q^2)
         -(5s^3/162)q(9p^2+4q^2)+s^4K.

Periodicity gives `<q>=0` and `<pr>=<q^2>`. The all-background quasiconvexity
theorem at I therefore gives (2) for every real s. Dividing by s^2 when s is
nonzero yields the globally nonnegative scalar quadratic

    5P/12 -(5T/162)s+D s^2 >=0.

Its leading coefficient D is nonnegative. Its discriminant is nonpositive:

    (5T/162)^2 <= (5/3)P D.

This is exactly (1), because `(5/3)*(162/5)^2=8748/5`. If D=0, the same
quadratic forces T=0. If P=0, it likewise forces T=0; no division by a zero
quantity is used. Conversely these conditions imply (2). QED.

The theorem extends to periodic v in W^(2,4) by strong smooth approximation.
Every term converges by Holder's inequality. It also applies to compactly
supported smooth potentials in R2, or clamped W0^(2,4) potentials on a bounded
domain, using the zero-boundary vector perturbation obtained from their first
derivatives.

The earlier anisotropic obstruction remains correct: estimates replacing D
by quartic expressions in p,q alone fail. This proof does not make that failed
bound true; it uses the complete compatible quartic D, whose nonnegativity is
now secured by an independent full nonlinear operation. In particular,
`K(1,0,-3/2)=-1/24` remains a negative unconstrained pointwise jet value, while
the integral D over every periodic Hessian is nonnegative.

The route is constructive at the certificate level: a single exact closed
heat identity proves the actual compatible action globally. The inequality
is not assumed as a definition of a reduced value or inferred from numerical
returns to an affine map.
