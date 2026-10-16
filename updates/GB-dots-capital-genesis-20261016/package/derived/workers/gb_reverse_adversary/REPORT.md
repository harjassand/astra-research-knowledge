# Reverse-radius adversarial reconstruction and singular-support extension

2026-10-16. Authored internal mathematical audit. This is not external expert review, formal proof verification, a historical-priority determination, or an implemented experiment. Historical novelty remains **UNKNOWN**.

## Outcome

I found no contradiction in the supplied classical complete-SLD/MMSE erasure threshold, faithful-CQ harmonic-radius theorem, finite-reference Petz/RLD law, or specified qubit/Bell decision fixtures after reconstructing the arguments. This is a scoped internal reconstruction, rather than an approval of unrestricted extensions.

The substantive new output is a support-sensitive extension to singular CQ outputs, proved below. It yields complete threshold one for two distinct nonorthogonal pure outputs. Naively replacing every inverse by a Moore–Penrose inverse is false: an explicit pure-qubit pair gives the spurious value `-21/4` while the true threshold is one. A finite faithful qubit-reference MMSE witness is supplied.

Two further exact boundaries are useful. A small cyclic channel is completely dominated in MMSE by erasure with reveal probability `1/4`, yet beats that erasure experiment in binary guessing and cannot be simulated from it. Also, simultaneously commuting reference preparations collapse to the ordinary comparison; dimension and separability alone do not supply the complete-reference advantage.

The root calibration/payoff derivation survives an independent audit. The sharper approximate-physical-simulation bound communicated by the parent also survives, with the restricted Bell-family maximum requiring its parameter branch to be stated explicitly.

## Inputs, provenance, and task contract

Read-only Astra navigation was pinned to

`/Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016`

at Git revision `61389569d6c53b439764f0d148b35b7fa6083eec`. I read `00_START_HERE.txt`, `AGENTS.md`, and the current N405/N403 dossiers before using the historical concepts. These documents are navigation and evidence-status records, not proof premises.

The source packages were:

- `/Users/harjas/Downloads/Dots/Astra_reverse_radius_erasure_2026-10-15`
- `/Users/harjas/Downloads/Dots/Astra_qubit_reference_Bell_addendum_2026-10-15`
- `/Users/harjas/Downloads/Dots/Astra_quantum_reference_resource_2026-10-15 (1)`

The resource ZIP and its `(1)` ZIP have identical SHA-256 `ef59d761c341e8cece9fbf2477613e480a228725a71537e2dee8a8692ae6e245`. The two Bell ZIPs likewise have identical SHA-256 `aa0ac4ab2b2825b8441f56a893d70c59bc9a562abe3b0ec5e6033dabe655d85f`. Thus those named duplicates do not constitute independent mathematical variants. Exact source hashes are in `SOURCE_MANIFEST.json`.

No other worker's files were inspected. No source package or Astra checkout was edited. This worker wrote only this assigned evidence directory. Root files were inspected only after the parent explicitly requested their audit.

The channels measure a specified classical input alphabet and prepare classical or quantum outputs. The erasure probability convention is **reveal probability q**. References are untouched finite quantum systems. Unless specifically restricted, the optimization permits unequal reference marginals and arbitrary joint output/reference measurements. Standard Petz/RLD and SLD are distinct metrics. Mathematical witness existence does not acquire preparation, transport, calibration, measurement synthesis, drift, detection, energy, or statistical confidence resources.

## 1. Reconstruction of the supplied core arguments

### 1.1 Classical radius, including zero entries

For column-stochastic `T`, the free-center optimization is

`C(T) = min_u max_i sum_y (T_yi-u_y)^2/T_yi`,

with the support condition `u_y=0` whenever some column has `T_yi=0`. Equivalently, put `J={y:T_yi>0 for every i}` and optimize only on J. The dual is

`C(T)=1-min_p sum_(y in J) [sum_i p_i/T_yi]^-1`.

The minimax step is legitimate because the remaining quadratics are uniformly coercive. If J is empty the answer is one. The free center is not normalized; treating it as a probability vector changes the optimization.

For a faithful POVM `R_i`, the input-normalized zero-sum vector problem is equivalent to positivity of

