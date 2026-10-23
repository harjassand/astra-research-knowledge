# Exact rank-flow audit for finite QCA collars

## Verdict

For a strict one-dimensional full-tensor-product QCA, the proposed relation is
valid on the actual finite collars in the opening, with the RWW orientation.
Write \(\kappa(\alpha)>0\) for the multiplicative GNVW index (RWW's
\(\operatorname{ind}\) is its logarithm):
\[
\frac{\operatorname{rank}J_A}{\operatorname{rank}J_B}
 =\kappa(\alpha)^{-2},\qquad
A=L_1'R_1,\quad B=L_1R_1'.
\]
This is an exact support/rank statement. It does not follow merely by taking a
Rényi limit of the von Neumann or second-Rényi formulas.

## Finite-collar rank functional

Use the RWW cut at a bond, with \(L_1\) and \(R_1\) each consisting of r
sites (the source's Eq. (4.10): the r sites immediately to the left and
right of the cut). Let \(J_A,J_B\) be the corresponding finite Choi
marginals, and define
\[
F_r(\alpha)=\tfrac12\bigl(\log\operatorname{rank}J_B-
                         \log\operatorname{rank}J_A\bigr).
\]
For any larger collars of size \(n\ge r\), the same functional has the same
value. The exact locality factorization used in RWW's Proposition 4.7 is
\[
\phi_{L_n'R_n}=\phi_{L_1'R_1}\otimes\tau_{L_2'R_2},\qquad
\phi_{L_nR_n'}=\phi_{L_1R_1'}\otimes\tau_{L_2R_2'},
\]
where the added factors are full-rank tracial states. Their ranks are the
same: both are the product of the Hilbert-space dimensions of the added
left-reference and right-output legs. Since ranks multiply under tensor
products, the added factors cancel from \(F_n\). Thus a proof using a larger
block-compatible collar proves the assertion for the original radius-r
collar as well.

For a careful circuit argument, use support fractions rather than claiming
that a half-chain circuit preserves the rank of a fixed finite matrix. Let
\(\tau_A\) be the normalized trace on the infinite cross algebra
\(A=L'R\). Strict locality gives the cross-state density
\(f_A=M_r J_A\) on its finite collar, extended by the identity outside,
where \(M_r=\dim\mathcal H_{L_1'R_1}\); hence
\[
t_A:=\tau_A(\operatorname{supp}f_A)=\operatorname{rank}J_A/M.
\]
Define \(t_B\) similarly; the matching collar on B has the same Hilbert-space
dimension \(M_r\). A half-chain circuit induces a
trace-preserving automorphism of the corresponding cross algebra; it sends
\(f_A\) to its automorphic image and preserves \(t_A\) (and likewise
\(t_B\)). Any finite-depth circuit can be factored into side circuits and a
unitary \(V\) supported on a finite collar around the cut: collect the
finitely many gates crossing the cut and absorb their finite-depth
conjugations into \(V\). The Choi vector of \(V\) is pure on the doubled
finite collar. Its two cross partitions are complementary, so their
reduced matrices have equal rank. The two collar Hilbert-space dimensions
are also equal, hence their normalized support fractions agree. Side
circuits preserve these fractions, proving \(t_A=t_B\) for the original
circuit. Since the actual equal-size collars have the same \(M\), this is
exactly \(\operatorname{rank}J_A=\operatorname{rank}J_B\). This avoids an
infinite-rank or finite-boundary handwave.

The functional has the three properties that characterize the GNVW index:

1. **Tensor additivity.** Choi marginals tensorize for \(\alpha\otimes\beta\),
   so ranks multiply and \(F(\alpha\otimes\beta)=F(\alpha)+F(\beta)\).
2. **Circuits give zero.** The support-fraction argument above shows
   \(t_A=t_B\), so \(F=0\) on any sufficiently large collar and, by
   collar independence, on the original one.
3. **Shifts have the index value.** For a right shift by k sites of a
   q-dimensional tensor factor (\(1\le k\le r\)), the finite collar has
   k Choi pairs internal to A, \(2(r-k)\) pairs split between A and B, and
   2k unpaired tracial legs on B at the collar boundary. Therefore
   \[
   \operatorname{rank}J_A=q^{2(r-k)},\qquad
   \operatorname{rank}J_B=q^{2r},\qquad F_r=k\log q.
   \]
   Idle tensor factors contribute equal ranks on the two sides. A left shift
   reverses the sign. Products of right/left subfactor shifts give
   \(F=\log(q_R/q_L)=\log\kappa\).

By the one-dimensional GNVW classification (equivalently the
classification step used in RWW's Lemma 4.5), for any \(\alpha\) one can
tensor an inverse-index generalized shift \(\beta\) so that
\(\alpha\otimes\beta\) has multiplicative index one and is a finite-depth
circuit. Choose
a common collar larger than the ranges of \(\alpha,\beta\), and that
circuit. The properties above give
\[
0=F(\alpha\otimes\beta)=F(\alpha)+F(\beta)
 =F(\alpha)-\log\kappa(\alpha),
\]
so \(F_r(\alpha)=\log\kappa(\alpha)\). Collar independence
then returns the exact result at the radius-r collar. This argument uses
the full-tensor QCA classification and does not assume translation
invariance; if a classification proof blocks sites, collar independence
allows that larger block collar without changing the rank ratio. If stable
equivalence is used to align local dimensions, each added idle tensor factor
contributes the same rank multiplier to A and B, so it leaves their ratio
unchanged.

## Consequence and checks

Exponentiating gives
\(\operatorname{rank}J_A/\operatorname{rank}J_B=
\kappa(\alpha)^{-2}\). The orientation agrees with a right shift:
RWW's \(I(L_1':R_1)=2k\log q\), \(I(L_1:R_1')=0\), while the right-shift
rank count above makes \(J_A\) the lower-rank marginal. An index-one circuit
has equal ranks, including circuits whose Choi spectra are non-flat.

The rank/matching argument in the opening is also consistent with mixed
finite-window Choi states. The all-sites-match projector selects vectors
whose input and output strings agree; every diagonal weight \(g_x\) is at
most the probability of output string x, namely \(1/M\) under the tracial
output marginal. Thus \(\|G_A-I/M\|_1=E\). Gentle projection and partial
trace yield \(\tfrac12\|J_A-I/M\|_1\le\sqrt E+E/2\), and a state of rank at
most \(M/a\) is at trace distance at least \(1-1/a\) from \(I/M\). These
are compatible with the exact rank ratio above; they do not require the
Choi marginal itself to be a projector or to have a flat spectrum.
