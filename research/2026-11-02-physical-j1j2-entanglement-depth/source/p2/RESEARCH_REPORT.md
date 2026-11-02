# ASTRA | Exchange-square completion and two-replica certificates for real frustrated quantum matter

**Scientific checkpoint:** 2 November 2026. **Status:** a connected, exact-arithmetic, internally reproducible mathematical result on the original square-lattice spin-1/2 J1-J2 model. **NOT:** an identified VBS/QSL/Néel phase, proof of new algorithmic complexity class, experiment, independently peer-reviewed or historically priority-cleared discovery.

## 1. Physical assertion and known baseline

Fix J1>0 and J2/J1=alpha. For even periodic square lattices of N=L² sites, L divisible by 4 and sufficiently large (L>=12 avoids tiny-torus interaction-wrapping exceptions), define

\[H_\alpha/J_1=\sum_{\langle i,j\rangle}\mathbf S_i\cdot\mathbf S_j+\alpha\sum_{\langle\!\langle i,j\rangle\!\rangle}\mathbf S_i\cdot\mathbf S_j,\qquad \mathbf S_i=\tfrac12(\sigma_i^x,\sigma_i^y,\sigma_i^z).\]

A *k-producible* state is a convex mixture of pure states which factor as a tensor product of disjoint groups, each of at most k physical spins. Groups may be nongeometric and the group partition may change between mixture components. Entanglement depth at least k+1 means the state is not k-producible. The assertion established here is that the ground state at alpha=1/2 has depth >=6; the same is true of the finite-volume Gibbs state at explicitly bounded positive temperatures. This certifies multipartite quantum correlations in the *same strongly frustrated Hamiltonian*, not an artificial surrogate.

The previous baseline is preserved byte for byte: `astra_independent_quantum_20261102.zip`, SHA256 `a339c1e31c60c27b0dfb77c13c725e19f04f8486a847e24e5f84ee2fe67e5a21`. Its independent 16-spin variational witness `upper_trial_L4.json` was re-run using `check_trial_upper.py` and gives

\[e_0(1/2)/J_1\le -0.4690973093800669\ldots<-0.46909.\]

The decimal is a display of a checked rational Rayleigh quotient, not a numerical thermodynamic extrapolation. The exact state resides in the physical half-up 16-spin Hilbert sector; a four-rotation twirl preserves its energy and makes every one-site spin expectation zero. Independent tiling of 4x4 patches therefore makes cross-tile physical exchange energies zero. No physical gap or access to the true ground state is assumed. The original separate energy lower bound -0.583212 remains preserved, not improved or reinterpreted here.

## 2. Exact exchange-square organizing identity

At alpha=1/2 and for any real vectors a_i in R³, let

\[E_{\rm cl}(a)=\sum_{\langle i,j\rangle}a_i\cdot a_j+\frac12\sum_{\langle\!\langle i,j\rangle\!\rangle}a_i\cdot a_j.\]

Counting each square plaquette gives the exact operator-independent identity

\[\boxed{E_{\rm cl}(a)+\sum_i\|a_i\|^2=\frac14\sum_{p}\left\|\sum_{i\in p}a_i\right\|^2\ge0.}\tag{1}\]

Equivalently, the 2D exchange Fourier eigenvalue is

\[\widehat J(q)=2(\cos q_x+\cos q_y+\cos q_x\cos q_y)=2[(1+\cos q_x)(1+\cos q_y)-1]\ge-2.\]

The identity is local and works also for zero-extended finite blocks. It keeps the correct two-dimensional frustration and is *not* a positive quantum-spin decomposition: noncommutativity remains in the intra-block quantum correlations.

For a pure block-product state and block B, define a_i=<S_i> and H_B as precisely the original exchange bonds *both ends of which lie in B*. Then

\[\langle H_{1/2}/J_1\rangle=E_{\rm cl}(a)+\sum_B\sum_{i<j\in B}J_{ij}[\langle \mathbf S_i\cdot\mathbf S_j\rangle-a_i\cdot a_j]\ge \sum_B F_B(\rho_B),\tag{2}\]

\[F_B(\rho)=\operatorname{Tr}(H_B\rho)-\sum_{i,j\in B}A_{ij}a_i\cdot a_j,\qquad A_{ij}=\delta_{ij}+J_{ij}/2.\tag{3}\]

Here J_ij=1 for NN, 1/2 for NNN, zero otherwise. A_B is positive semidefinite because it is a principal submatrix of the positive exchange-shift form in (1). Thus F_B is concave as a function of a density matrix and its minimum is attained by a pure state. No physical-state extension operation is assumed anywhere in (2)--(3).

