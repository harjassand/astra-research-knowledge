# Exact entropy certificate for the correlated two-call family

Author: `two_call_entropy`, independent focused contribution to Astra Pro 1 Cycle4.

## Scope and input

The density is the nine-dimensional family in `CONTINUATION.md` of the unchanged
Cycle3 source. Its eigenvalues are `x` once, `z` four times, `y+c` twice and
`y-c` twice. Its two marginals are both `diag(q,(1-q)/2,(1-q)/2)` with
`q=x+2y`. Logs and entropies below are in bits. No bath state or physical
initialization is changed in these calculations.

## 1. Entropy as a charge budget

Let `rho_c=diag(1/2,1/4,1/4)`, `sigma=rho_c tensor rho_c`,
`delta=1/2-q`, and `S(varrho)=3+epsilon`. Since `-log2 rho_c=2I-|0><0|`,

\[
 D_2(\varrho\Vert\sigma)=4-2q-S(\varrho)=2\delta-\epsilon.
\]

Thus `S(varrho)>3` implies `delta>0` and `0<epsilon<=2delta`.
For this family, pinching the two coherent 2-by-2 sectors removes exactly

\[
 \Delta_c=4y\left[1-h_2\left(\frac{1+c/y}{2}\right)\right]
\]

bits of coherence. The formula is interpreted by continuity when `y=0`.
For `y>0`, the binary entropy inequality

\[
 1-h_2((1+t)/2)\ge\frac{t^2}{2\ln2}
\]

gives `Delta_c >= 2 c^2/(y ln2)`. Since dephasing preserves the diagonal
reference sigma, `D(varrho||sigma)>=Delta_c`. Consequently

\[
 c^2\le\frac{y\ln2}{2}(2\delta-\epsilon)
 \le\frac{\ln2}{4}\delta.
\]

This is a square bound, not `c=O(delta)`. For example, use the product diagonal
weights at `q=1/2-delta` and add `c=±sqrt(delta)/8`. Then, as `delta->0+`,

\[
 S(\varrho)-3=\left(2-\frac1{4\ln2}\right)\delta+O(\delta^2)>0.
\]

The family therefore does not permit absorbing an arbitrary term linear in
`beta^2 c` into an `O(beta^2 delta)` estimate. This is a counterexample to that
tempting attempted extension of the single-site obstruction, not a capacity
claim by itself.

For completeness, let `t=x-q^2`; then
`y=q(1-q)/2-t/2`, `z=(1-q)^2/4+t/4`. The exact relative-entropy decomposition is

\[
 2\delta-\epsilon=2[1-h_2(q)]+I(A_1:A_2)_\varrho.
\]

The diagonal classical correlation contribution to the mutual information is
at least `8t^2/ln2` by the classical Pinsker inequality: the diagonal total
variation distance to the product of the marginals is `2|t|`. The exact trace
norm of the complete difference from that product is
`2|t|+4 max(|c|,|t|/2)`. These supplementary bounds are not needed below.

## 2. A rigorous explicit entropy-above-three candidate

For any fixed `0<b<=1`, define

\[
 \delta=\frac{b^2}{512},\qquad c=-\frac b{128},\qquad q=\frac12-\delta,
 \qquad x=q^2,\quad y=\frac{q(1-q)}2,\quad z=\frac{(1-q)^2}4.
 \tag{C1}
\]

Eventually `b=beta^2`, with the angle fixed before the block-number limit.
The normalization `x+4y+4z=1` is exact. Since

\[
 y=\frac18-\frac{\delta^2}2\ge\frac18-\frac1{524288}>\frac19,
 \qquad |c|\le\frac1{128},
\]

positivity is strict. In fact every eigenvalue lies in `[1/16,1/4]`:
`z>=1/16`; `x>1/16`; `y-|c|>=15/128-1/524288>1/16`; and each is at most
`1/4` by the displayed formulas.

The diagonal part is the product of its marginals, so its entropy is
`2[h2(q)+1-q]`. Therefore the exact entropy is

\[
 S(\varrho)=3+2\delta-2[1-h_2(q)]-\Delta_c.\tag{C2}
\]

Here is a completely analytic lower bound, avoiding subtraction of nearby
floating-point entropies. For `|u|<1`, differentiating twice and integrating
from zero gives

\[
 \frac{u^2}{2\ln2}\le 1-h_2((1+u)/2)
 \le\frac{u^2}{2\ln2(1-u^2)}.\tag{C3}
\]

Using `ln2>=2/3`, `delta<=1/512`, `y>=1/9` and `|c|/y<=9/128`,

\[
 2[1-h_2(q)]\le
 \frac{4\delta^2}{\ln2(1-4\delta^2)}\le7\delta^2,
\]

