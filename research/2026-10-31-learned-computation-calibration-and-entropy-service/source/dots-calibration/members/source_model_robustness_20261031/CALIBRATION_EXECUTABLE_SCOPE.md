# Executable calibration scope and conservative costs

31 October 2026. The mathematical receiver and this executable are separate review targets.

`calibrate_affine_innovations.py` exposes `calibrate(F,G,beta,transitions,*,N,radius,delta,b,T,p_slots,epsilon_model)`. Matrices are lists of integer bits; integer source labels use the low bit as coordinate zero. Budgets accept integers, rational strings or `Fraction`, never binary floating point.

The executable validates the stated mechanism's algebraic prerequisites, computes the classical controllability horizon, checks each residual is in im(G), and returns PASS/ABORT using exact rational arithmetic. It uses the deliberately conservative confidence certificate

    N radius^2 >= 2(2^k+j),       2^-j <= delta,

with the smallest such integer j. Indeed 2^D exp(-N radius^2/2) <= 2^(D-floor(N radius^2/2)) <= 2^-j. This avoids floating logarithms entirely. A sparse histogram includes all absent symbols' contribution analytically.

Exactly N pairs must be supplied. The caller must commit N and budgets before observing data and must supply all actual clock events if using trajectory pairs. The code cannot establish those historical facts, detect an N-pair change-only record presented as complete, verify fresh iid innovations, establish the known mechanism from finite data, verify the supplied Hamiltonian bound b, or acquire the clock rate. It cannot prevent a user from repeatedly running the test until PASS; such selection needs a separately allocated confidence budget. The `model_promise_verified` output is always false.

A passing record can be rare and misleading. The tests deliberately retain a balanced transcript which passes under the assumed confidence protocol but has positive probability under a true innovation law (9/10,1/10), whose actual distance4/5 exceeds the test threshold1/4. This is statistically permitted, not an implementation defect. Confidence is an unconditional false-PASS bound under the declared protocol, not per-transcript truth or conditional-on-PASS certainty.

`test_affine_calibration.py` tests exact PASS/ABORT threshold arithmetic, fixed sample-count boundaries, malformed algebraic mechanisms, failed controllability, off-image transitions, invalid labels/budgets, all-tick self-loop extraction, and exhaustive recovery for all injective n-by-k matrices with1<=k<=n<=3. The tests establish these finite checks, not a quantum simulator or a proof of arbitrary-model truth.

`calibration_sample_cost_examples.json` contains exact rational sufficient sample counts for radius=eta_target/4 and delta=1/1024, with no instrument slots. Examples:

- m=1,k=1,b^2T=0.01,epsilon_model=0.1: 489,982,526 samples.
- m=4,k=4,b^2T=0.01,epsilon_model=0.1: 74,042,017,055 samples.
- m=16,k=4,b^2T=1,epsilon_model=0.01: 9,168,048,231,546,880,000 samples.

These counts result from conservative theorem constants and an ordinary nonoptimized estimation bound. They are NOT minimax lower bounds, achievable-throughput claims, or evidence that calibration is practical. Smaller task-specific perturbation constants, exact source structure, or a more targeted statistical test may materially improve them; none is supplied here. The actual advance of this receiver is a rate-independent certified parameter interface under a narrow known mechanism, not demonstrated acquisition efficiency.
