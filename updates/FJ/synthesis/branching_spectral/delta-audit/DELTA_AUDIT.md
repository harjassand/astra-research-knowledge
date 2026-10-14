# Delta audit: hard caps for the bounded PDE correction observation channel

This is a separate addendum to the frozen FJ branching packet. It audits the
root-proposed composition of N722's positive Poisson-clipped Gaussian-mean
factory with bounded PDE correction samples, and independently checks a
nonlinear multitype certificate for hard tree caps. The frozen originals were
not edited. The claim is conditional on the N722 theorem's ideal-real model;
this addendum does not turn its source status into an independent literature
or finite-bit certification.

## Audited construction

For a root type (x), let one exact FJ tree return (S_x=h(x)Z_x), with
(|Z_x|le1). For a vector acquisition, independently generate the fixed-root
outputs (S_A,S_B) and return

\[
 X=(S_A,S_B)/\sigma,
 \qquad \|X\|_2\le R=\sqrt{h_A^2+h_B^2}/\sigma.
\]

Across acquisitions, use fresh independent tree randomness. Dependence between
the two coordinates would also be allowed by N722; only independence of the
full vector acquisitions is required. Their mean is
\(\mu=(e_A,e_B)/\sigma\), where (e=u-v) is the PDE correction.

Apply the N722 factor factory with

\[
 m=\left\lceil64(1+R^2)\log\frac{64(1+R^2)}{\varepsilon_g}\right\rceil.
\]

Under the exact N722 interface, it returns (Y) with
\(\operatorname{TV}(\mathcal L(Y),N(\mu,I_2))\le\varepsilon_g\), without
using or estimating \(\mu\). For \(\sigma>0\), the affine output
\(v+\sigma Y\) is therefore within the same TV distance of
\(N(u,\sigma^2 I_2)\). This is a composed observation-channel operation for
an acquired bounded correction oracle. It is not a new FORS result and does
not supply a generic closure of N687: a globally Lipschitz field evaluated at
a Gaussian input need not have the certified bounded radius N722 requires.

## Frontier product certificate

Let a multitype branching tree have bounded offspring, and let (N) be the
number of processed nodes under breadth-first search. For every type (x),
suppose there is a finite offspring multiset and numbers (z>1), (t(x)\ge1)
such that

\[
 z\,\mathbb E_x\!\left[\prod_{c\in\mathrm{children}}t(\mathrm{type}(c))\right]
 \le t(x). \tag{F}
\]

After (k) nodes have been processed, let (Q_k) be the current frontier and
put

\[
 W_k=z^{k\wedge N}\prod_{c\in Q_{k\wedge N}}t(\mathrm{type}(c)).
\]

If the next node has type (x), its processing replaces the factor (t(x))
by the product over its children and multiplies the whole expression by (z).
Condition (F) gives \(\mathbb E[W_{k+1}\mid\mathcal F_k]\le W_k\). Once the
frontier is empty, this stopped process stays at (z^N). It is a nonnegative
supermartingale starting at (t(x_0)). On \(N>n\), the frontier after (n\)
steps is nonempty and every frontier factor is at least one, so

\[
 \Pr_{x_0}(N>n)\le t(x_0)z^{-n}.
\]

Fatou's lemma applied to (W_k\) yields
\(\mathbb E_{x_0}z^N\le t(x_0)\); in particular the tree terminates almost
surely. This proves the root-proposed frontier argument. The assumption that
the child multiset is sampled fresh conditional on its parent type is the
branching independence premise; dependence across generations beyond that
premise is not covered.

For comparison, suppose every processed type has conditional mean offspring at
most (q<1), and offspring count lies in \([0,b]\). Pad the BFS offspring
sequence by zeros after extinction. The centered increments have conditional
range length at most (b). On (N>n), the queue remains nonempty after (n)
processed nodes. Azuma-Hoeffding gives the conservative bound

\[
 \Pr(N>n)\le
 \exp\!\left[-\frac{2(n(1-q)-1)_+^2}{n b^2}\right].
\]

