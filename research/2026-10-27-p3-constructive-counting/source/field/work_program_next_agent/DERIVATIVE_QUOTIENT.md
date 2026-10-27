# Acquiring the nonlinear quotient modulo quadratics

This subsidiary construction generalizes the earlier cubic-radical step to an arbitrary explicitly given Boolean ANF. It is a reusable exact reduction; no first-priority claim is made. Linear structures and their coordinate reductions have longstanding ancestry, for example O'Connor--Klapper, *Algebraic nonlinearity and its applications to cryptography* (1994), including the cited work of Lai:
https://www.cs.engr.uky.edu/~klapper/pdf/nonlinearity.pdf

Let p:F2^n -> F2 have ANF degree k. For j>=0 define

    R_j = {a: degree(Delta_a p) <= j},
    Delta_a p(x)=p(x+a)+p(x).

Each R_j is a linear space. Indeed Delta_{a+b}p=Delta_a p+tau_a Delta_b p, and translation preserves the degree bound. Starting with R_{k-1}=F2^n, suppose a basis of R_{j+1} is known. On this space the homogeneous degree-(j+1) coefficient vector of Delta_a p is linear in a: translation changes a degree-at-most-(j+1) polynomial only in its lower-degree terms. Evaluate that coefficient map on the known basis and take its kernel. This computes exactly R_j, and iteration acquires R_1 without assuming a supplied nonlinear subspace.

Choose a complementary basis U to R_1, so x=A(u,v) and r=dim U. Every monomial involving a v-coordinate has degree at most two: otherwise its derivative in that coordinate would have degree at least two. Therefore

    p(A(u,v)) = f(u) + q(u,v),

where q is quadratic and can be chosen to contain only terms involving v, while f(u)=p(A(u,0)). Its coefficients are acquired using only values at the basis vectors and their pairwise sums. No dense expansion of the pulled-back polynomial is required.

This quotient is minimal: any representation p(x)=g(Bx)+q_0(x), with q_0 quadratic, has ker B contained in R_1, and consequently rank B>=r. The acquired representation attains r. Gaussian summation over v leaves at most 2^r exact evaluations of the core, regardless of the rank of the original quadratic background.

For an explicit ANF of L terms, each derivative can be expanded in O(L 2^k) term operations. There are polynomially many derivative and linear-algebra operations in n and k. Thus acquisition costs 2^{O(k)} poly(n,L), followed by 2^r poly(n,L) for the count using polynomial-time quadratic sums. A nonquadratic p with such a quotient has k<=r. The acquisition workspace can be exponential in k; polynomial space is not claimed in this general growing-degree version.

The executable `derivative_quotient.py` checked 20 affine-disguised higher-degree fixtures, 68 complete derivative-subspace comparisons and 5,888 pointwise quotient identities. Its finite quadratic leaves are exhaustively evaluated; those checks are identity validation, not a new Gaussian implementation.

## Raw program boundary

This does not infer a hidden degree promise from a few value queries to an arbitrary program. Along the zero function, any unqueried point a can hide the point indicator product_i(x_i+a_i+1), computed by a linear-size AND/NOT circuit. Exact deterministic black-box identification with zero, or certification of cubic degree for n>3, therefore requires all Boolean inputs in the worst case. The executable includes the all-ones point indicator on eight bits, which agrees with zero at every Hamming-weight-at-most-three query but has a different exact count. This is a value-query obstruction, not a lower bound against white-box circuit analysis.
