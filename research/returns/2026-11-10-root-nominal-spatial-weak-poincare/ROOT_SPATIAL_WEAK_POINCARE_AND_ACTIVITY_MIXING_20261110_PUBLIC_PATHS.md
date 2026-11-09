ROOT: VARIABLE-GRAPH NOMINAL MIXING FROM A WEAK POINCARE COMPARISON
10 November2026 Brisbane. Complete construction conditional only on the accepted fixed-R nominal catalytic theorem. This extends a proved conservative spatial interface; it does not reopen that accepted theorem or prove independent-error robustness.

PRIOR CAPITAL AND CORRECTION. Pinned Astra main09698fe177238ebdb9cb9208767aa49c8373fb39, N1782 content_version d7f3b1511525c6d438ec5175c18dfae85b9c7a94feae31f70c2713863bf46022 already supplies the exact spatial class/multinomial disintegration, conditional diffusion Poincare, reaction-source/target Palm comparison and a FULL original-clock spatial Poincare theorem for conservative fixed complex-balanced local chemistry at bounded density. Its equilibrium sampler is polynomial COMPLETE-BINARY, using accepted DDB1 binomial draws, not a numeric-particle loop. ROOT read its WHOLE governing proof:
 research/returns/2026-11-09-root-spatial-reaction-diffusion/ROOT_SPATIAL_REACTION_DIFFUSION_THEOREM_AND_ENDPOINT_INTERFACES_PUBLIC_PATHS.md8297UTF8/SHA219959e4e92cbb832f19a1708a613df41951cb2ad9a27639210965a62bb0bf45.
The static/fibre components rederived in ROOT_SPATIAL_POISSON_FIBRES_AND_PROJECTION_20261110.txt7692/132a9fd6 therefore overlap existing capital and are NOT additional discoveries. The genuinely unclosed comparison there concerns general NONCONSERVATIVE infinite classes, where the coarse exit rate has no finite conserved-mass bound. Here that unbounded term is paid through a weak Poincare defect and exponential stationary tails.

THEOREM. Fix any finite weakly reversible reaction structure R on d species, including nonconservative networks and zero complexes. On ANY variable finite connected undirected simple graph G with n vertices, put R at each site and independent species hops at rate1 along each oriented edge. There is a fixed finite degreeK depending ONLY on globalR and a polynomial-BIT nominal local catalytic rate compiler such that:
(i) only fixed-degree translated copies of original local reactions are added; the spatial directed state graph stays EXACTLY unchanged;
(ii) on every actual finite/infinite spatial class, the minimal process is nonexplosive and has exactly product-Poisson site activitieslambda/n conditioned on that class;
(iii) for every binary initial configurationx0, rationalactivitieslambda>0 and rational0<epsilon<1/8, a rational timeT is compiled with ENTIRE endpointTV and every absolute first-moment error to that nominal stationary law<=epsilon;
(iv) T, inverse rate constants and expected TOTAL ACTUAL channel firings byT are polynomial in
 W=2+n+|x0|1+sum_i(lambda_i+lambda_i^-1)+epsilon^-1,
with explicit computable fixed-R constants/exponents. Compiler work/memory/output are polynomial in complete BINARY input length, including graph/configuration/output descriptions.
No population-uniform L2 gap for the full spatial process or coefficient-error robustness is asserted. Physical time/firings are polynomial NUMERICALW, not polynomial in logpopulation.

1. RATE/SUPPORT/LAW INTERFACE.
Take the accepted global fixed-R catalytic degreeK and circulationa_r. Put D=max_r|y_r|, L=max(1,D+K), V=1+sum_i(lambda_i+lambda_i^-1),
 c0=[(1+sum_r a_r)*V^D]^-1, c=c0*n^(-(D+K)).
At each site choose
 kappa_(r,w)=c*a_r*n^(|y_r+w|-1)/(w!*lambda^y_r), |w|<=K.
All rates are positive rational<=1, with fixed-R polynomial inverse bounds in n,V. At theta=lambda/n their complex flux is c*a_r*lambda^w/(n*w!), so translated local cycles balance. Hops balance homogeneously. Gather/redistribute arguments identify the ACTUAL spatial class as every placement with aggregate N in Gamma_R(N0), N0=totalsx0.
Summing factorial weights gives aggregatepi_bar(N)=Z^-1 lambda^N/N!, and conditionalmu_N the product of uniform multinomial site allocations. No lattice replacement or transient lumpability is assumed.
Factorial moments give EXACT stationary averaged global catalytic rates
 qbar_r(N)=c*a_r*lambda^(-y_r)*(N)_y_r*F_K(|N-y_r|).