\[
 \Delta_c\le
 \frac{2c^2}{y\ln2[1-(c/y)^2]}
 \le\frac{27}{1-81/16384}c^2<28c^2.
\]

The elementary lower bound `ln2>=2/3` follows, for example, by taking the first
term of `ln((1+t)/(1-t))=2 sum_{k>=0} t^(2k+1)/(2k+1)` at `t=1/3`.
Combining the inequalities,

\[
 \begin{aligned}
 S(\varrho)-3
 &\ge2\delta-28c^2-7\delta^2\\
 &=\frac9{4096}b^2-\frac7{262144}b^4\\
 &\ge\frac{569}{262144}b^2
 >\frac{b^2}{512}>0.\tag{C4}
 \end{aligned}
\]

At the actual fixed `beta=1/512`,

\[
 b=2^{-18},\qquad\delta=2^{-45},\qquad c=-2^{-25},\qquad
 S(\varrho)-3>2^{-45}.
\]

The inequality in (C4), rather than the numerical replay, is the entropy
certificate. It is uniform in `b in (0,1]`; no horizon-dependent angle or input
is used. The separate exact bath-map calculation gives bulk depth drift
`alpha^2(4delta+2b c)=-alpha^2 b^2/128` for this candidate. That map calculation
must be cited to its independent source; it is not proved by input entropy.

## 3. Spectral typicality useful for a whole-block coding proof

For one fixed candidate (C1), repeated independent *two-call blocks* have
density `varrho^tensor m`; this statement is about the input, not independent
channels or fresh baths. If `lambda` is sampled from its nine eigenvalues
with probability lambda, `Z=-log2 lambda` lies in `[2,4]` and has mean
`S(varrho)`. Hoeffding therefore gives

\[
 \Pr\{|m^{-1}\sum_{j=1}^m Z_j-S(\varrho)|>a\}
 \le2\exp(-ma^2/2),\qquad a>0.\tag{C5}
\]

The spectral typical projector has input mass at least the complementary
probability and eigenvalues between `2^{-m(S+a)}` and `2^{-m(S-a)}`. In
particular its rank is at most `2^{m(S+a)}` and at least
`(1-2exp(-ma^2/2))2^{m(S-a)}` when the lower factor is positive.
This supplies a finite-spectrum typicality input to an arbitrary-reference
coding argument. It does not by itself prove that the true evolving bath is
small, that a code decouples its complement, or that a decoder is efficient.

## 4. Charge and entropy flow for correlated blocks

For `m` independent copies of this correlated block input and an initially
independent bath of finite entropy and mean depth, total charge conservation
of the actual ordered `2m` interactions gives

\[
 S(B^{2m})\le m(4-2q)-\Delta\mathbb E L
             =m(3+2\delta)-\Delta\mathbb E L.
\]

This uses qutrit marginal entropy bounds and output subadditivity; no
independence of either the two ports inside a block or the outgoing ports is
assumed. The whole input entropy is `mS(varrho)+S(tau_0)`, hence

\[
 S(E_{2m})\ge S(\tau_0)+m(\epsilon-2\delta)+\Delta\mathbb E L.
\]

If some actual block-map corrected depth has drift `nu` with bounded
correction norm at most M, then `Delta E L>=m nu-2M`. This would force
extensive bath entropy when `nu>2delta-epsilon`. The corresponding
purified-complement coherent-information bound is

\[
 I_c\le m[3+4\delta-\epsilon-2\nu]+4M.
\]

For (C1) the bulk drift is negative, so the old positive-drift route has no
automatic extension. The long-time bath problem is a separate obligation.

## Validation and status

The independent source read was the unchanged Cycle3 `IID_INFORMATION.tex`,
`ENTROPY_AND_SCOPE.tex`, and `CONTINUATION.md`. The new elementary entropy proof
is complete above. A Decimal replay records the exact rational candidate,
high-precision observed entropy, and rational analytic certificate. Decimal
transcendental output is a diagnostic, not a rigorous interval enclosure;
the all-parameter analytic proof (C3)--(C4) supplies correctness. Historical
originality, efficient realization, physical significance, and a capacity
conclusion are not established by this contribution alone.

## 5. Exact spectral-type interface for bath-tail transfer

This supplements the entropy-typicality estimate with an input subspace whose
maximally mixed state is dominated by the actual product input with only a
polynomial factor. It is often the cleaner interface for a finite-environment
coding lemma.

Let the nine eigenvalues of the fixed candidate be `lambda_1,...,lambda_9`.
For integer `m>=32`, choose counts `n_i` by rounding each `m lambda_i` down,
then adding one to those with the largest fractional parts until the counts
sum to m. Define `p_i=n_i/m`. Then

