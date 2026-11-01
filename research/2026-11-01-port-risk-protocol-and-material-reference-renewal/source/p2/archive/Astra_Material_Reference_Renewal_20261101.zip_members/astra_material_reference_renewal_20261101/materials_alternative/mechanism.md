# Independent construction: scheduled turnover from a retained rest metric

## Result

A physically admissible route exists for a finite mission and a specified accuracy: a multiply connected truss with replaceable members, replaceable digital target memory, and mobile service robots that **install a calibrated stress-free member by elastically straining it into the current gap**. Maintenance can run on a fixed schedule, so it does not require a damage observer at every site. Every load-bearing member can turn over; no particular scaffold survives forever. The mechanism does require retained reference information. Removing that requirement as well makes the problem unidentifiable.

The strongest version is almost deliberately mundane: preferentially spend finite stock and throughput on preventive replacement instead of claiming that a material must infer which invisible constituent has drifted. Local damage remains below a recoverable limit because every member has a bounded service age. The controller needs to locate ports, decode an identity, and verify a mechanical connection with finite error; it need not estimate the instantaneous external load or reconstruct the whole deformed shape.

This is an engineering construction and a testable hypothesis, not a claimed new experimentally demonstrated material. Its distinctive step is to preserve the *rest metric* during loaded replacement. Generic gap filling, material addition, and strength recovery do not establish that property.

## 1. First-principles obstruction

For an elastic object with configuration x and retained reference parameters g, let its energy be E(x;g). At static equilibrium, an external load f satisfies

    gradient_x E(x;g) = f.

