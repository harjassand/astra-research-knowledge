# Exact charge bias of the actual temporal operator

Cycle10 bounded contribution. This result uses the original Cycle7 `H_k`,
not an endpoint-distance surrogate. Source read: the actual three-case token
normal form in `SHARP_TEMPORAL_GROWTH.tex`, sections 3--4, carried into the
Cycle9 `INHERITED_ENDPOINT_RESPONSE.tex`. All statements about `H` concern
the input operator defined by the physical **bulk coefficient**. No root
identity, physical prefix preparation, or independent fresh-channel model is
introduced.

## 1. Exact theorem

Let

\[
\sigma_p=\operatorname{diag}(1-p,p/2,p/2)^{\otimes k},\qquad
\sigma=\sigma_{1/2},\qquad A=Q-k/2,
\]

and retain the fixed Cycle7 `H_k` (it is not reoptimized when `p` changes).
For a simple symmetric walk `S_j` starting at zero, define

\[
c_k=\operatorname{Tr}(\sigma A H_k^2).
\]

Then for every `k>=2`,

\[
\boxed{c_k=\frac18\sum_{j=1}^{k-2}(k-1-j)\,\mathbb E|S_j|.}
\tag{1}
\]

Consequently `c_2=0`, `c_k>0` for `k>=3`, and

\[
\boxed{c_k=\frac{\sqrt{2/\pi}}{30}k^{5/2}+O(k^{3/2}).}
\tag{2}
\]

This is an all-length analytic identity. The included bounded exact replay
checks its implementation, not its asymptotic validity.

## 2. Reduction to minima of a walk

Different endpoint pairs occupy disjoint binary-charge matrix blocks.
Therefore all cross terms in the trace of `sigma_p H^2` vanish. On a fixed
oriented block `01`, the exact inherited color operator is

\[
K=P(I-\mathrm{SWAP}),\quad P/2,\quad0
\]

according as `h>d`, `h=d`, or `h<d`. Here `h` is the unmatched push count
before the earlier endpoint and `d` is the middle pop deficit. The normalized
color traces of `K* K` are respectively `1`, `1/4`, and `0`:
`(I-SWAP)^2=2(I-SWAP)` and a swap of two color qubits has normalized trace
`1/2`. The reversed endpoint block has the same singular-value trace.

For endpoints `i<j`, put `r=j-i-1`, `n=i+r`. The two endpoint orientations
together have probability `2p(1-p)`. The charge bits before and between them
are independent Bernoulli `p`; the later suffix does not enter the trace.
Concatenate these two parts into a length-`n` walk with increments `+1` for
a color charge and `-1` for zero. At the split `i`,

\[
h=S_i-\min_{0\le u\le i}S_u,\qquad
d=S_i-\min_{i\le u\le n}S_u.
\]

Let `f_n` and `ell_n` be the first and last times of the global minimum of
the entire walk, including time zero. Then exactly

\[
h>d\iff i>\ell_n,\qquad
h=d\iff f_n\le i\le\ell_n.
\]

Summing all `n+1` possible splits gives

\[
\sum_{i=0}^{n}\left(1_{h>d}+\frac14 1_{h=d}\right)
=n-\frac34\ell_n-\frac14 f_n+\frac14.
\]

Thus the exact tilted second moment is

\[
v_k(p):=\operatorname{Tr}(\sigma_p H_k^2)
=2p(1-p)\sum_{n=0}^{k-2}
\left[n+\frac14-\frac34\mathbb E_p\ell_n
                         -\frac14\mathbb E_p f_n\right].
\tag{3}
\]

No asymptotic probability approximation has occurred.

## 3. Elementary derivation of the needed argmin derivatives

The following generating-function proof avoids invoking an unproved general
argmin or fluctuation theorem. All identities are identities of formal power
series, so coefficient differentiation at `p=1/2` is legitimate.

Let `a_n(p)` be the probability that every partial sum of a length-`n` walk
is nonpositive, and `A_p(z)=sum a_n(p) z^n`. Set `q=1-p` and

\[
C_p(z)=\sum_{m\ge0}\mathrm{Cat}_m(pqz^2)^m
=\frac{2}{1+\sqrt{1-4pqz^2}}.
\]

This is the generating series of nonpositive excursions ending at zero:
a balanced excursion with `m` upward and `m` downward steps has weight
`(pq)^m`, and the Catalan first-return decomposition proves
`C_p=1+pq z^2 C_p^2`.

An alive nonpositive path fails on its next step exactly when it is at zero
and takes a positive step. Therefore

\[
(1-z)A_p(z)=1-pzC_p(z).
\tag{4}
\]

