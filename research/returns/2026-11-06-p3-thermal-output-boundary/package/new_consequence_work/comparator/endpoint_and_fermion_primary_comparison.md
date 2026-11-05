# Primary comparison for the next consequence

Research date: 2026-11-05. This note preserves the earlier bounded-factory construction without re-auditing it. It compares two new questions at their actual apparatus scopes. It records a literature comparison, not a claim of priority.

## Recommendation

The strongest current target is the **physical endpoint obstruction for finite-temperature Gibbs delivery**, provided it includes the planar, bounded-degree, product-ground, uniformly gapped family and the connected amplification against arbitrary correlated upstream preparation. The elementary inverse-channel criterion is established precompensation mathematics. A newly identified close primary, Pettinari arXiv:2610.41871v2, already implies bare exponential local endpoint fragility by an elementary bridge. The substantive addition must therefore be the positive, uniformly gapped product-ground construction and the connected global delivery obstruction that survives unlimited upstream computation, entanglement, preparation time, and active error correction.

The fermionic parity route has an important limitation: its elementary lightcone argument applies to nonadaptive local channels/circuits. Allowing local measurements and long-range classical feedforward admits fermionic entanglement swapping. It therefore does not establish a limitation of the full measured-factory apparatus without additionally charging classical communication latency and the quantum storage needed while outcomes travel.

## A. Endpoint obstruction: closest primary results

### General quantum error precompensation

Chengjie Zhang, Liangsheng Li, Guodong Lu, Haidong Yuan, and Runyao Duan, **Quantum error pre-compensation for quantum noisy channels**.

- Primary full text: <https://arxiv.org/pdf/2309.01434>.
- Journal: Physical Review A 106, 042440 (2022), <https://doi.org/10.1103/PhysRevA.106.042440>.
- Actual result: invert a specified finite-dimensional channel where possible, test positivity of the preimage, and use semidefinite optimization for the best achievable fidelity when exact inversion fails. The paper explicitly permits nonexistence of an exact physical preimage.
- Consequence for the present work: neither inverse feasibility nor the existence of a separating witness should be presented as new. The missing many-body issue is whether fixed local noise admits a size-independent feasibility margin and what happens for extensive output delivery. The paper does not provide the planar gapped family, a dimension-sensitive radius law, or a strong converse under correlated upstream preparations.

### Complex-time locality and its failure in two dimensions

Gabriel Bouch, **Complex-Time Singularity and Locality Estimates for Quantum Lattice Systems**, arXiv:1011.1875; Journal of Mathematical Physics 56, 123303 (2015).

- Primary full text: <https://arxiv.org/pdf/1011.1875>.
- Main theorem, PDF p. 2: a translation-invariant nearest-neighbor interaction on the square lattice, bond norm one, and a one-site observable have complex-time evolution whose norm diverges along growing square volumes at sufficiently large fixed imaginary time. The displayed sufficient threshold is **4^21**, not 4/21.
- Section 6 constructs rooted lattice trees with many admissible growth orders. Section 7 uses oriented two-site Pauli interactions and a single-site Pauli observable.
- Theorem 3.1 also gives uniform one-dimensional complex-time locality estimates. Finite-range one-dimensional interactions retain the all-complex-time conclusion associated with Araki. One must not extend this statement unchanged to arbitrary exponentially decaying interactions.
- Actual comparison: Bouch already supplies a qualitative two-dimensional failure of a size-uniform local-noise preimage radius after the elementary channel bridge. It does not supply the proposed positive, frustration-free Hamiltonian with a unique product ground state and a uniform spectral gap, nor the raw-delivery strong converse.

### Closest primary: weak Gibbsianity and a direct endpoint corollary

Lorenzo Pettinari, **A Finite-Range, Translation-Invariant Counterexample to Weak Gibbsianity**, arXiv:2610.41871v2, 2 November 2026.

