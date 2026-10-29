# Frozen resonant-fiber construction

Read `PRIOR_AND_DECISION.md` first. This branch is not a new broad/practical
many-body capability claim. The retained input/output and proven errors are
in `PROOF.md`; the same-source dynamical failure of exact resonance selection
and its detuning-resolved repair are in `PROJECTOR_OBSTRUCTION.md`.
The parent whole scientific acceptance is recorded separately in
`ROOT_WHOLE_REVIEW.md`.

Actual outputs are `EXACT_SOURCE_CHECK.json`, `QUADRATURE_ACQUISITION.json`,
`TAYLOR_EXECUTION.json`, `TAYLOR_RAW.json` and `PREDICTION.json`.
`FROZEN.json` binds their source versions; hashes are preservation, not a
substitute for the mathematical proof or a physical qualification.

The frozen pipeline was executed once. To reproduce, first copy this folder
to an independent working location so its receipts are not overwritten.
Use Python with NumPy and a compiler supporting signed `__int128`:

```sh
python check_resonance.py
python acquire_quadrature.py
clang++ -std=c++17 -O2 taylor.cpp -o taylor
./taylor QUADRATURE.txt TAYLOR_RAW.json
python receive_prediction.py
```

The source check and mathematical receiver use standard-library exact
rationals; NumPy supplies only proposals for quadrature roots, whose exact
sign/weight qualification is performed before use. No original-time
many-body trajectory, state vector, source sampling or Hilbert-space
diagonalization enters this pipeline. A new run's timing must be kept
separate from the original receipts.