## 3. Main operator theorem: two-copy certificate

On two formal copies of the **same** finite physical cluster define

\[\boxed{W_B=\tfrac12(H_B^{(1)}+H_B^{(2)})-\sum_{i,j\in B}A_{ij}\mathbf S_i^{(1)}\cdot\mathbf S_j^{(2)}.}\tag{4}\]

For every pure physical cluster state |psi>, the equality

\[\langle\psi\psi|W_B|\psi\psi\rangle=F_B(|\psi\rangle\langle\psi|)\tag{5}\]

is exact. By concavity this implies that a state-independent operator lower bound `W_B >= -gamma |B| I` forces `F_B(rho) >= -gamma |B|` for **every** density rho on the cluster. For a cluster whose weighted interaction graph has multiple connected components, F_B is the sum of the same functional on reduced component density matrices; the bound therefore follows from separate connected-component bounds, even if the original block state entangles those components.

At alpha=1/2 (4) simplifies to a *relative-spin bilayer* identity:

\[\boxed{W_B=-\sum_{i\in B}\mathbf S_i^{(1)}\cdot\mathbf S_i^{(2)}+\frac12\sum_{i<j\in B}J_{ij}(\mathbf S_i^{(1)}-\mathbf S_i^{(2)})\cdot(\mathbf S_j^{(1)}-\mathbf S_j^{(2)}).}\tag{6}\]

The bilayer is a **certificate representation, not an asserted physical substitute** for the Heisenberg system. Its larger two-copy Hilbert space deliberately relaxes the condition that a vector equal |psi> tensor |psi>; this can lower its minimum eigenvalue and weaken the bound. A positive operator certificate nonetheless remains rigorous in the required direction.

### The exact finite-geometry computation

For k=1,2,3,4,5, connected physical J1-J2 interaction clusters, modulo vertex relabeling preserving J=1 versus J=1/2, have respectively

\[\boxed{1,\ 2,\ 4,\ 15,\ 45\quad\text{distinct weighted graphs, totaling 67}.}\]

The enumeration grows a connected set by adjoining one of its eight NN/NNN lattice neighbours, translates it to a canonical origin, and quotients only by exact weighted-graph isomorphism. Every connected k-site support is reached inductively. Disconnected supports need not be separately enumerated by the additivity observation above.

**Certified matrix inequality (primary result):** for every connected weighted graph of <=5 sites, the rational 2-copy operator satisfies

\[\boxed{W_B+\frac{91}{200}|B|I\succ0.}\tag{7}\]

Every interaction coefficient and shift in the constructed matrices is rational. All 22 cases at k<=4 passed exact fraction-free Bareiss positive-definiteness tests in *every* 2-copy total-Sz sector, largest block 70x70. All 45 five-site cases passed separate exact integer Gram witnesses. Each five-site matrix restricted to total Sz=0 has dimension binomial(10,5)=252 and, after multiplying by 400, is integer. For each supplied integer lower-triangular R and scale s=2^18, verification explicitly constructs integer

\[E=s^2[400(W_B+(91/200)|B|I)]_{S_z=0}-RR^\mathsf T.\tag{8}\]

It checks all E_ii>sum_{j != i}|E_ij|; hence E is positive definite and the bracketed operator is a sum of PSD Gram and strictly positive diagonally dominant matrices. All arithmetic in this verification is integer, with explicit checked signed-64-bit overflow ceilings. The R matrices were *constructed* using approximate floating Cholesky but no floating eigensolver, convergence assumption or solver tolerance is used to *verify* their validity. In addition, SU(2) invariance of W_B means that every eigenvalue of its even-spin-number system occurs in the total-Sz=0 block: all irreducible total spin values are integers and each has a magnetic-zero vector. Consequently the verified positive zero-sector block certifies the entire operator.

The strongest unsuccessful nearby demand, `W_B+(9/20)|B| I >= 0`, is **false** on the physical four-spin 2x2-square motif; the integer Bareiss verifier returns a negative pivot. The successful -91/200 constant is a conservative threshold of this relaxation, not the exact optimum over k-producible physical states.

### Full physical consequence

Combining (2)--(7), every 5-producible N-spin density matrix obeys

\[\boxed{\operatorname{Tr}(H_{1/2}\rho)/(NJ_1)\ge-91/200=-0.455.}\tag{9}\]

