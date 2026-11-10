Sharp cubic lifting from the new four-square identity, and a fixed-field all-parameter calculation

Use the original J_k, k>1/3, ell=3k-1,n=k+1,m=3k+1. The completed 7916AD return supplies the bilinear four-vector S(A,E) with
 D2J_k(A)[E,E]=|S(A,E)|^2+2lambda(A)det E,
 lambda(A)=[3ell(k|A_col1|^2-|A_col2|^2)+24k det A]/(2m).
Its exact four weighted forms are in the original packet. No general global Jensen theorem is assumed.

1. An exact cubic identity in the SAME strain space.

Differentiate the displayed Hessian identity with respect to its background A in direction G, keeping E=G. Quartic polarization gives D3J(A)[G,G,G]=6 DJ(G):A. Bilinearity of S therefore yields pointwise
 3 DJ(G):A=S(A,G).S(G,G)+Dlambda(A)[G]det G.
Because lambda is quadratic, Dlambda(A)[G]=Dlambda(G):A.

For an actual mean-zero compatible G define the finite-rank map
 K_G:A -> S(A,G) in L2(T2;R4),
 g_G=S(G,G), r_G=int Dlambda(G)det G,
 c=int J(G), b=int DJ(G), H[A,A]=int D2J(A)[G,G].
The constant-background determinant integrates to zero, so K_G^*K_G=H. Integration of the new cubic identity gives exactly
 3b=K_G^*g_G+r_G.
The already accepted range condition b in range H implies r_G in range H as well. Hence the least-norm solution of K_G^*z=3b is explicitly
 z_min=K_G H^dagger(3b)=P_G g_G+K_G H^dagger r_G,
 P_G=K_G H^dagger K_G^*.
Here P_G is the orthogonal projection onto the finite-dimensional range of K_G, not a projection of arbitrary matrix fields into compatible gradients.

Thus the full sharp moment inequality is equivalent to the concrete lifting bound
 ||z_min||2^2<=18c.
This is an exact reformulation, NOT a proof of the bound. The four-square factorization identifies the specific correction r_G that must be paid, rather than giving a positive cubic estimate for free.

There is an exact defect identity. Put q_G=int lambda(G)det G. Euler homogeneity gives ||g_G||2^2=12c-2q_G, so
 18c-||z_min||2^2
 =6c+2q_G+||(I-P_G)g_G||2^2
   -2(K_G^*g_G)^T H^dagger r_G-r_G^T H^dagger r_G.
Every term is finite for G in L4; the pseudoinverse is of the actual finite matrix H. Singular-H cases retain their accepted treatment. No signed weighted determinant is declared a null Lagrangian, and no positive bound for the last two terms is supplied.

The pointwise strain cannot itself control this correction. Take A=I and D=diag(2,-m). The supplied strain identity gives S(I,D)=0, while direct evaluation gives
 Dlambda(I)[D]=3n ell/m,
 det D=-2m,
 DJ(D):I=-2n ell !=0.
Thus a universal pointwise estimate |DJ(G):A|<=C sqrt(J(G))|S(A,G)| is FALSE, for every finite C. Compatibility and integration must enter any sharp lifting construction. D is a constant matrix, not a mean-zero compatible periodic gradient, so this is not a negative quasiconvexity witness.

2. Exact extension of one supplied finite field across ALL affine means and k.

The original updated ZIP is P1_PRO_7916AD_QUARTIC_ORIGINAL_20261110.zip,427729bytes/SHA08c3f11db748b86725fa9f1943cf29012800b91324f9703d39ae47fdfdb47d08. The field is exactly the128-triangle N8 nodal potential in continuation/construction_continuation/exact_below_one_third_reserve.json. Its nodes are fixed; only its affine mean and k vary in this calculation. The archive was read unchanged, and none of its verification scripts was executed.

Direct algebra gives a degree-three parameter polynomial:
 Phi_k(F):=8(k+1)J_k(F)
 =3u^2 k^3+(-u^2+12u j)k^2
  +(6uv-4u j+3v^2-12v j+20j^2)k
  +(-v^2-2uv+4v j+4j^2),
 u=|F_col1|^2,v=|F_col2|^2,j=det F.
The positive normalizer8(k+1) preserves all gaps for k>1/3. For fixed G, exact triangle averages and15 evaluations of the quadratic all-mean gap at0,+-e_i,e_i+e_j determine the polynomial5x5 moment matrix M(k)=[[2c,bT],[b,H]] for Phi_k.

ROOT constructed a NEW standard-library Fraction/primitive-Sturm implementation in ROOT_QUARTIC_FIXED_FIELD_PARAMETER_SCHUR_20261110.py. It reads the hash-pinned original nodes, forms the actual128 compatible constant gradients and integrates their degree-three parameter coefficients exactly. It then computes det H (degree8) and det M (degree11) by finite permutation determinants. Primitive polynomial Euclidean remainders preserve positive normalization of every Sturm entry. At1/3 it takes the right-hand sign using the first nonzero derivative, so a root at the excluded parameter boundary is not miscounted. At infinity it uses the leading coefficient.

The recorded exact result is ROOT_QUARTIC_FIXED_FIELD_PARAMETER_SCHUR_20261110.json. The Sturm variations for det H are2 at1/3+ and2 at infinity; for det M they are3 at1/3+ and3 at infinity. Thus NEITHER determinant has a zero on(1/3,infinity). The accepted Legendre-Hadamard/compatibility argument gives H>=0 for all such k; its nonzero determinant makes H positive definite. At17/50 the optimized ORIGINAL gap is
 1103644079891252812567006309238107721302039259
 /703580456616520609051430213052820164098129920000 >0.
Therefore det M is positive throughout the connected interval, and the Schur complement proves a strictly positive original gap for EVERY real affine mean and EVERY k>1/3 for THIS ONE FIXED FIELD. In particular, changing only k or the mean of this supplied reserve-obstruction field cannot make a negative witness.

Its optimized gap-to-c ratio is exactly
 2207288159782505625134012618476215442604078518
 /197361508643616347939057394377076505416778807191.
The small positive ratio does not prove existence of a saturating sequence, a uniform global reserve, or a negative elsewhere. The producer's stronger c/3 failure remains valid at its stated mean; this new calculation is not a rerun or challenge to that accepted certificate.

Actual finite work:128 triangles,15 gap-polynomial evaluations,24 four-by-four and120 five-by-five determinant permutations, and two finite Sturm chains ending at degree1. The new run completed in0.059167209023144096 seconds. The largest final primitive determinant coefficient had116 bits; intermediate arithmetic and peak memory were not separately profiled. No optimizer, numerical quadrature, PDE solver, installed dependency, extra worker or physical experiment was used. Exact source/result files contain the full degree8/11 polynomials and sign sequences. There is no claimed efficient positive termination or all-gradient certificate; the computation is one mathematical parameter study of a supplied admissible field.

3. Scope of the constructive opening.

The completed return's frequency/concentration-independent cubic estimate and one-direction positive neighborhood remain substantive accepted mathematical tools. The sharp original operation is still the energy bound for a compatible cubic lifting, equivalently b^T H^dagger b<=2c for all remaining actual gradients. The new exact lifting identity locates the signed Jacobian correction; the fixed-field result rules out a particular parameter/mean-only negative route. Neither resolves the full original question. The scientist may bypass both representations.
