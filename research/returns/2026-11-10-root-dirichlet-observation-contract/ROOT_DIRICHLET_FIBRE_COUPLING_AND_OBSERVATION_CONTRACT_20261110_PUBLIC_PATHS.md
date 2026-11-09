ROOT MATHEMATICAL PREPARATION: DIRICHLET FIBRE COUPLING AND FINITE-OBSERVATION CONTRACTS
10 November 2026 Brisbane. Direct coupling/contraction calculations and a small-time output-contract counterexample. No finite-population transition theorem, generic reaction-network transfer, complete simulator, priority or new principal allocation is claimed.

PRIMARY SOURCE CONTRACTS ACTUALLY INSPECTED. Sant-Jenkins-Ruggiero, arXiv2611.08623v1, https://arxiv.org/pdf/2611.08623v1 : Sections2-4, Definition3.1, Propositions3.2/3.4/3.6, Theorem4.1, Algorithms1/2 and their governing formulas. Their selected Wright-Fisher diffusion has positive parent-independent mutation, genic selection, an exponential-polynomial dual, and a Dirichlet-mixture transition from an infinite-entrance birth-death dual. The dual has linear births and quadratic deaths. Algorithm1 uses finite initialisation or Gaussian approximation; its identity is not a uniform finite-bit transition sampler. Algorithm2 has a stationary truncation-TV certificate, not a transient certificate. Jenkins-Spano, arXiv1506.06998v4 (29September2023), https://arxiv.org/pdf/1506.06998 : Section2 and Proposition5/Section4 inspected. Neutral positive-mutation retrospective simulation is exact in its stated real-arithmetic sense; coefficient work increases at small time. No arbitrary complete-bit/polylog-small-time bound is imported. No cited-but-unread proof or inaccessible predecessor is supplied as a quantitative premise.

DIRECT SHARED-GAMMA COUPLING. Let a=(a_i)>0, a0=sum a_i, and b=(b_i)>=0, b0=sum b_i. Draw independent G_i~Gamma(a_i,1) and H_i~Gamma(b_i,1), with Gamma(0,1) defined as deterministic0. Set
 X_i=G_i/sum G_j, Y_i=(G_i+H_i)/(sum G_j+sum H_j).
Then X~Dir(a), Y~Dir(a+b). If b0=0 they coincide. Otherwise, with R=sum H/(sum G+sum H) and Z=H/sum H,
 Y=(1-R)X+RZ, E R=b0/(a0+b0).
Since ||Z-X||1<=2,
 E||X-Y||1<=2*b0/(a0+b0).
The gamma-sum and beta-ratio identities prove the claimed laws; no sampling from an unknown parameter law is granted.
For adjacent b=e_i one obtains the sharper exact expectation
 E||X-Y||1 =2/(a0+1)*(1-a_i/a0),
because R is independent of X and Z=e_i. These are transportation bounds, not total-variation bounds on the continuous Dirichlet laws.

COUNT-INDEXED MIXTURE LIFT. For n,n' in N^K let c_i=min(n_i,n'_i), a=alpha+c, d1=|n-c|1, d2=|n'-c|1. Use common G~Gamma(a) and independent nonnegative gamma increments for each difference. Both Dirichlet draws have their exact required marginals, and
 E[||Y-Y'||1 | n,n']
 <=min(2, 2*d1/(|alpha|+|c|+d1)+2*d2/(|alpha|+|c|+d2)).
Integrating this bound over ANY coupling of two count-index mixing laws gives a valid Wasserstein-L1 bound on their two Dirichlet mixtures. Independence of the two count indices is unnecessary. A small scalar difference between their TOTAL degrees alone is insufficient when their compositions differ: the common coordinatewise part |c| is the actual smoothing denominator. An exact or quantitative coupling of the mixing indices is still an unconstructed operation unless separately supplied.

WHOLE FINITE-OBSERVATION TV FROM LATENT TRANSPORT. Given random frequency vectors X,Y on the simplex coupled arbitrarily, sample r ordered categorical observations independently conditional on each latent vector. Couple each pair maximally conditional on X,Y and independently across the r positions. Every ordered row then has its entire required mixture-of-product law, while
 Pr(observation rows differ)<=E min(1,(r/2)*||X-Y||1).