The prior independently replayed original-H variational *upper* is < -0.46909, strictly below (9). Therefore every finite-volume ground state on sufficiently large compatible even periodic tori is **not 5-producible**; entanglement depth is >=6. The same uniform inequality survives thermodynamic limits, in the precise sense that a local-limit state cannot be an infinite-volume mixture/limit of 5-producible preparations with the same energy density. It does not say every set of six sites is genuinely entangled or force an extensive entanglement length.

The certified energy separation from the whole 5-producible convex set is at least

\[\delta_5/J_1>0.46909-0.455=0.01409\quad\text{per physical spin}.\tag{10}\]

This is a substantive assertion about the original strongly frustrated system. No field response, unknown susceptibility, spectral gap, global quantum marginal or orthogonal-dimer overlap metric was supplied as a premise.

## 4. Fully analytic sharp two-site benchmark and frustration interval

The exact k=2 case can be solved analytically with no replicas or numerical matrices. For any two-spin state, denote a=<S1>, b=<S2>, p=<P_triplet>=<S1.S2>+3/4. Define u=a+b, v=a-b. The triplet total spin has norm <=1, so |u|<=p. The difference spin connects singlet and triplet sectors with orthonormal Cartesian triplets; positivity of the off-diagonal singlet/triplet density block gives |v|²<=4p(1-p). Therefore

\[\boxed{\langle\mathbf S_1\cdot\mathbf S_2\rangle+\frac34\ge|a|^2+|b|^2+a\cdot b.}\tag{11}\]

At alpha=1/2, apply (1) and (11) to every pair. If a pair is a NN, its block functional is >= -3/4; if it has no bond, it is >= -1/2; interpolation covers internal couplings 1/2. An isolated spin contributes >= -1/4. Thus every 2-producible state obeys

\[\langle H_{1/2}\rangle/(NJ_1)\ge -3/8.\]

This bound is *sharp* on even square lattices: product nearest-neighbour singlet dimers gives exactly -3/8 per spin. This is an explicit control confirming that the k=5 result is not merely a restatement of the much easier exclusion of static dimers.

For 0<=alpha<=1, the minimum exchange-Fourier eigenvalue is -2-4|alpha-1/2|. Repeating the pair argument gives

\[e_{\text{2-producible}}/J_1\ge -3/8-\tfrac12|\alpha-1/2|.\tag{12}\]

An explicit physical four-spin singlet vector on a square (cyclic site order 1,2,3,4) has coefficients 2 on alternating 0101 and 1010 configurations and -1 on the other four two-up configurations, divided by sqrt(12). Its exact NN ring energy is -2 and sum of two diagonal spin correlations +1/2. Tiling this genuine four-spin wavefunction over the 2D lattice, with all cross-tile one-spin means zero, gives

\[e_\text{trial}(\alpha)/J_1=-1/2+\alpha/8.\tag{13}\]

This falls strictly below the 2-producible threshold for

\[\boxed{1/3<\alpha<3/5.}\tag{14}\]

Hence depth >=3 is rigorously unavoidable throughout that interval. The plain analytic four-site trial is too weak to establish the stronger depth-six conclusion: for that we genuinely use the original 16-spin certified physical trial, not an unconstrained numerical extrapolation.

## 5. Positive-temperature consequence; all entropy and preparation costs stated

For a finite-volume Gibbs state \(\rho_{\beta}=e^{-\beta H}/\mathrm{Tr}(e^{-\beta H})\), \(F_\beta=E_\beta-T S_\beta\) is minimized by the Gibbs state. A physical trial state with energy \(E_{\rm tr}\) provides \(F_\beta\le E_{\rm tr}\); the thermal entropy obeys \(S_\beta\le N\ln2\) (k_B=1). Thus

\[e_\beta/J_1\le e_{\rm tr}/J_1 + (k_BT/J_1)\ln2.\tag{15}\]

No assumed thermal gap, mixing time, local Gibbs oracle, or sign-free simulation is present in this argument. The *mathematical* witness works for all finite thermal states on the admitted finite tori; physical preparation/measurement remains an unperformed laboratory operation.

At alpha=1/2, using the independently verified 16-site tile upper bound < -0.46909:

\[\boxed{k_BT/J_1<\frac{0.46909-0.455}{\ln2}=0.0203275\ldots\quad\Longrightarrow\quad\text{Gibbs entanglement depth }\ge6.}\tag{16}\]

The weaker 2-producible threshold also gives depth >=3 whenever \(k_BT/J_1<(0.46909-0.375)/\ln2=0.135743\ldots\). Using only the transparent four-spin trial and (12), depth >=3 for the broader alpha interval (14) at

