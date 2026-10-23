# Finite-dimensional quantum upper bound for the random BG graph game

This checks the stated operator/net argument for the game with questions \(x,y\in[k]\), answers \((s,\ell),(t,\ell')\) where \(s,t\in[k]^r\), and win condition
\[
\ell=\ell',\qquad s_\ell=x,\qquad t_\ell=y,\qquad \xi_{st}=1.
\]
Here \(N=k^r\), the graph bits \(\xi_{st}\) are independent Bernoulli(\(q\)) variables, and the proposed regime is \(q=k^{-1/5}\), \(r=k^{1/3}\). The conclusion is a finite-local-dimension bound only.

## Fixed-strategy edge weights

Fix any finite-dimensional tensor-product strategy, independent of the random edge bits. Let \(p(s,\ell;t,\ell'\mid x,y)\) be its joint outcome law and define
\[
w_{st}=\frac1{k^2}\sum_{\ell=1}^r
p(s,\ell;t,\ell\mid s_\ell,t_\ell).
\]
Then its payoff is exactly
\[
Z_\Gamma=\sum_{s,t}w_{st}\xi_{st}.
\]
The weights are nonnegative. For each \(s,t,\ell\), the corresponding summand is at most \(1/k^2\), so
\[
w_{st}\leq \frac r{k^2}.
\]
Also
\[
\sum_{s,t}w_{st}
=\frac1{k^2}\sum_{x,y}\sum_{\ell}
\sum_{\substack{s:s_\ell=x\\t:t_\ell=y}}
p(s,\ell;t,\ell\mid x,y)
\leq1.
\]
For each fixed \(x,y\), the sum is over a subset of the disjoint joint outcomes of the two complete measurements. Importantly, although a string pair \((s,t)\) can use several \(\ell\)'s in the definition of \(w_{st}\), the total over all labels and strings at a fixed input pair is still at most one.

For \(b=r/k^2\), convexity gives, for \(\lambda\geq0\) and \(0\leq w\leq b\),
\[
e^{\lambda w}-1\leq \frac{w}{b}(e^{\lambda b}-1).
\]
Independence and \(\sum w_{st}\leq1\) therefore imply
\[
\mathbb E e^{\lambda Z_\Gamma}
\leq \exp\!\left(\frac q b(e^{\lambda b}-1)\right).
\]
For \(a>q\), optimizing Chernoff at \(e^{\lambda b}=a/q\) yields
\[
\Pr[Z_\Gamma\geq a]
\leq
\exp\!\left[-\frac1b\left(a\log\frac aq-a+q\right)\right].
\]
The condition \(a>q\) matters; it holds for every fixed \(a>0\) once \(k\) is sufficiently large. With \(q=k^{-1/5}\), \(r=k^{1/3}\), and fixed \(a\),
\[
\frac1b\left(a\log\frac aq-a+q\right)
=\frac{a}{5}k^{5/3}\log k+O_a(k^{5/3}).
\]

## Finite nets without an answer-alphabet penalty

Fix a local dimension \(d\). A maximum of the payoff over states and POVMs exists in finite dimensions. A mixed shared state can be replaced by a pure state without decreasing the maximum, because the payoff is linear in the state for fixed measurements. For each input and each party, the payoff is linear in that input's POVM while the other choices are fixed. Replacing the POVMs one at a time by maximizing extreme POVMs thus gives a maximizer with every POVM extreme. The nonzero effects of an extreme POVM are linearly independent in the real vector space of Hermitian \(d\times d\) matrices, so there are at most \(L=d^2\) nonzero effects per input. Pad with zero effects and record the output labels of the at most \(L\) slots. Across both parties and all \(k\) inputs, the number of ordered label patterns is at most
\[
(rN)^{2kL}.
\]

For each fixed label pattern, pad each POVM to \(L\) outcomes. Its effect tuple lies in a bounded subset of the real vector space \(\mathrm{Herm}(d)^L\), of dimension \(Ld^2=d^4\). A volumetric net with centers inside the complete \(L\)-outcome POVM set, in the maximum operator norm on the effects, has size at most
\[
(C/\delta)^{O(d^4)}
\]
for radius \(\delta\). Across \(2k\) input POVMs, this contributes \((C/\delta)^{O(kd^4)}\). This is a net of valid POVMs: the centers remain positive and sum to identity.

A unit-vector net for pure states in \(\mathbb C^{d_A}\otimes\mathbb C^{d_B}\), with \(d_A,d_B\leq d\), has size \((C/\delta_\psi)^{O(d^2)}\). Thus, with fixed target payoff accuracy \(\epsilon>0\), take \(\delta=\epsilon/(8L)\) for every effect and \(\delta_\psi=\epsilon/8\). The complete net cardinality is bounded by
\[
(rN)^{2kd^2}
(Cd^2/\epsilon)^{O(kd^4)}
(C/\epsilon)^{O(d^2)}.
\]

Here is the payoff continuity check, including its dependence on the outcome count. For fixed \(x,y\), the success event is a coarse-graining of the product of the two complete POVMs, hence is an effect \(0\leq E_{xy}\leq I\). Changing the state vector by \(\delta_\psi\) changes this event probability by at most \(2\delta_\psi\). To change Alice's POVM, condition on each Bob outcome \(b\); the accepted Alice outcomes form a subset of at most \(L\) retained labels. The corresponding difference of Alice effects has operator norm at most \(L\delta\). Summing against Bob's positive POVM effects preserves this bound, since they sum to identity. The Bob replacement contributes another \(L\delta\). These bounds are uniform in \(x,y\), the graph, and the original alphabet size \(rN\), so the net changes total payoff by at most
\[
2\delta_\psi+2L\delta\leq \epsilon/2<\epsilon.
\]
Using a slightly finer net if desired gives any stated \(\epsilon\).

## Union bound and scope

Choose, for example, \(\epsilon=1/8\). If some dimension-\(d\) strategy wins with probability \(>1/2\), a net strategy with the same \(d\) and recorded labels wins \(>3/8\). Apply the fixed-strategy tail with \(a=3/8\), then union-bound over the net and over integer \(d\leq k^{1/6-\eta}\). The log net size at the largest dimension is
\[
O_\eta(k^{5/3-2\eta}\log k)
+O_\eta(k^{5/3-4\eta}\log k)
=o(k^{5/3}\log k),
\]
whereas the tail exponent is \((3/40)k^{5/3}\log k+O(k^{5/3})\). The number of possible dimensions adds only \(O(\log k)\). Consequently, for each fixed \(0<\eta<1/6\), with probability \(1-\exp[-\Omega_\eta(k^{5/3}\log k)]\), every finite-dimensional tensor-product strategy of local Schmidt rank at most \(k^{1/6-\eta}\) has value at most \(1/2\).

Shared randomness cannot improve this bound: its payoff is an average of the payoffs of its fixed-seed strategies. The proof does not cover unrestricted local dimension, commuting-operator strategies, or produce an explicit graph without a separate derandomization/construction.
