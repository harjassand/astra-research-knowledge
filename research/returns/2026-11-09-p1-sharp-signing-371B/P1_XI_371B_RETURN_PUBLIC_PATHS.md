# P1 Xi completed return — 371b729e

Source: https://chatgpt.com/c/6af15f26-6528-83ec-9e3c-adc51c6e40c3
Model: GPT-6 standard, Extra High. Exact prompt: P1_FULL_PRESCRIBED_RAMANUJAN_BASE_LIFT_XI_20261109.txt.

No producer ZIP visible. The accessible activity tree omitted two inline math expressions, noted below.

## Visible activity

I’ll check the four specified versioned papers first, then work on the remaining nonbipartite Ramanujan-base case. I’ll distinguish a polynomial-time construction, a counterexample, and partial structural results; the existing bipartite theorem and non-Ramanujan obstruction do not settle this question. Assessed constructions and spectral signing bounds to evaluate the remaining gap

Searched 16 websites

The specified papers confirm that the unrestricted signing conjecture is false, but its published counterexample is not Ramanujan. The sharp polynomial-time result applies to bipartite bases. The remaining question is whether the Ramanujan promise alone guarantees a sharp two-sided signing for every nonbipartite base; none of the four papers establishes that. Clarified the conclusion

Searched 1 website

Clarified the conclusion

Analyzed explicit Ramanujan signings and sharp spectral bounds

Reviewed the mathematical gap, scope, and direction

Searched 1 website

Tested perfect-matching signings for cubic Ramanujan graphs

Assessed the problem

Searched 10 websites

Condensed the approach and evaluated the remaining gap

Computed symbolic interlacing obstruction and verified Ramanujan signing counterexamples

I’ve also checked a separate algebraic construction: a 16-vertex, nonbipartite, 5-regular Ramanujan graph admits a signing whose square is exactly [inline expression not accessible], so its signed eigenvalues are all [inline expression not accessible]. I’m checking how far that construction generalises and separating it from the still-missing uniform theorem. Assessed progress and sharpened partial results

Classified XOR Cayley signings using linear phases

## Complete response

# Constructive Ramanujan 2-lift closure: research result

(Full assertion unresolved)

The four specified versioned papers have been checked against their governing results. They establish neither a polynomial-time sharp signing algorithm for every prescribed nonbipartite Ramanujan graph nor a Ramanujan-base counterexample.

In particular\:

- **Bipartite bases\:** solved constructively, with the strict sharp bound and polynomial bit complexity. citeturn189440view1
- **Arbitrary nonbipartite bases\:** the original universal assertion is false, but Xu's counterexample violates the Ramanujan input promise. citeturn189440view2
- **General approximate signing\:** the best applicable supplied constructive guarantee is \(2\sqrt{2(d-1)}\), not \(2\sqrt{d-1}\)\. citeturn189440view0
- **Mixed-root selection\:** improves an existential approximation, but does not enforce the required two-sided bound. citeturn189440view3

I have, however, obtained an explicit sharp construction for an infinite, variable-degree family of prescribed **nonbipartite Ramanujan bases**, described below. It preserves every original edge and uses polynomial bit resources.

## 1\. Constructive positive theorem for dense Ramanujan bases

**Theorem.** Let \(G\) be any connected simple \(d\)\-regular graph on \(n\ge64\) vertices satisfying

\[
0\le t:=n-1-d\le \frac{\sqrt n}{4}.
\]

There is a uniform deterministic algorithm producing one sign per original undirected edge such that

\[
\boxed{\|A_s\|_{\mathrm{op}}<2\sqrt{d-1}.}
\]

The algorithm uses \(O(n^2\log n)\) elementary bit operations under a straightforward implementation, and polynomial working memory. It does not require a Ramanujan or spectral oracle.

Moreover, every graph in this class is automatically nonbipartite and Ramanujan.

### Explicit signing algorithm

Set \(N=2^{\lceil\log_2n\rceil}\)\. Label the vertices \(0,\ldots,n-1\), using their binary representations. For every original edge \(\{u,v\}\), output

\[
\boxed{s_{\{u,v\}}=(-1)^{\operatorname{popcount}(u\mathbin{\&}v)}.}
\]

Here `&` denotes bitwise AND and `popcount` counts set bits. This assigns exactly one common sign to both copies of an edge in the resulting 2-lift.

### Proof of the spectral bound

Define the symmetric Walsh–Hadamard matrix \(H_N\) by

\[
(H_N)_{uv}=(-1)^{\langle u,v\rangle_{\mathbb F_2}}.
\]

It satisfies

\[
H_N^2=NI,\qquad \|H_N\|_{\mathrm{op}}=\sqrt N.
\]

