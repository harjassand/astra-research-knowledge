# A conserving-ring current obstruction to common deterministic rotation

29 October 2026. Root supplied the exact parity-dependent conserving-ring family and its current corrector. This complementary note completes a functional current-CLT receiver for deterministic rotation. Root's separately developed common-Poisson construction supplies a stronger rare-current upper-bound obstruction; this note does not duplicate or claim that result.

## 1. Concrete consequence

There is a uniformly elliptic, reversible, conserving nearest-neighbor ring for which an actual common phase rotation can become arbitrarily fast and still fail to recover the mean-rate current fluctuations.

Let \(N\) be even, let \(M_N\) be odd with \(M_N/N\to m\in(0,1)\), and start the occupations from the uniform canonical law \(\pi_{N,M_N}\). The actual native rate on bond i is

\[
r_i(t,\eta)=c[1+\alpha\cos(\Omega_Nt)\,p(\eta)\delta_i(\eta)],
\quad c=s/2,\quad0<\alpha<1, \tag{1}
\]

where

\[
\delta_i=\eta_i-\eta_{i+1},\qquad
p(\eta)=(-1)^{\sum_{i=1}^N i\eta_i}. \tag{2}
\]

The requested observable is the **actual total signed particle current** \(J(t)=\sum_iJ_i(t)\), not parity. If

\[
\Omega_N\to\infty,\qquad \Omega_N/N\to0, \tag{3}
\]

then on every fixed macroscopic interval \([0,T]\),

\[
\left\{\frac{J(N^2t)}{N^{3/2}}:0\le t\le T\right\}
\ \Rightarrow\
\sqrt{s\,m(1-m)(1-\alpha^2/2)}\,B_t. \tag{4}
\]

For the mean-rate SSEP, the corresponding variance coefficient is \(s\,m(1-m)\). Thus a genuine low-order transport observable retains an order-one effect from global context, even while the common rotation frequency diverges. The intermediate regime \(\Omega_N\asymp N\), and a sharp deterministic threshold for every conserving model, are not derived here.

The initial visible law is explicitly canonical equilibrium. The proof does not claim a pointwise conditional theorem after exposing the entire initial microscopic configuration, nor the deterministic-initial-profile rare-event result of root's independent-control theorem. A warranted baseline preparation could supply this initial law at its actual cost. No copying, selective restart or microscopic reversal is used by the controller.

## 2. Why this is an admitted reversible exchange family

For even N, every active nearest-neighbor exchange flips p, including the periodic wrap bond. It also flips \(\delta_i\). Therefore

\[
\alpha_i(\eta):=\alpha p(\eta)\delta_i(\eta)
\]

is invariant under its own bond exchange and obeys \(|\alpha_i|\le\alpha\). Inactive bonds have \(\delta_i=0\) and cause no state change. Equation (1) is exactly the cosine-modulation family with a single common phase \(\theta(t)=\Omega_Nt\), and the phase-preserving native transitions conserve particle number.

All rates are between \(c(1-\alpha)\) and \(c(1+\alpha)\). Every instantaneous generator is reversible in \(\pi_{N,M_N}\). Consequently the visible marginal stays exactly canonical for every deterministic schedule q(t) in place of the cosine, even though the process is time-inhomogeneous.

The amplitude depends on the full configuration. This is intentionally inside the allowed nonlocal mathematical class. It is not an apparatus construction of instantaneous global parity coupling. The counterexample identifies a real distinction between admitted control interfaces; it does not establish that a particular laboratory device realizes these coefficients.

## 3. Exact native-current martingale

Put \(A(\eta)=\sum_i\delta_i^2\), the number of active bonds, and let q(t) be any differentiable deterministic function with \(|q|\le1\). The total exit rate is

\[
\sum_i r_i\delta_i^2=cA,
\]

because \(\sum_i\delta_i=0\) on the ring. The exact generator identities are

\[
L_tJ=c\alpha q(t)pA,\qquad L_tp=-2cpA. \tag{5}
\]

Define \(\mathcal M(t)\) by summing, at each native particle jump on bond i, the increment

\[
\Delta\mathcal M=\delta_i-\alpha q(t)p_{t-}. \tag{6}
\]

Its conditional drift is exactly zero:

\[
\sum_i r_i\delta_i^2(\delta_i-\alpha qp)
=c(1-\alpha^2q^2)\sum_i\delta_i=0.
\]

Hence \(\mathcal M\) is already a martingale; no compensator of order N was omitted. Its jumps have magnitude at most \(1+\alpha\), and

