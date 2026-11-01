# Compact return kernels and bounded kinetic coupling

2026-11-01. Independent construction for the fresh Astra mandate. Earlier P2 work is untouched.

## Decision

The elementary boundary-response proposal is already supplied by exact milestoning, graph transformation, and resolvent methods. Few retained states do **not** imply a small exact memory model. A genuine positive class nevertheless exists: exponentially rare collective configurations of many coordinates can be predicted from a compact return kernel; bounded local kinetic interactions admit a controlled expansion whose error does not grow with inverse target probability.

The basic tensor/Neumann operation has strong prior art: Masetti and Robol (2019) directly compute mean absorption in loosely interconnected stochastic automata with a local Kronecker-sum inverse, interaction expansion, tensor trains, and a quadratic-convergence variant. Therefore neither “no rare trajectories” nor “Neumann expansion of many-body kinetics” is a novelty claim. The construction below supplies an explicit narrower theorem, a coefficient algorithm with stated costs, and discriminating failures. It is reusable capital; it is not established as a civilisation-changing foundation.

## 1. Complete service and microscopic input

There are n binary coordinates, x_i in {0,1}. In the baseline each flips 0->1 at alpha_i and 1->0 at beta_i. Define lambda_i=alpha_i+beta_i, p_i=alpha_i/lambda_i, and the exact product equilibrium law pi. All rates are input microscopic laws; none are inferred from a coarse trajectory or fitted rare-event rate.

The target b is one fully specified configuration; relabeling allows b=(1,...,1). The initial distribution is pi conditioned on x != b. The outputs are:

* the exact mean first hitting time;
* the positive-real Laplace transform of the first hitting distribution for the independent baseline;
* a rigorously bounded interaction expansion for the mean under bounded kinetic coupling.

This does not claim arbitrary initial distributions, arbitrary target sets, a stable inversion of a numerically approximate Laplace transform at every time, strong energetic couplings, or microscopic validity for an unspecified physical material.

## 2. Renewal identity: complete clock, not a rate fit

For any finite irreducible chain and singleton target b, define

    G_xb(s) = integral_0^infinity exp(-s t) P_xb(t) dt.

The strong Markov property at the first hitting time gives

    G_xb(s) = F_x(s) G_bb(s),

including the atom at time zero when x=b. Hence F_x=G_xb/G_bb. Averaging the starting state under equilibrium gives G_pi,b=pi_b/s. Write

    R_s = integral_0^infinity exp(-s t) [P_bb(t)-pi_b] dt.

Then the transform for equilibrium conditioned outside b is

    F_out(s) = [1/(1+s R_s/pi_b)-pi_b]/(1-pi_b),

and

    M_out = R_0/[pi_b(1-pi_b)].                         (1)

The return probability, including every repeated excursion and its duration, supplies the complete physical clock. A two-state rate chosen only to match (1) need not reproduce the distribution.

### A useful mean-only failure

Let P->B have rate a, P->H have rate c_in, and H->P have rate c_out. Then

    F_P(s)=a(s+c_out)/[(s+a+c_in)(s+c_out)-c_in c_out],
    E_P tau=(1+c_in/c_out)/a.

At a=1, c_in=0.01, c_out=1e-8, about 99% of trajectories finish on a microscopic time, while a small fraction enters a very long trap. An exponential distribution with the same approximately 1e6 mean predicts a wholly different prompt-completion probability. Matching a mean lifetime does not earn a usable lifetime law.

## 3. Product return kernel and rarity-independent integration time

For independent binary coordinates,

    P_bb(t) = product_i [p_i+(1-p_i) exp(-lambda_i t)].  (2)

This costs O(n) per evaluation. Expanding (2) into exponentials is unnecessary. Let lambda_min=min_i lambda_i and Lambda=sum_i lambda_i. The nonstationary part is a positive sum of exponentials with decay rates in [lambda_min,Lambda] and weights summing to 1-pi_b. Consequently,

    (1-pi_b)/Lambda <= R_0 <= (1-pi_b)/lambda_min,
    integral_T^infinity [P_bb(t)-pi_b] dt
      <= (1-pi_b) exp(-lambda_min T)/lambda_min.       (3)

Choosing T=lambda_min^-1 log[Lambda/(epsilon lambda_min)] bounds the truncation error by epsilon R_0. This horizon depends on local mixing, not on the rare first-hitting time. The same tail bound with lambda_min+s works for R_s at real s>=0.

Numerical cancellation is avoided by evaluating the product through logs and using expm1 for P_bb-pi_b. The rare probability itself is stored as log(pi_b). The scaled quantity W=pi_b(1-pi_b)M_out=R_0 is at least inverse-polynomial when the rate scale and target's individual probabilities are bounded. There is no need to numerically subtract two numbers of order one to recover pi_b.

