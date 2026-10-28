# Independent two-face determinant and whole relative-peak-three audit

27 October 2026. Analytic PASS after independent reading of the frozen canonical reduction_criterion_whole_entropy_root_theorem.md and exact checker replay. This proof does not rely on boundary coercivity, inverse-trace positivity, pinching, or entropy whitening.

Let E be the trace-preserving physical-qutrit conditional expectation and N=W3 tensor id. Both are unital completely positive and Hilbert–Schmidt self-adjoint; N²=(id+3E)/4. Fix any finite reference dimension and 0<epsilon<1<c<3. The compact slice epsilon I<=M<=cI, EM=I has strict feasible point I. Both M and NM are uniformly faithful. Its determinant functional F=2 logdet NM−logdet M attains a minimum.

Use the extension F_full(X)=2 logdet NX−logdet X−logdet EX, which agrees on the slice and is invariant under every invertible reference congruence. Its gradient at M is G=2N((NM)^−1)−M^−1−I. Semidefinite KKT applies by strict feasibility: G+I tensor Lambda+S_plus−S_minus=0, with nonnegative normals supported respectively on the c and epsilon eigenspaces. In particular these supports are orthogonal.

Reference-congruence invariance gives Tr_A(MG+GM)=0. Substitution and Tr_A M=3I give Lambda=−c Tr_A(S_plus)/3+epsilon Tr_A(S_minus)/3. Therefore
G=c E(S_plus)−S_plus−epsilon E(S_minus)+S_minus.

Let P_plus be the upper-face projection. M>=cP_plus implies cE(P_plus)<=I. The CP map cE from this corner algebra is subunital; its Schwarz inequality gives c||E(S_plus)||_HS²<=||S_plus||_HS². Hence
Tr(S_plus G)=c||E(S_plus)||²−||S_plus||²−epsilon Tr[E(S_plus)E(S_minus)]<=0.
The cross trace is nonnegative because both conditional expectations are positive. No commutation of the expectations is needed.

Operator inverse Jensen for the actual CP map N gives
G>=8(M+3I)^−1−M^−1−I=f(M),
f(m)=(m−1)(3−m)/(m(m+3)).
Thus Tr(S_plus G)>=f(c)Tr S_plus with f(c)>0, forcing S_plus=0. If any eigenvalue m of M exceeded one, its eigenvector would be orthogonal to the lower-face support and would have G expectation −epsilon<E(S_minus)><=0, contradicting f(m)>0 since m<=c<3. Consequently M<=I, and EM=I forces M=I by trace. Every global minimizer is therefore I, proving F>=0 with equality only at I on this slice. Choosing epsilon and c around any faithful M<3I proves the dimension-free strict-cap determinant theorem.

For arbitrary X>=0 with X<=3tau, tau=EX, restrict to its actual reference support so tau>0. At each s>0 set M_s=(tau+sI)^−1/2(X+sI)(tau+sI)^−1/2. Then EM_s=I, M_s>0, and M_s<3I because 3(tau+sI)−(X+sI)>=2sI. Reference congruence commutes with N. The exact original-source trace-entropy Bregman identity yields
Delta(X)=integral_0^infinity [2 logdet NM_s−logdet M_s] ds.
Linear terms vanish by E(X−tau)=0. This is not an entropy congruence argument: whitening is used only within each exact determinant integrand. At zero, any singularities are at worst integrable logarithms; at infinity the zero first-order trace yields O(s^−2).

Every integrand is nonnegative, and if X!=tau then M_s!=I for every s, so every integrand is strictly positive. Therefore X<=3EX implies Delta(X)>=0 in EVERY finite reference dimension, with equality exactly X=EX. Singular sources and singular original reference marginals are covered by actual-support restriction and the same convergent integral. No claim beyond relative peak three is implied.

The canonical PPT corollary is also received: for X^{T_A}>=0, CP positivity gives N(X^{T_A})=(3EX−X)/2>=0. Every separable source is PPT by termwise transposition. Thus all PPT and separable sources are included; reduction-violating inputs are not. The singular regularization by X_t=tX+(1−t)tau is valid: each individual Bregman integrand is convex in t, has its minimum at zero, and increases for t>=0, so its nonnegative integral passes to the endpoint. The entropy difference is then the difference of two finite received integrals.
