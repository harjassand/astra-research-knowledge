# A paid-discovery obstruction for classical transport sampling

Date: 2026-11-02. Status: independently derived route-closing lemma, NOT a claimed novel theorem or scientific opening. No positive material prediction capability was obtained.

## 1. Intended capability, and why this gate matters

The proposed mechanism was to replace exponentially slow equilibrium exploration by a learned nonequilibrium transport/path representation, while paying for discovery/training, initialization, all potential/force evaluations, and the importance-weight variance. Success on a physically consequential explicit model could make metastable material free energies, phase weights, and rare-transition predictions accessible without waiting for physical equilibration.

The following is the indispensable acquisition test. It refutes a generic black-box version of that proposal. It does NOT refute specialized algorithms using the actual explicit structure of a local Hamiltonian, a known phase decomposition, or physically acquired additional observables. In particular it is not a hardness theorem for bounded-degree pairwise Ising models, ordinary interatomic potentials, or a named material.

## 2. Exact input/output contract

The input is dimension d and exact adaptive point-oracle access to a smooth periodic potential U on the unit d-torus. A query may return U, its gradient, its Hessian, or even all derivatives at that point. The family below is known, but the hidden label is not. All queries, including learning, validation, initialization, tempering, and post-training use, are charged. Computation between queries is unrestricted.

Two output tasks:

1. Estimate log Z within a < (log 2)/2, with success probability at least 1-delta in every admitted world, where Z=int exp(-U).
2. Return one sample whose distribution is within epsilon in total variation of P_U=exp(-U)/Z in every world.

The admitted input family includes the flat baseline U_0=0 and one potential U_b per b in {0,1}^d.

## 3. A smooth, extensive-depth hidden phase

Set r=1/8, c_b,i=1/4+b_i/2, and

    eta(z) = exp[-z^2/(1-z^2)]  for |z|<1,
             0                  otherwise.
    I = integral_(-1)^1 eta(z) dz,
    m = (r I)^d,
    psi_b(x) = product_i eta((x_i-c_b,i)/r),
    f_b(x) = 1 + psi_b(x)/m,
    U_b(x) = -log f_b(x).

Every support B_b = product_i (c_b,i-r,c_b,i+r) is disjoint from every other support. Its volume is v=(2r)^d=4^(-d). There are N=2^d supports.

The standard flatness of exp[-1/(1-z^2)] at |z|=1 shows eta, psi_b, and U_b are C-infinity. All derivatives of U_b vanish outside B_b, including on its boundary. Thus all allowed oracle replies there equal those in the baseline.

By product integration, int psi_b=m. Consequently

    Z_0=1,             Z_b=2,
    P_b = (1/2) Uniform(torus) + (1/2) product bump_b,
    P_b(B_b)=(1+v)/2 >=1/2.

This is an order-one equilibrium phase, not a negligible tail. Its energy depth is extensive:

    0 <= -U_b <= log(1+1/m) <= log 2 + d log(8 e^(1/3)).

The last bound uses I>=exp(-1/3), by integrating over [-1/2,1/2]. Hence there is no exponential barrier height smuggled into the instance.

### Polynomial force and curvature

Inside B_b write z_i=(x_i-c_i)/r,

    a_i=z_i^2/(1-z_i^2),  a=sum_i a_i,
    ell=log(1/m)=O(d),  p=exp(ell-a)/(1+exp(ell-a)).

Then U=-log(1+exp(ell-a)), so

    grad U=p grad a,
    Hess U=p Hess a - p(1-p)(grad a)(grad a)^T.

Direct differentiation gives

    |partial_i a| <= (2/r)(1+a)^2,
    ||Hess a||op <= (8/r^2)(1+a)^3.

For each integer k>=1,

    p(1+a)^k <= k^k(1+ell)^k.

Indeed for a<=ell this is immediate; for a=ell+t>=ell use p<=exp(-t) and (1+ell+t)<=(1+ell)(1+t), then maximize exp(-t)(1+t)^k. Thus

    ||grad U||2 <= (8 sqrt(d)/r)(1+ell)^2 = O(d^(5/2)),
    ||Hess U||op <= (216/r^2)(1+ell)^3
                    +(1024d/r^2)(1+ell)^4 = O(d^5).

The bounds extend to the boundary by smoothness. These constants are intentionally loose. Every fixed higher derivative order also has a polynomial-in-d bound by the same exponential-tail argument, though no uniform-in-order assertion is needed below.

## 4. Coupling of all adaptive oracle transcripts

Fix the internal random seed of an algorithm and run it on the baseline. Until a query lands in B_b, its run against U_b has exactly the same answers, queries, stopping rule, and output as the baseline run. Every baseline query can meet at most one of the N supports.

If there are at most q queries on every run, a uniformly selected hidden b is discovered with probability at most q/N. More generally, if Q_0 is the number of baseline queries and E Q_0 is finite, the probability is at most E Q_0/N: condition on the seed, count the supports touched by the baseline path, then average. This proof includes fully adaptive training and validation.

### Theorem A: free-energy acquisition

