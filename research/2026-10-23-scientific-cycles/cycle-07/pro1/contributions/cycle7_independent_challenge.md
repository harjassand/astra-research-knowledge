# Independent challenge of the Cycle7 all-length prefix optimum

This is a bounded internal mathematical challenge of the new claim, not a
repeat of the inherited capacity audit or an external certification. I read
the actual Cycle6 endpoint/duality proof and the actual new files
`temporal_word_extension.md` and `symmetric_prefix_dual.md`. The argument
below was independently reconstructed before reading their completed notes.
No finite-check count is used as evidence for an all-length theorem.

## 1. Exact word reduction: accepted with its bulk scope

For an endpoint sector `01`, put `E=U_(i-1)...U_0`,
`M=U_(j-1)...U_(i+1)`, and `D=M* U_j M`. Involution cancellation gives

    C_j C_i = E* U_i D E,
    C_i C_j = E* D U_i E.

Work on the sufficiently deep coordinate core used in the inherited
coefficient proof. The physical finite-prefix representation then identifies
the same bulk coefficient at initial depth at least `k`. No extension of the
graded pieces through the root is needed or justified by this calculation.

A balanced matched Dyck factor transports its input colors to its matched
pop ports and leaves the bath identically unchanged. Its inverse on that
output sector has the same property. Such factors cancel in `M* U_j M`
even when the intervening bath differs; neither endpoint acts on their
ports. After these factors are removed, the middle is `0^d 1^e` in the
unmatched-stack normal form. If its unmatched push colors are `u_1,...,u_e`
and the endpoint color is `z`, the conjugation `D` shifts that queue and
inserts `w=u_1` (or `w=z` if `e=0`) at bath index `d`. Its unmatched pop
ports return to zero. This is an exact token identity, not a replacement of
amplitudes by a classical distribution.

The earlier prefix leaves a stack

    P=(a_h,...,a_1,B_m,B_(m+1),...),

where the `a` are its unmatched input pushes and the `B_0,...,B_(m-1)`
are stored in its unmatched pop ports. The two local orders are insertion
at index `d` followed by a top pop, or a top pop followed by that insertion.
For `d>0` their stacks differ only by exchanging `w` and `P_d`; for `d=0`
the same exchange occurs between the popped input wire and the top stack.
The reverse prefix removes precisely its first `h` stack colors and restores
the stored bath prefix. Therefore the cases are determined by `h>d`,
`h=d`, and `h<d`, exactly as claimed. No additional permutation of old bath
coordinates is hidden in the critical case.

The required initial bath coordinates fit inside the inherited finite
prefix: the original unmatched prefix pops use at most `i` coordinates,
and the middle uses at most `j-i-1` further coordinates. All remaining bath
coordinates and the seed are spectators on this core.

## 2. Arbitrary coherent prefix contractions: accepted

For `h>d`, both words restore the bath and their difference is an input
permutation times `I-SWAP` on two distinct input color wires. Its normalized
color square is exactly `2-2(1/2)=1` for every prefix density.

For `h=d`, one word restores the bath and the other exchanges one input
wire with the original coordinate `B_m`. Thus the difference is

    (P_input tensor I)(I-SWAP_(input,m)).

For any prefix density `zeta`, including complex coherences and entanglement
among coordinates, its contraction is `P_input(I-zeta_m)`. There is no
transpose in this convention: explicitly,

    Tr_B[(I tensor zeta)SWAP]_(a,c)
       = sum_b zeta_(b,c) delta_(a,b) = zeta_(a,c).

Spectator partial traces replace the full density by its reduced density
at `m`. Since `Tr zeta_m=1`, the normalized square is

    (1/2)Tr[(I-zeta_m)^2]
      = 1/4 + (1/2)Tr[(zeta_m-I/2)^2] >= 1/4.

For `h<d`, both words extract the same old bath color and insert the same
input color at different adjacent final positions. A contraction against
`|u><u|^tensor k` gives the same ket `|u>` at the extracted input location
and the same bra `<u|` on the exported color in both words. Every other
overlap is one. Hence the two contractions coincide for each complex unit
vector `u` before any averaging. The arbitrary-prefix square remains
nonnegative, but is not generally zero.

## 3. Simultaneous optimum and scalar certificate: accepted

The density

    zeta_sym = integral |u><u|^tensor k du = P_sym/(k+1)

has one-color marginals `I/2`, and so simultaneously attains all three
patternwise lower bounds `1,1/4,0`. Complete charge-pattern and distinct
endpoint-pair block orthogonality makes their squared norms add. This is
therefore a minimizer over **all** prefix densities; it is not an assumption
that symmetric densities suffice.

