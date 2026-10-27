# Ordinary cubic identifiability and split-plane lifting over a chain ring

Let A=F_q[pi]/pi^e with q=2^d, d>=3, and let lambda be the field trace of the top pi coefficient. Root proposed the identifiability proof below. This audit independently checks it, supplies an explicit seven-dimensional factor lift, and executes both claims. These are interfaces to the current exact counter, not a priority claim for Hensel lifting or finite-ring structure.

## 1. The homogeneous ordinary cubic is identifiable

**Lemma.** Let H in A[X_1,...,X_b] be homogeneous of ordinary degree three, and G have ordinary degree at most two. If lambda(H(X)+G(X))=0 for all X in A^b, then H=0 as a formal polynomial.

**Proof.** Fix X and scale all its coordinates by rho in the embedded coefficient field. Put c=top_pi(H(X)). The assumed scalar identity reads

    Tr(c rho³ + a rho² + b rho + f)=0 for every rho in F_q.

For d>=3 the binary cyclotomic orbit of exponent 3 modulo q-1 has length d and is disjoint from the orbit of 1 and the constant exponent. Indeed 3 is not congruent to a power of two modulo q-1. If 3*2^i is congruent to 3 for 0<i<d, then q-1 divides 3(2^i-1); for i<=d-2 the latter is smaller than q-1, and the only remaining i=d-1 forces d=2. Thus no such i exists. Expanding the traces and reducing exponents gives a polynomial function with disjoint exponent supports. Its cubic-orbit coefficients must vanish, so c=0.

Therefore the top coefficient of H is zero for every X in A^b. Expand each X_i as sum_(k=0)^(e-1) X_(i,k) pi^k with X_(i,k) in F_q. The top coefficient is an ordinary F_q-polynomial of total degree three, strictly less than q, in the be coefficient variables. Evaluation zero on every field point implies it is the zero formal polynomial.

Write H=sum_(|alpha|=3) sum_j h_(alpha,j) pi^j X^alpha. Choose an index i with alpha_i odd. Such an index exists because the total degree is odd. For j<e-1 put k=e-1-j>0. The coefficient-variable monomial

    X_(i,k) X_(i,0)^(alpha_i-1) product_(l!=i) X_(l,0)^(alpha_l)

in top(H) has coefficient alpha_i h_(alpha,j)=h_(alpha,j). No other exponent vector or coefficient layer can contribute: grouping coefficient variables by their original X-variable identifies alpha, and their pi weight identifies j. For j=e-1 use the monomial product_i X_(i,0)^alpha_i. All h_(alpha,j) therefore vanish. QED.

The qualifier d>=3 is necessary. In d=1 or 2, top-layer ordinary cubic functions have scalar trace aliases with lower ordinary degree or with zero. The executable coefficient-kernel test reproduces these aliases. This lemma does not say that the third Boolean difference alone identifies H: repeated-variable ring cubics such as X²Y are Boolean quadratic. The full scalar function, including its lower Boolean coefficients, is needed.

## 2. Residue factorization followed by seven corrections

Let H be a homogeneous ordinary cubic on A³ whose residue H_bar factors into three independent F_q-linear forms with a nonzero multiplier. Acquire those forms by the previously audited seven-probe field factorization and invert their coefficient matrix. After that F-linear coordinate change and multiplication by a residue unit, H is XYZ modulo pi.

Suppose a product L_1 L_2 L_3 is correct through pi^(j-1), where L_i reduces to the corresponding coordinate and j>=1. Update

    L_i <- L_i + pi^j M_i

for F_q-linear forms M_i. Modulo pi^(j+1), the product changes by

    pi^j (M_1 YZ + X M_2 Z + XY M_3).

The image has precisely these seven monomials:

    XYZ, X²Y, X²Z, XY², Y²Z, XZ², YZ².

The pure cubes X³,Y³,Z³ are absent. Fix a gauge by setting the Y coefficient of M_2 and the Z coefficient of M_3 to zero. The seven remaining coefficients map bijectively to the seven monomials. Solve the correction directly. If a nonzero pure-cube error occurs at this layer, reject: no lift to independent planes exists.

Why can this gauge not reject a genuine factorization? Any actual lift of the three residue planes can be normalized so the coefficient of Y in its second factor and the coefficient of Z in its third factor are exactly one; they are units. Absorb both unit scalars in the first factor. Under this normalization the first-order correction is unique at every layer. Thus any actual split product follows the same lift. The final product is verified coefficient by coefficient modulo pi^e.

The root implementation uses the equivalent gauge with all three diagonal plane coefficients one and a separate multiplier lambda. Then the XYZ error corrects lambda, and the six remaining monomials correct the six off-diagonal entries using the inverse of lambda's residue. This is algebraically equivalent to the audit gauge.

Every returned plane matrix reduces to an invertible field matrix, hence is invertible over A. Gaussian elimination over A uses only pivots that are units; modulo the maximal ideal, ordinary nonsingular elimination guarantees a unit pivot exists at each stage.

For fixed three variables, each layer uses constant-size polynomial arithmetic and field operations. Schoolbook ring multiplication is O(e²d²) bit operations; e layers cost O(e³d²), besides the prior field factorization and exact fitting. There is no search through q or q^e elements.

## 3. A decisive lifting failure

For any 1<=j<e, the polynomial XYZ+pi^j X³ has split independent residue XYZ. At its first nonzero error layer the pure-cube term is outside the seven-dimensional correction image. It therefore has no factorization into three A-linear forms whose reductions are independent. It is rejected by both the independent audit and root factor interface. Residue-field splitting alone is insufficient.

## 4. Executed checks

`chain_cubic_hensel_audit.py` acquired 72 independently generated products of three ring-linear forms, with random unit multipliers, for (d,e)=(3,2),(3,3),(4,2),(4,4),(5,3),(8,4). All full coefficient identities passed, together with 1,728 pointwise checks. Four nonliftable pure-cube cases were rejected.

The scalar coefficient-map kernel was computed exactly on all Boolean points of weight at most three. Since all candidate functions have Boolean degree at most three, these evaluations determine their complete ANFs. Results:

| d | e | n | coefficient columns | kernel dimension | basis relations involving cubic coefficients |
|---|---|---|---|---|---|
| 1 | 2 | 6 | 40 | 19 | 12 |
| 2 | 2 | 12 | 80 | 24 | 9 |
| 3 | 2 | 18 | 120 | 23 | 0 |
| 3 | 3 | 27 | 180 | 35 | 0 |
| 4 | 2 | 24 | 160 | 31 | 0 |

The lower-degree alias dimensions are not failures: the cubic block is unique when d>=3, whereas trace-linear square and constant aliases remain and must be handled by exact fitting. No generic ring-polynomial factorization theorem or point-counting implementation is claimed by this audit.
