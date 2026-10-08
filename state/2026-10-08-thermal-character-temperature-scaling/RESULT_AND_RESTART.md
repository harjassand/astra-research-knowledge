# Spin-character concentration, near-unit full-separability distance, and the sqrt(N) occupation exponent

Checkpoint: 2026-10-08 Brisbane. **Internally derived proof candidate with explicit algebra and finite independent numerical identity checks; no external expert review, formal verification, experimental validation or priority certification.** A self-contained argument is supplied below; the stationary collective model and the earlier angular anti-concentration strategy are inherited. No assertion that this is an already-recognized open-problem resolution.

## I. Model / inherited context / novelty scope
Let N spin-1/2 qubits with J_a=(1/2) sum_i sigma_i^a, J_±=J_x±i J_y. Consider the ideal collective finite-temperature Lindbladian with terms (nu+1)D[J_-]+nu D[J_+], started in I/2^N. Irrep decomposition V_j (spin j) with multiplicity m_{N,j}, and weights w_{N,j}=(2j+1)m_{N,j}/2^N. The stationary state is exactly
rho_(N,nu)= direct_sum_j w_(N,j) (rho_(j,beta) tensor I_(m_j)/m_j),
rho_(j,beta)=exp(-beta J_z^(j))/Z_j(beta),
beta=log(1+1/nu) for nu>0, beta=infty for nu=0. The sector weights are conserved from the fully mixed input.
This description is the model-level input inherited from Astra N120/N130 and standard collective-spin representation theory; cf. Li-Xu https://arxiv.org/abs/quant-ph/0505216 for earlier two-spin collective-thermal entanglement. The source N131 supplies a weaker full-separability distance convergence rate O(N^-1/6 (log N)^(2/3)) via second moments and angular anti-concentration, and has not been externally priority-reviewed. Here its separable-product inequality is rederived independently below. New candidate content: exact spin-character subGaussian lemma, a nonasymptotic target tail, improved N^-1/4 logarithmic distance rate, and a **sharp polynomial occupation exponent 1/2** separating distance-to-full-SEP limits 1 and 0. Exact critical-window behavior nu=c sqrt(N) remains open.

## II. Exact spin-character concentration lemma (full proof)
For spin j>=0 define chi_j(z)=sum_(m=-j)^j exp(z m)=sinh((2j+1)z/2)/sinh(z/2), with continuous value at zero.
For t real and beta>0 let
  eta(t)=2 arcosh(cosh(beta/2) cosh(t/2)).
Using the spin-j character of the SL(2,C) element exp(-beta sigma_z/2) exp(t sigma_x/2) with fundamental eigenvalues exp(±eta/2), we get the exact identity
  M_j(t):=Tr[rho_(j,beta) exp(t J_x)] = chi_j(eta(t))/chi_j(beta).
The ket expectation is a positive trace, not a classical independence assumption.
Since eta>=beta and chi_j(z)=exp(j z) sum_(k=0)^(2j) exp(-k z), the latter sum decreases with z, and
  M_j(t) <= exp[j(eta(t)-beta)].
For t>=0 put C=cosh(beta/2), S=sinh(beta/2). Differentiating cosh(eta/2)=C cosh(t/2),
  eta'(t)=C sinh(t/2)/sinh(eta(t)/2).
Since sinh(eta/2)^2=C^2 cosh(t/2)^2-1 >= S^2 cosh(t/2)^2, we have
  eta'(t)<=coth(beta/2) tanh(t/2)<=coth(beta/2)*t/2.
Integrate from 0 to t (eta(0)=beta), and use evenness to obtain
  eta(t)-beta <= coth(beta/2) t^2/4.
Let c_nu=coth(beta/2)=2nu+1. Thus for ALL real t,
  **M_j(t) <= exp(j c_nu t^2/4).**
The nu=0 formula holds as beta->infty: rho_j=|j,-j><j,-j|, M_j(t)=cosh(t/2)^(2j)<=exp(j t^2/4).
Z-axis covariance gives the same MGF for any J_theta=J_x cos(theta)+J_y sin(theta).
Chernoff for j>0 (and trivially j=0) gives
  Pr_{rho_j}(|J_theta| >= w) <= 2 exp[-w^2/(j c_nu)].
