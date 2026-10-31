# Acquiring the weights of phases that the experiment never visits

## Outcome and priority status

This is a stronger consequence-first operation than the one-site contraction construction in REPORT.md. It crosses a physical metastability barrier: a local trajectory that remains in one phase can determine the weights of unseen equilibrium phases to ordinary fixed accuracy. The explicit route is local conditional likelihood estimation followed by a constructed dilute-defect (polymer) sampler and phase-weight calculation.

**The bridge below is derived here, but historical novelty is unestablished. Ordinary conditional maximum likelihood plus existing low-temperature polymer algorithms supplies the same operation. There is no separation from that strongest matched route.** The useful result is an acquisition-complete construction and a matching quadratic observation obstruction for a natural query. No experimental phase switch, reset, supplied block sampler or exact output is used.

## 1. Native task and model

Let G be a known connected n-vertex graph of maximum degree Delta. Let its edge expansion satisfy |boundary S| >= b|S| whenever 1<=|S|<=n/2. This is not a free oracle: a certified lower bound lambda on the second eigenvalue of the unweighted graph Laplacian implies b=lambda/2, since

    1_S^T L 1_S >= lambda |S|(1-|S|/n) >= (lambda/2)|S|.

One may verify the spectral lower bound by finite-precision interval linear algebra or exact rational inertia tests. Its polynomial cost and desired margin must be charged. A supplied graph is not a supplied equilibrium sampler.

The stationary spin law on {-1,+1}^n is

    mu_h(sigma) proportional to exp(beta sum_edges sigma_i sigma_j
                                   + h sum_i sigma_i).

Initially beta and G are known; the physically consequential unknown is a weak uniform bias h in [-H,H]. Later one may ask for another calibrated uniform bias h+u while retaining the same model. The extension to unknown couplings requires additional calibration and is addressed separately below.

One running experiment follows random-site heat-bath updates. At an update of i, with neighbour sum z, the probability of +1 is

    p_z(h) = logistic(2 beta z + 2h).

The update attempt, z and outcome are observed, including null updates. The initial state can be all plus. No equilibrium or phase crossing is assumed. The target can be the mean active fraction f=(1+sum_i sigma_i/n)/2 to a fixed tolerance such as 0.04, or samples within a prescribed total-variation error. Exact output is unnecessary.

## 2. Earn the bias without visiting the other phase

For N observed updates, define the conditional likelihood

    L_N(h) = product_t p_{z_t}(h)^{Y_t} (1-p_{z_t}(h))^{1-Y_t}.

This is the likelihood conditional on the observed predictable contexts and update schedule; the contexts need not be independent or stationary. The full path likelihood differs only by parameter-independent factors. The maximum-likelihood estimate is the unique zero of

    S_N(h) = sum_t (Y_t-p_{z_t}(h)),

clipped to [-H,H]. Computing it is a one-dimensional monotone root problem; no equilibrium partition function is needed. Counts of (z,Y) are sufficient for this calculation. The original trajectory can be retained at no change to the guarantee.

Set kappa=logistic(-2(beta Delta+H)). Then p_z(h) stays in [kappa,1-kappa]. At the true h, S_N(h) is a bounded martingale sum. Its derivative is

    S_N'(h)=-2 sum_t p_{z_t}(h)(1-p_{z_t}(h))
            <= -2N kappa(1-kappa).

Consequently, with probability at least 1-delta,

    |h_hat-h| <= sqrt(log(2/delta)/(8N kappa^2(1-kappa)^2)).

The bound is conservative in its temperature dependence; an empirical likelihood confidence set or a sharper variance-sensitive inequality improves it. It already proves N=O(n^2 tau^-2 log(1/delta)) for fixed beta, Delta and H when global Gibbs-law error tau is required. There is no mixing-time factor.

For any h,h', integration of the Gibbs tilt, or a direct likelihood-ratio argument, gives the safe bound

    ||mu_h-mu_h'||_TV <= n |h-h'|.

Thus estimating h to tau/(4n) budgets at most tau/4 for physical-model error. This precision is not an artificial exactness demand: Section 6 proves that ordinary fixed-accuracy macroscopic predictions really can require distinguishing biases separated by 1/n.

### A usable finite-trajectory confidence set

For any fixed finite grid g_1,...,g_K with positive weights w_j summing to one, put

    M_N = sum_j w_j L_N(g_j).

For the true continuous h, E_h[M_N/L_N(h)]=1. Therefore

    C_N(delta) = {h in [-H,H]: log L_N(h) >= log M_N + log delta}

