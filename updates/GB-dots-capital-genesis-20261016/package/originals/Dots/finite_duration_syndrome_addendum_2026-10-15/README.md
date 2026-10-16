# Finite-duration and syndrome-measurement addendum

This separate research addendum extends the interface analysis in the earlier coherent-memory packet. It does not replace that packet or establish a hardware realization. Read the three results separately: finite correction duration, its restricted composition with an atomic joint post-error, and an ideal syndrome-measurement alternative to frame randomization.

## Dependency and reading order

The required earlier packet is coherent_memory_packet_2026-10-15.zip, SHA-256 b2e1ed52cf2b4e9533e24599fc75699ec5ad4adb57a1ff80e7d56a18376b815d, 106,260 bytes. It remains byte-for-byte unchanged. Extract both ZIPs under one parent directory with their directory names intact to resolve the relative references. DEPENDENCY.json records the exact dependency. The finite checkers here can run without extracting the earlier packet, but their success does not replace its theorem dependencies.

1. finite_duration/LIMITED_START_CLOCK_THEOREM.md and INDEPENDENT_BRIDGE_CHECK.md: fixed-duration correction gadgets, skipped-start saturation, individual bad gates, finite-window flags and rate-duration tradeoff.
2. finite_duration/COMPOSED_POST_ERROR_INTERFACE.md and INDEPENDENT_COMPOSITION_CHECK.md: restricted composition with the earlier joint-bath character instrument. The statement includes the actual-record definition requested by its audit.
3. syndrome/SYNDROME_SANDWICH_ALTERNATIVE.md and SYNDROME_SANDWICH_AUDIT.md: a distinct ideal pre/post syndrome measurement instrument with genuine mismatch labels.

## What the finite-duration result assumes

Starts are independent exogenous rate-κ Poisson streams. Duration τ is fixed; gate count, supports and conflict incidence are bounded. Every clean correction receives actually reset private ancillas and realizes exactly the completed correction on arbitrary joint inputs. Conflicting, dirty, pending and skipped attempts are charged, with their individual local gates retained in chronological order. Long conflict components are never contracted into a single bounded fault. Selected completion clocks are not assumed Poisson.

For the composed joint-bath result, EVERY ideal correction gate acts as identity on the persistent bath. A merely bath-independent composite circuit is insufficient, as the exact CNOT-echo counterexample shows. Only these ideal correction gates are serialized to their starts. The bath-coupled randomized post-error remains an ATOMIC assumed primitive at completion. Its duration and physical implementation have not been established.

## Probability and channel statement

With x=κτ≤1 and Δ=Cb/κ, the additional conservative block budget is

    A0 ν/κ + B0 κτ + C0 δ_coh²,
    A0=F(Cb+2), B0=N[2D(Cb+2)+1], C0=N(Cb+2).

The base δ_ideal contains slow and fast terms only. Geometry, full spacetime dependence, dirty ancillas and the local terminal strip are charged as stated in the proofs. For fixed ν and τ, the first two terms have minimum 2√(A0 B0 ντ) only when the minimizing rate obeys all admissibility constraints. Failing this conservative sufficient budget is not an impossibility result.

The good CP map is selected by a fixed input-independent predicate on ACTUAL instrument records, not by a state-dependent auxiliary Bernoulli coupling. Good=Id_logical⊗Λ_good with Λ_good trace-nonincreasing. The reference coupling bounds the bad effect uniformly; bath completion gives the 2ε joint-input diamond bound.

The resulting memory statement is pointwise for each DETERMINISTIC endpoint T, with one fixed ideal decoder and the earlier asymptotic size/noise hypotheses. It does not establish an adaptive-stopping-time guarantee or a single physical homology trajectory valid at all intermediate coherent states. Initial logical–bath–reference entanglement is allowed under the fixed finite-dimensional auxiliary/bath assumptions.

## What the syndrome alternative changes

Ideal local check measurements before correction and after a bounded joint post-error yield genuine predicted-versus-observed syndrome labels with conditional mismatch probability at most δ². This trades private fresh-frame and frame-independent-error assumptions for actual ideal measurement backaction, truthful records and a uniform norm bound conditioned on genuine records. The aggregate inactive correction branch is not reinterpreted as a full syndrome measurement.

This measured composite event is a separate ideal interface. These documents do not prove a finite-duration implementation of the entire syndrome sandwich, noisy measurement circuits, noisy readout or unrestricted record-driven feedback. Its coexistence in this ZIP must not be read as an automatic composition of all three results.

## Scope and verification

The arguments depend on the earlier support, forcing, domination, torus/homology, common-decoder and quantum transfer modules, including the Hartarsky–Toninelli/Toom-contour imports. The reviews are mathematical checks under stated premises, not external referee validation or a formal machine proof. No hardware feasibility, autonomous finite controller, new noise-tailoring principle, practical numerical threshold, general faulty-clean-gate theorem or arbitrary continuous system–bath coupling theorem is claimed.

The syndrome construction applies the established QEC syndrome-projection principle. Asynchronous decoding and finite decoder latency are established concerns; the finite-duration source gives relevant prior-art links. Historical originality of these tailored interfaces remains unresolved.

## Replay and integrity

With Python 3.12 and SymPy from requirements.txt installed, run:

    python3 verify_manifest.py
    python3 replay.py

The runner accesses no network and installs nothing. Assertions must remain enabled. SHA256SUMS hashes every included file except itself. Source scientific texts are copied with only file-reference paths changed; PROVENANCE.json gives original source hashes. Executable certificates are byte-exact copies. See verification/ for captured results and their limited meaning.

To verify the prior dependency too, provide its ZIP:

    python3 verify_dependency.py /path/to/coherent_memory_packet_2026-10-15.zip

To rebuild this archive deterministically in the same Python/zlib environment:

    python3 build_archive.py /path/outside/addendum/rebuilt.zip
