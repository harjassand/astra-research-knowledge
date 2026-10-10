# N629 development verification pilot

This is a public, exposed development audit of an existing candidate. The finite
oracle is independently implemented from the definition, but its operator is
the same source-exposed audit agent. There is no independent external expert,
blinded evaluator, formal kernel, unseen task, or model comparison. No existing
card, source, proof gate, or evaluation ledger is changed.

Source revision: `90bd835a23d3ecdd8815b84ad2be8660389449b2`.
Branch: `foundry/n629-verification-pilot`.
Source directory:
`updates/CS/package/Astra_Global_Coupling_Proofs_2026-10-10_0708/independent_programme/additive_projection_gate_20261010/`.

## Reproduce

From the repository root on macOS or Linux, with Python 3.10 or newer:

```sh
python3 -m venv /tmp/n629-venv
/tmp/n629-venv/bin/python -B foundry/pilots/n629/archive.py verify \
  foundry/pilots/n629/results/raw-execution-evidence.zip \
  foundry/pilots/n629/results/raw-execution-evidence.manifest.json
/tmp/n629-venv/bin/python -B foundry/pilots/n629/run.py --output /tmp/n629-fresh-results
/tmp/n629-venv/bin/python -B foundry/pilots/n629/archive.py pack /tmp/n629-fresh-results \
  --prefix foundry/pilots/n629/results \
  --archive /tmp/n629-fresh-results.zip \
  --manifest /tmp/n629-fresh-results.manifest.json
/tmp/n629-venv/bin/python -B foundry/pilots/n629/archive.py verify \
  /tmp/n629-fresh-results.zip /tmp/n629-fresh-results.manifest.json
python3 evaluation/research_eval.py validate
python3 -m unittest discover -s evaluation -p 'test_*.py'
python3 frontier/build_access.py check
```

Use fresh directory names if these paths already exist. No packages need to be
installed. The recorded execution used a fresh Python 3.14.3 venv; exact paths,
Python build, platform, commands, seeds, source hashes, and implementation hashes
are in `results/run-20261010-v4/environment.json` and per-process receipts.
The environment record is an archive member at
`foundry/pilots/n629/results/run-20261010-v4/environment.json`; per-process
receipts are stored beside it. The runner refuses existing output directories
and checks that input bytes match the pinned Git revision, even when run from
the later PR commit.

The committed run files are consolidated in
`results/raw-execution-evidence.zip`. Its adjacent SHA-256 manifest verifies the
archive and every original file. ZIP member names retain their full repository
paths, so extraction at the repository root restores the original layout. The
archive writer sorts paths and normalizes ZIP timestamps and modes; packing the
same bytes with the same Python/zlib runtime produces the same archive. The
manifest verifier checks byte counts, paths, modes, and every member hash.
To list or extract members with the Python standard library, use
`python3 -m zipfile -l` or `python3 -m zipfile -e`.

Original documented commands are `python fpt_sampler.py`, `python verify_gate.py`,
and `python exact_m5.py`, from their source directory. The runner copies the
unchanged `.py` files into a temporary directory and runs the exact programs with
the venv interpreter and `-B`. Archived JSON is never overwritten. It preserves
stdout, stderr, generated JSON, exit codes and resource measurements, then compares
the entire generated JSON with the archived JSON except the `seconds` field.

The independent finite suite can also run alone:

```sh
/tmp/n629-venv/bin/python -B foundry/pilots/n629/check.py /tmp/n629-checks.json
```

`reference.py` uses explicit image tuples, their four-element binary span, and
enumeration of all `4^m` pairs. It does not import or reproduce signed counting,
Gaussian elimination, cover reduction or unranking. `check.py` imports the
unchanged proposed sampler only as the implementation under test.

## Evidence and limits

- `CONTRACT.md`: exact supplied-input, randomness, cost and exclusion contract.
- `AUDIT.md`: outcomes, proof reconstruction, limitations and next experiment.
- `proof_gates.json`: local development gates using the existing proof-gate
  template shape. The repository gate `G-CS-N629` stays open.
- `claim_audit.json`: scoped findings and original-byte evidence pointers.
- `results/pilot_summary.json`: compact final-run machine summary.
- `results/raw-execution-evidence.zip` and
  `results/raw-execution-evidence.manifest.json`: every original v3/v4 result,
  raw stdout/stderr, process receipt, generated JSON and artifact manifest, plus
  both historical harness failures and their diagnoses. The member names retain
  the original repository paths, including `results/run-20261010-v4/`.
- `results/run-20261010-v3/` is the first complete run, retained before
  correcting the algorithm timer's treatment of source module loading. The
  failed preflights are `results/run-20261010/` and `results/run-20261010-v2/`;
  these paths identify archive members, not loose files.
- `development_history.json`: preliminary execution and setup failures.

The first historical harness failure used a nonexistent long dossier filename
instead of `frontier/dossiers/N629.txt`; the corrected preflight left all source
files unchanged. The second attempted Darwin `RLIMIT_AS` setup with an unlimited
hard limit and failed before execution; the recorded diagnosis switches to CPU
and wall limits plus a sampled RSS guard. Both failures, their raw records and
their diagnoses are preserved in the archive.

One process runs at a time. Source scripts have 120 s wall / 100 s CPU limits;
the finite suite has 180 s / 160 s, and each benchmark 45 s / 40 s. All have a
256 MiB RSS guard sampled every 0.2 s. Darwin rejected `RLIMIT_AS`, so its memory
guard is sampled and can overshoot; Linux also gets a 1 GiB address-space limit.
Peak RSS is the child's `wait4` high-water measurement, including interpreter
and imports. CPU is user plus system time. Process wall time includes startup
and polling overhead; algorithm timers separately include preparation and draws.
Monitoring CPU, interactive audit work, checkout and preparation are outside
these child measurements. They are not zero-cost claims.

Brute force is admitted only through `4^m <= 2^20` candidate pairs. Rejection
stops after 1,000,000 proposals and retains any partial result. There are three
replicates, 16 draws per method, common inputs and equal requested outputs;
setup is charged to every method. The definition-first baseline uses a simple
tuple predicate, not optimized SIMD or a C implementation. Finite timings do not
establish universal asymptotics or a best possible implementation comparison.
Exploratory SciPy/HiGHS MILP files are preserved as source evidence and not run.
No paid model API or additional model agent is used.

This pilot follows `evaluation/PROTOCOL.md`'s separation of finite diagnostics,
universal proof, novelty and independent adjudication. It deliberately does not
register an unseen trial or append an independent outcome to `VERIFIED_OUTCOMES.jsonl`.