contains h with probability at least 1-delta, by Markov's inequality. Its interval endpoints are roots of a concave one-dimensional function. The true h need not lie on the mixture grid. This is a likelihood-ratio/martingale construction, not an asymptotic standard-error assertion. The code uses this exact mathematical confidence rule with ordinary floating-point root evaluation and explicitly does not claim formal interval-arithmetic certification.

## 3. Earn an explicit sampler across the two phases

The following elementary construction gives a fully priced low-temperature route. It intentionally uses conservative constants and is not competitive with the best published polymer algorithms.

Write a configuration in the plus phase as a collection of connected minus-spin components. A connected defect gamma has activity

    w_+(gamma)=exp(-2 beta |boundary gamma|-2h|gamma|).

In the minus phase a connected plus-spin component has

    w_-(gamma)=exp(-2 beta |boundary gamma|+2h|gamma|).

Distinct components must be disjoint and nonadjacent. If |gamma|<=n/2 and |h|<=H, both activities satisfy

    w_+/- (gamma) <= exp(-a |gamma|),  a=2 beta b-2H.

This activity formula is built directly from the inferred h and known local energy; no block probability or phase sampler is supplied.

### Count and enumerate defects

A connected set of size k containing a specified vertex has a canonical depth-first traversal of length 2(k-1). There are at most Delta^{2(k-1)} such walks. Put A=Delta^2 and r=A exp(-a). If r<1, the total activity of all size-k defects is at most n A^{k-1} exp(-ak).

Choose a cutoff K<=floor(n/2). The probability, conditional on either phase, that a connected defect has size greater than K is at most

    R_K = n exp(-a) r^K/(1-r).

Proof: removing a specified connected component maps an allowed phase configuration injectively to a lower-defect allowed configuration and divides its weight by exactly w(gamma); therefore its phase probability is at most w(gamma). Sum over large components. This avoids an assumed equilibrium sampler.

Taking K=O(log(n/epsilon)/(a-log A)) makes R_K<=epsilon. If this cutoff exceeds floor(n/2), enumerate all phase-allowed defect sizes; the tail is then zero. The finite list of types can be generated by growing connected vertex sets and deduplicating, in time n Delta^{O(K)}. For fixed Delta and a-log A>0 this is polynomial in n and inverse error, with the exponent charged.

### Simulate the finite polymer gas

Temporarily allow any compatible collection of these listed defects, regardless of its total volume. Its probability is proportional to the product of activities. Run a continuous-time birth-death chain:

- every occupied defect dies at rate 1;
- every listed defect proposes a birth at rate w(gamma), accepted exactly when it is compatible with all occupied defects.

Use an explicit enumerated activity table and weighted sampling data structure. The total death rate is at most n. The total birth-attempt rate is at most n s, where

    s=exp(-a)/(1-r).

These rates and preprocessing costs are charged. The local birth/death detailed-balance ratio is exactly w(gamma), so this chain has the desired finite polymer-gas stationary law.

Couple two chains with common birth attempts and deaths. Give an unmatched defect weight |gamma|. Starting from configurations differing in one defect gamma, its death removes distance |gamma| at rate 1. The only additional disagreements arise from births of defects incompatible with gamma. Their total weighted rate is at most

    sum_{eta incompatible gamma} |eta| w(eta)
       <= (Delta+1)|gamma| exp(-a)/(1-r)^2
       = theta |gamma|.

The bound counts at most (Delta+1)|gamma| possible vertices in the closed neighbourhood and all defects containing one of them. If theta<1, path coupling gives contraction at rate 1-theta in the weighted symmetric-difference metric. Removing unmatched defects then adding target defects is a valid path, so the path metric is the weighted symmetric difference. The diameter is at most 2n. Thus a run of

    t >= log(2n/epsilon)/(1-theta)

physical units of this **digital** chain yields total-variation error at most epsilon. Its expected number of attempted events is O(n(1+s)t); events may be simulated explicitly with rejection. This proves the sampler instead of calling one as an oracle.

### Recover the actual phase restriction

For the plus phase accept total defect volume <=floor(n/2); for the minus phase accept total defect volume <=ceil(n/2)-1. These conventions partition the full spin state space, including ties. In the unconstrained polymer gas, each defect has inclusion probability at most w(gamma), hence expected total volume <=ns. If s<=1/4, Markov's inequality bounds rejection probability by 2s<=1/2 for either phase. Digital rejection therefore takes at most two proposals in expectation for the exact gas, with a constant adjustment for approximate proposals. It does not require experimental preparation. Sampling error is amplified only by this constant acceptance factor.

## 4. Acquire relative phase weights without a partition-function oracle

