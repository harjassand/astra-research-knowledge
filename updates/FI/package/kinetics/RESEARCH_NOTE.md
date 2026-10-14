# ASTRA FRONTIER — Reverse-relaxation acquisition and source-complete kinetic references

Research checkpoint: 14 October 2026.

## Status and strongest result

The retained objective is reliable long-timescale molecular residence/reaction prediction with unknown conformational gating. This continuation removes the previous requirement for an analytically closed homogeneous Glauber slow space. It does not establish a fundamentally new general molecular algorithm or a state-of-the-art performance advantage.

The executed operation acquires an energy law and a separate, initially unknown kinetic interaction law; constructs a globally comparable local reference dynamics; solves the recoupled response in a compressed representation; and verifies the complete mass source and residual with rational arithmetic. It does not identify a global committor or assume known slow eigenfunctions. Its strongest acquisition result distinguishes equal-energy models with identical all-zero-context clock readings whose equilibrium-conditioned means differ by more than 54.68%.

The final physical-information interface is **reverse relaxation under the original potential**, rather than the earlier exploratory energy-balancing intervention. The learner prepares the locally unfavorable state and interrogates its downhill elementary relaxation rate. The construction requires an explicit reversible two-state microscopic law and the ability to prepare/hold a context without changing its conditional clock. No physical experiment was performed. The executed observations are exact evaluations of an authored microscopic generator, not estimates of metastable escape rates.

At 18 binary coordinates, the final model contains heterogeneous couplings, fields, microscopic clocks, a frustrated local bond and chorded interaction graphs. Exact local algebra demonstrates that the single-spin observable space is not invariant. It is an authored modular diagnostic, not an independently selected molecule. The reference exploits modularity discovered from the acquired graph, so the construction does not solve strongly nonmodular molecular gates.

Two canonical results (model time units):

* A: [148838921.68597248, 148841714.37773330], displayed to floating precision; exact rational endpoints are in reverse_A.json.
* B, same equilibrium energies but different context-dependent mobility: [230236128.12863976, 230236140.68770093], exact rational endpoints in reverse_B.json.
* The exact ratio B_lower/A_upper is greater than 1.54685216.

Both laws can be recovered from 172 energy queries and 2772 fast reverse-clock interrogations, without supplied kinetic context supports. Full source coverage involves 262144 configurations, but the candidate constructs only three 64-state local models and compressed global response arrays. It does not construct a global conformation list. This is local state enumeration, not zero enumeration anywhere.

At a matched upper/lower ratio goal of 1.05, the full-state preconditioned solver is faster: approximately 3.26 s versus 6.58 s for the compressed candidate in the final single-run comparison. The benefit established here is model-conditional information recovery and reduced represented storage, not a runtime or energy advantage.

Close prior art is substantial. Masetti and Robol (2019) already split weakly interconnected components and use tensors for mean absorption times. Tensor generator learning, preconditioning, Boolean coefficient recovery, detailed-balance reversal and functional residual certificates are not inventions claimed here. Historical novelty of the particular acquisition/comparison/certification combination remains unresolved.

## 1. Exact obstruction: finite perfect regularized responses can miss arbitrarily slow mass

Let a reversible killed mixture have rates lambda_j>0 and source weights p_j>0, sum p_j=1. Its regularized response is

    F(s) = sum_j p_j/(lambda_j+s),    s>0,

and its mean lifetime is F(0). This is a positive Stieltjes response. The transient components can be completed to an irreducible reversible star network by adding reverse transitions from the target before killing; no unknown waiting-time estimate is embedded in the example.

Take baseline rates 1,2,3,4, each with mass 1/4. The three exact observations at s=1,2,4 are

    F(1)=77/240, F(2)=19/80, F(4)=533/3360.

The baseline mean is 25/48. Add mass delta=1/1000 at a new rate epsilon. Adjust the four old weights to preserve normalization and all three observations. This is a 4-by-4 Cauchy-system solve, executed exactly. Every adjusted weight remains positive in the tested examples.

    epsilon       mean, approximately
    10^-2         0.6170719333
    10^-4         10.5170007291
    10^-8         100000.5170000001
    10^-12        1000000000.517

All three observations remain exactly unchanged, not just within noise. Generalization to any fixed finite collection of distinct positive shifts follows from invertibility of the Cauchy-plus-normalization matrix: its correction coefficients stay bounded as epsilon tends to zero, so a sufficiently small fixed delta preserves positivity while delta/epsilon diverges.