This is a uniform subGaussian tail in each spin irrep with variance proxy j c_nu/2.

## III. Irrep-tail lemma (full proof)
Under I/2^N, the outcome m of J_z conditioned on j is uniformly distributed over -j,...,j. For any real R>=1, if j>=R, at most R+1 of the 2j+1 values have |m|<R/2. Therefore
  Pr(|m| >=R/2 | j>=R) >= R/(2R+1)>=1/3.
But J_z=(1/2)sum_i epsilon_i on I/2^N with independent epsilon_i in {±1}, so Hoeffding gives
  Pr(|J_z|>=R/2) <= 2 exp[-R^2/(2N)].
It follows, with sector weights unchanged under the collective dynamics, that
  **Pr(j>=R) <= 6 exp[-R^2/(2N)].**
Consequently, for any R>=1,w>=0 and every theta, splitting sectors at R,
  **Pr_{rho_(N,nu)}(|J_theta|>=w) <=6 exp[-R^2/(2N)]+2 exp[-w^2/(R c_nu)].**
This is a sub-Weibull-4/3 type global tail at transverse fluctuation scale N^1/4 for fixed nu, and remains quantitative when nu grows with N.

## IV. Fully separable angular anti-concentration (independent reconstruction)
Measure each qubit along common independently random theta, n_theta=(cos theta,sin theta,0), and accept if |J_theta|<=w. Fix an arbitrary product state, pure or mixed. The measured local outcomes are independent ±1/2 with variances v_i(theta)=[1-(r_i dot n_theta)^2]/4, where |r_i|<=1. Let V_theta=sum_i v_i(theta).
Fourier inversion and 1-x<=exp(-x) give the largest lattice atom <=(2pi)^(-1) int_(-pi)^pi exp[-2V_theta sin²(t/2)]dt. Since sin(|t|/2)>=|t|/pi, this is <=sqrt(pi/(8V_theta)); interpret the bound as trivial at V_theta=0.
An interval of radius w contains at most 2(w+1) lattice atoms, so product acceptance <=min(1, sqrt(pi/2)(w+1)/sqrt(V_theta)).
The 2-by-2 planar covariance is V_theta=(N-n_theta^T S n_theta)/4 with S=sum r_i^(xy)(r_i^(xy))^T, tr(S)<=N. One of its eigenvalues is >=N/8, hence for some theta_0,
  V_theta >= (N/8)sin²(theta-theta_0).
Let a=2 sqrt(pi)(w+1)/sqrt(N). Uniform theta over [0,pi) gives acceptance <=
  B(a)=1 if a>=1,
  B(a)=(2/pi)[arcsin(a)+a log((1+sqrt(1-a²))/a)] if 0<a<1.
Convexity extends the bound to EVERY fully separable state, including arbitrary mixtures; no permutation-symmetry premise.
The thermal target is rotationally invariant about z, and has <J_theta>=0, so the sector-tail bound of III is its rejection bound.
Trace-distance data processing applied to the one-shot LOCAL measurement distinguishes target from SEP_N:
  **D(rho_(N,nu),SEP_N) >=1-6 exp[-R²/(2N)]-2 exp[-w²/(R c_nu)]-B(a).**
D is half the trace norm. The RHS may be negative for small N (then the statement is vacuous).

For any T>0 with R=sqrt(2NT)>=1, choose w=sqrt(R c_nu T), a=2 sqrt(pi)(w+1)/sqrt(N). Then
  **D >=1-8 exp(-T)-B(a).**
Take T=log N for fixed nu to obtain
  **D >=1-O_nu(N^(-1/4) (log N)^(7/4)).**
This sharpens N131's Chebyshev N^-1/6 rate. It is an explicit candidate bound, NOT a confirmed historical novelty claim.
A uniform grid of L axes preserves the target bound and changes the separable average by at most O(1/L), since theta->min(1,a/|sin(theta-theta0)|) has bounded total variation on [0,pi]. Even the conservative 4/L from N131 suffices. Per experimental shot: random log L-bit axis, N calibrated single-qubit measurements and classical counting. No global tomography or nonlocal joint measurement. Add instrument noise to the acceptance radius and pay its calibration cost.

