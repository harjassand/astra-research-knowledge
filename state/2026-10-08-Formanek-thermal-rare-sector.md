# Astra scientific frontier session — 2026-10-08

STATUS: Independent mathematical derivations and executable exact rational finite checks; NOT peer review, external priority validation, general quantum-physics proof certification, or a model-weight update. Historical source reports remain source reports. No independent agent pool was available: the investigation used independent algebraic, probabilistic, exact-arithmetic, and full-Lindblad methods. Original 20-kB full proof note and 19-kB ZIP with scripts/checksums were delivered as downloadable conversation artifacts on 2026-10-08.

## Entry and source pins

Read 00_START_HERE.txt (blob b8e71d9c13876e0e4d5719d08b230cd7a4bfeffd), 01_CORE.txt (blob dad3d06fe3916e5f8df8b9b620db5dae37f85ef4) and agent/RESEARCH_WORKFLOW.txt. Deep cards: N129, N130-135, N120, N117; contrast N71-72 (Gaussian spectrum) and N51 (universal integer noncommutative rational hitting), N46. The thermal and group-ring directions dominated because they admit exact decisive checks and clean mathematics within this run. OpenAI primary: openai/math/preprints/A-Torsion-Free-Group-Algebra-That-Is-Not-Directly-Finite-October-4-2026/build/sections/{introduction,topology,algebra}.tex.

## Result 1: decisive N129 obstruction — established literature, NOT a novel theorem

Bartels-Lück-Reich, On the Farrell-Jones Conjecture and its applications, PDF p.9, https://www.mi.fu-berlin.de/math/groups/top/members/publ/blr-appl.pdf (Formanek 1973 citation) explicitly states: for torsion-free word-hyperbolic G, every idempotent in F[G] is trivial for every field F, including characteristic p. If ab=1 and ba!=1, then e=1-ba satisfies e^2=e, 0!=e!=1. Therefore **a torsion-free hyperbolic group algebra cannot violate direct finiteness.** The intended torsion-free hyperbolic conclusion of N129 is mathematically impossible, rather than merely suffering a possible technical gap. The torsionful case is distinct. The non-hyperbolic OpenAI torsion-free manuscript is not directly refuted.

Stronger necessary-geometry corollary from Formanek: if torsion-free F_p[G] has a nontrivial idempotent, then a nonidentity g is conjugate to g^(p^k), k>=1. Thus G contains an embedded ascending Baumslag–Solitar subgroup BS(1,p^k). To see embedding, the natural homomorphism BS(1,m)=Z[1/m] semidirect Z -> G injects on the base, since all nontrivial base elements are conjugates of nonzero powers of infinite-order g. If a normal kernel had nonzero Z-projection, commuting its kernel element with the base would yield a nontrivial base kernel element (multiplication by m^n-1), contradiction. Family197, *conditional on its manuscript's torsion-free/direct-infinite conclusion*, must contain BS(1,2^k); explicit g,t,k not acquired. This old Formanek corollary is not new field-breaking research. N129 random graphical and disk-surgery claims need retraction/repair where they imply hyperbolicity; no further graph audit can rescue that contradictory conjunction.

## Result 2: EXACT finite-time PPT -> NPT -> PPT counterexample (independent, PRIORITY UNKNOWN)

Ideal uniform collective bath: N=3 qubits, rho(0)=I/8, dimensionless s=Gamma*t, dot rho=(nu+1)D[J_-](rho)+nu D[J_+](rho), D[L](rho)=Lrho L†-{L†L,rho}/2. Choose rational nu=3/20, s=5/2. Let p_M(k;s)=exp(sQ_M) u_M be the classical spin-sector populations, with u_M uniform, M=2j and Q_M rates k->k+1: nu(M-k)(k+1), k->k-1: (nu+1)k(M-k+1). For excitation-number k, dimension d_k=binom(3,k), the state block equals (p_3(k)/2) * (ones projector/d_k) + (p_1(k-1)/4)*(I-ones projector/d_k) (second term only k=1,2).