Let `B_p(z)` generate paths whose every partial sum is strictly positive,
including the empty path. Decompose any walk at its **last** global minimum.
The reversed prefix is nonpositive and the remaining suffix is strictly
positive. Independence, together with invariance of iid weights under
reversal, gives

\[
\Pr_p(\ell_n=j)=a_j(p)b_{n-j}(p),\qquad
A_p(z)B_p(z)=\frac1{1-z}.
\]

Hence

\[
\sum_{n\ge0}\mathbb E_p\ell_n z^n
=\frac{z}{1-z}\frac{\partial}{\partial z}\log A_p(z).
\tag{5}
\]

Decomposing at the **first** global minimum instead gives a reversed
strictly negative prefix and a nonnegative suffix. Replacing `p` by `q`
changes signs, so

\[
\sum_{n\ge0}\mathbb E_p f_n z^n
=\frac{z}{1-z}\frac{\partial}{\partial z}\log B_q(z)
=\frac{z}{1-z}\left[\frac1{1-z}
                   -\frac{\partial}{\partial z}\log A_q(z)\right].
\tag{6}
\]

At `p=1/2`, the derivative of `C_p(z)` in `p` vanishes. With
`s=sqrt(1-z^2)`, equation (4) yields

\[
\left.\partial_p\log A_p(z)\right|_{1/2}
=-\frac{zC_{1/2}(z)}{1-zC_{1/2}(z)/2}
=1-\frac{1+z}{s}.
\]

Equations (5) and (6) therefore have the same `p` derivative at the fair
point, namely

\[
-\frac{z(1+z)}{(1-z)(1-z^2)^{3/2}}
=-\frac{z}{(1-z)^2\sqrt{1-z^2}}.
\tag{7}
\]

For the symmetric walk,
`E|S_{j+1}|-E|S_j|=Pr(S_j=0)`. Since the return generating function is
`1/sqrt(1-z^2)`,

\[
\sum_{j\ge0}\mathbb E|S_j|z^j
=\frac{z}{(1-z)\sqrt{1-z^2}}.
\]

Comparing with (7) proves the exact derivative identities

\[
\left.\frac{d}{dp}\mathbb E_p\ell_n\right|_{1/2}
=\left.\frac{d}{dp}\mathbb E_p f_n\right|_{1/2}
=-\sum_{j=1}^n\mathbb E|S_j|.
\tag{8}
\]

## 4. Finishing the moment identity and asymptotic

Differentiating the reference density gives

\[
\frac{d}{dp}v_k(p)
=\frac{\operatorname{Tr}[\sigma_p(Q-kp)H_k^2]}{p(1-p)}.
\]

The derivative of `2p(1-p)` vanishes at `p=1/2`. Combining (3) and (8),

\[
v'_k(1/2)=\frac12\sum_{n=0}^{k-2}\sum_{j=1}^n\mathbb E|S_j|.
\]

Since `c_k=v'_k(1/2)/4`, reversing this finite double sum proves (1).

The exact elementary values are

\[
\mathbb E|S_{2m}|=2m\binom{2m}{m}4^{-m},\qquad
\mathbb E|S_{2m+1}|=(2m+1)\binom{2m}{m}4^{-m}.
\]

Stirling's formula yields `E|S_j|=sqrt(2j/pi)+O(j^{-1/2})`. Therefore

\[
\sum_{j=1}^{k-2}(k-1-j)\sqrt j
=\frac4{15}k^{5/2}+O(k^{3/2}),
\]

and the weighted error is `O(k^{3/2})`. This proves (2).

## 5. Operationally relevant failure of raw squaring

The actual normalized positive square

\[
\rho_t=\frac{\sigma(I-tH)^2}{1+t^2v_k}
\]

has exact charge excess

\[
\boxed{\operatorname{Tr}(A\rho_t)
=\frac{t^2c_k}{1+t^2v_k}.}
\tag{9}
\]

For `t=gamma b`, `bk -> r>0`, this is asymptotic to

\[
\frac{\gamma^2r^2\sqrt{2/\pi}}
     {30(1+\gamma^2r^2/8)}\sqrt k.
\tag{10}
\]

Thus normalizing only by total trace does not preserve the charge budget.
It creates a positive charge bias diverging as `sqrt(k)` in the proposed
long-block regime. This is an exact obstruction to treating the quadratic
repair as a bounded charge-cost correction.

Equation (10) alone does not establish outward drift at nonzero `b`; its
offdiagonal physical response must also be bounded. The receiving Cycle10
full-prefix response theorem supplies exactly that missing bound, as follows.

### 5.1 Full-operator outward-drift consequence

Use the independently proved Cycle10 response interface: on initial depth
at least `k`, for any charge-preserving input operator `Y` with
`P(Y)=0`,