Let \(H\) be its leading \(n\times n\) principal submatrix. Write \(D=\operatorname{diag}(H)\), and let \(C\) contain the Walsh entries corresponding to missing edges, with zeros elsewhere.

The output signed adjacency matrix is exactly

\[
A_s=H-D-C.
\]

Since principal compression cannot increase operator norm,

\[
\|H\|\le\sqrt N.
\]

Also \(\|D\|=1\), and \(C\) is symmetric with at most \(t\) nonzero entries of magnitude one in each row. Consequently,

\[
\|C\|\le t.
\]

Therefore

\[
\boxed{\|A_s\|\le\sqrt N+1+t.}
\]

Now \(N\le2n\)\. For \(n\ge64\) and \(t\le\sqrt n/4\),

\[
\sqrt N+1+t
\le\left(\sqrt2+\frac38\right)\sqrt n,
\]

whereas

\[
2\sqrt{d-1}
=2\sqrt{n-2-t}
\ge\frac{\sqrt{15}}2\sqrt n.
\]

The strict numerical inequality

\[
\sqrt2+\frac38<\frac{\sqrt{15}}2
\]

proves the claimed sharp bound.

### Why these inputs are Ramanujan

The complement \(\overline G\) is \(t\)\-regular and

\[
A(G)=J-I-A(\overline G).
\]

On the subspace perpendicular to the all-ones vector, \(J=0\)\. Every nontrivial eigenvalue of \(A(G)\) consequently has absolute value at most \(t+1\), which is strictly smaller than \(2\sqrt{d-1}\) in the stated range.

Furthermore \(d>n/2\), so \(G\) is connected and contains a triangle. It is therefore nonbipartite.

This gives a genuine polynomial-time sharp signing theorem for an infinite subclass satisfying the exact input promise.

It does **not** resolve the unrestricted case, since it requires \(n-1-d=O(\sqrt n)\)\.

## 2\. All complete Ramanujan bases admit explicit sharp signings

The same construction extends to every complete graph \(K_n\), including the small cases.

**Corollary.** For every \(n\ge4\), the prescribed nonbipartite Ramanujan graph \(K_n\) has a deterministic, polynomial-bit computable signing with

\[
\|A_s\|<2\sqrt{n-2}.
\]

For \(n\ge6\), use the Walsh signing above. If \(N\) is the smallest power of two at least \(n\), then

\[
\|A_s\|\le\sqrt N+1<2\sqrt{n-2}.
\]

To check the inequality uniformly, for \(N\ge16\) use \(n\ge N/2+1\), which reduces it to

\[
N-2\sqrt N-5>0.
\]

The remaining \(N=8,\ n=6,7,8\) cases satisfy the bound directly.

For \(K_4\), the following symmetric signing, with zero diagonal, has characteristic polynomial \((x^2-5)(x^2-1)\)\:

\[
A_s=
\begin{pmatrix}
0&1&1&1\\
1&0&-1&-1\\
1&-1&0&1\\
1&-1&1&0
\end{pmatrix}.
\]

Thus \(\|A_s\|=\sqrt5<2\sqrt2\)\.

For \(K_5\), use

\[
A_s=
\begin{pmatrix}
0&1&1&1&1\\
1&0&-1&-1&-1\\
1&-1&0&-1&-1\\
1&-1&-1&0&1\\
1&-1&-1&1&0
\end{pmatrix}.
\]

Its characteristic polynomial is

\[
(x-1)^2(x+1)(x^2+x-8),
\]

so

\[
\|A_s\|=\frac{1+\sqrt{33}}2<2\sqrt3.
\]

All complete graphs therefore satisfy the requested sharp signing property constructively. This result covers a particular class of nonbipartite bases, not arbitrary Ramanujan bases.

## 3\. A further obstruction to the direct two-sided interlacing strategy

There is a stronger limitation than merely observing that one signing of \(K_8\) is bad.

Consider the natural doubled characteristic polynomial

\[
P_G(x)=\mathbb E_s\det(x^2I-A_s^2),
\]

where the expectation is over independent uniform undirected edge signs.

For the nonbipartite Ramanujan graph \(G=K_5\), exact expansion gives

\[
\begin{aligned}
P_{K_5}(x)={}&x^{10}-20x^8+130x^6\\
&-340x^4+365x^2-88.
\end{aligned}
\]

Set \(y=x^2\)\. The resulting degree-five polynomial is

\[
F(y)=y^5-20y^4+130y^3-340y^2+365y-88.
\]

Its exact discriminant is

\[
\operatorname{Disc}(F)=-1\,476\,403\,200\,000<0.
\]

