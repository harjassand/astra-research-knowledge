# Independent integrated review: Tanner energy, quantum barrier, and finite-rate compiler

2026-10-30 UTC. Read the actual directory, including its added explicit circuit and status index. Final exact source hashes appear in `SOURCE_SHA256.txt`; reviewed copies are retained here. Earlier circuit bytes/initial hashes are preserved separately. Original files were not edited by this reviewer.

## Verdict and contract classification

The Tanner-specific mathematical interfaces are discharged under the accepted GPT density/code hypotheses and the previously reviewed abstract weighted-drift, killed-basin, positive-record, and coefficientwise compiler theorems:

1. **Ideal atomic continuous-noise route:** local energy/unary-token geometry, progress, orbit noise bounds and linear high-potential boundary satisfy the imported killed-basin hypotheses. This yields the stated ideal atomic exp(cN)-scale bound for additive bounded local joint Hamiltonian/Lindblad noise, with a retained common bath and fixed logical-independent bath initialization.
2. **Ideal Poisson route:** the RAW-SYNDROME candidate-persistence correction, integer-energy finite work, suffix localization and D0/D1 dichotomy supply the deterministic contract for the existing common-record spacetime argument, now with a linear cutoff.
3. **Native finite-rate Poisson route:** the added explicit GPT circuit, complete reservation footprint, grouped physical-qudit convention and dressed incidence budgets instantiate the accepted transactional compiler rather than merely asserting that fixed degree implies a possible controller. The existing positive regeneration/fault-mass/service results are applied with the new fixed constants and a newly chosen small rate threshold.
4. **Native onsite Markov-cushion route:** follows from the accepted finite-dimensional Choi reduction using the ACTUAL full grouped-site dimensions and actual onsite depolarization. Its noise class is finite system-local generator deviations, not arbitrary shared-bath continuous couplings. Alternative CP analysis records are not original detector records.

These are scoped theoretical model conclusions. Concrete useful thresholds, efficient low-degree hardware, noisy operational quantum retrieval, fault-tolerant initial encoding, Euclidean routing, and a generic continuous-noise finite-duration-controller theorem are NOT discharged. The earlier abstract theorem contracts remain imported, not re-proved by this receipt.

## 1. Local energy is a syndrome function

For each potential view, the selected local stabilizer basis has kernel equal to its local codespace. Its measured raw syndrome therefore fixes the coset whose minimum Hamming weight defines U_v. This is independent of nearest-codeword ties. Global same-syndrome replacement preserves every local distance and every candidate's energy-change test. No classical error mixture is assumed.

Distance to a fixed code is 1-Lipschitz under bit changes. Since each data qubit belongs to exactly two energy views in one sector, U(E)≤2|E| and |U(E+F)-U(E)|≤2|F|, with the stronger sum of local absolute changes bounded the same way. These inequalities do not require reducedness.