\[
\|D_b(\sigma Y)\|\le2r\|Y\|_{2,\sigma},\qquad
r=bk\le1/2,\qquad
\|Y\|_{2,\sigma}^2=\operatorname{Tr}(\sigma Y^*Y).
\tag{14}
\]

The complete-pattern diagonal response is exactly
`2(1-b) Tr(sigma A Y_diag) I`. This includes color operators within a
fixed binary pattern: distinct move/stay masks have distinct output charge
words, so that diagonal displacement is scalar on the input-color/bath
fiber. Equation (14), rather than a single-prefix expectation, is the
separate load-bearing response dependency of the following corollary.

For `F_t=(I-tH)^2/(1+t^2 v_k)`,

\[
(F_t)_{\rm off}
=\frac{-2tH+t^2(H^2-\mathcal P(H^2))}{1+t^2v_k}.
\]

Pinching is an orthogonal projection in the weighted Hilbert--Schmidt norm
because `sigma` commutes with its projections. The inherited fourth moment
is `Tr sigma H^4<=105 k^4`. Consequently

\[
\|(F_t)_{\rm off}\|_{2,\sigma}
\le\frac{2|t|\sqrt{v_k}+t^2\sqrt{105}\,k^2}{1+t^2v_k}
\le\frac{|t|k}{\sqrt2}+\sqrt{105}(tk)^2.
\tag{15}
\]

Fix any `gamma>0` and `0<r<=1/2`, and take the small-angle family
`b=r/k`, `t=gamma b`. Combining (9), (14), and (15) yields the exact bulk
operator lower bound

\[
\boxed{D_b(\rho_t)\ge
\left[
\frac{2(1-b)t^2c_k}{1+t^2v_k}
-2r\left(\frac{\gamma r}{\sqrt2}+\sqrt{105}\gamma^2r^2\right)
\right]I.}
\tag{16}
\]

The first term grows as a strictly positive constant times `sqrt(k)` by
(2), while the subtracted term is independent of `k`. Thus the actual
normalized raw-square input has **strict uniform outward bulk drift for
every sufficiently large k**, and its bulk drift lower bound diverges as
`sqrt(k)`. All colors and coherent/entangled bath prefixes are included.

This closes the raw-square proposal as a replacement for the inward-drift
code construction at fixed positive `bk`. It does not prove a capacity
converse, escape from every initializer, or failure of every possible code
using that density. It does not establish any corresponding assertion for
the Cycle9 positive-part input. The parameter family varies `b` with `k`
only in this outer small-angle statement; each physical device and input
block must still be fixed before its own coding horizon.

## 6. Exact charge-preserving normalization interface

There is a finite-dimensional repair that removes this issue exactly.
Let `P` be complete binary-charge-pattern pinching, let `H=H*` preserve total
charge and satisfy `P(H)=0`, and let `sigma=f(Q)` be faithful. For real `t`,
define

\[
C=I-tH/2,\qquad D=\mathcal P(C^2)
=I+t^2\mathcal P(H^2)/4,\qquad
F=D^{-1/2}C^2D^{-1/2}.
\tag{11}
\]

Then `D>=I`, so all inverses exist, `F>=0`, `[F,Q]=0`, and

\[
\boxed{\mathcal P(F)=I.}
\tag{12}
\]

Indeed `D^{-1/2}` belongs to the range algebra of `P`; the bimodule
identity of block pinching gives
`P(D^{-1/2} C^2 D^{-1/2})=D^{-1/2} D D^{-1/2}`. This does not assume
that `D` commutes with `H`. It commutes with `sigma` because both preserve
charge and `sigma` is scalar on each total-charge sector.

For every strictly positive charge-only tilt `T(Q)` with
`Tr sigma T=1`, the actual density

\[
\rho=\sigma T(Q)F
\]

is positive, normalized, preserves total charge, and obeys

\[
\mathcal P(\rho)=\sigma T(Q),\qquad
\operatorname{Tr}(g(Q)\rho)=\operatorname{Tr}(g(Q)\sigma T(Q))
\tag{13}
\]

for every function `g`. Thus its charge budget is set exactly by the tilt.
This is a definition of the physical input density, not a successful
filtering branch or a bath operation.

For the inherited `H`, the moment theorem gives
`0<=D-I<=3t^2 k^2 I/4`. Hence the normalizer is uniformly close to identity
when `|t|k` is small, even though `||H||` can grow faster than `k`.
Equation (9) is the load-bearing counterexample to replacing this conditional
normalization by the scalar `Tr sigma C^2`.

The remaining receiving obligations are entropy and the full offdiagonal
operator response of (11)--(13), followed by the unchanged root/coding
theorem. This contribution does not certify those obligations on its own.
