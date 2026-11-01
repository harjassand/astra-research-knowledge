# Discovery from action contrasts, before validation

New research, not covered by any previous receipt. No previous source/archive
is modified. The current useful scientific question is not whether ordinary
reward-free learning already permits many goals (it does), nor whether SAT can
be hidden in a future reward circuit (it can). It is:

**Can an economical useful task representation be acquired, rather than merely
validated, despite an arbitrary full-rank microscopic background and finite
operator observations?**

The current threshold-community proposal has no general success theorem. A
rank promise alone does not supply useful probes, and one-action spectral
separation can fail. The first constructive foothold is a COMMON-BACKGROUND
contrast class. Two actual actions are observed independently; no paired-seed,
reverse-transition, exact probability, optimal teacher or supplied partition
oracle is granted.

## Model class for a success theorem (not advice given to the learner)

There are n named states, two iid forward row samplers, and an UNKNOWN balanced
partition into r blocks of size k=n/r. Write Z for its indicators and W=Z^T/k.
For unknown common K and macro matrices C_a,

 A_a = K + Z C_a W + R_a,       a=0,1.

The actual A_a are stochastic. For reuse, K reduces the block subspace and is
bistochastic; C_a has zero row/column sums. For discovery alone these reduction
conditions on K are unnecessary because it cancels. Let D=C_1-C_0 be centered
and rank r-1, with least nonzero singular value Delta. The ideal contrast
C*=Z D W has that same nonzero singular spectrum. Its left range is precisely
the centered block subspace. Microscopic dynamics need not be low rank.

A success regime assumes ||R_1-R_0||_2 is small and the per-row L1 contrast
perturbation is small. These are unknown properties of the class; the later
independent acquired c/e/d certificate, NOT the class assumption, admits reuse.
The algorithm may refuse elsewhere. Tiny nonzero perturbations may make exact
small algebraic closure disappear and the centered contrast have rank n-1; a finite resolution is
used throughout. No claim that low rank alone is learnable cheaply is made.

## Actual proposed acquisition

1. Acquire a simultaneous column-sum cap B from ordinary uniform-row samples.
   This is needed by matrix concentration; B is not automatically constant in
   an unbalanced source. Collect N independent named-row transitions per action.
   Store the resulting sparse row counts. Center the empirical action contrast
   on both sides with J=I-11^T/n. Common K cancels IN EXPECTATION, not samplewise.
2. Use a paid ordinary spectral filter/SVD on that contrast to propose its
   finite-resolution left subspace. Add the constant vector. Infer candidate r
   from the resolved spectral rank; do not treat a stalled rank test as proof
   no useful representation exists. A dense, fully finite-precision spectral
   filter is being specified as a no-oracle constructive backend; a practical
   sparse SVD is an equally informed ordinary comparator, not a weak baseline.
3. Cluster projector rows by a deterministic densest-ball/greedy procedure,
   avoiding an assumed global k-means optimizer. Under a quantified gap this
   mislabels only a small fraction of states, with all errors in a bounded bad
   set. All candidate rank/resolution rounds and failed clustering cost money.
4. On FRESH samples, retain each chosen row's destination PROPOSAL-block counts
   under BOTH actions. Their difference cancels K again. Even an imperfect
   proposal turns the macro contrast into D T, where T is the actual confusion
   matrix. If few labels were wrong, T is well conditioned. These new row
   contrasts have separated prototypes; elementary threshold components recover
   the exact unknown partition, without a prototype oracle or n^2 finely learned
   transition entries. No source-row tags are discarded.
5. Acquire/receive the uniform stochastic-projection c/e/d certificate for all
   actions on further valid data, including finite-bit and failure budgets. The
   full-record, feedback, monitor and population consumers then use the learned
   partition only IF it passes. Discovery is not itself a reuse certificate.

## First quantitative calculation

With a column cap B>=1, N row samples, and Klog>=ln(4n/delta), matrix Bernstein
for the empirical stochastic matrix gives, per action,

 tau = sqrt(2 B Klog/N) + 4 Klog/(3N).

Indeed each centered row-sample matrix has norm <=2/N, left variance <=1/N and
right variance <=B/N. The contrast noise is <=2 tau. Centering does not increase
it. The ambient-square variance penalty is absent, but the actual B remains.

Suppose total contrast error to C* is beta and Delta>=256 sqrt(r) beta. An
ordinary singular-subspace estimate has projector Frobenius error at most
sqrt(2r) beta/(Delta-beta), plus a paid numerical-filter error. True projector
rows coincide within blocks and are separated by sqrt(2/k). Calling a row bad
when its error exceeds one-sixteenth of that separation bounds the bad count
by O(n beta^2/Delta^2). The stated conservative gap makes this <k/16.

A densest ball of radius separation/4 contains good points of only one true
block and at least k-bad_count points. Enlarging it to separation/2 includes
all good points of that block and no good point from another. Repeating r
rounds, and assigning leftover bad points arbitrarily, confines every possible
mislabel to that bad set. Thus ||T-I||_2<=2 bad_count/k<1/8 after relabelling.
The row-prototype separation in D T is at least (7/8)sqrt(2) Delta.

If fresh empirical contrasts are within beta/32 in L2 and row perturbations
within beta/32 in L1, each feature row is within beta/16 of its correct prototype.
Within-block distances are <=beta/8 and cross-block distances are larger than
beta/4. Threshold components therefore recover all labels exactly. Coordinate
Hoeffding with N_fresh >=2048 r log(4nr/delta)/beta^2 suffices. Combined with the
spectral stage, observations are O(n poly(r,B,1/gap) log(n/delta)), rather than
estimating all n^2 microscopic entries finely. Constants/precision/computation
and the separate reuse-validation bill must still be fully charged.

This is a first proof calculation, not yet a complete theorem or executable
claim. Common-background subtraction, spectral clustering, sample splitting,
cleanup and matrix concentration are ordinary tools; exact prior-match work
must determine what, if anything, is new in this acquisition theorem. Every
strong multi-view/spectral method gets the same contrast observations and can
adopt the same subsequent certificate. There is no comparative superiority or
practical/civilisation-level claim yet.