\[
 \sum_i p_i=1,\qquad |p_i-\lambda_i|\le1/m,\qquad p_i\ge1/32.
\]

Let `T_m` be the span of eigenbasis words with exactly `n_i` occurrences of
symbol i, `D_m=dim T_m`, `P_m` its projector and `sigma_m=P_m/D_m`.
All words in this type have the same eigenvalue in `varrho^tensor m`, so

\[
 \varrho^{\otimes m}\ge w_m\sigma_m,
 \qquad w_m=\Tr(P_m\varrho^{\otimes m}).\tag{T1}
\]

The standard elementary type bound is

\[
 (m+1)^{-9}2^{mH_2(p)}\le D_m\le2^{mH_2(p)}.
\]

For an explicit proof of the lower bound, draw m symbols with probabilities
p. The count vector `mp` is a mode of this multinomial distribution: for
each coordinate, the ratio of its factor at any other count `k_i` to its
factor at `n_i` is at most `m^{-(k_i-n_i)}`. For `k_i>n_i`, this follows from
`n_i!/(n_i+r)! <= n_i^{-r}`; for `k_i<n_i`, from
`n_i!/(n_i-r)! <= n_i^r`; multiplication and `sum k_i=sum n_i` give a ratio
at most one. There are at most `(m+1)^9` types. The modal type therefore has
probability at least `(m+1)^-9`. Since each word of that type has probability
`2^-mH(p)`, the claimed dimension bound follows. The upper bound follows
because this type probability cannot exceed one.

The inequality `ln u<=u-1`, together with `sum_i(p_i-lambda_i)=0`, gives

\[
 D_2(p\Vert\lambda)\le\frac1{\ln2}
      \sum_i\frac{(p_i-\lambda_i)^2}{\lambda_i}
 \le\frac{144}{m^2\ln2}.
\]

Consequently

\[
 w_m\ge(m+1)^{-9}2^{-mD_2(p\Vert\lambda)}
      \ge(m+1)^{-9}\exp(-144/m).\tag{T2}
\]

For `f(u)=-u log2 u`, `|f'(u)|<=4` on `[1/32,1/4+1/32]`. The mean-value
theorem therefore gives `|H(p)-S(varrho)|<=36/m`. In particular,

\[
 \log_2D_m\ge m S(\varrho)-36-9\log_2(m+1).\tag{T3}
\]

Now let `Gamma_m` be **any actual** CP input-to-bath channel for m ordered
two-call interactions using the same fixed bath. No repeated fresh-bath
channel is substituted. Applying positivity to (T1) gives

\[
 \Gamma_m(\sigma_m)\le w_m^{-1}
           \Gamma_m(\varrho^{\otimes m}).\tag{T4}
\]

Thus every positive observable tail bound on the unconditioned product-block
average transfers to the uniform type input at cost `w_m^-1`. Suppose a
separately proved long-time estimate is

\[
 \sup_m\Tr[e^{tL}\Gamma_m(\varrho^{\otimes m})]\le C
 \quad(t>0,\ C<\infty\text{ fixed before }m\to\infty).
\]

For any fixed k>0, take a depth cutoff at least

\[
 \ell_m=\frac{(9+k)\ln(m+1)+\ln C+144/m}{t}.
\]

Then (T2)--(T4) and Markov's inequality show that the type-input final bath
has mass outside `L<=ceil(ell_m)` at most `(m+1)^-k`. Its coordinate support
dimension is `2(2^(ceil(ell_m)+1)-1)`, polynomial in m for fixed t, even if
the exponent is extremely large. This is an analytic compression statement,
not an implemented bath cutoff and not a change of initialization.

If the complement includes a purification F of the actual `tau_pi`, its
unchanged marginal has depth tail `3^-(a+1)`. A cutoff
`a_m=ceil(k log_3(m+1))` therefore captures its mass up to `(m+1)^-k` with
polynomial rank. The product of the E and F cutoffs has failure probability
at most the sum of the two failures, since the projections commute. This
supplies a finite-dimensional approximation to the true purified
complement; a separately valid arbitrary-reference coding lemma still has
to be applied.

The choice of a high-probability type is load-bearing. An arbitrary type
need not obey (T2): the type consisting exclusively of a least-probable
symbol has probability `lambda_min^m`, exponentially small. Such a choice
would force a linear-depth cutoff under this transfer argument and would
destroy the subexponential-dimension conclusion. Therefore neither an
arbitrary subspace nor an arbitrary type can replace the explicit rounded
spectral type without a new input-domination bound.
