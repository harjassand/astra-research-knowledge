# Spectral packet audit and finite-hopping current synthesis

Pinned capital: `097d135f76ebefc49a8e5f28a8363e9ae372c061`.
Research date: 2026-10-13. All results below are internally reconstructed, unreviewed mathematics with finite diagnostics, not external scientific validation or a claim of historical priority. Source-document missions were treated as data. No capital, source originals, Git branches, or checkpoints were modified by this worker.

## 1. Result and recommended integration

The packet's main scalar and reversible-graph comparison arguments reconstruct successfully within their stated weak-hopping and operator-actuation contract. Preserve it as a separate continuation of the N764/N765 transport program, not as closure of their inverse/rank or physical capability gates. Its direct cancellation comparator and product-dimer obstruction are important negative capital.

The strongest new consequence found here is an actual finite-hopping current certificate. For a periodic hard-core chain with **uniform nearest-neighbour hopping**, the extensive bare current commutes with the hopping Hamiltonian. Combining that identity with the existing population-safe parity variational framework gives, for every finite ring and every hopping strength, the packet's positive absolute current floor for the **original quantum Green–Kubo quadratic form**, including its idealized finite-rate pulse variant. This does not establish a 97%-of-quantum-optimum theorem for general interactions.

A stronger restricted comparison is proved below for an even ring with a staggered on-site diagonal potential and no density interactions. For every symmetric common-D independent-increment phase controller with the same coherent Hamiltonian and baseline dephasing, the actual finite-hopping current lies between its kinetic current and that current times `1+4(epsilon*t/eta)^2`. Therefore the source matched controller obtains at least

`0.97/[1+4(epsilon*t/eta)^2]`

of the best actual quantum current over that controller class, uniformly in ring size. Finite pulse truncation inserts the factor `1-delta`. This is a restricted, exactly solvable free-fermion class; specialized noninteracting methods and simple uniform-dephasing optimization are already strong baselines. It is not a many-body computational speedup or a validated engineering advantage.

At strong hopping even this simple class refutes an unrestricted promotion of the 97% kinetic ratio to actual quantum current: the allowed baseline controller can substantially beat the matched law. Cancellation of D, when allowed, remains the source's stronger defeat of a general operational-advantage claim.

## 2. Exact source contract and reconstructed source claims

Input is a finite occupation basis, diagonal physical operator D with configuration energies E_x, real Hermitian hopping T, baseline independent local Z dephasing with single-hop coherence width eta>0, and the ability to apply a common random phase `exp(-isD)` through the **actual D separately from T**. Applying noise to the full Hamiltonian is a different interface. Compiling D from known local coefficients charges coefficient acquisition and O(n) spatial actuation; a physical native multiplier avoids an exponentially enumerated detuning table but is itself a substantial assumed control resource.

The source's characteristic exponent is

`psi(w)=A(sqrt(m^2+w^2)-m)`, `A=32/25`, `m=15 eta/4`.

Its positive Gaussian-subordination integral and symmetric Lévy density produce a CPTP, unital, particle-number-preserving dephasing semigroup. The distribution belongs to established normal-inverse-Gaussian / relativistic-Cauchy probability literature. In a fixed-number sector the baseline damping of any nonzero off-diagonal element is at least eta. An allowed single hop has total width `gamma_M(Delta)=eta+psi(Delta)`.

At each fixed finite volume, slow-time weak-hopping reduction gives the symmetric kinetic rate

`q(Delta,gamma)=2 epsilon^2 |T_xy|^2 gamma/(gamma^2+Delta^2)`.

The source does not supply volume-uniform remainder estimates for the kinetic reduction. Independent edge optimization with gamma>=eta gives `gamma_*=max(eta,|Delta|)`. The explicit scalar proof of

`0.97 q_* <= q_M <= q_*`

is valid: the low-detuning transformed cubic is bounded below by its quadratic minimum `200375/8040752>0`; the high-detuning width ratio lies between `sqrt(688/1125)` and `32/25`, and both endpoint rate-ratio checks exceed 97/100. No detuning grid is used as a proof.