With the exact queue convention (Q_n=1-n+\sum_{k\le n}\xi_k\),
\(N>n\) actually implies \(\sum D_k\ge n(1-q)\), so the displayed bound
can be strengthened. The parent-proposed version is valid and sufficient. For
\(n\ge2/(1-q)\), it implies
\(\Pr(N>n)\le\exp[-n(1-q)^2/(2b^2)]\). This uniform-mean route cannot be
applied when a type has mean offspring above one; condition (F) can still
apply by accounting for the types of descendants.

## Exact two-type PDE witness

Use the frozen two-state continuous-time Markov chain and semilinear equation

\[
 L=\begin{pmatrix}-3&3\\3&-3\end{pmatrix},\quad \Lambda=2,\quad
 K=2(2I-L)^{-1}=\begin{pmatrix}5/8&3/8\\3/8&5/8\end{pmatrix},
\]
\[
 -Lu+F(x,u)=s,\quad v=0,\quad s=(1,0),\quad
 F_A(a)=a+a^2/2,\quad F_B(a)=2a,
\]
with envelope \(h=(2,1)\), tangent \(V=(1,2)\), and quadratic envelope
coefficient \(B_2=(1/2,0)\). All input values and rows are rational. The
source masses \(A_0=K(|s|/2)\), unary masses
\(A_1=K[(1-V/2)h]\), and quadratic masses
\(A_2=K[B_2h^2/2]\) are respectively

\[
 A_0=(5/16,3/16),\qquad A_1=(5/8,3/8),\qquad A_2=(5/8,3/8).
\]

Their totals are \((25/16,15/16)\le h\), so the pointwise branching
probabilities are source/unary/binary/zero-leaf

\[
 (5/32,5/16,5/16,7/32)\text{ at A},\qquad
 (3/16,3/8,3/8,1/16)\text{ at B}.
\]

Every child endpoint has type A: both \((1-V/2)h\) and \(B_2h^2/2\) are
supported only at A. Thus the offspring PGFs are

\[
 G_A(s)=3/8+(5/16)s+(5/16)s^2,\qquad
 G_B(s)=1/4+(3/8)s+(3/8)s^2.
\]

The mean-progeny matrix is
\(M=\begin{pmatrix}15/16&0\\9/8&0\end{pmatrix}\). A rational weighted
mean witness \(w=(1,6/5)\) gives \(Mw=(15/16)w\), so the root-B mean above
one does not imply a supercritical tree. For the stronger tail certificate,
take

\[
 t_A=11/10,\qquad t_B=9/8,\qquad z=501/500.
\]

Exact arithmetic gives
\(G_A(t_A)=351/320\) and
\(zG_A(t_A)=175851/160000\le11/10\), while
\(G_B(t_A)=893/800\) and
\(zG_B(t_A)=447393/400000\le9/8\). These are exactly (F), including
the type-B row. Consequently

\[
 \Pr_A(N>n)\le(11/10)(501/500)^{-n},\qquad
 \Pr_B(N>n)\le(9/8)(501/500)^{-n}.
\]

This exact case fails the frozen source's scalar global test: with
\(\lambda=\min V=1\), \(B_2=1/2\), and residual bound 1,
\(\sup_{a\ge0}(a-a^2/2)=1/2<1\); also the reported
\(\Gamma=2>\lambda\). It is nevertheless certified by the local envelope,
the weighted mean-progeny condition, and the new exponential-moment witness.
The frozen weighted-\(M\) proof already established expected termination;
the delta's addition is an exponential tail and a deterministic truncation
bound, not a newly discovered PDE solution or a new expected-work claim.

The exact solution in the certified tube is
\(u_A=(-11+3\sqrt{19})/5\), \(u_B=3u_A/5\). The identity
\(u_A^2+(22/5)u_A-2=0\) is checked coefficientwise in
\(\mathbb Q(\sqrt{19})\). The resolvent, envelope, event probabilities,
offspring PGFs, mean matrix, old-criterion failure, and the new \((t,z)\)
inequalities are checked by `verify_delta.py` using exact fractions.

## Exact outer cap and costs

For this PDE oracle use \(\sigma=1\), \(d=2\),
\(X=(S_A,S_B)\), \(R^2=2^2+1^2=5\), and
\(\varepsilon_g=\delta=1/4\). The exact ceiling checks give

