# Exact boundary elimination: current construction and nonautomatic steps

Working notes, no theorem claimed.

For a bounded-coordinate set B and finite box J of its population values, retain unbounded coordinates u. A reaction (a,b)→(a',b') at phase r∈J with r≥b has coefficient k(r)_b, count source a, phase target r'=r+b'−b. If r' lies outside J it is a killing edge for the restricted strip; its actual incoming adjoint contribution from outside must later be supplied as boundary forcing. If r' lies inside J it is a finite-mode mass-action edge.

The exact frozen phase generator Q0(u) ignores count shifts, includes phase changes with rates k(r)_b(u)_a, and kills upon leaving J. Its ordinary transient-block forest cofactors are positive polynomials in the rates. Their logarithmic derivatives are bounded by degree/u_i once all unbounded coordinates are above source orders. This fact does not use recurrence.

However the matrix relevant to mu(u,r)=(u!)^(−alpha)v_r(u) is the factorial-tilted phase matrix, not Q0. Its ideal forward off-diagonal edge weight is

    k(r)_b a_a(u)^(1−alpha) a_a'(u)^alpha,

with the original total outgoing rates on the diagonal, including same-phase count-changing edges as tilted diagonal contributions. A positive inverse of this tilted matrix does NOT automatically have a positive-coefficient polynomial expansion; cancellations can occur in determinants/principal minors. The simple example (u−v²)²+1 shows why positivity of an algebraic function alone gives no degree/u log-derivative bound.

An original weakly reversible return path from a lifted complex either returns within J or exits J. Consequently closed lifted complex components and genuinely leaking components must be distinguished. The former can coexist with the latter in one finite phase strip. For example, the single-linkage triangle0→A+B→2A+3B→0 has many full residual complex layers entirely contained in a B strip, while other layers meet its boundary. One cannot assert that every lifted complex is killed merely because the frozen physical phase chain can reach the strip edge.

## Candidate robust route
Prove a tilted M-matrix with a strict RELATIVE diagonal margin, not merely spectral negativity. A finite-dimensional coercivity estimate uniform in u could bound its principal minors relative to products of diagonal activities. Positive path/cofactor formulas would then furnish comparison with finite sums of positive monomials, potentially restoring shift control. Alternatively smooth its positive resolvent with a positive kernel having bounded log-shift ratios, but then prove that the tails preserve the relative matrix margin uniformly in highly anisotropic u; a bound polynomial in max u is insufficient when min u grows only logarithmically.

Neither robust matrix claim nor the required inter-stratum boundary-forcing estimate is presently proved. The accepted finite-phase one-unbounded-coordinate result avoids multivariate valleys through univariate rational asymptotics; that argument cannot simply be reused when several u coordinates escape at unrelated rates.
