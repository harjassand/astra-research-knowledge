# Independent substantive review: monotone constitutive remainder and convex quartic companion

## Verdict and exact bindings

The stated all-r monotonicity result passes this independent original-density reconstruction. I found no mathematical defect in the same-row finite identity, its all-matrix extension, strictness, exterior curvature, or the k=1 illustrative Schur calculation.

The separately supplied convex companion also passes: Psi is globally convex for every k>1/3, and its displayed strict Hessian lower bound follows from the actual Hopf-coordinate identity. This is a separate consequence, not the assertion that the original J is convex or quasiconvex.

Bindings:

- `ALL_R_MONOTONE_CONSTITUTIVE_REMAINDER.md`, SHA256 a80b7285b04294eefaadf7ef58d2bba2e69456f2a0a6cdbc232f71fbe111a449.
- `CONVEX_RADIAL_POTENTIAL_AND_SIGNED_MINOR.md`, SHA256 567eeaede9019353d8064498b7d9af03b4414d87ec59aaef714515996f0e8539.

Both exact source snapshots are preserved with this review. Their governing bytes were not edited. The main source's w(E) means the inner product of the two columns; the companion explicitly supplies this definition.

The conclusion is reusable constitutive and convexity machinery. It does NOT settle the remaining signed weighted-minor/current term or the original full J_r quasiconvexity question. No historical novelty conclusion is given.

## 1. Reconstruction from the original density

I used the uncompleted original column formula

    8n J=ell(k^2u^2+v^2+2uv+4kuj-4vj)+4(5k+1)j^2,

with k>1/3, ell=3k-1, n=k+1, m=3k+1. This equals j^2+ell R with R=H^2/(8n)+uv/4 and H=ku-v+2j.

The actual selector coefficient is

    lambda=[3ell(ku-v)+24k j]/(2m)
           =2j+ell L,
    L=[(3/2)(ku-v)+2j]/m.

Consequently T_full=DR-L cof F satisfies DJ=lambda cof F+ell T_full exactly. The first-row restriction uses clockwise C and cof F's first row C times the second row; its sign is correct.

The independent executable derives this decomposition directly, rather than importing any author function or certificate code.

## 2. Differential sign, including arbitrary matrix directions

The quartic reciprocity D^2J(F)[E,E]=D^2J(E)[F,F] and the common selector give

    D^2J(F)[E,E]=P(E)[F,F]+2lambda(F)det E.

Differentiating lambda cof F contributes

    Dlambda(F)[E] Dj(F)[E]+2lambda(F)det E.

The two determinant-direction terms therefore cancel, for ALL E, not only rank-one E. Hence

    Q(F,E):=ell DT_full(F)[E]:E
           =P(E)[F,F]-Dlambda(F)[E]Dj(F)[E].

The second channel has Dlambda(F)[E]+beta Dj(F)[E]=(3/m)L2(E,F), beta=3n/m>0. Completing its signed product gives

    Q(F,E)=[Dlambda(F)[E]-beta Dj(F)[E]]^2/(4beta)
                    +sum_(i != 2) C_i L_i(E,F)^2>=0.

All four coefficient weights are nonnegative on the exact domain k>1/3. The executable independently checks this full polynomial identity from the original constitutive map, including all mixed entries.

## 3. Finite secant and strict quartic remainder

For E=F1-F0 and Fm=(F0+F1)/2, Q(Fm+tE,E) is quadratic in t. Integrating from -1/2 to 1/2 gives the exact finite secant

    ell [T_full(F1)-T_full(F0)]:E
                  =Q(Fm,E)+Q(E,E)/12.

Now P(E)[E,E]=12J(E)-2lambda(E)det E, while the product term in Q(E,E) is 4lambda(E)det E. Therefore

    Q(E,E)/12=J(E)-lambda(E)det E/2=Psi(E).

Quadratic midpoint polarization gives Dlambda(Fm)[E]=delta lambda and Dj(Fm)[E]=delta j, yielding the stated finite identity exactly.

The displayed positive form is also exact:

    Psi=ell[H-beta j]^2/(8n)+ell w^2/4
                               +3ell n(2m-3)j^2/(8m^2).

Its last coefficient is positive because 2m-3=6k-1>0. If Psi=0, then j=w=0. The identity uv=w^2+j^2 forces one column to vanish. H=ku-v=0 then forces the other to vanish because k>0. Thus Psi(E)>0 for every nonzero E.

This proves strict monotonicity, with a fourth-power modulus rather than an incorrectly asserted constant quadratic strong-monotonicity modulus at the origin. A positive per-k Euclidean fourth-power floor follows by compactness. The source's same-row floor is explicit: det E=0 gives Psi(E)=J(E)=ell[k^2e1^4+2e1^2e2^2+e2^4]/(8n). It stays nondegenerate after division by ell as k approaches 1/3 from above, but no uniform coefficient as k tends to infinity is asserted.

For same-row comparisons, the symmetric original Bregman equals P(E)[Fm,Fm]+J(E), since det E=0. Subtraction of delta lambda delta j produces exactly the same signed square, not a separately spendable determinant cost. This verifies both the row and full-matrix versions.

