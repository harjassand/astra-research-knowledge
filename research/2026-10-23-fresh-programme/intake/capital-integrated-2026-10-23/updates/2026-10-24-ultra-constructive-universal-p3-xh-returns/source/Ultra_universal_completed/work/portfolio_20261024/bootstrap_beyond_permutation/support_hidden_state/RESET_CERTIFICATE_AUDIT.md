# Audit: Hankel span acquisition and a robust reset certificate

Scope: checks the proposed observable-coordinate sampler/reset construction
in `../FIRST_CONSTRUCTION.md`. The results below are conditional on a finite
action/test interface and an actual finite-dimensional Hankel-rank promise.
They do not claim that a reset mixture exists or that it amortizes the
external initializer.

## Exact finite-word span from a rank bound

Suppose the raw action alphabet is finite, of size (q), the experiment
probabilities are time-homogeneous, and their full Hankel matrix

\[
H_{w,t}=h(wt)
\]

has rank (r\le m). For a linear representation
\(h(wt)=\alpha A_w A_t\beta\), let
\(R_k=\operatorname{span}\{\alpha A_w:|w|\le k\}\). If
\(R_k=R_{k+1}\), then (R_k) is invariant under every one-letter action
matrix and hence is the full reachable row space. Otherwise its dimension
strictly increases. Thus words of length at most (r-1\), and certainly at
most (m-1\), span the reachable space. The reverse argument for columns
\(A_t\beta\) gives the same bound for tests. Therefore the finite block
\(\mathcal H_m=(h(wt))_{|w|,|t|\le m-1}\) has the full Hankel rank (r\).

This justifies complete-span acquisition with exact probabilities by
enumerating all words through length (m-1\), forming the block, and selecting
an invertible (r\times r\) minor. With (q\) actions, the word count is
\(N=\sum_{k=0}^{m-1}q^k\); the uncompressed block has (N^2\) entries and
the longest acquired experiment has at most (2(m-1)\) symbols. This is
finite, but already exponential in (m\). A supplied *upper bound* (m\) is
enough for exact span acquisition under these finite-alphabet and
time-homogeneous assumptions; it does not provide a good basis or a cheap
one.

If controls have a continuum of durations/levels, a finite set of known
generators or another finite distinguishing-test promise is needed. A rank
bound alone does not make an uncountable raw action interface enumerable.
Likewise, “bounded tests” must include the normalization experiment (the
empty continuation, or an acquired linear combination (c) with
\(Hc=\mathbf 1\) and (x(w)c=1\)). If executions can terminate or lose mass,
failure/death must be included among outcomes before using this normalization.

The all-continuation bound applies to the continuation-test family whose
Hankel span was promised. Arbitrary observation-adaptive policies are covered
only if their finite policy/event trees are also represented in that same
controlled linear interface; an open-loop rank promise should not be
silently extended to a different output interface.

## Exact reset implication and outer-box bound

Take acquired preparation and test bases (B=(b_i)_{i=1}^r) and
\(T=(t_j)_{j=1}^r\), with nonsingular (H_{ij}=h(b_i t_j)). Let
\(H_u[i,j]=h(b_iut_j)), \(M_u=H^{-1}H_u\), and
\(S=\sum_{u\in U}\lambda_uM_u\), where \(\lambda_u\ge0\) and
\(\sum_u\lambda_u=1\). Write \(G=HS=\sum_u\lambda_uH_u\).

If every row of (G) is the same row (v), then
\(S=H^{-1}\mathbf 1v=cv\), where (Hc=\mathbf 1\). For every reachable
history (w), its test coordinate row (x(w)) satisfies
\(x(w)c=1\), and hence
\(x(w)S=x(w)cv=v\). The intervention resets predictive behaviour, even
if it does not reset a physical hidden state.

There is also a useful approximate version that does not assume a latent
reachable cone. Suppose, for some row (0),

\[
\max_{i,j}|G_{ij}-G_{0j}|\le\delta.
\]

