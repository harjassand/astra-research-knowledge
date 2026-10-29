# Finite random encoder seed and repeated physical encoding cost

2026-10-29. Root additive finite-interface clarification, receiving review requested.

Let G=2^(n²+2n) product_(j=1)^n(4^j-1) be the n-qubit Clifford group size modulo global phase. Using the established integer-to-Clifford bijection, an exact uniform integer in[0,G-1] gives an exact uniform Clifford. Draw b=ceil(log2G) fair bits per attempt and reject integers>=G. Acceptance probability is greater than1/2, and conditional on success the selected integer is exactly uniform. Exact uncapped sampling has finite expected bit cost but no deterministic bit cap.

For a fully bounded implementation use at mostR attempts, then choose a specified fixed encoder on all-rejection. Failure probability is at most2^-R. The resulting encoder distribution differs from exact uniform by total variation at mosteta_seed=2^-R. Composition with every seed-dependent physical learner is CPTP, so addeta_seed to the reduced half-diamond/fidelity error budget. The ideal exact-design formula in the governing draft remains unchanged; the capped physical theorem includes this extra term. ChoosingR=ceil(log2(1/eta_seed)) uses at mostbR fair bits.

Koenig--Smolin arXiv1406.2170 gives finite polynomial integer-to-symplectic/Clifford generation (O(n³) classical scale) and references ordinary O(n²)-gate Clifford synthesis; these are established algorithms. This research packet has not executed the full native uniform sampler or the large learner.

There are N_train+1 PHYSICAL executions of the known encoder gate list for one payload batch: once on every logical Choi training half and once on the actual payload. Reusing the classical description does not remove those gate costs. Each service payload also pays its logical Pauli and inverse (O(logk) gates,2logk private bits), with key retirement. Known Bell/zero-ancilla preparations, storage and routing remain paid. The source-query count is N_train+1, but total implementation error gamma must include all repeated encoder/control/padding errors as well as the decoder/compression errors. No noisy encoder can be silently treated as ideal merely because its description is known.