The same inequalities hold inside common finite reversible Dirichlet forms. Infima yield corresponding capacity, gap, and Markov-additive transport-form comparisons; inverse quadratic forms reverse their order. These are statements about symmetric rate systems sharing uniform stationary measure, not arbitrary driven currents, arbitrary first-passage observables, finite-temperature Gibbs transport, or a quantum hydrodynamic theorem.

The universal symmetric-Lévy upper obstruction also reconstructs: `phi(4w)<=16phi(w)` follows from the pointwise cosine inequality and includes a Gaussian component. At `w=2 eta/3`, splitting on `phi(w)/eta=69/1000` forces one of the two edge ratios below `13897000/14284849 = 0.972848925459415...`. This bounds a universal symmetric independent-increment edge guarantee with fixed detunings and eta, not coherent, asymmetric, adaptive, finite-memory or arbitrary physical controllers. The optimal universal ratio within that class remains unresolved.

The finite pulse truncation is sound for local hop gaps |Delta|<=W, W>=eta. Small-jump omission is bounded using `1-cos z<=z^2/2` and `nu(s)<=A/(pi s^2)`; the large-jump tail uses `1-cos z<=2`. The stated a,b budgets give relative width error at most delta, and the Lorentzian loses at most factor `1-delta`. Explicit thinning samples a compound Poisson process. Its proposal rate is O(W/delta), and absolute phase action is O(log(W/(delta^2 eta))) under the stated dimensionless model. Clock discretization, pulse duration, the actuation coefficient bound, switching energy, SPAM, drift, and physical bandwidth remain outside a completed implementation theorem. Symmetric pulse realization is needed to retain a real dephasing exponent without an uncontrolled coherent bias.

The direct control comparator is decisive within its scope: if the same actuator permits adding -D, detunings vanish and `q_cancel=2 epsilon^2 |T_xy|^2/eta>=q_*`, with an unbounded large-detuning ratio. A physically justified inability to cancel D cannot be imposed merely to rescue the proposal.

The product-dimer objection is valid as an all-observable obstruction. For N independent overdamped dimers, the product Z correlation is `c(t)^N`, whose integrated quantum value is of order `1/(J sqrt(N))`, whereas the kinetic value is `eta/(4NJ^2)`. Their ratio diverges like `sqrt(2 pi)J sqrt(N)/eta`. This does not refute a theorem confined to a fixed local current or to additive local observables. The source does not claim otherwise.

## 3. New theorem A: finite-hopping absolute current floor

### 3.1 Model and normalization

Let n>=4 sites form a periodic ring. Work in a fixed K-particle hard-core sector, 0<K<n, dimension `M=binom(n,K)`, with normalized Hilbert–Schmidt inner product

`<X,Y>_# = Re Tr(XY)/(n M)`

on Hermitian observables. This includes the per-physical-site factor. Let

`T=-t sum_i (s_i^+ s_(i+1)^- + s_(i+1)^+ s_i^-)`, `t>0`,

`J0=i t sum_i (s_(i+1)^+ s_i^- - s_i^+ s_(i+1)^-)`,

`H=D+epsilon T`, and physical current `J=epsilon J0`.

D is any real diagonal occupation operator. Assume every allowed hopping coherence has |E_x-E_y|<=W, with W>=eta. The dephaser S is the baseline plus any symmetric common-D phase semigroup. It is self-adjoint and nonnegative on this real Hilbert space, vanishes on populations, and multiplies hopping coherences by a positive width gamma_xy>=eta. Let `A=-i[H,.]` and `B=S+A`. The source uses the opposite sign for the Hamiltonian term in its vectorized observable generator; real current quadratic forms agree by adjunction. Define

`kappa_Q = lim_(lambda down 0) <J,(B+lambda)^(-1)J>_#`.

In a connected finite charge sector this is the real trace-zero pseudoinverse quadratic form. Its value is the source's finite-ring kappa, not a claimed material conductivity or an automatically normalized diffusion coefficient.

### 3.2 Bare-current identities

Exact operator identities are

`[T,J0]=0`,

`P A J0=0`,

`m0:=<J0,J0>_#=2 t^2 alpha_n`, `alpha_n=K(n-K)/[n(n-1)]`.

