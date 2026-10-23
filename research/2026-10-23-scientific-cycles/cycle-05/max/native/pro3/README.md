# Astra PRO3 Cycle4 receiving instructions

Start with `CONTINUATION_SEED.md`, then `REPORT.md`. The main scientific result
is `BRANCHING_SHARPNESS.md`; the next-boundary result is
`CRITICAL_WINDOW_LOWER.md`. Read `INCOMING_ACCEPTANCE.md` for the single owner
acceptance of the received proofs and `STATUS.md` for the separate review and
claim statuses. Max owns integration; this archive does not assert integration.

## What is new

An admitted symmetric branching tree matches the received killed-operator
upper, proving exact coefficient `max(K,1/(d c_*))` for every fixed positive
K,d and alpha in (0,1). It also proves the logarithmic risk exponent
`min(1,lambda c_*)`. A further critical-window lower retains its leading
amplitude for r0<1. Exact critical amplitude and its limit remain open.

## Complete source chain

`sources/Astra_Cycle4_Operator_Capital_20261022.zip` is the unchanged complete
incoming capsule. It contains the original 831,074-byte Cycle3 owner ZIP under
`owner_original/`, including its older nested source archives. Both incoming
proofs and native reviews are also extracted under `sources/incoming_operator/`.
The principal source prerequisites are extracted under `sources/owner_cycle3/`.
No original archive was mutated. The capsule preserves the old search records,
failed queries and costs without replaying the campaign.

New independent contributions and receipts are in `contributors/` and
`reviews/`. Exact numerical inputs, partial failed output, successful results
and resources are in `evidence/`. The explicit oracle/cost contract is
`EXPERIMENT_CONTRACT.md`; numerical scope and ordinary comparisons are in
`NUMERICS.md`. `FAILED_APPROACHES.md` preserves the corrections that mattered.

## Portable replay

Use Python 3.11 or later; no third-party packages, network, GPU or installation
is required. Extract this ZIP into any new directory and, from its top folder,
run:

```bash
python replay.py --output-dir /tmp/astra_pro3_cycle4_replay
```

The replay first verifies every manifest payload hash. It then runs the new
principal 80-reserved-digit calculation, compares its science output and exact
inputs byte-for-byte with the frozen files, and independently replays the
small native tree check. Timing fields in the latter are excluded from equality.
All outputs go to the requested directory; preserved sources are not rewritten.
It does not replay any nested historical campaign. The portable replay receipt
reports its own elapsed time and the actual output folder.

To repeat just the principal check at another precision:

```bash
python code/branching_checks.py --reserve 120 \
  --output /tmp/astra_branching_120.json \
  --resources /tmp/astra_branching_120_resources.json
```

These computations check finite identities and numerical stability. The full
proofs, rather than repeated runs, carry the universal/asymptotic results.
The diagnostic quotient is exact because of level symmetry; it does not
materialize its largest native state space or execute its enormous horizon.

## Private text transport

The separately supplied delivery identity names the original ZIP plus ordered
`zip.b64.part001.txt`, `part002.txt`, etc. Each part is below the authorized
1 MiB source-text limit. Read them through the existing private Page API,
remove only surrounding ASCII whitespace from each part, concatenate in
numeric order and apply strict base64 decoding. The result must match the
ZIP byte count and SHA256 in the identity/receipt. Verify that before extracting.
The original ZIP is unchanged by transport. No browser, user relay, public
hosting or permission change is required.

The external delivery receipt is not embedded in the ZIP whose own hash it
records. It distinguishes upload/readback integrity from Max's reading,
scientific acceptance and integration. The same Page source is available to
the evaluator through its existing authorized access.
