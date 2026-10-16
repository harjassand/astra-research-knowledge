# Finite-pulse hardware comparison: randomized and bounded-control DD

Date: 2026-10-16. Bounded primary-source check. This supplements the refresh robustness audit; it is not an exhaustive priority search.

## Verdict

Physical random Pauli/stabilizer applications are established operations. The full control path, always-on drift during finite pulses, bounded noise norms, and pulse-duration overhead are standard concerns in dynamical decoupling (DD). The finite-pulse Bell-state witness demonstrates a failure of a proposed zero-odd-action qualification, not a previously unknown general DD obstruction.

Do not compare the proposed hardware module only against uncorrected square pulses or describe all prior DD results as leading-order heuristics. There are rigorous random-decoupling bounds, full-remainder finite-width bounds, dynamically corrected gates (DCGs), and explicit DD-to-fault-tolerance integration.

## Primary comparisons

### 1. Random decoupling: direct antecedent of randomized physical controls

[Viola and Knill, Random decoupling schemes for quantum dynamical control and error suppression, PRL 94, 060502 (2005)](https://arxiv.org/pdf/quant-ph/0511120).

Theorems 1–2 assume group-valued random controls with specified independence and a uniformly bounded Hamiltonian or system-bath interaction. They prove an ensemble worst-case error bound of order T Delta_t lambda^2 in its stated small-error regime. The framework explicitly extends to open systems, and discusses selective/reducible groups and random–deterministic hybrids. Thus physical group randomization and its error-suppression role are not new. This is a rigorous asymptotic-regime bound, not merely an averaged first-order Hamiltonian calculation. It does not state the present sharp scheduled multi-parent endpoint/support product with unrestricted common bath.

### 2. Eulerian DD: full finite pulse paths are already the object analyzed

[Viola and Knill, Robust dynamical decoupling with bounded controls, PRL 90, 037901 (2003)](https://arxiv.org/pdf/quant-ph/0208056).

Equations (7)–(9) average the drift conjugated by the entire generator-pulse trajectory, then group-average the result. Their theorem gives the desired group symmetrization for controls in the decoupling-group algebra. Robustness covers a stated class of repeatable implementation errors. The symmetrized object is the leading average Hamiltonian, with the fast-control approximation and higher-order corrections explicitly distinguished. An endpoint-equivalent implementation that violates the full-path algebraic condition is therefore not automatically covered. This directly supports charging the Bell-witness drift in the toggling frame.

### 3. DCGs: stronger comparison for implementing a protected nontrivial S

[Khodjasteh and Viola, Dynamical quantum error correction of unitary operations with bounded controls, PRA 80, 032314 (2009)](https://arxiv.org/pdf/0906.0525).

This work treats bounded-control gate implementations in a system–bath model, defines the error phase along the whole control trajectory, and constructs first-order corrected target gates using balance pairs. Section III C's black-box no-go result explains why arbitrary endpoint-equivalent implementations cannot generically be composed into a corrected nontrivial gate; implementation relations are required. The hypotheses include bounded error/bath norms and perturbative conditions. This is a direct gate-level competitor, more relevant than comparing only to an unprotected physical stabilizer pulse.

[Khodjasteh, Lidar, and Viola, Arbitrarily accurate dynamical control in open quantum systems, PRL 104, 090501 (2010)](https://arxiv.org/pdf/0908.1526).

Concatenated DCGs extend cancellation to an arbitrary specified perturbative order using finite control resources. Equation (4) states an error bound with explicit growth from sequence duration and concatenation; for fixed switching time the best level is finite. It is stronger than first-order Eulerian DD as a constructive bounded-control comparator. Its bounded total error Hamiltonian, available control reversals/stretching, and duration overhead must be matched before importing its guarantee.

### 4. Strongest direct hardware-to-fault-tolerance comparator found

[Ng, Lidar, and Preskill, Combining dynamical decoupling with fault-tolerant quantum computation, PRA 84, 012305 (2011)](https://arxiv.org/pdf/0911.3202).

Use Section V, equation (51) and Table I for certified full-remainder noise bounds; Section VI C for finite-width Eulerian schemes; Section V C for the fault-tolerance comparison. This is the closest complete established competitor identified. Its Section II B local-bath condition requires commuting bath operators for simultaneous disjoint locations. Hence its circuit-level qualification cannot simply be transplanted to an unrestricted shared bath. The pulse/noise Hamiltonians and resource assumptions still offer a concrete baseline for a local module.

For an additional explicitly rigorous finite-width norm analysis, see [Khodjasteh and Lidar, PRA 78, 012355 (2008)](https://arxiv.org/pdf/0803.4320), especially the error-phase treatment and finite-pulse contribution in the discussion of equation (97). It already charges noncommuting residual system terms and finite-width pulse errors.

## What is actually different in the refresh project

The different mathematical target is a sharp finite-action syndrome-endpoint/record-event effect for specified actual refresh channels, tensorized through independent causal testers against unrestricted joint memory. The scheduled own-entry/retirement construction and actual-channel support refinement are additional interfaces. They cannot be replaced by merely showing that an average Hamiltonian vanishes. Conversely, such a mathematical endpoint theorem does not supply a competing pulse-design or experimental qualification theorem.

A hidden I/S coin implements the dephasing channel (Id+Ad_S)/2 exactly only when its physical branches implement those operations jointly on the persistent system/bath boundary and its record remains inaccessible wherever the theorem requires. DD often keeps and compensates a control trajectory in a toggling frame. These are different channel objectives using familiar control operations; the physical random-Pauli operation itself should receive no novelty claim.

The Bell witness's baseline was declared free because it preserved the original good projector. During the compiled path it is no longer harmless. In a standard toggling-frame/DD analysis that drift is included automatically. The witness therefore locates the missing qualification assumption; it does not rule out an Eulerian or DCG repair.

## Practical gate before a hardware claim

Specify the actual available generators, full always-on system/bath Hamiltonian, norm or correlation bounds, maximum amplitude, minimum switching time, and footprint. Compare the proposed pulse against an Eulerian/DCG implementation under those SAME resources. Include total durations, endpoints, fresh-record isolation, and reservation conflicts.

A useful bridge is elementary: a full-joint operator-norm estimate ||U_actual-U_target||<=eta implies half-diamond channel error at most eta. A common free bath unitary can be absorbed into the prover/comparison frame if done consistently. For private random branches, convexity bounds the averaged channel error by the average of these branchwise joint errors. Reduced-state fidelities alone do not provide that qualification. Once the resulting local full-joint epsilon budget is established, the separate first-fault causal refresh transfer can use it.

Conclusion: the strongest defensible claim is a distinct sharp causal endpoint/support interface that may accept known DD/DCG hardware certificates. It is not a new random-Pauli control primitive, a first recognition of finite-pulse drift, or a demonstrated hardware improvement over established DD constructions.
