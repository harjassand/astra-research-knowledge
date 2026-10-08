# Audit update and preparation-time escalation

8 October 2026. Read this BEFORE RESULT_AND_RESTART.md. Status: internally derived candidate mathematics, not external peer review, proof-assistant certification, or priority clearance. No independent subagents were available.

This file supersedes the old checkpoint's execution counts, hashes, missing-code reference, and unresolved preparation-time statement. The earlier stationary-state and anti-concentration arguments remain candidate proofs. Current portable exact code: certify_finite_time.py in this directory.

## 1. Prior-art and prior-capital corrections

Li and Xu, arXiv:quant-ph/0505216v2, already give the SAME collective thermal generator, stationary two-qubit formulas, and threshold nu_*=(sqrt(15)-3)/6. See Eq. (1), Eqs. (10)-(11), and p. 3, including their explicitly discussed initially maximally mixed case r=0. Their symbol N is bath occupation, not our number of qubits. Submitted 2005; International Journal of Quantum Information 6,1165 (2008). The numerical constant and basic bath-induced entanglement are NOT new.

A final repository refresh found AA/N120, cards/N120-thermal-depth-two.txt, blob 4eddcc744a068d497456b4ad166bae33801864e3. It already records ideal thermal activation, a finite-time entanglement bound via a reflecting-chain spectral-gap comparison, stationary pair decompositions, and a stronger source-reported all-time depth-two result. Thus neither basic finite-time thermal entanglement nor the birth-death comparison strategy is claimed new. The added finite-time conclusion here is an explicit singleton-PPT margin combined with asymptotically strong separation from full separability. N120's all-time depth statement was not independently certified by our finite-time code. The refreshed 01_CORE.txt blob was 4f84ffebb34d7724e0d6c07ffbbb4ff0c554e282; the earlier start/core snapshot in RESULT_AND_RESTART.md is historical provenance, not the current repository state.

Candidate contributions requiring specialist priority review: the all-size singleton-separability/PPT extension; the reusable common-axis LOCC anti-concentration bound; full-separability distance tending to one; the regularized-relative-entropy lower bound with arbitrary local cross-copy correlations; and the combined finite-time PPT preparation/group-distillation interface. These are not claimed as established historical firsts.

Other relevant primary literature: Toth et al. arXiv:0806.1048 (spin-variance witnesses and bound entanglement); Eggeling-Werner quant-ph/0010096 (tripartite invariant-state separability); Smolin quant-ph/0001001 (different unlocking pattern); Horodecki-Horodecki quant-ph/9708015v3 Sections V-VI (singlet fraction >1/d implies distillability); Moharramipour et al. arXiv:2406.08542 (symmetry-sector maximally mixed entanglement). Bassler arXiv:2504.13646/doi:10.1103/qxx1-xr44 addresses symmetric diagonal states, including fully excited input; do not extend that restriction to the entire Hilbert space. Source scopes/read depths are in the research note.

## 2. Freshly executed certificate and corrected convention

The earlier checkpoint referred to packet bytes not present in the active runtime at continuation. Its execution claims were not substituted for fresh execution. New exact and numerical scripts were reconstructed, saved and actually run successfully.

Model: Gamma[(nu+1)D[J_-]+nu D[J_+]], rho(0)=I/2^N, UNNORMALIZED uniformly coupled collective jumps. At N=4, nu=1/5, Gamma*t=8, the exact-rational script proves:

- singleton PT eigenvalues >1/20000-epsilon;
- sum_a Var(J_a)-N/2 < -0.04; display -0.04152141367819679;
- two-group herald probability >49/10000; display 0.004921171305935521;
- heralded spin-singlet fraction >7/20>1/3; display 0.3527841245878097;
- all these inequalities survive arbitrary additional STATE trace-norm perturbation <=1/100000.

Uniformization: rate 9, Poisson parameter 72, cutoff 400, explicit rational trace-error bound <3.151e-158. All 16 LDL pivots of the partial transpose minus I/20000 are exactly positive. No pass/fail test uses rounded eigenvalues. This certificate proves finite-time PPT, not finite-time singleton separability or depth two.

