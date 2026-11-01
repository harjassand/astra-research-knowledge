# A constructive success theorem for contrastive partition acquisition

Draft new work; not independently reviewed. This is a discovery guarantee for
a precise class, followed by independent reuse validation. It is not a
universal representation learner or a new spectral-clustering claim.

## 1. Unknown class and receiving interface

There are n named states and two ordinary iid forward row samplers A0,A1.
All chosen rows and observed destinations may be retained. No reverse sampler,
common random seeds, true probabilities, partition, prototypes, rank, spectral
basis, or efficient teacher is supplied. The algorithm chooses a rational
resolution beta>0 and a confidence budget. All resolution/search attempts use
nonanticipating fresh samples and separately budgeted failure events.

For the SUCCESS theorem only, assume an unknown balanced partition P=ZW,
W=Z^T/k, r blocks, k=n/r, 2<=r<=n. Let J=I-11^T/n. Suppose

 C*=Z D W, D1=0, 1^T D=0, rank(D)=r-1,
 sigma_min_nonzero(D)=Delta >=256 sqrt(r) beta,
 ||(A1-A0)-C*||_2 <= beta/2.                         (1)

Also assume max_i ||[(A1-A0)-C*][i,:]||_1<=beta/32. These are properties
of the unknown family, not quantities the learner may simply assert. The final
independent reuse certificate is necessary even if discovery works.

An actual source family is A_a=K+Z C_a W+R_a with common arbitrary full-rank K,
centered macro C_a, and small R_a. K cancels from contrast expectations. For
future reuse, K must additionally reduce P (and suitable tasks must respect P),
or the later c/e/d certificate must otherwise pass. Contrast structure alone
does NOT imply a useful abstraction. Example failures will be kept explicit.

## 2. Acquiring operator accuracy without n^2 entrywise precision

A paid preliminary ordinary uniform-source sample acquires a simultaneous
column cap B>=max_(a,j)sum_i A_a(i,j), with B>=1. This is the inherited elementary
column-count certificate; no B=O(1) assertion is made for arbitrary sources.
Explicitly, for N_c uniform-source outcomes per action, a column count X_j has
mean N_c q_j, q_j=(column sum)/n. Except with probability e^(-K_c),
q_j<=2X_j/N_c+8K_c/N_c: otherwise a multiplicative Chernoff lower-tail event
X_j<N_c q_j/2 occurs with probability <=exp(-N_c q_j/8)<=e^(-K_c).
Union over 2n columns/actions with K_c>=ln(2n/delta_c) yields
B=min(n,max(1,max_(a,j) n(2X_j+8K_c)/N_c)). The source rows used for these
observations are legitimate retained metadata for every competing method.
Now take N independent samples from EVERY named row of each action. Let Ahat_a
be its sparse empirical stochastic matrix. For a fixed action, write the error
as the sum of centered row-sample matrices. Each summand has norm<=2/N; the
sum of left variance matrices is <=I/N and the right variance sum is bounded
by diag(column_sums)/N<=BI/N. Rectangular matrix Bernstein therefore gives

 ||Ahat_a-A_a||_2 <= tau
 tau=sqrt_up(2 B Klog/N)+4 Klog/(3N),
 Klog>=ln(4n/delta_s),                                (2)

simultaneously for both actions with failure<=delta_s. Constants are chosen
conservatively from the 2n-dimensional self-adjoint dilation. Choose N until
2 tau<=beta/2. Then C=J(Ahat_1-Ahat_0)J satisfies ||C-C*||_2<=beta on (1),(2).
The common background cancels only in expectation. Independent forward noise
is fully charged; no samplewise cancellation is assumed. Sampling is
O(n B log(n/delta_s)/beta^2) per fixed resolution, not fine n^2 entry learning.
The actual B, failed rounds and preliminary column samples remain costs.
The count frontend uses outward square-root precision at least
ceil(log2(64/beta)) bits. Its closed sufficient N reserves slack for this
rounding (sqrt and linear terms each <=beta/16, root rounding <=beta/64);
it never assumes that an unrounded equality still passes after rounding.

## 3. No assumed spectral oracle: an explicit finite-bit projector proposal

