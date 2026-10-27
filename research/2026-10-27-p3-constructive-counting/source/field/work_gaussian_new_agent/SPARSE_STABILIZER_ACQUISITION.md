# Acquiring a sparse stabilizer interface for dense quadratic phases

27 October 2026. Acquisition and all finite identities are unconditional. The
subexponential counting conclusion depends on the preserved Astra P3 local-phase
extension of the pinned OpenAI manuscript. Finite code uses exhaustive leaves
or exact elimination of introduced linear constraints. It does not execute
that asymptotic phase engine. No practical speed or first-priority claim is made.

## 1. Acquired counting theorem

Input: an explicit alternating binary matrix B on n independent bits, and m
explicit Boolean phase factors of fixed locality k. Constant-size ANF expansion
gives their sum P. L includes the raw matrix and all factor descriptions.
In the quantitative bounds below, m denotes the resulting ANF monomial count;
this is at most 2^k times the initially supplied factor count.

    Z(B,P)=sum_x (-1)^[q_B(x)+P(x)],
    q_B(x)=sum_(i<j)B_ij x_i x_j.

B may be dense and full-rank. No decomposition, sparse inverse, change of
coordinates, or short stabilizer generators are given. Define

    C_B={(a,Ba):a in F_2^n}.

Joint support weight is wt(a OR z), X weight is wt(a), and Z weight is wt(z).
These weights have different computational roles.

**Theorem.** Given support limit w and X-cost budget A_0, a deterministic
polynomial-space algorithm acquires independent a_1,...,a_r with

    wt(a_i OR Ba_i)<=w,
    A:=sum_i wt(a_i)<=A_0,
    D:=sum_i wt(Ba_i)<=rw,
    delta:=n-r.

It expresses Z(B,P) as 2^delta exactly reconstructed fixed-local phase counts,
each on N=r+2A bits, with common denominator 2^A. Each count contains at most
m+3A+D+r+O(1) monomials of degree at most max(k,2). Acquisition costs

    poly(n) 2^[O(w log(en/w))]

for 1<=w<=n/2; generally use poly(n) sum_(j<=w) binom(n,j)2^j. Total bit time is

    poly(L+n+A_0)[2^[O(w log(en/w))]
                  +2^[delta+F(N,m+3A+D+r+O(1))]],

where F is the preserved local-phase exponent with its guarded exhaustive
fallback. Space is polynomial in the explicit input and acquired certificate.

**Hidden-witness guarantee.** Suppose C_B contains an independent family of
rank n-delta_* with total X weight <=A_0 and total joint weight W_*.
The family is only an existence promise, not supplied data. Then

    delta<=delta_*+floor(W_*/(w+1)).

Therefore exact original-n counting is subexponential if

    A_0=O(n), delta_*=o(n), W_*=n exp(o(log n)),
    m=n exp(o(log n)).

Choose w=n^o(1) growing faster than W_*/n. The defect is o(n), N=O(n), and
the factor count is n exp(o(log n)). Since every nonzero a has X weight>=1,
A>=r and N>=3r=Theta(n) in this regime. Thus the phase theorem is applied at
the correct variable scale. No rank bound on B or primitive cubic block size
is required; P is arbitrary within its stated locality and density.

Budgets are search parameters, not useful representations. Unknown budgets
can be handled by acquired prefixes and a polynomial-size dovetailed portfolio.
Exhausting an unfavorable exponential case before a good one would not prove
this bound.

## 2. Weighted acquisition

For a physical support U, a graph-code word is supported in U exactly when
a_(U^c)=0 and B[U^c,U]a_U=0. Gaussian elimination obtains this kernel.
Streaming all combinations of a kernel basis enumerates all supported words.
For X weight j=1,...,w, enumerate supports of size<=w, retain kernel vectors
with wt(a)=j, and feed them into linear-matroid greedy. Every short word occurs,
possibly repeatedly, in nondecreasing X weight.

Add a word exactly when it increases rank and fits the X budget. Stop when
the next independent word exceeds that budget; all later words cost at least
as much. Each prefix has minimum X cost among independent subsets of the same
size in the searched family.

An arbitrary kernel basis alone is insufficient for this weighted claim:
it spans the directions but may not minimize X weight. The implementation
explicitly streams its combinations in the weighted routine.

Delete from the hidden witness all words of joint weight>w. At most
floor(W_*/(w+1)) are deleted. The remaining independent family has the promised
rank and X cost<=A_0, and occurs in the search. Greedy reaches at least its
rank before its budget ends. This proves the witness guarantee.

The current support, kernel, coefficient counter, independence basis and at
most n selected vectors take polynomial space. Candidate count is bounded by
poly(n) sum_(j<=w) binom(n,j)2^j; no exponential table is stored.