The first reconstruction used the wrong filter sign; a fidelity assertion caught it. Correct: K^dagger K=q^(2-J_z) for two spin-one groups. Single-qubit filter diag(1,1/sqrt(6)) in EXCITED,GROUND order, reversed in ground,excited order. Corrected code was rerun successfully.

Actual numerical tests: 54 full density matrices N=2..7; 960 moment fixtures; 100 product arrays/16000 atom bounds; seven angular quadratures; 316 spectral-gap comparisons; 228 evolution/mixing comparisons; 30 explicit stationary-PPT-margin checks. Seed 8102026. All passed, without implying all-size proof certification or independent expert review.

Current SHA256 hashes (supersede earlier checkpoint hashes):
- certify_finite_time.py: 08ddfd0a28d134e7e3faf87f5ce4c7aecd4f4fb93dfb072fcf70111f23fad713
- certificate.json: 7a71270f725dafc860aae0c9e3f84413b7ce52a317bfef18a42757bae5619a18
- diagnostics.py: 872ebc60e8029f392a9f4c3e257b4117181c0556f50a6ccc8b21bd13c840acf9
- diagnostics.json: a08886094c7d0dff009a557bda5da458dd6a26bba57f0780fdc593a4bb00e9ef
- final RESEARCH_NOTE.md: c4ad59f0c6b4cb0bb7d5b07e54b5f0d71818e4f372840c74e7a80c610e08709e

The full conversation packet contains the 12-page note/PDF, scripts, JSON outputs, logs, requirements, and manifest. The exact certificate is also committed here independently of that packet.

## 3. Uniform approximate-preparation bound

Set beta=log(1+1/nu), q=exp(-beta), c_nu=(sqrt(nu+1)-sqrt(nu))^2>0. For ALL N>=2 and the SPECIFIED input I/2^N,

D(rho(t),rho_N) <= (1/2) exp[-c_nu Gamma*t+beta/2]

whenever Gamma*t>=beta/(2c_nu), where D is HALF the trace norm. Accuracy epsilon<1/2 therefore needs

Gamma*t >= [beta/2+log(1/(2epsilon))]/c_nu.

This is independent of N only under the stated jump convention. It is not an N-independent hardware/energy claim. Replacing J with J/sqrt(N) multiplies physical times by N.

PROOF. In spin j, dimension d=2j+1, population indices are r=0,...,d-1. Down a_r=(nu+1)r(d-r), up b_r=nu(r+1)(d-r-1), stationary pi_r proportional to q^r. Every edge factor (r+1)(d-r-1)>=d-1. Its reversible Dirichlet form dominates d-1 times that of the reflecting constant-rate chain down nu+1, up nu. That chain's gap is

2nu+1-2sqrt(nu(nu+1))cos(pi/d) >= c_nu.

Thus sector gap >=(d-1)c_nu. For uniform sector input u_r=1/d,

chi^2(u||pi) <= max_r(u_r/pi_r)-1 <= exp[beta(d-1)].

Reversible L2 contraction/Cauchy-Schwarz imply

D(p_j(t),pi_j) <= (1/2) exp[-(d-1)(c_nu Gamma*t-beta/2)].

Spin zero is stationary; other d-1>=1. Sum over the conserved weights w_Nj. This input has no generated sector coherences, so populations suffice for full trace norm. N120 already used the reflecting-chain comparison mechanism; the present estimate charges the initial chi-square divergence explicitly.

## 4. Explicit PPT margin and actual finite-time bound entanglement

Fix STRICT nu>nu_*, with Delta=4-cosh(beta)>0. The stationary state satisfies

lambda_min(rho_N^(T_i)) >= m_N := (2Delta/9) exp[-N(beta+log 2)]

for each singleton cut.

PROOF. In the qubit-spin-k central block, f_+=f_(k+1/2), f_-=f_(k-1/2). The potentially small partial-transpose eigenvalue is

f_+ [(2k+2)/(2k+1)] [1-(f_-/f_+)/(2k+2)].

