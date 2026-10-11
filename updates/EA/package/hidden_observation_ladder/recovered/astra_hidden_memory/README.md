# Astra hidden-observation ladder

Main result: an explicit family of rapidly mixing, rational hidden Markov chains needs exponential passive observation time to distinguish from equilibrium, while a specified conservative-field endpoint test takes polynomial time. The observed paths are exactly time symmetric; every joint distribution at up to 2r times matches equilibrium.

Read `proof_note.md` for the complete construction, proofs, interfaces, prior-art attribution, and unresolved limitations. This is an unreviewed research proof candidate. Historical priority and independent correctness are not established.

## Files

- `proof_note.md`: full mathematical record, including finite-field sample costs and a dimension-independent positive hidden-cost certificate.
- `test_lift.py`: exact rational and integer finite tests; entropy numbers are floating diagnostics.
- `test_response.py`: exact state-permutation and shortest-word checks, plus numerical matrix-exponential response tests.
- `check_results.json`, `response_results.json`: executed results, with exact/numerical status separated.
- `export_model.py`: explicit rational model exporter.
- `model_r1.json`, `model_r4.json`: exported models under the main theorem's normalization.
- `exact_run.log`, `response_run.log`: executed logs.

## Run

Python 3 with NumPy is needed for exact checks/export. SciPy is additionally needed for numerical response checks.

```sh
python test_lift.py
python test_response.py
python export_model.py 4 --output another_model.json
```

The dense exporter allocates a quadratic-size integer matrix, uses signed 64-bit entries with an overflow guard, and is not designed for enormous model sizes. The theorem's general construction is given algebraically in the proof note. No Monte Carlo implementation of the conservative sample budget or formal proof-assistant verification is included.

The thermodynamic statements use ordinary stationary time reversal with every hidden state even. The mathematical reversal permutation in the model file is not substituted as physical time reversal. The field law must be physically justified in any application.
