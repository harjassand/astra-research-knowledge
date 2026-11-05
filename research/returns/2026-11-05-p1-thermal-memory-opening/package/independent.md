# Independent selection route: low-temperature sampling, and a transport challenge

Date: 5 November 2026. This note was constructed without reading the other Pro participant's new tournament proposal. Prior equilibrium and quantum artifacts were not changed.

## Decision

The strongest independent full question I screened is whether an explicit polynomial-time algorithm can sample the **quenched** Sherrington--Kirkpatrick (SK) Gibbs law at a fixed inverse temperature beta > 1, with normalized Wasserstein error tending to zero. That accuracy already determines bounded Lipschitz functions of replica overlaps; total variation is not necessary for the first consequential theorem.

Complete success would cross the spin-glass transition algorithmically, produce correctly weighted thermal states rather than only low-energy configurations, and defeat the known obstruction for stable algorithms. It would be a major statistical-physics/algorithms result. It would not by itself prove an efficient sampler for arbitrary materials, sparse spin glasses, arbitrary optimization, or real physical cooling.

**I do not recommend nominating this route merely on that consequence.** My opening exposes a plausible finite state-weight representation, but does not construct the essential quenched state generator. Treating that generator as an oracle would hide the hard operation. The parent's local thermal-transport reduction currently has a more concrete central operation.

## Full question, conventions, and implication

Given the actual n by n GOE coupling matrix J (entries scaled by n^-1/2), prepare a classical spin sample from

    mu_J(sigma) proportional to exp[(beta/2) sigma^T J sigma],
    sigma in {-1,+1}^n,

in polynomial bit complexity and randomness cost, for typical J and one fixed beta>1. The distribution must be conditional on the supplied J; sampling the disorder-averaged spin law is trivial and is not the goal. There is no Gibbs-sample oracle, equilibrium initialization, free energy-gradient oracle, or supplied list of pure states. Input precision must be included, especially because a successful low-temperature sampler necessarily reacts sharply to disorder changes.

Use d_n(mu,nu)^2 = inf E||X-Y||_2^2/n. If independent replicas can be coupled with d_n<=eta, then their overlaps R_12=n^-1 X_1 dot X_2 obey

    E|R_12-R_12'| <= 2 eta.

Proof: split the dot-product difference into two terms and use Cauchy--Schwarz with ||X_i||=sqrt(n). Thus an eta-accurate sampler estimates any 1-Lipschitz function of the overlap to error at most 2 eta plus ordinary Monte Carlo error. This would operationalize a central observable of replica symmetry breaking for the supplied disorder, not merely reproduce its free energy.

## Strongest prior comparison

1. Du, Huang, Mohanty, Rajaraman, **Sampling from the Sherrington--Kirkpatrick Model up to Criticality**, arXiv:2610.17717 (13 October 2026). Theorem 1.1 gives polynomial-time simulated annealing with arbitrarily inverse-polynomial total-variation error for every fixed beta<1. Their algorithm uses O(n log n) Glauber steps per inverse-temperature increment of order 1/n, with constants depending on the desired accuracy exponent and beta. Worst-start fixed-temperature Glauber mixing throughout beta<1 is explicitly left open. This makes beta<1 an insufficient new target.
   - https://arxiv.org/html/2610.17717v1
   - Primary source refs retrieved: turn61view1, turn66view2.

2. El Alaoui, Montanari, Sellke, **Sampling from the Sherrington--Kirkpatrick Gibbs measure via algorithmic stochastic localization**, arXiv:2203.05093v2. Their positive result covers beta<1/2 in normalized Wasserstein distance; their negative theorem excludes their defined stable algorithms for beta>1, even in that weaker metric. It does not exclude all polynomial-time algorithms. The route uses stochastic localization with an AMP approximation to the tilted mean, not just knowledge of a scalar Parisi free energy.
   - https://arxiv.org/html/2203.05093v2
   - Primary source refs retrieved: turn61view2, turn66view1.

3. Incremental AMP can construct low-energy states under appropriate no-overlap-gap/FRSB conditions. A low-energy construction is not a Gibbs sampler: it need not generate states with their thermal probabilities. The full sampling question is therefore not settled by demonstrating good energy density.
   - Primary researcher talk: https://simons.berkeley.edu/talks/incremental-approximate-message-passing
   - Retrieved ref: turn50search7.

## A real, but insufficient, representation opening

An ideal one-level Ruelle/Poisson--Dirichlet state-weight model has a useful property: exponentially many potential states need not require exponentially many *weight-carrying* representatives at fixed accuracy.

For size-biased GEM(alpha,0) weights with 0<alpha<1, let

    V_k ~ Beta(1-alpha,k alpha), independently,
    P_k=V_k product_{i<k}(1-V_i).

The unexplored mass after K representatives is R_K=product_{k<=K}(1-V_k), and exactly

    E R_K = Gamma(K+1) Gamma(1/alpha) / Gamma(K+1/alpha)
          = O_alpha(K^{-(1-alpha)/alpha}).

This follows by multiplying E(1-V_k)=k alpha/(1-alpha+k alpha). Conditional on already possessing a size-biased state generator, truncating after K representatives gives an expected total-variation error no larger than E R_K after reallocating the residual mass. The cover size depends on accuracy and alpha, rather than the number of microscopic configurations.

This is a conditional opening, not a SK sampling algorithm. There are decisive missing steps:

