# Postincident recovery receipt — new artifact, not the old audit manifest

## Result

The final theorem acceptance was reconstructed from warm tool-visible text and **matches its known preincident SHA-256 exactly**:

`SOURCE_BOUND_ACCEPTANCE.md`: `adae18f170a955bcd658d94e618425cd22dab7aaa114093036016b1f7f172837`.

Its verdict remains theorem-only PASS for the four exact author sources. It does not accept the numerical receiver, physical preparation, hardware or nonzero processing.

## What happened and what is newly verified

Around 01:14 UTC, workspace transport disconnected/recovered and the new audit directory vanished. This was a workspace-loss incident, not an access denial. No permission escalation or access bypass was attempted. The root recovered earlier dependencies; the author restored the four new theorem sources. Their hashes and all thirteen main/narrow proof-dependency hashes were freshly verified in this recovery directory.

The two independent scripts were reconstructed from the preserved tool-call text and **freshly rerun after recovery**:

- `check_independent.py`: PASS, **716** exact assertions.
- `check_narrow_joins.py`: PASS, **342** exact assertions.
- Total fresh checks: **1,058**, separately from the identical preincident count.

Their original individual script hashes were not printed before the incident, so byte identity of those scripts is not asserted from an unavailable reference hash. Their current exact bytes, fresh outputs and input bindings are preserved and hashed in the new recovery manifest. No candidate code was imported.

The author sources freshly checked are:

- Main: `4a8110be17507c8f0552a6ff5553e7b8f5caecfc94808900a4a05fda31cc1892`.
- Finite-rate/sharp baseline: `a71d9b0aa28300d6f23783dc9a045ec87a62ecc32eea66820b59ad1c9a30ed86`.
- No-gap note: `b9b22c3710cf03bb76582113936c734d8feb00bb58196c2dd3094dbaa567d7ac`.
- Concrete domain/local time: `9463769ee6e31d51d06c41b6b083cd5541834ef24881c6328b4c3c3519a00d2c`.

## Historical evidence versus current recovery

The exact restored acceptance is the historical preincident receipt. Its statement that 18 author files plus 31 dependencies matched records the **preincident completed verification**. At the time this recovery receipt was written, the full author `FROZEN_SHA256.json` and all 49 artifacts were not yet restored in their original paths, so this receipt does not claim a fresh whole-freeze check.

The original audit manifest had known SHA `550c48dc20ebacc522afff9674251982f28799030b7e3435f6379bed56f1bbef`; its original bytes have **not** been reconstructed here. The author freeze's known SHA was `847d4f65a454e209f4857615f8b3f79cff1354cfa794d0bd057cd1fb5afde8c1`. Neither digest is attached to fabricated new bytes. The new file is explicitly `RECOVERY_AUDIT_SHA256.json`, with its own hash and provenance.

The exact historical acceptance's references to the vanished detailed audit files are retained verbatim so that its original digest is preserved. `RECOVERED_CONTINUUM_REVIEW.md` is a newly rendered mathematical recovery of the concrete proof and narrow joins, not a claim to reproduce either vanished review's unknown individual digest. It explicitly supplies current/readable reasoning for the actual committor, boundary finite variation, global inverse forms, count identity and retained-state coupling.

## Remaining recovery boundary

Action: recover/reverify the old full author freeze and original audit-manifest bytes if available. Target: the vanished historical manifests and non-theorem runtime artifacts. Reason: their whole original byte content is not in this recovery directory. Status: pending with author/root, not denied. This does not block the exact final theorem acceptance or the fresh 1,058 independent checks; it does block claiming a new full executable/freeze audit from this recovery alone.