This does not prove impossibility within a fully identified finite-dimensional physical class. It says that finite regularized observations, even exact ones, do not alone provide global information about source-visible near-zero rates. The missing information must exclude such completions, for example through a verified structural generator law or a source-weighted tail restriction. This is classical moment/resolvent structure applied to the acquisition obstruction; no priority claim is made.

## 2. Mechanisms investigated

1. Fitting or measuring a few slow response modes cannot certify that an additional slow component is absent. Section 1 gives an exact rather than noise-based obstruction.
2. Pinning-coordinate/conditional-mixing methods could provide a lower bound on the complement of functions of pinned coordinates. A noninvariant Galerkin calculation would then give a Schur correction. But finding a small pinning set with a global conditional bound and acquiring the required conditional integrals were not solved or tested end-to-end in this run. No performance result is attributed to that route.
3. The successful route constructs a **reference generator retaining every local mode**, rather than selecting a presumed set of global slow modes. The actual coupled operator is bounded on both sides by this reference. A response is then discovered iteratively and its complete residual checked independently.

The iterative solver is conventional preconditioned linear algebra in tensor form, not a new CG method. The research question addressed is whether the necessary reference and source comparison can be acquired without exact homogeneous closure. The answer is positive for the declared modular microscopic class below, negative for the strongly nonmodular diagnostic in Section 10.

## 3. Physical model and allowed information

Let x in {0,1}^n denote elementary coordinates. The globally declared energy class is

    W(x) = product_i h_i^(x_i) product_(i,j) t_ij^[x_i=x_j].

Neither the graph nor coefficients are initially given to the learner. The physical target is a local reaction with hazard k(x)=kappa x_0. The target location and kappa are specified inputs, not discovered pathways.

The microscopic single-bit flip law is

    q_i(x) = a_i(x_-i) W(x^i)/(W(x)+W(x^i)),

where a_i is independent of the flipped bit. This gives detailed balance. The unknown prefactor law is assumed globally to be a positive multilinear Boolean polynomial of degree at most two in the other coordinates. Its support need not coincide with the energy graph and is not supplied. Positivity can be checked after recovery by enumerating the small recovered local support; the prototype rejects supports above ten bits.

These are structural premises, not consequences of finite observations. A cubic prefactor perturbation supported on three excited context bits is invisible to the degree-two acquisition queries. An unknown higher-order energy term can similarly preserve all pairwise probes. No certificate is claimed outside the declared class.

The tested model is not a general inertial or overdamped molecular force field. Its elementary local heat-bath law is an explicit microscopic model, not an expensive basin-to-basin rate oracle. Interpreting q_i as a metastable transition estimate would invalidate the resource accounting.

### 3.1 Energy acquisition

Query W(0), W(e_i), and W(e_i+e_j). Then

    t_ij^2 = W(e_i+e_j) W(0)/(W(e_i) W(e_j)),
    h_i = W(e_i)/W(0) product_(j incident i) t_ij.

The complete pairwise energy is thereby recovered with 1+n+binom(n,2) observations: 172 at n=18. The exact synthetic weights are rational and the pair factors have rational square roots. A general noisy/irrational coefficient fitter is not implemented.

Each energy query evaluates all terms in the explicit synthetic law; the computation is charged. No equilibrium samples or partition function are input. Small local partition sums and the complete global normalizer are computed later.

### 3.2 Reverse-relaxation acquisition without a biased clock assumption

At a fixed context y, write r=W(1,y)/W(0,y). The rates are

    q_01=a r/(1+r),    q_10=a/(1+r).

Prepare the less probable local state and read the downhill original-law rate d. Then

    d = a max(1,r)/(1+r),
    a = d (1+r)/max(1,r),
    a/2 <= d <= a.

This removes thermodynamic suppression from the rate readout; it does not remove intrinsically small mobility a, or the cost of preparing/resetting/clamping a context. No bias is present during the rate interrogation, so invariance of the prefactor under an energy-equalizing bias is no longer needed. The conditional microscopic law after preparation must still be the intended law.

The earlier balanced-clock pilots remain in the packet as exploratory evidence. The final reverse_* transcripts and witnesses supersede them as the main acquisition interface.

### 3.3 Discovering unknown kinetic support