- Acquire the representatives and their correct weights for the actual supplied J.
- Handle a continuum of hierarchical overlap scales, rather than assuming a supplied one-level cascade.
- Justify the finite-n representation and error in the requested metric.
- Maintain or regenerate the represented states under the random tilts of stochastic localization. A small unexplored mass can become important after tilting.
- Avoid smuggling in assumptions about generic perturbations that preserve free energy but may radically change the quenched Gibbs law.

The difficult operation is weighted quenched state generation. Neither scalar free-energy evaluation, an abstract cascade, nor unweighted low-energy AMP outputs implement it. I therefore regard the route as a consequential question with an insufficient opening for this selection round.

## Concrete contribution to the parent's thermal-transport challenge

### Weak filtering cannot remove the postselection bill by itself

Let h^2=I, [h,H0]=0, and rho_s proportional to exp(-H0-s h). The complete weak measurement

    K_+ = exp(-delta h/2)/sqrt(2 cosh delta),
    K_- = exp(+delta h/2)/sqrt(2 cosh delta)

obeys K_+^dagger K_+ + K_-^dagger K_-=I. Its two conditional outputs are exactly rho_{s+delta} and rho_{s-delta}. This suggests accepting every outcome and doing a parameter random walk until the desired coupling is reached.

For the simplest rho_0=I/2 and target a=k delta>0, that walk hits a with probability

    p_hit = (1+exp(-2a))/2 = exp(-a) cosh(a),

not probability one. Conditional on the hidden h=+1 eigenvalue, the walk has upward probability exp(-delta)/(2 cosh delta) and reaches +k with probability exp(-2a). Conditional on h=-1, it drifts upward and reaches +k almost surely. Averaging gives the formula.

Every hit produces rho_a, so this is precisely the ordinary postselection success cost. For N independent spins the all-target cost is p_hit^N. More generally, nondemolition measurements preserve the mean populations; each posterior population is a bounded martingale. Almost-sure stopping at a fixed different population would contradict optional stopping. Feedback that only changes further nondemolition measurement strengths cannot cure this. Real population exchange, a reset/repair channel, or accepted postselection must enter.

Equivalently, starting from I/d, a diagonal success operation producing p tau obeys p<=1/(d ||tau||_infinity). The weak-walk realization saturates this for the two-level thermal target. This is an elementary resource-accounting deduction, not a claimed new thermodynamic theorem.

The example supports the parent's insistence on acquiring the missing rejection operation. It also shows why a weak-filter or random-walk relabeling alone is not an advance.

### Warm-start transport may demand less than universal conditional repair

The SK criticality paper is a relevant cross-field comparator: it proves annealing by a weak Poincare inequality and a supplied sequence of nearby Gibbs starts, while worst-start fixed-temperature mixing remains unresolved. The scientific endpoint is thermal transport, so all-state mixing or arbitrary outcome-conditioned recovery may be stronger than necessary.

For a quantum linear Gibbs path rho_s=exp[-beta(H0+s V)]/Z_s, set F(s)=log Z_s. Then

    D(rho_s || rho_{s+delta})
        = F(s+delta)-F(s)-delta F'(s)
        <= (beta^2 delta^2 ||V||^2)/2.

The bound follows from the Duhamel/Kubo--Mori variance expression for F'' and its upper bound by the ordinary variance, hence beta^2||V||^2. This is a rigorous small relative-entropy step, independent of Hilbert-space dimension. It does not by itself provide a local CPTP channel transporting the states.

The classical stronger operator-order warmness bound cannot be imported from a generic matrix exponential inequality. For H0=diag(-L,L) and V=X, the excited diagonal element of rho_delta is approximately delta^2/(4L^2), whereas that of rho_0 is exp(-2 beta L). Hence

    D_max(rho_delta || rho_0)
        >= 2 beta L + 2 log(delta/(2L)) + o(1),

despite D(rho_delta||rho_0)<=beta^2 delta^2/2. This example lets the local norm L grow, so it is not a counterexample to a bounded-local-strength many-body class. It demonstrates only that true locality/imaginary-time information is required for a uniform warmness claim.

Thus a potentially weaker central operation is a local, implementable entropy/response transport bound along the particular Gibbs path, rather than universal recovery from every allowed conditional disturbance. Either route must actually produce a channel and account for how its coefficients are obtained.

### A current weak-measurement comparator does not supply the missing mixing theorem

Jiang and Irani, **Quantum Metropolis Sampling via Weak Measurement**, arXiv:2406.16023v1, accepted in PRX Quantum 2 November 2026, constructs a provably correct approximate Gibbs fixed point using boosted QPE and weak measurement. Its introduction explicitly states that the manuscript focuses on correctness; efficiency still depends on mixing. It therefore should be compared, but its existence is not a ready-made proof of polynomial thermal transport throughout the parent's clustering class.

- https://arxiv.org/html/2406.16023v1
- Primary ref retrieved: turn66view0; lines 98--104 distinguish correctness and mixing.
- Accepted-paper primary page: https://journals.aps.org/prxquantum/accepted/10.1103/xxq6-d82l

## Recommendation

Do not choose the SK programme solely because its full solution would be famous. This round has not built its weighted state generator. The parent's thermal-transport question has the stronger currently constructed reduction. Challenge that question by asking whether restricted Gibbs-path transport can replace the stronger conditional-repair requirement, while retaining the exact weak-filter martingale example as a check against hidden postselection cost.
