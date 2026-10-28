# Affine row-prefix sampler: focused prior-art and comparison check

2026-10-28. This note concerns the new code
`../affine_sampler/affine_slice_prefix_sampler.py` and the independent argument
`../independent_audit/ROW_PREFIX_CHARACTER_INDEPENDENT_AUDIT.tex`, both read
in full for this check. It is a focused literature/implementation comparison,
not an exhaustive novelty search or a second execution audit.

## The precise operation now acquired

The literal-coordinate problem is to count and sample pairs
X in Fq^(p×d), Y in Fq^(d×r) with XY=Z, where Y belongs to an arbitrary binary
affine slice of actual codimension c, q=2^a. The new conditional-count family
fixes complete acquired rows of Y and a binary prefix of its next row.

The existing signed universal product-fiber evaluator is reused. Complete
fixed rows are absorbed into a quotient by their span. For a partially fixed
row, the rank-dependent summand is constant on three nested-space strata.
Their signed masses are obtained by three binary linear solves. Consequently
the outer enumeration stays at 2^c original characters; it does not grow to
2^(c+number of prefix bits).

Exact prefix completion counts then select Y with probability proportional
to its number of X-completions. Uniform affine solves select X. The checked
coordinate bijection transfers the resulting uniformity to original inputs.
The native wrapper enforces 2^c <= compact circuit-description bytes.
Unrestricted c retains exponential dependence. The proved conditioning
family is acquired Y-row prefixes, translated when needed into original
affine equations; it is not arbitrary original-bit conditioning.

## Closest primary mathematical techniques

### 1. Additive characters and rank-metric duality

Alberto Ravagnani, *Duality of Codes Supported on Regular Lattices, with an
Application to Enumerative Combinatorics*:
https://arxiv.org/pdf/1510.02383 .

This is a close conceptual antecedent. Theorem 7 states the character-group
MacWilliams transform; Example 26 treats chain supports, and Corollary 31
gives the Fourier-reflexive stratum partition for a subgroup chain.
Example 39 and
Section 8 specialize to matrix rank. Theorem 55 and Corollaries 56–59 compute
rank-restricted matrix counts under certain linear constraints by switching
to an annihilator whose rank distribution can be evaluated. The paper also
explicitly uses finite abelian groups, which is relevant when a slice is only
binary-linear inside a larger finite field.

Alberto Ravagnani, *Rank-metric codes and their duality theory*:
https://arxiv.org/pdf/1410.1333 .

Theorem 31 gives q-binomial moment identities, and Corollary 33 inverts them
recursively. Appendix A relates these formulas to Delsarte's original
rank-metric MacWilliams transform. Thus neither Fourier reduction to the
dual nor the rank-transform kernel should be presented as a new principle.

**What is an additional argument here:** these results do not, merely by
being cited, supply the implemented matrix-product row-prefix evaluator.
The code's proof must still establish the quotient product equation, its
multiplicity, the surviving frequency condition, and the partial-row
three-stratum formula. The independent audit supplies those explicit steps.

### 2. The three-mass collapse is elementary Fourier linear algebra

Using the audit's notation, K ⊆ L ⊆ E. Write f0,f1,f2 for the three
universal fiber scalars. The relevant function of the new frequency row w is

    g(w) = (f0-f1) 1_K(w) + (f1-f2) 1_L(w) + f2 1_E(w).

This is a linear combination of three subspace indicators. Its signed sum
over an affine frequency slice is therefore the same combination of three
affine-subspace character sums. For a nonempty solution coset lambda0+V,

    sum_(lambda in lambda0+V) (-1)^(lambda·b)
       = 0                         if b is nonzero on V,
       = (-1)^(lambda0·b) 2^dim(V)  otherwise.

This identity follows immediately by pairing terms under a translation in
V. It requires only an affine solve and a character-triviality check. The
rank changes (0,0), (1,0), (1,1) follow from appending one row and applying a
fixed linear map to that row. These individual facts are standard; no
standalone priority claim is justified for them.

The meaningful gain within P3 is proving that **all needed sampler prefixes
have this form**, with the original character count unchanged, then actually
connecting the evaluator to acquired matrix/field coordinates and the
original-input reconstruction. An appeal to general count-to-sampling
self-reduction without this closure argument would have left the hard step
unresolved.

### 3. Quotienting, puncturing and affine translates

Eimear Byrne and Alberto Ravagnani, *Covering Radius of Matrix Codes Endowed
with the Rank Metric*:
https://researchrepository.ucd.ie/rest/bitstreams/26355/retrieve .

Section 3 defines matrix-code puncturing and shortening; Theorem 12 proves
their trace-duality relation. Section 4 analyzes translates and uses
projections with affine fibers; Lemma 16 and Theorem 20 make precise
assumptions when deriving coset rank distributions. These are close
established tools for the code's quotient/fiber reasoning. The paper does
not itself claim this arbitrary binary-affine matrix-product sampler, and
its Fq-linearity assumptions must not be silently substituted for binary
linearity.

### 4. Uniform generation from completion counts

