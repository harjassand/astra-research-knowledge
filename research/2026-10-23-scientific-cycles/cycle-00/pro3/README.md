# Astra Restore PRO3 20261021

**Current result:** forward KL alone does not preserve a proposal-start convergence guarantee after ordinary reversible local MH is added. With both forward and reverse KL bounded, the lazy random mixture has a finite uniform guarantee and a proved leading log-cost bracket. It is sharp when the reverse budget does not exceed the forward budget.

Start with `REPORT.md`. Current full proofs are `PROOF.md`, `JOINT_KL.md` and `JOINT_KL_FUNNEL_NOTE.md`. The latter two advance and supersede the tentative next question in `PROOF.md` Section 8. `CONTINUATION_SEED.md` identifies the remaining J>K boundary. `FAILED_APPROACHES.md` preserves failures and corrected premises.

## Replay

Core arithmetic needs Python 3.12 and the standard library. From this directory:

```bash
python verify_manifest.py
python experiments.py --output-dir replay_360 --digits 360
python experiments.py --output-dir replay_440 --digits 440
python joint_kl_checks.py
python compare_replays.py
```

The first two calculations write new directories. `joint_kl_checks.py` and `compare_replays.py` write their named result receipts; preserve the original archive if comparing resource timestamps. The comparison script checks the frozen principal and precision-check directories against independently coded evidence. Its logic and field-counting conventions are in the source. To compare newly produced replay directories, copy them into a separate extracted checkout under those names before running it.

`independent_counterexample.py` runs the separate stdlib checker. `plot_results.py` optionally uses matplotlib to redraw the included PNG/PDF from frozen results, without new sampling. Set MPLCONFIGDIR to a writable temporary directory if the runtime's default cache is read-only.

There is no private data dependency for the new mathematics or arithmetic. All distributions, graph proposals, thresholds and budgets are in the scripts and `INPUTS.json`; the numerical contract is `EXPERIMENT_CONTRACT.md`. These are full transition-law calculations, not trajectory simulations, empirical discovery or interval arithmetic.

## Sources and historical preservation

The `sources/` directory contains attribution, exact public URLs, hashes and focused theorem comparisons. Full downloaded papers are not embedded in this compact executable capsule. The mathematical arguments and replay are self-contained; the finite-support SIR/IMH dominance comparison is attributed to its cited primary theorem.

`preserved/` contains exact B3 checkpoint members and the immutable full archive's private identity/hash. Its original data, fits and failures remain available in that unchanged source archive. This delivery performs no new B3 or R3 scientific run. `authority/` records the restoration instruction and common handoff read for this allocation.

Private source handoff is for Max and the evaluator. Public publication is not authorized by this delivery. The final external receipt records the ZIP hash and exact native references after upload; the ZIP does not contain a self-referential archive hash. Upload success and producer replay are distinct from receiver verification and external scientific acceptance.
