# Challenge of the path identification-versus-stability construction

## Verdict and precise model

The root's proposed construction is correct. It proves a structural stability
failure for two exact query directions on path support, despite injectivity.
The proof uses symmetric tridiagonal matrices including their diagonals.
For the two-column query matrix X, EVERY row x_i has Euclidean norm1. Noise
is measured by the absolute Frobenius norm of the whole action-error block.

The lower bound does not, as written, cover every query block with only a
bound on total energy and arbitrarily unequal row energies. The unit-row
hypothesis is part of the theorem. Comparisons below retain it exactly.

This is a universal mathematical family argument, not another numerical
benchmark or a claim about conditioning of the actual NIST nine-column data.
No historical novelty is claimed for path incidence spectra, graph coloring,
or direct sparse probing.

## Exact identification threshold

One query never identifies this support for n>=2. On any adjacent pair of
vertices, choose a nonzero vector w orthogonal to the two restricted query
entries; `D=w w^T`, extended by zero, is a nonzero allowed symmetric matrix
annihilating that query.

For two columns, if adjacent row vectors x_i,x_(i+1) are dependent, the same
rank-one construction using a nonzero w with `w^T X_pair=0` proves
noninjectivity. Unit rows ensure neither vector is zero, but the argument
also handles a zero row if that normalization is dropped.

If every adjacent determinant is nonzero, leaf elimination proves injectivity.
The first output row is `D_11 x_1+D_12 x_2=0`, so both coefficients vanish.
Symmetry removes D_21. The next row then contains only the independent x_2,
x_3, and induction proceeds to the final diagonal coefficient. Hence two is
the exact minimum for injectivity, and adjacent independence is necessary and
sufficient under the unit-row assumptions.

## Flow construction: signs and endpoints

Write each row x_i as a column vector when using the following two-dimensional
formula. Let `J=[[0,-1],[1,0]]`, so `det(x_i,J x_i)=1` for unit x_i.
Choose arbitrary real scalars c_0,...,c_n with c_0=c_n=0 and put

    delta_i = det(x_i,x_(i+1)),
    b_i = c_i/delta_i,                       1<=i<n,
    a_i = -b_(i-1)<x_i,x_(i-1)> - b_i<x_i,x_(i+1)>.

Missing endpoint terms are zero. Let D have diagonal a and off-diagonal b.
The unit-vector decomposition is

    x_j = <x_i,x_j> x_i + det(x_i,x_j) J x_i.

Its parallel component cancels by the definition of a_i. The left-neighbor
determinant equals `-delta_(i-1)`, while the right one equals delta_i, giving

    (D X)_(i,:) transposed = (c_i-c_(i-1)) J x_i.

Therefore the exact energy identities and lower bound are

    ||D X||_F^2 = sum_(i=1)^n (c_i-c_(i-1))^2,
    ||D||_F^2 = sum_i a_i^2 + 2 sum_i b_i^2 >= 2 sum_(i=1)^(n-1) c_i^2.

The inequality uses `|delta_i|<=1`, not a lower determinant bound. Small
adjacent determinants can make the constructed D larger, so they cannot
repair this obstruction.

## The root's tent gives an operator-norm lower bound

Take `c_i=min(i,n-i)` and put `m=floor(n/2)`. Each difference is plus or minus1,
except the single zero central difference when n is odd. Thus

    ||D X||_F^2 = 2m <= n.

Also `||D||_2>=max_i|b_i|>=m`. Every inverse constant satisfying

    ||D||_2 <= C_2 ||D X||_F   for all allowed symmetric D

must therefore obey

    C_2 >= m/sqrt(2m) = sqrt(m/2) >= m/sqrt(n).

The root's stated bound is valid. The displayed middle expression is the
slightly stronger exact odd-n version. Diagonal single-entry matrices also
give C_2>=1; the tent bound becomes the decisive growth statement for large n.

For the Frobenius inverse constant, the same tent gives

    C_F^2 >= [2 sum c_i^2]/(2m).

For n=2m, `sum c_i^2=m(2m^2+1)/3`, giving `(2m^2+1)/3`.
For n=2m+1, `sum c_i^2=m(m+1)(2m+1)/3`, giving `(m+1)(2m+1)/3`.
In particular C_F grows at least linearly with n.

