FINITE INFORMATION FOR INTERVENTION RESPONSE AND GLOBAL DESIGN
7 November 2026

Start with RESEARCH_REPORT.txt. It states the input/output, acquisition,
moment, actuation and complete resource contracts, with full proofs.

Pure Python 3 reproduction (standard library only):
  python run_acquisition.py
  python verify_records.py

intervention.py provides:
  compile_predictor / evaluate_predictor / read_predictor
  ellipsoid_design (polynomial-record, rational global design)
  certified_design (separate bounded-precision conditional-gradient method)
  represented_name_reader (paid continuum coefficient-name acquisition)
  finite_quadratic_reader (explicit rational matrix acquisition)

PREDICTOR.json is a reusable rational tensor polynomial plus acquisition
records and its uniform certificate. read_predictor loads its coefficients
without any new source call. The design JSON files contain the exact finite
records, feasible settings, arithmetic parameters and stopping certificates.
EXECUTION_SUMMARY.json reports costs for the executed numerical example;
AUDIT.json reports independent exact-source checks of its saved records.

predecessor_exact_response.py is an unchanged copy of the accepted continuum
certificate solver. PREDECESSORS.json identifies all six preserved archives.
SHA256_MANIFEST.json identifies the files in this packet.

These are deterministic numerical constructions, not physical measurements.
The results do not establish a uniform efficient solver for arbitrary
measurable coefficients, arbitrary system prediction, or a QUBO resolution.
