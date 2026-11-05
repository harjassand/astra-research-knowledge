# Minimum fully symmetric two-error qubit memory

Status: the independent directed-integer residual verifier certifies exclusion at n=18 with strict margin at least 0.00006908479009717404. Together with exact LP certificates below 18 and a certified algebraic 19-qubit code, this establishes n_min=19 under the stated model. Both independent adversarial reviews and their fresh certificate replays passed; see audit_residual/AUDIT.md and audit_second/INDEPENDENT_REVIEW.md. No claim of a new decoder, experimental memory, general quantum-code optimum, or asymptotic result is made.

## Intended capability and scope

Encode one arbitrary logical qubit in n physical qubits, with every codeword in Sym^n(C^2), and exactly correct two arbitrary single-qubit errors. Equivalently the rank-two code projector P detects all Pauli errors of weight at most four. The collective spin-j representation, j=n/2 and D=n+1, has operator sectors of tensor rank r=0,...,n. Detecting physical errors of weight <=4 implies

P E P = Tr(P E) P / 2

for every irreducible tensor operator E of rank r<5. This follows directly by expanding collective spin polynomials into local Pauli products; it also follows from Proposition B2 of Kubischta–Teixeira v2. Arbitrary complex Dicke amplitudes are allowed. No parity, real-codeword, time-reversal-invariant, stabilizer, or special support assumption is imposed.

## Exact incumbent bound

For Hilbert–Schmidt orthonormal spherical tensors T_rm, define

a_r = (D/4) sum_m |Tr(P T_rm)|^2.

The intrinsic SU(2) MacWilliams matrix is

M_kl=(2k+1)(-1)^(n+k+l) { j j k ; j j l }.

Necessary conditions are a>=0, a_0=1, sum a=D/2, G a>=0 with G=2M-I, and (G a)_r=0 for 1<=r<5. These are established prior-art LP conditions, originating in Bumgardner and developed by Okada. Okada already tabulated a distance-five bound implying n>=18. The exact files give independently replayable rational positive dual identities excluding n=9,...,17; this weaker lower bound is not claimed as new. Quantum Singleton is an elementary exclusion for n<9, not the strongest general bound: the Rains shadow bound already gives n>=11 for two-error correction. The intrinsic certificates cover all lengths through17 regardless. The n=18 LP remains feasible even with time-reversal shadow nonnegativity; exact_feasible18.json supplies an exact rational witness. This comparison is a stronger standard bound given the same physical-code definition, not a weaker selected baseline.

## Three-copy necessary conditions

For an actual code, X3 = integral U^(tensor 3) P^(tensor 3) U^dagger(tensor 3) dU. Its trace is 8. Couple the first two spin-j copies to spin l, then to total spin J. X3 has multiplicity blocks R_J, with identity on the (2J+1)-dimensional spin space.

Copy permutations commute with X3. In this coupled basis, V=S12 is diagonal V_ll=(-1)^(n-l), while

