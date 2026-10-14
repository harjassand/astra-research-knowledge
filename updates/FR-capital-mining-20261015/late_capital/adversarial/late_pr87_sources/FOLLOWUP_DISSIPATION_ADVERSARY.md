# Independent adversarial audit: geometric path affinity and a hidden dissipation floor

**Disposition, 15 October 2026.** I found **no fatal flaw** in the proposed geometric-mean path certificate under the paper's exact class: a finite irreducible stationary CTMC, a deterministic even-variable observation, ordinary path reversal, and entropy production in the paper's convention. The proof below is independent algebraic verification, and an exact-rational script certifies, for the specified $q=1/20$ ring law, a floor **$V_\infty(P_{1/20})>0.1536$** in the source's time units. The sharpened numerical value is approximately $0.1536598029579099$; $0.154$ is a rounded display, **not** a certified lower threshold. This is a lower bound, not the optimum or a proof of finite-dimensional attainment. It conflicts with [Aznagulov's explicit $V_\infty(P_{1/20})=0$ conjecture](https://arxiv.org/html/2609.14623), not with a theorem. It requires independent specialist review before external theorem or novelty claims.

## The generic certificate and the attempted failure points

Let $Q$ be a finite irreducible generator, $\pi Q=0$, and $Q^*_{ij}=\pi_jQ_{ji}/\pi_i$ for $i\ne j$. The stationary flow equation gives **statewise** $Q^*_{ii}=Q_{ii}$; this is essential. Let $P$ and $P^*$ be the stationary microscopic path laws of $Q$ and $Q^*$ on $[-t,t]$. Their arithmetic and geometric path measures are
$$
\mu=(P+P^*)/2,\qquad d\nu=\sqrt{dP\,dP^*},\qquad A=\nu(\Omega)\le1.
$$
Taking a common dominating measure gives $d(\mu-\nu)=\tfrac12(\sqrt{dP}-\sqrt{dP^*})^2\ge0$, of total mass $1-A$. Thus the signed subtraction used by the certificate is actually a **positive measure**.

For a CTMC trajectory, its initial-state factor is $\pi_i$ under both laws, each holding-time factor is $e^{Q_{ii}\tau}$ under both, and a jump $i\to j$ contributes $\sqrt{Q_{ij}Q^*_{ij}}$ to $\nu$. Consequently $\nu$ is represented by the sub-Markov generator
$$
G_{ii}=Q_{ii},\qquad G_{ij}=\sqrt{Q_{ij}Q^*_{ij}}\quad(i\ne j).
$$
It is genuinely sub-Markov: $\sum_jG_{ij}\le Q_{ii}+\tfrac12\sum_{j\ne i}(Q_{ij}+Q^*_{ij})=0$. Further,
$$
\pi_iG_{ij}=\sqrt{\pi_iQ_{ij}\,\pi_jQ_{ji}}=\pi_jG_{ji},
$$
so $G$ and $e^{tG}$ are self-adjoint in $L^2(\pi)$. No normalization of $\nu$ is inserted; doing so would lose the killing mass $1-A$ and spoil the argument.

Fix a visible block $B$, any $a\in(0,1)$, $f=\mathbf1_B-a\mathbf1$, and the three-time witness
$$
W=\mathbf1_B(X_0)f(X_{-t})f(X_t).
$$
Time reflection swaps the two endpoint factors and leaves $W$ unchanged. Because $P^*$ is the reflected law of stationary $P$, $\mathbb E_\mu W=\mathbb E_PW$. The geometric measure gives a nonnegative square:
$$
\mathbb E_\nu W=\langle f,e^{tG}\operatorname{diag}(\mathbf1_B)e^{tG}f\rangle_\pi
=\sum_{i\in B}\pi_i[(e^{tG}f)_i]^2\ge0.
$$
Here the central-state factorization is legitimate for the killed semigroup; it does not assert conditional independence after normalizing $\nu$. Since $W\ge-a(1-a)$, if the observed law fixes $\mathbb E_PW=-D<0$, then
$$
-D=\mathbb E_\nu W+\mathbb E_{\mu-\nu}W
\ge-a(1-a)(1-A),\qquad D\le a(1-a)(1-A). \tag{1}
$$

For finite entropy production, $S=\log(dP/dP^*)$ has $\mathbb E_PS=2t\,\sigma(Q)$ in [Aznagulov's convention](https://arxiv.org/html/2609.14623), and $A=\mathbb E_Pe^{-S/2}$. Jensen gives $A\ge e^{-t\sigma(Q)}$. Combining with (1), provided $0<D<a(1-a)$,
$$
\boxed{\displaystyle \sigma(Q)\ge-\frac1t\log\left(1-\frac{D}{a(1-a)}\right).} \tag{2}
$$
If an allowed edge has no reverse edge, $\sigma=+\infty$ and (2) is automatic. This verification covers arbitrary *finite* hidden dimension and arbitrary finite rates; no compactness or uniform activity bound enters. The observable witness needs only three snapshots at $-t,0,t$.

## Exact target check

Use the three-state ring with clockwise rate $1$, counterclockwise rate $q=1/20$, labels $A,B,B$, uniform $\pi$, and $s=1+q$. This realizes the source's $P_q$ exactly: entry from $A$ into the two $B$ states has distribution $\alpha=(1,q)/s$, the killed block is $S=\left(\begin{smallmatrix}-s&1\\q&-s\end{smallmatrix}\right)$, and exits are $v=(q,1)^\top$, giving $\alpha(zI-S)^{-1}v=[(2q/s)z+(1+q+q^2)]/[z^2+2sz+(1+q+q^2)]$, identical to the [source transform](https://arxiv.org/html/2609.14623). Let $t=3/10$ and $\theta=\sqrt3(1-q)t/2=57\sqrt3/400$. Choose the **endpoint** mean
$$
a=\Pr(X_t\in B\mid X_0\in B)
=\frac23+\frac13e^{-3st/2}\cos\theta.
$$
This $a$ is not the probability of uninterrupted residence in $B$ through $t$. The two $B$ microstates have forward endpoint probabilities $a+\delta,a-\delta$ and backward probabilities $a-\delta,a+\delta$, where $2\delta=(2/\sqrt3)e^{-3st/2}\sin\theta$. Therefore
$$
\mathbb E_PW=-D,
\qquad D=\frac{2}{9}e^{-3st}\sin^2\theta>0.
$$
The [exact-rational verifier](geometric_affinity_certificate.py) brackets $\sqrt3$, exponential, sine, cosine, and $-\log(1-z)$ using rational alternating-series bounds. It executed successfully and yielded
$$
0.8681827585774305281153172566<a<0.8681827585774305281153172975,
$$
$$
0.0051557673801924791878773898<D<0.0051557673801924791896361765,
$$
$$
0.1536598029579099273421< -t^{-1}\log[1-D/(a(1-a))]
<0.1536598029579099273959.
$$
The loose claim $V_\infty(P_{1/20})>0.1536$ follows directly, with no floating-point premise. A separate 60-digit matrix-exponential calculation agreed with the ring values; that was a diagnostic only. The known ring itself has $\sigma=(1-q)\log(1/q)\approx2.846$, so the new lower certificate is far from identifying the optimum.

## Adversarial scope and strongest comparator

1. **Stationarity is structural.** It supplies the common initial $\pi$, equality of forward/reverse escape rates at each state, reflection of $P$ into $P^*$, and $\mathbb E_PS=2t\sigma$ without boundary correction. For nonstationary starts these identities need a new proof and likely boundary terms.
2. **Even-variable reversal is structural.** For an odd physical variable, reversal can include an involution on states; the geometric generator is then not automatically self-adjoint in the ordinary $L^2(\pi)$ inner product, and the displayed square need not follow. A parity-invariant observation alone is not a substitute for proving the appropriate twisted identity. [The source paper](https://arxiv.org/html/2609.14623) explicitly chooses ordinary reversal of even variables.
3. **Exact time scale and observation class matter.** The same $q$ at a rescaled physical clock rescales both $t$ and $\sigma$. The theorem concerns exact stationary three-time probabilities implied by the full target path law. With finite data, one must acquire stationary triplets, estimate $a,D$ with dependence-aware uncertainty, and propagate their confidence region through (2). The script is an analytic verification, not experimental inference.
4. **The competitor already proves a qualitative positive floor.** The [3 October 2026 unrefereed candidate proof](https://github.com/ipitchford/hidden-dissipation-floor/blob/main/PAPER.tex) discloses additive reversibilization and a certified $>0.017568198744$ fixed-window bound from two-sided *uninterrupted persistence*. Equation (2) raises the exhibited bound by about $8.75$ times with a different three-snapshot statistic, but it does **not** establish novelty of the general theorem, superiority over all optimized previous certificates, or the exact infimum. The simpler forward third finite difference of stationary no-exit probability also supplies a valid weaker certificate; its ingredients overlap the disclosed candidate and it is not the strongest follow-up.

For an acquisition-inclusive comparison, the strongest incumbent should be allowed the same stationary trajectory budget, timing accuracy, observation errors and choice of statistic, including optimally tuned persistence or multi-time tests. The three-snapshot witness needs resolved labels at three scheduled instants, whereas uninterrupted persistence needs reliable detection of every intervening visible exit. Yet the negative signal here is only about $0.00516$, so repeated, sufficiently separated triplets or a valid dependent-trajectory confidence method may be costly. No sample-complexity or instrumentation advantage follows from the exact-law bound alone.

**Next decisive test:** ask an independent mathematical referee to scrutinize the path-law geometric measure, the killed-semigroup factorization, and the exact ring identity, then compare optimized witnesses under the *same* observed-law and data-acquisition budget. A useful finite-data extension would report a lower confidence bound on $D/[a(1-a)]$ from dependent stationary trajectories; neither exact-law mathematics nor rational numerics supplies that statistical guarantee.
