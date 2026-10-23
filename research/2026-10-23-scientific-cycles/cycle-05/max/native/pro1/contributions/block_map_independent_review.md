# Independent focused review of the correlated block map

Reviewer: `two_call_entropy`, separately assigned after completion of the
entropy certificate. Review date: 22 October 2026.

## Source and scope

Reviewed `CORRELATED_CAPACITY_GAIN.tex`, the sections “The exact correlated
block map” and “A closed depth law with the exact boundary,” equations
(5)–(15), and the later added separable decomposition (21a). Compared with
`contributions/two_call_algebra.md` and the unchanged native
`starting_source/Astra_Amplification_Cycle3_PRO1_20261022/representation/exact_representation.py`,
especially its `port_matrix`, `amplitude`, and exact root/Fock multiplication
rules. This was an independent algebraic reconstruction of the load-bearing
identities, not another finite-cutoff simulation or a repeat of the code theorem.

**Finding:** No correction is needed in the reviewed map, depth-kernel or
separability formulas. The statements are valid with the retained root exchange
on the full infinite bath. The review details below identify why arbitrary
trace-class inputs and coherent bath initializers are covered.

## 1. Ordered amplitudes and complete off-diagonal map

Write `h=alpha beta`, `a=alpha^2`, `b=beta^2`,
`f=alpha^3 beta=a h`, `P_j=S_j S_j*`, and `P=I-P0`.
The actual time order is
`K_(o1 o2,i1 i2)=V_(o2 i2) V_(o1 i1)`, matching `amplitude()` in the native
representation. `RS_j=0` and `S_k* S_j=delta_kj I` give the four common
nonzero output amplitudes for input pair `(j0,0j)`:

| Output | Input `j0` | Input `0j` |
|---|---|---|
| `00` | `i h S_j` | `a S_j R+i h S_j` |
| `0j` | `a I` | `i h R-b I` |
| `j0` | `i h R-b I` | `a P_j` |
| `jj` | `i h S_j*` | `i h S_j*` |

Other output words can occur for one input, but not for both, and hence do
not contribute to their cross map. For an arbitrary trace-class X, adding
`K_left X K_right* + K_right X K_left*` row by row gives:

| Output | Contribution for fixed j |
|---|---|
| `00` | `2ab S_j X S_j* + i f S_j(XR-RX)S_j*` |
| `0j` | `-2ab X + i f(RX-XR)` |
| `j0` | `-ab(XP_j+P_jX)+i f(RXP_j-P_jXR)` |
| `jj` | `2ab S_j* X S_j` |

Summing j and using `sum_j P_j=I-P0` proves exactly

\[
 \Gamma(X)=ab[2\mathcal C(X)+2\mathcal D(X)-6X+P_0X+XP_0]
 +if[\mathcal C([X,R])+2[R,X]+RXP-PXR].
\]

In particular the real `-6X` coefficient and the sign of the imaginary root
terms are correct. There was no replacement of `X` by `X*`, so this derivation
is complex-linear and works for non-Hermitian trace-class X as claimed. All
left and right factors are bounded; the finite sum defines a bounded normal
map on the trace class. The diagonal input terms give
`x A^2+y(AB+BA)+zB^2`, with composition in the stated order.

As a separate normalization check, `Tr C(X)=2 Tr X` and
`Tr D(X)=Tr[(I-P0)X]` cancel the trace of the real cross term. The trace of
each imaginary commutator vanishes, and `PR=RP=0` cancels the remaining root
pieces. Thus `Tr Gamma(X)=0`. A is trace preserving and B multiplies trace
by two, so the trace of the complete map is
`(x+4y+4z)Tr X=Tr X`. Complete positivity belongs to the full map obtained
from the positive input density and the actual unitary; it is not claimed
for Gamma alone. This distinction is correctly stated in the manuscript.

## 2. Dual closure is stronger than radial-state preservation

For a bounded depth function `Y=g(L)`, exact Fock shifts give

\[
 \mathcal D(Y)=2g(L+1),\qquad
 \mathcal C(Y)=g(L-1)(I-P_0),\qquad RYR=g(0)P_0.
\]

Thus

\[
 A^*g(L)=b g(L)+a g((L-1)_+),\qquad
 B^*g(L)=2b g(L)+2a g(L+1).
\]

The imaginary dual of Gamma is

\[
 if\{[R,\mathcal D(Y)]+2[Y,R]+PYR-RYP\}.
\]

Every term vanishes for this Y: `D(Y)=2g(L+1)` is scalar on the vacuum,
`[Y,R]=0`, and `PR=RP=0`. Therefore the entire exact dual is

\[
 \Gamma^*g(L)=ab\{4g(L+1)+2g(L-1)(I-P_0)-6g(L)+2g(0)P_0\}.
\]