## 4. Exterior curvature and the non-gradient qualification

As a one-form on matrix space,

    T_full dot dF=dR-L dj,
    d(T_full dot dF)=-dL wedge dj.

This exterior derivative is generally nonzero. For example at F=E11, dL wedge dj has coefficient 3k/m in the da wedge dd direction. Thus T_full is not a gradient map. The checker verifies all six antisymmetric derivative entries, not just one example.

A positive symmetric derivative therefore does not license a convex-potential interpretation of T_full itself. Along a physical path changing both rows, the mixed second-row work remains. The row result cannot be applied to a full difference whose second row changes.

## 5. Independently reconstructed global convexity of Psi

Write K=Psi/ell=R-Lj/2. Direct differentiation and quartic reciprocity give

    D^2Psi(F)[E,E]=[Q(F,E)+Q(E,F)]/2>=0.

This identity is checked independently by exact polynomial arithmetic. It proves global convexity of Psi, distinct from the monotonicity of the nonconservative map T_full.

Since Q(E,F)-Q(F,E)=2[lambda(F)j(E)-lambda(E)j(F)], positivity also gives the companion's radial two-state area bound. This is not a general two-direction sector bound on d lambda wedge dj.

The companion's direct feature form is correct:

    K=[3(ku+v)^2+(ell/n)H^2+4w^2]/(16m).

To verify it, substitute uv=w^2+j^2 and H=ku-v+2j; the difference reduces to 3[(ku-v)^2-(ku+v)^2]+12kuv=0.

In first-column-scaled Euclidean coordinates, N=ku+v and the three actual quadratic features q=ku-v, r=2sqrt(k)j, z=2sqrt(k)w obey q^2+r^2+z^2=N^2. The stated orthogonal rotation gives Q_plus=sqrt(k/n)H, so

    K=[3kN^2+ell Q_plus^2+z^2]/(16km).

For nonnegative feature weights c_i, differentiating their squares gives a positive sum plus 4 sum c_i Q_i(F)Q_i(E). The actual feature-norm identity bounds the latter below by -4 max(c_i)N|E|_k^2. Combining it with the radial Hessian proves exactly

    D^2K(F)[E,E]>=min(ell,1)N|E|_k^2/(4km).

Thus the explicit strict Hessian bound and its stated integrated 1/36 factor are valid. The latter follows by minimizing the exact quadratic integral integral_0^1(1-t)|F+tE|_k^2 dt at F=-E/3.

A separately derived useful consequence is the exact general convex-quartic identity

    B_Psi(F+E;F)
       =(1/2)D^2Psi(E)[F+E/3,F+E/3]+Psi(E)/3
       >=Psi(E)/3.

It is sharp at F=-E/3. This is a full-matrix convex Bregman resource. It belongs to the SAME Psi term, not an addition to an already allocated original J budget.

## 6. Function spaces, costs and reuse

The finite statements are pointwise identities for real matrices. They integrate for L4 matrix fields because T_full is cubic, Psi is quartic and all products are integrable. No spatial regularity, boundary condition or compatibility is needed for these constitutive identities. Applying them to a gradient PDE, a varying reference state or a transported covector still requires that problem's actual weak formulation, periods and mixed-work ledger.

The radial identity ell T_full(F):F=4Psi(F) supplies coercivity in addition to monotonicity. This makes the map genuinely reusable in auxiliary monotone-operator constructions, while the convex Psi gives a genuine full-matrix Jensen and Bregman resource. Those consequences are more than a renamed selector square: they specify an actual nonlinear map, its finite secant, its nonconservative curvature, a strict homogeneous modulus, and a convex companion. Their algebra does follow from the already earned selector, so no novelty claim or new complexity theorem is warranted.

The unresolved original energy is exactly

    J=Psi+lambda j/2.

Lambda here is the actual quadratic selector lambda, not a constant affine multiplier. Its product with j is not a null Lagrangian. Monotonicity or convexity of the companions does not sign its fluctuation, authorize heat decrease of J, or prove the original quasiconvexity statement. Nor may these companions be added as independent reserves to a previously spent Bregman allocation.

## 7. Independent execution and disposition

The separately written `check_original_density.py`, SHA256 008b0dc9558fa042aa6292e612d09a2e001841e76d43742e3df037d380391144, starts from the uncompleted original J and imports no author code. One externally capped 15-second single-thread execution passed all 19 exact identities:

- Original stress decomposition and explicit Psi sum of squares.
- Full differential and finite monotonicity identities and the row quartic floor.
- All six exterior-curvature entries.
- Convex-Psi Hessian reciprocity and radial coercivity.
- The k=1 explicit map, symmetric derivative, eliminated block, Schur remainder and determinant.

It completed in 2.630853198 seconds scientific time, 3.293546952 seconds wrapper time, return code 0, maximum child RSS 52,268 KiB. The stdout, stderr, exit code, protocol and receipt are preserved. There were no failed runs, parameter samples, floating optimization or scientific retuning.

The Hopf strict bound above was reconstructed analytically, not presented as an additional executed check. The verdict is favorable for both fixed source statements and the explicitly separated consequences at the exact scopes stated here. The full J_r quasiconvexity question remains open in this work.
