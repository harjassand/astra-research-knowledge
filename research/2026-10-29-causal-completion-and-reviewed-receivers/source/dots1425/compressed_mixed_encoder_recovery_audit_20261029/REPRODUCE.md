# Reproduction

With Python3, NumPy and SymPy:

```sh
python independent_checks.py
```

This writes `INDEPENDENT_CHECKS.json`; it does not alter source snapshots. The exact h=8 certification checks deliberately enumerate principal minors as an independent small diagnostic. The operational finite schedule may instead use its polynomial-time exact LDL/Sylvester positive-definiteness test.

Author replay, kept separate from frozen inputs:

```sh
mkdir -p author_replay
cp source_snapshot/check_physical_petz.py author_replay/
python author_replay/check_physical_petz.py
```

Compare the resulting JSON to `source_snapshot/check_physical_petz.json`. `REVIEW_RECEIPT.json` binds the governing draft, both corrections, finite rational schedule, compiler dependency, review and independent evidence by SHA256. These are mathematical and small-model numerical checks, not physical execution of the full query schedule.
