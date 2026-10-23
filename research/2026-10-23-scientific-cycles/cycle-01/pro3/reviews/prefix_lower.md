# Independent lower construction: the necessary IMH correction prefix

Author: `/root/prefix_lower_challenge`, 21 October 2026. This is a new
load-bearing lower construction for the principal's prefix question, not a
re-review of the completed joint-KL theorem. No historical-priority claim.

## 1. Exact claim and changed contract

Let `K>0`, `0<alpha<1`, and `beta=1-alpha`. Begin at `q`, perform `m` ordinary
independence-MH transitions `G`, and then iterate the fixed lazy reversible
mixture `C=(I+alpha G+beta L)/2`. The full initial law is therefore
`q G^m`, with `m+1` independent proposal candidates already acquired. Here we
impose the **forward** population bound `D(pi||q)<=K`, equivalence of the two
measures, and no reverse-KL bound. The original joint-KL theorem is unchanged.

Define

\[
b_*=1-e^{-K},\qquad \lambda_K=-\log b_*,\qquad
\theta_*={\beta\over1-\alpha b_*}
           ={\beta\over\beta+\alpha e^{-K}}.
\]

For every fixed finite integer `m>=0`, the supremum of the subsequent
`C`-mixing time is infinite whenever

\[
\boxed{\epsilon\le\theta_* b_*^{m+1}.}                \tag{1}
\]

This is a sufficient condition for nonuniformity, including equality. A
matching sufficiency theorem above the threshold belongs to the principal's
separate upper argument and is not presumed here.
In particular, if an integer-valued prefix length satisfies

\[
\limsup_{\epsilon\downarrow0}
 {m(\epsilon)\over\log(1/\epsilon)}
 < {1\over-\log(1-e^{-K})},                         \tag{2}
\]

then that supremum is infinite for every sufficiently small `epsilon`.
The same conclusion holds for a bound
`m(epsilon)<= (1-delta) log(1/epsilon)/lambda_K`, for any fixed `delta>0`.

The factor `theta_*` sharpens the first-local-update lower estimate `beta`.
Repeated proposals that redraw the low-weight entrance provide additional
opportunities for local capture. This constant does not change (2).

## 2. An admitted three-state family with all finite conditions explicit

Fix any

\[
0<b<b_*,\quad 0<\rho<1,\quad
0<\kappa<K+\log(1-b).
\]

Such a positive `kappa` exists because `b<b_*`. Put

\[
d_0=1-b-e^{-(K-\kappa)}>0.
\]

Let `p` tend down to zero subject to

\[
0<p\le\min\{1/4,b/2,d_0,\kappa/(K-\kappa)\}.
\tag{3}
\]

Set

\[
r=p e^{-\kappa/p},\quad s=p e^{-2\kappa/p},\quad
\pi_p=(p,s,1-p-s),\quad q_p=(r,b,1-b-r).
\tag{4}
\]

Every mass is strictly positive. The bounds in (3) imply `s<=p`,
`pi_C>=1/2`, `q_C>=exp(-(K-kappa))`, and `q_C<=pi_C`.
The forward divergence has the finite bound

\[
\begin{aligned}
D(\pi_p\Vert q_p)
 &=\kappa+s\log(s/b)+\pi_C\log(\pi_C/q_C)\\
 &\le\kappa-\log q_C\le K.                         \tag{5}
\end{aligned}
\]

Here `s<=b`, `pi_C log pi_C<=0`, and
`-pi_C log q_C<=-log q_C`. As an additional check, the actual divergence
converges to `kappa-log(1-b)<K`.

Use the symmetric proposal

\[
Q=\begin{pmatrix}
1-\rho&\rho&0\\
\rho&0&1-\rho\\
0&1-\rho&\rho
\end{pmatrix}
\]

and ordinary MH with target `pi_p`. Since `s<=p` and `s<=pi_C`, this gives

\[
L_p=\begin{pmatrix}
1-\rho s/p&\rho s/p&0\\
\rho&0&1-\rho\\
0&(1-\rho)s/\pi_C&1-(1-\rho)s/\pi_C
\end{pmatrix}.                                      \tag{6}
\]

Detailed balance holds on both edges. `Q` and `rho` are fixed across the
whole `p`-family; `L_p` is fixed in time for each admitted instance. The
chain is irreducible and the lazy mixture is aperiodic. This is not an
adaptive or nonreversible construction.

The importance ratios satisfy `W_B<1<W_C<=W_A` under (3). Thus the exact
independence-MH matrix is

