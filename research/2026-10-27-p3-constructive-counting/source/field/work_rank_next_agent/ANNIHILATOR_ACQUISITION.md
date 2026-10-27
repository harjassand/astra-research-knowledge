# Acquiring a hidden low-rank perturbation through a polynomial annihilator

27 October 2026. All matrix algebra is over F₂. The acquisition theorem and its
finite executions are unconditional. Its original-input counting consequence
uses the separately preserved local-phase theorem, conditional on the pinned
OpenAI replacement-form manuscript. No practical speedup or first-priority
claim is made.

## 1. Result and scope

Let the raw input be a symmetric n by n matrix B. A quadratic Boolean phase
uses its off-diagonal entries; the diagonal may be retained for algebraic
purposes. Suppose B has an unknown decomposition

\[
B=D+S,\qquad D=UKU^\top,\qquad \operatorname{rank}D=r,
\]

where U has r independent columns, K is invertible and symmetric, S is
symmetric and every row of S has at most Δ nonzero entries, including a
possible diagonal entry. Neither U, K, D, S nor a sparse graph is supplied.

Let h be a monic binary polynomial of degree q with h(S)=0. Define the
unobserved orbit matrix

\[
W=[\,U,\;SU,\;\ldots,\;S^{q-1}U\,].
\]

The class conditions are:

1. W has all qr columns independent;
2. the code spanned by W has minimum nonzero Hamming weight greater than 2Δ.

These are additional structural conditions, not consequences of arbitrary
low rank and sparsity. Their role is explicit. Crucially, the useful code
does not need to be supplied: the theorem below manufactures it directly
as the column space of h(B), and checks its decoding margin.

**Acquisition theorem.** Under these conditions, one deterministically
recovers the exact D and S from B, h and Δ in

\[
\operatorname{poly}(n+q)\,2^{qr}
\]

bit time and polynomial space. No original input coordinate is deleted,
and there is no condition involving r times the number of sparse edges.
Every returned decomposition is checked by exact matrix arithmetic.

For fixed q, h can itself be acquired by a constant-size portfolio of
all monic binary polynomials of degree at most q. For q=2 there are only
four monic quadratics, plus the two monic linear polynomials. A supplied
polynomial is therefore not an assumed decomposition.

The initial computational scope is a raw dense quadratic matrix plus
explicit fixed-locality factors in those same coordinates. The algebraic
condition h(S)=0 survives permutations and orthogonal coordinate changes.
It does not survive arbitrary congruence GSGᵀ. Consequently this result
does not automatically extend through arbitrary GL block gauges from the
cubic centroid compiler. No unknown metric is being assumed.

## 2. Why the raw polynomial h(B) reveals the code

**Lemma.** If W has full column rank, then

\[
h(B)=WHW^\top
\]

for an invertible symmetric qr by qr matrix H. In q by q blocks of size r,

\[
H_{ij}=0\quad(i+j>q-1),\qquad
H_{ij}=K\quad(i+j=q-1),
\]

where block indices run from zero to q−1. Therefore

\[
\operatorname{rank}h(B)=qr,\qquad
\operatorname{im}h(B)=\operatorname{im}W.
\]

**Proof.** Expand each power of B=S+D as a sum of noncommutative words.
The terms containing no D sum to h(S)=0. In every remaining word, write
the segment before the first D as S^i and the segment after the last D
as S^j. Substitution D=UKUᵀ factors that word as

\[
S^iU\,H_{ij}^{(\mathrm{word})}\,U^\top S^j.
\]

Its outer exponents satisfy i+j≤q−1. Equality is possible only for the
single-D terms of the leading power B^q, because h is monic. Every such
term is S^i U K Uᵀ S^j with i+j=q−1. Thus the asserted zero pattern and
anti-diagonal blocks follow.

The polynomial h(B) is symmetric. Since W has full column rank, its core
H in a factorization WHWᵀ is unique, so H is symmetric. Reverse the
block columns of H: the resulting matrix is block triangular with
invertible diagonal blocks K. Hence H is invertible. Finally W is
injective and Wᵀ is surjective, so WHWᵀ has rank qr and image im W.
This proves the lemma.

For a quadratic h(t)=t²+a t+b, the identity is especially explicit:

\[
h(B)=[U,SU]
\begin{bmatrix} K(U^\top U)K+aK&K\\ K&0\end{bmatrix}
[U,SU]^\top,
\]

