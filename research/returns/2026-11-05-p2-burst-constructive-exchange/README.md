# P2 constructive exchange: finite-seed recovery under Pareto bursts

P2's completed 5 November return supplies the positive construction for P3's selected scheduled-circuit question. Within the finite-local-hit-rate Pareto regime `alpha > d`, the supplied result is

\[
\text{fixed finite-seed classical recovery at sufficiently small positive intensity}
\quad\Longleftrightarrow\quad \alpha>d+1.
\]

The negative half is [P3's complete-cone obstruction](../2026-11-05-p3-burst-recoverability-opening/README.md). The positive half uses a local concatenated repetition circuit with a forced-output invariant and a separated Poisson-source argument. The original proof and the attached implementation are preserved here. This is a theorem under the declared circuit premises; physical manufacture, measured performance and a quantum-memory construction are separate questions.

## Read the proof and original implementation

| Entry | Contents |
|---|---|
| [Complete supplied return](P2_CONSTRUCTIVE_EXCHANGE_20261105_RETURN.txt) | Exact issued prompt, complete rendered answer and expanded activity, and the available native verbatim prefix |
| [Forced-output gadget and burst recurrence](forced-output-and-noise.md) | Malformed-input semantics, locality, two separated child failures and the actual recurrence |
| [Encoding, readout, implementation and costs](implementation-and-resources.md) | One-bit ascent/hold/descent, total error, footprint, full operation count and source-reported finite tests |
| [Original burst_gadget.py](original/burst_gadget.py) | Original code attachment downloaded from the producer chat; preserved without execution |
| [Source and publication metadata](SOURCES.json) | Exact byte sizes/hashes, provenance, source scope and publication boundary |

The producer chat is [P2 constructive exchange](https://chatgpt.com/c/6aec168c-f3c0-83ec-afa0-fd470a8c62e5), GPT-6 Pro in normal Chat, observed completed at 08:48 UTC on 5 November 2026 (6:48 PM Brisbane). No ZIP was supplied. The original loose code attachment was retrieved separately from the visible file viewer. Rendered mathematics may be degraded; the native prefix ends during section 6 because of the source reader's 20,000-character limit. Nothing missing has been reconstructed.

## Exact positive contract

Fix dimension `d >= 1`, the Pareto law `Pr(R > r) = r^(-alpha)` for `r >= 1`, and `alpha > d+1`. The construction fixes its architectural constants first. For every sufficiently small fixed positive burst intensity, a uniform algorithm produces a finite input-independent layout and schedule for each requested horizon `T`.

Only physical cell 0 initially contains the unknown bit. All other prebuilt data and work registers are input independent and may be arbitrary. The circuit uses a fixed finite local gate basis, nearest-neighbor operations and bounded update rate. Bursts may arbitrarily replace every mutable register they reach, including encoding, repair and decoding workspace. No erasure flags or analytical badness labels are available to the device.

Immutable local gate laws and an input-independent schedule are explicit immune premises. They are not inferred protected mutable controllers. The input-dependent seed stays one bit independently of `T`; expansion is performed under noise. Total worst-input error is at most `1/4`, including encoding, holding, local decoding and the terminal read window. The claim supplies one requested output per execution. It does not require simultaneous success of an infinite stream or arbitrarily small error at one fixed noisy cell.

## Ambient bursts reaching a wire

Put the mutable registers along a coordinate axis. A cubical radius-`r` burst reaches it from a transverse center volume `(2r)^(d-1)`. The exact reduced marked intensity is

\[
\lambda 2^{d-1}r^{d-1}\nu(dr)\,dx\,dt.
\]

For the stated Pareto density this becomes the one-dimensional interval-burst law with

\[
a=\alpha-d+1,\qquad
\lambda_1=\lambda 2^{d-1}\frac{\alpha}{a},\qquad
\Pr(R>r)=r^{-a}.
\]

Thus `alpha > d+1` is precisely `a > 2`. Centers outside the wire are included. The strict margin allows a repair duration `L^kappa` with `1 < kappa < a-1`, replacing the earlier demand for exactly linear repair.

## What is established and what remains separate

The supplied proof closes the selected strict-Pareto positive target through the deterministic forced-output lemma, separated Poisson-source recurrence and paid finite-seed encoding/readout. Its source-reported finite implementation checks concern a smaller deterministic instance. They do not numerically establish the all-level probability theorem. Capital preserves those checks at their supplied scope and performs no new scientific replay or audit.

General sufficiency under only `E[R^(d+1)] < infinity` for an arbitrary non-Pareto law is not proved here. Autonomous fabrication, finite-sample certification of an unrestricted tail law, laboratory hardware, quantified practical advantage, exhaustive historical priority and quantum positive recovery are not claimed. The code is an original executable artifact, not a proof-assistant certificate or a new independent external validation.

P1's [full source-conditional quantum loader](../2026-11-05-p1-thermal-memory-opening/package/selection_brief.tex) and [existing-method comparison](../2026-11-05-p1-thermal-memory-opening/package/csw_bdl_comparison.md) retain their actual scope. P2's [local thermal intervention](../2026-11-05-p2-local-thermal-trials/README.md) retains its physical access and entropy-budget claims. Neither supplies an unproved bridge into this burst-memory class.

This direct GitHub publication adds source files and agent navigation. Generated current retrieval has not been rebuilt. No source program, solver, simulation, PDF build, numerical array load or heavy corpus build was run.
