# Fixed-width bulk upgrade

Author-derived and unaudited. This strengthens the weaker logarithmic-bulk construction in `BULK_CONSTRUCTION.md`; that file is preserved as the initial derivation. The global function, exact finite-jump bound, source-cut proof, classwise plateau exclusion, normalization and scale gluing remain the same. The improvement is a sharper use of the acquired active-region distance.

## Theorem

Subject to the governing finite affine-family lemma cited and read in the preceding construction, every finite weakly reversible mass-action network with fixed positive rates admits, on each positive affine compatibility class, a nonnegative normlike function V on the count orthant with

    L V(x)<=-1

outside a class-dependent finite set wherever EVERY coordinate is at least K=max(1,2D), where D is the largest source degree. The assertion covers arbitrary dimension and arbitrary linkage multiplicity. It is a BULK statement, not general recurrence: the union of excluded strips x_i<K is infinite. No bound uniform across conserved enzyme pools or actual communication classes is silently supplied.

If the compatibility class has no point with all coordinates >=1, its bulk is empty. Otherwise choose a single such c as the representative in the affine construction. A count state in the bulk has all sources enabled, and actual falling factorials are uniformly comparable to monomials. No high-volume or continuum limit occurs.

## The strengthened near-active calculation

Write n=min x_i, N=max x_i, R>=2N, and retain affine labels active somewhere in [1,R]^d as before. Their slopes are nonpositive, and the uniform Hoffman constant B is acquired from fixed coefficient matrices. Let

    ell=L log(2+N),

where L is a finite constant chosen below. Call a label near-active when its affine gap is at most ell. It has an actual active point z in [1,R]^d with

    |z-x|_infinity<=B ell.

Both x and z have every coordinate at least one. Hence, even when some x_i are bounded, every coordinate ratio between them is between

    1/(1+B ell) and 1+B ell.

The original derivation unnecessarily demanded a factor-two ratio, which required n to grow logarithmically. A polylogarithmic distortion is enough. If r_i.u<r_i.v, the primary source sign-gap lemma at z gives

    z^v/z^u<=R^(-H),
    x^v/x^u<=(1+B ell)^(|v-u|_1) R^(-H)
              <=(1+B ell)^(2D) R^(-H).                     (A)

At x_i>=2D, the actual propensity ratio loses only 2^D kmax/kmin. For every sufficiently large N, the quantity

    m_E 2^D (kmax/kmin) (1+BL log(2+N))^(2D) (2N)^(-H)

is at most 1/3. This holds uniformly for ALL R>=2N. Consequently every near-active slope satisfies d_i>=Gamma_i/2 for the actual count generator.

The total soft weight of every other label is at most

    m exp(-ell/theta)=m(2+N)^(-L/theta).                    (B)

The exact smooth-minimum jump estimate therefore gives, uniformly for R>=2N,

    L U_R(x)<=C Q(x)(2+N)^(-L/theta),

and, when x is on the chosen affine class and outside K_(1/R),

    L U_R(x)<=-c0+C Q(x)(2+N)^(-L/theta),
    c0=2H kmin/(3m)>0.                                   (C)

An active label is near-active, has weight at least 1/m, and lies outside S-perp in the latter case. It therefore changes along an enabled source edge by at least 2H, so its Gamma is at least 2H kmin. This is the acquired constant behind c0.

## The same scale sum now covers a fixed bulk

Use R_k=2^k, p=2D+2 and V=sum R_k^p U_(R_k), exactly as in the preceding proof. Choose

    L/theta > p/H+D+2.

For 2N<=R<=(2N)^(1/H), the total positive error in (C) is

    O(N^(p/H+D-L/theta))=O(N^(-2)).

The range R<2N still has adverse contribution O(N^(p+D)), and the range R>(2N)^(1/H) still has the locally uniformly convergent exponential tail. A dyadic R in [N^(3/2),2N^(3/2)] is outside the plateau because sqrt(R)<N, and contributes -c0 N^(3p/2). Since 3p/2>p+D, it dominates the adverse range. The same normlikeness proof applies.

All thresholds are selected consistently: the finite family and H first; then theta and Hoffman B; then p and L; then the finite large-N threshold for (A) and the scale estimates. The source cutoff K=max(1,2D) is fixed by the raw reaction list, before these choices. No alpha/strip-width circularity or growing finite-phase family occurs in this bulk proof.

## What this changes and what it leaves

The fixed-width conclusion is stronger than the initial logarithmic band. It removes one specific acquisition problem for a potential boundary join: the bulk cutoff no longer grows with inventory or has to be selected after an unknown strip contraction exponent. It does not by itself supply that join.

N1394's accepted fractional-factorial adjoint bulk lemma is restricted to a SINGLE strongly connected complex graph. Its reviewed multiple-linkage counterexample invalidates that particular unweighted measure; it does not invalidate this different primal, source-cut, finite-affine construction. The rejected residual-factorial softmax is an adjoint algebraic expression with an explicit low-count defect. It is not the log-sum-exp of affine count potentials used here, and the present proof makes no sign claim on its excluded low-count sequence.

Neither result can be combined automatically with a leaky strip resolvent: adjoint/primal orientation, actual neighboring forcing and leakage hypotheses must agree in the same regime. Closed conserved enzyme phases need an actual-time receiver even though all of their stationary tails can be finite and their L2 gap can vanish. A global solution of those conditions remains unearned.

Historical priority and publication-ready correctness remain UNKNOWN pending full checking. The new scientific content is the actual finite-jump curvature bound, near-active acquisition and scale construction above; finite diagnostics or source hashes cannot replace these proofs.
