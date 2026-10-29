# A literal rational radius for the joint design SDP

30 October2026. Independent reviewer derivation supporting the producer's
existing weak-SDP claim. It is not a new solver or an assertion about the
floating CLARABEL runtime. No source case or solver run is added.

Let q=m-1,p=n-1,t=1-c and use the producer's rational H_i>0. At the constant
release K0=1/m and center a0=t(1/m)1, the lower block of M_i is

`Di=diag(H_i^-1,c,t)`.

The top-to-lower coupling times Di^-1 is `[0,x0,0]`, with
`x0=(1/m)1_q`, whose norm is sqrt(q)/m<1. Its Schur complement is

`S0=c[diag(x0)-x0x0^T]>=c/m^2 I`.

Writing M_i as the block-triangular congruence of diag(S0,Di), the inverse
of that triangular factor has norm at most1+||x0||<2. Therefore the EXACT
rational number

`mu0=(1/4)min{c/m^2,t,1/max_i Tr(H_i)}`

is a lower bound on every lambda_min(M_i(K0,a0)). We used
lambda_min(H_i^-1)>=1/Tr(H_i), valid because H_i is positive definite.
No eigenvalue or unknown condition number is supplied to get this bound.

Eliminate the last output row of K by column stochasticity, and take the
independent variables to be first q rows plus a. If their Euclidean
perturbation norm is nu, then ||Delta K||_F<=sqrt(m)nu and
||Delta a||<=nu. Since ||B_n||=sqrt(n), the offdiagonal top-to-lower
perturbation Z obeys

`||Z||_F<=sqrt[m(n+5)]nu`.

Indeed its three components are Delta D, c Delta x_i and
Delta a-t Delta x_i, bounded by sqrt(mn)nu, sqrt(m)nu and2sqrt(m)nu.
The top diagonal perturbation is bounded by sqrt(m)nu. Consequently

`||Delta M_i|| <=4(m+n)nu`

is a conservative rational Lipschitz bound for all m,n>=2. The literal
interior-ball radius

`rin=min{1/2,(1/m-kappa)/(2m),mu0/[8(m+n)]}`

keeps every lifted block at least mu0/2 positive, every K entry strictly
above its floor, and every center coordinate strictly inside[-2,2]. For
the eliminated last row, |Delta K_mi|<=sqrt(q)nu<=m nu pays the same floor.
The center satisfies |a0_h|<1/m and |Delta a_h|<=1/2.

The whole feasible set lies in a known rational-radius box, for example
Rout=mn+4m about the constant release in these coordinates. All H_i and
their traces have polynomial rational bit length from the exact inverse
of L. Hence log(Rout/rin) is polynomial in the rational input length, even
when its numerical conditioning is poor. Standard affine/block-PSD
conversion has polynomial dimensions and rational metric distortion, so
this is the geometric input required by ordinary weak-SDP optimization.

The controlling PRIMARY complexity theorem is de Klerk--Vallentin,
arXiv:1507.03549v2, Theorem1.1 (attributing the ellipsoid result to
Groetschel--Lovasz--Schrijver): a known rational feasible center and
relative inner/outer radii supply polynomial dependence on their log ratio,
log(1/epsilon) and rational input size for an additive-optimal feasible
rational answer. Its exact arithmetic/rounding assumptions are not a
generic guarantee for a fixed-precision black-box solver.

The mathematical design problem therefore pays a meaningful polynomial
weak-optimization interface. Exact optimum rationality is neither required
nor asserted. The executed primal/dual receiver remains a separate exact
certificate for its supplied proposal.
