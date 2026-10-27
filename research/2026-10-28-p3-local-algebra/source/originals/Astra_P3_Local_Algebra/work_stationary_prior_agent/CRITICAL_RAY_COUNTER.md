# Critical-ray compression for arbitrary homogeneous ternary chain cubics

## The coefficient-level theorem

Let A=F_q[t]/(t^e), q=2^d, and let
lambda_e(a)=Tr_{F_q/F_2}([t^(e-1)]a). Let H in A[X,Y,Z] be an ordinary
homogeneous cubic whose XYZ coefficient mu is a unit. Let Q be an explicit
binary polynomial of degree at most two on the coordinates of
(A/t^h A)^3. Assume 3h<=e+1. Then

    Z(H,Q)=sum_{x in A^3} (-1)^(lambda_e(H(x))+Q(x mod t^h))

has a deterministic exact algorithm polynomial in e,d and the explicit
coefficient description, except for a possible finite-field terminal when
e=1 modulo3. A known fixed-variable finite-field point counter makes that
terminal polynomial in d as well. No smoothness, splitting, low rank, or
supplied critical points are assumed. There is no branching over q residue
points and no Walsh expansion.

The implemented API is

    weighted_homogeneous_sum(field_modulus,e,P,Q,
        terminal_bit_budget=24,field_terminal=None)

in `homogeneous_chain_counter.py`. It returns `(signed_count,certificate)`.
P is a dictionary from ordinary exponent triples to packed ring coefficients;
Q is a set of Boolean ANF masks. Coordinates have three consecutive blocks
of ed bits, with low t powers first and d consecutive field bits per power.
The ring and its coordinates are supplied to this coefficient-level module;
the root compiler manufactures them and the H+Q representation from raw ANF.

The executable computes all depths congruent to0 or2 modulo3 without any
field or ring enumeration. At depth1 it calls an explicitly supplied exact
field backend, or performs explicitly budgeted enumeration. The implementation
does not silently claim that enumeration is polynomial in d.

## 1. Manufacture at most three projective singular rays

Write H_0 for the residue cubic. Since mu_0!=0, H_0 is square-free over the
algebraic closure. Indeed a nonsquarefree ternary cubic has the form L^2 M
for linear forms L,M, and in characteristic two such a product has zero XYZ
coefficient. A square-free plane cubic has at most three singular projective
points: an irreducible cubic has at most one (a line through two singular
points would have intersection multiplicity at least four); a line and an
irreducible conic have at most two intersections; three lines have at most
three pairwise intersections. These arguments also cover coincident
intersection points.

Use three disjoint affine charts, normalizing the last nonzero residue
coordinate to one. In the Z=1 chart, write

    f(x,y)=a x^3+b x^2 y+c x y^2+d y^3+mu x y
           +u x^2+v y^2+w x+s y+k.

Its transverse gradient is

    g_x=a x^2+c y^2+mu y+w,
    g_y=b x^2+d y^2+mu x+s.

This is an affine F_2-linear map on F_q^2. Construct its 2d by2d binary
matrix by its action on the coordinate basis and solve by binary Gaussian
elimination. Its ordinary Jacobian is the constant invertible matrix

    [0 mu; mu 0].

Consequently every algebraic root is isolated and simple. Bezout bounds
the number of roots of the two quadratics by four, so the binary kernel has
dimension at most two. Enumerating its at most four solutions is constant
work after the linear solve. Filter by f_0(x,y)=0 and the disjoint-chart
condition. Euler's identity for degree three shows that these are precisely
the projective singular points of H_0. This construction uses neither a
field-element scan nor a polynomial factorization routine.

The same formulas hold after permuting the distinguished chart coordinate.
The implementation checks the kernel and total-ray bounds rather than
continuing under an invalid assumption.

## 2. Lift each transverse critical point uniquely

The transverse gradient over A remains affine F_2-linear, with invertible
ordinary Jacobian. Every residue solution has a unique lift c=(c_x,c_y)
such that g(c)=0 modulo t^e. For a direct constructive proof, suppose c is
known modulo t^j for j>=1. The change t^j(delta_x,delta_y) changes the jth
gradient coefficients by (mu_0 delta_y,mu_0 delta_x), since its square has
valuation at least2j>j. The two new field digits are determined immediately.
The code executes these corrections and verifies both full gradient
identities.

Put C=f(c), and write the degree-two Taylor part around c as

    A U^2+mu U V+B V^2,
    A=u+a c_x+b c_y,     B=v+c c_x+d c_y.

Only the residues A_0,B_0,mu_0 are needed for the sign

    kappa=(-1)^Tr(A_0 B_0/mu_0^2).