- Primary: <https://arxiv.org/pdf/2610.41871v2>.
- Full text inspected: `new_consequence_work/control/weak_gibbs_2610_41871.pdf` and its text extraction. Web HTML/PDF retrieval returned a service error, but the primary PDF was available in the shared source cache.
- The paper uses the translation-invariant square-lattice facilitated interaction \(H=J\sum_{i\sim j}^{\rm ordered}n_iX_j\), with the convention \(\rho\propto e^{+\beta H}\). Its vacuum lies in the kernel; the paper does not claim it is a unique gapped ground state.
- Theorem 1.2 proves exponential-in-area failure of operator-order comparison between infinite-volume and finite-volume Gibbs states. Lemma 2.5 bounds spanning-tree growth-order weights on full squares. Remark 2.8 provides a finite-volume version comparing the all-up event with the event that only one boundary site is unrestricted.

Here is the explicit operational bridge, which should be credited as an immediate corollary of that primary. Let \(Y=X\cup\{r\}\), \(|\Omega\rangle\) be the all-up vector, \(|r\rangle=X_r|\Omega\rangle\), and set

\[
b=\langle\Omega|\rho_Y|\Omega\rangle,
\qquad a=\langle r|\rho_Y|r\rangle.
\]

The unrestricted-boundary projector is the sum of these two rank-one projectors. The displayed finite-volume inequality of Remark 2.8 gives, along its square sequence and at its fixed sufficiently low temperature,

\[
a+b\ge e^{c|X|-2J\beta}b.
\]

If \(\rho_Y=\mathcal K_p(\tau)\) for a physical state \(\tau\), evaluating \((1-p)\rho_Y-pX_r\rho_YX_r\succeq0\) on \(|\Omega\rangle\) forces

\[
p\le\frac{b}{a+b}\le e^{2J\beta-c|X|}.
\]

Therefore **the bare exponential raw-port threshold is already accessible from Pettinari's theorem**, without the present positive Hamiltonian. Independent-cell amplification can then be supplied by the general channel-image witness argument. The stronger current claim is the preserved product ground state and gap, explicit geometry, and the connected amplifier; it should not be sold as discovering facilitated thermal amplification or exponential operator-order separation for the first time.

The square-tree lemma also offers a compatible improvement to the current family's geometry: add positive diagonal terms to a positive-path facilitated Hamiltonian while retaining the path-count lower bound. This extension needs its own explicit Hamiltonian, norm convention and proof; the existing primary's \(e^{+\beta H}\) convention cannot simply be renamed a positive, gapped physical Hamiltonian.

David Pérez-García and Antonio Pérez-Hernández, **Locality Estimates for Complex Time Evolution in 1D**, Communications in Mathematical Physics 399 (2023).

- Primary full text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC10113381/>.
- Publisher: <https://doi.org/10.1007/s00220-022-04573-w>.
- This is a useful source for the precise finite-range versus exponentially decaying interaction distinction. The latter setting has an analyticity strip controlled by the interaction-decay rate; it is not an unrestricted all-temperature theorem by definition.

### Positive operator-growth paths and facilitated quenches

Xiangyu Cao, **A statistical mechanism for operator growth**, Journal of Physics A 54, 144001 (2021).

- Primary full text: <https://arxiv.org/pdf/2012.06544>.
- The paper proves lower bounds on high-frequency moments for two-dimensional quantum Ising models, with a modified one-dimensional behavior, using nonnegative path expansions in Pauli-operator space. This is a close rigorous mechanism precursor for imaginary-time amplification. Its theorem concerns operator growth and spectral tails, not delivery through a noisy physical endpoint.

Xiangyu Cao, **Quantum quenches that resemble operator growth**, Physical Review B 114, 204310 (2026).

- Primary full text: <https://arxiv.org/html/2605.23874v3>.
- DOI: <https://doi.org/10.1103/4k2f-xvq3>.
- The setup uses local terms annihilating a product state, but calls that state a *false vacuum* because it generally lies in the bulk of the spectrum. Its main local example is the one-dimensional East-West Hamiltonian \(\sum_j X_j(n_{j-1}+n_{j+1})\). Its growth-quench hypothesis and localization analysis are distinct from a uniform gap and a positive product-ground Hamiltonian. No noisy Gibbs-delivery obstruction was located there.

### Gibbs recovery is a different ordering of operations

Chi-Fang Chen, **Note on Strong Quantum Markov Properties**, arXiv:2605.02877.

