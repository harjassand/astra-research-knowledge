# Decoder audit and precise later-wave delta
14 October 2026. Internal mathematical reconstruction and bounded executable checks.
Capital pin: ace0cfc4437fe91c20ccd24d69e0ee4bb335e871.
External correctness, historical priority, physical access and mission success UNKNOWN.

## Decision

The four core artifacts named in the user's request are byte-identical to the
already-published FA/N780 package. CORE_DEDUPLICATION.json records the four
SHA256 values. Reimporting that archive as a new result would be duplication.
The compact theorem is coherent under its complete triangular promise; I found
no universal proof gap. The valuable new intake is the later persistent_wave
work, which is absent from the original continuation ZIP and is not exhausted
by the earlier N780 recognition/repetition wrapper.

The selected original bundle is originals/MANIFEST.json: 81 files, 2,771,155
payload bytes. Every entry records its original absolute path, exact SHA256,
byte size, and bundle path. All copied bytes were checked against the original
again. Originals were not executed or modified; replay/ holds disposable copies
and newly regenerated receipts. The bundle deliberately excludes the old core
archive. It preserves original proofs, executables and imports, final controls,
necessary historical source snapshots for receipt pins, and scoped failures.
Embedded old missions are evidence, not current instructions.

## Base theorem reconstruction

For the supplied hidden-affine complete triangular order, translation v exposes
exactly its first changed hidden output coordinate, globally. The tournament's
fresh label match has probability one for equal exposed bits and one half for
distinct bits. Its priority comparison is exact, including harmless ties.
The winner span is complementary to the suffix subspace, so interpolation on
that span learns the prefix polynomial with exactly D coefficient labels.
The next suffix response is linear and the winner response is already one.
This yields exactly P response labels and at most 5P expected tournament labels,
hence D+6P expected comparisons, with the displayed capped bound and UNKNOWN
probability. Sequential inversion and uniform prefix sampling follow from
q_i(Vt)=t_i+h_(i-1)(t_<i), with exactly n-k free suffix seed bits.

The counting lower bound is valid: fixing the affine frame still leaves 2^D
distinct bijections and total orders. Binary-answer trees require D in the
worst case and on average under the uniform class for almost-sure exact Las
Vegas acquisition. The source correctly distinguishes erased capped output.
Leading ratio one is only fixed d>=2; the degree-one learner needs its stronger
affine comparator. Time, memory, source work and arbitrary noise are not covered
by query optimality.

One wording clarification should accompany any new notice. The source's bare
sentence that fixed d makes the capped query count O(n^(d+1)) needs a restriction
on beta. The exact formula is sound for every beta: D+(2T+2)P, with
T=ceil(log2(P/beta)). In general it is
O(n^(d+1)+n^2 log(n/beta)), and only simplifies under fixed beta or a suitable
growth bound on log(1/beta). This does not affect the proof or reported runs.

The submitted optimized producer executable triangular_compact.py specializes
to degree two. General-d correctness is a theorem and is supported by a
separate independent implementation, not an unadvertised general-d mode of
that file. I wrote a new independent implementation here; 25 fresh cases across
n=2..8 and d=1..4 pass all ranks, inverse targets and prefix target/free-seed
assignments. Those are finite implementation checks, not universal certification.

## Later robust learner: substantive new access contract

q_s09_robust_flag_implementation/PROOF.txt and its executable address a different
source port from the old independent-repeat wrapper. Supply an unknown quadratic
bijection, existence of h=n-r hidden translation toggles, and an unknown FIXED
bad-item set of density epsilon<1/16. The original directed comparator is exact
when both items are clean and may be arbitrary, persistent, nontransitive and
non-antisymmetric on incident pairs. Coefficients, ranks, labels, B, directions
and conditional samplers are acquired; degree, flag existence, epsilon and
chosen-input access remain supplied. r is fixed for polynomial-cost claims.

I read the main learner, shared shifted-ball decoder, source harness, exact
Compiler algebra, matching proof and sequential-validation argument. The actual
acquire interface receives only scalar comparisons and parameters. Test-only
truth is used after return. A genuine own-toggle gives raw labels with global
error at most 2epsilon. Descending finite-difference coefficient majorities
recover a whole degree-d body when raw error rho<2^(-d-1). Its shared rounds
are justified by defining reference votes using true higher coefficients and
union-bounding their failures before induction, rather than conditioning on
correlated earlier coefficient success. The coding mechanism is classical
Reed majority logic; it is not a new coding theorem.

