# ASTRA FRONTIER — Energy-interrogated, source-complete defect closure

Research checkpoint: 14 October 2026. Intrinsic model time is distinct from computation time.

## 0. Status

The retained objective is reliable molecular residence/reaction-time prediction under genuinely hidden conformational gating. This investigation attacks a dominant cooperative trap rather than extending the previous softened-East chain.

The executed operation is: infer a microscopic interaction graph and coefficients from energy interrogations under a declared pairwise model class; derive a small slow-observable space and a global relaxation bound for its orthogonal complement; discover an energy-defect sector; and certify the full source response, including every configuration omitted from that sector.

A 24-coordinate ferromagnetic Glauber ring with a tagged local reaction was treated after 301 exact energy/weight interrogations. Its mean lifetime lies in [144878.2730259796, 156850.6573922623], ratio 1.0826375419601, although its state space has 16777216 configurations. The response solve uses 554 low-defect configurations; exact residual evaluation touches their 10178-state one-flip neighborhood and includes the source on all remaining configurations analytically. The global spectral closure has dimension TWO, not an assumed low tensor rank. A second model can be distinguished by more than 31.4% in mean residence even after the stated energy and microscopic-clock uncertainties are propagated.

This is a restricted, model-conditional capability. It is NOT a calibrated molecular prediction, an independently verified breakthrough, proof of historical novelty, or a demonstrated advantage over the strongest tensor/WE/TAMMBER/AIMMD implementations. Glauber spectral structure, finite-state projection, Schur complements, variational residual bounds and energy-based truncation are established ingredients. The candidate contribution for further priority review is their constructive source-complete acquisition/certification combination, including the finite-rarity bound in Section 6.

The most important premise is explicit: the global energy is pairwise in elementary binary coordinates and the microscopic dynamics follows the stated heat-bath law. Sparse probes do not establish those premises. General force fields, unknown configuration-dependent mobility and strongly symmetry-breaking gates remain unresolved.

## 1. Information inherited, and mechanisms that did not solve the hard case

The previous conditional-envelope construction bounded the mass source and transport/reaction forms independently. A 100-fold interaction-weight uncertainty in the dominant all-closed trap yielded a lifetime ratio above 5.5 million. Its source-aware Schur identity correctly retained boundary response, accumulated source and internal residence, but obtaining useful coupled constraints remained open.

### Local response moments

For a reversible un-killed generator L >= 0 in L2(pi), killing k >= 0 and K=L+k, split constants from mean-zero functions. Write mu=<k>, g=k-mu and C=Q K Q on the mean-zero space. Exact block elimination gives

    tau_eq = 1/[mu - <g,C^{-1}g>].

This is standard Schur algebra. Locality permits computing finitely many moments of C from local generator action and Gibbs marginals, without trajectories. Gauss/left-Radau bounds on the inverse moment are also prior art.

The implemented local-moment procedure was useful for rare populations caused by a strong field, but failed for the cooperative trap. At n=32, zero field and coupling parameter t=100, four acquired moment levels still allowed <g,C^{-1}g> to exceed mu, so no finite lifetime upper bound followed. The broad result was not reported as a prediction. The exact results and failures are in pilot.jsonl.

The moment code uses only a proven positive Dobrushin bound when available. An unused exploratory canonical-gap fallback was removed before packaging; no result depends on it.

### Polynomial fitting and iterative refinement

Linear and quadratic trial fields, and preconditioned iterations using a larger single-spin slow space, were also tested. They gave valid but wide intervals in the cooperative regime. For n=16,t=1000, a linear trial gave ratio about 4.56; eight iterative refinements reached only about 1.483 while increasing the number of polynomial terms to 1472. A first implementation using repeated Fraction products timed out; the completed implementation uses common-denominator contractions. All completed pilots are retained. These failures motivated energy-defect selection rather than assuming a favorable low-rank response.

### Energy alone does not determine the clock

Detailed balance leaves symmetric conductance factors undetermined. The same energy can have arbitrarily slow microscopic mobility. Thus an energy-interrogation operation still needs an explicit microscopic mobility law or independently justified bounds on it. This investigation does not hide a basin-to-basin rate in that input.

## 2. Physical model and actual acquisition interface

The independently established kinetic model is a zero-field one-dimensional ferromagnetic Ising ring with Glauber/heat-bath dynamics. A local reaction hazard is added as an authored diagnostic; this is not an independently selected protein or atomistic force field.

