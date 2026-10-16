# Independent implementation audit

## Scope and gate

Review of own simulator.cpp against MODEL_CONTRACT.md, TENSOR_READOUT_VERIFICATION.md, supplied original_theorem.md, and primary https://arxiv.org/html/1609.00510v2 section 6.3. No authors' simulator was installed or run. This audit covers the sweep/Poisson-Toom implementation, not DKLP (absent), and not any proof of the supplied theorem.

Gate PASS for the frozen bounded L16, kappa1, T5 sweep/Poisson-Toom pilot manifest. Built-in and independent external tests passed. An initial external test run was interrupted by concurrent executable replacement, not a mathematical failure; its full restart against a frozen copy passed.

## Source inspection

- Geometry is orientation-major on the four-dimensional periodic dual cubical lattice; face boundary and independently written gather formula agree structurally.
- Sweep reads all eight incident syndrome bits, vetoes incoming defects, rejects odd outgoing patterns, and returns the fixed sorted-consecutive pair faces from OLD syndrome before applying any flip. One attempt clocks the vertex, not each of seven patterns.
- Toom inspects north and east checks without an incoming veto. The originally short-circuited check expression was changed to bitwise conjunction so the two-check accounting is accurate at the algorithmic level.
- At kappa=1, total proposal rate is L^4(1+6 alpha); independent exponential increments and thinning select a rate-L^4 correction process and rate-6L^4 alpha noise process. Uniform vertex or face selection gives sweep vertex rate1 and Toom face rate1/6, with face noise rate alpha. Null attempts are retained, and proposals beyond T are excluded. This is an event-driven Poisson algorithm, subject to ordinary finite-precision/PRNG approximation, not time-discretized evolution.
- Four seed-derived streams separate clock, event type, noise location and correction location. Bounded integer selection uses rejection to avoid modulo bias. Fixed engine/seed scheme is recorded. Seed reproducibility of actual pilot endpoints remains to be checked after the pilot.
- Accumulated physical chain E is never reset. decode accepts only geometry and syndrome, with no error chain or history argument. Residual scoring occurs after recovery choice and verifies closedness.
- The local branch uses connected edge components, integer lift consistency, exact strict pairwise ambient wrapped diameter test, and deterministic coordinate-box prism contraction. If ANY component fails, all partial local corrections are discarded and H acts on the WHOLE syndrome. Individually winding components are never solved separately.
- Dense H implements all 12 tensor terms with correct vertex projection, seam-edge broadcast and reverse parity integration. Cut0 homology is applied only to closed chains.
- L16 is used for the pilot. L<=8 test cases intentionally invoke global fallback; they are algebra tests only. At L16, adjacent two-face width2 disks already fail the strict diameter test. This is an important fallback-frequency limitation, not a reason to change the cutoff.

## Independent executed tests

independent_audit.py and independent_algebra_results.json: tuple-cell boundary and binary-matrix oracle for L2,3,4. Checks d1 d2=0 and d2 d3=0 on all corresponding basis cells; all cube boundaries have zero six-bit homology; all six translated coordinate sheets give identity homology at every cut. Exact ranks d2=d3=45,240,765 respectively, equal 3L^4−3, giving H2 dimension6.

check_kernels.py and independent_kernel_results.json: 704 external executable truth-table cases. All 256 incident-edge patterns at origin and seam test sweep eligibility, fixed pairing, incoming veto and odd-pattern rejection. All 16 face-boundary patterns for every orientation at origin and seam test Toom's north/east predicate.

check_executable.py tests every basis face at L3/4 against independent literal H, isolated local face recovery under translations/seams at L16/17, multi-face disks and strict cutoff, pairs of winding loops, winding-plus-disjoint-local components, seeded arbitrary boundaries and repeat determinism. All 5,150 external decode cases PASS, including 3,072 isolated translated/seam faces; results are saved in independent_executable_results.json.

## Interpretation limits

The primary paper uses parallel plane groups and per-cycle noise; this code deliberately implements an own Poissonized schedule. Its noiseless final recovery also differs. The decoder is complete but neither minimum-weight nor maximum-likelihood. Global H can convert isolated face errors into logical faults when used alone, which is why local readout is essential. Frequent fallback may dominate any finite-T results. Equal attempted updates is not equal check reads: sweep spends8 per proposal, Toom2; equal-check-read Toom would require rate2/3 per face, a different experiment.

No threshold, lifetime fit, optimal-decoder assertion, original-paper reproduction or hardware-resource equivalence follows from this gate. Tiny pilot confidence intervals must be reported and zero observed failures must not be called zero risk.

## Frozen source and final verdict (2026-10-15 20:57 UTC)

PASS for the bounded pilot. Post-accounting-fix reviewed source SHA256: 5f6badc5b613f78ce08a8c649f61e9b5b05bfb593f2624a4706affccab983070. Executable SHA256: 7915b8f4fd4d2a5aa19df3352f0d7d679227bada888a67793e7292f32639b454. Frozen externally tested executable SHA256: 7915b8f4fd4d2a5aa19df3352f0d7d679227bada888a67793e7292f32639b454.

Independent external decode suite completed 5,150/5,150 cases. Pilot completed20/20 endpoints within4.171 CPU seconds and25,708KiB maximum RSS. Builder repeat checks match every non-timing field for alpha.01 seed2026101501 under both methods. All18 nonzero-noise endpoints used whole-syndrome global fallback. Thus the pilot has hit the readout-quality limitation: the deterministic all-or-nothing policy discards even valid local fills when just one component is too large. The outcomes cannot establish a useful comparison of intrinsic memory protection. A future separately frozen common decoder could preserve all qualifying local fills and apply H to the COMBINED unresolved syndrome, since the remaining total syndrome is still a boundary. Such a change must not rewrite this completed pilot.

Scheduler rates were checked by source inspection and pilot counts; a dedicated large-sample no-correction parity/waiting-time distribution experiment was not run. No claim of such stochastic validation is made.