The new stronger gradient identity also follows. For `H=H_(zeta_sym)`,
the normalized input trace of `H* K` is `I` in the first case, `I/4` in the
critical case, and zero in the third. The adjoint orientations have the same
weight because total input charge is preserved. The input-diagonal part of
`G1` pairs to zero with `H`. Consequently

    T(sigma H)=v_k I

on the complete finite prefix, including all coherent vectors. This exact
matrix statement supports the full operator direction, rather than merely
its expectation in the optimizing density. The symmetric density is an
analytic dual witness; it is never the physical initializer.

## 4. Counting normalization and an immediate quadratic lower

Conditional input charge bits are fair under `sigma`. The oriented endpoint
event has probability `1/4`; the adjoint block doubles its equal weight.
The remaining prefix and middle walks are independent. Reversing the prefix
walk shows that its number of unmatched pushes has the law of a fair-walk
maximum `M_i`; the middle deficit has the law of an independent `M_r`.
Thus the factor and domain in the proposed formula are correct:

    v_k=(1/2) sum_(i,r>=0, i+r<=k-2)
           [Pr(M_i>M_r)+(1/4)Pr(M_i=M_r)].

Swapping `i` and `r` within this triangular domain gives

    v_k=k(k-1)/8-(1/8) sum_(i+r<=k-2)Pr(M_i=M_r).

In particular the collision probability is at most one termwise, so

    v_k >= k(k-1)/16 >= k^2/32,  k>=2.

This quadratic lower does not require the later exact generating-function
evaluation. The owner's closed-form convolution and nonlinear transfer
are separate obligations to be reviewed in their actual assembled source.

## 5. A counterexample to dropping the coherent-prefix correlations

It is insufficient to use only the statement that every one-color marginal
is maximally mixed. Consider `k=3`, charge word `001`, endpoints `i=0,j=2`.
Here `h=0<d=1`. With input color `z` and the first two original bath colors
`B_0,B_1`, the two raw maps, ignoring identical spectators, are

    (z;B_0,B_1) -> (B_0;z,B_1),
    (z;B_0,B_1) -> (B_0;B_1,z).

Against the independent maximally mixed prefix `I/4`, these contract to
`I/2` and `I/4` on the one color wire. Their difference is `I/4`, with
normalized squared norm `1/16`. Against `zeta_sym` the difference is zero.
Both densities have the same one-color marginals. Thus the deep-case
cancellation uses the specific repeated-color mixture, not just its marginal
data. With the endpoint-pattern weight, this contributes `1/64`, consistent
with the earlier exact `k=3` uniform-prefix excess `33/64-1/2`.

This example also shows why a single relative transposition does not imply
a universal positive bound on every endpoint pattern: which source wires
the transposition exchanges, and their final bath positions, matter.

## Status and costs

No surviving gap was found in the new token classification, arbitrary-prefix
contractions, simultaneous minimizer, scalar gradient or counting weights.
Acceptance is internal and mathematical; it does not establish historical
originality, external acceptance, a practical code compiler or physical
device performance. The actual root remainder, fixed-before-horizon block
choice, positivity and nonlinear exact drift remain necessary for a coding
claim and are not replaced by this variational result.

This review was analytic source reconstruction. No new finite-cutoff model,
long numerical sweep, paid resource, outreach or user administration was used.
Total inference, discovery and review costs are unknown.

## 6. Actual owner count and nonlinear transfer reviewed

I subsequently read the complete actual `COUNT_AND_TRANSFER.md`. Its exact
collision identity, closed finite expression, asymptotic coefficient and
unconditional transfer are accepted after the checks below.

The reflection identity `Pr(M_n=m)=p_n(m)+p_n(m+1)` includes `m=0` and
both lattice parities. The resolvent `sum_n p_n(m)z^n=r^m/D`, with
`D=sqrt(1-z^2)` and `r=(1-D)/z`, gives the collision generating function
`(1+r)/[(1-r)D^2]=1/[(1-z)D]`. Comparing coefficients proves the aggregate
return-probability formula. The finite sum follows from the two central
binomial recurrences displayed by the owner. Stirling's formula gives the
stated term `-k^(3/2)/(6 sqrt(2 pi))`, with the separate `-k/8` and a
remainder of order `sqrt(k)`. No distance-wise endpoint identity is used.