For confinement, use the smaller guaranteed decoding radius, not the larger existence-of-a-decreasing-flip radius. The adopted constants and dual-sector hypotheses were checked in the preceding independent density review against the [GPT primary source](https://arxiv.org/html/2206.06557). A reduced component below that correction radius has U(C)≥Delta^(-2)|C|. Code distance and rate are linear and constant, respectively, once the large admissible degree/local codes are fixed. All cutoff constants here are strictly below both sector distances and correction radii.

## 2. Persistence correction is essential and correct

Unary energy can hide a changed local coset. The document's example with equal weight-one errors but opposite response to the same flip is a real counterexample to token-only persistence. The revised window proof instead packs complete raw-syndrome dependencies of an initially accepted candidate. These sets have bounded size/overlap in the fixed full-read graph, so a constant-fraction independent family exists at distinct hubs.

Until a dependency bit changes or its own hub evaluates, the initial candidate remains accepted. An own-hub evaluation must execute some decreasing candidate, even if it chooses another one. A correct correction changes at most dw raw bits and resolves at most dw+1 packed candidates. A bad mask resolves at most d|F| candidates. The own-hub term must be retained; the text does retain it.

If D_U is total accepted integer-energy decrease, the number of correct moves is at most D_U. Hence the resolution inequality and U_end≤U_start−D_U+2Q combine to exactly the displayed a,A,B. Control-only faults are charged to missed availability, not fictitious data changes. The containing-hub majorant remains fixed for each spatial witness, so later history-dependent candidate selection introduces no independence assumption.

## 3. Unconditional finite work and component localization

The graph contains full decision-read, energy-view, raw-check and event-support cliques. For a component of incoming error plus actual event supports, any executed correction is supported wholly there, and all currently erroneous qubits influencing that correction's decision are there too: otherwise the read clique would join the components. Energy views cannot simultaneously meet errors in separate components. Therefore restricted accepted moves have the same decrease and their count is at most U_in+2Q≤2|E_in|+2Q. The execution-support bound follows with 1+2w.

Appending a global sectorwise minimum-syndrome representative may merge execution components, but each old component remains wholly in an enlarged one. Raw-check support cliques make same-syndrome equality componentwise. Replacing the endpoint representative inside one enlarged component by the actual endpoint error cannot lower weight, by global minimality. This yields the stated factor-two D0 bound without a small-error premise. Below distance, componentwise zero-syndrome differences are stabilizers.

The future-support equality is exact XOR bookkeeping, including arriving bad events. Full-read cliques make suffix restriction valid. The density statement also applies to a nonreduced restricted error of small weight by choosing a no-heavier stabilizer representative; locality is recovered from the ORIGINAL error because any active hub must meet nonzero energy in its read region, and hence an original erroneous qubit there. The proof does not pretend the reducing representative remains inside that original support.

Same-syndrome virtual starts reproduce the entire raw-syndrome trajectory and candidate decisions, not merely total energy. They are mathematical branch relabelings. Final minimum-representative subsets are reduced, so confinement applies componentwise even when the union has large total weight. The suffix footprint inequality follows by cancelling final energy against the work bound. No monotonicity under arbitrary qubit deletion is used.

Nested boundary sets discard whole future-support components, where energy additivity is valid. Iterating the resulting contraction gives the displayed fresh-obstruction alternative or growing-ancestor alternative. The final seed-density enlargement is to ORIGINAL execution-support components, preserving the target rooting and allowing D0 to use actual incoming seeds. Thus the D0/D1 interface has the required containment, rooting, multiplicity and seed-density properties.

## 4. Unary tokens are valid for weighted drift, not for persistence

Token occupation is an exact function of commuting raw-syndrome projectors, with occupied count equal to U. For an accepted move, unary Hamming change equals the sum of absolute local-energy changes; it is nonzero, bounded by 2w, and has net removal at least one. This supplies beta=1/(2w).

For a physical Pauli orbit on data support Z, any two local errors differ on at most |Z∩Q(v)| bits. The full range of U_v on that orbit therefore has that width. Exactly the tokens between its minimum and maximum can vary, giving at most 2|Z| variable tokens in one sector and 4|Z| in both. The varying token identities can depend on the orbit, but every such token lies in a view meeting Z; the fixed incidence bound needed to sum orbit oscillations still holds. No token independence or token-space physical noise channel is assumed.

The mixed dummy/token graph supplies connected containers for arbitrary connected data sets. Intersecting containers join their data sites by construction. Any occupied token in J(C) has an error in its energy view; that error's own container meets J(C), so it belongs to C. Conversely all occupied tokens caused by C are included. Thus the containers partition occupied tokens exactly. An active hub's full read region cannot contain errors from different components, and its changed-token set lies inside its component container. Bounded token incidence and the accepted active density complete the abstract weighted-coverage premises.

The abstract animal proof applies to this graph even though some vertices are always-empty dummies and token configurations obey unary constraints. It only uses occupancy, bounded surplus, container size/disjointness and incidence. The source-to-target entropy charges and vacuum summability therefore transfer; the resulting drift is a syndrome-diagonal operator inequality for the atomic CPTP feedback instrument.

## 5. Continuous-noise and linear boundary transfer

The canonical gauge still uses DATA Pauli representatives. Componentwise minimum-weight replacement for E union Z union F is unchanged. Source confinement supplies at least h_T(|K|/2−s) occupied tokens in connected J(K), and its size is at most D0|K|. This yields the stated linear-cutoff exponential boundary with u≤h_T/(4D0), ell≥8s. Every source below the threshold has trivial canonical logical action on local Pauli edges; tokenization has not weakened the code-distance step.

Local joint data/bath operators preserve their full raw-syndrome Pauli orbits. Orbitwise range of V is therefore a scalar bound on each invariant orbit block, and the bounded variable-token/counting calculation gives the same coherent/Lindblad adjoint bound by C_osc W. Both CSS sectors and full nominal read Kraus/loss supports are included. Bath-only dynamics is retained and commutes with the potential.

The reviewed CP killing, logical factorization and reference-level Duhamel comparison then apply with ell proportional to N and O(N) total local norm budget, giving C N^(3/2)t exp(−cN), capped by two. The initial vacuum has O(N) potential and is below the threshold for sufficiently large N. This ideal atomic route tolerates arbitrary bounded joint bath operators of the stipulated additive noise class; it is NOT an assertion about instantaneous drift of partial transactional computation.

## 6. Exact finite local GPT instrument

The explicit circuit locks R_h, the union of EVERY energy view affected by ANY candidate on Q(h), not just the chosen correction mask. There are at most 2w views and 2w² data resources/raw check generators. Its local distance table computes each affected energy from raw syndrome, and exhaustive lexicographic search finds an improving mask whenever one exists. The offline lookup/code-selection costs are finite functions of degree, explicitly not polynomial practical guarantees.

Coherent controlled-stabilizer extraction realizes sum_y Pi_y|psi>|y>. All measured checks commute; redundant inconsistent outcomes have zero projector. The reversible truth-table oracle computes the correction mask without disturbing y, then controlled data Paulis apply it. Scratch is uncomputed, but syndrome and mask registers are deliberately retained until complete terminal reset. Therefore the exact channel is sum_y P_f(y) Pi_y rho Pi_y P_f(y)^dagger on arbitrary reference/bath-entangled data. Uncomputing y after correction would generally change that instrument; the file expressly forbids that shortcut.

Distinct clock positions carrying unitary payload gates, complete resolved workspace reset channels, unchanged acquisition backtracking, and reset-before-release during committed computation/attached abort phases fit the inherited transactional theorem. Full read locks also exclude interfering opposite-sector transactions. No global syndrome or minimum-weight decoder is embedded in the local controller.

## 7. Native grouping and support budgets

The explicit native convention combines all clock, workspace and private-monitor factors into ONE hub qudit; each resource combines its payload, complete free/o_h/z_h tag and resource monitor. The resource tag bound is 32w+1, not 16w+1. The complete dimensions, including huge workspace/clock factors, are the dimensions used in any Markov cushion.

Workspace-only payload edges are onsite. Data-touching controlled-Pauli extraction/correction edges involve one hub and one resource, with the ownership projector on that resource. Inherited acquisition/abort/cleanup Hamiltonians remain two-site, and complete hub/resource/monitor resets remain onsite. The native claim does not use a spatially distributed one-hot clock. Thus it instantiates bounded-degree two-site-Hamiltonian/onsite-dissipation locality in the stated grouped-qudit convention, not a practical qubit-local layout.

The read-incidence count is conservative: at most 8w hubs per resource per sector, hence 16w both sectors, with |R_h|≤2w². The resulting conflict/read graph degree bounds are finite. A physical site meets at most 1+16w commuting forest factors. Conjugation consequently involves only factors intersecting the original primitive support; commuting factors do not generate recursive support growth. The displayed dressed-data support bound and reverse-incidence count through at most 1+b_read f_size possible physical sites are valid overestimates. The marked-owner bound uses the same argument and explicitly pays its original-footprint incidence.

These constants discharge bounded enlarged support/incidence for the existing positive record mass/service construction. Its window duration and small noise threshold must be chosen again after fixing this circuit's length/dimensions/conflicts. The result is an existence theorem at enormous fixed overhead, not an assertion that the old FGL numerical constants are unchanged.

## 8. Readout and native-noise scope

For the ideal killed-basin theorem, strict per-move V decrease and the edge barrier keep terminal noiseless GPT scans in the safe basin. Active density excludes a nonzero-energy no-change scan. The scan therefore reaches zero energy with correct canonical logical action.

For the Poisson/common-record theorem, efficient ideal GPT readout requires a different argument: append its ENTIRE noiseless scan computation as one final D0-only root suffix. It has Q=0 and at most 2N accepted integer-energy decreases. If all enlarged suffix components are below cutoff, terminal nonzero energy contradicts componentwise activity, and the zero-energy endpoint is stabilizer-equivalent to the correct output. Any failure supplies a cutoff-bad suffix root. D0 supplies incoming seed density; the backward chain proceeds only through actual earlier memory blocks and cannot terminate with a fresh event in the noiseless suffix. This adds one root, not fictitious good-service windows or an unproved residual distribution. It preserves the N(1+t)exp(−cN) envelope and the common-correctable-span quantum step. Physical noise during a real readout computation is not thereby controlled.

Native Poisson CPTP kicks may retain the common bath under the accepted compiler model. The onsite Markov-cushion reduction has a different scope: finite system-local HP trace-annihilating deviations plus ACTUAL full-site depolarization at rates satisfying the local Choi bound. It does not cushion unrestricted joint bath directions. Its nominal clean reset record may belong to an alternative positive unraveling of the identical unconditional generator, not the original detector log. Since no external feedback uses that analysis log and the final decoder is fixed on system registers, unconditional channel transfer is valid. Depolarizer implementation errors and its full-dimension rate penalty remain charged as in the earlier audited reduction.

## 9. Reset-budget comparison

Checked the linked [reservoir ceiling paper](https://arxiv.org/html/2610.26228). The scope note correctly separates its fixed-depolarization, entropy-budget, post-washout reservoir setting from initially encoded memory with retained bath or arbitrary continuous noise. No universal optimality theorem for this construction is established. O(N) reset capacity at fixed degree counts supplied local ancillary resources per time, not actual entropy production or dissipated heat.

## Regression, preserved limitations, and blockers

`check_energy_tokens.py` independently checks 8,192 exact pairwise token/Lipschitz identities and 8,192 full local-Pauli-orbit token-range bounds in small two-endpoint toy systems. It also preserves the counterexample to energy-only candidate persistence. PASS; this is algebra regression, not a numerical test of Tanner expansion or a lifetime simulation.

The original source's pending-density language is resolved by its STATUS index and the separate exact-hash density acceptance, not by silently editing frozen transfer files. No failed test or obstruction was hidden. Native grouping, complete tag dimensions, acquisition-release wording and final GPT readout require the explicitly recorded clarifications, not informal assumptions. No tool/permission blocker occurred.