For each i, interrogate all contexts with zero, one or two of the other bits excited. Define acquired attempt values a_i(S), |S|<=2. Möbius differences give

    c_empty = a_i(empty),
    c_j = a_i({j}) - a_i(empty),
    c_jk = a_i({j,k}) - a_i({j}) - a_i({k}) + a_i(empty).

Under the degree-two premise,

    a_i(y)=c_empty+sum_j c_j y_j+sum_(j<k)c_jk y_j y_k

holds for every context, including those never interrogated. Nonzero coefficients identify the kinetic support. At n=18 this costs

    n[1+(n-1)+binom(n-1,2)] = 2772

original-law rate interrogations. This recovers a kinetic interaction graph separate from the equilibrium energy graph.

One tested variant has a dependency from coordinate 1 to the clock at coordinate 0, despite no energy bond (0,1). It is recovered by the same scan and handled by the operator compiler. No global reaction path is specified by this recovery.

The number of measurements is polynomial for this fixed-degree class, but support-table validation can be exponential in the acquired support size. A degree-two polynomial can have dense support. Small useful supports are observed in these fixtures, not guaranteed universally.

## 4. Acquired reference and coupled mass-conductance comparison

Partition the recovered graph into blocks. The implemented search tries thresholds of bond contrast, excludes blocks above six bits and scores admitted candidates by local-solve size, cross-coupling contrast and cross-term count. This is a transparent heuristic, not a globally optimal partition algorithm.

Let rho_b be the exactly computed local equilibrium law obtained by removing cross-block energy terms. Define the normalized product reference

    rho_0(x)=product_b rho_b(x_b).

After an irrelevant scalar rescaling, the true unnormalized mass is

    m(x)=rho_0(x) w(x),    1<=w(x)<=R_m,
    Z=<w,1>_rho0.

For the pairwise model, a conservative R_m is the product of max(t,1/t) over cross-block bonds. This bound is compiled from the acquired law, not supplied as a favorable constant.

A local reference attempt is the minimum of the recovered attempt law over external contexts while retaining its internal dependence. Therefore

    1 <= a_i(x_-i)/a_i^0(x_block\i) <= R_k.

Kinetic dependencies outside the energy graph are included in the actual operator's context projectors. The reference may use an external-context minimum, but the actual dynamics is never replaced by that minimum in the response solve.

Let

    C = sum_b L_b^0 + k

be the local reference killed generator in L2(rho0). The target block contains k; other blocks are conservative. The actual positive weighted operator is

    A = w(-Q+k).

The mean-time field satisfies A u=w, NOT A u=1 when w is nonconstant.

### Theorem: a complete kinetic reference comparison

Under the stated reversible microscopic law,

    C <= A <= R C,    R=R_m R_k.                         (1)

Proof. For a physical edge with reference masses m0_x,m0_y, its actual/reference conductance ratio is

    (a/a0) (m0_x+m0_y) w_x w_y/(m0_x w_x+m0_y w_y).

The second factor is a weighted harmonic mean of w_x and w_y and lies in [1,R_m]. The reaction conductance also lies between its reference value and R_m times it. Sum the edge and reaction quadratic forms. This includes every microscopic configuration and transition in the declared law.

This is a direct form-comparison theorem based on standard conductance monotonicity. Historical novelty is not claimed for the inequality by itself. Its useful feature is that the mass source, dynamics and comparison constant are all derived from one recovered physical law.

### Barrier-independent ideal conditioning, not unconditional algorithmic complexity

The spectrum of C^(-1/2) A C^(-1/2) lies in [1,R]. Exact preconditioned Richardson with step 2/(1+R) therefore contracts in C norm by (R-1)/(R+1). This factor does not contain the smallest local kinetic eigenvalue. Increasing an internal barrier can make the physical lifetime enormous without changing R.

The statement is for exact inverse actions and exact iteration. It does not guarantee low tensor rank, cheap C inverse application, finite-precision stability or convergence of rounded CG. The implemented method uses approximate tensor solves, and its output is accepted only by the independent certificate below. A standard preconditioned-CG refinement outperformed Richardson and repaired several initial failures.

## 5. Source-complete certificate without a global slow eigenspace

For an arbitrary trial v, define

    r=w-A v,
    L=2<w,v>_rho0 - <v,A v>_rho0.

The exact residual identity gives

    <w,A^-1 w> = L + <r,A^-1 r>.

If C>=alpha I>0, equation (1) gives

    L/Z <= tau_eq <= [L+||r||_rho0^2/alpha]/Z.           (2)