- Primary full text: <https://arxiv.org/html/2605.02877v1>.
- The paper characterizes recovery after local postselected measurement, under the relevant clustering and approximate detailed-balance assumptions, and derives repeated measurement/recovery consequences.
- This does not bypass an unavoidable terminal delivery channel. Recovery after that channel changes the endpoint contract; if recovery itself is followed by the same final channel, the endpoint-image obstruction remains. The distinction is operational order, not the computational strength of the recovery method.

## B. Concrete deductions earned by the endpoint construction

**Final-result update.** The elementary beta>64 Taylor bound retained below is a valid earlier estimate, not the governing temperature condition. The completed Perron witness gives the connected strong converse at beta=12, with A=96e sqrt(2), g=18-2 log A=6.1781564365... and delta as in the governing note. The separate independent audit also proves the fixed-global-accuracy precision law with q=52 and alpha=0.1714076087... .

The following deductions use the parent construction, not claims found verbatim in the sources above. For \(\rho=e^{-\beta H}/Z\), local Hermitian involution \(P\), and \(0<p<1/2\), define

\[
\mathcal K_p(\tau)=(1-p)\tau+pP\tau P.
\]

Its exact physical preimage exists precisely when

\[
\rho\succeq\frac{p}{1-p}P\rho P,
\qquad
p\le \frac{1}{1+\|e^{\beta H/2}P e^{-\beta H/2}\|^2}.
\]

The parent family is

\[
H=\sum_v n_v+\frac12\sum_{u\to v}n_u(I+X_v),
\]

on an explicitly subdivided planar binary H-tree. Every term is positive, the vacuum is the unique zero-energy state, and \(H\succeq\sum_v n_v\) gives gap at least one. The claimed and separately audited growth bound is

\[
\|e^{\beta H/2}X_o e^{-\beta H/2}\|
\ge(\beta/64)^{N-1}.
\]

For fixed \(\beta>64\), the sufficient obstruction is exponential in the **physical number of sites**. The embedding cost and every subdivision site must remain counted. This is a nonuniform planar family, not a translation-invariant square-lattice model unless an additional construction proves that property.

An additional useful separation follows without a new apparatus assumption. Since only the root field and its at-most-two outgoing terms change under \(P=X_o\),

\[
\|PHP-H\|\le 3,
\qquad
D(P\rho P\|\rho)
=\beta\operatorname{tr}[\rho(PHP-H)]\le3\beta.
\]

Yet

\[
D_{\max}(P\rho P\|\rho)
=2\log\|e^{\beta H/2}P e^{-\beta H/2}\|
\ge2(N-1)\log(\beta/64).
\]

Thus bounded local energy cost and bounded ordinary relative-entropy disturbance do not control endpoint feasibility. The ground-state gap and product ground state do not repair this gap between average and worst-direction behavior. These properties do **not** by themselves prove absence of finite-temperature phase transitions or uniform thermal clustering.

There is an even more direct local/global separation. The root occupation commutes with this Hamiltonian, so

\[
H=|0\rangle\langle0|_o\otimes H_0
 +|1\rangle\langle1|_o\otimes(H_0+V),
\qquad
V=I+\frac12\sum_{v:o\to v}(I+X_v),
\qquad I\preceq V\preceq3I.
\]

Write \(Z_a=\operatorname{tr}e^{-\beta H_a}\). Eigenvalue monotonicity gives \(e^{-3\beta}\le Z_1/Z_0\le e^{-\beta}\), even though matrix exponentiation is not operator monotone. The smaller root-marginal eigenvalue therefore obeys

\[
\frac1{1+e^{3\beta}}\le q_o=\frac{Z_1}{Z_0+Z_1}
\le\frac1{1+e^\beta}.
\]

The isolated root marginal has an exact bit-flip precompensation radius \(p\le q_o\), uniformly positive in volume. The correlated Gibbs target can nevertheless have exponentially vanishing radius for the very same root noise. Thus even uniform local mixedness and bounded conditional energy change fail to certify the required global apparatus channel.

