# Audit of the acquired eight-moment field terminal

## Conclusion

The semilinear acquisition and the reduced eight-state terminal in
`work_stationary_prior_agent/acquired_pair_terminal.py` are correct on
the stated raw-input promise. No flaw was found in the scalar handling,
normal-form completeness, Gaussian sign argument, moment reconstruction,
or composition with arbitrary higher nilpotent cubic coefficients and
the certified quotient quadratics.

The strongest verified theorem uses eight moments of total degree at
most three, hence ordinary cubic Artin--Schreier hypersurfaces in at most
eight variables. With the cited Lauder--Wan algorithm, the terminal has
conservative bit bounds `soft-O(d^31)` time and `soft-O(d^20)` space,
plus polynomial acquisition, reconstruction, and output arithmetic.
These exponents are independent of the number of repeated pairs.

The generic point-count engine has not been implemented or executed.
The executable moment interface and all tests use explicitly supplied
moments; test scans are labeled as such. The theorem is not an empirical
polynomial-time performance result. The older 49-moment reconstruction
is also correct, but its `d^85`/`d^56` bound is superseded here.

## 1. Semilinear descent, including every scalar

Let `m=b-1` and let `sigma` denote coordinatewise squaring. In a centered
contact chart, write

    H=G3(x)+z Q2(x)+tau z^3,
    grad G3=M x^[2],       polar(Q2)=Omega,
    S=Omega^(-1) M sigma.

For the advertised source form, let `D0` be the direct sum of
`[[0,1],[1,1]]`, and let `gamma0` be its common coefficient. After a hidden
field coordinate change and centering the unique transverse critical
point, the old and new coordinates satisfy

    x_old=R x,             z_old=t z.

Include an independent phase scale `theta != 0`. The transformed matrices
are

    M = theta gamma0 R^T M0 R^[2],
    Omega = theta gamma0 t R^T Omega0 R,
    S = t^(-1) R^(-1) D0 sigma R.

Thus the phase scale cancels from `S`; the radial scale does not. Its
Frobenius norm is nevertheless one, since `t^(q-1)=1`. Consequently

    K=S^d=R^(-1)D0^d R.

For `3` not dividing `d`, choose `r=d^(-1) mod 3` and put `D=K^r`.
Then

    D=R^(-1)D0 R,
    F=D^(-1)S=t^(-1)R^(-1)sigma R,
    Fix(F)=R^(-1)t F_2^m.

The implementation's recurrence `K <- A sigma(K)`, starting with the
identity, computes the coefficient matrix of `S^d` in the correct order.
It chooses `K` when `d=1 mod 3` and `K^2` when `d=2 mod 3`, as required.
For any accepted norm certificate, `D` and `S` commute as maps and
`F^d=I`. The code independently verifies the fixed-space dimension and
that its binary basis is also a field basis.

If that basis is `U=R^(-1)t E`, with `E` invertible over `F_2`, then

    U^T Omega U=theta gamma0 t^3 E^T Omega0 E.

This proves the common scalar is `gamma=theta gamma0 t^3`. In particular,
radial rescaling contributes a cube, not a first or second power. Both
the transverse cubic and the `z Q2` term have that same common scalar.
The extra `tau z^3` is permitted and transforms separately; it must not
be silently absorbed into an unsigned distribution.

## 2. The acquired symplectic planes are complete

On the descended binary space, `D^2+D+I=0`, and `D` preserves the
nonsingular alternating form `B=Omega/gamma`. The binary quadratic

    v -> B(v,Dv)

has polar form `B`, since `D^(-1)=D+I`. It therefore takes the value one
on some vector. A basis and its pairwise sums suffice to find one: a
quadratic vanishing at all these vectors would have every coefficient
zero. The plane spanned by `v,Dv` is nonsingular and `D`-stable, and its
orthogonal complement is also `D`-stable. Repetition constructs the
advertised two-dimensional blocks without enumerating the field.

The identity `S=D sigma` on the acquired fixed basis gives `M=Omega D`.
On each block,

    Omega/gamma=[[0,1],[1,0]],
    M/gamma=[[1,1],[0,1]],

which is precisely the gradient matrix of `X^3+XY^2+Y^3`. A homogeneous
ordinary cubic with no squarefree terms is determined by this matrix:
every repeated cubic has a unique odd-exponent derivative, and Euler's
identity also excludes a derivative-free cubic.

