# Audit update and preparation-time escalation

8 October 2026. Read this BEFORE RESULT_AND_RESTART.md. Status: internally derived candidate mathematics, not external peer review, proof-assistant certification, or priority clearance. No independent subagents were available.

This file supersedes the old checkpoint's execution counts, hashes, missing-code reference, and unresolved preparation-time statement. The earlier substantive stationary-state and anti-concentration proofs remain candidate proofs with the caveats below. Current executable certificate: certify_finite_time.py in this directory.

## 1. Decisive priority correction

Li and Xu, arXiv:quant-ph/0505216v2, 'Stationary entanglement and nonlocality of two qubits or qutrits collectively interacting with the thermal environment: The role of Bell singlet state', already give the SAME collective thermal generator, stationary two-qubit formulas, and threshold nu_*=(sqrt(15)-3)/6. See Eq. (1), Eqs. (10)-(11), and p. 3, including their explicitly discussed initially maximally mixed case r=0. Their symbol N denotes bath occupation, not our number of qubits. Submitted 2005; International Journal of Quantum Information 6,1165 (2008).

The numerical constant and basic bath-induced entanglement are NOT new. The candidate contribution is the all-size singleton-separability extension, strong distance from full separability, regularized-relative-entropy lower bound, and their preparation/group-extraction interfaces. Priority for that combination remains unresolved.

Other inherited inputs/nearby work: Toth et al. arXiv:0806.1048 (collective-variance witnesses and bound entanglement); Eggeling-Werner quant-ph/0010096 (tripartite invariant-state separability); Smolin quant-ph/0001001 (different unlocking pattern); Horodecki-Horodecki quant-ph/9708015v3 Sections V-VI (singlet fraction >1/d implies distillability); Moharramipour et al. arXiv:2406.08542 (symmetry-sector maximally mixed entanglement). Bassler arXiv:2504.13646/doi:10.1103/qxx1-xr44 addresses symmetric diagonal states, including fully excited input: this cannot be indiscriminately applied to the full-space maximally mixed state, which contains all spin sectors. Exact source scopes and inspected depths are recorded in the accompanying research note.

## 2. Freshly executed certificate; earlier hashes superseded

The earlier checkpoint referred to a packet whose bytes were not present in the active runtime at continuation. Its execution claims were not substituted for fresh execution. A new exact-rational certificate and numerical diagnostics were reconstructed, saved, and actually run successfully.

Model remains Gamma[(nu+1)D[J_-]+nu D[J_+]], rho(0)=I/2^N, UNNORMALIZED uniform collective jumps. For N=4, nu=1/5, Gamma*t=8, the exact certificate establishes:

- every singleton partial transpose has minimum eigenvalue >1/20000-epsilon;
- sum_a Var(J_a)-N/2 < -0.04 (display value -0.04152141367819679);
- two-group heralding probability >49/10000 (display 0.004921171305935521);
- heralded spin-singlet fraction >7/20>1/3 (display 0.3527841245878097);
- these inequalities remain true under any additional STATE trace-norm perturbation <=1/100000.

Uniformization rate 9, Poisson parameter 72, cutoff 400. The explicit rational trace-error bound is <3.151e-158. All 16 LDL pivots of the partial transpose minus I/20000 are exactly positive. The tests do not use rounded eigenvalues. The certificate establishes finite-time PPT, NOT finite-time singleton separability or depth two.

An initial code reconstruction had the wrong sign in the filter square; the fidelity assertion caught it. The corrected formula is K^dagger K=q^(2-J_z) for the two spin-one groups. The single-qubit filter is diag(1,1/sqrt(6)) in the EXCITED,GROUND basis (reversed in ground,excited basis). Corrected code was rerun and passed.

Actual numerical diagnostics: 54 full density-matrix fixtures N=2..7; 960 moment fixtures; 100 product arrays with 16000 pointwise anti-concentration checks; seven angular quadratures; 316 birth-death spectral-gap comparisons; 228 population-evolution mixing comparisons; 30 checks of the explicit PPT margin below. Seed 8102026. All passed. These finite checks are not independent expert reviews or substitutes for the all-size proofs.