Initially the learner knows the number n of elementary binary coordinates and the pairwise model class, but not their ring ordering, coupling or uniform field. With x_i in {0,1}, weights have the form

    w(x) = r^(sum_i x_i) t^(sum_{(i,j) in E} 1[x_i=x_j]),  t>1.

The graph E is an unknown cycle. The hard-trap compiler accepts the recovered symmetric case r=1. The single-coordinate microscopic law is heat bath with attempt frequency nu; the reaction hazard is k(x)=kappa x_0. nu and kappa are model coefficients, not acquired metastable escape rates.

The synthetic oracle returns exact rational Boltzmann weights w(x), equivalently dimensionless energies -log w(x). This choice makes all subsequent calculations rational. A laboratory has not implemented this oracle. Numerical evaluation of an explicit interaction law is the intended computational interpretation; finite-error energy observations are addressed separately below.

### Recovering the global pairwise law

Query w(0), w(e_i), and w(e_i+e_j) for every pair. Then

    R_ij = w(e_i+e_j) w(0) / [w(e_i) w(e_j)]

is t^2 on an edge and 1 otherwise. The learner reconstructs the graph, checks that it is one connected cycle with uniform coupling, and computes

    r = t^2 w(e_i)/w(0).

The query count is 1+n+binom(n,2), or 301 at n=24. The target coordinate remains physical coordinate 0; the recovered cycle is ordered from it. Eighteen relabeling/parameter fixtures were audited, including nonzero field recovery. No gate ordering is supplied by the oracle. The computation of each synthetic energy inspects n interactions, so the total arithmetic for acquisition is polynomial and is charged.

This reconstructs the energy everywhere ONLY within the declared global pairwise class. A higher-order energy term supported at a configuration with at least three excited bits can leave every query unchanged. No claim is made that pairwise structure was established from these observations.

### Local kinetic coefficients

Set sigma_i=2x_i-1, and

    eta=(t^2-1)/(t^2+1).

The flip rate is

    q_i(sigma)=nu/2 [1-eta sigma_i(sigma_{i-1}+sigma_{i+1})/2].

This follows by evaluating the specified heat-bath law on the recovered energy, not by waiting for a rare transition. Creating a two-wall defect in an aligned configuration has rate nu/(t^2+1). The gate is genuinely rare at large t.

nu and kappa are independent physical clocks. They can in principle be calibrated in balanced single-coordinate and activated-reaction settings only if the intervention is known to preserve the assumed local prefactor law. No such physical calibration was executed. The exact prototype takes them as microscopic model inputs; the uncertainty calculation uses declared intervals.

## 3. Acquiring the slow space and controlling everything outside it

Let L=-Q be the un-killed positive generator in the actual Gibbs Hilbert space. Define collective magnetization

    m(sigma)=(1/n) sum_i sigma_i.

Direct local algebra gives

    L 1=0,
    L m=lambda m,
    lambda=nu(1-eta)=2nu/(t^2+1).

The slow lifetime scale is derived from elementary local rates. It is not measured by long trajectories. This Glauber magnetization identity is established prior art, not a newly invented invariant.

The relevant additional construction is a complete lower bound on all modes orthogonal to span{1,m}:

    L >= lambda P_m + gamma (I-P_1-P_m),
    gamma=nu[(1-eta)+4eta/n^2].                          (1)

Here P_m is the orthogonal projector onto m, not multiplication by m. Unlike lambda, gamma stays of order nu/n^2 as t grows.

### Derivation of the complementary bound

For a spin monomial chi_S=product_{i in S} sigma_i,

    L chi_S = nu |S| chi_S
        -nu eta/2 sum_{i in S, j=i+-1} chi_{(S\{i}) symmetric_difference {j}}.

The degree is unchanged or reduced by two. Thus the monomial filtration gives a block-triangular representation. On the degree-p quotient, the diagonal block is p nu(1-eta) plus p nearest-neighbor walkers with jump rate nu eta/2, killed on collision.

For p>=2, extend functions by zero to the labeled product space and retain the Dirichlet energy of any two walkers. All other walker energies are nonnegative. Their separation is a walk on {1,...,n-1}, killed at 0 and n, whose lowest energy is 2nu eta[1-cos(pi/n)]. Additional exclusions only increase this Dirichlet energy. Hence every degree-p block has spectrum at least

    p nu(1-eta)+2nu eta[1-cos(pi/n)]
      >=2nu(1-eta)+4nu eta/n^2.

