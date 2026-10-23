# Independent receiving review: cut balance and the supplied strip operation

Reviewer: `/root/bounded_component_literature`, 22 October 2026 Brisbane.

## Verdict and scope

**PASS within the stated known-support, proper-coordinate-design contract.**
The cut-balance all-noise argument is valid. An independently written exact
checker reconstructed all supplied noisy and noiseless outputs, the explicit
cut and ramp witnesses, the double-star obstruction, and the same-graph ordinary
three-query comparator. It also received the new strip extension into its
99-vertex original-support action problem, including the stronger inherited
constant that remains available there.

This review does not settle four versus five queries for all degree-four
partial two-trees, establish historical novelty, validate an application
speed advantage, or certify a generic algorithm for the reduced coloring
problem. The arm and double-star supports have maximum degree 33.

The reviewer read the supplied JSON data and root `PROOF.md`, Sections 1–5.
Neither `src/cut_balance.py` nor either producer experiment was read or imported.
The checker uses Python's standard library, exact integers and `Fraction`.
Its decoder uses signed mean projection followed by leaf elimination, without
centroid or cut-vector code. Centroids and cut vectors are constructed separately
for the all-noise verification. No floating eigenvalue calculation is used.

## Pinned inputs and executable material

| Input | Bytes | SHA-256 |
|---|---:|---|
| `results/cut_balance_operations.json` | 178207 | `b613d5621d5d1122fd52c382603bfbfb8bde6d68cb77171f4a4f613d9ef02912` |
| `results/received_strip_operation.json` | 47466 | `7cfc8edd7e7f6de69fa56eb675e41cb7637a50ee52bb41a044b44f8bc42bc758` |
| `research/structure/RESULT.json` | 43519 | `b4bd6a41445802e840bc1c47ff0f623ebbde661d35f3a0a9e9e2c73d46804e82` |

The third input is used only to bind the receiving fixture's original/reduced
graphs and colors to the supplied structural output. No transition diagnostic
or earlier coloring experiment was replayed.

Run from the archive root:

```sh
python verification/check_cut_balance_independent.py
```

The default input paths are relative to the checker location, so relocation
does not require reproducing the author's filesystem. Every input hash is
checked before its claims are accepted. Output is
`verification/cut_balance_independent_result.json`; execution body records
append to `verification/cut_balance_independent_runs.jsonl`.

Checker identity at the successful execution: 34603 bytes, SHA-256
`8e77a4d54b43d5942a8b653b1e30e8321c14cec5a543a8344544d5ada61944d0`.
Result identity: 167578 bytes, SHA-256
`2df5bb597eff1e8ab1a5d6e3f01dc99a5740839827be31dc4ecaf6dd290cf74f`.

## Independent all-noise argument

Let a proper coordinate coloring be fixed. A bichromatic tree T has unsigned
incidence matrix B. Multiplying its rows by the two bipartition signs converts
B into an oriented incidence matrix. Its range is exactly the vectors whose
entries sum to zero. Mean projection is therefore the orthogonal projection
onto the action image for this channel. Eliminating a leaf with current signed
divergence f gives its edge coefficient as `sigma_leaf*f_leaf`; adding that
divergence to the neighbor and deleting the leaf repeats the exact inverse.
The last divergence is zero. This supplies the independently implemented
decoder, including inconsistent noisy observations.

For a centroid-rooted tree of order N, let a child subtree S have size a and
let `h=1_S-(a/N)1`. Summing the signed incidence equations over S proves that
the recovered edge error is the signed inner product of h with the signed
action noise. The checker compares these cut-map values to the errors from
the independent leaf decoder, entry by entry.

For children of one parent, the subtrees are disjoint. Their centered-cut
Gram is exactly

\[
G=\operatorname{diag}(a)-aa^T/N.
\]

The checker constructs each centered-cut vector as an integer numerator
`N*1_S-a`, takes direct integer dot products, and verifies every Gram entry.
For the component's maximum centroid branch size M,

\[
MI-G=\operatorname{diag}(M-a)+aa^T/N\succeq0.
\]

This is an explicit PSD decomposition: nonnegative diagonal entries plus a
positive multiple of one outer product. It proves the bound for arbitrary
real noise. It is not a solver status, a finite sample of noise vectors, or
a rounded spectral test.

Different color-pair components use disjoint observation cells, and none uses
a diagonal observation cell. Thus, if U stores edge errors oriented away from
the component centroids,

\[
\max_i\sum_j U_{ij}^2\le M\|E_{\rm off}\|_F^2.
\]

If each column has at most r0 incoming edges, then for every real z,

\[
\|U^Tz\|_2^2
\le r_0\sum_i z_i^2\sum_j U_{ij}^2
\le r_0M\|E_{\rm off}\|_F^2\|z\|_2^2.
\]

Consequently the symmetric off-diagonal error has operator norm at most
`2*sqrt(r0*M)*||E_off||F`. The diagonal error is bounded by `||E_diag||F`.
Their disjoint channels and Cauchy–Schwarz give the all-noise constant

\[
C^2=1+4r_0M.
\]

The decoder is the inverse on the action range followed by orthogonal
projection. Its Frobenius-to-operator norm therefore equals the fixed-design
inverse ratio rho. Any exact decoder, including a nonlinear one, must have
noise constant at least rho: use true matrix D and noise `-DX`, which produces
the same zero observation as the noiseless zero matrix. This reasoning relies
on the unrestricted linear symmetric-support class and is valid under it.

