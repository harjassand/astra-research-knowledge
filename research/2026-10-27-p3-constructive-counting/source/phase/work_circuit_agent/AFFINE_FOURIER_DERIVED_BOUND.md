# A derived exact-counting bound for fixed-width CNF with arbitrary affine program constraints

**Status:** a useful theoretical consequence of the supplied ETH theorem, standard Fourier projection, and standard disjoint affine branching. This is not a claim of a newly invented replacement-form compiler, historical priority, practical speed, or completion of the general circuit research objective.

## 1. Input model and exact statement

Let F be a k-CNF on n original Boolean inputs, where k≥2 is fixed. In addition, an arbitrary straight-line affine Boolean program may compute internal values from those same inputs using XOR, NOT and constants, with S internal states. Require a supplied list of its outputs to equal specified bits. Equivalently, after symbolic propagation, the extra constraints are

\[
Ax=b\quad\text{over }\mathbb F_2.
\]

The matrix A may be dense, have arbitrarily overlapping rows, and have any rank r. No sparsity, small rank, small width or graph decomposition is promised. Every affine program state has one uniquely determined value for each original x; the count is the number of original assignments x satisfying both requirements.

Let L be the full binary input-description length, including the CNF, affine program, output constraints, and variable/gate indices. An explicit matrix may instead be supplied, with its bits included in L. Since k is fixed, a direct gate-list representation has length O((mk+S+t)log(n+S+2)) for m clauses and t output tests. Explicit huge descriptions may dominate the running time; the statement keeps this polynomial input cost visible.

Define γ_k∈(1,2) by

\[
\sum_{j=1}^{k}\gamma_k^{-j}=1,
\qquad
\alpha_k=\log_2\gamma_k,
\qquad
\beta_k=\frac{\alpha_k}{1+\alpha_k}.
\]

Write

\[
\rho_*(n)=\frac{n\log\log(n+16)}{\sqrt{\log(n+16)}}.
\]

The harmless offset handles bounded inputs.

**Derived theorem.** Using Theorem 1.1 of the supplied 25 October 2026 ETH paper as a subroutine, the exact count can be obtained deterministically in polynomial space and

\[
\boxed{L^{O_k(1)}\,
\min\left\{2^{r+O_k(\rho_*(n))},\ \gamma_k^{n-r}\right\}}
\]

bit operations, with polynomial overhead absorbed in the leading factor. Consequently the worst case over arbitrary rank is

\[
\boxed{L^{O_k(1)}2^{\beta_k n+O_k(\rho_*(n))}.}
\]

The exponents are measured against the original n bits, independently of S. This is a single-exponential bound, not a subexponential bound for this unrestricted affine-constrained family.

| k | γ_k | α_k | β_k | 2^β_k |
|---:|---:|---:|---:|---:|
| 2 | 1.618033988750 | 0.694241913631 | 0.409765516982 | 1.328469878688 |
| 3 | 1.839286755214 | 0.879146421607 | 0.467843490799 | 1.383040583220 |
| 4 | 1.927561975483 | 0.946777246799 | 0.486330548786 | 1.400877251657 |
| 5 | 1.965948236645 | 0.975225336064 | 0.493728648706 | 1.408079361448 |
| 8 | 1.996031179735 | 0.997134256997 | 0.499282536216 | 1.413510437505 |

These decimals are explanatory; exact root definitions govern the theorem.

## 2. Compile all affine internal states without adding counting variables

Store each program value as a vector in F_2^(n+1): n linear coefficients and one constant. An XOR gate adds two vectors, a NOT gate flips the constant, and input x_i starts as its unit vector. This takes O(Sn) elementary bit operations with a naive bit-vector implementation and O(Sn) stored bits. Output comparisons give the rows of Ax=b.

Gaussian elimination either detects inconsistency, in which case the answer is zero, or constructs an equivalent independent r-row system. Straightforward elimination costs O(tn²) bit operations and polynomial space. Since t,n,S are bounded by the explicit description, all these costs are polynomial in L. The representation is manufactured from the given program; no hidden small linear summary is assumed. Its semantic validity follows inductively gate by gate.

This elementary affine compilation does not apply to arbitrary nonlinear intermediate states. That limitation is fundamental to the scope of this result.

## 3. Signed fixed-width counting follows from the source theorem

For a∈F_2^n define

\[
W_F(a)=\sum_{x\in\{0,1\}^n}F(x)(-1)^{a\cdot x}.
\]

**Lemma 1.** Every W_F(a) can be computed in L^{O_k(1)}2^{O_k(ρ_*(n))} deterministic bit operations and polynomial space, uniformly in a.