## Strengthening: the optimal two-query Frobenius constant is exact

Within the same unit-row model, the flow construction gives more than an
asymptotic lower bound:

    inf_X sup_(D nonzero, symmetric tridiagonal)
        ||D||_F/||D X||_F = 1/[sqrt(2) sin(pi/(2n))].

The infimum is over all two-column X with each row of norm1; a noninjective
X has infinite inverse constant. No numerical optimization is needed.

### Universal lower bound

For any injective X, choose `c_i=sin(pi i/n)` in the flow construction. The
Dirichlet difference identity is

    sum_(i=1)^n (c_i-c_(i-1))^2
       = 4 sin^2(pi/(2n)) sum_(i=1)^(n-1) c_i^2.

To verify it, use
`2c_i-c_(i-1)-c_(i+1)=2(1-cos(pi/n))c_i` and sum after multiplication by c_i.
Combine this identity with `||D||_F^2>=2 sum c_i^2`. The resulting ratio is
at least `1/[sqrt(2)sin(pi/(2n))]`, for every admissible X.

### Attainment by alternating orthogonal rows

Take `x_i=e_1` for odd i and `x_i=e_2` for even i. For arbitrary diagonal a
and off-diagonal b, self and neighbor contributions occupy different output
coordinates, so

    ||D X||_F^2 = ||a||_2^2 + ||T b||_2^2,
    ||D||_F^2 = ||a||_2^2 + 2||b||_2^2,

where T is the n-by-(n-1) unsigned vertex-edge incidence matrix of the path.
Its Gram matrix has diagonal2 and off-diagonal1. The sine eigenvectors give
eigenvalues `2+2cos(j pi/n)`, j=1,...,n-1. Its smallest eigenvalue is
`4sin^2(pi/(2n))`. Consequently

    ||D||_F/||D X||_F <= max(1,sqrt(2)/sigma_min(T))
                        = 1/[sqrt(2)sin(pi/(2n))].

Equality is attained with a=0 and the smallest-singular-value vector b, namely
an alternating-sign multiple of `sin(pi i/n)`. This is exactly the universal
flow witness above because adjacent determinants alternate between plus and
minus1. At n=2 the constant is1; for large n it is asymptotic to
`sqrt(2)n/pi`. This is an exact optimum for the stated Frobenius stability
objective, not an exact operator-norm optimum.

## Three columns restore an isometry at the same row energy

Set row i of X_3 to `e_(i mod 3)` in R^3 (with a consistent one-based color
convention). Each row still has norm1 and total query Frobenius energy is n.
The diagonal and at most two neighbor contributions in each product row
occupy three distinct coordinates. Therefore for EVERY symmetric tridiagonal D,

    ||D X_3||_F^2 = sum_i a_i^2+2 sum_i b_i^2 = ||D||_F^2.

This implies the exact inverse constants C_F=1 and C_2=1; a single nonzero
diagonal entry shows1 cannot be improved under unit row energy. In the
small n=2 case, two columns already achieve this, so the three-column statement
is a sufficient construction rather than a pointwise minimality claim at n=2.

For the growing path family, two-column unit-row schemes have unbounded
inverse constants, whereas the fixed three-column construction is uniformly
isometric. Exact injectivity therefore does not ensure uniformly stable
identification. A reconstruction or spectral-use claim still needs the actual
action error model and total numerical cost.

## Checks and limits

`checks/check_path_stability.py` uses exact Fraction arithmetic on small
rational unit-row examples, including both determinant signs, odd/even n,
the parallel-row null witness, and the three-color isometry. It verifies the
flow identity directly. It does not infer the universal proof from sampling,
run a new scientific benchmark, or compute a large operator spectrum.

The script's receipt is `results/path_stability_challenge.json`. Reasoning,
proof authoring and integration are additional, unmetered costs. The closest
historical machinery includes graph-coloring matrix recovery and the classical
path incidence spectrum; their use is not presented here as a new discovery.
Observed script body including imports:0.029332419s wall,0.029304189s CPU,
peak RSS9437184 bytes. Twelve exact rational fixtures and two parallel-row
null-witness cases passed; there was one run and no numerical optimization.
