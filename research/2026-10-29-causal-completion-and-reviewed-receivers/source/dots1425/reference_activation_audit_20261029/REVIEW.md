# Independent receiving review: faithful-channel reference activation

2026-10-29. Reviewer: review_finite_quantum_sampler. Verdict: PASS for the stronger Choi-support obstruction and the exact reference-activation theorem, together with mandatory ACTIVATION_SCOPE_CLARIFICATIONS.md. The original, different EB-channel obstruction is not needed by this receipt.

## What is proved
For the fixed channel Phi=Ad_X composed with amplitude damping 1/2, with faithful fixed state sigma=diag(1/3,2/3), there is no finite constant controlling either (i) computational/spectral dephasing relative entropy by one-step relative-sigma loss or (ii) two-step by one-step relative-sigma loss, uniformly over states with an untouched qubit reference. This is an exact asymptotic counterexample, not a numerical optimizer inference. Separately, Phi admits no positive-weight CPTP entanglement-breaking component in CP order.

## Channel and CP-order obstruction
The symmetric isometry |0> -> |00>, |1> -> (|10>+|01>)/sqrt(2), followed by X on both receivers, supplies a full-domain symmetric extension. Direct marginal action gives the stipulated Phi and its faithful fixed state.

In input-reference/output Choi ordering the support is S=span{|01>+|10>/sqrt(2),|11>}. The coefficient matrix of a generic vector is [[0,a],[a/sqrt(2),b]], with determinant -a^2/sqrt(2). Thus only the ray |11> is a product vector in S. If a positive multiple of a CPTP EB map were CP-below Phi, its positive separable Choi operator would have support in S. In any separable decomposition all product vectors must lie in S, so its input marginal has rank one, contradicting trace preservation. This is stronger than merely failing minorization by the spectral pinching. The submitted explicit witness has expectation zero against J(Phi) and 1/3 against J(Phi Delta); it was replayed with exact symbolic arithmetic. No EB-minorization route survives for THIS channel, but this does not prohibit an EB approximation in a different metric.

## Exact state and first step
For 0<e<1 take rho_e=(1/3)|01><01|+(2/3)|psi_e><psi_e|, psi_e=sqrt(e)|00>+sqrt(1-e)|11>. The two mixture components are orthogonal, hence input spectrum {1/3,2/3,0,0}. The reference marginal is preserved by each application on A. Computing the Kraus action gives one-step characteristic polynomial

 u^2 [u-(1+e)/3] [u-(2-e)/3].

The A=0 population changes by -e. Since log sigma0-log sigma1=-log2 and the reference logarithms cancel, the relative-entropy loss is

 L1=h((1+e)/3)-h(1/3)+e log2=(4/3)e log2+O(e^2).

The first-order coefficient is positive, so the ratios below are well defined for sufficiently small positive e. Computational pinching removes only the coherence inside the second orthogonal component. Its relative entropy is exactly (2/3)h(e), whose leading term is (2/3)e log(1/e). Therefore its ratio to L1 diverges with leading coefficient 1/(2log2) multiplying log(1/e).

## Exact second step
The submitted two-step matrix was obtained independently from Kraus multiplication. Its 00/11 block has trace 2/3-e/6 and determinant e/9-e^2/18. The small eigenvalue has slope 1/6 at zero, while the independent eigenvalue in the 10 sector is e/3. The other eigenvalues tend to 2/3 and 1/3 and contribute analytic O(e) changes to entropy. Therefore the new small eigenvalues contribute (e/6+e/3)log(1/e)=(e/2)log(1/e). The A=0 population changes by -e/2, so the relative-sigma term is only (e/2)log2. Thus

 L2=(e/2)log(1/e)+O(e),
 L2/L1 ~ [3/(8log2)]log(1/e).

No finite complete one-step-to-two-step constant exists for this fixed channel. The matrix trace, reference marginal, characteristic polynomial, population changes, determinant and eigenvalue slope were all checked independently using symbolic arithmetic.

## Mandatory limitations
1. The untouched reference carries the identity channel, which is NOT self-compatible. The example does not automatically refute a theorem where every subsystem undergoes a self-compatible noisy channel. Applying noise to R changes the problem and may change leading asymptotics.
2. This is a fixed spectral-dephasing entropy comparator, not a proof that every prior-adapted EB map fails. No unrestricted actual-prior N371 counterexample is established.
3. It does not refute direct square-root trace control. Here T(rho_e,Delta rho_e)=(2/3)sqrt(e(1-e)), and its ratio to sqrt(L1) tends to 1/sqrt(3log2), a finite constant. The positive rescue is therefore compatible with this failure theorem.
4. The unrotated Petz map at sigma equals Phi. Phi has negative KMS eigenvalues, while its square is positive in the associated KMS geometry. The example blocks a constant Umegaki-loss transfer from the square to one step; it does not refute a theorem restricted to positive Petz squares. General universal recovery is rotated/averaged Petz and cannot silently be replaced by the unrotated square.
5. Historical novelty, broad no-cloning consequences, computational advantage, and experimental significance have not been established.

## Independent executed evidence
Verified STRONGER_SHA256SUMS.txt, REFERENCE_ACTIVATION_SHA256SUMS.txt and ACTIVATION_SCOPE_SHA256SUMS.txt. Replayed the author's exact stronger Choi calculation and 70-digit activation table in the audit directory, leaving originals unchanged.

Independent script computes the full symbolic input/one-step characteristic polynomials, reference preservation, population shifts and second-step eigenvalue slope. It also uses a separate dense 90-digit eigensolver at e=10^-4,10^-12,10^-30 rather than reusing the author's block-spectrum evaluation. The entropy ratios grow and their log-normalized coefficients converge toward the analytical values. The trace/square-root-loss ratio approaches 0.6934683460, agreeing with 1/sqrt(3log2). Floating/high-precision evidence is diagnostic; the exact asymptotic proof governs.

Two implementation-only issues in the independent test harness were repaired before receipt: SymPy's block-factor sorting could not compare a symbolic relational, so the characteristic determinant was computed directly; algebraically identical factorizations were compared after simplification rather than by structural equality. Neither was a defect in the submitted mathematics.