## V. The matching high-occupation upper bound (full proof)
At beta=0 (equivalently nu=infinity), the state is I/2^N and fully separable. For each j, write the Gibbs distribution p_beta(m)=exp(-beta m)/Z_j(beta) over m=-j,...,j; p_0 is uniform. Then
  partial_beta p_beta(m)=-(m-E_beta m)p_beta(m).
Therefore its total-variation speed is
  (1/2) sum_m |partial_beta p_beta(m)| = (1/2) E_beta |m-E_beta m|
  <=(1/2) sqrt(Var_beta m) <= j/2.
Integrate beta from 0 to the requested value. By block-orthogonality and fixed weights w_(N,j),
  D(rho_(N,nu),I/2^N)<= (beta/2) sum_j w_(N,j) j.
Using sum_j w_(N,j) j(j+1)=Tr[(I/2^N)J²]=3N/4 and Cauchy-Schwarz,
  **D(rho_(N,nu),SEP_N) <= (sqrt(3N)/4) log(1+1/nu)** for nu>0.
This is a genuine finite-N upper bound on distance to FULL separability (not an equality), and it needs no N130 singleton threshold.

## VI. Sharp exponent and practical interpretation
Let nu_N=N^alpha (or asymptotically comparable powers):
- If alpha<1/2, c_nu=O(1+N^alpha) and the lower error is O(N^(-1/4+max(alpha,0)/2) (log N)^(7/4)); hence **D->1**.
- If alpha>1/2, upper bound <=O(N^(1/2-alpha)); hence **D->0**.
- At alpha=1/2, the methods do not establish a constant threshold or limiting D. It is mathematically inappropriate to label it a fully solved thermodynamic phase diagram.
More general sufficient limits: nu_N=o(sqrt(N)/(log N)^(7/2)) gives D->1; nu_N/ sqrt(N)->infty gives D->0. These leave a logarithmic critical window.
For fixed nu, the witness can distinguish target from EVERY fully separable state with one randomized local-measurement run and total type-I+type-II error tending to zero (asymptotic mathematical statement). An actual device requires preparation fidelity, calibrated identical common axes, readout noise control, finite N, realistic bath and post-preparation noise; no hardware result is claimed.
If the *separately unreviewed* N130 singleton-separability/PPT theorem remains valid, the alpha<1/2 regime yields a stronger global-versus-singleton entanglement contrast even for diverging bath occupations. This does NOT establish nondistillability across arbitrary grouped bipartitions.

## VII. Verification, limitations, next attack
Independent numerical check: scipy dense spin-j matrices for j=1/2,1,...,8; nu in {0.01,0.2,1,5}; t in {-1.5,-0.7,-0.2,0,0.2,0.7,1.5}: 448 instances. Trace-character ratio error <=4.83e-13 (relative); maximal MGF-bound excess 2.23e-16, at floating-point tolerance. See companion verify_spin_character.py and spin_character_checks.json. This validates algebra on finite cases, not a proof; the proof is Section II.
Other supporting literature: classical collective dissipation Li-Xu https://arxiv.org/abs/quant-ph/0505216; recent different strong-SU(2)-symmetry entanglement transitions Mo-Altman-Garratt https://arxiv.org/abs/2610.00826; high-temperature separability for LOCAL Hamiltonian Gibbs states Bakshi-Liu-Moitra-Tang https://arxiv.org/abs/2403.16850 is *not* directly this nonlocal sector-preserving Lindbladian.
Strong priority check still needed: search representation-theoretic concentration inequalities, spin squeezing anti-concentration, de Finetti sector ensembles and large-N thermal collective radiation. Search did not establish originality. Have independent specialist check exact measurement/sector assumptions and the finite grid constants. The finite-size bound can be weak/trivial for moderate N due constants.
Next higher-value question: resolve nu=c sqrt(N) by asymptotics of irrep weights and separable-state approximation; seek nontrivial limiting D(c) or a sharp constant threshold. Try improving the angular witness logarithm and finite-N constants. Then establish time-to-stationarity, noise robustness, and any singleton PPT claim with separately audited N120/N130/N133 inputs. No assertion of a globally field-breaking theorem yet.

End checkpoint.
