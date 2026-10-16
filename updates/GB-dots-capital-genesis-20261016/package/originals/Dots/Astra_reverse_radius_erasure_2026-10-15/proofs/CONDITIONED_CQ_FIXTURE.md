# Well-conditioned exact quantum-output/reference decision reversal

## Certified result

For the three rational-complex qubit outputs sigma_j=(I+(3/5)P_j)/2, P_j=X,Y,Z, erasure reveal probability q=1/5 exceeds the exact ordinary SLD/MMSE threshold 9/50. Nonetheless the finite three-level-reference binary experiment below has an exact quantum-output MMSE advantage

728016375068464825987973551550411077632
/92681868499575890293064731399721815408585
approximately 0.007855003215346228, strictly above 3/400=0.0075.

This is a larger certified numerical gap in a different proposed experiment. Different channels and reference resources prevent a matched performance comparison with the previously mentioned 0.005 example. It is an exact decision-theoretic separation, not a claim that a laboratory can prepare the states or resolve the gap. Here conditioning means explicit positive eigenvalue margins; no perturbation/noise-robustness radius has been certified.

## Rational data and physical states

Let

Q=[[88,32,-121],[88,-121,32]]/153,
s=(89,88,88)/153,
v_i=Q e_i,
z_i=s_i v_i.

Exact identities Q Q^T=I_2 and Qs=0 hold. The prior s_i^2 is a rational near-uniform prior. Put

epsilon=1/100,
delta=1/5,
t=2/5,
q=1/5,
R_i=(v_i v_i^T+epsilon I_2)/(1+3epsilon),
B_i=diag(R_i,delta/3),
H_i=[[0_(2x2),z_i],[z_i^T,0]].

The two equally likely labels theta=+1,-1 produce the normalized classical-input/reference states

rho_theta=direct_sum_i (B_i+theta t H_i)/(2+delta).

They have the same reference marginal diag(I_2,delta)/(2+delta). They are faithful. Exact principal-minor tests prove every eigenvalue of either full state lies strictly between 1/250 and 1/3; hence both state condition numbers are below 250/3. This is a finite conditioning certificate, not an eigenvalue plot or floating-point tolerance.

## Exact distinguishability and loss

For the unnormalized baseline and tangent, exact Sylvester solves give

E_input=69874286085120/18961198152379,
N_target=826097397710359059245621760/977595062872621232748363023.

Their ratio is approximately 0.22930876093308997, strictly above q=0.2. The erasure SLD cost is q E_input because the erased-reference tangent vanishes. For squared-error estimation of theta in {-1,+1}, the optimal MMSEs are exactly

MMSE_target=1-t^2 N_target/(2+delta),
MMSE_erasure=1-t^2 q E_input/(2+delta).

Their difference is the positive fraction stated above. These are exact binary-experiment formulas, not a small-t approximation; t=0.4 is explicitly within the strict positivity region.

## Receiver resources

- Preparation: a three-symbol classical input jointly correlated with a three-level quantum reference, using the explicitly specified two binary-labeled block states. The classical-reference states are separable across the classical/quantum cut.
- Target receiver: the prepared qubit output together with the untouched three-level reference, total Hilbert-space dimension 6.
- Erasure receiver: a four-valued classical reveal-or-erase register together with the same three-level reference, total direct-sum dimension 12.
- The optimal squared-loss estimator is a Hermitian observable obtained from the corresponding SLD/Sylvester equation. A spectral measurement on the target's six-dimensional joint system suffices, with at most six distinct outcomes. For erasure the optimal observable is classical-block diagonal.

No tensor-product measurement restriction, hardware architecture, detector efficiency, or experimental implementation is assumed. Model-based sampling bounds are given below. The gap concerns optimized decision risk for the fully specified mathematical experiments.

## Certification boundary

Only the achieved gap and positivity of these specified parameters are certified. The preparation is not claimed globally optimal. Eigenvalue conditioning is not a measurement of noise robustness.

Run the package verification runner. checks/robust_sld_witness.py reconstructs the rational-complex Sylvester calculation, risk gap, Schur complements, and all conditioning minors, and compares checks/ROBUST_SLD_WITNESS.json. checks/check_robust_cq_flag.py independently solves the full output Sylvester system and checks the same finite gap and eigenvalue bounds. The ordinary coefficient proof is in PAULI_ORDINARY_AND_FINITE.md.

## Sufficient fixed-receiver error budget