For the degree-one block, the nonuniform Fourier modes have eigenvalues nu[1-eta cos(2pi j/n)], bounded below by nu[(1-eta)+8eta/n^2]. The uniform magnetization is the one exceptional mode lambda. Because L is reversible and span{1,m} is invariant, these block spectral bounds imply (1). The rational trigonometric bounds use sin(z)>=2z/pi on [0,pi/2].

This proof was checked against exact small matrices; it is not externally reviewed or formally verified. It specializes to the stated zero-field homogeneous cycle. A generic perturbed or nonlocal mobility law cannot inherit (1).

## 4. A two-dimensional inverse that retains hidden residence

Let K=L+k, with k=kappa(1+sigma_0)/2. From (1),

    K >= C = lambda P_m + gamma(I-P_1-P_m)+k.           (2)

All expectations needed by C can be acquired from the recovered energy. With u=(t-1)/(t+1),

    Z=(t+1)^n+(t-1)^n,
    pi(sigma)=t^(n-d(sigma))/Z,
    s=<m^2> = (t/n)(1-u^n)/(1+u^n),
    <m sigma_0>=s.

Here d is the number of domain walls. These are exact finite-ring partition/correlation formulas, computed rather than supplied as equilibrium data.

Let B have columns 1 and m, G=diag(1,s), T=diag(0,lambda), D=gamma+k and

    J=(T-gamma I)G^{-1}.

Then C=D+BJB*, and

    C^{-1}=D^{-1}-D^{-1}B (I+J H)^{-1} J B*D^{-1},
    H=B*D^{-1}B.                                       (3)

Only a 2-by-2 matrix is inverted. Write

    a=[1/gamma+1/(gamma+kappa)]/2,
    b=[1/(gamma+kappa)-1/gamma]/2.

Then D^{-1}=a+b sigma_0 and H=[[a,bs],[bs,as]]. Every term is rational for rational t,nu,kappa.

For ANY admissible trial v, define r=1-Kv and

    L_v=2<1,v>-<v,Kv>.

The standard exact residual identity and (2) give

    L_v <= tau_eq <= L_v+<r,C^{-1}r>.                  (4)

The significance is not a new residual identity; it is obtaining a useful inverse minorant from the acquired physical law while retaining the slow source direction explicitly.

## 5. Discovering an energy-defect sector without a full conformation list

From the recovered ferromagnetic cycle energy, the compiler selects S={configurations with zero or two domain walls}. These are the aligned configurations and every single contiguous reversed domain, not one supplied dominant path. Its size is

    |S|=2+n(n-1).

All low-energy nucleation locations and both directions of growth are included. A sparse killed equation K_SS v_S=1 is solved, with v=0 outside S. Exiting S is artificial absorption only in the trial problem, not in the certified model.

The true residual is evaluated as

    r(x)=1-(Kv)(x)

EVERYWHERE. It is 1 outside the one-flip neighborhood of S, not zero. Inside that neighborhood it is obtained from local elementary rates. Its constant component represents every unlisted source state. Computing <r^2/D> and <B,r/D> consists of their complete constant-source expectations plus finitely supported corrections. Thus the omitted source and its internal residence are not discarded.

The one-flip neighborhood has O(n^3) configurations. At n=24, the trial has 554 entries and its residual neighborhood 10178 entries, versus 16777216 total configurations. This is selective polynomial-size enumeration, not zero enumeration of every configuration. The procedure does not reconstruct all hidden states.

Floating sparse solves propose v. The verifier rounds entries to dyadic rationals and evaluates (4) with exact Fraction arithmetic. No spectral estimate or floating solve residual is passed off as the final certificate.

### Same-response ablation: what information actually helps

Holding the acquired energy law and the entire trial response FIXED, replace the resolved slow-mode/complement operator by the ordinary global-gap bound L>=lambda(I-P_1). The resulting certificates are much broader:

| n | t | Global-gap ratio | Acquired-complement ratio |
|---|---:|---:|---:|
| 16 | 1000 | 98.23733 | 1.01246008 |
| 24 | 1000 | 287.91950 | 1.08263755 |
| 16 | 10000 | 98.25725 | 1.00012465 |