SHA256 of current actual files:
- certify_finite_time.py: 08ddfd0a28d134e7e3faf87f5ce4c7aecd4f4fb93dfb072fcf70111f23fad713
- certificate.json: 7a71270f725dafc860aae0c9e3f84413b7ce52a317bfef18a42757bae5619a18
- diagnostics.py: 872ebc60e8029f392a9f4c3e257b4117181c0556f50a6ccc8b21bd13c840acf9
- diagnostics.json: a08886094c7d0dff009a557bda5da458dd6a26bba57f0780fdc593a4bb00e9ef
- RESEARCH_NOTE.md: c0cbd8138df8b1a45693267d417ab45319e2d8c224edf96c42c50db498151d7a

The full conversation packet supplies the note, PDF, both scripts, JSON outputs, logs, requirements, and manifest. The portable exact script is also committed beside this file. Do not reuse the superseded hashes in RESULT_AND_RESTART.md.

## 3. New uniform approximate-preparation bound

Set beta=log(1+1/nu), q=exp(-beta), and c_nu=(sqrt(nu+1)-sqrt(nu))^2>0. For ALL N>=2, the SPECIFIED initial state I/2^N satisfies

D(rho(t),rho_N) <= (1/2) exp[-c_nu Gamma*t + beta/2]

whenever Gamma*t>=beta/(2c_nu). Here D is HALF the trace norm. Thus epsilon<1/2 accuracy needs

Gamma*t >= [beta/2+log(1/(2epsilon))]/c_nu,

independent of N in the stated unnormalized collective-jump convention. This is not an N-independent hardware/energy assertion. Replacing J by J/sqrt(N) multiplies physical time by N.

PROOF. In spin j, dimension d=2j+1, index populations r=0,...,d-1. Down rates a_r=(nu+1)r(d-r), up rates b_r=nu(r+1)(d-r-1). Stationary pi_r is proportional to q^r. Each edge factor (r+1)(d-r-1) is at least d-1. The reversible Dirichlet form therefore dominates d-1 times the reflecting constant-rate chain with down rate nu+1 and up rate nu. The smallest nonzero eigenvalue of minus that chain is

2nu+1-2sqrt(nu(nu+1))cos(pi/d) >= c_nu.

The sector gap is >=(d-1)c_nu. For the uniform sector initial population u_r=1/d,

chi^2(u||pi) <= max_r(u_r/pi_r)-1 <= exp[beta(d-1)].

Reversible L2 contraction and Cauchy-Schwarz yield

D(p_j(t),pi_j) <= (1/2) exp[-(d-1)(c_nu Gamma*t-beta/2)].

Spin zero is already stationary. All other sectors have d-1>=1. Sum with conserved Schur weights w_Nj to obtain the bound. This initial state produces no sector coherences, so the population comparison suffices for the full trace norm.

## 4. New explicit PPT margin and finite-time bound entanglement at all large sizes

Fix STRICT nu>nu_*, so Delta=4-cosh(beta)>0. The stationary singleton partial transposes obey the conservative explicit bound

lambda_min(rho_N^(T_i)) >= m_N := (2Delta/9) exp[-N(beta+log 2)].

PROOF. Use the old qubit-spin-k central block aI+b sigma.K, f_+=f_(k+1/2), f_-=f_(k-1/2). The potentially small partial-transpose eigenvalue is

f_+ [(2k+2)/(2k+1)] [1-(f_-/f_+)/(2k+2)].

For k>=1, f_-/f_+ <= [2k/(k+1)]cosh(beta), so the bracket is >=1-cosh(beta)/4=Delta/4. At k=1/2 it is exactly 2Delta/9. The prefactor is >=1. The other eigenvalue is >=f_+; the k=0 block is harmless. Since x/sinh(x) decreases, f_j decreases with j. Also f_(N/2)>=(exp(-beta N/2)), because Z_(N/2)<=(N+1)exp(beta N/2). Therefore the central partial transpose has minimum eigenvalue at least (2Delta/9)exp(-beta N/2). The product filter has squared minimum singular value exp(-beta N/2), and normalization contributes 2^-N. This proves the claimed m_N.

