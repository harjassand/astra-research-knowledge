# Random-matching singlet survival: dimension-free loss witness

Date: 2026-10-29. Status: author derivation, awaiting independent review.
This is a new construction, not an assertion of historical novelty or hardware readiness.

## Operational statement
Let n=2m >=4 spin-1/2 systems, let P be their total-spin-zero projector, and
let d=rank(P)=binom(2m,m)/(m+1). Let N be ANY CPTP map from these n systems
back to the same physical space. No collective-noise model is assumed.
A test consists of:
1. Privately sample a uniform perfect matching M of the n labelled systems.
2. Prepare a singlet on each of its m edges, yielding the pure state |M>.
3. Apply N once, with the same source boundary as the intended storage operation.
4. Measure each of the SAME m edges in the Bell basis. Pass iff EVERY edge
   reports its singlet. Equivalently the passing effect is rho_M=|M><M|.
Let q=1-E_M Tr[rho_M N(rho_M)] be the actual average failure probability.

For every isometry V:C^K -> range(P), use the physical encoder V and the
reset-completed decoder D_V(X)=V* X V + Tr[(I-VV*)X] tau, where tau is any
fixed logical density matrix. Then

    1-F_e(D_V N V) <= (d/K) [(n+2)/(n-1)] q.                 (1)

Here F_e is maximally mixed input entanglement fidelity; notation N V means
rho -> N(V rho V*). In particular K=d gives coefficient (n+2)/(n-1).
Choosing K the largest power of two <=d gives d/K<2 (or =1 when d is a
power of two). The coefficient stays below 2(n+2)/(n-1), irrespective of
Hilbert-space dimension. For K=1 actual logical entanglement infidelity is
zero under the reset-completed decoder, but (1) remains a valid loose bound.

The statement certifies the currently tested map, not a future arbitrary map.
In a conditional sequential experiment the same inequality applies separately
at each actual source-memory history whenever that history defines a CPTP
source input-output map and the current matching is sampled independently.
It is NOT by itself a composable memory-comb or postselected diamond theorem.
Existing sequential guard results require their separate hypotheses.

## 1. Exact matching frame spectrum
Work in the Hilbert-Schmidt operator space End(range(P)). Define

    F = E_M |rho_M))((rho_M|.

There are L=(2m-1)!! matchings. Singlet contraction around each connected loop
of the union of two matchings gives

    |<M|N>|^2 = 4^(loops(M,N)-m).

(The overlap itself can have an orientation sign; the squared overlap does
not.) Consequently the Gram matrix of the normalized frame columns
|rho_M))/sqrt(L) is

    G_MN = 4^loops(M,N) / (4^m L).

This is exactly the orthogonal pair-partition Gram matrix with dimension
parameter 4, divided by 4^m L. Collins and Matsumoto, arXiv:0903.5143,
Eq. (3.6), Lemma 4.3, Eq. (4.6), give its eigenvalues

    f_lambda = [product_(i,j) in lambda (4+2j-i-1)] / (4^m L),

for partitions lambda of m with at most four rows; multiplicity f^(2lambda)
is the symmetric-group irreducible dimension. Partitions with >=5 rows have
zero eigenvalue. F and its Gram matrix have the same nonzero spectrum;
additional operator-space null directions do not affect the upper bound.

The average rho_M is P/d: the average is invariant under all permutations,
is supported in spin zero, and the spin-zero space is the irreducible S_n
module of shape (m,m). Its trace is one. Thus F(P)=P/d. This identifies the
scalar eigenvector. Alternatively the formula below identifies its simple
maximal eigenvalue.

For lambda=(m), the numerator is product_(j=1)^m(2j+2)=2^m(m+1)!.
Using 4^m L=2^m (2m)!/m! gives f_(m)=1/d.
For lambda=(m-1,1), replacement of the final first-row box by (2,1) gives

    f_(m-1,1) / f_(m) = 3/(2m+2) = 3/(n+2) = r.

Here is a complete ordering argument, avoiding an unproved second-eigenvalue
claim. For any nontrivial partition of m of length <=4, repeatedly remove the
last box in its bottom nonempty row i>=2 and append it to the first row,
stopping when only one box remains outside the first row. At every step the
partition stays a partition. The removed factor is 2 lambda_i +3-i, which is
positive because i<=4 and lambda_i>=1. The added factor is 2 lambda_1+5,
strictly larger since lambda_1>=lambda_i. The resulting terminal partition is
(m-1,1). Thus every other nontrivial eigenvalue is smaller or equal to its
value. The all-one-row partition is uniquely largest by the same procedure.
Therefore, for EVERY complex traceless operator B on the singlet space,

    E_M |<M|B|M>|^2 <= (r/d) ||B||_2^2.                  (2)

This includes complex and nonsymmetric operators: F is a positive Hermitian
operator on the complex Hilbert-Schmidt space. Real preparation vectors do
not justify restricting errors to real operators. Some complex directions are
in the kernel, which only strengthens (2).

## 2. Arbitrary CPTP noise, including leakage
Choose Kraus operators K_a for N. Set A_a=P K_a P,
a_a=Tr(A_a)/d, B_a=A_a-a_a P, and f0=sum_a |a_a|^2.
Averaging the scalar/traceless cross term vanishes by E rho_M=P/d. Hence

    p_pass = f0 + sum_a E_M |<M|B_a|M>|^2
           <= f0 + (r/d) sum_a ||B_a||_2^2
           = (1-r) f0 + r s,
    s = (1/d) sum_a ||A_a||_2^2 <=1.

