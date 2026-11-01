# Explicit recovery boundary — not a silently replaced freeze

At approximately 2026-11-01 01:14 UTC the execution server disconnected and
returned an older workspace snapshot. The current author and reviewer trees
were absent. No final whole executable receipt had been delivered. Pre-incident
author tests (2,503 checks) and an independent copied author replay had passed,
but the later independent suite's output/readback was lost; that suite is not
counted as a completed whole acceptance.

The original 8,613-byte author manifest was recovered by the whole reviewer
from its complete printed transcript, byte-exact SHA
`847d4f65a454e209f4857615f8b3f79cff1354cfa794d0bd057cd1fb5afde8c1`.
It is preserved as `FROZEN_SHA256_PRE_INCIDENT.json`, a HISTORICAL descriptor,
not a claim that every original result byte remains present.

All scientific Markdown and Python sources were reconstructed from full tool
text and checked against that manifest: the nine source/text files match
exactly. All 31 dependency files were recovered from previously delivered
archives or exact transcript backups and their original hashes verified.
`DEPENDENCIES.json` also reproduces its original hash exactly. The theorem
reviewer recovered its source-bound theorem-only acceptance byte-exact at SHA
`adae18f170a955bcd658d94e618425cd22dab7aaa114093036016b1f7f172837`.
That acceptance is not a whole executable receipt.

The two production cases and complete 2,503-check author suite were actually
rerun after recovery. Their proof outputs, task refusals and exact check reports
reproduced. `RECOVERY_COMPARISON.json` lists every old/current hash. Three files
have genuinely new bytes: `results.json`, `run_stdout.txt`, and
`small_certificate.json`, because their timing fields were unprinted and could
not honestly be recovered. No fabricated old timing was inserted. All other
15 original author payload files match the old hashes exactly, including the
test report, refusal report and small fixture/replay.

One recovery command used the wrong working directory for installing source
text. Its later producer command still ran, but its test command ran before
`check.py` had been installed and failed with file-not-found. That failure is
preserved in `recovery_check_before_source_install.txt`. The source installation
was corrected, and the full test suite was then actually rerun successfully.
This was a recovery orchestration error, not a mathematical/source repair.

The new current descriptor is `FROZEN_SHA256_RECOVERY_V2.json`. Its status is
**whole executable audit pending**. A lean checkpoint may preserve these
reviewable bytes durably before that audit finishes. No new scientific scope,
numerical width, physical implementation or acceptance is inferred from the
recovery itself. Future independent acceptance must bind this actual new
descriptor and the regenerated evidence rather than pretending the missing
old timing files survived.
