# Acquired collective kinetics with a relative-energy certificate

Principal construction, version 1. Status: proofs supplied below, not yet cross-reviewed. No claim of historical priority. Fast stirring, conditional expectation, stochastic averaging, and finite kinetic tables are established mechanisms.

## 1. Nonautonomous relative-form stability

Let A_t,C_t be positive self-adjoint matrices in a fixed Hilbert space H, piecewise continuous in time. Suppose, for all v,w,

|<v,(A_t-C_t)w>| <= d E_Ct(v)^(1/2) E_Ct(w)^(1/2), with d<1.

Write D(d)=d/[2 sqrt(1-d)]. Evolution under -A_t and -C_t satisfies

||U_A(T,0)-U_C(T,0)|| <= min(2,D(d)), for every T.

Proof. A_t >=(1-d) C_t. Pair Duhamel with f,g and put h_t=U_A(T,t)^*g, k_t=U_C(t,0)f. Its integrand has absolute value at most d/sqrt(1-d) sqrt(E_At(h_t)) sqrt(E_Ct(k_t)). The two energy integrals are at most ||g||^2/2 and ||f||^2/2, respectively: reverse time in the first equation. Cauchy-Schwarz proves the assertion. No spectral gap or regularity of the drive derivative is used. The common Hilbert metric is indispensable.

## 2. Relative coarse coupling

Let F>=0 and B_t>=0 be negatives of reversible Markov generators for a common full-support pi. Let P be orthogonal conditional expectation onto a partition, ker F=ran P, Q=I-P, and F>=gamma Q. Set A=F+B and C=PBP+QAQ. If

||QBP f||^2 <= C_c <f,PBP f> for all Pf=f,

then ||(QAQ)^(-1/2) QBP (PBP)^(-1/2)|| <= sqrt(C_c/gamma)=d. Inverses are on positive ranges; the displayed inequality makes the off-diagonal map vanish on the retained kernel. Block Cauchy-Schwarz gives the hypothesis of section 1 for A,C.

For a retained norm-one observable g, and any initial density f=dmu/dpi, the microscopic mean differs from evolution of the retained marginal under PBP by at most ||f||_2 D(d). This holds for arbitrary time-dependent B_t preserving pi. It also holds for sub-Markov killed dynamics when the killed set is a union of whole fibers: restrict both forms to its complement. No assumption on the macroscopic gap is made.

The cruder always-valid estimate is C_c=||B_t||. Indeed ||QBP f||^2<=||B|| <f,Bf>, since B>=0. A local fluctuation calculation can give a much smaller C_c.

## 3. Explicit count-energy model, including strong nonconvex collective interactions

Partition N binary sites into disjoint blocks V_r of sizes m_r. Each block has a connected physical swap graph with random-walk gap lambda_r. At rate kappa per unit edge conductance, exchange two neighboring spins. Its positive generator is F. The energy is a supplied efficiently evaluated function U(k), k_r=sum_(i in V_r) x_i, with bounded one-spin energy increments |Delta_r^+/- U|<=J. U may contain arbitrary bounded-degree interactions between block counts and nonconvex potentials of order m_r; no convexity or macroscopic mixing is required.

Each site has a known type and a known within-block neighborhood N_i, excluding i. At most d neighbors enter a mobility, and each spin enters at most d such neighborhoods. The unknown shared finite table b(type,neighbor pattern) lies in [b_min,b_max], b_min>0. The physical slow rate to flip i is

c_i(x,t)=b(type_i,x_Ni) a(type_i,x_Ni,t) exp[-beta (U_t(k(x^i))-U_t(k(x)))/2].

Known kinetic multipliers a lie in [a_min,a_max], depend on neighbors but not the central spin, and are the same in forward and reverse flips. Future U_t may be a new time-dependent collective energy with the same locality/evaluation and increment bounds. Controls may be chosen after acquisition. The table b itself and its reuse across sizes are physical class assumptions.

Conditional on counts, the Gibbs law is exactly product uniform on the count shells, independent of U_t. Therefore P is explicit and constant even under thermodynamic driving. For fixed U, all kinetic drives preserve the same pi(x) proportional exp[-beta U(k(x))]. The coarse equilibrium weights are proportional [product_r binomial(m_r,k_r)] exp[-beta U(k)].

Caputo-Liggett-Richthammer, Theorem 1.1 and section 4.1.1 (0906.1238v3), imply gamma=kappa min_r lambda_r. Empty/full shells have no Q component. Tensor products preserve this minimum gap. These are finite Markov generators, so the stated hypotheses hold directly.

## 4. Computable coarse rates and size transfer

For a type with d_t specified neighbors, a pattern alpha with j ones, conditional on a zero central spin in a block of count k and size m, has probability

p_+(alpha|k,m)=(k)_j (m-k-1)_(d_t-j)/(m-1)_(d_t).

