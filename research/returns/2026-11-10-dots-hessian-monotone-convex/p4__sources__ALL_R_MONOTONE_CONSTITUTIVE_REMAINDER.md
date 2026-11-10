# All-r monotonicity of the actual constitutive remainder

10 November 2026. A strict finite-amplitude sign for the SAME original pressure/determinant ledger. The sign was first obtained by a direct k=1 Schur completion; the general identity follows from the endpoint-exact second selector channel. This does not establish quasiconvexity, because the physical second-row variation remains coupled.

## 1. Actual constitutive map

Use k>1/3, ell=3k-1, n=k+1, m=3k+1 and C clockwise. For F with first row h and second row s, write

    J_k(F)=j(F)^2+ell R_k(F),
    R_k=H^2/(8n)+uv/4,
    H=ku-v+2j,
    lambda=qS/2=2j+ell L_k,
    L_k=[(3/2)(ku-v)+2j]/m,
    T_k(F)=D_row1 R_k(F)-L_k(F) C s.

Then the ORIGINAL row stress has the exact decomposition

    D_row1 J_k(F)=lambda(F) C s+ell T_k(F).             (1)

T_k is not assumed to be a gradient in h, and R_k is not separately row-convex. The claim below concerns monotonicity of this particular actual remainder map.

## 2. Exact all-r same-row identity

Let F0,F1 have the same second row, e=h1-h0, E=[e;0], Fm=(F0+F1)/2. Set

    delta lambda=lambda(F1)-lambda(F0),
    delta j=j(F1)-j(F0),
    beta=3n/m.

In the GENERAL four-channel convention, C2=3/(4nm), and midpoint polarization gives

    delta lambda+beta delta j=(3/m)L2(E,Fm).          (2)

Because J is quartic and det E=0, its symmetric row Bregman is exactly

    B_J(F1;F0)+B_J(F0;F1)
      =P(E)[Fm,Fm]+J_k(E)
      =(delta lambda+beta delta j)^2/(4beta)
         +sum_(i != 2) C_i L_i(E,Fm)^2+J_k(E).        (3)

On the other hand, (1) implies that the left side of (3) equals

    delta lambda delta j+ell (T_k(F1)-T_k(F0)) dot e.

Completing just this SAME signed determinant/selector cross yields

    ell (T_k(F1)-T_k(F0)) dot e
      =(delta lambda-beta delta j)^2/(4beta)
        +sum_(i != 2) C_i L_i(E,Fm)^2+J_k(E)
      >=J_k(E).                                      (4)

Every quantity in (4) belongs to the original finite secant action. It is not a second determinant budget. The exact quartic floor is

    J_k(E)=ell [k^2 e1^4+2 e1^2 e2^2+e2^4]/(8n).

Consequently T_k is globally strictly monotone in its first row for every fixed second row, with the parameter-explicit endpoint-uniform modulus

    (T_k(F1)-T_k(F0)) dot e
      >=[k^2 e1^4+2 e1^2 e2^2+e2^4]/(8n).            (5)

The case e=0 is immediate; for e!=0 the right side is strictly positive. No inverse Hessian, frequency restriction, or parameter fit appears.

The differential form follows either by a difference quotient or directly from (2): for E=[e;0],

    ell e^T sym(D_h T_k(F)) e
      =[Dlambda(F):E-beta Dj(F):E]^2/(4beta)
        +sum_(i != 2) C_i L_i(E,F)^2 >=0.              (6)

The finite identity is stronger at a degenerate contact because it retains the original quartic floor in (4).

## 3. Intrinsic k=1 discovery

At k=1, put F=[[a,b],[c,d]], u=a^2+c^2, v=b^2+d^2 and j=ad-bc. The actual remainder is

    T1=a(u+v+2j)/4+d(v-u)/8,
    T2=b(u+v-2j)/4-c(v-u)/8.

