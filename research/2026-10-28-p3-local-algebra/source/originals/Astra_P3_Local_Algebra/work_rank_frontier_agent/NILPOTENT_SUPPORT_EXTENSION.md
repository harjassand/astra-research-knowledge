# Direct use of an acquired nilpotent uniformizer

This proved and executed extension of the selfadjoint support mechanism removes its residue-field-degree threshold. The input operator is multiplication by the uniformizer already acquired from a chain algebra. The implementation is `nilpotent_support.py`; its matrix tests and decisive failure are in `nilpotent_support_results.json`. Exact ordinary-ring fitting and counting remain the responsibility of the complete counter.

Let \(A=\mathbb F_{2^d}[\pi]/(\pi^e)\), \(e\ge7\), and \(V=A^b\), with \(n=bde\) original bits. Use the nondegenerate Frobenius pairing

\[
\langle x,y\rangle=\operatorname{Tr}[\pi^{e-1}]\sum_i x_i y_i
\]

of binary matrix \(G\). Multiplication \(N=M_\pi\) is selfadjoint and \(N^e=0\). This \(G\) is the **ring top-coefficient Gram matrix**, not the block trace Gram matrix of the residue field.

Suppose \(L=G^{-1}B=L_0+E\), where \(B\) is an actual alternating polar matrix, \(E=E^*\), \(GE\) is alternating of binary rank \(r\), and \(L_0\) is the quadratic polar map of the scalar image of an ordinary cubic over \(A\), after subtracting its canonical alternating trilinear lift. This is the ordinary-ring base used by the chain counter.

## Annihilation without an invertible Frobenius

The squaring map \(\phi(x)=x^2\) on \(A\) is binary-linear but need not be invertible. It satisfies

\[
\phi N=N^2\phi,\qquad N\phi^*=\phi^*N^2.
\]

The ordinary ring-quadratic polar blocks are sums of multiplication maps, \(M_a\phi\), and \(\phi^*M_a\). On these three types, respectively, one of the commuting left/right operators

\[
\mathsf L_N+\mathsf R_N,\qquad
\mathsf L_N^2+\mathsf R_N,\qquad
\mathsf L_N+\mathsf R_N^2
\]

vanishes. Their product therefore annihilates \(L_0\). Its expansion is

\[
H=L N^4+N^4L+(N+N^2)L(N+N^3)+(N+N^3)L(N+N^2).                 \tag{1}
\]

No inverse-square or inverse-uniformizer identity is used.

## Acquiring support despite a nonunit multiplier

Set \(c=N+N^2\), \(q=N+N^3\),

\[
C=\langle I,N^4,c,q\rangle_{\mathbb F_2},\qquad
S=C+cC=\langle I,N,N^2,\ldots,N^6\rangle_{\mathbb F_2}.
\]

These polynomial identities hold because \(N\) has nilpotency index at least seven. They give \(\dim C=4\), \(\dim S=7\), and \(C\cap cC=\mathbb F_2c\). Write \(E=U K U^*\), where \(K\) is nonsingular alternating. Require the Krylov directness condition

\[
\operatorname{rank}[U,NU,\ldots,N^6U]=7r.                    \tag{2}
\]

With \(V_C=[U,N^4U,cU,qU]\) and \(J_4\) swapping blocks zero with one and two with three,

\[
H=V_C(J_4\otimes K)V_C^*,\qquad W:=\operatorname{im}H=CU.
\]

The expression \(c^{-1}(W\cap cW)\) cannot use an inverse on the entire ambient space: \(c\) is nilpotent. Instead restrict multiplication by \(c\) to \(W\). Condition (2) makes \(c|_W\) injective, because the four scalar polynomials defining \(cC\) are independent. Furthermore \(W\cap cW=cU\). Thus

\[
U=\{w\in W:cw\in W\}.                                    \tag{3}
\]

This subspace is acquired by binary linear algebra inside \(W\). Express \(H\)'s columns in \([U,N^4U,cU,qU]\); the second block of coefficient rows is \(KU^*\). Multiplying that block by \(U\) recovers the exact error \(E\), hence the planted base \(L_0\).

