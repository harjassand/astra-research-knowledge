# Independent initial report: what can actually close collective dynamics

Researcher: existing-machinery researcher, 7 November 2026. This report was written independently, without reading the principal's or the other researchers' constructions. The governing workflow and the earlier reusable-intervention dossier were read. This initial report is to be frozen; subsequent corrections belong in a separate follow-up.

## 1. Strongest conclusion

There are already rigorous mechanisms that supply a reusable collective law for genuinely new preparations and drive protocols. Two especially clean ones are **strong lumpability under an exact symmetry** and **a common contraction of local causal influence**. Neither is a newly discovered general theory of interacting matter. They expose the decisive missing step more sharply than an exact Mori–Zwanzig identity does: obtain a small, experimentally identifiable predictive quotient, with a certificate valid uniformly over the intended preparations and controls.

I give below a complete finite-noisy-acquisition theorem for arbitrary controlled, interacting finite-state lattice dynamics with a common Dobrushin influence bound. Its error is uniform in system size and time, its drive may vary arbitrarily quickly inside a declared compact control family, its new initial states need only have an acquired finite-window marginal, and its reduced dynamics is an explicit finite master equation. This is a **proved restricted construction in this report**, subject to the stated physical and acquisition contracts. It does not require a global Gibbs-source approximation, an equilibrium conditional distribution, a known memory functional, or a microscopic state reconstruction on the entire specimen.

The price is substantial: the retained state is the full law on a bounded microscopic window. Its dimension grows as an exponential of a power of log accuracy, and its initial-state measurement cost can be even worse under noisy readout. It excludes conservation-induced slow modes, coexistence and criticality unless these are retained separately. Thus this construction **does not achieve the requested broad foundational capability or a demonstrated practical advantage**. Its mathematical novelty is **UNKNOWN**; the proof is a direct adaptation of classical disagreement coupling and local approximation, with finite acquisition accounting added.

The second, exact-symmetry construction permits nonlinear phase switching and metastability, with no weak-noise requirement, but is the familiar quotient process of a Curie–Weiss-type system. It demonstrates that the requested capability is not logically impossible in every interacting class, while making symmetry, horizon and acquisition costs explicit.

## 2. A complete construction: finite acquired local law, arbitrary new drives

### 2.1 Physical class and non-hidden promises

Let V be a finite subset of a bounded-degree graph (a finite torus is allowed), with n sites and alphabet S of q symbols. At site i a rate-one clock replaces the symbol by a sample from

\[
 p_{i,u_i(t)}(\cdot\mid x_{N_i}),\qquad |N_i|\le d,
\]

where N_i is a known neighborhood. All clocks and update randomness are independent conditional on the current configuration. Self-dependence is allowed by including i in N_i. The control u_i(t) is an arbitrary prescribed measurable function in a compact set U. The known transition architecture is a finite-state classical Markov model; the theorem does not infer that architecture, independence or locality from finite data.

There are at most a site types, so only a different local kernel tables need be acquired. Completely inhomogeneous systems use a=n. The local kernels obey a declared TV-Lipschitz bound L in their control argument. A finite control set uses its exact cardinality instead of a net. Neither arbitrary unknown controls nor an unknown regularity modulus are covered.

For each edge j to i define

\[
 C_{ij}=\sup_{u,x,y:\,x_\ell=y_\ell\ (\ell\ne j)}
       \|p_{i,u}(\cdot\mid x)-p_{i,u}(\cdot\mid y)\|_{TV}.
\]

The essential common certificate is

\[
 \alpha:=\sup_i\sum_j C_{ij}<1,\qquad \gamma=1-\alpha.\tag{M1}
\]

The supremum is over all allowed controls. It is much stronger than saying that every frozen controlled generator happens to mix rapidly. It supplies one contraction geometry for every time-dependent composition.

The finite calibration interface permits clamping/resetting the declared neighborhood to any configuration, selecting a control value, executing one **update event**, and reading its output symbol through a calibrated q-by-q stochastic detector matrix A with a known inverse. Let chi=||A^{-1}||_{1 to 1}. Reset errors and residual detector errors have a warranted measured-distribution TV budget b. Costs of clamps, resets, timing, one-event control and calibration are part of the acquisition cost; these operations are not inferred from passive equilibrium data.

