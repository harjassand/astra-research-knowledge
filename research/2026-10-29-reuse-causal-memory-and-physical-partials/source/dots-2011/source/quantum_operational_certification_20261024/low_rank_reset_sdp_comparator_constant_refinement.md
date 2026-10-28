# Constant refinement of the received overlapping-reset SDP comparator

27 October 2026. Local post-cutoff. Separate independent receiving requested. The whole theorem is already frozen in `overlapping_rank_two_reset_reusable_sdp_receiver.md`. This note only sharpens its comparator constant from6e/M to2e/M, without replacing or reopening that received theorem.

## Source and normalization

Let V:C3 tensor L -> R be isometric, C>=0 on L with rank C<=r, and Y>=0 on R with rank Y<=2. Reset may overlap the code, including coherent reset-only spectators. Use unnormalized Omega=sum_i|ii> and

 X=(I tensor V)(P_Omega tensor C)(I tensor V*)+I3 tensor Y,
 A=V(I3 tensor C)V*, c=TrC, tY=TrY,
 M=TrX=3(c+tY), J=X/M,
 p=3c/M, delta=Delta(J).

Assume c>0 and M>0. The actual TP source is

 E(rho)=V(rho tensor C/(c+tY))V*+Tr(rho)Y/(c+tY).

Thus J is its normalized Choi operator, p is genuine signal weight, and 1-p=3tY/M is reset weight. No separate normalization of main and reset is used in the entropy estimate.

Define e=e(A,Y). The independently received discrimination stability theorem gives

 e^2<=K tY Delta(X),
 K=1944 for rankY<=2, K=216 for rankY<=1.             (1)

The overlap classification is separate; only this quantitative inequality is used.

## Explicit feasible comparator

Let Q be an optimal Helstrom PROJECTOR deciding Y in discrimination of A from Y, and let P=I-Q. Then

 TrAQ+TrYP=e.

Let P_code=V(I3 tensor P_suppC)V*, and let Pi be the true Bell/active-flag projector on A_ref tensor R. Its rank is rankC<=r and

 Tr_Aref Pi=P_code/3.

Define the operator

 F_*=(I_Aref tensor P) Pi (I_Aref tensor P).           (2)

This is an ACTUAL feasible point of the low-trace decoder SDP:

 F_*>=0,
 Tr_Aref F_*=P P_code P/3<=I_R/3,
 TrF_*=Tr[Pi(I tensor P)]<=r.

By the received operational decision-set identity, F_* is precisely a CP trace-nonincreasing accepted decoder, followed by an erasure completion. It is not an abstract score matrix or a normalized compression surrogate. The unknown Q and Pi are only used to prove comparator existence; the learned SDP does NOT receive either as an oracle or supplied inverse.

## Source-native utility payment

Write Gamma for the genuine part of J. It has trace p, reference marginal A/M, and Pi Gamma=Gamma Pi=Gamma. Put

 alpha=TrAQ/M, betaY=TrYP/M.

Expanding (2) using I tensor P=I-I tensor Q gives genuine entanglement overlap

 f_s=Tr Gamma F_*
    =p-2alpha+Tr[Gamma (I tensor Q)Pi(I tensor Q)]
    >=p-2alpha.                                     (3)

The last term is nonnegative by positivity; no commutation of Q with code or reset is assumed. The genuine accepted mass obeys a_s<=p. The reset accepted mass obeys

 a_n=3Tr[Y P P_code P]/M<=3betaY,

and its entanglement overlap is f_n=a_n/9 because the reset is input independent.

For the SDP's actual utility loss L_*=2p/3-Tr[(J-3omega)F_*], the exact operational decomposition therefore gives

 L_* =2p/3-f_s+a_s/3+(2/9)a_n
     <=p-f_s+(2/9)a_n
     <=2alpha+(2/3)betaY
     <=2e/M.                                        (4)

This is an actual original-source bound; it does not rely on a false generic monotonicity of the entropy deficit under a reference filter.

Combining (1),(4), homogeneity Delta(X)=M delta, and tY/M=(1-p)/3 yields

 L_*<=2 sqrt[K(1-p)delta/3].                         (5)

## Receiving into the frozen whole theorem

The canonical `overlapping_rank_two_reset_reusable_sdp_receiver.md` already supplies the complete learned receiver and confidence/resource accounting using the weaker safe comparator L_*<=6e/M. Its proof and statement remain unchanged. Equations (4)--(5) above may be substituted only as an optional constant refinement in its received robust-comparison interface. No new whole theorem, accuracy exponent, or acquisition claim is asserted here.

## Scope guards

No arbitrary reset rank, arbitrary nonreversible main, unrestricted entropy conjecture, efficient gate synthesis, or structural-promise certification is inferred. The source has no independent full-rank white floor in this statement, because (1) is the received zero-white low-rank-reset stability result. The code comparator is an existence proof used by an acquired optimization, not an algorithm given the unknown V or Helstrom projector. Approximate SDP optimization must be charged through its separately stated tolerance term.