These exact-rational ablations are in gap_ablation.json. Thus merely selecting low-energy states or computing a plausible trial does not explain the useful result: one must distinguish the genuine collective slow direction from the remaining response. The microscopic local law supplies that distinction here. No extra trajectory training or changed trial function is used in this comparison.

## 6. A finite-rarity guarantee, not merely a large-number example

For n>=4, t>=n and fixed positive nu,kappa, let v be the EXACT killed solution on S. Define

    D_n=1+n(1+nu/kappa).

The same source-complete bound obeys

    (U-L)/L <= [D_n^2/t^2]
                  [(63/4)n^7+(9/4)(nu/kappa)n^5].       (5)

The constants are deliberately conservative and much weaker than the computed intervals. Equation (5) nevertheless shows polynomial, rather than exponential-in-n, sufficient rarity for a requested relative accuracy. At fixed n and clocks, the certified relative width is O(t^-2). It does not assert favorable scaling at arbitrary t/n or arbitrary field.

### Proof

Let H be the omitted region with at least four walls. Counting wall sets gives

    pi(H) <= sum_{j>=4} binom(n,j)t^-j
          <= e^(n/t)(n/t)^4/24 <= n^4/(8t^4).

A two-state comparison for the target bit uses minimum opening rate nu/(t^2+1), maximum closing rate nu t^2/(t^2+1), and killing kappa. It gives

    0<=v(x)<=(1/nu+1/kappa)(t^2+1).

The exact residual is zero on S, nonnegative on H, and bounded there by D_n(t^2+1). Consequently, writing R=<r> and N^2=<r^2>,

    R<=n^4 D_n/(4t^2),
    N^2<=n^4 D_n^2/2.

For f=a0+b0 m+h, with h orthogonal to 1 and m, its C-energy controls lambda s b0^2, gamma||h||^2 and kappa||1_A f||^2. Since <1_A m>=s/2 and the projection of 1_A onto the orthogonal complement has norm sqrt(1-s)/2,

    |<r,f>| / sqrt(<f,Cf>)
       <= R sqrt(2/kappa)+2R/sqrt(lambda s)+(N+R)/sqrt(gamma).

Taking the supremum and squaring by the three-term inequality yields

    <r,C^{-1}r>
       <= 6R^2/kappa +12R^2/(lambda s)+6(N^2+R^2)/gamma.

For t>=n>=4, s>=1/2, lambda>=nu/t^2 and gamma>=3nu/n^2. Substitution, followed by t>=n, gives

    <r,C^{-1}r>
       <= (21/8)n^6 D_n^2/nu +(3/8)n^4 D_n^2/kappa.

The all-closed configuration belongs to S. Before its first microscopic flip, reaction is impossible. Its equilibrium mass is at least 1/6, and its mean first-flip wait is (t^2+1)/(n nu). Thus L=<1,v> >=t^2/(6n nu). Division proves (5).

The complexity claim concerns rational model inputs: exact solution of the O(n^2)-dimensional truncated system and exact O(n^3)-neighborhood contractions have polynomial bit complexity in n and input bit length, including log t. No factor proportional to the physical wait t^2 is needed. The implemented float proposal is not claimed to remain well conditioned at arbitrarily large t; it can be replaced by exact or sufficiently high precision linear algebra. Actual final certificates remain independently checked.

Equation (5) is internally derived mathematical progress; its historical novelty and relevance beyond this integrable physical family are not established.

## 7. Executed parameter sweeps and decisions

Authoritative results are in experiments.json and the acquired_*.json witness/transcript files. Times below include exact synthetic energy interrogation, inference, representation construction, sparse solve and rational certification. They are single-run container timings, not a controlled hardware comparison or a measure of total research effort.

### Rarity, at fixed n=16 and nu=kappa=1

| t | Exact lower (rounded here) | Exact upper (rounded here) | Upper/lower ratio |
|---|---:|---:|---:|
| 10 | 8.17858 | 192.99099 | 23.5971 |
| 100 | 1657.21038 | 3656.55214 | 2.20645 |
| 1000 | 167978.69997 | 170071.72640 | 1.01246008 |
| 10000 | 16800167.39206 | 16802261.38832 | 1.00012465 |

The first two rows fail a ten-percent target. The method becomes more useful in the genuine rare, cooperative-trap regime; it is not uniformly successful.

### Dimension, at fixed t=1000 and nu=kappa=1

