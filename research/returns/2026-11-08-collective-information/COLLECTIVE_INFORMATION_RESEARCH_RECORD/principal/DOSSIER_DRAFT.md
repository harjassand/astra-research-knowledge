# Constructed collective information for new preparations and drives

Research dossier, 7 November 2026. **The broad requested breakthrough remains OPEN / NOT ACHIEVED.** No historical priority, physical validation or practical advantage is asserted.

## 1. Strongest result actually achieved

We obtained an acquired collective predictor for a specified class of interacting block populations, including nonconvex collective energies and very slow phase switching. Its error can be bounded without the inverse macroscopic relaxation gap. Positive kinetic estimates plus a mass-metric repair allow reliable predictions at all frozen-control horizons without calibration precision proportional to an exponentially rare transition rate. The predictive object contains count-resolved positive rates and equilibrium weights, rather than an unknown many-body functional. Within the explicit access model it is constructed once and evaluated for new permitted preparations and drives without performing their target experiment or solving the microscopic state again.

The scientific principle established at this scope is: **retain the slow collective sector; control discarded kinetic fluctuations relative to collective dissipation; acquire positive conditional rates and masses; then propagate a finite stochastic law with the appropriate common-metric, mass-metric or finite-horizon certificate.** The relative-energy certificate is derived for the physical class, not simply postulated for arbitrary matter.

This does NOT establish a general representation-discovery theorem or a new law of generic interacting matter. The successful class has supplied count coordinates, controlled internal mixing and strong local calibration rights. Strong collective interactions are allowed; arbitrary strongly interacting discarded sectors are not proved tractable. The retained spatial field can itself remain hard to evaluate. The strongest equal-information incumbent can use established conditional averaging, reversible-network methods and coarse kinetic Monte Carlo. Superiority over that incumbent has not been shown.

The main complete theorem is Part A below, with its exact physical, preparation, noise, source-warmness and control assumptions. Part B repairs estimated stationary weights. Part C derives interacting-shell conditional acquisition and its resource bounds. Part D expands thermodynamic drives and constructs noisy preparation. Part E proves numerical evaluation costs. These contracts are distinct: one must not combine their conclusions while dropping their additional hypotheses.

### The resulting operation

For N binary sites in B blocks, the acquired descriptor is a finite positive mobility/conditional-rate table, count-shell weights or their ratios, geometry, and calibrated uncertainty bounds. A query supplies a computable permitted collective energy, kinetic protocol, initial count law/source certificate and bounded count observable. It returns an expectation interval (or a probability interval for an effect), clipped to its physical range. A single acquisition event covers adaptive selection of numerical queries satisfying the budgets; this does not grant arbitrary measurement-feedback control of the physical dynamics. Monte Carlo evaluation adds its own per-query failure budget; physical fluctuations are separate from epistemic uncertainty.

At a fixed number of blocks, q=product_r(m_r+1) is polynomial in N, so frozen-generator evaluation is polynomial in q, log(T+1), input bits and requested numerical precision. At growing B the full count grid is exponential. Ordinary sparse coarse trajectories are polynomial in T, not log T. The theorem does not conceal a large coarse solve inside the word collective.

For all residual W_r identically zero, known energies and a common equilibrium law, if z=sqrt(C_c/gamma)<1 and the learned positive mobility table has relative error eta<1, every bounded retained readout from an ideal source of L2 Gibbs warmness W has error at most

W[z/(2sqrt(1-z))+eta/(2sqrt(1-eta))]+2 zeta_source+epsilon_eval.

This holds for all horizons and arbitrary prescribed kinetic protocols preserving that law. The explicit derived C_c is independent of total block number and block sizes; gamma is the physical conditional swap gap. Changing thermodynamic fields has a bounded-action theorem, or a separate finite-horizon/arbitrary-source theorem. Unknown empirical masses use the autonomous repair in Part B; they do not automatically inherit arbitrary switched common-metric control.

An additional relative mean-lifetime theorem handles a count target from Gibbs conditioned on its ENTIRE transient complement. It can certify an exponentially large mean with polynomial kinetic precision. It does not turn TV-only preparation error into relative accuracy of an unbounded hitting observable. Part D supplies the stronger noisy-source repair and charges its growing pin energies.

### Scientific status

- PROVED at stated finite-state assumptions: relative-energy and mass-metric lemmas, volume-independent fluctuation bound, exact count-rate synthesis, finite-noisy table acquisition, finite-horizon reuse, thermodynamic-action reuse, noisy pin writer, killed Schur and relative mean-lifetime comparison, stochastic numerical evaluation.
- CONDITIONAL ON AN ACTUAL QUANTITATIVE GAP/APPARATUS CERTIFICATE: efficient interacting-shell acquisition beyond the uniform-shell model. The primary high-temperature Kawasaki theorem supplies a class; it does not supply generic low-temperature mixing.
- OPEN: discover sufficient variables for general short-range strongly interacting matter; obtain generic efficient conditional kinetics; preserve efficient accuracy under extensive changing fields and growing independent controls; efficiently evaluate a growing noncontractive collective field at rare-event horizons.
- UNKNOWN: historical novelty of the particular composition and estimates. NOT ESTABLISHED: consequential matched practical advantage or the larger foundational capability.
- Physical experiments performed: zero. All numerical records below are synthetic checks supplementing analytic proofs.

Earlier Gibbs, thermal-memory and P1/P2/P3 capital remains intact at its recorded scope. No theorem from it is a load-bearing premise here. The Astra retrieval connector was unavailable; local pinned records and primary literature were used. This dossier is a research return, not a manuscript or publication instruction.

## 2. Reading and dependency map

The main mathematical dependence is finite reversible Markov dynamics -> conditional count projection -> a derived local fluctuation inequality -> gap-free evolution comparison. Known exclusions supply the actual conditional graph gap. Statistical calibration supplies positive kinetic coefficients. Estimated masses require the separate contour proof. No Mori–Zwanzig closure, a learned neural functional or an unspecified orthogonal propagator is imported as a computational oracle.

Full derivations and independent challenges are retained in the supporting record. Parts A–E reproduce the load-bearing proof developments. Independent alternatives, exact primary-source review, obstructions and the unresolved frontier follow them. The initial reports are preserved without retroactive editing; a brief principal-result description reached the constructor before its written freeze, after it reports having formulated its own route. This boundary is disclosed in the record and is not described as four sealed written returns.

# Part A. Main explicit construction and proofs

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

Caputo-Liggett-Richthammer, Theorem 1.2, Corollary 1.3 and section 1.2.3 (0906.1238v3), imply gamma=kappa min_r lambda_r. Empty/full shells have no Q component. Tensor products preserve this minimum gap. These are finite Markov generators, so the stated hypotheses hold directly.

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

# Part B. Estimated stationary masses: autonomous repair

Principal follow-up, proof independently checked by the three reviewers; not part of the frozen initial. No priority claim.

Let A,C>=0 be self-adjoint matrices in one Hilbert space. Suppose |<v,(C-A)w>|<=d <v,Av>^(1/2)<w,Aw>^(1/2), and M>0 satisfies ||M-I||<=d<1. Put B=M^(-1)C. Checked gap-free bound:

sup_(t>=0)||exp(-tA)-exp(-tB)|| <=8d/(1-d).

For z outside |arg z|<pi/3, scalar spectral calculus gives ||(z-A)^-1||<=2/(sqrt3 |z|), ||A^(1/2)(z-A)^-1||<=|z|^-1/2, ||A(z-A)^-1||<=2/sqrt3. Write H=M^-1/2 C M^-1/2. Then ||(zM-C)^-1||<=2/[sqrt3(1-d)|z|] and ||(zM-C)^-1 C^1/2||<=1/[sqrt(1-d)sqrt(|z|)]. Since C>=(1-d)A, replace C^1/2 on the right by A^1/2 at cost (1-d)^-1/2. These estimates hold also on the left by adjunction.

Resolvent identity:
(z-B)^-1-(z-A)^-1=(zM-C)^-1[(C-A)-(M-I)A](z-A)^-1.

The two terms are bounded by d/[(1-d)|z|] and 4d/[3(1-d)|z|], hence total <=3d/[(1-d)|z|].

For t>0 use Dunford contour rays arg z=+/-pi/3, |z|>=1/t joined by the LEFT arc |z|=1/t, pi/3<=arg z<=5pi/3. Close at large radius in the right sector, beyond all (finite) eigenvalues, then pass to infinity. This contour encloses nonnegative spectra including zero. Small arc contributes <=(2e/3)*3d/(1-d). Rays contribute <=3d/[pi(1-d)] times integral_1^infinity exp(-r/2)/r dr; this integral is <1: split at 2 to obtain at most 2exp(-1/2)-exp(-1)<1. Thus total <8d/(1-d). At t=0 trivial. No gap/inverse A is used. This is likely standard analytic-semigroup perturbation; novelty UNKNOWN.

## Reversible-chain application
True positive generator A is self-adjoint in L2(pi), learned generator B in L2(pihat). Define M=diag(pihat/pi), C=M B. Its quadratic form uses learned conductances pihat(x) qhat(x,y). If pointwise relative mass error <=d_m and edge-rate relative error <=d_q, form error <=d_m+d_q+d_m*d_q. Apply the lemma with d at least this and d_m, if d<1. Forecast error for |g|<=1 and initial density f is <=||f||_L2(pi)*8d/(1-d), plus source/numerical error. This repairs changed equilibrium weights for FROZEN control, not arbitrarily switched estimated metrics.

## Acquisition implication requiring physical checking
For energy U(k)+sum_r W_r(microblock), conditional Gibbs mu_(r,k) is independent of U. Acquire positive bare coarse rates a_r^+(k),a_r^-(k) by count-clamped conditional mixing then local rate probes (avoid noisy full-count inversion). Detailed balance implies Z_r(k)a_r^+(k)=Z_r(k+1)a_r^-(k+1). Positive estimates define what_r(0)=1, what_r(k+1)/what_r(k)=ahat_r^+(k)/ahat_r^-(k+1). The future learned generator with rates ahat_r^+/-(k_r) exp[-beta Delta_r U/2] is exactly reversible in pihat_U proportional exp(-beta U) product_r what_r(k_r).

If all bare rates have relative error eta<=1/2, log ratio errors <=4eta. With N=sum_r m_r, unnormalized log weight error <=4Neta and normalized |log(pihat_U/pi_U)|<=8Neta, UNIFORMLY in the new U. Thus d_m<=exp(8Neta)-1, giving fixed-control all-time error O(W Neta), polynomial precision eta=O(epsilon/(WN)) instead of 1/T. Must derive polynomial conditional mixing, local-rate measurement/noise conditioning, state preparation and all costs. No arbitrary strongly interacting shell promise is granted. For growing number of blocks, a full coarse matrix still has exponentially many count states; ordinary simulation remains O(T). Only fixed block number can use polynomial-log(T) matrix evaluation.

# Part C. Interacting conditional shells and acquired weights

## 3. Residual microscopic interactions: full conditional-variance extension

Take

\[
 E_t(x)=U_t(k(x))+\sum_r W_r(x_{V_r}).\tag{F1}
\]

Each W_r is fixed, known, finite range and bounded locally. Its one-spin and exchange increments are bounded by J_W,J_sw. Beta is fixed. There are no residual microscopic interactions across blocks; U_t may couple counts arbitrarily within its declared increment/evaluation budget. Changing W, beta or block size requires new conditional compilation/acquisition.

The exact conditional law is nu_{r,k}(x)=Z_{r,k}^{-1} exp[-beta W_r(x)] 1_{|x|=k}, independent of every future U_t. Hence P is fixed. Fast stirring MUST use W-reversible Kawasaki rates kappa exp[-beta Delta_swap W/2], not uniform swaps. Slow flips have rate

\[
 b_i(x_{N_i})a_i(x_{N_i},t)
 e^{-\beta\Delta_iW_r/2}e^{-\beta\Delta_rU_t/2},\tag{F2}
\]

with b,a excluding the central spin so they agree on a flip and its reverse.

