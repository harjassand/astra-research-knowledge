# Separate binary estimation certificate

This is an independently reconstructed internal exact certificate for one idealized estimation protocol. It is separate from the Petz/RLD theorem; no sharp general SLD formula, experimental advantage, or practical advantage is asserted.

## Earlier ideal model comparison

The first certificate below supplies an ideal-model comparison. The recommended compact noise-aware certificate follows afterward.

### States and channels

Draw U uniformly from {+1,-1}. For U=+1 use the three integer vectors (135,694), (0,0), (631,-437); for U=-1 use (0,0), (684,176), (473,-603). For each sign form B_i=v_i v_i^T and Z=sum_i Tr B_i, then define the qubit blocks

rho_(U,i) = (1-6f) B_i/Z + f I_2, with f=1/100000.

The full state is direct_sum_i rho_(U,i). It is faithful, normalized, classical-quantum, and separable. The classical symbol passes through EN or FN, the strictly positive rational channels in CHECKS.md; the qubit is retained as an untouched reference. Preparing conditional qubit states and sampling the classical block implement this encoding without entanglement.

## Optimal receiver and exact comparison

For each observed output j, let P_j and Q_j be the unnormalized qubit output blocks for U=+1 and U=-1, respectively. Set A_j=(P_j+Q_j)/2 and K_j=(P_j-Q_j)/2. Solve the Hermitian equation

A_j O_j + O_j A_j = 2 K_j.

Measure O_j spectrally and use its eigenvalue as the estimate of U. The fixture supplies each exact rational observable and its Bloch-axis coordinates. For any Hermitian estimator O the block risk is Tr A + Tr(A O²)-2 Tr(K O). Completion of squares about the solution O_j gives the minimum Tr A-Tr(K O_j). General POVM estimators cannot improve this: their second-moment operator is at least the square of their first-moment operator, while the spectral measurement attains equality. This establishes the optimal quadratic-loss receiver for the specified states and classical output.

The independently recomputed optimal mean squared errors are

- Source EN: 0.8047695060269698
- Target FN: 0.7989547824464164
- Target advantage: 0.005814723580553494

Exact rational risks, variances, observables, and states are in checks/optimized_binary_mmse_certificate.json. checks/check_optimized_mmse.py reconstructs the states from integers, solves the receiver equation using a separate vectorized method, compares each observable and rational cost, and directly recomputes first and second moments of the squared loss.

## Ideal sampling bound

All estimator eigenvalues lie strictly between -1 and 1; squared loss therefore lies in [0,4]. Let Delta be the exact positive risk gap and V the sum of the two single-shot loss variances. For independent IID trials on the two fixed device/receiver protocols, a conservative Bernstein bound on reversed empirical ordering is

Pr(wrong ordering) <= exp[-n Delta²/(2V+(16/3)Delta)].

The checker verifies that n=144811 trials per device makes the exponent at least 3, so the error bound is exp(-3)<0.05. This is a sufficient ideal-model count, not an optimal sample complexity or a demonstration of feasibility. It assumes known states, correct calibrated receivers, independent label draws, and independent IID runs; it excludes receiver learning, calibration, preparation errors, and drift. The exact reconstruction also checks V approximately 0.8005234308947743.

## Recommended compact noise aware certificate

Use the same two channels and equiprobable labels, with smaller integer preparation vectors. For U=+1 use (20,12), (0,0), (4,-25); for U=-1 use (0,0), (20,-12), (-4,-25). Each sign has total squared norm 1185. Form the blocks with f=1/1000 using the normalization formula above, then apply the same known reference-noise map to every subnormalized qubit block:

b -> (99/100)b + (1/100) Tr(b) I_2/2.

This is exactly 1% qubit reference depolarization. Each full state remains normalized, separable, and bounded below by I_6/1000. The noise acts identically for both labels and both channels. The optimal receiver is recomputed for these known noisy states; the certificate does not claim the noiseless receiver retains the same performance.

The independently reconstructed results are:

- Source optimal MSE: 0.8133024604921525
- Target optimal MSE: 0.8083444005242252
- Target advantage: 0.004958059967927283
- Sum of single-shot loss variances: 0.7725661896321884
- Sufficient Bernstein trials per device: 191794

The same exact Bernstein calculation gives an exponent at least three and hence a wrong-ranking probability below 5%, under the independent IID, known-state, fixed-calibrated-receiver assumptions stated above. The count is sufficient, not minimal. The receiver is optimal for this fixed encoding; no global optimality of the preparation is claimed.

checks/robust_binary_mmse_certificate.json supplies exact rational states, observable matrices, costs, and variances. checks/check_robust_mmse.py independently rebuilds the states and noise map, solves the receiver equations by the Kronecker method, compares exact observables and costs, and verifies the loss moments and sample bound against checks/robust_mmse_check.json.

This establishes an advantage in a specified noisy mathematical model. It does not establish general hardware robustness, an experiment, practical advantage, or an error budget for calibration and implementation. Those remain the decisive operational next steps.
