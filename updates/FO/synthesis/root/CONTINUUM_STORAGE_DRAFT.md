# Continuous opposite-carrier calibration — root derivation

Draft 1, 15 October 2026. Independently derived before seeing the continuum
worker's conclusions. This draft is preserved if a stronger version follows.

Let G(A)=3(u+v-2j)^2+(35/24)u^2+j^2-(5/2)ju,
u=|A_1|^2,v=|A_2|^2,j=det A. For arbitrary real periodic W^{1,4}
amplitudes r,s set phi(x,y)=r(x)e^{iy}+s(x)e^{-iy}, with complex notation
for R^2. Then, for every constant B,

    E[G(B+Dphi)-G(B)] >= (1/2) E|Dphi|^4.

There is no winding-moment cancellation, grid, bound on real amplitudes,
restriction on positive strip widths, or sign condition on individual strips.
It covers continuously varying amplitudes as well as all polygonal paths.
It is NOT a proof for arbitrary profiles or for the full quartic cone.

Write p=r',q=s', L=Ey G(Dphi), N=Ey |Dphi|^4. Direct Fourier averaging gives

    U=p^4+q^4+4p^2q^2, V=r^4+s^4+4r^2s^2,
    W=(p^2+q^2)(r^2+s^2)-2rs pq,
    Z=(rq+sp)^2/2,
    T=rp^3-sq^3-2sp^2q+2rpq^2,
    R=r^3p-s^3q-2r^2sq+2s^2rp,
    L=(107/24)U+3V+19W-13Z-(29/2)T-12R,
    N=U+V+2W.

The storage potential is

    P(r,s)=-(16/3)r^4+(25/4)s^4-(11/6)r^2s^2.

Exactly, L-DP(r,s)[p,q]-N/2=z6^T Q6 z6+z4^T Q4 z4,
where z6=(r^2,p^2,s^2,q^2,rp,sq), z4=(rs,rq,ps,pq), and the rational
matrices and their strictly positive leading principal minors appear in
discovery/EXACT_STORAGE_CERTIFICATE.json. This is a polynomial identity;
the matrices were discovered numerically but exact rational arithmetic,
not the solver, establishes positive definiteness. Integrate DP along a
closed path to get the zero-background assertion. The Sobolev chain rule
applies because r,s are bounded in one dimension.

To include all B, X=Dphi obeys X(x,y+pi)=-X(x,y), so the odd terms in the
quartic expansion vanish. Thus the gap equals E G(X)+(1/2) E D^2G(X)[B,B].
Quartic polarization gives E D^2G(X)[B,B]=E D^2G(B)[X,X]. Each x-Fourier
coefficient of a gradient is rank one in its real Fourier components, so
Parseval and rank-one convexity of G make this quadratic average nonnegative.
Alternatively use the exact inherited acoustic Gram certificate for G
(FI original Section 5.1), which must be independently reconstructed in
the final checker. B=0 attains the infimum. No inverse-Hessian or bounded-B
assumption is used.

The same proof works for any nonzero integer transverse frequency k, with
storage k^3 P(r,s) (for k<0 exchange carriers or use signed k consistently).
For k>0 insert R=kr,S=ks in the pointwise identity and divide the total
derivative by k. No sum of distinct transverse frequencies is asserted.

This replaces the source's finite opposite-carrier graph certificate with
a continuous potential for this real-amplitude family. It removes that
particular discretization gate, while leaving the unrestricted profile-space
storage inequality, general integrand problem, novelty and external review open.