### A one-port memory obstruction

Equation (2) has 2^n distinct exponential terms if all subset sums of the lambda_i are distinct. One can choose lambda_i=1+2^-i, so this remains true even when every local rate scale lies between 1 and 2. All coefficients are positive. Thus G_bb has 2^n distinct poles. Any exact finite-dimensional linear state-space realization of this single-port return response needs at least 2^n states (or 2^n-1 for its stationary-subtracted response). A single port does not bound exact memory dimension.

This is a lower bound on a particular linear realization, not computational hardness: the nonlinear product representation (2) is compact. It identifies the relevant resource more accurately than port count.

### Physical locality is not low rank in configuration space

Changing one independent microscopic coordinate gives a generator perturbation Delta Q_i tensor I_spectators, of rank 2^(n-1) when Delta Q_i has rank one. Half the subset poles change. Likewise, an operation enabled by a local r-coordinate pattern has projector P_local tensor I_spectators, of rank 2^(n-r). A local reset generally retains the unreset bath state. Repeated local reactions therefore cannot be replaced by a scalar renewal process merely because their spatial footprint is small.

## 4. Interacting kinetics with product equilibrium

Let baseline flip rates q_0(x,x^i) be multiplied by a_i(x_-i), independent of the value of the flipped bit. The multiplier may depend on at most r-1 neighbors and need not be separable over them. Assume

    1-rho <= a_i <= 1+rho,       0<=rho<1.             (4)

Every edge has the same factor in each direction, so detailed balance with the same product pi holds exactly. This is an interacting kinetic model, even though its equilibrium energies are additive.

Let L=-Q be the positive backward generator in L^2(pi), L_0 the independent one, and P the projection perpendicular to constants. On that subspace,

    (1-rho)L_0 <= L <= (1+rho)L_0.                    (5)

This follows edge by edge from the reversible Dirichlet form. Define

    g = 1_{b}/pi_b - 1.

The exact mean from equilibrium outside b satisfies

    M_out = <g,L^+ g>_pi/(1-pi_b).                    (6)

The direct consequence is

    M_0/(1+rho) <= M_out <= M_0/(1-rho).              (7)

The inequality is meaningful without constructing any large probability vector.

## 5. Constructive perturbation, not merely a comparison bound

Write L=L_0+V, A=L_0^(-1/2) V L_0^(-1/2), and h=L_0^(-1/2)g. Equations (4)-(5) imply ||A||<=rho. Therefore

    <g,L^+g> = <h,(I+A)^-1 h>
              = sum_{k=0}^K (-1)^k <h,A^k h> + E_K,

    |E_K| <= rho^(K+1)/(1-rho) ||h||^2.              (8)

Relative to the true answer, the error is at most

    (1+rho) rho^(K+1)/(1-rho).                        (9)

Neither (8) nor (9) contains pi_b^-1. The interaction contrast, rather than target rarity, determines the required expansion order.

### Why the coefficients can be computed without all configurations

Use the symmetric representation S_0=diag(pi)^(1/2) L_0 diag(pi)^(-1/2) and similarly V. Write V=sum_i V_i, each supported on at most r coordinates and annihilating the stationary vector on both sides. Define the scaled coefficients

    C_k=pi_b <g,L_0^+(V L_0^+)^k g>_pi.

For k>=1 they equal

    C_k = sum_{i_1,...,i_k} integral_[0,infinity)^(k+1)
      <b| exp(-S_0 t_0) V_{i_1} exp(-S_0 t_1) ...
          V_{i_k} exp(-S_0 t_k) |b> dt_0...dt_k.      (10)

Stationary-projector terms vanish because every V_i kills the stationary vector. Thus no exponentially large factor 1/pi_b remains in the integrand. Outside the union of the k local supports, each coordinate contributes only its scalar return probability at time sum_j t_j. The active union contains at most rk coordinates. A string can therefore be evaluated with O(n) scalar products and matrices on at most 2^(rk) states. The number of strings is n^k. This is a worst-case construction; symmetries or tensor contractions can reduce it, but are not assumed.

The entire source projector does couple all coordinates. Its exact product form is what allows the untouched coordinates to factor out. An arbitrary target set does not inherit this argument.

### Tail, short-time, quadrature, and precision costs

All spaces here are finite, so (10) has no short-time singularity. If ||V_i||<=v and the baseline spectral gap is lambda_min, each string's absolute integrand is bounded by v^k exp[-lambda_min sum_j t_j]. This uses the stationary annihilation on both sides of every V_i. Truncating every integration variable at T gives absolute normalized error no larger than

    (k+1) (n v)^k exp(-lambda_min T)/lambda_min^(k+1).

