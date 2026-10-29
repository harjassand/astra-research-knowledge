# Higher-moment freedom does not remove canonical phase-overlap cost

## 1. Exact physical input and result

Use M sites, exactly K=M bosons of EACH of two flavors, and the stable diagonal Hamiltonian

`H=U sum_i(n_bi-n_ci)^2`, with `t=beta U=4`.

There is no artificial local occupation cap. The only bound n_i<=K is forced by the actual canonical particle counts. The ordinary positive occupation dynamic program solves this diagonal model. Our result is not a simulation-hardness theorem: it tests an entire proposed representation lever before spending effort optimizing it on a frustrated model.

Let C_K be the M-compositions of K, D=|C_K|=binom(K+M-1,K), and

`h_K(z)=sum_(alpha in C_K) z^alpha`, `W(z)=|h_K(z)|^2`.

Each phase z_i lies on the unit circle. A site law may be discrete, continuous, or mixed and may differ from all the other site laws. Assume independence and the native HS moments

`E z_i^j = exp(-4j^2)` for every integer |j|<=K.

All moments beyond this band are completely unrestricted except for being moments of a probability law. In particular this includes EVERY positive finite quadrature exact on the physical K,K sector, not just a chosen Gaussian or a chosen K+1-atom rule.

**Site theorem.** If M is a multiple of32 and M>=64, then

`Var(W)/(E W)^2 >= (5/4)^M/(2M+1) - 2(8/25)^M - 1`.       (1)

Thus even globally optimizing all the unused one-site moments cannot give polynomial fixed-relative-RMSE DIRECT iid averaging at fixed density. It also cannot give a polynomial constant-envelope rejection sampler based on this product proposal; section 7 gives that implication.

We prove a stronger finite-range version. Partition the sites into equal B-site blocks. The blocks are independent; within a block use ANY joint positive phase law whose required Fourier moments match the physical interaction. Take R=64B, M a multiple of R, and M>=16R. Then

`Var(W)/(E W)^2 >= (5/4)^M/(2M+1) - 2(4/5)^M - 1`.       (2)

The block theorem allows arbitrary internal correlations and arbitrary unused block moments. Its large threshold is a conservative proof cost. It is a fixed-B, all-size obstruction, not a bound for blocks growing with M, a posterior field-MCMC law, importance reweighting, or a conditionally integrated estimator.

## 2. The mean is fixed by the physical moment band

For every admitted law,

`mu := E W = sum_(alpha,beta in C_K) exp[-4||alpha-beta||^2]`.

Every frequency alpha_i-beta_i lies between -K and K, so no unused moment enters. It is exactly the physical canonical partition. In particular

`D <= mu <= D Theta(4)^M`,

where Theta(t)=sum_(j in Z)exp(-t j^2). The lower bound keeps alpha=beta. For the upper bound fix alpha and drop the nonnegativity/total-count restriction on beta, enlarging its sum to Z^M.

We will use the elementary bounds e^4>50 and

`Theta(4) <= 1+2 exp(-4)/(1-exp(-12)) < 21/20`.             (3)

Here j^2>=1+3(j-1) for j>=1. The same mean identity holds under block laws matching

`E z_block^q = exp[-4||q||^2]`

whenever |q^+|_1 and |q^-|_1 are both at most K. These are the actual finite-sector Fourier indices. Section 6 shows that exact independent-block HS identities force this matching, up to one harmless common phase, rather than supplying it as a new oracle.

## 3. A central-coefficient lower bound

Write the analytic polynomial F=h_K^2 as

`F(z)=sum_(|s|=2K) r_s z^s`,

where r_s is the number of ordered composition pairs alpha+gamma=s. Thus sum_s r_s=D^2 and

`r_s=[x^K] product_i(1+x+...+x^(s_i))`.

The coefficient sequence of that product is symmetric and unimodal. One direct proof decomposes each symmetric unimodal factor into nonnegative centered interval indicators; convolution of two such indicators is symmetric unimodal, and nonnegative sums preserve the property. The middle coefficient is therefore at least the average of its2K+1 coefficients:

`r_s >= product_i(s_i+1)/(2K+1)`.                          (4)