Its symmetric first-row derivative satisfies

    4 sym D_hT=
      [[3a^2+b^2+c^2+d^2+3ad-2bc,
         2ab-(ac+bd)/2],
       [2ab-(ac+bd)/2,
         a^2+3b^2+c^2+d^2-2ad+3bc]].

For a row direction (r,s), let R=r^2+s^2>0. In the quadratic form 4(r,s) sym D_hT (r,s)^T, elimination of (c,d) uses the positive block R I. The exact remaining (a,b) matrix is

    [[3r^2(r^2+9s^2)/(4R), 9rs/4],
     [9rs/4, 3s^2(9r^2+s^2)/(4R)]].

Both diagonal entries are nonnegative and its determinant is

    36 r^4 s^4/R^2>=0.

This gave the first monotonicity sign without a computation. Identity (4) then supplies the simpler all-r proof and the exact finite quartic remainder.

## 4. What is and is not paid in the full construction

For every finite original fixed-second-row orbit trial, (4) can be inserted into the symmetric original Bregman/affine-drift ledger. In particular

    B_J(F1;F0)+B_J(F0;F1)-delta lambda delta j>=J_k(E).

The signed cross is retained, not bounded in absolute value. This is a genuine nonlinear pressure/determinant payment on a same-second-row comparison.

For a physical path, however, s'=g is nonzero. Its actual constitutive derivative is

    T_k'=D_hT_k h+D_sT_k g.

Only the first term has the sign (6). Likewise a finite physical secant has a coupled second-row change; applying (4) to the entire difference would be invalid. The mixed D_sT_k term, the actual affine drift, and the original selector/stream action must remain in one ledger. No assertion that T_k' dot h is nonnegative, and no full J_r quasiconvexity conclusion, is made.

No scientific execution or dedicated intermediate audit was used. The construction is the displayed exact selector polarization, symmetric quartic secant identity, and signed square completion.

## 5. Stronger full-matrix monotone map, with its curvature retained

The same sign extends beyond a single row. Define the full four-component map

    T_full(F)=DR_k(F)-L_k(F) cof F,
    DJ_k(F)=lambda(F) cof F+ell T_full(F).

This map is NOT asserted to be a gradient. For every matrix direction E, the exact selector identity and the derivative of the cofactor give

    ell DT_full(F)[E]:E
      =P(E)[F,F]-(Dlambda(F):E)(Dj(F):E)
      =[Dlambda(F):E-beta Dj(F):E]^2/(4beta)
        +sum_(i != 2) C_i L_i(E,F)^2 >=0.              (7)

Here D(cof F)[E]:E=2 det E is essential: its contribution cancels the selector translation 2lambda det E exactly. There is no restriction det E=0 in (7).

For arbitrary F0,F1, set E=F1-F0 and Fm their midpoint. Exact cubic secant quadrature yields the finite identity

    ell [T_full(F1)-T_full(F0)]:E
      =(delta lambda-beta delta j)^2/(4beta)
        +sum_(i != 2) C_i L_i(E,Fm)^2+Psi_k(E),        (8)

where the final homogeneous quartic is

    Psi_k(E)=J_k(E)-lambda(E)det(E)/2
      =ell/(8n)[H(E)-beta det(E)]^2
        +ell w(E)^2/4
        +3ell n(2m-3)det(E)^2/(8m^2).                (9)

Since 2m-3=6k-1>0, Psi_k is positive away from zero. Thus T_full is globally strictly monotone, with an explicit original quartic modulus. Formula (4) is the det E=0 restriction, when Psi_k(E)=J_k(E).

This stronger map does not remove the compatibility problem. Its nonconservative differential is exactly the feature curvature -dL_k wedge dj (equivalently the retained lambda/j area after the endpoint term is separated). A positive symmetrized derivative does not authorize calling T_full a convex gradient. In a physical path, testing only the first-row equilibrium does not spend the positive full-matrix form without retaining the second-row work. The signed weighted determinant/feature area remains the full-theorem obstruction.