`F_c(R)=c diag(A_y)-sum_i t_i t_i^T tensor R_i+[A_y A_z]_(y,z)`.

The certificate is the exact identity

`F_c(R)=sum_i [c diag(t_i)-(t_i-u)(t_i-u)^T] tensor R_i`

`          +(B-u^T tensor I)^*(B-u^T tensor I)`,

where `B=[A_1,...,A_n]`. The factor order is correct. This proves an all-reference upper bound; checking a scalar channel alone would not.

For the lower bound choose a strictly positive prior p, `s_i=sqrt(p_i)`, `P=I-ss*`, `v_i=P e_i`, `R_i=v_i v_i*`, and `z_i=s_i v_i` on `s^perp`. The input energy is one. The compressed diagonal Schur complement gives exactly the dual output energy, including the zero-row contribution. Faithful regularization is justified only on the supported inverse quadratic forms, rather than by pretending full inverses converge as matrices.

The same-dimension RLD Hermitian realization also works. With `H_i=h_i R_i`, the centered matrices are `Z_i=z_i w*`, where `w*=s*diag(h)P`. Consequently the trace ratio is the vector ratio. Subtracting a common scalar from h makes the total tangent trace zero without changing Z. This realization generally has a nonzero reference tangent K.

For positive T the active-prior bound gives a sufficient RLD reference dimension `min(m,n)-1`. The source correctly does not claim minimality, and does not transfer this bound to fixed-reference SLD.

### 1.2 Complete MMSE/SLD threshold and the flag cost

The normalized radius center w and signed compiler D obey `D E_q=T`. For each input the second-moment defect is a real PSD covariance matrix. Applying a real PSD factorization to arbitrary noncommuting reference observables produces a sum of squares of Hermitian operators. This is the needed complete step.

A POVM estimator is no better in squared loss than spectral measurement of its first-moment observable: its second moment dominates the square of that observable. The variational identity

`g_B(H)=sup_(A=A*) [2Tr(HA)-Tr(BA^2)]`

therefore gives the exact binary risk `1-t^2 g_B(H)` for normalized states `B±tH`, and the corresponding centered finite-second-moment ensemble formula.

For necessity, a vector RLD witness is converted using baseline `diag(R_i,delta a_i)` and off-diagonal tangent z_i. The exact input SLD cost is

`4 sum_i z_i*(R_i+delta a_i I)^-1 z_i`.

At the target it converges to four times the vector output cost. Strict slack is selected first; a finite positive delta is then selected; a nonzero perturbation t is finally selected by the Schur condition. This establishes ordinary, unsmoothed physical binary witnesses. It adds **one reference dimension**, not a free transformation inside the original reference space. No interchange of delta and the positivity perturbation is needed.

Thus complete RLD and complete SLD/MMSE erasure thresholds agree, although ordinary RLD and ordinary SLD may disagree and their fixed-r coefficients are not equated.

### 1.3 Faithful CQ radius

For faithful prepared outputs sigma_i, weighted matrix Cauchy applies to

`A_i=sigma_i tensor R_i`, `B_i=(sigma_i-U) tensor Z_i`.

Taking the output partial trace gives the upper coefficient `max_i f_i(U)`, with

`f_i(U)=1-2Tr U+Tr(U sigma_i^-1 U)`.

The minimax stationarity equation is `M_p U+U M_p=2I`, solved by `U=M_p^-1`, where `M_p=sum_i p_i sigma_i^-1`. The noncommuting harmonic formula follows without interchanging scalar and operator inverses.

The lower witness is the compression of `direct_sum_i sigma_i` to `s^perp tensor C^d`. Its Schur complement gives `sum_i p_i sigma_i-M_p^-1`. The same common-row Hermitian realization proves trace sharpness with no added RLD flag. The sufficient bound `min(m,d^2)-1` follows from an exposed-face Caratheodory argument in the d^2-dimensional Hermitian inverse space. The separate SLD conversion has sufficient bound `min(m,d^2)`.