The strong converse is operationally essential: exact inverse negativity can otherwise occur in a very small spectral sector. The parent/control construction now connects the cells by a positive nearest-neighbor classical spin chain, with no long links and bounded degree. Conditional on the connector bits, the cells have independent Gibbs states for \(H+h n_o\), with bounded \(h\ge0\). The same root-sector witness margin remains valid uniformly over these fields. This is the interface that upgrades independent-cell amplification to a genuinely connected family; its details belong to the separately audited construction. Conditioning on classical connectors does not restrict the adversarial upstream state, which remains arbitrary.

The amplification must retain its cell size, witness separation, number of repeats, connectors, and physical volume. Its force is a foundational impossibility even against unlimited upstream resources; no useful laboratory threshold or near-term energy advantage follows merely from the asymptotics. The root-marginal and ordinary-relative-entropy bounds above are for the unconnected cell; added root fields increase their bounded constants accordingly.

## C. Fermionic route: already-known geometry and an adaptive bypass

### The current ideal source already keeps a nonlocal resource

Saúl Pilatowsky-Cameo, Georgios Styliaris, Ainesh Bakshi, and Daniel Malz, **One-dimensional quantum Gibbs states in constant circuit depth**, arXiv:2609.35973.

- Primary: <https://arxiv.org/html/2609.35973v1>.
- Its fermionic analogue uses bounded-depth local parity-preserving circuits acting on **Gaussian states**, not on products of bounded physical fermion seeds. Appendix E constructs a generally nonlocal Gaussian pairing source after parity projection. Consequently, a lower bound charging creation of that source would not contradict the theorem. The theorem itself already recognizes that its fermionic source differs from the spin block-product source.

Gilles Parez and William Witczak-Krempa, **The Fate of Entanglement**, SciPost Physics 20, 002 (2026), §VI.

- Primary: <https://arxiv.org/html/2402.06677v5>.
- Local physical fermionic factors commute with their local parity. Their convex hull has no interior in the full physical state space: arbitrarily small cross-parity hopping coherences leave it. Bipartite fermionic entanglement can therefore persist at arbitrarily high finite temperature. This qualitative mechanism is already known and must not be relabeled as a new preparation theorem.

### Measurement and feedforward defeat the naive lightcone claim

Tiago Debarba, Fernando Iemini, Geza Giedke, and Nicolai Friis, **Teleporting Quantum Information Encoded in Fermionic Modes**, Physical Review A 101, 052326 (2020), §§III.2–III.3.

- Primary: <https://arxiv.org/pdf/2002.08201>.
- The paper supplies deterministic single-mode teleportation / entanglement swapping with a fermionic Bell pair, a Gaussian Bell measurement, two classical outcome bits, and local Gaussian correction. The correction uses one auxiliary fermion mode so total parity remains conserved; the auxiliary stays separable and can be reused.

Consequently a chain of neighboring fermionic Bell pairs, with bounded modes per site, permits simultaneous internal Bell measurements followed by a classically computed endpoint correction. Its conditional output has charged endpoint correlations at arbitrary separation. Thus arbitrary globally correlated **preselected** classical mixtures do not create distant odd-odd correlations, but **measurement-generated records and feedforward** can. The two control models cannot be interchanged.

A physically charged version must count propagation of the measurement outcomes and endpoint quantum storage while waiting. With unrestricted fast classical communication, a nonadaptive geometric lightcone lower bound does not apply to this architecture. With finite-speed local classical communication, one obtains a causal time/storage question rather than a parity-only obstruction. Fixed noise along the swapping route introduces an additional quantitative issue; the ideal bypass alone already invalidates the stronger ideal lightcone premise.

## Selection conclusion

The endpoint question has the stronger present opening because its obstruction is stated after every possible upstream strategy. It directly tests whether known full-rank thermal targets can be physically delivered through imperfect local ports. Pettinari already supplies an immediate exponential endpoint-obstruction corollary, so the contribution must be assessed against that strong baseline. The primary texts inspected do not supply the conjunction of a positive product-ground Hamiltonian with uniform gap, bounded planar geometry, and the connected global strong converse under arbitrary correlated preparation. This is a scope comparison, not an exhaustive proof that no prior theorem implies the result.
