# Size-uniform local emission progress: constructive existence

For fixed maximum degree D and g,kappa,t>0 there IS a strictly positive lower bound, independent of graph size and arbitrary initial clock density matrix, on at least one emission at a specified site by time t. The bound below is constructive by a terminating finite certificate search, not an efficient closed-form estimate. No mixing or spectral-gap hypothesis is used.

## Stronger spin model

Work first on the full qubit tensor product, with n_z=|1><1|, G_z=product_{y~z}(1-n_y), H_z=g G_z X_z and jumps sqrt(kappa) sigma^-_z. The independent-set subspace is invariant and restriction is exactly the requested model. Proving the claim for ALL full-qubit initial states is stronger and avoids complications in graph/state compactness.

Let L* be the Heisenberg Lindbladian. Define

 A_G(delta)=kappa integral_0^delta exp(s L*)(n_x) ds.

Its expectation is E[N_x(delta)]. Since the stochastic intensity at x is at most kappa, conditioning at the first x event gives E[N_x(delta)] <= (1+kappa delta) Pr(N_x(delta)>=1). Thus any lower bound on A_G gives the desired event bound, divided by 1+kappa delta. This is an event-probability statement, not merely a stationary mean.

## Local no-dark-trajectory lemma

Suppose a state trajectory has <n_x>_s=0 for every s in a nonempty open time interval. Positivity implies support in Q=1-n_x. Direct block compression gives

 Q (L*)^2(n_x) Q = 2 g^2 G_x Q.

Indeed L*(n_x)=i[H_x,n_x]-kappa n_x. All H_z with z!=x commute with n_x; their action preserves x-off-diagonal blocks. All dissipators also preserve that off-diagonal block sector. Only applying H_x twice contributes surviving curvature. Since the second derivative of <n_x> is zero, <G_x>=0 throughout the interval.

Let Pi_m project onto exactly m occupied neighbors of x, and P_k=sum_{m=0}^k Pi_m. P_0=G_x and P_d=I for d=degree(x). One has exactly

 D*(P_k)=kappa (k+1) Pi_{k+1}.

If <P_k>=0, positivity/Cauchy-Schwarz implies <[H,P_k]>=0 (only finitely many local H terms matter). Consequently the first derivative identity forces <Pi_{k+1}>=0, and hence <P_{k+1}>=0. Induction reaches <I>=0, contradiction. For d=0 the initial G_x=I already contradicts zero expectation.

Every identity involves bounded finite-support observables and is equally valid in infinite bounded-degree graphs. In particular, no finite or infinite graph/state can have <A_G(delta)>=0 for delta>0.

## Explicit local Taylor control

Use the intentionally loose constant

 C=2(g+kappa)(D+2)(D+1),  delta=min(t,1/(4C)), q=C delta<=1/4.

For a norm-one observable initially supported at x, each nonzero nested generator term intersects the existing support. Each site meets at most D+1 Hamiltonian stars and one dissipator. Each term has superoperator norm at most 2(g+kappa); after j terms the support has at most 1+jD sites. Therefore

 ||(L*)^k(n_x)|| <= C^k k!.

The Taylor expansion converges absolutely for s<1/C, uniformly in graph size. Its remainder after degree m is at most (Cs)^(m+1)/(1-Cs). If B_R(x) is the induced ball with R=2m+2, full and truncated graph expansions agree through degree m: a Hamiltonian star can enlarge graph-distance support by at most two per application, and all guards relevant to these orders lie strictly inside the ball. Hence, after identifying operators on the ball,

 ||A_G(delta)-A_{B_R}(delta)|| <= epsilon_m,
 epsilon_m=2 kappa delta q^(m+1)/(1-q).

This deliberately overestimates the integrated remainder.

## Uniform positivity, without a gap

If inf_{finite rooted degree-D G} lambda_min(A_G(delta)) were zero, choose graphs and states with expectations tending to zero. Bounded degree gives a subsequence of rooted graphs whose every finite-radius ball stabilizes up to rooted isomorphism. Compactness of finite-dimensional reduced states and a diagonal subsequence give a consistent state on the resulting finite/infinite rooted graph. The uniform Taylor locality estimate passes the expectation of A to the limit, which is zero. Positivity of n_x and continuity then imply <n_x>_s=0 throughout (0,delta), contradicting the local lemma. Thus the infimum a_*(D,g,kappa,delta) is strictly positive.

## A terminating, finite algorithm for c

For m=0,1,2,...:

1. Set R=2m+2. Enumerate, up to rooted isomorphism, all finite connected rooted graphs of maximum degree <=D and radius <=R. This is a finite set with an explicit degree/radius vertex bound.
2. For each graph compute/certify a lower bound for the minimum eigenvalue of A_G(delta), using its finite Lindblad matrix exponential/integral and interval arithmetic. Let a_R be the minimum of these eigenvalues (or certified lower approximations with error tending to zero).
3. Stop when a_R>epsilon_m. Output

 c=(a_R-epsilon_m)/(1+kappa delta)>0.

Every finite full graph's induced R-ball occurs in the enumeration, so the local Taylor estimate proves the bound. Termination follows from a_R>=a_*>0 and epsilon_m->0. With approximate eigenvalues use errors <=2^-m, say, and strict certified inequality. Computability assumes g,kappa,t are supplied as computable positive reals; rational inputs are sufficient. The algorithm is astronomically expensive and does not claim an engineering-useful rate.

## Boundaries

The argument permits arbitrary initial states, including states entangled with a reference after taking their reduced clock state. It proves marginal progress uniformly after arbitrary histories, since a conditioned clock state is again an arbitrary density matrix. This yields exponential tails for a SINGLE site's waiting time by block iteration. It does NOT alone yield a spatial joint-fault law, independence, a threshold theorem, or a robust noisy implementation.
