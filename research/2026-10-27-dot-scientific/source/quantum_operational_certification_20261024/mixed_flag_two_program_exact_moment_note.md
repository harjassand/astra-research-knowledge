# Two-program mixed-flag Haar moment

2026-10-27. Exact small-n diagnostic, not a many-program complexity theorem.

For the family in `mixed_flag_haar_collision_inverse_lower_bound.md`, the half trace distance of the two logical-data Haar experiments with exactly TWO normalized Choi programs is

 (10+2sqrt(3))/(27r), r>=2.

A direct S3-Weingarten reduction corroborates this symbolically. Twirl the three B registers while retaining the two qutrit A registers. In a permutation basis, the Haar Gram matrix is G_pi,sigma=(3r)^(cycles(pi^-1 sigma)). The retained9x9 contraction X_pi is the logical matrix-unit cycle contraction times r^(cycles(pi)-3)/9. Its only data-label-dependent terms are the two program/data transpositions and the two3-cycles.

Decompose the B permutation algebra into S3 irreducibles: trivial, sign, and standard2-dimensional representation, with multiplicities d(d+1)(d+2)/6, d(d-1)(d-2)/6, and d(d²-1)/3 respectively, d=3r. The executable symbolic checker prints factored characteristic polynomials of each connected block of the retained-reference/irrep difference matrix, multiplied by its representation multiplicity and by r.

The positive-eigenvalue sums of these scaled difference blocks are

 trivial:(2r+1)/(27r),
 sign:(2r-1)/(27r),
 standard:(6+2sqrt3)/27.

They sum to(10+2sqrt3)/27, proving the displayed half-distance after dividing by r. The matrices are Hermitian and traceless, so their positive-eigenvalue sum equals half their trace norm.

Files: `mixed_flag_two_program_moment.py/.txt` (numeric positivity, normalization and six ranks), and `mixed_flag_two_program_symbolic_check.py/.txt` (exact factored blocks).

This improves the two-program constant over the general collision bound, but establishes no stronger n-versus-r asymptotic lower bound. In particular the observed growth from coefficient1/3 at n=1 to(10+2sqrt3)/27 at n=2 does not justify extrapolating linear or square-root behavior in n.
