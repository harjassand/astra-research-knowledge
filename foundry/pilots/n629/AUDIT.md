# N629 research audit

10 October 2026, Australia/Brisbane. Source revision
`90bd835a23d3ecdd8815b84ad2be8660389449b2`.

The development pilot passed its finite verification contract. No mathematical
counterexample or discrepancy was found in the checked domain. Two harness
failures were retained with their diagnoses and corrected without changing any
source assertion. The original card remains `source_derived_unreviewed`;
`G-CS-N629` remains open. The universal arguments below are internal
reconstructions conditional on an imported classical theorem. Originality is
unresolved. This pilot contains no independently certified new mathematical
result.

## Completed finite evidence

The final run is the `results/run-20261010-v4/` member of
`results/raw-execution-evidence.zip`; its compact machine summary is
`results/pilot_summary.json`. Raw commands, stdout, stderr, JSON, hashes,
interpreter details and resource receipts are preserved byte-for-byte in the
archive and checked by `results/raw-execution-evidence.manifest.json`.

All three original scripts completed unchanged. Their entire generated results
match the archived JSON except `seconds`:

- `fpt_sampler.py`: 80 small cases, 3,320 exhaustive prefix checks, 805 valid
  draws, complete small-case unranking images, and the exact `m=30,w=3` product
  count `1,142,827,901,003,938,843` using 125 terms.
- `verify_gate.py`: 101 jointly injective cases, 32 constructive witnesses,
  seven cover-restriction steps and 211,944 coupling triples.
- `exact_m5.py`: 47,905 dimension-four three-kernel families and 7,686,547
  dimension-five representative families. This is a reproduction of the source
  reduction/search, not a second independent dimension-five exhaustion.

The new reference uses only tuple images, explicit four-point spans and direct
pair enumeration. Its 1,039 exhaustive cases cover every kernel multiset for
`m<=3,w<=3`, including repetitions. There are exactly 1, 2, 5 and 16 distinct
kernels at dimensions 0, 1, 2 and 3. A map's admissibility depends only on its
kernel, so one row-basis representation per kernel suffices for this stated
finite coverage. Separate tests cover redundant rows and representation changes.

The 62 detailed named/seeded instances check 16,766 prefixes, all 5,573 ranks,
the exact `1/|C|` implied mass of every output, and 101,198 translated triples
with exact marginals and valid block patterns. Cases include no blocks, empty
ambient space, zero maps, rank-one maps, noninjective rank-two maps, repeated
rows/maps, inconsistent prefixes, `m<2w`, `m=2w`, and `m>2w`.
All comparisons passed. Synthetic wrong totals, wrong prefix counts and a
colliding unranking were all rejected. These injected faults are detector tests,
not defects in the original algorithm.

An additional 32 seeded jointly injective instances use `(m,w)=(6,5)` or `(7,6)`.
Each agrees with direct enumeration and has a good plane. This goes beyond the
source's exhaustive dimension-five scope but is only a selected finite sample;
it neither proves nor exhaustively checks the proposed sharper `m>w` statement.

## Resource results and interpretation

See `BENCHMARKS.md` for the final measured table and aggregate resource use.
All inputs, draws, proposal counts, process CPU/RSS and separate setup/draw
timers are machine-readable in the archived
`results/run-20261010-v4/benchmarks.json`. Three replicates request 16
outputs from each method. Setup is included. Module loading is included in
process receipts and excluded consistently from algorithm timers.

At fixed `w=2`, the FPT implementation avoids the rapidly growing brute-force
pair scan as `m` increases from 6 to 10. Rejection is faster than FPT on every
admitted sampling scenario in this run, including low-acceptance coordinate
examples. It does not supply an exact count. Thus no overall performance win
over rejection is demonstrated. At `m=30,w=3`, brute force is explicitly skipped
because `4^30=2^60` exceeds the `2^20` pair budget; FPT's count agrees with the
independent analytic disjoint-block formula, not a nonexistent exhaustive run.

Repeated identical blocks leave the count fixed at 211 and merge to five terms,
but construction still enumerates `5^w` choices: at `w=7` that is 78,125 choices.
This exposes avoidable practical redundancy in the source implementation and
illustrates the width dependence; it does not refute its FPT upper bound.
Measurements are local to one Apple M4 / 16 GiB macOS host and a simple Python
oracle. They establish neither universal asymptotics nor optimal constants.

## Arguments reconstructed in this audit

The following are human-readable internal reconstructions by the source-exposed
audit agent. No gap was found in these deductions conditional on the stated
classical cover theorem. They are not external or kernel-checked proofs.

**Cover/restriction.** Under joint injectivity and absence of a good plane, put
`K_i=ker L_i`. If they cover the space, a minimal subcover of size `k` bounds
the codimension of their intersection by `k-1`. Otherwise pick `x` outside
every kernel. Every other vector `y` lies in some `K_i+<x>`: failure of the plane
`<x,y>` forces one of `y,x+y` into a kernel. These enlarged spaces cover.
Their minimal subcover has common intersection `D` of codimension at most
`k-1`; intersecting its `k` kernel hyperplanes costs at most `k` more dimensions.
The resulting `H` has codimension at most `2k-1`. Delete these blocks and
restrict to `H`; joint injectivity and absence of good planes are preserved.
If none remain, `H=0`; otherwise induction bounds `dim H<=2(w-k)-1`.
Thus `m<=2w-1`. Zero maps/full kernels cause no exception: a full-space member
forms a one-element minimal cover.

