# Independent construction audit: thermal loading of a 3D quantum memory

Date: 2026-11-05. Internal note for question selection. The external rival's new proposal was not inspected. The independent SK opening and its two exact counterexamples are preserved in learning_new.md.

## Verdict

The bounded-degree decoder-history polymer sampler has a valid abstract polynomial-time proof under explicit local constraints, uniqueness, and component-energy assumptions. A strengthened compiler now includes every physical syndrome by adding a complete constant-size base-validity factor. The soundness induction and finite-table construction below close the earlier bad-mass floor and do not reveal a new mathematical obstruction. This conclusion accepts the cited BDL decoder and cochain-map lemmas; it is not an independent verification of BDL's entire proof. Existing Code Swendsen–Wang and regular-matroid algorithms remain unresolved comparison gates: neither is proved applicable or inapplicable to the actual BDL matrices. An established novelty separation from these algorithms must not be claimed.

## Primary sources and scope

Balasubramanian, Davydova and Lin (BDL), arXiv:2605.10943v1, proves its lifetime result for the main random-embedding family. Its separate deterministic embedding lacks the full lifetime proof in v1. Section 1.3 leaves efficient initialization open; arbitrary perturbative Hamiltonian stability is not proved. Sections 4–5 supply finite-local decoder maps, alternating syndrome-weight contraction, and exponentially high thermal probability for the good event \(\sigma_2=0\).

Bergamaschi, Gheissari and Liu (BGL), arXiv:2507.10976v1, gives sector mixing under additional redundancy/connectedness conditions; BDL says its LDPC-metacheck hypothesis fails here. That excludes this theorem, not every sampler.

Hangleiter, Ju and Vazirani, *Code Swendsen-Wang Dynamics*, arXiv:2510.08446, gives efficient code-Gibbs sampling under the near-graphic/cographic condition below. Definition 8 and Corollary 15 were checked in v1; root separately checked v4.

Goldberg and Jerrum, arXiv:1010.6231 / SICOMP 42(3), 1132–1157 (2013), gives an FPRAS for ferromagnetic Ising partition functions on regular matroids.

- https://arxiv.org/html/2605.10943v1
- https://arxiv.org/html/2507.10976v1
- https://arxiv.org/html/2510.08446v1
- https://arxiv.org/abs/1010.6231

## 1. Exact classical-to-quantum consequence

Let \(V\) encode the unknown input into the ground code, and let \(E_s\) be the error representative specified by the decoder's logical frame. Define

\[
\operatorname{Enc}_p(\rho)=\sum_s p_s E_sV\rho V^\dagger E_s^\dagger.
\]

Distinct syndromes occupy orthogonal subspaces. For arbitrary entanglement with an external reference,

\[
\tfrac12\|\operatorname{Enc}_p-\operatorname{Enc}_q\|_\diamond
=\tfrac12\sum_s|p_s-q_s|=d_{\rm TV}(p,q).
\]

Hence a polynomial classical sampler for the syndrome Gibbs law, a ground-state encoder, and decoder-frame Pauli injection provide the thermal encoder needed by the memory theorem. Ground-state encoding alone does not inherit a theorem about a thermal logical sector. Waiting for thermalization requires a preparation estimate.

CSS X and Z compatibility conditions factor, because a product of X and Z stabilizers can equal identity only if both parts separately do. Under the specified additive stabilizer energy, their thermal laws factor too. Sample them separately and add their TV errors.

A full-Gibbs sampler is sufficient: read its syndrome, discard its logical sector, then load a fresh arbitrary logical input in the decoder frame. Logical randomization is **not** a reason to exclude Code SW or another full-Gibbs algorithm.

## 2. Abstract positive-history polymer theorem

Assume \(M\) history variables, alphabet size \(q\), distinguished zero, and a graph \(G\) of maximum degree \(\Delta\). Every local constraint scope must be a clique in \(G\), so this must be the constraint-primal graph, not merely the variable-factor incidence graph. Assume:

1. The all-zero tuple satisfies each constraint.
2. A valid history is unique for its physical top syndrome.
3. A complete base-validity factor, together with the cochain residual identities, ensures the top syndrome is physically admissible. Terminal zero is a sufficient special case, but is not required.
4. Energy is additive over nonnegative initial-syndrome contributions.
5. Each connected nonzero-support component \(\gamma\) has \(E_\gamma\ge a|\gamma|\), with fixed \(a>0\).

### Factorization

