# Independent audit of Claim B

## Verdict

**The stated inequality is correct.** The adjoint orientation, prefix index, normalized conditional expectation, and inclusion of all other task factors are consistent. A nearest-neighbor open-chain circuit of standard gate depth `h_a` satisfies the stated inclusion. Positivity is not needed for the advertised inequality.

There is a useful sharpening: the term at `i=N` is invariant under the product unitary, so the advertised additive allowance `min(h_a,N)` can always be replaced by `min(h_a,N-1)` (for `N>=1`). The original allowance is valid but must not be described as an attained or exact finite-dimensional cost.

## Proof with the orientation and tensor factors explicit

Fix task `a`; write `h=h_a`, and set

\[
\mathcal A_i
=I_{a,1\ldots i}\otimes
  \mathcal B(\mathcal H_{a,i+1\ldots N})\otimes
  \mathcal B(\mathcal H_{\ne a}),\qquad 0\le i\le N.
\]

Here `A_0` is the full global matrix algebra. In particular, `A_N` is identity on **the whole of task a**, but still the full algebra on every other task. These algebras decrease with `i`.

The map

\[
E_i(Z)=\frac{I_{a,1\ldots i}}{D^i}\otimes
          \operatorname{Tr}_{a,1\ldots i}Z
\]

is the orthogonal projection onto `A_i` in the global Hilbert-Schmidt inner product. Thus `p_i(Z)=||E_i Z||_2^2`, and `p_0(X)=||X||_2^2=1`.

Let `T=Ad(U)`, a unitary operator on this Hilbert-Schmidt space. Then

\[
 p_i(UXU^\dagger)
 =\|T^{-1}E_iT X\|_2^2
 =\|P_{T^{-1}\mathcal A_i}X\|_2^2.
\]

The hypothesis is precisely

\[
T^{-1}\mathcal A_i
=\operatorname{Ad}(U^\dagger)(\mathcal A_i)
\subseteq\mathcal A_{\max(i-h,0)}.
\]

Orthogonal projection onto a subspace cannot have larger projected norm than projection onto a containing subspace. Consequently,

\[
p_i(UXU^\dagger)\le p_{\max(i-h,0)}(X). \tag{1}
\]

For `h<N`, summing (1) gives

\[
\begin{aligned}
\sum_{i=1}^N p_i(UXU^\dagger)
&\le h+\sum_{j=1}^{N-h}p_j(X)\\
&=\sum_{j=1}^Np_j(X)
 +h-\sum_{j=N-h+1}^Np_j(X)\\
&\le\sum_{j=1}^Np_j(X)+h.
\end{aligned}
\]

For `h>=N`, every output term is at most `p_0(X)=1`, giving the claimed allowance `N`. For `h=0`, (1) gives the desired allowance zero; indeed finite-dimensional equal-dimension inclusion forces each conjugated algebra to equal `A_i`, so every `p_i` is invariant.

The other tasks may be entangled with task `a`. No factorization of `X` was used. Because `U` is a product across tasks, conjugation by all `U_b`, `b!=a`, sends the full factor `B(H_ne_a)` onto itself. Therefore the taskwise inclusion tensored with all other factors is exactly the global inclusion used above. If a proof replaced the other factors by their traces, or treated `X` as a product across tasks, that would be an unnecessary and generally unjustified change of the claim.

The `U^dagger` in the hypothesis is essential to the proof for the output `UXU^dagger`: it is the **pullback of the tested suffix algebra**. An assumption only about `Ad(U)(A_i)` does not supply this step for a general unitary. For an actual depth-`h` circuit, the inverse circuit has the same depth, so the required orientation can be established directly.

## Circuit inclusion

For a single layer of disjoint nearest-neighbor gates on the open chain, an operator initially supported on sites `i+1,...,N` can acquire support only as far left as site `i`. Gates wholly within the identity prefix commute with that operator; gates within the suffix preserve its support; the sole possible crossing edge is `(i,i+1)`.