Consequently T=O([k log(n v/lambda_min)+log(1/delta)]/lambda_min) suffices for scaled error delta. The spectral norm of S_0 is Lambda. Derivatives of order m in one integration coordinate cost at most Lambda^m times the corresponding operator-norm bound. A deterministic composite quadrature therefore exists with polynomial cost in n, Lambda/lambda_min, and 1/delta at each fixed k. There are k+1 time integration dimensions, not one. A crude midpoint bound already proves the fixed-order claim; high-order quadrature is much more efficient.

For a relative error epsilon in M, choose scaled absolute errors proportional to epsilon C_0. Since C_0>= (1-pi_b)/Lambda, this asks only for inverse-polynomial absolute precision at bounded rate ratios and p_i bounded away from 1. Summing n^k signed strings may require extra O(k log n) precision bits. It does not require a number of bits proportional to pi_b^-1, nor an exponentially small absolute tolerance. Computing log(pi_b) and returning the logarithm of the lifetime costs O(n) input-scale bits.

The honest complexity statement is: **for fixed locality r, fixed contrast rho<1, and fixed relative accuracy, work is polynomial in n, without an inverse-target-probability factor.** As accuracy increases, K=O(log(1/epsilon)/log(1/rho)), and the n^K strings plus K+1-dimensional quadrature are expensive. This is not a general fully polynomial approximation scheme, nor evidence of superiority to modern tensor solvers.

## 6. Executed nontrivial coefficient

Choose cyclic nearest-neighbor multipliers

    a_i(x)=1+epsilon(2 x_{i-1}-1),      |epsilon|<1.

Writing L=L_0+epsilon V, the first coefficient in (10) reduces analytically from two time integrals to one. Put

    r_i(v)=p_i+(1-p_i)e^(-lambda_i v),
    ell_i(v)=(1-p_i)lambda_i e^(-lambda_i v),
    Z_j(v)=v[p_j(2p_j-1)+(1-p_j)(1-2p_j)e^(-lambda_j v)]
           +4p_j(1-p_j)(1-e^(-lambda_j v))/lambda_j.

Then

    C_1 = integral_0^infinity sum_i ell_i(v) Z_{i-1}(v)
                         product_{j notin {i,i-1}} r_j(v) dv.             (11)

This is O(n) per quadrature node. If W=pi_b(1-pi_b) M, operator convexity gives the stronger first-order enclosure

    W_0-epsilon C_1 <= W <= W_0-epsilon C_1
                                  +epsilon^2 W_0/(1-|epsilon|).          (12)

Indeed, the remainder is epsilon^2 <h,A^2(I+epsilon A)^-1 h>, nonnegative and bounded as shown. Equation (12) does not assume the correction has a particular sign.

`return_kernel.py` verifies (1), (11), and (12) against exact dense generator inversions for n=3,5,8 and epsilon in {-0.4,-0.15,0.15,0.4,0.8}: 15 interaction checks plus baseline checks passed.

It then evaluates n=128, all p_i=0.1, lambda_i linearly spaced from 1 to 2:

* state count: 340282366920938463463374607431768211456;
* target equilibrium probability: 1e-128;
* independent mean: 5.792303034296142e125 microscopic time units;
* independent integration horizon: 28.2833463;
* analytic baseline tail bound: 5.2083333e-13 on normalized W_0=0.0057923030;
* epsilon=0.2 interacting interval from (12): [0.8000030681, 0.8500030681] times the independent mean;
* positive-real transform at s M_0 in {0.1,1,10}: approximately {0.9090909091,0.5,0.09090909091};
* compact large calculation: about 0.04 seconds in the current environment.

These are deterministic calculations for the stated model, not physical experimental results. The SciPy adaptive quadrature error estimate is not a directed-rounding certificate. The operator and analytic tail inequalities are proved; the displayed numerical interval would need quadrature plus rounding enclosures before being called a machine-verified interval. Timing is an observation for this run, not an asymptotic complexity guarantee.

## 7. Failures that prevent overclaiming

1. **Strong kinetic constraints.** A soft East-type multiplier m+(1-m)x_neighbor has contrast rho=(1-m)/(1+m) after recentering. As m->0, expansion order diverges approximately as m^-1 log(1/epsilon). At a hard constraint the gap and accessibility can change qualitatively. Product equilibrium alone earns no cheap kinetics.
2. **Energetic interactions.** Multipliers that differ between forward and reverse transitions change pi. The product normalization and coefficient proof no longer apply as written.
3. **Arbitrary target sets.** The target must have an earned compact representation. A low-dimensional label does not mean its microscopic projector is low rank or easy to contract.
4. **Local physical ports.** A spatially local event still leaves all spectator configurations. A finite list of full patterns is a different condition.
5. **Time law.** The baseline transform is exact as a function; numerically recovering every deadline probability from finitely accurate transform evaluations is a separate inverse problem.
6. **Generality/priority.** Tensor-structured absorption solvers already achieve much of the service. No advantage over their best implementations has been demonstrated.

