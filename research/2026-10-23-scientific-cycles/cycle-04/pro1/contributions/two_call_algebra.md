# Exact correlated two-call bath map and radial closure

Independent contribution by `two_call_algebra`, 22 October 2026. This derives the
new block map on the entire two-seed Fock bath. It does not iterate the closed iid
theorem, remove the root, or assume a finite reflecting bath.

## Definitions and exact map

Write `a=alpha^2`, `b=beta^2`, so `a+b=1`; use `P0=R^2`, `P=I-P0`, and

\[
 \mathcal C(X)=\sum_{j=1}^2S_jXS_j^*,\qquad
 \mathcal D(X)=\sum_{j=1}^2S_j^*XS_j.
\]

The bath maps of a zero input and the unnormalized sum of the two colored inputs
are, respectively,

\[
 A(X)=a(RXR+\mathcal D(X))+bX-i\alpha\beta[R,X],\qquad
 B(X)=a\mathcal C(X)+2bX.
\]

`A` is trace preserving, while `B` multiplies the trace by two. Composition is
right-to-left. For the specified normalized block input the exact map is

\[
 \Phi=X\longmapsto x A^2(X)+y(AB+BA)(X)+z B^2(X)+c\Gamma(X),                 \tag{1}
\]

where

\[
\begin{aligned}
 \Gamma(X)={}&ab\{2\mathcal C(X)+2\mathcal D(X)-6X+P_0X+XP_0\}\\
 &+i\alpha^3\beta\{\mathcal C([X,R])+2[R,X]+RXP-PXR\}.                    \tag{2}
\end{aligned}
\]

The cross map `Gamma` by itself is not positive; complete positivity belongs to
(1) with the input inequalities `x,z>=0`, `y>=|c|`, `x+4y+4z=1`.

### Derivation without deleting any root overlap

Let `Q=alpha R+i beta I`. For input words `(j,0)` and `(0,j)`, the common output
words that contribute to the off-diagonal bath map are exactly `(0,0)`, `(0,j)`,
`(j,0)`, and `(j,j)`. Their two amplitudes, in this order, are

| Output | Input `(j,0)` | Input `(0,j)` |
|---|---|---|
| `(0,0)` | `i alpha beta S_j` | `alpha^2 S_j R+i alpha beta S_j` |
| `(0,j)` | `alpha^2 I` | `i alpha beta R-beta^2 I` |
| `(j,0)` | `i alpha beta R-beta^2 I` | `alpha^2 S_j S_j*` |
| `(j,j)` | `i alpha beta S_j*` | `i alpha beta S_j*` |

This table follows by multiplying `V_(out2,in2) V_(out1,in1)` in that time order
and using `RS_j=S_j*R=0`, `S_j*S_j=I`. Sum the maps `K_left X K_right*` and their
Hermitian partner, then sum over j. The real terms give the first line of (2),
and the imaginary terms give the second. This verifies (2) as a linear map on
all trace-class X, not just on Hermitian or diagonal X.

## Exact depth Markov chain

Let `e_l=P_l/2^(l+1)` be the normalized uniform state on depth l. All three maps
`A`, `B`, `Gamma` preserve the linear span of these states. The root exchange
commutes with every `e_l`, and its root action is retained:

\[
\begin{array}{ll}
 A(e_0)=e_0,&A(e_l)=a e_{l-1}+b e_l\quad(l\ge1),\\
 B(e_l)=2a e_{l+1}+2b e_l,&\Gamma(e_0)=4ab(e_1-e_0),\\
 &\Gamma(e_l)=ab(4e_{l+1}+2e_{l-1}-6e_l)\quad(l\ge1).
\end{array}                                                            \tag{3}
\]

In particular the actual `tau_pi` remains radial at every block boundary.
More strongly, the dual of (1) preserves the algebra of all bounded functions
of L. For `A* f(L)`, the commutator vanishes because `[R,f(L)]=0`; the shift
relations give the backward version of (3). For `Gamma* f(L)`, the imaginary
terms vanish: `C* f(L)=2f(L+1)` commutes with R, and both `P f(L)R` and
`R f(L)P` vanish. Thus **the depth distribution follows the same Markov chain
for every normal initial bath**, even if its within-level matrix is not radial.

For l>=2, the five increment probabilities are

