CONTROLLED TRANSPORT BOUNDARY AND FINITE-SLEW DIAGNOSTIC
Date: 2026-11-05

Governing construction: CONTROLLED_TRANSPORT.md
Status: Complete at its declared mathematical and calibrated-interface scopes.

The all-causal conjugate-force/current record bound is
  KL <= a(1+T) + a^2 E T^2,
for reference transport 1 and alternative transport any M>=2. It implies
uniform upper-confidence and locally finite adaptive-stopping obstructions
over the class permitting a unit reference and weak second modes. The
separate exact-minimal-order-two consequence is a fixed-budget obstruction;
the stronger stopping claim is not asserted for that restricted class.

A finite-slew trapezoid attains the matching U^2 a^2 T^3 visibility scale
for a specified candidate pair. Its endpoint diagnostic includes finite
meter, ADC, timing, force-error and mechanical-work-reserve accounting.
The candidate models, stationary source, and calibrated interfaces are
supplied. No hardware factory, natural-system closure or uniform transport
predictor is claimed. Native initialization can require the slow time.

Executed example:
  a=1e-4, M=1000, lambda=a/999, peak=10, ramp=1, pulse=800.
  Inclusive wall time=800.0204; actual effort <=79868.264675.
  Error including mechanical-reserve abort <0.004183.
  Same-time passive maximum testing error >=0.449934.
  Slow relaxation time is approximately 9.99 million time units.
  22 bits per endpoint; timer has 28 counter bits and 160 million ticks.
  Its phase accuracy is separately calibrated, not supplied by bit count.

Run from the package root:
  python3 next5_physical/audit_controlled_transport.py
  python3 next5_physical/certify_endpoint.py

audit_results.json contains symbolic/numerical checks and synthetic scalar
draws. Separate endpoint ADCs and physical SDE paths were not simulated.
endpoint_certificate.json contains directed-rounding enclosures of the
decision, reserve, passive comparison and hidden-alternative bounds.
execution_environment.json records runtime versions. source_provenance.json
records the unchanged original sources. manifest.sha256 lists new artifacts.

The governing original-source links target the final archive layout beside
preserved_first_event/. Their source files were hash-matched to the original
first_event_research_package copies. Originals remain unchanged.

00_CHECKPOINT.txt preserves the early attempt; the complete governing file
and certificate supersede its preliminary status and approximate accounting.

No external publication was made. Historical firstness is not established.