Now choose a fixed superblock size r dividing M, and restrict alpha and gamma to have exactly r particles in EACH consecutive r-site superblock. There are

`D_r^(M/r)` such alpha, with `D_r=binom(2r-1,r)`.

For independent uniform restricted alpha,gamma,

`Pr(alpha_i=gamma_i=0)=((r-1)/(2r-1))^2 <=1/4`.

Jensen applied to (4) and log(s_i+1)>=log2 whenever s_i>0 gives

`E_restricted r_(alpha+gamma) >=2^(3M/4)/(2K+1)`.

If S is any set of monomials containing these restricted sums, then r_s^restricted<=r_s yields

`sum_(s in S) r_s^2 >= D_r^(2M/r) 2^(3M/4)/(2K+1)`.       (5)

We need only fixed finite combinatorial constants, not a large many-body state. For r=32 the exact integer check

`binom(63,32)^2 100^32 >1323^32`

implies, using D<=4^M, (3), and 2^(3/4)>5/3,

`[sum_(s in S) r_s^2]/[D^2 Theta(4)^(2M)] >=(5/4)^M/(2M+1)`. (6)

For ALL r>=64 the same inequality D_r^2 100^r>1323^r follows even from D_r>=4^r/[2(2r+1)]. Check the latter bound at r64; its ratio improves with r because (131/129)^2<1600/1323. This supplies r=R=64B in the block theorem without a new r-dependent oracle or large enumeration.

## 4. Site laws: isolate the low-frequency core instead of assuming all moments positive

Split F=F0+F1. F0 contains the monomials with s_i<=K at every site. Because two monomials in F0 differ only by frequencies in [-K,K], every term in E|F0|^2 has its fixed nonnegative Gaussian moment. Hence

`E|F0|^2 >=sum_(s in F0) r_s^2`.

Restricted sums from r32 superblocks have every s_i<=64<=K and are included in F0, so (6) applies. Also E|F1|^2>=0 for ANY positive phase law. It remains to control a possibly negative cross term; this is the step that the previous Gaussian-only argument did not pay.

Take s from F0 and t from F1. As |t|=2K, at most one coordinate i has t_i>K. All frequencies s_j-t_j for j!=i lie in [-K,K]. If the remaining frequency at i also lies in that band, the whole moment is nonnegative. Otherwise t_i-s_i>=K+1. The remaining low frequencies sum to at least K+1, so Cauchy gives

`sum_(j!=i)(s_j-t_j)^2 >=(K+1)^2/(M-1)`.

The one unused moment has modulus at most one. Thus every potentially negative cross monomial is at least minus exp[-4(K+1)^2/(M-1)] times its positive coefficient. Their total coefficient mass is at most (sum_s r_s)^2=D^4. Therefore

`E W^2 >=sum_(s in F0)r_s^2 - 2D^4 exp[-4(K+1)^2/(M-1)]`.

Normalize the positive term using mu<=D Theta^M and (6), and the negative term using mu>=D. Since K=M, (K+1)^2/(M-1)>M, D^2<=16^M, and e^4>50, the negative ratio is at most2(8/25)^M. Subtracting one gives (1). No sign condition on an unused moment was invoked.

## 5. Arbitrarily correlated bounded-size block laws

Let each HS block have B sites and align them inside superblocks of size R=64B. Set C=2R and assume M>=16R. Define Fcore using monomials with at most C particles in EACH HS block. The restricted sums of section3 lie in this core, so (6) applies with r=R. All Fourier indices inside E|Fcore|^2 are in the required block moment band, giving its zero-frequency lower bound.

In the cross term against the remainder, any t having at most K particles in every HS block gives only required moments, all nonnegative. Otherwise t has exactly one block A with more than K particles. All other block moments are required. If A's moment is outside the required band, its negative part has at least K+1 particles while its positive part has at most C. Thus its NET negative frequency is at least K+1-C. The frequencies outside A must have net positive sum of that size. Consequently

`||q_outside A||^2 >=(K+1-C)^2/(M-|A|) >=49M/64`.

