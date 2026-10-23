# Astra PRO3 Cycle3 research return

Read CONTINUATION_SEED.md first, then REPORT.md and VANISHING_SCREEN_THEOREM.md.
The new question is screening that vanishes across predetermined horizons or
errors while remaining fixed within each run. The received fixed-eta gap is
accepted and closed; both original proofs are included unchanged.

The new theorem gives the exact uniform convergence criterion, an explicit
screen-independent finite upper bound, a stronger growing-path obstruction,
and direct bounds for the accuracy-policy mixing coefficient. It leaves the
finite-constant crossover open. Pure IMH remains the coefficient-K comparator;
there is no demonstrated practical speedup.

## Complete arguments and acceptance

- VANISHING_SCREEN_THEOREM.md: principal theorem and integrated consequences.
- reviews/vanishing_lower_proof.md: full positive three-state/path constructions.
- reviews/vanishing_transport_source_binding.md: actual-source upper challenge
  and targeted check of the lower-to-accuracy conversion.
- LOWER_ACCEPTANCE.md: principal's separate acceptance of the full lower proof.
- RECEIVED_TEMPERED_ACCEPTANCE.md: owner acceptance of the two new inputs.
- EXPERIMENT_CONTRACT.md and NUMERICS.md: frozen calculations, access, comparator,
  precision and full proposal/target/caching/implementation cost boundaries.
- FAILED_APPROACHES.md, SOURCES.md, PRESERVATION.md and RESOURCE_RECEIPTS.json:
  failures, primary boundary, original-state preservation and observed resources.

The unchanged native Cycle2 archive is in sources/. The received proof/method/
review folders are in sources/received_tempered/. INPUT_RECEIPT.json identifies
every preserved copy. No complete target table is silently handed to a sampler;
the finite matrices in diagnostics are verifier ground truth.

## Verify bytes and replay actual calculations

Only Python 3.12+ standard-library modules are required. From this extracted
directory:

```bash
python3 verify_manifest.py
python3 replay.py --receipt /tmp/astra_pro3_cycle3_receiver_replay.json
```

The replay creates temporary output files and leaves all included source and
recorded results unchanged. It reruns only the new principal certificate grid
and the 16 new adverse-chain laws, checking the saved numerical outputs.
It does not rerun old source archives or turn numerical checks into a proof.

Individual commands, with outputs outside the frozen source, are:

```bash
python3 code/uniform_certificate.py --dps 80 --output /tmp/astra_cycle3_upper.json
python3 reviews/vanishing_lower_checks.py --base-precision 90 --output /tmp/astra_cycle3_lower.json --resources /tmp/astra_cycle3_lower_costs.json
```

For ZIP verification:

```bash
python3 verify_manifest.py --zip /absolute/path/Astra_Amplification_Cycle3_PRO3_20261022.zip
```

MANIFEST.json hashes all payloads except itself. The outer ZIP's exact bytes,
SHA256 and private references are in its separate delivery identity/receipt,
avoiding a circular self-hash. The same Page includes ordered UTF-8 base64
transport parts, each below 1 MiB, for receivers whose authorized source API
cannot materialize ZIPs. Concatenate their stripped text in numbered order,
decode once, check the recorded ZIP hash and size, then verify
the member manifest. Private upload and readback do not assert recipient
reading, scientific acceptance or Max integration.

## Next scientific step

Study the killed transport operator before the first safe hit, coupling
global escape with the weighted norm instead of treating them separately.
The goal is the exact finite-d crossover, with the current admitted path as
the lower comparator. No background calculation remains running at handoff.
