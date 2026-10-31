# Noncommuting acquisition: costs and contribution boundary

## What changed scientifically

The previous accepted class had A(y)=I+v(y)H, so one fixed matrix
diagonalized every conditional covariance. This continuation proves a
different organizing condition: **Loewner-monotone conditional precision
with bounded curvature has bounded integrated transport resistance**.
Matrices at different y may genuinely fail to commute. The general
factor is 1+L/(2 beta a²), not the old 17/9 estimate.

This is a derivation from ordinary Gaussian Sylvester transport,
Dirichlet/Thomson principles, and a positive-matrix trace inequality. The
root proposed the inequality and an independent conditional-theorem review
checked it before this raw-input constructor. No located primary source
has yet been shown to supply the exact full construction. Historical
novelty remains unresolved. An equally informed ordinary implementation
augmented with this new certificate gets the same capability; that is
not a second independent prior-art victory.

## Executed raw-input route

`compile.py` receives only rational polynomial monomials in physical
coordinates. The high-dimensional runs use sparse aligned coefficients,
not a supplied block decomposition: the parser verifies the entire
monomial dictionary, reads the actual joint nonzero matrix graph, and
acquires its connected components. Exact PSD Schur elimination validates
the two fibers and dyadic spectral upper certificates. The matrix-norm
acquisition uses uI-H>=0, not row absolute sums that could introduce an
artificial dimension factor under a dense rotation.

The raw input stores full exponent vectors. Thus O(m) nonzero monomials
still use O(m²) small entries. General dense degree-ten input can have
O(n^10) monomials. Dense rotated recognition, physical-metric acquisition,
polynomial division/full identity and rational determinant computation
are real costs, not implied to match the aligned fast path.

| Physical n | Raw terms | det-polynomial degree | Exact points | Horner steps | Largest determinant-rational bits | Full conductance interval |
|---:|---:|---:|---:|---:|---:|---:|
|3|13|4|4097|16388|192|[0.08961835,0.63250548]|
|5|26|8|2049|16392|358|[0.06113258,0.43073662]|
|17|104|32|2049|65568|1457|[0.002308845,0.01629638]|
|33|208|64|4097|262208|3205|[1.4937205e-5,1.0520096e-4]|
|65|416|128|4097|524416|6477|[3.1947012e-10,2.2558438e-9]|

All runs acquire u1=u2=1 and a finite-rate factor7 at beta=1; the remaining
width is below1% numerical error. The 65-dimensional run's noncommutator
has squared Frobenius norm1/64, so this is not a commuting family renamed.
Its acquisition took about0.20s and its entire construction about7.45s in
one author run. A distinct fully expanded rotated 5D input (1791monomials)
also succeeds in about8.16s. These are diagnostics on this machine, not
universal benchmark guarantees or physical clocks.

## Determinant degree is not physical dimension

The determinant polynomial may have degree2m, or an intermediate degree
for rank-deficient H2. The executable always passes the ACTUAL physical m
and det_+(H1) to the mass-tail bound, using A>=vH1. It does not inherit
the scalar constructor's accidental equality between determinant degree
and fiber dimension. Explicit rank-deficient and irrational-direction
fixtures are saved and replayed.

The inherited arithmetic class is reused only at its exact accepted hash;
`new_integrator` supplies the different physical tail parameters explicitly.
Integer square-root enclosures, outward rational Darboux sums, fixed
precision rejection, finite cutoff/point/grid/precision/Horner budgets,
safe non-proof display and serialization behavior are retained. The
receiver reconstructs the ENTIRE adaptive computation again. This is more
work than checking only the final grid, but it is paid and avoids treating
a fitted acquisition record as evidence. A differently gridded valid
certificate can be rejected: the receiving implementation is intentionally
sound and incomplete.

## Bit, search and current costs

The matrix graph requires O(n²) entry inspection. PSD/norm acquisition
costs sum of cubic rational eliminations on the acquired components,
with all intermediate rational bit growth. Spectral-upper doubling is
capped at128tries; exhausting it returns UNKNOWN. On the observed bounded
spectra it takes two tests total. A dense input may lose this block
advantage and is charged accordingly.

The exact determinant polynomial has O(m) degree (at most2m); Horner
evaluation pays O(m) rational multiply-adds per point. Under fixed positive
lower/upper conditioning of H1 and bounded H2 operator norm, its marginal
well/resistance widths have the same polynomial-in-m inverse-tolerance
control as the scalar case, with changed constants. Product/coefficients
and output bit lengths grow polynomially, not as the inverse rare flux.
The listed bit proxy measures determinant rationals, not total peak
symbolic memory or every final reciprocal integer. Arbitrary stiff or
ill-conditioned inputs need not be cheap and may hit UNKNOWN budgets.

The current is not assumed to have a convenient common eigenbasis.
It is the explicit linear-system program
`vec S=-(I tensor A+A tensor I)^-1 vec A'`. Exact rational execution at
selected points is in the tests. A generic direct rational solve has its
full n²-unknown cost (naive O(n^6) field operations); no claim is made that
it is free. The analytic certificate avoids expanding this entire current
at every quadrature point because positive-definiteness and the proved
trace bound certify its resistance directly. This is a proved sufficient
operation, not a black-box current optimizer or sampling oracle.

## Real boundaries and strongest alternatives

* Global evenness, not merely slab symmetry, identifies right-tail MA
  with the left-basin mass. The actual polynomial family is globally even.
  The abstract theorem must otherwise use the actual left mass.
* Rotating isospectral fibers can have positive transport cost and zero
  log-determinant derivative. They fail the needed PSD order premise;
  no determinant-only theorem is asserted.
* Ordinary free-energy/determinant methods provide the same scalar upper
  bound efficiently. The newly derived current estimate supplies the
  full-rate multiplicative lower bound. Existing conditional dynamics,
  potential-theoretic capacity, Gaussian geometry and sample-based sliced
  committor work retain all the credit documented in the parent's primary
  source ledger. This continuation has not established a priority search.
* The graph/block routine can improve exact ordinary integration too;
  no unfair fresh-start baseline or withheld matrix structure is used.
* Basins come from the recognized polynomial grammar. No arbitrary basin
  shapes, pointwise MFPT, fixed-deadline CDF, nonreversible or underdamped
  process, nonlinear conditional family, model noise, physical parameter
  measurement, or operational intervention is supplied.

All work remains mathematical/non-operational, with no publication,
upload, outside agents, equipment, purchases, biology or Morrey work.
