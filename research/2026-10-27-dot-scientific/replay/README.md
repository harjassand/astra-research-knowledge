# Reproduce the current stored-moment certificate

From the repository root, using Python 3.12, NumPy 2.3.5 and SymPy 1.14:

```sh
OPENBLAS_NUM_THREADS=1 python3 research/2026-10-27-dot-scientific/replay/replay_morrey.py \
  --output /tmp/astra-morrey-replay
```

The output directory must not exist. The wrapper first checks every retained
input's size and SHA-256 against `INPUTS.json`. It reconstructs the deliberately
omitted 135,796,872-byte volume and 12,583,040-byte face fields, then executes 11
frozen scientific checkers or receiving scripts with source writes intercepted.
The three reconstructed field hashes must match the original receipt exactly.
The source tree remains unchanged; new arrays, logs and the replay report stay
under the output directory. The original helper is preserved unchanged as
`reproduce_adopted141_fields.py`.

The historical scientific path prefix is rebound to `--source-root` in memory.
Only text path bindings change; SHA-256 always reads the unmodified original
bytes. JSON comparisons ignore wall-clock `seconds` fields. Regenerated exact
polynomial arrays are compared element by element rather than saved over the
originals. `validation/morrey-replay.json` records the actual completed replay
against the selected repository source tree, not merely against the larger
transfer packet.

The checks cover the 30 positive law identities and exact root/proxy arithmetic,
current certificate ledger, stored-field reassembly, arithmetic plan, full K96
Gram and outward all-strata sums, tree-completable posterior neighborhood,
independent guarded-chart and shear algebra, fixed-hull bulk ceiling, compatible
box overlap and exact heat-kernel constants. The full K96 sum returns
`N <= U141`, the exact `global_negative_mass_upper` rational in the received
ledger. The source's `0.004714574814154892` is a rounded display; exact rational
comparison gives the safe outward bound `N < 0.004714574814154893`. The replay
records the exact source field/hash and verifies this decimal enclosure.
This is the certified negative-stress upper bound,
not a W1, affinity, PSD-membership or Morrey solution.

The adopted negative-stress certificate and the optional compatible-box credit
have separate source and replay statuses in the report. The adopted bound is
replayed exactly from its stored fields/root/ledger/Gram arithmetic and does
**not** subtract the optional overlap credit.

For the compatible-box computation, every stored scalar, scalar upper bound on
the patch, and exact rational gain must match the frozen receipt exactly. Only
`disjoint_negative_patches[*].guarded_gradient_L1_upper` may differ when its
`np.einsum` contraction is recomputed. The report records each affected patch
center, old/new exact rational bound, signed/absolute difference, and its actual
certificate margins. There is no generic discrepancy-tolerance acceptance gate.

Each new gradient bound must be strictly below the source's `1/1000` cap. That
bound already includes a derivative numerical guard `2^-20` per coordinate,
`3/2^20` in total. At patch radius `r=1/8192`, the scalar upper must equal the
exact stored scalar plus `2^-29`, the linear allowance `(1/1000)r`, and the
Taylor allowance `150r²`. It must remain strictly below `-q`, `q=1/200000`;
`alpha<q` and the exact gain formula `3 alpha (2r)^3` are also rechecked. These
actual positive margins justify the optional tiny credit. A difference in the
gradient diagnostic is never compared with the tiny gain or an unrelated scalar
tolerance. The report identifies exact patch quantities separately from the
recomputed gradient bounds, and the frozen receipt is never replaced.

Fresh independent moment acquisition is **not rerun**. Its original script,
base moments/coefficient archive, current proxy and four historical proxy inputs
are retained for explicit provenance. Running that producer against preserved
sources would intentionally conflict with its existing receipt. No optimizer,
whole historical pipeline, or independent original law acquisition is claimed.

The complete original-law tree/source and pooled-flow replays need the
explicitly omitted `global_halfspacing_geometry.npz` (SHA-256
`d211c4bd71f3dd0ad16d5371e1ea2c6c71bf1951ff6f93732613ce5f802e95cc`),
`corrective132_adjoint/inherited_fine/full_actual_indexed_DAG.npz` (SHA-256
`122de1f8616125f7d743c2d150c25f6a424e62eb324fd2bb4d071298f8c87df6`)
and other historical geometry/DAG inputs. Their presence is not inferred from a
source pointer. The compact symbolic replay conditions on frozen frontier
receipts; it does not reconstruct those omitted source policies.
`pooled_full_structure.npz` is retained as the current pooled-law fixture, but
its full original-law structure/flow generation was not rerun. The nine
historical unmatched receipt hashes remain explicitly unverified.

Check directed decimal presentations independently with Python's exact fractions:

```sh
python3 research/2026-10-27-dot-scientific/replay/verify_decimal_enclosures.py
```

This verifies eight selected bounds against their hash-bound receipt fields.
Rounded source displays are retained as provenance; the exact rational and the
reported safe outward decimal govern an inequality or interval endpoint.