This establishes the bounded observable identity, not merely equality of
expectations for radial inputs. Since the dual preserves the whole depth
algebra, iteration applies to every normal initializer, including coherent
states between and within levels. Such states need not become radial. Their
depth probabilities nevertheless have the exact same kernel. This logical
step is valid; radial Schrödinger closure alone would not have sufficed.

For the separate radial statement, `e_l=P_l/2^(l+1)` obeys
`C(e_l)=2e_(l+1)`, `D(e_l)=e_(l-1)` for l>0 and zero at l=0.
`R e_0 R=e_0`, and `[e_l,R]=0`. The three identities in manuscript (11)
follow immediately, including `Gamma(e_0)=4ab(e_1-e_0)`.

## 3. Independent reconstruction of the five probabilities and two boundaries

In the bulk the unnormalized contributions of A and B are respectively a
down/stay step with weights `(a,b)` and an up/stay step with weights
`(2a,2b)`. Combining their ordered products and the cross term yields

\[
 (p_{-2},p_{-1},p_0,p_1,p_2)
 =\bigl(xa^2,\ 2ab(x+2y+c),\ b^2+4ya^2-6cab,
 4ab(y+2z+c),\ 4za^2\bigr).
\]

These agree with (12). At depth one, A squared sends mass `a+ab` to zero,
which equals `a^2+2ab`: precisely the `-2` and `-1` bulk contributions combined
at depth zero. Neither mixed ordering has another exceptional contribution
there. Thus clamping only the `-2` transition at depth one is correct.

At the vacuum, A fixes `e_0`, and the two mixed orderings give

\[
 AB(e_0)=(2a^2+2b)e_0+2ab e_1,\qquad
 BA(e_0)=2b e_0+2a e_1.
\]

With `B^2(e_0)=4b^2e_0+8ab e_1+4a^2e_2` and the exact Gamma root row,

\[
 \begin{aligned}
 P(0,0)&=x+y(2a^2+4b)+4zb^2-4cab,\\
 P(0,1)&=2ay(1+b)+8zab+4cab=p_1+2ya^2,\\
 P(0,2)&=4za^2=p_2.
 \end{aligned}
\]

This reproduces (13). It also independently checks the stated positivity:
using `|c|<=y`, the first row entry is at least
`x+2ya^2+4yb^2+4zb^2`, and the second at least `2a^2y+8zab`.
The bulk zero-step lower bound in the manuscript is correct. Normalization
uses `a+b=1` and `x+4y+4z=1`.

The bulk first moment is

\[
 d=-2ax+8az+2ab c=4a\delta+2ab c.
\]

Thus **negative real c lowers the drift**, exactly as required by the chosen
construction. At the root the extra drift is

\[
 2p_{-2}+p_{-1}+2ya^2=2a[x+y(1+b)+bc],
\]

and at depth one it is `p_-2=xa^2`. This proves (15), including its root
coefficient. The expression is a bounded increment identity; it does not
authorize subtraction of two infinite expectations. The grade argument in
the manuscript gives the stated domain-safe interpretation.

## 4. Added separable averaging-density decomposition

Checked proposition (21a) after its addition. Write
`H_j(phi)=e^(i phi)|j><0|+e^(-i phi)|0><j|`,
`sigma=diag(q,(1-q)/2,(1-q)/2)` and `u=beta/8`.
The only nontrivial 2-by-2 minor of `sigma±u H_j(phi)` has determinant
`q(1-q)/2-u^2=y-u^2>1/9-1/64>0`; their trace is one. Hence every displayed
factor is a density.

The phase average over `0,pi/2,pi,3pi/2` kills both H's first moment and the
terms in `H tensor H` proportional to `exp(±2i phi)`. It retains precisely
`|j0><0j|+|0j><j0|`. Therefore the average of
`(sigma+uH) tensor (sigma-uH)` over four phases is
`sigma tensor sigma-u^2(|j0><0j|+|0j><j0|)`.
Averaging j=1,2 gives coefficient `-u^2/2=-b/128=c`, with unchanged product
diagonal. The decomposition and normalization are correct. The text properly
restricts separability to the selected average density, not the eventual
isometric quantum code.

## Status and limits of this review

The reviewed algebra, full-map scope, imaginary-root cancellation, all five
bulk probabilities, both boundary rows, bulk-coherence sign, and separable
average are accepted internally. No finite truncation, stationarity simulation
or new numerical replay was used. This review does not re-prove the inherited
compression/coding theorem or certify the full capacity argument externally.
The entropy certificate was my earlier separate contribution; it was not
counted as an independent review of itself. Historical originality, efficient
implementation and physical performance remain separate questions.
