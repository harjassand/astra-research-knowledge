# Independent audit: adaptive pure-state estimator, known-center part

28 October 2026. This receives only the ideal known-center mathematical interface in sections 1–3 of `ordinary_adaptive_pure_matrix_query_20261028.md` as read at 07:17 UTC. It does NOT receive coarse-center acquisition, finite Haar/QR compilation, the imported random-purification channel, or the full mixed-state result. The author is still completing that ledger. No earlier frozen proof changes.

## Finding

The measurement moments, binomial reciprocal estimates, mean bias and covariance constants 24/80 are sound for q>=3/4, m>=2 and l>=m. The same Bernoulli K must be used for t and h, and the same vector records for zhat and Khat, as the author specifies. The estimator is Hermitian but need not be positive or trace one.

## Independent finite binomial verification

Let s=1-q, K~Bin(l,q), t=K/l, h=(l+1)/(K+1), R=h-1/q+(t-q)/q^2. Integration of the binomial generating polynomial gives

    E h=(1-s^(l+1))/q.

For j>=1 and B~Bin(N,q), the beta integral gives

    E[1/((B+1)...(B+j))]
       <= N!/[q^j (N+j)!].

Together with the author's elementary reciprocal denominator inequalities, this yields

    E h^2<=2/q^2,
    Var h<=6s(l+1)/[q^3(l+2)(l+3)]<=32/(9l),
    Var(ANOVA orders >=2 of h)
       <=40s^2(l+1)/[q^4(l+2)(l+3)(l+4)]
       <=(640/81)/l^2<8/l^2.

The MSE E(h-1/q)^2 includes squared bias s^(2l+2)/q^2, and is below 4/l. Differentiating the exact E h formula gives the first-order ANOVA coefficient

    l E Delta h=-1/q^2+s^l(lq+1)/q^2.

Hence R's remaining first-order variance is

    s^(2l+1)(lq+1)^2/(l q^3).

For fixed l>=2, both this quantity and the squared bias decrease with q on [3/4,1]. Their l^2-scaled maxima at q=3/4 are respectively

    l(3l+4)^2/(27*16^l),     l^2/(9*16^l).

Both decrease with integer l>=2; at l=2 they equal 25/864 and 1/576, each <1/16. Thus E R^2< (8+1/8)/l^2 <9/l^2. These are finite inequalities, not Taylor expansions.

## Independent covariance accounting

The effective one-record density is |sqrt(q)+sqrt(d)v*b|^2 on the complex d-sphere. Its moments are

    E w=z=sqrt(q)b,
    E ww*=qI+d/(d+1)[(1-q)I+bb*],
    E ww^T=0.

For xi=w-z, let Sigma=E xi xi*, Pi=E xi xi^T=-zz^T. In particular Sigma<=2I. For Hermitian O=[[alpha,c*],[c,B]], put b0=z*Bz and r=Tr(P O^2). The vector

    chi=(1/sqrt(q), -b/q)

has norm squared 1/q^2 and Re<psi|O|chi>=alpha-b0/q^2. Thus A^2<=r/q^2. The shared-K contribution obeys

    Var_K(alpha t+b0h)
      <= (2/3)r/m+(162/256)Tr(B^2)/m^2.

The linear vector contribution uses v0=c+Bz/q, q||v0||^2<=r and ||Bz||^2<=qs Tr(B^2), giving

    E_K Var_w[2Re((c+hBz)*delta_z)]
      <= (64/3)r/m+12Tr(B^2)/m^2.

The degenerate pair term is orthogonal to the linear vector term even with nonzero pseudocovariance. Its contribution is at most 64Tr(B^2)/m^2. Summing gives strictly less than

    24 r/m+80 Tr(O^2)/m^2.

When O annihilates psi, r=0 and only the n^-2-scale term remains. This cancellation holds for the actual coupled estimator, not for separately estimated blocks.

The only ideal mean error is the bottom block -s^(l+1)zz*/q, with trace norm s^(l+2). The attached independent check uses exact rational binomial sums and, separately, a real-coordinate covariance representation for complex vector records. It does not reuse the author's covariance routine or sample a proposed hardware circuit.

## Explicit remaining scope

A finite receiver theorem additionally needs a paid coarse center, all-history output bound, finite random-unitary arithmetic/compilation, and the stated mixed-state interface checked independently. This note makes no global encoder acquisition, free matrix oracle, physical-PSD estimator, or conventional separation claim.
