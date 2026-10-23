# Native one-crossing critical lower and its actual full law

Contributor: `/root/heterogeneous_transport`. Scientific date: 22 October
2026, Australia/Brisbane. This is a new three-state construction for the
Cycle6 global-dominant critical window. It does not take a singular endpoint
of a growing-tree proof. Its proposal is a fixed symmetric matrix independent
of n, pi, q and the target evaluations.

## 1. Statement and exact family

Fix K>0, alpha in (0,1), beta=1-alpha, and a real s. Let

\[
 L=\log n,\qquad u_n=\eta_n L=\log L+s+o(1),\qquad
 \delta=e^{-K},\quad b_K=1-\delta.
\]

For all sufficiently large integers n define

\[
 b=b_K-u_n^{-2},\qquad p=L^{-4},\qquad
 q_\ell={p\over nL^2},\quad q_r=b,\quad q_z=1-b-q_\ell,
\]

\[
 \pi_r={p\over n^2},\qquad \pi_\ell=p,\qquad
 \pi_z=1-p-p/n^2.                                      \tag{1}
\]

The labels r,ell,z mean root, leaf and core. Use the proposal

\[
 Q=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}                  \tag{2}
\]

in the order (r,ell,z). Thus Q is symmetric stochastic and target independent.
Use the original native two-factor L_eta, independence G, and
`C=(I+alpha G+beta L_eta)/2`. Initialize with the complete law q. Eta_n is
fixed within its run.

**Proposition.** This family is eventually strictly positive and has
`D(pi||q)<K`. Its ACTUAL full-law TV error satisfies

\[
 \boxed{\quad
 \lim_{n\to\infty} L\|qC_{\eta_n}^{\,n}-\pi\|_{\rm TV}
   ={\beta\over\alpha}(e^K-1)e^{-s}.\quad}          \tag{3}
\]

The construction and (3) hold for every fixed K>0 and alpha in (0,1). Their
specific use is the regime `r0=alpha exp(-K)/beta>=1`, where they supply the
proposed sharp one-crossing amplitude. Combining the construction with the
unchanged ordinary-tail lower gives, in that regime,

\[
 \liminf L R_{\eta_n}(n)
  \ge\max\left\{K,{\beta\over\alpha}(e^K-1)e^{-s}\right\}.       \tag{4}
\]

Equation (4) is a minimax LOWER only until the separate all-class upper has
been accepted. No candidate upper or weighted energy argument is assumed here.
The two terms are from separate admitted families and do not add their budgets.

## 2. Positivity, exact weights and the single KL budget

Since b_K>0 and u_n tends to infinity, b>0 eventually. Also
`q_z=delta+u_n^-2-q_ell` tends to the strictly positive delta, while the target
core mass tends to one. All entries of pi,q are therefore strictly positive
and each vector sums to one exactly. The weights are

\[
 W_r={p\over b n^2},\qquad W_\ell=nL^2,\qquad
 W_z={1-p-p/n^2\over\delta+u_n^{-2}-p/(nL^2)}.
\]

For sufficiently large n they obey

\[
 0<W_r<1<W_z<W_\ell.                                \tag{5}
\]

In particular the root's KL contribution is negative. The core contribution
is at most log(1/q_z), so

\[
 D(\pi\|q)\le p\log(nL^2)+\log(1/q_z).
\]

Here `q_ell=o(u_n^-2)` and

\[
 \log(1/q_z)=K-e^K u_n^{-2}+o(u_n^{-2}),\qquad
 p\log(nL^2)=O(L^{-3})=o(u_n^{-2}).
\]

Consequently

\[
 D(\pi\|q)\le K-e^K u_n^{-2}+o(u_n^{-2})<K          \tag{6}
\]

eventually. The target tail entropy and the depleted-proposal entropy use one
budget. No rounded normalization, zero target probability, or empirical-KL
inference is used.

## 3. Exact native transitions

Let

\[
 \sigma=(q_\ell/b)^{\eta_n}.
\]

