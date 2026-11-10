# Convex radial potential and the remaining signed minor

10 November 2026. This is a companion to the FIXED source ALL_R_MONOTONE_CONSTITUTIVE_REMAINDER.md, SHA a80b7285b04294eefaadf7ef58d2bba2e69456f2a0a6cdbc232f71fbe111a449. It supplies a convex decomposition of the ORIGINAL density, not an extra reserve and not a quasiconvexity proof.

Use ell=3k-1>0, n=k+1, m=3k+1; u=|F_col1|^2, v=|F_col2|^2, j=det F, w=F_col1 dot F_col2, H=ku-v+2j. Let lambda=qS/2 and

    Psi_k(F)=J_k(F)-lambda(F)j(F)/2,
    K_k=Psi_k/ell.

## 1. Exact global convexity from the actual monotone map

Let

    Q(F,E)=ell DT_full(F)[E]:E>=0.

The two-variable polarization identity is

    Q(E,F)-Q(F,E)
      =2[lambda(F)j(E)-lambda(E)j(F)].                 (1)

Direct differentiation of the displayed quartic Psi gives

    D^2Psi(F)[E,E]
      =Q(F,E)+lambda(F)j(E)-lambda(E)j(F)
      =[Q(F,E)+Q(E,F)]/2>=0.                          (2)

Thus Psi is globally convex. Moreover

    |lambda(F)j(E)-lambda(E)j(F)|
      <=D^2Psi(F)[E,E].                               (3)

The quantity in (3) is the RADIAL two-state feature area. It is not the general two-direction differential sector form d lambda wedge dj. In particular (3) does not replace the actual pressure/current or justify an unrelated constant-sector bound.

## 2. A direct strict Hessian bound in actual feature coordinates

There is an exact alternative form

    K_k=[3(ku+v)^2+(ell/n)H^2+4w^2]/(16m).             (4)

Scale the first column of F by sqrt(k). In those Euclidean coordinates set

    N=ku+v,
    q=ku-v, r=2sqrt(k)j, z=2sqrt(k)w.

The actual Hopf identity is

    q^2+r^2+z^2=N^2.

Rotate q,r by the orthogonal matrix whose first row is (sqrt(k),1)/sqrt(n). Then

    Q_plus=(sqrt(k)q+r)/sqrt(n)=sqrt(k/n)H,
    Q_minus=(q-sqrt(k)r)/sqrt(n),
    Q_plus^2+Q_minus^2+z^2=N^2,
    K_k=[3k N^2+ell Q_plus^2+z^2]/(16km).             (5)

For completeness, a quadratic feature Q_i in this Hopf triple is F^T A_i F with A_i symmetric; the triple obeys the displayed norm identity for F and for any increment E. If c_i>=0, then

    D^2(sum_i c_i Q_i^2)[E,E]
      =8 sum_i c_i(F^T A_i E)^2
        +4 sum_i c_i Q_i(F)Q_i(E)
      >=-4(max_i c_i) N |E|_k^2,

where |E|_k^2=k|E_col1|^2+|E_col2|^2. The radial term N^2 has Hessian at least 4N|E|_k^2. Applying this to (5), with coefficients ell,0,1, yields

    D^2K_k(F)[E,E]
      >=[min(ell,1)/(4km)](ku+v)|E|_k^2.             (6)

Indeed 3k-max(ell,1)=min(ell,1)>0. Multiplying by ell gives a strict explicit Hessian bound for Psi at every F!=0. This proof uses the actual feature identity, not independent feature variables or a free covariance relaxation.

One consequence, if a coarse finite modulus is useful, is

    B_Psi(F+E;F)
      >=[ell min(ell,1)/(144km)]|E|_k^4.

The factor 1/36 comes from minimizing integral_0^1(1-t)|F+tE|_k^2 over F. This lower bound is part of the SAME convex Psi term, not an additive resource.

## 3. Exact remaining current

The original density is

    J_k=Psi_k+lambda j/2.                             (7)

The multiplier lambda is quadratic in F; lambda j is not a null Lagrangian. Even on compatible periodic fields, one cannot replace it by lambda(A)<j> or discard its fluctuations.

The actual monotone map also has the radial decomposition

    T_full=DK_k+[j DL_k-L_k Dj]/2.

The second term is orthogonal to the radial vector F but carries the nonconservative feature curvature. Thus (7) isolates the original convex resource and the signed weighted minor without pretending that T_full itself is a gradient.

For an actual compatible mean-A field, convexity pays <Psi(A+Dphi)>-Psi(A). The remaining signed quantity

    (1/2)<lambda(A+Dphi)det(A+Dphi)-lambda(A)det A>

still has to be coupled to that SAME convex Bregman and the actual pressure/affine boundary current. A proof of its unconditional positivity is neither asserted nor needed as a separate target. The original contact degeneracies already preclude discarding its cancellation against the convex part.
