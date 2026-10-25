# Independent audit: WH3 entropy target for every normalized projector input

2026-10-25. **PASS for the complete projector-input class.** The source acquisition and operator-Schur receiving chain proves the WH3 entropy inequality for every rho=P/m, where P is any rank-m orthogonal projection on C^3 tensor a finite reference system. The reference marginal may be nonflat, its rank may be deficient, and m is arbitrary. This is not a proof for arbitrary nonflat global spectra or arbitrary density operators.

The proof below was independently reconstructed from the actual source interface rather than inferred from numerical examples. The previously audited operator theorem is an explicit import. Four fresh small generic-projector diagnostics check implementation identities separately and are not used as universal proof premises.

## 1. Channel and conditional expectation

Write

N=W3 tensor id_R,
W3(X)=[Tr(X)I_3-X^T]/2,
E(X)=I_3/3 tensor Tr_A X.

N is completely positive: the three antisymmetric Kraus matrices (|i><j|-|j><i|)/sqrt(2), i<j, give this expression. It is unital, trace preserving and self-adjoint for the Hilbert-Schmidt inner product. Direct substitution gives

N^2=(id+3E)/4.

E is a trace-preserving, self-adjoint conditional expectation. On any finite reference support, for every X>=0 one has X<=9E(X). For example, writing X as a positive 3-by-3 block matrix, block Cauchy-Schwarz bounds its quadratic form by three times the sum of diagonal-block quadratic forms, and every diagonal block is bounded by Tr_A X. This gives X<=3I_3 tensor Tr_A X=9E(X).

## 2. Complement index acquires an actual operator resource

Let P be a projection and B=E(P). Applying the same index bound to I-P>=0 gives

I-P<=9E(I-P)=9I-9B,

hence

9B-P<=8I.                                                   (1)

This is an actual source-compatible operator inequality. It is much stronger than the equal-trace constraint alone and is not a conjectured trace-to-norm implication. It uses the projection complement essentially.

## 3. Maximal marginal rank produces a saturated Schur interface

First assume rank P=m and the reference marginal has its maximal possible rank 3m. Restrict the reference to that support, so its dimension is 3m and B is faithful.

Write P=UU*, where U:C^m -> C^3 tensor C^(3m) is an isometry. In the system basis, U has three blocks U_i of shape (3m)-by-m, with sum_i U_i*U_i=I_m. Let

V=[U_1 U_2 U_3], R_ref=Tr_A P=VV*.

Maximal marginal rank means the square matrix V is invertible. Thus

V*(VV*)^-1 V=I_(3m).

Each diagonal m-by-m block is U_i*R_ref^-1 U_i=I_m. Since B^-1=3I_3 tensor R_ref^-1,

U*B^-1U=3 sum_i U_i*R_ref^-1U_i=9I_m,

or equivalently PB^-1P=9P as a compression to ran P.

Split the ambient space as ran P plus its orthogonal complement, and write B in 2-by-2 block form. B_22 is faithful. The block-inverse identity now implies that the Schur complement is exactly

B_11-B_12 B_22^-1 B_21=I_m/9.

Therefore

B=P/9+LL*,
L=[B_12 B_22^-1/2; B_22^1/2].

Combining this with (1) gives 9LL*<=8I. The nonzero singular values of L and L* coincide, or directly ||L||^2=||L*L||, so

9L*L<=8I.                                                   (2)

This is exactly the previously missing operator allocation, now derived from the physical source structure rather than assumed.

## 4. Exact placement in the audited operator-Schur theorem

Define on the lower space

V_env=9B_22>0,
Z=3B_12 B_22^-1/2,
H=Z*Z.

Then

9B=X_1=[[I+ZZ*,Z sqrt(V_env)],[sqrt(V_env)Z*,V_env]],

and H+V_env=9L*L<=8I. The audited operator transport with beta=4 applies without assuming H and V_env commute:

P log X_1 P >= 2P log X_4 P-2log(4)P.

Here P is compression onto the upper space. Since

(P+3B)/4=X_4/12,

the scale constants cancel exactly, yielding

2P log[(P+3B)/4]P-P log B P<=0.                            (3)

This is a compressed logarithmic statement for the actual source pair P,E(P), not an arbitrary pair with matching trace.

## 5. Singular output logs are handled by regularization

NP may have a kernel, so the expression N(log NP) must not be used without qualification. For epsilon>0, unital completely positive Jensen gives

N(log(NP+epsilon I))<=log(N^2P+epsilon I).

Take trace against P and use self-adjointness of N:

Tr NP log(NP+epsilon I)<=Tr P log(N^2P+epsilon I).

The left limit is Tr NP log NP because zero eigenvalues contribute exactly zero and lambda log(lambda+epsilon) tends to lambda log lambda. The right limit is finite since N^2P=(P+3B)/4>=3B/4>0. Consequently

2Tr NP log NP<=2Tr P log[(P+3B)/4]<=Tr P log B,              (4)

where the last inequality is the trace of (3).

As log B belongs to the range of E, self-adjointness of E gives

Tr P log B=Tr B log B.

The homogeneous WH3 gap of the unnormalized projection is