For large n, q_ell/b<1. The root-to-leaf target ratio is n^2, so the native
forward two-stage acceptance is exactly sigma: its second factor is
`min(1,n^2/sigma)=1`. The reverse first screen is one, and its second factor
is exactly `sigma/n^2`. Both are individual-state ratios; there are no grouped
level masses or suppressed multiplicities. Thus

\[
 L_{\eta_n}=
 \begin{pmatrix}
 1-\sigma&\sigma&0\\
 \sigma/n^2&1-\sigma/n^2&0\\
 0&0&1
 \end{pmatrix}.                                    \tag{7}
\]

Its diagonal is the actual rejection diagonal. In the same state order, the
independence kernel is exactly

\[
 G=\begin{pmatrix}
 b&q_\ell&q_z\\
 \pi_r/W_\ell&1-(1-p)/W_\ell&\pi_z/W_\ell\\
 \pi_r/W_z&q_\ell&1-\pi_r/W_z-q_\ell
 \end{pmatrix}.                                    \tag{8}
\]

These formulas follow directly from (5). In particular they retain all
return transitions, including core-to-root and core-to-leaf moves.

Put

\[
 f={\beta\sigma\over2},\quad
 a={\alpha q_z\over2},\quad
 c=f+{\alpha q_\ell\over2},\quad e_r=a+c.           \tag{9}
\]

The root's exact exit probability in C is e_r; its exit to the leaf has
probability c, including BOTH local and global moves, while its exit to the
core has probability a. Every other root transition is a true hold. The
leaf's exact escape probability is

\[
 e_\ell={\alpha(1-p)\over2nL^2}+{f\over n^2}.       \tag{10}
\]

The second term in (10) is the actual reverse-local probability, and the
first sums both accepted global exits. All quantities in (9)-(10) belong to
the unmodified three-state chain.

## 4. Exact finite lower, including time and retention

Let H=floor(n/2). Starting at the root, the probability that the first exit
is to the leaf and occurs by H is

\[
 {c\over e_r}[1-(1-e_r)^H].
\]

After that hit, staying at the leaf for all remaining steps has probability
at least `(1-e_ell)^n`. Selecting only these paths from the actual chain and
charging their actual proposal-start mass b gives

\[
 \boxed{\quad
 \|qC^n-\pi\|_{\rm TV}
 \ge b{c\over e_r}[1-(1-e_r)^H](1-e_\ell)^n-p.\quad}       \tag{11}
\]

Other initial states, earlier arrivals, failed paths and later returns are
not removed from the chain. They contribute nonnegative mass to the leaf
event and are simply unused by this lower certificate. In particular the
initial law is q, not a conditioned or deliberately cold root start.

## 5. A matching upper for the actual full law

Let tau_z be the first core hit, including time zero. Starting from the root,

\[
 P_r(\tau_\ell<\tau_z)=c/e_r,\qquad
 P_r(\tau_\ell\wedge\tau_z>n)=(1-e_r)^n.
\]

Therefore the full initial law obeys

\[
 P_q(\tau_z>n)\le q_\ell+b[c/e_r+(1-e_r)^n].       \tag{12}
\]

This is an upper bound: it deliberately counts every root-to-leaf arrival
before the core, whether or not a subsequent core hit occurs before n.

Let `p_tot=1-pi_z=p(1+n^-2)`. At a first core hit at time t, the subsequent
law is the exact original `delta_z C^(n-t)`, with every excursion and return
retained. TV contraction gives

\[
 \|\delta_z C^{n-t}-\pi\|_{\rm TV}
 \le\|\delta_z-\pi\|_{\rm TV}=p_{\rm tot}.
\]

Decomposing by the first core hit proves the finite upper

\[
 \boxed{\quad
 \|qC^n-\pi\|_{\rm TV}
 \le p_{\rm tot}+q_\ell+b{c\over e_r}+b(1-e_r)^n.\quad}       \tag{13}
\]

This is a full-law estimate and not a claim that later returns are absent.
It shows why potential later re-entry attempts from the core cannot change
this family's leading amplitude.

## 6. Asymptotics and the claimed amplitude

The screen satisfies the exact logarithmic identity

