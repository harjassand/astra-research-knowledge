INDEPENDENT COMPLETED CONSTRUCTION — 5 NOVEMBER 2026

Governing proof: CONTROL_FOR_CALIBRATION.md

Question: Can an arbitrary unknown quantum input/reference be exported through
the accepted pure coherent Weyl ports without learning its unknown bounded
Hamiltonian, if actual calibrated single-site source control is added?

Answer: Yes within the explicit Markov/control/receiver model. A covariant
full-output randomized frame construction approximates the noise-only dilation;
its known reset/export instrument then recovers the input for every r>0.

Main bound, unhalved diamond convention:
  error <= 2 n exp(-r T) + 2 Lambda^2 T^2/B
           + 2 (Lambda+n r) (total discarded pulse/guard time)
           + all calibrated controller/receiver/memory/port errors.

Fresh random keys are used for coherent output correction and then excluded
from the returned target. A per-key or key-plus-payload quadratic guarantee is
not claimed. The proof includes the explicit counterexample.

The finite smooth source pulse prescription has growing strength and slew.
It purchases source control instead of Hamiltonian-learning exposures. The
accepted finite field receiver, its large array, propagation, precision,
protected storage, and calibration costs remain. There is no device, hard
aggregate passband, microscopic Markov completion, or practical advantage claim.

Established random DD and its 2026 quadratic improvements are explicitly
credited. Same-access best achievable resource scaling and historical priority
for the combined consequence are not established. The useful independent
contribution is the retained-output covariance/averaging/export interface and
its finite-pulse resource trade, not a new general DD mechanism.

audit_covariant_export.py and audit_results.json:
  Completed 12 finite pure-collision-dilation parameter points on 1 and 2 source
  qubits, retaining the source plus environment in normalized Choi comparisons.
  Also checked the exact kept-key/discarded-key identity and evaluated the
  sufficient schedule for n=1,4,16,64. These are mathematical diagnostics;
  no continuous field, full receiver, calibration, or hardware is simulated.

source_provenance.json:
  Exact fixed-revision source URLs, SHA256 hashes, and matching Git blob hashes
  for three governing P1 construction files retained in sources/. Previous
  research originals were read without modification.

All files in this directory are final at the scope above. Root may package them
as an independent companion; they are not recommended to displace a stronger
acquired intervention-decision endpoint solely because this theorem is closed.
