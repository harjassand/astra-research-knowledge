# Comparison decoder continuation: independent intake review

13 October 2026. Capital baseline independently checked as
`097d135f76ebefc49a8e5f28a8363e9ae372c061`. The current user request governs;
embedded worker missions and older instructions are source data. No capital,
Git state, original submission or memory file was changed by this reviewer.

The complete triangular decoder theorem is coherent under its supplied promise.
I independently reconstructed its main invariants, exactness, inverse/fiber
operation and comparison accounting, and wrote a fresh implementation which
passed twelve exhaustive small cases. The strongest new intake consequence is
an exponential exact class-recognition obstruction, now fully proved and
independently criticized. Promised acquisition can be cheap while certifying
that promise from arbitrary comparison access is exponentially expensive.
No novelty, practical acquired advantage or civilization-level breakthrough is
established by this review.

## Exact submitted operation and proof review

Input: `n>=2`, `1<=d<=n`, exact chosen-pair comparator of a permutation rank
`Q(x)=(q_1,...,q_n)` on `F_2^n`, and the complete hidden-affine triangular promise
`u=Lx+c`, `q_i=u_i+g_i(u_1,...,u_(i-1))`, `deg(g_i)<=d`. The significance order is
actual most-significant rank-bit order. The affine input encoding, coordinate
labels, target rank code, toggle directions and prefix samplers are not supplied.
The learner obtains a compact winner basis `V` plus prefix coefficient lists.
The promise and repeatable exact chosen-input access ARE supplied.

The following proof steps were reconstructed independently from the theorem.

1. If the first nonzero coordinate of `Lv` is `j`, translation by `v` leaves all
   earlier hidden inputs and rank bits fixed, and flips actual `q_j`. Therefore
   `1 xor C(x,x+v)=q_j(x)` globally. This is the special algebraic property;
   it fails for arbitrary polynomial permutations or partial flags.
2. The suffix subspace `S_k` preserves the first `k` hidden inputs. A basis
   exposes no bit earlier than `k+1`, and at least one vector exposes that bit.
   For distinct exposed bits the labels on a fresh uniform raw input are jointly
   uniform because the full rank map is bijective. A label match has probability
   `1/2`; same-bit candidates match surely. After a match one additional
   comparison between the two translated inputs selects the earlier bit, with
   harmless ties. Adaptive prior history does not change these fresh-input laws.
3. Earlier winners span a direct complement `W_k` to `S_k`: a nonzero combination
   has a first active winner, whose corresponding hidden row cannot cancel.
   Interpolating the selected next coordinate only on `W_k` therefore acquires
   its degree-`d` prefix polynomial, not an exponential full-prefix table.
4. On `S_k` the selected coordinate has an affine response, since its nonlinear
   term depends only on already fixed inputs. The winner response is known to be
   one; `dim(S_k)-1` extra comparisons determine the remaining linear row and its
   kernel. This maintains the invariant without acquiring a global polar form.
5. At termination, in `x=Vt` the exact coordinate identity is
   `q_i(Vt)=t_i+h_(i-1)(t_1,...,t_(i-1))`. Sequential triangular inversion gives
   every inverse rank. Solving a requested first `k` bits and choosing the other
   `n-k` bits uniformly is a bijection from suffix seeds to its fiber. No source
   comparisons, rejection or hidden conditional sampler are used afterwards.

Let `P=binom(n,2)` and `D=sum_(j=0)^d binom(n,j+1)` with out-of-range binomials
zero. There are exactly `P` tournament contests and `P` additional response
comparisons. Each contest costs at most five comparisons in expectation, while
restricted interpolations sum exactly to `D` by hockey-stick summation. Thus
expected comparison count is at most `D+6P`, with almost-sure termination.
Cap each matching contest at `T=ceil(log2(P/beta))`: failure is explicit UNKNOWN
with probability at most `beta`, no semantic error on completed promised runs,
and worst comparison count `D+(2T+2)P`. The source integer cap implementation
accounts exactly for the supplied binary-rational float `beta`.