All subsequent changes within the descended space are binary. Therefore
a planted binary `Q2/gamma` retains binary coefficients. Its known polar
form removes cross terms between distinct manufactured planes; its
remaining square coefficients give the two bits for each plane. The
rotation `(X,Y)->(Y,X+Y)` preserves the cubic and cycles the three square
types `(0,0),(0,1),(1,0)`, while fixing `(1,1)`. It preserves the common
`gamma` and `z`; there is no extra phase or radial coefficient.

The code compares the complete transformed ordinary polynomial with the
manufactured template. Thus none of these conclusions depends on equality
at a sample of field points, and small-field polynomial-function aliases
cannot create a false coefficient certificate.

## 3. The quartic polar-kernel bound has the correct gamma factors

For either pair Gaussian, the binary polar kernel consists of `(x,y)`
satisfying

    gamma x^2+(gamma x)^(q/2)+gamma y^2+gamma z y=0,
    (gamma x)^(q/2)+gamma y^2+(gamma y)^(q/2)+gamma z x=0.

Squaring these equations and dividing by `gamma` gives exactly

    gamma x^4+x+gamma y^4+gamma z^2 y^2=0,
    x+gamma y^4+y+gamma z^2 x^2=0.

Over the input field, squaring is bijective, so these are equivalent,
not merely necessary conditions. Over the algebraic closure the quartic
system has the constant invertible Jacobian `[[1,0],[1,1]]`. Its affine
solutions are all isolated and simple. The degree bound gives at most
sixteen geometric solutions, so the binary kernel has dimension at most
four. Since the polar matrix is alternating on `2d` bits, that dimension
is `k=0,2,4`. No assumption of a generic `gamma` or `z` is used.

## 4. Why the minus Gaussian is never zero, with its exact sign

The complete minus-pair polynomial is invariant under

    C:(x,y)->(y,x+y),       C^2+C+I=0.

This is an ordinary polynomial identity, so it survives arbitrary
`gamma`, `z`, and the absolute trace. Its binary polar radical `R` is
`C`-stable. The quadratic is linear on `R` and invariant under `C`.
For `r` in `R`, applying it to `r+Cr+C^2r=0` forces its value at `r` to
be zero. The quadratic therefore descends to a nondegenerate quadratic
on the quotient by the radical.

The induced `C` remains symplectic and satisfies the same order-three
polynomial. The invariant-plane construction from Section 2 applies.
For a plane basis `v,Cv` with `B(v,Cv)=1`, invariance and
`C^2v=v+Cv` imply

    Q(v)=Q(Cv)=Q(v+Cv)=1.

Each such plane is anisotropic and has Gaussian sum `-2`. There are
`d-k/2` planes, and the radical supplies a factor `2^k`. Thus

    A_-(z)=(-1)^(d-k/2) q 2^(k/2).

The plus Gaussian has the same polar matrix. At `k=0` it is nonzero;
at `k=2,4` it can be zero or have either sign with that magnitude.
This proves exactly the eight-state palette in the implementation.
The proof works over every residue degree; `3` not dividing `d` is
needed separately for the promised one-critical-point acquisition.

## 5. Exact moment reconstruction and costs

Let `epsilon=(-1)^d`. The three distinct minus-value levels are
`epsilon q,-2 epsilon q,4 epsilon q`. Moments with indices

    (0,0),(0,1),(0,2), (1,0),(1,1),(1,2), (2,0),(2,1)

recover their masses and first plus-value sums by two three-by-three
Vandermonde solves. At the first level, the second plus-value sum is
already `q^2` times its mass. The last two moments recover the remaining
two second plus-value sums. At each level these data determine its two
or three state masses uniquely, even when the masses are signed by
`(-1)^Tr(tau z^3)`.

For the exact node and row ordering used in the code, the magnitude of
the eight-by-eight evaluation determinant is

    2^15 * 3^7 * q^14.

Thus all denominators and intermediate entries have `O(d)` bits. Each
moment has `O(d)` bits as well: its total degree is at most three. The
final state powers have `O(bd)` bits and are computed by ordinary exact
integer arithmetic. The Python rational inversion implements this
orientation correctly; signed mass and integrality checks are correct.
The convention `0^0=1` is needed when one pair multiplicity vanishes and
is correctly implemented by Python integer powers.

The largest expanded character moment has three independent pair copies
and one shared radial coordinate: seven field variables. The additional
Artin--Schreier coordinate gives one degree-three equation in eight
variables. Its exact point count minus `q^7` is the moment. Smaller
moments use the corresponding smaller exponent. The zeroth moment is
itself binary quadratic and is computed directly by the implementation.

