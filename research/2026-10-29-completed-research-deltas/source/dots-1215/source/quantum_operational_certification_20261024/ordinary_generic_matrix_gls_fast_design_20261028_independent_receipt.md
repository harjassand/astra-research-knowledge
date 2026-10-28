# Independent receiving audit: generic matrix-GLS active encoder acquisition

**RECEIVED with the stated k^5 source price, O-tilde(k^2) matrix-bank count, and paid collective-receiver/common-frame contract.** 28 October 2026.

Bound sources:

- `ordinary_generic_matrix_gls_fast_design_20261028.md`, SHA-256 `a331566da59a07b7d9b679e4516368866fd38df20e44cff4f87f8496332d52ea`.
- `ordinary_generic_matrix_gls_fast_design_20261028_fixed_cap.md`, SHA-256 `23a7d41b408007eb11c5616129cb2bc5253ba3bd44e92538659d2382cda3072c`.

This is a fresh independent mathematical review of the block-design composition and its finite source ledger. The reviewer did not derive this construction before reading the manuscript. The local matrix-query and retained-frame/compiler theorems are separately received imports, not newly implemented here. The author identified and corrected the local restriction zeta<=m_i^-2 before this receipt; only the corrected source above is received. Its original manuscript and initial diagnostics remain preserved.

## 1. The local covariance and the nonzero bias really compose

For a fixed stage history and mathematical common frame U, T_i+eta I<=U_i and m_i>=r/eta imply, for every Hermitian O,

    Tr(T_i O^2)+(r/m_i)Tr(O^2)<=Tr(U_i O^2).

The received implemented MSE therefore bounds Cov(vec Y_i) by100 K(U_i)/m_i. The Jordan map is used as a positive operator on the REAL Hilbert-Schmidt space; no assertion that it is a completely positive state map is needed. Independence is between fresh whole homogeneous query banks, conditional on common U and earlier records. The local latent purification is averaged only after its whole-query estimate, with the same target T_i for every latent value.

Since m_i>=n pi_i, direct GLS covariance algebra gives

    Cov(theta_batch)<=100 V^-1/n.

The estimator is not unbiased. Put A_i=sqrt(pi_i)V^-1/2 F_i K_i^-1/2; then sum_i A_i A_i^T=I. This contraction proves the displayed weighted-bias inequality

    ||E theta_batch-theta||_V^2
      <=sum_i pi_i b_i^T K_i^-1 b_i<=zeta^2/eta.

Trace-norm mean error implies the required Hilbert-Schmidt coordinate bound. Adding the bias outer product gives the true-parameter second-moment bound101 V^-1/n. The argument neither assumes identical batch biases nor silently drops them.

The corrected choice zeta=min{eta/(10^6 D n),m_bar^-2} satisfies BOTH the bias transfer and every local import's zeta<=m_i^-2. The tightening changes logarithmic precision/coarse work only.

## 2. Block leverage and finite conditioning

The initial ten-anchor feature covariance is at least1/4000, and K(U)^-1>=I/19. Hence the source's lambda_*=2^-20 is conservative. Its feature norm and Lambda=4/eta bounds are also conservative.

For a violating trace leverage, the determinant lower bound uses only PSD eigenvalues:

    det(I+M/(D-1))>=1+Tr M/(D-1).

Together with(1-1/D)^D>=1/4 and Tr M>8D, this is a factor greater than2. Retained initial mass gives an inductive polynomial-magnitude lower eigenvalue bound throughout the predeclared update horizon. In fact lambda_*/(4[(4/eta)/lambda_*]^2) follows from the same argument, stronger than the source's fourth-power version. No post-termination conditioning assumption is being used to justify earlier inversions.

The conjugated operator F_x^T V^-1 F_x has trace at mostL in the K(U_x) metric, so it is at mostL times that metric in Loewner order. This is valid for the rank-p block query, not merely for one direction. Scanning the polynomial encoder grid computes the leverage without any full-decoder quadratic maximization.

## 3. Coordinate medians imply all-projector confidence without a projector net

LDL whitening is correctly oriented: phi=L_0^T theta, and L_0^T V^-1 L_0=diag(d_j^-1). The complete MSE bound101/(n d_j), threshold64/sqrt(n d_j), and independent-batch medians give the stated simultaneous coefficient V-norm event. The per-batch failure bound101/4096 is less than1/16. Coordinates need not be independent within a batch.

For P=vv*, ||v||=1,

    <P,K(U)P>=Tr(U P^2)=v*Uv.

