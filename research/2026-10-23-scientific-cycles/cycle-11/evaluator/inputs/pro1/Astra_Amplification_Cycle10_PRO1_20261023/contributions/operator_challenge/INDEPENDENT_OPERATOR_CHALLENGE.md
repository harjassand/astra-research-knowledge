# Cycle10 independent challenge of the full operator response and Gram input

Date: 23 October 2026, Australia/Brisbane. Role: bounded independent challenge.

## Source and scope

I read the actual Cycle9 endpoint-response proof, the governing model and inherited moment interface, and the operator-coding/compression sources. The main predecessor is `SPECTRAL_CLIPPING_CAPACITY.tex`, 30,874 bytes, SHA256 `2fceb5bc5ffe836e41ea3d52154577d3c9511ac3bc94b19b4007746401eef086`. The endpoint-response source is 9,094 bytes, SHA256 `812ea02e15411be64c3c45b3c98f3ea182cc8e92516c10b273e8d3d6f72007fe`; operator coding is 5,677 bytes, SHA256 `d61719a490ff0dd206c7a4a3d09aed91f604b4aafe4d38344efe71f591a3884e`; compression is 5,183 bytes, SHA256 `278f881e709240f029720835960295e8f4dab721c6347109974d351e154e3101`.

This challenge independently derives the proposed full-operator estimate, then checks the owner's concrete transfer window. It does not repeat the old capacity audit or establish historical originality, external acceptance, or code efficiency. The integrated Cycle10 manuscript was not yet available when this file was written; its future version must not be silently identified with this review.

## 1. Definitions and indispensable scope

Let `b=beta^2`, `a=1-b`, and `r=bk`. Work on the inherited deep-bulk finite-prefix representation, valid for initial bath depth at least `k`. Let `P_x` project onto a complete input binary charge pattern `x in {0,1}^k`; its color fiber can have dimension `2^{|x|}`. Let `P_Q` denote pinching by total input charge and `P` pinching by complete patterns. Set

\[
 G=Q-W_k^*QW_k,\quad \widehat G=\mathcal P_Q(G),\qquad
 \sigma=\operatorname{diag}(1/2,1/4,1/4)^{\otimes k}.
\]

The finite-prefix identity represents the actual bulk operator, tensor the unchanged seed and deeper tail. It does not replace the bath by a cutoff, and is not asserted at the vacuum.

For every charge-preserving input `Y`, its weighted contraction against `G` equals its contraction against `widehat G`. This step must precede squaring: uncontrolled unequal-total-charge blocks of `G` are not part of the required observable.

## 2. Exact diagonal response

For fixed initial pattern `x`, two move/stay histories have the same output charge pattern only when they use identical choices at every call. Initial depth at least `k` ensures that no call starts at the root, so a move flips that site's charge and a stay preserves it. For each such history, the output charge is a scalar, and the complete history is unitary before restriction. Its contribution to the diagonal block is therefore that scalar times identity on all input colors and bath coordinates.

Each move has squared amplitude `a`; each stay has squared amplitude `b`. Averaging the output charge gives

\[
 \mathcal P(\widehat G)=a(2Q-kI)\otimes I.
\]

This is stronger than a diagonal input expectation: each complete charge-pattern block is a scalar operator on its entire color fiber and bath.

## 3. Offdiagonal distance-`2m` block

Take `x,y` of equal total charge, at distance `2m`, with differing set `T`. Exactly `m` initial ones and `m` initial zeros occur in `T`. Common output charge requires equal move/stay choices at all spectator positions and complementary choices at every endpoint in `T`.

Freeze a spectator stay set `S`. The common spectator weight is

\[
 b^{|S|}a^{k-2m-|S|}.
\]

The `2m` endpoints supply the common magnitude `(ab)^m`. If the ket endpoint stay set is `s subset T`, write `R_s` for the compressed cross-history operator. Every `R_s` is a contraction: it is a block of the product of two full unitary move/stay words, with all actual color and final-bath overlaps retained. The phase is a sign, since the two endpoint masks are complementary and have total length `2m`.

Keep spectators fixed to `U` or `I` and endpoints equal to `V_beta`. This auxiliary ordered word is unitary on the actual bath. Its offdiagonal `x,y` block in `W^*W` vanishes. Dividing its common endpoint amplitude for `0<b<1`, and then using the polynomial identity at the endpoints, yields

\[
 \sum_{s\subseteq T}\operatorname{sign}(s)R_s=0.
\]

For fixed `S`, all spectator output charges are constant. This identity cancels their full contribution to `W^*QW`. It also permits subtracting the endpoint mean `m` from every endpoint output charge. As `s` runs through all masks, the endpoint output word runs bijectively through `{0,1}^{2m}`. Hence the centered coefficient norm is at most

\[
 c_m=\sum_{j=0}^{2m}|j-m|\binom{2m}{j}
     =m\binom{2m}{m}.
\]

Summing the nonnegative spectator weights, which total one, proves

\[
 \|P_x\widehat G P_y\|\le c_m(ab)^m.
\]

