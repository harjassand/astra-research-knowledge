# Quartic upper order for independent charge-preserving temporal blocks

Author: Cycle5 fixed-block obstruction contribution. Date: 22 October 2026,
Australia/Brisbane. This is an owner-internal proof contribution, not external
certification or a historical-priority claim. The unchanged Cycle4 strict-gain
theorem is the comparator and is not re-audited here.

## Result and scope

Fix a positive integer `k` before taking beta to zero. Let each `rho_j` be an
arbitrary density on k successive qutrit inputs satisfying
`[rho_j,Q_k]=0`, where `Q_k` counts nonzero port colors. The states can differ
between blocks and can depend on the final horizon. The full input is the tensor
product of these blocks; there is no independence assumption on the physical
channel or its evolving bath. The theorem applies to the same actual `tau_pi`;
more strongly, its upper bound is uniform over every normal initializer.

Put, with logarithms in bits except `ln`,

\[
 \gamma_k=(3/8)^k,\quad D_{0,k}=\frac{\gamma_k^2}{8k^2\ln2},
 \quad B_k=4k^2,\quad C_k=4k^3,
 \quad \beta_k=\min\{1/2,D_{0,k}/(2B_k)\}.
\]

For every `0 <= beta <= beta_k`, every number `n` of blocks, and every such
sequence of input densities,

\[
 \frac1{nk}I_c(\rho_1\otimes\cdots\otimes\rho_n,
                  \mathcal N_{nk}^{\tau})
 \le \frac32+8k^5\ln2\,\beta^4. \tag{T}
\]

This is uniform in the horizon, the block densities, and the normal initializer
tau (which is independent of the external input). In particular it
allows horizon-dependent optimization. It is an upper bound on the coherent
information of the stated independent-block input class, not an upper bound
on general reliable capacity or on arbitrarily correlated inputs. It uses the
actual same-bath process and retains the root. For identical blocks the constant
can be halved and the allowed beta threshold doubled; those constants are not
the scientific point.

The Cycle4 pair construction gives an attainable quartic lower increment. For
any fixed k>=2, putting at least one correlated pair into a k-site independent
block and padding with critical diagonal sites preserves a negative bulk drift
away from the finite boundary. Its exact bounded-jump depth chain admits the
same exponential-moment, type-domination and compression proof. Thus the
optimized asymptotic coherent information in the present fixed-k class has
quartic order for k>=2. The all-single-site iid optimum at k=1 remains exactly
3/2 by the stronger inherited theorem. A detailed padded-block lower proof is
an owner integration obligation if this corollary is stated in the main result.

## 1. Bounded drift operator and charge covariance

Let `Q=Q_k` on the k external ports, with spectrum `{0,...,k}`, and let L be
bath depth. Every physical interaction commutes with `L+Q`: an ordinary U move
trades one unit of bath depth for one port color, and the vacuum seed exchange
preserves both. Identity histories also preserve it. Therefore

\[
 [W_s,L+Q]=0,\qquad W_s=V_s^{(k)}\cdots V_s^{(1)},
 \qquad V_s=\cos s\,U+i\sin s\,I.
\]

Define the bounded self-adjoint operator

\[
 G_s=Q-W_s^*QW_s,\qquad \|G_s\|\le k.
\]

On the finite-depth core it equals `W_s^* L W_s-L`; hence it represents the
exact bounded depth displacement without differentiating an unbounded operator.
For an input density rho let

\[
 D_s(\rho)=\operatorname{Tr}_A[(\rho\otimes I)G_s]
           =\Phi_\rho^*L-L.
\]

The partial trace notation defines a bounded operator even on the infinite
bath, and `||D_s(X)|| <= k ||X||_1` for every Hermitian input matrix X.
Since G_s commutes with L+Q, charge preservation `[rho,Q]=0` gives

\[
 [D_s(\rho),L]=0. \tag{1}
\]

