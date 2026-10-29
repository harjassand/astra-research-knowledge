# An explicit local evaluator, not a precision oracle

This appendix makes the sufficient elementary-cost contract in EXPECTED_BITS
constructive. It is an ordinary arbitrary-precision interval implementation
on a bit machine. It is not an assertion that every version of Arb uses these
particular algorithms, nor a new implementation benchmark.

Use dyadic/rational endpoints, directed integer arithmetic and a postorder
stack for the finite DAG. Re-evaluate at successively doubled precision until
the required strict comparison/floor separates. No unknown conditioning
height is given to the algorithm; heights are used only to bound when its
ordinary refinement must stop.

* Addition/multiplication/division: integer arithmetic with outward dyadic
  rounding. Once a true nonzero denominator's interval excludes zero, the
  inverse-width bound is its ordinary derivative1/x^2. Requested precision
  is increased until that happens. Its additional bits are logarithmic in
  the inverse true denominator, paid in EXPECTED_BITS.
* Integer powers: repeated squaring with O(log(n+1)) products, followed by
  a reciprocal for negative n. The factory's positive intermediate has log
  magnitude <=O(1+e_l G), not O(2^l); marked exponents are at most q. Both
  argument height and amplification are therefore included in that proof.
* Square root: first bracket by dyadic powers, then directed bisection or
  Newton with rational bounds. For a positive argument it has derivative
 1/(2sqrt(x)); inverse-log conditioning is already charged. Exact zero
  components are squared as polynomials, not passed through log.
* Log: binary-rescale x into[1,2], so
  log x = k log2 +2 sum_(j>=0) y^(2j+1)/(2j+1), y=(x-1)/(x+1), |y|<=1/3.
  Its geometric tail gives P-bit enclosures in polynomial work in P and
  1+|log x|. log2 uses the same positive atanh series at y=1/3.
* Exp of real or complex x: binary range reduction to |x/2^k|<=1/2, an
  ordinary factorial Taylor remainder bound, then repeated squaring.
  P+O(1+|x|) internal bits suffice for an absolute P-bit enclosure; this
  conservative polynomial bound is enough here. All random argument
  magnitudes used by the program have the finite moments proved in
  EXPECTED_BITS; rational time is fixed, not a hidden uniform-time constant.
* Gaussian CDF: the entire erf series
  erf(x)=2/sqrt(pi) sum_(n>=0) (-1)^n x^(2n+1)/(n!(2n+1)).
  Taylor's integrated exponential remainder is bounded by
  (2/sqrt(pi))exp(x^2)|x|^(2M+3)/((M+1)!(2M+3)). Taking
  M>=16(P+x^2+1), with conservative directed bounds, gives a geometric
  accuracy bound sufficient for P bits (small arguments can be treated
  even more cheaply). Thus work is polynomial in P+1+x^2, including
  intermediate cancellation precision. pi is acquired by Machin's
  formula16 atan(1/5)-4 atan(1/239), with alternating-series enclosures.
  Its square root is enclosed as above. There is no constant-value oracle.

For all these operations, an ordinary chain/product differentiation bound
on a finite realized expression gives an error at most2^-P times an
amplification factor whose logarithm is polynomial in expression length,
argument magnitude and the paid denominator/log heights. Increasing the
requested precision by that polynomial controls propagated error. Each
operation and every repeated refinement therefore has polynomial bit work
in exactly the random heights whose fixed moments were proved finite.

Gaussian inversion's special all-grid height handles all reused CDF
comparisons simultaneously, and the integer-threshold density argument
handles the nonfresh factory comparisons. Those are probabilistic facts
about the supplied source, not additional numerical subroutines. The
construction establishes an implementable finite-mean bit receiver; a
small explicit bit bound and direct complexity verification of a particular
Arb build remain separate claims.