**Exact import:** Boudou–Caputo–Dai Pra–Posta, arXiv:math/0505533v2, Theorem 3.1 uses normalized complete-graph rates m^{-1}exp(-beta Delta W/2). Its norm assumption is sup_i sum_{A containing i}|A|sup|Phi_A|<infinity. At sufficiently small beta it gives a gap lambda_*>0 uniformly in volume, density and boundary conditions. For finite-range potentials Corollary 3.3 gives the nearest-neighbor gap c_beta/diam(V_r)². Choose standard lattice blocks or verify the comparison-path geometry; finite diameter alone does not cover arbitrary disconnected regions. Multiplication by kappa scales the gap. Constants must be extracted with the actual potential/rate normalization; a spectral gap is not automatically a uniform LSI. [Primary text](https://arxiv.org/html/math/0505533v2); cache `source/0505533v2.{html,txt}`.

Put w_min=b_min a_min exp(-beta J_W/2), w_max=b_max a_max exp(beta J_W/2), K_sw=exp(beta J_sw/2). If a spin affects at most s local slow summands, swapping a pair changes each S_r^+/- by at most L_s=2s w_max. The normalized complete-graph W-Kawasaki Poincare inequality gives

\[
 \operatorname{Var}_{\nu_k}(S_r^+)
 \le\frac{K_{sw}L_s^2}{2\lambda_*m}k(m-k)
 \le\frac{K_{sw}L_s^2}{2\lambda_*}(m-k),
\]

and the minus bound uses k. Means are at least w_min(m-k) and w_min k. Therefore the principal proof extends with

\[
 V_W=\frac{e^{\beta J_U/2}K_{sw}L_s^2}{2\lambda_*w_{min}},\quad
 C_c=4V_W,\quad
 \gamma_F\ge\kappa\min_r c_\beta/\operatorname{diam}(V_r)^2.\tag{F3}
\]

Conditional blocks remain independent. This is a real nonuniform interacting-shell extension with d²=C_c/gamma_F and no macroscopic gap.

## 4. Conditional acquisition: actual mixing, measurement and calibration costs

At fixed m,W,beta, acquire all conditional local pattern probabilities needed by Delta_i W and b,a, for every count k. Let s now bound the required support size and chi be the calibrated single-site detector inverse norm. Corrected local-pattern scores have absolute value <=chi^s. For absolute pattern error delta_p,

\[
 M=O(\chi^{2s}\delta_p^{-2}\log(m^2 2^s/\delta))\tag{F4}
\]

fresh shell samples suffice. To give every forward and reverse total rate relative error eta, uniformly over all allowed positive local kinetic weights, it suffices conservatively to use delta_p=O(eta w_min/[m 2^s w_max]). Near-empty/full counts are why an m factor appears. Include positivity-projection factors, b calibration and systematic bias. The finite support and a_min>0,a_max<infinity are essential. Passive noisy count inversion is not assumed.

Prepare a known configuration of exact count k, pause slow flips, and run W-Kawasaki. Bounded local W gives nu_min>=2^{-m}exp[-beta osc W], with osc W=O(m). Reversibility and the spectral gap give the stronger relative mixing estimate

\[
 |P_t(x,y)/\nu_k(y)-1|
 \le e^{-\gamma_Ft}/\sqrt{\nu_k(x)\nu_k(y)}
 \le e^{-\gamma_Ft}/\nu_{min}.\tag{F5}
\]

Thus TV OR pointwise-relative conditional accuracy epsilon_mix is obtained in O(gamma_F^{-1}[m+log(1/epsilon_mix)]) time. Fresh reset/mix/readout trials are independent; a spaced single trajectory needs a conditional-freshness/martingale argument. Each record pays O(m) reset/readout operations and expected swap count

\[
 O\!\left(\frac{|E|\operatorname{diam}(V)^2}{c_\beta}
 e^{\beta J_{sw}/2}[m+\log(1/\epsilon_{mix})]\right).
\]

Kappa cancels from this event count. There are m+1 shells and M records per shell; all actual bath/work/control costs multiply these counts. No practical advantage has yet been shown.

The residual W changes the two-state calibration. Clamp its required neighbors and pause stirring. Starting at zero, with known Delta W,

\[
 p_b(h)=\frac{1-e^{-2b\cosh(\beta\Delta W/2)h}}{1+e^{\beta\Delta W}}.\tag{F6}
\]

Choose h=[4b_max cosh(beta J_W/2)]^{-1}. Then dp/db>=h exp(-beta J_W/2-1/2), so inverse Lipschitz constant is at most exp(beta J_W/2+1/2)/h. The principal's corrected binary Hoeffding acquisition applies with this constant, detector contrast and warranted systematic bias. The symmetric U=0 calibration formula is wrong if W remains present.

## 5. Frozen-control all-time repair with empirical conditional rates

The principal's recursive-ratio construction is operational after (F4)–(F6). For one block let the positive acquired bare rates a_hat,k^+/- have uniform relative error eta<=1/2. Define z_hat,0=1 and z_hat,k+1/z_hat,k=a_hat,k^+/a_hat,k+1^-. True detailed balance gives the same recursion for Z_k/Z_0. Every log-ratio error is <=4eta. Over all blocks with N total spins,

\[
 |\log(\widehat\pi_U/\pi_U)|\le8N\eta
\]

after normalization, uniformly over every new U. Learned driven rates a_hat,k^+/- exp(-beta Delta U/2) are exactly reversible in pi_hat,U. Put d_m=exp(8Neta)-1, d_q=eta and d=max(d_m,d_m+d_q+d_m d_q). The verified mass-metric lemma gives the learned-vs-exact-coarse observable error <=W 8d/(1-d), for d<1. Add the principal's microscopic averaging term W D(sqrt(C_c/gamma_F)), initial-source error and numerical error.

Hence eta=O(epsilon/[WN]) suffices for **frozen U and frozen kinetic control** at all horizons; acquisition is polynomial in N and inverse error, with the explicit conditional mixing/noise costs above. This closes the empirical-stationary-weight problem without pretending empirical rates preserve the true Gibbs measure. It does not justify arbitrary switching from a finite list of separately symmetrized kinetic tables whose inferred stationary measures differ.

For a fixed number of blocks, the full coarse state count is polynomial in N and a frozen semigroup may be evaluated with polynomial log(T) arithmetic/bit precision. A growing block count has an exponentially large count grid. Ordinary coarse trajectories cost O(T) jumps. These different computational contracts must stay separate.

## 6. Exact offline conditional compilation as an alternative

For a finite-range one-dimensional W, compute Z(z)=sum_x exp(-beta W(x))z^{|x|} with a position/last-r-bits/count dynamic program. All Z_k cost O(m²2^r) arithmetic. Constrain each needed local pattern and repeat; conservative total O(m³2^{O(r+s)}) arithmetic and O(m²2^{O(s)}) retained coefficients give every conditional pattern probability. Future U only multiplies these stored rates, so no conditional microscopic solve is repeated.

The learned b table can then remain inside exact conditional expectations, preserving the true pi_U and the principal's stronger common-pi time-dependent kinetic-drive certificate. General dimensions pay exponential elimination width; this is not a general efficient partition solver. Rational local Boltzmann and half-Boltzmann factors, or factors in one fixed-degree common algebraic field, give exact coefficients with polynomial bit length at fixed range. Unrestricted collections of algebraic numbers need additional degree accounting. General computable-real W needs interval compilation to the declared numerical workload; arbitrary rounded rows must not inherit an ideal infinite-horizon theorem silently. New block sizes need new conditional compilation.

## 8. Positive partition-ratio acquisition and relative lifetime repair

An independent way to obtain one kinetic-control-independent Z_hat table uses the positive insertion identity

\[
 s_k=E_{\nu_k}\left[(m-k)^{-1}\sum_{i:x_i=0}e^{-\beta\Delta_iW}\right],
 \qquad Z_{k+1}/Z_k=\frac{m-k}{k+1}s_k.\tag{F7}
\]

To prove it, multiply the unnormalized shell-k weight by the insertion factor; each shell-(k+1) state appears k+1 times. The positive observable lies between exp(-beta J_W) and exp(beta J_W). Z_0=exp[-beta W(0)] is known. Estimate each log s_k to eps_z/m; accumulated partition error then satisfies |log(Z_hat,k/Z_k)|<=eps_z. The finer 1/m precision is paid.

With local noisy detectors, the corrected insertion score has absolute bound at most m chi^s exp(beta J_W), including k=m-1. A conservative sufficient per-shell sample count is

\[
 M=O(\chi^{2s}e^{4\beta J_W}m^4\varepsilon_z^{-2}
       \log(m^2 2^s/\delta)).\tag{F8}
\]

Conditional mixing and residual detector bias must meet the corresponding absolute mean-error budget. More repetitions do not remove systematic bias. This is a safe polynomial bound, not an optimal or small practical cost. The conditional mixing/readout operations are exactly those already charged above.

Let a_k^+(a) be the conditional forward mobility total. Edge reversal gives M_k(a)=Z_k a_k^+(a)=Z_{k+1}a_{k+1}^-(a), because b and a agree on each microscopic flip and its reverse. Use positive estimates a_hat,k^+(a), uniformly log-relative eps_a accurate over allowed local weights a. Define

\[
 \widehat w_k=\widehat Z_k e^{-\beta U(k)},\quad
 \widehat c_k=\widehat Z_k\widehat a_k^+(a)
 e^{-\beta[U(k)+U(k+1)]/2},\quad
 \widehat q_{k,k+1}=\widehat c_k/\widehat w_k,\quad
 \widehat q_{k+1,k}=\widehat c_k/\widehat w_{k+1}.\tag{F9}
\]

This shared-flux construction is reversible in hat w for every future U and every frozen future a. Its stationary weights do not depend on a. True and learned unnormalized weights differ by exp(plus/minus eps_z), edge conductances by exp(plus/minus(eps_z+eps_a)), and rates by exp(plus/minus(2eps_z+eps_a)). The mass lemma supplies the same frozen-control all-time repair, with no unknown exact partition ratio left over. It does not prove arbitrary switched semigroups even though the learned mass is now fixed.

There is also a direct relative mean-lifetime comparison requiring no semigroup contour. For a transient count set C and killed unnormalized conductance Laplacian K,

\[
 \tau=\frac{w_C^T K^{-1}w_C}{w(C)}.\tag{F10}
\]

If pointwise hat w/w is within exp(plus/minus eps_z) and each conductance ratio is within exp(plus/minus eps_c), quadratic form comparison gives exp(-eps_c)K<=K_hat<=exp(eps_c)K. Its inverse is entrywise nonnegative, as a killed-chain Green matrix. The two positive weight vectors cost exp(plus/minus 2eps_z), inverse comparison costs exp(plus/minus eps_c), and normalization costs exp(plus/minus eps_z). Hence

\[
 e^{-(3\varepsilon_z+\varepsilon_c)}\tau
 \le\widehat\tau\le e^{3\varepsilon_z+\varepsilon_c}\tau.\tag{F11}
\]

For (F9), eps_c=eps_z+eps_a. Combining with the principal's Schur bound yields

\[
 e^{-(4\varepsilon_z+\varepsilon_a)}
 \le\tau_{micro}/\widehat\tau
 \le e^{4\varepsilon_z+\varepsilon_a}/(1-d^2).\tag{F12}
\]

No exponentially small killing gap appears even if tau grows exponentially in m. This compares equilibrium-conditioned mean lifetimes, not arbitrary sources or an exit-time law.

An operational source can be prepared by drawing counts from hat w conditioned on C, loading a known configuration at that count, and running W-Kawasaki to pointwise log-relative error eps_mix using (F5). Its density relative to the true equilibrium-conditioned source lies within exp(plus/minus[2eps_z+eps_mix]). Since hitting times are nonnegative, their actual mean differs by those same multiplicative factors; add 2eps_z+eps_mix to the exponents in (F12). A TV-only preparation promise would not establish such relative control for an unbounded hitting observable. A one-block birth/death positive-sum formula evaluates the learned mean in polynomial arithmetic/bit precision in m, input lengths and log tau. Increasing the number of blocks reintroduces the large coarse-state problem, and blockwise log errors add.

## 9. Supplementary finite check and extra predecessor

`check_residual_shell.py` exhaustively constructs a six-site model with nonuniform nearest-neighbor residual W, count-dependent nonconvex U, local neighbor-dependent mobilities and W-reversible nearest-neighbor swaps. It checks the count transfer polynomial, insertion identity, exact edge-flux identity, conditional coupling/gap certificate, killed mean-lifetime comparison and changed-mass semigroup bound across 121 times. `RESIDUAL_SHELL_CHECK.json` records residuals below 6e-14, microscopic/coarse lifetime ratio 1.00003612 below 1.00017214, and measured operator error 0.00201438 below 0.01866941. These are finite algebra diagnostics; they do not prove the general theorems, demonstrate physical advantage or establish priority.

Artur Stephan, *Coarse-graining and reconstruction for Markov matrices*, Z. Anal. Anwend. 44 (2025), 251–275, [DOI 10.4171/ZAA/1796](https://ems.press/content/serial-article-files/51411), is another directly inspected primary predecessor. Theorem 2.6 constructs the stationary-measure conditional reduction and preserves reversibility; Section 2.5 / Proposition 2.8 control error using the reduced spectral relaxation rate, with an analogous continuous-time statement. Its discrete-time exposition needs the usual spectral/aperiodicity qualifications; I do not import a claim that an arbitrary unique-invariant discrete Markov matrix converges at the real part of its second eigenvalue. The positive reversible heat-semigroup specialization is the relevant comparator. Full PDF/text are cached as `source/Stephan2025.{pdf,txt}`.

A further numerical-incumbent lead is Kannan–Sharpe–Swinburne–Wales, *Optimal dimensionality reduction of Markov chains using graph transformation*, J. Chem. Phys. 153 (2020), 244108, DOI 10.1063/5.0025174. Its supplied-network exact MFPT/graph-reduction approach should be compared when the full transition network is already known. Only its primary abstract/open manuscript landing result was inspected here; no detailed theorem from it is imported. It does not by itself acquire an exponentially large microscopic network from local experiments. Form-perturbation literature (Mugnolo–Nittka–Post, arXiv:1007.3932v2; Post–Simmer quasi-unitary equivalence) remains a primary priority-search lead, not a verified claim of an exact earlier identical bound.


# Part D. Thermodynamic controls and physically specified noisy preparation

## 6. New constructive extension: bounded total thermodynamic action

This is an elementary moving-metric extension of the principal's energy proof. It supplies a checked theorem for changing U, rather than an assertion that arbitrary thermodynamic switching is free.

### Statement

Let pi_t(x)=w_t(z)rho_z(x), z=phi(x), be positive stationary measures with a **fixed conditional family** rho_z. Assume piecewise C1 time dependence with finitely many jumps, and positive reversible generators A_t=F+B_t. Assume the principal's block-diagonal C_t and relative coupling condition hold uniformly with parameter d<1 in L2(pi_t); the conditional projection is fixed. Write D(d)=d/[2sqrt(1-d)]. Define

K_T=(1/2)integral_0^T max_x[-partial_t log pi_t(x)]_+dt
 +(1/2)sum_j max_x log[pi_(t_j-)(x)/pi_(t_j+)(x)].         (6.1)

The jump maxima are nonnegative for probability measures; they can harmlessly be replaced by their positive parts. If the initial source has W_0=||dmu_0/dpi_0||_2, then for every retained |g|<=1 the microscopic/coarse terminal expectation error is at most

W_0 exp(K_T) D(d).                                      (6.2)

If learned coarse generators at each t are exactly reversible in the same pi_t and have relative conductance error eta<1, an additional W_0 exp(K_T) D(eta) suffices. Initial source/readout/numerical errors add at their actual bounded-observable norms. This last learning clause assumes the true pi_t is maintained exactly; arbitrary estimated metrics need an additional argument, not an appeal to the fixed-control mass-metric theorem.

For Gibbs energies U_t depending only on counts, with fixed beta,

K_T<= (beta/2)integral_0^T osc_x(partial_t U_t)dt
 +(beta/2)sum_j osc_x(U_(t_j+)-U_(t_j-)).                 (6.3)

Thus a family with bounded total thermodynamic action has a horizon-free certificate, even if the dynamics continues for an arbitrarily long time after the last change. Extensive perturbations can make this sufficient bound exponential in N. Repeated bounded-amplitude cycles can make K_T grow with the number of cycles. This is not a claim that such exponential cost is necessary; the bound can be conservative.

### Complete proof

Use the counting-space isometry y_t(x)=p_t(x)/sqrt(pi_t(x)) for forward probability densities. With D_t=diag(pi_t), detailed balance makes

Atilde_t=D_t^(1/2) A_t D_t^(-1/2)

positive self-adjoint, and similarly Ctilde_t. The transformed dynamics is

y'_t=-(Atilde_t+V_t)y_t,
V_t=(1/2)diag(partial_t log pi_t).                        (6.4)

The transformed retained projection has block vector sqrt(rho_z), hence is time independent. Because V_t is constant on each fiber it commutes with that projection. Thus evolution under Ctilde_t+V_t is still block diagonal, and its retained block is exactly transformed coarse evolution. At a measure jump probabilities are continuous and y_(t_j+)=J_j y_(t_j-), where

J_j=diag sqrt(pi_(t_j-)/pi_(t_j+)),
||J_j||=exp(k_j),
k_j=(1/2)max_x log(pi_(t_j-)/pi_(t_j+)).                  (6.5)

The same jump acts in both dynamics and commutes with the retained projection.

Let nu_t=max(0,-lambda_min(V_t))=(1/2)max_x[-partial_t log pi_t]_+, and let K(t) be the cumulative integral of nu plus jump costs. For the forward comparison k_t solving -(Ctilde_t+V_t), the weighted energy identity/inequality gives

integral_0^T exp[-2K(t)] E_Ctilde_t(k_t)dt<=||k_0||^2/2.  (6.6)

Indeed d[exp(-2K)||k||^2]/dt equals -2exp(-2K)[E_Ctilde(k)+<k,(V+nu I)k>], with V+nu I>=0. At a jump its weighted norm cannot increase because ||J_j||<=exp(k_j). Summing the intervals proves (6.6).

For backward adjoint h_t=U_(Atilde+V)(T,t)^*g_T, the same argument in reverse time gives

integral_0^T exp[-2(K(T)-K(t))]E_Atilde_t(h_t)dt<=||g_T||^2/2.  (6.7)

At reversed jumps the adjoint J_j^* has the same norm bound. The relative form condition still yields E_Ctilde(h)<=E_Atilde(h)/(1-d). Duhamel for two systems with identical jumps has only the continuous generator-difference integrals; common jumps introduce no new forcing. Pair it with k_0,g_T. In each integrand, insert the two weights from (6.6)–(6.7); their inverse product is exactly exp(K(T)). Cauchy–Schwarz therefore gives

||U_(Atilde+V)(T,0)-U_(Ctilde+V)(T,0)||
 <=exp(K_T)d/[2sqrt(1-d)].                               (6.8)

The initial transformed density has norm W_0. The terminal vector sqrt(pi_T)g has norm <=1. Since the comparison's retained block propagates only the projected initial density, (6.2) follows. Apply the same estimate to coarse true/learned forms to get the learning clause.

Finally partial_t log pi_t=-beta(partial_t U_t-E_pi_t partial_t U_t), so max[-partial_t log pi_t]<=beta osc(partial_t U_t). For a jump, log(pi_old/pi_new)=beta DeltaU+log(Z_new/Z_old), whose maximum is at most beta osc(DeltaU). This proves (6.3).

### Source, resource and precision limits

This changes the mathematical drive scope, not the physical availability of U_t. One must pay count/field implementation, timing, energy, all control segments and their variation. For bounded K and W_0, selecting d,eta=O(epsilon exp(-K)/W_0) is sufficient. Since d^2=C_c/gamma, the required stirring scales as W_0^2 exp(2K)C_c/epsilon^2, with the actual graph-gap factor. Calibration precision and numerical precision must be selected accordingly. At K=Theta(N), this theorem alone does not establish polynomial total resources. A numerical log(T) algorithm for a frozen generator does not evaluate an arbitrary long, finely switched protocol at log(T) cost.

For the action bound, U_t must be computably specified with a warranted variation majorant. Estimating a continuous uncontrolled function from a finite mesh is not a free action certificate. A wrong unknown energy changes pi_t; the fixed-control mass-metric lemma does not automatically telescope with no accumulated switching cost.

## 7. Preparation repair: direct pinning without switching U off

The principal's original product-pinned-Gibbs writer is mathematically valid in its declared pin-mode Arrhenius model. Its spectral comparison is correct because neighbor-dependent b_i is unchanged by flipping the central spin. The stated time actually gives mixing TV<=zeta/8 under its pi_min bound, so the looser zeta/2 claim is safe. The target product Gibbs wrong-string probability is <=zeta/4. A global throttle [2cosh(betaH)]^(-1) keeps the maximum flip rate bounded and rescales the gap to at least b_min, if that extra clock-control range is available.

A stronger direct argument removes the Uoff operation and does not use global spectral mixing.

### Direct drift writer theorem

Let a target bitstring s be given. Pause stirring, keep the original possibly unknown/nonconvex count energy U with every one-spin increment bounded by J, and add on-site pin energy -H sum_i s_i sigma_i using +/-1 spin notation. Assume the same neighbor-dependent mobility law, b_min<=b_i<=b_max, continues to hold in this pin mode. Wrong bits then correct at rate at least

A=b_min exp[beta(H-J/2)],

and correct bits become wrong at rate at most

B=b_max exp[-beta(H-J/2)].

Let W(x)=number of wrong bits. Pointwise application of the generator gives

L W <= NB-(A+B)W,

so for any initial microscopic state or distribution,

E W_t <=N exp[-(A+B)t]+NB/(A+B)
       <=N exp(-At)+NB/A.                               (7.1)

Choose

H=J/2+(2beta)^(-1)log[4N b_max/(zeta b_min)],
t=A^(-1)log(4N/zeta).

Then B/A=zeta/(4N) and P(X_t !=s)<=E W_t<=zeta/2. This proof holds despite correlations, arbitrary nonconvex collective interactions and unknown actual U inside its increment bounds. No assumption about a pinned global gap or microscopic equilibrium sampling is used.

The maximal total flip rate is <=N b_max exp[beta(H+J/2)]. Dividing by A shows the expected event exposure before the writing time is <=

N(b_max/b_min)exp(beta J) log(4N/zeta).                    (7.2)

A hard event cap can be set by Poisson domination using the actual maximal rate and time. Pin switch work is bounded by O(NH) at either switch in the ideal spin-energy model; recording a thermodynamic heat/work claim still requires the apparatus/bath accounting.

Optionally throttle every pin-mode rate by exp[-beta(H+J/2)]. Then every single-site rate is <=b_max, the correction lower bound becomes b_min exp(-betaJ), and the required time is

t'=exp(betaJ)b_min^(-1) log(4N/zeta).                      (7.3)

The same distributional guarantee holds. This throttle is an additional writer-mode kinetic-control range; the original target-mode fixed a_min does not grant it. Its actual dynamic range, leakage and implementation cost must be supplied. A field of logarithmic magnitude suffices for ordinary inverse-polynomial write error, while exponential write accuracy below requires linearly growing fields.

### Relative lifetime source: valid with exact target-set semantics

Let C be the **entire non-target transient set**, target D=X\C, and nu=pi(.|C). Suppose ideal strings are drawn from nu and the conditional writer outputs the requested string with probability >=1-delta uniformly for every requested string. For any i in C, the actual mixture mu satisfies

(1-delta)nu(i)<=mu(i)<=nu(i)+delta.

If delta<=zeta nu_min with nu_min=min_(i in C)nu(i), then (1-zeta)nu(i)<=mu(i)<=(1+zeta)nu(i). Since tau_D=0 outside C and tau_D>=0 everywhere,

(1-zeta)E_nu tau_D<=E_mu tau_D<=(1+zeta)E_nu tau_D.       (7.4)

No arbitrary-TV stability of a huge mean was used. If C is only a selected subwell while its complement contains other non-target transient states, declaring all outside-C errors to have lifetime zero is invalid. Postselection on C is a different source and carries a normalization/detection correction.

For the count-energy model with |Delta U|<=J, osc(U)<=NJ along the hypercube. Therefore on any nonempty C, nu_min>=exp[-N(log2+betaJ)]. A one-block ideal draw uses N+1 known count weights followed by a uniform string at the sampled count. Choosing delta<=zeta exp[-N(log2+betaJ)] needs H=O(N+log(1/zeta)), and the throttled writer time is O(N+log(1/zeta)) at fixed beta,J,b bounds. The event bound and pin-switch energy are polynomial. This is a real stronger control contract, not fixed maximum field hardware.

The error guarantee includes **all** uncontrolled write-failure channels. An unknown fixed reset-error or stirring-leak floor cannot be removed by statistical readout repetition. The polynomial conclusion is conditional on the declared pin/throttle/noise mechanism implementing these rate and leakage bounds at polynomial actual cost. The energy barrier formula warrants exponentially small thermal wrong flips inside that model; it does not empirically certify every unknown apparatus error to exponential accuracy from polynomial trials.

### Nonuniform conditional source via native mixing

For a finite reversible count-conserving conditional chain with stationary mu_k and gap gamma,

|P_t(x,y)/mu_k(y)-1|
 <=exp(-gamma t)sqrt[(1/mu_k(x)-1)(1/mu_k(y)-1)]
 <=exp(-gamma t)/mu_min.                                 (7.5)

This is the spectral-gap Cauchy–Schwarz bound on centered point-mass densities. Hence t>=gamma^(-1)log[1/(zeta mu_min)] gives a uniform pointwise relative conditional error <=zeta, from any microscopic initial law in that shell. It is polynomial when the gap inverse and log(1/mu_min) are polynomial. For many independently mixed blocks allocate relative errors so their sum/product remains controlled, or use a global minweight/gap bound. A possible exponentially slow conditional Kawasaki gap is not repaired by the logarithm. Counts must really be conserved during this stage; flip/stir-switch leakage is an additional error channel.

## 8. Optional constructive removal of supplied one-block count energy

This is an additional checked operation within the same clamped finite-state kinetic model, not a claim about generic Hamiltonian learning. It addresses the concern that precise macro stationary weights were supplied. It requires the stronger clamps/pins and noise budgets already discussed.

For one block of N spins, leave one central spin free and hold all others in a specified bitstring with rest count k. Pause stirring. For a fixed neighbor pattern the central chain has rates

r_+=b exp[-beta DeltaU(k)/2],
r_-=b exp[+beta DeltaU(k)/2].

Starting the central spin in each sign and observing a common duration h gives transition probabilities

p_01=r_+/(r_++r_-)[1-exp(-(r_++r_-)h)],
p_10=r_-/(r_++r_-)[1-exp(-(r_++r_-)h)].

Therefore at any h>0,

DeltaU(k)=-beta^(-1)log(p_01/p_10),
r_++r_-=-h^(-1)log(1-p_01-p_10),
b=sqrt(r_+r_-).                                         (8.1)

There is no finite-difference derivative or multiple-jump truncation. The same neighbor mobility cancels in the forward/backward probability ratio. If a known kinetic multiplier is present, divide it out with its actual accuracy/conditioning.

Let C_E=exp(betaJ/2), h=1/(4b_max C_E). Then r_++r_-<=2b_max C_E and

p_01,p_10>=p_min:=b_min exp(-1/2)/(4b_max C_E^2),
1-p_01-p_10>=exp(-1/2).

These bounds follow by integrating a first transition with no later transition, or directly from the formulas. Thus inversion is uniformly conditioned at fixed declared parameters. With corrected binary readout contrast v, simultaneous probability accuracy alpha costs O(v^(-2)alpha^(-2)log(N/delta)) trials per direction/count. For alpha<=p_min/2, the increment error is at most 4alpha/(beta p_min). Acquiring all N increments to error epsilon_U/N and summing from the gauge U(0)=0 gives sup_k|Uhat(k)-U(k)|<=epsilon_U, using

O(N^3 v^(-2) beta^(-2)p_min^(-2)epsilon_U^(-2)log(N/delta))

shots. Each shot pays its N-spin writing/clamping/reset and h; this increases physical operation cost by the actual preparation cost, ordinarily at least O(N). A fixed unknown clamping/readout/timing bias must be below alpha; it is not averaged away. Other spins must really remain pinned, not merely have the correct initial count. Pins of logarithmic size can make their unwanted event probability over h polynomially small under the declared rate model. This source/clamp validity is a real apparatus premise.

This acquires a size-N count-energy table. It does not transfer unknown U_N to a new size without a specified shared energy family. A new supplied count perturbation V(k) may be added after acquisition; the absolute baseline potential error remains the same for every such fixed V, subject to its actual physical implementation and increment bounds.

### Relative mean-lifetime robustness with imperfect stationary weights

Here is a direct elementary comparison which does not require exact pi in both learned models. Let pi,pihat be reversible probability weights on the same transient state set C and full target graph, with

exp(-s)<=pihat_i/pi_i<=exp(s),
1-eta<=qhat_ij/q_ij<=1+eta.

For killed generators write K=D_pi A and Khat=D_pihat Ahat. These are symmetric positive-definite Dirichlet matrices. Conductance comparison gives

e^(-s)(1-eta)K <= Khat <= e^s(1+eta)K.

Their inverses have the opposite quadratic-form bounds. Khat^(-1) is entrywise nonnegative because it is a killed Green kernel times a positive diagonal. Let r=pi restricted to C and rhat=pihat restricted to C. The equilibrium-conditioned means are

m=r^T K^(-1)r/pi(C),
mhat=rhat^T Khat^(-1)rhat/pihat(C).

Entrywise rhat/r between e^(-s),e^s costs at most e^(+/-2s) in the positive Green-kernel quadratic form; denominator comparison costs one more factor e^(+/-s), and inverse-form comparison another. Hence

e^(-4s)/(1+eta) <= mhat/m <= e^(4s)/(1-eta).             (8.2)

For a uniform potential error epsilon_U, normalized Gibbs log-mass error is at most s=2beta epsilon_U. Local rate error from that potential and a relative mobility error eta_b is also controlled: eta can be taken as max((1+eta_b)e^(beta epsilon_U)-1, 1-(1-eta_b)e^(-beta epsilon_U)). Thus polynomial energy/mobility accuracy gives relative lifetime accuracy even if m is exponentially large. This comparison is separate from the all-horizon semigroup mass-metric result.

For the actual microscopic process, also include the principal's 1/(1-d^2) Schur factor. If the written physical source is pointwise within (1+/-zeta) of learned pi(.|C), its relation to the true pi(.|C) costs e^(+/-2s). A conservative complete bracket for physical mean M_phys versus learned coarse mhat is

(1-zeta)(1-eta)e^(-6s)
 <=M_phys/mhat
 <=(1+zeta)(1+eta)e^(6s)/(1-d^2).                         (8.3)

The source and target-set qualifications of section 7 apply. This removes a supplied exact energy from the one-block lifetime operation at explicit polynomial acquisition cost, but still assumes the special count-energy kinetic family and clamp/pin mechanism. No generic material or unknown spatial interaction is covered.


# Part E. Certified numerical evaluation

## Positive scaling and squaring, including its cost
For a q-state Markov row generator Q with exit bound R>0 and rational time T, take s=ceil(log2(max(1,RT))) and h=T/2^s. Then Rh<=1 and P=I+Q/R is stochastic. Approximate exp(hQ) by
S0=exp(-Rh)sum_(j=0)^(K-1)(Rh)^j P^j/j!+[Poisson(Rh) tail from K] I.
It is stochastic and has row-l1 operator error <=2e/K!. K=O(s+log(1/nu)) suffices for base error nu/2^(s+2). Square s times; stochastic contraction makes each squared-matrix error at most twice the previous one. For finite arithmetic round entries down to positive b-bit dyadics and add each row deficit to the diagonal. This preserves stochasticity, changing row-l1 by <=2q2^-b. Allocate each of K+s operations error <=nu/[2^(s+3)(K+s+1)]. Then total error <=nu with b=O(s+log q+log(K+s+1)+log1/nu). Positive rounded-down Poisson weights plus a diagonal remainder give the analogous coefficient implementation. Dense cost O(q^3(K+s)) arithmetic, with polynomial input and working bits.
This proves polynomial log(T+1) numerical cost for a supplied polynomial-size finite generator. It neither makes q=product_r(m_r+1) polynomial in a growing number of blocks nor removes physical parameter error. H separately described control segments cost H evaluations with numerical budgets split across them. Input drive description, output observables and initial-law sampling are paid.


# Part F. Resource consequence, comparators and independent alternatives

## F1. A complete allocation in the explicit count-energy model

Fix beta, J_U, b bounds, local degree, type count and a fixed block number B. Fix a desired error epsilon and an ideal preparation with Gibbs L2 warmness W. Choose z and eta proportional to epsilon/W; then gamma>=C_c/z^2 and kappa>=C_c/[z^2 min(lambda_r)] suffice. Mobility calibration costs O(D_tab v^-2 W^2 epsilon^-2 log(D_tab/delta)) trials, in addition to preparation/hold/calibration costs and the required systematic-bias budget. Constructing rates and a q-state matrix is polynomial in q=product_r(m_r+1), local table size and energy evaluation cost. Part E gives polynomial numerical cost in log(T+1), rather than T. The graph, pinning and control communication costs are separate physical costs. None depends on the inverse macroscopic phase-switching rate.

For a growing number of blocks use sparse coarse kinetic Monte Carlo: O(epsilon_MC^-2 log(1/delta_MC)) trajectories, each with at most O(R_s T) expected jump attempts under Poisson domination. A hard cap and its tail probability provide a finite runtime guarantee. Each attempt pays the actual local energy/control lookup cost. Memory is the learned local tables plus counts, observations and query workspace. A full matrix is exponential in B and is never silently stored. Dynamic source sampling and readout integration must also be evaluable in the claimed costs.

A single block may have U(k)=-J(2k-m)^2/(2m). For beta J>2log2, the equilibrium-conditioned mean hitting time of the upper half is exponentially large in m. The birth/death formula below already gives a lower bound exp[m(beta J/2-log2)-O(log m)] from the middle edge and the all-zero weight, while all one-spin increments remain bounded. This is a sufficient example, not a sharp transition threshold. Thus the relative-lifetime theorem has a nonvacuous exponential-horizon use. It does not need to observe that rare transition during calibration.

For reflecting 0 and target b, put unnormalized weights w_i, edge conductances c_i=w_i q_(i,i+1), S_j=sum_(i<=j)w_i and W_C=sum_(i<b)w_i. Then

E_(w|C) tau_b = (1/W_C) sum_(j=0)^(b-1) S_j^2/c_j.

Proof: solve successive flux differences c_j(t_j-t_(j+1))=S_j with t_b=0 and average. All terms are positive; logarithmic summation computes the mean or its logarithm with polynomial bit costs in m, input lengths and log of the answer. This is standard birth/death/network machinery, not a new rare-event method.

An equal-information incumbent can use the same conditional averaging, histogram/umbrella information, reversible coarse rates, birth/death formulas and accelerated network methods. Comparing solely against uninformed microscopic trajectory simulation would exaggerate novelty and benefit. The construction removes the explicit fast-stirring cost from numerical reuse and compresses 2^N microscopic states at fixed block number. A matched advantage over the strongest existing coarse-graining method is NOT ESTABLISHED.

## F2. A fully explicit conditional-gap fallback, and its limitation

For a residual block W with known oscillation O_W=max W-min W, midpoint Kawasaki conductances are proportional to exp[-beta(W(x)+W(y))/2]. Shift min W to zero. Relative to the uniform shell, the Dirichlet form is at least (D/Z)exp(-beta O_W) times the uniform form; variance is at most (D/Z) times the uniform variance (choose the uniform mean as centering constant). Therefore the actual gap is at least kappa lambda_graph exp(-beta O_W). The normalized complete-graph conditional gap is at least exp(-beta O_W). This is a self-contained computable certificate for every finite residual W, but can be exponentially bad in block volume.

Consequently Part C has a completely explicit finite resource bound even without a favorable mixing theorem; efficiency then requires a stronger derived certificate. O_W=O(log m) is one sufficient polynomial-cost subclass. Boudou et al.'s high-temperature Theorem3.1/Corollary3.3 supplies a much broader density-uniform gap class under its exact summability/range/geometry hypotheses. Its actual constants must be supplied/extracted before a numerical sample count is certified; an unspecified low-temperature gap is not a predictive algorithm. No high-temperature theorem is transferred to generic coexistence or glassy discarded sectors. Strong nonconvex collective U does not enter these conditional gaps because it is constant on each fiber.

## F3. Independent nonlinear field construction

The constructor independently derived a finite-noisy pair-force learner for overdamped Kac-normalized interacting particles. It retains a learned bounded Lipschitz pair force and a nonlinear McKean–Vlasov probability field, then evaluates it with an explicit finite nonlinear Markov update. Deterministic microscopic initial configurations are allowed through their empirical W1 descriptor; iid particles are not assumed after interactions. New smooth spatial preparations and new bounded Lipschitz extensive drives are covered.

Its combined bound has finite-size contribution [2BT exp(CT)+1]/sqrt(N), plus exp(CT) times initial empirical error, physical force bias, force-learning error T alpha, time-discretization error O(T sqrt(Delta)), spatial rounding T s/Delta and certified numerical errors. Pair acquisition at alpha accuracy uses O(alpha^-d) separation points and O((alpha^-4+sigma_m^2 alpha^-6)log(1/delta)) fresh pair releases per point, with all isolation/reset/readout costs. Dense field evaluation is polynomial in inverse accuracy at fixed spatial dimension and fixed T. It is exponential in the proof's horizon constant and does not establish metastable rare-event reuse.

The complete formal statement, acquisition bias calculation, finite-N coupling proof and numerical recursion are in [the constructor initial report](COLLECTIVE_INFORMATION_RESEARCH_RECORD/initial/constructor.md). This is established force-learning/propagation-of-chaos machinery composed with explicit costs. It is not a new discovery or a theorem for ordinary fixed-strength short-range fluids. Known predecessors include Lu–Zhong–Tang–Maggioni (PNAS2019), Lu–Maggioni–Tang (JMLR2021) and Yao–Chen–Yang (COLT2022). Their access/coercivity metrics do not automatically imply uniform all-preparation accuracy; the paid pair-isolation interface here is stronger.

## F4. Independent local causal construction

The machinery researcher derived a full noisy-acquired local lattice predictor under a common Dobrushin influence bound alpha<1 over every allowed control. A core of k sites uses a window of radius R. Its error for every new prescribed drive and every horizon is bounded by

2k[zeta exp(-(1-alpha)t)+alpha^(R+1)+eta(1-exp(-(1-alpha)t))/(1-alpha)].

Only a paid initial window marginal is needed, even for arbitrarily correlated exterior preparations. The law is an explicit window master equation, and a finite-data robust influence certificate can be computed from learned local kernel rows plus 2d eta. It retains q^m microscopic window states, m=O(log(1/epsilon)^D); noisy initial tomography additionally pays the detector inverse conditioning. It excludes conserved slow modes, criticality and coexistence unless those modes are retained separately. It predicts the mean of a macroscopic spatial average by averaging local means; it does not establish concentration for arbitrary correlated sources.

The full proof and costs are in [the machinery initial report](COLLECTIVE_INFORMATION_RESEARCH_RECORD/initial/machinery.md). This is a competent established disagreement-coupling/local-computation comparator. The relative-energy construction permits a slow retained sector instead of contracting all influence; the nonlinear field route instead derives a limiting law. These mechanisms have different domains and cannot be concatenated without checking their interfaces.

# Part G. Exact obstructions and constructive repairs

The following independently derived proofs are retained because they delimit what a generic physical principle would have to earn. They do not refute the scoped positive theorems above or formal exact microscopic variational identities.

## 1. Exact kinetic nonidentifiability: equilibrium is not a kinetic clock

For a finite connected graph, known energies E_h(x), beta>0, and arbitrary positive symmetric conductances c_h(x,y), define q_h(x,y)=c_h(x,y)exp(beta[E_h(x)-E_h(y)]/2). Detailed balance holds with pi_h proportional to exp(-beta E_h), since pi_h(x)q_h(x,y)=c_h(x,y)exp(-beta[E_h(x)+E_h(y)]/2)/Z_h. Complete equilibrium information for every h leaves the symmetric kinetic prefactors unidentified.

**Theorem A (proved).** Take x in {-1,1}, beta=1, known E_h(x)=-hx, and flip rate a(h)exp(-hx). Models a_0(h)=1 and a_1(h)=exp(Kh^2), with K chosen so a_1(h_*)=4 at h_*=atanh(1/2), give exactly the same baseline generator at h=0, hence the same law of every passive baseline experiment for every baseline preparation. Their equilibrium distributions coincide for all h. Both a functions are positive and analytic.

For the query preparation E[x(0)]=0 and constant h, applying the generator to x gives m'=2a sinh(h)-2a cosh(h)m, hence m_h(t)=tanh(h)[1-exp(-2a(h)cosh(h)t)]. Put lambda=2cosh(h_*)=4/sqrt(3) and t_*=log(4)/(3lambda). The query means differ by

Delta=(1/2)(4^(-1/3)-4^(-4/3))=(3/8)4^(-1/3)>0.236.

The acquired data have identical laws. For any prediction error radius strictly less than Delta/2, the success intervals are disjoint; their probabilities cannot both exceed 1/2. This is exact nonidentifiability, not a sample-size failure. Detector noise cannot help.

**Repair and scope.** Derive the drive dependence of symmetric rates from a warranted transition-state/bath model, or acquire informative driven kinetics. Quantitative regularity is needed for a finite control net: analyticity without norm/radius bounds is insufficient. This theorem does not refute prediction given a warranted complete controlled generator. It identifies the missing kinetic premise in deriving time evolution from free-energy forces.

## 2. An exact reversible hidden-memory counterexample and macroscopic consequence

Consider (x,z) in {-1,1}^2. The hidden z flips at rate gamma>0. Model I flips x at rate 1; model II flips x at rate 1+uz, |u|<=u_*<1. Every generator is symmetric, with the same unique uniform invariant distribution for all u. Rates are uniformly positive and bounded when gamma,u_* are fixed.

At baseline u=0, both visible x paths are precisely the rate-one telegraph process, for arbitrary x preparations and arbitrary hidden z laws. Even unlimited baseline records, and complete stationary states at every u, do not distinguish them. This does not require a slow phase switch.

For the driven preparation x(0)=1 and unbiased z(0), put m=E x, q=E xz. Direct generator application in model II yields the exact closed equations

m'=-2m-2u(t)q,
q'=-2u(t)m-2(1+gamma)q.                  (2.1)

For constant u, m(0)=1,q(0)=0,

m(t)=exp[-(2+gamma)t][cosh(st)+(gamma/s)sinh(st)],
s=sqrt(gamma^2+4u^2).                    (2.2)

Model I gives exp(-2t). At gamma=0.1,u=0.75,t=1 the difference is about 0.171. For n independent identically prepared pairs, M_n=n^(-1)sum x_i has these respective means, while at each fixed time P(|M_n-E M_n|>=r)<=2exp(-nr^2/2). Thus an order-one driven macroscopic discrepancy survives while fluctuations vanish. Preparation/readout requires O(n) local operations. This is a kinetically coupled block-product class, not an extended interacting phase transition.

Solving for q gives the exact history equation

m'(t)=-2m(t)-2u(t)e^[-2(1+gamma)t]q(0)
 +4u(t) integral_0^t e^[-2(1+gamma)(t-s)]u(s)m(s) ds.       (2.3)

The passive kernel at u=0 is exactly zero. The driven kernel depends on both u(t) and u(s); the hidden initial cross field q(0) supplies an initial-force term. A passive stationary kernel cannot simply be reused. Exponential decay alone does not justify deleting a kernel of appreciable integrated strength. Retaining q repairs the closure exactly.

## 3. Complete constructive repair for the same example

Assume the physical kinetic family rate_x=1+uz, rate_z=gamma is warranted, one shared gamma in [0,Gamma] is unknown, controls |u|<=u_*<1 are calibrated, and the additional cross field xz is physically measurable. Permit preparation x=z=1. Independent binary detector errors have known contrasts v_x,v_z with v_x v_z>=v_*^2>0; unknown residual bias is charged separately.

Use baseline u=0 for tau=1/[2(1+Gamma)]. Then c=E[x(tau)z(tau)]=exp[-2(1+gamma)tau]>=e^(-1). Average N corrected scores Y_xY_z/(v_x v_z), project to the allowed c interval, and set gamma_hat=clip_[0,Gamma](-log(c_hat)/(2tau)-1). Since log is e-Lipschitz there,

N >= 2e^2(1+Gamma)^2 v_*^(-4) eta^(-2) log(2/delta)       (3.1)

ensures |gamma_hat-gamma|<=eta with probability >=1-delta. This follows from Hoeffding at score-mean precision eta/[e(1+Gamma)]. Each trial pays a two-spin reset, tau holding, two measurements, clock accuracy, detector calibration and all apparatus refinement. Systematic corrected-score bias b produces coefficient uncertainty O((1+Gamma)b); repetition does not remove it.

Let y=(m,q) and A_gamma(u)=-2[[1,u],[u,1+gamma]]. For every admissible u,

y^T A_gamma(u)y<=-2(1-u_*)||y||^2.

The controlled propagator therefore contracts at lambda=2(1-u_*), uniformly for arbitrary piecewise-continuous controls. The learned model is also physical after clipping gamma. Variation of constants gives, simultaneously for all future controls and t>=0,

||y_hat(t)-y(t)|| <= e^(-lambda t)||y_hat(0)-y(0)||
 +(2sqrt(2)eta/lambda)(1-e^(-lambda t))+E_num.              (3.2)

Proof: ||A_hat-A||<=2eta, and the physical comparison trajectory has ||y||<=sqrt(2). An H-segment piecewise constant query can be evaluated with H explicit 2x2 matrix exponentials at per-segment numerical error E_num/H. Acquisition and model memory are independent of n and T; input bits, H, numerical precision and exponential evaluation are paid. If actually implementing a drive on n pairs for time T, the physical nT holding cost remains nT.

New preparations are covered only when both retained m_0 and q_0 are supplied/measured. Equal m_0 alone is insufficient. Collective means for every n obey (3.2) exactly; product preparations give the concentration bound above. This is a complete finite-noisy-acquisition/reuse demonstrator with a measurable extra field and a known controlled generator family. It is small exactly soluble kinetics, not a new many-body principle or an established advantage.

## 4. Sharp rare-clock acquisition-duration obstruction

**Theorem D (proved).** Let the visible process itself be a symmetric telegraph process with unknown rate r or 2r. Stationary distributions coincide. Full noiseless observations over total physical exposure S have Poisson(rS) versus Poisson(2rS) jump counts. Couple by adding a rate-r clock: the full paths coincide until the first added event. Consequently

TV(P_r^S,P_2r^S)<=1-exp(-rS)<=rS.                        (4.1)

This also holds for fresh-run splits and adaptive observations with an almost-sure total exposure budget, by coupling the extra clock on actual observed time. Noisy data processing cannot improve TV.

For a future preparation X(0)=1 and T=1/r, the two means are exp(-2) and exp(-4), a gap >0.117. If a predictor has error strictly below half this gap and failure probability <=delta in both models, the disjoint success intervals require TV>=1-2delta. Thus

S>=(1-2delta)/r.                                        (4.2)

For r_n=exp(-bn), acquisition exposure is exponential in n. This refutes a general polynomial-in-n-and-log(T) claim; polynomial in T is not refuted. Parallel wall time does not erase total exposure/copies. Equilibrium energies do not determine the kinetic prefactor.

Repair: informative active preparation near the bottleneck, accelerated controls with a proved original-clock reweighting relation, or a physical lower bound on relevant rates changes the accounting. A bias can change the reaction path, so acceleration is not a free time rescaling. For general chains, rates differing only in a stationary region with expected affected-transition intensity a_n give a coupling TV upper bound O(a_n S), while a new preparation placed there may show a rapid difference. Do not claim a bounded-local-strength many-body implementation of every abstract r_n without constructing it: this is an access-interface theorem.

## 5. General exact criterion and finite-data constructive repair

Let X_t be finite microscopic controlled Markov dynamics, K_a its one-step kernels, and phi:X->Z a collective coordinate, |Z|=q. A finite control alphabet has size M.

**Theorem E1, established controlled strong lumpability.** The collective process is Markov with kernels B_a for every microscopic initial distribution and every control sequence iff sum_{y:phi(y)=z'}K_a(x,y)=B_a(phi(x),z') for every a,x,z'. Necessity: start from each microscopic point and examine one step. Sufficiency: condition on the entire past; every hidden law within the current fiber gives the same collective next row. For affine generators L_u=L_0+sum u_j L_j it suffices that every coefficient generator preserves fiber-constant observables. Baseline closure alone is insufficient. This is established machinery, not new mathematics.

**Theorem E2, proved finite-noisy acquisition composition.** Suppose (i) for all controls, the projected one-step rows at any two points in the same fiber have TV distance <=c; (ii) each macrostate z can be freshly prepared, with any fixed within-fiber law mu_z; (iii) noisy detector scores psi_j(Y) are known, unbiased for macro indicators, and bounded by K; (iv) all actual preparation, step, detector, calibration and refinement costs are paid and no microscopic solver is hidden in the interface. Define B_a(z,.) from mu_z. After N trials for each (z,a), entrywise score averages followed by l1-nearest simplex projection yield simultaneous row TV error <=eta with confidence 1-delta if

N>=2K^2 q^2 eta^(-2) log(2Mq^2/delta).                   (5.1)

Proof: Hoeffding at entry error eta/q; raw l1 error <=eta; simplex projection at most doubles it; TV is half l1. Conditional-fresh martingale data admit the same bounded-score concentration. Preparation macrostate error and residual corrected-score bias add their actual row error; unknown systematic bias is not reduced by repetition.

For every future preparation and control sequence of length H, with known macro initial law p_0,

TV(p_H,p_hat_H)<=TV(p_0,p_hat_0)+H(c+eta).                (5.2)

Condition on the true coarse history; its hidden conditional row differs from the acquired fiber average by <=c. Telescope Markov-kernel contractions. The confidence event is uniform over future/adaptive numerical queries. If each B_a has Dobrushin coefficient <=1-kappa,

TV(p_H,p_hat_H)<=(1-kappa)^H TV(p_0,p_hat_0)
 +(c+eta)[1-(1-kappa)^H]/kappa.                          (5.3)

This is a genuine uniform controlled stability premise, stronger than passive mixing. It may be certified from the finite acquired rows because delta(B_a)<=delta(B_hat_a)+2eta. This improvement is for final marginals, not automatically full path laws/hitting events. Full path laws retain the H(c+eta) coupling bound.

For continuous controls in a d-dimensional compact set with known projected-row Lipschitz constant L, an r-net gives additional per-step Lr error and cardinality generally O((L/r)^d). With fixed d choose r,eta=O(epsilon/H), or O(kappa epsilon) for contractive final marginals. Growing independent actuator dimension retains the covering curse.

Acquisition pays qMN actual trials, their macro preparation, physical step duration, detector/calibration/refinement and random/control administration. Straight aggregation costs O(Mq^2 N), memory O(Mq^2) numbers at requested precision, query O(Hq^2) arithmetic. Polynomial q,M,K,1/kappa and actual trial/refinement costs give a polynomial full-cycle predictor. None follows from entropy, an MZ identity or fitted low rank. Strong/approximate controlled lumpability itself needs physical proof; one averaged trajectory cannot certify every hidden conditional preparation.

A concrete constructive class is permutation-symmetric fixed-species population dynamics: count states form an exact polynomial-size quotient at fixed species number. Prove this symbolically from the rates, then acquire and propagate it. This is an established aggregation route, not a general spatial many-body reduction. Even q=n+1 does not imply good fixed-step TV contraction: distant macrostates can remain almost disjoint for many relaxation times. A Wasserstein/Lipschitz-observable proof can be much better, but needs its own explicit target/metric.

## 6. Noise conditioning, instability and limits

**Theorem F (proved).** Take N bits uniform over even versus odd parity. Independent bit noise of fixed contrast v in (0,1) yields output law 2^(-N)[1 +/- v^N(-1)^(sum y_i)]. The only nonconstant Walsh coefficient is parity and detector action multiplies it by v^N. One-shot TV is v^N. Writing a=v^N<=1/2, KL=a log((1+a)/(1-a))<=4a^2. For L independent records, Pinsker gives TV<=sqrt(2L)v^N, so a fixed discrimination advantage requires L=Omega(v^(-2N)). The likelihood ratio depends only on count parity, so retaining only the N+1-valued collective count does not remove the obstruction. A small collective state count therefore does not imply a well-conditioned noisy detector. In E2, K must be physically warranted.

This does not refute efficient smooth macroscopic observables: normalized magnetization has no order-one gap for this pair. Full fine count-TV may be an unnecessarily strong target. Conversely replacing a full-law target by a mean without saying so hides a gap.

For trajectory forecasts, x'=lambda x(1-x^2) has solution x(t)=x_0 exp(lambda t)/sqrt[1+x_0^2(exp(2lambda t)-1)]. Initial values +/-c exp(-lambda T) lead to order-one separation at T. Gaussian observation noise of fixed variance needs Omega(exp(2lambda T)) initial samples to choose their signs with fixed reliability. This is a trajectory/initial-information obstruction, not a lower bound for all law or invariant-average forecasts.

Finite-volume uniqueness, a correct free-energy functional, successful fixed-size fits and one preparation's decay do not establish uniform kinetic acquisition or a thermodynamic closure. A finite-size extrapolation must control new slow modes, the size dependence of the gap, conditioning, initial conditional lifts and relevant rare events. Preserve each target: mean, smooth observable, path law, hitting event, single realization and invariant average are different.


# Part H. A genuinely local constitutive operation

# Constructor follow-up: acquired local nonlinear transport

7 November 2026. Written after reading the frozen peer reports. The initial report and its disclosure/exposure accounting remain unchanged.

Later constructive extension: `DUAL_ADAPTIVE_BRACKET.md` supplies a primal/dual observed stopping certificate for density-uniform conductivity acquisition, removing the need to supply numeric homogenization constants to the coefficient algorithm. References below to that particular coefficient-stopping limitation record the earlier stage and are superseded by the linked note. The separate finite-N hydrodynamic constants and arbitrary-force extension remain open.

## Outcome and exact status

The stronger local route has a real constructive operation: **the finite-cell conductivity is estimable in polynomial time and samples without enumerating its exponentially many microscopic configurations**. Its cell gap is derived from the physical exchange rates and explicit Bernoulli reservoirs. A finitely acquired local rate table drives a kinetic Monte Carlo sampler for all these cells. In one dimension the acquired constitutive law has a computable nonlinear PDE solver with an energy error certificate requiring no unknown smoothness modulus. New finite sequences of homogeneous kinetic controls can be obtained by an explicit entropy restart argument.

This is a constructive composition of established homogenization with new derivations of acquisition/error accounting, not a new foundational physical mechanism. Numeric constants in the imported homogenization/hydrodynamic theorem have not been extracted; its entire 109-page proof has not been independently re-established. Arbitrary new weak external force fields are not covered by the imported theorem or by the kinetic-control concatenation. Hardware, favorable full cost and historical novelty are NOT_ESTABLISHED. The broad objective remains OPEN.

## 1. Current governing source

The primary source is Funaki–Gu–Wang, [arXiv:2404.12234v3](https://arxiv.org/html/2404.12234v3), 14 January 2026. The frozen initial used the older v2; preserve both. In v3, Hypothesis 1.1 requires known finite range, translation invariance, rates in [1,lambda], and independence of the two exchanged occupancies. Theorem 1.3 constructs density-uniform correctors. Theorem 1.5 gives algebraic finite-cell conductivity convergence. Theorem 1.4 gives a quantitative H^(-alpha) hydrodynamic error for alpha>d/2, uniformly for individual times in [0,T], under its smooth-profile/normalized-entropy source condition. Proposition 7.1 supplies corrector support <=n and sup norm <=C n^2 log n. Section 7.3 gives the entropy estimate needed for restart.

No arbitrary external-force theorem is stated there. The finite-cell experiment below is matched exactly to its variational coefficient rather than substituted from a periodic or differently bounded cell.

Pins in `sources/`:

- `funaki_gu_wang_2404.12234v2.html`: SHA256 `390d164e8bea5bc0063170e0c79fdd11f43af1464795b1e72ac0a2e616d310bd`.
- `funaki_gu_wang_2404.12234v3.html`: SHA256 `18350f0690e9bb0bb58ce3068f3407b752edc6c98dafc84ccb16b7c5d53252d2`.
- `funaki_gu_wang_2404.12234v3.txt` is an inspection aid retaining math alt text.

## 2. Exact marked-current realization of the finite-cell coefficient

This lemma works in any fixed lattice dimension d. Let V=|Lambda_L|, I=Lambda_L^- (remove its outermost layer), and E=overline(Lambda_L^*) for the source's issued-bond convention, so |E|=dV. Enlarge to a finite set S containing all sites needed to evaluate these local rates, and put G=S minus I. At fixed interaction range, |S|<=C_(d,r)V. Fix rho in [a,1-a], a>0, and |xi|<=1.

The persistent state is eta_I. At each proposal independently draw all ghost bits eta_G as Bernoulli(rho), select a bond b={x,x+e_i}, accept its exchange at rate c_b(eta), update only eta_I to (eta^b)_I and record

\[
d_b(\eta)=\xi\cdot e_i(\eta_x-\eta_{x+e_i}). \tag{C1}
\]

Ghost-to-ghost events may have nonzero marks without changing eta_I. **They must be recorded**. Dropping them changes the coefficient. An exact digital implementation uses a Poisson proposal clock of rate R=lambda dV, a uniform issued bond, fresh ghost bits, and acceptance probability c_b/lambda. This is a local simulation on O(V) bits. A physical implementation would require paid, controllable reservoir refresh and a current counter; it is not automatically a passive finite piece of the original material.

The persistent stationary law is pi=Bernoulli(rho)^I. The marked process is reversible: reverse an exchange and simultaneously replace ghost bits by their exchanged values. The product weight and c_b are unchanged because c_b does not depend on endpoint occupancies, while d changes sign. This pairing includes persistent-state self events.

Write L for the persistent generator, G_0=-L, J_t for the sum of marks,

\[
j(x)=\sum_{\text{marked moves }x\to y}r(x,y,d)d,
\qquad A=\mathbb E_\pi\sum r d^2\le\lambda dV.
\]

All sums average ghost configurations. Marked reversibility gives, for any interior function f,

\[
\mathbb E_\pi\sum r[d+f(y)-f(x)]^2
=A-4\langle j,f\rangle_\pi+2\langle f,G_0f\rangle_\pi. \tag{C2}
\]

The mean of j is zero. Minimization on mean-zero functions yields f=G_0^(-1)j and

\[
v_L(\rho,\xi):=\lim_{t\to\infty}\frac{\mathbb E_\pi J_t^2}{t}
=A-2\langle j,G_0^{-1}j\rangle
=\inf_f\mathbb E_\pi\sum r[d+\nabla f]^2. \tag{C3}
\]

**Matching proof:** d_b=pi_b ell_xi, f ranges over exactly F_0(Lambda_L^-), and averaging interior plus ghosts is the full Bernoulli expectation. Thus v_L/V=xi.cbar(rho,Lambda_L).xi in the source's (1.25). It is neither a periodic approximation nor an arbitrary-boundary one. The normalization is c=1 => cbar=2rho(1-rho)I.

## 3. Polynomial cell gap and finite-exposure bias

### 3.1 The gap is physically derived

A conservative explicit comparison gives

\[
g_L\ge a^2/(12L^2). \tag{C4}
\]

For integer cubes large enough to contain an interior, the proof uses only the following operations. Bernoulli variance tensorizes:

Var_pi f <=rho(1-rho) sum_(x in I) E_pi[f(eta^x)-f(eta)]^2.

Move the spin at x along a straight first-coordinate path to the boundary, flip it using the Bernoulli reservoir, then reverse the swaps. The path has at most 2L+1 moves. Swaps preserve pi. After the single flip the pushed-forward density is at most a^(-1) times pi. Each edge in a column belongs to at most L paths and is used at most twice. Telescoping/Cauchy–Schwarz bounds the product variance by C L^2/a times the sum of internal-swap and boundary-flip square differences. Actual internal rates are >=1, and averaged boundary flip rates are >=a, so the Dirichlet form dominates a/2 times that sum. Enlarging constants gives (C4); tiny cells can be treated separately. No thermodynamic-volume gap is being assumed. The full material retains its diffusive conserved field.

### 3.2 Exact finite-duration control

Define the marked tilted generator L_z f(x)=sum_(y,d) r(x,y,d)[e^(zd)f(y)-f(x)], with the sum including all marked self events y=x. Thus its subtraction uses the total marked-event intensity, not just the exit intensity of the persistent state; at z=0 the self terms cancel. Twice differentiating E_pi exp(zJ_t)=<1,exp(tL_z)1> and using <1,L'_0f>=-<j,f> gives

\[
\mathbb E_\pi J_t^2=At-2\int_0^t(t-s)\langle j,e^{-sG_0}j\rangle ds. \tag{C5}
\]

The spectral theorem and (C3) imply

\[
0\le\frac{\mathbb EJ_t^2}{t}-v_L
=\frac2t\langle j,G_0^{-2}(1-e^{-tG_0})j\rangle
\le\frac{A}{g_Lt}. \tag{C6}
\]

The last step uses 2<j,G_0^(-1)j><=A, since the variational infimum is nonnegative. Conductivity finite-exposure error <=delta follows from

\[
\tau\ge\lambda d/(g_L\delta)=O(\lambda dL^2/(a^2\delta)). \tag{C7}
\]

Initialization is a paid product placement of O(V) Bernoulli bits, not waiting for macroscopic equilibrium.

### 3.3 Finite noisy records and exact counts

For a physical cell assay suppose every current-carrying exchange is counted, its bond orientation is recorded, and the particle-motion sign is independently flipped by a calibrated detector of contrast v>=v_*>0. Write a_l=xi.e_(i_l) for the known directional weight of event l, so its true mark is d_l=a_l sigma_l with sigma_l in {-1,1}. Given the true trajectory, put Q=sum_l a_l Y_l/v and K_2=sum_l a_l^2=sum_l d_l^2. Then

\[
S=\{Q^2-K_2(v^{-2}-1)\}/(V\tau) \tag{C8}
\]

is unbiased for J_tau^2/(Vtau). Indeed the conditional detector variance is (v^(-2)-1)sum_l a_l^2. For one dimension or a unit coordinate direction all nonzero marks have magnitude one, and K_2 is simply their count K; substituting K for K_2 for a general matrix direction would be wrong. Events with a_l=0 contribute zero. The subtraction is essential: squaring a visibility-corrected noisy current alone creates false conductivity. This contract does not silently cover uncounted or mislocated jumps. Distinct physical runs must be fresh; correlations within each run are handled by (C5). Since |a_l|<=1 and K_2<=K, every cap and polynomial resource bound below is unchanged.

Cap a run if its proposal count exceeds H. A Poisson variable of mean Rtau dominates that count. Its explicit tail and fourth moment permit H=C[Rtau+log(MQ_rho d^2/delta_A)] with truncation bias <=delta/8. On the cap event |S|<=B_S=C H^2/(v_*^2 Vtau). Hoeffding needs

\[
M\ge C B_S^2\delta^{-2}\log(2Q_\rho d^2/\delta_A). \tag{C9}
\]

All counts are polynomial in L,a^(-1),lambda,delta^(-1),v_*^(-1), with logarithmic confidence factors. The occurrence of M inside log is removed by any sufficiently large explicit polynomial upper count, or by computing and verifying a Poisson quantile for a proposed finite M. Per density/direction expected updates are MRtau; naive ghost refresh costs O(MRtau |G|). Memory is O(V+local-table size), plus summaries or raw evidence as retained. Hard caps and finite-bit probability simulation add declared failure/bias budgets.

For a deliberately wasteful completely explicit choice, take tau>=1, delta<=1, let q be the total number of density/direction cells, and set W=max(2,Rtau,q/delta_A,delta^(-1),v_*^(-1)), H=ceil(100W^2), M=ceil(10^12 W^20). Then |S|<=4H^2/(v_*^2 Vtau)<=C W^6, Hoeffding error <=delta/4 holds jointly over q cells, and Mq times the Poisson tail beyond H is smaller than delta_A/4. The omitted-tail expectation is bounded by the Poisson factorial-moment identities E[K(K-1)1_(K>H)]=mu^2 P(Pois(mu)>H-2), E[K1_(K>H)]=mu P(Pois(mu)>H-1), mu<=W; the bound (e mu/H)^H makes it <=delta/8. This gives an explicit polynomial construction without solving an implicit sample-count inequality; practical implementations should use the much smaller verified quantile/count calculation.

The digital version sets v=1 and uses acquired rates. It needs no new specimens after local-table acquisition, and charges all random proposals and arithmetic. This is the simplest operational algorithm. For an actual noisy cell, unknown systematic current/source errors can be amplified by squaring and are not removed by more runs. A calibrated path-TV error e changes the capped statistic by at most 2B_S e. All control, preparation and readout refinement needed to reach that inverse-polynomial budget must be charged.

## 4. Uniform densities, controls and corrector queries

Let m=|S|. For p,q in [a,1-a], every Bernoulli product likelihood ratio on S lies in exp(+-m|p-q|/a). Apply this to each nonnegative variational objective before taking infima:

\[
e^{-\theta}v_L(q,\xi)\le v_L(p,\xi)\le e^\theta v_L(q,\xi),
\qquad\theta=m|p-q|/a. \tag{C10}
\]

Because v_L/V<=lambda d, density spacing a delta/(C lambda d m) gives a uniform covering with Q_rho=O(lambda d m/(a delta)) entries. Only O(d^2) directions are needed for matrix conductivity. Affine combinations of finitely many acquired rate tables can be queried directly by the same cell sampler; relative rate comparison also provides a uniform control modulus.

The finite-cell Poisson corrector has polynomial *query evaluation*, although listing all 2^|I| values is exponential. Since pi_min>=a^|I| and |j|<=R,

|P_tj(x)|<=R min(1,a^(-|I|/2)e^(-g_Lt)),
f(x)=integral_0^infinity P_tj(x)dt.

Take tau_f >=g_L^(-1)[(|I|/2)log(1/a)+log(R/(g_L epsilon_f))]. The remaining tail is <=epsilon_f uniformly in x. Starting the acquired-cell simulator at a queried x and averaging integrals of the known j estimates f(x); every integral is bounded by Rtau_f. O(R^2tau_f^2 epsilon_f^(-2)log(1/delta_f)) runs suffice. This does not mean a finite array has stored an entire arbitrary corrector, or that the source's density-free corrector has already been assembled. The PDE predictor only needs conductivity. The use of log(pi_min^(-1)) is polynomial in volume; substituting pi_min^(-1) would unnecessarily make the bound exponential.

The corrector sampling estimate first treats its specified finite rate table as exact; simulating an acquired table computes that table's corrector. A true-table comparison can also be paid polynomially. Let T_mix bound the mean-zero inverse-generator infinity norm; the conservative full infinity-operator estimate is T_mix<=g_L^(-1)[2+|I|log(1/a)], obtained by integrating min(2,a^(-|I|/2)e^(-g_Lt)). Use the analogous That_mix for the acquired table. Relative rate error eta gives ||deltaj||infty<=eta R and ||deltaG||infty-to-infty<=2eta R. The identity Ghat(fhat-f)=deltaj-deltaG f therefore gives ||fhat-f||infty<=eta R That_mix(1+2R T_mix). Refine eta to fit the allocated corrector error. This extra precision is unnecessary for the sharper conductivity monotonicity estimate (C11).

## 5. Noisy acquisition of the microscopic law

Known finite range, translation invariance and the local Markov update architecture are physical structural promises, not conclusions certified against arbitrary hidden-range models. At fixed r,d there are only P=d*2^O(r^d) local patterns. For each prepare a constant-radius pattern with central bond 10. Short native evolution gives

P(central exchange by h)=c(pattern)h+O(C_(d,r)lambda^2h^2).

The bias follows by integrating the probability that a relevant local update has changed the hazard; a constant-radius buffer or a standard bounded-rate influence estimate handles exterior updates. Alternatively count central-bond events. Known nonzero detector contrasts permit corrected bounded scores. With h=Theta(eta), inverse-polynomial preparation/clock bias budgets and O(eta^(-4)log(P/delta_A)) fresh releases per pattern, the elementary estimator attains absolute rate error eta. Efficient event-time estimators may improve the exponent. Reset, clamps if used, clocks, readout, calibration and refinement costs multiply the actual counts. A residual score bias divided by h is a real floor.

Clip estimates to [1,lambda] in the containing dictionary; endpoint independence and reverse-bond consistency must be preserved. On the one uniform rate event, eta<1 gives

\[
(1-\eta)\mathbf c(\rho)\preceq\widehat{\mathbf c}(\rho)
\preceq(1+\eta)\mathbf c(\rho), \tag{C11}
\]

and likewise for every finite-cell coefficient. This follows immediately by comparing all nonnegative variational objectives before minimizing. It is uniform in density and convex combinations of finitely many calibrated tables. In 1D comparison with SSEP gives 1<=D<=lambda, hence |Dhat-D|<=lambda eta before cell/statistical errors. This avoids extensive physical-state sensitivity.

Given valid numerical constants C_h,gamma_h from Theorem 1.5, choose L >=(C_h/delta_c)^(1/gamma_h). Combining (C6),(C9),(C10),(C11), then dividing by 2rho(1-rho), gives a uniform D approximation on [a,1-a]. The division costs at most [2a(1-a)]^(-1). Clip Dhat to [1,lambda], interpolate and integrate its explicit table to an increasing primitive Ahat. Choose the density cutoff to contain the whole PDE trajectory; unforced scalar diffusion preserves the initial range. Do not extrapolate unacquired endpoint behavior.

Only the primitive up to an additive constant matters. For coefficient-error comparison choose A(a)=Ahat(a)=0, so its uniform error on the acquired interval is at most its length times the diffusivity error. For numerical convex-energy bounds Ahat can separately be shifted to Ahat(0)=0 after its elliptic extension; neither the PDE nor its Fourier ODE changes. This avoids charging an unknown integral through unacquired densities.

At fixed class parameters and valid source exponents, all operations are polynomial in inverse coefficient accuracy. The exponent can be very large. The paper does not provide a turnkey numeric pair C_h,gamma_h, and I have not extracted them. This is a proved reduction conditional on effective imported constants, not a numeric certificate service already completed today.

## 6. Fully computable one-dimensional nonlinear PDE

Put A'=D in [1,lambda]. For equal-mass solutions u_t=partial_xx A_t(u) and uhat_t=partial_xx Ahat_t(uhat), assume sup_(t,rho)|A_t-Ahat_t|<=delta_D. Let E=||u-uhat||_dotH^-1^2 and lambda_1=(2pi)^2. Testing with the inverse Laplacian gives

E'<=-||u-uhat||_2^2+delta_D^2<=-lambda_1 E+delta_D^2,

hence

\[
E(t)\le e^{-\lambda_1t}E(0)+\delta_D^2/\lambda_1. \tag{C12}
\]

This horizon-free coefficient-error improvement was supplied by the principal during follow-up; the calculation independently checks. It holds across arbitrary finite kinetic switches. With lower ellipticity a_D instead of 1, replace decay by a_D lambda_1 and the floor by delta_D^2/(a_D^2 lambda_1). Add mass mismatch separately.

An explicit spatial solver avoids a hidden smoothness oracle. Extend Ahat globally with derivative in [1,lambda], let P_M project onto Fourier modes |k|<=M, and solve the nonlinear finite ODE

\[
\dot w_M=P_M\partial_{xx}\widehat A_t(w_M),\qquad w_M(0)=P_Mu_0. \tag{C13}
\]

Write r=(I-P_M)uhat and e=P_Muhat-w_M. Then

(1/2)d||e||_dotH^-1^2/dt
=-<e,Ahat(uhat)-Ahat(w_M)>
<=-(1/2)||uhat-w_M||_2^2+(lambda^2/2)||r||_2^2.

The L2 energy law gives integral_0^T||partial_x uhat||_2^2<=||u0||_2^2/2, independently of switching. Therefore

\[
\sup_{t\le T}\|\widehat u_t-w_M(t)\|_{\dot H^{-1}}
\le C\lambda\|u_0\|_2/[2\pi(M+1)]. \tag{C14}
\]

This uses only the uniform ellipticity/Lipschitz primitive, not derivatives of learned D. The retained state dimension increases with accuracy and its ODE remains nonlinear.

For time computation, (C13) is a convex gradient flow in H^(-1), with gradient Lipschitz beta_M=lambda(2pi M)^2. Explicit Euler maps are nonexpansive in that norm for Delta<=1/beta_M. Taking also Delta<=1/[lambda^2(2pi M)^2] makes the L2 energy nonincrease: expand one step and use ||partial_xx P_M Ahat(w)||_2<=2pi M lambda||partial_xw||_2. Align steps with all K control switches. On the exact Galerkin path, integral_0^T||dot w_M||_H^-1^2<=Klambda||u0||_2^2/2, by summing the convex energy dissipation over pieces while L2 never grows. Nonexpansive Euler telescoping gives the conservative temporal error

\[
E_{time}\le C\beta_M\Delta\sqrt{K\lambda T}\|u_0\|_2. \tag{C15}
\]

Certified quadrature of the explicit Lipschitz Ahat composed with a finite trigonometric polynomial computes its Fourier coefficients with a polynomial modulus in M, precision and the known L2 bound. Per-step H^(-1) arithmetic error theta adds at most (#steps)theta. Thus M=O(lambda/epsilon), inverse-polynomial Delta and theta provide a polynomial algorithm in inverse accuracy, T and finite control-list length. Input profile integration, new-control description length and probability/bit precision are paid. A bounded weak readout of H^1 norm <=1 inherits these errors directly.

## 7. New preparation and new kinetic-drive theorem

### Product source is sufficient; no thermal oracle

The source theorem's reference measure has a corrector exponent

R_N=N^(-1)sum_x partial_x logit(rho0(x/N)) tau_x F_N.

A smooth-profile Bernoulli product already differs in normalized relative entropy by <=C||F_N||infty/N. With the source's F_N=Phi_floor(N^s), 0<s<1/[8(d+2)^2], this is O(N^(2s-1)logN). The user need not prepare the second-order corrected state.

If independently prepared site probabilities differ from the desired rho0(x/N) by at most zeta, their normalized product KL is <=C_a zeta^2; add the same corrector term. Section 7.3's bound is affine in initial entropy before Gronwall, so the weak-observable error has an extra C_T zeta term. One can instead take polynomially shrinking zeta_N to satisfy the literal initial condition in Theorem 1.4. Correlated writer noise requires its own entropy bound; single-site mean accuracy is insufficient. A global writer-TV budget zeta_TV can be converted using finite-alphabet entropy continuity to normalized entropy O(zeta_TV)+h(zeta_TV)/N, not by claiming independent errors.

Every new source pays N placements, independent random bits, calibrated thermal pins/resets, achieved precision, clocks, work/heat and detector refinement. If the physical target is actually run, its N^2T microscopic horizon also pays its N-site holding, local update, drive, readout and reset costs. In 1D its expected number of native update opportunities is O(lambda N^3T). Numerical prediction does not reenact that horizon.

### New homogeneous kinetic sequences

Fix a finite alphabet of homogeneous local exchange tables c^(1),...,c^(q), each satisfying Hypothesis 1.1 and acquired once. A future query gives a previously unperformed finite sequence (a_1,t_1),...,(a_K,t_K), total macroscopic duration T. On piece j the physical generator is N^2 L_(c^(a_j)) and the PDE is

\[
\partial_t\rho=\partial_{xx}A_{a_j}(\rho). \tag{C16}
\]

This is a new driven protocol preserving the common homogeneous Bernoulli equilibrium family. It is not arbitrary force or thermodynamic driving.

At a switch, the old and new corrected reference measures for the SAME current smooth profile have the same product part. Their log density ratio per volume is bounded by C[||F_N^old||infty+||F_N^new||infty]/N=O(N^(2s-1)logN). Hence the new initial normalized entropy is bounded by the old final normalized entropy plus this amount. Apply the source's quantitative entropy estimate on each piece and iterate. For each fixed finite protocol, finite alphabet and smooth source there are C_*,kappa_*>0 such that

\[
\sup_{t\le T}\mathbb E\|\rho_t^N-\rho_t\|_{H^{-1}}^2
\le C_*[\zeta^2+N^{-\kappa_*}]. \tag{C17}
\]

The proof needs that entropy-reference switch; empirical-density convergence alone would not justify restarting. Constants can worsen with K, T and the intermediate profile bounds. No fixed all-protocol/all-horizon microscopic constant is asserted. Uniformity over a bounded protocol class requires actually tracing those dependencies. Every finite protocol is legitimate without presuming it appeared in acquisition.

On the one uniform microscopic-table event, for any declared protocol and mean-zero weak phi with ||phi||_H1<=1,

\[
\mathbb E|\langle\phi,\rho_t^N\rangle-\langle\phi,\rho_t^{num}\rangle|
\le\sqrt{C_*}(\zeta+N^{-\kappa_*/2})
+\delta_D/\sqrt{\lambda_1}+C\lambda/M+E_{time}+E_{arithmetic}. \tag{C18}
\]

Add the mass mode, source and detector errors as applicable. Markov/Chebyshev yields an individual-specimen probability. With effective imported constants this is a size/horizon/noise/preparation/control/all-count theorem for local interacting conserved matter. Numeric constant extraction is still missing for an operational certificate. The PDE error is horizon-free at fixed coefficient error; the microscopic switched-hydrodynamic estimate is not thereby uniform over unrestricted K,T.

## 8. Why arbitrary weak external-force driving is still open here

Tilting bond rates by exp[E(t,x/N).e_i(eta_x-eta_y)/(2N)] formally suggests

partial_t rho=partial_x[D(rho)partial_xrho-chi(rho)D(rho)E],

with the chosen force normalization and chi=rho(1-rho). Acquiring equilibrium conductivity does not establish this driven quantitative hydrodynamic theorem.

Two shortcuts are invalid. A finite-drive current is not its derivative: a remainder bound involving cell generator norms and inverse gap must be proved, and its inverse-polynomial drive amplitude/relaxation/readout costs charged. Equilibrium variance avoids this extrapolation for acquiring the coefficient, not for proving the driven infinite-volume law. Also, a weak O(1/N) perturbation over N^2 time has path relative entropy of order N^d, so the full driven path is not close in TV to the unforced path. One cannot inherit (C17) by a small path coupling.

The constructive missing operation is the second-order entropy/corrector cancellation with the new space/time field, its drive-modified corrector, time derivatives and PDE density bounds. The finite-cell coefficients and their uncertainties are now computable. An actual quantitative driven proof and effective constants remain required. General nonproduct Gibbs measures require an additional physical conditional-mixing derivation; the present product-reversible class does not solve that automatically.

## 9. Principal mass-metric lemma check

I independently checked `../principal/MASS_METRIC_REPAIR.md` in finite dimensions. The resolvent identity and bounds are correct. Douglas factorization justifies replacing the noncommuting C square root by the A square root. The left inner contour arc includes the common zero mode. Constant 8d/(1-d) is safe. An elementary bound for the ray integral is integral_1^infinity e^(-r/2)/r dr <=e^(-1/2)log2+e^(-1)<1 by splitting at 2. This confirms the fixed-control repair; it does not extend itself to arbitrarily switched metrics.

## 10. Diagnostic and ledger

`check_cell_current.py` uses exact fractions in a diagnostic with three active spins and fresh ghosts. Nine combinations of rho and the nongradient rate 1+a eta_(x-1)eta_(x+2) verify marked reversibility, Poisson equation, Green–Kubo = Dirichlet objective, nonnegativity, SSEP factor 2rho(1-rho), and the conservative gap bound. `cell_current_check.json` preserves the output. Enumeration is only a sign/factor/boundary diagnostic; the proposed algorithm uses kinetic Monte Carlo.

The principal identified the general-direction detector correction and tilted-generator notation after this report's first review. Both are repaired above. A new exact detector diagnostic uses weights 1/2 and 1/3, true signs +1 and -1, and contrast 1/2: K_2 subtraction has mean 1/36, exactly the target squared current, whereas replacing K_2 by the event count gives -44/9. This explicitly checks the correction rather than relying on the one-dimensional/unit-weight cell tests.

Proved in this follow-up: exact cell matching; current identity and duration bias; derived polynomial gap; density coverage; local-rate error monotonicity; polynomial corrector query sampling; 1D PDE coefficient, space and time error estimates; source-reference switch and finite kinetic-drive concatenation conditional on the imported entropy estimate.

Imported, not reproved: quantitative homogenization and unforced quantitative entropy/hydrodynamic limit at their exact uniformly elliptic, finite-range, product-reversible scope.

Conditional/open: effective constants, full arbitrary-new-force driven hydro, physical acquisition/refinement realization, matched full-cost advantage and historical priority. C17 is an imported-entropy/finite-switch extension with no operational numeric certificate until the constants and complete applicability checks are supplied. The finite-cell matching/acquisition theorem is the strongest local operation actually proved here. This is a useful acquired local constitutive operation, but it must not be renamed a generic new principle of emergent matter.

# Part I. Certified adaptive primal-dual compilation

# Certified adaptive constitutive acquisition by primal and dual cells

7 November 2026. Follow-up to the principal's proposed dual-cell attack. The independent auditor separately checked the conditional source matching. This note strengthens the coefficient-acquisition result in `FOLLOWUP.md`; it does not remove the independent finite-N hydrodynamic or arbitrary-force gaps.

## Achieved operation

In one-dimensional finite-range uniformly elliptic product-reversible speed-change exclusion, finite noisy local-rate acquisition followed by polynomial local Monte Carlo produces a **certified density-uniform interval for the nonlinear diffusivity**. The stopping test uses observed primal/dual interval width and requires no supplied numerical homogenization convergence constants. The published algebraic convergence theorem proves termination and a polynomial complexity bound at fixed physical class parameters. It is used for runtime, not as an unevaluated error term in the returned interval.

The principal identified the dual representation. The exact normalization, conditional sampling, error bounds and adaptive uniform-density construction below close it. This remains a composition with established homogenization and spectral-gap theory; historical novelty and practical advantage are unestablished.

## 1. Source objects, normalizations and exact finite-scale order

Use Funaki–Gu–Wang [2404.12234v3](https://arxiv.org/html/2404.12234v3), Proposition 4.1 and (4.1)–(4.11). Let Lambda be a cube of volume V, Gamma=Lambda^+, and E=overline(Lambda^*) its issued bonds. In one dimension Lambda={0,...,L-1}, Gamma={0,...,L}, E={(x,x+1):0<=x<L}. The primal diffusivity is

\[
U_L(\rho)=\overline D(\rho,\Lambda)
=\frac{1}{2\chi(\rho)V}\inf_{f\in\mathcal F_0(\Lambda^-)}
 \mathbb E_\rho\sum_{b\in E}c_b[\pi_b(\ell+f)]^2,
\quad\chi(\rho)=\rho(1-\rho). \tag{D1}
\]

It is exactly the open-cell marked-current coefficient from `FOLLOWUP.md`, divided by 2chi. The dual quantity is

\[
\nu_*(\rho,\Lambda,q)
=\frac{1}{2\chi V}\sup_u\mathbb E_\rho\sum_{b\in E}
 [ (\pi_b\ell_q)(\pi_bu)-\tfrac12c_b(\pi_bu)^2]
=\tfrac12q\overline D_*^{-1}(\rho,\Lambda)q. \tag{D2}
\]

For q=1 define H_L=overline D_*^(-1). Both U_L and H_L are nonincreasing along the exactly tiled cubes L=3^j by Proposition 4.1(4). Proposition 5.1 gives the same conductivity limit for the primal and dual families; Proposition 6.9 identifies it with the hydrodynamic conductivity. Consequently, at EVERY such finite scale,

\[
1/H_L(\rho)\le D(\rho)\le U_L(\rho),
\qquad 1\le U_L,1/H_L,D\le\lambda. \tag{D3}
\]

This is the essential certified finite-scale bracket. One does not infer it from two consecutive estimates looking similar. The exact issued-bond tiling and the source's common-limit identification are load-bearing. No arbitrary domain, periodic cell or changed boundary convention is substituted. The source algebraic convergence is not required to compute (D3), but does prove its width tends to zero polynomially in L uniformly on a compact density interval.

## 2. The dual cell is CLOSED; its outside is frozen

Let S=N_r(Gamma), Z=S minus Gamma. At the start of every independent run sample eta_Gamma and zeta_Z independently as Bernoulli(rho). **Hold zeta fixed throughout that run.** Evolve all sites of Gamma by exchanges along E with the rates c_b(eta_Gamma,zeta). This differs from the open primal cell, whose ghost bits are refreshed at each proposal. Confusing these two constructions invalidates the matching.

Conditional on the conserved count k in Gamma and the outside zeta, the stationary law is uniform on the k-particle shell. Product initialization automatically samples precisely the correct binomial count mixture; no rare shell is postselected and no table of all counts/outside patterns is enumerated.

Let G_c=-sum_(b in E)c_b pi_b and G_1=-sum_(b in E)pi_b, and put g_q=G_1 ell_q. In one dimension with q=1,

\[
g(\eta)=\eta_L-\eta_0,\qquad |g|\le1. \tag{D4}
\]

For every fixed count, g has mean zero. Empty and full shells have g=0. More generally g is a known boundary sum, computable from the cell geometry, with a polynomial supremum bound. Reversibility on each shell gives

\[
\sum_b\langle\pi_b\ell_q,\pi_bu\rangle
=2\langle g_q,u\rangle,
\quad\tfrac12\sum_b\langle c_b(\pi_bu)^2\rangle=\langle u,G_cu\rangle.
\]

Therefore the conditional dual optimization is

\[
\sup_u[2\langle g,u\rangle-\langle u,G_cu\rangle]
=\langle g,G_c^{-1}g\rangle,\qquad G_cu=g. \tag{D5}
\]

The inverse is on the mean-zero space of each count shell. The conditional maximizer may depend on k and zeta; Proposition 4.1(1), (4.9)–(4.11) allows these optimizers to be pasted into a single local function independent of rho. Thus the full product average gives exactly

\[
H_L(\rho)=\frac{\mathbb E_{k,\zeta}\langle g,G_c^{-1}g\rangle_{k,\zeta}}
{\chi(\rho)V}. \tag{D6}
\]

The factor is 1/(chi V), whereas nu_* is half of this expression. These normalizations are verified independently in the exact diagnostics below.

## 3. A fully numeric polynomial cell-gap bound

The issued graph on Gamma is connected. For every k and zeta, c_b>=1 implies its Dirichlet form dominates unit-rate symmetric exclusion on this finite graph. Caputo–Liggett–Richthammer's spectral-gap theorem equates the latter gap to the unit-rate random-walk gap. The primary v3 [PDF](https://arxiv.org/pdf/0906.1238v3) has main Theorem **1.2** and its exclusion consequence in **section 1.2.3**. The numbering Theorem 1.1/section 4.1.1 belongs to a different version and must not be mixed with this pin. All hypotheses hold: a finite connected undirected graph, symmetric unit edge weights, and a fixed particle count; uniform-shell stationarity remains valid after fixing zeta.

For a path of n=L+1 vertices, a deliberately weak explicit bound is

\[
\gamma_c\ge n^{-2}. \tag{D7}
\]

One can use the exact path eigenvalue 2[1-cos(pi/n)] instead. A general connected issued graph with n vertices and diameter d_G has random-walk gap at least 1/n^2 when d_G<=n-1, up to an inessential conservative factor: write uniform variance as (2n^2)^(-1)sum_(x,y)(f(x)-f(y))^2, telescope along shortest paths, and bound every edge's ordered-pair congestion by n^2. This gives the safe fully explicit bound 1/n^2. For clarity the operational theorem here uses the one-dimensional path. No homogenization constant and no minimum shell probability enters (D7).

## 4. Bounded finite-exposure dual estimator

Each conditional chain is stationary. Its spectral theorem implies

\[
H_L=\frac1{\chi V}\int_0^\infty\mathbb E[g(X_0)g(X_t)]dt,
\quad
0\le H_L-H_{L,\tau}
\le\frac{G_{max}^2e^{-\gamma_c\tau}}{\chi V\gamma_c}. \tag{D8}
\]

This uses mean zero on every shell, not just cancellation after mixing different conserved counts. The right side is explicit. In 1D G_max=1. Choose tau by the logarithm of this bound to make the tail <=e_H/4.

A practical estimator needs only one random-time readout. Independently choose S uniform in [0,tau], run the closed cell to S, and record

\[
Y_H=\frac{\tau}{\chi V}g(X_0)g(X_S). \tag{D9}
\]

Its expectation is H_(L,tau), and |Y_H|<=tau G_max^2/(chi V). Averaging M_H fresh runs and Hoeffding gives a two-sided statistical interval of radius e_H/4 with

M_H=O([tau G_max^2/(chi V)]^2 e_H^(-2)log(2/alpha_H)).

Add the nonnegative tail only to the upper endpoint. Clip H to [1/lambda,1]; its upper confidence endpoint H^+ is strictly positive, so 1/H^+ is a certified lower diffusivity bound.

In the digital version g is exact and the acquired table supplies rates; Poisson proposals have rate <=lambda V and act on O(V) bits. A hard proposal cap and finite-bit random-time/probability errors add explicit budgets. No matrix on 2^(L+1) states is built. Physical two-time readout is also possible under a declared nondestructive classical detector: use independent calibrated unbiased scores for the boundary occupations at the two times. If score magnitude is <=G_max/v_*, their product is unbiased and its bound increases by v_*^(-2). Initialization, frozen outside clamps, measurement, holding, detector calibration and systematic-bias refinement must all be paid. Unknown correlated detector noise does not preserve (D9).

For a physical source deviating from the declared product law by path/source TV e, the bounded score expectation changes by at most 2tau G_max^2 e/(chi V v_*^2). Thus inverse-polynomial preparation/control errors suffice at these polynomial durations, but are not automatically supplied. Acquiring a constant-radius microscopic table and simulating digitally avoids needing large physical closed cells.

## 5. The primal upper endpoint is particularly simple

The open-cell current formula in `FOLLOWUP.md` gives

\[
\frac{\mathbb EJ_\tau^2}{2\chi V\tau}\ge U_L,
\quad
0\le\frac{\mathbb EJ_\tau^2}{2\chi V\tau}-U_L
\le\frac{\lambda}{2\chi g_{open}\tau},
\quad g_{open}\ge a^2/(12L^2). \tag{D10}
\]

Therefore an upper statistical confidence endpoint for the finite-duration current-square mean is already a valid upper endpoint U^+ for U_L: no unknown asymptotic bias is subtracted. The explicit bias bound determines a sufficiently long exposure for efficient stopping. The correct noisy weighted-current square subtraction and total marked self-event convention remain as repaired in `FOLLOWUP.md`. In the scalar 1D theorem the nonzero marks are simply +/-1.

All primal variance caps and sample counts in that file are explicit polynomial functions of L, a^(-1), lambda, e_U^(-1), detector contrast and confidence. One may use the wasteful W,H,M recipe there or a directly verified tighter Poisson cap.

## 6. Density-uniform confidence intervals without a hidden modulus

Fix rho in [a,1-a]. Let m be the number of bits in the enlarged local envelope required by both cells. At fixed r, m=O(L). The normalized primal and dual variational quantities satisfy, for p,q in this interval,

\[
e^{-\theta}U_L(q)\le U_L(p)\le e^\theta U_L(q),
\quad
e^{-\theta}H_L(q)\le H_L(p)\le e^\theta H_L(q),
\quad\theta=(m+2)|p-q|/a. \tag{D11}
\]

For the primal, compare the Bernoulli weights of every nonnegative variational objective before taking infima, then include the chi normalization. For the dual, its conditional optimum w(k,zeta)=<g,G_c^(-1)g> is nonnegative and independent of rho, so the same product likelihood-ratio bound applies after averaging w; again include chi. The +2 pays the two factors in chi=rho(1-rho). This argument is not a bound on the signed finite-time single-run score; it is a modulus for the exact dual coefficient.

At scale L, choose density mesh radius h_L<=a epsilon/[C lambda(m+2)] and compute U^+,H^+ at every grid point. For any p nearest q, the interval

\[
I_L(p)=\left[e^{-\theta}/H_L^+(q),\ e^\theta U_L^+(q)\right]\cap[1,\lambda] \tag{D12}
\]

contains D(p) on the joint cell confidence event. Thus it is a uniform interval function on the ENTIRE density interval. The number of grid points is O(lambda m/(a epsilon)), polynomial. Only the observed endpoints enter the stopping test. There is no unknown D derivative or uncomputed functional.

## 7. Acquired-rate uncertainty and actual stopping algorithm

Acquire the local microscopic table to relative error eta<=epsilon/(64lambda), with one confidence event as in `FOLLOWUP.md`. Clip the acquired table to [1,lambda]. Its own homogenized diffusivity satisfies

(1-eta)D_true <=D_acquired <=(1+eta)D_true

by variational monotonicity. The primal/dual cell procedure computes certified bounds for D_acquired. Inflate any interval [ell,u] to

\[
[\ell/(1+\eta),\ u/(1-\eta)]\cap[1,\lambda]. \tag{D13}
\]

This retains a controllable O(lambda eta) noise floor. Alternatively use separate monotone lower/upper rate tables. No larger physical system is used to improve the error by assumption.

For target epsilon, perform stages j=1,2,... with L_j=3^j. At each stage:

1. Choose the density grid and explicit cell time/statistical error budgets, e.g. e_U<=epsilon/128 and e_H<=epsilon/(128lambda^2), with analogous width slack for (D11) and the rate inflation.
2. Acquire both finite-cell confidence endpoints for every grid point, using fresh digital randomness and all known caps. Allocate total failure probability alpha_j=alpha*2^(-(j+1)^2), distributed across that stage's finite cells. Its sum is <alpha.
3. Form the uniformly widened, rate-inflated intervals (D12)–(D13). Stop if their maximum width is <=epsilon. Return those intervals or their midpoint as an epsilon-accurate constitutive table. If an interval is inconsistent, continue/refine and retain the diagnostic rather than invent an endpoint.

On the one joint event, EVERY returned interval is valid, including at the data-selected stopping stage. This remains true without knowing any numerical homogenization constants. The published density-uniform algebraic convergence guarantees that the true primal-dual width is <=epsilon/4 at a scale L_* polynomial in epsilon^(-1) for the fixed physical class. The other error budgets fit the remaining slack, so a statistically good stage at or beyond L_* stops.

Per-stage costs are polynomial in L_j, epsilon^(-1), a^(-1), lambda and log(1/alpha_j). Therefore the accumulated work through the first such scale is polynomial in inverse accuracy at fixed class parameters. The constants/exponent depend on the published convergence theorem but need not be known by the algorithm. If an expected-runtime statement is desired, the squared-exponential alpha_j schedule is useful: after the convergence scale, reaching stage j+1 requires a statistical failure at stage j. Stage work grows only exponentially in j times a polynomial in j, while alpha_j decays as 2^(-j^2), so its expected tail is summable. This argument is conditional on the fixed acquired rate table; every clipped table satisfies the same ellipticity/range class, so it does not require a successful rate-learning event for termination. Correctness for the true material additionally uses that event.

This distinction matters: the procedure supplies an effective, observed stopping certificate; the theorem supplies a class-dependent polynomial complexity assurance. It does not supply a convenient numeric worst-case runtime constant or an optimized exponent. No unknown asymptotic constant appears in the returned error interval.

## 8. Scope earned and remaining gaps

At a chosen accuracy and confidence, the retained finite constitutive table covers all densities in [a,1-a]. A finite alphabet of microscopic kinetic laws can be acquired and certified once each. The same tables support new smooth product preparations and new finite homogeneous kinetic protocols through the nonlinear PDE solver in `FOLLOWUP.md`. The primitive-error and Galerkin estimates there are constructive and need no homogenization rate constant.

The numeric finite-N hydrodynamic constants in C17/C18 remain a separate limitation. Observed coefficient bracketing does not certify the finite-N hydrodynamic error. Arbitrary spatial/time force drives still require a verified driven entropy/corrector theorem. Initial source promises, physical same-law transfer, detector refinements, all reset/hold/control/heat/work costs and an equal-information incumbent remain explicit. This note closes the **effective conductivity stopping** gap only; it must not be presented as closing those other gates.

## 9. Exact diagnostic

`check_dual_bracket.py` checks 24 exact-fraction cells at L=3,5, rho=1/3,1/2,2/3, for both gradient rates 1+a(eta_(x-1)+eta_(x+2)) and nongradient rates 1+a eta_(x-1)eta_(x+2), with a=0,1. It solves only tiny diagnostic Poisson equations conditional on frozen outside/count and verifies the normalization, 1<=1/H<=U<=lambda, SSEP equality, and, in the gradient subclass, the known infinite-volume D=1+2a rho lying in the bracket. `dual_bracket_check.json` retains all values. All 24 cases pass.

The open primal cells at L=3,5 happen to have zero refreshed-ghost drift and hence zero Poisson correction, even for this nongradient rate. To avoid using only that easy special case, the script also checks the nongradient L=7, rho=1/2, a=1 cell: its exact primal value is 276736825/222538988, strictly below the uncorrected activity value 5/4. This passes a genuinely nonzero Green–Kubo-correction stress test. The earlier nine-cell current diagnostic remains valid but should not be described as having tested a nonzero corrector.

The algorithm above does not enumerate these states. The diagnostic checks factors, signs, frozen-vs-refreshed boundaries and the specific known comparator; it does not prove the infinite-volume source theorem or historical priority.

# Additional transport predecessors

Primary full texts inspected; cache pins in sources/TRANSPORT_PREDECESSOR_PINS.json. No black-box theorem is imported from these comparators.

Arita–Krapivsky–Mallick [1611.07719v2](https://arxiv.org/html/1611.07719v2), III.2/equations31–33, already gives increasing finite-subspace variational upper diffusivity bounds for nongradient generalized exclusion and tests new reservoir profiles. State/subspace enumeration need not be polynomial in cell volume; a lower finite-noise certificate is a distinct operation. Their [1711.10616v2](https://arxiv.org/html/1711.10616v2), sections3–4/8, equations11/17, applies related upper bounds to a kinetically constrained gas. Its zero rates/high-density slowing fall outside the uniform positive-rate hypothesis used here. No new ability to approximate nongradient diffusivity is claimed.

Embacher–Dirr–Zimmer–Reina [1710.03680v3](https://arxiv.org/html/1710.03680v3), sections2–3/6 (Proc.R.Soc.A474(2018)20170694), extracts nonlinear diffusivity from nonequilibrium fluctuations under local-equilibrium/Gaussian premises, with preparation/storage/simulation costs. It leaves a general rigorous theory open; its Kawasaki-type outlook reports exploratory mobility measurements while the entropy and hydrodynamic limit remain unproved, so it does not determine the diffusivity there. A proof-based bracket differs from treating a formally inferred SPDE or successful fit as a finite-noise certificate, while this remains a competent matched numerical incumbent.

Funaki–Gu–Wang2404.12234v3 supplies the decisive homogenization/duality machinery in the sampling construction. Green–Kubo, Poisson representations, fluctuation measurements, local variational approximation and nonlinear hydrodynamics are established. Priority of the particular self-certifying noisy compilation remains UNKNOWN. Practical advantage over the strongest equally informed implementation has not been measured.

# Part H. Primary-source, novelty and dependency audit

All nine sources supplied in the question were read beyond abstracts, including all three original Zenodo PDFs. Exact versions, hypotheses, passage locations, applicability limits and cached bytes are in [the machinery audit](COLLECTIVE_INFORMATION_RESEARCH_RECORD/initial/machinery.md), [the hostile audit](COLLECTIVE_INFORMATION_RESEARCH_RECORD/initial/auditor.md), [source completion](COLLECTIVE_INFORMATION_RESEARCH_RECORD/auditor/POST_FREEZE_SUPPORT.md) and [the constructive cross-review](COLLECTIVE_INFORMATION_RESEARCH_RECORD/machinery/FOLLOWUP.md). None is imported from snippets. The block-model proofs are self-contained except for the explicitly matched exclusion/Kawasaki gaps. The local constitutive parts additionally import the quantitative homogenization, duality and unforced hydrodynamic results identified there.

| Exact primary result | What is inherited and what is not |
|---|---|
| Caputo–Liggett–Richthammer [0906.1238v3](https://arxiv.org/abs/0906.1238v3), Theorem1.2, Corollary1.3, section1.2.3 | Connected weighted graph exclusion gap equals the one-particle gap; exact conditional/rate applicability proved above. This version is titled A recursive proof of Aldous' spectral gap conjecture. Theorem1.1/section4.1.1 was a version mismatch in the initial note, corrected here. |
| Boudou et al. [math/0505533v2](https://arxiv.org/html/math/0505533v2), Theorem3.1, Corollary3.3 | Density-uniform high-temperature Kawasaki gaps, with actual potential norm, normalization, range and block geometry retained. This does not certify generic low-temperature discarded matter. |
| Hilder–Sharma [2201.10256v2](https://arxiv.org/html/2201.10256v2), Theorem3.1, Lemma3.8/Remark3.9, Proposition4.11 | Uniform-time conditional coarse-graining already exists; its useful prefactors/positive-initial-data and reduced-relaxation dependence matter. Our relative-energy estimate is a specific alternative, not the invention of coarse-graining. |
| Blassel [2610.36078v1](https://arxiv.org/html/2610.36078v1), Definition3, Theorems5/7, Corollary8, Proposition11 | Existing killed/conditioned-flow and exit-event bounds use actual QSD conditional measures and separation constants. Those measures are not supplied for free. Our equilibrium-conditioned mean-lifetime comparison is a distinct target. |
| Stephan, ZAA44(2025), [DOI10.4171/ZAA/1796](https://doi.org/10.4171/ZAA/1796), Proposition2.8 | Existing Markov coarse-graining/reconstruction; reduced relaxation enters the transient estimate. Full PDF checked. |
| Tian–Kannan, SAA24(2006), [primary PDF](https://people.nmsu.edu/jtian/publications/2006-3.pdf), Definition2.9, Theorems2.10–2.11 | Established block-sum strong-lumpability criterion; applying it uniformly to controls is routine. Passive closure alone is weaker. |
| Lin–Lu–Vanden-Eijnden [1609.02511v2](https://arxiv.org/html/1609.02511v2), Theorem5.2, section6 | Exact optimal-milestoning mean times under backward-isocommittor surfaces, regularity, correct reinitialization and unique ergodicity. Discovering/sampling these is not free. Rare-event acceleration itself is known. |
| Aristoff–Bello-Rivas–Elber [1505.02451v2](https://arxiv.org/html/1505.02451v2), Theorem3 | Exact flux/mean-time identity with actual milestone flux measure and finite expected crossing count. The exact v2 label is Theorem3, not Theorem3.3. Correct-source short trajectories are a strong incumbent. |

Mori–Zwanzig noiseless operator learning, Zhu's finite-rank hypocoercivity theorem, formally exact power functionals, neural-force transfer and adiabatic constrained dynamics retain their real premises. Our kinetic nonidentifiability example concerns inference without warranted mobilities; it does not refute a fully specified Brownian model or its formal functional identity. The later [Han–Zhao–Li record](https://arxiv.org/abs/2609.37392) is withdrawn v2 (2October2026) for dataset-publication timing concerns; this is not evidence that its mathematics is false. The inspected v1 local-realization result is preserved at its actual scope.

The original Zenodo PDFs [20410346](https://zenodo.org/records/20410346), [22722557](https://zenodo.org/records/22722557) and [23587917](https://zenodo.org/records/23587917) respectively assume useful orthogonal decay, prove geometric memory for a fixed block-linear surrogate, and introduce physical/regularization axioms. Valid conditional algebra is credited; their application to generic matter remains unproved. The audits distinguish an axiom from its derivation rather than awarding a universal law on the basis of a title or script.

Important additional incumbents are Katsoulakis–Plechac–Sopasakis, [SIAM JNA44(2006),2270–2296](https://doi.org/10.1137/050637339), on stochastic-lattice coarse-graining and transient/metastable numerical acceleration, and Katsoulakis et al., [M2AN41(2007),627–660](https://www.numdam.org/articles/10.1051/m2an:2007032/), on systematic equilibrium coarse graining and error control. No uninspected theorem number is a dependency. The full audits also inspect Galves et al.1008.2740v3, Lucia et al.1409.7809v2 and Rudolf–Schweizer1503.04123v3 as local-forgetting/stability comparators. A literal tail error in the first source is scoped to the printed total-event bound, not used to dismiss its other results.

The exact count compiler, relative-energy estimate, mass repair and complete acquisition/source/error accounting are the constructions written and checked in this return. Conditional averaging, Poincare estimates, analytic semigroups, conductance comparison, birth/death formulas, propagation of chaos and constitutive variance are established machinery. Historical novelty of the particular synthesis is UNKNOWN. Practical superiority over the same-information incumbent is NOT ESTABLISHED. No repository deposit or reviewer agreement is proof of priority or hardware advantage.

# Part I. Remaining decisive operations

1. **Discover sufficient fields/history.** Counts and kinetic architecture are supplied here. A general method must acquire preparation distinctions and add dynamically relevant cross fields with controlled conditioning/cost; entropy or finite representation rank alone does not do this.
2. **Construct conditional kinetics beyond favorable sectors.** Derive useful physical mixing and conditional averages, or replace the representation. Do not put the original many-body solve into an unknown functional or gap. The local constitutive route above is a concrete competing attack. Its remaining finite-N gate is a nonlinear one-/two-block or renormalized-energy replacement: measured small-cell constitutive residuals do not already establish it.
3. **Earn growing real control.** Bounded-action reuse may be exponential under extensive field changes. Frozen mass-metric stability is not arbitrary switched empirical-metric stability. A control net retains its curse when independent actuator dimension grows.
4. **Evaluate a growing noncontractive collective field.** Count compression does not solve a large interacting count process. A new stable hierarchy, memory representation or independently proved hydrodynamic limit must earn the computational gain, including rare events if those are the target.
5. **Meet physical access and matched full costs.** Pins, conservation during conditional mixing, clocks, detectors, work and source precision must actually satisfy their warranted budgets. A fixed unknown leakage/error floor survives repetitions. Compare against conditional Monte Carlo, learned force functionals, milestoning, network elimination and the strongest hydrodynamic construction with the same information and controls.

The broad requested foundational principle remains OPEN. The strongest actual results and the most promising constructive opening are retained without relabeling established tractable mechanisms as a discovery.