For k>=1, f_-/f_+ <= [2k/(k+1)]cosh(beta), so the last bracket is >=1-cosh(beta)/4=Delta/4. At k=1/2 the bracket is exactly 2Delta/9. The prefactor is >=1; the other eigenvalue is >=f_+; k=0 is harmless. Since x/sinh(x) decreases, f_j decreases with j. Also Z_(N/2)<=(N+1)exp(beta N/2), so f_(N/2)>=exp(-beta N/2). The central partial transpose therefore has minimum eigenvalue >=(2Delta/9)exp(-beta N/2). The product filter contributes its squared minimum singular value exp(-beta N/2), and normalization contributes 2^-N. This proves m_N.

Partial transpose preserves Hilbert-Schmidt norm, so

||(rho(t)-rho_N)^(T_i)||_op <= ||rho(t)-rho_N||_1.

Every time obeying

Gamma*t_N >= [beta/2+N(beta+log 2)+log(9/Delta)]/c_nu

therefore gives trace-norm error <=m_N/2, strictly positive singleton partial transposes with eigenvalues >=m_N/2, and trace DISTANCE to stationarity <=m_N/4. Combining the stationary theorem D(rho_N,SEP_N)->1 with the triangle inequality gives

D(rho(t_N),SEP_N)->1.

For each fixed nu>nu_*, actual finite-time states are consequently multipartite bound entangled for all sufficiently large N. The conservative time is O_nu(N)/Gamma with unnormalized jumps, O_nu(N^2)/Gamma with J/sqrt(N). This is an exact-PPT conclusion, not merely an approximation to a bound-entangled target. It does not prove a finite-time singleton-separable or depth-two decomposition. The endpoint nu=nu_* is excluded. The explicit N=4 certificate is much faster than this conservative large-size guarantee at its interior parameter.

## 5. Retained scope and restart

Stationary main result: at fixed finite nu>=nu_*, all singleton cuts are separable. For sufficiently large N, the state is not fully separable, N separate parties cannot distill pure entanglement, full-separability trace distance tends to one, regularized relative entropy is between (1/4)log N-O_nu(log log N) and (1/2)log(3N+1), depth is exactly two, every o(sqrt(N))-qubit marginal approaches maximally mixed, and entropy per qubit tends to one bit. The regularized lower bound permits quantum cross-copy correlations WITHIN each laboratory; its proof is sequential LOCC plus the classical relative-entropy chain rule, not an iid-alternative assumption.

This is not genuine N-party entanglement or a resolution of the NPT-bound-entanglement problem. Full-separability distance is not distance from the two-producible set. Larger cuts need not be PPT. Two groups can obtain a distillable mixed pair using joint operations within BOTH groups, with Theta(N^-3) heralding at fixed nu and selected spin along allowed parities; high-temperature constants may be very poor. Heralding is not Bell-pair yield and is not the stronger Smolin grouping pattern. Post-preparation depolarization retains detected bound entanglement asymptotically for lambda>sqrt(pi/8), but this says nothing about symmetry-breaking noise during preparation. No quantum-computing, metrological or thermodynamic advantage was demonstrated.

Use RESULT_AND_RESTART.md for the detailed stationary/block/anti-concentration/overlap proofs, with this file's precedence corrections. Run the exact script using Python 3.10+ and SymPy. Independently audit the common-axis anti-concentration constant, cross-copy relative-entropy argument, qubit-spin separability twirl, birth-death comparison, and PPT margin. Prior-art review should start with Li-Xu, N120 and invariant-state literature.

Retained failed escalation: the relative-entropy coefficient gap 1/4 versus 1/2 is not closed. Sharp independent sector-overlap bounds lose their gain on summation. A proposed conditional strengthening fails for N=2, |+> tensor |->: singlet probability 1/2, magnetization-zero probability 1/2, erroneous RHS 1/4. High-temperature extraction costs, nonuniform coupling robustness, and larger-cut structure remain unresolved. Do not restore the earlier missing-preparation-bound claim: Sections 3-4 replace it, while crediting N120's earlier activation/mixing mechanism.
