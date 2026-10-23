# Magic-square endpoint norm check

This note checks the finite endpoint calculation and the tensorization step. It does not establish a separate BG-game construction or a quantum-versus-classical value claim.

## The graph and the \(p=1\) maximizers

Use the standard magic-square winning graph. A left vertex is a row \(i\in[3]\) and an even-parity string \(a\in\{0,1\}^3\); a right vertex is a column \(j\in[3]\) and an odd-parity string \(b\in\{0,1\}^3\). There is an edge exactly when \(a_j=b_i\). Thus each side has 12 vertices. Each vertex has degree 6: for each opposing question, two of the four parity-constrained answers agree at the intersection.

Let \(W\) be its \(12\times12\) adjacency matrix and \(K=W/6\), acting by matrix multiplication (there is no extra \(1/12\) in the sum over the right vertex). All \(L_p\) norms below use uniform probability measure on the 12 vertices. Set
\[
\mathcal D=\{f\geq0:\mathbb E f=1\},\qquad
T(f,g)=\mathbb E_x f(x)(Kg)(x),\qquad
C(p)=\max_{f,g\in\mathcal D}\frac{T(f,g)}{\|f\|_p\|g\|_p}.
\]
This convention is the one for which \(C(1)=2\). The \(L_1\) constraints only fix scale: the quotient is separately homogeneous, so its maximum is also the nonnegative operator norm \(\|K\|_{p\to p^*}\), where \(p^*=p/(p-1)\) (with \(p^*=\infty\) at \(p=1\)). Indeed, duality gives
\[
\sup_{f,g\geq0}\frac{\langle f,Kg\rangle}{\|f\|_p\|g\|_p}
=\sup_{g\geq0,\,\|g\|_p=1}\|Kg\|_{p^*}.
\]

For \(f,g\in\mathcal D\), put \(P_f(x)=f(x)/12\) and \(P_g(y)=g(y)/12\). These are probability distributions, and the regular degree gives the exact identity
\[
T(f,g)=2\sum_{x,y}P_f(x)P_g(y)W_{xy}.
\]
Consequently \(T\leq2\), with equality iff \(\operatorname{supp}(P_f)\times\operatorname{supp}(P_g)\) is a complete biclique of \(W\). In particular, \(C(1)=2\).

The largest biclique has area \(B=6\). For an upper bound, let \(I\) be the set of Alice rows represented in a biclique and \(J\) the Bob columns represented. If \(m=|I|\) and \(n=|J|\), then each Alice answer set in a fixed row has all its \(n\) bits on \(J\) fixed; an even-parity triple has at most \(a(n)\) completions, where \(a(1)=2\), \(a(2)=a(3)=1\). Similarly each Bob answer set has at most \(a(m)\) elements. Hence
\[
|S||T|\leq m n a(n)a(m).
\]
For \((m,n)\ne(3,3)\), this upper bound is at most 6. The \((3,3)\) case is impossible: nonempty selected answer sets would fix a full \(3\times3\) cell-bit array whose three row parities are even and whose three column parities are odd. The parity of the total number of ones would then be both 0 and 1. Finally, one left vertex together with its six neighbors is a biclique of area 6, proving \(B=6\).

## Right derivative at \(p=1\)

For \(f\in\mathcal D\), define \(\ell_p(f)=\log\|f\|_p\). On the compact simplex \(\mathcal D\subset[0,12]^{12}\),
\[
\ell_1(f)=0,\qquad
\partial_p\ell_p(f)|_{p=1}=\mathbb E[f\log f]
=\log12-H(P_f),
\]
using \(0\log0=0\) and Shannon entropy in nats. The derivative is continuous jointly in \(p,f\) at \(p=1\): each \(z^p\log z\) extends continuously to \(z=0\) for \(p\geq1\), and the simplex is compact. Therefore
\[
\ell_{1+h}(f)=h(\log12-H(P_f))+o(h)
\]
uniformly over \(f\in\mathcal D\) as \(h\downarrow0\).

Apply the one-sided Danskin envelope rule to
\(H_p(f,g)=T(f,g)\exp[-\ell_p(f)-\ell_p(g)]\). The uniform expansion just established is the needed uniform differentiability on the compact parameter set. At an active maximizer for \(p=1\), \(T=2\) and the two supports form a biclique. Thus
\[
C'_+(1)=\max_{T(f,g)=2}-2(\ell'_1(f)+\ell'_1(g))
=2\max_{T(f,g)=2}\{H(P_f)+H(P_g)-\log144\}.
\]
For a biclique with sides \(S,T\), the entropy sum is at most \(\log|S|+\log|T|\leq\log B\). Uniform distributions on the two sides of a maximum-area biclique attain \(\log B\). Hence
\[
C'_+(1)=2\log(B/144),\qquad
\left.\frac{d}{dp}\log C(p)\right|_{1+}=\log(B/144)=-\log24.
\]

For \(F(p)=8C(p)4^{-2/p}\), \(F(1)=1\), and
\[
\left.\frac{d}{dp}\log F(p)\right|_{1+}
=-\log24+2\log4=\log(2/3)<0.
\]
The right derivative therefore proves that \(F(p)<1\) for every \(p>1\) sufficiently close to 1. This conclusion is local in \(p\); it supplies no explicit numerical interval without a remainder bound.

## Tensorization for arbitrary inputs

Let \(A:X\to Y\) and \(B:U\to V\) be nonnegative finite kernels, with product probability measures, and let \(1\leq p\leq q\leq\infty\). Then
\[
\|A\otimes B\|_{L_p(X\times U)\to L_q(Y\times V)}
=\|A\|_{L_p(X)\to L_q(Y)}\,\|B\|_{L_p(U)\to L_q(V)}.
\]
For the upper bound it suffices to take \(h\geq0\), since positivity gives \(|(A\otimes B)h|\leq(A\otimes B)|h|\). Apply \(B\) first and set \(g(x,v)=(Bh(x,\cdot))(v)\). The single-fiber operator bound gives
\[
\|g\|_{L_p(X;L_q(V))}\leq\|B\|_{p\to q}\|h\|_{L_p(X\times U)}.
\]
Now apply \(A\) in the \(x\) coordinate. For each \(v\), its bound is from \(L_p(X)\) to \(L_q(Y)\), so
\[
\|(A\otimes B)h\|_{L_q(V;L_q(Y))}
\leq\|A\|_{p\to q}\|g\|_{L_q(V;L_p(X))}
\leq\|A\|_{p\to q}\|g\|_{L_p(X;L_q(V))}.
\]
The last inequality is mixed-norm Minkowski for \(p\leq q\). Combining gives the upper bound for every (not necessarily product) input. Product near-extremizers give the reverse inequality. Induction yields
\[
\|K^{\otimes n}\|_{p\to p^*}=C(p)^n,\qquad 1\leq p\leq2,
\]
because \(p\leq p^*\) on this interval. This is a genuine arbitrary-input tensorization statement; it uses positivity to reduce signed inputs to nonnegative ones and Minkowski to exchange the mixed norms.