Partial transpose preserves Hilbert-Schmidt norm, so

||(rho(t)-rho_N)^(T_i)||_op <= ||rho(t)-rho_N||_1.

Consequently, any time satisfying

Gamma*t_N >= [beta/2 + N(beta+log 2) + log(9/Delta)]/c_nu

makes the state trace-norm error at most m_N/2. Every singleton partial transpose is then strictly positive, with eigenvalue >=m_N/2. The trace DISTANCE from the stationary state is at most m_N/4.

The stationary theorem D(rho_N,SEP_N)->1 and the triangle inequality now give

D(rho(t_N),SEP_N)->1.

Thus for every fixed nu>nu_*, ACTUAL finite-time states are multipartite bound entangled for all sufficiently large N. Preparation time is conservatively O_nu(N)/Gamma with the unnormalized jumps, or O_nu(N^2)/Gamma with J/sqrt(N). This exact-PPT conclusion is stronger than merely approximating a bound-entangled stationary state. It uses singleton PPT, not a finite-time singleton-separable decomposition or finite-time depth-two claim. The endpoint nu=nu_* remains outside this finite-time theorem. The four-qubit exact certificate gives a substantially shorter time at one interior point.

## 5. Main candidate result retained and its boundaries

For the selected stationary state at fixed finite nu>=nu_*, all singleton cuts are separable, but for sufficiently large N the state is not fully separable and no pure entanglement can be distilled by N separate laboratories. Its full-separability trace distance tends to one, while entanglement depth is exactly two, all o(sqrt(N))-qubit marginals tend to maximally mixed, and entropy per qubit tends to one bit. The regularized relative entropy in nats is between (1/4)log N-O_nu(log log N) and (1/2)log(3N+1). The lower bound permits quantum correlations across copies WITHIN each laboratory; it follows from the sequential LOCC binary-test relative-entropy chain rule, not an iid-alternative assumption.

This is not genuine N-party entanglement or a resolution of the NPT-bound-entanglement conjecture. The distance is from FULL separability, not from the two-producible set. At N>=4 larger cuts need not be PPT. The strong stationary cutwise-separability/depth statements are not automatically claimed for finite-time states.

Two large groups can extract a distillable mixed spin pair. Both receiving groups may perform joint operations. At fixed temperature and fixed selected spin, heralding is Theta(N^-3) along compatible parities; high-temperature constants/filtering can be extremely poor. Heralding probability is not Bell-pair yield. This differs from Smolin's pattern of joining one pair to help two still-separated recipients.

Post-preparation depolarization retains entanglement for all sufficiently large N whenever lambda>sqrt(pi/8), with singleton separability/PPT preserved. This sufficient threshold says nothing about unequal couplings or symmetry-breaking noise DURING preparation. No quantum-computing, metrology, or thermodynamic advantage was demonstrated.

## 6. Restart priorities and retained failures

Read RESULT_AND_RESTART.md for stationary/block/anti-concentration/projection-overlap derivations, but apply the precedence corrections here. Run the exact script with Python 3.10+ and SymPy. The current packet's requirements and manifest contain the versions and complete artifact hashes.

Audit the common-axis Bernoulli anti-concentration argument, cross-copy regularized-relative-entropy proof, qubit-spin separability twirl, birth-death gap comparison, and explicit product-filter PPT margin independently. Then undertake specialist prior-art review, beginning with Li-Xu and invariant-state literature.

The logarithmic coefficient gap 1/4 versus 1/2 is not closed. Independent sharp single-sector product-overlap bounds lose their advantage when summed over sqrt(N) relevant spins. The proposed conditional strengthening is false already for N=2, |+> tensor |->: singlet probability 1/2, magnetization-zero probability 1/2, erroneous RHS 1/4. Better extraction at high temperature, robustness to nonuniform couplings, and larger-cut structure remain open. Do not revive the earlier missing-uniform-preparation claim: Sections 3-4 now provide explicit bounds.
