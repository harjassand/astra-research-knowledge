# Public evidence replay runner

`replay_public_evidence.py` replays a bounded set of Python checks from an
integrated package. It is a local audit aid: successful execution and matching
predicates establish only that these selected programs ran against the copied
inputs and returned the required finite checks. They do not prove a theorem,
establish novelty or priority, validate the work externally, or demonstrate a
physical or practical capability.

## Package and output contract

Pass the root of the published package, whose layout is:

```text
package/
  originals/
    expanded/
      pair/
      interchange_path_exterior/interchange_path_exterior/
  prior_convergence/       # required by the controller receiving audit
  derived/
    root/
    workers/
```

The runner reads that package and constructs a fresh disposable copy for each
check. It skips `__pycache__`, `*.pyc`, `.git`, and every path named
`acquired_excluded_from_publication`. It does not follow source symlinks. In
each copy only, it adds `derived/originals -> ../originals` for a check whose
existing relative paths expect that location, and, when needed,
`2026-10-16-convergence-genesis-v1 -> prior_convergence` for the controller
audit's legacy path. The runner leaves the supplied package untouched and
records before/after package hashes.

When preserved inputs are under `originals/expanded`, the runner also adds
`originals/pair -> expanded/pair` and
`originals/exterior -> expanded/interchange_path_exterior` inside each copy;
the archive's nested `interchange_path_exterior/` prefix is retained.

The output directory must be new and outside the package. The runner creates
it once, writes `PUBLIC_EVIDENCE_REPLAY.v0001.json`, saves each child's exact
stdout and stderr under `logs/`, and copies generated receipts under
`artifacts/`. It never overwrites an existing output directory or a package
receipt. Keep the output outside any frozen receipt tree.

Use the actual interpreter intended for the replay. `--python` defaults to the
interpreter running the runner; the runner probes that selected executable for
NumPy and SymPy, and does not install dependencies. Each child timeout is at
most 120 seconds. A timeout or missing checker, input, or dependency is
`INCOMPLETE`. A nonzero exit or failed semantic predicate is `FAIL`. Numerical
warnings are preserved and qualify a successful child as `QUALIFIED`, which
prevents an aggregate `PASS`. Generic warning lines are preserved in the
receipt and logs.

## Selected checks

Mandatory checks include the stdlib `root/direct_average.py` path6 replay with
its named dependency snapshot; the independent root composition audit; the
three sparse receipt checks for `branch6`, `source20`, and `ungapped6`; the
sampler adversary exact checks; the exterior finite checks and a small
eight-sample endpoint receiver run; and the controller exact receiving,
reusable-map, recycler, and genesis receiver checks. The mandatory reciprocal
completion check replays exact projection, reciprocal-distance, allocation,
and mixture-to-random-unitary calculations, while checking hashes of the eight
frozen sampler-adversary files and its two named source inputs.

Every check has a semantic predicate beyond exit status. The predicates
compare exact rational checker results and source hashes where available,
verify expected finite result shapes and counts, and retain expected negative
controls as negative controls. The exterior receiver's random draws use the
source program's `secrets` randomness; the receipt checks output validity, not
reproducibility of sampled endpoints.

`root/finish_direct_receipts.py` dynamically imports the unchanged original
fair-bit sampler. It is excluded from mandatory checks and runs only when
`--include-source-sampler-finish` is supplied. When selected, it runs inside a
disposable copy and its generated stable receipt is compared with the package's
existing receipt.

The deterministic fixture file `REPLAY_PUBLIC_EVIDENCE_FIXTURES.json` covers a
matching sparse receipt, a corrupted checker result, a missing mandatory
check, warning qualification, and the optional-check aggregation rule. Run it
with `--self-test`; this mode needs no package and starts no child checks.

## Example

After integration has produced the package, choose a new output directory
outside it and run:

```sh
python3 /path/to/replay_public_evidence.py \
  --package-root /path/to/package \
  --output-dir /path/to/new-replay-output \
  --python /path/to/selected/python3 \
  --receiver-samples 8
```

To include the optional source sampler composition, add
`--include-source-sampler-finish`. The process exit code is zero only for an
aggregate mandatory `PASS`; the JSON receipt remains the authoritative record
of per-check `PASS`, `QUALIFIED`, `INCOMPLETE`, and `FAIL` states.