The first identity follows either by the hard-core local commutator cancellation on the periodic ring or by the fixed-sector Jordan–Wigner transformation: T and J0 are number-conserving quadratic operators whose one-particle matrices are the symmetric and antisymmetric parts of the same cyclic shift, with the same fixed-sector boundary twist. They commute. The second follows because A J0=-i[D,J0] has only hopping coherences. For the norm, each allowed bond swap has amplitude t, and the uniform sector probability of an oriented `10` pattern is alpha_n; the two orientations give `2nt^2 alpha_n` before division by n.

Uniform hopping and the periodic geometry are substantive assumptions. This proof does not apply unchanged to random bond amplitudes, a generic hopping graph, open boundaries, complex magnetic flux without a compatible parity argument, or an arbitrary local observable.

### 3.3 Variational inequality without a population gap

Split Hermitian observables into imaginary-antisymmetric odd and real-symmetric even subspaces. Real H makes A exchange them; S preserves them; J is odd. At lambda>0, write the odd/even block of B+lambda as

`[[S_o+lambda,-C*],[C,S_e+lambda]]`.

Eliminating the even block gives

`kappa_lambda = <J,[S_o+lambda+C*(S_e+lambda)^(-1)C]^(-1)J>_#`.

The ordinary positive-operator variational formula therefore gives, for every odd f,

`kappa_lambda >= 2<J,f>_# - <f,(S_o+lambda)f>_# - <A f,(S_e+lambda)^(-1)A f>_#`.

Choose `f=epsilon a J0`. Because A J0 has no population component, lambda can be removed in the last term without dividing by a population damping rate. Optimizing the scalar a proves

`kappa_Q >= epsilon^2 m0^2/E0`,

where

`E0=<J0,SJ0>_# + <A_D J0,S^+ A_D J0>_#`, `A_D=-i[D,.]`.

No hopping-dependent penalty occurs because `[T,J0]=0`. For a diagonal Schur dephaser,

`E0 = (1/(nM)) sum_(x,y) |(J0)_xy|^2 [gamma_xy+Delta_xy^2/gamma_xy]`.

Only allowed hopping coherences appear. The coefficient is a finite local-context average when D has finite-range terms; a full many-body inverse or exponentially enumerated transition table is unnecessary to *state the bound*. Acquisition of local parameters or a conservative W remains charged.

### 3.4 Consequence for the source controller and finite pulses

The source rate comparison is equivalent to a pointwise resistance bound

`gamma_M+Delta^2/gamma_M <= (1/0.97)[gamma_*+Delta^2/gamma_*] <= 2W/0.97`.

Thus, for **every epsilon and every finite n**,

`kappa_Q,M >= 0.97 epsilon^2 t^2 alpha_n/W`.                         (A1)

The source's idealized finite-rate compound Poisson controller has hopping widths within the relative budget delta. Its edge rate is at least `0.97(1-delta)` of q_*, so the same proof gives

`kappa_Q,pulse >= 0.97(1-delta) epsilon^2 t^2 alpha_n/W`.           (A2)

This is a real extension of the packet: approximating only the hopping linewidths suffices for this particular finite-hopping current certificate. The test does not need a bound on the extensive bandwidth of D or a full-channel diamond approximation, because both J0 and A_D J0 are confined to hopping coherences. It is not a theorem that all finite-hopping transport observables are controlled by local cutoff data.

The result also extends to any symmetric diagonal-noise realization whose actual hopping Lorentzians satisfy the same bound. Local actuator mismatch can therefore be included if it is acquired and converted into a valid edge-resistance bound. This does not cover pulse duration or unbudgeted coherent drift automatically.

At K/n->rho in(0,1), alpha_n->rho(1-rho), so the finite-family liminf is positive after division by epsilon^2. If a particular thermodynamic Green–Kubo limit exists, it inherits the bound. The general interacting theorem here does not prove existence of that limit, Gaussian diffusion, a finite-time settling bound, or laboratory throughput after actuation overhead.

The corresponding simple upper bound is `kappa_Q<=epsilon^2 m0/eta`, from the odd Schur operator being at least eta. A sufficiently strong uniform dephaser gives a comparable positive absolute lower bound. Consequently A1/A2 do not establish the operational value or novelty of the spectral matching law by themselves.