No approximate slow-space closure or omitted-mode model is needed. The full residual, including source on every unvisited configuration, is contracted exactly.

### Obtaining alpha locally rather than assuming a global gap

Solve the reference target-block equation C_t u=1 numerically. Round u to dyadic rationals and verify u>0 and

    ||C_t u-1||_infinity <= delta <1

using exact arithmetic. Inverse positivity implies C_t^-1 1<=u/(1-delta), and hence

    alpha=(1-delta)/max(u)

is a valid spectral lower bound for C_t and for the global Kronecker sum C. This is a local 64-state solve in the main fixture. A source-free reaction block would not supply this bound; the present target must be reachable within the reference target block.

### Representation and precision

All local modes are retained in the reference factors. Numerical eigensolves propose inverse actions; no computed eigenvalue is trusted as a final bound. A tensor train represents the response by small arrays, with rank selected and varied experimentally. The global operator is represented as a sum of products of exact local matrices. In the main case there are 16 operator terms and four source terms.

The floating response is converted to an exact physical dyadic witness (42 bits per core). Products with the rational operator and source, energy, residual norm and normalization are then computed by integer/rational contractions. There is no sampled residual, projection of the residual back into a smaller basis, global state vector or ignored probability tail. Approximate inverse/rounding errors therefore enter equation (2) rather than being assumed harmless.

### Prepared sources

For a specified initial law p, define b2=p/rho0. A second response solves A v2 approximately equal to b2. Let B=[w,b2], V=[v1,v2], R=B-AV and

    G0=B*V+V*B-V*AV,    Gamma=R*R/alpha.

Then 0<=B*A^-1B-G0<=Gamma. The off-diagonal uncertainty lies between

    [Gamma12 - sqrt(Gamma11 Gamma22)]/2
    and [Gamma12 + sqrt(Gamma11 Gamma22)]/2.

The square root is rounded outward rationally. This handles the tested all-closed point source; it does not provide arbitrary experimentally prepared distributions for free.

## 6. Heterogeneous test family and actual recovered information

The authored fixture has three six-bit modules before relabeling, but that partition is hidden from acquisition. Each module has a disordered cycle plus chords; internal equality factors are powers 2^(r*j) with j in {2,3,4}. One module has an antiferromagnetic bond 2^(-r). Site fields and clocks vary independently among powers of two. Modules are connected through recovered inter-block energy bonds. All non-target coordinates are permuted with a fixed seed.

The main energy cross-factor is 3/2. Energy-derived threshold search recovers three six-bit blocks, R_m=9/4. Context-dependent clocks in model B slow mixed local contact configurations by a factor of 100 without changing all-zero-context clocks. The unknown-support polynomial scan discovers the supports; they are not passed to it. In the main case those dependencies remain internal to acquired blocks and R_k=1.

An exact degree-three Walsh coefficient of L sigma_0 is nonzero:

    -716315425690944856882208507775 /
      3254325115870155011914264328332.

Its local support is [0,3,6,13,16]. Thus the single-spin observable space is not invariant. The previous homogeneous linear Glauber closure cannot be invoked. No claim is made that the system is beyond all specialized algebra or that it is an independently validated molecular force field.

### Canonical reverse-acquired decision

reverse_A.json and reverse_B.json contain exact rational endpoint strings. Model B has the same equilibrium energies and the same 18 all-zero-context reverse rates as A; it differs only in recovered context-dependent mobility.

    A: 148838921.68597248 .. 148841714.37773330
    B: 230236128.12863976 .. 230236140.68770093
    B_lower/A_upper > 1.54685216.

Both are recovered through the same 172 energy and 2772 reverse-clock queries. Each interrogated downhill rate is between one half and one times the local attempt prefactor; these identities were checked exactly for both transcripts. There are no rare uphill waiting-time samples.

The final B witness stores 8256 tensor coefficients, compared with 262144 entries in one full conformation vector. The local reference uses 192 configurations total. Operator factors, rational integers and intermediate arrays also cost memory; coefficient count is not a peak-memory measurement.

### Kinetic dependency outside the energy graph

The separate unknown_support_cross variant replaces one local clock by a degree-two dependence containing an off-energy-graph coordinate. The same support-agnostic acquisition recovers that dependency. Its exact interval is approximately

    190623514.96005 .. 190624266.44420,