\[
 m=2818,\quad K=78,\quad J_{\rm cap}=19,\quad
 B=r_{\rm roots}mKJ_{\rm cap}=8{,}352{,}552,\quad r_{\rm roots}=2.
\]

Allocate \(\delta/3\) each to the factory proposal cap, Poisson cap, and
tree-node cap:

* A proposal succeeds with conditional probability at least \(e^{-2}\).
  Hence failure for one factor in \(K\) attempts is at most
  \((1-e^{-2})^K\le e^{-K/e^2}\le\delta/(3m)\). A union bound over (m)
  factors costs at most \(\delta/3\).
* For each Poisson(2) draw,
  \(\Pr(J>J_{\rm cap})\le\exp(2(e-1)-J_{\rm cap})\). The chosen cap makes
  this at most \(\delta/(3mK)\); union over at most \(mK\) proposals costs
  at most \(\delta/3\). Implement capped inversion by comparing a uniform
  draw with the exact \(F_{\mathrm{Pois}(2)}(J_{\rm cap})\); abort if it is
  above that CDF, otherwise search only the finite range through (J_{\rm cap}).
  Clamping (J) to the cap or sampling a conditional truncated Poisson
  without an abort changes the factory law and does not have this coupling.
* For the (B) possible tree slots, choose
  \[
  n_{\rm cap}=\left\lceil
  \frac{\log(3B(9/8)/\delta)}{\log(501/500)}\right\rceil=9280.
  \]
  The ceiling is exact because
  \((501/500)^{9279}<112{,}759{,}452\le(501/500)^{9280}\), where
  \(112{,}759{,}452=3B(9/8)/\delta\). The union-bound contribution is at
  most \(\delta/3\).

Abort globally on any cap failure and return a fixed fallback vector. On the
complement of all cap failures, couple every factory proposal, Poisson draw,
and tree with the uncapped N722 execution; the outputs agree. Therefore
\(\Pr(\mathrm{abort})\le\delta\), and the returned law obeys

\[
 \operatorname{TV}(\mathcal L(v+\sigma Y),N(u,\sigma^2I_2))
 \le \varepsilon_g+\delta=1/2.
\]

The deterministic branch-node cap is
\(B n_{\rm cap}=77{,}511{,}682{,}560\). It is mathematically finite but
very conservative. The exact rational ceiling checks are in the verifier;
its logarithm enclosures use a positive atanh series with a rational geometric
remainder, and the nonlinear tree cap uses exact rational powers.

The expected number of branch nodes is much smaller. From the mean matrix,
\(\mathbb E N_A=1/(1-15/16)=16\), and
\(\mathbb E N_B=1+(9/8)/(1-15/16)=19\). Thus each full vector acquisition
has expected 35 node visits. The outer factory requests the next acquisition
before observing that acquisition's vector or its tree cost: proposal state
and the current Poisson count are already known. If \(I_k\) indicates that
acquisition (k) is requested, it is measurable with respect to the prior
history; for fresh acquisition cost \(C_k\),

\[
 \mathbb E\sum_k I_k C_k
 =\sum_k\mathbb E[I_k\,\mathbb E(C_k\mid\mathcal F_{k-1})]
 \le \bar C_X\,\mathbb E N_{\rm acq}
 \le 2e^2m\,\bar C_X.
\]

This predictable-acquisition argument permits \(C_k\) to correlate with
\(X_k\). If an individual tree cap aborts partway through a requested vector,
couple that partial run to the full latent uncapped acquisition; its processed
work is no more than the full acquisition cost used in the expectation bound.
For these roots, the expected node-type counts per vector are 34 A-nodes and
1 B-node. A nonzero source/unary/binary event draws one tilted resolvent
endpoint; its expected count is exactly \(55/2\) per vector. If \(c_A,c_B\)
price node processing excluding endpoint draws, \(c_K\) prices an exact
tilted endpoint operation, and \(c_{\rm read}\) prices vector writes/reads,
then \(\bar C_X=34c_A+c_B+(55/2)c_K+c_{\rm read}\), after separately
charging setup. With one unit per node and ignoring the separate endpoint
charge, this yields at most \(70e^2m\) expected node visits plus output reads
and factory arithmetic.
It requires a uniform conditional expected acquisition-cost bound; iid vector
values alone do not imply that bound. The setup charge
\(C_{\rm setup}\) must include acquisition and full-domain verification of
\(L,K,\Lambda,v,r,V,B_m,h,A_j\), event probabilities, the spatial/type
partition, the complete \(t,z\) inequalities, and tilted endpoint laws.
Each node also pays for event selection, exact endpoint sampling, coefficient
reads, and return arithmetic. In this two-state example those are finite
rational operations and a finite-state resolvent draw. For a continuous
diffusion, exact tilted resolvent sampling and full-domain certificate
acquisition are not discharged here; they cannot be treated as free.

