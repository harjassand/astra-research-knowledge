# Independent Astra research programme: proof-carrying envelopes for frustrated 2D quantum matter

**Research checkpoint:** 2 November 2026 (Australia/Brisbane). **Status:** mathematically reproducible finite-support certificates and exact thermodynamic bounds; **no new physical phase, algorithmic speedup, or civilization-scale breakthrough established**. This package is independent from earlier symmetry-response, nonlinear-response and fusion-scout programmes.

## A. Original scientific objective, input/output contract, and initial notebook

The independently selected north star is a useful, rigorous, thermodynamic-limit computation of phases and quantitative observables of frustrated two-dimensional quantum matter, without relying on a spectral gap, Monte Carlo sign cancellation, or exponentially large global wavefunctions. Inputs are the explicit local Hamiltonian and classical computational operations; no oracle supplies infinite-state marginals or phase labels. A successful ultimate output would certify the competing ground-state energies and order diagnostics with errors small enough to settle an important material or many-body mechanism.

`00_pre_retrieval_notes.md` was written **before** consulting Astra's direction catalogue or primary papers. The initial mechanism was an operator-dual local certificate glued by translation, plus a genuinely prepared/constructed variational upper state. The decisive missing operation was global *quantum marginal extension*: locally positive consistent reduced states do not automatically form a positive global state, especially on 2D loops. The initial falsifier explicitly requires comparison with Anderson cluster methods and quantum/SDP bootstrap at identical information and resources. This first note remains unchanged.

## B. Model and exact physical information

Let the square lattice have spin-1/2 operators `S_i`, `J1>0`, and `alpha=J2/J1`. The nearest-neighbour and diagonal next-nearest-neighbour Hamiltonian is

\[
H_\alpha=J_1\sum_{\langle ij\rangle} \mathbf S_i\cdot\mathbf S_j + \alpha J_1\sum_{\langle\!\langle ij\rangle\!\rangle}\mathbf S_i\cdot\mathbf S_j .
\]

Define `e_infty(alpha)` as the thermodynamic ground-state energy per site, obtained from periodic square tori with linear sizes divisible by four. Standard finite-range surface-energy estimates identify this with the ordinary infinite-volume density limit; none of the certificates requires correlation decay. All numerical values below take `J1=1`.

The high-frustration interval `[0.4,0.6]` is scientifically meaningful: finite PEPS simulations claimed a gapless spin-liquid regime (Liu et al., Science Bulletin 2022), whereas a high-accuracy DMRG/FAMPS study argued for a direct Neel-to-VBS transition around `alpha=0.535(3)` (Qian & Qin, PRB 2024). These are model-dependent competing interpretations, not conditions or conclusions of the present proof.

## C. Initial unfrustrated mechanism and exact one-sided proof

At `alpha=0`, put `A_i = S_i · sum_{j~i} S_j`. Combining the four outer spin-1/2's into total outer spin `j`, addition of the central spin gives minimum eigenvalue `-(j+1)/2 >= -3/2`, with `j≤2`. Each nearest-neighbour bond belongs to two stars, so `H_0=J1/2 sum_i A_i`. Hence `e_infty(0)≥-3/4`, while a Neel product state gives `e_infty(0)≤-1/2`.

A centre set `C={(x,y) in Z² : x+2y=0 mod 5}` is a perfect Lee-radius-one code: each lattice site is a centre or one of the four immediate neighbours of exactly one centre in `C`. Thus the five-star crosses, indexed by centres in `C`, partition the set of *stars*, though their physical 13-spin supports may overlap. Define `B_c=sum_{i in {c and four neighbours}} A_i`. If `B_c≥ℓ I`, summing inequalities gives `e_infty(0)≥ℓ/(2×5)`.

For ℓ=`-7096680/1000000`, `cross_exact_integer_witness.json` and `check_certificate.py` provide a **full exact-integer proof** on the 13-spin cross: all `2^13=8192` basis states, split by up-spin number. The bond graph is bipartite; after the Marshall diagonal sign gauge, the Hamiltonian is stoquastic (real nonpositive off-diagonals). For each spin-number sector, a strictly positive integer vector `f` satisfies componentwise `(B'_c−ℓ I) f≥0`. The ground-state transform gives

