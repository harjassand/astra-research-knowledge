# Independent mechanical comparator and obstruction report

Research date: 2026-11-01. This is an independent competing construction, not a claim that the proposed integrated device has already been built. Numerical artifacts are `mechanical_comparator_test.py` and `mechanical_results.json` in the same directory.

## Finding

The narrowed objective has substantial prior art at three different levels:

1. Physical adaptive trusses already perform redundancy-based damage diagnosis and actuator compensation. Some experiments date to 2007; a particularly explicit 2025 prototype exposes the instrumentation and control costs.
2. Self-stress projection, elimination of compatible displacement, and actuator-induced eigenstrain are standard force-method algebra. Sparse prestress adjustment also has a direct 2021 predecessor.
3. Correcting corrupted geometric distances without being given the original coordinates is an established distance-geometry error-correction problem, with work from 1996/1999 and an exact single-error study in 2024.

I did not locate an integrated experimental system that autonomously identifies and restores arbitrary original natural lengths after sparse drift, under unknown load, with neither original coordinates nor original length setpoints supplied to its controller. A claim of having done that should still be compared against a straightforward combination of calibrated member metrology, existing distance-geometry correction, and motorized length adjustment. I implement that comparator below. A physical self-stress decoder could improve its sensing, communication, latency, or robustness costs; the underlying compatibility projection and geometric error-correction idea are not new.

## A. The strongest located physical comparator

Reksowardojo, Senatore, Blandini and Smith (2025) demonstrate diagnosis and compensation on a 6.6 m spatial truss: 20 nodes, 54 members, static indeterminacy four, 12 ball-screw actuators, 54 axial-force strain sensors, eight infrared tracking cameras, and a central PXIe computer. Each actuator has 150 mm stroke and 6.8 kN maximum force. Sequential small actuator perturbations identify a measured redundancy matrix; candidate numerical matrices locate simulated member removal. Shape changes then redistribute stresses. The reported damage-induced stress increase, up to 22%, is recovered by adaptation. The work explicitly neglects stochastic load variation, sensor noise, and modeling errors. Its “self-repair” is mitigation of the structural consequences of removal; it does not reconstitute the removed bar or restore unknown original natural lengths. Data are available on request, rather than an identified public code release. [1]

Adam and Smith (2007) already studied a physical active tensegrity under partially defined loading and damage. Candidate simulations were compared against measured response and active perturbations; changes in strut lengths controlled shape and compensated some loss of stiffness. The controlled serviceability quantity included top-surface slope. This directly defeats a broad claim that autonomous structural diagnosis followed by mechanical compensation is new. It is weaker than original-reference restoration. [2]

Prokosch et al. (2023) give a particularly direct mathematical predecessor for diagnosis under unknown loading. In their notation the redundancy matrix is

\[
R=I-A(A^TCA)^{-1}A^TC,
\qquad R\Delta l_0=-\Delta l_{el}.
\]

A member-removal hypothesis updates matrix entries through

\[
r'_{ij}=r_{ij}-r_{ik}r_{kj}/r_{kk}.
\]

Active test strokes produce distinguishable residual signatures. The paper explicitly cancels unknown disturbances by differencing measurements before and after actuation, assuming the disturbances remain constant and linear superposition applies. It requires an intact reference model and sufficient separation relative to model and measurement uncertainty. Its damage class is member failure, rather than sparse drift of otherwise functioning natural lengths. [3]

## B. What is already established algebraically

Use our notation: let \(B\) map small nodal displacements to member extensions; \(K\) is diagonal axial stiffness; \(e\) is natural-length drift; \(a\) is a commanded rest-length increment. Then

\[
f=K(Bu-e-a).
\]

If the rows of \(H\) span the left nullspace of \(B\),

\[
HB=0,
\qquad -HK^{-1}f=H(e+a).
\]

Unknown nodal load affects \(u\), but disappears from this compatibility equation. This equation does not itself identify a fault or select the original geometry.

Wang and Senatore (2020) write the corresponding compatibility condition using a self-stress basis, \(W_s^T e_{total}=0\), and combine elastic elongation and eigenstrain. They explicitly treat actuator length changes as controllable eigenstrain. The extended method addresses prestress-stable mechanisms; its stated assumptions include small strains and small displacements. [4] Senatore, Duffour and Winslow (2019) likewise formulate compatibility through the nullspace of the equilibrium matrix, including thermal, plastic, creep, and lack-of-fit contributions, and optimize active structural control with embodied and operational energy costs. [5]