The last inequality follows from trace preservation, not from unitality or
noise-model assumptions: sum ||P K_a P||_2^2 <=sum ||K_a P||_2^2=d.
Therefore 1-f0 <=q/(1-r). A reset-completed full-singlet decoder has fidelity
at least f0; its leakage Kraus terms add nonnegative contributions. This proves
(1) when K=d without assuming the source preserves the singlet space.

## 3. Every fixed singlet subcode
Let Q=VV* be any K-dimensional subprojection of P, and put
b_a=Tr(Q K_a Q)/K. A reset-completed subcode decoder has fidelity at least
sum_a |b_a|^2. By trace preservation and least-squares minimization in the
scalar coefficient,

    1-sum_a |b_a|^2
      = (1/K) sum_a min_c ||K_a Q-c Q||_2^2
      <=(1/K) sum_a ||(K_a-a_a I)Q||_2^2
      <=(1/K) sum_a ||(K_a-a_a I)P||_2^2
      = (d/K)(1-f0).

The second inequality is positivity of the Hilbert-Schmidt quadratic form
when Q<=P; it makes no simultaneous diagonalization assumption. Combining
with Section 2 proves (1). The factor d/K is a worst-case localization cost,
not claimed sharp for every subcode.

## 4. Sharpness of the full-code coefficient
The largest traceless frame eigenspace has a nonzero traceless Hermitian
operator H: the frame is generated by Hermitian projectors and preserves
adjoints. Let N_t act as exp(i t H) on the singlet space and as identity on
its orthogonal complement. It has no leakage. As t tends to zero,

    1-F_e(N_t|P) = t^2 Tr(H^2)/d + O(t^4),
    q_t = t^2 [Tr(H^2)/d - E_M <M|H|M>^2] + O(t^4)
        = (1-r)t^2 Tr(H^2)/d + O(t^4).

Thus the ratio approaches 1/(1-r). No uniformly smaller multiplicative
coefficient can cover all channels for this exact test. An explicit useful
candidate is the traceless part of a transposition on the singlet module;
numerical checks below verify this candidate lies in the second eigenspace.
The existence argument, rather than that candidate identification, is the
proof of sharpness.

## 5. What this changes, and what it does not
- Previous one-random-edge witnesses paid a linear-in-n loss coefficient.
  This test changes the operation: it prepares and checks an entire random
  matching. It does not contradict a lower bound for the old one-edge test.
- Only Bell-pair preparation and Bell-pair measurements are needed per test,
  with no retained test ancilla and no full Schur encoder per test. Uniform
  matching can be sampled exactly by selecting a uniform partner of the first
  unpaired vertex repeatedly, costing O(n log n) expected fair random bits.
  Finite random-bit caps require an explicit failure probability.
- All-to-all paired gates permit O(n) gates per prepare/readout layer. A line
  needs routing: any chosen matching can be brought to neighboring pairs using
  O(n^2) adjacent swaps and O(n) depth, then inverted for the source boundary
  and final readout. No free long-range operation is assumed.
- Known local frame rotations may be applied before/after this test, and the
  whole statement is then unitarily conjugated. Inexact rotations alter the
  actual test; they need calibration or an explicit error debit. A learned
  candidate frame need not be a true collective symmetry for witness soundness.
- If every test circuit differs in total variation by at most eta from its
  ideal counterpart, q_ideal<=q_observed+eta. Hence the right side in (1) is
  C(q_observed+eta). A gatewise hybrid bound gives eta<=sum primitive errors.
  With C bounded, sufficient per-primitive errors are O(epsilon/n) for direct
  paired access or O(epsilon/n^2) for line routing. These are conservative
  sufficient budgets, not hardware measurements or optimal fault-tolerance.
- A logical 2-design survival test has coefficient (K+1)/K and can be better
  statistically. This construction substitutes pair routing/preparation for
  full code-state preparation; actual total-cost advantage requires comparing
  implementations under equal resources. No general advantage is asserted.
- Entanglement fidelity does not itself upper-bound worst-case diamond error
  linearly. An ACTUAL logical Pauli twirl with private pre/post keys, retirement
  of those keys, and a reset-completed logical channel can turn entanglement
  infidelity into the half-diamond distance of the twirled channel. Without
  that operation the familiar square-root/worst-case issue remains.
- The matching and role must not be leaked to the source. Uniformity for each
  fixed CPTP map does not cover a map selected after learning M. For example
  a source that receives M can apply a reflection about |M>; every test passes,
  while an unrelated encoded input can suffer a nontrivial logical unitary.
- A pass does not demonstrate a collective microscopic environment; generic
  noise agreeing on the protected input space is equally compatible.

## Source and evidence
Primary source read on 2026-10-29:
https://arxiv.org/html/0903.5143 (equations 3.6, 4.6 and Lemma 4.3).
https://arxiv.org/pdf/0903.5143 is the PDF alternative. Page metadata displays
inconsistent regenerated dates; the stable identifier is arXiv:0903.5143v1.
The theorem above is derived from its exact Gram spectral identity, not from
search snippets or a claimed new representation-theoretic theorem.

Reproduce checks: OPENBLAS_NUM_THREADS=1 python3 check_matching_survival_v1.py
Outputs: check_matching_survival_v1.json. Checks are numerical diagnostics for
finite instances and exact-integer partition ordering; they do not replace the
all-n argument or constitute physical observations.
