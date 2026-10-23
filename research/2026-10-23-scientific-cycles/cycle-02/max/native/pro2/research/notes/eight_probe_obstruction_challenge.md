# Independent challenge: eight directions cannot identify the original pattern

## Verdict

The root's new dimension obstruction is correct. It sharpens the earlier
chronological7--9 identification bracket to an exact optimum of9 directions,
when combined with the existing verified nine-column injectivity certificate.
The earlier absence of a9-clique remains true; that failed necessity mechanism
has been replaced by a denser induced-subgraph dimension argument.

No large657-variable linear system was formed or solved for this challenge.
The conclusion follows from an exact source count and a general rank theorem.

## Independent source facts

`checks/check_eight_probe_obstruction.py` independently parses the original
exact-decimal gzip Matrix Market source, with its SHA256 pinned. It does not
import the previous support parser. A FIFO deletion of vertices whose current
off-diagonal degree is below8 reconstructs the8-core independently of the
saved minimum-degree-heap peeling order.

The resulting vertex set exactly equals the root's saved84-vertex set in
`results/eight_probe_core_preliminary.json`. In that induced subgraph:

- There are573 undirected off-diagonal edges.
- All84 diagonal entries belong to the original allowed pattern.
- Thus symmetric matrices supported entirely on this core form a vector
  space V of dimension573+84=657.
- Eight action vectors would supply84*8=672 raw coordinates on these rows,
  but those coordinates cannot be independent for symmetric operators.

Setting all entries outside this induced core, including all edges crossing
its boundary, to zero is permitted by the original support constraint.
Consequently any annihilator found in V extends to the full1074-dimensional
pattern without introducing forbidden nonzero entries.

## Rank theorem, with all dependencies explicit

Let X be an exact real m-by-q matrix of rank r. Consider the linear map

    Phi_X : Sym_m(R) -> R^(m by q),    D |-> D X.

Then

    rank(Phi_X) = m*r - r*(r-1)/2.

Proof. Choose an orthogonal row-coordinate matrix Q and an invertible
q-by-q column-coordinate matrix R so that

    Q^T X R = [[I_r,0],[0,0]].

Such matrices exist by choosing a basis of the column space and then reducing
the full-row-rank r-by-q coordinate matrix by invertible column operations.
The transformations `D -> Q^T D Q` on the domain and `Y -> Q^T Y R` on the
codomain are vector-space isomorphisms, so they preserve the linear-map rank.

Write the transformed symmetric matrix as

    D = [[C,K^T],[K,F]],  C=C^T, F=F^T.

Its action on the canonical X retains exactly C and K and discards F. The
retained C has r(r+1)/2 independent entries, while K has (m-r)r independent
entries. Every such C,K can occur. Thus the image dimension is

    r(r+1)/2+(m-r)r = m*r-r(r-1)/2.

This argument does not assume that the supported subspace V is preserved by
the coordinate transformation. It computes the image dimension of the FULL
symmetric space. The image of any restricted supported subspace is contained
in that full image, which is all the subsequent bound needs.

## Applied obstruction

Let X_core contain the core rows of any q<=8 full query directions, and let
r=rank(X_core)<=8. With m=84, the theorem gives

    rank(Phi_X on V) <= rank(Phi_X on Sym_84)
                       = 84*r-r*(r-1)/2 <= 644.

The last expression increases for r=0,...,8 and has value
84*8-28=644 at r=8. Rank-nullity on the657-dimensional space V therefore yields

    dim {D in V : D X_core=0} >= 657-644 = 13.

In particular there is always a nonzero symmetric D supported on the core
annihilating all eight query columns. Extending D by zero gives an allowed
nonzero full matrix with `D X_full=0`.

This holds for every choice of eight real directions, irrespective of their
rank or statistical distribution. A rank-deficient query block only makes
the upper image dimension smaller. The13 is a guaranteed lower bound on
the kernel dimension, not a claim that it always equals13.

## Identification consequence and quantifiers

The previous exact modular certificate proves injectivity for one fixed
nine-column query block consisting of already saved rational directions.
Once fixed as constants, that block identifies every real symmetric matrix
on the given support from its exact actions. The new lower bound proves
no eight-column block can be injective on this class. Therefore the minimum
number of exact matrix-vector actions for injective identification of this
known symmetric pattern is exactly9.

For a deterministic adaptive matvec-only algorithm using at most8 queries,
run it on an interior allowed matrix A and collect the directions it chose.
Choose a nonzero annihilator D of the resulting block. For sufficiently small
nonzero epsilon, A+epsilon D stays in any specified strict spectral interval
containing A and, if desired, keeps every initially nonzero allowed entry
nonzero. Every queried response is unchanged. By induction over the query
sequence, the deterministic algorithm chooses the same directions and sees
the same transcript on both matrices. It cannot identify both exactly.

This adaptive statement assumes the information model permits queries of
the operator through matvecs and known pattern data. It does not apply to an
algorithm additionally given all coefficient values of the input, as in the
actual fully stored NIST problem. It is a statement of information content,
not a requirement that practical code reconstruct the whole operator first.

There is no claimed approximate CDF lower bound, condition-number bound,
noise-robust identification theorem, or fixed-A/random-probe minimax theorem.
Small perturbations in a nontrivial annihilator space need not produce a
macroscopic eigenvalue-count ambiguity at a prescribed threshold. The exact
nine-direction upper result does not itself compute the nine exact actions,
or establish a faster total spectral calculation.

## Exact small tests and resource accounting

The independent script additionally forms the full symmetric-action map only
for five tiny rational fixtures, including rank-deficient query blocks and
r=0. Exact Fraction elimination verifies the rank formula for each. These
checks supplement the proof and do not replace it.

The script writes `results/eight_probe_obstruction_challenge.json`, containing
the source digest, exact84-vertex set, induced counts, all small fixture
results, and process resource measurements. Its body includes the independent
source parse, FIFO core reconstruction, receipt binding and small exact tests.
No precision or direction-count search occurred. Analytical reasoning and
authoring costs are additional and not fully metered. Observed complete script
body, including imports:0.048456051s wall,0.048455013s process CPU, peak RSS
17444864 bytes. The five small Fraction fixtures consumed0.005783346s within
that total. One documentation patch failed to match its expected text and was
repaired after reading the actual surrounding lines; no scientific calculation
or data changed during that authoring repair.