Erase all nonzero support except one connected component. Each constraint sees either its previous tuple or the all-zero tuple, because a constraint cannot meet two support components. Thus deletion preserves validity. Conversely, nonadjacent valid components recombine. Uniqueness prevents history multiplicity from altering physical syndrome weights. The resulting measure is exactly the hard-core polymer gas

\[
\pi(\Gamma)=Z^{-1}\prod_{\gamma\in\Gamma}w_\gamma,
\qquad w_\gamma=e^{-\beta E_\gamma}.
\]

### Enumeration and truncation

A canonical depth-first traversal of a size-\(r\) connected support takes \(2(r-1)\) steps. The number of labelled polymers through a fixed vertex is therefore at most \(\kappa^r\), with the loose convenient choice

\[
\kappa=(q-1)\max(2,\Delta)^2.
\]

Set \(x=\kappa e^{-\beta a}\), requiring \(x\le1/[8(\Delta+1)]\). Since

\[
\Pr(\gamma\in\Gamma)=w_\gamma Z_{\rm compatible}/Z\le w_\gamma,
\]

the large-polymer probability is at most \(M\sum_{r>L}x^r\). Choosing \(L=O(\log(M/\epsilon))\) makes this at most \(\epsilon\). The truncated measure is exactly the full measure conditioned on absence of larger polymers, so this is a TV bound. Enumerating all valid labelled supports up to \(L\) takes \(M\kappa^{O(L)}\), polynomial for fixed structural constants.

### Direct heatbath proof

Enumerate the \(K\) small polymers. Choose one uniformly at each step, setting it absent when blocked and otherwise present with probability \(w_\gamma/(1+w_\gamma)\). If \(K=0\), output the empty family.

The weighted Hamming metric

\[
d(A,B)=\sum_{\gamma\in A\triangle B}|\gamma|
\]

is a path metric: remove \(A\setminus B\), then add \(B\setminus A\). Its diameter is at most \(2M\). For two states differing only by \(\gamma\), updating \(\gamma\) merges them with certainty under a common heatbath bit. Incompatible births create disagreements of expected total weight at most