U=S23, U_ll'=(-1)^(n+l+l') sqrt((2l+1)(2l'+1)) { j j l ; j J l' }.

The alternating S3 component vanishes because wedge^3(range P)=0. The remaining symmetric and standard multiplicity spaces are parameterized by positive semidefinite matrices A_J and B_J. Symmetric/standard projectors are formed from the exact permutation matrices. Exact projected seed bases, not a floating eigenspace assumption, are used for the proposed certificate.

One may take the real part of all blocks: all retained equations and maps have real coefficients, and the real part of a Hermitian positive semidefinite matrix is a real positive semidefinite matrix. This is a relaxation of arbitrary complex codes, not a restriction on codewords.

Define w=(4/D) M diag((-1)^r) a. These are total-spin weights of X2=twirl(P tensor P). The marginal constraints are

sum_J (2J+1) (R_J)_ll = 2 w_l.

The lifted Knill–Laflamme equations follow from

Tr[(P tensor P tensor P)(F tensor G tensor E)(S23-I/2)] = 0

for every detectable E and arbitrary F,G. Projecting onto SU(2)-scalar operator tensors with local rank r on copy 3 gives the implemented weighted 6j equations. The r=0 equations include P^2=P contractions.

Partial time reversal on copy 3 is ordinary partial transpose followed by a fixed local unitary. It preserves positivity of P tensor P tensor P, and commutes with collective SU(2) averaging. In operator rank r on that copy it acts by (-1)^r. The implemented Racah transform reconstructs its total-spin blocks, all of which must be positive semidefinite.

Also, twirl[P tensor P tensor (I-P)] is positive and remains positive after partial time reversal on copy 3. Thus B12-R_J and B12-PPT3(R_J) must be positive, where B12=diag(w_l/(2l+1)). These complement constraints are necessary and do not assume I-P is a code.

## Certificate, not floating-point solver status

A numerical SDP minimizes epsilon after adding epsilon I to every PSD block. A positive reported optimum alone is insufficient. The verified rigorous certificate instead sets epsilon=0 and uses nonnegative linear multipliers and positive semidefinite matrix multipliers to form a Lagrangian L. Every true feasible code has L<=0. The same affine expression is

L=c+r_a dot a+sum_i Tr(r_i X_i).

Exact trace identities give sum a=D/2 and sum_J (2J+1) Tr(R_J)=8. If exact projected bases have Gram lower bounds g_i, then a rigorous upper bound on the residual pairing is

(D/2) ||r_a||_infinity + 8 max_i ||r_i||_operator / ((2J_i+1) g_i).

A certified positive value of c minus this bound proves exclusion. Exact dyadic Cholesky-factor products can certify PSD dual multipliers. Original coefficients omitted by numerical sparse thresholds must be restored in interval verification. The epsilon stationarity equation is irrelevant to this zero-slack contradiction.

## Sources and novelty boundaries

The final source-priority assessment is LITERATURE_PRIORITY_AUDIT.md. It supersedes preliminary statements elsewhere about novelty of the weaker n>=18 bracket. Only the unrestricted n=18 exclusion and resulting minimum19 are the proposed substantive advance.

- Bumgardner, Codes for quantum metric spaces (2011 dissertation / 2012 preprint): https://arxiv.org/abs/1205.4517
- Okada, 2023 dissertation (2025 posting), Table3.1: https://arxiv.org/pdf/2502.14165

- Kubischta and Teixeira, MacWilliams Identities for Intrinsic Quantum Codes, arXiv:2604.16023v2 (26 August 2026): https://arxiv.org/html/2604.16023v2
- Teixeira, Orthogonal Polynomials and the MacWilliams Transform for Permutation-Invariant Qudit Codes, arXiv:2605.15372: https://arxiv.org/abs/2605.15372
- Aydin, Alekseyev and Barg, A family of permutationally invariant quantum codes, Quantum 8, 1321 (2024), Section7: codeword ansatzEq31 and coefficient systemEq32. https://arxiv.org/html/2310.05358v3#S7
- Rains, Quantum shadow enumerators (general-code bound, not the decisive intrinsic bound): https://arxiv.org/abs/quant-ph/9611001
- Bond et al., Permutation-invariant codes: a numerical study and qudit constructions, arXiv:2603.10981: https://arxiv.org/abs/2603.10981
- Minimal two-error PI-code problem, literature checked through 15 September 2026: https://qiqc-op.com/problem/op_a72722e455d85d55/
- General minimum-length conjecture: https://qiqc-op.com/problem/op_2fba72464e1b4de4/
- General quantum-code SDP hierarchy is prior art: https://arxiv.org/abs/2408.10323
- Rigorous rational SDP certificates are prior art: https://arxiv.org/abs/2603.19901
- Three-point quantum CV MacWilliams bounds and collapse results are prior art: https://arxiv.org/abs/2607.14920

Searches through 5 November 2026 did not locate an explicit minimal-19 proof or this specific spin three-copy PPT evaluation. That is a bounded literature-search statement, not guaranteed novelty. A known 19-qubit code supplies the upper bound; an exact explicit positive-control reconstruction and direct lifted-constraint sanity checks have been independently completed in audit_positive19/.

## Resources and reproducibility

Python 3.12, SymPy exact Wigner6j/rational arithmetic, NumPy/SciPy, CVXPY and Clarabel. A local isolated dependency environment was installed (about 542 MB). Numeric solvers use one OpenBLAS thread. Runtime reports currently record solve/compilation duration, not full end-to-end CPU accounting, and no speed or compute-efficiency claim is made. Numerical failed and inaccurate runs remain preserved. Exact LP witnesses/certificates do not depend on trusting solver status.

## Export-orientation correction

CVXPY 1.9.3 stores the sparse-matrix equality `Marg @ fullR == 2*w` as the expression `2*w - Marg @ fullR`. The raw exported equality multiplier at linear_duals[6] therefore has the opposite orientation to the mathematical constraint used by the independent verifier. The final witness negates that free equality multiplier once. No physical constraint, PSD multiplier, or numerical solve was changed. Both the initially failed sign convention and the corrected passing verification are retained. Use audit_residual/dual_witness_corrected.json, not the raw exported witness, for replay.

The last constructor run completed optimization and wrote all raw duals, then was interrupted during redundant floating gradient diagnostics. The expensive repeated diagnostic-gradient evaluation is fixed in the current script; the original extraction version is preserved. The independent proof verifier does not depend on constructor diagnostics or on solver status.
