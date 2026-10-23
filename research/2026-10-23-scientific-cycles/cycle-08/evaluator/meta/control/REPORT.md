# Control receiver: anisotropic full-prefix susceptibility

**Status: solved at the stated finite bulk-coefficient scope.** The derivation uses the supplied Cycle7 source's stack-word cancellation and independent weighted quadratic minimization. I did not read `OPERATION.txt` or another receiver/evaluator's work.

## 1. Formula and attained optimizer

Write

\[
\eta=\sum_{a=1}^d p_a^2,\qquad A=2(1-\eta).
\]

There is a unique \(t>0\) satisfying

\[
\sum_{a=1}^d(1-t/p_a)_+=1.
\]

Define

\[
r_a=(1-t/p_a)_+,\quad R_*={\rm diag}(r_a),\quad
B=\sum_a p_a(1-r_a)^2.
\]

Equivalently, for \(J=\{a:p_a>t\}\),

\[
t=\frac{|J|-1}{\sum_{a\in J}p_a^{-1}},\qquad
B=\sum_{a\notin J}p_a+(|J|-1)t.
\]

At least two colors belong to \(J\). Ties \(p_a=t\) have \(r_a=0\); either convention for including ties in the threshold equation gives the same answer.

For \(k\ge2\), put

\[
C_k=\sum_{n=0}^{\lfloor(k-2)/2\rfloor}
(k-1-2n)4^{-n}\binom{2n}{n}.
\]

The requested minimum is

\[
\boxed{v_k(P)=\frac A8 k(k-1)+\frac{2B-A}{4}C_k.}
\]

An attainable density on the entire prescribed prefix is

\[
\boxed{\zeta_* =\sum_{a=1}^d r_a
(|a\rangle\langle a|)^{\otimes k}.}
\]

This is a correlated separable density. Its optimality is over all densities, including coherent and entangled competitors. Rational \(p_a\) give rational \(t,r_a,B,v_k\). The formula also holds for strictly positive real \(p_a\).

For a closed expression, with \(N=\lfloor(k-2)/2\rfloor\),

\[
C_k=(2N+1)4^{-N}\binom{2N}{N}
\left(k-1-\frac{2N}{3}\right).
\]

In particular, \(v_k(P)/k^2\to(1-\eta)/4\).

## 2. Proof against arbitrary coherent competitors

Use the source's endpoint decomposition \(G_1=[C_-,C_+]\). Its same-index term cancels \(2Q-kI\) in \(H_\zeta\). Different endpoint pairs and charge patterns occupy disjoint matrix blocks. Every charge pattern has probability \(2^{-k}\); conditional on a pattern with \(q\) colored ports, the color weight is \(P^{\otimes q}\).

Fix endpoint charges \(0,1\). Let \(m,h\) be the unmatched pops and pushes before the first endpoint, and let \(\delta\) be the unmatched middle pops. The source's raw identities

\[
C_jC_i=E^*U_iDE,\qquad C_iC_j=E^*DU_iE
\]

remain valid for every number of prepend colors. Deleting matched push/pop factors leaves pop-after-insertion versus insertion-after-pop. If the stack after the prefix is
\((a_h,\ldots,a_1,B_m,B_{m+1},\ldots)\), insertion at index \(\delta\) exchanges the input wire being inserted with the wire initially at that index. Undoing the prefix yields precisely three cases:

| Condition | Contracted block, up to an input-color permutation \(U_A\) | Weighted squared norm |
|---|---|---|
| \(h>\delta\) | \(U_A(I-\mathrm{SWAP})\) between two input colors | \(A\) |
| \(h=\delta\) | \(U_A(I-R_m)\), with prefix marginal \(R_m\) | \(f(R_m)=\mathrm{Tr}\,P(I-R_m)^2\) |
| \(h<\delta\) | Both words export the same input color at adjacent bath positions | Nonnegative; zero on every repeated pure-color prefix |

The insertion/pop identities are algebraic wire identities; they require no uniform color distribution. Every input-color permutation preserves \(P^{\otimes q}\). Thus the first value is \(2[1-\mathrm{Tr}(P^2)]\). In the second case, partial contraction of the input/bath swap is \(R_m\), without transposition. The reverse block gives the same weighted norm in these first two cases. For the third case only nonnegativity is needed for arbitrary competitors; cancellation for \(|u\rangle^{\otimes k}\) is exact before averaging.