ratio 1.000003943. This variant was acquired through the earlier balanced interface and replayed from its transcript; it is not mislabeled as a separate reverse-acquired physical experiment. The final reverse operation would recover the same prefactor algebra, but that variant's reverse acquisition was not separately run.

## 7. Parameter sweeps, repairs and failures

The following are not all equally successful. All completed outputs are retained.

### Internal rarity at fixed dimension, cross-coupling and clocks

For the baseline heterogeneous 18-bit family, seven Richardson refinements at rank eight gave:

    rarity r=1: [465.1490574,465.1543754], ratio 1.00001143
    r=2: [280943.7774,281011.3245], ratio 1.00024043
    r=3: [148838921.6684,152270396.5958], ratio 1.02305496
    r=4: [76396941583.761,225309369060.052], ratio 2.94919 (failure).

Standard truncated preconditioned CG at rank eight repaired r=4:

    [76396941585.60052,76710049631.86708], ratio 1.00409844.

This repair is credited to the stronger conventional solver, not a new theorem. It also shows why a failed finite iteration budget is not a lower bound on the method's possible performance.

### Cross-coupling, independently at r=2

With rank eight/eight PCG steps, inter-block factors 1.5,1.9,3,6 gave ratios approximately 1.00000511,1.00043818,2.04843,4363.37. Rank sixteen/sixteen iterations repaired the factor-three instance to

    [184607.766439269,184609.007658997], ratio 1.000006724,

taking 16.86 s in the recorded single run. The factor-six run remains unresolved at the tested budget; no general impossibility is inferred.

### Rank, field and clocks

At r=3, the same Richardson recipe gave ratio 1.1397 at rank two, 1.02323 at rank four and 1.02305 at rank twelve. Merely increasing rank did not eliminate iteration error.

Independent field-scale changes and uniform microscopic-clock factors 0.1 and 10 were tested at r=2, all with narrow certificates. Changing mass and changing dynamics are not conflated. Details are in field_*.json and clock_*.json.

### Preparation

For the r=2 baseline, the equilibrium mean is near 280944. A two-load, all-closed point-source computation gives

    [378969.7911218756,379283.6278298192].

This is a different preparation, not an equilibrium mean multiplied by an assumed heuristic factor. It is a separate parameter setting from the main r=3 A/B decision.

## 8. Finite-error acquisition and the cost of a physical implementation

The executed generator interrogations are exact rational computations. A finite-error extension is derived and evaluated, but no laboratory acquisition is claimed.

Suppose every dimensionless energy query has absolute error at most delta_E. Allow even nominally absent pair terms to be uncertain. The total energy-discrepancy oscillation is bounded by

    Omega <= [2n+6 binom(n,2)] delta_E.

At each degree-two clock query, at most two context bits are one. The recovered log local weight ratio has error at most 10 delta_E. Let e=exp(10 delta_E), delta_q bound the original downhill-rate observation error, and a_hat,max be the largest recovered attempt at probed contexts. Reverse conversion gives a pointwise attempt error at most

    D=2 e delta_q + a_hat,max (e-1).

Möbius coefficient recovery implies the conservative global error

    |a_true(y)-a_hat(y)| <= H D,
    H=1+2(n-1)+4 binom(n-1,2).

This controls all unmeasured contexts within the degree-two class, including uncertain small coefficients outside the nominal support. It is conservative; cancellations and shared energy errors are not exploited. Dividing by the exactly verified nominal minimum attempt gives a relative clock envelope eta, also enlarged to include reaction-clock uncertainty.

The common mass and heat-bath conductances then imply

    exp(-2Omega) tau_nom/(1+eta)
       <= tau_true <=
    exp(2Omega) tau_nom/(1-eta).                         (3)

For n=18, delta_E=10^-10, delta_q=10^-8 and reaction-clock relative uncertainty 0.002, the computed global clock envelope is eta about 0.0025476000024. Rational Taylor bounds enclose the exponentials. The robust intervals are approximately

    A: [148460674.8718444,149221900.4907883]
    B: [229651025.2471127,230824232.4318655].

Hence B/A >1.53899008 under those stated input errors. This propagates deterministic oracle accuracy; it does not assert those errors have been achieved experimentally.

### Explicit measurement accounting

Repeated independent first-flip dwell measurements at fixed prepared context estimate a downhill rate q. A conservative sample count based on exponential dwell concentration is

    m >= 4 eps^-2 log(2M/delta),

