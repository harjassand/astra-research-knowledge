# Focused primary comparison at the Cycle9 milestone

The comparison concerns the strongest claim: exact-coordinate count p+1,
uniform stable-coordinate count p+2, and worst-case star count2p+1 on the
stated intrinsic complete-bipartite block-tree class. Historical priority of
this exact separation has not been established by the bounded search.

## Established recovery machinery

Gebremedhin, Pothen, Tarafdar and Walther, *Efficient Computation of Sparse
Hessians using Coloring and Automatic Differentiation*, INFORMS Journal on
Computing21(2),2009, author manuscript:
https://www.cs.purdue.edu/homes/apothen/Papers/hessian-coloring-joc.pdf

The paper gives the support/seed/compressed-action/recovery workflow, relates
star coloring to direct recovery and acyclic coloring to substitution, and
analyzes recovery complexity and numerical stability. In particular Section3.3,
Theorem3.1 bounds an entry's substitution error using a subtree size. The
present operation uses canonical LS and an arbitrary absolute Frobenius-noise
contract; its global constant follows from the specific spider structure.
Allowing nonstar trees or using substitution is not a novelty claim.

Coleman and Cai, *The Cyclic Coloring Problem and Estimation of Sparse Hessian
Matrices*, SIAM J.Algebraic and Discrete Methods7(2),1986,221-235:
https://epubs.siam.org/doi/10.1137/0607026
Primary earlier report, Cornell1984:
https://ecommons.cornell.edu/entities/publication/9e03cca8-ab7d-406d-a78e-314ecd6b897f

The authors already characterize substitution graph-theoretically and analyze
roundoff error and work/storage. The report landing page and publication
metadata were read; its PDF download returned a tool error in this turn, so
no claim relies on reading that unavailable PDF. The later Hessian manuscript's
actual stability section was read directly.

## Established star-color comparison

Albertson, Chappell, Kierstead, Kundgen and Ramamurthi, *Coloring with no
2-Colored P4s*, Electronic Journal of Combinatorics11(1),R26,2004:
https://www.combinatorics.org/ojs/index.php/eljc/article/view/v11i1r26

The primary paper states the classical star-color upper bound binomial(t+2,2)
for treewidth t and its sharpness. This is a broader-class comparator; it
does not state the present absolute-noise inverse on C_p. The owned earlier
general treewidth theorem is preserved, not reproved here.

## What changes relative to the owned checkpoint

The actual marked-root obstruction proves that the accepted atom theorem
cannot simply be glued. A constructive parity assignment on the same hard
block family, its global incidence estimate, and coordinate/star lower bounds
give the three distinct query counts. The full original-action receiving
calculation uses that result. The p+2 operation pays weaker conditioning than
the 2p+1 star control; no practical total-cost advantage is inferred.

Focused searches for star/acyclic colorings of complete-bipartite block trees,
cut-vertex composition, and sparse-Hessian substitution did not identify a
matched primary theorem for all three present counts and this noise contract.
Search coverage is limited, and many hits were unrelated edge-coloring work.
This is not a proof of originality. No bibliography sweep, paid access, or
author outreach was undertaken.