Hence their WHOLE observation-law TV is at most (r/2)*E||X-Y||1; multinomial-count observation TV is no larger by projection. Combining this with the preceding exact gamma coupling yields an explicit observation-TV certificate from a count-index coupling. This does not give TV closeness of the continuous latent laws, and does not turn an unknown source into a probability/ratio oracle. In particular it is not the sample-only P1 coupler: here the mathematical conditional kernels have known model parameters.

A SIMPLEX-PRESERVING RANDOM ROUNDING KERNEL. Let M=2^b, C_i(x)=sum_(j<=i)x_j, and take U~Uniform[0,1]. Put R0=0,RK=M and R_i=floor(M*C_i(x)+U) for i=1,...,K-1. Output Z_i=(R_i-R_(i-1))/M. Then Z is on the simplex grid, each cumulative coordinate is unbiased, and the SAME U couples the rounded outputs for x,y with
 Pr(Z(x,U)!=Z(y,U))<=M*sum_(i<K)|C_i(x)-C_i(y)|
 <=M*(K-1)*||x-y||1/2.
The last bound uses sum_i(x_i-y_i)=0, so every partial sum has absolute value at most halfL1. Thus this explicitly RANDOMISED observation kernel turns latent Wasserstein-L1 error into whole-grid TV error, with the displayed factor. Its target differs from deterministic rounding and must be stated as such; no free change of output contract is allowed. Exact uniform draws here mean mathematical couplings; a claimed finite-bit implementation must pay its own known-parameter comparisons.

DETERMINISTIC GRID SMALL-TIME COUNTEREXAMPLE. Consider the ordinary two-allele Wright-Fisher diffusion with any fixed finite smooth drift and positive mutation, begun at x=1/2. At that interior point the diffusion coefficient is sqrt(x(1-x))=1/2. Continuity of the coefficients, a martingale small-time limit and an O(t) drift give
 (X_t-1/2)/sqrt(t) converges in law to Normal(0,1/4).
Fix any b>=1, M=2^b, and use deterministic grid index floor(M*X_t). The initial point is EXACTLY a grid boundary. The probability of moving below it tends to1/2, whereas the probability of leaving the two neighbouring bins tends to0. Consequently
 TV(Law(floor(M*X_t)), pointmass_(M/2)) ->1/2 as t down to0.
Vanishing variance and convergence in probability to the initial frequency therefore do not justify returning the initial deterministic gridpoint under a whole-law TV contract. This is a counterexample to the shortcut, not a no-go for an appropriate short-time simulator. Also ANY finite-bit point output is supported on a countable set and is singular to an absolutely continuous interior frequency law; comparing those two unrounded laws in TV always gives1. A simulator must instead specify lazy real digits, an explicit observation law or a precise rounding target.

TRANSFER BOUNDARIES. A diffusion is a limit of finite-population chains, not the exact finite-population endpoint. Neither weak convergence nor a moment match pays finite-chain whole-law TV or binary-time cost. Fixed-model positive mutation differs from a uniform bound through vanishing mutation/boundaries. An entrance-law representation does not provide an algorithm to draw its weights with certified parameter-uniform error, nor pay their actual event count. The shifted selection and positive normalisation constants must retain their actual scopes. Random gamma/Poisson auxiliary variables in a proof are not new allowed chemical species or an authorised change to P3's original state graph. Conditional-Poisson and Dirichlet/beta-binomial families are different target measures; common terminology is not a transfer theorem. DDB1's accepted exact binomial operation is not automatically a beta-binomial/gamma/Dirichlet finite-bit cost bound.

These calculations identify a usable conditional composition: a quantitative mixing-index coupling plus known Dirichlet fibres plus finite observations. The first operation, endpoint uniform costs, boundary handling and any finite-population approximation remain separate and unproved here. No scientist method is prescribed and no full question is replaced. All known/unknown source/access/transfer/resource holds, threeXi/Capital/dispatcher, Solclosed/Dotsprotected and current resource guards apply; neither successful primary read recovered a held original.