## 4. New theorem B: a restricted uniform finite-hopping competitive ratio

Assume additionally that n is even, n>=6, and

`D=h sum_i (-1)^i n_i`, `Delta=2|h|>0`.

There are no density interactions. Every nearest-neighbour coherence has detuning magnitude Delta. Every symmetric independent-increment common-D phase law is characterized, for the relevant hopping coherences, by the single width

`gamma=eta+phi(Delta)>=eta`.

Its fixed-detuning kinetic current is exactly

`kappa_kin(gamma)=epsilon^2 m0 gamma/(gamma^2+Delta^2)`,

because every allowed kinetic hop has the same rate and the total signed exclusion drift vanishes configuration by configuration.

Define fixed odd/even trials

`f0=gamma J0/(gamma^2+Delta^2)`,

`g0=-A_D J0/(gamma^2+Delta^2)`,

and `y=epsilon(f0+g0)`.

They obey, exactly,

`S f0+A_D g0=J0`, `S g0+A_D f0=0`, `A_T f0=0`,

where `A_T=-i[T,.]`. Hence the complete residual is

`B y-J=epsilon^2 A_T g0`,

which is odd and has no populations. The corrected response functional from the N765 parity identity evaluates here to `kappa_kin(gamma)`.

For an odd normalized residual r, the exact identity

`kappa_Q-F=<r,R(I+S^(-1/2)AS^(-1/2))^(-1)r>`

is nonnegative: Rr=r and the real quadratic form of an accretive inverse is nonnegative. Its absolute value is at most `||r||^2` by the norm-one inverse bound. One can first use S+lambda and remove lambda; population balance makes the limit legal. Therefore

`0 <= kappa_Q(gamma)-kappa_kin(gamma) <= epsilon^4 ||A_T g0||^2_(#,S+)`. (B1)

The needed norm is explicit. In the fixed charge sector, Jordan–Wigner quadratic operators obey the traceless one-particle trace identity

`<dGamma(a),dGamma(b)>_# = alpha_n Tr(a b)/n`.

For this staggered model,

`[D,A_T A_D J0]=0`,

`||A_T A_D J0||^2_# = 8 Delta^2 t^4 alpha_n`.

The resulting operator consists of off-diagonal same-sublattice two-step terms. It is untouched by common-D phase noise and has baseline damping eta. The norm can be calculated from the one-particle cyclic shift or from `mean(sin^2 k cos^2 k)=1/8`; n>=6 avoids the special length-four aliases. Thus

`||A_T g0||^2_(#,S+) = 8 Delta^2 t^4 alpha_n/[eta(gamma^2+Delta^2)^2]`.

Combining with B1 proves

`1 <= kappa_Q(gamma)/kappa_kin(gamma)`

`  <= 1 + 4 epsilon^2 t^2 Delta^2/[eta gamma(gamma^2+Delta^2)]`

`  <= 1 + 4(epsilon t/eta)^2`.                                    (B2)

This is volume-uniform for this local current and all symmetric common-D phase laws, at finite nonzero hopping. It is not a full-channel estimate and does not contradict the product-observable obstruction.

Let `kappa_kin,*` be the edge-optimized kinetic benchmark. Every such phase controller has kinetic current <=kappa_kin,*. By B2 its actual current is <=`[1+4(epsilon t/eta)^2]kappa_kin,*`. By the source theorem and B1, the matched controller's actual current is >=`0.97 kappa_kin,*`. Hence

`kappa_Q,M >= [0.97/(1+4(epsilon t/eta)^2)] sup_phi kappa_Q,phi`.   (B3)

The supremum includes all symmetric independent-increment common-D phase laws with the same fixed coherent D, baseline eta, and hopping amplitude. It excludes coherent cancellation, changes to hopping, asymmetric coherent phase shifts, finite-memory non-Markovian drives, and arbitrary laboratory controls. Since a Gaussian phase law can realize any prescribed gamma>=eta at the one nonzero gap, this controller class is not artificially missing a single-width optimizer.