In particular, \(F\) has nonreal roots, and therefore the averaged doubled characteristic polynomial is **not real-rooted**\.

The calculation can be reproduced by switching all four edges incident to a designated vertex to \(+1\), enumerating the remaining six edge signs, and averaging the resulting 64 determinants. Vertex switching leaves \(\det(x^2I-A_s^2)\) invariant.

**Consequence\:** The direct strategy of applying a standard real-rooted interlacing-family selection argument to these doubled characteristic polynomials fails already on the valid Ramanujan base \(K_5\)\.

This is a proof of failure of that particular polynomial mechanism, **not** a counterexample to Ramanujan 2-lift closure. Indeed, the explicit \(K_5\) signing above satisfies the sharp bound.

## 4\. A sharper construction using conference matrices

For a second infinite family of dense bases, the Walsh bound can be improved.

Suppose \(n=q+1\), where \(q\equiv1\pmod4\) is prime. The symmetric Paley conference matrix \(C\) of order \(q+1\) has zero diagonal, off-diagonal entries in \(\{\pm1\}\), and

\[
C^2=qI.
\]

It is explicitly computable using quadratic residues modulo \(q\)\. Index its rows by \(\{\infty\}\cup\mathbb F_q\), with

\[
C_{\infty,x}=1,\qquad C_{x,y}=\chi(x-y)\quad(x\ne y),
\]

where \(\chi\) is the Legendre symbol.

For any prescribed regular graph \(G\) on these vertices, restrict the signs of \(C\) to its existing edges. If its complement has degree \(t\), then

\[
\boxed{\|A_s(G)\|\le\sqrt{n-1}+t.}
\]

This follows because the matrix of deleted entries has operator norm at most \(t\)\.

Thus the construction is sharp whenever

\[
\sqrt{n-1}+t\le2\sqrt{n-t-2}.
\]

In particular, it works for every such \(n\ge64\) satisfying

\[
t\le\frac34\sqrt n.
\]

All computations, including primality checking, Legendre symbols, and comparison of the spectral bound, have polynomial bit complexity in the explicit input length. The input graph is unchanged.

This extends the dense positive region for infinitely many graph orders, although it still does not reach general sparse Ramanujan graphs.

## 5\. Exact nonbipartite example with a flat signed spectrum

A different construction works for a sparse Ramanujan base.

Let \(V=\mathbb F_2^4\)\. Form the 5-regular graph with edges corresponding to addition by

\[
e_0,\ e_1,\ e_2,\ e_3,\quad g=e_0+e_1+e_2+e_3.
\]

This is a connected, nonbipartite, simple graph on 16 vertices.

Its unsigned adjacency spectrum is exactly

\[
\operatorname{spec}(A)
=
\{5^{(1)},1^{(10)},(-3)^{(5)}\}.
\]

Hence it is Ramanujan, since its nontrivial eigenvalues have absolute value at most \(3<4=2\sqrt{5-1}\)\.

Define the signs for \(x=(x_0,x_1,x_2,x_3)\) by

\[
s_{\{x,x+e_i\}}
=(-1)^{\sum_{j<i}x_j},
\qquad 0\le i\le3,
\]

and

\[
s_{\{x,x+g\}}=(-1)^{x_0+x_2}.
\]

These assignments are consistent on undirected edges.

**Exact identity\:**

\[
\boxed{A_s^2=5I_{16}.}
\]

To prove it, write \(A_s=U_0+\cdots+U_4\), where each \(U_i\) is the signed translation associated with a generator. The formulas give

\[
U_i^2=I,\qquad U_iU_j=-U_jU_i\quad(i\ne j).
\]

Every cross term cancels when the sum is squared.

Consequently,

\[
\operatorname{spec}(A_s)
=
\{(\sqrt5)^{(8)},(-\sqrt5)^{(8)}\},
\]

and

\[
\|A_s\|=\sqrt5<4.
\]

The resulting 32-vertex 2-lift is therefore a connected, nonbipartite, 5-regular Ramanujan graph.

### Generalisation

This algebraic construction has a polynomial-time recognition-and-construction criterion for XOR-labelled Cayley graphs on \(\mathbb F_2^k\)\.

Let the distinct nonzero generators be \(g_1,\ldots,g_d\)\. Seek binary vectors \(a_1,\ldots,a_d\) satisfying

\[
a_i\cdot g_i=0,\qquad
a_i\cdot g_j+a_j\cdot g_i=1
\quad(i\ne j),
\]

over \(\mathbb F_2\)\.

These are linear equations. Whenever they are solvable, the signing

\[
s_{\{x,x+g_i\}}=(-1)^{a_i\cdot x}
\]