The quantum-output observable compiler's purification orientation is correct: use `v=vec(sqrt(sigma))` and `w=vec((omega-sigma)sigma^-1/2)`. Then `sqrt(sigma) w_matrix^*=omega-sigma`; this is the factor order needed for noncommuting states.

### 1.4 The finite-reference resource law

For a rank-r projection P and a unit x in its kernel, define block masses p_i and directional diagonal q_i. Then `sum p_i=1`, `sum q_i<=r`, and `q_i<=1-p_i`. The identity

`r^2 p+q-(r+1)^2 pq = (rp-q)^2+(1-p-q)(r^2p+q)`

proves the pinched compression bound `r/(r+1)`. The resulting zero-sum inverse inequality combines with the alphabet bound and spectral Jensen to give

`eta_(m,r)(lambda)=lambda^2/[lambda+((1-lambda)/m)(k+1)/k]`,

`k=min(r,m-1)`.

The Hermitian regular-simplex construction reaches the trace ratio in closure, and an operator inequality precedes whitening reversal and taking trace. Thus the proof does not incorrectly assume scalar ratios are invariant under congruence. The endpoints lambda=0,1 are handled separately.

This is a standard-Petz/RLD conditional-excess result. It proves neither an SLD finite-memory law nor the same law under an added equal-reference-marginal constraint. The supplied lower witness usually has K nonzero. This fact alone does not prove that unequal marginals are mathematically necessary for every possible sharp witness.

## 2. Singular-CQ extension: exact theorem and proof

### 2.1 Statement

Let sigma_i be arbitrary finite-dimensional PSD density matrices. First restrict the output to `S=span_i supp(sigma_i)`, so `sum_i sigma_i>0` there. Define

`L=intersection_i supp(sigma_i)` and let P_L be its projection.

If L is nonzero, put

`Q_i=(P_L sigma_i^+ P_L)|_L >0`,

`h=min_(p in Delta_m) Tr_L[(sum_i p_i Q_i)^-1]`.

If L is zero, set h=0. Then the complete conditional standard-Petz/RLD coefficient and the complete ordinary SLD/binary-MMSE erasure threshold both equal

`C=1-h`.

In particular, C=1 **if and only if** L=0: when L is nonzero the finitely many positive Q_i have a uniform finite upper bound, so their inverse-harmonic trace has a strictly positive minimum.

The coefficient is also

`min_(U=U*, U=P_L U P_L) max_i [1-2Tr U+Tr(U sigma_i^+ U)]`.

For a nonconstant m-input family, reference dimension m-1 suffices in the RLD supremum; m suffices for a strict SLD/MMSE counterexample below threshold. These are sufficient bounds. No improved active-support bound is claimed for singular outputs.

All input states in the physical comparison may be faithful. Quantum outputs and SLD/RLD quantities are interpreted on the fixed union support S. This support does not depend on the faithful input baseline.

### 2.2 Upper bound and minimax

For U supported on L, `sigma_i-U` has range in `supp(sigma_i)`. Therefore generalized weighted Cauchy applies with `A_i=sigma_i tensor R_i` and `B_i=(sigma_i-U) tensor Z_i`: each B_i has range in A_i. It gives the same operator-valued conditional bound as in the faithful case, with sigma_i^+ in the cost. The formula expands to `1-2Tr U+Tr(U sigma_i^+ U)` because both left and right support projections act as identity on U.

On Herm(L), the quadratics are uniformly coercive since every Q_i is strictly positive. Convex minimax and the Lyapunov stationarity equation give `U=(sum_i p_i Q_i)^-1` and value `1-Tr_L U`. If L=0, only U=0 is allowed and the upper bound is one. This avoids giving an unsupported pseudoinverse cost to a center outside a prepared output's range.

### 2.3 Supported harmonic limit

Fix **strictly positive** p first. Write

`M_epsilon=sum_i p_i (sigma_i+epsilon I_S)^-1`.

Relative to `S=L direct_sum L^perp`, the L block converges to `M_L=sum_i p_i Q_i`, while the off-diagonal blocks stay bounded. The L^perp block is

`epsilon^-1 G+O(1)`, `G=sum_i p_i P_(ker sigma_i)|_(L^perp)>0`.

