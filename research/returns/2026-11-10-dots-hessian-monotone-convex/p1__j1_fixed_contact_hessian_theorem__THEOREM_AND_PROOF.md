# An arbitrary-Hessian contact theorem for J_1

9 November 2026. A restricted theorem with a separate independent mathematical review. It is not a proof of full quasiconvexity.

## 1. Exact statement and normalization

All integrals below are normalized averages over a rectangular two-dimensional torus. Let psi be real and periodic in W^{2,4}. Set

    U=psi_xx, V=psi_xy, W=psi_yy,
    X=diag(2,-4) D^2 psi = [[2U,2V],[-4V,-4W]],
    A_1=[[0,1],[1,0]].

For F=[[a,b],[c,d]], put u=a^2+c^2, v=b^2+d^2, j=ad-bc. The original density at r=k=1 is

    J_1(F)=j^2+(u-v+2j)^2/8+uv/2.

Then, for every real t,

    <J_1(A_1+tX)> >= J_1(A_1).

The inequality is strict when t is nonzero and D^2 psi is nonzero. There are no Fourier support, parity, separability, sign-of-Jacobian or amplitude restrictions. The affine mean is specifically A_1. This does not assert the result at arbitrary affine means or at r other than 1. By periodizing a compactly supported scalar potential inside a larger rectangle, the same statement holds for smooth compactly supported Hessian-potential perturbations of A_1, with unnormalized integrals of the Jensen difference. Approximation extends it to the corresponding W^{2,4} closures.

## 2. A global heat operator with its paid norm

Initially take psi smooth. Let P_s=exp(s partial_y^2), acting only in y, and use subscripts s for P_s. Define

    R(U,V)=-6 integral_0^infinity partial_y P_s[V_s partial_y U_s] ds.

The integral can first be truncated. For every lambda>0 it has an L2 limit and satisfies

    ||R(U,V)||_2^2 <= (9/2) <(lambda U^2+lambda^{-1}V^2)^2>.       (H1)

Here and throughout, norms use the normalized torus measure. To prove (H1), dualize against g in L2. Self-adjointness and integration by parts give

    <g,R>=6 integral <(partial_y P_s g) V_s partial_y U_s> ds.

The heat energy identity gives integral ||partial_y P_s g||_2^2 ds <= ||g||_2^2/2. With z_s=(sqrt(lambda)U_s,lambda^{-1/2}V_s),

    d/ds <|z_s|^4>
      =-4<|z_s|^2 |partial_y z_s|^2>
       -8<(z_s dot partial_y z_s)^2>.

The first integrand contains V_s^2 (partial_y U_s)^2 with coefficient one. Consequently

    integral <V_s^2 (partial_y U_s)^2> ds
      <= <(lambda U^2+lambda^{-1}V^2)^2>/4.

Cauchy--Schwarz in space and heat time now proves (H1). The same bound for any tail interval, with its first factor tending to zero, proves that the truncated R operators are Cauchy in L2 for smooth data. Bilinearity and the optimized lambda bound give continuity L4 times L4 to L2, so R extends uniquely to all L4 inputs. The nonzero limiting y-average of U is harmless: only its y derivative occurs, and the nonnegative terminal fourth moment was merely discarded.

## 3. Exact Hessian compatibility identity

Hessian compatibility yields U_y=V_x and W_x=V_y, also after heat flow. The y-average of V vanishes at every x. Hence

    <V^3> = 6 integral_0^infinity <V_s (partial_y V_s)^2> ds.

On the other hand,

    <W,R> = 6 integral <(partial_y W_s) V_s (partial_y U_s)> ds.

At each s, periodic integration by parts gives

    <W_y V V_x> = -(1/2)<W_xy V^2>
                 = -(1/2)<V_yy V^2>
                 = <V (V_y)^2>.

Therefore

    <V^3>=<W R(U,V)>.                                      (H2)

This identity includes all interacting frequencies. It is not a sum of independent mode estimates. Smooth approximation and (H1) extend (H2) to psi in W^{2,4}.

## 4. The one-channel sharp budget

Set F=R(U,V)+4VW. Take lambda=2/5 in (H1), then use

    ||R+4VW||_2^2 <= (3/2)||R||_2^2+48||VW||_2^2.