| n | Full states | Trial states | Residual neighborhood | Ratio | End-to-end seconds |
|---|---:|---:|---:|---:|---:|
| 8 | 256 | 58 | 194 | 1.00043491 | 0.0259 |
| 16 | 65536 | 242 | 2562 | 1.01246008 | 0.5271 |
| 24 | 16777216 | 554 | 10178 | 1.08263755 | 1.6710 |
| 32 | 4294967296 | 994 | 26114 | 1.31419071 | 5.3835 |

The n=32 row fails the ten-percent criterion. Strong dimension growth still harms closure quality. There is no favorable-rank premise.

### Independent microscopic kinetic clocks, at n=16,t=1000

(nu,kappa)=(0.1,1) gives [1404897.32749,1418560.41941], ratio1.00973.
(10,1) gives [26040.75643,26684.41387], ratio1.02472.
(1,0.1) gives [260407.56433,266844.13862], ratio1.02472.
(1,10) gives [140489.73274,141856.04195], ratio1.00973.
These are changed physical model coefficients, not experimental clock estimates.

### Different preparations

For binary killing k=kappa 1_A, stationarity gives <1_A,K^-1 1>=1/kappa. Hence

    tau_{pi|A}=1/[kappa pi(A)],
    tau_{pi|A^c}=[tau_eq-1/kappa]/[1-pi(A)].

Here pi(A)=1/2. Thus the open-conditioned mean is exactly 2/kappa, while the closed-conditioned mean at n=24,t=1000 lies in [289754.54605,313699.31479]. Mixtures of these two defined preparations are immediate.

A separate two-load computation treated the point preparation with every bit closed, NOT an equilibrium ensemble. With b2=1_{all-closed}/pi(all-closed), the inherited matrix residual bound was applied to loads 1 and b2. The certified point-prepared mean is

    [289799.3453074289,313745.3363051287].

The cross-error enclosure uses E<=Gamma and E>=0:

    E12 in [(Gamma12-sqrt(Gamma11 Gamma22))/2,
            (Gamma12+sqrt(Gamma11 Gamma22))/2].

The square root was rounded outward rationally. This is a represented point preparation, not a solution for arbitrary experimentally prepared ensembles.

## 8. Coupled mass, mobility and reaction uncertainty

For heat-bath conductance, c_ij=nu m_i m_j/(m_i+m_j). If a common energy perturbation implies, after an irrelevant scalar mass shift, m0<=m<=R m0, and microscopic clocks lie between factors a and b of reference clocks, then

    a A0 <= A <= b R A0,
    tau0/(b R^2) <= tau <= R^2 tau0/a.                 (6)

This follows from operator order, inverse positivity, the common mass source, and its normalization. It is not a comparison of unrelated source and rate parameters. In the present uniform family, errors |delta log t|<=eJ and |delta field|<=eh give log R<=n(eJ+eh).

If each queried dimensionless energy has absolute error at most delta, four-energy contrasts give eJ<=2delta, and the recovered uniform field has eh<=6delta, assuming the separated edge/nonedge classifications and declared model class. This is an analytic error-propagation result. The executed graph-reconstruction prototype uses exact weights; a general noisy graph-fitting backend was not implemented.

For delta=10^-5 and independent nu/kappa relative uncertainty0.002, the n=24,t=1000 interval becomes

    A: [144034.9373754090,157769.6611491243].

A second acquired model at t=1200 gives

    exact-input B: [208653.7035252942,220631.5241090090],
    same uncertainty B: [207439.1314356965,221924.2263705704].

Consequently B/A >1.31482 for the specified equilibrium-conditioned means. This is a genuine distinguishable model decision in a dominant-trap regime, not a claim about ligand performance.

The exponential factors in these robustness calculations are enclosed by rational Taylor sums with explicit remainder bounds. Clock intervals are assumed physical model information, not experimentally acquired in this run.

Field-mass uncertainty was varied independently at fixed coupling and clocks. For uniform-field error0,10^-5,10^-4,10^-3,10^-2, the resulting ratios are1.08264,1.08368,1.09308,1.19172,2.82752. Thus large unresolved mass uncertainty still defeats precision. Clock uncertainty0,0.002,0.01,0.05 gives ratios1.08264,1.08698,1.10451,1.19660. These failed precision cases remain in experiments.json.

## 9. Competitors and significance

### Implemented competitors