\[
\frac1K\sum_{\gamma'\not\sim\gamma}|\gamma'|w_{\gamma'}
\le\frac{(\Delta+1)|\gamma|}{K}\sum_{r\ge1}rx^r
\le\frac{|\gamma|}{4K}.
\]

Thus the contraction factor is at most \(1-3/(4K)\), and

\[
t_{\rm mix}(\delta)\le\frac{4K}{3}\log\frac{2M}{\delta}.
\]

Numerical heatbath probabilities need a total error budget across these steps; polynomial precision suffices. This proof requires no physical Glauber gap. Root's abstract sampler argument is accepted at this scope.

## 3. Strengthened all-syndrome compiler: final bounded audit

This section supersedes the earlier good-syndrome-only construction. Retain all base syndromes that are genuine coboundaries, rather than fixing the base syndrome to zero. The base is constant-size; one can stop at BDL's level 2 to match the modified decoder of Section 5.1.1, or use the original finite seed. Relabel the chosen base as level 0 for the following argument.

Use bounded-size, disjoint local syndrome blocks per scale. Derive each correction \(f_i\) as a deterministic local function of \(s_i\), rather than storing a generic computation transcript. Include both the coarse-output table constraints and the cochain residual identities

\[
s_i=\delta_i^1f_i(s_i)+F_{i-1}^{2}s_{i-1},
\qquad s_0\in\operatorname{im}\delta_0^1.
\]

The last condition is one complete finite base factor. Its entire scope must be included in the primal constraint graph. This increases structural constants but not their dependence on system size.

### 3.1 Soundness, completeness, and component closure

Suppose a history satisfies all constraints. Since \(s_0\) is a coboundary, write \(s_0=\delta_0^1e_0\). The cochain property gives the induction

\[
s_i=\delta_i^1\big(f_i(s_i)+F_{i-1}^{1}e_{i-1}\big)
\quad\text{when }s_{i-1}=\delta_{i-1}^1e_{i-1}.
\]

Every syndrome in the history is therefore physical. Each local table is now being evaluated on a physically realizable input, where it agrees with the chosen decoder. Its arbitrary extension on unrealizable local patterns cannot produce a spurious valid history. Conversely, each physical top syndrome has the chosen decoder history, with a physical base. Determinism makes that history unique. This is the desired exact bijection for the full syndrome law.

All-zero local tuples are valid once zero corrections and zero coarse outputs are chosen on zero inputs. The base factor also accepts zero. Clique completion of every factor scope therefore proves component deletion/recombination exactly as in the abstract theorem. An isolated component is a valid complete history; the same base-to-top induction establishes its physical admissibility. No separate failure-witness property is needed.

Every isolated component is consequently a genuine trajectory of the decoder, so the alternating contraction applies to it:

\[
\sum_i|s_i|\le4|s_{\rm top}|.
\]

For syndrome-only variables on disjoint blocks, each nonzero variable accounts for at least one nonzero syndrome bit. Hence

\[
|\gamma|\le\sum_i|s_i^\gamma|
\le4|s_{\rm top}^\gamma|,
\qquad E_\gamma\ge(J_{\min}/4)|\gamma|.
\]

The all-syndrome polymer measure is exact before algorithmic truncation. There is no omitted unstable-syndrome mass \(b_N\) in its sampling accuracy. The BDL unstable mass remains relevant to the storage lifetime theorem, but not to the initialization approximation floor.

### 3.2 Sparse degree-two cochain maps

Choose the unperturbed homological contractions blockwise. In the code-embedding complex, the perturbation \(g\) runs from the X block through Q to Z. The embedded coarse degree-two input lies in the terminal local Z cohomology block. Its representative therefore obeys \(gi=0\). With the source's Appendix A formula

\[
i'=i+h\Sigma i,
\qquad \Sigma=g+ghg+ghghg+\cdots,
\]

we obtain \(i'=i\) on that input. Consequently \(F^2\) is the local representative inclusion. For R_X, a coarse bit occupies the two local Z points. For R_Z, it is represented by one chosen point in the connected local \(Y_z\) block. The supports for distinct coarse checks lie in their corresponding local blocks; both row and column support bounds are constant. The coarse-map input embedding from the preceding complex must be the specific diagonal/inclusion used in the construction, not an arbitrary dense change of cohomology basis.

This inference was checked against the direction of the source's Eq. (38), the embedding maps of Sections 3.2.4/3.2.6, and Eq. (247). A bounded complex by itself is not a general reason for an arbitrary perturbation series to terminate; here the directional X-to-Q-to-Z structure supplies the bounded nilpotence. This audit uses that actual structure.

One must fix the representative maps and the local decoder tables consistently. In particular, an R_Z correction must move odd local parity to the same chosen point used by \(F^2\). The source's Theorem 4.6 explicitly allows this point inside its local block. Replacing \(F^1\) by unrelated lifts while silently retaining an old logical frame would be unjustified. It is safe to fix one coherent HPL choice and its associated decoder, or to use the compiler solely for the classical syndrome distribution and apply the separately fixed BDL logical-frame decoder at quantum injection. The sampled full syndrome law does not depend on the sampling certificate's choice of error representative.

### 3.3 Uniform finite-table construction

There is a direct construction that avoids an oracle for whether a local pattern admits a physical completion. Fix an ordering of the constant-size local coordinates and choose the lexicographically first correction satisfying the stated conditions, with zero first.

For R_X, on each local X block input \(u\), enumerate \(f_x\) satisfying

\[
\delta_x^1f_x=u,
\qquad\sum_{q\sim x}|g_{xq}^1f_x|\le|u|.
\]

If none exists, define the table value to be zero. Lemma 4.8 guarantees existence for every input arising in a physical syndrome. Form the locally updated Q syndrome and similarly choose \(f_q\) satisfying

\[
\delta_q^1f_q=u_q,
\qquad\sum_{z\sim q}|g_{qz}^1f_q|\le|u_q|.
\]

Lemma 4.12 supplies existence on physical inputs. After these two cleaning stages, define each coarse Z bit from one of the two residual Z points. The residual identity factor enforces equality of the pair and vanishing of residuals in the other blocks. These functions have the radius-one/radius-two dependencies in Definition 4.3.

For R_Z, the coarse bit is the parity of the local input \(u_z\). Choose the first solution of

\[
\delta_z^1f_z=u_z+(\operatorname{parity}u_z)e_{b_z},
\]

where \(b_z\) is the same representative point used in \(F^2\). The right side has even parity on a connected local graph, so a local solution exists. The zero input selects the zero correction.

All enumerations are bounded by a constant depending on the fixed subdivision parameter; the number of gadgets is polynomial. These are uniform finite procedures on the supplied combinatorial local complexes, not uncomputable prechosen lookup tables. A cruder generic alternative is to decide local-pattern extendability by binary linear algebra on the full syndrome image and evaluate the decoder on one completion; this is also polynomial if decoder evaluation is polynomial, but the direct bounded-block search is cleaner.

The source's correction lemmas are accepted here at their stated scope. This audit checked their input/output conditions and the ensuing compiler deduction; it did not independently prove every geometric inequality in BDL's 102-page argument.

### 3.4 Remaining qualifications

The proof still requires a fixed bounded local block partition and factor graph, with the base factor and every dependency included. Those conditions are explicit and mechanically checkable from the construction. One should not replace the syndrome-only representation by a generic gate transcript: that could add \(\log N\) inactive persistence overhead and change the energy bound. The base factor may increase \(q\) or \(\Delta\) substantially, and those constants must enter the cooling and runtime estimates.

At this checkpoint I find no fatal gap in the strengthened all-syndrome deduction under the stated BDL lemmas. The unresolved novelty comparison with Code SW and regular matroids remains unchanged.

## 4. Code SW: the actual comparison condition

For \(h\in\mathbb F_2^{c\times n}\), the primal condition requires a graph incidence matrix \(g\) on the **same check-coordinate set** with

\[
\ker(h^T)\subseteq\ker(g^T),\qquad
\dim\ker(g^T)-\dim\ker(h^T)\le\Delta.
\]

The dual condition substitutes \(\operatorname{col}(h)\) for \(\ker(h^T)\). Polynomial mixing follows for \(\Delta=O(\log n)\). The graph need not respect physical locality.

None of these properties excludes that theorem: one logical qubit; non-LDPC metachecks; Tanner square complexes; a nonconstant sheaf; slow ordinary thermalization; or logical randomization by a full-Gibbs sampler.

BDL's preserved \(H^1\) controls logical qubits, whereas Code SW concerns end-space relation kernels. R_X adds local top-cohomology relation spaces and doubles top check coordinates. Hence its Code SW defect cannot simply be identified with the logical dimension.

### Exact counterexample: one logical qubit does not bound either defect

Let \(h_F\) be the \(7\times3\) matrix whose rows are all nonzero binary triples. Take \(m\) disjoint three-qubit blocks with these seven Z checks per block, plus one untouched qubit; there are no X checks. This is a bounded-LDPC CSS family encoding exactly one qubit.

The relation space \(S=\ker h_F^T\) is the \([7,4,3]\) Hamming code. If it were a graph cycle space, incidence rank would be three. Minimum cycle weight three rules out loops and parallel edges, so such a graph has at most \(\binom42=6\) edges, contradicting seven.

The dual \(S^\perp=\operatorname{col}(h_F)\) is the \([7,3,4]\) simplex code. A representing graph would have incidence rank four. Its cycles all have even length, and it has no loops/parallel edges; it must be simple and bipartite. At effective rank four such a graph has at most six edges. Disconnected components cannot increase this maximum, by summing their rank-constrained bipartite bounds.

If a graphic cycle supercode \(T\) contains \(S^{\oplus m}\), restrict it to each seven-coordinate block. Restriction is again a graph cycle space containing \(S\). Equality is impossible, so every block requires at least one additional dimension. Since these restrictions have disjoint support,

\[
\dim T-\dim(S^{\oplus m})\ge m.
\]

The same argument for \((S^\perp)^{\oplus m}\) gives the dual lower bound. Thus both Code SW defects are at least \(m\), despite bounded LDPC and one logical qubit. This diagnoses the invalid inference; it does not establish that BDL contains these blocks.

### Partial structural progress on actual BDL

For R_Z acting on Z-check relations, local transposed cellular incidence forces the new relation to be constant on each connected local \(Y_z\) vertex block; gluing imposes the previous relation. The relation space is therefore the old one with each coordinate repeated over its local block. Repetition preserves graphic cycle spaces by subdividing edges and graphic cut spaces by adding parallel edges. This step supplies no obstruction.

The difficult step is R_X for Z checks, and dually R_Z for X checks, where added local top-cohomology relations and gluing must be classified. It is not known in this audit whether these spaces admit graph representations within logarithmic defect. One Fano/Fano-dual minor excludes exact regularity but does not alone exclude \(O(\log N)\)-defect approximation; one needs repeated independent obstructions or a quantitative rank-distance argument. No such BDL argument has been established.

## 5. Regular-matroid FPRAS is a second comparison gate

Even excluding near-graphic/cographic structure would not by itself establish an unavailable operation. If the actual check row matroids are regular, Goldberg–Jerrum's FPRAS provides a polynomial sampling route.

Use the positive random-cluster partition function

\[
Z_M=\sum_{A\subseteq E}\gamma_A2^{-r_M(A)},
\qquad\gamma_A=\prod_{e\in A}\gamma_e,\quad\gamma_e\ge0.
\]

Conditioning edge \(e\) absent contributes \(Z_{M\setminus e}\); present contributes \(\gamma_e2^{-r_M(e)}Z_{M/e}\). Regularity is preserved by deletion and contraction. Approximate both nonnegative masses to relative error \(O(\epsilon/c)\), choose that conditional bit, and recurse. A coupling over the \(c\) choices gives TV \(O(\epsilon)\). The random-cluster/code coupling then samples uniformly from the kernel of retained checks using Gaussian elimination.

Therefore regularity is a concrete sufficient condition for the desired classical sample. Whether BDL's alternating replacements preserve it is unresolved here. This must remain an explicit immediate comparator test, not be dismissed from the sheaf terminology.

## 6. Physical and accuracy accounting

The sufficient sampler temperature is explicit:

\[
\beta a\ge\log\kappa+\log(8(\Delta+1)).
\]

It may be colder than the temperature range established for the memory itself. Fixed \(\ell\) makes \(q,\Delta,C\) asymptotic constants, but \(q\) can be exponential in the constant local block size, and BDL's proved embedding constants are very large. The enumeration exponent scales with \(\log\kappa/\log(1/x)\). A polynomial theorem is therefore not evidence of a practical device or moderate resource overhead; explicit constants and the increased cooling requirement must remain visible.

The classical sampler, ground-state Clifford encoder, routing, and decoder-frame injection all have execution costs. Polynomial graph computation does not imply small Euclidean circuit depth. Preparation requires initialized ancillas, calibrated operations, and protection of the input while it is loaded. The classical sample can be generated before the input arrives; protection during quantum handoff and encoding is still a paid resource.

Use the lifetime theorem only at its specified stabilizer-Hamiltonian and bath conditions. Classical precision, sampler TV, preparation faults, and readout faults must enter one channel-error budget. Arbitrary static noncommuting Hamiltonian uncertainty is outside the cited BDL v1 theorem. Reuse requires unloading, resetting/repreparing, and paying preparation costs again unless a reusable cycle is separately proved.

## 7. Preserved thermal-repair warning

For the earlier postselected strong-local-thermal-repair idea, a failed weak filter generally leaves the original Gibbs-path family. A repair theorem must specify the outcome conditioning and the dependence on inverse success probability or operator condition number. Undoing every failure and retrying cannot implement the normalized action of an arbitrary nontrivial filter as a deterministic channel. An inverse-filter restoration has a residual branch, controlled by spectral spread; weak steps do not automatically make its accumulated probability vanish. This is a distinct issue from recovery of an unconditioned Gibbs state.

## 8. Positive commuting coupling disorder: audited extension

This extension uses the same admissible deterministic decoder for the polymer certificate and the protected logical frame, including the source's small-error guarantee at the constant-size base. Let the actual Hamiltonian be

\[
H_J=\sum_a J_a\frac{I-S_a}{2},\qquad
0<J_{\min}\le J_a\le J_{\max}<\infty,
\]

on the same known commuting stabilizer checks \(S_a\). Thus a violated check has energy \(J_a\), not \(2J_a\). Constants and calibration factors below use this convention. This covers inhomogeneous positive coefficients on the same checks; it does not cover perturbations of the check operators, additional arbitrary commuting logical terms, or general coherent perturbations.

### 8.1 Weighted unstable-mass bound from full polymer factorization

Use one binary variable per syndrome bit at each scale, with the complete finite base factor in the primal graph. Then a polymer's size is exactly the number of nonzero syndrome bits in its isolated history. If it contains a nonzero bit at base level 2, physicality of the isolated history and alternating contraction imply

\[
|s_{\rm top}^\gamma|\ge2^{k-1}|s_2^\gamma|
\ge 2^{k-1},\qquad |\gamma|\ge|s_{\rm top}^\gamma|.
\]

The count of contracting steps from level \(2k\) down to level 2 is \(k-1\). If one instead counts block variables containing at most \(B\) syndrome bits, the last inequality must be replaced by \(|\gamma|\ge|s_{\rm top}^\gamma|/B\), and the tail threshold becomes \(\lceil2^{k-1}/B\rceil\). The exponent remains stretched exponential for constant \(B\), but the unmodified numerical threshold is justified by bit variables.

For arbitrary positive coefficients,

\[
E_J(\gamma)=\sum_aJ_as_{{\rm top},a}^\gamma
\ge J_{\min}|s_{\rm top}^\gamma|
\ge\frac{J_{\min}}4|\gamma|.
\]

The Gibbs activities still factor exactly over polymers: disjoint history components have disjoint top-syndrome supports. With \(x=\kappa\exp(-\beta J_{\min}/4)<1\), the rooted count and \(\Pr(\gamma\text{ present})\le w_\gamma\) give

\[
\Pr_J(s_2\ne0)
\le M_{\rm base}\sum_{r\ge2^{k-1}}x^r
=\frac{M_{\rm base}x^{2^{k-1}}}{1-x}.
\]

There is no system-size prefactor in this union bound beyond the fixed number of base bits. Summing the two CSS sectors gives twice this expression when using common upper-bound constants. This is uniform over all coefficients in the stated interval. Since \(N\) grows by a fixed factor per construction level, the result is \(\exp(-cN^\eta)\) for some fixed positive \(c,\eta\). The sampler can use the stronger earlier condition \(x\le1/[8(\Delta+1)]\).

### 8.2 Consequence for actual weighted dynamics

The dressed logical observables and the good-base-syndrome projector commute with every stabilizer, hence with \(H_J\). Their protection condition depends on the decoder and error operators, not on the numerical coupling strengths. BDL Theorem 2.6 therefore applies to an actual bath generator \(\mathcal L_J\) whose Gibbs stationary state is that of \(H_J\), provided its jump operators belong to the protected error class. In its stated statewise trace-norm convention,

\[
\|\Phi_{J,t}\operatorname{Enc}_J(\rho)
-\operatorname{Enc}_J(\rho)\|_1
\le8\|\mathcal L_J\|_1\,t\,p_{\rm bad}(J).
\]

For Davies-type frequency resolution of a protected local operator, the extra spectral projectors of \(H_J\) commute with the dressed observables and the good projector, so frequency resolution preserves the required protection. One should state the jump class or this argument rather than claiming arbitrary Gibbs-stationary dynamics are protected.

An exponential lifetime in fixed physical time units additionally needs a uniform bound \(\|\mathcal L_J\|_1\le\operatorname{poly}(N)\), or an explicitly retained bath-rate factor. Positive bounded couplings alone do not prevent arbitrary rescaling of the bath generator. Under bounded local bath rates this is the usual polynomial prefactor. The weighted unstable-mass estimate supplies the exponential factor.

The source's displayed theorem is statewise for a single logical qubit. A conservative reference-preserving bound follows by expanding a joint input in the four qubit Pauli operators: if the statewise trace-norm bound is \(\alpha\), the joint trace-norm bound is at most \(4\alpha\). Thus one safe half-diamond storage bound is \(16\|\mathcal L_J\|_1t\,p_{\rm bad}(J)\). A sharper existing conversion may improve this universal constant without changing the consequence.

### 8.3 Calibration is an initial-state error for the actual weighted theorem

Write \(\theta_a=\beta J_a\) and \(\widehat\theta_a=\widehat\beta\widehat J_a\). Both syndrome laws live on the same compatibility space. Interpolate \(\theta(t)=\widehat\theta+t(\theta-\widehat\theta)\), and set \(X(s)=(\theta-\widehat\theta)\cdot s\). Then

\[
\partial_tp_t(s)=-p_t(s)(X(s)-\mathbb E_tX),
\]

and \(\operatorname{range}X\le\sum_a|\theta_a-\widehat\theta_a|\). The mean absolute deviation of a bounded random variable is at most half its range, giving

\[
d_{\rm TV}(p_\theta,p_{\widehat\theta})
\le\min\left\{1,\frac14\sum_a
|\beta J_a-\widehat\beta\widehat J_a|\right\}.
\]

The orthogonal-syndrome identity gives exactly the same encoder half-diamond calibration bound. Evolve both initial states under the **actual** \(H_J,\mathcal L_J\); channel contractivity propagates this preparation error without a factor of storage time. Add the weighted storage bound, sampler error, and physical implementation errors. This addresses calibration against the actual weighted Hamiltonian rather than comparing its long dynamics to a nominal unweighted model.

The estimate specifies required information, not a free calibration procedure. A worst-case total budget \(O(\epsilon)\) across \(O(N)\) checks requires average dimensionless coefficient error \(O(\epsilon/N)\). The actual experimental access and precision cost must be paid. Use a conservative positive lower bound satisfying the cooling condition for the actual and sampled coefficient vectors. The extension supplies no guarantee for uncertainty in noncommuting operator terms.