Let \(a(w)=x(w)H^{-1}\). Each coordinate of (x(w)) is a probability, so
\(x(w)\in[0,1]^r\), giving
\(
\|a(w)\|_1\le \sqrt r\|x(w)\|_2\|H^{-1}\|_2
\le r/\sigma_{\min}(H)=:C_H.
\)
Normalization gives \(\sum_i a_i(w)=1\). Taking the legal target to be
the predictive state produced from (b_0) followed by the randomized word,
\(v=G_{0,:}\), yields

\[
\|x(w)S-v\|_\infty
 =\left\|\sum_i a_i(w)(G_{i,:}-G_{0,:})\right\|_\infty
 \le C_H\delta.
\]

For any bounded continuation test (s), let
\(q_s=(h(b_i s))_i\in[0,1]^r\). Completeness gives its basis-coordinate
vector \(\theta_s=H^{-1}q_s\), so
\(\|\theta_s\|_1\le C_H\). Therefore

\[
|h(wUs)-h(b_0Us)|=|(x(w)S-v)\theta_s|
\le C_H^2\delta.
\]

This is uniform over all reachable past histories and all continuation tests
in the acquired finite-rank interface, including tests of any finite future
horizon. Thus the positive outer box ([0,1]^r) is enough to give a
certificate, but the price is **quadratic amplification by the inverse-basis
condition bound**. If only a fixed finite family of terminal outcomes is
available, the statement is for those scalar tests; transcript total
variation additionally needs all relevant event tests (or an explicit
outcome-count/horizon conversion).

## Finite-noise certificate, with its required promises

Assume binary outcomes, (n_0) independent externally initialized trials
per scalar probability, and use a simultaneous Hoeffding event. For (M)
predeclared probability entries, each estimate has error at most \(\eta\)
with probability at least (1-\alpha\) when

\[
n_0\ge \frac{1}{2\eta^2}\log\frac{2M}{\alpha}.
\]

If all entries of an (N\times N\) truncated Hankel block are estimated,
its spectral error is at most (N\eta_H\). A finite-sample **exact span
completeness** certificate needs a separation promise: for example, every
nonzero singular value of the true truncated block is at least
\(\gamma_{\rm rank}>0\). With \(N\eta_H<\gamma_{\rm rank}/4\), thresholding
the estimated singular values at \(\gamma_{\rm rank}/2\) certifies its true
rank; the length-(m-1\) argument then makes that the complete Hankel rank.
An upper bound (r\le m\) alone is insufficient to distinguish a true zero
singular value from an arbitrarily small nonzero one.

After selecting a square basis block, if its entrywise estimation error is
at most \(\eta_B\), then
\(\sigma_{\min}(H)\ge\widehat\sigma_{\min}-r\eta_B=:\gamma_B\).
Require \(\gamma_B>0\); then (C_H\le r/\gamma_B\). For a fixed finite
word library (U), estimate all entries of all (H_u) with simultaneous
entrywise error \(\eta_U\). Choose λ by the linear program

\[
\min_{\lambda\in\Delta(U)}\max_{i,j}
\left|\sum_{u\in U}\lambda_u
  (\widehat H_u[i,j]-\widehat H_u[0,j])\right|.
\]

If its value is \(\widehat\delta\), the true row residual for the selected
mixture is at most \(\widehat\delta+2\eta_U\), even when λ was selected
adaptively from these data, because the confidence event is simultaneous
over the whole predeclared library. Alternatively, use independent
validation samples after selecting λ. The resulting all-history,
all-continuation error certificate is

\[
\epsilon_{\rm beh}\le
\left(\frac{r}{\gamma_B}\right)^2(\widehat\delta+2\eta_U)
 +\rho_{\rm mix},
\]

where \(\rho_{\rm mix}\) is the total-variation error from implementing
the desired word distribution with finite random bits. It is zero for exact
sampling; a dyadic approximation within \(\rho_{\rm mix}\) adds at most that
much to any event probability. A robust LP can instead constrain the
confidence intervals directly.