Fixing `L=I,c=0` still gives `2^D` coefficient choices and distinct permutations,
hence distinct total orders. Binary comparison decision trees require at least
`D` worst-case queries and average `D` on the uniform class for a zero-error
Las Vegas learner. For fixed `d>=2`, `6P=o(D)` gives leading expected ratio one;
for fixed beta the capped logarithmic term is also lower order. For `d=1` the
ratio here is seven, so the stronger tailored affine baseline must be retained.
With erasure probability beta the capped lower bound is instead
`D+log2(1-beta)`; no unchanged zero-erasure lower bound is imported.

No proof gap was found in these finite exact contracts. This is internal
reconstruction and implementation evidence, not formal or external validation.
Boolean polynomials use multilinear ANF, and affine substitutions preserve the
degree bound. Actual raw polynomials can be expanded without more comparisons,
but expansion/bit cost is separate from the compact acquisition query theorem.

## Resources and retained evidence

Each comparator call transmits two `n`-bit words and returns one bit, giving
`2nQ` transmitted input bits and `Q` response bits. Canonical compact output uses
`D+n^2` logical bits, plus optionally `n^2` for inverse-basis caching. Interpolation
uses `O(2^d D)` field operations; subspace arithmetic, evaluation, random draws,
source preparation, communication, acquisition and checking are separately
charged. The synthetic dense quadratic teacher's cache saves repeated rank
computations but charges `U` fresh rank evaluations and `2nU` logical payload;
Python memory overhead and peak RAM remain unprofiled.

The reported n64 result (`53,746` comparisons, `15.1205...` seconds including
cached synthetic source acquisition) is preserved producer evidence. I did NOT
rerun n64 or independently benchmark a real comparator. Acquired-model and
source-ground-truth checks after termination do not establish physical access,
priority or comparison against a strongest same-oracle prior implementation.

The original ZIP has SHA256
`9848606896fc32920a1d0f6dbe2da8c7d7bdecbdcba5ad60e4990b781e74df89`,
23,478,559 bytes, 413 indexed payload files plus `MANIFEST.json` =414 members.
All 413 producer byte-size/hash pins were checked directly against ZIP bytes;
membership was exact and extraction rejected unsafe/symlink/duplicate paths.
Scratch replay writes never replace original evidence. Extraction inventory is
`extraction.json`; exact source/access scopes are in `SOURCE_ACCESS.json`.

The six submitted bounded replay groups all passed in a fresh scratch copy with
one-thread environment variables, using the local Python standard library:
compact n8/n12, independent quadratic tournament, independent degrees3/4,
independent compact degrees3/4, exact Euclidean selector counterexample and
joint quadratic fibers. The receipt is `REPLAY_RECEIPT.json`; individual logs
are in `source/work/continuation/new_core_replay/`. Source-independent finite
diagnostics are `independent_checks.py` and `independent_results.json`:

- 12 new complete learner cases spanning degrees1–4, with every rank/inverse
  and every prefix target/suffix-seed assignment enumerated; forced cap UNKNOWN.
- 124 exact adjacent-swap recognition witnesses for n3–7, checking all unordered
  comparisons; 48 invertible affine degree-invariance fixtures.
- 18 exact iid binomial majority-tail checks and a correlated-repeat falsifier.

PRNG tests do not certify ideal independent entropy. No inherited 1236-file
original archive replay or physical simulation was performed in this subtask;
the eight legacy replay claims retain their source-reported receipt scope.
An early inspection command used the clone cwd with workspace-relative scratch
paths and failed harmlessly; it was corrected before any replay. No scientific
check failed in the retained six-group or independent runs.

## New consequences and capital relationships

`RECOGNITION_AND_NOISE.md` contains complete new arguments. `CRITIC.md` records
an independent internal critique and the fixes it required.

**Exact recognition obstruction.** For `n>=3`, `1<=d<=n-2`, accept identity with
probability at least `1-alpha` and reject every nonmember with probability at
least `1-beta`. A single adjacent last-bit rank swap has coordinate degree
`n-1`, so is outside the class under every hidden affine representation, yet
changes only that pair's comparison. Transcript coupling forces expected
identity-run query cost at least `max(0,1-alpha-beta)2^(n-1)`. This decisively
refutes polynomial exact arbitrary-oracle recognition as an uncharged wrapper
around the polynomial promised-class learner. It does not obstruct approximate
or separated-distance testing; these particular bad oracles are extremely close.