This interface is strong and experimentally class dependent. A short free-evolution experiment is not silently treated as a one-event experiment. A separate short-time generator-estimation proof would be needed to replace it.

### 2.2 What a genuinely new preparation supplies

For a core A0 of k sites choose B to contain every site within graph distance R of A0, measured in the dependency graph of the N_i. A query supplies an initial distribution p0^B on S^B, or acquires an estimate hat p0^B with

\[
 \|p0^B-\widehat p0^B\|_{TV}\le\zeta.
\]

Nothing is required of the initial exterior conditional on B. The physical source may have arbitrary long-range correlations and may be far from equilibrium. No global trace/TV promise is used. A new unknown preparation needs its own paid finite initial descriptor; a previously unperformed product preparation can instead specify that descriptor analytically, with its warranted preparation errors included. No fixed old dataset can describe an unspecified future preparation for free.

### 2.3 Constructible eliminated dynamics

Fix any exterior symbols, for example all zero. Delete exterior sites and let the retained B sites evolve with the acquired local update tables, using the fixed symbols when a neighborhood crosses the boundary. This defines a **known stochastic generator** hat Q_B(u_B) on D=q^{|B|} configurations. Its probability vector solves

\[
 \dot{\widehat p}_t=\widehat p_t\widehat Q_B(u_B(t)),
 \qquad\widehat p_0=\widehat p0^B.\tag{M2}
\]

All coefficients come from a finite table and the supplied controls. There is no unknown memory kernel, conditional Gibbs solve, or inner many-body optimization in (M2). It retains microscopic configurations only on the fixed window; calling it a few-variable order-parameter closure would be false.

Suppose the acquired kernels satisfy, simultaneously for all their arguments and all u,

\[
 \|p_{i,u}(\cdot\mid x)-\widehat p_{i,u}(\cdot\mid x)\|_{TV}\le\eta.
\]

**Theorem M.** For every n, every allowed prescribed control field, every initial physical law having the specified B marginal, every t>=0 and every f:S^{A0}->[-1,1],

\[
 \left|\mathbb E f(X_t)-\widehat p_t(f)\right|
 \le 2k\left[
       \zeta e^{-\gamma t}+\alpha^{R+1}
       +\frac{\eta}{\gamma}(1-e^{-\gamma t})
       \right].\tag{M3}
\]

An additional numerical TV error nu adds 2 nu. The corresponding core-marginal TV bound is k times the square bracket. The same acquisition event proves the bound for **all** future controls and numerical queries; no union bound over their number or over time is necessary. This is not a guarantee for controls that depend on the actual unmodeled specimen through a new online observation channel. Such feedback needs its own observation/policy coupling contract.

**Proof.** Couple the two initial B configurations by a maximal coupling, so every site initially disagrees with probability at most zeta. Use the same rate-one clocks at retained sites. At each update use a maximal coupling of the true and learned output laws. Let e_i(t) be the disagreement probability. Telescope changes in the neighbors one coordinate at a time. For i in B,

\[
 e_i'(t)\le-e_i(t)+\sum_{j\in B}C_{ij}e_j(t)
                  +\sum_{j\notin B}C_{ij}+\eta.
\]

The inequality holds in the integral/upper-Dini sense and is enough for finite-dimensional cooperative comparison, including measurable controls. Put C_B=(C_ij)_{i,j in B}. Positivity of exp(t(C_B-I)) and C_B 1<=alpha 1 bound the initial term by zeta exp(-gamma t) and the constant eta forcing by eta(1-exp(-gamma t))/gamma.

For the boundary term, its infinite-time upper bound is

\[
 v=\sum_{\ell\ge0}C_B^\ell C_{B,B^c}\mathbf1.
\]

Interpret C as the transition weights of a substochastic random walk, with the missing row mass killed. Then v_i is its probability of reaching B^c before death. Starting at i in A0, exit needs at least R+1 dependency steps. Each step survives with probability at most alpha, hence v_i<=alpha^{R+1}. This proves the site bound. A union bound on the k core sites gives the core-TV estimate. Coupled f values differ by at most 2 on a disagreement, proving (M3). The calculation uses only the common C, so it is uniform in arbitrary time dependence of the controls. QED.