For a tree edge splitting a,b vertices, uniform signed divergences `1/a` and
`-1/b` give a unit cut edge and action norm squared `1/a+1/b`. Thus
`rho^2 >= ab/(a+b)`. At a centroid, every oriented child side is the smaller
side, and `Gamma <= M <= 2*Gamma`. Together with the diagonal lower bound,
this proves the claimed degree-free uniform-stability criterion for fixed q.
The constants supplied by the upper estimate are not asserted to be optimal.

## Actual exact receiving results

### 397-vertex arms

The actual graph has 33 arms of 12 edges, a unique degree-33 hub, 396 edges,
and the supplied proper two-color design. Direct graph reconstruction gives

\[
\Gamma=4620/397,\qquad M=12,\qquad r_0=1,\qquad C^2=49.
\]

All diagonal and edge outputs agree with the independent decoder. Exact
noise accounting is

\[
\|E\|_F^2=55448/10201,
\quad\|E_{\rm diag}\|_F^2=27766/10201,
\quad\|E_{\rm off}\|_F^2=27682/10201.
\]

The supplied error Frobenius norm squared is exactly
`59113654988/1607769409`. This observed output norm is not used in place of
the all-noise proof. The latter checks 1452 exact local Gram entries over
364 nonempty parent groups.

The cut witness has side sizes 12 and 385, a unit boundary edge, and action
norm squared `397/4620`. Its signed divergence is exactly constant on each
side with the prescribed reciprocal sizes.

The ramp lies on an actual 25-vertex path joining two arms. Its coefficients
are exactly `(-1)^(j-1)*min(j,25-j)`; all off-path entries and diagonals vanish.
Direct sparse action gives action norm squared 24 and matrix Frobenius norm
squared 2600. Thus its Frobenius inverse ratio squared is `325/3 > 49`, whereas
the same admitted design has the proved operator upper 49. This is a valid
separation of output norms; it does not assert a larger operator ratio for
this witness.

For the same graph's ordinary q3 comparator, all 364 bichromatic components
are stars. For every such component the checker verifies
`B^T B = I + 11^T`; 1452 exact incidence Gram entries are checked. Its edge
inverse has Euclidean norm at most one, and symmetric off-diagonal matrix
entries count twice. The resulting Frobenius and operator upper is
`C^2=2`. Saving one query therefore does not dominate conditioning.

### Double-star gluing failure

The graph has 66 vertices, two adjacent degree-33 hubs, and 32 leaves at each
hub. Its diameter is exactly three. The central coefficient is one and every
leaf coefficient is `-1/33`, with zero diagonal. All 132 action entries match
the independently multiplied result, and

\[
\|DX\|_F^2=2/33,
\qquad\Gamma=33/2,
\qquad\rho^2\ge33/2.
\]

The covariance verifier additionally checks 2113 exact Gram entries, giving
the proposed cut upper 133; the supplied inherited upper 66 remains stronger
for this particular graph. This supports the stated fixed-coordinate gluing
failure. It is neither a degree-four obstruction nor a universal real-design
obstruction.

### Full 99-vertex strip receiving operation

The graph and coloring bind exactly to the separately pinned structural
output. The original graph has 99 vertices and 194 edges, maximum degree
four, and q4. Its 90 bichromatic tree components have

\[
\Gamma=20/9,\qquad M=4,\qquad r_0=3,\qquad C_{\rm cut}^2=49.
\]

All noiseless and noisy outputs agree. The new covariance proof checks 262
Gram entries over 160 nonempty parent groups.

The stronger inherited row estimate is also independently certified. Around
any vertex of a bichromatic tree, the incident cut sides away from that
vertex partition the other N−1 vertices. If their sizes are a, then for every
sign vector epsilon,

\[
\left\|\sum_j\epsilon_j h_j\right\|_2^2
=N-1-(a^T\epsilon)^2/N\le N-1.
\]

The checker verifies the exact Gram underlying this identity for all incident
groups, with 596 Gram entries in 284 groups. Disjoint-channel Cauchy–Schwarz
and the maximum absolute row-sum bound give

\[
C_{\rm row}^2
=1+\max_v\sum_{T\ni v}(N_T-1)=20.
\]

Hence this receiving operation must retain 20 as its best supplied bound;
49 is valid but weaker here. Noise in unused cells is explicitly retained
in the total budget:

| Quantity | Exact squared value |
|---|---:|
| Total action noise | `27735/10201` |
| Diagonal channels | `6949/10201` |
| Used off-diagonal channels | `19846/10201` |
| Unused channels | `940/10201` |
| Output Frobenius error | `12828889/3672360` |

The supplied reduced graph has eight vertices and six edges, Gamma `1/2`.
Its own design is a Frobenius action isometry because every vertex's neighbor
colors are distinct. This explains its best constant one.

Removing all retained old edges from each final two-color graph leaves
components with at most one old vertex. The exact maximum attachment mass
per old vertex and color pair is A=7; the largest detached component has B=5.
The transfer lemma therefore gives

\[
\Gamma_{\rm final}\le
\max\{(1+7)/2,7,5/4\}=7,
\]

and the actual `20/9` satisfies it. This verifies this receiving use of the
extension. A generic reduced coloring solver is still absent.

## Failures and limits

The single checker execution passed; there were no failed executions or
numeric precision adjustments. The requested strip case was added before
the first execution. One read-only extraction of result counts and identities
followed the successful run; it did not rerun the checker.

The independent checker deliberately finds centroids by testing candidates
and materializes exact local cut vectors. It is a transparent finite verifier,
not the claimed linear-time production decoder. Its runtime should not be
used as a production complexity claim or as the cost of discovery. Resource
records and all exclusions are in `COSTS_CUT_BALANCE.md`.
