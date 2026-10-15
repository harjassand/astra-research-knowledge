# Primary probability statements and retrieval boundary

Audit date: 16 October 2026, Australia/Brisbane.

## Hartarsky--Toninelli, arXiv:2212.08437v2

Primary full text: [versioned HTML](https://arxiv.org/html/2212.08437v2),
[versioned PDF](https://arxiv.org/pdf/2212.08437v2).
Fresh local receipts are in `sources/` and `SOURCE_RECEIPTS.json`.

Locations: Section 2.4, PDF pages 6--7; Definition 9.1 and the diameter
convention, PDF page 23; Corollary 9.5 and its proof, PDF page 25. The
arXiv HTML anchors are `S2.SS4`, `S9.Thmtheorem1`, and `S9.Thmtheorem5`.

Paraphrase of the relevant definitions and result: a CA uses one local
finite-coordinate map synchronously at all translates. Attractiveness is
coordinatewise monotonicity. Erosion requires extinction of every finite
zero island in an otherwise all-one configuration. Death marks are iid
Bernoulli variables indexed by both site and integer time and force the
output to zero. The upper invariant law is the limiting all-one law.
Connectivity and diameter use Euclidean distance. For each fixed positive
radius `k` and each attractive eroder, there are `c>0,delta_0>0` so that
every `0<delta<=delta_0` satisfies

```
P(diam A_(x,t) >= ell) <= delta^(c(ell+1)),
```

where `A_(x,t)` is the anchored space-time zero component in the trajectory
initialized with that upper invariant law. The hypothesis is explicitly
an "attractive and an eroder" CA, with an "upper invariant measure" initial
law. The result concerns space-time components, not merely a one-site
stability probability.

Application checks and cold-start path coupling are independently derived
in `CLUSTER_IMPORT_AUDIT.md`; they are not additional paraphrases of HT.
For comparison only, HT Section 10, equation (10.6), PDF page 31 uses its
own all-one-to-upper-invariant comparison for a decreasing trajectory event.

## Liggett--Schonmann--Stacey, 1997

Published identity: *Domination by product measures*, Annals of Probability
25(1), 71--95, DOI [10.1214/aop/1024404279](https://doi.org/10.1214/aop/1024404279).
The [original abstract reproduced in Liggett's complete bibliography](https://celebratio.org/Liggett_T/article/840/)
is item [69], around web-extracted lines 1810--1816.

Paraphrase of the part of that original abstract needed here: on a countable
graph of bounded degree, a binary field whose conditional probability of
one, given the values outside a site's neighborhood, is uniformly at least
`p` dominates a positive-density product law when `p` is sufficiently high.
The dominated density can approach one as `p` approaches one. Its further
sharp one-dimensional thresholds are irrelevant to this audit.

The exact qualitative external premise used in the reconstruction is:

```
For a fixed finite degree bound D and every rho<1 there is p_D(rho)<1
such that any binary field H on a countable graph of maximum degree D
with

P(H_v=1 | sigma(H_w : w outside the closed neighborhood N[v]))
  >= p_D(rho) almost surely, for each v,

stochastically dominates iid Bernoulli(rho) on the graph's vertices.
```

Finite dependence with sufficiently high uniform one-site marginals
is a special case because the displayed conditioning leaves the marginal
unchanged. No association, FKG property, translation invariance, equal
marginals, or independence of adjacent sites is needed for that premise.
The application in the audit verifies this conditional premise directly.

Original theorem-page retrieval status: **not acquired**. Crossref identifies
the version-of-record PDF endpoint as
`http://projecteuclid.org/download/pdf_1/euclid.aop/1024404279` and the official
article page as the DOI-resolved `.full` endpoint. These and the contemporary
`.pdf` endpoint returned security-challenge HTML, rather than PDF bytes.
The article page in the ordinary browser also displayed hCaptcha; that
challenge was not solved. The author's [papers page](https://www.math.ucla.edu/~rhs/papers.html)
links `papers/lss.dvi`, which returned 404. Thus this audit does not assign
an original theorem number or certify the original proof by inspection.

Independent primary corroboration of the application class: HT v2 Section 8,
proof of Corollary 8.2, PDF page 22, applies LSS to a field of good blocks with
a fixed dependence range and marginals approaching one. That is corroboration
of the needed standard import, not a replacement claim that the original LSS
theorem pages were read.

## Swart--Szabo--Toninelli scope

The HT proof refers to Toom-contour results in Swart--Szabo--Toninelli.
I briefly inspected the [versioned v1 HTML](https://arxiv.org/html/2202.10999v1)
only to check whether local-map and self-input conventions introduced an
extra obstruction. No SST theorem is used as an independent replacement
for HT, and no generic continuous-time eroder-stability implication is used.
The proof reconstructed here compares the microscopic process to a genuinely
synchronous **analysis** CA through explicit good flags.
