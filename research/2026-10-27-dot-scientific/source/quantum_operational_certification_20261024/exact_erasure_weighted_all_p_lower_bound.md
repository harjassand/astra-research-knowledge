# Weighted-reference sharpening: every p has the same quadratic constant

2026-10-27. Analytic refinement of the all-p dilution corollary; pending independent receipt. It does not change the task/access scope.

For0<p<=1/2 let D=floor(1/p), and use the same padded channel in `exact_erasure_hidden_flag_all_p_and_recovery_corollaries.md`. Its normalized Choi state is

 J_(U,psi)=B0+p (Phi_U-I9/9) tensor Ppsi,
 B0=(p/9) I9 tensor I_D + (1-pD)(I3/3) tensor |e><e|.

The two summands of B0 have orthogonal receiver supports, B0 has trace one, and its eigenvalues are p/9 on the9D-dimensional main block and(1-pD)/3 on the extra3-dimensional block. The perturbation has zero trace and lies in the main block. Hence, with inverses taken on supp B0,

 Tr[J_(U,psi) B0^(-1) J_(U,phi)]=1+8p t,
 t=|<psi|phi>|^2.

If pD=1, discard the zero-weight extra support; no singular inverse is used. The common Weyl teleportation correction acts as W on the main logical factor and as the identity on the extra erasure output, so the full adaptive-query stretching remains exact.

For S_U=E[J_(U,psi)^tensor n tensor Ppsi] choose reference
 B=B0^tensor n tensor I_D/D.
The weighted chi-square is

 chi²=Tr[(S_U-B)B^(-1)(S_U-B)]
     =E[D t(1+8p t)^n]-1.

For Hermitian X supported on B, the trace norm bound follows from the polar sign and Hilbert-Schmidt Cauchy-Schwarz:

 ||X||_1=Tr(sign(X)X)
 <=sqrt(Tr B) sqrt(Tr[X B^(-1)X]).

For example factor the trace as Tr[(B^(1/2)sign(X))(X B^(-1/2))]; the first squared Hilbert-Schmidt norm is Tr[B sign(X)^2]<=Tr B. No simultaneous diagonalization with X is required.

Using Haar moments, for x=8pn/(D+1)<1,

 chi²+1=sum_(k=0)^n binom(n,k)(8p)^k
                  (k+1)!/[(D+1)...(D+k)]
 <=sum_(k>=0)(k+1)x^k=(1-x)^(-2).

The two inverse hypotheses have orthogonal ideal outputs, so exactly as in the canonical proof,

 n >= (D+1)/(8p) [1-1/sqrt(1+(1-zeta)^2)].             (1)

Since D+1>1/p, this implies the uniform slightly weaker non-strict statement

 n >= 1/(8p^2) [1-1/sqrt(1+(1-zeta)^2)].               (2)

In particular zeta<=1/4 requires n>=1/(40p^2) for EVERY0<p<=1/2. The branch x>=1 automatically satisfies(1). Receiver dimension is3floor(1/p)+1, all sources have EXACT zero deficit, and n counts a maximum number of adaptive physical channel queries.

Replacing1-zeta by the positive separation s=alpha-17delta/(8p) gives the same all-p refinement for complete noisy recovery under the separately proved transfer lemma. Fixed absolute recovery error as p tends to zero, expected-cost query budgets, known flags, and fixed receiver dimension are not covered by this statement.