Indeed a vector annihilated by G lies in every support, hence in L; its intersection with L^perp is zero. The inverse of this divergent block is O(epsilon). Its Schur complement on L therefore tends to M_L. Consequently

`M_epsilon^-1 -> P_L M_L^-1 P_L`.

For L=0 the inverse tends to zero. This is a matrix limit after the common-support decomposition; it is not the substitution `(sigma_i+epsilon I)^-1 -> sigma_i^+`.

### 2.4 Matching lower witness and correct limiting order

Use the weighted-simplex frame from Section 1 with positive p. Apply the ordinary block Schur identity to `D_epsilon=direct_sum_i(sigma_i+epsilon I_S)`. Its compressed lower block is `A_epsilon=A_0+epsilon I_(s^perp tensor S)`. The off-diagonal block W is unchanged because `sum_i z_i=0`.

Positivity of the unregularized block matrix implies `range W subset range A_0`. Thus

`Tr(W* A_epsilon^-1 W) -> Tr(W* A_0^+ W)`.

The Schur identity and Section 2.3 give this limit as

`1-Tr_L M_L^-1`.

The input frame energy is one. The common-row Hermitian realization gives the same physical RLD trace ratio. Its physical H_i and output tangent are supported in the original baselines. Now regularize the **input** frame to faithful `R_i(eta)=(R_i^0+eta I)/(1+m eta)` while keeping H_i fixed. Supported inverse input costs converge. For the target, the perturbation is a strictly positive matrix proportional to `(sum_i sigma_i) tensor I`; compression to range A_0 and a block Schur complement again prove convergence of the supported quadratic costs. Matrix inverses on the entire space need not converge.

Finally approximate an optimal boundary p by strictly positive priors. On the fixed space L, every Q_i has a uniform positive spectral floor, so `Tr_L[(sum p_i Q_i)^-1]` is continuous on the closed simplex. This supplies sharpness at the displayed minimum without changing L at boundary p. The order is: positive p; supported output limit; faithful input approximation; then boundary-prior approximation and a small physical tangent.

### 2.5 Complete SLD/MMSE equality survives singular outputs

If L is nonzero, the normalized density center omega lies in L. The purification variance proof still works with `sigma_i^+` and `sigma_i^{+1/2}`, since both omega and `omega-sigma_i` are supported in sigma_i. The signed-observable sufficiency argument is unchanged. If L=0, q=1 plainly simulates the CQ preparation.

For q<C, select a strict faithful-input vector witness using Section 2.4. Its output baseline `A=sum_i sigma_i tensor R_i` is strictly positive on `S tensor C^r`: every R_i has a positive lower bound, and `sum_i sigma_i>0` on S. Similarly `sigma_a=sum_i a_i sigma_i>0` for positive a_i. Add one small coherent reference flag. The target off-diagonal SLD block solves

`A X_delta+delta X_delta sigma_a=2B`.

The Sylvester inverse converges continuously to left multiplication by A^-1 because A is strictly positive. Hence target SLD cost tends to `4Tr B*A^-1 B`, while input cost tends to four times its vector energy. Strict slack persists at finite delta>0. The Schur condition then admits a small nonzero t, giving faithful normalized binary input states with **equal reference marginals** and an exact MMSE reversal. No singular-input or infinite-dimensional experiment is used.

### 2.6 Exact countermodels and finite witness

Let `sigma_0=|0><0|` and `sigma_1=|v><v|`, `v=(3/5,4/5)`. Their supports are distinct lines, so L=0 and C=1. At p=(1/2,1/2), the incorrect uncompressed pseudoinverse recipe gives

`1-Tr[((sigma_0^++sigma_1^+)/2)^-1]=-21/4`.

This is an explicit failure of that proposed generalization, rather than a defect in the supplied faithful theorem.

For a nonzero-common-support example, take

`sigma_0=diag(1/2,1/2,0)`, `sigma_1=diag(1/4,0,3/4)`.

Then L=span(e_0), `Q_0=2`, `Q_1=4`, and C=3/4. At half prior the harmonic trace limit is 1/3. The optimal common-support dual is at boundary prior `(0,1)`, but deleting the first symbol would change the channel to a constant channel with coefficient zero. Therefore the faithful-output active-support argument cannot be transferred by simply replacing d with dim L. Positive-prior approximation pays for the rare symbol.