For `k>=2` and `b k^4<=2^-12`, the new quadratic lower `v>=k^2/32`
replaces the only use of the old `k>=4` guarded-word bound. Every other
norm estimate used by the owner holds for these smaller lengths as well.
The three relative drift-remainder terms are respectively bounded by
`3 delta`, `16 sqrt(32) delta`, and `12 delta`, where `delta=2^-12`;
their sum is below `1/2`. Their derivation contracts the physical remainder
only against `rho-sigma`, using the inherited exact zero drift of sigma.
Thus the actual operator drift, rather than its leading coefficient alone,
is negative. Also `kappa=(ln2)v b^2/16<=k`, as required by the inherited
coding theorem: use `v<=k^2` and the stated window. This small additional
hypothesis should remain explicit in the assembled proof.

The commuting relative density `Z` obeys `||Z||<1/2`; hence the input is
positive, normalized and charge preserving. The quadratic relative-entropy
term and its cubic remainder give exactly the displayed correction
`(9/8)b^2 v/k + ||Z||[8/3+(3/2)b^2v/k]`. It is below `1/2` in the same
window, so the same input supplies the claimed entropy excess and drift.

For `0<beta<=2^-8`, `k=floor(beta^(-1/2)/8)` is at least two and is at
least `beta^(-1/2)/16`; furthermore `beta^2 k^4<=2^-12`. Dividing the
entropy bound by `k` therefore yields the coefficient `ln(2)/16384` and
power `beta^(7/2)`. Both the actual density and the block length are fixed
before the coding horizon. The inherited coding theorem applies to the
exact drift with its finite root remainder. Its initializer-independent
code sequence remains pointwise for every fixed normal initializer; the
coherent-information equality is appropriately limited to the actual
initializer with its finite entropy/exponential moment.

The owner correctly retains the stronger existing finite-angle floor at
`beta=1/512`; the coarse new bound is not advertised as beating it there.
The operational gain established is the improved attainable asymptotic
power. The unrestricted capacity exponent, feedback equality, useful
blocklength and efficient encoder remain unproved.

This acceptance concerns the exact source hashes in the accompanying
receipt. The final assembled main proof remains a separate, focused
integration check rather than a new whole-programme audit.

## 7. Bounded integration of the assembled proof

I read the actual assembled `SHARP_TEMPORAL_GROWTH.tex`, the adapted
`INHERITED_OPERATOR_CODING.tex`, and the relevant inherited appendix
interface. The complete `INHERITED_COMPRESSION.tex` is byte-identical to
the verified Cycle6 predecessor. The following integration points were
checked against the previously reviewed scientific source:

* The endpoint orientation, zero-based indices, unmatched-stack counts,
  finite-prefix coordinate range and raw-word order agree. The new three-case
  classification is explicitly a bulk result; the older narrower whole-bath
  guard identity is kept separate.
* The explicit prefix minimizer, unique minimizing observable, scalar
  operator certificate and Pythagorean identity follow from the same
  patternwise traces. No uniqueness of the representing density is claimed.
* The exact collision sum is aggregate, with independent maxima even when
  their lengths agree. The parity-sensitive walk law and closed sum yield
  the stated asymptotic and all-length lower.
* The actual input and window are the reviewed ones. The formerly required
  `k>=4` is correctly replaced by `k>=2` using the new lower bound. The
  `beta<=2^-8` range, floor, explicit `kappa<=k`, positivity and exact drift
  all match. The density and temporal block are fixed before the horizon.
* The included coding theorem points to the new exact-drift equation, retains
  its finite root term, and has no low/high-depth cross terms. Its `C1--C12`
  references remain consistent. The full-diamond error and explicit half-
  diamond conversion are preserved, as are the initial-tail quantifier,
  `r^2` compression factor, auxiliary normalization and polar repair.
* The actual-initializer coherent-information limit is distinguished from
  the pointwise all-normal code guarantee. No fresh physical block channels,
  terminal return, physical preparation of the dual prefix, full capacity
  formula or efficient implementation is introduced.
* The stronger existing finite-angle comparator at `beta=1/512` is retained.
  The new asymptotic power is not represented as a finite-angle optimum.

No surviving mathematical integration gap was found. Two purely typographic
repairs were requested before freeze: the missing trace macro in the
Pythagorean display, and explicit parentheses around the rank-one projector
before its tensor power. Neither changes any constant, hypothesis or proof.
The accompanying receipt identifies the final source hashes inspected after
those repairs. This review does not certify PDF rendering, external priority,
later edits to other hashes, or receiving-party reading/integration.

### Final bibliography formatting verification

The final PDF layout edit adds only a small-font group around the bibliography
and local item/paragraph spacing. Removing those three formatting additions
reproduces the previously reviewed main-source SHA256 exactly. No scientific
text, mathematical formula, reference content or included source changed.
The receipt is updated to the final main-source hash. This is a byte-level
change-scope check, not a repeated scientific audit or PDF rendering review.