For example, epsilon*t/eta=.05 gives a proved ratio at least 97/101, approximately .960396. It is a comparison of current values, not algorithmic runtime or laboratory time. With the instantaneous finite pulse law, replace the numerator by `0.97(1-delta)`.

### 4.1 Exact Fourier closure and thermodynamic scope

The same restricted model has a direct quadratic-operator solution. Write allowed twisted one-particle momenta as `k_m=2 pi(m+s)/n`, with s=0 for K odd and s=1/2 for K even. In the `(k,k+pi)` block, T is proportional to `cos(k) sigma_z`, D to `h sigma_x`, and current to `sin(k) sigma_z`. The three relevant quadratic components have damping gamma, gamma, eta. The zero-frequency three-component inverse yields

`kappa_Q(gamma) = (alpha_n/n) sum_m 4 epsilon^2 t^2 sin^2(k_m)`

`  / [gamma + Delta^2/(gamma+16 epsilon^2 t^2 cos^2(k_m)/eta)]`.      (B4)

No population pole is divided out: the possible staggered-density mode has zero coupling after the odd-in-k current weighting. This closure can equivalently be checked directly in the real-space bilinear equations. It is an independent, explicit formula for this restricted class, not an interacting inverse algorithm.

As n->infinity with K/n->rho, B4 is a Riemann sum with a positive continuous denominator and alpha_n->rho(1-rho). Thus the restricted model's zero-frequency scalar has a thermodynamic limit, given by the corresponding integral. This establishes that scalar limit within this solvable class. It does not prove Gaussian hydrodynamics, identify a finite-temperature conductivity, or extend to interacting D.

## 5. Strong-hopping falsifier and surviving open problem

At fixed finite even n with no allowed momentum at cos(k)=0, B4 divided by epsilon^2 tends to `m0/gamma` as epsilon grows. Thus the baseline eta controller eventually beats a matched width gamma_M(Delta)>>eta by a factor approaching gamma_M/eta. Taking Delta/eta large defeats a 97% actual-current comparison at unrestricted hopping.

The saved formula diagnostic uses n=2048, K=1024 (antiperiodic one-particle twist), eta=1, Delta=100, epsilon*t=10000. It gives matched/baseline actual current about `0.008084749677`. This is a floating-point diagnostic of B4 and a strong-hopping counterexample scope, not a disproof of a perturbative current law at fixed small epsilon*t/eta. The analytic limit above supplies the general failure mechanism.

For genuinely interacting diagonal D, the kinetic optimizer generally needs configuration-dependent edge amplitudes and a nonlocal population corrector. Multiplying J0 by a local function of Delta does not generally preserve population balance. An explicit small diagnostic of nearest-neighbour interaction rates found nonzero configuration drift already at n=6 (configuration `001011`), so constant-corrector closure does not persist. That observation motivates an open gate; it is not a proof that no economical balanced corrector exists.

The unresolved consequential theorem is a constructive, volume-uniform bound on the complete S^+-weighted commutator residual of a sufficiently accurate **balanced kinetic current trial**, or an equivalent comparison tailored to actual local current. It must charge acquisition of the trial, Hodge corrections, local pulse and coherent errors, and total actuation time. Existing N764 exact feasibility repair and N775 small-word results do not supply its near-minimum-energy or rank/conditioning cost. The free-fermion/staggered theorem is a controlled solved subclass, not closure of this general gate.

## 6. Checks and interpretation

Two original producer scripts were inspected completely before execution in a scratch extraction. They read local data, use NumPy/SciPy/stdlib, write only their own local result JSON, and make no network or hardware calls. Both completed with one BLAS/OMP/Numba thread. The original ZIP and attachment were not executed or modified in place. The scratch source result JSON was overwritten by those replays, so provenance must hash the original ZIP's members, not assume the scratch replayed output equals original bytes.

Producer replay reproduced the stated exact scalar assertions, Lévy integrals, finite pulse cutoff, cancellation comparison, finite n=4/6 quantum solves, and analytic product-dimer numerical integration. Matched/oracle kinetic ratios were .986819854494 and .985370974511. At epsilon=.02 the actual/kinetic current ratios were **above one**, 1.000113171144 and 1.000063013775. The source states absolute discrepancies, so this sign is consistent; do not silently describe them as deficits. The million-dimer diagnostic is analytic scalar integration, not a million-dimer state-space simulation.