A fully finite singular-output SLD witness uses pure qubit preparations

`sigma_±=[I+(Z±X)/sqrt(2)]/2`,

and reference conditional states

`tau_(theta,i)=[[1,theta i/5],[theta i/5,1/16]]/(1+1/16)`.

Draw i independently and uniformly. These are faithful because `1/16-1/25>0`; both label-conditioned reference marginals agree. At q=3/4, Bell spectral measurement is exactly optimal and the target MMSE advantage is

`24832/2550425 > 0`.

The output preparation states are singular, but the actual binary experiment's average output is faithful on the full two-qubit space. The exact SLD equation and physical positivity are checked in `check_exact.py`.

## 3. Exact limits of generalization

### 3.1 Complete MMSE is not guessing order or simulation

Use the supplied nonsymmetric cyclic channel

`T=[[1/2,1/6,1/3],[1/3,1/2,1/6],[1/6,1/3,1/2]]`.

Its complete MMSE threshold is 2/11. Thus E_(1/4) dominates it in every complete squared-MMSE experiment. For the equiprobable labels encoded as input symbols 1 and 2, however,

`p_guess(T)=2/3 > 5/8=p_guess(E_(1/4))`.

The optimal squared risks for that same ensemble are `157/180` for T and `3/4` for erasure. Both orderings can hold because posterior magnitudes matter to squared loss.

The exact stochastic erasure-simulation threshold is

`q_sim=1-sum_y min_i T_yi=1/2`.

Proof: the common erase-output distribution must have mass `(1-q)w_y<=min_i T_yi`; summing gives necessity, and normalizing any available common mass gives sufficiency. At q=1/4 the signed compiler has entries as low as -1/3. It compiles observables but cannot prepare distributions. This furnishes concrete counterexamples to both overextensions.

### 3.2 Commuting reference blocks give no complete advantage

Suppose all label/input conditional reference matrices are simultaneously diagonalizable in one basis, so the reference is a classical variable s. The receiver can read s without disturbance. The target and source risks both decompose as a weighted sum of conditional ordinary experiments indexed by s. An ordinary channel-order inequality holds on every such conditional ensemble and hence after summation. Conversely a one-dimensional reference is included. Therefore the threshold with arbitrary **classical** references equals the ordinary threshold.

The Pauli example's reference advantage consequently requires noncommuting conditional reference preparation. Its input is nevertheless separable across the classical/quantum cut; entanglement and noncommutativity are different resources. This theorem does not claim that every particular joint measurement must be entangled or that every noisy reference retains a useful advantage.

### 3.3 Bell fixture and finite resource accounting

The analytic two-input Bell fixture is correctly separate from the three-axis family. For preferred `a=9/10`, ordinary SLD threshold is `81/200`, complete threshold `81/119`, and `q=9/20`. The finite encoding uses a reference qubit and a four-dimensional joint target receiver. Exact reconstruction gives

`MMSE_source=524/605`, `MMSE_target=14723/17639`,

`Delta=335421/10671595`.

The rational three-input qubit fixture's unequal reference marginals are real, and its erased-reference SLD cost must be retained. Reconstructing its source optimum and fixed rational receiver gives the stated gap approximately 0.005216075051827943, strictly above 1/200. The reference explained variance is the nonzero exact fraction `43227124794193/892341237500000`.

These are achieved ideal decision risks, not global encoding optima. The Bell basis is a joint analyzer; the proof does not mandate a two-photon entangling gate. Local X measurements already optimize 0–1 label guessing in the rotated Bell example, so the MMSE gain must not be described as a demonstrated advantage of entangled measurement for guessing. A full physical protocol still needs the specified mixed states, hidden preparation randomness, untouched reference, calibrated scores, all loss events, and independent evaluation.

The claimed sufficient IID evaluation counts are conditional on fixed calibrated preparation and receivers. They do not include calibration samples or establish actual risk confidence bounds. Package replay confirms their exact arithmetic; it does not acquire their physical premises.