This is an exact operator identity, including every seed and color coordinate.
It does not say that the entire depth algebra is scalar or that the block map
is radial. Its crucial use is that no matrix element crosses from depths `<k`
to depths `>=k` in the drift observable.

At s=0 the full W is a computational-basis permutation. Each non-vacuum U call
flips its port between zero and colored; a zero input at the vacuum remains
zero and exchanges the seeds. On each joint basis vector,

\[
 L_{\rm final}-L_{\rm initial}=2Q_{\rm input}-k+N_0,
 \qquad 0\le N_0\le k,
\]

where N_0 is the number of these vacuum-zero events. Consequently

\[
 G_0\ge 2Q-kI. \tag{2}
\]

If the initial bath depth is at least k, no active call encounters the vacuum,
and (2) is equality on that initial subspace.

## 2. Exact bulk parity and derivative estimates

Let `P_hi=1_{[k,infinity)}(L)`. Expand W_s into move/stay histories. For a
history with r stays, every one of its k-r moves flips a port color indicator
when starting in P_hi. Thus input and output charges q,q' satisfy

\[
 q'-q\equiv k-r\pmod2.
\]

In a matrix element of `W_s^* Q W_s` with the same input charge on both sides,
the two contributing histories have the same stay-count parity. The coefficient
is therefore even in s: `cos(s)` is even, and their total sine power is even.
This includes arbitrary complex coherence inside a charge sector. If
`mathcal P_Q` pinches an input operator into total-charge blocks, then

\[
 (I\otimes P_{\rm hi})\mathcal P_Q(G_s)(I\otimes P_{\rm hi})
 \quad\text{is even in }s. \tag{3}
\]

The root is not discarded: (3) is only a high-initial-depth identity. The
low-depth part is controlled separately below.

All V_s, V_s', and V_s'' have operator norm one. Product differentiation yields

\[
 \|W_s'\|\le k,\quad \|W_s''\|\le k^2,
 \quad\|G_s'\|\le2k^2,\quad\|G_s''\|\le4k^3. \tag{4}
\]

Let beta=sin(s) with `0<=beta<=1/2`. Then
`s<=2 beta/sqrt(3)`. Equations (2)--(4) imply the coarse global bound

\[
 D_s(\rho)\ge 2mI-B_k\beta I,
 \qquad m=\operatorname{Tr}(Q\rho)-k/2,\quad B_k=4k^2. \tag{5}
\]

Taylor's theorem applied to the even compression (3), followed by partial
trace against any charge-preserving X, gives

\[
 \left\|P_{\rm hi}[D_s(X)-D_0(X)]P_{\rm hi}\right\|
 \le C_k\beta^2\|X\|_1,\qquad C_k=4k^3. \tag{6}
\]

The constants follow from `2k^3 s^2 <= (8/3)k^3 beta^2 <= C_k beta^2`.
No Kraus-rank surrogate or finite reflecting truncation is used.

## 3. A positive boundary margin absorbs root coherences

Let `rho_c=diag(1/2,1/4,1/4)` and `sigma=rho_c^tensor k`. Its physical bath
map is the k-fold composition of the critical one-site map T_s, because this
particular averaging input is a product; the bath still evolves between calls.
On depth functions T_s is the true lazy symmetric birth/death chain. Exactly,

\[
 T_s^*L-L=(a/2)P_0,\qquad a=1-\beta^2,
\]

and therefore

\[
 B_s:=D_s(\sigma)=(a/2)\sum_{j=0}^{k-1}(T_s^*)^j(P_0). \tag{7}
\]

This is scalar on every depth and seed space. It vanishes on P_hi. From depth
ell<k the path of ell consecutive down steps reaches the vacuum with
probability `(a/2)^ell`; the j=ell term of (7) is present. For beta<=1/2,

\[
 B_s\ge(a/2)^kP_{\rm lo}\ge\gamma_k P_{\rm lo},
 \quad P_{\rm lo}=I-P_{\rm hi},\quad\gamma_k=(3/8)^k. \tag{8}
\]