Set S=C C^T and R=||C||_F^2+4 beta^2. Let X0=(S-4 beta^2 I)/R. Its spectrum
lies in [-1,1]. Under (1),(2), its eigenvalues have absolute value at least

a=min(1/2,3 beta^2/R),

because unwanted singular values of C are <=beta and wanted ones are
>=Delta-beta>=3beta. Apply the polynomial p(x)=(3x-x^3)/2 repeatedly. For
0<=x<=1/2, p(x)>=(11/8)x. For x>=1/2,
1-p(x)=(1-x)^2(2+x)/2 <=(3/2)(1-x)^2.
Thus a computable number T=O(log(1/a)+log log(1/nu)) of repetitions makes
p^T(X0) within nu/8 in operator norm of sign(X0). T is obtained solely from
a and nu using rational multiplications and squarings, not unknown eigenvalues.

Use nu=1/(1024n). Round X0 and EACH subsequent p(Y) entrywise downward to a
common dyadic denominator 2^b, preserving symmetry, with

 n*2^(-b)*4^(T+1) <=nu/8.                              (3)

If ||Y-X||_2<=nu/8 and ||X||_2<=1, then
||p(Y)-p(X)||_2<=4||Y-X||_2, by expanding Y^3-X^3. Entry rounding has norm
<=n2^-b. Induction and (3) therefore bound the total roundoff by nu/8.
The rational matrix

 F=(I+Y_T)/2+11^T/n

is within nu of the orthogonal projector P_hat onto the resolved left
singular subspace plus the constant vector. C is centered on both sides, so
the latter is orthogonal to its nonzero left singular vectors. The true rank
r is the nearest integer to trace(F), since |trace(F)-r|<=n nu<1/2.
If the inferred r is not a divisor of n or other receiving conditions fail,
the discovery procedure refuses. Away from the success class, F is merely a
proposal: its apparent rank is not a structural proof.

This dense backend uses O(T n^3) rational/integer scalar products and O(n^2)
storage, not a free basis oracle. After each rounding its entries have O(b)
bits; cubic intermediates have O(b+log n) bits up to constant factors. Input
formation/common denominators and source-count bits are also paid. Sparse
randomized SVD, signed-graph spectral methods and ordinary multi-view methods
are equally informed practical comparators and may be much faster. This dense
construction establishes finite-bit polynomial computability, not practicality.

## 4. Approximate partition without a k-means oracle

Let P* be the true block-averaging projector. Since the least resolved singular
value is at least Delta-beta, the elementary singular-subspace calculation

 (I-P*) U_hat = (I-P*) (C-C*) V_hat Sigma_hat^(-1)

gives ||P_hat-P*||_F<=sqrt(2r) beta/(Delta-beta). Therefore

 ||F-P*||_F^2 <=4r beta^2/(Delta-beta)^2 +2n nu^2.       (4)

All true P* rows in a block coincide; distinct block rows have distance
s0=sqrt(2/k). Call a row bad if its error exceeds s0/16. By (4),

 b_bad <=512n beta^2/(Delta-beta)^2 +256n^2 nu^2/r <k/16. (5)

The last inequality follows from Delta>=256 sqrt(r) beta, n>=r>=2 and the
chosen nu. This bound is not the algorithm's knowledge of which rows are bad.

Among remaining rows of F, choose a center having the largest number of
remaining rows within radius s0/4. Ties are broken by the named-state order.
Some true block still has at least k-b_bad good rows, all pairwise within
s0/8, so the selected ball has at least that many points. Its good points
belong to only one true block: distinct-block good rows are separated by
>=7s0/8, larger than the ball's diameter. The center is within5s0/16 of that
block's true row. Assign every remaining row within s0/2 to this cluster.
This includes all good rows of that block and excludes every other good row.
Repeat r times and assign leftover bad rows arbitrarily. Every possible error
is confined to the same bad set. No optimizing k-means or prototype oracle is
used. Squared rational distances compare with r/(8n) and r/(2n); no irrational
threshold is numerically assumed. Dense distance/greedy work is O(n^3+n^2r).

Let Tgh be the fraction of TRUE block g assigned to proposal block h, after
aligning labels for analysis. Because only b_bad states can be wrong,
||T-I||_infinity<=2b_bad/k and ||T-I||_1<=2b_bad/k. Hence ||T-I||_2<1/8.