For an occupied central spin, replace k by k-1 and m-k-1 by m-k. A negative falling factorial count means zero. Each pattern is a specified binary string, so no additional binomial factor is included. Sum over all alpha and multiply by (m-k)/m or k/m, the number of sites of that type, and the known exponential energy factor. This is the exact PBP birth/death rate in block r. Evaluate by finite combinatorics, never by a microscopic partition function. If m<=d_t, evaluate the finite feasible shell directly; alternatively require m>=d+1.

The local table has D_tab=sum_types 2^(d_type) entries. Dense preprocessing of all local count configurations is optional. A generator query costs O(B D_tab d) plus the supplied cost of all local energy differences, or O(D_tab d) per selected block. Exact reuse across different m follows from the declared shared table and the hypergeometric identity. Finite experiments cannot certify this structural promise for arbitrary future sizes.

## 5. Size-independent conditional fluctuation bound

Set b'_max=b_max a_max, b'_min=b_min a_min, C_E=exp(beta J/2), and L_s=2(d+1)b'_max. Swapping a pair of spins changes S_r^+(x)=sum_(i in V_r, x_i=0) b_i a_i by at most L_s. It changes only the two central indicators and the at most 2d affected neighbor-dependent mobilities. The same bound holds for S_r^-.

The complete-graph exchange generator with rate one per unordered pair has gap m (elementary diagonalization or the same exclusion theorem). Its Poincare inequality yields, on a uniform k shell,

Var(S_r^+) <= [L_s^2/(2m)] k(m-k) <= (L_s^2/2)(m-k),

and Var(S_r^-) <=(L_s^2/2)k. Since E S_r^+>=b'_min(m-k) and E S_r^->=b'_min k,