\[
 -\log\sigma
 =\eta_n[L+6\log L+\log b]
 =u_n+o(1),                                         \tag{14}
\]

because u_n is of order log L, b tends to fixed positive b_K, and
`eta_n log L=O((log L)^2/L)->0`. Hence

\[
 \sigma={e^{-s}\over L}(1+o(1)),\quad
 f={\beta e^{-s}\over2L}(1+o(1)),\quad
 a\longrightarrow{\alpha e^{-K}\over2}>0.
\]

Also q_ell/f tends to zero, c/f tends to one, and e_r tends to the same
positive constant as a. Thus

\[
 L b{c\over e_r}
 \longrightarrow {b_K\beta\over\alpha e^{-K}}e^{-s}
 ={\beta\over\alpha}(e^K-1)e^{-s}.                \tag{15}
\]

The finite waiting loss in (11) tends to zero exponentially in n.
Furthermore, (10) gives

\[
 n e_\ell={\alpha(1-p)\over2L^2}+{f\over n}
 \longrightarrow0,
\]

so the retention factor is 1+o(1), a relative estimate on the capture term.
Finally Lp, Lp_tot and Lq_ell all vanish; the remaining exponential term in
(13) vanishes after multiplication by L. Equations (11), (13), and (15)
squeeze the actual full law to (3).

The proof uses direct three-state formulas and their explicit errors. It is
not a finite-matrix observation extrapolated to an asymptotic theorem.

## 7. Same-instance ordinary independence-MH comparator

The comparison can be made analytically on this very family. For an integer
m>=0, a pure-G path at the root exits to the leaf with probability q_ell and
to the core with probability q_z; its total exit probability is 1-b. Thus the
same first-core decomposition gives

\[
 \|qG^m-\pi\|_{\rm TV}
 \le p_{\rm tot}+{q_\ell\over1-b}+b^{m+1}.          \tag{16}
\]

For the lower, the leaf can be occupied only if it was occupied initially or
if at least one of the m global proposals was the leaf. A union bound gives
`qG^m(ell)<=(m+1)q_ell`, regardless of rejection and later returns. Therefore

\[
 \|qG^m-\pi\|_{\rm TV}\ge p-(m+1)q_\ell.          \tag{17}
\]

For any deterministic m_n with `m_n/n->t in (0,infinity)`, (16)-(17) imply

\[
 \|qG^{m_n}-\pi\|_{\rm TV}\sim p=(\log n)^{-4}.    \tag{18}
\]

This includes m_n=n and m_n=floor(alpha n/2), the latter matching the hybrid's
expected number of global proposals up to rounding. It does not match target
cache misses, oracle latency, memory use or acceptance-uniform cost. No such
practical benchmark is claimed. The same-instance hybrid error is of order
1/log n, so the extra local crossing is demonstrably harmful on this family.

The general ordinary pure-IMH minimax comparator remains K/log n; equation
(18) is a different, same-instance statement. On a known three-state support,
access that permits evaluating the entire target also permits direct
normalization and discrete sampling. Such an implementation may be an even
stronger ordinary method; this construction makes no oracle advantage claim.
The proof's normalized tables do not disclose a normalizer to the sampler.

## 8. Status, unsuccessful routes and resources

No flaw in the candidate lower amplitude was found. A growing-tree endpoint
argument is unnecessary here: the finite optimal spacing is replaced by one
screened crossing with probability of order 1/log n, competing against constant
accepted-global escape. Q needs only three states and is literally unchanged
for all n. The global-dominant factor 1/r0 comes from this exact competition.

The all-class upper is a separate principal-owned obligation. This source does
not assume it or claim that a three-state lower excludes a stronger adverse
geometry. The inherited Q=I K lower is used only in (4), at its accepted scope.

No numerical job, matrix-power calculation, native graph materialization,
external search, hardware spending or outreach was performed for this proof.
Observed source-reading/writing timestamps may be recorded separately; active
reasoning time, inference/token costs, monetary cost and historical discovery
totals are unknown. Historical originality, internal proof acceptance, external
mathematical acceptance and practical sampler performance are distinct claims.
