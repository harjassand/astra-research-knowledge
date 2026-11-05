# Exact adaptive phase sampling, and the obstacle exposed by closing its sampling access

## Decision

A correct constructive theorem survives: calibrated unnormalized densities, fresh phase-conditional samples, and an invertible coordinate map generate independent exact equilibrium phase labels even when the map and branch probability are changed after every attempt. This is a synthesis of transport, detailed-balance flux, and a Bernoulli race; originality is not claimed.

The stronger scientific endpoint does not survive the ordinary-method comparison in the explicit family closed here. For the explicit envelope-balanced branch choice constructed here, conditional rejection from a known common reference makes ordinary global rejection no more costly for a complete equilibrium configuration than the race is for a phase label. More generally, the final conditional draw alone in this race architecture costs as much on average as direct global rejection, before paying for phase selection. The inequality is exact. Therefore this route should be retained as a lemma and an access-model diagnostic, not presented as a new general solution to metastability or free-energy computation.

## 1. Actual starting operations and the question

Let two phases be labelled disjoint copies of equal-dimensional configuration spaces, with positive integrable weights w_A and w_B, integrals Z_A,Z_B, and conditional laws mu_i=w_i/Z_i. The desired equilibrium phase probability is p_B=Z_B/(Z_A+Z_B).

The initial construction assumes the following operations, with their cost counted separately:

- Draw a fresh sample from either conditional law, independent of the complete previous history.
- Evaluate a calibrated ratio of unnormalized weights, including their relative energy offset.
- Evaluate an invertible map T, its inverse, and its Jacobian determinant.
- Generate independent random coins.

These are an interface, not a statement that an unknown physical system supplies the interface cheaply. Section 5 constructs the sampling and map operations for an explicit family; section 6 proves the resulting dominance obstacle. A finite spin implementation removes the need to interpret floating-point continuous sampling as mathematically exact.

Relative calibration is necessary. Adding a constant c to the energy of phase B leaves its normalized conditional distribution and energy gradients unchanged while multiplying Z_B by exp(-beta c). Conditional samples and scores alone therefore cannot determine p_B. The ratio operation must include the missing offset or an equivalent physical calibration.

## 2. The adaptive race and its exact cancellation

Before attempt t, choose any invertible map T_t and any branch probability q_t in (0,1), as measurable functions of the entire observed past. Freeze them before generating the current branch and conditional sample. Define

r_t(x)=w_B(T_t x)|det DT_t(x)|/w_A(x).

With probability q_t, draw X from mu_A and accept with probability min(1,(1-q_t)r_t(X)/q_t). If accepted, output the label B. With probability 1-q_t, draw Y from mu_B and accept with probability min(1,q_t/((1-q_t)r_t(T_t^{-1}Y))). If accepted, output A. On rejection, try again; update the map and q using the completed attempt if desired.

The emitted label is opposite the source phase. This reversal is essential.

Conditional on any complete past history, put

C_t=integral_A min(q_t w_A(x),(1-q_t)w_B(T_t x)|det DT_t(x)|) dx.

Direct integration, including the change of variables y=T_t x in the second branch, gives

P(accept and B | past)=C_t/Z_A,
P(accept and A | past)=C_t/Z_B.

Their ratio is Z_B/Z_A. Hence, conditional on this attempt accepting, the output probability is exactly p_B, regardless of its map, branch probability, or past failures. Summing over the disjoint possible waiting times proves that the next accepted label has probability p_B conditional on all preceding accepted labels and their histories. Provided the procedure terminates almost surely after every accepted label, the sequence of labels is iid Bernoulli(p_B).

A sufficient termination condition is a uniform conditional success bound

lambda_t=C_t(1/Z_A+1/Z_B) >= alpha > 0.

It also gives expected attempts at most 1/alpha per label. Merely learning a map, without controlling overlap, does not establish this condition.

For a full equilibrium configuration, draw a new independent conditional sample from the emitted phase. The point used in the acceptance decision generally follows a bridge-tilted law, so reusing that point is biased.

The pointwise Metropolis minimum maximizes C_t among acceptance functions satisfying the same local common-flux balance. This is only an optimality statement within that restricted race architecture; it says nothing about the best estimator or sampler using all the available information.

