# Reviewer reconstruction of the global guarantees

This derivation was made from the accepted free representation and the frozen phase 1 sources, without importing producer verification code. Its universal argument is separate from `EXACT_ALGEBRA.json`, which only diagnoses six exact finite implementations of the identities. No statement here applies to nonpositive channel entries or noninjective L.

Write B=((1,0),(0,1),(-1,-1)), P=(I_2,0), R_M=PMB, and A_M(Q)=sum_y (M_y B)^T(M_y B) tensor W_y^-1. All W_y lie between min_i M_yi I and max_i M_yi I. Also A_L dominates the strictly positive matrix B^T L^T diag(1/max_i L_yi) L B tensor I. Consequently the quotient has no nonzero zero denominator, its normalization is compact, and PSD boundary effects are legitimate limits of faithful effects.

For positive W_1+W_2+W_3=I, put w=(W_1,W_2)^T. Direct ordered multiplication, using W_3^-1(W_1+W_2)=W_3^-1-I, proves

    N(W)^-1 = diag(W_1,W_2)-w w*,
    N(W) = [[W_1^-1+W_3^-1,W_3^-1],[W_3^-1,W_2^-1+W_3^-1]].

This uses no commutation of W_1 and W_2. Since R_L is invertible, H_L=A_L^-1=R_L^-1 N(W^L)^-1 R_L^-T. Expanding the output weights and evaluating the affine remainder at deterministic scalar effects gives

    H_L(Q)=sum_i H_L(e_i) tensor Q_i + Gamma(Q),
    Gamma=diag(Q_1,Q_2)-[Q_1;Q_2][Q_1,Q_2] >=0.

The final positivity is the covariance/compression inequality: diag(sqrt(Q_i)) times the projection I-r*r times diag(sqrt(Q_i)), with r=[sqrt(Q_1),sqrt(Q_2),sqrt(Q_3)] and rr*=I, has this as a principal block.

For X13 let x_i=PK[:,i], D=PKB, T_i=diag(x_i)-x_i x_i^T, and S_i=D H_L(e_i)D^T. Equality of the nonzero singular values of an operator and its adjoint gives, even if K is singular,

    A_K<=c A_L iff p_c=c N(W^K)^-1-D H_L D^T>=0, c>=0.

Let X=sum_i x_i tensor Q_i and V=sum_i x_i x_i^T tensor Q_i-XX*>=0. Ordered expansion gives

    p_c=sum_i(cT_i-S_i) tensor Q_i+(c-1)V.

For c>=1 the vertex tests cT_i-S_i>=0 therefore suffice, and taking Q_i=I makes them necessary. Thus a vertex maximum at least one is the exact all-reference coefficient, including singular K. For c<1 and any real z,

    p_c=(1-c)(X-zI)(X-zI)*
        +sum_i[cT_i-S_i-(1-c)(x_i-z)(x_i-z)^T] tensor Q_i.

The three rational PSD residuals are a global certificate over all complex effects in every finite dimension. Sufficiency does not depend on numerical optimality. Completeness follows by writing E_i=U*Q_iU, G=sum E_i, d=sum E_i x_i for two arbitrary test columns U. Projection gives ||X*w||²>=d*G^+d, with equality realizable on supp(G), dimension at most two. The resulting first-moment SDP has Slater points E_i=I/6 with large Schur variable. Its attained dual is exactly the displayed three residuals after completing the square. Averaging complex moment data with its conjugate preserves feasibility and objective, so a real center suffices. This is a legitimate real reduction of a complex problem.

X68's portable vertex and center certificates are the same covariance argument in the inverse K coordinates. Its singular-K expansive extension follows by K_epsilon=(1-epsilon)K+epsilon L and uniform continuity of all output inverses. Its additional general certificate avoids inversion of K: put M=KB and

    p_c=c diag(W^K)-M H_L M^T.

For three test columns V set X_i=V*Q_iV, Y_ij=V*Q_iQ_jV, H=diag(X_i)-Y. Then Y,H>=0 and H[I;I;I]=0. With s=(M[:,1],M[:,2],0) stacked, p_c's quadratic form is sum_i Tr([c diag(k_i)-M H_L(e_i)M^T]X_i)-s*Hs. A real symmetric 9x9 matrix A with those diagonal blocks, A>=0 and T^T(A-ss^T)T>=0, where T spans ker([I,I,I]), bounds this by Tr(AY)+Tr((A-ss^T)H)>=0. This proves the upper guarantee independently of the solver. The source's degree-two moment completeness argument is sound: normalize a positive contraction by diag(X_i)^1/2, use HE=0 to fix the test columns, and dilate the contraction to a projection. This realizes the moments as POVMs, including complex ones. Slater feasibility of the normalized moment SDP then supplies the claimed exact finite-SDP characterization.

For lower bounds I checked effects and vectors directly. X13's rational E_i,h_i denote Q_i=G^-1/2 E_i G^-1/2 and u_i=G^-1/2 h_i, G=sum E_i>0. The output inverse quadratic term equals h_y*E_y^-1h_y exactly; the square root cancels by congruence. X68 supplies rational Q_i summing to I. In both cases PSD, sum u_i=0, positive denominator, and the reported exact ratio are checked. Boundary effects are allowed only through the stated uniform-positive-output closure. The accepted active/vacuum construction supplies the Umegaki lower limit; these free witnesses are not physical preparation experiments.

The coefficients, compactification, and certificates remain tied to strictly positive rational 3x3 classical channels and injective L. General coherent quantum channels and singular output mixtures are outside this proof.