**Noise lift, conditional only.** With a supplied full-history conditional
per-answer correctness gap rho, odd majority repetitions give a physical budget
`rB`, `B=D+(2T+2)P`, `r>=log(B/beta_n)/(2rho^2)`. An explicit global budget/invalid-
state UNKNOWN wrapper is required. Exact decoder return probability is at least
`1-beta_t-beta_n`; incorrect-model probability is at most `beta_n`, rather than
zero. Marginal accuracy alone fails under correlated errors. This is standard
amplification, not a novel learning mechanism or acquired physical gap.

**Conditional prefix versus common radical.** A complete triangular quadratic
map supplies prefix fibers even when the new submission's one-shot common-
radical rank certificate fails. The explicit four-bit map
`(x1,x2,x3+x1*x2,x4)` has uniform first-three-bit fibers, but their common-radical
translation map has rank one rather than three. Sequential acquired triangular
correction therefore covers this restriction without a full common-radical
right inverse. This does not extend to arbitrary jointly balanced quadratics.

Targeted current routing found no prior exact ordinal/triangular decoder card.
P-learning concerns a distinct latent low-degree graph model. N580/N582 concern
supplied bilinear matrices, a collective-rank envelope and a local rank-ascent
trap; no theorem transfers without a different representation/acquisition lemma.
The primitive-genesis current checkpoint concerns N698 finite-population terminal
laws and also does not supply this decoder class. Robust tracking has a shared
supplied/acquired-interface issue, not a proven logical bridge to decoder recovery.
No architecture changes are justified by lexical adjacency or these finite checks.

## Other submitted lanes: bounded review scope

The full summary and selected joint-quadratic and robust-tracking notes were read.
The common-radical sampler is coherent supplied-coefficient algebra, with explicit
unequal/missing fiber counterexamples; all fiber balancedness is a different,
potentially exponential test. This supplies useful conditional/negative capital,
not general quadratic solving or acquisition. Its finite exhaustive group passed.

The robust-tracking fixed-block reduction keeps local rank fixed, explicit
horizon and inverse strict margin in its cost; it is conditional on an inherited
general existence theorem that I did not independently audit. The factorized
all-time wrapper reuses a retained low-dimensional invariant rather than newly
synthesizing general selector closure. The exact Euclidean two-step counterexample
rejects convexifying winning states only; its finite group passed. The general
arbitrary-schedule compiler remains open.

Quantum, water, bioenergy, transport, thermometry, rare paths, molten-metal and
sparse-monomial lanes remain source-reported here, with their report's negative
controls and unresolved physical gates intact. Root is handling broad-lane
integration; this review gives no unperformed proof/physical audit credit.

## Prior art and next decisive work

[Maubach's primary manuscript](https://arxiv.org/html/1106.5800v3), §2.1, explicitly
defines the classical triangular permutation family. [Booth et al.'s primary
paper](https://www.lamsade.dauphine.fr/~lang/papers/bclms09.pdf), §4, studies exact
chosen-pair preference elicitation on visible binary attributes and counting
bounds. Those objects and access methods are prior; this bounded review did not
settle the exact hidden-affine low-degree acquisition interface. No nonfinding
is a novelty certificate. [Viola's primary abstract](https://eccc.weizmann.ac.il/report/2015/205/)
concerns constant-depth circuit sampling of quadratic graph distributions, a
different operation from polynomial-time supplied-coefficient fiber correction.
Precise access scopes, not merely citations, are in `SOURCE_ACCESS.json`.

The highest-value next gate is a strongest same-oracle prior comparison and a
real target whose structural promise can be justified without arbitrary-oracle
exact recognition. A useful mathematical continuation would remove the complete
triangular assumption under a precise bounded-degree outside-class promise or
meaningful approximation criterion. For noisy access, acquire and test a legal
conditional noise/repetition contract before interpreting repetition as hardware
robustness. Specialist proof and priority review remain required. Mission status
remains NOT ACHIEVED.