## 3. Error, precision, and execution bill

For a fixed number K of accepted labels, Hoeffding's inequality gives

P(|mean(label)-p_B| > sqrt(log(2/delta)/(2K))) <= delta.

Thus K >= log(2/delta)/(2 epsilon^2) gives additive epsilon accuracy. Expected work includes K/alpha conditional draws, map/inverse/Jacobian and ratio evaluations on those attempts, all training costs, and K additional conditional draws if full configurations are wanted. The required conditional-sampler cost is not hidden inside the attempt count.

A statement about additive phase probability is not automatically a statement about relative partition-function accuracy or free-energy accuracy. If p_B is tiny, small additive error can still be uninformative about log(Z_B/Z_A).

The fixed-K condition matters. Stopping after an attempt budget can make the number of accepted observations depend on preceding labels through adaptation. An ordinary fixed-sample interval should not be used at an outcome-dependent stopping time; use a predeclared accepted count or a suitable anytime-valid confidence sequence.

For approximate conditional access, suppose the entire one-attempt outcome law differs in total variation by at most e from its ideal law, uniformly conditional on every reachable history. One may take the uniform upper bound e=sup_past [q eta_A+(1-q)eta_B+nu], where the eta terms bound the conditional sampler errors and nu bounds the numerical acceptance-coin error. If e<alpha, the actual race still terminates. Coupling the ideal and actual executions until the first mismatched attempt bounds conditional error of each emitted label by min(1,e/alpha): the ideal expected number of opportunities for mismatch is at most 1/alpha.

The K-label joint law is therefore within K e/alpha in total variation. For scalar mean estimation a better statement is available: conditional label bias is at most e/alpha, so bounded martingale concentration gives, with probability at least 1-delta,

|mean(label)-p_B| <= e/alpha+sqrt(log(2/delta)/(2K)).

An additional independent final conditional draw adds its own approximation error when constructing a full configuration.

This error theorem does not assign a small total-variation error to a floating-point approximation of a continuous random variable: a finitely supported floating-point distribution and a genuinely continuous distribution are mutually singular. Continuous calculations here use the conventional random-real sampling model. Finite arithmetic exactness is instead demonstrated in section 7 for a finite target, where ordinary fair-bit randomized algorithms apply without this issue. The NumPy continuous experiments are numerical checks of formulas and algorithm behavior, not proofs of exact continuous simulation or certified numerical error budgets.

## 4. What transport buys, and what it does not

For q=1/2, let a=E_muA min(1,r), b=E_muB min(1,1/r). Then a/b=Z_B/Z_A and lambda=(a+b)/2. A perfect normalized transport, T#mu_A=mu_B, makes r identically rho=Z_B/Z_A, giving

lambda=(1+min(rho,1/rho))/2 >= 1/2.

This removes the cost of geometric separation only after perfect transport and conditional sampling have been supplied. For a perfect map, q=p_B makes both branches accept surely, but that optimum uses the initially unknown answer. Predictable online estimates of q preserve correctness, without guaranteeing a fast convergence rate to that optimum.

For equal-weight unit-variance Gaussian phases with residual displacement e after applying the map, the fair-branch acceptance is 2 Phi(-|e|/2). At e=12, the expected attempt count is about 5.07e8. Thus even a formally correct race can retain an exponential overlap problem. A finite training run that appears to learn a useful map is not a dimension-uniform theorem about learning cost or overlap.

For completeness, a many-phase composition is possible. From current phase i, choose another phase j uniformly, then use the exact two-phase race to resample between i,j. Its transition probability is P(i,j)=pi_j/((k-1)(pi_i+pi_j)), i!=j. Detailed balance holds. Both off-diagonal and diagonal entries satisfy P(i,j)>=pi_j/(k-1), so total variation contracts by at most 1-1/(k-1) per update. This gives O(k log(1/epsilon)) pair updates, but each update still pays the full conditional-sampling and overlap bill. It is an ordinary pairwise heat-bath construction, not a new universal mixing theorem.

## 5. Close both access assumptions for a broad explicit family

Consider phase i with x=m_i+A_i z, A_i invertible, and

w_i(x)=exp[-c_i-||z||^2/2-V_i(z)],
L_i <= V_i(z) <= U_i,