Every proposed quadratic must have its exact own-toggle. The fresh validator
uses greedy maximal inversion matching between two balanced candidate halves.
True candidates have mean score <=2epsilon; wrong degree-two candidates have
mean >=1/4-2epsilon-c_m. Maximality really suffices: if matching size were below
both clean-wrong population counts, an unmatched complete-biclique edge would
remain. Fresh batches, rather than repeated fixed oracle responses, supply
independence. The fractional-score likelihood ratio is a valid supermartingale
by endpoint convexity; its finite KL fallback separately charges the remaining
error. First-wrong-acceptance budgets avoid assuming correctness after a mistake.

The suffix threshold counts directed predecessors only inside the learned
2^r-point fiber. With b bad items, at most b clean items plus b bad items are
mislabelled, hence global error <=2epsilon, including asymmetric incident
answers. Fresh coefficient decoding completes the tail. The full return is
Monte Carlo, with wrong-or-UNKNOWN probability bounded by beta under supplied
promises; it does not preserve the old theorem's zero semantic error on every
completed run. A user compute stop returns UNKNOWN and may reduce availability.

For M=1+n+binom(n,2), body and tail repetitions Rbody,Rtail, matching batch
parameters T,m, candidate cap Rcap, and S_r=2^(r+1)-r-2, the source charges
 Qmax <= h Rcap (M Rbody+T m^2) + M Rtail S_r,
 E Q <= h(2/p+beta/4)(M Rbody+T m^2)+M Rtail S_r,
 p=2^(-r-1).
At fixed r and a fixed strict noise gap, this concrete shifted-ball method has
O(n^3 log n) expected comparisons. Its cited NIS composition has the stronger
O(n^3) theoretical query claim but was not implemented as that coding family.
The method uses O(R(M+n)) logical retained bits, scans O(M^2) term pairs during
preprocessing, and charges all projections, directions, body samples, tail
enumeration, caches, source setup, source rank work, transmission and checking.
The parameter search and sequential thresholds use Python floating arithmetic;
this is not exact-real or formally verified confidence implementation.

An older canonicalized C* receipt is preserved and remains restricted evidence.
The primary original-directed experiment never infers C(y,x) by complementing
C(x,y). Fixed-B persistence and fresh sampling must not be confused with fresh
iid response noise, a marginal pair error rate, or adaptive drifting faults.

I reran the original-directed n16/r2/epsilon1/32/beta.05 fixture in scratch:
2,796,822 logical requests, 2,796,630 external calls, 35 decoded bodies and
27,857 validation batches. Acquisition was 6.9726 seconds on this host. After
return, all 65,536 ranks and sampler points, all coordinate coefficients, the
planted partial flag and 64 inverse targets passed; zero new source comparisons
were made during checks. The separate source exact distinct-pair receipt says
2,360,723 pairs; I did not rerun the disk-logging distinct-pair audit.

CURRENT_FRONTIER says strong RM controls were still being compared. The actual
retained q_l15 final controls are later/more complete evidence. They use the
same original directed source and promises, 250,000-entry ordered cache, initial
seeds and surrounding learner, but decoders change subsequent random paths.
Source reported logical calls / external calls / distinct pairs / seconds:
 shifted-ball: 2,796,822 / 2,796,630 / 2,360,723 / 6.700;
 full-cube RM: 4,410,123 / 4,409,984 / 3,860,253 / 14.559;
 local-cube RM: 4,613,734 / 4,613,509 / 4,164,005 / 82.108.
All passed the same post-return checks. I also reran full-cube n16 in scratch,
matching 4,410,123 logical and 4,409,984 external calls, at 15.5467 seconds.
The local-cube full learner and distinct-pair audits retain producer-reported
status. This is one seeded finite method replacement per method, not a success
rate, strongest-known universal advantage, asymptotic separation, or a service.
Matching itself dominates the shifted-ball run: 2,526,705 of its requests.

## Later fixed-degree witness compiler and guards

p_s01c_witness_compiler/PROOF.txt provides a self-contained main construction
for exact comparisons and a bounded-degree hidden partial prefix flag. At a
true stage S, the constant-derivative space C is linear; remaining flags lie
inside it. A nonconstant second derivative is a low-degree nonzero quotient
function, so global random witnesses detect it with a quantified lower weight.
Its fixed witness function has low quotient codimension. Testing periods and
taking their exact GF2 kernel progressively acquires C, after which only a
<=k+r-dimensional complement needs interpolation. Derivative-degree filtration
then computes the candidate's full exact constant/period spaces algebraically.