Jerrum, Valiant and Vazirani, *Random generation of combinatorial structures
from a uniform distribution*, Theoretical Computer Science 43 (1986),
169–188:
https://www2.stat.duke.edu/~scs/Courses/Stat376/Papers/ConvergeRates/RandomizedAlgs/JerrumValiantVaziraniTCS1986.pdf .

The count/generation connection is classical. Section 2 also explains the
random-bit issue when exact branch probabilities are non-dyadic. Choosing
branches by exact completion-count ratios and telescoping their
probabilities is not a new sampling paradigm. The present implementation's
expected polynomial bound for exact random-interval draws is the appropriate
qualification; it does not claim a bounded worst-case number of fair bits.

### 5. Earlier matrix-product enumeration

Wei and Zheng, *The number of solutions to the bilinear matrix equation over
a finite field*, Journal of Statistical Planning and Inference 94 (2001),
359–369, DOI https://doi.org/10.1016/S0378-3758(00)00266-4 .

The primary publisher's indexed abstract describes counts for XAY^T=B,
including prescribed factor ranks, and a correction to Hodges's 1964 count.
Full text was not acquired in this focused check. This establishes nearby
historical work, not that the new constrained sampler already appears there.

## Existing implementations and limitations

**KUS** already implements exact uniform sampling after d-DNNF compilation.
Its primary paper's Theorem 1 proves uniformity by child model counts and
decomposability:
https://www.cs.toronto.edu/~meel/Papers/lpar18.pdf .
Official code: https://github.com/meelgroup/KUS .

**decdnnf_rs** provides conditioned model counting, direct access and uniform
sampling. Its 2026 paper, Section 3, gives the direct-access descent and
count-weighted structural traversal:
https://drops.dagstuhl.de/storage/00lipics/lipics-vol377-sat2026/LIPIcs.SAT.2026.38/LIPIcs.SAT.2026.38.pdf .
Official code: https://github.com/crillab/decdnnf_rs .
Neither tool makes compilation free; the point of comparison is acquiring
and querying the representation on the same original circuit.

**SageMath 10.8's rank-metric module** is a useful implementation reference for
field-basis conversions and rank support, but its documentation explicitly
restricts this module to codes linear over the larger extension field and
says codes merely linear over the smaller field are not supported there.
It does not advertise this constrained factor-pair sampler:
https://doc.sagemath.org/html/en/reference/coding/sage/coding/linear_rank_metric.html .
This is a statement about that module, not a claim that Sage cannot express
the problem using generic matrices and linear algebra.

## Recommended claim and baseline wording

Suggested mathematical wording:

> We completed a constructive extension of the acquired matrix-product
> counter. Arbitrary binary affine slices of codimension c now admit exact
> acquired-row-prefix counts, witnesses and uniform original-input sampling
> in 2^c times polynomial expected time, without an exponential factor in the
> growing prefix. The native admitted family has 2^c bounded by its explicit
> circuit-description length. The construction uses classical character
> orthogonality, rank-metric transforms, linear fibers and count-based
> generation; the specific prefix-closure argument and its integration are
> proved and implemented here. Historical priority is not established.

The existing baseline report is appropriately narrow. In subsequent reports:

- Say **two specified exact counters timed out on the unique-extension CNF
  of one saved circuit**, and **a separate d4 decision-DNNF compilation
  attempt timed out before reaching sampling**. The first two commands
  were d4 `-mc` and SharpSAT-TD. The third used d4 `-dDNNF` with the measured
  export time charged inside its 120-second total budget; its output file
  was empty and invalid. Do not say two compilers or all ordinary
  compilation routes failed.
- Retain the concrete 72-input / 24,676-gate fixture and its hash. This is a
  constructed algebraic fixture with reversible disguise, not a broad
  application benchmark or all other 72-input examples from the transcript.
- Charge native acquisition, coordinate manufacturing, sampler preprocessing,
  count, and the requested number of samples on the new route. Keep one-time
  software download/build costs separate on both sides. The old baseline
  export time is already included in its per-instance totals.
- The first two ordinary tests measured **counting**. The third attempted
  the compilation needed by the identified count/witness/uniform-sampling
  pipeline. A completed new count can be compared to the counting timeouts,
  and a completed new sampling pipeline can be compared to the ordinary
  pipeline not reaching its sampling stage within the compilation budget.
  No ordinary sampling runtime or sampling-speed ratio was measured; the
  downstream decdnnf_rs stage was not invoked. These results also do not
  measure ordinary SAT witness search.
- A timeout supplies a lower bound on the completion time under those exact
  settings, not a measured runtime ratio. SharpSAT-TD was still preprocessing;
  this is not evidence that its counting search itself needs 120 seconds.
- Keep the 120-second budget, pinned commits, parameters, memory policy and
  shared research environment visible. No alternative XOR-aware encoding,
  d4v2 native circuit mode, BDD route or solver parameter portfolio was
  exhaustively benchmarked. This limits the comparative claim, while the
  proved prefix-closure result stands independently of that experiment.

The specific missing operation removed is the exponential growth of naive
prefix Fourier conditioning, together with the previous rejection-sampling
failure. The dependence on original c and the native recognizer's hypotheses
remain. This search found close classical ingredients; it does not establish
that no earlier paper or implementation combines them in the same way.