\[k_BT/J_1<\frac1{8\ln2}\begin{cases}3\alpha-1,&1/3<\alpha\le1/2,\\3-5\alpha,&1/2\le\alpha<3/5.\end{cases}\tag{17}\]

The threshold temperature is sufficient, not critical. No claim about a thermal phase transition, exotic spin-liquid order, or real material with specified exchange J1 is made.

## 6. Robust local observable consequence and an acquisition protocol

On a square torus there are 2N NN bonds and 2N NNN bonds; at alpha=1/2 their exchange-weight sum is 3N. Since \(\|\mathbf S_i\cdot\mathbf S_j\|_\infty=3/4\), for any actual ground state rho and every 5-producible comparison sigma,

\[\boxed{\frac1{3N}\sum_e J_e\|\rho_e-\sigma_e\|_1\ge\frac{0.01409}{(3/4)\cdot3}>0.00626.}\tag{18}\]

Thus the certified distinction is visible at the level of average physical two-spin reduced states, not only in an exponentially fragile global overlap. At finite T the numerator becomes \(0.01409-(k_BT/J_1)\ln2\), when positive. (The trace norm is the full norm \(\|\cdot\|_1\), without an extra factor 1/2.)

If a device prepares independent identical physical-lattice states, draw a bond with probability proportional to its physical positive exchange weight, choose a random Pauli axis x/y/z, measure the two-site Pauli product \(\xi=\pm1\), and report \(Y=\frac94\xi\). Then \(\mathbb E Y=e/J_1\) and |Y|<=9/4. Hoeffding gives

\[\Pr(|\overline Y-e/J_1|>\epsilon)\le2\exp[-n\epsilon^2/10.125].\tag{19}\]

With target margin half of the conservative ground separation 0.01409 and confidence 99%, this bound requires approximately 1,080,864 independently prepared samples. This does not include device fidelity, bond/axis readout calibration, correlated sampling, drift, or physical cooling; none was performed. The operation is a feasible-information *contract*, not a claim of a demonstration.

## 7. Necessity, limitations, failures and strongest informed alternatives

1. **Physical phase is still unresolved.** Entanglement depth >=6 rules out all mixtures of independent five-site blocks; a VBS, a QSL or a symmetry-breaking antiferromagnet may all satisfy it. There is no proof of long-range dimer correlations, gaplessness or small-field nonanalyticity. The central near-zero-field susceptibility obstruction of the earlier phase programme remains open.
2. **The k=5 cutoff is real.** The method entails exponentially growing 2-copy operators (4^k), combinatorially many lattice motifs, and large exact proof objects. Numerical reconnaissance of size six is not a certificate; depth >=7 has not been established. The -9/20 threshold fails exactly on one four-site motif; the attained -91/200 is conservative and not a certified optimum over physically 5-producible states.
3. **This is not a new general quantum marginal solver.** The new k-producible certificate never reconstructs an arbitrary global quantum state. Its two-copy relaxation can have unphysical copy-to-copy correlations; positivity is used only in a sufficient direction.
4. **Established physical methods remain stronger for energy and phase estimation.** Wang et al. (PRX 2024, arXiv:2604.01555v1) already give structured noncommutative SDP ground-state and observable bounds on large spin lattices, and demonstrate up to 16x16 in 2D. On the 10x10 frustrated finite torus their -0.510813 lower is much tighter for that *different finite-volume energy question*. Tensor-network/DMRG/NQS approaches report more accurate physical energies and correlation-based phase suggestions, though without automatically furnishing the uniform exact entanglement-floor operator proved here. This work does not beat their energy accuracy or runtime at equal resources.
5. **Energy entanglement witnesses and symmetric two-copy extensions are established.** Dowling, Doherty & Bartlett (2004) introduced the energy-entanglement-gap/temperature concept; Troiani & Siloi (2012) studied multipartite energy witnesses. Symmetric-extension hierarchies and replicated polynomial optimization are standard antecedents. What is new **within this research session** is the checked model-specific combination of (1), (4), all five-site physical motif inequalities, and the existing certified 16-spin upper witness to yield the depth-six ground and finite-T consequences. Historical priority, external verification, performance advantage and general novelty remain unestablished.
6. **Astra provenance does not silently supply a theorem.** The public source corpus was refreshed at main commit `64c8eb9bf413c9e76d6bcbd87bda70cf1aa43c28` (2 November). N130 concerns a very different collective dissipative Gibbs model; N198 addresses Casimir separability and retains a cross-copy nonmultiplicativity notice; N1077's planar tensor recognition retains its all-weight/speedup-failure successor notice. None supplies the present J1-J2 floor or a dimer-phase transfer. Earlier N1274 is a specific frustrated boson return obstruction, not a spin-state extension theorem. Full conditions were retained rather than promoting lexical similarity to applicability.

