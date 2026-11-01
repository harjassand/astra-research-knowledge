# Gap-free acquisition by bounded nonlinear projection and corrected outputs

Root constructive draft, 2026-11-01. Pending independent receiving. Built during parallel work with the scalar constructor. This replaces the proposed inverse-Gram linear realization, not the physical source contract. Governing N1515 already supplied noisy bounded-l1 projection, kernel Frank-Wolfe, and failed-successor retention. The proposed distinction is expanded m*aconv(V), nonlinear task-by-task projection, corrected scalar outputs and rank-log acquisition, rather than a globally invariant unit hull or linear intertwiner. Projection, Frank-Wolfe, dual-weighted correction, and determinant potentials are prior mathematical machinery. Novelty and consequential application remain unresolved.

## Source and task

Real Hilbert contractions T_a, ||f||<=1, finite alphabet closed under supplied actual adjoints, fresh bounded binary scalar reports of Gamma(u,v)=<T_u f,T_v f>. Conditional unbiasedness, stationary preparation where used, controls, episodes and bit costs remain charged. Requested output is F(w)=<f,T_w f> for |w|<=H. No general readout, state, conditional record law or planner is supplied.

Dictionary V consists only of actual descriptors, including f. At size m, put B=m and K_m={Vc: ||c||_1<=B}. This is a symmetric convex subset of the physical Hilbert space, not an assumed coordinate representation. It need not approximate every reachable state before future tasks arrive. No physical superposition preparation is required: combinations are mathematical calculations of measured scalar means.

Set lambda=epsilon/(128 H^4). At precision epoch b=nextpower2(m), acquire/cache all needed G=V*V, K_a=V*T_a V, H_a=(T_a V)*(T_a V) entries to absolute accuracy

 alpha=lambda/[128(b+4)b²].

All statements below are on their simultaneous confidence event. Use the same accuracy for prefix self/cross returns. Finite family/confidence allocation and permanent failure latch follow the earlier scalar receiver, but its inverse-Gram model is not reused.

## A finite convex operation instead of Gram inversion

Given previous coefficient d, ||d||_1<=B, choose c with ||c||_1<=B approximately minimizing

 qbar(c)=c*Gbar c-2c*Khat_a d+d*Hhat_a d,
 Gbar=Ghat+m alpha I.

Gbar is PSD because ||Ghat-G||<=m alpha. Stop with certified convex Frank-Wolfe gap at most delta=B² alpha. The constant target term need not enter optimization. No positive Gram eigenvalue is required.

On the coefficient ball, qbar differs from true ||T_a Vd-Vc||² by at most (m+4)B² alpha. More sharply, the nonconstant part differs by at most (m+3)B² alpha. Hence the chosen physical vector lies within

 zeta=sqrt((2m+7)B² alpha)<=sqrt(lambda)/8

of the exact metric projection P_K(T_a Vd). This follows from the squared-distance projection inequality, not coefficient conditioning. Different coefficients may represent the same vector without harming the argument.

Start y_0=f, c_0=e_seed and iterate this operation along w. Independently compute dual modeled states b_j along reverse-adjoint labels a_l*,...,a_1*, starting at f. All coefficients stay in the bounded ball. There is no B^H operator multiplication or assumed exact linear reduced model.

## Corrected output and an executable certificate

Let r_i=T_(a_i)y_(i-1)-y_i; let s_j be the analogous dual residual. Each residual squared is a quadratic form of G,K,H with total coefficient weight at most4B². Thus

 R_i²=estimated ||r_i||²+4B² alpha

is an upper bound, exceeding true squared norm by at most8B² alpha. Likewise define S_j. Negative radicands on a bad-data event trigger failure, not acceptance.

Return the corrected scalar estimate

 Fhat_corr=estimated [<f,y_l>+sum_(i=1)^l <b_(l-i),r_i>].

Each correction is c_b*(K_a c_prev-G c_next). This is computable from retained scalar means; it is not a hidden residual-vector oracle. Its cumulative statistical error is at most

 D=(B+2l B²)alpha.

The exact forward Duhamel identity, with the actual backward suffix replaced by its separately modeled counterpart, gives

 |F(w)-Fhat_corr| <= D+sum_(i=1)^l R_i sum_(j=1)^(l-i) S_j.  (1)

This identity does NOT need Galerkin orthogonality, an interior-polytope margin, or an exact reduced contraction. The scalar correction explicitly pays the in-span residual pairing. Output clipping to[-1,1] cannot increase error.

Use rational upper square roots with additive tolerance eta=epsilon/[128 H²(B+1)]. Since physical model vectors have norm<=B, each true residual norm<=2B, and each exact upper norm<=3B. Product-sum rounding excess is <=3H²B eta+(H²/2)eta²<epsilon/32. Accept only when the computed upper certificate is <=epsilon. The empty word uses its directly acquired scalar return.