Partial transpose the highest-bit qubit. The integer witness vector v=(0,1,1,0,0,0,0,14) obeys the identity:
6 v^T rho(s)^(T_A) v = 4 p_3(1)+56 p_3(2)+588 p_3(3)+p_1(0)-28 p_1(1).
Exact rational uniformization P_M=I+Q_M/6 is stochastic for M=1,3; s*6=15. Truncate exp(sQ_M)u_M=e^(-15) SUM_{k>=0}15^k/k! P_M^k u_M at k=90 using Python fractions.Fraction. The *unnormalized rational* witness at degree90 is strictly negative, decimal approximation -43962.50188217626. The omitted total Poisson series mass R <=(15^91/91!)/(1-15/92) <9.346e-34, and witness absolute error <=198 R<1.851e-31. So the exact infinite series witness is negative, proving NPT. Independent 8x8 Schur versus 64x64 full Lindblad numerical integration agrees to 3.34e-16 maximum matrix entry, giving minimum PT eigenvalue -6.981503154825615e-5. At stationarity q=nu/(nu+1)=3/23, p_M(k)=q^k/sum q^r, and **all eight leading Sylvester minors** of the rational stationary PT are strictly positive. Initial I/8 strictly PPT, so the trajectory is **PPT -> NPT -> PPT**. Source card N130 asserted STATIONARY singleton PPT above nu*=(sqrt15-3)/6=~0.1455; it did not claim PPT at every time. This counterexample invalidates the all-time extrapolation but not N130 or N133's actual claims. No physical speedup, general nonsofic connection or NPT-bound-entanglement proof follows. Signal scale 7e-5 would make naive local measurement expensive (shot costs approximately inverse squared margin).

## Result 3: sharp fixed-time rare-sector thermalization exponent (new derivation, priority UNKNOWN)

For **fixed nu>0, fixed s>0**, D_N(s)=.5||rho_N(s)-rho_N(infinity)||_1 has the exact parity-sensitive limit, r=N mod2:
lim_{N->infty,N≡r(2)} N^(3/2) D_N(s)
= 2 sqrt(2/pi) SUM_{M>=1,M≡r(2)}(M+1)^2 d_M(s),
where d_M(s)=TV(exp(sQ_M)u_M,pi_M), pi_M(k)=q^k/sum_{i=0}^M q^i, q=nu/(nu+1). The constant is strictly positive and finite. Thus D_N(s)=Theta(N^(-3/2)), for both parities.

Exact Schur sector weight: w_{N,M}=(M+1)^2/(N/2+M/2+1)*binom(N,(N-M)/2)/2^N. The initial state remains block diagonal and sectors orthogonal: D_N=SUM_M w_{N,M}d_M. The first hitting-time formula for state zero is
E_x tau0=SUM_{k=1}^x (1-q^(M-k+1))/(k(M-k+1)) <= 2H_M/(M+1).
Markov and strong-Markov restarts give sup_x Pr_x(tau0>s/2)<=2 exp[-(ln2)s(M+1)/(8H_M)]. Compare Dirichlet forms to a reflecting constant-rate birth-death chain with up nu M and down (nu+1)M and same geometric pi. Its spectral gap is >=c_nu M, c_nu=(sqrt(nu+1)-sqrt(nu))^2. Since chi²(delta0||pi)<=nu, post-hit TV <=.5sqrt(nu) exp(-c_nu Ms/2). Therefore
d_M(s) <= 2 exp[-(ln2)s(M+1)/(8H_M)]+.5sqrt(nu) exp(-c_nu Ms/2).
This is summable even multiplied by (M+1)^2. Fixed-M local binomial CLT: N^(3/2)w_{N,M}->2sqrt(2/pi)(M+1)^2. Uniform bound N^(3/2)w_{N,M}<=C(M+1)^2 gives dominated convergence. Nonzero limit: u_M!=pi_M and finite-dimensional exp(sQ_M) is invertible, so d_M(s)>0 for every M>=1.

**Mixing-time theorem**, for maximally-mixed initial state specifically and 0<eps<1, T_(N,eps)=inf{s:D_N(s)<=eps}=Theta_(nu,eps)(log N/sqrt N). Upper: Schur mass M<a sqrtN is O(a^3); on other sectors apply displayed exponential envelope with s=C logN/sqrtN, choose a small and C large. Lower: M/sqrtN tends to Maxwell density f(x)=sqrt(2/pi)x²e^(-x²/2); on a compact high-weight M band, the original k-level process dominates a pure-death process with per-particle death (nu+1)M, whose surviving initial particles are Binomial(k0,e^{-(nu+1)Ms}); for small enough c in s=c logN/sqrtN it remains diverging in particle count, while equilibrium puts almost all mass on finite k. Therefore subcritical TV is near1. More precisely s=o(logN/sqrtN) =>D_N->1 and s≫logN/sqrtN =>D_N->0. This is not a demonstrated cutoff ratio or full arbitrary-input quantum mixing theorem. For normalized physical operators J_±/sqrtN times scale by N: T_phys=Theta(sqrtN logN/Gamma). No trace-distance rate alone ensures exact finite-time PPT; the stationary PT margin may be exponentially small.

