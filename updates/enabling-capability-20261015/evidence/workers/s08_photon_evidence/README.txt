Run photon_baseline.py --all with NumPy/SciPy after acquiring the checksum-pinned
Figshare archive via acquire_inputs.py. Default path /tmp/astra_premise_quantum_data.zip.
Then run localization_baseline.py with OPENBLAS_NUM_THREADS=1 for bounded CPU
execution. Reports are BASELINE_SUMMARY.json, BASELINE_ALL.json, and
LOCALIZATION_BASELINE.json; source claims and limitations are in REPORT.txt.
Current available Python: ../computation_search/.venv/bin/python.
Exact-source .m files and BSD license are in ../premise_challenge.
Only source-valid frames are used for localization. No raw data were simulated.
