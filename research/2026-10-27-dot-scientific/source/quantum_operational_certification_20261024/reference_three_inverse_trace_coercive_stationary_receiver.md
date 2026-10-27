# Reference-three inverse-trace target: complete singular-boundary exclusion

27 October2026. Exact extension of reference_two_inverse_trace_boundary_and_stationarity.md. This receives minimum attainment and constrained stationarity for the original3×3 inverse-trace problem; it does not establish its sign.

Let C={M:0≤M≤2I9, EM=I9}, Y=NM, and for faithful M define

R(M)=TrM^(-1)−2TrY^(-1)+9.

Then R tends to +infinity along every faithful sequence in C approaching a singular source. Consequently its global minimum is attained with both M and Y faithful. Any hypothetical negative minimizer obeys

M^(-2)+(Y^(-2))^(T_A)=I3⊗Λ+S,
S≥0, S(2I−M)=0,
EM=I, 0<M≤2I.

The actual upper-face normal is retained; the lower face is excluded by the boundary proof below.

## 1. Schmidt-rank thresholds for output kernels (any finite reference)

Suppose0≤M≤kI, EM=I, and ψ∈kerNM has Schmidt rank r∈{1,2,3}. Compress the source to ψ's reference Schmidt support S, of dimension r. Its partial trace is still3I_S. The positive Qψ=N*(Pψ) has kernel dimension r(r+1)/2 on C3⊗S: in Schmidt coordinates its kernel consists of |ii> and the pair vectors

[sqrt(r_i)|ij>+sqrt(r_j)|ji>]/sqrt(r_i+r_j), i<j.

There is no kernel in the complementary physical subspace over S. Positivity forces the compressed M_S to be supported on this kernel. Therefore

3r=TrM_S≤k·r(r+1)/2,

and necessarily k≥6/(r+1).

In particular, at k=2 there are no product output-kernel vectors. If r=2, equality in the trace/rank bound forces M_S=2P_kerQψ. Its marginal forces the two Schmidt coefficients equal. Hence M_S is exactly2P_sym,2 in its physical-two/reference-two Schmidt block, with zero on the remaining physical line.

Because the S-corner of M/2 is a projection, positivity of M and2I−M kills all cross blocks between C3⊗S and its reference complement. Thus this rank-two-kernel block is REDUCING, not merely a compression. The remaining source still satisfies the same effect and marginal bounds. This lemma is valid in every reference dimension.

## 2. Every singular output in3×3 has a simple kernel

If kerY had dimension at least two, choose two independent coefficient matrices for its vectors. Either one is already singular, or the determinant polynomial of their linear pencil has a complex root. Thus their span contains a nonzero vector of Schmidt rank at most two. Rank one is excluded by Section1, so a rank-two kernel vector exists.

The reducing-block lemma then splits M as2P_sym,2 plus a source on the remaining one-dimensional reference. The first output has exactly one zero eigenvalue. On the reference-one remainder, TrM_rest=3 and M_rest≤2I3 imply

N(M_rest)=(3I3−M_rest^T)/2≥I3/2.

Thus the whole output kernel is exactly one-dimensional, a contradiction. Therefore every singular Y in this3×3 region has a simple kernel.

## 3. Uniform entanglement of a full-Schmidt zero vector

Let ψ be a full-Schmidt kernel vector with weights r1,r2,r3>0, sum1. Then Qψ=N*(Pψ) has three positive eigenvalues

q_i=(1−r_i)/2,

and M is supported on its six-dimensional kernel. Since M≤2I,

M≤2P_kerQψ.

Taking the partial trace and examining reference coordinate j gives

3≤2[1+sum_(i≠j) r_i/(r_i+r_j)].                  (1)

Let a=max r_i, with remaining weights b,c. Concavity of x/(a+x) at fixed a yields

b/(a+b)+c/(a+c)≤2(1−a)/(1+a).

Equation(1) requires the left side to be at least1/2, so a≤3/5. Hence every q_i≥1/5. Consequently

(Tr sqrt(Qψ))²=1+2sum_(i<j)sqrt(q_iq_j)≥11/5>2.  (2)

If the unique kernel vector has Schmidt rank two, Section1 instead gives positive Qψ eigenvalues1/2,1/4,1/4, whose squared square-root sum is3/2+sqrt2>11/5. Thus the uniform lower bound(2) holds for every possible zero vector here.

## 4. Coercivity along arbitrary singular approaches

Let faithful M_j∈C converge to singular M0. If Y0=NM0 is faithful, R(M_j) tends to infinity directly. Otherwise Y0 has a simple zero eigenvalue by Section2. Let y_j be the smallest eigenvalue of Y_j and ψ_j its eigenvector. Its projector converges to the unique zero-vector projector of Y0. Set Q_j=N*(Pψ_j).

The exact Hilbert–Schmidt Cauchy estimate is

TrM_j^(-1)≥(Tr sqrt(Q_j))²/Tr(M_jQ_j)
 =(Tr sqrt(Q_j))²/y_j.

The coefficient tends to at least11/5 by Section3, while all other output inverse eigenvalues remain bounded because the limiting zero is simple. Therefore

R(M_j)≥[(Tr sqrt(Q_j))²−2]/y_j−O(1)→+∞.

This handles arbitrary eigenvalue rates and moving eigenvectors. It does not infer coercivity from kernel counts alone.

## 5. Constrained stationary receiving

The set C is compact, contains the strictly feasible point I9, and R(I9)=0. Boundary coercivity excludes singular accumulation points of a minimizing sequence, so a finite global minimum is attained faithfully. Its first derivative is

G=−M^(-2)+2N(Y^(-2)).

The marginal equality and the upper semidefinite constraint give G+I⊗Λ0+S=0, with S≥0 and S(2I−M)=0. Using2N(Z)=3E(Z)−Z^(T_A) and absorbing reference-only terms gives the displayed stationary equation. No sign or rank assumption on the upper-face normal is added.

This is the concrete next interface: exclude faithful negative stationary solutions of this system, or exhibit one. The integrated VALUE theorem in reference≤3 does not itself answer this pointwise inverse-trace question.