This lower bound is an operator bound on ALL low-depth vectors, including
seed and color coherences. It is not merely an expectation for radial states.

Write X=rho-sigma and x=||X||_1. Since Tr X=0,
`|2m|=|Tr((2Q-k)X)|<=kx`. Equations (7)--(8) and the linear norm estimate give

\[
 P_{\rm lo}[D_s(\rho)-2mI]P_{\rm lo}
 \ge(\gamma_k-2kx)P_{\rm lo}. \tag{9}
\]

Thus if `x<=x0=gamma_k/(2k)` the low-depth part is nonnegative. On P_hi,
`D_0(rho)=2mI` and `D_s(sigma)=0`, so (6) gives

\[
 D_s(\rho)\ge[2m-C_k\beta^2x]I\qquad(x\le x_0). \tag{10}
\]

Combining the low and high restrictions is legitimate by the exact covariance
(1). Without (1), separately proving two diagonal compressions would not bound
the full operator; no such step is silently assumed.

## 4. Entropy forces the relevant input close enough to the reference

Define the finite-dimensional relative entropy in bits

\[
 D=D_2(\rho\Vert\sigma),\qquad
 \varepsilon=S(\rho)-3k/2.
\]

Since `-log_2 sigma=kI+Q`, the exact entropy identity is

\[
 \varepsilon=m-D. \tag{11}
\]

Quantum Pinsker gives
`x<=sqrt(2 ln(2) D)`. Hence (10) holds whenever

\[
 D\le D_{0,k}:=x_0^2/(2\ln2)=\gamma_k^2/(8k^2\ln2). \tag{12}
\]

For arbitrary D, combine the near bound (10) with the coarse bound (5):

\[
 D_s(\rho)\ge
 \left[2m-C_k\beta^2\sqrt{2\ln2\,D}
             -\frac{B_k\beta}{D_{0,k}}D\right]I. \tag{13}
\]

For D<=D0 the last term is unnecessary but harmless. For D>D0 its magnitude
is at least B_k beta, so the right side is below the valid coarse bound.
Equation (13) is valid for every charge-preserving density, including states
far from sigma. It is the reusable operator interface for nonidentical blocks.

### Exact entropy Hessian in the prescribed four-call tangent space

For a charge-preserving Hermitian perturbation X with Tr X=0, sigma and X
commute because `sigma=2^{-(k+Q)}` is scalar on each charge sector. Therefore

\[
 S(\sigma+zX)=\frac{3k}{2}+z\operatorname{Tr}(QX)
 -\frac{z^2}{2\ln2}\operatorname{Tr}(\sigma^{-1}X^2)+R_X(z).
\]

For `|z| ||sigma^{-1}X||<=1/2`, scalar third derivatives in the common
eigenbasis give the explicit remainder bound

\[
 |R_X(z)|\le\frac{2|z|^3}{3\ln2}
                 \operatorname{Tr}(\sigma^{-2}|X|^3).
\]

At k=4 the critical entropy is six bits and the quadratic form is

\[
 \operatorname{Tr}(\sigma^{-1}X^2)
 =\sum_{q=0}^4 2^{4+q}\operatorname{Tr}(X_q^2),
 \qquad X_q=1_{\{q\}}(Q)X1_{\{q\}}(Q).
\]

Thus the exact charge-sector weights are 16,32,64,128,256. Any nonzero
charge-preserving correlation direction costs entropy quadratically. Bulk
interference starts only at beta squared by (3). The nonlinear proof above
extends this local entropy/drift balance to arbitrary densities and horizons;
the Hessian alone would not establish an information upper bound.

## 5. Actual same-bath information upper bound

Let the n block densities be rho_j, with parameters m_j,D_j. They are
independent as input blocks, so before block j its ports are in rho_j and
independent of the bath marginal. The bath may be correlated with every past
external output; tracing those outputs leaves the exact bath evolution
`tau_j=Phi_{rho_j}(tau_{j-1})`. No bath is replaced or reset. Iterating (13)
therefore bounds the accumulated charge transfer Delta by