The row-sum condition can be replaced by a weighted influence certificate with a positive vector w and Cw<=alpha w. Then distances and endpoint factors use w; the improvement is real only when those factors remain controlled. The unweighted theorem is the checked claim here.

### 2.4 Finite noisy acquisition and a computable contraction certificate

Take an h-net of U of size G. There are K=a G q^d kernel-table rows. With M fresh trials per row, let the observed categorical empirical law be r_hat. Apply A^{-1} and project to the probability simplex in l1. A union of the qK Hoeffding events gives, with probability at least 1-delta,

\[
 \eta\le \chi q\sqrt{\frac{\log(2qK/\delta)}{2M}}
              +2\chi b+Lh.\tag{M4}
\]

The factor 2 in the systematic term comes from inversion and simplex projection; more repetitions do not remove it. Choosing the nearest control-net point defines the learned kernel for every u. This simple estimator need not be statistically optimal.

Compute influence entries from the acquired table, taking the maximum over net points, and call the largest row sum hat alpha. Each true neighbor influence is at most its table estimate plus 2 eta, so

\[
 \alpha\le\alpha_{rob}:=\widehat\alpha+2d\eta.\tag{M5}
\]

If alpha_rob<1, it is a **finite-data sufficient certificate**, conditional on the known locality, update architecture and control modulus. Otherwise the method abstains; failure is not evidence that the material lacks a useful collective description. Use alpha_rob in (M3). This certificate does not infer a uniform control modulus or an absence of hidden degrees of freedom.

Total calibration trials are KM, and total reset/measurement cost is KM times their actual costs. If U has p parameters and fixed diameter, G=O(h^{-p}); the curse of control dimension is explicit. Homogeneous laws have a=1; general inhomogeneity may force a=n.

For an arbitrary new initial B marginal with m=|B| and Q=q^m, direct histogram tomography through independent calibrated site detectors has inverse norm at most chi^m. An elementary empirical-l1 estimate gives a sufficient fresh-copy count

\[
 M_0\ge\frac{\chi^{2m}}{\zeta^2}
       \left(\sqrt{q^m}+\sqrt{2\log(1/\delta_0)}\right)^2,\tag{M6}
\]

up to the explicitly separate systematic source/detector budget. Indeed E||r_hat-r||_1<=sqrt(Q/M0), bounded differences adds sqrt(2 log(1/delta0)/M0), inversion multiplies by chi^m and simplex projection converts the l1 error into at most that TV bound. A measured-distribution TV bias b0 adds 2 chi^m b0 to zeta. Fresh copies mean independent specimens or a warranted conditional-freshness replacement. Spatial samples from one arbitrary correlated specimen are not fresh copies.

### 2.5 Scaling, output scope and whether this is enough

For a D_lat-dimensional lattice with fixed interaction range, m=O(k(R+1)^{D_lat}). To make the boundary error epsilon, R=O(log(k/epsilon)/|log alpha|). Consequently

\[
 D=q^m=\exp\left(O(k[\log(k/\epsilon)/|\log\alpha|]^{D_{lat}})\right).
\]

The law is independent of n and of the future horizon at fixed accuracy, but becomes very expensive near alpha=1 and in dimension three. Local-window initial tomography can be the dominant cost. Merely saying “polynomial in n” would conceal the relevant obstruction.

For S piecewise-constant control segments, each query multiplies S explicit D-dimensional stochastic semigroups. Dense matrix exponential with scaling, series approximation and repeated squaring gives finite arithmetic cost polynomial in D, S, log(1+mT) and log(1/nu), with precision and all rounding errors charged. A simpler sparse uniformization implementation has cost linear in mT up to the required Poisson truncation and Dm factors. Thus horizon-independent **model error** does not mean free processing of a long control specification.