## 4. Independent audit of root stability and payoff claims

I read the root `ROBUST_RADIUS_AND_PAYOFF.md` and executed its `check_radius_crossover.py` after the parent requested this audit. No fault was found in the stated faithful-output contract.

Relative Loewner calibration `(1-epsilon)sigma_i<=tau_i<=(1+epsilon)sigma_i` reverses under inversion, is preserved by a common-prior sum, reverses again, and is preserved by trace. The pointwise inequalities survive minimization over the same prior simplex. Thus `|C(tau)-C(sigma)|<=epsilon(1-C(sigma))`. An operator-norm ball of radius delta around states bounded below by lambda I gives epsilon=delta/lambda when delta<lambda. This is uncertainty propagation conditional on membership, not a confidence-region acquisition method.

For the two-state family with Bloch vectors `(±r sin(theta),0,r cos(theta))`, symmetry and convexity give the half-prior harmonic minimum. Direct inversion yields complete threshold

`r^2 sin(theta)^2/[1-r^2 cos(theta)^2]`.

The full ordinary SLD ratio at binary prior coordinate z is `B A(1-z^2)/(A-Bz^2)`, with `A=1-r^2 cos(theta)^2`, `B=r^2 sin(theta)^2`. Its derivative in z^2 is negative for r<1, so ordinary threshold is B. At r=1 and theta>0, mixtures with interior prior are faithful on the two-dimensional union support; substituting into that **mixture** calculation gives ratio B directly. This provides the endpoint argument without incorrectly inverting an individual pure state.

The root's uniform bounded-loss payoff bound is correct: preparation distance to the common-average replacement channel is `r sin(theta)/2`, uniformly after arbitrary reference assistance. Clipped binary squared loss changes by at most four times that trace distance. Erasure can ignore its revealed symbol and reproduce the reference-only replacement experiment. Thus its risk advantage is at most `2r sin(theta)`.

The parent subsequently asked me to audit a sharper simulator for pure outputs with Bloch vectors `(±a,0,b)`, `a^2+b^2=1`, b>=0. Set

`L=sqrt[q^2+2(1-q)(1-b)]`.

Prepare north pole on erase and unit Bloch vector `(±a,0,b-1+q)/L` on reveal. Its output Bloch error is exactly `(1-q/L)(±a,0,b-1+q)`, so its trace-norm error is `L-q`. Tensoring with positive reference blocks and summing preserves this worst-case bound. Any clipped binary-MMSE advantage is consequently at most

`2(L-q)=4(1-q)(1-b)/(L+q)=O(a^2)`

for fixed q>0 as a tends to zero. The source can physically implement this approximate output, so this is an all-encoding upper bound.

The restricted Bell family's boundary-encoding payoff is

`(1-x)[a^2/(1-(1-a^2)x)-q]`, `0<=x<=1`.

Its stationary maximum equals `a^2/(1-a^2)(1-sqrt(q))^2` only for `0<a<1` and `a^4<=q<=1`. This condition is automatic in the intended ordinary-dominance region q>=a^2. If q<a^4 the family maximum is the endpoint value `a^2-q`. Pure orthogonal outputs a=1 require a separate endpoint. The family supremum is not a global optimum; it and the simulator upper bound establish matched a^2 scaling for each fixed `0<q<1` as a tends to zero. The q=1 payoff is zero. Approaching the Bell supremum uses increasingly rank-deficient preparations, so this scaling does not imply a uniform conditioning, calibration, or hardware cost.

## 5. Independently checked primary antecedents

Primary sources were browsed on 2026-10-16. The following observations delimit components, not historical priority of the assembled theorem.

