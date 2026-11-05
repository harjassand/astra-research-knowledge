# Continuous-time autonomous quantum correction: the earned local service and missing global theorem

The strongest live opening in this dossier is continuous-time autonomous quantum correction with noisy local controllers. **The north star was not achieved.** A bounded local quantum-service mechanism and sparse service-failure witnesses are proved. Preserving physical quantum gate order and protected idle periods throughout noisy controller repair remains the decisive global theorem.

The separate fully frequency-resolved bath obstruction is a proved limitation of a thermal model/transfer argument. It is not a fixed-microscopic-coupling impossibility theorem for physical quantum storage. Earlier Gibbs results remain unchanged and are not equated with stationarity, preparation or memory.

## Governing sources

| Read | Contents |
|---|---|
| [Complete supplied dossier](NORTH_STAR_RESEARCH_DOSSIER.txt) | Outcome, exact proved/open boundaries, strongest incumbents and appended full accepted proofs |
| [Sparse service appendix](package/north_star_round/poisson_service_appendix_a.txt), [researcher C](package/north_star_round/researcher_c.txt) | Final adaptive-start fixed-box service proof and remaining causal-frontier operation |
| [Secular bath and cold-start obstructions](bath-and-cold-start.md) | Arbitrary-encoder/decoder bound, affine genericity, physical-time caveats and failed domination route |
| [Comparators and global construction](comparators-and-open-operations.md) | Incumbent autonomous correction, classical control, passive memory and actual missing quantum induction |
| [Original research record](original/SCIENTIFIC_OPENING_RECORD.zip), [package guide](package/README.txt) | All 38 original members across both research rounds |
| [Source-cache index](package/source-file-index.json), [publication metadata](SOURCES.json) | Primary source URLs/cache hashes and exact delivered-byte map |

The dossier is a research record dated 5 November 2026, with exactly three independent researchers alongside the principal as reported by the source. Existing internal derivations, audits and exact checks retain their actual scope. Capital did not spawn researchers, rerun their code or add a scientific audit.

The archive's `SOURCE_INDEX.json` is preserved byte-for-byte under the public member path `package/source-file-index.json` to avoid colliding with the repository's canonical discovery files. Its original name and every original member remain unchanged inside the ZIP. That index describes inspected source-cache bytes and references, not a release-member checksum manifest. Third-party paper PDFs are not redistributed. The package guide mentions a separate ledger not included in the two supplied artifacts; no ledger is reconstructed.

## Desired capability and the operation actually proved

The full target is finite-dimensional, bounded-density/range/rate, fixed local time-independent driven/dissipative dynamics in 2D or 3D, preserving unknown encoded quantum information for `exp(c L^a)` time under nonzero local noise on data, controllers, clocks and ancillas. Storage has no perfect global clock or noiseless decoder. Driven resets consume power and export entropy. A natural noise contract is a per-site bounded local GKLS/cb-norm perturbation independent of size and duration. No complete theorem for that capability is supplied.

The concrete local mechanism keeps main quantum registers in place. Per-register NEXTOP tags enforce causal eligibility; one owner acquires a gate's footprint locks atomically. A short reservation lease, one-shot in-place unitary and done flag prevent repeated execution across retries. A longer independent deadline commits even an omitted gate, advancing tags once and disabling old attempts. Gate hazard is independent of the reference-entangled input; controller progress never waits on the unknown payload.

Theorem S begins with **clean, continuously causally eligible requests and compatible ownership/tag states**. It does not repair arbitrary global scheduler states. Noise-damaged control records require the separately charged controller-damage/cleanup contract.

## Exact sparse service statement

On a bounded-degree conflict graph of degree at most `d`, fixed independent local grant, lease, unitary-attempt and deadline proposal clocks admit a forcing word of duration `S` with probability `p>0`. It clears clean leases, excludes competitors, grants the target and fires its unitary, regardless of outside clean state. Thus, after eligibility,

\[
P(\text{no }U\text{ by }t)\le(1-p)^{\lfloor t/S\rfloor}.
\]

For an `H`-stage final deadline of rate `nu_d`, put `h=H/(4nu_d)` and `m=max(0,floor(h/S)-2)`. Every adaptive-start omission is dominated by a fixed proposal-clock witness in a two-`h` box, with

\[
\beta_H=e^{-H(\log2-1/2)}+(2h/S+4)(1-p)^m.
\]

Coloring the squared conflict graph and time indices modulo 3 gives `chi=3(d^2+1)`, independent of `H`. For every fixed marked set of owner/start boxes `F`,

\[
P(\text{all marked service witnesses})\le\beta_H^{|F|/\chi}.
\]

The mathematical grid is an analysis device, not a physical clock. Fixed-box domination handles adaptive starts without conditioning on a retrospectively chosen failed window. Short leases and the done flag across retries are essential; holding all locks for the growing long deadline would not supply the same size-independent `p`.

## The global boundary remains open

Service after eligibility does not bound time waiting **to become** eligible. A repaired classical history must identify the correct physical quantum worldline frontier outside sparse damage. Every wait must execute protected lower-level idles or have a sparse bad-rectangle witness. A controller can keep a bounded-dwell heartbeat while its NEXTOP field makes no progress. Copying classical old/new histories cannot restore unknown quantum data or undo side effects.

The required theorem must preserve those frontiers and gate order through reconstruction, then prove a joint diamond-norm recursion for the actual quantum macro-locations, including general local GKLS perturbations. The service theorem closes one local counting contribution; it does not close that hierarchy.