The hard bound is a node-count bound in the ideal exact-random-real model.
Factory work can also be deterministically bounded in that model by the
proposal/acquisition caps, with at most (mK) proposals and (mKJ_{\rm cap})
vector acquisitions. This does not certify bit complexity, random-bit
consumption, finite-precision acceptance, physical energy, or a rounded-output
TV guarantee. N722 states these limits explicitly.

## Uniform-subcritical control case

For an independent check of the queue/Azuma route, take
\(L=[[-1,1],[1,-1]]\), \(\Lambda=2\),
\(K=[[3/4,1/4],[1/4,3/4]]\), equation \(-Lu+u=(1/4,1/4)\), predictor
zero, and (h=(1,1)). Then (u=(1/4,1/4)), (A_0=(1/8,1/8)),
(A_1=(1/2,1/2)), zero-leaf probability (3/8), and the offspring count
is Bernoulli(1/2): (q=1/2,b=1). Exact sampling of a unary endpoint is a row
of (K), and each tree has expected two nodes. Here both controls apply:
the constant nonlinear witness (t=2,z=4/3) satisfies
\(z(1/2+1/2\cdot2)=2\), while the uniform-mean Azuma tail also applies.
With the same \(\varepsilon_g=\delta=1/4\), the exact cap arithmetic gives
\(m=1276,K=72,J_{\rm cap}=18,B=3{,}307{,}392,n_{\rm cap}=140\), or
\(463{,}034{,}880\) hard branch nodes. Again, setup, finite-state transition
data, endpoint draws, and exact arithmetic are charged.

## Prior methods and status

Positive supersolutions for branching-PDE moments are established prior art.
Agarwal and Claisse, Proposition 3.4, bound (L^q) moments using a
nonnegative spatial supersolution; their Section 3.3 says a nonconstant
supersolution may need to be found case by case. Huang and Privault (2026
revision), Sections 6–7, control multiplicatively weighted progeny through
stochastic dominance and Hamilton–Jacobi bounds. The frozen FJ packet already
compares its event-first positive resolvent decomposition with these methods
and notes that the actual endpoint proposal laws, envelopes, and certificate
must be acquired and priced.

The present frontier condition is a compact probability-generating-function
Lyapunov certificate for a different quantity: the exponential moment of
total BFS node count, with a direct tail sufficient to truncate the tree.
It is compatible with the same family of positive-supersolution methods and
is not claimed as historically novel. Event-first sampling of source/unary/
nonlinear marks with coefficient-tilted resolvent endpoints remains an
importance-sampling-style change of measure. Marked branching representations
and variance-directed importance-sampling schemes already appear in
Henry-Labordère et al.'s branching PDE work; this delta neither improves that
proposal quality nor reduces expected work. The two-type exact example adds a
hard-cap route where the uniform (q<1) cap fails, but its hard cap is huge
and it establishes no computational advantage over deterministic, multilevel,
or existing branching methods.

The N722 positive Poisson factory is itself a known stochastic FORS
specialization, not a new operation. Chen et al.'s primary paper presents
FORS and its Gaussian-tilt stochastic-query theorem (Theorems 3.1–3.2);
N722 records the bounded-vector mean specialization and identifies this as its
strongest same-oracle comparator. N722's source dossier remains
`source_derived_unreviewed`, with an open acquisition/finite-bit gate. The
composition here supplies a concrete bounded PDE oracle and explicit failure
caps under the stated assumptions; it does not promote that source evidence
status, close N687, or establish novelty, diffusion feasibility, or physical
validation.