All lifted critical points can be computed once at the original depth.
Their truncations are the unique critical points at every later depth.

## 3. Exact transverse elimination with a quotient weight

Fix a unit radial coordinate r and one projective critical point v. In its
chart, the three-variable vector is r(x,y,1), with x,y restricted to the
selected residue pair. Let v_e=(c_x,c_y,1) be its lifted critical vector.
Assume the quotient weight sees h<=floor(e/2) digits.

For e=2m, split the two transverse variables as a+t^m u. The quadratic and
cubic Taylor terms vanish modulo t^e. Summing u forces the gradient at a
to vanish modulo t^m, hence forces a to the unique critical lift. The
remaining value of Q is Q(r v_e), and the exact transverse factor is

    q^e (-1)^(lambda_e(r^3 C)+Q(r v_e)).

For e=2m+1>=3, first sum the last m digits. This forces a critical lift
modulo t^m and leaves one field digit in each transverse variable. The
weight Q is constant on these digits. Their exact field Gaussian is

    sum_(U,V in F_q) (-1)^Tr(r_0^3(A_0 U^2+mu_0 U V+B_0 V^2))
       =q kappa.

To verify the sign, replace the square terms under the trace by linear
terms. Summing U imposes
V=sqrt(r_0^3 A_0)/(r_0^3 mu_0). The residual trace is
Tr(sqrt(A_0 B_0)/mu_0)=Tr(A_0 B_0/mu_0^2), independent of r.
Together with the earlier q^(2m) factor, the transverse contribution is

    q^e kappa (-1)^(lambda_e(r^3 C)+Q(r v_e)).

The case e=1 is deliberately excluded from this Taylor argument: its cubic
term does not vanish and is handled by the field terminal.

## 4. Radial counting is binary quadratic, including arbitrary quotient noise

The remaining radial phase

    rho(r)=lambda_e(C r^3)+Q(r v_e)

is a binary polynomial of degree at most two. Squaring in A is F_2-linear,
so r^3=r*r^2 is quadratic. Multiplication by each coordinate of v_e is
F_2-linear, and Q was binary quadratic. Thus exact binary quadratic
elimination evaluates

    R_e(C,Q,v_e)=sum_(r in A^*) (-1)^rho(r)
       =sum_(r in A) (-1)^rho(r)
        -sum_(s in tA) (-1)^rho(s).

The two Gaussian sums have ed and d(e-1) binary variables. Their complete
matrices and affine terms are manufactured by evaluations at zero, basis
vectors, and basis pairs. There is no assumption of a supplied Gaussian
decomposition. Every critical ray contributes q^e R_e for even e, and
q^e kappa R_e for odd e.

For Q=0 there is a useful cross-check. The unit sum vanishes unless
v_t(C)>=e-1. If C=0 it equals q^(e-1)(q-1). If C=t^(e-1)b it equals
q^(e-1) times the field Gaussian sum of Tr(b r^3), minus q^(e-1).
Highest-digit orthogonality proves the vanishing case. The separate
unweighted implementation uses this formula, so the two executed paths
also give differently organized checks.

## 5. The origin contributes one recursive state

The highest-digit orthogonality identity forces every surviving nonzero
residue vector onto one of the acquired projective singular rays. The
remaining residue vector is zero. Restrict it by X=tY. Homogeneity gives
H(tY)=t^3 H(Y), and Q(tY) sees at most h-1 quotient digits.

For e>=4, the two top layers of Y are unused. Their six field coordinates
contribute q^6, leaving one state at depth e-3 with the restricted quadratic.
The implementation constructs this restricted ANF and checks that no term
uses a proposed discarded coordinate. At e=2 or3 the cubic vanishes and,
under the stated height bound, the remaining weight is Q(0); the origin
contributes (-1)^Q(0) q^(3(e-1)).

The condition 3h<=e+1 is preserved by h->max(h-1,0), e->e-3. It guarantees
h<=floor(e/2) at every non-field stage. At a depth-one terminal the weight
is constant. Thus at most three nonrecursive Gaussian ray calculations and
one smaller state are created per stage. The depth is O(e), not an
exponentially branching tree.

## 6. Costs and the finite-field terminal

Let N=3ed and let B_Q be the bit length of the explicit quadratic ANF
description. Field and ring arithmetic, gradient acquisition, Hensel
lifting, and Gaussian coefficient manufacture all have polynomial cost.
A conservative direct bound is O(N^7+B_Q N^3) bit operations and
O(B_Q+N^4) bits of working storage. This deliberately allows schoolbook
field arithmetic and unoptimized pointwise coefficient manufacture. The
answer and every accumulated integer have O(N) bits.

