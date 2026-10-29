# A matched ordinary positive calculation on the same input

The all-phase barrier does not imply that the physical model is difficult. This file gives the actual positive conditional operation used for comparison, on the SAME zero-hopping, M=K=64, t=beta U=4 canonical model.

For occupations alpha,beta of total K let d=alpha-beta, with positive mass p=sum d_i^+, negative mass n=sum d_i^- and energy E=sum d_i^2. Canonical equality forces p=n. Every pair with this difference is uniquely

`alpha=d^++r`, `beta=d^-+r`, with `sum_i r_i=K-p`.

There are binom(K-p+M-1,M-1) such r. Let N_M(p,n,E) count integer M-vectors with these three statistics. The exact partition function is

`Z=sum_(p,E) N_M(p,p,E) binom(K-p+M-1,M-1) q^E`, q=exp(-4).

N_M is acquired by a positive integer sitewise DP. A coordinate d=0 leaves all statistics unchanged; d>0 increments p by d and E by d^2; d<0 increments n by |d| and E by d^2. This is ordinary occupation/conditional integration, not a new general many-body method.

For an energy truncation H, retain all E<=H and bound the omitted partition by

`tail_Z <=D^2 q_upper^(H+1)`, D=binom(K+M-1,K).

Since Z>=D, the relative tail is at most D q_upper^(H+1). Thus H=O(log D+log(1/epsilon)) at fixed t. There is no imposed local occupation cap: the omitted physical states are included through a rigorous tail. Positive Taylor bounds for exp4 yield rational q_lower and q_upper, and all retained coefficients are exact integers. Evaluation at those endpoints gives a rational interval for Z.

Similarly the numerator of the squared-density-difference mean is sum E c_E q^E. Its omitted part is at most2K^2 tail_Z. The positive-difference-mass numerator has omitted part at most K tail_Z. These give exact rational intervals for both physical observables, rather than an inference from TV or a sampled unbounded moment.

At fixed density D has logarithmic size O(M), and H=O(M+log(1/epsilon)). Because p+n<=E, there are O(H^3) possible DP states and O(sqrt(H)) one-site transitions per state. The straightforward implementation therefore uses O(M H^(7/2)) integer updates as a coarse bound. Count bit lengths are O(M log(H+1)) before the occupation multiplicity, which also has polynomial bit size. The phase-space state count D^2 is never enumerated.

## Executed receipt

`compile_bound_and_condition.py` actually qualified the M64,K64 input with target relative tolerance10^-12:

* H=28, maximum2100 DP states and437414 positive integer updates;
* largest difference-count integer86 bits;
* exact rational Z interval relative width below2.790e-14;
* logZ display85.96207276955925;
* squared-density-difference mean per site display0.01599916413005032;
* DP+qualification time0.05327746s after imports; no random draws;
* interval endpoint descriptions17,976 and18,622 numerator-plus-denominator bits.

The logarithm/mean decimal displays use MP arithmetic; the saved rational interval endpoints, not those rounded displays, are the qualified quantities. The full sector has about1.434e74 states. That count is not a reason to compare only against full enumeration: this ordinary DP is precisely the competent alternative.

For comparison, the new all-positive-phase theorem gives, on this same input and regardless unused one-site moments, direct iid relative variance at least12348.55 and at least1,234,855 field samples for relative RMSE1/10. Even the optimally bounded constant-envelope rejection law needs at least12349.55 proposals per accepted configuration. These are mathematical work bounds, not measured wall times or a lower bound on the DP, field MCMC, importance/control-variate, cluster or all other algorithms.

The computation does not acquire a noncommuting hopping conditional. Turning on frustrated hopping couples intermediate density histories and requires another paid contraction or correlated sampler. No claim about that operation follows from this easy physical model.
