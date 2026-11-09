# Completed Xi return — 12588d87-cf4b-470e-95b6-0ad85aa7c422

Source: https://chatgpt.com/c/6af15f26-6528-83ec-9e3c-adc51c6e40c3
Model: GPT-6 standard, Extra High. Exact prompt reference: P1_371B_EXACT_SUPPLIED_PROOF_BODY.txt.

No producer ZIP visible.

## Visible activity

I’ll continue from the accepted constructions and limits rather than reprove them. I’ll investigate a different route through exact signed spectral constraints, check current literature for a general construction or obstruction, and test any promising claim against the full variable-degree, polynomial-bit requirement.

Developed theorem and constructed product signings

Extended the construction

Searched 15 websites

Constructed sharp-signing Cartesian graph products

Validated examples and formulated and consolidated a theorem

Searched 6 websites

Analysis paused (visible interface indicator).

## Complete response

# P1 continuation — a new algebraic signing construction

(Full assertion still unresolved)

I investigated a different mechanism from the accepted Walsh, Paley, linear-phase and polynomial-interlacing constructions: **anticommuting signed adjacency operators on Cartesian graph products**\.

It yields a precise deterministic construction, including nonbipartite Ramanujan examples, but it does not extend to every prescribed Ramanujan base.

## 1\. New constructive theorem: graded Cartesian signing

**Theorem.** Let \(H\) be a finite bipartite graph with maximum degree \(a\ge3\), and \(K\) any finite graph with maximum degree \(b\ge3\)\. Suppose polynomial-bit algorithms produce signings \(S_H,S_K\) satisfying

\[
\|S_H\|\le2\sqrt{a-1},
\qquad
\|S_K\|\le2\sqrt{b-1}.
\]

Then there is a deterministic polynomial-bit signing of the prescribed Cartesian product \(G=H\square K\) satisfying

\[
\boxed{\|S_G\|\le2\sqrt{a+b-2}
<2\sqrt{a+b-1}.}
\]

Importantly, the signed spectral bounds combine **quadratically**, not additively.

### Construction

Let \(P\) be the diagonal bipartition matrix of \(H\)\: its entries are \(+1\) on one side and \(-1\) on the other. Bipartiteness gives

\[
PS_H=-S_HP.
\]

Define

\[
\boxed{S_G=S_H\otimes I_K+P\otimes S_K.}
\]

This is a valid undirected-edge signing of \(H\square K\)\.

The first term assigns signs to edges within the \(H\) direction. The second assigns signs to edges within the \(K\) direction, multiplied by the bipartition sign of the \(H\) coordinate.

Every nonzero entry corresponds to exactly one original edge, and each sign belongs to \(\{\pm1\}\)\.

### Proof

Squaring,

\[
\begin{aligned}
S_G^2
={}&S_H^2\otimes I
+S_HP\otimes S_K\\
&+PS_H\otimes S_K
+P^2\otimes S_K^2.
\end{aligned}
\]

The mixed terms cancel because \(S_HP+PS_H=0\), and \(P^2=I\)\. Hence

\[
\boxed{S_G^2=S_H^2\otimes I+I\otimes S_K^2.}
\]

Both summands are positive semidefinite, commute, and act on separate tensor factors. Therefore

\[
\|S_G\|^2=\|S_H\|^2+\|S_K\|^2.
\]

Applying the assumed bounds proves the theorem.

There are no approximate comparisons or continuous optimization steps. Given the two input signings, the construction costs polynomially many bit operations in the explicit product graph size.

### Constructive implication

The bipartite factor \(H\) can be signed using Xu's deterministic polynomial-bit algorithm. Thus, for any explicitly signable graph \(K\), the theorem gives a polynomial-bit signing of every Cartesian product \(H\square K\)\.

If \(K\) contains an odd cycle, the product is nonbipartite. When the product also satisfies the unsigned Ramanujan promise, this gives a genuine sharp signing of that prescribed nonbipartite Ramanujan graph.

This is a closure property of a **structured family of signable graphs**, not the unrestricted closure asserted in P1.

## 2\. An explicit nonbipartite Ramanujan example

Consider

\[
G=K_{3,3}\square K_3.
\]

It has 18 vertices, is 5-regular, and is nonbipartite.

### Verify the unsigned Ramanujan promise

The spectrum of \(K_{3,3}\) is

\[
\{3,-3,0^{(4)}\},
\]

and that of \(K_3\) is

\[
\{2,-1^{(2)}\}.
\]