**Proof by a direct parsimonious encoding.** Let N_odd count assignments satisfying F and a·x=1. Then

\[
W_F(a)=\#F-2N_{\rm odd}.
\]

A single parity constraint on w≤n bits has a chain of at most w−1 binary XOR gates. Encode each XOR gate z=u⊕v by its four width-three clauses and pin the final output. The gate values are uniquely determined by the original bits. The new formula has at most 2n variables and m+O(n) clauses, of width max{k,3}. The supplied Theorem 1.1 therefore computes both counts within the claimed bound. The zero-support parity is handled directly. The one computation of #F can be shared across all a. ∎

The introduction of at most n internal variables here is harmless: only **one** parity is encoded per Fourier coefficient. Encoding all r dense parity constraints at once could require Θ(rn) internal variables and would lose this bound.

### Optional direct weighted use of the source construction

No parity gates are necessary if one uses the source's general tensor machinery. In Appendix D.3, the variable-group tensor for a selected incidence monomial replaces each variable's contribution by

\[
\sum_{x_v\in\{0,1\}}(-1)^{a_vx_v}x_v^{b_v}
=
\begin{cases}
1+(-1)^{a_v},&b_v=0,\\
(-1)^{a_v},&b_v>0.
\end{cases}
\]

This keeps every wire count and entry-evaluation bound unchanged. Fixed-variable branches receive their corresponding sign multiplier. Work modulo 2^(n+2) so that the final signed integer in [−2^n,2^n] has an unambiguous centered representative.

**The greedy parity-test selection in source Section 6 must remain unweighted.** Its elimination guarantee compares nonnegative numbers of surviving assignments. Signed counts can cancel and do not justify that greedy step. Only after the unweighted procedure has constructed an equivalent accepted set should the final evaluator apply the signs. This distinction prevents an unsound weighted shortcut. The direct parity-chain proof above avoids this issue entirely.

## 4. Fourier projection removes all dense equations at once

For the independent r-row system, character orthogonality gives

\[
\mathbf 1[Ax=b]
=2^{-r}\sum_{\lambda\in\mathbb F_2^r}
(-1)^{\lambda\cdot(Ax+b)}.
\]

Thus the desired count is

\[
\boxed{N(F,A,b)=2^{-r}\sum_{\lambda\in\mathbb F_2^r}
(-1)^{\lambda\cdot b}\,W_F(A^T\lambda).}
\]

Evaluate one character at a time using Lemma 1. Computing A^Tλ takes polynomial time. A signed coefficient lies in [−2^n,2^n], so any partial accumulator has absolute value at most 2^(n+r); n+r+2 signed bits suffice. The final numerator is divisible by 2^r exactly. Division is a bit shift on the nonnegative final numerator.

This uses 2^r signed-counting calls and only polynomial storage: the current selector λ, current character, one counter workspace, and one signed accumulator. It establishes the first branch of the theorem.

Fourier projection itself is standard finite-group character orthogonality. No novelty is claimed for it.

## 5. A stronger primal algorithm than enumerating the whole affine fiber

The straightforward primal alternative enumerates 2^(n−r) affine-fiber points. Standard disjoint branching improves this to γ_k^(n−r), still with polynomial space.

At a recursive call let the remaining affine space have dimension d. Restrict every literal in a clause to an affine function of its d free coordinates. If their simultaneous zero equations are inconsistent, the clause is true everywhere in this space and can be discarded. If every literal is identically zero, the call contributes zero.

Otherwise the simultaneous-zero locus is a nonempty affine subspace of codimension j, where 1≤j≤k. Choose j of the clause's affine literal functions ℓ_1,…,ℓ_j with independent linear parts. Consistency of their joint-zero equations guarantees that every other literal is a linear combination of these as an affine function, so the original clause is equivalent on the current space to

\[
\ell_1\vee\cdots\vee\ell_j.
\]

Partition its satisfying points into the **disjoint** cases

\[
\ell_1=1;quad
\ell_1=0,\ell_2=1;quad\ldots;\quad
\ell_1=\cdots=\ell_{j-1}=0,\ell_j=1.
\]

Their dimensions are respectively d−1,…,d−j. Recurse on every case and add counts. If every clause is already true on the residual space, return 2^d.

The branching recurrence has at most the characteristic growth

\[
T(d)\le\sum_{i=1}^{k}T(d-i)+\operatorname{poly}(L,n),
\]

