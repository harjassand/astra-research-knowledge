# Acquired first rung and tested next-depth restriction

The first connected input is frozen and independently accepted. All material
in this note beyond that input is numerical feasibility data. No additional
exact/cyclotomic acquisition was launched after the first accepted result.

At beta3, exact degree192 power arrays evaluated by bounded Chebyshev series
give scalar Rayleigh lower322705.85 and current A4 radii

    I:334848.06, O:354492.56, N sixth moment:356009.92.

The interval evaluation is accurate enough to expose this particular failed
mode count. Increasing its polynomial degree or arithmetic precision would
not remove the displayed count failure. This does not prove that the N sixth
moment exceeds the true leading eigenvalue, which is not accurately acquired.

## Boundary channels and deflation preview

For a spin-j irreducible boundary tensor, one actual transfer mode contributes
to the A4 lists with multiplicities

| j | I | O, per copy | N |
| ---: | ---: | ---: | ---: |
| 0 | 1 | 0 | 0 |
| 1 | 0 | 0 | 1 |
| 2 | 0 | 1 | 1 |
| 3 | 1 | 0 | 2 |
| 4 | 1 | 1 | 2 |

The physical diagonal tensor components used in the numerical preview are
orthogonal weight-zero irreducible tensors with values on m=-2,...,2:

    j1: [-2,-1,0,1,2], j2: [2,-1,-2,-1,2],
    j3: [-1,2,0,-2,1], j4: [1,-4,6,-4,1].

Their actual source message moments are endpoint tensor correlations on
open2--6. The new exact endpoint-spin producer acquired j1 moments, with
independent analytic open2/3 checks. Higher j channels have only numerical
proposals. `code/multichannel_discovery.py` computes all SU(2) multiplets.

The simple two-vector proposals at beta3 leave I/O/N residual radii
333471.62,344664.71,338367.62, all above the scalar lower322705.85. Triplet
deflation alone cannot fix the independently failed I/O counts. No higher-j
exact producer was started on the basis of this negative preview.

## Parent-proposed A5 refinement

The independently assessed A5 five-angle preview is in
`results/a5_preview.json`, with complete physical sectors and literal closing
rotations. It took7.13s. At beta3, the best p4/p6 radius divided by the same
scalar lower is

| A5 list | radius/theta | selected moment |
| --- | ---: | ---: |
| 1, other modes | .8391860 | 6 |
| 3 | 1.0197939 | 6 |
| 3prime | .6859565 | 6 |
| 4 | .7003242 | 6 |
| 5 | .8772552 | 6 |

This fixes the I/O contamination in that preview and isolates one remaining
triplet-list obstruction. It is useful complementary structure, but its raw
relative loop-tail proposal is453.2. No accepted beta3 spatial seed follows.
At beta1.5 all ratios pass; at beta6 all relevant ratios fail.

Further numerical checks did not justify costly field acquisition:

- The degree-six Christoffel count from A5 triplet moments2--6 gives
  a negative radius1.012158 times scalar theta, still above one.
- Triplet event-fugacity enrichment with16 actual trial messages raises the
  Rayleigh proposal from277951.22 to294119.44. The variance remains5.238e9.
- Removing all16 compressed Ritz sixth powers from the A5 triplet sixth
  moment leaves a proposed residual radius291915.36. The full moment-budget
  upper for the top mode is328912.54, or1.019233 times scalar theta. The
  Rayleigh/residual separation is too small for a useful Temple bound.

These are failures of particular acquired/proposed interfaces. They are not
general lower bounds, a gap obstruction, or a reason to reject richer
messages, different compression or ordinary thermal methods.

## Cost and domain of the fugacity interface

The scalar finite-message identity in `COSTS_AND_COMPARISON.md` is an identity
of history kernels/quadratic forms on finite-history functions. D_t is
generally unbounded when|t|>1, so no bounded-operator similarity is assumed.
The actual finite messages remain in the Hilbert space: if x has k events,

    |f_(r,a)(x)| <=25(2 sqrt(beta)|r|)^k exp(12|a|),

and the squared norm is at most625 exp(24|a|+12 beta r^2). The Poisson
history measure supplies this finite sum. Complete source quadratic forms
therefore exist at every finite parameter used by the numerical proposer.

Trial rank R does not enlarge the maximum six-site physical system, but the
number of new inhomogeneous thermal traces can grow asR^2. They are not free
oracle inputs. Certifying the current large enriched grids would incur a
substantial new acquisition cost, and their numerical previews still miss
the target; no such job was launched.
