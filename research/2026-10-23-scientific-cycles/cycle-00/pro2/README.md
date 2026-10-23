# Astra PRO2 restored scientific checkpoint

This is the source and replay package for a checked finite-precision
spectral-distribution construction. It contains a positive sharp completion
theorem and a scoped practical defeat on an actual public structural matrix.
It does not reopen the retired molecular calculation.

Read **RESULT.md** for the outcome and decision, **PROOF.md** for the integrated
argument, **COSTS.md** for resource boundaries, and **CONTINUATION.txt** for the
next owner-selected scientific step.

## Replay the delivered result

Requirements: Python 3.12 or compatible; NumPy, SciPy and threadpoolctl. The
recorded versions and platform are in results/experiment_resources.json.
Matplotlib is needed only for the optional figure. No internet, API token,
licensed solver, GPU, remote calculation or external source retrieval is needed
to replay the delivered witnesses.

From the extracted archive directory:

```bash
python3 src/verify_manifest.py
python3 src/run_experiment.py --replay
python3 src/diagnose_error.py
```

The replay recomputes input allowances, saved-bit probes and coupling, exact
integer residuals, Sturm/weight certificates, dense completeness and all CDF
envelopes. It does not invoke a floating eigensolver or draw new probes. It
updates only replay receipts. Verify the original manifest before replay so
updated timing receipts do not appear as unexplained source changes.

The producer command is `python3 src/run_experiment.py --run`, but it must be
used in a separate copy with an empty witnesses directory: generation refuses
to overwrite or redraw the delivered bit block. This is a fresh experiment,
not replay of this archive. No fresh run is needed for integration.

Independent small challenges are in checks/ and notes/check_*.py. The complete
replay command above is the integration gate. Diagnostic floating tests are
explicitly separate from exact certificate arithmetic; their receipts are
retained alongside exact examples and deliberate rejection tests.

## Files and exact boundary

- sources/bcsstk08.mtx.gz and bcsstm08.mtx.gz are the original compressed
  public decimal data. Both source digests are checked during replay.
- witnesses/ contains the actual saved bits, dyadic probe matrix, Krylov bases
  and Jacobi matrices, and a complete dense eigenbasis/diagonal proposal.
- results/ contains exact rational budgets, independently bound quadrature
  certificates, every displayed interval, cost receipts and unedited logs.
- notes/ preserves local mathematical arguments, implementation challenges,
  deliberately rejected inputs, earlier Gaussian fixture interface, and the
  bounded literature comparison.
- figures/ contains a scientific display and its source script is in src/.
- HISTORICAL_STATE.txt pins the retired source and common restoration packet.
- protocol/AGENT_HANDOFF.txt is the supplied private-handoff protocol.

The two consulted arXiv PDFs are identified by URL and digest in SOURCES.json;
their full texts are not duplicated in this source package. All local proof and
replay material needed for the construction is included. DKWM and classical CMS
are named imported mathematical theorems with exact statements and references.

## Status

Producer run: complete. Exact full replay: passed. Separate theorem/code
challenges: passed after the documented repairs. Practical whole-CDF advantage
on the tested matrix: rejected. Historical priority of the combined construction:
not established. Private upload is distinct from Max's receipt verification,
repository integration and scientific acceptance.