The Cartesian-product spectrum consists of all pairwise sums\:

\[
\boxed{\operatorname{spec}(G)
=\{5^{(1)},2^{(6)},(-1)^{(9)},(-4)^{(2)}\}.}
\]

Since the Ramanujan threshold is

\[
2\sqrt{5-1}=4,
\]

all nontrivial eigenvalues satisfy the promise, including the eigenvalue \(-4\) exactly at the boundary.

### Explicit sharp signing

For \(K_{3,3}\), use the signed biadjacency matrix

\[
T=
\begin{pmatrix}
1&1&1\\
1&1&-1\\
1&-1&1
\end{pmatrix}.
\]

Its singular values are \(2,2,1\)\. Consequently, the corresponding symmetric signed adjacency matrix \(S_H\) satisfies \(\|S_H\|=2\)\.

For \(K_3\), take every edge sign positive, giving \(\|S_K\|=2\)\. Although \(K_3\) has degree two, the same tensor identity applies.

The constructed product signing therefore obeys

\[
\boxed{
\|S_G\|=\sqrt{2^2+2^2}=2\sqrt2<4.
}
\]

In fact, its full spectrum is

\[
\operatorname{spec}(S_G)
=
\left\{
(2\sqrt2)^{(2)},
(-2\sqrt2)^{(2)},
(\sqrt5)^{(6)},
(-\sqrt5)^{(6)},
(\sqrt2)^{(1)},
(-\sqrt2)^{(1)}
\right\}.
\]

Thus we obtain a certified 36-vertex, connected, nonbipartite, 5-regular Ramanujan 2-lift preserving precisely the prescribed 18-vertex base.

Unlike the earlier XOR-Cayley flat construction, this signing does not require all signed eigenvalues to have the same absolute value.

## 3\. Why this construction does not close the full problem

The construction extends algebraically to products of several signable factors using appropriate grading operators. However, **signability of a product and the unsigned Ramanujan property of that product are different requirements**\.

For example, let \(H\) be a sequence of connected, \(a\)\-regular bipartite graphs with increasing vertex counts, and let \(K\) be a fixed connected \(b\)\-regular graph.

The unsigned Cartesian product has a nontrivial eigenvalue

\[
b+\lambda_2(H).
\]

For fixed \(a\ge3\), the Alon–Boppana lower bound gives asymptotically

\[
\lambda_2(H)\ge2\sqrt{a-1}-o(1).
\]

But

\[
b+2\sqrt{a-1}>2\sqrt{a+b-1}
\]

for every \(b\ge1\) and \(a\ge3\)\.

Therefore sufficiently large members of these fixed-degree Cartesian-product sequences fail the unsigned Ramanujan promise, regardless of their excellent signed spectra.

This rules out a straightforward attempt to turn the tensor construction into a universal fixed-degree Ramanujan tower.

## 4\. Additional literature finding

A recent paper dated October 29, 2026, urlStrongly explicit Ramanujan 2-lift towers via Hilbert modular formshttps://arxiv.org/abs/2610.39485, constructs infinite nonbipartite Ramanujan 2-lift towers for certain degrees \(p+1\), using arithmetic methods. citeturn667093view0

This is relevant progress on explicit nonbipartite towers, but the advertised construction starts from particular arithmetic graph families. It does not establish that an arbitrary supplied Ramanujan graph admits the required signing, nor does its fixed-\(p\) complexity statement establish a uniform polynomial-bit algorithm for variable \(d\)\.

The distinction remains important: constructing infinitely many excellent graphs does not imply closure for **every prescribed base**\.

## 5\. Assessment and next mathematical barrier

The new tensor construction provides an exact operation under which sharp signed spectral control is preserved with a strict margin. Its hypotheses and bit costs are explicit. But it does not presently yield a reduction from arbitrary nonbipartite Ramanujan graphs to the constructive bipartite theorem.

A full positive still requires a uniform way to handle sign frustration on arbitrary interacting odd cycles while controlling both extreme eigenvalues simultaneously. A full negative instead requires an all-signings obstruction inside an unsigned Ramanujan graph.

Neither follows from the new construction or the available literature.

\[
\boxed{\text{P1 FULL STATUS: UNRESOLVED}}
\]

**New result in this continuation\:** a constructive graded Cartesian-product signing theorem with exact squared-norm composition, together with an explicitly certified nonbipartite Ramanujan base and its sharp 2-lift.

**Not established\:** a polynomial-time sharp signing algorithm for all promised inputs, or any valid promised-base counterexample.