The simpler unweighted variant enumerates supports in increasing size and
inserts arbitrary kernel basis vectors. A newly independent vector at support
size t has actual joint weight t, since smaller directions were already
spanned. This yields the minimum-joint-weight basis prefix. If a full minimum
basis has total weight W_min, a prefix of cost W and defect delta obeys
W+delta(w+1)<=W_min. The weighted theorem is stronger for counting because
numerous Z actions add no variables.

## 3. Exact stabilizer identity, with signs

Define

    K(a)|x>=(-1)^[q_B(a)+(Ba)·x]|x+a>
           =(-1)^q_B(a) X^a Z^(Ba)|x>.

The q_B(a) sign is necessary. Quadratic polarization implies
K(a)K(b)=K(a+b). The operators commute and square to identity. For any binary
basis a_1,...,a_n,

    product_j (I+K(a_j))|0>=sum_x (-1)^q_B(x)|x>.

No normalization occurs: basis selectors parametrize every x once. This is
established stabilizer algebra, written explicitly to track phases and costs.

Complete acquired vectors to a basis with d_1,...,d_delta. For each dense
selector eta put x_eta=sum_l eta_l d_l. Applying the dense factors first gives
(-1)^q_B(x_eta)|x_eta>. The unstructured complement costs 2^delta branches
but creates no long wire trace.

## 4. Variable-efficient phase compilation and arithmetic

The conditional action of a short generator, with selector lambda_j, is

    phase (-1)^[(Ba_j)_v lambda_j y_v],
    update y_v<-y_v+(a_j)_v lambda_j,

at coordinate v, plus its global sign (-1)^[q_B(a_j)lambda_j]. At a coordinate
with both X and Z, apply the Z phase to the OLD bit before the X update.

For each X update create state bit t and multiplier mu. The exact identity

    1_[t+y_v+lambda_j=0]
       =(1/2)sum_mu (-1)^[mu(t+y_v+lambda_j)]

adds two variables and at most three quadratic or unary monomials. Z-only
actions add one local monomial and no variables. Initial wire bits are the
known x_eta. Every final physical bit is a constant or its last state bit, so
the original P factors remain k-local.

There are exactly A X updates. Hence N=r+2A and common denominator 2^A.
Summing multipliers enforces a unique trace per selector. Over eta and lambda,
the final original x runs through F_2^n exactly once, proving the identity.

Reconstruct each signed phase sum exactly, sum branch numerators, and only
then divide by 2^A. Premature division of modular residues loses precision.
A conservative numerator bound is 2^(N+delta), so O(n+A) bits suffice.
The target lies in [-2^n,2^n]; output counts are (2^n+Z)/2 and (2^n-Z)/2.
Internal states are not original independent inputs.

Once acquisition succeeds, fixed-local counting is a composition with the
governing theorem. The changed scope is the acquired interface for a raw dense
quadratic description; Fourier enforcement is established machinery.

## 5. Unknown robust sparse inverse: a concrete covered family

Suppose B=Q^(-1)+S, where Q is invertible alternating, nnz(Q)=O(n), maximum
column degree Delta=n^o(1), and S has M=n exp(o(log n)) unordered edges.
Neither Q nor S is supplied. The rows of Q form hidden independent X vectors,
whose Z rows are Q B=I+QS. Total X cost is O(n); total Z cost is at most

    n+sum_v degree_Q(v)degree_S(v)<=n+2 Delta M.

The weighted acquisition theorem applies. B can have full rank and
Theta(n^2) entries. After adding S, its inverse need not remain sparse.
No low-rank completion, repeated response types or nonlinear centroid blocks
are required. More generally, the promise is an unknown invertible multiplier
A with nnz(A)=O(n), nnz(AB)=n exp(o(log n)); an o(n)-dimensional unstructured
complement is also allowed.

An equally informed ordinary method handles the uncorrupted sparse-inverse
case directly. For nonsingular B and gamma_B=sum_x(-1)^q_B(x)=+-2^(n/2),

    Z(B,P)=2^(-n)gamma_B
       sum_(a,y)(-1)^[q_B(B^(-1)a)+a·y+P(y)].

The transformed quadratic has polar B^(-1); the displayed expression retains
its unary correction. If B^(-1) is near-linear sparse, this is a local phase
count on 2n bits. The acquired compiler adds corrupted and partial-basis cases;
it does not claim to invent Gaussian Fourier duality.

## 6. Decisive generic boundary

For random alternating B, fix U of size u and nonzero a supported there.
The coordinates (Ba) outside U are independent uniform bits, so a word is
supported in U with probability 2^(-(n-u)). Union bounding gives

    Pr[nonzero word of joint weight<=epsilon n]
      <=sum_(u<=epsilon n)binom(n,u)(2^u-1)2^(-(n-u))
      <=2^[-n(1-H_2(epsilon)-2epsilon)+O(log n)].