Xue et al. (2021) directly combine member-length adjustment, a sensitivity matrix, SVD-based choice of measured and active members, and sparse regression with modified orthogonal matching pursuit. Their numerical examples reduce construction-induced prestress error with few active members and examine noise robustness. The sparse vector selects correction actions against a desired prestress target; it is not a proof of reconstructing an unknown original geometric reference after arbitrary sparse drift. [6]

For an ideal linear sparse decoder, uniqueness is equivalent to

\[
\ker H\cap\{v:0<\|v\|_0\le 2s\}=\varnothing.
\]

Because \(\ker H=\operatorname{range}B\), this says that every nonzero compatible extension has support greater than \(2s\). It is an ordinary code-distance condition, not a consequence of having at least one redundant member. Noise conditioning matters as well: an extremely small singular value of a relevant column submatrix of \(H\) makes a formally unique correction physically unusable.

There is a basic degree bound. Move one generic node and choose its displacement orthogonal to \(d-1\) incident-member directions. The resulting compatible extension touches at most \(\deg(v)-d+1\) members. Therefore

\[
d_{linear}\le \min_v\deg(v)-d+1.
\]

For guaranteed correction of any \(s\) member errors, a necessary generic condition is \(\min_v\deg(v)\ge 2s+d\). Fixed coordination cannot provide an extensive adversarial error budget as system size grows. It can still support local fault guarantees and useful stochastic performance.

## C. Existing geometric error correction without an original shape

Berger, Kleinberg and Leighton formulate reconstruction of a three-dimensional model from arbitrarily corrupted interpoint distances. Their published author abstract describes a randomized algorithm that lists all structures consistent with a specified per-row error budget, rather than taking the original coordinates as input. The 1999 JACM article follows their 1996 STOC paper. This is direct conceptual prior for treating Euclidean realizability as an error-correcting constraint. [7]

Alfakih, Jung, Wolkowicz and Xu (2024) study a Euclidean distance matrix with one corrupted symmetric off-diagonal entry, known embedding dimension, and unknown error location and magnitude. They develop facial-reduction algorithms and analyze degenerate/ambiguous cases. Their problem is sparse corruption correction; simply projecting to the nearest Euclidean distance matrix generally does not recover the original matrix. This is algorithmic prior, not an autonomous mechanical device. [8]

### Explicit conventional construction

Choose a generic, originally unstressed, seven-node complete truss in three dimensions, \(K_7\). It has 21 members. Each member contains a calibrated axial spring element, an axial-force sensor, an end-to-end length measurement channel, and a motorized rest-length adjustment. The digital controller knows connectivity, the embedding dimension, the allowed number of errors, and sensor/constitutive calibration. It need not store the original geometry or original member lengths.

For a Hookean axial spring with independently calibrated \(k_i\), infer the current natural length from

\[
\hat r_i=l_i^{meas}-f_i^{meas}/k_i.
\]

For a bar whose calibrated constitutive law is engineering strain, \(f_i=E_iA_i(l_i/r_i-1)\), use instead

\[
\hat r_i=\frac{l_i^{meas}}{1+f_i^{meas}/(E_iA_i)}.
\]

Thus the external load need not be identified. Decode the corrupted vector \(\hat r\) as a valid three-dimensional distance vector with at most one altered entry. Command the corresponding member's natural length back to the decoded value. If stiffness, connectivity, support conditions, and load are unchanged and the loaded equilibrium remains in a unique stable basin, restoring all natural lengths restores the undamaged loaded equilibrium.

The criterion is restoration of the original reference and its loaded response. Restoring unloaded coordinates while a nonzero load continues to act is a different control objective and generally needs persistent active force.

For generic \(K_7\) in three dimensions, deleting any two edges leaves a globally rigid graph. A short proof suffices. If the deleted edges share a node, the other six nodes form an intact complete subgraph; the remaining node has four known distances to affinely independent anchors. If they are disjoint, choose five intact anchors, excluding one endpoint of each missing edge; each excluded endpoint has four intact anchor distances. Four generic distances determine a point in three dimensions. Consequently two distinct valid length vectors cannot differ in only two members, which gives exact one-error uniqueness.