Delta_N(P)=2S(NP)-S(P)-S(Tr_A P)-m log3.

S(P)=0 and S(B)=S(Tr_A P)+m log3. Hence

Delta_N(P)=Tr P log B-2Tr NP log NP>=0.

This checks the sign, all entropy normalizations, and the only potentially singular logarithm. No support-compression substitution for log NP is made.

## 6. Constructive density of the maximal-rank source interface

An arbitrary rank-m projection has marginal rank at most 3m. Restrict the reference to its actual marginal support, then embed that support into C^(3m) by adding zero coordinates. The projection and all relevant channel entropies are unchanged by this reference isometry.

Choose an isometry U representing the embedded projection. Choose an isometry W whose three blocks W_i have mutually orthogonal m-dimensional ranges and are scaled by 1/sqrt(3). Then [W_1 W_2 W_3] is an invertible (3m)-by-(3m) matrix.

Set T_e=U+eW and U_e=T_e(T_e*T_e)^-1/2 for sufficiently small real e. T_e*T_e tends to I_m, so U_e is well defined, isometric and converges to U. The determinant

det([U_1 U_2 U_3]+e[W_1 W_2 W_3])

is a nonzero polynomial: its leading coefficient is the nonzero determinant of the W block matrix. Thus it has only finitely many roots. Choose a sequence e_j->0 avoiding them. Right normalization multiplies each block by the same invertible matrix, so [U_(e_j),1 U_(e_j),2 U_(e_j),3] remains invertible.

Therefore P_j=U_(e_j)U_(e_j)* are rank-m projections with maximal marginal rank 3m, and P_j->P in a single fixed finite-dimensional ambient space. The proof above gives Delta_N(P_j)>=0. Entropy is continuous in finite dimension, so Delta_N(P_j)->Delta_N(P), proving Delta_N(P)>=0 even when the original marginal is rank deficient.

This limiting step uses entropy continuity, not continuity of singular logarithms or an unjustified identification of varying marginal supports.

## 7. Return to normalized flat-spectrum states

The homogeneous gap scales linearly: the log-scaling terms cancel because N and partial trace preserve total trace. Therefore for rho=P/m,

Delta_N(rho)=Delta_N(P)/m>=0.

Equivalently, the original normalized entropy target holds for every density operator whose nonzero global eigenvalues are equal, of any rank and with arbitrary finite quantum reference. This is the entire normalized-projector input class, not only a chosen invariant 1+8 family and not only flat reference marginals.

## Checks and residual scope

`wh3_projection_input_independent_checks.py/.json` records four reproducible generic cases of ranks 1 through 4, reference dimensions 3 through 12. It independently implements N by partial transpose, checks N^2, the compressed inverse identity, the complement index, the compressed survivor and the actual homogeneous entropy gap. All pass; this is bounded diagnostic evidence only. The argument above proves the dimension-independent statement.

The operator resource bound is now acquired for projection inputs through their complements and generic Schur saturation. It is not acquired for arbitrary nonflat input spectra. Convexly mixing normalized projections does not automatically preserve the WH3 gap, whose required concavity has not been proved. No full-conjecture conclusion, historical novelty claim or physical decoder follows from this theorem.

## Additional audit of the author's stronger compressed-log limit

The governing complete theorem is `wh3_all_projector_inputs_entropy_theorem.md`. After the entropy-continuity proof above was independently reconstructed, its Section 5 supplied a stronger conclusion: the compressed operator inequality itself survives the generic approximation. This extra argument also **PASSES**.

For faithful B_e and log_eta(B_e)=log(max(B_e,eta I)), the low-spectrum difference F_e=log_eta B_e-log B_e is PSD. Thus

||U_e*F_e U_e||<=Tr P_e F_e<=9Tr B_e F_e<=9D eta/euler_number.

The middle inequality follows from P_e<=9B_e and positivity of F_e, without requiring their commutation. The last inequality is the exact scalar bound lambda log(eta/lambda)<=eta/euler_number on 0<lambda<eta, summed over at most D eigenvalues. The identical argument using P_e<=4C_e yields 4D eta/euler_number. These bounds are uniform in e.

At the limiting pair, kernels must be treated on support: P<=9B and P<=4C imply that ran P is orthogonal to both kernels. Consequently the compressed low-spectrum estimate ignores the zero eigenvalues, and the same bounds hold using supported logarithms. One must not assert that an arbitrarily extended log difference is PSD on the kernel; the author's explicit supported-limit convention avoids that mistake.

For fixed eta, log_eta is continuous on a common bounded spectral interval. Continuous functional calculus and U_e->U therefore give convergence of the truncated compressions. The uniform tails then give convergence of U_e*log B_e U_e and U_e*log C_e U_e. This proves the author's compressed inequality for every projector, even with deficient marginal rank.

Its final Jensen step is valid with NP+epsilon I before taking any log of a singular output. For limiting C, the same supported domination gives the compressed right-hand convergence. The equality Tr P log B=Tr B log B uses self-adjointness of E and the supported log B in its range. N fixes that range as well. Hence the author's direct entropy receiver and the independently reconstructed entropy-continuity receiver agree.
