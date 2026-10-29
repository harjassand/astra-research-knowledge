# A free Fisher unit ball gives a finite affine design operation

30 October 2026. Governing developing proof. The inherited conditional-Umegaki/free-Fisher theorem is an accepted programme input; the linear-pencil reduction below is proved here. Execution, prior and final cost receipts are separate. No physical calibration, privacy, guessing or multi-use claim is made.

## 1. Scope and reusable input

Let L be a strictly entrywise positive, column-stochastic ell-by-n classical channel, n>=2. Its shape and rank are arbitrary. Let K be an m-by-n column-stochastic channel, with an imposed rational entry floor 0<kappa<1/m. The floor is useful for design and uniform inverse denominators; it can be arbitrarily small. The budget c is nonnegative. Both channels share the SAME explicitly classical input boundary.

For classical-quantum hypotheses and any finite complex reference R, write

    J_A(rho,sigma) = D((A tensor id)rho || (A tensor id)sigma)
                    - D(rho_R || sigma_R).

Only finite differences are defined. This is a SUBTRACTED/conditional comparison, equivalently the equal-reference-marginal comparison. It is NOT the uncentered all-reference inequality D_K<=c D_L: identical reference information forces c>=1 in that different task. The accepted input theorem in sol24/c_independent_opening/source_entry/FREE_UMEGAKI_PROOF.md says J_K<=c J_L for all finite references iff

    F_K(Q,u) <= c F_L(Q,u),                                  (1)
    F_A(Q,u) = sum_y (A u)_y^* (A Q)_y^{-1} (A u)_y,
    Q_i>=0, sum_i Q_i=I, sum_i u_i=0.

Here u_i are complex vectors and (AQ)_y=sum_i A_yi Q_i. Positivity of every channel entry makes all inverse denominators positive, including boundary effects Q_i=0. The faithful-Q and closed-Q versions agree by mixing each Q_i with I/n and continuity. This proof starts from (1), rather than reopening that inherited theorem.

The output of the construction is ONE finite SDP, affine jointly in unknown K and c, whose feasibility is EXACTLY (1). For a fixed positive budget and floor, linear utility design has a rational strictly feasible certificate, a bounded feasible set, and polynomial weak-optimization complexity with the usual explicit bit/accuracy inputs. Exact threshold decision at a boundary and practical solver speed are separate claims.

## 2. Operatorization and the unit-ball equivalence

Replace vectors u_i by arbitrary operators U_i on the reference space, still with sum_i U_i=0. Define the operator-valued quadratic form

    F_A(Q,U) = sum_y (A U)_y^* (A Q)_y^{-1} (A U)_y.

The vector inequality (1) implies this operator inequality: test any vector xi and put u_i=U_i xi. Conversely every vector tuple is represented by rank-one U_i=u_i e^* for a unit e, so the two universal assertions are equivalent. U_i need NOT be Hermitian.

Consider the Hermitian pencils

    A_L(Q,U) = diag(Q_1,...,Q_n)
                 direct_sum [ diag((LQ)_1,...,(LQ)_ell)   LU ],
                            [             (LU)^*          I  ]

    B_K,c(Q,U) = [ diag((KQ)_1,...,(KQ)_m)   KU ].          (2)
                [            (KU)^*          c I ]

The LU and KU blocks are block columns. Their scalar coefficient sizes are e=n+ell+1 and f=m+1. Source positivity means precisely Q_i>=0 and F_L(Q,U)<=I; target positivity means F_K(Q,U)<=c I. Therefore (1) implies free pencil inclusion A_L>=0 => B_K,c>=0.

