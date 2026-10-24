# Comparator and source boundary for the quadratic-rank construction

24 October 2026. Bounded source/comparator audit for `FIRST_CONSTRUCTION.md`.
This is not a priority or correctness review.

## Finding

The archive’s exact N780 governing proof is a strong same-oracle incumbent on
its promised class, but it does not cover every bounded-joint-polar-rank
quadratic permutation. The candidate’s most consequential distinct step is
therefore the acquired *conditional-fibre sampler* for a prefix whose
quadratic forms share a low-codimension radical. The subsequent low-degree
recovery/self-correction is close to standard polynomial-learning machinery.
No strict advantage or novelty follows: on the N780 overlap, its decoder and
prefix sampler already give the same reusable capability, and ordinary
learning methods are strong post-label baselines.

## Exact N780 comparison

I read the exact governing source
[`COMPARISON_DECODER_THEOREM.txt`](../../../astra-capital/updates/FA/package/decoder_continuation/COMPARISON_DECODER_THEOREM.txt),
not only `frontier/dossiers/N780.txt`. Its theorem assumes exact chosen-pair
comparisons and a *complete hidden-affine triangular flag*: for an unknown
invertible affine input coordinate `u=Lx+c`, the significance-ordered bits
are `q_i(x)=u_i+g_i(u_1,...,u_(i-1))`, with supplied degree bound `d`.
Translation comparisons expose an exact coordinate label,
`1+C(x,x+v)=q_{j(v)}(x)`. A tournament finds the next significant
translation, polynomial interpolation learns that bit, and a response row
updates the flag. The proof gives expected comparison count
`D+6*binom(n,2)`, where `D=sum_{j=0}^d binom(n,j+1)`; for `d=2`, this is
`O(n^3)`. It compiles the exact inverse and any rank-prefix sampler with no
additional comparisons (proof lines 12–42, 46–108, 110–122).

Thus, for any target in the intersection of the candidate class and this
triangular class, N780 is already an equally informed comparison-only learner
with the desired decoder, inverse, and fibre-sampling outputs. It is stronger
than a baseline that only predicts pairwise answers. Its proof also states an
information lower bound `D` for its triangular subclass, so the candidate’s
quadratic query order cannot be presented as an improvement there.

The class boundary is explicit in the same proof. N780 says its complete-flag
criterion yields the triangular form, while an initial/partial flag is
insufficient (lines 124–143). Its example

```text
Q(x0,x1,x2,x3) = (x0 + x2*x3, x1 + x2*x3, x2, x3)
```

is a bijection with inverse
`x2=y3, x3=y4, x0=y1+y3*y4, x1=y2+y3*y4`. Its first two coordinate polar
forms coincide:
`B_1(x,v)=B_2(x,v)=x2*v3+x3*v2`, and `B_3=B_4=0`. Their common radical is
`{v:v2=v3=0}`, so the candidate’s joint polar codimension is exactly `2`.
Yet `q1` has nonzero polar form and cannot be made affine by any invertible
affine input change; N780 requires its first significance bit to be affine.
Reordering output bits is not allowed because it changes the comparison order.
This is a concrete member of the candidate’s bounded-rank class that is outside
N780’s theorem, not evidence that the candidate’s general theorem is proved.
For this example the candidate sampler is transparent: at prefix length one,
enumerate the four `(x2,x3)` cores and solve `x0=y+x2*x3`, with `x1` free;
each feasible core has the same number of solutions. At prefix length two,
solve both `x0,x1` and again obtain equal-size fibres.

The source card/dossier labels N780’s claims source-derived and unreviewed;
the proof itself leaves historical priority and external validation open. The
archive is an incumbent and a boundary witness here, not an independent
certification.

## Closest published methods and their oracle boundary