- [Hirche, Quantum estimation, channel orders, and private capacity, arXiv:2610.03706v1](https://arxiv.org/html/2610.03706): Section 2.1 gives binary MMSE/SLD/measured-chi-square relations; Definition 3.1 states reference-complete signed variance domination; Appendix A treats a Hermitian-smoothed converse. Its separately named quantum chi-square is BKM. This supports attribution of the dictionary and general compiler framework, not automatic identification with ordinary RLD or a fixed-memory theorem.
- [Zhu–Wang, Quantum Incapacity beyond No-Cloning and PPT Mechanisms, arXiv:2607.24693v2](https://arxiv.org/html/2607.24693v2): Definition 3.3 and Proposition 3.4 supply signed lifts and CP-defect certificates. The text distinguishes observable reconstruction from POVM simulation. These are established components of the supplied compiler interpretation.
- [Hirche–George–Nuradha–Wilde, Conditional contraction coefficients and their applications to quantum networks, arXiv:2608.27171v1](https://arxiv.org/html/2608.27171v1): Section 2 explicitly develops conditional reference-subtracted coefficients and separates them from other complete conventions. The subtraction and marginal contract must be matched before importing a result.
- [Gu–Polyanskiy, Non-linear Log-Sobolev Inequalities for the Potts Semigroup and Applications to Reconstruction Problems](https://people.lids.mit.edu/yp/homepage/data/nlsi_potts.pdf): Appendix A, Proposition 40, Eq. (231), states the ordinary symmetric-channel coefficient `m lambda^2/[2+(m-2)lambda]`. That scalar comparator is prior work.
- [Ordentlich–Polyanskiy, Strong Data Processing Constant Is Achieved by Binary Inputs](https://arxiv.org/abs/2010.01987): establishes ordinary binary-input reduction. It does not by itself supply the arbitrary quantum-reference coefficient.
- [Jeong–Kim, Barycenter of the arithmetic-harmonic quantum divergence](https://journals.uwyo.edu/index.php/ela/article/download/8883/6985): the binary trace arithmetic-minus-harmonic objective already appears explicitly. Thus the harmonic matrix expression is not a new invented divergence.
- [Mosonyi–Bunth–Vrana, Geometric relative entropies and barycentric Renyi divergences](https://arxiv.org/html/2207.14282): provides left/right weighted quantum-radius context, including support conventions. This is component-level precedent rather than a verified predecessor of the complete conditional coefficient formula.
- [Kim, Single-photon two-qubit entangled states: preparation and measurement](https://arxiv.org/abs/quant-ph/0303125): an established architecture reference. It does not certify the supplied mixed-state preparations, task-specific calibrated receiver, or risk gap.

Targeted searches for complete classical/harmonic-radius coefficients and the rank-sensitive projection lemma did not locate a decisive predecessor. Search non-discovery is not an absence theorem; priority of both the supplied identification and this singular extension stays UNKNOWN.

## 6. Exact tests and their boundaries

`check_exact.py` is authored independently, imports no package executable, uses SymPy exact arithmetic, and emits `exact_results.json`. It checks:

1. Cyclic primal/dual equality 2/11; signed compiler reconstruction and PSD second moments; opposite guessing and MMSE orderings; simulation threshold 1/2.
2. Faithful noncommuting Pauli radius 3/11 and the same-reference-dimension supported RLD physical witness with input excess 2/3 and output excess 2/11.
3. The pure-pair pseudoinverse countermodel and the correct supported harmonic limit.
4. A rank-two/rank-two singular qutrit family with one-dimensional common support, including its boundary-prior warning.
5. The full four-dimensional Bell SLD equation, Bell eigenvectors, faithful preparation, and exact preferred risks.
6. A finite faithful qubit-reference witness for singular outputs, equal reference marginals, q=3/4, and gap 24832/2550425.
7. The rational three-input fixture's source optimum, erased-reference term, fixed target risk, exact gap, and state eigenvalue margins by principal minors.
8. The projection scalar identity and the resource-law benchmark 4/11.
9. The sharper simulator's exact Bloch error identity and the Bell restricted-family stationary expression and branch condition.

The three original package runners were also replayed without editing their source. Their logs are `producer_reverse.log`, `producer_bell.log`, and `producer_resource.log`. All completed successfully. Root's three-check crossover script also passed. Producer replay is corroborating arithmetic, not an independent proof of universal quantifiers. No random optimizer output is used as a certificate.

The exact tests do not mechanically verify the general theorem, establish external review, novelty, polynomial exact bit complexity, global encoding optimality, or actual physical calibration. The proofs above carry the universal claims, and the stated input/measurement/support/marginal costs remain part of those claims.