for relative dwell-mean error eps and M contexts. Convert rate error using eps/(1-eps). The expected dwell budget sums m/q over contexts; add all preparation, resetting and clamping costs.

For the particular nominal rates and 10^-8 absolute-rate error used above, the simple sufficient design costs about 9.6e20 model-time units of expected dwell, before resets. This is prohibitive and far longer than the predicted means. It is a conservative sufficient protocol, NOT a necessary measurement lower bound. It establishes no experimental speedup. Higher-precision direct evaluation of a justified microscopic law has different computational costs, but that law must actually be available.

The largest local unfavorable-state energy gap encountered in the final queries is approximately 21.49 kBT. Preparing the entire context and maintaining constraints can cost more. Work/heat, apparatus control, drift and force-field errors have not been measured.

The forward thermodynamic waiting factor is absent from the chosen reverse rate because q_down>=a/2. This does not make preparation or precise clock acquisition free. That distinction is a major unresolved physical limitation of the operation.

## 9. Comparators and full resource accounting

### Matched implemented comparator

The final comparison uses the same reverse-acquired heterogeneous model B and the same upper/lower goal 1.05. Both methods receive all acquisition information and the same reference factors. The full-state method is deliberately preconditioned with the same acquired structure, not handicapped as plain simulation.

    Tensor candidate: [230236127.696682,234586384.284724],
      ratio 1.018894761, 5 PCG steps, 9088 response coefficients, 6.58 s.
    Full-state preconditioned CG: [230236128.091320,230402298.292072],
      ratio 1.000721739, 6 steps, 262144-state vectors, 3.26 s.

Timings include exact synthetic reverse-query acquisition, partition search, operator construction, proposal and final validation. They exclude research, failed pilot development, literature work and serialization overhead. They are single runs on the recorded environment, not controlled hardware measurements. The full-state method uses directed-rounding residual bounds and exact integer source averaging; the tensor endpoints use exact rational contractions. Their returned accuracies are both within the same goal but not numerically identical.

The full method allocates global configuration vectors and three floating rate arrays per coordinate, plus additional working arrays. The candidate avoids those allocations but uses local matrices, product terms and large exact integers. No measured peak-memory or energy-consumption advantage is claimed.

### Complexity and what can explode

* Pairwise energy acquisition: 1+n+binom(n,2) queries; each synthetic evaluation visits the explicit interactions.
* Degree-two unknown-support clock acquisition: n[1+(n-1)+binom(n-1,2)] queries. Physical read precision and preparation are additional costs.
* Local models: sum_b 2^|B_b| states, dense local diagonalization roughly sum_b (2^|B_b|)^3 arithmetic. No polynomial bound without a block-size restriction.
* Cross-term compilation: the present expansion can be exponential in the number of inter-block bonds and context variables. The small term count is not guaranteed globally.
* Tensor response storage: approximately sum_b d_b r_(b-1) r_b. Required ranks are not known before solving.
* Exact residual verification: polynomial contractions in term count and ranks, multiplied by big-integer arithmetic cost. Input bit length and lifetime magnitude affect required precision; there is no measured uniform barrier-independent runtime theorem.

### Close literature and unexecuted comparisons

Masetti and Robol (2019) already derive tensor MTTA algorithms by splitting local and synchronization dynamics. This is particularly close prior art for the numerical representation. Their method was read, not reproduced as an independent package.

Verma, Benner and Nueske's September 2026 tensor molecular-kinetics work learns generator spectra and reaction coordinates from trajectory data, including state-dependent diffusion. The existence of that work prevents claiming that tensor-based discovery of slow kinetics is itself new.

Optimized weighted ensemble, TAMMBER and descriptor-free AIMMD are strong acquisition/pathway competitors. They have not been implemented or benchmarked against this candidate here. No superiority over their molecular results, tensor production implementations, graph-transformation methods or a specialized multidimensional exact solver is established.

## 10. A genuinely nonmodular failure

A separate preflight diagnostic has eighteen variables and all 153 heterogeneous pair interactions with factors at least two. With block size at most six, any partition leaves at least

    binom(18,2)-3 binom(6,2)=108

cross edges. Therefore the implemented product comparison constant is at least 2^108 for every admitted partition. The threshold heuristic actually selects singleton blocks with a still larger constant. The explicit cross-term compiler is stopped rather than expanding an exponential expression.

