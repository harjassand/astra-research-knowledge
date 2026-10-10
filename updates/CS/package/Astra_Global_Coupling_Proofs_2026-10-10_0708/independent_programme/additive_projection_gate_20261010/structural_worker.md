# A linear dimension bound for the additive-projection obstruction

## Result

Let \(V\) be an \(m\)-dimensional vector space over \(\mathbb F_2\), and let \(K_1,\dots,K_w\le V\), where \(w\ge1\), satisfy
\[
\bigcap_{i=1}^w K_i=\{0\}.
\]
Suppose every two-dimensional subspace \(U\le V\) has \(\dim(U\cap K_i)=1\) for at least one \(i\). Then
\[
\boxed{m\le 2w-1.}
\]
Equivalently, if \(m\ge2w\), binary linear maps with joint kernel zero admit a two-dimensional subspace on which each map has rank either zero or two.

The sharper proposed threshold \(m>w\) is not established by this argument.

## External ingredient, independently checked

A. E. Brouwer, *An inequality in binary vector spaces*, Discrete Mathematics 59 (1986), 315–317:
https://ir.cwi.nl/pub/2507/2507D.pdf

We use only the following consequence of its theorem: if \(J_1,\dots,J_k\) are an irredundant cover of a binary vector space \(V\) by linear subspaces, then
\[
\operatorname{codim}_V\bigcap_{i=1}^kJ_i\le k-1.
\]
The actual theorem also permits affine cosets. The quoted bound is explicit in the theorem on page 315 and does not rely on any later, withdrawn result.

## Proof of the result

Call a two-dimensional subspace **good** if every \(K_i\) meets it in dimension zero or two. Assume there is no good subspace. We induct on the number \(w\) of kernels. During the induction, an empty family with joint kernel zero can occur only on the zero-dimensional space.

We exhibit a nonempty index set \(I\), write \(k=|I|\), and put
\[
H=\bigcap_{i\in I}K_i,
\]
such that
\[
\operatorname{codim}_V H\le2k-1.\tag{1}
\]

**Case 1: the kernels cover \(V\).** Choose an irredundant subcover \(\{K_i:i\in I\}\). Brouwer's theorem gives the stronger estimate
\[
\operatorname{codim}_V H\le k-1.
\]

**Case 2: the kernels do not cover \(V\).** Choose
\(x\in V\setminus\bigcup_iK_i\), and set
\[
J_i=K_i+\langle x\rangle.
\]
These \(J_i\) cover \(V\). Indeed, \(0\) and \(x\) belong to every \(J_i\). For any other \(y\), the plane \(\langle x,y\rangle\) is not good, so some \(K_i\) contains exactly one of its three nonzero points. Since \(x\notin K_i\), that point is \(y\) or \(x+y\). Either possibility implies \(y\in J_i\).

Choose an irredundant subcover \(\{J_i:i\in I\}\), and put
\(D=\bigcap_{i\in I}J_i\). Brouwer gives
\[
\operatorname{codim}_V D\le k-1.
\]
Each \(K_i\) is a hyperplane of \(J_i\), since \(x\notin K_i\). Consequently each \(D\cap K_i\) has codimension at most one in \(D\). Since
\[
H= D\cap\bigcap_{i\in I}K_i,
\]
we obtain
\[
\operatorname{codim}_V H
\le\operatorname{codim}_V D+\operatorname{codim}_D H
\le(k-1)+k=2k-1,
\]
proving (1).

Now restrict the remaining \(w-k\) kernels to \(H\). Their joint intersection is zero. They still admit no good two-dimensional subspace: such a subspace would also be good for the deleted kernels, which contain all of \(H\).

If \(w-k=0\), joint intersection zero forces \(H=0\), and (1) yields \(m\le2w-1\). Otherwise induction gives \(\dim H\le2(w-k)-1\), and hence
\[
m\le(2k-1)+[2(w-k)-1]=2w-2\le2w-1.
\]
This completes the proof.

## Additional exact reformulation

For any nonzero \(x\in V\), define
\[
W_x=\bigcap_{i:x\in K_i}K_i,
\]
with an empty intersection understood as \(V\). Absence of a good plane is equivalent to the following cover holding for every nonzero \(x\):
\[
W_x=\bigcup_{i:x\notin K_i}\bigl[(K_i\cap W_x)+\langle x\rangle\bigr].
\]
The terms \(0,x\) are covered because joint kernel zero ensures at least one index with \(x\notin K_i\). For other \(y\in W_x\), kernels containing \(x\) contain the whole plane \(\langle x,y\rangle\). Thus a kernel cuts that plane in one point precisely when it does not contain \(x\) and contains one of \(y,x+y\). This gives both directions.

## What this does and does not settle

The constant-factor target is proved with constant 2 and an explicit additive improvement: no-good-plane arrangements have \(m\le2w-1\). No counterexample to the sharper conjecture \(m\le w\) was found, and no proof of it is claimed. The extra loss in this proof occurs when replacing the covering spaces \(J_i\) by their hyperplanes \(K_i\), which can cost one additional dimension per selected index.