For each sign, let Z_gas denote the unrestricted truncated polymer partition function, and let A_phase be the acceptance probability for the phase-volume restriction. Then

    Z_plus^K = exp(beta|E|+hn) Z_gas,+ A_plus,
    Z_minus^K = exp(beta|E|-hn) Z_gas,- A_minus.

The phase odds are obtained from these two quantities; the common edge factor cancels. Neither Z_gas nor A_phase is supplied.

Estimate A_phase by the explicit sampler above; it is at least 1/2. Estimate Z_gas by deleting graph vertices one by one. At a deletion step, if v is the next vertex and p_v is the probability that no current polymer contains v, then

    Z_current = Z_after-deleting-v / p_v.

Moreover p_v>=1-s>=3/4, since the probability that some polymer contains v is at most the sum of its activities. At the end Z_empty=1. The same contraction proof holds after vertices are removed, because the list of allowed defects only shrinks.

Estimate each p_v to additive O(epsilon/n) with a prescribed failure budget, and multiply the reciprocals, or sum logarithms. Their positive lower bound makes the total log-partition error O(epsilon). Hoeffding costs O(n^2 epsilon^-2 log(n/delta)) independent digital samples at each of n stages. Each is supplied by the priced polymer chain. This is an inefficient but explicit polynomial counting procedure; it contains no hidden FPRAS oracle. Better existing approximate-counting routines should be used in the strongest practical comparator.

Combining calibration uncertainty, polymer truncation, digital mixing, phase-weight estimation and phase-volume acceptance yields an adjustable total-variation error. Split the requested tau among these five terms. To answer a bounded numerical query, sample and average with the same requested tolerance. Future calibrated fields are allowed whenever the uncertainty-enlarged bound on |h+u| passes r<1, theta<1 and s<=1/4.

## 5. Why a physical phase switch is unnecessary

Assume n is odd for simplicity and start at all plus. Any local-update path reaching negative magnetisation must visit a configuration with (n-1)/2 or (n+1)/2 minus spins. For a set S of size floor(n/2), its stationary weight relative to all plus is at most

    exp(-2 beta b floor(n/2)+2Hn).

Detailed balance gives P^t(x,y)<=mu(y)/mu(x). A union bound over at most 2^n middle configurations and N update times therefore yields the valid (loose) crossing bound

    P(cross by N) <= N 2^n exp(-2 beta b floor(n/2)+2Hn).

When H=c/n and beta b>log 2, this is exponentially small in n for polynomial N. Yet the conditional-likelihood estimator above still has polynomial observation cost for fixed beta and Delta. The experiment can remain in the plus phase throughout calibration while the later digital sampler returns the correct mixture of phases.

This is a separation from waiting for spontaneous physical phase transitions, not a separation from an ordinary model-aware retained-data algorithm. It does not assert that every initial state has an exponential hitting time, nor that the bound is sharp.

## 6. Quadratic observations are naturally necessary

Consider the same known low-temperature graph and coupling under h_+=c/n and h_-=-c/n, with the same all-plus initial state. For any predictable update schedule, a single outcome is Bernoulli with logistic natural parameters separated by 4c/n. The Bernoulli log-partition function has second derivative at most 1/4. Therefore one observed update has conditional KL divergence at most

    (4c/n)^2/8 = 2c^2/n^2.

By the adaptive transcript chain rule, KL between the N-update transcript laws is at most 2Nc^2/n^2. Any constant-success test distinguishing them needs constant KL, and hence N=Omega(n^2). Retaining the full observations does not avoid this information requirement.

The hypotheses differ by a constant in a natural bounded observable. At h=0 use symmetry and the dilute-defect bound. With s<=1/16, the probability that |M|>=n/2 is at least 1-4s. For h=c/n,

    E_h[M/n]
      = E_0[(M/n) sinh(cM/n)] / E_0[cosh(cM/n)]
      >= (1-4s) sinh(c/2)/(2 cosh(c)).

For c=1 the last quantity exceeds 0.12. The expected active fractions under h_+ and h_- differ by this same amount. An estimator with ordinary absolute error 0.04 and success probability at least 2/3 therefore yields a distinguishing test, so it requires Omega(n^2) updates. No exact output or exponentially small requested error creates the lower bound.

The upper likelihood bound is O(n^2) for fixed low-temperature parameters, followed by the explicit polynomial sampler/counting construction. Thus the observation exponent is matched in this restricted but consequential problem. The temperature-dependent constants may be prohibitive and are not hidden.

## 7. Unknown local interactions: feasible but more costly bridge

If all J_ij and h_i are unknown in a bounded-degree Ising heat-bath model, first acquire local conditional probability tables using the no-reset argument in REPORT.md. Half-logit values have the form

    (1/2) logit p_i(z)=h_i+sum_j J_ij z_j.