The actual code uses a simple enumerated numerical fit: omit each candidate edge, fit all others, and compare residuals. It does not implement the 2024 paper's globally analyzed algorithm and does not establish convergence for arbitrary large errors. This separation matters: the geometric uniqueness condition is stronger than the convergence guarantee of our particular least-squares routine.

### Resource accounting

| Resource | What the comparator pays |
|---|---|
| Target information | The desired geometry is first encoded in the manufactured/calibrated rest lengths. Generic seven-node shape has 15 continuous degrees of freedom modulo rigid motion; there is no generation of target information from nothing. |
| Permanent geometric template | No separate jig, original-coordinate file, or protected per-member target length is used during decoding. The intact majority of member lengths carries the reference redundantly. |
| Instrumentation | 21 length channels, 21 force channels, 21 constitutive calibrations, temperature/environment compensation as required. Real gauges have finite error. |
| Actuation | To correct an arbitrary member autonomously, every eligible member needs an actuator or a genuinely available servicing mechanism. Twenty-one embedded actuators are the simple choice. |
| Controller | Stored topology and calibration, an error-correction algorithm, local bus or central communications, protected processing/memory, and sensor/actuator fault handling. |
| Power and time | Finite actuation work plus electronics power over the mission. A bound must include \(\int\sum_i|f_i\dot a_i|/\eta_i\,dt\), sensing, computation, settling, and actuator speed. Continuous service needs replenished energy. |
| Physical access | The selected example is an open truss with embedded member actuators. Repair of a buried dense solid does not follow. Cabling, joints, fatigue, buckling, backlash, and replaceable failed hardware remain engineering costs. |
| Fabrication and calibration | Initial lengths must lie within tolerance of a compatible target. Dense manufacturing errors or deliberate residual stress invalidate the exact unstressed-distance code unless explicitly modeled. |
| Scaling | Constant-size cells can share four noncoplanar nodes and use local communication, giving linear part count. This requires a local error budget and controlled overlap/conditioning; one error per cell is not the same as arbitrary sparse errors anywhere in the entire body. |

This is a credible existing-components competitor, not a located demonstration of the fully integrated capability.

## D. Executed discriminating test

`python mechanical_comparator_test.py` uses NumPy and SciPy and writes `mechanical_results.json`. The restoration function receives no original coordinates or lengths. The simulator separately retains them only to score recovery. A fixed random seed makes the run reproducible.

| Measured outcome | Result |
|---|---:|
| Structure | 7 nodes, 21 spring members, 6 self-stress modes |
| Imposed free-load norm, hidden from decoder | 762.9 N |
| Largest damaged-state member force | 368.9 N |
| Injected single natural-length drift | 30 mm |
| Correct damaged member selected | Yes |
| Noiseless length-restoration error | \(5.31\times10^{-14}\) m |
| Noiseless loaded-geometry restoration error | \(1.31\times10^{-13}\) m |
| Finite-noise length-restoration error | 2.85 μm |
| Finite-noise loaded-geometry restoration error | 6.86 μm |
| Absolute mechanical work along sampled repair path | 7.47 J |
| Largest actuator force along sampled path | 368.9 N |
| Smallest supported tangent-stiffness eigenvalue along sampled path | 69.0 N/m |

The finite-noise trial uses 2 μm standard deviation in length measurements, 0.05 N in force measurements, and \(10^{-4}\) relative stiffness calibration error. The best-fit residual is about 8.04 μm; the next-best error-location hypothesis has 11.21 mm residual. These are specified simulation assumptions and one modeled trial, not validated specifications of a built instrument.

The actuation path uses 21 quasistatic samples. All have positive supported tangent stiffness, so the computed path passes a local stability check in this spring model. The work estimate integrates absolute force against rest-length change; it excludes motor inefficiency, electronics, and between-sample uncertainty. No claim about actual actuator speed or hardware energy consumption follows from it.

The six scalar support constraints eliminate rigid-body freedom; they do not prescribe the internal shape. Restoring the reference can equally be defined modulo rigid motion.

## E. Three failure modes that a stronger construction must survive

### E1. Tangent uniqueness does not imply global geometric uniqueness

The executable test constructs two five-node complete planar frameworks. Reflect one node across the line through two others. Two incident distances stay unchanged; only its other two incident distances change. A received length vector taking one changed distance from each framework is one corruption from either healthy geometry. No observer can uniquely select the original from that data.