There is no `k` from `||Q||` in this bound. The spectator weights arise after matching coherent amplitudes; they do not turn the physical channel into classical noise. This argument checks the full prefix operator rather than an expectation in any chosen prefix density.

## 4. A row bound and completely positive Cauchy--Schwarz

Define

\[
 Z=\widehat G-a(2Q-kI)\otimes I.
\]

It is Hermitian with `P(Z)=0`. For a fixed `x` of charge `q`, there are

\[
 \binom qm\binom{k-q}{m}
 \le\frac{k^{2m}}{4^m(m!)^2}
\]

equal-charge patterns at distance `2m`. Since

\[
 P_x Z^2P_x=\sum_y (P_yZP_x)^*(P_yZP_x),
\]

the row is a sum of positive operators. The block-norm estimate bounds it without counting individual color coordinates. Using

\[
 \binom{2m}{m}\le2^{2m-1}\quad(m\ge1)
\]

gives the all-length operator inequality

\[
 \mathcal P(Z^2)
 \le\sum_{m\ge1}\frac{m^2 4^{m-1}r^{2m}}{(m!)^2}I
 =r^2\sum_{j\ge0}\frac{(4r^2)^j}{(j!)^2}I
 \le r^2e^{4r^2}I.
\]

Here `a<=1` was used. Because `sigma=P(sigma)`, the unital completely positive map

\[
 \Phi_\sigma(M)=\operatorname{Tr}_A[(\sigma\otimes I)M]
\]

satisfies `Phi_sigma(Z^2)=Phi_sigma(P(Z^2))`. Its matrix Cauchy--Schwarz inequality yields, for Hermitian charge-preserving `Y` with `P(Y)=0`,

\[
 \|\Phi_\sigma((Y\otimes I)Z)\|
 \le\sqrt{\operatorname{Tr}\sigma Y^2}\,
      \|\Phi_\sigma(Z^2)\|^{1/2}.
\]

The diagonal term vanishes in contraction against `Y`. Therefore

\[
 \boxed{
 \|D_b(\sigma Y)\|
 \le r e^{2r^2}\|Y\|_{2,\sigma}
 \le2r\|Y\|_{2,\sigma}\quad(0\le r\le1/2).
 }
\]

No commutation between `Y` and `Z`, and no chosen bath-prefix state, is used. The norm is the full finite-prefix operator norm, hence the full actual bulk norm after tensoring the untouched tail. The same calculation agrees with the independently developed distance-level argument of the Hamming-response contribution.

## 5. Gram normalization: checks that prevent hidden assumptions

Use the owner's parameters

\[
 \ell=\ln2,\quad\gamma=\ell/4,\quad
 v=\operatorname{Tr}\sigma H^2,\quad m=3\ell v/32,
 \quad X=-\gamma bH,
\]

\[
 C=I+X/2,\quad D=\mathcal P(C^2)
 =I+\mathcal P(X^2)/4,\quad R=D^{-1/2},\quad F=RC^2R.
\]

The actual `H` is total-charge preserving, so `C,D,R,F` commute with `Q` and `sigma`. It is NOT necessary to assume `[D,H]=0`, and no such assumption is justified. `D>=I`, so `R` exists and `||R||<=1`. Conditional-expectation bimodularity gives

\[
 \mathcal P(F)=R\mathcal P(C^2)R=I.
\]

Set `A=Q-k/2` and

\[
 T=I+(4m/k)b^2A,\qquad \rho=\sigma TF.
\]

Since `T` is a function of total charge, it commutes with `F`. `T` is positive in the selected window. Thus `rho` is positive, Hermitian, normalized, and charge preserving. The identity `P(F)=I` gives exactly

\[
 \operatorname{Tr}\rho A=mb^2.
\]

The normalization is input spectral algebra, not a physical filtering or success-conditioning step. `F` and `rho` may be singular; the inherited coding theorem already handles only positive eigenvalues when defining spectral types.

## 6. Independent check of the actual norm budgets

Let `u=||X||_{2,sigma}`, `e=||F-I-X||_{2,sigma}`, and `r=bk<=1/256`. The inherited moments give

\[
 \mathcal P(H^2)\le3k^2I,\qquad
 \operatorname{Tr}\sigma H^4\le105k^4.
\]

Hence `||D-I||<=3 gamma^2 r^2/4` and `||R-I||<=3 gamma^2 r^2/8`. Expanding the actual normalized matrix, without commuting `R` through `X`, gives

\[
 F-I-X=(RXR-X)+\frac14R[X^2-\mathcal P(X^2)]R.
\]

Weighted `L^2` contraction on the right uses `[R,sigma]=0`; left contraction uses `||R||<=1`. Pinching is an orthogonal projection in this weighted `L^2` space. Consequently

\[
 e\le\frac{3\gamma^2r^2}{4}u
       +\frac{\sqrt{105}}4\gamma^2r^2
 \le3\gamma^2r^2.
\]

Let `eta=||T-I||=2mb^2<=r^2/32`. Then

