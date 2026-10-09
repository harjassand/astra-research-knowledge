# Recursive falsifier for Han's absolute-edge coordinate-selection criterion

## Exact target

For a Boolean function define
\[
A_i(f)=\sum_{S\not\ni i}|\widehat f(S)\widehat f(S\cup\{i\})|.
\]
Xiao Han's Question 3.1 in arXiv:2312.08271v2 asks whether there is a
dimension-free constant \(C\) such that every Boolean \(f\) has at least
one coordinate \(i\) with \(A_i(f)\le C I_i(f)\). The paper says it can
neither prove nor disprove this. A balanced monotone block-composition family
gives an exact negative answer to that auxiliary question:
\[
\min_i \frac{A_i(F_k)}{I_i(F_k)}=\frac{k+1}{2}
=\frac14\log_2 n(F_k),
\qquad n(F_k)=4^{k+1}.
\]
This does **not** disprove FEI. It only falsifies this proposed sufficient
one-coordinate absolute-edge induction criterion; the entropy-increment
criterion itself is a different statement.

## Seed gate

On variables \(x_1,x_2,x_3,x_4\), define \(h=+1\) if either at least
three variables are +1, or exactly two are +1 and the positive set is one
of \(\{1,2\},\{3,4\},\{1,3\}\); otherwise \(h=-1\). Its +1 set is an
up-set of size \(1+4+3=8\), so \(h\) is balanced and monotone.
The exact nonzero spectrum is
\[
\begin{array}{c|rrrrrrrrrr}
S&1&2&12&3&23&123&4&14&34&134\\\hline
\widehat h(S)&1/2&1/4&1/4&1/2&-1/4&-1/4&1/4&-1/4&1/4&-1/4.
\end{array}
\]
The singleton coefficients and coordinate influences are both
\((1/2,1/4,1/2,1/4)\). Directly,
\[
(A_1,A_2,A_3,A_4)=(1/4,1/4,1/4,1/4),
\]
so the seed local ratios are \((1/2,1,1/2,1)\). Every coordinate is
essential.

## Coordinate-wise composition identities

Let \(h\) be balanced and \(F=g(h_1,\ldots,h_n)\) for disjoint copies of
\(h\). For coordinate \(j\) in the outer function and coordinate \(r\)
inside its copy of \(h\), uniqueness of active Fourier blocks gives
\[
A_{(j,r)}(F)=I_j(g)A_r(h)+|\widehat h(\{r\})|A_j(g),
\qquad
I_{(j,r)}(F)=I_j(g)I_r(h).
\]
For the first identity, split adjacent spectral pairs inside block \(j\):
if both local frequencies are nonempty, the outer block set is unchanged,
and summing its squared coefficient weight gives \(I_j(g)A_r(h)\); if the
pair is empty versus singleton \(\{r\}\), the outer block set changes
between \(T\) and \(T\cup\{j\}\), yielding
\(|\widehat h(\{r\})|A_j(g)\). All other active blocks sum by Parseval.
The influence identity follows from the same unique-block spectrum and
Parseval.

Since \(h\) is monotone,
\(|\widehat h(\{r\})|=I_r(h)\). Thus, whenever the relevant influences
are nonzero,
\[
\frac{A_{(j,r)}(F)}{I_{(j,r)}(F)}
=\frac{A_r(h)}{I_r(h)}+\frac{A_j(g)}{I_j(g)}.
\]

## Iteration and lower bound for every coordinate

Let \(F_0=h\). Define
\[
F_{k+1}=h(F_k^{(1)},F_k^{(2)},F_k^{(3)},F_k^{(4)}),
\]
where the four copies of \(F_k\) use disjoint input blocks. Thus
\(n_k=4^{k+1}\). Each coordinate of \(F_k\) lies at a leaf of a 4-ary
composition tree with \(k+1\) seed gates along its path. The coordinate
identity, applied with outer gate \(h\) and inner balanced monotone gate
\(F_k\), shows that the leaf ratio is the ratio at the inner leaf plus the
seed ratio for its outer slot: monotonicity gives
\(|\widehat F_k(\{r\})|=I_r(F_k)\). Repeating, each leaf ratio is the sum
of the seed ratios along its path. Every seed ratio is at least \(1/2\),
so every leaf ratio is at least \((k+1)/2\); choosing a path that uses a
seed coordinate of ratio \(1/2\) at every layer attains equality.

For clarity, one step with outer and inner gate both equal to \(h\) gives
the following exact ratios, grouped by inner block:
\[
\begin{array}{c|c}
\text{outer coordinate }j&\text{ratios for the four inner coordinates}\\\hline
1&(1,3/2,1,3/2)\\
2&(3/2,2,3/2,2)\\
3&(1,3/2,1,3/2)\\
4&(3/2,2,3/2,2).
\end{array}
\]
The minimum is 1. An exact 16-bit Walsh computation in
`fei_aggregate_A_counterexample.py` verifies the coordinate influences and
absolute edge sums, as well as the global values \(I=9/4\), \(A=3\).

## Explicitly FEI-bounded family

The Fourier spectrum of a balanced block composition has the exact entropy
and influence laws
\[
H(g(h_1,\ldots,h_n))=H(g)+I(g)H(h),\qquad
I(g(h_1,\ldots,h_n))=I(g)I(h).
\]
For this seed, \(H(h)=3\) bits and \(I(h)=3/2\). Thus the recursion
\(F_{k+1}=h(F_k^{(1)},\ldots,F_k^{(4)})\) obeys
\[
I(F_k)=(3/2)^{k+1},\qquad
H(F_k)=6\big((3/2)^{k+1}-1\big),
\]
so \(H(F_k)/I(F_k)=6(1-(3/2)^{-(k+1)})<6\). This makes the scope
unambiguous: the construction rules out the proposed one-coordinate split
criterion while respecting FEI with a uniform constant on the entire family.

## Current literature scope

Han's primary statement is Question 3.1 of arXiv:2312.08271v2,
https://arxiv.org/html/2312.08271, lines 280–286. The June 2026 primary paper
González–MacManus–Pereyra, arXiv:2606.00246v2,
https://arxiv.org/html/2606.00246v2, restates this as a sufficient local
inductive inequality and proves it for specific classes. It exhibits
\(\delta\)-tribes where a designated split fails but a carefully chosen
variable works for that family. It does not claim the coordinate-selection
statement holds for all Boolean functions. The construction here appears to
refute Han's stated open auxiliary question; FEI itself remains unresolved.

## Reproducibility and novelty caution

The proof of all dimensions is the coordinate composition identity plus
iteration; the finite exact check is a consistency test, not a substitute
for the proof. Before making any historical novelty claim, perform a broader
primary-literature check for recursive-composition counterexamples to
Question 3.1. The result should be described narrowly as a counterexample to
that proposed local criterion, not as FEI progress or a counterexample to
FEI.