\[
\langle x,(B'_c-\ell I)x\rangle =
\sum_i \frac{[(B'_c-\ell I)f]_i}{f_i}x_i^2 +
\sum_{i<j}[-(B'_c)_{ij}]f_if_j\left(\frac{x_i}{f_i}-\frac{x_j}{f_j}\right)^2\ge0.
\]

All coefficients checked are integers after multiplying by the fixed denominators. This proves `e_infty(0)≥-0.709668` without a numerical eigensolver in the verifier. Numerical eigenvectors were used only to *find* a witness, never to establish positivity.

**Failure 1.** Two neighbouring star minima can be achieved simultaneously, so simply adding a second adjacent star does not improve the local `-3/2` per star bound. The more widely separated motif improves it, but this entire approach is an instance of the known Anderson-cluster lower-bound principle, not an independently novel global extension algorithm.

## D. Hard physical obstruction: antiferromagnetic frustration breaks the sign gauge

For `alpha>0`, the interactions form triangles (two square edges and one diagonal). Restrict to the single-down-spin sector. Spin exchange has positive real offdiagonal hopping along every such edge. The product of hopping signs around any triangular cycle is positive and invariant under diagonal phase redefinitions; three nonpositive real hoppings would have negative product. Consequently **no diagonal rephasing in that sector can make all off-diagonals nonpositive.** This does not rule out every possible nonlocal representation or approximate signed estimator. It specifically invalidates reuse of the previous stoquastic integer-positive-vector certificate.

An Astra source on paired-boson *return kernels* independently illustrates a related gauge-invariant frustrated-triangle sign obstruction, but has a different Hamiltonian, Hilbert space and observable. It is a warning against a false transfer, not a proof for our spin system. See Section J.

**Mechanism change:** replace sign-dependent Collatz inequalities with universally applicable **exact rational positive-definiteness** of a finite Hamiltonian block, verified using fraction-free integer elimination. This permits arbitrary real symmetric local sign structures at the cost of exponentially growing finite-cluster matrices.

## E. Exact Casimir decomposition and an analytic incompatibility theorem

At `alpha=1/2`, the spin addition identity on a four-site plaquette `p` gives

\[
P_p=\frac14\left[\left(\sum_{i\in p}\mathbf S_i\right)^2-3I\right]
=\frac12\sum_{\{i,j\}\subset p}\mathbf S_i\cdot\mathbf S_j.
\]

Each nearest-neighbour edge belongs to exactly two plaquettes, each diagonal edge to exactly one. Thus

\[
\boxed{H_{1/2}=J_1\sum_p P_p}. \tag{1}
\]

Since four spin-1/2 have total-spin squared eigenvalues `0,2,6`, `P_p≥-3/4`. This gives the basic global `e_infty(1/2)≥-3/4`.

**Two overlapping plaquettes have a strict joint penalty.** Take plaquettes meeting only at a common spin `s=1/2`, with total outer three-spin operators `X,Y`, having spins `j_X,j_Y∈{1/2,3/2}`. Their squared plaquette spins obey

\[
(s+X)^2+(s+Y)^2
=2s^2+X^2+Y^2+2s\cdot(X+Y).
\]

For a fixed resultant `R=|X+Y|`, the minimal spin coupling to `s` yields `2s·(X+Y)≥-(R+1)`, and `R≤j_X+j_Y`. Therefore

\[
(s+X)^2+(s+Y)^2\ge \tfrac12+j_X^2+j_Y^2\ge 1.
\]

Hence `P_p+P_q≥-5/4` for any such diagonal pair. A perfect pairing of plaquettes by diagonally adjacent centres proves

\[
\boxed{e_\infty(1/2)\ge -5/8=-0.625.} \tag{2}
\]

This result needs neither numerical computation nor local marginal compatibility assumptions.

## F. Exact 9-spin lower operator and continuous frustration interval

Group four elementary plaquettes whose lower-left corners are `(0,0),(1,0),(0,1),(1,1)`. Their combined operator `B` is supported on the 3×3 physical-site patch (nine spins). Every plaquette is in exactly one such group under translation of groups by two in both directions, so `H=sum_blocks B_block` and there is one block per four sites.

Define, in each fixed-up-spin sector, the **exact integer** matrix

\[
A_k=8(10^6 B_k+2332848 I).
\]

`verify_frustrated_bareiss.py` constructs this from bond multiplicities using integers and verifies *strict positive definiteness* in all sectors of dimensions

`1, 9, 36, 84, 126, 126, 84, 36, 9, 1`, totalling all 512 states.

The algorithm performs symmetric, fraction-free **Bareiss elimination**. At every step the pivot equals the next leading principal minor divided by the previous one; the division is asserted exact, and every pivot is strictly positive. Sylvester's criterion proves each real symmetric sector matrix is positive definite. Thus `B > -2.332848 I` and

\[
\boxed{e_\infty(1/2)\ge-2.332848/4=-0.583212.}\tag{3}
\]

`test_sharpness_and_failure.py` is an exact **negative control**: in the four-up-spin sector the stronger trial `B≥-2.332847 I` produces a negative principal-minor pivot. So

\[
\boxed{-2.332848 < \lambda_{\min}(B) < -2.332847}. \tag{4}
\]

The first inequality is strict because the verified matrix is positive definite. The second is implied by its negative minor and a direct sign test. **Further precision on this nine-spin block cannot materially improve the global lower bound.** Improving the science requires a different cluster, dual or global-compatibility mechanism.

For general `alpha`, the local operator is constructed by assigning weight `1/2` per appearance of a nearest-neighbour edge in the four plaquettes, and weight `alpha` per appearance of a diagonal edge. The same block-cover identity holds for all `alpha`. `verify_parameter_interval.py` proves, with exact integer elimination, these local bounds:

| `alpha` | local 4-plaquette ℓ | thermodynamic `e_infty(alpha)≥ℓ/4` |
| ---: | ---: | ---: |
| `2/5` | `-2.446632` | `-0.611658` |
| `9/20` | `-2.385720` | `-0.596430` |
| `1/2` | `-2.332848` | `-0.583212` |
| `11/20` | `-2.290033` | `-0.57250825` |
| `3/5` | `-2.259156` | `-0.564789` |

For any `alpha=(1−t)a+tb` between consecutive knots, `B(alpha)=(1−t)B(a)+t B(b)`. Since the PSD cone is convex, the exact inequality `B(alpha)≥[(1−t)ℓ(a)+tℓ(b)]I` holds for **every real `t∈[0,1]`**, not just finite sampled values. The piecewise-linear interpolation is consequently a rigorous lower envelope over the full interval `[0.4,0.6]`.

`check_geometry.py` independently checks NN and diagonal-bond multiplicities for 4×4, 6×6, and 8×8 periodic torus tilings; the general proof uses the same periodic combinatorial identity and is not contingent on the finite checks.

## G. Exact constructive thermodynamic upper bound

A lower energy certificate does not imply realizability. For a **separate** upper state, use a 4×4 open physical-site patch and a rational approximation `|v>` to its lowest spin-sector eigenvector. `upper_trial_L4.json` contains all 12,870 integer amplitudes in the half-up sector, the complete weighted bond list, and the exact integer numerator and denominator of its Rayleigh quotient for the open `J1-J2(1/2)` Hamiltonian. The state need not be the exact local ground state.

Let `rho=|v><v|`, and twirl it by the four collective spin rotations represented by `I`, `X^⊗16`, `Y^⊗16`, `Z^⊗16` to produce `rho_t`. This **preserves** all internal Heisenberg energies and gives `Tr(rho_t S_i^a)=0` at every site and for each component `a=x,y,z`. Tile the plane by independent copies of `rho_t` on disjoint 4×4 physical patches. Every cross-tile Heisenberg bond has expectation zero by product-state factorization. Thus the infinite-volume product mixed state has an **exactly evaluated** energy density:

\[
 e_\infty(1/2)\le \frac{\langle v|H_{\rm open,4\times4}|v\rangle}{16\langle v|v\rangle}
 = \frac{N_{\rm integer}}{8\,(16)\,D_{\rm integer}} 
 \approx -0.4690973093800669.
\]

This yields the rationally safe rounded bound `e_infty≤-0.46909`. `check_trial_upper.py` checks bond identities, amplitudes, normalization, exact integer numerator and denominator without NumPy/SciPy. Numerical eigensolving was used only to **find** a finite trial vector, not to verify its upper bound. Mixed states are valid variational states, and in principle this twirl can be replaced by a classical random ensemble of four fixed rotations; no physical apparatus is being claimed.

Combining (3) with this construction:

\[
\boxed{-0.583212\le e_\infty(1/2)/J_1\le-0.46909.}\tag{5}
\]

The interval width is `0.114122 J1`. It is **too wide** to decide between the disputed spin-liquid/VBS/critical phase interpretations. It is nevertheless fully independent of finite-size extrapolation and sign-free Monte Carlo, unlike an estimated thermodynamic energy.

## H. A physical observable corollary: exact plaquette total-spin and singlet-density constraints

From (1), every thermodynamic ground state at `alpha=1/2` satisfies

\[
\overline{\langle S_p^2\rangle}=3+4e_\infty/J_1.
\]

Equation (5) therefore implies the **certified density** interval

\[
\boxed{0.667152\le\overline{\langle S_p^2\rangle}\le1.12364.}
\]

Let `P_{p,0}` be the projector onto the total-spin-zero **subspace** of the plaquette (which has multiplicity two), so `P_{p,0}=(S_p^2−2I)(S_p^2−6I)/12`. The eigenvalues `0,2,6` show `2(I−P_{p,0})≤S_p^2≤6(I−P_{p,0})`; hence the average plaquette-singlet-subspace probability of any ground state obeys

\[
\boxed{0.43818\le\overline{\langle P_{p,0}\rangle}\le0.888808.}
\]

These are weak, but physical, observable bounds—not phase-identifying order-parameter bounds. They follow entirely from already-certified energy endpoints and an exact local spectral identity. They should not be mistaken for improved precision over the published many-body SDP observable certificates.

## I. Same-information, strongest-established-alternative comparison

**Same 3×3 cluster, same exact Hamiltonian, roughly same arithmetic resources.** The strongest straightforward comparator is the standard **Anderson local-cluster bound**, implemented using conventional diagonalization and an independently certified spectral enclosure. It obtains the same optimal local 3×3 bound to within `10^-6`. The present exact-integer Bareiss verifier helps with proof portability and the absence of numeric trust; it offers **no algorithmic advantage over a conventional certified cluster diagonalization**. The positive alternative has equal access to the local model, tiling, rational arithmetic and independently verified eigenvalue bounds.

**Stronger published SDP on a larger *finite* lattice.** Wang *et al.*, *Phys. Rev. X* **14**, 031006 (2024), Appendix A explicitly states the classical Anderson bound and develops structured NPA/noncommutative-polynomial SDP relaxations, combining them with variational bounds to constrain observables. For `alpha=.5` on a **10×10 periodic finite torus**, their Table XIII reports lower `-0.51462802` and best quoted DMRG upper `-0.4988` per site (~3.173% relative separation). These results are substantially tighter than our crude local envelope, though they refer to a **different mathematical target** (100-site periodic energy vs the *infinite-volume* bound) and demand substantially more resources. Their public implementation `wangjie212/QMBCertify` implements the model's actual J1-J2 structured NPA hierarchy using Julia, JuMP and MOSEK. We inspected its README and dependencies, but did **not** run it or verify its finite numeric SDP residuals. It would be misleading to claim that our method beats this established approach on practical physics.

**Stronger numerical large-system alternatives.** 2026 spatial-attention neural-network quantum states report a `20×20` frustrated square-lattice variational energy around `-0.496732(1)` at `alpha=.5`, with a further **extrapolated estimate** around `-0.49684(1)` (Viteritti *et al.*, arXiv:2602.02665). These much more informative results employ expensive variational sampling; the claimed error bars and extrapolations are not exact infinite-volume PSD certificates. High-accuracy DMRG/FAMPS and PEPS likewise access physical correlations and disputed phases that the current interval does not determine. QuSpin is an established open-source exact-diagonalization baseline, not a missing operation.

**No fair same-resource breakthrough.** Our exact integer checks take seconds for nine spins; the 16-spin variational candidate requires a 12,870-dimensional numerical sector, then an integer replay. The conventional comparator can use the same resources and achieve essentially the same result. Our lower proof's computational cost scales exponentially in local quantum support; the cost of globally consistent RDM recovery is not removed.

## J. Astra retrieval: pinned source conditions, valid and invalid transfers

**Pinned corpus revision:** `harjassand/astra-research-knowledge` commit `51ce47ce39f976517d60e2f87bbe280b651f6056`. Began at `00_START_HERE.txt`. Astra search was performed *after* the independent initial mechanism, primarily using operation-oriented TSV browses and source packets because GitHub's server code-search index returned no useful text hits. Topics included marginal compatibility, 2D many-body dynamics, positive operators, tensor contraction and spectral gaps. The repository did not replace the intended task with an archived branch narrative.

- `N1077` (and `U1077-local-quadratic-compatibility-without-global-field`) describes an exact compiler for generic **loopless planar trivalent binary rational tensor** contractions with nonzero hyperdeterminants and edge CP pairings. We read its governing `PROOF.md` lines 33–128 and parent `REVIEW.md`. Its Pfaffian tractability **does not** solve arbitrary 2D quantum-state compatibility, a frustrated spin energy, four-port positive gadgets, or noisy tensor inference. Rejected as an unsupported shortcut.
- `U1007-finite-graph-chern-underdetermination` constructs gapped 2-band systems with identical data on a finite embedded graph but different Chern number. It reinforces that a finite collection of local response/energy numbers is not a free certificate of global topology. Distinct input geometry and topological theorem; **not directly used** to prove our energy bound.
- `N1274-positive-paired-endpoints-without-positive-renewal` supplies a **different** bosonic trimer example where positive endpoints do not lead to a positive first-return kernel: a sign-frustrated triangle remains. We read source `.../paired_endpoint/PROOF.md` lines 65–190. Its explicit restrictions on number sector, hopping and return representation preclude transferring its quantitative bounds to the spin lattice. It supports making signed path failures explicit rather than assuming a positive representation.
- `N1214-graded-return-path-nonlinear-impurity-response` is restricted to a specially prepared eta-coherent Hubbard state and bounded local source. Its gradient/grade representation is **not** a generic frustrated ground-state representation. Existing symmetry/nonlinear-response work remains intact and unmodified.

Retrieval sharpened the negative-transfer tests and made it harder to overstate novelty; **no Astra result was silently used as a theorem for this Hamiltonian**.

Astra exact packet routes, all relative to the pinned Git revision: `knowledge/current/packets/N1077.json`, `U1077-local-quadratic-compatibility-without-global-field.json`, `U1007-finite-graph-chern-underdetermination.json`, `N1274.json`, `N1214.json`. Governed tensor source: `research/2026-10-23-fresh-programme/intake/capital-integrated-2026-10-23/updates/2026-10-27-compiled-physical-interfaces/source/tensor/originals/alternative/representation_operation_20261027/PROOF.md`. Signed-return source: `research/2026-10-29-physical-control-and-persistence/source/ultra0924/a_independent/paired_endpoint/PROOF.md`.

## K. Disposition, negative findings, and the truly missing invention

**What is earned:** independent derivation, a symbolic two-plaquette monogamy inequality, reproducible exact arithmetic for a frustrated 9-spin local block, a continuously valid thermodynamic energy lower envelope over `alpha∈[.4,.6]`, a separate 16-spin constructively tiled upper state, and elementary local spin/singlet-density corollaries. No physical state preparation, experimental measurement, universality or priority is inferred.

**What failed decisively:** (i) adjacent stars cannot improve their spectral sum; (ii) the Marshall/stochastic positive-vector method fails on sign-frustrated triangles; (iii) making the 9-spin PSD certificate more precise cannot improve its thermodynamic lower bound by meaningful amounts, as the exact negative control proves; (iv) a larger 3×3 plaquette-centre motif (16-spin support) numerically improved the bound only marginally (about `-0.579702` per site, **uncertified**); (v) strongest ordinary local/SDP alternatives already cover this class and can do more with serious budgets; (vi) energy and singlet-population bands do not identify order or topology.

**Next decisive primitive, *not yet constructed*:** a noncommutative, loopy quantum-marginal **extension-or-obstruction certificate** with controlled cost that turns overlapping 2D local density matrices into (a) a globally realized state, or (b) a quantitative, volume-extensive inconsistency witness, *without assuming exact quantum Markovity, a nonzero gap, or a nice sign basis*. Existing chordal/quantum-Markov completion results explicitly require extra trace/commutation conditions and do not supply this for general loopy 2D critical states. A promising but falsifiable development is to invent a hierarchy of *cycle-consistency residual operators* with a theorem bounding the global energy error in terms of paid, computable local residuals. The central theorem is missing; an SDPs-on-larger-patches campaign alone does not deliver it.

**Hard benchmark to continue:** the same `J1-J2` operator and information, no invented gap or precomputed thermodynamic state; match established SDP/NQS performance on a representative finite problem **at the same computational resources**, then obtain an independently verified *infinite-volume* interval narrow enough to discriminate phase hypotheses (target width on the order of `0.005 J1` or an order-parameter exclusion), or abandon this route. A trace/Markov or tensor gauge assumption must be *proved for the target*, not introduced by definition. Do not equate running a larger expensive fixture with solving this bottleneck.

## L. Reproduction and provenance

The files are all local research artifacts, **not** published to GitHub. The exact proof scripts use Python standard library only; numerical candidate constructors additionally use NumPy/SciPy. No GPU or external solver is required to replay the proof.

```
python check_geometry.py
python check_certificate.py cross_exact_integer_witness.json
python verify_frustrated_bareiss.py
python verify_parameter_interval.py
python test_sharpness_and_failure.py
python check_trial_upper.py upper_trial_L4.json
```

Files: `00_pre_retrieval_notes.md` (frozen hypothesis), `star_bound_explore.py`, `block_cover_explore.py`, `construct_certificate.py`, `cross_exact_integer_witness.json`, `check_certificate.py`, `frustrated_plaquette.py`, `verify_frustrated_bareiss.py`, `explore_parameter.py`, `verify_parameter_interval.py`, `test_sharpness_and_failure.py`, `check_geometry.py`, `construct_trial_upper.py`, `upper_trial_L2.json`, `upper_trial_L4.json`, `check_trial_upper.py`, this `RESEARCH_REPORT.md`.

## Selected primary sources and scientific software

1. Wang, Surace, Frérot, Legat, Renou, Magron & Acín, *Certifying Ground-State Properties of Many-Body Systems*, *Phys. Rev. X* 14 031006 (2024), DOI `10.1103/PhysRevX.14.031006`. Includes Appendix A Anderson bound and Appendix G finite-size J1-J2 benchmark. https://journals.aps.org/prx/abstract/10.1103/PhysRevX.14.031006 ; https://github.com/wangjie212/QMBCertify
2. Kull et al., 2024, renormalization-assisted quantum marginal relaxations: compare full paper before claiming distinct spectral/energy advantage. (Literature search source, not a premise in the exact proofs.)
3. Qian & Qin, *Absence of spin liquid phase in the J1-J2 Heisenberg model on the square lattice*, *Phys. Rev. B* 109 L161103 (2024). https://journals.aps.org/prb/abstract/10.1103/PhysRevB.109.L161103
4. Liu et al., *Gapless quantum spin liquid and global phase diagram*, *Science Bulletin* 67 (2022) 1034–1041, DOI `10.1016/j.scib.2022.03.010`. https://www.sciencedirect.com/science/article/pii/S2095927322001001
5. Viteritti, Rende, Sachdev & Carleo, *Approaching the Thermodynamic Limit with Neural-Network Quantum States* (2026), arXiv:2602.02665. https://arxiv.org/abs/2602.02665
6. QuSpin, open-source spin exact-diagonalization, https://github.com/QuSpin/QuSpin ; source J1-J2 example https://quspin.github.io/QuSpin/examples/example11.html
7. Hasik, publicly shared iPEPS J1-J2 states, https://github.com/jurajHasik/j1j2_ipeps_states ; PEPS model https://peps-torch.readthedocs.io/en/stable/models/j1j2.html
8. Lauritzen & Zwiernik, *The Marginal Problem for Density Operators* (2026), arXiv:2605.19453; extra trace condition for quantum Markov completion on chordal graphs. https://arxiv.org/abs/2605.19453
9. Astra corpus *pinned to* `51ce47ce39f976517d60e2f87bbe280b651f6056`: https://github.com/harjassand/astra-research-knowledge/tree/51ce47ce39f976517d60e2f87bbe280b651f6056

No claim of Zenodo evidence, a laboratory result, external peer review of this report or comparative computational speedup is made. The central unsolved global extension operation remains clearly exposed.