Uniform Walsh averages recover h_i and J_ij from this finite table. On [kappa,1-kappa], the half-logit derivative is at most 1/[2kappa(1-kappa)], so table error eta yields parameter error at most eta/[2kappa(1-kappa)]. Symmetrise edge estimates and propagate intervals.

The data can thereby certify ferromagnetic coupling lower bounds, an activity exponent a and the polymer conditions. A worst-case global Gibbs-TV guarantee from all parameter intervals uses total energy error sum_e|delta J_e|+sum_i|delta h_i|, so it may require each local parameter to O(tau/n). The simple acquisition proof then has O(n^3) update-attempt dependence rather than the O(n^2) one-parameter result. Better task-specific correlated uncertainty could improve this, but it is not proved here.

The graph and finite-range model are supplied assumptions. Learning unknown topology can use existing dynamics-learning algorithms with their own stated assumptions and costs. Model validation, noisy local contexts and unknown actuation remain separate gaps.

## 8. Strong ordinary comparator and relevant primary literature

The strongest conventional route is precisely: retain the trajectory; fit a local conditional likelihood; use an appropriate established low-temperature counting/sampling algorithm; propagate statistical uncertainty. It receives identical observations, prior knowledge, computational resources and accuracy requirements. It matches the operation above. The original row-sum/Dobrushin comparator is inadequate in this regime and is not used to claim a novel advantage.

- [Helmuth, Perkins and Regts, Algorithmic Pirogov-Sinai theory](https://arxiv.org/abs/1806.11548): established low-temperature counting and sampling via contour representations.
- [Chen et al., Fast algorithms at low temperatures via Markov chains](https://ora.ox.ac.uk/objects/uuid%3A743b4aff-3278-445d-b3b4-dcde6b0a5d5b): established rapidly mixing polymer dynamics and efficient spin-system sampling on expanders. The elementary explicit chain above is a conservative instance of this existing idea.
- [Gheissari and Sinclair, Low-temperature Ising dynamics with random initializations](https://arxiv.org/abs/2106.11296): demonstrates another strong ordinary route, suitable mixtures of phase initialisations, and explains the need to treat within-phase mixing separately from the global bottleneck.
- [Gaitonde, Moitra and Mossel, Better Models and Algorithms for Learning Ising Models from Dynamics](https://arxiv.org/abs/2507.15173): stronger observation-model learning algorithms than the simple one used here.
- [Discrete distributions are learnable from metastable samples, Nature Communications 2026](https://www.nature.com/articles/s41467-026-75439-1): a further direct precedent that metastable data can reveal model parameters. Its stated independent metastable-sample premise and empirical trajectory tests must be distinguished from a finite single-trajectory theorem; the simple martingale proof here explicitly uses actual transition outcomes.

## 9. The many-phase boundary suggested by sparse parity models

Unknown sparse parity interactions could encode exponentially many phases. Learning the parity constraints from dynamics is already a substantial conventional capability: [Gaitonde, Moitra and Mossel, Bypassing the Noisy Parity Barrier: Learning Higher-Order Markov Random Fields from Dynamics, STOC 2025](https://doi.org/10.1145/3717823.3718231) reports efficient trajectory-based graph and parameter learning, despite noisy-parity barriers in the independent-sample setting.

For a binary parity-check matrix A with independent rows and energy depending only on Ax, the syndrome bits are independent and a uniform affine-kernel lift is obtained by Gaussian elimination. This exact ordinary route must be tested first. It already handles exponentially many equal-weight phases.

External fields on physical bits or dependencies among syndrome coordinates generally introduce weighted code counting. [Goldberg and Jerrum, Approximating the Tutte polynomial of a binary matroid and other related combinatorial polynomials](https://arxiv.org/abs/1006.5234) gives approximation-hardness results for general binary matroids and code weight enumerators. Linear algebra alone does not solve this task.

A nontrivial established tractable region is regular matroids: [Goldberg and Jerrum, A polynomial-time algorithm for estimating the partition function of the ferromagnetic Ising model on a regular matroid](https://arxiv.org/abs/1010.6231) uses Seymour decomposition to give an FPRAS. Recognising and decomposing an acquired regular matroid, followed by this conventional algorithm, is a much stronger comparator than treating exponentially many phases as intrinsically intractable. Arbitrary logical conditioning may leave this tractable class; its closure must be checked rather than assumed.

No new earned operation beyond these exact and approximate routes has been established. A credible advance would need to acquire and exploit a broader representation for weighted phase codes, with a priced construction and a theorem that survives these ordinary comparators.