This is n^(-(D+K)) times the accepted global nominal clock. Thus a computable G0=C_R*n^(D+K)*V^p_R bounds its reciprocal Poincare gap. Pick a fixed integer Q0>=1+sum_(r,w)a_r. Total averaged activity satisfies qbar(N)<=Q0(1+|N|1)^L. Self-events may be retained in this upper bound and in firing costs.

2. COMPLETE WEIGHTED COMPARISON, INCLUDING ZERO COMPLEXES.
Let H=E_pi_bar Var_muN f, F(N)=E_muN f, and let E_reac,E_diff,E_bar be the spatial-reaction, spatial-diffusion and averaged-global stationary Dirichlet forms (factor1/2 convention). Independent-particle tensorization gives H<=n^2 E_diff, uniformly in ALL counts; n=1 hasH=0.
For a local channel with sourcearitya,targetarityb, its normalized source-edge marginal relative to mu_N is n^(a-1)*sum_v(x_v)_y/(N)_y whena>=1, bounded byn^(a-1). Whena=0 the density is1. The target marginal has the analogous boundn^(b-1) forb>=1 and1 forb=0, by the exact remove-reactants/add-products Palm construction. Thus all bounds are <=h=n^(L-1). Products have arity<=D+K by weak reversibility.
If densityg<=h, its mean bias squared is <=(h-1)Var_mu f by Cauchy-Schwarz. Split F(N)-F(M) into source bias, the actual edge difference, and target bias. Sum the three-square inequality against stationary coarse edge flux. Stationary incoming flux equals outgoing flux even without detailed balance. The N1782 calculation therefore gives, WITHOUT a conserved-mass bound,
 E_bar(F)<=3E_reac+3h E_pi_bar[qbar(N) Var_muN f].
With the global accepted gap and total variance,
 Var_pi f<=H+3G0 E_reac+3G0*h E_pi_bar[qbar(N) Var_muN f].
For an integer cutoffB>=0 split only this PROOF sum into |N|<=B and its complement. No chemical state truncation or reflection is introduced. Since conditional variance<=osc(f)^2,
 Var_pi f<=a(B)(E_reac+E_diff)+b(B)*osc(f)^2,
 a(B)=max(3G0,n^2[1+3G0*h*Q0*(1+B)^L]),
 b(B)=3G0*h*Q0 E_pi_bar[(1+|N|)^L 1_(|N|>B)].
This is a complete weak Poincare inequality; the unbounded activity was not silently replaced by a uniform maximum.

3. PAY TAILS AND THE INITIAL ATOM, WITHOUT EXPONENTIAL-SIZE BINARY OUTPUT.
Write S0=|x0|1. The accepted anchor bound, or the unconditioned Poisson generating function directly, gives
 Pr_pi_bar(|N|>s)<=min(1,exp(D0-s)), D0=4V(1+S0)^2.
Indeed Z>=lambda^N0/N0!>=exp[-S0(V+S0)] and sum_N e^|N|lambda^N/N!=exp(e sumlambda), e<3.
For the fixed L take C_L=16*(4L+4)^(L+1). Summing the exponential tail gives
 E_pi_bar[(1+|N|)^L 1_(|N|>B)]<=C_L exp(D0-B/2).
The full initial spatial atom obeys pi(x0)>=exp(-A0), with A0=4(n+V)(1+S0)^2: Z<=exp(sumlambda) and logarithms of n,activities and factorials are bounded by n,V,S0. These bounds include arbitrarily rare actual classes.
For desired endpointTV eta in(0,1/8), put
 R0=1+3G0*h*Q0*C_L,
 B=ceil[4(D0+A0+R0+eta^-1+10)],
 T=ceil[a(B)(A0+eta^-1+10)].
All these expressions use fixed powers/rational arithmetic on binary inputs. The quantities exp(-A0) and exp(-B) occur ONLY in the proof; no enormous denominator2^A0 is constructed or output. The choices imply
 b(B)<=eta^2 exp(-A0)/64, exp(-2T/a(B))<=eta^2 exp(-A0)/64.

