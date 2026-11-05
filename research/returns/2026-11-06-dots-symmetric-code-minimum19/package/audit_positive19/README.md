# Certified 19-qubit positive control

This directory contains a genuine rank-two, fully symmetric 19-qubit code of
distance exactly five. It is the real Pollatsek–Ruskai-form example reported by
Arda Aydin, Max A. Alekseyev, and Alexander Barg in *A family of permutationally
invariant quantum codes*, Quantum **8**, 1321 (2024), Section 7, Equation (32)
and Proposition 7.1: https://arxiv.org/html/2310.05358v3#S7
Published DOI: https://doi.org/10.22331/q-2024-04-30-1321.

The paper prints approximately six significant digits, and describes an msolve
interval solution. We did not obtain or execute that software/output. Instead,
the scripts here refine the printed root and independently certify it using
exact rational arithmetic. The exact definition is algebraic, not a claim that
the printed decimal coefficients are exact.

## Codewords

Set q0=1. Let (q2,...,q18) be the unique real common zero of the nine polynomials
in `positive19_certificate.json` within the rational box recorded in that file.
Every coordinate has radius 10^-40 around its recorded rational center. Define

N = sum_{i=0}^9 binomial(19,2i) q_(2i)^2,
c0[2i] = q_(2i) sqrt(binomial(19,2i)/N), c0[odd]=0,
c1[w] = c0[19-w].

Then |a_L> = sum_w ca[w] |D_w^19>, with normalized Dicke states. The two columns
are exactly normalized and orthogonal: normalization follows from N, while
opposite support parity gives orthogonality. For convenient inspection, the
nonzero c0 coefficients at weights 0,2,...,18 are approximately:

0.27605970767460486, 0.17240114480700283, -0.45931542887160404,
-0.23025527925703998, 0.25266458926658519, 0.44237567653046611,
-0.058697374225638192, 0.45458388782655601, 0.076363608708871808,
0.39321978439548361.

## Exact proof and independent replay

For the nine polynomial equations f(x)=0, let x0 be the rational center and R
the recorded rational approximate inverse Jacobian. On the closed box of
radius r=10^-40, the map T(x)=x-R f(x) has the exact bounds

||T(x0)-x0||_infinity/r < 1.906e-11,
sup ||DT(x)||_infinity < 1.946e-36.

These bounds prove T maps the box strictly into itself and is a contraction.
Also ||I-R J(x0)||<1, so R is invertible. Hence the box contains exactly one
zero of f. Every bound and strict inequality is evaluated with exact rationals.

For completeness, all 25 entries of the off-diagonal logical four-qubit reduced
operator and all 25 entries of the difference between logical diagonal reduced
operators are proved to be exact linear combinations of these nine equations.
The positive factors sqrt(binomial(4,a)binomial(4,b))/N are removed in this
polynomial check. Thus every weight-at-most-four physical operator has scalar
compression to the code. This proves arbitrary two-qubit error correction.

A five-site Pauli Z string has different logical diagonal entries; an exact
rational box bound proves their difference is nonzero. Consequently the
distance is exactly five, not merely at least five.

Run `python replay_certificate.py` for a fast standard-library-only exact
replay. It does not perform root finding and needs no third-party packages.
Run `python verify_positive19.py` to regenerate using SymPy, mpmath, and NumPy.

The numerical independent spin-monomial check covers every J+^a Jz^b J-^c with
a+b+c<=4 (35 monomials): maximum residual divided by max(1,Frobenius norm of
the operator) is 3.323e-17; the Gram error is 2.221e-16. The unscaled maximum
monomial residual is 3.411e-13, reflecting operator norms at degree four.

## Using the positive control

`positive19_dicke.npz` contains V, the 20-by-2 float64 Dicke coefficient matrix,
and P=V V^T. It also records n=19 and d=5. These floating values are numerical
approximations to the exactly specified certified code, not themselves an
exact certificate.

`check_lift_positive19.py` constructs the coupled three-copy twirl directly
from the code's tensor-product columns, without an 8000-by-8000 density matrix.
It checks the exact same marginal, enumerator, rank-zero-through-four lifted
KL, permutation-commutant, antisymmetric-support, PPT, and complement constraints
used in `three_copy_sparse.py`. It writes `positive19_lift_receipt.json` and
`positive19_lift_blocks.npz`. A separate direct coupling of the time-reversed
third code copy checks the PPT recoupling map. This is a numerical sanity test
of the SDP identities, separate from the exact proof of the code itself.

The completed check passes at tolerance 10^-10, with no optimization involved:

- Marginal residual: 1.311e-14; multiplier residual: 4.552e-15.
- Maximum lifted KL residual: 2.253e-16.
- Direct versus recoupled PPT image: 1.688e-16.
- Minimum eigenvalue of R: -1.369e-18; of PPT(R): -5.947e-17.
- Minimum eigenvalue of B-R: -6.198e-18; of B-PPT(R): -9.910e-18.
- Triple trace error relative to trace 8: 5.418e-14.
- Antisymmetric-support residual: 2.797e-17.
- Worst scalar MacWilliams identity residual: 7.816e-14.

Negative eigenvalues are at floating-point roundoff scale. The receipt retains
all per-block eigenvalues and every lifted-KL residual. Construction and checks
took about 108 seconds in this environment.

No constructor or solver source files were changed. In particular, the sparse
fallback in `audit_lift.py` is a 21-qubit code and was not relabeled as 19.

## Targeted literature freshness check, 2026-11-05

A brief public-web search for unrestricted exclusions at n<=18 or a minimal-19
theorem, including Sep–Nov 5, 2026 queries, found no such published result.
This is a scoped negative search, not an exhaustive novelty certification.

The current primary records checked were:

- Bond, Minar, Ozols, Safavi-Naini, Visnevskyi, *Permutation-invariant codes:
  a numerical study and qudit constructions*, arXiv:2603.10981. The current
  arXiv record still has v1 dated 11 March 2026. Section 3.1 reports numerical
  searches and states Conjecture 3.1; it does not supply an unrestricted
  mathematical exclusion at n<=18.
  https://arxiv.org/abs/2603.10981
  https://arxiv.org/html/2603.10981v1#S3.SS1
- Kubischta and Teixeira, *MacWilliams Identities for Intrinsic Quantum Codes*,
  arXiv:2604.16023. The current record still has v2 dated 26 August 2026.
  Appendix B-D gives the distance-three PI example; no distance-five
  n<=18 exclusion was located in it.
  https://arxiv.org/abs/2604.16023
  https://arxiv.org/html/2604.16023v2

The AAB paper's Section 7 remark about no shorter code is in its restricted
real parity-separated construction context. It is not used here as an
unrestricted no-go theorem. The Zoo's September 15 status is consistent with
the primary records, but the present code verification does not depend on the
Zoo: https://qiqc-op.com/problem/op_a72722e455d85d55/.