New `independent_current_checks.py` does not import the producer scripts. It independently constructs hard-core sectors and sparse Liouvillians. It checks 25 exact-integer bare-current commutator/norm cases (n=4,...,8, all nontrivial K), including exact staggered second-commutator identities on even n>=6. It then checks 30 finite floating cases: 12 genuinely interacting/disordered n=4,...,7 at epsilon=.05,.5,2 for theorem A, and 18 staggered n=6/8 cases for B1/B2 and the separate Fourier formula B4. Maximum normalized solve residual was `6.314975403902136e-15`. One-thread runtime observed was about 13.36 s. Numerical checks are not rigorous enclosures or universal proof; the written identities above bear the universal claim.

Saved files: `producer_checks_replay.json`, `producer_additional_replay.json`, `independent_current_checks.py`, `independent_current_results.json`, `independent_current_run.log`, and separate `SOURCE_ACCESS_AND_REPLAY.json`.

## 7. Existing capital and primary overlap

Read the current dossiers/notices/gates of N764/N765/N768/N773/N775 and the decisive N765 population-safe parity/error identities (`updates/EX/.../research_note.md`, lines62-224). N764's pressure/repair capital does not itself solve the actual current. N768 supplies an acquisition/decision context, not these phase-actuation hypotheses. N773's protected-probe result does not certify a reservoir. N775 explicitly refutes small source-word dimension implying small tensor rank. These distinctions survive this integration.

The variational inequality and residual-error identity are established linear algebra and already appear in N765; no invention of that general technique is asserted. The new scoped consequence is their combination with `[T,J0]=0`, the packet's pointwise spectral resistance guarantee, and the explicit second-commutator structure of the staggered subclass.

Live primary-source checks confirm substantial prior art:

- Maier et al., experimental noise-assisted excitation transport in a ten-qubit ion network and spectral-noise effects: https://arxiv.org/abs/1809.07680 . Abstract inspected; no claim of a first ENAQT mechanism.
- Uchiyama, Munro and Nemoto, spatial/temporal environmental correlation engineering: https://arxiv.org/html/1711.01025v2 . Full returned HTML inspected selectively around model and scope. This is prior engineering context, not the packet's universal ratio proof.
- Žnidarič and Horvat, noninteracting disordered XX/dephasing transport via closed quadratic equations: https://arxiv.org/html/1207.5952v2 . Model and closure equations8-11 inspected; exact noninteracting transport and specialized polynomial solvers predate this work.
- Jacob et al., dephasing-assisted tight-binding transport and optimized scalar dephasing in a linear potential: https://arxiv.org/html/2407.21715v2 . Exact small-size results and tridiagonal approximation scope inspected. The present staggered closure must be compared to this established analytical-design tradition.
- Ampelogiannis and Doyon, rigorous hydrodynamic diffusion bounds for open chains: https://arxiv.org/html/2501.07749v2 . Introduction/setup/main bound inspected. Their positive bound requires a spin-transporting dissipative contribution and uses distinct hydrodynamic/chaoticity assumptions; it is not an imported proof of pure-dephasing interacting transport here.
- Nachtergaele, Vershynina and Zagrebnov, time-dependent local Markovian Lieb–Robinson and thermodynamic-limit theory: https://arxiv.org/html/1103.1122v2 . Setup and assumptions inspected. The source's **averaged common noise is not automatically a sum of finite-range Lindblad terms**, so that theorem cannot be applied directly by topic association. A rotating-frame route dresses each hopping term by local commuting diagonal phases with unchanged norm and could supply pathwise locality, but the complete cadlag/infinite-jump and covariance limiting argument was not finished here and is NOT used to claim general interacting limit existence.

Historical originality of the performance/cost construction, theorem A/B, and obstruction remains UNKNOWN. These selective checks do not constitute a priority clearance or external proof review. This worker did not identify a validated material/control interface with useful-power gain after overheads and stronger native controls.