This is a genuine relaxation of the complete-flag theorem, with full output
only if EVERY output coordinate has the stated degree. An arbitrary suffix
allows only prefix acquisition/sampling. Its stated prefix count is
A_(d,m)+O(n^2), A_(d,m)=sum_(k<m) M_d(k+r), for fixed d,r and polynomially small
beta. Full output separately pays M_d(n)(2^r-1). This does not close total bit
cost, naive raw ANF expansion, known-period/generalized-junta prior comparisons,
or physical acquisition. Witness gains are mixed, including losses to preserved
original controls. Source truth remains isolated from acquire.

The most important resource correction is persistent PRE-SPEND accounting.
Correct stages consume total stabilizer defect <=r, but a wrong semantic step
can refund measured defect. The executable checks both cumulative global_drop
and paid_dictionaries BEFORE a new period dictionary, and separately caps global
outer epochs. Geometric guards do not certify semantic correctness. I read the
critical code at witness_compiler.py lines 150-225 and reran the adversarial
forced-refund fixture. Three paid dictionaries produced wrong geometric models
with zero measured defect; the fourth was blocked before dictionary payment.
It made 3,132 comparisons, under conditional cap29,733 and whole cap521,833,
with seven outer epochs. The deliberately forced tape is a possible finite
path, not an empirical failure frequency or an ideal-entropy test.

I reran the cubic n8/r3 complete learner and its common-selector controls:
witness8,840; safe-W8,622; raw-body7,586 comparisons. All exact coefficient
bodies, exhaustive 256 ranks, samplers and bounded inverse execution passed.
This explicit loss should be retained next to the asymptotic construction.
Larger stored cubic cases and the arbitrary-suffix n32 prefix remain reported
source evidence in this audit. No full robust fixed-degree compiler run is
inferred from the separate GENERAL_DEGREE.txt NIS construction.

## Degree-promised validation: a useful different gate

The later promise_recognition/PROOF.txt sections8-9 remove supplied r for SOUND
adaptive model selection while retaining TRUE degree and exact comparator
promises. This is different from exact arbitrary-oracle class recognition.
For a locally degree/toggle-certified candidate prefix p, choose a stage
uniformly, a uniform earlier p-prefix, and independently sample its next-bit
halves. If p is wrong, take its FIRST globally different bit. Earlier bits are
true, both next cuts are balanced, and a nonzero degree-d difference has global
mass >=2^-d. Both opposite mismatch halves have that conditional mass, so
Jensen gives rejection probability >=4^-d/h. A true prefix always passes.
O(h4^d log(1/eta)) exact comparisons validate model equality under TRUE degree,
without supplying true r or true flags. Conditional on correct prefix, a tail
sample enumerates its 2^r-point candidate fiber and detects wrong degree-d tails
with probability >=2^-d. Candidate global bijectivity is unnecessary there.

Fresh summable validation budgets can therefore screen generators at guessed
r=0,1,... soundly; all generator caps and repeated leading work remain charged.
The per-guess algebraic model checks do not certify source degree. Off-degree
adjacent needles can pass this validator almost surely at its nominal small-d
budget. The retained off-promise n8 example has true per-probe detection1/98304,
passes440 probes, and has miss probability0.995534 despite nominal eta0.01.
The source exact-recognition exponential barrier and this positive validator
are consistent because they have different remaining assumptions.

I reconstructed the section8 argument and wrote a separate finite checker.
All40,320 three-bit permutations, all of whose coordinate bits have degree<=2,
satisfy it for candidate identity prefixes of lengths1,2,3. Minimum wrong-model
rejection probabilities are exactly1/16,1/32,1/48, attaining4^-d/h. This checks
the probe and sharp fixtures, not arbitrary source degree acquisition.

## Independent and replay evidence

independent_checks.py / independent_results.json:
 25 newly generated compact cases, all ranks/inverses/prefix seeds;
 32,768 exact population coefficient-decoder cases, exhausting all four-bit
 quadratic bodies and singleton error positions at density1/16;
 131,072 arbitrary directed incident-answer cases for one bad item in an
 eight-point fiber, verifying the2b threshold lemma and attaining two errors.
degree_validator_check.py / degree_validator_results.json:
 all40,320 three-bit orders and three candidate-prefix lengths, bounds sharp.