with fewer branches when j<k and the obvious bounded-dimension base cases. Standard induction, or a γ_k^d branching potential, bounds the number of leaves by O_k(γ_k^d); depth at most n makes total overhead polynomially larger. Gaussian elimination and clause restriction at a node take polynomial bit operations. Depth-first traversal stores at most n polynomial-size affine systems; each accumulated count needs n+1 bits. This proves the second branch of the theorem.

This is the generalized Fibonacci branching principle already associated with Monien–Speckenmeyer and explicitly discussed for subspace satisfiability by Arvind–Guruswami. The disjoint partition makes the counting version valid; overlapping decision branches could not simply be added.

## 6. Combine the two algorithms without a rank promise

Run the Fourier and affine-branching algorithms in interleaved steps and stop when either completes. They compute the same exact integer. This incurs at most a constant time factor over the faster algorithm and the sum of two polynomial workspaces, so it yields the stated minimum without needing unknown constants in the source bound.

For any nonnegative g,

\[
\max_{0\le r\le n}\min\{r+g,\alpha_k(n-r)\}
\le\beta_kn+\beta_kg.
\]

Take g=O_k(ρ_*(n)), absorbing polynomial factors into L^{O_k(1)}. This proves the rank-independent bound.

The simpler pair “Fourier versus affine enumeration” would give 2^(n/2+o(n)). The disjoint affine recursion is a strictly stronger equally informed comparator and must be included.

## 7. Exact finite checks and their limits

`affine_fourier_checks.py` implements:

1. Gaussian reduction and affine parameterization;
2. original-input exhaustive counting;
3. the Fourier projection formula with each signed coefficient computed by **explicit exhaustive summation**;
4. disjoint affine-clause recursion;
5. symbolic propagation of a dense XOR program into its exact matrix.

It does **not** implement the source paper's subexponential counter, substitute a fake oracle, or assert practical subexponential execution. Finite execution validates the identities and compiler only.

All 65 cases passed. The collection covers every rank from zero to n for n=2,…,10, an inconsistent system, and a dense-program fixture. It encountered 1,603 negative Fourier coefficients, exercising cancellation and signed reconstruction.

For the dense family n=2r, take A=[I_r | J_r−I_r] over F_2. Each output has r inputs; a separate XOR chain per output uses

\[
S=r(r-1)=n(n-2)/4
\]

internal states. The executed n=14,r=7 instance has 42 internal XOR states, 56 original-plus-internal states, and rank seven. Symbolic propagation recovered A exactly. Direct enumeration, Fourier projection with 128 characters, and the disjoint recursion all returned count one. No performance claim is inferred from this small fixture or its particular count.

## 8. Primary-source comparison and novelty assessment

- **Governing source:** OpenAI, *The Exponential Time Hypothesis is False*, revised 25 October 2026, supplied PDF; Theorem 1.1 supplies the fast exact counter, Section 6 supplies unweighted parity-test selection, and Appendix D supplies the tensor/weighted route. Canonical pinned source: https://github.com/openai/math/blob/7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026/paper.pdf .
- **Arvind and Guruswami (2021/2022), *CNF Satisfiability in a Subspace and Related Problems*.** This is the same CNF-plus-arbitrary-affine-constraints problem, not a new problem family. Their primary preprint explicitly discusses generalized Fibonacci branching (including the deterministic φ^d algorithm for 2-Sub-Sat), randomized 1.5^d decision, and the 1.4312^n decision hybrid. Remark 5 discusses exact counting through switching-lemma decision trees and distinguishes it from the faster decision methods. Sources: https://eccc.weizmann.ac.il/report/2021/112/ and https://eccc.weizmann.ac.il/report/2021/112/download ; published conference record https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.IPEC.2021.5 .
- **Nagao, Seto and Teruyama (May 2026), *A Deterministic O*(2^(n/2))-time Algorithm for 2-CNF Satisfiability in a Subspace*, IEICE COMP2026-5.** The official abstract states a deterministic polynomial-space 2^(n/2) decision algorithm using a new branch-and-bound method. The abstract does not establish its exact-counting behavior, so it must not be silently treated as either an exact counter or an obsolete result. Official source: https://ken.ieice.org/ken/paper/20260521McuY/eng/ .

These searches do not establish an exhaustive priority claim. The displayed bound follows by combining known Fourier duality, known affine branching, and the newly supplied counting theorem. It is scientifically useful because it removes the Θ(rn) auxiliary-variable cost of naively encoding all dense XOR constraints. Nevertheless, it is a relatively short derived consequence, not the new constructive machinery sought in the research assignment. It should remain a benchmark and a possible ingredient for a stronger compiler.