* Schapire and Sellie, [“Learning Sparse Multivariate Polynomials over a
  Field with Queries and Counterexamples”](https://doi.org/10.1006/jcss.1996.0017),
  *JCSS* 52(2), 201–213 (1996), give exact learning using membership and
  equivalence queries (with counterexamples), polynomial in the number of
  variables and number of monomials. Each dense degree-two Boolean coordinate
  has at most `1+n+binom(n,2)` monomials, so this is a strong conventional
  baseline *if labelled evaluations/equivalence feedback are available*. The
  candidate receives only comparisons of the unknown permutation; these
  polynomial-learning oracles are not supplied by that interface. Its median
  labels are randomized weak labels, not exact membership answers.

* Booth, Chevaleyre, Lang, Mengin and Sombattheera, [“Learning conditionally
  lexicographic preference relations”](https://doi.org/10.3233/978-1-60750-606-5-269),
  ECAI 2010, 269–274, study pairwise ordinal comparisons and learn LP-tree
  models with conditional importance/local preferences. Their alternatives
  have *visible binary attribute values*. In the present interface the
  attribute vector is the hidden `Q(x)` itself, with each bit a nonlinear
  function of the submitted object `x`; the LP-tree result does not furnish
  the hidden-coordinate or conditional-fibre acquisition step.

* Blum, Luby and Rubinfeld, [“Self-Testing/Correcting with Applications to
  Numerical Problems”](https://doi.org/10.1016/0022-0000(93)90044-W),
  *JCSS* 47(3), 549–595 (1993), and Rubinfeld and Sudan, [“Robust
  Characterizations of Polynomials with Applications to Program
  Testing”](https://doi.org/10.1137/S0097539793255151), *SIAM J. Comput.*
  25(2), 252–271 (1996), place polynomial identities and self-correction in
  an established framework. In degree two, the identity
  `xor_{S subset {a,b,c}} f(x+sum(S))=0` is exactly the vanishing third
  finite difference; hence recovering `f(x)` from the seven other vertices
  is a standard low-degree local-correction move once suitably accurate
  labels are available. These works do not give the candidate’s pairwise
  comparison-to-prefix-fibre sampler.

## Follow-up: Kane–Lovett–Moran–Zhang (FOCS 2017)

The primary paper [“Active Classification with Comparison Queries”](https://doi.org/10.1109/FOCS.2017.40)
(also [author-hosted PDF](https://www.ias.edu/sites/default/files/math/csdm/2017-2018/KaneLoMoZh2017.pdf))
is a closer framework-level comparator than visible-attribute preference
learning, but its theorem does not by itself subsume this comparator-only exact
acquisition task.

Their query model has **both** label queries and score-comparison queries:
for a concept `sign(f(x))`, the learner can ask `f(x)>=0?` and compare
`f(x1)>=f(x2)` (paper §I-B2, definition of inference dimension; Theorem I.5).
The inference-dimension bound reveals labels on a finite realizable sample
using `O(k log k log N)` label/comparison queries, with `k` the inference
dimension. Their concrete low-query results are for halfspaces and use
geometric/margin or input-bit-complexity conditions; the paper does not state
an inference-dimension bound for hidden quadratic Boolean permutations.

There is a useful exact reduction of the *comparison* part. After a prefix
`p=Q_1...Q_t` is known, let `F_p` be its fibre, `m=n-t`, and let `r_p(x)` be
the integer represented by the suffix bits `Q_{t+1...n}(x)`. For `x,y` in
`F_p`, the original oracle compares `r_p(x)` and `r_p(y)`. The next bit is
the sign of
`f_p(x)=r_p(x)-(2^(m-1)-1/2)`, so the same-prefix oracle supplies precisely
the pairwise score-comparison operation in their framework. But a label query
`sign(f_p(x))`, which is exactly `Q_{t+1}(x)`, is not supplied. The candidate’s
uniform-fibre median routine can simulate a *randomized, averaged-accuracy*
label query at a uniformly random fibre point; it does not establish exact
labels at arbitrary points, and Kane et al.’s cited theorem is not a theorem
for this noisy label simulator. In particular, its adaptive choice of labeled
sample points need not preserve the candidate’s uniform-point average-error
bound; no per-query or selected-point noise guarantee is currently available.

Accordingly, KLMZ is a potentially strong **conditional post-label
comparator**: if one proves a useful inference-dimension bound for the
candidate-induced suffix-score family, and handles the median-label noise,
their machinery might reduce the number of label acquisitions needed on each
sample. Those two steps are not in their halfspace theorem or in the current
candidate. Nor does their paper supply the prefix-fibre sampler, recover all
quadratic ANF coordinates, or establish exact whole-domain decoding from the
rank comparator alone. The candidate should therefore compare against this
route after its median label interface is formalized, but should not describe
KLMZ as already solving the task.

The closest methods therefore split the candidate’s pipeline: N780 is a
complete same-oracle solution on the affine-triangular subclass; polynomial
query learners and self-correctors handle labelled polynomial data under
their own oracles; preference learning handles visible attributes under
pairwise comparisons. In the bounded-rank non-triangular case, an equally
informed comparator should be allowed to retain the acquired prefix
polynomials and sampler, spend the same median comparisons, and then use any
standard robust/exact quadratic-learning procedure. The seven-point local
correction should be compared against such a baseline before it is treated as
algorithmically consequential.

## Remaining proof and comparison obligations

1. The first construction marks the median-label error bound as “to be
   proved/checked.” A precise finite-population/order-statistic bound is
   necessary before its `O(n^3 log(n/delta))` success claim is theorem-grade.
2. Establish independence of the repeated self-correction trials conditional
   on all acquired prefixes, including fresh sampler randomness and fresh
   medians; charge exact uniform sampling over a non-power-of-two number of
   feasible cores.
3. Compare post-label recovery to a conventional retaining learner given
   exactly the same weak labels, sampler, memory and query budget. N780 already
   ties on its class; outside it, the candidate’s valid claim is an extension
   to bijective degree-two permutations with an a-posteriori rank-dependent
   runtime, not superiority to general comparison learning.
4. Keep class recognition separate. Bijectivity and degree at most two remain
   supplied promises; computing `b(Q)` from acquired polars is not a certificate
   that an arbitrary comparison oracle satisfies those promises. The candidate
   explicitly disclaims exact recognition, which should remain a gate.

## Sources checked

* Internal exact governing source: `work/astra-capital/updates/FA/package/decoder_continuation/COMPARISON_DECODER_THEOREM.txt`, especially theorem/interface and proof §§1–4, the complete-flag boundary, and the source-status close (lines 1–16, 46–143, 210–221).
* Robert E. Schapire and Linda M. Sellie, JCSS 52(2), 201–213 (1996), DOI `10.1006/jcss.1996.0017`.
* Richard Booth et al., ECAI 2010, pp. 269–274, DOI `10.3233/978-1-60750-606-5-269`.
* Manuel Blum, Michael Luby and Ronitt Rubinfeld, JCSS 47(3), 549–595 (1993), DOI `10.1016/0022-0000(93)90044-W`.
* Ronitt Rubinfeld and Madhu Sudan, SIAM J. Comput. 25(2), 252–271 (1996), DOI `10.1137/S0097539793255151`.
* Daniel M. Kane, Shachar Lovett, Shay Moran and Jiapeng Zhang, FOCS 2017, DOI `10.1109/FOCS.2017.40`.

This was a focused primary-source check, not an exhaustive literature review.

## Owner scope update (24 October 2026)

The construction owner subsequently clarified that the draft need not be given
an upper bound `b`. After each learned prefix, it computes the common-polar
radical codimension `r_t` directly from the acquired polar matrices and
enumerates those `2^{r_t}` core values. Since `r_t` is nondecreasing and
`r_n=b(Q)`, this removes supplied `b` from the interface while retaining
comparison-query count polynomial in `n`; the sampler/field-work runtime is
`poly(n) 2^{b(Q)}` (with polynomial storage), hence can be exponential in
general. Earlier wording in this note that describes `b` as a supplied class
promise refers to the first draft and is superseded. Bijectivity and the
degree-two coordinate promise remain supplied; the algorithm does not
recognize them from comparisons. This update strengthens the N780-boundary
claim only at the interface level: the explicit `b(Q)=2` witness remains
outside N780, and no runtime advantage over general methods is established.

The KLMZ ruling above is therefore unchanged: its comparison operation maps
exactly within a learned prefix fibre, but the absent label oracle, unproved
suffix-score inference-dimension bound, and lack of a robustness theorem for
the median simulator prevent a direct comparator-only exact-acquisition
reduction. Treat it as a strong post-label/general baseline to test, not as a
published result that already subsumes the construction.