It follows that

    ||F||_2^2 <= <E(U,V,W)>,
    E=(27/25)U^4+(675/16)V^4+(27/2)U^2V^2+48V^2W^2.          (H3)

Expansion of the ORIGINAL J_1, without discarding determinant cross terms, gives

    J_1(X)=2U^4+194V^4+32W^4+36U^2V^2+16V^2W^2
           +112U^2W^2-16U^3W+64UW^3-240UWV^2.

We prove pointwise J_1(X)>=E. Write T=V^2, and define

    a=2429/16,
    b=(45/2)U^2-240UW-32W^2,
    c=(23/25)U^4-16U^3W+112U^2W^2+64UW^3+32W^4.

Then J_1(X)-E=aT^2+bT+c, and exactly

    4ac-b^2=(2621/50)U^4+1084U^3W+11852U^2W^2
             +23504UW^3+18408W^4.

This last quartic has the Gram matrix on (U^2,UW,W^2)

    G=[[2621/50,542,300],
       [542,11252,11752],
       [300,11752,18408]].

It is positive definite by the following entirely rational bounds. The first diagonal entry a0 is between 52 and 53. Its Schur complement satisfies

    S11=11252-542^2/a0 > 5600,
    S22=18408-300^2/a0 > 16600,
    0 < S12=11752-162600/a0 < 8700.

Thus det S>5600*16600-8700^2=17270000>0. Consequently

    J_1(X)-E
      = a[T+b/(2a)]^2 + (4ac-b^2)/(4a) >= 0.                 (H4)

It is strictly positive away from (U,V,W)=0: if (U,W) is nonzero the Gram term is positive, and if U=W=0 it equals a V^4. Combining (H3)--(H4),

    ||R(U,V)+4VW||_2^2 <= <J_1(X)>.                         (H5)

All constants are explicit. The inequality is not inferred from a numerical optimizer or a scalar real-input Beurling norm conjecture.

## 5. Original contact gap and exact conclusion

For a general mean-zero compatible X=[[a,b],[c,d]], the original k=1 contact expansion is

    <J_1(A_1+tX)>-J_1(A_1)
     = t^2 <(2b+c)^2+d^2>
       +t^3 <(b+c)(b^2+d^2)-(4b+2c)det X>
       +t^4 <J_1(X)>.

The first-order term has zero average. On our Hessian class 2b+c=0, d=-4W, b+c=-2V. Thus

    q=16<W^2>,
    C=-8<V^3+4VW^2>=-8<W F>.

In particular, the factors are 16 and -8, not 4 and -4. Using (H2), the complete original gap is exactly

    t^2 ||4W-tF||_2^2
       +t^4[<J_1(X)>-||F||_2^2] >= 0.                      (H6)

By (H3)--(H4) the final bracket is at least the average of the strictly positive quartic remainder J_1(X)-E. This also proves strictness for nonzero Hessians and nonzero t. Density of smooth periodic potentials in W^{2,4}, continuity of J in the L4 gradient norm and (H1) complete the function-space extension.

## 6. Prior and limits

The contact expansion can be checked directly from the displayed original density. In the particular Hessian class its pointwise identity at amplitude one is

    J_1(A_1+X)-J_1(A_1)
      = -2V+24(UW-V^2)+16W^2-8V^3-32VW^2+J_1(X).

Both <V> and <UW-V^2> vanish for a periodic scalar Hessian. The included exact-arithmetic checker verifies this identity, the original quartic expansion, the reserve identity and the positive Gram minors. The heat argument and Sobolev passage are analytic, not established by a finite check.

Strong related primary prior includes Guerra, arXiv:2608.23388v1, https://arxiv.org/html/2608.23388v1, which proves Hessian-restricted quasiconvexity for Burkholder and separating functions. No derivation of the present transformed J_1 statement from that theorem is supplied here. The density is different and the transformation diag(2,-4) is indefinite. A real-input Beurling estimate cannot be imported without checking its exact hypotheses and convention.

The heat-energy argument uses standard semigroup ideas. The density-specific step is their simultaneous payment by the full quartic reserve. The separate review gives an alternative exact payment. This packet makes no historical novelty claim and does not constitute an exhaustive literature review.

Open extensions include arbitrary affine means, all r>0, and unrestricted vector gradients. A compactly supported scalar Hessian potential is not an arbitrary zero-boundary vector perturbation. No negative Jensen field or full quasiconvexity theorem is asserted.