\[
G_p=\begin{pmatrix}
1-(1-p)r/p&sr/p&\pi_Cr/p\\
r&b&q_C\\
r&sq_C/\pi_C&1-r-sq_C/\pi_C
\end{pmatrix}.                                      \tag{7}
\]

In particular, proposing `B` from `B` keeps the chain there, while a
proposal of `C` from `B` is always accepted.

## 3. The prefix law and the limiting post-prefix chain

As `p` decreases to zero, the finite matrices and laws converge entrywise:

\[
q_p\to(0,b,1-b),\qquad
G_p\to G_0=\begin{pmatrix}1&0&0\\0&b&1-b\\0&0&1\end{pmatrix},
\]

\[
L_p\to L_0=\begin{pmatrix}1&0&0\\\rho&0&1-\rho\\0&0&1\end{pmatrix}.
\]

For each fixed finite `m`, continuity of matrix multiplication gives

\[
q_pG_p^m\longrightarrow(0,b^{m+1},1-b^{m+1}).        \tag{8}
\]

The extra power is essential: `m` transitions use `m+1` proposals including
initialization. In the limiting chain, the entrance remains occupied only
when all of those draws are at `B`. For the actual finite chain, the same
all-`B` event directly proves `q_pG_p^m(B)>=b^{m+1}`; the limit in (8)
also accounts for the vanishing additional paths and mass at `A`.

Let

\[
z={1+\alpha b\over2},\qquad
\theta_\rho={\beta\rho\over1-\alpha b}.
\]

The limiting mixture has `A` and `C` absorbing, while from `B` it moves to
`A` with probability `beta rho/2`, stays at `B` with probability `z`, and
otherwise moves to `C`. Notice `0<theta_rho<1` and `0<z<1`.
After `n>=0` post-prefix lazy steps, its masses at `A` and `B` are exactly

\[
\mu_{m,n,0}(A)=b^{m+1}\theta_\rho(1-z^n),\qquad
\mu_{m,n,0}(B)=b^{m+1}z^n.                         \tag{9}
\]

Since `pi_p` converges to the point mass at `C`, continuity of finite-state
total variation gives, for each fixed finite `m,n`,

\[
\lim_{p\downarrow0}
 \|q_pG_p^m C_p^n-\pi_p\|_{\rm TV}
 = b^{m+1}\big[\theta_\rho+(1-\theta_\rho)z^n\big]
 \ge b^{m+1}\theta_\rho.                            \tag{10}
\]

This retains the low-weight mass still at `B`, so it does not require a
large-`n` limit to establish the lower bound at a finite target time.

## 4. Nonuniformity and the logarithmic necessary prefix

First suppose the inequality in (1) is strict. By continuity, choose `b<b_*` and `rho<1` sufficiently
close to their endpoints that

\[
\epsilon < {\beta\rho b^{m+1}\over1-\alpha b}.
\]

Then fix any positive `kappa` in the admissible interval above. For every
integer `N`, (10) supplies a sufficiently small positive `p` satisfying
(3) with

\[
\|q_pG_p^m C_p^N-\pi_p\|_{\rm TV}>\epsilon.
\]

Because `C_p` is `pi_p`-invariant, total variation along the subsequent
`C_p` evolution is nonincreasing. Thus the first sufficient time exceeds
`N`. Since `N` was arbitrary, its supremum over the admitted class is
infinite. Each individual finite chain still converges; the assertion is
failure of a uniform finite bound, not nonconvergence of one chain.

Equality in (1) also gives nonuniformity. For each fixed finite integer
`N`, the right side of (10), as `b` increases to `b_*` and `rho` increases
to one, converges to

\[
F_{m+1}+b_*^{m+1}(1-\theta_*)z_*^N>F_{m+1},\quad
F_{m+1}=\theta_*b_*^{m+1},\quad z_*=(1+\alpha b_*)/2.
\tag{10a}
\]

The inequality is strict because `alpha>0`, `b_*<1`, and consequently
`theta_*<1`. Choose `b<b_*` and `rho<1` close enough that the finite-`N`
formula still exceeds `F_{m+1}`. Then choose a positive `kappa` within the
remaining entropy slack, and only then let `p` become sufficiently small.
This yields an admitted instance whose TV at time `N` exceeds the threshold
itself. No reducible `rho=1` instance or zero-`kappa` instance is admitted;
these endpoints serve only to choose nearby strict parameters. The choices
of `b`, `rho`, and `p` may depend on `N`, as permitted in a supremum of
mixing times. Therefore the uniform time is infinite also at equality.

There is no exchange of a growing-`m` limit with `p` here. At each fixed
target `epsilon`, `m(epsilon)` is a finite integer; the construction and
arbitrarily large `N` argument apply at that fixed value.