The imported inequality is the linear-cover specialization of Brouwer's
1986 theorem: an irredundant cover of a binary vector space by `k` subspaces
has common intersection of codimension at most `k-1`. The theorem statement
and direction were checked visually on original p.315, not from a search
snippet. [Original primary PDF](https://ir.cwi.nl/pub/2507/2507D.pdf), downloaded
SHA-256 `7f8229a2150024fa0714df35cf963d2330b44c5dbf97cb09802193d7f19326f9`.
Its published proof is accepted as an imported premise, not independently
re-proved or formalized here. No withdrawn theorem is used.

**Incidence/counting.** With joint kernel zero, only `(0,0)` is an admissible
dependent pair, and each good plane has six ordered bases. Hence `|C|=1+6G`.
For `m>=d=2w>=2`, every `d`-subspace contains a good plane by the previous
argument applied to the restricted maps. Count plane/subspace incidences:
`G >= ((2^m-1)(2^m-2))/((2^d-1)(2^d-2)) >= 4^(m-d)`.
For `m<2w`, the zero pair suffices for the weaker bound. With common-kernel
dimension `h`, factor through the quotient; every quotient pair has `4^h`
lifts. This gives `|C|>=4^(m-2w)` for arbitrary maps. Handle `w=0` directly
(`C=V^2`), rather than inserting `d=0` in the incidence formula.

**Counting/unranking.** For one block, with `delta(x)=1[L_i x=0]`, the expression
`1-delta(u)-delta(v)-delta(u+v)+3 delta(u)delta(v)` is 1, 0, 1 at ranks 0, 1, 2.
The product expands into `5^w` signed linear-system counts. Prefix equations
are affine, so inconsistent systems contribute zero. Gaussian elimination
otherwise contributes `2^(2m-rank)`. Equivalent reduced row spaces can be
merged with coefficients added; cancellations are exact integers. At each bit,
partition completions into counts `N0,N1`; choosing a uniform rank and subtracting
`N0` in the second interval recursively identifies every valid leaf once.
This proves the abstract unranking distribution without frequency tests.

Review of the source elimination finds a consistent pivot invariant: homogeneous
rows have zero RHS; prefix rows carry RHS through every XOR; a zero row with
RHS one is inconsistent. Both rows and RHS are inserted at a new highest pivot.
The stored basis is not modified by `count`, and reduced homogeneous bases are
canonical for merging. This is a code review argument plus finite tests, not
a formal refinement proof for arbitrary Python inputs.

**Coupling/complexity.** Translation by fixed `u,v` preserves the uniform law;
the triple transformation is invertible, giving exactly `2^m|C|` equiprobable
latent triples and `KL=log(4^m/|C|)`. The `5^w` expansion, polynomial elimination
and `2m` prefix steps give the stated deterministic FPT work. The absolute sum
of coefficients is at most `7^w`, bounding accumulator bit lengths by O(m+w).
This includes integer costs, rather than treating exponentially large counts
as fixed-width machine numbers.

## Remaining obligations and boundaries

- The universal proof has an imported classical theorem and an internal
  reconstruction. Independent expert review or formal verification of the
  entire derivation and source-code refinement has not occurred.
- The deterministic `5^w poly(S)` bound is internally reconstructed; the
  unspecified polynomial factor, formal code complexity and arbitrary-size
  execution are not certified by these timings. The proposed streaming-memory
  variant is not implemented. Ideal unbiased bits are an explicit assumption;
  a seeded PRNG is not an exact randomness certificate.
- The stronger `m>w` threshold remains unresolved. Finite tests cannot close it.
- The sampler assumes supplied maps, basis, full binary support and uniform law.
  It returns a pair including diagonal mass; independent translation and any
  distinctness conditioning are caller operations. These are substantive
  restrictions compared with arbitrary set-family sunflower finding.
- Originality remains `UNKNOWN`. This pilot checks one imported premise and
  does not conduct a systematic prior-art search or establish historical priority.
  Existing source-worker agreement is source evidence, not another external review.

## Proposed next experiment: test the acquisition boundary

A consequential extension would acquire, from a sunflower-free transversal
family `F` of width `w`, a full injective binary-affine image contained in `F`,
with explicitly recoverable maps and at least `|F|/A^w` distinct rows for some
absolute constant `A`. If such a universal extraction theorem held, then
`|F| >= (4A)^w` would force extracted dimension at least `2w`, and N629 would
produce three distinct sunflower rows. An efficient extraction algorithm would
also turn the sampler's supplied representation into an acquired capability.
This is a new, strong structural obligation, not a consequence of N629.

Start with a small falsifiable development experiment: width two, four symbols
per block, with fixed binary labels. Enumerate all 65,536 families in the
16-row universe, identify sunflower-free ones by direct triple enumeration,
and enumerate all affine subspaces of F_2^4 to find the largest full additive
image contained in each. Report exact worst-case extraction loss, inclusion
certificates and the smallest defeating family for each tested loss bound.
Freeze the loss target before the search. Four-symbol permutations are affine
recodings of F_2^2, so this particular full affine-subspace search already covers
their relabelings. Larger alphabets require explicitly accounting for recodings.

Keep the first stage within 60 CPU seconds and 256 MiB; retain an unfinished
search as unfinished. A finite positive result would only motivate a structural
lemma. A negative certificate would rule out that precise acquisition interface,
not N629 or all generalization routes. Do not run this proposed experiment as
part of the present pilot or promote a gate from it without separate proof.