Equivalently,

\[
h(B)=U[K(U^\top U)K+aK]U^\top
      +UKU^\top S+SUKU^\top.
\]

The block core is invertible whenever K is. This does not rely on a real or complex
eigendecomposition, spectral gap, incoherence oracle, or a known sparse
matrix.

## 3. Raw algorithm and exact certification

Compute h(B) by matrix polynomial evaluation and find a full-column-rank
basis V of its image by binary elimination. On the promised family V
has d=qr columns, although neither U nor W has been given.

Stream all 2^d codewords of im V using Gray-code enumeration. Find the
minimum nonzero Hamming weight. Reject this route if it is at most 2Δ.
For every observed column B_j, stream the codewords again and find a
codeword D'_j satisfying

\[
\operatorname{wt}(B_j-D'_j)\le\Delta.
\]

There is at most one, because two such codewords would differ by a
nonzero codeword of weight at most 2Δ. Under the theorem's hypotheses
the true D_j belongs to im U⊆im V, while B_j-D_j=S_j has weight at most
Δ. Therefore D'_j exists and equals D_j.

Assemble D', set S'=B-D', and verify:

- exact entrywise equality;
- symmetry of D' and S';
- the rank of D';
- the row-weight and off-diagonal edge budgets;
- h(S')=0.

The promised family recovers exactly its D and S. Outside that family,
any accepted output is still an exact, independently checked
representation; failed hypotheses cannot cause an incorrect count.

Matrix polynomial evaluation costs O(qn³) elementary binary operations
by ordinary multiplication. Rank and symmetry checks are polynomial.
The distance computation and n decodings cost O(n² 2^d) bit operations
with a conservative accounting, and all codewords can be streamed.
Storage is O(n²+nd+q) bits apart from polynomial indexing overhead;
there is no exponential codeword table.

If the annihilating polynomial is not supplied, enumerate the monic
polynomials through a degree budget q₀, compute each raw image rank
first, and discard images above a chosen code-dimension budget d₀.
The total acquisition bound is

\[
2^{q_0+1}\operatorname{poly}(n+q_0)\,2^{d_0}.
\]

Whenever a promised polynomial has degree q≤q₀ and qr≤d₀, its trial
succeeds. Degree and dimension budgets may be dovetailed by their
explicit work bound. Running an unfavorable full-rank code trial to
completion before trying a good polynomial would not justify the
promised complexity.

The implementation takes h and Δ as explicit trial parameters. These
are small integer/model budgets, not hidden matrix data.

## 4. Original-input exact counting

Consider the explicitly described phase sum

\[
Z=\sum_{x\in\mathbb F_2^n}
(-1)^{q_{\mathrm{off}(B)}(x)}
\prod_{j=1}^{m}\phi_j(x|_{A_j}),
\]

Every A_j has fixed size at most k and each local phase has a fixed
power-of-two root order. The input length L includes the raw n by n
quadratic matrix and every local factor; generally L is at least of
order n². The variable count is the original n.

After acquisition, let M=e(S) be its explicitly counted number of
off-diagonal edges. The residual contributes exactly M quadratic
factors, with M≤nΔ/2. The recovered symmetric D has rank r.
Use the preserved exact quadratic refinement and Gaussian-Walsh
expansion of its rank-r core. There are at most 2^r characters, and
every character changes only original-variable unary phases.

For a symmetric core K the fourth-root refinement includes the known
unary diagonal and Boolean substitution corrections; dropping these
corrections is invalid. Each inner local-phase answer is reconstructed
exactly before Gaussian multiplication and division by the Fourier
denominator. The numerator has O(n+r) bits in a fixed-dimensional
cyclotomic integer basis.

Writing F(n,m') for the preserved local-phase exponent, the complete
conditional bit bound is

\[
\operatorname{poly}(L+n+q)
\left(2^{qr}+2^{\,r+F(n,m+M+O(n))}\right).
\]

This is poly(L+n+q)2^o(n) with polynomial space when

\[
qr=o(n),\qquad
\log(2+(m+M)/n)=o(\log n).
\]

In particular fixed q, arbitrary r=o(n), and m+M=n^(1+o(1))
suffice, subject to the stated code margin. The stronger bounded-degree
condition Δ=n^o(1) is a convenient way to guarantee the sparse-edge
bound, but is not otherwise required by the counting statement.
Acquisition makes no rM=o(n²) demand.

This is an acquired restricted-family extension. It does not prove
generic dense-quadratic-plus-local counting, generic matrix rigidity
recovery, arbitrary-circuit SAT, or polynomial-time SAT.

## 5. A large explicit family: hidden sparse Cayley graphs

Let n=2^d and let S be the adjacency matrix of the d-dimensional
hypercube, with its vertices arbitrarily permuted. The d coordinate
translation matrices commute and square to the identity. In
characteristic two all cross terms in their square cancel, so

\[
S^2=(d\bmod2)I.
\]

Thus q=2, Δ=d=log₂n, and h(t)=t²+(d mod 2). The graph and its vertex
labelling are not supplied to the decoder.

Put c=d mod 2 and N=S+cI. Then N²=0 and rank N=n/2. For completeness,
use the usual two-halves hypercube recurrence

\[
N=\begin{bmatrix}C&I\\ I&C\end{bmatrix},
\qquad C=A_{d-1}+cI,\qquad C^2=I.
\]

Its kernel is exactly the set of pairs (x,Cx), so its nullity and
rank are both n/2. Permutations preserve this fact.

Choose an n by r matrix U with independent uniform binary entries,
where r is even, and a fixed invertible alternating r by r K.
Then D=UKUᵀ is alternating. Let V(n,t) denote the binary Hamming-ball
volume Σ_{j=0}^t binom(n,j).

For any coefficient pair (a,b)≠(0,0), the vector

\[
Ua+SUb
\]

is uniform on all F₂^n except for exactly 2^r−1 coefficient pairs,
when it is uniform on im N of dimension n/2. Indeed, independent a,b
give independent Ua,Ub. For dependent nonzero pairs over F₂ the
possibilities are a=0, b=0, or a=b. Of the two potentially singular
operators S and I+S, exactly the one equal to N is singular; the
other is invertible.

A union bound, including the zero vector in the bad ball, proves

\[
\Pr\{\operatorname{rank}[U,SU]<2r
\ \text{or}\ d_{\min}(\operatorname{im}[U,SU])\le2\Delta\}
\le
V(n,2\Delta)\left[
\frac{2^{2r}-2^r}{2^n}
+\frac{2^r-1}{2^{n/2}}\right].
\]

For r=o(n) and Δ=log₂n this is 2^(-Ω(n)). Thus the transversality
and decoding hypotheses are established with high probability for
an explicit broad family, not posited as a free code.

Take, for example, r asymptotic to n/log₂n, rounded to an even integer.
The hidden sparse error count is M=n log₂n/2, so rM is asymptotic to
n²/2. This lies outside the previous sufficient condition rM=o(n²).
The acquired-annihilator method costs 2^(2r) times a polynomial and
the conditional count remains subexponential in n.

The same proof works for a direct sum of a fixed number of equal
hypercubes, permitting n divisible by three if one wants disjoint
cubic triple foreground terms. Arbitrary fixed-locality foreground
factors are permitted; no compatible interaction decomposition is
assumed.

More generally, every binary Cayley adjacency matrix on an elementary
abelian 2-group satisfies S²=(degree mod 2)I. The decoder theorem
applies whenever its acquired code has the required margin. The
particular n/2-rank probability bound above is proved for hypercubes;
it is not being asserted for every generating set.

## 6. What fails, and why it is not a generic recovery theorem

The orbit-rank condition can fail completely. Let S be a perfect
matching within each of two equal even-sized vertex classes, and
let D be the adjacency matrix of the complete bipartite graph between
the classes. Then rank D=2, S²=I, D²=0 and SD=DS. Therefore

\[
(S+D)^2+I=0.
\]

The raw quadratic annihilator reveals the zero code and erases the
entire latent perturbation. The algorithm rejects because the dense
observed rows have no weight-one residual in that code. This is a
failure of this manufactured code, not a counting lower bound.
The older generic compiler still applies to that family.

Full orbit rank alone also does not imply an error-correcting margin.
With S a perfect matching, take U supported on two coordinates whose
partners are distinct. Then [U,SU] has rank four but spans coordinate
unit vectors, so its distance is one. Radius-one decoding is not
unique. This failure is checked separately in the executable.

The algebraic error condition and the margin are restricted-class
assumptions. An arbitrary sparse matrix will not have a small-degree
annihilating polynomial, and arbitrary dense changes of basis need
not preserve either sparsity or the ordinary matrix identity h(S)=0.

## 7. Equally informed alternatives and ancestry

The proof uses familiar matrix-polynomial/Krylov algebra, finite-field
linear codes, and nearest-codeword uniqueness. Those ingredients
are not new. The specific object examined here is the complete raw
compiler: h(B) reveals the perturbation orbit, the manufactured code
is certified, exact decoding recovers the unknown sparse part, and
the original-n phase counter consumes the result.

The strongest inspected general binary low-rank approximation
comparators do not supply the same parameter guarantee.

- Fomin, Golovach and Panolan, Parameterized low-rank binary matrix
  approximation, Data Mining and Knowledge Discovery 34 (2020),
  Theorem 6, give an exact algorithm with exponent of order
  r sqrt(k log(rk)), where k is the number of changed matrix entries.
  The 2020 theorem improves the preliminary 2018 exponent. It is a
  general matrix-approximation result, and does not assume the
  annihilator condition. Its displayed guarantee does not become
  subexponential in n at r≈n/log n, k≈n log n.
  https://fedorvf.github.io/articles/2020/2020f.pdf

- Kumar, Panigrahy, Rahimi and Woodruff, Faster Algorithms for Binary
  Matrix Factorization, ICML 2019, give a constant-factor binary-field
  approximation in 2^O(r³) poly(n) time with rank O(r log n).
  https://proceedings.mlr.press/v97/kumar19a/kumar19a.pdf

- Velingker, Vötsch, Woodruff and Zhou, Fast (1+ε)-Approximation
  Algorithms for Binary Matrix Factorization, ICML 2023, Theorem 3.2,
  give a randomized (1+ε) binary-field bicriteria approximation in
  2^poly(r/ε) poly(n) time, with rank O(r log r/ε). This is stronger
  than merely retaining the older log n rank inflation. Its stated
  parameter dependence still gives no original-n subexponential
  guarantee for the near-linear r regime here. A nonsymmetric
  approximation also requires a symmetry-preserving interface.
  https://proceedings.mlr.press/v202/velingker23a/velingker23a.pdf

A simple admissible symmetry repair is C=X∘Xᵀ. If X has rank t,
then C is symmetric of rank at most t², and for symmetric B,
Ham(B,C)≤2 Ham(B,X). This follows by checking each transpose pair
and expanding the entrywise product of two rank-t factorizations.
It is valid, but the rank square is not a solution at t≈n/log n.

These are comparisons of proved guarantees on the specified family,
not execution-based speed comparisons or proofs excluding every
hybrid of existing methods. A focused primary-source search did
not identify this complete annihilator-decoding compiler. That
search does not establish historical priority.

The governing phase source is the user-pinned OpenAI manuscript:
https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf
The saved phase proof is deliverables/Astra_P3_Constructive_Phase_Representations.tex,
and the Gaussian correction audit is
work_gaussian_cont/ROOT_IMPLEMENTATION_AND_DIAGONAL_REPAIR.md.

## 8. Executed work

The standard-library executable annihilator_acquisition.py receives
only the raw B, a polynomial trial h and the row-weight budget Δ.
Hidden matrices are used only by the independent fixture generator
and post-execution equality assertions.

Ten fixtures recovered the exact hidden D and S. They include:

- arbitrarily permuted matching errors on 12 and 16 variables;
- permuted hypercube errors on 32, 64, 128 and 512 variables;
- permuted unions of paths with annihilator degrees three through six.

For all ten, the program checked the full block-core factorization,
including the K anti-diagonal and zero blocks beyond it. It checked
20,000 pointwise quadratic identities and two complete mixed
quadratic/cubic phase counts over 69,632 assignments in total.

The largest instance had n=512, r=6, q=2, acquired code dimension 12,
code distance 219, sparse degree 9, and 2,304 sparse edges. Five
rejection cases include the explicit nontransversality and missing
decoding-margin failures above.

These are actual finite computations. The phase leaves are exhaustive;
the source manuscript's asymptotic phase engine was not executed.
The files annihilator_acquisition.py and
annihilator_acquisition_results.json preserve the program, inputs and
exact results.