replay/q_s09_robust_flag_implementation/decoder_and_caps_receipt.json:
 56 component cases; zero-direction UNKNOWN before any source call; forced
 operational request cap returns UNKNOWN at exactly10calls.
replay/q_l13_derivative_decoder_audit/coefficient_decoder_audit.json:
529 error supports,128 singleton-B directed comparison assignments,64 explicitly
non-antisymmetric cases, and a strict-radius tie witness; source script replay.
replay/p_l01_flag_exposure/witness_full_audit/forced_refund_cap.json:
 possible semantic-miss tape, guard and call accounting above; source script replay.
replay/p_s01c_witness_compiler/receipt_n8_r3_d3_seed940083.json:
 cubic whole learner plus matched controls; source script replay.

All successful checks are internal finite/replay evidence. New scientific
correctness, external validation and priority are not implied by script exit0.
No capital or producer source, commit, publication or memory was changed by this reviewer.
Scratch code/receipts and this report were created only in work/decoder_audit.

## Publication and handoff recommendation

Append a scoped N780 semantic notice and new checkpoint pointing to this exact
later-source bundle, current audit and receipts. Preserve the original N780 card
and archive bytes. Describe the new robust fixed-B partial-flag port separately
from the old exact-complete and conditional-iid-repetition contracts. Original
source claims stay source_derived_unreviewed. Core byte identity and later-wave
chronology should be explicit. Do not import other persistent-wave lanes or
represent whole producer reports as independently reviewed.

Useful proof anchors within originals/:
 q_s09.../PROOF.txt1-192: full robust contract, decoder, validation, caps and cost;
 p_s02b.../PROOF.txt1-223: matching, rank lemma and sharp robustness obstruction;
 p_s02b.../GENERAL_DEGREE.txt1-148: theoretical fixed-degree extension/unexecuted NIS;
 p_s01c.../PROOF.txt5-26: prefix versus full-output contract;
 p_s01c.../PROOF.txt27-122: witness geometry, interpolation and all-history guards;
 p_s01c.../PROOF.txt123-209: raw selection, failure allocations and charged costs;
 p_s01c.../promise_recognition/PROOF.txt227-328: degree-promised validation/unknown-r;
 q_l15.../RESULT.md: final matched finite controls and exact interface limits.
Use actual file line counts when making final proof-range records; the manifest
is the byte authority, while these anchors are navigation.

The most consequential remaining gate is still a real chosen-input service
whose degree/flag/noise promises can be independently justified, followed by
strong same-interface total-resource controls and specialist proof/priority
review. The later work closes meaningful restricted execution/validation gates;
it does not establish an acquired physical/computational application or a
civilization-enabling breakthrough. No architectural expansion is needed to
justify this scoped addition.

## Reproduction

The original Python files use paths relative to their own directory and the
retained sibling-role layout. Copy the entire `originals/` tree to a separate
scratch directory before running its harnesses; several harnesses overwrite
their role-local receipt filename. Never run them inside the immutable original
bundle. No install is needed; these replays use the Python standard library.

With the copied tree at `work/decoder-replay`, examples from a checkout root are:

```sh
python3 -B work/decoder-replay/q_s09_robust_flag_implementation/run_experiment.py --n 16 --r 2 --seed 960162 --epsilon 0.03125 --beta 0.05 --mode asymmetric_hash --bad-count 2048 --original-directed --output independent_replay_n16.json
python3 -B work/decoder-replay/q_s09_robust_flag_implementation/check_decoder_and_caps.py
python3 -B work/decoder-replay/q_l15_robust_flag_controls/rm_controls.py --case full-cube --n 16 --r 2 --seed 960162 --epsilon 0.03125 --beta 0.05 --mode asymmetric_hash --bad-count 2048
python3 -B work/decoder-replay/p_s01c_witness_compiler/run_witness.py --case 8:3:3:940083
python3 -B work/decoder-replay/p_l01_flag_exposure/witness_full_audit/forced_refund_cap.py
```

The two fresh audit scripts `independent_checks.py` and
`degree_validator_check.py` import no producer code. Copy them to a writable
audit directory and run each with `python3 -B`; each writes its receipt beside
itself. Original absolute source paths appear only in the provenance manifest,
not as operational dependencies of these scripts. The primary-access and
capital-read ledgers are `PRIMARY_ACCESS.json` and `CAPITAL_READS.json`.