has \(A_s^2=dI\)\.

In fact, this phase-linear construction is feasible precisely when every binary dependence \(w\) among the generators satisfies

\[
\binom{|w|}{2}\equiv0\pmod2,
\]

or equivalently, every such dependence has Hamming weight congruent to \(0\) or \(1\pmod4\)\. This follows by expressing the anticommutation conditions as a bilinear form whose quadratic form is \(\sum_{i<j}w_iw_j\)\. The vanishing of that quadratic form on the relation space is both necessary and sufficient for the corresponding bilinear extension.

The condition can be checked from a kernel basis using binary Gaussian elimination. It provides another polynomial-time sharp-signing subcase, but it is not a criterion for general graphs, nor a necessary condition for ordinary sharp signability.

## 6\. Exact general decision procedure — but exponential time

There is a uniform exact-arithmetic procedure that distinguishes successful signings from all-signings obstructions for any finite input graph.

For a candidate signing, form the integer matrix

\[
M_s=4(d-1)I-A_s^2.
\]

The requested property is precisely

\[
\boxed{M_s\succeq0.}
\]

This can be decided with polynomial bit complexity, without numerical eigenvalue approximations.

For example, compute

\[
h_s(z)=\det(zI+M_s).
\]

Because \(M_s\) is real symmetric, it is positive semidefinite if and only if every coefficient of \(h_s\) is nonnegative. Indeed, a negative eigenvalue of \(M_s\) would give a positive root of \(h_s\), which is impossible for a polynomial with nonnegative coefficients and positive leading coefficient.

Vertex switching further reduces the search space. Fix a spanning tree and switch all its edges to \(+1\)\. The remaining independent signs number

\[
m-n+1=\frac{dn}{2}-n+1.
\]

Thus exact feasibility is decidable in

\[
2^{m-n+1}\operatorname{poly}(B)
\]

bit time and polynomial working space.

This is an exact finite decision algorithm, but its exponential time disqualifies it as a full positive under the requested computational contract.

## 7\. What remains unproved

The research now separates into three cases\:

| Input class | Established outcome |
|--------|--------|
| Arbitrary prescribed bipartite graph | Sharp deterministic polynomial-bit signing, from Xu |
| Dense nonbipartite Ramanujan bases, complete bases, and the algebraic examples above | Explicit sharp polynomial-bit constructions |
| Every other prescribed nonbipartite Ramanujan base | **Unresolved** |

The outstanding difficulties are substantive.

First, the Ramanujan promise controls the unsigned spectrum but does not ensure that partially constructed signed adjacency matrices retain either spectral constraint. The two-sided repair argument still incurs the factor of two in its deletion analysis. citeturn189440view0

Second, the usual one-sided characteristic-polynomial method does not automatically become a two-sided method. The \(K_5\) calculation above provides an explicit failure of the most direct doubled-polynomial averaging construction, even under the Ramanujan promise.

Third, Xu's all-signings obstruction is not transferable unchanged: its completed seeds create an unsigned nontrivial eigenvalue greater than \(2\sqrt2\)\. Specifically, Proposition 7.1 gives

\[
\lambda_2(A(F))
\ge3-\frac1{2^{65}+1}>2\sqrt2.
\]

citeturn189440view2

Finally, the constructions developed here do not supply a procedure for sparse Ramanujan bases of arbitrary degree. They establish additional positive subclasses, not a way of choosing signs on every promised graph.

## Final determination

\[
\boxed{
\begin{gathered}
\text{The full constructive Ramanujan-base}\\
\text{2-lift closure assertion remains OPEN.}
\end{gathered}}
\]

**Strongest established output of this investigation\:** explicit, polynomial-bit sharp signings for infinite families of prescribed nonbipartite Ramanujan bases; a spectral-flat algebraic construction; an exact failure certificate for direct doubled-polynomial interlacing; and a general exponential-time, polynomial-space feasibility decision method.

None proves that every prescribed Ramanujan base is signable, and none supplies a promised-base all-signings counterexample. I therefore cannot claim either a full positive or a full negative.

The four governing versioned sources were directly inspected\:

- urlJadbabaie–Saberi–Sra, v1 — Randomized repair and exact arithmetichttps://arxiv.org/html/2609.23855v1
- urlXu, v3 — Deterministic bipartite constructionhttps://arxiv.org/html/2610.09972v3
- urlXu, v4 — Cubic counterexample and non-Ramanujan proofhttps://arxiv.org/html/2609.15591v4
- urlLin–Zhou, v2 — Mixed-root bounds and K8 obstructionhttps://arxiv.org/html/2609.15715v2