\[
\frac{d}{dt}\langle\mathcal M\rangle_t
=\sum_i r_i\delta_i^2(\delta_i-\alpha qp)^2
=cA(1-\alpha^2q(t)^2). \tag{7}
\]

At a native jump, \(\Delta p=-2p_{t-}\). Integration by parts therefore gives the exact identity

\[
J(t)=\mathcal M(t)-\frac\alpha2[q(t)p_t-q(0)p_0]
                 +\frac\alpha2\int_0^t q'(u)p_u\,du. \tag{8}
\]

The endpoint term is bounded by \(\alpha\). The only nontrivial rotating-control residue is the last integral.

For a constant q this residue is zero. The same proof below immediately yields the current Brownian coefficient \(s\chi(m)(1-\alpha^2q^2)\), with no parity inverse estimate needed. This is an exact conserving counterpart of a kinetic floor, but constant q alone would not challenge increasingly rapid averaging.

## 4. Parity has a microscopic inverse-energy bound of order 1/N

Choose the fixed disjoint matching \((1,2),(3,4),\ldots,(N-1,N)\). Let K be its number of active pairs, and let

\[
L_{\rm match}=\sum_{i\in\{1,3,\ldots,N-1\}}(\tau_i-I).
\]

K is invariant under matching swaps, and

\[
L_{\rm match}p=-2Kp. \tag{9}
\]

Since the total particle number M is odd, K is odd and never zero. Conditional on every pair's particle count, at least one pair has one particle; its uniform orientation flips p. Thus p has mean zero in every matching class, as well as globally. In particular

\[
g=\frac{p}{2K},\qquad -L_{\rm match}g=p,
\quad\langle p,g\rangle=\mathbb E_\pi\frac1{2K}. \tag{10}
\]

The reciprocal expectation has a useful direct counting bound. Put n=N/2. The generating polynomial for particle number x and active-pair count t is

\[
(1+2tx+x^2)^n.
\]

Integrating t from 0 to 1 gives

\[
\mathbb E_\pi\frac1{K+1}
=\frac{\binom{N+2}{M+1}-\binom{n+1}{(M+1)/2}}
       {(N+2)\binom NM}
\le\frac{N+1}{(M+1)(N+1-M)}. \tag{11}
\]

Since \(1/(2K)\le1/(K+1)\), (10)-(11) bound the matching inverse energy. The actual instantaneous native Dirichlet form dominates \(c(1-\alpha)\) times the matching form. Its full canonical chain is connected. Therefore, uniformly in t and the prescribed q,

\[
\langle p,(-L_t)^{-1}p\rangle_\pi
\le C_N:=\frac{N+1}
 {c(1-\alpha)(M+1)(N+1-M)}=O(N^{-1}). \tag{12}
\]

This estimate uses a fast collective parity direction without assuming a global spectral gap of order N. The ordinary visible conserved gap can still be of order N^-2. The matching is a proof comparison, not an extra physical operation.

## 5. A time-dependent forward/backward maximal estimate

Here is the needed estimate with its time dependence explicit. Suppose finite-state generators \(L_t\) are reversible in the same \(\pi\), the process starts at \(\pi\), and a smooth centered source \(v_t\) satisfies

\[
\langle v_t,(-L_t)^{-1}v_t\rangle\le b_t.
\]

Then, on a physical interval \([0,S]\),

\[
\mathbb E_\pi\sup_{t\le S}
\left|\int_0^t v_u(X_u)du\right|^2
\le20\int_0^S b_u\,du. \tag{13}
\]

To verify it, set \(f_t=(-L_t)^{-1}v_t\). The forward Dynkin martingale for \(f_t(X_t)\) has expected bracket \(2\int\mathcal D_t(f_t)dt\). The reversed visible process on \([0,S]\) has generator \(L_{S-t}\), because its marginals are \(\pi\) and the instantaneous generators are self-adjoint. Its backward Dynkin martingale has the same bracket expectation. Adding the two identities cancels both endpoint values and the time derivatives of f:

\[
-2\int_0^tL_uf_u(X_u)du
=M_t+\widehat M_S-\widehat M_{S-t}. \tag{14}
\]

Two applications of Doob's inequality and the bound
\(\sup_t|\widehat M_S-\widehat M_{S-t}|\le2\sup_t|\widehat M_t|\)
give (13). All inverses are finite matrices here. Smooth q makes f smooth at fixed N, so no unproved derivative-domain assertion is needed. The reversal in (14) is a mathematical proof, not a microscopic time-reversal actuator.