### Execution and bit costs

- k<=4: 22 connected weighted graphs, two-replica 2k-qubit integer matrices; total-Sz sectors up to dimension 70; exact Bareiss positive leading minors, Python standard library, ~2.1 s in this environment.
- k=5: 45 graphs; SU(2) reduces each 10-qubit proof to dimension 252 at total Sz=0; approximate floating Cholesky *proposes* integer Gram factors R, but the verifier independently rebuilds physical integer matrices and checks the exact Gram remainder with signed-64-bit overflow guards. 45 factors compressed to ~3.1 MB, independent proof replay ~15.8 s on this execution environment with NumPy. It rejects a tampered Gram factor. Signed-int arithmetic, 252^3 matrix work, and 45 distinct cases are not charged as free.
- Prior physical upper: 12,870 nonzero half-up 16-spin amplitudes, exact Rayleigh quotient, mixed spin-twirled physical tiled state; preserved source proof and checker independently replayed here. Numerical eigensolving was merely the **candidate constructor**.
- No 100-site structured SDP, state preparation, PEPS, QMC, real plasma/chemical interface or lab experiment was run for this result.

## 8. Relevant primary literature and exact source routes

- Wang, Jansen, Frérot, Renou, Magron & Acín (2026), *Scalable Ground-State Certification of Quantum Spin Systems via Structured Noncommutative Polynomial Optimization*, **arXiv:2604.01555v1**: https://arxiv.org/abs/2604.01555v1 (16x16 results and omission of state-optimality constraints in frustrated 2D); public implementation https://github.com/wangjie212/QMBCertify .
- Wang et al. (2024), *Certifying Ground-State Properties of Many-Body Systems*, PRX 14, 031006: https://doi.org/10.1103/PhysRevX.14.031006 .
- Dowling, Doherty & Bartlett (2004), *Energy as an entanglement witness for quantum many-body systems*, PRA 70, 062113: https://doi.org/10.1103/PhysRevA.70.062113 .
- Troiani & Siloi (2012), *Energy as a witness of multipartite entanglement in chains of arbitrary spins*, PRA 86, 032330: https://doi.org/10.1103/PhysRevA.86.032330 .
- Doherty, Parrilo & Spedalieri (2004), *Complete family of separability criteria*, PR A 69, 022308: https://doi.org/10.1103/PhysRevA.69.022308 ; compare symmetric-extension quantum witnesses, not an assumed new framework.
- Qian & Qin (2024), *Absence of spin liquid phase in the J1-J2 Heisenberg model on the square lattice*: https://doi.org/10.1103/PhysRevB.109.L161103 . Competing phase analyses exist; none is converted into an exact phase assertion here.
- Günal, Zhao & Keleş (Oct 2026), *Evidence of valence bond solid and quantum paramagnetism in J1-J2-J3*, https://arxiv.org/abs/2610.26135 , illustrates active dimer-response questions but relies on approximate pf-FRG flows.
- Astra preserved corpus original revision `51ce47ce39f976517d60e2f87bbe280b651f6056`, current examined revision `64c8eb9bf413c9e76d6bcbd87bda70cf1aa43c28`; canonical source route `https://github.com/harjassand/astra-research-knowledge/blob/64c8eb9bf413c9e76d6bcbd87bda70cf1aa43c28/00_START_HERE.txt` and targeted current packets under `knowledge/current/packets/`.

## 9. Final scientific conclusion

The continuation earns a physically connected and exactly checkable **six-spin entanglement-depth lower certificate** for a strongly frustrated 2D Heisenberg ground state, with a conservative positive-temperature extension and a strictly positive two-site local-observable distinguishability gap against every five-producible competitor. The mathematical bridge is the **exchange-square completion + two-replica local spectral lower bound**, on the original model, with all physical quantum overlaps retained. It replaces an unavailable global-extension/near-zero-response premise with a different target for which the indispensable operation has been constructed.

It does **not** identify a quantum phase or demonstrate a new generic solver or major scientific breakthrough. The unresolved next limit is whether the same representation can be strengthened to certify a phase-sensitive, extended observable (or larger entanglement depth) without its finite-cluster cost growing impractically; none is presumed.
