# GF refresh capital integration tools

These scripts adapt the overlay builder, neutral metadata sidecar generator, and explicit overlay applier from the read-only checkout at `f937563cbc5d2249b8e0dd96bcbd3b8f78eb85c6` (`updates/GE-endpoint-exterior-genesis-20261016/package/derived/root/overlay_tools`). This package contains tooling only. Root-authored configuration, claim cards, gates, notices, and bridges must be supplied later; these scripts do not make scientific claims.

The intake namespace is `GF-refresh-capital-genesis-20261016`. It accepts one to six card IDs using routes N908 through N913. At the pinned checkout above, the route check found those IDs unused in the claim, status, catalog, graph, alias, gate, notice, bridge, and web indexes, and in their card, review-card, connection, and dossier paths. The builder and applier repeat that check against the checkout they receive, so a later collision fails closed.

Every configured source needs both its intended repository path under `updates/GF-refresh-capital-genesis-20261016/` and an explicit `source_file`. The source file must resolve inside this research package (`R`); its bytes are read and hash-checked, then staged byte-for-byte when new. An existing target is accepted only if its bytes already match. The scripts do not rewrite or execute source files. Claims must keep `claim_status` at `source_derived_unreviewed`, with all configured external validation fields set to `UNKNOWN`. New gates require nonempty `title`, `question`, and `pass_condition`; new notices require a nonempty `clarification`. Optional `checkpoint_metadata.failed_attempts` entries need an attempt, exact failure scope, and hash-checked refs; these become evidence-reference IDs. Optional `cross_branch_updates` entries may contain only a checkpoint path and must resolve to an existing checkpoint JSON whose path matches its branch and checkpoint IDs.

The builder and sidecar generator write only to a new stage outside the pinned checkout. Their receipts describe source-byte, schema, and reference integrity; they do not certify scientific truth, priority, formal proof, or physical capability. Registry additions preserve existing JSON object key order and append to existing arrays, leaving their prior elements as prefixes. The existing protected-baseline check remains enabled and does not close any global checkpoint blocker.

The applier can write a reviewed stage into its explicitly supplied checkout. It is an application boundary for root review: review all staged files and the plan, then have the root task decide whether application is authorized. This support task does not run the applier, alter the pinned checkout, commit, or publish anything.

## Read-only route guard

```sh
python3 -B workers/gf_integration_tools/build_overlay.py \
  --repo /Users/harjas/Documents/ChatGPT/ultra/work/astra-positive-memory-20261016 \
  --check-routes-only
```

For a later root-authored configuration, the intended sequence is:

```sh
python3 -B workers/gf_integration_tools/build_overlay.py \
  --repo /path/to/pinned/astra-checkout \
  --research-root /path/to/this/research-package \
  --config /path/to/root-authored/gf-claim-config.json \
  --output /path/to/new/external-review-stage

python3 -B workers/gf_integration_tools/metadata_sidecars.py \
  --repo /path/to/pinned/astra-checkout \
  --research-root /path/to/this/research-package \
  --config /path/to/root-authored/gf-claim-config.json \
  --stage /path/to/external-review-stage
```

The applier accepts only a stage plan tied to the pinned checkout and exact stage hashes. Use it only after the root task has completed scientific review and made the application decision:

```sh
python3 -B workers/gf_integration_tools/apply_overlay.py \
  --repo /path/to/approved/astra-checkout \
  --stage /path/to/reviewed-stage \
  --receipt /path/outside/astra-checkout/gf-apply-receipt.json
```
