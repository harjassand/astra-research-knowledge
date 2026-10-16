# Qualified correction-core addendum

This separate addendum relaxes the earlier exact quantum-core assumption to specified noisy Clifford cores under actual fixed-core conjugation covariance. The scheduled composition and its support/probability audit pass under the explicit strong premises. It does not qualify every component of a correction controller. Previously delivered archives remain unchanged.

Start with HANDOFF.md, core/SCHEDULED_QUALIFIED_CORE_MEMORY_THEOREM.md and core/SCHEDULED_CORE_SUPPORT_PROBABILITY_AUDIT.md. Read core/GATE_INTERFACE_AND_OBSTRUCTION.md and its audit for the compiler convention and counterexamples. The refinement and detector modules below are separately scoped.

## Main mathematical change

For an intended Clifford C, use input Pauli T, the SAME noisy physical core C W for every seed, and output Pauli C T† C†. The resulting operation is C T† W T. A finite-duration fixed-core interaction-picture construction supplies the corresponding actual conjugation form under its common-dilation premises. Full Pauli frames cover the entire quantum gate support, including extraction ancillas. This is a qualification assumption about the implemented compiler, not a consequence of small isolated-gate infidelity.

A gadget's joint subset strength is

    p_g = sup_b Σ_(e in gadget b) a_e².

If any gate character is nonzero, the WHOLE gadget is charged throughout its reserved interval, including possible omission of its correction at the start. The appropriate parent window is [t−τ,t+Δ], not a completion-only window. With μ_int≤κN(Δ+τ), the local-stochastic bound uses

    q = [d0+p_g μ_int]^(1/Q).

All geometry and support counts must be recomputed for extraction, wrappers, records and reset. The earlier constants cannot be reused without this recount. Gate/gadget characters are global final Kraus indices; there is no small chronological conditional probability or independent physical fault-mixture claim.

The same fixed ideal decoder then gives the conditional asymptotic memory bound min(2,A L⁴(1+κT)exp(−cL)) at each deterministic T, for sufficiently small parameters and sufficiently large compatible sizes, under the theorem's named imports. No adaptive-stopping-time guarantee or actual all-times Pauli trajectory is established.

## Genuine syndrome refinement

The target is C_ref=C D_R. Measuring finer checks changes the full-input channel on syndrome coherences; it preserves every encoded Pauli-orbit transition and therefore the universal common-decoder proof. The eight incident sweep checks really resolve the decision, with a 24-plaquette data-support union. Ancilla, circuit and timing resources remain additional costs. The refinement audit and exact checker are in refinement/ and checks/refinement/.

## Still ideal or separately qualified

Exact or qualified wrappers; actual fresh per-attempt ancilla and local-record reset; ideal measurement; protected record storage/transmission; exact classical lookup and branch selection; private independent frames; fixed padded timing; exogenous starts; full reservation cleanliness; ideal encoding and final recovery. Protected records cannot be flipped or coherently mixed by the bath or error terms. Every selected frame must complete independently of endogenous outcomes. Errors in those retained ideal resources are not automatically covered by noisy-core qualification.

The all-zero-character gadget needs only its intended unnormalized per-record orbit transition, possibly with bath filtering. It need not be a normalized ideal channel tensor a common bath channel. The global support-good map is CP trace-nonincreasing, and the uniform bad effect is handled by bath completion.

## Two essential obstructions

A compiler that changes the noisy drive with its frame can leave calibration error entirely in character zero. In the exact example, every logical gate is C E rather than C, while all nontrivial characters vanish. This does not contradict the positive fixed-core construction; the compiler assumptions differ.

A mutable stored syndrome can also be corrupted by an identity-on-data error, remain invisible to data characters and select wrong feedforward. Protected records and fresh per-attempt initialization are substantive premises.

## Separate deletion-null detector module

The optional detector_separate/ module contains an independently checked abstract lemma and protected ideal-syndrome application. Fixed commuting actual output flags satisfy a product-action-squared subset bound when the SAME whole dilation obeys exact deletion-nullness for every counterfactual interpolation. No private frame is needed for that lemma.

This module trades ideal frame resources for trusted pre/post measurements, a protected intended target and an exact comparison. The target must come from the trusted prelabel; predicting from a potentially wrong internal gadget decision can miss every wrong correction. Its exact scripts demonstrate that obstruction and an unframed crossing-pulse example. It does NOT qualify faulty detectors, corrupted records or generic noisy measurement, and no additional scheduled detector-memory theorem is asserted merely by including it here.

## Review status and dependency limits

Core, refinement, detector and scheduled-composition audits are included. Historical files titled CANDIDATE retain their original development labels; their accompanying audits supply the current scoped verdict. These are independent internal mathematical reviews, not external validation, a formal machine proof, hardware evidence, a useful numerical threshold or priority certification. Randomized compiling, Pauli randomization and syndrome projection are established prior art, attributed in the core report.

The three earlier frozen packets are named and hashed in DEPENDENCIES.json. They supply the global subset lemma, local-stochastic contours, support/homology and common-decoder imports. Extract all archives under the same parent with their directory names intact for portable relative references. The current benchmark and future gate/controller work are excluded.

## Reproduction

Python 3.12 and SymPy 1.14.0 were used. With requirements installed, run:

    python3 verify_manifest.py
    python3 replay.py

The five exact scripts are separated into core, refinement and detector folders. There are no floating-point tests in this packet. The replay uses no network, installs nothing and requires assertions enabled. Captured results and their scope are in verification/.

Verify the three older ZIPs in the order listed in DEPENDENCIES.json:

    python3 verify_dependencies.py COHERENT.zip FINITE_DURATION.zip OVERLAPPING.zip

Rebuild deterministically in the same Python/zlib environment:

    python3 build_archive.py /path/outside/addendum/rebuilt.zip

SHA256SUMS covers every included file except itself. PROVENANCE.json records source hashes and limited copy edits. Source scripts are byte-exact. Fresh-extraction replay and prior-archive integrity are checked before delivery.