\[
 Y=T(F-I)-X,\quad \mathcal P(Y)=0,
\qquad
 \|Y\|_{2,\sigma}\le(1+\eta)e+\eta u<4\gamma^2r^2.
\]

All these matrices are Hermitian. Applying the new response estimate bounds the whole nonlinear correction by

\[
 \|D_b(\sigma Y)\|\le8\gamma^2r^3
 \le16\ell r\,\mathcal B,
 \qquad\mathcal B=\ell vb^2.
\]

The final inequality uses `v>=k^2/32`. The exact inherited endpoint response is used only for `X`, never silently extended to the nonlinear `F`.

## 7. Concrete drift and entropy constants

Assume also `b<=1/1024`, so `a>=1023/1024`. The signed affine comparison satisfies

\[
 D_b(\sigma T+\sigma X)
 \le-a\mathcal B(1/16-2r)I.
\]

To retain the requested final bound `D_b(rho)<=-a mathcal B I/128`, it suffices that

\[
 a(7/128-2r)\ge16\ell r.
\]

At the worst permitted parameters, the left side is at least `(1023/1024)(3/64)`, while the right side is less than `0.7/16`. Their rational difference is `1009/327680>0`. Thus the drift constant passes with strict margin.

For entropy, `rho` commutes with `sigma`, and normalization gives the global chi-square bound

\[
 D_2(\rho\Vert\sigma)
 \le\frac1\ell\operatorname{Tr}\sigma(TF-I)^2.
\]

The diagonal and offdiagonal terms are orthogonal in weighted `L^2`, so

\[
 \operatorname{Tr}\sigma(TF-I)^2
 \le4m^2b^4/k+(1+\eta)^2(u+e)^2.
\]

The bounds `e/u<=5r`, `eta<=r^2/32` imply

\[
 (1+\eta)^2(1+5r)^2
 \le(1+2^{-21})^2(261/256)^2<17/16.
\]

With `u_0=vb^2/k<=r^2/16`, the charge-tilt variance contributes `9u_0 mathcal B/256`, less than `mathcal B/256`. Therefore

\[
 D_2(\rho\Vert\sigma)\le18\mathcal B/256,
\qquad
 S(\rho)-3k/2\ge24\mathcal B/256-18\mathcal B/256
 >\mathcal B/64.
\]

The owner's stated entropy constant is thus conservative and valid.

Finally, for `0<beta<=1/32`, the choice `k=floor[1/(256b)]` has `k>=4`, meets all windows, and satisfies `k>=1/(512b)`. The inherited coding theorem consequently yields

\[
 Q(V_\beta,\tau)\ge\frac32+rac{\ell v_kb^2}{64k}
 \ge\frac32+\frac{\ln2}{2^{20}}\beta^2.
\]

The exact root-retaining operator-coding theorem accepts this density and drift hypothesis without a scalar depth chain. Its initializer-independent sequence remains pointwise for each fixed normal initializer, in full diamond norm. The half-diamond convention is exactly half the full error. `beta,k,rho` stay fixed before the outer coding horizon. No terminal bath return or efficient encoder follows.

## 8. Concrete omitted-premise failures

- The response estimate is bulk only. For one call with input port zero and an initial vacuum, the actual `U` exchanges vacuum seeds and leaves port charge zero. The diagonal displacement is zero, whereas the bulk formula would give `-a`. Extending the diagonal identity through the root is false.
- Offdiagonal removal is essential. A diagonal charge-preserving `Y` can have nonzero response already at `b=0`; an `O(bk)` bound for all `Y` is false. For example `Y=Q-k/2` has diagonal response `k/2` at `b=0` under the actual `sigma`.
- Total-charge pinching is performed before the row-square estimate. The proof does not bound all unequal-charge blocks of the unpinched `G` by the displayed even-distance series.
- `T` must commute with `F` if one writes `rho=sigma TF`. An arbitrary pattern-dependent positive matrix need not commute with `F`, and its unsymmetrized product need not be Hermitian. The actual charge-only tilt meets the required premise.
- `D` need not commute with `H`; treating it as a scalar normalization would be an invalid shortcut. The estimates above retain both left and right factors.

## 9. Assessment and remaining boundary

No concrete flaw was found in the new full-operator response mechanism or the displayed Gram-input transfer. The argument pays higher-endpoint coherences by their weighted norm and the all-distance history bound. It does not merely improve an affine spectral norm estimate or use a scalar-prefix average.

The new input changes the positive family and resolves the logarithmic loss for an admissible construction. It does not prove that the original positive-part family has controlled correction at fixed `bk`; that separate family-specific question remains open. No sharp capacity exponent, feedback equality, upper converse, historical priority, useful finite code, or efficient preparation is certified by this challenge.

Observed checks were source reading, analytic derivations, and exact rational verification of the two displayed constant inequalities. Their role is a concrete load-bearing consistency check, not discovery-cost measurement. Total reasoning/review cost was not instrumented and remains unknown. No physical runs, paid compute, or outreach were performed.