At depth one the remaining signed sum is
Z_1=sum_(x in F_q^3)(-1)^Tr(H_0(x)). Introduce one field variable w and count
the zeros of w^2+w+H_0(x). Their number is q^3+Z_1. Lauder--Wan,
Proposition36 and its affine torus decomposition in Section6.4, give
deterministic soft-O(d^19) time and soft-O(d^12) space for this fixed-degree,
four-variable problem in characteristic two. This is established
finite-field point counting, not a new algorithm claimed here. A caller
may supply such a backend to the executable. Its built-in enumeration is
only a transparent finite validation backend.

Combining the known terminal with the proved recurrence yields a polynomial
coefficient-level algorithm for every e and d. Combining this with the root
compiler's acquired-ring and exact-fit theorem is a separate raw-input
claim; it must retain its own acquisition and admissibility hypotheses.

## Executed evidence

`homogeneous_chain_checks.py` completed88 unweighted cases through18 bits,
covering6,628,416 complete truth-table assignments. The cases include XYZ,
nonsplit/reducible singular cubics, a nodal cubic, generic cubics, and random
nilpotent coefficients. Four additional randomly transformed split-product
oracles at72,180,192,1152 original binary coordinates matched the known
XYZ count. The1152-bit case has d=12,e=32; it is a coefficient-level test,
not a raw-representation acquisition benchmark.

`weighted_homogeneous_checks.py` completed88 weighted cases through24 bits,
covering291,836,416 complete truth-table assignments. It tests fields of
degrees1,2,3, smooth and singular residues, arbitrary randomized nilpotent
coefficients, and quotient quadratics with the largest possible even polar
rank. A72-bit d=12,e=2 example with rank36 quotient noise matched an
independent three-axis Gaussian oracle, giving signed count8658654068736.
The tests make no practical speed or historical priority claim.

Ten additional cases in `critical_ray_extension_checks.py` use the
geometrically irreducible nodal cubic

    H_0=X^2 Z+XYZ+Y^2 Z+X^3.

At its unique singular point (0,0,1), the tangent cone X^2+XY+Y^2 is
nonsplit over F_(2^d) for odd d. The tests verify the negative Arf sign,
random higher ring coefficients, and quotient noise over d=1 and3,
through24 bits. The same program tests eight larger-height residuals below;
the combined18 cases cover53,319,368 complete truth assignments.
For geometric irreducibility, regard H_0 as a linear polynomial in Z over
the algebraic closure's polynomial ring in X,Y. Its two coefficients
X^2+XY+Y^2 and X^3 are coprime, so Gauss's lemma proves irreducibility.

## 7. Adaptive extension beyond the sufficient height bound

The exact ray calculation only requires 2h<=e at the current stage. Hence
one may continue the same algorithm for a larger initial height until
this inequality fails, then enumerate the single residual state. This is
implemented by the optional `residual_bit_budget` argument. The default
still rejects inputs outside the polynomial theorem's height range.
Enumeration is explicitly recorded and budgeted, and never represented
as a polynomial-time primitive.

Let h_0=floor((e+1)/3), Delta=max(0,h-h_0). At stage j, the current depth
and height are e-3j and max(h-j,0). While the weight is nonconstant, the
ray elimination condition is equivalent to j<=e-2h. Thus the first
unhandled depth, if the loop has started, is 6h-2e-3. If it cannot start,
the residual depth is e. For Delta>=1 the residual variable count is at
most

    min(3ed, 3d*max(1,6Delta-1)).

The additional exact cost is therefore exponential only in this residual
dimension, with a polynomial factor for evaluation. For constant d and
constant excess height Delta, this remains polynomial in the original
number of bits, even when the error rank grows with e. It is a parameter
bound, not a generic polynomial-time claim for growing d*Delta.

The smooth examples in `QUOTIENT_HEIGHT_SHARPNESS.md` violate the universal
sign-only invisibility identity at one extra quotient digit. The adaptive
counter nevertheless exactly handles all eight tested depths1 through8
using residuals of at most15 bits, including the24-bit original instance.
This distinguishes a failed simplification from a counting obstruction.

## Source

Alan G. B. Lauder and Daqing Wan, *Counting points on varieties over finite
fields of small characteristic*, https://arxiv.org/pdf/math/0612147,
Proposition36 and Section6.4. The core local cancellation belongs to the
classical stationary-phase tradition; this note proves the specific
critical-ray, binary-gradient acquisition, and quadratic-weight interface.
