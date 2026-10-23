# Local spectral-rank coercion and aggregation: independent lemma review

Reviewer: `/root/fan_port_lemma`, 22 October 2026 Australia/Brisbane.
Reviewed object: the root's local rank-coercion and many-child aggregation
lemmas, not the separate global core/cancellation proof. This is a proof
review and improvement; no numerical experiment or old theorem replay.

## 1. Precise hypotheses

For a graph G with free diagonal, let

    C_2(G,X) = sup_{0 != D in S_G} ||D||_2 / ||DX||_F,

with infinity if a supported nonzero kernel exists. Assume each row of the
real n-by-5 matrix X has Euclidean norm at most one. Suppose G contains an
attached child fan whose apex plus M path vertices form an allowed fan
support. The full graph may have further edges or vertices; a supported
matrix confined to this fan and zero elsewhere is always permitted.

If C=C_2(G,X) is finite, the child's restricted query block inherits

    ||D||_2 <= C ||D X_child||_F

for every supported symmetric child matrix D. This follows by extending D
by zero. Its operator norm is unchanged and no additional output rows become
nonzero. The apex row is included in the child output norm. It need not have
zero action.

Let F(M)>0 be an accepted all-design inverse lower bound for three-query
recovery on the fan with M path vertices, at the same row cap. For example,
for the admissible M in the supplied theorem one may use

    F(M)=max(1,[2 sqrt(M-1) sin(3 pi/(2M))]^(-1/2)),

or the weaker explicit lower bound max(1,M^(1/4)/sqrt(3 pi)). This is the
accepted fan theorem preserved in the previous archive; its proof is an
explicit dependency. Write a=1/F(M).

Let W be the M-by-5 matrix of child path query rows, excluding the apex, and
let A=W^T W. Its eigenvalues are lambda1>=...>=lambda5>=0. Define

    T(A)=lambda3+lambda4+lambda5.

## 2. Projection perturbation lemma

**Lemma.** Under these hypotheses,

    T(A) >= (1/C - a)_+^2.

In particular lambda3(A)>=(1/C-a)_+^2/3. The tail-sum inequality is the
stronger and more useful statement for aggregation.

**Proof.** Choose any rank-two orthogonal spectral projection P onto two
largest eigenvalues of A. If eigenvalues coincide, choose any orthonormal
eigenvectors within the repeated eigenspace; every such choice has the same
trace. Replace W by WP but keep the apex row exactly unchanged. The resulting
full child block Xtilde has row-span dimension at most three: all path rows
belong to range(P), and the apex adds at most one dimension. Orthogonal right
compression into three columns preserves each row norm and every Frobenius
action norm. Padding by zero columns handles rank less than three.

The inherited three-query theorem gives a supported child matrix D of operator
norm one with ||D Xtilde||_F<=a. Existence can be justified without an
approximate minimizer: the unit operator-norm sphere in the finite-dimensional
supported matrix space is compact, so the continuous action norm has a
minimum. If the compressed block has a kernel, the minimum is zero.

The input perturbation has zero apex row and path block W(I-P), hence

    ||X_child-Xtilde||_F^2
      = tr((I-P) A (I-P)) = tr((I-P) A) = T(A).

Submultiplicativity and the normalized operator norm give

    ||D X_child||_F <= a + sqrt(T(A)).

The child inheritance inequality therefore implies

    1/C <= a+sqrt(T(A)).

Taking the positive part and squaring proves the lemma. Finally
T(A)<=3 lambda3(A). QED.

**Apex clarification.** Only the apex row of the INPUT perturbation is zero.
The apex row of D Xtilde or of D(X_child-Xtilde) need not be zero. Neither
zero-output assertion is used or required. The global inverse assumption
controls the full child output, including that row.

## 3. Aggregation with an improved constant

Let N child fans at one apex have respective path Grams A_1,...,A_N. All
have the same path length M for simplicity, and all inherit the same global
inverse constant C. Define t=(1/C-a)_+ and A_sum=sum_j A_j. Then

    lambda3(A_sum) >= N t^2 / 3.                 (1)

The root's initially proposed N t^2/9 also follows, but loses an unnecessary
factor three by discarding each child's full tail sum too early.

**Proof.** For every positive semidefinite five-by-five matrix A,

    T(A)=min_{P orthogonal, rank(P)=2} tr((I-P)A).

For completeness, diagonalize A. The diagonal weights of P in an eigenbasis
lie in [0,1] and sum to two, so tr(PA)<=lambda1+lambda2, attained at a top-two
spectral projection. This proves the displayed variational formula without
assuming simple eigenvalues.

Consequently,

    T(A_sum)
      = min_P sum_j tr((I-P)A_j)
      >= sum_j min_P tr((I-P)A_j)
      = sum_j T(A_j)
      >= N t^2.

Since T(A_sum)<=3 lambda3(A_sum), (1) follows. QED.

The same proof works for unequal child lengths, giving

    lambda3(A_sum) >= (1/3) sum_j (1/C - 1/F(M_j))_+^2.

It also handles deficient or zero path rank: such a child can satisfy the
global assumption only when its tail lower bound is zero. If C is infinite,
the desired global obstruction is already present and these inequalities
need not be invoked. Finite C is positive (indeed at least one under the row
cap and free diagonal), so every displayed reciprocal is legitimate.

## 4. Quantifiers and computational status

The claims hold for arbitrary real query rows and do not assume a finite
palette, local orthogonality, independent subblocks, or repeated child data.
All child frames can be graph-adapted and mutually different. Child Gram
eigenspaces are chosen only for the mathematical lower-bound proof. Their
construction has not been treated as a free numerical algorithm or certificate.

The witness D used in the projection lemma may depend on the projected child
block; this is permitted by the all-design inverse quotient. The global
assumption applies to every such supported D. No simultaneous selection of
these witnesses is needed to sum the scalar tail inequalities.

This contribution certifies only the local rank and aggregation lemmas. A
complete five-query lower bound still requires the root's global graph,
dimension count, support-preserving cancellation, operator normalization and
full error estimate. Those obligations are not inferred from (1) alone.

## 5. Costs and dependency

This was a symbolic proof review and constant improvement. No numerical run,
web search, original benchmark replay, or new optimization was used. Proof
reading/development, model inference, file authoring, monetary cost and energy
are unmetered additional costs, not zero. Its only mathematical dependency
beyond elementary finite-dimensional linear algebra is the accepted three-query
fan obstruction, retained in the prior owner source.
