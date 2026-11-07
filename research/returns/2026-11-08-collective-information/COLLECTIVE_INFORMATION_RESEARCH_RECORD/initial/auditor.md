# Independent hostile-auditor initial return

Researcher 3; frozen independently on 7 November 2026. No peer/principal research notes were consulted. This is a research record, not a publication or priority claim. Supporting primary sources are in ../auditor/source/.

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

## 7. Primary literature and status check

The primary caches and SHA256 manifests are in ../auditor/source/. No external theorem is load-bearing for the self-contained proofs above.

- Lin–Tian–Anghel–Livescu, https://arxiv.org/html/2101.05873v3 , section 5, equations (48)–(51), Algorithms 1–2: genuine data-driven MZ/Koopman predecessor. The primary text restricts its analysis to noiseless deterministic observations; it differentiates correlations and inverts C(0). Finite noisy conditioning, controlled projection changes and full costs are additional work.
- Zhu, https://arxiv.org/html/2109.01990v2 , Theorem 1, Proposition 2, Corollaries 1.1–1.2: finite-rank symmetric projection, DMS/GS H1–H4 and domain D, diffusion factorization and a specific Hilbert space. Exponential orthogonal decay holds on QH intersect ker(K)-orthogonal with operator-dependent constants. This is not automatically a size/control-uniform operational norm bound or acquired kernel/initial-force law.
- Zimmerman et al., https://arxiv.org/html/2406.03606v1 , section III.5: strong actual numerical comparator, with steady-state local neural-force training, larger boxes and time-dependent tests. The primary explicitly calls nonstationary reuse approximate because steady and transient memory differ, and attributes observed deviations to this. Do not misclassify the empirical transfer as a uniform theorem.
- Schmidt, https://arxiv.org/html/2607.19255v1 , equations (37)–(42): formally exact universal entropy-superpower functional and current derivatives. Constructible finite-data functional evaluation, controlled memory truncation and complexity do not follow from formal universality.
- Yang et al., https://arxiv.org/html/2610.40117v1 , II.3, III.1–III.2, VII: rapid microscopic relaxation is an explicit hypothesis; equations (27)–(29) quantify leading thermal lag with cross-coupled currents. Constrained microscopic solves and kinetic coefficients remain real costs.
- Han–Zhao–Li, https://arxiv.org/html/2609.37392v1 : reconstruction-free latent learning with microscopic initial-state access and local convergence results, rather than general noisy macro-only acquisition. **Current source status:** https://arxiv.org/abs/2609.37392v2 is withdrawn, dated 2 October 2026. The stated reason concerns timing of public dissemination of results based on a dataset; that is not evidence its mathematics is false. Cite v1 with current status, not silently as an unqualified current published theorem.
- Tian–Kannan, Stochastic Analysis and Applications 24 (2006), 685–702, primary https://people.nmsu.edu/jtian/publications/2006-3.pdf , doi:10.1080/07362990600632045, Definition 2.9 and Theorems 2.10–2.11: generator block-sum criterion and generator/semigroup lumpability equivalence. Theorem 2.3 recalls Kemeny–Snell. This is the exact established mechanism in E1; the proof via powers verifies it. Uniformly applying it to controls is routine.
- Zenodo https://zenodo.org/records/20410346 , primary four-page PDF inspected. Theorem 1(ii) is conditional on strong orthogonal-semigroup decay and bounded RL. The full controlled QL decay/rescaling is not derived merely from a fast-fiber spectral gap; there is no finite noisy acquisition. Prose reverses an exponential inequality for t<=epsilon/alpha, although the weaker local upper bound by one still follows. Do not import as a free uniform closure theorem.
- Zenodo https://zenodo.org/records/22722557 : public metadata read, full PDF download initially incomplete and then access errors; title Mori–Zwanzig Perspective on Neural Representation Dynamics: Coarse-Graining via Short-Memory Closure. No theorem imported from metadata. Full-file check pending at freeze.
- Zenodo https://zenodo.org/records/23587917 , primary seven-page PDF inspected. Cross-scale information, subgrid regularization and infinite-horizon predictability enter as named axioms. Theorem 4.3 invokes an external harmonic-brake global-smoothness assertion plus coercive damping; Theorem 4.4 introduces hyperbolicity/gap beyond a positive Lyapunov exponent; Theorem 4.2 does not prove the dynamic intertwining needed to infer transport from information loss/fiber symmetry. Sections 1–2 give direct counterexamples to that inference. Its script evaluates assigned formulas, not universal physics. No general law imported.

The earlier local reusable-intervention dossier was inspected at its exact scope (sparse thermal relative updates and acquired launch-response interfaces). No result from it is used to infer general macro closure. Historical novelty remains UNKNOWN; practical advantage is NOT ESTABLISHED.

## 8. Decisive constructive challenge

The strongest useful positive route must derive, for a specified physical class: (i) a tractably discoverable controlled sufficient field/history, (ii) noise-compatible acquisition of drift, memory and fluctuation law with conditional initial preparations, (iii) size/horizon/control-uniform stability in the chosen macro metric, and (iv) an evaluator whose preprocessing/storage do not conceal microscopic trajectories, conditional Gibbs solves or rare clocks. An especially strong attack is physical Wasserstein contraction for empirical fields plus local kinetic acquisition, avoiding unnecessary full-TV/parity resolution. Another is retaining actual kinetic cross fields and proving the remaining controlled memory small. Baseline equilibrium closure, entropy, passive kernel decay and fitted low rank do not close these operations.
