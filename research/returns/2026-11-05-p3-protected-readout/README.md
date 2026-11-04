# P3 — learn a protected representation and read its logical data

**Governing source:** [complete visible return and exact prompt](P3_PROTECTED_QUANTUM_READOUT_20261105_RETURN.txt). The source contains a verbatim native prefix and an overlapping rendered ending; damaged or duplicated glyphs are preserved. This page extracts its construction and limitations without re-proving it or executing scientific code.

The result is a protected **measurement interface**, not a universal coherent decoder or a way to recover an already destroyed unknown input. The reader acquires a particular unknown code representation, measures physical pairs with a fixed circuit, and performs correction in the classical record. A prepared encoded reference makes the same physical reader programmable for logical Pauli measurements.

## Exact specimens and access

There are m disjoint square toric blocks with side `L>=5`, encoding `k=2m` logical qubits in `N=kL^2` physical qubits. All specimens have the same unknown physical permutation and product of single-qubit Cliffords. Wire identities and laboratory measurement axes are calibrated. **Corresponding physical wires in two banks can interact.** A traveling measurement port alone does not supply that paired access.

Protection is already present in the input family. For a constructed asymptotic family the source chooses `L=Theta(log k)`; for an existing specimen the reader must acquire its actual distance and evaluate the bound. It cannot enlarge the code distance automatically.

Noise has a local stochastic **support** decomposition into CP maps `W_B`, with

```text
W = sum_B W_B
|| sum_(B containing A) W_B ||_diamond <= q^|A|.
```

A site is one physical qubit in calibration and one corresponding pair in Bell readout. The CP summands need not be trace preserving; coherent action inside a faulty support is allowed. This is a declared noise family, not arbitrary hardware noise.

Conditional on correct acquisition, the source derives a guarantee for the **whole logical Bell-measurement channel**, including inaccessible-reference correlations and arbitrary joint logical states in the two banks:

```text
(1/2)||M_reader-M_logical_Bell||_diamond <= beta(N,L,q)
beta(N,L,q) = (8N/3) (6 sqrt(q))^L / (1-6 sqrt(q)),
q < 1/36.
```