where the bounds, affine data, relative c_i, and potential evaluations are available. Write W_i=V_i-L_i in [0,R_i], R_i=U_i-L_i, and let phi be standard Gaussian measure. Then

B_i=exp[-c_i-L_i]|det A_i|(2 pi)^(d/2),
s_i=E_phi exp[-W_i],
Z_i=B_i s_i.

A conditional sample is constructive: draw z from phi, accept with probability exp[-W_i(z)], return m_i+A_i z. The expected number of reference proposals is 1/s_i<=exp(R_i), without any partition-function oracle.

The explicit map T_ij(x)=m_j+A_j A_i^{-1}(x-m_i) aligns the common reference. Choose the known source-i branch probability q=B_j/(B_i+B_j). The acceptance functions become min(1,exp[W_i-W_j]) and min(1,exp[W_j-W_i]).

Put I=E_phi min(exp[-W_i],exp[-W_j]) and D=(B_j/s_i+B_i/s_j)/(B_i+B_j). One race attempt succeeds with probability D I and spends D expected reference proposals obtaining its conditional sample. A renewal calculation gives the exact mean reference-proposal cost per emitted label:

D/(D I)=1/I <= exp(max(R_i,R_j)).

All potentials and affine arithmetic still count. A straightforward dense implementation has O(d^3) factor setup and O(d^2) affine work per applicable operation, in addition to the supplied potential-evaluation cost. R_i=O(log d) yields a polynomial reference-proposal bound; extensive R_i proportional to d does not.

## 6. Decisive dominance by ordinary global rejection

The same available operations already implement a simpler sampler. Choose phase i with probability B_i/(B_i+B_j), draw z from phi, and accept exp[-W_i(z)]. An accepted pair (i,z) is a complete exact equilibrium configuration. Its success probability is

s_global=(B_i s_i+B_j s_j)/(B_i+B_j).

Pointwise, min(exp[-W_i],exp[-W_j]) is no larger than their B-weighted average. Therefore I<=s_global and

expected direct proposals = 1/s_global <= 1/I = expected race proposals per label.

Direct rejection evaluates only the selected potential for each proposal, whereas the race also evaluates the other phase's potential in its comparison. The race then needs another conditional sample to output a full configuration. Hence the direct method wins before those additional costs are included.

The label-only inequality just proved is for q=B_j/(B_i+B_j). It must not be advertised as applying to every branch choice or every adaptive allocation. A stronger comparison for full configurations does cover arbitrary phase-label algorithms followed by a fresh rejection-based conditional sample: the expected reference cost of that final draw alone is p_i/s_i+p_j/s_j=(B_i+B_j)/(B_i s_i+B_j s_j)=1/s_global. This already equals the entire direct-rejection cost; all work spent selecting the phase is additional. Thus arbitrary adaptive q does not rescue a full-configuration advantage within this resample-after-label architecture. This statement does not exclude a different algorithm that constructs a correctly distributed configuration without the additional conditional draw.

This proof extends immediately beyond Gaussians to any exactly sampleable common reference distribution phi, with known factors B_i and evaluable acceptance weights a_i in (0,1]. It also extends to labelled coordinates connected by a known bijection. The Gaussian representation is a concrete scientific family, not an essential restriction of the dominance argument.

The result is a rejection criterion for this research direction. It is not a theorem that every possible implementation of phase-conditional sampling, or every transport-based algorithm, must be dominated. For example, black-box external conditional samplers might provide a different access model. No broadly useful closed model with a proven advantage under such alternative access has been established here.

## 7. Finite verification and a genuinely finite target

Three reproducible programs are included.

`verify_transport_race.py` tests the flux identities by quadrature for 36 combinations of displacement, energy offset, and branch probability. The largest implied phase-probability error was 3.37e-11. For two separated Gaussians with true p_B=0.25 and 50,000 labels, a fixed exact map, a continually learned map, and a continually learned map plus branch probability all agreed within the stated Hoeffding interval. Mean attempt costs were 1.49836, 1.49904, and 1.0154. These examples check the predicted invariance under adaptation, not a general training guarantee.

