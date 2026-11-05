# Independent 19-qubit construction and literature review

Date: 2026-11-05. Scope: fully symmetric, rank-two qubit codes correcting arbitrary errors on at most two qubits. This is not a novelty assessment.

## Result

The positive 19-qubit construction is genuine. I independently retrieved Aydin–Alekseyev–Barg, refined the printed root, certified an exact root using rational arithmetic, and checked the reduced Knill–Laflamme equations. I then examined and replayed the existing `pi_code_bound_20261105/audit_positive19` certificate. No substantive mathematical gap was found in its root existence, full reduced-error check, or exact distance-five witness.

## Primary source and construction

Arda Aydin, Max A. Alekseyev, Alexander Barg, “A family of permutationally invariant quantum codes,” Quantum 8, 1321 (2024), Section 7, Proposition 7.1 and Equation (31).

- https://doi.org/10.22331/q-2024-04-30-1321
- https://arxiv.org/abs/2310.05358
- https://quantum-journal.org/papers/q-2024-04-30-1321/pdf/

Set q0=1, and take the real common zero of the nine quadratic equations specified by Proposition 7.1 for n=19,t=2, near the printed decimal vector. Define S=sum_i binomial(19,2i) q_(2i)^2, alpha_(2i)=q_(2i)*sqrt(binomial(19,2i)/S), alpha_odd=0, beta_w=alpha_(19-w). The logical codewords sum_w alpha_w |D_w^19> and sum_w beta_w |D_w^19> are orthonormal and individually invariant under every qubit permutation. This is pointwise fully symmetric support, not merely an invariant projector.

The nine printed values begin 0.0477572, -0.0267249, -0.00506367, 0.00332914, 0.00527235, -0.000947223, 0.0152707, 0.00888631, 0.32678. Their exact meaning is an isolated algebraic root, not the finite decimal vector. The article describes msolve interval output enclosing an exact solution and a Mathematica cross-check.

## Independent exact reconstruction

`verify19.py` generated the nine equations directly from the proposition, independently of the existing certificate. It used high precision only to choose a rational center c. With B=J(c)^(-1) computed exactly over the rationals and r=10^-50, exact rational calculations establish

- ||B F(c)||_infinity < 10^-65;
- ||B||_infinity < 2;
- max_l sum_(j,k) |d_j d_k F_l| = 45758;
- kappa = r ||B||_infinity 45758 < 10^-40;
- ||B F(c)||_infinity + kappa*r < r.

Thus x -> x-BF(x) is a contraction from the closed box into itself and its fixed point is an exact real common zero. This is independent of the msolve claim. Numerical checking of all four-qubit reduced logical transitions at a 100-digit root gave maximum residual approximately 3.6e-102, but that numerical check is supplementary, not the existence proof.

Files: `verify19.py`, `verify19_output.txt`, `certificate_data.json`.

## Audit of the existing standard-library certificate

`python pi_code_bound_20261105/audit_positive19/replay_certificate.py` passes. Additional checks established:

1. The recorded KL rows cover exactly the full set {cross,difference} x {0,...,4} x {0,...,4}, each once. The verifier loops over provided rows without asserting completeness; the actual file is complete.
2. The rational preconditioner is invertible because ||I-RJ(c)||<1. Together with the contraction proof, this converts the fixed point into F=0.
3. The Hessian bound is valid for these quadratics, including doubled diagonal contributions.
4. The reduced operators are supported on Sym^4(C^2). Their omitted multiplicative factors sqrt(binomial(4,a)binomial(4,b))/S are positive. The 50 identities therefore establish zero off-diagonal logical reductions and equal diagonal reductions. Arbitrary operators on four sites follow by linearity, and any four sites follow by symmetry. Products of two weight-at-most-two errors have weight at most four, so full two-error KL follows.
5. The five-site Z witness is the odd Krawtchouk polynomial K5(w), with a nonzero overall denominator S*binomial(19,5). Its certified numerator cannot vanish on the root box, proving distance exactly five.
6. The independently certified 10^-50 box is strictly contained in the existing 10^-40 box; uniqueness proves that both certificates specify the same exact code.

Small documentation correction: AAB's codeword ansatz is Equation (31), not Equation (32) as stated in the existing README's opening citation. Equation (32) is a later derivation identity.

## Literature boundary for lower bounds

Bond–Minar–Ozols–Safavi-Naini–Visnevskyi, arXiv:2603.10981v1 (11 March 2026), Section 3.1 and Conjecture 3.1:
https://arxiv.org/html/2603.10981v1#S3.SS1

The unrestricted complex-coefficient searches first find t=2 codes at n=19; the proposed n_min(t)=3t^2+3t+1 remains explicitly conjectural. Failed local minimization does not prove exclusion. AAB's shorter-length assertion is in its real, odd-length, parity-separated PR-form discussion and is not an unrestricted theorem over all complex coefficients and even lengths.

Kubischta–Teixeira, arXiv:2604.16023v2 (26 August 2026), Proposition B2, Appendix B-D:
https://arxiv.org/html/2604.16023v2

This supplies the general intrinsic/PI distance correspondence and proves the seven-qubit distance-three extremality example. I found no stated distance-five n<=18 exclusion there. Teixeira, arXiv:2605.15372v1, gives the general explicit transform, not a stated minimal-19 theorem:
https://arxiv.org/abs/2605.15372

A safe general lower bound already stronger than Singleton is n>=11, from Rains's shadow bound t<=floor((n+1)/6), applicable to arbitrary binary quantum codes, including degenerate/nonadditive ones:
https://arxiv.org/pdf/quant-ph/9611001

Do not describe Singleton's n>=9 as the strongest known general lower bound. A search finding no explicit sharp PI theorem is not proof that no stronger consequence of established programming bounds was previously known. The exact LP computations in the parent project are separate evidence, not statements I found in these papers.