The program verifies (2), error rank and alternation, and the annihilator identity for the base candidate. In this nilpotent case the kernel of (1) can be larger than the ordinary-ring base space. The complete counter must therefore run its exact ordinary-ring coefficient fitter before accepting a count. Under the theorem's model the planted error has been recovered, so that fit succeeds. Matrix acquisition alone never claims to certify an ordinary-ring base.

All operations are on explicit binary matrices and acquired operators, so the acquisition uses polynomial time and space. There is no enumeration of \(A\), its residue field, or error supports.

## Exact probability bound

For independent uniform support columns \(u_i\in\mathbb F_2^n\), failure of (2) means \(\sum_i f_i(N)u_i=0\) for a nonzero tuple of binary polynomials of degree at most six. Let \(v\) be the smallest valuation among nonzero \(f_i\). Every polynomial with nonzero constant term is invertible when evaluated at a nilpotent matrix. Consequently the sum is uniform on \(\operatorname{im}N^v\), and its zero probability is exactly \(2^{-\operatorname{rank}N^v}\).

There are \(2^{(7-v)r}-2^{(6-v)r}\) tuples with minimum valuation \(v\). The union bound is therefore

\[
\Pr[\text{failure}]\le
\sum_{v=0}^{6}\bigl(2^{(7-v)r}-2^{(6-v)r}\bigr)
2^{-\operatorname{rank}N^v}.                              \tag{4}
\]

On the free chain module, \(\operatorname{rank}N^v=n-bdv\). A looser bound is \(2^{7r-n+6bd}\). Conditioning on support rank \(r\le n-1\) multiplies (4) by at most two. As with the field case, fixed nonsingular alternating \(K\) and uniformly chosen full-rank \(U\) produce the uniform rank-\(r\) alternating polar error distribution. No independence of individual bad events is assumed.

For fixed residue degree, growing chain length, and \(r=o(n)\), failure is \(2^{-n+o(n)}\). In particular degrees three through six are now included, although their residue fields cannot contain the earlier seven-dimensional scalar space. Combining this acquisition with the independently proved ordinary-chain cubic evaluator gives \(2^r\operatorname{poly}(L+n)\) counting time and polynomial space. The ordinary cubic identifiability condition \(d\ge3\) is retained.

Equations (1)–(4) also apply to any known selfadjoint nilpotent operator with index at least seven, using its actual ranks in (4). A suitable base-annihilation identity and exact evaluator must still be established for each application.

## Executed checks and a decisive failure

Five matrix fixtures recovered the exact planted base and defect:

| Bits \(n\) | Residue degree \(d\) | Chain length \(e\) | Module rank \(b\) | Error rank \(r\) |
|---:|---:|---:|---:|---:|
|72|3|8|3|6|
|108|3|12|3|10|
|96|4|8|3|8|
|126|6|7|3|6|
|144|3|16|3|16|

Each passed 1,024 exact quadratic identities, in addition to complete matrix equality. These are acquisition tests, not executions of the full cubic counter.

For the decisive kernel test, a rank-two alternating defect was generated from support inside \(\ker N\), over residue degree seven and chain length eight. Its manufactured syndrome is zero, so the matrix interface returns it as a rank-zero base candidate. A necessary field-band test rejects that candidate as incompatible with any ordinary-ring quadratic base. This explicitly demonstrates why the complete ordinary-ring fitter cannot be omitted.

### Public interface

`base_candidate, exact_defect, certificate = acquire_nilpotent_base(B, h, e, module_dimension=3)`

The coordinate order is module block, then uniformizer power, then field bit. The certificate marks `base_fit_required=True`. No root source file is modified by this module.

The support-intersection ancestry and prior-art qualifications are as in `SYLVESTER_SUPPORT_ACQUISITION.md`; the new repair here is the restricted preimage for a nonunit multiplier and the valuation-sensitive probability calculation.