The primary Lauder--Wan paper explicitly gives, for fixed characteristic,
total degree, and variable count `N`, a point-count bit bound
`soft-O(d^(3N+7))` and space bound `soft-O(d^(2N+4))`. It permits singular
hypersurfaces and accepts an irreducible-polynomial field presentation.
With `N<=8`, the asserted `31` and `20` exponents follow. This is at most
seven nontrivial point-count calls plus the zeroth Gaussian. There is no
dependence on growing `b` inside their fixed-variable parameter.

Primary source, checked directly: Lauder and Wan, *Counting points on
varieties over finite fields of small characteristic*, Theorem 1 and the
quantitative paragraph immediately following it; Proposition 36:
<https://arxiv.org/pdf/math/0612147>.

## 6. Completeness after raw affine acquisition and deep perturbations

For the promised residue, the alternating third form is a nonzero scalar
times `z wedge omega`, with `omega` symplectic of dimension at least four.
Its centroid over the residue field is exactly the scalars. The full
scalar centroid over the chain ring is also the base ring, even when all
higher cubic coefficients are arbitrary. Indeed, radical-freeness makes
centroid operators commute with the known scalar ring, hence makes them
ring-linear. Reducing an operator modulo the maximal ideal makes it
scalar. Subtract that scalar and divide by the uniformizer; induction
over the remaining depth makes every successive layer scalar too.

The raw compiler therefore reacquires the full ring and a free module
basis. The quotient coefficient lemma and modular center solve identify
the residue homogeneous cubic uniquely up to the acquired ring,
module, and functional coordinate changes. In the certified height
range `3h<=e+1`, the ambiguity is in `J^(e-h)`, and `e-h>=1`; it cannot
alter the residue cubic. This is why an arbitrary binary quotient
quadratic cannot invalidate the extra pair certificate after a valid fit.

Ring automorphisms preserve the maximal-ideal filtration and induce a
field automorphism on the residue. They preserve the binary coefficients
of the displayed pair model. A change of primitive Frobenius functional
multiplies the residue polynomial by a nonzero scalar, already handled
in Section 1. The unknown binary affine input disguise is removed by the
acquired module coordinates and center, rather than assumed to be an
available field-coordinate decomposition.

Each pair's centered affine gradient reduces to

    X^2+Y^2+Y=0,           Y^2+X=0.

Its nonzero solutions would give a root of `Y^3+Y+1`, irreducible over
`F_2`; none exists when `3` does not divide `d`. There is consequently one
affine transverse critical point, independent of the number of pairs.
The invertible square matrix excludes the missing projective hyperplane.
The radial cubic makes this point a projective critical ray precisely
when `tau=0`. All higher nilpotent coefficients retain unique transverse
Hensel lifting. The existing weighted origin descent then reaches this
same certified residue at a field leaf, if a field leaf occurs at all.
The original quotient support condition is exactly what that descent
uses; a small binary rank of the quotient quadratic is unnecessary.

## 7. Additional executed adversarial checks

The owned script `eight_state_audit.py` tested 406 `(gamma,z)` pair
Gaussians over degrees one through five, with 327,056 complete pair-phase
evaluations. It checked the ordinary quartic equations against the exact
binary polar kernel at every tested vector, checked order-three invariance
and vanishing on the radical, and compared the minus Gaussian with the
proved sign and magnitude. The nullity histogram was

    k=0:247 cases,       k=2:152 cases,       k=4:7 cases.

Signed moment reconstruction was also checked for pair multiplicities
including `(0,0),(1,0),(0,1),(3,5),(20,31)`. The exact determinant formula
above was checked. All assertions passed.

`pair_terminal_deep_audit.py` manufactured a new raw 80-bit cubic with
`d=4,e=4,b=5`, both pair types, nontrivial phase scale, arbitrary higher
nilpotent cubic coefficients, a rank-20 quotient quadratic, and a hidden
binary affine disguise. The root compiler reacquired the chain ring,
center, homogeneous lift, quotient quadratic, and pair certificate. It
found one critical candidate and one projective ray, and returned the
signed count

    -3659174697238528.

This agreed with a coefficient-level chain counter whose field leaf was
independently exhausted over all `16^5=1,048,576` field assignments. The
whole 80-bit domain was not enumerated. The manufactured field scale was
seven and the acquired common scale was two, exercising nontrivial
normalization. The saved moments were then replayed through the updated
eight-moment interface and compared exactly with the retained 49-moment
interface. The moments themselves came from an explicit 16-value field
scan. This is a compositional correctness check, not an execution of the
general polynomial-time point-count theorem.

Data are in `eight_state_audit_results.json` and
`pair_terminal_deep_audit_results.json`. No other agent's files were
modified. Historical novelty of the complete compiler is a separate
question from the mathematical correctness audited here.
