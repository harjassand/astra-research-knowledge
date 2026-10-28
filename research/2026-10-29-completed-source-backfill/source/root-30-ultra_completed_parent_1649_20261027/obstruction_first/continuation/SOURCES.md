# Exact primary sources, versions and comparators

The source spin-one theorem, arbitrary-spin criterion, Lanczos/Temple bounds,
rotation projections, 1D Gibbs MPO existence and positive temperature powers
are established inputs. No novelty or advantage is asserted for reusing them.
The construction here is the acquired actual-kernel compression and its finite
warm scope/cold failure boundary. Source hashes identify bytes, not correctness.

1. **OpenAI, The periodic spin-one Haldane gap**, source revision
   `7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a`, directory last changed at
   `adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
   [Pinned paper](https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-periodic-spin-one-Haldane-gap-September-24-2026/paper.pdf).
   Frozen stage1 `sources/haldane_primary.pdf`, SHA256
   `989f14096403897c693467f4007eb8997899648fd50029d5bee50ca9f8471ba6`.
   Read through analytic/arithmetic/variational appendices and verification
   README/manifest. The original full-column verifier was not executed.
   Its spin-one proof and sector initialization are not new results here.

2. **Hal Tasaki**, October19,2026 revisions.
   [Author page](https://haltasaki.github.io/writings/AI/OpenAI_Haldane.html),
   [CT PDF](https://haltasaki.github.io/writings/AI/OpenAI_Haldane_CT.pdf),
   [DT PDF](https://haltasaki.github.io/writings/AI/OpenAI_Haldane_DT.pdf).
   Frozen CT SHA256 `5bc1b8f29d8892f2e723395a198d626a3ac555e2cb49a40e37846fae684ad9b9`.
   CT sections3–6, AppendixC.1 and AppendixD govern this continuation.
   The merged-history kernel, actual-temperature trace identities, SO(3)
   twists, all-spin extension and Eq5.10 are used at their stated scopes.
   Theorem6.2 uses temporal purity on2L. AppendixD's converse assumes a
   zero-temperature gap and additional finite-size energy decay; neither
   assumption is imported to prove that gap.

3. **Kuwahara–Alhambra–Anshu**, Improved thermal area law and quasi-linear
   time algorithm for quantum Gibbs states,
   [arXiv:2007.11174v2](https://arxiv.org/abs/2007.11174v2), March11,2021.
   `sources/thermal_mpo_primary.pdf`, SHA256
   `17842d24ec7b0ea8ef5b8c107192ea62a75e3c6dc34b4070d284fee2b835c4e8`.
   Read Theorems2/3, the positive-power lemma, local polynomial construction,
   and explicit SVD norm warning. This is the strongest direct ordinary
   all-Schatten/MPO/temperature-lift comparator. It proves a constructive
   controlled representation; it does not give an acquired modest bond or
   numerical tail certificate for the present cold spin-two rings.

4. **H. Fawzi–O. Fawzi–S. Scalet**, A subpolynomial-time algorithm for the
   free energy of one-dimensional quantum systems in the thermodynamic limit,
   [corrected arXiv:2209.14989v3](https://arxiv.org/abs/2209.14989v3), July3,2024.
   `sources/free_energy_v3.pdf`, SHA256
   `9b74b8c34cdfab3657195ecba4681b4be1369b4d5d67c5918e38d9ec9e772302`.
   Read Algorithm2, Araki CP transfer, primitivity/convergence and explicit
   Hamiltonian-norm dependent lengths. The corrected edition is used rather
   than treating the earlier published version as unrevised.

5. **S. Scalet**, A Faster Algorithm for the Free Energy in One-dimensional
   Quantum Systems, [arXiv:2402.19030v1](https://arxiv.org/abs/2402.19030v1),
   February29,2024, [JMP65,081901](https://doi.org/10.1063/5.0218349).
   `sources/faster_free_energy.pdf`, SHA256
   `bb65d6f3adc8f7dc0bdb1f3127b54f309f512d21520c0c0276971cbae2c2e4b9`.
   Read main algorithm, finite-interval ratio proof and MPO theorem interface.
   Together with the preceding source, this prevents claiming that a rigorous
   compressed 1D thermal representation is generally missing. Pressure is a
   different output from certified periodic S/T loop corrections.

6. **Alhambra–Capel–Gondolf–Ruiz-de-Alarcon–Scalet**, Conditional Independence
   of1D Gibbs States with Applications to Efficient Learning,
   [published May5,2026](https://doi.org/10.1007/s00023-026-01655-6),
   [arXiv:2402.18500](https://arxiv.org/abs/2402.18500).
   Journal `sources/conditional_independence.pdf`, SHA256
   `9736135908d8dc140319906acecb468952f8b7ed3551cefb8c28678afc1b132b`.
   Proposition3.9 and Theorem4.11, including their proofs/scope, were read.
   Their direct multiplicative purity theorem is a stronger comparator than
   generic Gibbs-MPO trace continuity. It concerns intervals with stated
   interaction assumptions and beta-dependent constants. Periodic folding,
   endpoint terms, paired-site marginals and numerical constants are separate
   acquisition debts, not an asserted theorem transfer.

7. **Scalet et al.**, Classical Estimation of the Free Energy and Quantum
   Gibbs Sampling from the Markov Entropy Decomposition,
   [arXiv:2504.17405v2](https://arxiv.org/abs/2504.17405v2), December29,2025.
   `sources/med_2025.pdf`, SHA256
   `ac1609e94920acb588b47237bdfbb41e1b0be60704e9f5d9ead798d752b55f75`.
   Read main setup, ordinary relaxation/convergence and rounding scope. Used
   as a strong convex free-energy comparator, not as an uninspected numerical
   discarded-spectrum or Gibbs-sampling oracle.

8. **Childs–Su–Tran–Wiebe–Zhu**, A Theory of Trotter Error,
   [arXiv:1912.08854v3](https://arxiv.org/abs/1912.08854v3), February3,2021.
   `sources/trotter_error_v3.pdf`, SHA256
   `c76e2980dee799253ac3a5fa6176ac9005f78c844c1243dc2e579433137c7965`.
   Section5.1's exact Strang integral representation was read; imaginary-time
   conjugation norms are paid. No real-time unitary norm bound is reused as
   an imaginary-time certificate without its exponential factors.

9. **Mann–Minko**, Algorithmic Cluster Expansions for Quantum Problems,
   [arXiv:2306.08974v2](https://arxiv.org/html/2306.08974v2), January16,2024,
   [PRX Quantum5,010305](https://doi.org/10.1103/PRXQuantum.5.010305).
   Preserved `sources/algorithmic_cluster_v2.html`. Read formal polymer/log
   expansion and partition-function application. The early linked-cluster
   warm bound in `thermal_purity_lift.py` uses finite inclusion-exclusion and
   an explicit entire Taylor tail; it is not a claimed new cluster theorem or
   an assumption of that paper's high-temperature convergence radius.

Stage1 SOURCE_REGISTER.md retains the numerical QMC/DMRG/high-spin cluster
comparators, ordinary TEBD source, renormalization energy-relaxation source
and exact archive access pin. No new numerical gap extrapolation is offered
as competition to those established physical estimates. No source or theorem
claims an advantage of this branch over an equally precise optimized MPO,
Araki transfer, sign-free replica-QMC or original full-column implementation.