## 8. Exact primary constructions and executable counterparts

* Bello-Rivas and Elber, Exact Milestoning (2015): https://pmc.ncbi.nlm.nih.gov/articles/PMC4352169/ . The full phase-point kernel is exact; loss of memory is not required. An efficient finite-dimensional approximation is an additional condition.
* Swinburne et al., PyGT: https://github.com/tomswinburne/PyGT and https://pygt.readthedocs.io/en/latest/ . Stable known-network graph transformation preserves branching probabilities and mean first-passage times; source code and examples are public.
* Masetti and Robol (2019), Tensor methods for the computation of MTTA in large systems of loosely interconnected components: https://arxiv.org/abs/1907.02449 and https://arxiv.org/pdf/1907.02449 . Public implementation: https://github.com/numpi/kaes . Sections 3.3, 4, and 5 contain the exponential-sum inverse, Neumann iteration, quadratic variant, truncation/rank issues, and computational conditions. The paper reports up to 3^32 potential states; rank behavior and tuning remain important.
* Georg et al. (2022/2023), Low-rank tensor methods for Markov chains with applications to tumor progression models: https://pmc.ncbi.nlm.nih.gov/articles/PMC9718722/ . Uses uniformization/Neumann plus low-rank tensors for an exponentially time-marginalized law. Its efficient costs depend on low solution ranks; data/code are available by author request, not a verified public repository in this audit.
* Kazeev et al. (2014), Direct Solution of the Chemical Master Equation Using Quantized Tensor Trains: https://pmc.ncbi.nlm.nih.gov/articles/PMC3953644/ . Establishes substantial existing deterministic CME machinery; low rank is the decisive compressibility resource.

## Reconciliation with root's construction

An exactly solvable interacting Gaussian/free-fermion baseline can replace the product baseline in the same return-kernel principle. The crucial new burden is then to compute the required insertions/return matrix elements and prove the perturbation bound and numerical conditioning. A local physical reaction cannot be silently treated as a low-rank full-configuration reset. The strongest possible synthesis is a controlled nonintegrable extension around an earned interacting baseline, not the renewal identity alone.

### Additional challenge to the interacting Gaussian route

The following exact sources were checked to prevent an overly broad novelty claim:

* Buchete and Straub (2001), Mean First-Passage Time Calculations for the Coil-to-Helix Transition: The Active Helix Ising Model, DOI 10.1021/jp0104031. Author-hosted full text: https://people.bu.edu/straub/pdffiles/pubs/JPC.105.6684.2001.pdf . Its kinetic MFPT uses a mean-sequence approximation. It does not already establish the desired finite-temperature Gaussian return-kernel service.
* Hill (1969), Mean First Passage Time in a Linear System with Nearest-Neighbor Interactions. Application to a Theory of Muscle Action, DOI 10.1063/1.1671507. The published abstract identifies an internal-equilibrium approximation.
* Blom and Godec (2021), Criticality in Cell Adhesion, DOI 10.1103/PhysRevX.11.031067. This is a substantive physical application of collective formation/dissolution first passage, with Bethe-Guggenheim and local-equilibrium approximations.
* Dornic and Conte (2026), Geometry of the Ising persistence problem and the universal Bonnet-Manin Painleve VI distribution: https://arxiv.org/abs/2603.28632 and DOI 10.1007/s10955-026-03608-z. Exact Pfaffian first-passage/persistence theory already exists in a zero-temperature semi-infinite-chain stationary scaling regime. That is a different target and regime from finite-temperature collective configuration hitting.
* Landi (2021), Waiting time statistics in boundary-driven free fermion chains, DOI 10.1103/PhysRevB.104.195408. Full text: https://repositorio.usp.br/directbitstream/8dcfc138-8906-44cf-a0d4-a0327fcacfd7/PhysRevB.104.195408.pdf . Quantum boundary jump waiting-time laws are computable with small fermionic matrices. Gaussian no-click/jump conditional evolution is therefore an existing operation; public implementation family: https://github.com/jayren3996/GaussianFermions.jl . Classical stochastic probability-ket translation needs its own positivity, normalization, parity, and event-clock proof.

A possible compatible physical interface is to monitor only transition channels J for which Q-J remains quadratic and J maps an individual Gaussian state to another Gaussian state. Unlike a general local pattern projector, this can carry spectator memory in a compact conditional state. It is a useful construction route, not a novelty claim. Stronger pattern-selective hazards or sums of unresolved jumps can break the Gaussian closure.