For a translation-invariant physical law, preparation and homogeneous drive, a single window predicts the expectation of the normalized macroscopic density n^{-1} sum_i tau_i f with the same bound. Arbitrary inhomogeneous drive/preparation fields require up to n windows or an additional representation of their variation. No theorem here turns the mean of a spatial average into its concentration or distribution for arbitrary long-range-correlated initial sources. For example a half all-plus/half all-minus mixture has O(1) initial variance of the global magnetization at every n. Local currents with a declared bounded neighborhood readout are covered after enlarging the core; an unnormalized time-integrated current incurs an additional T factor.

This class is a classical dissipative lattice model, including high-temperature heat-bath spins with beta sum_j |J_ij|<1 as a simple sufficient regime. The theorem predicts far-from-equilibrium responses to new fields and local preparation laws, but not generic conservation laws, critical coarsening, coexistence or a low-temperature phase diagram. It is a rigorous local causal compiler, not yet the sought learned macroscopic physics.

## 3. Exact collective states can retain phase switching: the symmetry comparator

For completeness, a mathematically stronger physical behavior is already attainable in a more symmetric class. Let X be a finite configuration space, G a group acting on X, and Q^u a controlled generator satisfying Q^u(gx,gy)=Q^u(x,y) for every g and allowed u. Let z(x) be its orbit. Then

\[
 \overline Q^u(z,z')=\sum_{y:z(y)=z'}Q^u(x,y)
\]

is independent of the representative x in z. The orbit process is Markov for **every initial law**, without exchangeability of that law. Its distribution satisfies an explicit controlled master equation. Proof: the generator maps every f composed with z to (bar Q^u f) composed with z; the finite forward equations then close, also under time-dependent controls. This is the elementary strong-lumpability mechanism, not a new result.

For N Ising spins with complete-graph Glauber heat bath, z is the number k of plus spins. With H=-(J/2N)(sum_i sigma_i)^2-h sum_i sigma_i, the rates are

\[
 q_{k,k+1}=(N-k)\frac{1+\tanh[\beta(J(2k-N+1)/N+h)]}{2},
\]
\[
 q_{k,k-1}=k\frac{1-\tanh[\beta(J(2k-N-1)/N+h)]}{2}.
\]

The self-spin correction +/-1 is necessary. Every new microscopic preparation is represented by its **measured initial count distribution**, and all new time profiles of J,h,beta preserving the permutation symmetry are allowed. The N+1-state tridiagonal law captures finite-N noise, hysteresis and switching probabilities; a deterministic mean-field ODE generally cannot retain rare switching on exponential horizons.

A fully explicit nonparametric acquisition interface can prepare each k, execute one uniformly chosen spin update, and read the count change, under a finite set of control generators. Uniformization has attempt rate N. If every acquired quotient transition row has TV error eta, common Poisson clocks and maximal coupling give, for every path event through time T,

\[
 \|\mathcal L(Z_{[0,T]})-\widehat{\mathcal L}(Z_{[0,T]})\|_{TV}
 \le\zeta+1-e^{-NT\eta}\le\zeta+NT\eta.\tag{M7}
\]

Here zeta is initial-count-law TV error. Convex mixtures of a finite set of calibrated generators allow continuously variable drive weights without a control net. A general nonlinear control family needs a net/modulus or a separately identified parametric model. Detector inversion on the count alphabet has condition number chi_N, which may grow exponentially if the only instrument is independently noisy single-spin readout. Count preparation, measurement and holding times cannot be omitted.

This exact quotient is an equal-information incumbent against any claim that a learned few-coordinate latent model has newly enabled phase-switching prediction for the same symmetric system. It has exponentially smaller state space than 2^N, but still O(N) collective states. On switching horizons T~exp(cN), the conservative acquisition precision eta=O(epsilon/(NT)) can itself be exponential. Neither exact closure nor a pretty sigmoid solves that statistical problem.

## 4. A hard preparation obstruction that the positive theorem avoids

Take N classical input bits uniformly distributed conditional on their parity being b in {0,1}. Every proper-subset marginal is exactly identical for b=0 and b=1. A nearest-neighbor reversible CNOT circuit can collect parity in one endpoint in O(N) time and then copy that bit into N initially zero ancillas in another O(N) time, giving final normalized ancilla magnetization differing by 2 between the two preparations. Controlled local Ising-type gate implementations or a local reversible cellular automaton realize this as interacting classical information processing; arbitrary gate drives are part of the obstruction's specified class.

