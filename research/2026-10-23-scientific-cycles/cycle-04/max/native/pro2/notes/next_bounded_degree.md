# Chosen next frontier: four versus five on bounded-degree partial 2-trees

This is a continuation seed, not a second experimental programme in the present
capsule. Keep exactly the free-diagonal, real row-cap, absolute Frobenius action
noise and operator-output contract of PROOF.md.

Question: does every support of treewidth at most two and maximum degree at
most four admit four graph-adapted real query directions and a dimension-
independent global inverse constant?

The accepted P_(8m)^2 obstruction has maximum degree four and excludes three.
The present triangular lower family and fan-tree proof use unbounded degree,
so neither settles four here. Restricting degree removes the just-proved
branching mechanism and isolates conditioning from an arbitrarily large local
action reservoir.

Five directions give a simple finite-palette upper guarantee. The square of
a graph of maximum degree four has degree at most4+4*3=16. Greedily color it
with at most17 colors. Give these colors17 fixed real vectors in R^5, each
of norm at most one and with every subset of at most five linearly independent
(for example normalized distinct Vandermonde rows). In each closed neighborhood
the colors are distinct, and there are at most five vertices.

There are finitely many submatrices made from at most five palette rows, all
having full row rank. Let eta>0 be the least positive smallest singular value
over them. Each observed action row determines its supported coefficient row
by a left inverse of norm at most1/eta. With arbitrary action error E, the
independently recovered row matrix T has ||T-D||_F<=||E||_F/eta. Project T
orthogonally onto the symmetric supported subspace; Frobenius norm cannot
increase. This yields the same operator upper bound. eta is independent of
graph size, although this note does not claim it is large or practical.

A supported rational unnormalized finite palette with each row scaled by a
rational cap could replace the normalized example, and eta can in principle be
certified. No such conditioning optimization or numerical certificate was
performed here. Five actions, distance-two graph preparation, local systems,
arithmetic error and later spectral work all remain real costs.

The first substantive next obligation is either a four-direction frame and
global inverse estimate or a bounded-degree all-design obstruction. Local
neighborhood rank at four columns is insufficient in degree-four rows, but
symmetry can couple their missing coefficient. Neither that rank deficit nor
another failed periodic palette decides the question. No precision, cluster,
query-length or old-benchmark sweep is an automatic repair.