If f is unknown, the same observed x is compatible with an alternative reference g' and load f'=gradient_x E(x;g'). Thus geometry observed under an arbitrary unknown load does not identify stress-free geometry. Any estimator claiming to do so has added assumptions about the load, constitutive properties, history, or an independent reference.

For one Hookean element, F=k(l-l0). Measuring only l cannot distinguish rest-length drift from elastic strain. Even measuring F will not close the problem if both k and l0 may drift, unless more information is supplied. Disconnecting an element provides the physically useful intervention F=0; a known calibration then permits direct measurement of l0. The proposed protocol can avoid that measurement by installing a fresh element with a calibrated l0 from a retained recipe.

There is a second obstruction to shape recovery based only on local geometric consistency. In a linear truss, length changes are B u, where B is the rigidity matrix. Compatibility checks C have C B=0. A drift delta_l=B v changes the unloaded shape by v while satisfying every compatibility check. More locally, moving one target node coherently changes just the lengths incident on that node; all triangles remain consistent. Consistency is not fidelity to the intended shape. An error-correcting geometric construction must specify which compatible metrics are valid stored targets, and preserve the information that distinguishes them.

## 2. Physical encoding

Choose a small-strain, rigid reference graph. In three dimensions use a volumetric tetrahedral or braced lattice with sufficient local redundancy; a triangulated surface by itself may still have bending or mirror branches. Store:

1. The adjacency graph and endpoint/port identities.
2. Quantized rest lengths and, where necessary, rest angles or curvature.
3. Chirality/orientation labels or keyed connectors to exclude reflected cells.
4. Boundary occupancy and component type.
5. A version/mission identifier so unrelated, individually valid components cannot silently mix.

An alternative compact representation is a quantized material-coordinate map X_i, from which the consistent lengths |X_i-X_j| are generated. Storing unrelated edge lengths tolerates local repair but independent manufacturing errors can introduce residual stress; exact compatibility is not assured at finite fabrication accuracy. A claim of an exactly stress-free state must not ignore this distinction.

For a generic geometry with N independently specified points, extent L, and coordinate resolution epsilon, the coordinate information is of order 3N log2(L/epsilon) bits before coding and connectivity overhead. A repetitive lattice or algorithmic shape may need much less. Accuracy and robustness still cost physical redundancy.

The words live in physically separated, error-corrected memory patches, spread beyond the anticipated single damage radius. Memory patches and readers can themselves be replaced in overlapping generations. Copies are decoded and scrubbed before enough independent faults accumulate. No memory chip is immortal. A single nonredundant decoder or manufacturing calibration source would be a common-mode vulnerability; it must be part of the maintained system or its finite mission failure probability must be counted.

Absolute scale cannot be derived from shape compatibility. It must come from a specified reproducible standard: for example, calibrated stock length referenced to a frequency standard, or a molecular/crystalline repeat under controlled conditions. The apparatus and standard atoms can turn over. Their finite uncertainty and sensitivity to temperature, stress, and chemistry enter the length budget. Invoking identical nominal parts without counting their dimensional drift would merely hide the reference.

## 3. Replacement while loaded

Give each important edge multiple parallel load paths and ensure that any allowed service removal leaves the remaining network rigid and below its strength/buckling limits. Alternatively, install a temporary local bypass before releasing the old member. The bypass is workholding, not the object’s persistent shape record.

At a scheduled visit:

1. A robot reaches an address by local port connectivity. Global Euclidean coordinates are unnecessary.
2. It decodes the target rest-length/angle word from several retained copies.
3. It obtains or manufactures a fresh member, calibrating its free geometry before attachment.
4. It attaches one end, stretches or compresses the member to meet the other current endpoint, and locks the second end. An elastic insertion fixture and a force/torque limit suffice; the actual external load need not be known.
5. It transfers load and removes the old member, or performs the reverse sequence when redundant capacity already suffices.
6. It updates the finite service record and refreshes the relevant memory copies.

The replacement has intended rest length l0 even when its installed length is l=l0+delta. The actuator must provide at least its stored elastic energy k delta^2/2, in addition to transport, fastening, manufacturing, control, and dissipation. A connection made stress-free at the instantaneous gap instead chooses l0,new=l and writes elastic deformation into persistent material geometry.

Junction blocks and robots are also constituents. To replace a junction, first introduce a duplicate junction and calibrated temporary links to enough surrounding surviving vertices, transfer the incident members, then remove the old junction. This requires a free attachment volume and local access. One cannot simply claim complete turnover while leaving every joint, cable, memory controller, or transport guide permanently intact. The minimal simulation below does not implement this node-replacement operation.

Maintenance under unknown load is therefore feasible only inside an elastic and insertion envelope: bounded strain, bounded load slew during the operation, adequate residual stiffness, no buckling, and sufficient actuator stroke/force. A load that changes arbitrarily fast or exceeds every finite force limit defeats any finite mechanism.

## 4. A finite observer is sufficient

A fixed turnover schedule removes the need to recognize every drifting member. With M members and R successful replacements per unit time, the worst service age is approximately tau=M/R, including travel, failed retries, and queueing. If rest-length drift is deterministically bounded by speed v, the drift accumulated between services is at most v tau, plus manufacturing error. For stochastic shocks, the guarantee becomes probabilistic and depends on the likelihood of enough simultaneous faults to defeat structural redundancy.

A more economical policy can detach a member, measure its unloaded length with noisy shared metrology, and replace only if a threshold is exceeded. Repeated observations and independent comparisons reduce error, but no perfect observer is needed or available. The construction’s simplest existence demonstration uses blind turnover.

For r odd independent physical copies of a logical bit, each incorrect with probability p at a scrub, majority-decoding failure is

    P_majority = sum_{j=(r+1)/2}^r choose(r,j) p^j (1-p)^(r-j).

Across K logical bits and S scrub rounds, K S P_majority is a union bound before including correlated faults and reader/writer errors. Redundancy protects a reference for a specified horizon and risk; it does not yield absolute permanence. A finite system with positive-probability paths to unrecoverable states eventually loses its information under ordinary recurring-noise assumptions. A finite closed stock of usable free energy also cannot fund indefinite dissipative maintenance.

## 5. Error and resource accounting

For rigidity matrix B, member stiffness matrix W, rest-length error delta, and stiffness K=B^T W B, the linearized unloaded displacement is

    u0 = K^+ B^T W delta.

Rigid translations/rotations are removed mathematically; they do not require a physical anchor. If the smallest nonrigid eigenvalue of K is kappa>0,

    ||u0|| <= ||W^(1/2) delta|| / sqrt(kappa).

Thus local precision alone does not establish global precision. Long, compliant structures amplify low-frequency errors. The relevant safety margin must remain positive for every admissible temporary removal and localized damage pattern. Thermal fluctuations impose an additional equilibrium covariance k_B T K^+ in the harmonic model. At nonzero temperature, exact instantaneous geometry is not meaningful; specify a tolerance, averaging time, and failure probability.

Throughput must exceed damage/consumption demands, not only average robot speed. With mean fault rate lambda per member, queue stability requires R>lambda M if all such faults need replacement; preventive turnover may require substantially more. For a finite mission duration T, unrecycled parts consumed are R T. Recycling can reduce feedstock consumption but adds energy, sorting, chemical purification, and time.

Transport must reach the interior. Surface-only supply capacity scales approximately as L^2 while uniform volumetric wear scales as L^3. Internal service channels, distributed depots, or size-dependent worker/transport capacity are required before claiming scale independence. The channel network also occupies volume, weakens some structural paths, and itself needs maintenance. Waste removal and heat extraction are part of the same accounting.

## 6. Executable minimal model

Run:

    python producer-workspace/rest_metric_demo.py

The script is NumPy-only. It constructs a 5-by-4 node rectangular truss, with 3-by-4 cells and both diagonals; nominal member lengths are exactly 3, 4, or 5 in simulation units. Every geometric edge has three parallel physical members. No node is physically fixed: a pseudoinverse only removes rigid-motion gauge freedoms. The balanced time-varying force is unknown to the repair policy.

The 55 target lengths use 13-bit words at 0.001-unit quantization and seven physical bit copies: 5,005 code bits. One of the 165 members is replaced per time step, using decoded memory and finite manufacturing noise. Independent memory bit flips, slow distributed drift, and sparse localized rest-length shocks occur throughout. A comparator performs the same replacements but copies the observed loaded gap.

One reproducible run, seed 64173, gives:

| Quantity | Result |
|---|---:|
| Replacement operations | 3,300 |
| Replacements of every original member | 20 |
| Memory bit flips | 192 |
| Incorrect decoded length words | 0 |
| Localized rest-length shocks | 98 |
| Final unloaded RMS displacement, calibrated repair | 0.0008983 |
| Maximum sampled RMS after first full turnover, calibrated repair | 0.0011391 |
| Final unloaded RMS displacement, gap-copying repair | 0.0550646 |
| Smallest nonrigid stiffness eigenvalue | 1.04884 |
| Worst smallest nonrigid eigenvalue with any one member removed | 0.97782 |

These are simulation results, not empirical material measurements. The roughly 61-fold final error difference illustrates the load-writing failure and its avoidance; one seed does not estimate a reliability threshold. The simulation checks removable-load-path rigidity and finite noisy memory, but idealizes controller logic, calibration, transportation, joint verification, and physical fabrication. Junction turnover, fracture/buckling, nonlinear large deformations, and correlated faults are not modeled. Stored target words are never read from a pristine reference by the repair policy; the simulator retains truth only to calculate constitutive dynamics and score results.

## 7. Primary research and its actual limits

The construction is supported by separate demonstrated ingredients, not an existing integrated solution.

| Source | What it establishes | What it does not establish |
|---|---|---|
| Gregg et al., *Science Robotics* 9 (2024), DOI 10.1126/scirobotics.adi2746. [Author manuscript](https://ntrs.nasa.gov/api/citations/20230005194/downloads/SciRobotics-ARMADAS_System_Paper_Distribution.pdf). | A 256-voxel stiff structural lattice assembled by mobile robots; transport, intrinsic lattice indexing, reversible fastening, disassembly and reconfiguration. | No demonstrated lifelong geometric homeostasis under unknown loading. The build used manual feed, a manually generated plan and centralized commands; faults sometimes required touch recovery. Full repair and health monitoring are described as requiring added sensors. |
| Abdel-Rahman et al., *Communications Engineering* 1, 35 (2022). [Paper](https://www.nature.com/articles/s44172-022-00034-3). | A discrete robotic/material architecture and planning for serial, recursive, and hierarchical construction; identifies travel-time scaling explicitly. | Neither a closed self-reproducing industrial supply chain nor full turnover of a precision body under load. |
| Moreno et al., *Nature Communications* 17, 5932 (2026), DOI 10.1038/s41467-026-75166-7. [Paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC13365805/). | Hundreds of physical locally communicating bricks support distributed shape classification and damage localization; recovery is investigated in simulation. | Active material repair is a future actuation requirement. Class recognition is not exact specimen memory: removing a chair’s back can cause recovery toward a table interpretation. Shape-conditioned recovery retains a supplied target representation. |
| Ong et al., *Nature* 552, 72–77 (2017), DOI 10.1038/nature24648. [Paper](https://www.nature.com/articles/nature24648). | Scaffold-free addressable DNA bricks form complex 3D structures with thousands to tens of thousands of distinct components. Shape can reside in distributed interaction specificity. | Load-bearing long-term renewal, arbitrary under-load repair, autonomous ingredient resynthesis, and indefinite reference retention. |
| Schulman, Wright and Winfree, *ACS Nano* 9, 5760–5771 (2015), DOI 10.1021/nn507493s. [Paper](https://pubs.acs.org/doi/10.1021/nn507493s). | Experimentally, increasing redundancy in DNA tile bitstring copying reduced errors; each added level gave roughly a factor-of-three reduction under their conditions. | Error-free repair or a load-bearing body. This is finite-probability molecular information retention, not a perpetual perfect template. |
| Soloveichik, Cook and Winfree, *Natural Computing* 7, 203–218 (2008), DOI 10.1007/s11047-007-9036-x. [Author record](https://authors.library.caltech.edu/records/7gj5t-g0873). | A theoretical tile-set transformation combines error proofreading and regrowth after tile removals for specified quarter-plane patterns. | Mechanical rigidity, continuous geometry under load, arbitrary loss of all target information, or a complete molecular maintenance machine. |
| Zhu et al., *Physical Review Research* 6, L042057 (2024), DOI 10.1103/PhysRevResearch.6.L042057. [Paper](https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.6.L042057). | A modeled two-stage local proofreading scheme improves colloidal assembly yield and robustness using target-compatible local environments and a reverse correction pathway. | An experimentally integrated precision load-bearing repair system. |

The practical next experiment is a small redundantly braced truss whose replaceable members contain calibrated free lengths and compliant insertion fixtures. Apply an unmeasured varying balanced load, impose length drift on selected members, cycle through every member with fixed service timing, then remove loads and measure geometry. Compare calibrated insertion with gap-copying insertion at equal parts, throughput, and sensor budgets. That test directly measures the claimed mechanism.