An attractive-coupling local-window solver was given the same recovered ring law and exact initial window marginal. Freezing both exterior boundary spins open yields a valid lower mean; freezing them closed yields a valid upper mean. The comparison uses the actual equilibrium marginal, not an artificial window equilibrium. Ferromagnetic heat-bath attractiveness and the increasing reaction hazard justify pathwise ordering.

At n=24,t=1000, window sizes3,5,7,9,11 give upper/lower ratios approximately185172,72437,38330,23514,15756. The 11-bit window uses2048 states and about2.16seconds for two solves and exact residual checks, but cannot reach the ten-percent target. This shows why a local boundary envelope is inadequate for this collective gate; it does not prove that all improved window methods fail.

Full sparse reference solves at n=6,8,10,12 agree with the intervals. At n=6 and8 the full solver is as fast or faster. At n=12 a full solve plus exact checking took about11seconds in the final replay, versus about0.081seconds for the candidate, but the full result has far tighter accuracy. This is NOT a matched-accuracy superiority claim.

The low-defect proposal itself is an energy-based finite-state projection and a domain-wall computation. An expert specialized solver can exploit the same structure. The added contribution is a source-complete error certificate, not the assertion that existing solvers must enumerate all states or wait in real time.

### Prior art and unexecuted comparisons

Exit-time finite-state projection explicitly addresses first-passage distributions and occupation measures; it is close prior art, not a method to ignore. Gauss/Radau inverse forms, low-energy truncation, Glauber correlations and matrix residual certification are established. Tensor/QTT master-equation methods and tensor rare-trajectory methods already avoid exponential state arrays.

Optimized weighted ensemble uses local first-passage information to allocate trajectories. TAMMBER combines atomistic exploration with missing-transition uncertainty. Descriptor-free AIMMD learns committors/path information for demanding ligand kinetics. No optimized-WE, TAMMBER, AIMMD or strong tensor implementation was run against this prototype. No global superiority over them is claimed. Their training/acquisition costs should be charged, but so must this method's structural assumptions, energy interrogations and exact certification.

## 10. Audits, costs, and limitations

The final audit executed6818 assertions, including exact detailed balance, exact magnetization action, exact small-matrix positive-semidefinite checks, exact Woodbury identities, parameter/graph recovery, full sparse comparisons and eight exact witness replays. The n=6 complementary PSD check is numerical; n=4/5 PSD checks are rational. Some assertion counts correspond to entries of an exact matrix identity rather than independent mathematical claims. The four small sparse references have exact rational residual enclosures, but containment was checked as interval overlap rather than pretending the floating reference was the exact real answer. None of this is external review or formal proof.

Candidate arithmetic uses polynomial-size defect sectors and their neighborhoods. Static moments and partition functions are evaluated by exact low-dimensional algebra for this interaction family, not assumed affordable high-dimensional integration. At general graph treewidth, frustrated couplings or higher-order interactions, that operation can become expensive.

The recorded times exclude research, literature review, failed pilots and software development. Several exploratory versions and one timed-out invocation preceded the final implementation. The full experiment sweep took about16.6seconds of runtime; the separate final audit about18.8seconds. These are not the total resources spent on this research. No physical energy-use advantage was measured.

The unknown graph is learned, but the global pairwise form and heat-bath clock law are assumptions. A hidden higher-order well at an unqueried configuration, or a configuration-dependent kinetic prefactor, can preserve the energy transcript while violating the certificate premises. Such a system must not be declared certified.

The successful slow-space construction uses an exact invariant inherited from a symmetric one-dimensional model. Extending it to generic coupled molecular gates requires a constructive global complement bound or another source-aware replacement when the slow observables are not algebraically closed. Merely fitting a few slow modes does not provide that guarantee.

## 11. Retained scientific objective

This run does not solve general molecular gate acquisition. It does show that the decisive coupled information can, in a nontrivial dominant-trap family, be derived from obtainable local energy interrogations plus an explicit microscopic dynamical law: source weights, rare nucleation rates, a collective slow mode, and a relaxation bound for every omitted mode are derived together.

The substantive next obstruction is a nonsymmetric, nonintegrable gate in which the acquired local law does not close a two-dimensional slow space. The operation must then either construct a controlled approximate slow space with a global complement certificate, or replace spectral closure altogether. Adding more coordinates to the present symmetric ring is not that next objective.