Suppose perturbed prepared outputs remain normalized qubit density matrices and ||σ'_i−σ_i||_op≤δ. Their differences are traceless Hermitian 2×2 matrices, so their trace distances are at most δ. For any cq/reference input, the output difference has trace norm at most Σ_i ||σ'_i−σ_i||_1 Tr R_i≤2δ, hence trace distance at most δ.

The ideal optimal binary squared-error receiver may be clipped to estimates in [−1,1], so its loss lies in [0,4]. A trace-distance change η changes any such fixed receiver's expected loss by at most 4η. Keeping the ideal target receiver fixed, and the source experiment unchanged, certifies a decision advantage at least Δ−4δ.

If each binary input state is additionally perturbed by trace distance at most κ, contractivity gives at most κ after either channel. The target fixed-receiver risk and source optimal risk each change by at most 4κ (the optimal-risk bound follows uniformly over bounded receivers before taking infima). Thus an achievable target advantage over the source optimum is at least

Δ−4δ−8κ.

For δ=.001, κ=0, this lower bound is approximately .003855003215346228. These are sufficient worst-case model-error budgets. They assume the receiver implementation itself is unchanged; detector, readout, drift or reference-memory implementation errors require separate bounds. No actual calibrated hardware performance is asserted.


## Loss moments, receiver ranges, and an IID sample bound

Let O denote the calibrated optimal estimator observable and theta the equiprobable label. Write m_2=Tr(rho_bar O^2) and m_4=Tr(rho_bar O^4). The optimality equation Delta=(rho_bar O+O rho_bar)/2 gives the exact identities

E[(theta-O)^2]=1-m_2,
E[(theta-O)^4]=1+2m_2-3m_4,
Var((theta-O)^2)=4m_2-3m_4-m_2^2.

Exact rational values are stored in `../checks/LOSS_STATISTICS.json`; their decimal summaries are:

- Target: mean loss 0.9385432547439124; second loss moment 1.0974582408329743; loss variance 0.2165947998076777.
- Erasure: mean loss 0.9463982579592587; second loss moment 1.0635183196530353; loss variance 0.16784865698471585.

The target receiver eigenvalues are approximately -0.4246714613, -0.2653126237, 0, 0, 0.2653126237, 0.4246714613. The three revealed input blocks have estimator eigenvalues respectively 0 and +/-0.5266579635, 0 and +/-0.5184126100, 0 and +/-0.5184126100. The erased block's estimator is zero.

Exact principal-minor certificates bound the target estimator norm by 43/100 and the erasure estimator norm by 53/100. Consequently target losses lie in [3249/10000,20449/10000] and erasure losses in [2209/10000,23409/10000]. Every individually centered arm loss is bounded in absolute value by M=53/25=2.12. This is not a bound on a centered paired difference. The proof applies Bernstein to all 2n independent centered arm variables before dividing their signed sum by n. The sum of the two arm variances is strictly below v=77/200=0.385, and the true gap Delta is strictly above g=157/20000=0.00785.

Suppose n independent trials are collected on each arm, with independent equiprobable binary labels, correct fixed state preparations, and independently calibrated optimal receivers used without fitting on the evaluation data. Let D_hat be sample mean erasure loss minus sample mean target loss. Bernstein's inequality gives

Pr(D_hat-Delta<=-x) <= exp[-n x^2/(2(v+M x/3))],

and the two-sided bound has an additional factor 2. Therefore:

- n=37,973 trials per arm suffice for probability below 5% that the empirical ordering is reversed. Rounding to 40,000 per arm gives a simple conservative count.
- n=185,705 per arm suffice for a two-sided 95% confidence error radius g/2=0.003925. On that event the resulting confidence interval certifies a positive gap. Rounding to 190,000 per arm gives a conservative count.

These are sufficient model-based IID Bernstein bounds, not optimal sample counts. They do not include receiver training/calibration samples, state-preparation errors, detector effects, correlated drift, device mismatch, or adversarial sampling. The first count concerns the sign of an empirical ordering and is not itself a confidence-interval certification procedure. The separate fixed-receiver error budget above bounds specified model perturbations; it does not remove the IID and calibrated-receiver requirements of these sample counts.

checks/check_loss_statistics.py verifies exact moment fractions and spectral ranges. It certifies the stated sufficient integer counts using rational logarithm upper bounds proved by truncated positive exponential series. The independent checks/check_robust_cq_flag.py recomputes the moments directly from conditional loss operators, using the full receiver equations. No floating-point spectra determine any bound.