We used C<=M/8 and |A|<=B. As before the sole unrestricted block moment has modulus at most one. The negative cross budget is at most2D^4 exp(-49M/16), and e^3>20 bounds its normalized ratio by2(4/5)^M. Dropping the nonnegative squared norm of the remainder and applying (6) proves (2).

The block theorem is stated for equal B-site blocks with M divisible by64B. No unequal-block packing or state/phase-transition assumption is imported.

## 6. The moment contract is forced up to a common harmless phase

Suppose a product of at least three block probability laws is an exact unitary-phase HS representation of the SAME diagonal interaction on the whole K,K sector. Its joint Fourier moments must equal exp(-4||q||^2) for every total-zero integer q with |q^+|_1=|q^-|_1<=K. This follows by evaluating the diagonal matrix elements in the actual occupation basis.

For one block's q, with each sign's mass<=K and net charge s, put a compensating charge -s in a different block. This is an allowed global q. Comparing two same-net-charge q choices shows that the ratio of the block moment to exp(-4||q||^2) depends only on s; call it a_A(s). Taking opposite charges in any two blocks gives a_A(s) conjugate(a_B(s))=1. With a third block this forces every a_A(s) to be the same modulus-one number a(s). Three blocks with charges s,t,-s-t, where s,t>=0 and s+t<=K, give a(s+t)=a(s)a(t). Thus

`a_A(s)=exp(i phi s)` for all |s|<=K.

A common phase shift of EVERY site removes this character. It multiplies h_K by a unit phase and leaves W unchanged. Hence exact independent-block phase representations are covered by the theorem after gauge removal; the low-moment match is not an added physical assumption. This necessity does not cover nonunitary factors, complex/signed weights, correlated blocks, or changed estimators.

## 7. Statistical, rejection and finite-precision costs

For S iid field weights, relative mean-square error is exactly Var(W)/(S mu^2). Equations(1)/(2) therefore give exponential DIRECT-sample cost at fixed relative RMSE. They are not fixed-confidence lower bounds for all estimators, nor statements about biased/truncated/adaptive importance methods.

There is a second operational consequence. Any constant-envelope rejection sampler with the admitted product proposal must use C_env>=esssup W. Since E W^2<=C_env mu, its acceptance is at most mu^2/E W^2. Thus its expected base proposals per accepted configuration are at least the exponential second-moment ratio in(1)/(2), EVEN with an optimal envelope. This covers the independent rejection mechanism of the frozen canonical construction; selecting a different finite alphabet alone cannot repair it uniformly.

The obstruction is robust at a paid finite precision. If each required marginal/block moment is within epsilon=2^(-10M) of its target, product telescoping changes the mean by at most M D^2 epsilon. Hence mu_approx is between D/2 and2D Theta^M. The low-core norm and cross estimates incur at most3M D^4 epsilon in total. It follows that the site bound can be weakened to

`Var(W)/mu_approx^2 >=(1/4)(5/4)^M/(2M+1) -8(8/25)^M -12M 2^(-6M)-1`,

and the block version replaces8/25 by4/5. The nearby physical mean's relative error is at most M2^(-8M). Thus an O(M)-bit absolute moment budget suffices to retain the exponential obstruction; it is not an artifact of demanding infinitely precise tiny high moments. This is an input-moment condition, not a claim that arbitrary finite-bit PRNGs implement an ideal probability law.

## 8. What information/operation remains missing

Canonical AFQMC already samples the CORRELATED posterior field law proportional to base_density*W through heat-bath/Metropolis and importance methods (Shen et al.2020, computational-details equations53–54). That ordinary route is outside this theorem. Conditional integration, control variates, cluster/worm methods, and changes to the estimator are outside it as well and must be compared at the same physical ensemble. The diagonal model's ordinary positive occupation DP removes all variance, so no fundamental physics/information barrier has been proved.

The failed lever is precise: a positive polynomial kernel plus optimized unused LOCAL HS moments, even finite-range blocks, is insufficient for a uniformly efficient independent sampler. A useful advance must acquire globally correlated proposals, a paid conditional contraction, or a different estimator/representation. For noncommuting frustrated hopping that operation still has to preserve canonical weights and pay its contraction/mixing cost. No result about it is inferred from the present diagonal discriminator or the previous M9 finite law.
