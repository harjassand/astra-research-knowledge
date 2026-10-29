# Canonical raw divergence can acquire an unknown nonlinear projective chart

## Result and acceptance contract

Input: a rational polynomial vector field `f` on `n` original coordinates, with no chart, inverse, projective matrix, or observable dictionary supplied. Manufacture

    q=-div(f)/(n+1),       T=D+q,       D=f dot grad.

Acquire the cyclic polynomial space

    V=span{1,T1,T^2 1,...}

by exact sparse elimination or circuit-jet evaluation plus the identity-admission rules in `PROOF.md`. If it closes at dimension `n+1`, choose the acquired basis as

    phi=(1,psi_1,...,psi_n)^T,       T phi=A phi.

Next **construct** a polynomial inverse `H` of `psi` by formal series iteration, and admit it only after checking both global identities

    H(psi(x))=x,       psi(H(y))=y.

No inference from constant nonzero Jacobian to global invertibility is used. A singular basepoint, failed identities, nontermination within a degree budget, deficient cyclic rank, or excessive cyclic rank returns an explicit not-acquired result.

For every admitted raw input the exact original flow is

    z(t)=exp(tA) (1,psi(x0)),
    x(t)=H(z_1(t)/z_0(t),...,z_n(t)/z_0(t)).

This holds on the connected nonsingular interval containing zero. The expression is exact; stable numerical evaluation has separate precision/conditioning costs. Input randomization does not turn finite-point checking into deterministic certification: the current experiment has exact coefficient replay of closure and both inverse identities.

The output now has a minimal possible `n+1` projective linear coordinate count, but **the inverse polynomial still has real degree/circuit/bit cost**. It has not vanished into a supplied decoder.

## Why this acquires hidden information

Suppose, as a sufficient completeness class rather than an admission premise, that the raw system is `f=h_*g`, where `h` is an unknown polynomial automorphism and

    g(y)=a+B y-(c^T y)y.

Define the homogeneous matrix

    M = [[0,c^T],[a,B]],       kappa=tr(M)/(n+1).

As proved in `PROOF.md`, constant Jacobian determinant of `h` implies divergence covariance. The raw operator `T` is transported to the action of `M-kappa I` on the hidden affine-linear functions `1,y_1,...,y_n`.

Assume the homogeneous denominator row `e_0^T` is cyclic for `M`: the rows

    e_0^T, e_0^T M, ..., e_0^T M^n

are independent. This is an open, nonempty algebraic condition on `M`; it is a genuine boundary, not a universal property. The acquired cyclic space then has dimension exactly `n+1` and equals the pullback of all hidden affine-linear functions. Thus the acquired `psi` is an invertible affine transformation of `h^{-1}`, and it has a polynomial inverse of degree `deg(h)`.

The algorithm does not receive cyclicity or `h`. It observes the actual rank, checks closure, builds the inverse, and tests the two identities. The hidden-class argument proves that these operations will eventually succeed at sufficiently large budgets. Genericity is used only to specify that completeness class. For example, affine-linear fields have constant divergence and their `T`-orbit of `1` is one-dimensional; this particular chart route correctly fails despite their being easy to solve by other means.

For an accepted inverse, the transformed field is visibly projective:

    psi'=A_tail,0+A_tail,tail psi - (A_00+A_0,tail psi) psi.

Since a polynomial inverse forces constant Jacobian determinant, divergence covariance further gives `tr(A)=0`. These are consequences/checks, not inputs supplying the chart.

## Constructive inverse, with no Jacobian-conjecture shortcut

Let `c=psi(0)` and `J=Dpsi(0)`. If `J` is invertible, set

    F(x)=J^{-1}(psi(x)-c)=x+N(x),       ord N>=2.

The formal inverse is the fixed point `G(z)=z-N(G(z))`. Starting from `G=z`, each iteration determines one more homogeneous degree. At a tested degree budget `E`, perform `E-1` iterations, truncating every polynomial to total degree `E`. Then test both exact polynomial identities `F(G(z))=z` and `G(F(x))=x`. If they hold, return

    H(y)=G(J^{-1}(y-c)).

If a polynomial inverse of degree `e` exists, a budget `E>=e` obtains it. Budgets `1,2,4,8,...` have total cost bounded polynomially by the first successful degree (or by the explicit final budget). Without a successful global identity test, the formal inverse remains merely local/formal and the algorithm returns no global chart.

For circuit input this can avoid multivariate monomial expansion. Insert a scalar homogenizing parameter `t`, keep coefficients of `G(tz)` through `t^E`, and carry each coefficient as an arithmetic circuit in `z`. Evaluate the circuit for `F` over the truncated ring. Ordinary convolution uses `O(E^2)` arithmetic-circuit operations per source gate per iteration; `O(E)` iterations give polynomial circuit size and arithmetic work in `E`, `n`, and source size. Shared DAGs must actually be retained. The current implementation uses exact expanded polynomials for this inverse step; the circuit construction is a proof-level route, not a claim that the existing script already avoids expansion here.

The global circuit identities require either randomized PIT with independent fresh randomness and degree bounds, or exact coefficient verification with its cost paid. Intermediate rational heights and the degree of the inverse are retained. A small forward circuit alone does not guarantee a cheap inverse. No unrestricted inversion algorithm or solution of the Jacobian conjecture is claimed.

