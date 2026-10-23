# Finite-error local projector bound and isolated-site coverage obstruction

## Finite-error bound

Let \(\alpha=\operatorname{Ad}V^\dagger\) be a strict QCA automorphism of a one-dimensional chain of equal \(d\)-dimensional cells, with radius \(R\). For a tested site \(i\), let \(P=P_{ij}=|j\rangle\langle j|_i\otimes I\) be the rank-one basis projector (with identity on the other cells of \(\Lambda=N_R(i)\)); let \(Q=\alpha(P)\), supported on \(\Lambda\). Put \(m=|\Lambda|\) and use unnormalized matrix trace \(\operatorname{Tr}\) on that local algebra. Assume the product state has full support and

\[
  \tau_\Lambda=\bigotimes_{x\in\Lambda}\tau_x\succeq p_*^m I,
  \qquad p_*>0.
\]

The local operators \(P,Q\) are projections. Their local ranks agree: the canonical normalized product trace \(\operatorname{tr}\) is invariant under a QCA automorphism, so

\[
  d^{-m}\operatorname{Tr}Q=\operatorname{tr}(Q)
  =\operatorname{tr}(\alpha(P))=\operatorname{tr}(P)=1/d.
\]

Thus \(\operatorname{Tr}P=\operatorname{Tr}Q=d^{m-1}\). This rank step uses trace preservation and the normalized local trace; it is what lets the one-sided mismatch control the full Hilbert–Schmidt distance.

Set \(A=P(I-Q)P\succeq0\). The given quantity is the *joint* label/mismatch contribution

\[
  e_{ij}=\operatorname{Tr}(\tau_\Lambda A),
\]

not the mismatch probability conditioned on observing label \(j\). Positivity and the product lower bound give

\[
  e_{ij}\ge p_*^m\operatorname{Tr}A.
\]

Using equal ranks,

\[
\begin{aligned}
  \|Q-P\|_2^2
   &=\operatorname{Tr}(Q-P)^2\\
   &=2\operatorname{Tr}P-2\operatorname{Tr}(PQ)\\
   &=2\operatorname{Tr}\!\left(P(I-Q)P\right)
    =2\operatorname{Tr}A,
\end{aligned}
\qquad\Longrightarrow\qquad
  \boxed{\|Q-P\|_2^2\le \frac{2e_{ij}}{p_*^m}}.
\]

Here \(\|\cdot\|_2\) is the unnormalized Hilbert–Schmidt norm. The same right-hand side bounds \(\|Q-P\|_{\rm op}^2\), since operator norm is at most Hilbert–Schmidt norm. For equal-rank projections one can sharpen this operator-norm statement:

\[
  \|Q-P\|_{\rm op}^2
   =\|P(I-Q)P\|_{\rm op}
   \le\operatorname{Tr}A
   \le e_{ij}/p_*^m.
\]

The equality is the principal-angle formula for equal-rank subspaces. It would not follow in this form without equal ranks; in general \(\|Q-P\|_2^2=\operatorname{Tr}P+\operatorname{Tr}Q-2\operatorname{Tr}(PQ)\), with an unmatched \(\operatorname{Tr}Q-\operatorname{Tr}P\) term.

The full-state eigenvalue floor can be conservative. Since \(A=PAP\), define

\[
  \lambda_{ij}=\lambda_{\min}\!\left(P\tau_\Lambda P\big|_{\operatorname{Ran}P}\right).
\]

Then \(e_{ij}\ge\lambda_{ij}\operatorname{Tr}A\), hence

\[
  \|Q-P\|_2^2\le2e_{ij}/\lambda_{ij},\qquad
  \|Q-P\|_{\rm op}^2\le e_{ij}/\lambda_{ij}.
\]

For a product state with the same one-cell \(\tau\) throughout \(\Lambda\), and \(P_{ij}=|j\rangle\langle j|_i\otimes I\),

\[
  \lambda_{ij}\ge q_{ij}p_*^{m-1},\qquad
  q_{ij}=\langle j|\tau|j\rangle.
\]

Thus, if \(\epsilon_{ij}=e_{ij}/q_{ij}\) is the mismatch conditional on the sampled site label, the sharper bounds are \(\|Q-P\|_2^2\le2\epsilon_{ij}/p_*^{m-1}\) and \(\|Q-P\|_{\rm op}^2\le\epsilon_{ij}/p_*^{m-1}\). Equality in the displayed floor occurs when \(p_*\) is the actual minimum eigenvalue and the neighbor factors attain it. Keep this normalization explicit: replacing joint \(e_{ij}\) by conditional \(\epsilon_{ij}\) without the factor \(q_{ij}\) changes the statement.

The coefficient 2 in the Hilbert–Schmidt inequality is sharp under only the global floor. For a uniform one-qubit state, \(P=|0\rangle\langle0|\), \(Q=|+\rangle\langle+|\), one has \(p_*=1/2\), \(e=1/4\), and \(\|P-Q\|_2^2=1=2e/p_*\). A nonuniform one-qubit state \(\tau=\operatorname{diag}(3/4,1/4)\) with the same \(P,Q\) has \(e=3/8\): the global-floor bound gives 3, while the compressed-weight bound gives the exact Hilbert–Schmidt square 1. These exact rational checks are in [check_finite_error.py](check_finite_error.py).

## Nontranslation-invariant coverage obstruction

At radius 2, an isolated tested site can be bypassed by a nontrivial-index QCA. On a chain of \(d\)-dimensional cells, choose a tested site \(c\), let \(T\) swap cells \(c-1\) and \(c\), and let \(S_\rightarrow\) shift every cell one site right. Define the cell permutation \(V=S_\rightarrow T\). In terms of source-cell locations,

\[
  f(c)=c,\qquad f(c-1)=c+1,\qquad f(x)=x+1\quad(x\notin\{c-1,c\}).
\]

This is a bijection: it is exactly the right shift composed with one finite swap. The cell at \(c-1\) jumps over \(c\), which stays fixed. The induced automorphism \(\alpha=\operatorname{Ad}V^\dagger\) has radius 2 (and its inverse also has radius 2), and \(\alpha(P_{cj})=P_{cj}\) for every basis label \(j\). Hence all the tested-site classical tags pass exactly, with \(e_{cj}=0\), despite nontrivial global information flow. The QCA has the right-shift index \(d\) (or its reciprocal under the opposite convention): a finite-depth local swap does not change the index. For \(d>1\), this is nontrivial.

Translating the defect realizes the construction at any chosen isolated site. A collection of nonadjacent tested sites can likewise be fixed by composing the right shift with the disjoint swaps \((c-1,c)\) at those sites; the radius remains 2 and the asymptotic index remains that of the shift. This is a coverage obstruction: exact agreement on sparse onsite tags does not certify a global index. It does not contradict the finite-error bound, which only forces the tested local projectors themselves to be close.

For a simple infinite nontranslation-invariant example, compose the right shift with all disjoint swaps \((2k-1,2k)\). The resulting cell permutation is

\[
  f(2k)=2k,\qquad f(2k-1)=2k+1.
\]

It fixes every even site (so all onsite tags there pass exactly) and shifts the odd sublattice one step to the right, i.e. two physical cells. Its radius and inverse radius are 2; its index is \(d\), since the disjoint swaps have trivial index and the odd sublattice carries one right-shifted \(d\)-dimensional cell across each cut. Thus even perfect tag coverage on one parity class does not rule out nontrivial information flow on the untested cells.