Pull the suffix algebra backward through the circuit, starting at the final layer. Each layer enlarges its support to the left by at most one site. After `h` layers, every pullback operator is identity on sites `1,...,max(i-h,0)`. This proves the stated inclusion for every `i`, and tensoring with all other task factors preserves it.

This uses standard circuit depth: each layer contains gates on disjoint edges (and arbitrary one-site gates). The open-chain restriction matters; a wraparound gate between sites `N` and `1` need not obey the same prefix light cone. The converse is not asserted: the one-sided algebra inclusion can hold with a much smaller `h` than the unitary's nearest-neighbor circuit depth.

## Sharpening and what the allowance means

Because `U` is a product across tasks, `E_N` commutes with `Ad(U)`. Hence

\[
p_N(UXU^\dagger)=p_N(X). \tag{2}
\]

Apply (1) only to `i=1,...,N-1`, and cancel (2). With `m=min(h,N-1)`, the stronger state-dependent bound is

\[
\boxed{
\sum_{i=1}^N\bigl[p_i(UXU^\dagger)-p_i(X)\bigr]
\le m-\sum_{j=N-m}^{N-1}p_j(X)
\le m.
} \tag{3}
\]

The empty sum is zero. In particular, for `N=1` the difference is identically zero for every depth.

For nonzero positive `X`, every `p_j(X)>0`. Thus, when `m>0`, the rightmost allowance `m` in (3) is not attained in a fixed finite-dimensional instance. A simple quantitative bound is `p_j(X)>=D^(-2j)`: for any positive `Z` on `A tensor B`, spectral decomposition gives

\[
\|\operatorname{Tr}_A Z\|_2^2
\ge \frac{\|Z\|_2^2}{\dim A},
\]

since each pure eigenvector has reduced purity at least `1/dim A` and cross terms of positive reduced operators are nonnegative. Applying the normalization of `E_j` gives the claim. This supplies an additional finite-dimensional improvement in (3), though it is not asserted to be optimal.

Nevertheless, linear dependence on `h` is necessary uniformly over dimensions. For `1<=h<=N-1`, take one maximally entangled Bell pair between site `1` of task `a` and a spectator site in another task, and put normalized identities `I/sqrt(D)` on every other site of task `a`. Other spectator factors can also be normalized identities. This gives `X>=0`, `||X||_2=1`. Moving the Bell-pair half from site `1` to site `h+1` by `h` sequential adjacent SWAP gates gives

\[
p_i(X)=D^{-2}\quad(i\ge1),\qquad
p_i(UXU^\dagger)=
\begin{cases}
1,&1\le i\le h,\\
D^{-2},&h<i\le N.
\end{cases}
\]

The gain is exactly `h(1-D^(-2))`, tending to `h` as `D` grows. This example obeys the actual depth-`h` nearest-neighbor circuit restriction.

Under the algebra inclusion alone, even fixed `D>1` permits gain approaching `h` as `N` grows: set `k=N-h`, entangle the first `k` sites of task `a` with `k` spectator sites, put normalized identities on its final `h` sites, and cyclically move those final `h` sites to the front. The permutation satisfies the one-sided inclusion with parameter `h`, although generally not depth `h`. Here

\[
p_i(X)=D^{-2\min(i,k)},\quad
p_i(UXU^\dagger)=D^{-2\max(i-h,0)},
\]

and the gain is `h(1-D^(-2k))`. This also explains why the inclusion parameter must not be identified with exact circuit depth.

The additive allowance is therefore a bound on the change of the **sum of squared projected Hilbert-Schmidt norms**. It is not a gate count, entropy, physical energy cost, preparation cost, or an automatically incurred penalty. Its normalization depends on `||X||_2=1`; without that normalization it scales as `||X||_2^2`.

## Requested correction

No correction is required for the claimed inequality or the depth-implies-inclusion statement. If a sharper theorem statement is desired, replace `min(h_a,N)` by `min(h_a,N-1)` and retain the product-unitary hypothesis for that sharpening. Avoid calling either allowance an exact finite-dimensional cost, and explicitly preserve the `U^dagger` pullback orientation and all other task factors.

This audit used direct finite-dimensional algebra only; no numerical calculation or external source was used.