For target error ε with exact mixture sampling, the validation precision
must satisfy \(\eta_U\le\epsilon\gamma_B^2/(4r^2)\) if the fitted residual
is negligible, giving
\(n_0=O(r^4/(\gamma_B^4\epsilon^2)\log(|U|r^2/\alpha))\) repeats per
entry. This is in addition to rank/basis acquisition. It is a certificate
conditional on a separated, well-conditioned basis, not a uniform bound
from (m) alone.

Every sample is a physical trial from the external initializer: estimating
\(h(wt)\) requires initializer + execution of the concatenated word + test
readout. Full-span discovery uses up to (N^2n_0\) such trials and at most
\(2(m-1)\) symbols per word. Reset validation for library (U) costs
\(|U|r^2n_0\) trials, with per-trial word length
\(|b_i|+|u|+|t_j|\). Charge initializer, actuation duration, readout,
LP/linear algebra, storage, precision, and randomization. After certification,
one reset use costs the sampled word’s expected execution cost plus random
selection; the comparison against the external initializer is an amortization
question, not a consequence of the algebra.

## Countermodel: rank bound alone gives no finite-noise uniform guarantee

Use two hidden states (0,1), an expensive initializer fixed at state (0),
one raw action (a), and a bounded test (t) that reports whether the state
is (1). Let

\[
P_\epsilon=\begin{pmatrix}1-\epsilon&\epsilon\\0&1\end{pmatrix},
\qquad
h_\epsilon(a^kt)=1-(1-\epsilon)^k.
\]

For (0<\epsilon<1), the continuation/Hankel rank is exactly two (the
sequence is the sum of the distinct exponentials (1^k) and
\((1-\epsilon)^k\)); for ε=0 it is one. With preparation basis
\((\varepsilon,a)\) and tests \((\varepsilon,t)\),

\[
H_\epsilon=\begin{pmatrix}1&0\\1&\epsilon\end{pmatrix},
\qquad \det H_\epsilon=\epsilon,
\qquad \sigma_{\min}(H_\epsilon)=\Theta(\epsilon).
\]

So the rank-2 span exists for every positive ε but becomes arbitrarily
ill-conditioned. The finite exact word span bound still holds; what fails is
uniform noisy rank identification and useful amplification control.

More directly, let a proposed reset mixture use words (a^j) with (j\le L).
Put (A=\sum_j\lambda_j(1-\epsilon)^j\ge(1-\epsilon)^L\). Starting
from state 0, its post-reset (t)-probability is (1-A); starting from the
reachable history (a^k), it is (1-(1-\epsilon)^kA). As (k\to\infty),
these differ by (A\ge(1-\epsilon)^L). Thus any common target incurs
worst-case error at least \((1-\epsilon)^L/2\). If
\(\epsilon\le1/(4L)\), this is at least (3/8); no mixture of words up to
length (L) is a (1/3)-reset for all reachable histories.

Yet every initializer-based query of total length at most (L) has success
probability at most (L\epsilon), and under the rank-one ε=0 model it is
zero. Across at most (N_q) such trials, the probability of seeing any
success under the rank-two model is at most (N_qL\epsilon). Choose
\(ε\ll1/(N_qL)\) and the two data laws are arbitrarily close, while
the finite-word uniform-reset conclusion differs. Therefore no algorithm
with a fixed finite noisy budget can both certify soundly and be complete
uniformly over the supplied rank-upper-bound class. A nontrivial guarantee
needs a singular-value/conditioning margin, a known reachability/synchronizing
promise, a restricted horizon/history set, or permission to return
“uncertified.”

This countermodel also shows why “small residual on the acquired basis rows”
alone is not a valid reset certificate: for a short word (a^j), the basis
row difference on (t) is only
\(h(a^{j+1}t)-h(a^jt)=\epsilon(1-\epsilon)^j\), while a long reachable
history can remain behaviorally far from the target. The (C_H^2) factor
detects this obstruction rather than treating the positive box as a free
latent cone.