## 5. Fresh contrast cleanup acquires every label

For each row/action collect N_f NEW forward outcomes and count only their
proposal-block labels, retaining the chosen source row. Conditional on the
old proposal these samples are iid with fixed design. Their expectation
contrast is

 [(A1-A0) Z_proposal][i,:] = D[g,:] T + error_i,
 ||error_i||_2<=||error_i||_1<=beta/32.                  (6)

This is the second cancellation of K. Since D is centered and has smallest
nonzero singular value Delta,
||D[g,:]-D[h,:]||_2>=sqrt(2) Delta for g!=h.
Consequently prototype separation after T is >=(7/8)sqrt(2)Delta.

Take coordinate error at most alpha=beta/(64 sqrt(r)) for each action/row/
proposal-block entry. A Hoeffding union bound gives this with failure<=delta_f
when

 N_f >=2048 r ln(4 n r/delta_f)/beta^2.                 (7)

The empirical action difference then has L2 noise<=2sqrt(r)alpha=beta/32.
Together with (6), every observed feature row lies within beta/16 of its true
prototype. Thus within-block distances are <=beta/8, while cross-block
distances exceed beta/4 by (1). Connected components at threshold beta/4
recover the exact partition, up to labels. A simple deterministic representative
scan also suffices under these inequalities; unexpected rank/size causes a
refusal. Comparisons use exact rational squared distances. This costs
O(n^2r) arithmetic conservatively, or less with a proved representative scan.
The algorithm never queries the unknown prototypes or uses the true labels.
`proposal_from_counts` builds the contrast from externally bound column/row
counts and refuses inadequate spectral precision. `cleanup_from_counts` binds
the old proposal hash, checks complete equal fixed row totals and its fresh
sample requirement, then constructs the contrast features itself. Statistical
provenance cannot be authenticated by these arrays. The supplied exact tests
exercise deterministic algebra/noise hypotheses and receiving refusals, not a
new stochastic source experiment or a fully executed reuse-validation pipeline.

## 6. Reuse is a separate acquired fact

The exact recovered partition is not automatically useful. Receive the actual
initial law and future observable interface, then independently acquire the
full-record c/e/d stochastic-projection certificate with all its observation,
confidence, finite-bit and search costs. Its verified E_L bound, not the
common-background assumption, authorizes future block-history/Bellman/monitor/
population consumers. The same learned ingredient is available to ordinary
spectral/range/reward-free methods. A common K which does not reduce P can make
reuse fail despite perfect contrast recovery; that is a substantive failure.

For the explicit useful family K P=P K and A_a=K+Z C_a W+R_a, the leakages arise
only from R_a. If max_i||R_a[i,:]||_1<=eta and ||R_a||_2<=rho, then c<=eta and
e<=sqrt(r)rho for balanced blocks. Therefore sufficiently small perturbations
permit a valid low-rank reusable model even though generic perturbations make
exact block closure disappear and the centered contrast have rank n-1.
Stochasticity still preserves the constant direction; no impossible full n-by-n
algebra claim is made. Statistical
validation may still cost much more than discovery; its bill is not erased.

## 7. Failures and exact scope

- No contrast gap: no promise that action variation supplies informative rank.
  Doubling/trying other resolutions is paid and may never acquire this P.
- Rank selection below perturbation scale can select microscopic directions;
  beta is a modeling resolution, not an exact-closure test.
- Arbitrary large column cap B destroys the favorable observation bill.
- Too many wrong labels make T ill-conditioned; fresh cleanup need not work.
- A common non-reducing background defeats reuse although it cancels perfectly
  from discovery. Validation is essential.
- Balanced blocks, a centered full block-space contrast and a quantitative gap
  are current success-class assumptions, not general properties of MDPs.
- Dense exact filtering has substantial time/storage; no practical gain follows
  merely from O(n polylog n) observations. Source observation calls and internal
  computational cost are separate.

Contrastive PCA, spectral clustering, sample-splitting exact community recovery,
matrix Bernstein, and polynomial matrix-sign filtering are established tools.
The present ordinary proof constructs their particular acquisition/validation
join. Prior matching is ongoing; no historical novelty or consequential
comparative advantage is asserted.