## Rejection supplies a real new descriptor

Suppose every actual forward and reverse-adjoint prefix of the requested word lies within sqrt(lambda) of K_m. Metric projection is nonexpansive, and approximate projection adds at most zeta. Therefore

 ||y_i-x_i|| <= i(sqrt(lambda)+zeta),
 ||r_i|| <=(2i-1)(sqrt(lambda)+zeta).

The residual confidence inflation contributes at most sqrt(8B² alpha)<=sqrt(lambda)/8, so R_i<=3i sqrt(lambda), and S_j<=3j sqrt(lambda). Thus the product sum in(1) is at most

 (9/24)l(l-1)(l+1)(l+2)lambda <=(3/4)H^4 lambda.

Together with D and rounding, the computed certificate is below epsilon/4. A rejected task therefore has an actual forward or reverse-adjoint prefix x with dist(x,K_m)²>lambda.

Find one by scanning ONLY those at most2H prefixes. For each, acquire its norm and cross returns with V, solve the same bounded convex distance problem, and form a lower bound

 L=qbar(c)-FW_gap-U,
 U=(m+4)B² alpha<=lambda/128.

Here the target is x, so its coefficient mass is1, not B; the displayed U is conservative. The true distance squared lies above L, while L>=dist(x,K_m)²-2U-delta>dist²-lambda/32. Hence some prefix will have L>lambda/2. Retain only such a certified prefix. If none is found, latch failure. Existing dictionary descriptors have distance0 and cannot be accepted on the confidence event.

## Lifetime progress, without measuring ridge inverses

Define analytic ridge residual leverage

 ell_lambda(x)=min_c {||x-Vc||²+lambda||c||²}.

This is used only in the proof, never evaluated by the algorithm. If ell_lambda(x)<=lambda/2, the minimizing coefficient has l2 norm<=1/sqrt(2), hence l1 norm<=sqrt(m/2)<=B, and dist(x,K_m)²<=ell_lambda(x)<=lambda/2. Therefore every accepted prefix has ell_lambda(x)>lambda/2.

The determinant potential logdet(I+V*V/lambda) increases by more than log(3/2) per retained prefix. If the reachable length<=H feature family is within nu<=sqrt(lambda)/4 of an unknown r-dimensional subspace, then at dictionary size m

 logdet(I+V*V/lambda)<=r log(1+m/(r lambda))+m/16.

Consequently m=O(r log(1/lambda)) for r>=1 (with seed/additive constants handled separately). No rank, basis, gap or optimal spanner is supplied to the learner. The conservative proposed ceiling 1+ceil(64r log(8/lambda)) is under independent review before publication.

## Costs and finite implementation obligations

Precision-epoch caching gives O((k+H)m²) distinct mean jobs over acquisition, up to logarithmic epoch factors and with actual matrix symmetries counted. Each binary mean uses O(alpha^-2 log(confidence^-1)) reports. Since alpha^-2=O(b^6 lambda^-2), a conservative sufficient total is O((k+H)M^8 lambda^-2 log(confidence^-1)), plus epoch bookkeeping. This changes the accuracy factor to epsilon^-2 up to logarithms, at fixed H and rank, rather than epsilon^-4/epsilon^-8 from uniform inverse-Gram control. It does not make the polynomial constants practical by itself.

Each report's chronological control word, preparation, and readout is charged. Accepted future predictions still cost finite small-model work; they do not call the source. Failed tasks pay at most2H prefix scans and the next precision epoch. The output correction uses O(H) bilinear forms, not an exponential word search.

A finite rational solver can use the l1-ball vertex minimizing the exact empirical gradient as the linear minimization oracle. Bound curvature conservatively by C=16mB², use a fixed rational step theta=min(1,delta/C) whenever the certified FW gap exceeds delta, and exploit objective decrease at least delta²/(2C). The bounded objective range gives a deterministic polynomial iteration ceiling. Fixed rational steps grow bit height linearly in iteration count, avoiding an unproved exact-line-search bit-cost claim. Exact PSD verification and an explicit cap/failure latch are required off the confidence event. These finite arithmetic constants and unconditional expected-acquisition closure have not yet received independent review or code execution.

## Scientific status

This is a new proposed construction within the same scalar experimental interface. It attacks a decisive bottleneck: acquiring bounded nonlinear predictive operations instead of accurately inverting an ill-conditioned hidden Gram matrix. It is not a new physical platform, practical cost advantage, full observable-law simulator, efficient planner or civilisation breakthrough. Strong existing convex projection, kernel approximation, active automata and goal-oriented reduced-model methods must receive the same source access and retention rights in comparisons.