`verify_closed_family.py` uses bounded sinusoidal perturbations with B_A=1 and B_B=3. Quadrature gives p_B=0.876910409. The race's expected reference-proposal cost is 4.88817 per label; direct rejection costs 2.17005 per complete configuration. The 20,000-output runs measured 4.8693 and 2.17745 respectively.

`verify_finite_spin_family.py` uses a finite reference of 16 independent fair spins and two labelled phase energies k_i(z) log(2), where the nonnegative integer k_i is computable from domain-wall and half-chain counts and is bounded by six. Acceptance weight 2^(-k_i) is implemented using k_i fair bits, with no exponential-function evaluation. The known factors are 1 and 3, so branch probabilities are exact two-bit coins. Exhaustive enumeration of 65,536 states gives

s_A=115163/524288,
s_B=906797/4194304,
I=595861/4194304,
p_B=2720391/3641695.

The exact expected reference-proposal costs are 7.03906448 for one race label and 4.60697999 for a full direct-rejection configuration. The 20,000-output runs measured 7.0406 and 4.6048. Each reference draw uses 16 fair bits; each conditional acceptance uses at most six; the final race comparison uses at most six additional bits. Potential evaluation is finite integer arithmetic. Correctness is under independent fair input bits, the usual randomized-algorithm model; seeded pseudorandom tests verify the implementation rather than establish physical randomness.

## 8. Strong ordinary comparators

Bennett acceptance-ratio estimation directly attacks the scalar free-energy ratio using bidirectional equilibrium observations. Bridge sampling and MBAR generalize the use of overlapping ensembles. An exact-label output is a different deliverable from an efficient scalar estimator; discarding a rich sample into an acceptance bit does not establish superior statistical efficiency. [Bennett 1976](https://www.sciencedirect.com/science/article/pii/0021999176900784); [Shirts and Chodera 2008](https://pmc.ncbi.nlm.nih.gov/articles/PMC2671659/).

Coordinate maps that reduce free-energy overlap problems are already central to targeted free-energy perturbation. Adaptive learned transports are also established in modern free-energy estimation and flow-augmented Monte Carlo. The Gaussian illustration is therefore not evidence that this construction originates the use of maps or online learning. [Jarzynski 2002](https://arxiv.org/abs/cond-mat/0109461); [Gabrié, Rotskoff and Vanden-Eijnden 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8915891/); [He et al., FEAT](https://arxiv.org/abs/2504.11516).

Bernoulli races already implement exact selections from weights that are accessible through coins rather than explicit normalizing constants. The mechanism here is a particular shared-flux coin construction, with a self-contained predictable-adaptation proof. A priority claim would require more detailed literature comparison than the evidence currently supports. [Schmon, Doucet and Deligiannidis 2019](https://proceedings.mlr.press/v89/schmon19a.html).

An ordinary independence Metropolis sampler using a learned global proposal can maintain a known equilibrium law, but exact independent output requires additional assumptions or perfect-sampling machinery. This distinction does not rescue the present closed family: known envelopes already permit the direct exact rejection method in section 6. Nor does arbitrary online adaptation automatically preserve a general MCMC invariant law; the cancellation proof here is the reason this particular accepted-label process is valid.

For convex or log-concave basins, ordinary annealing, rounding, sampling, and integration algorithms already give polynomial complexity under explicit oracle/geometric premises. Replacing the bounded-perturbation rejection step with such machinery would require deriving its actual conditioning, initialization, tolerance, and training costs, then comparing total work. There is no basis here to claim superiority over those equally informed algorithms. [Lovász and Vempala, Fast Algorithms for Logconcave Functions](https://faculty.cc.gatech.edu/~vempala/papers/integration.pdf); [Lovász and Vempala 2006](https://www.sciencedirect.com/science/article/pii/S0022000005000966); [Cousins and Vempala](https://arxiv.org/abs/1409.6011).

## Final scientific status

The exact algorithm, its adaptive cancellation, its sampling cost, its failure of overlap, its approximation interface, and its finite implementation are explicit. The decisive comparison is also explicit: the strongest closed family reached here is dominated by ordinary global rejection using the same information. I do not recommend selecting this as the programme's promised consequential scientific endpoint. It is useful supporting machinery and a concrete reason to reject an attractive but misleading oracle-level advantage claim.
