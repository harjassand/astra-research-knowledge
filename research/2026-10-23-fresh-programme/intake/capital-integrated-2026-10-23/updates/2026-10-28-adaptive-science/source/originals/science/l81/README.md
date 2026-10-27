# l81 scientific construction artifacts

Start with RESULT.md. Full proofs: THEOREM.md (acquisition and implemented law), OBSTRUCTION.md (iid-time first-correction barrier), STRATIFIED.md (stronger ordinary alternative and its scoped barrier), SECOND_ORDER.md (second acquired positive correction). SOURCES.md records unchanged frozen-source provenance; frozen_science/ preserves those source bytes. ACTION.md is the prospective choice recorded after source inspection.

The runtime sampler is covariance_sampler.py. It imports only NumPy. The exact mathematical program uses ideal Gaussian/real primitives; the NumPy executions are floating-point diagnostics. No original source script or active checkout is run or changed.

Reproduce from this directory, using Python 3 with NumPy (executed here with Python 3.14.3, NumPy 2.5.3):

    python3 run_checks.py
    python3 stratified_checks.py
    python3 second_checks.py
    python3 certificate_table.py
    python3 helper/check_shell.py

Every script resolves all output paths from its own file directory. run_checks.py writes checks.json and diagnostics.csv; stratified_checks.py writes stratified_checks.json and stratified_time_variance.csv; second_checks.py writes second_checks.json; certificate_table.py writes certificate_table.csv. The helper shell script writes its data only in helper/. No installation, network, paid service or external action is required.

certificate_table.csv contains evaluations of proved sufficient schedules, not measured or estimated TV. All Monte Carlo files describe moments or bounded events and do not certify TV upper bounds. Samples from the target are independent finite references and fluctuate too. Full-law statements are supported by the accompanying proofs, not by histogram/KS assertions.