Thus no descriptor acquired only from fixed-order proper-subset marginals can uniformly predict all later controlled macroscopic outcomes for all initial preparations. Even full noisy bitstring readout is expensive: independent binary detector visibility v in (0,1) changes the two output laws to

\[
 P_b(y)=2^{-N}[1+(-1)^b v^N\,\operatorname{parity}(y)].
\]

Their one-copy TV distance is v^N. For v^N<=1/2, a direct chi-square/KL calculation gives D(P_0||P_1)<=4v^{2N}. Pinsker on M independent records shows that constant distinguishing success requires M=Omega(v^{-2N}). This is not a claim against calibrated direct parity measurements or allowed acquisition-time intervention circuits; those are materially stronger access rights. It is a reason not to convert local passive information into an arbitrary-preparation guarantee.

The common contraction in Theorem M prevents this amplification. Any N-step path that transmits a remote hidden bit has influence at most alpha^N. Strong lumpability instead retains precisely the relevant orbit variable. Both are concrete structural operations; an exact elimination identity alone is neither.

## 5. Primary-literature audit and overlap

The following sources have been retrieved in full text, not taken only from snippets. Cached HTML/text and the three Zenodo PDFs are under ../machinery/source/. None is imported as a black-box premise in the proof of Theorem M; its central estimates are proved above. Exact known predecessors still deserve credit.

1. **Galves, Garcia, Loecherbach and Orlandi, “Kalikow-type decomposition for multicolor infinite range particle systems,” Ann. Appl. Probab. 23 (2013), arXiv:1008.2740v3, Theorem 1, Proposition 1, Theorems 2–3.** Continuous bounded-rate systems admit a mixture of finite-range update kernels; the declared high-noise branching criterion is sup_i sum_{r>=0}|V_i(r)| lambda_i(r)=gamma<1. With inf_i M_i>0 they prove exponential local forgetting and perfect stationary simulation. This is a direct predecessor of backward finite-dependency descriptions. Their homogeneous stationary result is not automatically a theorem for arbitrary externally switched generators. Important import check: the printed total-event tail in Theorem 3(1), P(N_STOP^F>N)<=|F|gamma^N, appears false literally for |F|>1: with lambda(-1)=1 and F of size two, gamma=0 but N_STOP=2 deterministically. The PDF confirms the wording (p.16, equation (5.4)). I do not import this estimate. Subcritical extinction and local forgetting have separate coupling proofs; the construction above uses neither disputed tail nor their stationary theorem.

2. **Lucia, Cubitt, Michalakis and Perez-Garcia, arXiv:1409.7809v2 (2015), Theorem 1, equation (2).** Their finite periodic local Lindbladian family has a unique fixed point and uniform rapid mixing ||A(t)-A(infinity)||<=c L^delta exp(-gamma t). A perturbation sum of local terms with cb norm at most epsilon changes any fixed-support observable by at most C_X||A||epsilon uniformly in time and system size. Disconnected support is permitted. This already supplies a broad stability mechanism beyond detailed balance, but is a fixed-generator theorem; it does not by itself certify a common contraction for arbitrary drive switching or identify a predictive representation from noisy experiments.

3. **Rudolf and Schweizer, arXiv:1503.04123v3, Theorem 3.1, equation (3.2).** If the exact kernel has Wasserstein contraction tau(P^n)<=C rho^n and the approximate kernel has a Lyapunov drift P_tilde V_tilde<=delta V_tilde+L, they prove W(p_n,p_tilde_n)<=C[rho^n W(p0,p_tilde0)+(1-rho^n)gamma kappa/(1-rho)], with their weighted one-step discrepancy gamma and moment bound kappa. Theorem M is in the same contraction-plus-one-step-error lineage. Time-inhomogeneous common contraction follows by its same telescoping argument, not by asserting all frozen chains satisfy the theorem independently.