\[
\begin{array}{c|c}
k&p_k\\\hline
-2&xa^2\\
-1&2ab(x+2y+c)\\
0&b^2+4ya^2-6cab\\
+1&4ab(y+2z+c)\\
+2&4za^2.
\end{array}                                                            \tag{4}
\]

They sum to one. Their positivity follows from the admissibility inequalities;
for the only less immediate entry,

\[
 p_0=b^2(x+4z)+4y(a^2+b^2)-6cab
 \ge b^2(x+4z)+y\{4(a-b)^2+2ab\}\ge0.
\]

At l=1 the `-2` transition is clamped to zero, so
`P(1,0)=p_-2+p_-1`, `P(1,1)=p_0`, `P(1,2)=p_+1`, `P(1,3)=p_+2`.
At l=0,

\[
 P(0,2)=p_{+2},\quad
 P(0,1)=p_{+1}+2ya^2,\quad
 P(0,0)=1-p_{+1}-2ya^2-p_{+2}.                                        \tag{5}
\]

Equivalently,

\[
 P(0,0)=x+y(2a^2+4b)+4zb^2-4cab,\qquad
 P(0,1)=2ay(1+b)+8zab+4cab.
\]

These entries are nonnegative: using `c<=y` bounds `P(0,0)` below by
`x+2ya^2+4yb^2+4zb^2`; using `c>=-y` bounds `P(0,1)` below by
`2a^2y+8zab`. Equations (4)-(5) are the real half-line chain with its exact
root boundary, not a finite reflecting truncation.

## Exact operator drift

Set `q=x+2y`, `delta=1/2-q`. The bulk drift is

\[
 d=\sum_k kp_k=2a(1-2q+bc)=4a\delta+2ab c.                            \tag{6}
\]

With `P1=sum_j S_j P0 S_j*`, the full bounded increment is

\[
 \boxed{\Phi^*(L)-L=dI+2a\{x+y(1+b)+bc\}P_0+xa^2P_1.}              \tag{7}
\]

This can be interpreted on the finite-coordinate core and extended as a bounded
form. The grade-one-call conservation relation also gives a direct domain-safe
proof: for each block amplitude `K_(out,in)`, `[L,K]=kK` with
`k=charge(in)-charge(out)`. The input coherences have equal charge, so their
common k can be taken outside each Kraus Gram term. Sum `k K_right* K_left`.

The four unnormalized input components separately give

\[
\begin{array}{c|c}
x&-2aI+2aP_0+a^2P_1\\
y&2a(1+b)P_0\\
z&8aI\\
c&2ab(I+P_0).
\end{array}                                                            \tag{8}
\]

Combining and using normalization proves (7). In particular, the one-site iid
obstruction cannot be invoked for this correlated family: negative c changes
the *bulk* drift linearly in `beta^2 c`, while its entropy penalty is quadratic
near the critical product point.

## Consequence available to the main proof

For every real t, let `m(t)=sum_k p_k exp(tk)`. For l>=2,

\[
 \Phi^*e^{tL}=m(t)e^{tL}
\]

on that level. The discrepancy is exactly supported on `P0+P1` and is obtained
from (5) and the clamped l=1 row. Thus if `d=m'(0)<0`, some fixed t>0 has
`m(t)<1`, and a true infinite-bath exponential Lyapunov bound follows. One must
retain the finite boundary remainder rather than pretend that the inequality
holds with no additive term at the vacuum.

This contribution does not itself assert a capacity gain, a reachable invariant
state, entropy control or arbitrary-reference coding. The parent is proving
those remaining obligations from the actual initializer.

## Executable verification and observed cost

`two_call_algebra.py` imports the unchanged exact Fock normal forms. Its scalar
ring is Gaussian-rational polynomials modulo `alpha^2+beta^2=1`, so it checks the
full parameter identity, not one numerical angle. It verifies (2) as a complete
superoperator, all four exact grade Gram operators including both boundaries,
trace preservation, the drift table (8), and bulk support. No bath truncation,
stationary approximation or floating point is used.

Replay:

```
python contributions/two_call_algebra.py --output contributions/two_call_algebra.json
```

The measured replay used approximately 0.024 seconds and 12.2 MiB maximum RSS
under Python 3.12.14 in this environment. These are replay costs only. Scientific
derivation/reasoning cost is not measured by that receipt. Internal agreement and
symbolic replay do not establish historical originality or external acceptance.