Thus the single coefficient event and block leverage imply(16) for EVERY projector and every grid encoder. No exponential union bound or universal average-to-supremum Bures assertion is hidden here. Entrywise Hermitian coefficient rounding costs less than eta/64 in evaluated operator norm, since sum|a_j|<5. The enlarged c=1/16 bound is safe. Nothing makes the resulting predictor a density matrix or a Choi completion.

## 4. Loewner first-failure induction and all histories

For t=v*T v, the decisive scalar coefficient is

    3/256+sqrt(32)/8 = 0.718825531... <3/4.

It implies both Loewner sides of(19) simultaneously over all v. Range checks with eta/16 eigenvalue enclosures have strict slack on every good history. On a bad accepted history, the certified positive/bounded envelope still supports the same finite design, inversion, bank and arithmetic caps. A first-failure union bound, rather than an unsupported conditional success assertion after acceptance, controls the total statistical failure probability.

Stagewise rounding and the explicit ten anchors control coefficient descriptions. The fixed algebraic Hermitian basis, rational update weights, and certified field/eigenvalue arithmetic require polynomial bit complexity. No ordinary source call is spent scanning the classical grid.

## 5. The final decoder trace penalty and original comparator

For a positive decoder matrix, summing over its eigenvectors and using scalar Cauchy gives(20) with Tr C=k EXACTLY. The resulting trace penalty is k eta, not d k eta. The proof needs positivity and trace k at this step; no decoder net or extra tomography bank is supplied.

The clipped-root bound, affine SDP objective gap tau, and two root transfers yield sqrt(q_selected)<=sqrt(q_*)+5sqrt(tau). Young's inequality with gamma/4 gives125 tau/gamma. The fixed-decoder encoder risk is a nonnegative bounded quadratic minimized at the optimal encoder, so the net charges squared chord radius h^2. Interior mixing and net error then give the exact conservative additive coefficient

    1335/65536 =0.0203704833984375 <1/16

multiplying epsilon on the good branch. The separate beta and whole-process finite-control debits fit inside the remaining budget. This establishes the stated expected one-payload completed-loss comparison with the ORIGINAL full-CPTP encoder/receiver optimum, not only a zero-loss comparator or a restricted learned family.

## 6. Every bank, coarse center and horizon is paid

The fixed-cap companion correctly dominates every realized support and batch BEFORE records are acquired. In particular:

- m_i<=m_bar and sum_i m_i<=n+S(f+1);
- l_i<=m_i+L_zeta and beta_i>=beta_bar;
- the explicit padded coarse count is at most n0_bar, with base-two logarithms conservatively replacing natural logarithms;
- each whole query uses at most n0_bar+2m_i+L_zeta ordinary calls;
- summing gives the displayed N_j_bar, N_bar and H=N_bar+1.

There is no support-probability or successful-history source refund. The d r center is paid for EACH invocation. Fine floors cost O-tilde(D r/eta_final), and coarse banks cost O-tilde(D d r); both are dominated by D^2/eta_final=O-tilde(k^5/(gamma epsilon)). The appended invocation bound Q_bar=b sum_j S_j=O-tilde(k^2) counts repeated support banks separately; dummy frame-padding calls remain in N_bar, not fictitiously reclassified as useful matrix queries.

The same actually paid causal common frame persists through adaptive banks and the payload. Its horizon, ambient-logarithmic control/memory costs and the local purification/receiver costs remain part of the import. A batch-only frame existence statement would not suffice. This construction uses ordinary inputs but a collective quantum receiver, not classical count-only data.

## 7. Independent evidence and limitations

`_independent_check.py/.json` passes:

- 15 physical erasure-loss block designs with hidden real control planes, including28 actual determinant updates;
- 1,800 rank-one projector transfer checks;
- 450 positive trace-k matrix risk comparisons (the final inequality uses precisely those properties);
- GLS covariance matrices arbitrarily close to the claimed upper envelope, weighted nonzero-bias checks, and good-update Loewner bounds.

`_fixed_cap_independent_check.py/.json` passes60 exact rational schedule/cap cases, including dyadic bank floors, the corrected bias restriction and outward integer logarithm bounds. Numerical matrix evidence supplements the analytic proof; it is not a physical execution of the imported query. Synthetic coefficient errors are explicitly used to test deterministic confidence transfer.

No k^2 source rate, newly efficient Hayashi/Keyl measurement, matrix-tail theorem, hardware performance, or advantage over the equally informed conventional learner is received. The constructive result is the generic k^5 fast-accuracy, polynomial-processing composition and its explicit O-tilde(k^2) active matrix-bank count. The sharper rank-squared source target remains open.