At epsilon=1/8 this vanishes exponentially. Typical dense B therefore has
no sublinear-support word: this compiler with w=n^o(1) acquires rank zero.
This is a representation failure, not a general counting lower bound.
The relation delta_loc(G)+1=min_(a!=0)wt(a OR Ba) is established local-minimum-
degree theory. One must not assume every dense Gaussian phase has a sparse
stabilizer presentation. Earlier rank and response-type compilers remain useful.

### A proved separation from the small-primitive-block hypothesis

For every n>=7, consider the n-term cyclic foreground

    P_cycle(x)=sum_(i mod n) x_i x_(i+1) x_(i+2).

Its third-derivative tensor T has zero radical and centroid exactly F_2 I,
so it has one intrinsic primitive block of dimension n. The present theorem
handles it with any favorable quadratic background above; the latest
response-type theorem's small-block hypothesis fails on this infinite family.
This does not exclude all alternative older certificates or algorithms.

Proof: T(v,e_j,e_(j+2))=v_(j+1), so the radical is zero. If P is in the
centroid, then T(Pe_i,e_i,z)=T(e_i,e_i,Pz)=0. The contraction by e_i is the
nondegenerate alternating path form on coordinates i-2,i-1,i+1,i+2. Thus
column i of P vanishes at these four coordinates. For row r, the identity

    P_(r,i)=T(Pe_i,e_(r-1),e_(r+1))

transfers P to either of the last two slots. Since a contraction on two
coordinate vectors is zero unless their cyclic separation is 1 or 2,
the first transfer allows, apart from the diagonal, only i=r+3 after the
four already excluded positions are removed. The other allows only i=r-3.
These are distinct for n>=7. Every off-diagonal entry therefore vanishes.
Finally T(e_i,e_(i+1),e_(i+2))=1 forces all diagonal entries of P equal.
This proves the centroid assertion over F_2 directly.

## 7. Primary-literature comparison

* Hein, Eisert and Briegel, Multi-party entanglement in graph states,
  Phys. Rev. A 69, 062311 (2004), https://arxiv.org/abs/quant-ph/0307130 .
  Graph-state stabilizer and cut-rank ancestry.
* Cattaneo and Perdrix, Minimum Degree up to Local Complementation: Bounds,
  Parameterized Complexity, and Exact Algorithms, ISAAC 2015,
  https://arxiv.org/html/1503.04702v2 . Property 1 states the short-support
  cut-rank characterization; this is not a new invariant.
* Khesin, Lu and Shor, Universal graph representation of stabilizer codes,
  PRX Quantum 6, 040325 (2025), https://arxiv.org/abs/2411.14448 .
  Inspected full v3 text, Section IV.3, Theorem IV.12, treats minimum-weight
  generator replacement as a graph optimization game. The current abstract
  explicitly lists minimum-weight generator selection. No claim is made to
  originate weight reduction or optimize every code in polynomial time.
* Bravyi et al., Simulation of quantum circuits by low-rank stabilizer
  decompositions, Quantum 3, 181 (2019),
  https://quantum-journal.org/papers/q-2019-09-02-181/ . A strong comparator for
  Clifford-plus-diagonal computations. This theorem does not establish
  practical superiority over stabilizer-rank or tensor-network algorithms.

The focused search did not locate this precise sparse-X / near-linear-Z
acquisition interface with the governing phase counter. That does not prove
first priority. The completed construction combines weighted acquisition,
variable-efficient Pauli traces, and explicit final reconstruction.

## 8. Executed source and data

The acquisition functions in sparse_stabilizer_compiler.py receive only raw B
and search budgets; hidden witnesses enter validation code separately.
The program implements both objectives, dense completion, phase compilation,
original brute-force counting, constraint elimination and full phase enumeration.

The run passed 93 joint-weight prefix audits, 465 joint-budget audits, 138
minimum-X-weight prefix audits, 12 raw matrix counts and six corrupted
sparse-inverse/foreground pairs. It checked 278,796 pointwise trace identities and all
82,752 assignments across 261 compiled branches. Most branches in the latter
number are zero-variable branches of the unfavorable case; nontrivial phase
tests include Y signs, dense-completion branches and cubic foregrounds.
Five malformed inputs were rejected. Larger cases use exact constraint
elimination, not an asymptotic phase engine. Complete data are saved in
sparse_stabilizer_results.json.
The primitive-cycle calculation was independently executed for every n from
7 through 24, and cyclic foreground counts were run on all three corrupted
sparse-inverse matrices.