\[
 \Delta\ge
 2M-C_k\beta^2\sqrt{2\ln2}\sum_j\sqrt{D_j}-uD_\Sigma,
 \quad M=\sum_jm_j,\ D_\Sigma=\sum_jD_j,
 \quad u=B_k\beta/D_{0,k}. \tag{14}
\]

Here `Delta=sum_j Tr[tau_{j-1} D_s(rho_j)]` is always defined because every
summand is the expectation of a bounded operator. In particular no difference
of two infinite depth means is taken. If Q_j is the charge on input block j,
it commutes with the interaction on every other block. Hence the bounded
identity

\[
 Q_{\rm total}-W_{\rm total}^*Q_{\rm total}W_{\rm total}
 =\sum_j W_{<j}^*\bigl(Q_j-W_j^*Q_jW_j\bigr)W_{<j}
\]

telescopes exactly. Taking expectations in the product input and the normal
bath gives `<Q_out>=nk/2+M-Delta`. For the actual finite-mean tau_pi, Delta is
also the mean depth increase; that interpretation is not needed for the proof.

For any qutrit marginal omega, pinching and entropy maximization in its colored
two-dimensional subspace give `S(omega)<=1+Tr(Q_1 omega)`; this is equivalently
nonnegativity of `D_2(omega||rho_c)`. Subadditivity retains every output
correlation while yielding

\[
 S(B^{nk})\le 3nk/2+M-\Delta. \tag{15}
\]

The input entropy is exactly
`H_in=3nk/2+M-D_Sigma`. Purify the finite-dimensional input on a finite
reference R, so that S(R)=H_in. All of R and B are finite dimensional and
`Ic=S(B)-S(RB)` is well-defined for any normal bath initializer. The two
directions of Araki--Lieb imply

\[
 I_c\le H_{\rm in},\qquad I_c\le2S(B^{nk})-H_{\rm in}. \tag{16}
\]

Indeed `S(RB)>=S(B)-S(R)` gives the first inequality, and
`S(RB)>=S(R)-S(B)` gives the second. No bath entropy or depth-moment assumption
is needed. The reference is analytic; its preservation is not an extra channel
resource. No independent-channel coding theorem enters (14)--(16).

Writing `E=I_c-3nk/2`, equations (14)--(16) give

\[
 E\le\min\{M-D_\Sigma,
 -3M+(1+2u)D_\Sigma+
       2C_k\beta^2\sqrt{2\ln2}\sum_j\sqrt{D_j}\}.
\]

Use a three-quarter/one-quarter convex combination of these two upper bounds
and Cauchy--Schwarz, `sum sqrt(D_j)<=sqrt(nD_Sigma)`:

\[
 \frac En\le -\frac{1-u}{2}\overline D
        +\frac{C_k\beta^2\sqrt{2\ln2}}2\sqrt{\overline D},
 \qquad \overline D=D_\Sigma/n. \tag{17}
\]

For beta<=beta_k, u<=1/2. Maximizing the resulting quadratic in
`sqrt(overline D)` gives

\[
 \frac En\le\frac{C_k^2\ln2}{2}\beta^4.
\]

Divide by k and insert C_k=4k^3 to obtain (T). Every estimate is uniform in
n and the choices of rho_j, so a density sequence optimized separately at each
horizon is included.

For identical blocks one can instead split into `D>D0` (coarse (5) plus
epsilon>0 gives a nonpositive excess if beta<=D0/B_k) and `D<=D0` (use (10)
without uD). Optimizing (17) with u=0 gives
`Ic/(nk)<=3/2+4k^5 ln2 beta^4`. The stronger nonidentical statement is the
recommended main scope because the coefficient is not the target.

## 6. An omitted-premise counterexample