4. **Lin, Tian, Anghel and Livescu, arXiv:2101.05873v3 (2021).** The paper constructs data-driven Markov and memory operators using Mori's linear projection and reduced-observable correlation data, and evaluates Lorenz-96 predictions. The GLE and memory are genuine prior machinery. They do not provide an end-to-end finite-noise acquisition theorem uniform over previously unobserved preparations and arbitrary drive laws; a projection/correlation identity is not such a theorem. See their projection construction, the data-driven operator algorithms and the numerical section. No mathematical theorem from this paper is imported here.

5. **Zhu, arXiv:2109.01990v2 (2021), Theorem 1 and Proposition 2.** Theorem 1 assumes the full hypocoercive conditions (H1)–(H4), the domain condition (D) of the cited Grothaus–Stilgenbauer framework, a differential factorization of the dissipative part, and a finite-rank symmetric projection. It obtains exponential orthogonal-semigroup decay on QH intersect ker(K)^perp. Proposition 2 specializes to Langevin potentials satisfying (C1)–(C3). This can justify decay of a specified memory kernel under its exact operator/domain hypotheses. It does not construct the kernel from finite noisy data or make the projection uniformly sufficient under new controls. Source conventions around the sign of D require care; I have not transplanted its proof into the present jump-process setting.

6. **Zimmerman et al., arXiv:2406.03606v1 / MLST 5, 035062 (2024), sections on time-dependent dynamics and conclusion.** They acquire a local neural force functional from steady-state Brownian simulations and apply it to new time-dependent drives and larger boxes. This is a strong practical comparator. The text explicitly identifies omission of history as an approximation: transient and steady-state memory differ, with potentially larger deviations at short times. It supplies empirical transfer, not a uniform new-preparation/new-drive theorem. A future physical benchmark must compare against this competent force-functional baseline, not just a memoryless mean-field toy.

7. **Schmidt, arXiv:2607.19255v1 (2026).** The full formulation starts at thermal equilibrium under an external potential and derives a formal one-body current plus interparticle-distance-flux variational structure. The intrinsic entropy superpower functional contains the difficult nonequilibrium contribution. It does not provide finite-data construction, a uniform approximation complexity or a source contract covering arbitrary new nonequilibrium initial laws. It is important existing structure, not a completed acquisition theorem.

8. **Yang et al., arXiv:2610.40117v1 (2026), sections II–III, Appendix A and discussion.** AVP explicitly assumes fast constrained microscopic relaxation relative to order evolution and that the retained sector includes all relevant slow modes; the simulations take a Markovian limit. The discussion states that dissipative coefficients remain phenomenological and evaluating transport kernels is future work. Constrained microscopic states are recomputed as the collective configuration changes. It is a substantial predecessor for phase-field closure, but its own text preserves precisely the time-scale and eliminated-kinetics limitations that the present task requires us to close.

9. **Han, Zhao and Li, arXiv:2609.37392v1 (2026), Proposition 4.1, Theorem 4 / Appendix B.5.5.** Proposition 4.1 separates next-macrostate fit from multi-step predictive closure. Theorem 4 assumes a pre-existing full-row-rank exact linear realization, population updates starting in a neighborhood of it, and a transverse residual singular-value inequality s_star>sqrt(lambda_tr)||A Sigma_x^{1/2}||. It gives local convergence and fixed-horizon, covariance-weighted rollout bounds. This is not global representation discovery, a finite experimental learning theorem or a uniform distribution/control-shift guarantee. Its experiments are relevant baselines, and its warnings about one-step fit support rather than remove the sufficiency problem.

10. **Zenodo 20410346, Lopez Villanueva (2026), 4-page PDF, Assumptions 1–3 and Theorem 1.** The estimate is a norm-product bound once orthogonal-semigroup decay and bounded return coupling are assumed. Assumption 2 already posits such decay, initially written exp(-alpha t); the proof substitutes exp(-alpha t/epsilon), requiring an additional uniform scaled bound rather than following merely from the frozen fast spectral gap. Fiber invariance/domain questions also need an actual model. No finite acquisition or usable general closure follows. I do not import it.

