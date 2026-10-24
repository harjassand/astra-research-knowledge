# Independent root check: exact qubit mutual-information coefficient

24 October 2026, 14:47 UTC. Worker supplied the dephasing-split construction; root independently checked the identities below. Historical priority and external review remain unresolved.

Claim for D_lambda(rho)=lambda rho+(1-lambda)I/2, 0<=lambda<=1:
eta_MI(D_lambda)=2lambda^2/(1+lambda), with arbitrary finite quantum reference.
This is distinct from eta_complete=eta_conditional=3lambda^2/(1+2lambda).

Choose the physical-qubit basis diagonalizing rho_A. Let Delta be dephasing of A in that basis, acting trivially on R. Since Delta preserves rho_A and rho_R, entropy orthogonality gives exactly
I(A:R)_rho=I(A:R)_(Delta rho)+D(rho||Delta rho).
The same identity holds at the output: D_lambda is basis covariant, commutes with Delta, and leaves rho_A diagonal in this basis.

The diagonal cq part is acted on by the binary uniform-reset channel K_(lambda,2). Its complete Umegaki coefficient is lambda^2. Apply this to the same-reference pair Delta rho and rho_A tensor rho_R. Their output relative entropy is precisely the output diagonal mutual information. Therefore
I(A:R)_(D_lambda Delta rho)<=lambda^2 I(A:R)_(Delta rho).

Put k=(1+lambda)/2, theta=lambda/k, and Gamma_theta=theta id+(1-theta)Delta. Let X swap the two diagonal basis vectors. Direct block calculation gives
D_lambda rho=k Gamma_theta rho+(1-k)X Delta(rho) X,
Delta D_lambda rho=k Delta rho+(1-k)X Delta(rho) X.
Joint convexity of relative entropy consequently bounds output coherence by
D(D_lambda rho || Delta D_lambda rho)<=k D(Gamma_theta rho || Delta rho).
The two-sector pinching contraction theorem, with conditional expectation Delta, gives
D(Gamma_theta rho || Delta rho)<=theta^2 D(rho||Delta rho).
Here the conditioning terms vanish because Delta Gamma_theta rho=Delta rho. No commutativity of reference blocks is assumed.

Thus output MI is at most lambda^2 times input diagonal MI plus (lambda^2/k) times input coherence. Both summands are nonnegative, and lambda^2<=lambda^2/k. This gives the claimed upper lambda^2/k for every rho and every finite reference dimension.

The product-baseline weak-correlation family in mi_product_baseline_obstruction.md approaches this value: biased physical marginal, increasingly rare quantum-reference sector, then small off-diagonal perturbation, in that order. It supplies the matching lower bound with a reference qubit. Rank-deficient cases follow by finite-dimensional regularization and entropy continuity; endpoints lambda=0,1 are direct.

At lambda=1/2 the full hierarchy is therefore ordinary coefficient 1/4, quantum-reference MI coefficient 1/3, equal-reference complete coefficient 3/8, and conditional coefficient 3/8. For 0<lambda<1 the latter gap is lambda^2(1-lambda)/[(1+lambda)(1+2lambda)]>0.

This closes both comparisons for qubit depolarization in HGWN26 Eq3.66: equality between complete and conditional, strict inequality between either and single-ensemble MI. It does not settle arbitrary quantum channels or assert a finite experimentally economical maximizer. The achieving limits can have negligible absolute information. The actual finite rational MI witness is recorded separately.