This is a failure of the present reference construction and access-to-computation route. It is not a hardness theorem for this model, proof that every possible comparison must be that loose, or a kinetic prediction. The main modular successes must not be extrapolated to this case.

The next missing operation is one that controls genuinely collective, heterogeneous slow structure without requiring a small low-contrast cut or a supplied invariant subspace. Possible conditional/pinned response constructions remain unvalidated. Merely increasing tensor ranks or asserting a good partition does not solve that acquisition problem.

## 11. Audits and provenance

The packet records 14576 exact assertions across staged tests. Most are elementary directed-edge identities, query conversions or entries of algebraic tests, not independent theorems. They include:

* exact small-model generator, detailed-balance and reference-comparison checks;
* exact 16-state inverse and preconditioned contraction checks;
* full-source rational tensor endpoint replays from public query transcripts, without private truth or hidden fixture labels;
* exact unknown kinetic-support recovery, including a dependency outside the energy graph;
* exact nonclosure witness for the single-spin observable space;
* exact finite-positive-shift response ambiguity;
* exact reverse-rate recovery and q_down in [a/2,a] for both canonical laws.

The final reverse transcripts, three reverse witness replays and combined_audit.json are authoritative for the main results. The all-at-once base audit was interrupted at 30 and 45 second tool limits; its component stages completed separately and their results were aggregated transparently. No unsuccessful invocation is counted as a pass. The final source files include the later kinetic-context compiler extension; selected earlier witnesses were replayed under it.

No external reviewer, proof assistant, experiment, protein force field, rare-event trajectory campaign or physical energy benchmark was used. Float optimization can fail; only completed exact endpoint checks are claimed as certificates.

## 12. Research assessment

This run removes an important technical restriction: a source-complete kinetic enclosure no longer requires a known invariant Glauber slow space. The unknown response can be solved relative to local models retaining all their modes, while a recovered physical interaction law controls recoupling globally. A separate reverse-relaxation scan can recover kinetic interactions that energies and representative clock readings miss.

That is not a fundamentally new general kinetics solution. The successful family remains modular; the rate law and finite-degree assumptions must be justified; physically obtaining precise context-conditioned clocks can be very costly; and the strongest implemented full-state comparator is faster at the tested size. Substantial numerical machinery is prior art.

The consequential objective remains an acquired, source-aware global kinetic description for genuinely nonmodular molecular gates. The present results specify exactly what information is sufficient in one nonclosed heterogeneous class, what finite response data cannot establish, and what further global structure or physical acquisition operation is still missing.

## Primary references and access

1. G. Masetti and L. Robol, Tensor methods for the computation of MTTA in large systems of loosely interconnected components (2019), arXiv:1907.02449. Full HTML inspected: https://arxiv.org/html/1907.02449v1 . Close prior art, not an independently replayed implementation.
2. M. Verma, P. Benner and F. Nueske, Tensor-based Approximation of Molecular Kinetics: Generator Learning, Reaction Coordinates and Incremental Updating (6 September 2026), arXiv:2609.06446. Abstract/full HTML inspected: https://arxiv.org/abs/2609.06446 . No molecular benchmark replication.
3. W. H. Ryu et al., Reducing Weighted Ensemble Variance With Optimal Trajectory Management, arXiv:2504.21663v3 (9 February 2026). https://arxiv.org/abs/2504.21663 . Current comparator, not run here.
4. T. D. Swinburne and D. Perez, Self-optimized construction of transition rate matrices from accelerated atomistic simulations with Bayesian uncertainty quantification, arXiv:1803.05273 (2018). https://arxiv.org/abs/1803.05273 . TAMMBER comparison, not run here.
5. S. M. Lichtinger and R. Covino, Accelerated descriptor-free path sampling for protein-ligand binding kinetics, arXiv:2607.15101 (16 July 2026). https://arxiv.org/abs/2607.15101 . Abstract-level comparator; not replicated.
6. V. Fanaskov, A. Rudikov and I. Oseledets, Neural functional a posteriori error estimates, arXiv:2402.05585 (2024). https://arxiv.org/abs/2402.05585 . Functional-error-majorant lineage, not a claim that the residual principle is new.
7. Inherited source: the uploaded Astra source-escape RESEARCH_NOTE.md, dated 14 October 2026. Its homogeneous exact closure is deliberately not a premise of the current proof. No theorem from optional external Astra/OpenAI repositories is load-bearing here.