Charge preservation is load-bearing. For k=1 take

\[
 \rho=\rho_c+ig|0\rangle\langle1|-ig|1\rangle\langle0|,
 \qquad0<g<1/(2\sqrt2).
\]

This is a positive density but does not commute with port charge. Its exact
one-call drift is

\[
 D_s(\rho)=\frac a2P_0-\alpha\beta g(S_1+S_1^*).
\]

Choose any word w with length at least one and the normalized bath vector
`psi=(|seed,w>+|seed,1w>)/sqrt2`. It is supported above the vacuum, and
`<psi,(S1+S1*)psi>=1`. Its expected drift is `-alpha beta g`, which is
linear in beta. Thus the bulk evenness and O(beta^2) correction fail if
charge coherence is admitted. This counterexample does not prove a capacity
gain: its input entropy is below the critical entropy, and the stronger
inherited single-site iid theorem still applies. It identifies precisely the
premise needed by the new block obstruction.

Nor is the boundary disposable. At beta=0 the critical single-site input has
root drift 1/2, and its k-block drift is the strictly positive B_0 in (7).
The proof uses that margin to absorb the full root contribution, rather than
pretending that bulk parity holds on the vacuum.

## 7. What this closes and what it leaves live

The attempt to obtain a better small-beta exponent by any fixed block length
for independent, charge-preserving temporal input blocks is obstructed at the
coherent-information level. Four-call, six-call and every other fixed k have
the same quartic order as the pair baseline. The explicit constants and beta
threshold depend strongly on k; no bound uniform in k is claimed. Therefore
blocks whose length grows as beta tends to zero are an actual remaining
operation, not a notational rewriting of the theorem.

The result does not cover arbitrary inter-block correlations, feedback,
non-charge-preserving block coherences, a general quantum code ensemble, or a
general capacity converse. It does not prove efficient encoders or useful
finite blocklength. The derivative and entropy tools are standard; the new
model-specific work is the exact bulk parity, the full-root boundary margin,
their operator combination, and the all-horizon independent-block consequence.

## 8. A controlled logarithmically growing block-length corollary

The explicit constants support a limited, genuinely uniform growing-block
statement. Let

\[
 0<c<\frac{1}{2\ln(8/3)},\qquad
 1\le k(\beta)\le c\ln(1/\beta)
\]

for all sufficiently small beta. Write `L_beta=ln(1/beta)` and
`nu=2 ln(8/3)`. The threshold in (T) is

\[
 \beta_k=\frac{e^{-\nu k}}{64k^4\ln2}
\]

for these positive k (the competing 1/2 is larger). Thus

\[
 \frac{\beta}{\beta_{k(\beta)}}
 \le64c^4\ln2\,L_\beta^4\,
      \beta^{1-\nu c}\longrightarrow0.
\]

Theorem (T) consequently applies for sufficiently small beta, uniformly in
the number of blocks, every charge-preserving block density (allowed to vary
between blocks and with the horizon), and every normal initializer. It gives

\[
 \frac{I_c}{n k(\beta)}-\frac32
 \le 8c^5\ln2\,\beta^4[\ln(1/\beta)]^5.
\]

In particular the positive excess is `o(beta^p)` for every fixed `p<4` in this
restricted independent-block coherent-information class. This does not exclude
a logarithmic enhancement of the quartic scale, blocks growing faster than this
proved range, non-charge-preserving inputs, or global inter-block correlations.
It remains an input-class information upper bound, not a general capacity
upper bound. The growing-block statement follows from quantitative constants;
one must not infer a uniform-k limit merely from an unspecified `O_k` theorem.
For each beta the device and block length are fixed throughout its communication
sequence; beta tends to zero only across this family of fixed-device problems.
There is no horizon-dependent device or initializer in the lower construction.

No simulation or finite cutoff establishes any statement above. Resource cost
of this contribution is analytic derivation; total model inference/discovery
cost is not measured.
