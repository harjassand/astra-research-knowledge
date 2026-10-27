# WH3 full entropy target for arbitrary maximally-correlated inputs

## Theorem

Let N=W3 tensor id_R and E=I3/3 tensor Tr_A. Let |r_0>,|r_1>,|r_2> be orthonormal reference vectors, and let

 A=sum_{i,j=0}^2 Xij |i,r_i><j,r_j|,  X>=0.

For the homogeneous entropy deficit

 Delta(A)=Tr A log A+Tr EA log EA-2Tr NA log NA,

one has

 Delta(A)>=3 lambda_min(X) log(4/3)>=0.             (1)

In particular every normalized maximally-correlated state satisfies the full WH3 target, without a restriction on its spectrum or commutation with its reference marginal. Local changes of the matched bases and reference isometric embeddings preserve the statement. Missing coordinates may be padded by zero.

## 1. The anchored class is now closed

Let A have largest eigenvalue one, and choose any unit top eigenvector psi. It lies in the matched correlated span. By changing local diagonal phases its nonzero Schmidt coefficients can be made positive. Its reduced projector is diagonal in the same reference basis as EA.

If psi has Schmidt rank at most two, `wh3_rank_two_commuting_marginal_anchor_theorem.md` proves

 g(A;P)=Tr EP log EA-2Tr NP log NA>=0,
 P=|psi><psi|.

For Schmidt rank three, no conjugation reduction is needed. After gauging the top vector u positive, the complex Hermitian correlated block satisfies Xu=u, 0<=X<=I. The pair Rayleigh identity uses only Re(Xij), and Xu=u gives exactly v_ij* Kij v_ij=(1-2lambda_k+lambda_k Xkk)/2 for the pair excluding k. Likewise S=X-uu*>=0 and Su=0 give the same paid diagonal trace constraint over complex matrices. Its anchored sign is therefore proved directly by:

- `wh3_aligned_zero_population_balanced_face.md` when all Schmidt weights are at most 1/2;
- the source-paid envelope in that same note, combined with `heavy_zero_population_scalar_theorem.md` and its exact certificate, when one Schmidt weight is at least 1/2.

Thus g>=0 for every top eigenvector of every maximally-correlated input in this class. The proof retains the true channel terms; it is not an assumed concavity or scalar layer-cake lift. Indeed concavity on this very class has an exact counterexample recorded in `wh3_maxcorr_concavity_obstruction.py/.json`.

## 2. Exact spectral lowering

First suppose X>0 and let mu=lambda_min(X)>0. Lower the largest eigenvalue of X until it meets the next eigenvalue, and continue lowering the entire current top eigenspace until all eigenvalues equal mu. Every intermediate matrix remains supported on the same correlated span. Hence every intermediate top anchor remains in the class proved in Section 1.

For any supported differentiable variation H,

 d Delta(A)[H]=Tr H G(A),
 G(A)=log A+log EA-2N(log NA),

with the first log understood on the fixed input support and the output log on its fixed support. For a top eigenvector with eigenvalue L, homogeneity of the logarithms gives

 <psi,G(A)psi>=g(A/L;P)>=0.

Consequently along lowering of the top spectral projector Q,

 d Delta(A)/dt=-Tr Q G(A)<=0.

Summing over its orthonormal top eigenvectors is justified by the anchored theorem for each such vector. The spectral path has finitely many merging steps. Therefore

 Delta(A)>=Delta(mu J),
 J=sum_i |i,r_i><i,r_i|.

There is no unproved entropy convexity or reference-discarding step here.

## 3. Endpoint and singular inputs

Directly,

 EJ=I_A tensor Pi_R/3,
 NJ=(1/2)sum_{i!=j}|i,r_j><i,r_j|.

Both have trace three. Hence Delta(J)=3log(4/3), and homogeneity gives Delta(mu J)=3mu log(4/3), proving (1) for X>0.

The supported derivative is legitimate: for faithful X the input support is the fixed correlated subspace; each 2x2 output pair block is positive definite, and the output support is the fixed span of the six offdiagonal matched vectors. Reference-marginal entries are positive. No logarithmic derivative crosses a changing support during the path.

For singular X, apply the faithful result to X+epsilon I3 and let epsilon decrease to zero. Finite-dimensional entropy continuity gives (1). This regularization stays within the proved correlated source class.

## Scope

This is a full entropy theorem for the entire maximally-correlated support class, including genuinely nonflat, non-modular-commuting inputs. It does not prove the arbitrary-input WH3 target. The aligned rank-three program with nonzero offdiagonal populations and general nonaligned entangled anchors remain outside this theorem.