This is not a bound inferred from identical-copy tests or one entanglement-fidelity calculation. [Source, lines 51–89](P3_PROTECTED_QUANTUM_READOUT_20261105_RETURN.txt#L51-L89).

## Acquire the code, signs, distance and decoder

Distance greater than four makes every weight-at-most-four Hermitian Pauli satisfy `Pi P Pi=0` or `±Pi`. The nonzero cases are signed stabilizers, independently of the logical payload. Calibration specimens may therefore have different logical states while sharing the code. For the promised square tori, the weight-four checks are exactly elementary stars and plaquettes.

At calibration support-noise parameter q_c, a weight-four expectation has bias at most `8q_c`. True signed checks have magnitude at least `1-8q_c`; nonchecks have magnitude at most `8q_c`. The threshold gap is `g=1/2-8q_c`.

The construction avoids exhaustive four-wire search. For a random product Pauli basis, collect t discovery rows, form all pairwise XORs of outcome columns and sort them up to complementation. Disjoint equal-key pairs propose signed quartets. Verify proposals with **fresh held-out rows** in that same basis.

With `a=1-4q_c`, `b=1/2+4q_c`, the explicit finite choices are

```text
t = ceil(2 ln(N)/ln(1/b))
R = ceil(81 a^(-t) ln(N/delta_m))
H = ceil(R(3N+N^2/4)/delta_t)
u = ceil((2/g^2) ln(2H/delta_v)).
```

H is an enforced comparison cap: exceeding it aborts. Missing checks, runtime abort and held-out verification contribute `delta_m`, `delta_t`, `delta_v`. Overlapping-pair comparisons are included in the runtime count; there is no assumed small collision bucket.

| Acquisition resource | Paid bound |
|---|---|
| Calibration specimens | `R(t+u)` |
| Classical bit operations | `O(RN^2 t log N + H(u+log N))` |
| Fixed-noise asymptotic copies | `O-tilde(N^alpha)` |
| Fixed-noise asymptotic classical work | `O-tilde(N^(2+alpha))` |

Here

```text
alpha(q_c) = 2 ln(1/(1-4q_c)) / ln(1/(1/2+4q_c)).
```

For `q_c<1/36`, the source bounds `alpha<1/2`. It does not claim this parity-search algorithm is optimal.

Local anticommutation of learned checks gives a connected bipartite graph for each block, separating stars from plaquettes up to exchange. The shared local axes recover the Clifford interpretation. The resulting primal/dual graphs, binary elimination and a four-sheet homology cover supply logical representatives and both distances. Incidences, commutation, ranks, orientability, genus and distance are explicitly checked by the reported construction; no code-description, distance or decoder oracle is assumed. [Source, lines 91–193](P3_PROTECTED_QUANTUM_READOUT_20261105_RETURN.txt#L91-L193).

## Fixed physical measurements, classical recovery

Each paired wire uses CNOT, a Hadamard on the first qubit, and two Z readouts, measuring XX and ZZ. The relation `YY=-(XX)(ZZ)` matters. For `P=i^(v.w) X^v Z^w`, its paired eigenvalue bit is

```text
v.x + w.z + v.w mod 2.
```

Thus the learned frames are applied by **classical affine relabeling**. The apparatus need not physically undo the unknown permutation or implement a learned coherent logical decoder. Minimum-weight matching on the acquired primal/dual graphs corrects the observed syndromes before logical parities are evaluated.

The channel proof is support-wise. On a support containing fewer than half the positions of every nontrivial cycle, minimum-weight correction cannot leave a nontrivial logical cycle. The source counts bad supports and shows that every supported Kraus operator obeys the same logical-projector relation. Bounding the missing ideal and actual bad instruments yields the half-diamond beta bound for arbitrary references.

For a learned logical Pauli P, prepare an encoded stabilizer reference `sigma_P` with P eigenvalue +1. Coarsening the corrected Bell outcomes by `P tensor P` gives joint effects `(I±P tensor P)/2`, hence effects `(I±P)/2` on the unknown specimen. The known reference is prepared before that specimen arrives. [Source, lines 194–253](P3_PROTECTED_QUANTUM_READOUT_20261105_RETURN.txt#L194-L253).

## Complete signed learning task and the actual comparator

The task distinguishes `rho_0=I/d` from `(I+sP)/d`, with `d=2^k`, unknown nonidentity logical Pauli P and unknown sign s. The purity gap is only `1/d`; a constant-shot SWAP-mean estimate would not solve it.

Two identical specimens produce logical Bell rows on an affine codimension-one hyperplane. Subtract the first row and use binary elimination to distinguish rank and identify unsigned P. The rank-failure bound for M rows is `2^(2k-M+1)`. Identical-copy sampling cancels the sign, so the construction then prepares `sigma_P` offline and uses a fresh specimen–reference readout to recover s.

The source's complete failure budget is

```text
delta_acq + (M+1) beta + 2^(2k-M+1)
          + delta_factory + delta_ctrl.
```

At fixed target error and fixed sufficiently small local noise, `M=O(k)` and a constructed family with `L=Theta(log k)` yield total asymptotic specimen count `O(k)`, including the sublinear-up-to-logs calibration cost.

The equally informed comparator receives the **entire code for free**, arbitrary adaptive POVMs and computation on each specimen, and unlimited classical memory. It may retain no quantum information between specimens. The stated likelihood-ratio argument gives transcript TV at most `T/(2^k+1)` on a hard ensemble, hence worst-case success 2/3 requires

```text
T >= (2^k+1)/3.
```

This is a quantum-memory/specimen-count comparison, not an unconditional runtime or hardware advantage. The upper bound is uniform over the declared noise class; the lower bound holds already on the noiseless or fixed hypothesis-independent-channel subfamily. Hypothesis-dependent faulty preparation could leak the answer, so the rigorous statement is **minimax**. [Source, lines 255–328](P3_PROTECTED_QUANTUM_READOUT_20261105_RETURN.txt#L255-L328).

## Preparation, hardware, synchronization and total work

Known hard-family states require no Haar-state oracle: choose logical Pauli eigenvalues with the required product, prepare their product eigenstate, and forget a fresh independent seed for each bank. The acquired signed stabilizers and logical eigenvalues specify known Clifford preparations, including logical Y. The conservative ideal size is `Theta=O(kL^4)` **before routing**; actual routing, reset and idle locations must be included.

The source invokes Christandl–Fawzi–Goswami Corollary 45, Eq. (138), as an external physical-output factory bridge. Under its circuit-stochastic assumptions, it states a factory approximation `||Phi_phys-W compose Phi_ideal||_diamond <=4Theta(cp)^r`, with local support parameter `2cp`. For `C=R(t+u)+2M+2` prepared banks, the explicit logarithmic choice of r pays the total factory failure allocation. No numerical threshold for an unspecified architecture is asserted.

One finite reader uses matched-pair `J Z_A Z_B`, local controls of norm at most `Omega/2`, finite ramps and terminal Z measurement. With allowed ramp time tau_r, its Bell-readout window is bounded by

```text
tau_B <= 5pi/(2Omega) + pi/(4|J|) + 4tau_r + tau_read.
```

Slew is finite and paid. Actual independent dephasing during that window gives pair-fault probability `1-exp(-2lambda tau_B)`. Factory, gate, readout and waiting contributions must jointly satisfy a condition of the form

```text
q <= 4cp + q_gates + q_readout + q_wait < 1/36.
```

There are N matched couplers and parallel control channels. The two banks must be synchronized or retained protected inside their factories until release. Leaving a bare bank waiting through growing preparation time would violate the noise budget. Integrated pulse-error precision is separately charged; the required calibration is not inferred from a simulation.

| Execution component | Cost reported in the source |
|---|---|
| Calibration | `R(t+u)` specimens; O(N) local gates and N readouts each |
| One Bell row | N CNOTs, N Hadamards, 2N readouts |
| Reader quantum storage | Two N-qubit banks during bounded release skew and readout |
| Known-state factories | `C Theta poly(r)` locations, including preparation/reset |
| Classical acquisition | `O(RN^2 t log N+H(u+log N))` bit operations |
| Classical decoding | `O(kL^6)` per row with blockwise dense blossom matching |
| Final inference | `O(Mk^2)` binary elimination |

Raw readout may finish before classical decoding, or calibration may finish before fresh specimens are requested. Neither schedule requires the unknown specimen to remain coherent throughout classical processing. [Preparation and control, lines 329–415](P3_PROTECTED_QUANTUM_READOUT_20261105_RETURN.txt#L329-L415); [resource table in the preserved rendered ending, lines 418–503](P3_PROTECTED_QUANTUM_READOUT_20261105_RETURN.txt#L418-L503).

## Reported execution, finite point and evidence boundary

The source reports a scrambled `[[50,2,5]]` torus run recovering all 50 signed checks, including 18 negative signs, with no false or missed checks; genus and both distance-five graphs were recovered. Its collision learner used 113,269 quartet verifications versus 230,300,000 exhaustive pattern/support tests on the same records.

It also reports 4,800 noisy Bell rows; an 800-wire/32-logical-qubit data-path check **reusing** the acquired block rather than rerunning full 800-wire calibration; and signed-reference checks. Reference stabilizer specifications were checked, but physical noisy factories were not simulated.

One reported conservative analytic point is `k=32, L=19, N=11,552, q=q_c=.003`: 694,998 prepared banks, 75 corrected Bell rows and 866,400 physical Bell gates, with learning/readout error below `.007251` before factory and separate control budgets. Allocating `.002` to those budgets keeps the stated full bound below `.01`. The source explicitly notes billions of wire readouts and substantial classical work. This is not an economical present-day hardware claim.

These executions and certificate values were producer-reported in the visible answer. **The subsequently authorized original ZIP and all 21 members are now supplied**, including the complete theorem, program sources, raw simulated calibration records, recorded results and rational-certificate files. They are preserved without execution, recompilation, new reproof or novelty audit. No separate independent reviewer artifact is inferred from the label “finite audit.”

At the initial publication the ZIP was uncollected. A later human instruction authorized collection and the original was supplied. Its nested earlier communication ZIP is byte-identical to the already authorized/public archive (SHA256 `623b20c473c15ea3b58ab3b212b1be68a13774beaffdcdb8aaefbebea270f3d2`). The earlier communication/cavity theorem scopes remain unchanged, and no unrelated source-recovery permission is inferred. The visible return's scientific body is unchanged; only its updated local download locator is replaced with the public path. [Availability chronology and hashes](SOURCES.json).

### Original reproducibility artifacts and distinct algorithm variants

| Artifact | Public file |
|---|---|
| Complete theorem and physical costs | [protected_quantum_readout_theorem.txt](package/protected_quantum_readout_theorem.txt) |
| Reproduction/evidence boundaries | [Packet guide](package/protected_readout_REPRODUCIBILITY.txt), [finite-audit README](package/latent_code_bell_README.md) |
| Sparse acquisition proof | [Collision lemma](package/latent_code_collision_lemma.md) |
| Default recorded run | [latent_code_bell_result.json](package/latent_code_bell_result.json) |
| Preserved comparison runs | [Exhaustive acquisition](package/latent_code_bell_result_exhaustive.json), [dynamic-programming matching](package/latent_code_bell_result_dp.json) |
| Selected sparse exact certificate | [Recorded certificate](package/latent_code_collision_certificate.json), [program](package/latent_code_collision_certificate.py) |
| Older all-candidate/minimum-sample certificate | [Recorded certificate](package/latent_code_parameter_certificate.json), [program](package/latent_code_parameter_certificate.py) |
| Raw finite measurement records | [latent_code_calibration.bin](package/latent_code_calibration.bin) |
| Learned signs and reference specifications | [Signs](package/latent_code_acquired_signs.json), [reference specifications](package/latent_code_reference_specifications.json) |
| Main program and licensed matching implementation | [Program](package/latent_code_bell_check.py), [blossom implementation](package/latent_code_blossom.py), [retained BSD notice](package/latent_code_networkx_LICENSE.txt) |
| Finite scanner sources | [Exhaustive scanner](package/latent_code_scan.cpp), [collision scanner](package/latent_code_hash_scan.cpp) |
| Original archive and supplied checksums | [ZIP](original/protected_quantum_readout_reproducibility.zip), [SHA256SUMS](package/SHA256SUMS.txt) |
| Unchanged earlier communication packet | [Nested original ZIP](package/preserved_communication/lossy_measurement_port_reproducibility.zip) |

The selected sparse large analytic point uses 694,998 prepared banks for the signed task. The older all-candidate certificate has a different acquisition/copy count; it is not silently substituted for the sparse learner's runtime claim. The larger point and physical noisy factories were not simulated. The finite C++ scanners are bounded audit implementations (at most 64 wires and 256 rows);the mathematical algorithm uses arbitrary-length bit strings. Statistical statements assume fresh independent shots or uniform conditional versions of their bounds;finite calibration does not certify unrestricted drift. In physical size, the learning lower bound is `exp[Omega(N/log^2 N)]`,not `exp[Omega(N)]`. All preparation,factory,control,waiting and failure costs remain as stated above. [Complete source](package/protected_quantum_readout_theorem.txt).


The source credits known stabilizer-code learning, transversal Bell readout, toric-code recovery, protected quantum learning and fault-tolerant uploading. It preserves the earlier lossy assisted-communication theorem and its finite-cavity operating point at their original scopes. Protection, paired-wire access and the declared local noise/factory conditions remain essential; this does not solve arbitrary unknown-code learning, general noisy experimental acquisition or coherent transfer of an already exposed unencoded input.

[Source metadata and exact byte hashes](SOURCES.json) · [Other supplied results](../README.md)

This is a directly navigable GitHub scientific result entry. No large generated retrieval-index build, scientific replay, reproof or novelty audit was performed for publication.