11. **Zenodo 22722557, 19-page PDF, local linear surrogate (2), Propositions 1–2.** For a fixed resolved/unresolved block system the exact kernel is N Q^{tau-1} P; assuming ||Q||<=1-gamma and small cross-couplings gives the geometric tail by a direct norm estimate. This is valid elementary elimination for the stated surrogate. It does not establish that a nonlinear driven material admits that surrogate uniformly or make the full resolved evolution stable under tail truncation without a further stability estimate.

12. **Zenodo 23587917, 7-page PDF, Axioms 2.1–2.6 and Theorems 4.1–4.6.** Several desired properties are placed in axioms, including subgrid regularization preventing blow-up. Theorem 4.2's entropy-loss-to-quotient-law argument does not establish dynamical lumpability: the same fibers and entropy loss permit different block transition rates. Therefore it cannot be imported as an established general closure theorem. Its numerical appendix evaluates selected formulae, not the missing implication. The source is retained; no inference is made from its promotional abstract alone.

Additional leads from the principal, received only while this initial report was being written: Hilder–Sharma arXiv:2201.10256v2 and Blassel arXiv:2610.36078v1. These are not yet inspected or imported in this frozen initial report; exact overlap will be checked in follow-up. Rebeschini–van Handel arXiv:1301.6585 is another strong local-filtering comparator; its exact theorem hypotheses remain to be checked before application. Strong lumpability sources (Kemeny–Snell, Buchholz) have been identified, but no numbered statement is being quoted without a verified primary full text; the orbit proof above is self-contained.

## 6. Consequential target and what is still missing

The strongest worthwhile next operation is not another formal memory representation. It is a **certified, learned predictive quotient that contains slow collective variables and contracts only the conditional unresolved sector**. The quotient must remain identifiable and sufficient under the whole declared control family and new preparation interface, while its law can be advanced without repeatedly solving the microscopic conditional problem. It should retain rare transitions when those are the consequential target.

A viable but unproved route would combine exact block counts/order parameters with a fast conditional mixing certificate inside each block, then learn the reduced generator by clamped local experiments. A proof needs: (i) quantitative conditional equilibration including its dependence on the evolving slow field, (ii) an initial-layer bound using only acquired initial descriptors, (iii) common control-uniform stability, (iv) constructive conditional rates with acquisition conditioning, (v) a boundary/localization bound if blocks interact, and (vi) an error that remains informative on the target switching/coarsening horizon. Standard averaging may do much of this in a specified scale-separated class. Without these operations, merely naming conditional mixing or fitting a local neural law is a proposal.

For the broad user objective, status is **OPEN / NOT ACHIEVED**. Theorem M and the exact-symmetry comparator are concrete mathematical controls for judging later candidates. Neither establishes historical priority, physical validation or a resource advantage over the same-information incumbent.

## 7. Status ledger and reproducibility

| Claim | Status | Evidence / limitation |
|---|---|---|
| Uniform-time, new-drive local prediction theorem M | Proved in this report under explicit model/acquisition contracts | Complete disagreement comparison and finite table estimator above |
| Finite-data sufficient common-influence certificate | Proved conditional on known locality, Markov update architecture and control modulus | Equations M4–M5 |
| Arbitrary new preparation needs only a finite-window marginal for theorem M | Proved at the stated local-output scope | No exterior assumptions; paid M6 acquisition |
| Phase-switching law for symmetric complete-graph spins | Established known mechanism, self-contained quotient proof | Exact permutation invariance and count acquisition |
| Unknown generic low-dimensional collective state can be acquired efficiently | Open | No representation/conditioning theorem |
| Fixed-order passive local information suffices for arbitrary new preparations and gate drives | Disproved for the stated access class | Parity preparation plus local CNOT readout amplification |
| Finite noisy acquisition has practical advantage | Not established | No physical data or matched end-to-end benchmark |
| Historical novelty of theorem M or the synthesis | UNKNOWN | Direct overlap with disagreement coupling, local simulation and perturbation literature |

Source hashes, finite diagnostic output and later source checks are to be preserved separately in ../machinery/. The source caches are evidence pins, not proofs of the proposed physical capability.