At the original generic framework, the minimum support of a nonzero *tangent-compatible* extension is three, verified by exhaustive rigidity-matrix rank checks. Thus its linear syndrome can meet the one-error uniqueness condition even though the nonlinear reference-recovery problem is globally ambiguous. The analogous three-dimensional counterexample uses \(K_6\) and reflection across the plane of three other nodes. A small-drift/basin condition, or a global rigidity condition after deletion of up to \(2s\) edges, is necessary.

### E2. Compatible drift is an information nullspace

A drift vector of the form \(e=Bu_*\) produces zero linear syndrome. It changes the unstressed geometry rather than producing an incompatibility. This does not contradict sparse recovery if such a drift has support outside the allowed budget; it does prevent any unconditional claim of restoring all drift.

The continuum version is established in inverse-eigenstrain analysis: a compatible eigenstrain \(\epsilon^*=\nabla_s U^*\) lies in the stress-map nullspace. Wensrich et al. (2025) analyze this nonuniqueness explicitly. Stress measurements alone cannot recover the actual compatible component of an unknown reference. Regularization selects a representative; it does not certify the historical original. [9]

### E3. The detector and geometry approximation are part of the fault model

The first-order natural-length estimate has error

\[
\delta\hat r_i\simeq \eta_{l,i}-\eta_{f,i}/k_i+f_i\delta k_i/k_i^2.
\]

Unknown large loads amplify stiffness-calibration error. One force-sensor bias \(b_i=-k_i e_i\) exactly imitates a length drift \(e_i\) in the inferred natural length. The test demonstrates this equality. It is a static indistinguishability statement under unknown load, not a claim that independent calibrated probing could never separate the hypotheses. An all-parts fault model must include the calibration, measuring apparatus, controller, and actuation system, or explicitly put them under a bounded-error assumption.

For a fixed tangent projector \(H_0\), a healthy finite deformation also produces

\[
H_0\bigl(l(p_0+u)-l(p_0)\bigr)=O(\|u\|^2),
\]

which resembles damage. In the test, healthy displacement norms of 1 mm, 10 mm and 100 mm produce projected signals of about 0.13 μm, 13.1 μm and 1.36 mm. Load rejection must be bounded within a declared linear regime or treated with a genuinely nonlinear model and adequate geometry information. Recomputing a tangent matrix at the current geometry does not by itself reconstruct the original reference.

## F. Public research code audit

TsgFEM is a relevant public, published research implementation: Ma, Chen and Skelton (2022), JOSS 7(75), 3390, DOI 10.21105/joss.03390. It supports self-stress analysis, nonlinear truss/tensegrity equilibrium, material models, external loads, and changes in member rest lengths. [10]

I inspected these actual public source files, not only the README:

| File | Blob SHA | Relevant dependency |
|---|---|---|
| `Function_library/tenseg_svd.m` | `680555f1e63cdeffa8b1948fde0671c5f584ebf0` | Computes mechanism and self-stress nullspaces by SVD of the supplied equilibrium matrix. |
| `Function_library/tenseg_equilibrium_matrix1.m` | `58f07666fda389ec5e4fde1de72863d3ba26b910` | Builds equilibrium matrices from supplied nodal positions, connectivity and boundary selectors. |
| `Function_library/tenseg_prestress_design.m` | `cea792329e8725e835696dbfa4fee840f2982177` | Combines a particular load solution and chosen self-stress coefficients using desired force values. |
| `Function_library/static_solver.m` | `7c2ce385496bad23b47d0429c89ec0792af38563` | Takes initial coordinates, external-load schedules, and rest-length schedules; solves nonlinear equilibrium. |

This code provides a real mechanics benchmark for the proposed actuator layer. It does not supply an unknown-reference sparse-drift decoder, eliminate sensor costs, or demonstrate an autonomous physical error-corrector. I inspected source but did not execute MATLAB. The separate Python test is our own small reproducible model.

There is also a direct prior for a broad phrase such as “autonomous mechanical error correction”: Jin et al. (2024) simulate three coupled, driven Duffing oscillators that mechanically correct a single logical-state upset by majority dynamics. The work includes finite drive and dissipation and discusses parameter mismatch. It concerns attractor-state storage, rather than load-bearing natural-length recovery. [11]

## Research judgment