## A proved exponential representation separation

This is a separation from **original-state-containing density-module linearization** and dense polynomial dictionaries, not a lower bound against every conventional symbolic/projective algorithm.

For integers `n>=2` and `e>=2`, let `b=e+1`, set

    lambda_j=b^(j-1), j=1,...,n,
    M=[[0,1,...,1],[0,lambda_1,0,...],...,[0,...,lambda_n]],
    g_j(y)=lambda_j y_j - y_j sum_k y_k.

Let the hidden polynomial automorphism be the triangular shear

    h_j(y)=y_j (j<n),
    h_n(y)=y_n+(sum_{j<n} y_j)^e.

This specifies a family used to prove a resource claim, not a supplied chart to the compiler. The raw pushed-forward field has a division-free arithmetic circuit of size polynomial in `n` and `log e`, degree at most `2e`, and rational input coefficient bit lengths polynomial in `n log(e+1)`. Substitution uses the compact inverse shear; generating the family does not place that inverse in the acquisition input.

**Small-chart route.** The eigenvalues of `M` are distinct. Eigenlinear forms of the homogeneous flow can be chosen as

    ell_0=Z_0-sum_j Z_j/lambda_j,       ell_j=Z_j.

Thus `Z_0=ell_0+sum_j ell_j/lambda_j` has a nonzero component on every eigenspace. Its cyclic rank is `n+1`; the chart route acquires an `n+1`-dimensional module. The chart inverse has degree `e`, and the circuit formal-inverse construction above has polynomial arithmetic cost in `n,e` and the acquired circuit size, not in `binomial(n+e,e)`.

**Original-state density route.** At weight `m`, its module must contain `1,h_1,...,h_n` in hidden coordinates. If `m<e`, the highest-degree part of repeated `T_m h_n` is multiplied at each step by a nonzero scalar times `sum y_j`, so degrees increase strictly forever. There is no finite original-state-containing module at those weights.

At `m=e`, the seed `1` corresponds under homogenization to `Z_0^e`. Its expansion in the eigenforms has a nonzero coefficient for every monomial

    ell_0^alpha_0 ... ell_n^alpha_n,       sum alpha_j=e.

The eigenvalues of these monomials, before an irrelevant common trace shift, are `sum_{j>=1} alpha_j b^(j-1)`. All are distinct: these are base-`b` expansions with digits in `0,...,e=b-1`. There are exactly `binomial(n+e,e)` of them. The Vandermonde criterion therefore gives a cyclic dimension of exactly that size already from seed `1`.

For `m>e`, the eigenvalue-support set from `Z_0^m` contains the set for `Z_0^e` (increase only `alpha_0`); all expansion coefficients are positive, so colliding eigenvalues do not cancel. Thus every finite original-state-containing integer-weight density lift has dimension at least `binomial(n+e,e)`, with equality achieved at weight `e`.

Taking `e=n`, the old linear-module dimension is `binomial(2n,n)` while the acquired chart uses `n+1` linear coordinates plus a degree-`n` inverse circuit. This is an exponential dimension separation on compact raw circuits. It is not merely another small hidden-shear benchmark. The nonlinear decoder is the mathematical reason the original-state linear lift need not carry the entire symmetric-power representation.

An equally informed conventional algorithm can exploit the same acquired chart and inverse. No exponential lower bound against arbitrary Lie/projective/Darboux recognition algorithms follows from the representation separation.

## Implemented result

`acquired_projective_chart.py` takes the raw coefficients only. On the recorded test it acquires

    phi=(1, x^4-2x^2 y+x^2-x+y^2-y, x^2-y),

with generator

    A=[[-8/3,-1,0], [0,-5/3,6], [0,0,13/3]].

The degree-one and degree-two formal inverses fail global checks; degree four passes both. The returned inverse is stored explicitly in `chart_results.json`. Twelve independent trajectory checks agree within `1.7e-16`; polynomial closure and both inverse identities are exact. This is a full acquired three-dimensional projective representation and original-coordinate decoder, not only a latent predictor.

## Conventional ancestry and nonclaims

The projectivization of linear systems, Riccati/Lie--Scheffers theory, density Lie derivatives, Darboux polynomial cofactors, and formal polynomial inversion are established mathematics. The sources and strongest symbolic first-integral comparator are in `PROOF.md`. Projective Riccati systems were explicitly linearized long before this work: *Linearization of homogeneous Riccati equations* (1983), https://doi.org/10.1016/0375-9601(83)90647-3 ; see also Carinena--de Lucas, *Lie systems: theory, generalisations, and applications*, https://www.impan.pl/shop/publication/transaction/download/product/88196 . These are not evidence that an unknown polynomial chart has been acquired from raw equations, but they prohibit claiming projective linearization itself as new.

The current contribution is an independently checkable **raw acquisition composition**: canonical divergence, a low-rank cyclic density module, actual inverse manufacture, and original-state reconstruction. Historical priority of that complete combination remains unestablished. No general claim about chaos, arbitrary polynomial flows, data-only identification, noisy robustness, numerical stability, or scientific usefulness follows automatically.