For (2), choose `delta>0` so that eventually
`m(epsilon)+1 <= (1-delta) log(1/epsilon)/lambda_K`. Then

\[
{\theta_* b_*^{m(\epsilon)+1}\over\epsilon}
 \ge\theta_*\epsilon^{-\delta}\longrightarrow\infty.
\]

This establishes the asserted coefficient. More precisely, finite uniform
mixing requires the necessary strict inequality

\[
m+1> {\log(\theta_*/\epsilon)\over\lambda_K};          \tag{11}
\]

the construction alone does not make (11) sufficient.

## 5. The separate sharp `K` lower bound survives a short prefix

The strongest ordinary comparator must be retained. Let `ell>1`,
`p=ell epsilon`, `a=exp(-K/p)`, and

\[
\pi=(p,1-p),\qquad q=(pa,1-pa),\qquad L=I.
\]

The forward divergence is strictly below `K`; the reverse divergence is
at most `-log(1-p)` and therefore eventually below every fixed `J>0`.
The two-state exact error after the prefix and mixture is

\[
\|qG^m C^n-\pi\|_{\rm TV}
 =p(1-a)(1-a)^m(1-\alpha a/2)^n.                    \tag{12}
\]

Assume `epsilon log(m(epsilon)+1)->0`, which includes every logarithmic
prefix. Then `m(epsilon)a->0`. For any fixed `0<c<log ell`, choose
`n=floor(2c/(alpha a))`. The right side of (12), divided by `epsilon`,
tends to `ell exp(-c)>1`. Meanwhile `epsilon log n -> K/ell`.
Taking `ell` down to one proves

\[
\liminf_{\epsilon\downarrow0}\epsilon\log T^{\rm prefix}(\epsilon)
 \ge K,                                                \tag{13}
\]

whenever a finite uniform time exists. The lower construction is also
admitted under any fixed positive reverse-KL budget, so it applies to the
principal's one-update joint-KL result. It is a sampler-class lower bound;
the explicitly given two-state target can of course be sampled directly.

## 6. What this does and does not establish

* The necessary logarithmic prefix coefficient is proved under forward KL
  alone. Sufficiency and its sharp subsequent `K` exponent belong to the
  principal's separate upper argument and have not been presumed here.
* Repeated entrance redraws improve the finite-prefix obstruction from
  `beta b_*^(m+1)` to `theta_* b_*^(m+1)`. Claiming the weaker bound is valid
  but would omit a mechanism relevant to the exact constant window.
* No reverse-KL constraint is hidden: in this obstruction the reverse
  divergence diverges as `p` decreases. It does not contradict the accepted
  joint-KL theorem or a one-update joint-KL correction result.
* The operation uses ordinary IMH and ordinary local MH. It yields no
  application speedup, no empirical-KL certificate, no finite-precision
  exactness claim, and no theorem about adaptive or deterministic schedules.
* The new finite-m endpoint `theta_* b_*^(m+1)` is a lower floor only;
  proving a matching universal floor would be a distinct next obligation.

## 7. Sources, diagnostic and observed resources

The construction reuses the owned three-state path and two-state lower
family in `restore_pro3/delivery/Astra_Restore_PRO3_20261021/PROOF.md`
Sections 3--4 and `JOINT_KL_FUNNEL_NOTE.md` Section 1, with the new exact
prefix and repeated-competition calculation in (8)--(10). Those sources
remain unchanged. No primary literature was consulted for this independent
lemma; the parent assigned the novelty boundary to a separate contributor.

`prefix_lower_checks.py` verifies (8)--(10) on exact rational instances by
independently multiplying the limiting matrices. It checks the extra
initialization power and the denominator `1-alpha b`, rather than replotting
the old funnel. The finite matrix-limit argument and KL proof above carry
the universal quantifiers. The diagnostic alone does not prove them.

This contributor's first recorded clock was 2026-10-21 13:45:28 UTC. The
diagnostic receipt records its own wall/CPU/RSS costs. Total research/model
cost and monetary cost were not observable and are not inferred from file
size or elapsed time. No network computation, package installation, new
hardware, external contact, or public delivery was used by this contributor.

The completed diagnostic passed 75 cases / 240 exact comparisons in
0.016807656 seconds wall time and 0.016806285 seconds CPU, with reported
peak RSS 8,960 KiB. The next recorded clock was 13:49:31 UTC, 243 seconds
after the first clock. One attempted documentation patch failed atomically
because its context used a lowercase initial word; the corrected patch
succeeded. No scientific diagnostic failed and no result was suppressed.