The strongest defensible contribution would be a demonstrated physical implementation that removes specified overhead from the calibrated metrology-plus-distance-decoder comparator while preserving a stated correction radius, finite-load validity, finite precision, access, and actuator budget. A result can be useful without being the first compatibility syndrome, the first sparse geometric decoder, or the first actively self-repairing truss. A simulation with a trusted original geometry, trusted calibration, ideal sensed forces, or arbitrary signed actuator coupling has not yet established autonomous reference restoration in an all-parts physical fault model.

## Primary sources

1. Reksowardojo et al. (2025), *Application of Self-Diagnosis and Self-Repair on a Truss Prototype That Adapts to Loading Through Shape Morphing*. [Full article](https://onlinelibrary.wiley.com/doi/full/10.1155/stc/8827609). Relevant sections: 2, 3.1, 4, and data availability. Browser ref `turn122view0`.
2. Adam and Smith (2007), *Self-Diagnosis and Self-Repair of an Active Tensegrity Structure*. [DOI](https://doi.org/10.1061/(ASCE)0733-9445(2007)133:12(1752)). [EPFL postprint](https://infoscience.epfl.ch/bitstreams/18be613e-9907-4989-9e07-98412d95c551/download). Direct postprint access was inconsistent; primary search abstracts and the 2025 experiment's discussion corroborate its scope.
3. Prokosch, Stiefelmaier, Tarin and Bischoff (2023), *Detection and Identification of Structural Failure Using the Redundancy Matrix*. [Conference paper](https://files.eccomasproceedia.org/papers/smart-2023/SM23_444431.pdf). DOI 10.7712/150123.9827.444431. Browser ref `turn131view0`.
4. Wang and Senatore (2020), *Extended Integrated Force Method for the analysis of prestress-stable statically and kinematically indeterminate structures*. DOI 10.1016/j.ijsolstr.2020.05.029. [Author-hosted preproof](https://www.gennarosenatore.com/assets/publications/Extended%20Integrated%20Force%20Method%20for%20the%20analysis%20of%20prestress-stable%20statically%20and%20kinematically.pdf). Browser ref `turn129view1`.
5. Senatore, Duffour and Winslow (2019), *Synthesis of minimum energy adaptive structures*. [Full article](https://link.springer.com/article/10.1007/s00158-019-02224-8). Browser refs `turn100view0`, `turn131search1`.
6. Xue, Luo, Xu, Wan and Shen (2021), *A robust method for pre-stress adjustment of cable-strut structures based on sparse regression*. [Primary abstract](https://www.sciencedirect.com/science/article/abs/pii/S0141029621011305). DOI 10.1016/j.engstruct.2021.112987. Browser ref `turn128search2`.
7. Berger, Kleinberg and Leighton (1999), *Reconstructing a Three-Dimensional Model with Arbitrary Errors*. JACM 46(2), 212–235. DOI 10.1145/301970.301972. [Author-hosted abstract](https://people.csail.mit.edu/bab/abstracts/reconstructing-3d-model-with-arbitrary-errors.html). Browser ref `turn126view0`.
8. Alfakih, Jung, Wolkowicz and Xu (2024), *Single Element Error Correction in a Euclidean Distance Matrix*. arXiv:2406.15969. [Author-hosted paper](https://www.math.uwaterloo.ca/~hwolkowi/henry/reports/SubmitCorruptedEDMcompletion.pdf). Browser ref `turn119view0`; Section 5 is important for ambiguity.
9. Wensrich et al. (2025), *Well-posedness and trivial solutions to inverse eigenstrain problems*. [DOI](https://doi.org/10.1016/j.ijsolstr.2025.113505). Browser refs `turn104search0`, `turn131search0`.
10. Ma, Chen and Skelton (2022), *Tensegrity Finite Element Method*. [JOSS](https://doi.org/10.21105/joss.03390), [public repository](https://github.com/Muhao-Chen/Tensegrity_Finite_Element_Method_TsgFEM). Source inspected through GitHub connector on research date; filenames and hashes above.
11. Jin et al. (2024), *Engineering error correcting dynamics in nanomechanical systems*. [Full article](https://www.nature.com/articles/s41598-024-71679-7). Browser ref `turn130search0`.

Parent citation note: browser reference names are provenance notes for this research branch. Open the corresponding pages in the root branch before using those reference IDs in a user-facing citation.
