# Exact acquisition of a hidden triple product: audit and exceptions

Let F=F_{2^d}, with d>=3. The root construction fits a raw Boolean cubic as Tr P(X,Y,Z), with ordinary field degree of P at most three. The homogeneous field-cubic part H can contain X^3 and X^2Y terms which are only quadratic as Boolean functions. These terms must be retained when testing whether the representation can be converted into a balanced triple product. Selecting the canonical cubic lift from the third tensor alone would lose them.

## 1. The homogeneous cubic is uniquely identifiable

If two degree-at-most-three field polynomials have the same scalar trace function on F^3, their homogeneous degree-three parts are equal for d>=3.

Proof. Expand the trace as sum_{j=0}^{d-1} P(X,Y,Z)^{2^j}, and reduce each positive variable exponent modulo q-1 to the range {1,...,q-1}, where q=2^d. The resulting polynomial of separate degree less than q is the unique polynomial representing its F-valued function. The degree-three exponent patterns, up to variables, are

    (3), (2,1), (1,1,1).

Each has a Frobenius orbit of length d, and its own exponent vector is the only member of that orbit whose total degree is at most three. For the pattern (3), doubling cyclically shifts its two adjacent binary ones; for d>=3, every other shift has value at least five. For (2,1), the wrapped shift has total degree 1+2^{d-1}>=5, and all other nontrivial shifts have still higher total degree. For (1,1,1), each nontrivial shift has total degree at least six. No lower-degree monomial belongs to any of these orbits. Therefore, in the reduced trace polynomial, the coefficient of each original cubic monomial is exactly its coefficient in P. Equality of trace functions forces equality of all those coefficients.

Lower field-degree coefficients need not be identifiable: Tr(c X^2)=Tr(c^{2^{d-1}} X), and the trace has a kernel on constants. Those aliases do not affect the homogeneous cubic.

The d>=3 hypothesis is real. At d=2, X^3 takes values in F2, and Tr(X^3)=0; a nonzero homogeneous cubic can disappear under trace. At d=1, X^3=X as functions. Both exceptions are exhibited in the executed coefficient-kernel audit.

## 2. Two searches through seven field elements suffice

Suppose H=c L_1 L_2 L_3, where c!=0 and the L_i are independent F-linear forms on F^3. Neither the factors nor their basis are supplied.

For seven distinct t in F, test v(t)=(1,t,t^2). Each L_i(v(t)) is a nonzero polynomial in t of degree at most two. Thus H(v(t)) is nonzero for at least one of the seven probes. Fix such a v, so each L_i(v)!=0.

For u(s)=(1,s,s^2), consider h_s(T)=H(u(s)+Tv). It has roots

    r_i = L_i(u(s))/L_i(v).

Its roots are pairwise distinct exactly when the following product is nonzero:

    product_{i<j} [L_j(v)L_i(u(s)) + L_i(v)L_j(u(s))].

Each bracket is a nonzero degree-at-most-two polynomial in s, since L_i,L_j are independent and both are nonzero at v. The product has degree at most six and is not the zero polynomial. Consequently one of any seven distinct s works. It is detected without knowing the factors by gcd(h_s,h_s')=1. The leading coefficient H(v) is nonzero, so h_s really has degree three.

These are constant-size searches independent of q; they require q>=8, precisely the stated d>=3 regime.

## 3. Deterministic splitting uses field traces, not enumeration

First verify h divides T^q-T by d modular squarings; combined with squarefreeness, this says all three roots lie in F. For every element a of an F2-basis of F, compute

    R_a(T)=Tr(aT) mod h

by d modular squarings. Split the current factors with gcd(factor,R_a). The nondegenerate trace pairing separates every two distinct F-roots, so after all d basis elements, all factors are linear. This costs O(d^2) field operations for the degree-three polynomials, plus polynomial-time gcd and inversion overhead; standard bit arithmetic is polynomial in d. No field-element loop of length 2^d appears.

For each root r_i put w_i=u+r_i v. Since only L_i vanishes at w_i,

    gradient H(w_i) = c L_j(w_i)L_k(w_i) gradient L_i,

which is a nonzero scalar multiple of the desired factor. The three gradients are independent. Multiply the acquired forms, recover their common scalar by any nonzero coefficient, and verify equality with all coefficients of H. These final checks make the output sound even on inputs outside the promise. A failed split, dependent normals or failed coefficient identity rejects this route.

## 4. Exact execution

`triple_factor_audit.py` reconstructed 120 independently generated hidden triple products over field degrees d=3,4,5,6,8. Every coefficient identity and all 3,840 extra pointwise checks passed. The largest observed searches used three v-probes and four u-probes, within the proved bound of seven. Five examples H=XYZ+X^3, which do not factor into three independent linear forms, were rejected.

The linear coefficient-kernel calculation checked degrees d=1,2,3,4,5. For d>=3, every trace-zero degree-at-most-three polynomial had zero homogeneous-cubic coefficient vector. For d=1,2 the audit found the predicted nonzero cubic aliases. These computations check the exact acquired factor interface, not an asymptotic point-counting backend.

## 5. Scope and ancestry

The trace/Frobenius polynomial representation and finite-field polynomial factorization have established algebraic ancestry. This audit provides a short explicit deterministic acquisition argument tailored to the hidden triple-product interface. It is not a first-priority claim for polynomial factorization or trace methods. The factor test is necessary for the specialized balanced-triple evaluator; the more general Lauder--Wan field-polynomial evaluator may apply even when this test fails.