For a Hermitian density \(R\),

\[
f(R)=\sum_a p_a(1-R_{aa})^2
+\sum_{a<b}(p_a+p_b)|R_{ab}|^2.
\]

Deleting off-diagonal entries preserves positivity and trace, and never increases this expression. The strictly convex diagonal problem on the probability simplex has KKT equations
\(r_a=(1-t/p_a)_+\). Hence \(f(R)\ge B\), with unique minimizing marginal \(R_*\). This explicitly includes complex coherences and marginals of entangled prefix states.

The proposed \(\zeta_*\) has every marginal \(R_*\), while its repeated-color components cancel all \(h<\delta\) blocks. It therefore attains all local lower bounds simultaneously. No assumption that a general prefix is symmetric or separable enters the lower bound.

For completeness, let \(M_i,M_r\) be independent maxima of fair walks of lengths \(i,r\). The prefix height has law \(M_i\) by reversal, and the middle deficit has law \(M_r\). Each endpoint orientation has probability \(1/4\), and its adjoint doubles its contribution. Consequently

\[
v_k(P)=\frac12\sum_{i+r\le k-2}
\{A\Pr(M_i>M_r)+B\Pr(M_i=M_r)\}.
\]

The index set is symmetric under \(i\leftrightarrow r\), so the strict-comparison sum is \([k(k-1)/2-C_k]/2\). To evaluate the collision sum, the reflection formula is
\(\Pr(M_n=m)=\Pr(S_n=m)+\Pr(S_n=m+1)\). With \(D=\sqrt{1-z^2}\) and \(a=(1-D)/z\), its generating function is \((1+a)a^m/D\). Squaring and summing over \(m\ge0\) gives

\[
\sum_{n\ge0}z^n\sum_{i=0}^n\Pr(M_i=M_{n-i})
=\frac1{(1-z)\sqrt{1-z^2}}.
\]

Coefficient comparison and summation through \(k-2\) give the displayed \(C_k\) and prove the formula.

## 3. Operator dual and support, including the boundary

Let \(H_*=H_{\zeta_*}\), and retain the source convention
\(T_k(X)=\mathrm{Tr}_A[(X\otimes I)G_1]\). The optimal blocks above commute with \(\sigma_P\), so
\(D_k:=T_k(\sigma_PH_*)\) is the correct Hermitian dual operator. This commutation is asserted for \(H_*\), not for arbitrary \(H_\zeta\).

Define

\[
\Delta=\operatorname{diag}((t-p_a)_+),\qquad
W=\operatorname{span}\{|a\rangle:p_a\ge t\}.
\]

Here is an explicit, finite formula for its weights. For a fair prefix walk of length \(i\), set \(m=-\min S\), \(h=S_i+m\); let an independent middle walk of length \(r\) have deficit \(\delta=-\min T\). Put

\[
w_{k,m}=\frac12\sum_{i+r\le k-2}
\Pr(-\min S=m,\ S_i+m=-\min T).
\]

Then

\[
\boxed{D_k=v_k(P)I_F+\sum_{m=0}^{k-2}w_{k,m}\Delta^{(m)}\ \ge v_k(P)I_F.}
\]

Here \(\Delta^{(m)}\) acts at prefix coordinate \(m\). Also
\(\sum_mw_{k,m}=C_k/2\), and every displayed weight is positive: the adjacent-endpoint event with \(m\) preceding zero ports contributes \(2^{-m-1}\).

To verify the operator identity, the critical block's cross contraction is

\[
\mathrm{Tr}[P(I-R_*)]I-P(I-R_*)
=BI+\Delta,
\]

because \(P(I-R_*)=\operatorname{diag}(\min(p_a,t))\) and
\(B=\mathrm{Tr}[P(I-R_*)]-t\). The other two cases contribute \(AI\) and zero. Summing proves the certificate, including all off-diagonal bath matrix elements.

Thus

\[
(D_k-v_kI)\zeta_*=0,\qquad
\ker(D_k-v_kI)=W^{\otimes(k-1)}\otimes\mathbb C^d.
\]

Every minimizing density must satisfy this support condition. More precisely, every density satisfies the exact identity