Var(q_r^+/-) <= V_0 E q_r^+/-, with V_0=C_E L_s^2/(2b'_min).

Here the exponential energy factor is constant on a count shell. Conditioned on all counts, different blocks' fluctuations are independent: the mobilities depend on microscopic spins within their own block only. Both signs in one block may correlate, so use Var(X+Y)<=2Var(X)+2Var(Y). Thus

||QBP f||^2 <=4 V_0 E_coarse(f).

Consequently C_c=4V_0=2 C_E L_s^2/b'_min is independent of the number of blocks and the block sizes. The physical swap graph used in F need not be complete: the complete graph here is only a mathematical variance inequality under the known uniform conditional measure. Hardware still pays kappa on the actual declared swap graph.

This is the crucial proved improvement over the crude total exit-rate estimate. The retained count field may be strongly interacting and may have an exponentially small gap.

## 6. Acquisition of the unknown kinetic table

During calibration set U=0, pause stirring, clamp the specified neighbors in alpha, and prepare the central spin zero. The central spin is a symmetric two-state chain of rate b, hence its flip probability at h is p_b=(1-exp(-2bh))/2. Choose h=1/(4b_max). Estimate p_b with calibrated binary readout contrast v>0 and a warranted total residual mean bias e_p. Projection onto the known probability range can only help; b=-log(1-2p)/(2h) is Lipschitz at most L_b=exp(2b_max h)/h on that range.

N_cal >=[log(2 D_tab/delta)/(2 v^2 eta_p^2)] trials per entry give stochastic probability error eta_p, hence mobility error L_b(eta_p+e_p), plus separately accounted calibration-field and clock bias. To obtain relative mobility error eta, require L_b(eta_p+e_p)<=eta b_min. More shots do not reduce e_p. Every trial pays central reset, neighbor clamps, stirring control, readout and h; finite precision of all known factors is budgeted likewise. No whole-system thermal preparation is used in this table acquisition. If mobilities lack a shared finite dictionary, the table size increases accordingly; no hidden discovery theorem is asserted.

All learned mobilities are clipped positive. Uniform relative error of the table implies the same relative error of every synthesized nonzero coarse jump rate under every permitted new U_t and kinetic drive. It also preserves detailed balance exactly when U is fixed, because the same learned neighbor mobility is used in both directions.

## 7. End-to-end reuse: two distinct contracts

### A. Fixed new U, arbitrary later kinetic drive, all horizons

Let d=sqrt(C_c/gamma)<1. Let eta<1 be the acquired relative table error. For a count observable |g|<=1 and any initial microscopic density f with ||f||_L2(pi_U)<=W, predict with the learned coarse generator. The error is at most

W [D(d)+D(eta)] + error_initial_count + error_numerical.

The first term is section 2; the second is section 1 applied to the coarse Dirichlet forms, which share pi_U. The statistical event is one uniform table event, so arbitrary adaptive future numerical queries remain covered. U may be a new extensive nonconvex energy, but must be fixed during this all-horizon statement. Preparing a W-warm source relative to a new U is a separate operation. Phase-conditioned equilibrium with phase weight a has W=a^(-1/2); arbitrary sharply prescribed sources need not have bounded W.

### B. Arbitrary initial microscopic state and changing collective energy, finite horizon

In this paragraph write S_t=-B_t for the slow Markov generator (B_t elsewhere is positive). Let L=sup_t ||S_t||_(infinity->infinity)<=2 N b'_max C_E, V_B total operator variation of S, and tau_F=integral_0^infinity ||exp(-tF)Q||_(infinity->infinity) dt. Direct Poisson/Dynkin calculation gives a terminal observable error no greater than

tau_F [4L+2 V_B+6 T L^2].

Proof: g_t solves the backward coarse equation and ||g_t||<=1. Set R=integral exp(-sF)Q ds, so FR=Q; h_t=R S_t g_t has ||h||<=2 tau_F L conservatively. Differentiate h in intervals, sum jumps, and apply Dynkin: the two boundary terms cost4 tau_F L; derivative variation costs2 tau_F V_B; g'_t and B_t h_t cost at most4 tau_F T L^2, so6 is safe. No exponential Gronwall. Sources with the same initial count law may differ arbitrarily inside a shell.

For finite uniform shells, ||exp(-tF)Q||_infinity <=min(2,sqrt(D_max)exp(-gamma t)); hence tau_F <=[2+log D_max]/gamma <=[2+N log2]/gamma. This sufficient bound is polynomial in microscopic volume; the exponential number of shell states appears only through its logarithm. A sharper exclusion mixing bound can improve it but is not needed for validity.

Learned-rate error is bounded by relative path entropy. For |qhat/q-1|<=eta<1 and total coarse exit rate<=R_s=N b'_max C_E, path KL <=R_s T eta^2/[2(1-eta)^2]. Therefore bounded terminal observable error <=eta sqrt(R_s T)/(1-eta). Add initial count-law error, instrument bias and evaluation error. This does not assert a path-law approximation for the microscopic projection itself. Finite-state path monitors require an additional explicit augmentation proof.

The sufficient stirring and calibration precision grow polynomially with N,T and inverse error. At fixed separation there is NO claim that this second certificate stays small as T grows without bound. Infinite-history, arbitrary regularity and free control switching are not granted: V_B and drive evaluation are charged.

## 8. A consequence not requiring exponentially accurate kinetics

For fixed U and a count target set, kill the process upon entry into the target, and assume all transient components reach it. In section 2 the Schur complement S=A_00-A_01 A_11^(-1)A_10 satisfies

(1-d^2) A_00 <=S<=A_00.

For initial Gibbs equilibrium conditioned on the entire transient set C, mean hitting time is <1,A^(-1)1>_pi/pi(C). Since P1=1 and P A^(-1)P=S^(-1), the exact microscopic mean lies between the exact coarse mean and that mean divided by 1-d^2. Learned same-pi coarse conductances within relative eta give mean lifetime within multiplicative factors 1/(1+eta),1/(1-eta). Thus combined mean-time comparison has a controlled RELATIVE error, even when the lifetime is exponentially large. This statement is about the specified equilibrium-conditioned source, not all starting states.

For one block there are only m+1 coarse states. Coarse mean hitting time is computable by tridiagonal linear algebra (or the standard birth/death positive-sum formula), with polynomial bit precision in m and the bit lengths of U, rates and the output logarithm. No exponentially long dynamical calibration is necessary when the local rate increments remain bounded and the conditional source can be prepared by sampling known count weights and uniformly placing spins. For growing numbers of blocks, computing those weights or solving the coarse rare-event problem can itself be hard; this consequence does not grant a general large-lattice rare-event solver.

## 9. Costs and status

Hardware: N sites, declared local swap graph, stirring rate kappa, finite table calibration controls and bounded increment fields. Actual swap-event cost scales as kappa times graph total conductance; heat/work/control fidelity must be supplied for the apparatus. Pausing stirring and clamping are physical controls, not consequences of statistical inference. Prediction does not reenact the target experiment.

Preprocessing: O(D_tab N_cal) calibration records at stated bit precision; construct counts, binomials and tables in polynomial costs. For a growing count lattice, Monte Carlo prediction of one bounded observable to numerical error epsilon_MC and failure delta_MC costs O(epsilon_MC^(-2)log(1/delta_MC)) independent trajectories, each O(R_s T) expected coarse jumps, plus actual sparse energy/control evaluation. A hard runtime cap adds the appropriate Poisson tail. Initial count sampling and observable evaluation are charged. Storing a full coarse matrix costs product_r(m_r+1)^2 and is NOT polynomial in a growing number of blocks. For a fixed number of blocks it is polynomial in N, and time-homogeneous horizons may be evaluated by certified stochastic scaling/squaring in polynomial log T arithmetic.

Established: a concrete acquired predictor with two different proved certificates, explicit conditional sufficiency and exact combinatorial closure, plus a relative lifetime consequence. Limitations: special count-energy/fast-stirring structure, shared finite mobility dictionary, calibrated clamps and known energy, common-pi/warmness requirement for all-time reuse, growing resource requirement for generic thermodynamic drives, no general representation discovery or generic-fluid theorem. Existing conditional averaging, rapid stirring, stochastic lattice coarse graining and metastability comparators must be checked before claiming novelty or superiority. The broad user objective remains OPEN unless a stronger independent route closes these restrictions.