Apply (13) to \(v_t=q'(t)p\) and use (12). With \(q=\cos\Omega_Nt\),

\[
\mathbb E\sup_{t\le N^2T}
\left|\int_0^tq'(u)p_u du\right|^2
\le20C_N\Omega_N^2N^2T. \tag{15}
\]

After multiplying by the squared CLT scaling \(N^{-3}\), this is O(\(\Omega_N^2/N^2\)). Thus under (3), (8) and (15) show that the current and its martingale are uniformly close in probability at current-CLT scale.

## 6. Bracket convergence and the actual current path limit

The canonical activity has exact moments, for N>=4,

\[
\mathbb E_\pi A=\frac{2M(N-M)}{N-1},
\qquad
\operatorname{Var}_\pi(A)
=\frac{4M(N-M)(M-1)(N-M-1)}{(N-1)^2(N-2)}=O(N). \tag{16}
\]

They follow by counting one active bond, two adjacent active bonds and two disjoint active bonds. Because the visible marginal is canonical at every time, for every bounded deterministic weight g,

\[
\mathbb E\sup_{t\le T}\left|
N^{-3}\int_0^{N^2t}[A_u-\mathbb E_\pi A]g(u)du\right|
\le \frac{T\|g\|_\infty}{N}\sqrt{\operatorname{Var}_\pi(A)}\to0. \tag{17}
\]

Taking \(g=1-\alpha^2\cos^2(\Omega_Nu)\), equation (7) gives the bracket of \(N^{-3/2}\mathcal M(N^2t)\). Since

\[
N^{-2}\int_0^{N^2t}\cos^2(\Omega_Nu)du
=t/2+O((\Omega_NN^2)^{-1}),
\]

that bracket converges uniformly in probability to

\[
s\chi(m)(1-\alpha^2/2)t. \tag{18}
\]

Scaled martingale jumps are at most \((1+\alpha)N^{-3/2}\). The bracket is continuous and uniformly bounded on a fixed horizon. The ordinary martingale functional central limit theorem therefore applies. Equations (8) and (15) transfer its Brownian path limit to J, proving (4) in Skorokhod J1 topology with continuous limiting support.

For mean-rate SSEP, J itself is a martingale, with bracket \(c\int A\). The same calculation gives \(s\chi(m)t\). Thus the comparator and failure are at the same current normalization and physical observation clock.

## 7. Scope and the relation to root's rare-current obstruction

This construction changes an actual signed transport observable at its equilibrium fluctuation scale. It does not merely exploit sensitivity of the high-order parity function. The parity is an unobserved kinetic context used to create the effect; its value need not be measured or learned by the controller.

This unit proves a conserving-ring **functional current CLT failure** for fast common deterministic rotation, under the stated canonical initialization and odd-count subsequence. It does not identify the limiting action at speed N, derive the full crossover for \(\Omega_N/N\to r>0\), or claim a sharp universal frequency threshold. Root's independent common-Poisson argument provides an actual rare-current upper bound, which is stronger for disproving the universal action claim under that supplier.

The deterministic control schedule may be retained. Canonical initialization and the fresh native jump law remain genuine premises. This proof does not assert the same conditional equilibrium fluctuation statement after selecting arbitrary rare initial or future records. Preparing the canonical ensemble, maintaining the nonlocal coefficient family, rotating the phase while preserving the native model, and reading signed current all carry their actual resource costs.

## 8. Established machinery and inspected sources

The forward/backward energy method is established. L. Wu, *Forward-backward martingale decomposition and compactness results for additive functionals of stationary ergodic Markov processes*, AIHP 35 (1999), 121–141, [primary paper](https://www.numdam.org/article/AIHPB_1999__35_2_121_0.pdf), was read through its introduction and continuous-time decomposition/maximal estimate. Equation (13) is proved here for the finite, time-dependent common-invariant setting; no extension of Wu's theorem is assumed by citation alone.

The martingale FCLT is established, with historical primary reference R. Rebolledo, *Central limit theorems for local martingales*, 1980, [publisher record](https://link.springer.com/article/10.1007/BF00587353). Only that original paper's publisher metadata was accessible, not its full proof. The exact convenient theorem and its hypotheses were checked in W. Whitt's author-hosted proof exposition, *Proofs of the martingale FCLT*, Probability Surveys 4 (2007), Theorem 2.1(ii), [paper](https://www.columbia.edu/~ww2040/WWproofs2007pub.pdf), [DOI](https://doi.org/10.1214/07-PS122). The continuous predictable bracket and uniformly vanishing bounded jumps above meet those hypotheses.

The construction and combinatorial inverse-energy estimate are mathematical results for the stated native family. No novelty of martingale homogenization, no physical implementation of parity-coupled rates, and no apparatus measurement are claimed.