4. NONREVERSIBLE SEMIGROUP AND ENTIRE-TV BOUND.
Formal stationarity is genuine: pi has all polynomial moments, total spatial intensity has fixed polynomial growth, so sum_x pi(x)q(x)<infinity. The accepted invariant-jump-chain/positive mean holding-time argument establishes nonexplosion from every actual state. Irreducibility then gives the unique stationary law. This is valid for each finite variable graph; no unproved physical-time gap is needed.
For0<=f<=1 let v(t)=Var_pi(P_t f). Stationarity gives v'=-2E(P_t f,P_t f), and osc(P_t f)<=1. The preceding inequality yields
 v(t)<=exp[-2t/a(B)]v(0)+b(B).
The single initial-atom inequality gives
 |P_T f(x0)-pi f|<=pi(x0)^(-1/2)*sqrt(v(T))<eta.
Taking the supremum over ALL suchf proves ENTIRE lawTV<=eta. Form approximation/localization justifies the stationary identity; pi q integrability pays it for bounded semigroup tests. No reversibility, finite cutoff dynamics or pointwise bound on the rates was used.

5. AUTOMATIC NOMINAL MOMENTS AND ALL ACTUAL FIRINGS.
For ANY stationary Markov kernel with invariantpi,
 P_t(x0,A)<=pi(A)/pi(x0),
because pi(A)=sum_x pi(x)P_t(x,A) contains that nonnegative initial-state contribution. Thus here, uniformly for ALLt>=0,
 Pr_x0(|N_t|>s)<=min(1,exp(D0+A0-s)).
Integrating gives E_x0(1+|N_t|)^m<=C_m(1+D0+A0)^m for every fixedm, with C_m=1+3*m!: split the tail integral atH=D0+A0, expand(1+H+u)^(m-1), and sum the integer factorial integrals againstexp(-u). Stationary moments have the same kind of bound. This avoids the exponentially poor multiplicative moment bound pi(x0)^-1/2: the exponential factor shifts an exponential TAIL threshold instead.
Spatial reaction rates<=1 and fixed local degree imply
 q_sp(x)<=(Q_R+1)n(1+|N|)^L,
whereQ_R is the fixed number of local catalytic channels; diffusion contributes at mostn|N| on a simple graph. Hence expected TOTAL ACTUAL firings byT are <=T*(Q_R+1)n*C_L'(1+D0+A0)^L, a polynomialNUMERICALW bound.
Choose the explicit rational polynomial M2=8*(1+D0+A0)^2, which majorizes both transient and stationary second moments. Run3-4 with eta=epsilon^2/[64(1+M2)] (decrease to1/16 if needed). A maximal coupling and Cauchy-Schwarz give each ABSOLUTE first-moment error<=2sqrt(M2*eta)<epsilon as well asTV<=epsilon. Both error requirements are paid separately. The compiler's finite rational operations remain polynomial COMPLETE-BINARY, including all fixed-R tables/constants and explicit graph/local-rate output. No actual physical experiment or simulation is needed to state this construction.

6. INTERFACE TO ROBUSTNESS AND EXISTING RESULTS.
The stationary-domination tail lemma is more general than this spatial theorem. For the fixed-R nominal catalytic process it automatically supplies polynomial transient moments from any deterministic initial state. Starting nominal dynamics from a law with sufficiently high polynomial moments also works: A0(x) is polynomial in |x|, so integrate the resulting polynomial bound. In D123's conditional robust transfer this pays nominal evolutions from perturbed stationarity once sufficiently high perturbed stationary moments are truly available. It does NOT prove perturbed recurrence/moments, because perturbed rates do not preservepi.
N1782's conservative FULL physical-gap/equilibrium positives stay accepted, not downgraded to this weaker mixing statement. Its arbitrary-volume/all-binary-time nonlinear transient sampler remains a DIFFERENT open endpoint; a polynomial NUMERICAL physical mixing time is not a binary-time fast-forwarder. The present nonconservative nominal theorem and its automatic-moment lemma do not close current P3's independent-coefficient-error assertion. No novelty, impact rating or practical-device claim is made. All original source/access/transfer/resource holds remain.
