# A genuine temporal jump-record mixing consequence

This note assumes the separately derived coefficient-norm contraction for the full-qubit guarded-drive/damping model. It derives an explicit, size-independent mixing estimate for finite-window jump-record events, including conditioning on arbitrary earlier records. It does **not** derive a same-window spatial product-fault law.

## Assumption and notation

Expand observables in tensor products of {I,n,sigma+,sigma-}. For A=sum_a c_a B_a, write

 F(A)=sum_{a != identity}|c_a|,
 W(A)=sum_{a != identity}|support(a)| |c_a|,
 ||A||_c=|c_identity|+F(A).

Each basis string has operator norm <=1. Let h=C(D)g, where the crude Hamiltonian column-sum constant C(D)=2^(D+2)(D+1) suffices, and assume lambda=kappa/2-h>0. For T_s=exp(s L*) the coefficient argument gives

 d^+F(T_s A)/ds <= -lambda W(T_s A),
 F(T_s A)<=exp(-lambda s)F(A),
 |d c_identity(T_s A)/ds|<=h W(T_s A).

The Hamiltonian column bound h|support| counts ALL output coefficients, including identity, while reset contributes negative diagonal coefficient at least kappa|support|/2. Therefore the FULL coefficient matrix has logarithmic l1 norm <=0 (its identity column is zero), giving

 ||T_s A||_c <= ||A||_c.                                (0)

This independently checks the parent worker's improvement: no scalar-leakage prefactor is necessary. For uniform notation below set M=1. Quotient contraction remains exponential, whereas full contraction is merely nonexpansive because I is fixed.

## Jump instruments on a monitored set

For one monitored site x, the jump adjoint J_x*(A)=kappa sigma+_x A sigma-_x has the following local basis action:

 I -> kappa n,   n ->0,   sigma+ ->0,   sigma- ->0.

Consequently ||J_x*||_{c->c}<=kappa exactly. Let R be r monitored sites, J_R*=sum_{x in R}J_x*, and K_R*=L*-J_R*. K_R is the generator conditioned on no emissions in R, while all other site emissions remain unobserved.

Dyson expansion as a bounded perturbation of T gives

 ||exp(s K_R*)||_{c->c} <= M exp(M kappa r s).

Signs in this Dyson expansion need not preserve coefficient positivity; the estimate uses absolute norms and is valid regardless.

For a specified ordered sequence of n monitored emissions at specified sites and times in a window of duration a, the dual event instrument is a product of n jump adjoints and n+1 killed semigroups. Its coefficient norm, applied to I, is at most

 M^(n+1) kappa^n exp(M kappa r a).

Integrating over ordered times contributes a^n/n!, and summing over site labels contributes r^n. Therefore any measurable cylinder event B of the monitored jump record in that window has an effect E_B, 0<=E_B<=I, satisfying

 ||E_B||_c <= M exp(2 M kappa r a).                    (1)

The same estimate applies to arbitrary measurable events obtained as limits of cylinder events: each effect is the absolutely convergent sum/integral of its selected trajectories, bounded by the sum of absolute norms over ALL trajectories. In finite volume the monitored count is nonexplosive because its intensity is <=kappa r. No independence or renewal assumption is used.

The estimate is intentionally crude. In particular, for an all-no-emissions event no jump insertions are needed and the sharper bound M exp(M kappa r a) suffices.

## Uniform mixing of future local records

Let A be any positive-probability event determined by the entire jump history up to time u. The conditional clock state rho_A(u) can be arbitrary. Let B concern r monitored sites in the future interval [u+s,u+s+a]. Its effect is T_s(E_B). For ANY two states rho,tau at time u,

 |Tr[(rho-tau)T_s(E_B)]|
 <=2 F(E_B)exp(-lambda s)
 <=2M exp(2M kappa r a-lambda s).                     (2)

Thus

 |P(B|A)-P(B)| <= min{1,2M exp(2M kappa r a-lambda s)}. (3)

This is a genuine, uniform temporal record-mixing estimate with constants independent of the total graph size, even when A involves arbitrarily many sites. The future window has a fixed monitored region and duration. It is stronger than an unconditioned two-point observable covariance estimate: rare past events and arbitrary post-selected past states are allowed.

If sigma is the unique finite-volume stationary state, the same bound compares P(B|A) with the stationary window probability p_B. For multiple chronologically disjoint windows B_1,...,B_m separated by gaps s_j, define epsilon_j=2M exp(2M kappa r_j a_j-lambda s_j). The chain rule gives

 P(intersection_j B_j)
 <=P(B_1) product_{j=2}^m min{1,p_{B_j}+epsilon_j}.

A corresponding lower bound uses max{0,p_{B_j}-epsilon_j}. These are explicit joint **temporal** bounds for arbitrary local record patterns, not just one-site waiting times.

## Precisely what remains open

1. The coefficient estimate (1) grows exponentially in monitored volume and window duration. It is not a small-fault estimate.
2. Conditioning on simultaneous/future failures at distant sites is not covered by (3); those events are not in the past sigma-algebra at time u.
3. This result does not show P(all chosen same-window sites fail)<=p^number-of-sites.
4. Spatial clustering could be sought by combining local forgetting with a rigorously localized record instrument and a product initial state. Additive pairwise/cylinder approximation errors alone still do not give a threshold-compatible all-orders product bound.
5. A promising stronger target is an extensive killed-semigroup estimate for arbitrary marked set R, ||exp(t K_R*)I|| <= exp(a|R|-b|R|t). Neither ordinary mixing nor the argument here proves this.