For the converse fix any Q,U and eps>0 and set T=(F_L(Q,U)+eps I)^(-1/2), U'_i=U_i T. Then sum U'_i=0 and

    F_L(Q,U')=T^* F_L(Q,U) T <= I.

Inclusion yields T^* F_K(Q,U) T<=c I. Congruence by T^{-1} gives F_K(Q,U)<=c(F_L(Q,U)+eps I). Let eps decrease to zero. This is valid even if F_L is singular or zero. In particular it introduces no inverse of L, no fixed-rank quotient and no nonexistent inverse on a null tangent.

## 3. Fixed coefficient matrices

Use 3(n-1) independent selfadjoint free variables X_j,Y_j,Z_j, j<n:

    Q_j=I/n+X_j,        Q_n=I/n-sum_{j<n}X_j,
    U_j=Y_j+i Z_j,      U_n=-sum_{j<n}(Y_j+i Z_j).

Then A=A0+sum_j A_j x_j and B=B0+sum_j B_j x_j are Hermitian affine pencils. All A coefficients are FIXED by L. All B coefficients are AFFINE in K and c. Specifically A0 is diagonal with n entries 1/n, then the ell row means s_z=(sum_i L_zi)/n, then 1. Hence

    A0>0,   Tr A0=3,   Tr A_j=0 for every nonconstant j.     (3)

The X_j diagonal coefficients are +1 on Q_j, -1 on Q_n and L_zj-L_zn on reference row z. The Y_j coefficient has L_zj-L_zn in the (z,last) and (last,z) source-block positions. The Z_j coefficient has i(L_zj-L_zn) above and -i(L_zj-L_zn) below. Target coefficients have the same last two patterns with K, and the X_j diagonals K_yj-K_yn. B0=diag(rowmeans(K),c).

Rank deficiency leaves some U directions unbounded in the source domain. No boundedness premise will be imposed to hide them. If h is in ker L, column stochasticity implies sum h_i=0. Substituting U_i=h_i T into (1) forces K h=0 for any finite c. The SDP below therefore enforces the necessary K ker L=0 gate automatically.

## 4. Exact linear free Farkas lemma, including unbounded domains

The following is ordinary free-linear Positivstellensatz machinery, with a short proof to pay the complex and unbounded-domain conventions. Let A(x)=A0+sum_{j=1}^g A_j x_j have Hermitian e-by-e coefficients and A0>0. Let B(x) have Hermitian f-by-f coefficients. Then positivity of B on every finite complex matrix level of {A>=0} is equivalent to

    B0=R+Phi(A0),  B_j=Phi(A_j),  R>=0, Phi completely positive.  (4)

Write the Choi matrix C=[C_ab]_{a,b=1}^e, C_ab=Phi(E_ab), C>=0. Then Phi(A)=sum_ab A_ab C_ab. Sufficiency is immediate by the Kraus representation and R>=0.

For necessity consider the cone of coefficient tuples given by (4). It is CLOSED: for any convergent tuple B^(r), positivity of A0 and the constant identity imply

    lambda_min(A0) Tr C^(r) + Tr R^(r) <= Tr B0^(r).

Thus C^(r),R^(r) are bounded PSD matrices and have convergent subsequences. If B is not in the cone, a real separating functional has Hermitian matrices Y_0,...,Y_g such that

    sum_j Tr(Y_j B_j)<0,
    Y0>=0,   W=sum_{j=0}^g A_j^T tensor Y_j>=0.             (5)

The transpose is important: it follows by expanding Tr(W C). Choose sufficiently small eps>0 so the first inequality remains negative after Y0 is replaced by Y0+eps I. Then W+eps A0^T tensor I is PSD. Put S=[(Y0+eps I)^T]^(1/2) and X_j=S^{-1}Y_j^T S^{-1}. Full transpose of W followed by congruence gives A(X)>=0 at matrix size f. With Omega=sum_{a=1}^f e_a tensor e_a and v=(I_f tensor S)Omega,

    v^* B(X) v = Tr[(Y0+eps I)B0]+sum_{j>=1}Tr(Y_j B_j)<0.

This contradicts inclusion. There is no compactness assumption on the SOURCE spectrahedron. The only compactness used is the bounded Choi/R certificate sequence furnished by A0>0. The proof also yields a violating matrix tuple of size at most f if inclusion fails.

Helton-Klep-McCullough (2012), Theorem1.1 and Section4.1, are controlling primary antecedents for this d=0 positivity/CP machinery. Their non-strict convex Positivstellensatz explicitly does not require boundedness. The proof above supplies the exact complex coefficient/transposition convention used here; it is not a new generic free Farkas theorem.

## 5. The general synthesis SDP

Combine Sections1-4. The exact feasible set is the projection of

    C>=0 of order (n+ell+1)(m+1),
    R>=0 of order m+1,
    Phi_C(A0)+R=B0(K,c),
    Phi_C(A_j)=B_j(K) for 1<=j<=3(n-1),
    sum_y K_yi=1,   K_yi>=kappa,   c>=0.                   (6)

Every equality is AFFINE JOINTLY in K,c,C,R. Thus the square inverse is removed for all positive rectangular/rank-deficient references; this is not a hierarchy or a finite-witness optimization with an unbounded hidden cutoff. The Choi variable certifies a map between pencil coefficient algebras. It is NOT a postprocessing channel from L outputs to K outputs, and (6) does not claim a physical degrader.

Although A_Z and B_Z are imaginary Hermitian, an exact REAL symmetric Choi/R realization suffices. Strip the common i from every Z equation, leaving real skew matrices. All equations now have real coefficients. If a complex Hermitian solution exists, its entrywise conjugate also solves these stripped equations; average them. The result is real symmetric and PSD, and reinstating i recovers every complex equation. Both symmetric and skew coefficient equalities must be enforced: dropping the skew equations would silently lose arbitrary complex references.

The semidefinite orders and number of equality entries are polynomial in n,ell,m. The certificate is exact for any c>=0. Positivity floors and c upper bounds are separate linear constraints rather than rational denominators.

## 6. Paid weak-SDP complexity

For fixed rational 0<c and 0<kappa<1/m, take K0_yi=1/m. Let

    eta=min(1/m,c)/6,    C0=eta I_(ef),
    R0=diag(1/m,...,1/m,c)-3 eta I_f.

All nonconstant coefficient matches vanish by (3). C0,R0 and the K entry slacks are strictly positive with rational polynomial-bit margins. This is an explicit strictly feasible point in the affine equality space, regardless of rank(L). If c is an optimized variable in [0,cmax] with rational cmax>0, use c0=cmax/2 and include its two scalar slacks; the same construction is strict. The c=0 constant-release boundary is included by the exact SDP, without claiming a strict c=0 certificate.

Let a0=min{1/n, min_z s_z,1}>0. From the constant match, for any feasible point with c<=cmax,

    Tr C <= (1+cmax)/a0,   Tr R<=1+cmax.                    (7)

The stochastic K and bounded c also have explicit norm bounds. Represent the PSD blocks and all scalar inequality slacks as one block-diagonal SDP variable. The baseline's smallest displayed slack is an explicit inner radius for a Frobenius ball IN THE AFFINE EQUALITY SPACE (take half the smallest slack); all block entries are affine coordinates, so no unknown condition number is required. Polynomial-bit Gaussian elimination can remove dependent equality rows. Equations(3),(7) give rational outer-radius bounds about that baseline. Hence the usual rational weak-SDP theorem (deKlerk-Vallentin, Theorem1.1) applies, with cost polynomial in alphabet sizes, rational input bit lengths and log(1/accuracy). This does not assert exact boundary decision, strongly polynomial runtime, a practical speedup over all source-aware methods, or cheap physical qualification.

## 7. Scope retained

The new interface starts from a supplied classical L, raw classical input X, a specified linear utility/cost and a justified one-use conditional-information contract. It does not acquire L from samples, give raw X to an observer who only has L(X), implement a quantum reference experiment, or amplify the one-use budget into correlated multi-use compression. References may be arbitrary and noncommuting in the guarantee, but no reference needs to be sampled by the compiler.

The general free-linear inclusion theorem was already available. The substantive representation is the Fisher UNIT BALL that exposes a small affine source pencil; ordinary SDP machinery then does the synthesis. Priority is UNKNOWN. The same-information ordinary route includes this construction once its reduction is known, binary scalar Fisher optimization when applicable, general rational free positivity and exact real-algebraic methods. Actual numerical/exact receiver results and their costs will be reported without demoting those incumbents.

## 8. Boundary channels: the same finite operation covers every classical L

Strict entrywise positivity can be removed, with an explicit boundary convention. Let L be ANY finite nonnegative column-stochastic reference, delete its identically zero output rows, and keep its remaining ell rows. Let K also be merely nonnegative column-stochastic; identically zero rows contribute zero to F_K. The accepted inherited free formula is stated for exactly these nonzero-output-row channels, with faithful Q_i>0. Every W_y of a nonzero row is then positive definite. A0 in Section3 is still positive definite because each remaining row mean is positive. Thus all coefficient construction, closed-cone proof and trace bounds remain unchanged.

To prove the inclusion reduction without inverting any singular boundary W, first work only with faithful Q. Schur complements apply to all nonzero rows; a zero K row has both W_y=0 and (KU)_y=0 and can be deleted from that block test. The right-normalization proof remains valid. It establishes target positivity at every source-feasible point with faithful Q. For an arbitrary boundary source-feasible tuple x, replace x by (1-delta)x. Its source pencil is

    A((1-delta)x)=(1-delta)A(x)+delta A0>0,

and every Q_i has the added delta I/n. Target positivity at these tuples and continuity give B(x)>=0. This pays the closure in the needed direction and never substitutes an inverse on a null boundary support. Conversely free inclusion immediately bounds the faithful-Q forms and invokes the same inherited theorem.

Consequently (6) covers arbitrary finite classical reference channels, including their zero entries, rectangular shapes and rank deficiency. K may be constrained by any 0<=kappa<1/m, including kappa=0. The strictly positive constant baseline still supplies all scalar K slacks at kappa=0. Nonzero reference row means give polynomial-bit a0 from rational input; deleting zero rows is exact rational preprocessing. Actual execution below uses a strictly positive tall source, so this boundary extension is analytic and not a separate executed boundary-channel case.
