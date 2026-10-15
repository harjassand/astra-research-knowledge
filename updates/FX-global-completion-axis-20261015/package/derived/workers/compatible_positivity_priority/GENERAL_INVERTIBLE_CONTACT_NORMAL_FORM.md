# A universal algebraic normal form for invertible acoustic contacts

Independent elementary deduction. Historical priority is unknown. This
classifies the necessary linear critical-contact space, not its ROC/QC cone.

Let F be a left-SO(2)-invariant homogeneous quartic and suppose
D2F(A0)[R0,R0]=0, with A0 invertible, R0 nonzero rank one, and F ROC.
Set M=R0 A0^(-1). A change F(A)->F(O A S), O in SO(2), S=O^(-1)A0,
normalizes A0 to I and conjugates M by O. Choose O so the image of M
is the first coordinate axis. The normalized direction is

    R = e1 tensor (tau,sigma),
    tau=tr M, sigma=M12-M21.

Trace and the signed skew entry are invariant under SO(2) conjugation.
Conversely they classify nonzero rank-one matrices under this conjugation:
the determinant-zero relation fixes the norm of the symmetric traceless
part, and rotations act transitively on that part's circle. Rescaling a
rank-one direction does not affect the contact. Thus the projective pair
[tau:sigma] is the normalized contact type.

If sigma is nonzero, set t=tau/sigma and use R=e1 tensor (t,1).
The trace-free shear stratum is t=0. If sigma=0, use the separate pure
stretch R=e11. This identifies the contact types omitted by a shear-only
normalization. Input GL changes preserve QC/ROC, but transform the chosen
distortion completion H as well; this is not an invariance assertion for
completion along the original untransformed H.

Use the invariant coefficient basis

    b=(u^2,v^2,uv,w^2,uw,vw,uj,vj,wj), F=b.f.

Target invariance makes ROC equivalent to nonnegativity of

    q(A,n,m)=D2F(A)[e1 tensor (n,m),e1 tensor (n,m)].

At a zero of this nonnegative polynomial, all first derivatives vanish.
The seven conditions q,q_a,q_b,q_c,q_d,q_n,q_m at (I,t,1) give M(t)f=0.
The verifier regenerates M(t) directly from F, without assumed acoustic
formulae. One five-minor is

    768(t^4+2t^2+3)>0

(rows q_a,q_b,q_c,q_d,q_n; columns f1,f3,f4,f5,f8). Hence the system
has rank five for every real t. Its kernel has the following polynomial
basis, with four columns and rows ordered as b:

    N(t)=
    [ -1       -(t^2+6)       3            t^2                 ]
    [ -t^4     -3t^2          2t^2-3      -3t^2                ]
    [ -2t^2    -6(t^2+2)     -6           -2(2t^2+3)           ]
    [ -4t^2     12            4t^2         2(t^4+2t^2+3)       ]
    [  4t       8t           -8t          -4t(t^2+1)           ]
    [  4t^3     0             0            0                  ]
    [  0        4(t^2+3)      0            0                  ]
    [  0        0             4(t^2+3)     0                  ]
    [  0        0             0            4t(t^2+3)           ].

Direct multiplication gives M(t)N(t)=0. Its four-minor on coefficient
rows f0,f2,f6,f7 is

    32(t^2+3)^2(t^4+2t^2+3)>0.

Therefore N(t) is a basis for every real t, including t=0. At t=0 its span
is exactly span{H,u^2,j^2,uj}, recovering the supplied shear-contact space.
The pure stretch system also has rank five, with kernel

    span{H,v^2,w^2,vj}.

All identities and ranks are regenerated in the standalone verifier.
The positivity of the displayed minors proves that these are universal
identities, not finite-parameter sampling claims.

The remaining mathematical problem for each t is intersection with the
full acoustic PSD cone and then with QC. Membership in this linear space
alone provides neither. This normal form is a tractable receiving target
for exact cone elimination or integral positivity constructions on contact
types other than shear.