\[
\mathrm{Tr}(\sigma_PH_\zeta^2)
=v_k+2\mathrm{Tr}[\zeta(D_k-v_kI)]
+\mathrm{Tr}[\sigma_P(H_\zeta-H_*)^2].
\]

It is optimal exactly when \(H_\zeta=H_*\); the support condition then follows. Support alone need not suffice. For a general noncommuting candidate the gradient uses \(T_k((\sigma_PH+H\sigma_P)/2)\).

The dual is scalar **if and only if** \(\min_a p_a\ge t\). Strictly excluded colors make it nonscalar. At a tie \(p_a=t\), the corresponding optimizer weight is zero but the dual gap is also zero. For example
\(P=(2/5,2/5,1/5)\) gives \(t=1/5\), \(r=(1/2,1/2,0)\), \(B=2/5\), and \(D_k=v_kI\). Thus rank deficiency does not itself imply a nonscalar certificate. Strict convexity still forces every optimal marginal at coordinates \(0,\ldots,k-2\) to equal \(R_*\), even at a tie; the unused last coordinate is not constrained this way.

## 4. Fixed exact diagnostics and direct matrix checks

| \(P\) | \(t\) | \(r\) | \(A\) | \(B\) | Nonzero dual gap |
|---|---:|---|---:|---:|---:|
| \((4/5,3/20,1/20)\) | \(12/95\) | \((16/19,3/19,0)\) | \(67/100\) | \(67/380\) | \(\Delta_{33}=29/380\) |
| \((1/2,1/3,1/6)\) | \(1/5\) | \((3/5,2/5,0)\) | \(11/9\) | \(11/30\) | \(\Delta_{33}=1/30\) |
| \((9/10,1/10)\) | \(9/100\) | \((9/10,1/10)\) | \(9/25\) | \(9/100\) | None |

Their all-length values, respectively, are

\[
\frac{67}{800}k(k-1)-\frac{603}{7600}C_k,\qquad
\frac{11}{72}k(k-1)-\frac{11}{90}C_k,\qquad
\frac9{200}\{k(k-1)-C_k\}.
\]

| \(P\) | \(v_2\) | \(v_3\) | \(v_4\) |
|---|---:|---:|---:|
| \((4/5,3/20,1/20)\) | \(67/760\) | \(2613/7600\) | \(2211/3040\) |
| \((1/2,1/3,1/6)\) | \(11/60\) | \(121/180\) | \(253/180\) |
| \((9/10,1/10)\) | \(9/200\) | \(9/50\) | \(153/400\) |

`native_check.py` builds integer \(G_1\) directly by applying the raw toggling words and forming \([C_-,C_+]\), rather than building it from the three-case classification. Exact rational contractions verify all entries of the full dual matrix and the attained objective for \(k=2,3,4\), all three diagnostics, and the boundary example. It checks every final tail is unchanged. For \(d=3,k=4\), the native coefficient has 78,570 nonzero entries. All assertions passed; detailed receipts are in `native_check.json`.

At \(k=2\), \(H_*\) is the off-diagonal block \(I-R_*\) between the two one-color endpoint sectors, and \(D_2=(B I+\Delta^{(0)})/2\). Its distinct eigenvalues in the three prescribed examples are respectively \(\{67/760,12/95\}\), \(\{11/60,1/5\}\), and \(\{9/200\}\).

## 5. Scope, sources, and cost

This proves only the specified susceptibility of the finite bulk coefficient, with sufficiently deep initial coordinates. The two-seed root exchange is retained in the model but is not encountered by the finite word evaluations. The prefix optimizer is an analytic density, not a proposed physical initializer. No infinite-bath cutoff, preparation, nonlinear transfer, coding, or capacity result is asserted.

Source read: `SHARP_TEMPORAL_GROWTH.tex`, especially its endpoint decomposition, insertion/pop proof, and walk summation; also its included `INHERITED_OPERATOR_CODING.tex` and `INHERITED_COMPRESSION.tex`. The latter operational statements are not transferred here. All source files are in the supplied Pro1 Cycle7 directory.

One research turn; no subagents or external search. The sole mathematical script run used **1.1138482 process CPU seconds** and **1.114878829 wall seconds**, measured internally. Receiver elapsed time and timing endpoints are recorded separately in `COST.json`. Internal inference tokens, inference computation, model effort, and total acquisition/review costs are unknown. These measurements support no speed or performance advantage claim.