Suppose log Z is estimated within a<(log 2)/2, with probability >=1-delta both on the baseline and on every hidden input. The two success intervals are disjoint. Thresholding between them is a test of baseline versus the uniform hidden-input mixture with error <=delta in both cases. Therefore the total variation distance between the two transcript/output laws is >=1-2delta. The coupling bounds it by E Q_0/N. Hence

    E Q_0 >= (1-2delta) 2^d.

In particular success probability 3/4 requires at least 2^(d-1) expected baseline queries.

### Theorem B: full equilibrium sampling

Let X_0 and X_b be coupled outputs from the baseline and hidden runs. Averaging over b,

    (1/N) sum_b Pr(X_b in B_b)
      <= E Q_0/N + (1/N) sum_b Pr(X_0 in B_b)
      <= (E Q_0+1)/N.

If each output law is epsilon-close in TV to P_b, its probability of B_b is at least (1+v)/2-epsilon. Consequently

    E Q_0 >= 2^d[(1+4^(-d))/2-epsilon]-1.

This lower bound allows nonlocal proposals, learned flows, arbitrary deterministic computation, and any finite-query implementable annealing/tempering procedure. It does not cover an uncharged global integration oracle or an exact continuous-time physical process that reveals the potential along an entire curve in one operation. Such access is materially stronger and must be priced separately.

## 5. The complementary weight-variance gate

For any target P, proposal Q, and event B with a=P(B), p=Q(B), Cauchy-Schwarz on B and its complement gives

    E_Q[(dP/dQ)^2] >= a^2/p + (1-a)^2/(1-p),
    chi^2(P||Q) >= (a-p)^2/[p(1-p)].

If p=0<a the second moment is infinite. This is the exact Bernoulli-coarsening lower bound; equality holds when the likelihood ratio is constant on each region.

Condition on a fixed no-discovery training transcript that leaves M hidden supports unqueried. The label is uniform over these supports, while any fixed post-training proposal Q is independent of which remaining label is true. Since sum_b Q(B_b)<=1 and P_b(B_b)>=1/2,

    (1/M) sum_(unseen b) E_Q[(dP_b/dQ)^2] >= M/4.

Thus at least one still-unseen target has relative weight variance >=M/4-1. A fitted transport may have tiny empirical weight variance on its observed region while the true variance is exponential. This is not a replacement theorem for general adaptive sequential estimators: Theorems A-B already charge their full adaptive queries.

## 6. Strongest equally informed comparator and the exact boundary

An ordinary algorithm queries every known candidate center c_b. At c_b, psi_b=1, so it discovers a hidden well immediately; after all N centers are flat it identifies the baseline. This costs at most N potential calls, matching the exponential acquisition lower bound up to constants. Random ordering uses about N/2 calls on a random hidden target.

After b is discovered, the target is the explicit 1/2-1/2 mixture above. For each bump coordinate, propose uniformly in (c_i-r,c_i+r) and accept with probability eta((x_i-c_i)/r). The acceptance is I/2>=exp(-1/3)/2, so an ideal-real sample needs O(d) expected one-dimensional proposals. For a requested finite quantization, standard computable-real/outward decisions pay the output precision; no claim of a finite bit string encoding an exact continuous real is made.

Therefore the hard operation is acquisition of the missing phase, not fitting or executing a transport after its label is supplied. Supplying b in the explicit input completely removes this particular lower bound. The theorem cannot be transferred to explicit local Hamiltonians merely because they have metastable wells.

## 7. Consequence and novelty verdict

The generic black-box route FAILS. Its hard construction cannot yield the proposed universal capability. Smoothness, extensive depth, a computable energy oracle, and an ideal low-variance transport representation do not acquire missing equilibrium phases at polynomial cost.

This obstruction is NOT presented as a new discovery. He and Zhang (2025), *On the query complexity of sampling from non-log-concave distributions*, https://arxiv.org/abs/2502.06200, gives substantially stronger lower/upper query-complexity results for globally log-smooth distributions on R^d. The compact periodic construction here is a transparent independent gate tailored to the acquisition claim.

Chatterjee and Diaconis (2015/2018), *The sample size required in importance sampling*, https://arxiv.org/abs/1511.01437, establishes the much broader information-theoretic sample-size issue. The elementary chi-square event calculation above is not a priority claim.

Koehler, Lee, and Risteski (2022), https://proceedings.mlr.press/v178/koehler22a.html, already provides polynomial sampling for Ising models with only a fixed number of eigenvalues outside a width-one interval. Cao and Vanden-Eijnden (2022), https://arxiv.org/abs/2206.09908, and Albergo and Vanden-Eijnden (2024), https://arxiv.org/abs/2410.02711, already develop nonequilibrium importance/transport sampling and optimal learned flow mechanisms. None licenses free discovery.

No physical implementation, practical speed advantage, new general sampler, or civilisation-scale enabling theorem was earned. The honest next research question must change the INFORMATION/STRUCTURE contract, not add another generic drift or variance estimator. I do not nominate an unconstructed restricted class as a positive opening.