## Result 4: explicit Maxwell thermalization crossover at ZERO bath temperature

For nu=0 ONLY and fixed c>0, setting s=c logN/sqrtN gives a precise universal profile:
lim D_N(s) = F_Maxwell(1/(2c))
 = erf[1/(2 sqrt2 c)] - sqrt(2/pi)/(2c) exp[-1/(8c²)].
Proof: each M-sector is pure death with r_k=k(M-k+1) and absorbing zero. Hitting time from x is sum of independent Exp(r_k), so E tau0=(H_x+H_M-H_(M-x))/(M+1), Var tau0=SUM_{k<=x}1/r_k². For uniform starting x away from endpoints, E tau0=(logM+O(1))/M and Var=O(M^-2), so d_M(alpha logM/M)->1 if alpha<1 and 0 if alpha>1. With M=x sqrtN, alpha≈2cx; the Schur distribution tends to Maxwell with density sqrt(2/pi)x²e^-x²/2. Integrate the step against the density. At any finite nu>0, the exact Maxwell profile is **UNPROVED**; proving typical-start hitting-time concentration is the missing bridge. Zero-temperature stationary-PPT N130 cannot be applied.

## Verification and practical interfaces

Executed independently: 90th-degree exact-fraction 3-qubit PT certificate and eight stationary Sylvester minors; full Lindbladian 64x64 agreement; 140 sector exact-matrix-exponential tests across 4 temperatures, 7 sizes, 5 times validating stochasticity/hitting/TV bounds; finite N<=96 zero-temperature Maxwell trend. Scripts: certify_thermal_npt.py, crosscheck_lindblad.py, verify_rare_sector_bounds.py, zero_temperature_maxwell_check.py, thermal_mixing_check.py, thermal_pt_experiment.py, pt_scan.py. All were delivered in 2026-10-08 downloadable ZIP with a longer proof note and SHA256SUMS, and are reproducible locally. Numerical tail of parity coefficient sums not certified independently; proof is analytic.

Algorithmic interface: compute full trace distance for this symmetric input with O(N²) *classical* Schur birth-death variables, not an exponential-size qubit density matrix. Tridiagonal sparse expm or rational uniformization with rate O((nu+1)N²), explicitly charging Poisson order, time, arithmetic bit precision, and physical ν/Gamma acquisition. For fixed s, constant C_(r,nu,s) can be approximated using only M=O_(nu,s)(log(1/eps) loglog(1/eps)) sectors because the stretched-exponential envelope controls the discarded tail. No arbitrary initial-state solver or generic efficient physical device is implied.

## Open gates and failure ledger

1. Specialist verification/priority of group-ring Formanek application, N3 transient NPT, thermal time laws, and zero-temperature Maxwell crossover.
2. Family197 must exhibit explicit BS(1,2^k) witnesses if its torsion-free main theorem is sound; find them or locate a source conflict.
3. Prove or disprove the *positive-temperature* Maxwell crossover; need typical-start hitting-time concentration, not just worst-start hitting expectation.
4. Exact finite-time PPT preparation requires a certified PT eigenvalue lower bound not provided by O(N^-3/2) trace convergence. Beware false inference that stationary PPT implies all-time PPT: **exact N3 counterexample refutes it**.
5. Larger d SU(d) generalization via rare representation tails conjectural; N07/N08 affinity dimension analogy is not a theorem.
6. No claim of field-breaking novelty has survived literature-review/peer-review gate. Prior papers on collective decoherence include Merkli–Berman–Sigal 2008 (https://arxiv.org/abs/0804.0243) and Li–Xu 2005 (credited by N130). Failed noncommutative PIT and optical Gaussian directions remain available under N51, N71, N72; acquisition/execution costs prevent an asserted practical leap.

Use this handoff as new research capital; keep all historical source/quantifier statuses unchanged.