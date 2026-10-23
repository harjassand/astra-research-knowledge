# N33 continuation: smoothing affine permanence barriers into controlled stochastic capture

**Date:** 2026-10-21 (Australia/Brisbane)  
**Status:** Independent mathematical derivation and adversarial checks; new to this scoped Astra investigation. Conditional on the original N33 deterministic theorem/affine lemma, its existing strict-facet stochastic exit argument, and standard stopped counting-process martingale estimates. **Not** a Lean/kernel-checked proof, externally peer reviewed discovery, historical-priority certificate, simulation of the stochastic horizon, or physical demonstration.  
**Archive policy:** Add a new research record; do not change the authority/status of N33, N34, N50, N54, N142, N145, N173, N181 or any open gate.

## 0. Decision and main improvement

The N33 polytope and the controlled-jump martingale certificate already implied exponentially long **residence when initially buffered inside** a strict inward region. Earlier scoped notes further treated a six-reaction synthetic example and species-specific balanced migration. Their gap was stochastic **entrance from arbitrary positive compact initial ranges**. Ordinary finite-time density-dependent approximations (Kurtz) give an entrance proof, but a naive worst-case Grönwall constant in a large positive box yields a risk exponent too tiny for meaningful finite-volume estimates.

This note develops a more direct mechanism: **regularize N33's finite affine minimum by log-sum-exp, preserve strict projected inward drift for *near-active* faces, and use the resulting smooth observable as a stochastic submartingale until entrance.** This controls molecular entrance without shadowing any particular deterministic trajectory. Nested finite-scale positive polyhedral guards protect the process while the next scale is reached, and the existing N33 exponential escape certificate protects the final basin. The resulting theorem is universal and uniform over arbitrary **predictable, history-dependent rate paths**, although its synthesis/volume constants remain existential for a general N33 network.

### Main conditional theorem (uniform stochastic capture plus finite exponential residence)

Let \(R\) be a finite **ordinary-endotactic** reaction network with source and target complexes \(y_e,y'_e\in\mathbb N^d\), displacements \(\nu_e=y'_e-y_e\), and \(S=\operatorname{span}_{\mathbb R}\{\nu_e\}\). Fix \(P=(c+S)\cap\mathbb R_{>0}^d\), \(0<\kappa\le K<\infty\), and a compact initial range \(D_0\subset P\). For integer molecular volume \(V\), consider the elementary-reaction pure jump process on nonnegative integer counts \(Z^V\), with \(X^V=Z^V/V\), increments \(\nu_e/V\), and predictable intensities

\[
V k_e(t,\mathrm{past})\phi_{y_e}^V(X^V_{t-}),\qquad
\phi_y^V(x)=V^{-|y|}\prod_{i=1}^d(Vx_i)_{y_i},\quad
\kappa\le k_e\le K.
\]

Only lattice-compatible initial states with \(X^V(0)\in D_0\) and \(X^V(0)-c\in S\) are claimed. Arbitrarily correlated compound/simultaneous jumps, anticipative policies and non-molecular real kinetic exponents are **not** included.

**Theorem C1.** Conditional on N33's original all-endotactic common-absorber proof, there exist a **single** compact convex positive polytope \(Q\subset P\), a deadline \(T_*<\infty\), positive \(a,b,C\), and integer \(V_*\) such that for all \(V\ge V_*\) and every permitted initial count vector and predictable rate control,

\[
\boxed{\displaystyle
\mathbb P\big\{X^V(t)\in Q\ \text{for all }t\in[T_*,T_*+e^{aV}]\big\}
\ge 1-C(1+V)e^{-bV}.}
\tag{C1}
\]

The **same** \(Q,T_*,a,b,C,V_*\) work for every initial concentration in the given compact \(D_0\) and every rate history. The absorbing polytope \(Q\) can in fact be selected before \(D_0\), with the deadline and small-volume bounds depending on \(D_0\); see the proof. No positive recurrence, invariant measure, infinite-horizon stochastic permanence, efficient numerical compiler, fixed-volume certainty, or physical time unit is claimed. If \(S=\{0\}\), every jump is zero and (C1) is immediate whenever the lattice condition is nonempty.

**Mode extension.** The same theorem applies to arbitrary predictable convex mixtures or pure switching among finitely many ordinary-endotactic modes having **the same exact stoichiometric span**, with every active mode's underlying edge coefficients in a common positive box. The actual stochastic intensities are \(Vk_{j,e}\alpha_j\phi^V_{y_{j,e}}\), where \(\alpha_j\ge0,\sum_j\alpha_j=1\). Individual reaction intensities are permitted to vanish when a mode is off. The requisite deterministic pointwise inward drift is inherited from the original N33 common-span switching theorem. No dwell time is assumed.

## 1. Exact inherited mathematics and attribution

### 1.1 Reconstruction (read from original TeX, not just the card)

N33 original source: `updates/P/package/outputs/endotactic_permanence.tex`, preserved as [`web/pages/d-326696af15b5e02b.html`](https://github.com/harjassand/astra-research-knowledge/blob/main/web/pages/d-326696af15b5e02b.html), 1,437 lines, indexed original SHA-256 `bbecea61cd373a787920bb4484494114b7d616d5f20ee096cae3831487707e9c` (hash from N33 dossier). Specific proof spans read and reused: definition/main theorem 66–140; family149 finite-affine reconstruction 142–395; sign preservation and weighted essential-source inward drift 396–518; compact plateau, neutral-slopes and a.e. minimum chain rule 519–677; global nonnested scale absorption 681–737; common-span switching 760–807; scalar compartment invariance 858–918; conditional molecular controlled finite-volume exit bound 1159–1310. Internal review sources `d-3bbc07797edc024a`, `d-def05360aaff95aa`, `d-bea170628b69f941` were previously read in full. Later dossiers N142/N145 keep the conditional one-scale Lean port distinct from global composition; N173 handles a different uniform log-valuation kinetic premise; N54 scalar spatial coupling is conditional on N33; N50 rational global recognizer remains non-efficient/conditional; N181 rejects deterministic permanence → stochastic positive recurrence.

N33 gives for one fixed finite family (slopes independent of the small scale \(h\)):

\[
F_h(x)=\min_{\lambda\in\Lambda}(r_\lambda\cdot x+b_\lambda(h)),\qquad
M_h=F_h(c),\qquad K_h=\{x\in P:F_h(x)=M_h\}.
\]

For sufficiently small \(h\), \(K_h\) is nonempty compact convex, contained in the interior of \(B_{\sqrt h}=[\sqrt h,h^{-1/2}]^d\). The family has a **constant, zero-slope active label** at \(c\), hence \(F_h\le M_h\) globally. If \(x\in P\cap B_h\) and \(r_\lambda\) is active at \(x\), then

\[
 r_\lambda\cdot f(x,k)\ge0;\qquad
r_\lambda\notin S^\perp\implies
r_\lambda\cdot f(x,k)\ge\delta_h:=\kappa Hh^M>0,
\]

uniformly over the supplied rate box. A label whose slope is in \(S^\perp\) is constant along \(P\), takes value at least \(M_h\), and therefore cannot be active outside \(K_h\). The strict drift proof uses *essential reaction sources*, **not** all vertices; tangent reactions are allowed. `E(r)` can be discontinuous and have zero global infimum; the family is fixed before extracting \(H>0\) and the small-scale cutoff. Offsets, slopes and effective \(h\) have no established practical bit bounds.

### 1.2 Literature and priority comparison

The finite-affine selection, compact polyhedral plateau and dyadic scale iteration are attributed to OpenAI family149 (pinned 5 October 2026 source commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`). N33's 7 October manuscript substitutes a weighted lowest-essential-source reaction comparison, handling arbitrary ordinary endotactic diagrams and measurable bounded rates. Comparable later work: Michael Mislan, *Uniform permanence of endotactic reaction networks with measurable rates*, Palomar 9 October 2026, registered source [`mmislan/palomar-endotactic-permanence`](https://github.com/mmislan/palomar-endotactic-permanence), pinned `c72c945264565397ecc3eee779e6bd5f3f3a061d`. Its Challenge/Solution declarations independently report a kernel-checked all-dimensional signed-real-complex theorem and explicitly credit OpenAI affine machinery. Dates/close mathematical correspondence **do not** prove influence, personal priority, or independent correctness of our new result.

Primary foundations/comparators: Craciun–Nazarov–Pantea (2013), *Persistence and permanence of mass-action and power-law dynamical systems*, DOI `10.1137/100812355` (two-species variable-rate endotactic result); Gopalkrishnan–Miller–Shiu (2014), *A geometric approach to the global attractor conjecture*, DOI `10.1137/130928170` (strongly endotactic general result and essential-source definition); Johnston–Pantea–Donnell arXiv:1412.4662 (endotactic conjecture); Craciun–Deshpande (2020), DOI `10.1137/19M1269312` (toric differential inclusions); C. Xu (2026), DOI `10.1007/s00285-026-02378-2` (first-order subclass). For stochastic links: T. Kurtz (1978), *Strong approximation theorems for density dependent Markov chains*, `Stochastic Processes and their Applications 6(3), 223–240`; Agazzi–Dembo–Eckmann (2018), *Large deviations theory for Markov jump models of chemical reaction networks*, DOI `10.1214/17-AAP1344`; A. Prodhomme (2023), *Strong Gaussian approximation of metastable density-dependent Markov chains*, arXiv:2010.06861; Anderson–Kim (2018) and Wiuf–Xu (2020) on additional hypotheses for stochastic recurrence. None of these sources was found in the present targeted search to state precisely (C1) with arbitrary history-dependent controls, N33 all-endotactic hypothesis and class-common multiscale absorption. **This is not a complete novelty/priority clearance.** Log-sum-exp smoothing, Foster drift and martingale concentration are themselves established tools.

## 2. Geometric ingredient: buffered N33 plateaux

Fix a sufficiently small N33 scale \(h\). On \(P=c+S\) define, for \(\rho>0\),

\[
Q_{h,\rho}=\{x\in c+S:F_h(x)\ge M_h-\rho\}
  =\bigcap_\lambda\{x\in c+S:L_{\lambda,h}(x)\ge M_h-\rho\}.
\tag{2.1}
\]

**Lemma 2.1 (strict nested buffers).** For every small fixed \(h\) one can choose \(\rho_h>0\) such that

\[
K_h\subset \operatorname{relint}Q_{h,\rho_h}
\subset Q_{h,\rho_h}
\subset\operatorname{relint}Q_{h,2\rho_h}
\subset Q_{h,2\rho_h}
\subset\operatorname{int}B_{\sqrt h}.
\tag{2.2}
\]

The two buffered polyhedra are compact, positive and convex. Every proper relative facet of \(Q_{h,2\rho_h}\) has strictly inward deterministic projected drift uniformly over all admissible rate controls. In fact each original defining affine inequality has at least \(\rho_h\) slack at points of the inner polytope \(Q_{h,\rho_h}\), so the proper-facet buffers are uniform, even when the affine representation has redundant constraints.

*Proof.* Original \(K_h\) is compact and contained strictly inside the inner concentration box. If arbitrarily small outward perturbations \(Q_{h,\rho_n}\), \(\rho_n\downarrow0\), were unbounded, pick \(x_n\in Q_{h,\rho_n}\), \(\|x_n\|\to\infty\), normalize \(v_n=(x_n-c)/\|x_n-c\|\), and extract a unit direction \(v\in S\) satisfying \(r_\lambda\cdot v\ge0\) for every label. Then \(c+tv\in K_h\) for every \(t\ge0\), contradicting compactness. Thus sufficiently small expanded sets are uniformly bounded. If points of a sequence of such sets escaped \(\operatorname{int}B_{\sqrt h}\), compactness would produce a point of \(K_h\) outside that open box, contradiction. Each \(x\in K_h\) satisfies all defining inequalities with slack \(\rho_h\) at level \(M_h-\rho_h\); similarly points of the inner set have slack \(\rho_h\) in the outer set. At a proper relative facet of the outer set, some label is minimizing with value \(M_h-2\rho_h\). Any label with \(r_\lambda\in S^\perp\) is constant on \(c+S\) and takes value \(L_\lambda(c)\ge M_h\), so it cannot be active on this boundary. Its supporting active slope is nonneutral. N33 gives projected drift \(\ge\delta_h>0\); finite compact facets and continuity extend the strict inequality to positive collars. The empty/nonproper facets are discarded. ∎

The lemma does **not** require the original successive N33 plateaux to be nested. The small buffer \(\rho_h\) is selected separately at each scale. A universal bound on \(\rho_h\) or polytope description length is not derived.

## 3. New mathematical principle: finite-affine softmin becomes a positive stochastic generator

For the same scale and a parameter \(\beta>0\), put

\[
\Psi_{h,\beta}(x)=-\beta^{-1}\log\sum_{\lambda\in\Lambda}
\exp[-\beta(r_\lambda\cdot x+b_\lambda(h))].
\tag{3.1}
\]

This function is smooth on **all** \(\mathbb R^d\), concave and globally \(R\)-Lipschitz, \(R=\max_\lambda\|r_\lambda\|_2\). Let \(n_\Lambda=|\Lambda|\). Then

\[
F_h-\frac{\log n_\Lambda}{\beta}\le\Psi_{h,\beta}\le F_h\le M_h,
\quad \nabla\Psi=\sum_\lambda p_\lambda r_\lambda,
\quad \nabla^2\Psi=-\beta\operatorname{Cov}_{p}(r_\lambda),
\quad\|\nabla^2\Psi\|_{\rm op}\le\beta R^2.
\tag{3.2}
\]

**Lemma 3.1 (uniform near-active drift).** Fix \(h\) and \(0<\rho<2\rho_h\). There exist \(\eta\in(0,\rho)\), \(\beta<\infty\), and \(\zeta_h>0\) such that for all \(x\in P\cap B_h\) with \(F_h(x)<M_h-\rho\), every admissible rate vector, and its mass-action field \(f\),

\[
\nabla\Psi_{h,\beta}(x)\cdot f(x,k)\ge\zeta_h>0.
\tag{3.3}
\]

The constants can be chosen independently of the rate history, including in the common-span arbitrary-switching setting.

*Proof.* Every active nonneutral \(r_\lambda\) satisfies \(r_\lambda\cdot f\ge\delta_h\) on the compact \(B_h\cap(c+S)\) for the compact rate box; a neutral label has projection exactly zero. Finiteness and continuity imply that some \(\eta>0\) makes \(r_\lambda\cdot f\ge\delta_h/2\) whenever its gap \(L_{\lambda,h}(x)-F_h(x)\le\eta\) and \(r_\lambda\notin S^\perp\). Indeed, a sequence of near-active counterexamples with gaps tending to zero would have one fixed label and convergent states/rates producing a counterexample at an actually active label. Choose \(\eta<\rho\). At a point with \(F_h(x)<M_h-\rho\), each neutral label has gap \(\ge\rho\), so **every** \(\eta\)-near-active label is nonneutral. Let \(G_h=\max_{\lambda,x,k}|r_\lambda\cdot f(x,k)|<\infty\) on this compact domain. In the weights \(p_\lambda\) of (3.2), labels with gap \(>\eta\) have total weight at most \(n_\Lambda e^{-\beta\eta}\), because the denominator includes a minimizing label. Fix \(\beta\) so that \(n_\Lambda e^{-\beta\eta}\le\delta_h/[4(\delta_h+G_h)]\). The good labels contribute at least \(\delta_h/2\) times their combined weight; the bad ones contribute at worst \(-G_h\) times theirs. Hence the total exceeds \(\delta_h/4\). Take \(\zeta_h=\delta_h/4\). The argument is pointwise, so predictable time dependence adds no problem. ∎

**Lemma 3.2 (finite-volume stochastic generator).** For all sufficiently large \(V\), the molecular generator of \(\Psi=\Psi_{h,\beta}\) satisfies, uniformly over all predictable rate histories,

\[
\mathcal L_t^V\Psi(x)\ge\delta_h/8>0
\quad\text{when }x\in P\cap B_h,\ F_h(x)<M_h-\rho.
\tag{3.4}
\]

*Proof.* On the positive box \(B_h\), let \(U_i=h^{-1}\) and use the finite factorial estimate from N33's appendix, \(0\le x^{y_e}-\phi_{y_e}^V(x)\le E_{y_e}(U)/V\). The stopped drift difference has norm \(\le A_h/V\), with \(A_h\) depending on the finite network, upper rates, sources and B_h. Taylor's formula along every jump \(\nu_e/V\) and the global Hessian bound from (3.2) give a second-order generator error bounded by \(\beta R^2\sum_e K U^{y_e}\|\nu_e\|_2^2/(2V)\). Thus

\[
|\mathcal L_t^V\Psi(x)-\nabla\Psi(x)\cdot f(x,k(t))|
\le \frac{C_h(\beta)}{V}
\tag{3.5}
\]

uniformly on the box, including the jump that first leaves it (because \(\Psi\) is globally defined). Choose \(V\ge 8C_h(\beta)/\delta_h\) and use Lemma 3.1. A convex mixture over finitely many same-span modes obeys the same bounds with maxima over the modes. ∎

**Why smoothing matters.** The original \(F_h=\min L_\lambda\) is nonsmooth at tied facets. Applying a stochastic jump generator directly can produce an uncharged loss when a small jump changes the minimizing label. Smoothing moves that loss into an explicit Hessian term \(O(\beta/V)\) while preserving strict active-slope drift through the finite near-active estimate. This is the critical new-to-Astra mathematical bridge; log-sum-exp smoothing itself is classical.

## 4. Stochastic multiscale entrance proof of Theorem C1

Fix the original N33 affine slope family and the positive class representative \(c\). Choose a final class scale \(h_P\). From any supplied compact \(D_0\), choose a sufficiently tiny \(h_0\le h_P\) so that \(D_0\subset K_{h_0}\). This uses the original N33 observation that when \(\|\log x/\log h_0\|_\infty<H\), all active slopes are zero; the compact-range bound makes this uniform in \(x\in D_0\). Thus the initial molecular concentrations lie **strictly inside** a buffered positive polytope \(O_0=Q_{h_0,2\rho_0}\), with all proper affine facet gaps at least \(2\rho_0\).

Take the finite dyadic sequence from N33:
\(h_{j+1}=\min(\sqrt{h_j},h_P)\), ending at \(h_N=h_P\). For every scale choose the nested **inner target** \(I_j=Q_{h_j,\rho_j}\) and **outer guard** \(O_j=Q_{h_j,2\rho_j}\) from Lemma 2.1, ensuring \(O_j\subset\operatorname{int} B_{\sqrt{h_j}}\subset B_{h_{j+1}}\). The \(I_j\) need not be nested between scales, and a nested chain is **not** presumed.

Suppose \(X^V\) starts a stage at an arbitrary stopping time \(s\) with \(X^V(s)\in I_j\) (at \(j=0\), one may start in \(K_{h_0}\)). Before exiting \(O_j\), it lies inside \(B_{h_{j+1}}\), so Lemmas 3.1–3.2 applied with \(h=h_{j+1}\), \(\rho=\rho_{j+1}\) give a smooth observable \(\Psi_{j+1}\) with generator at least \(d_{j+1}=\delta_{h_{j+1}}/8>0\) until the chain hits \(I_{j+1}\). Let

\[
A_j=M_{h_{j+1}}-\min_{x\in O_j}\Psi_{j+1}(x)\ge0,
\quad T_j=1+\frac{2A_j}{d_{j+1}}.
\tag{4.1}
\]

Because \(O_j\) is compact, \(A_j\) is finite. Stop at the first entrance into \(I_{j+1}\) or exit from \(O_j\). The compensated \(\Psi_{j+1}\) has martingale jumps bounded by \(J_j/V\) and predictable quadratic variation at most \(\mathcal B_j t/V\), for finite constants independent of future rate controls. If neither stopping event occurs before \(s+T_j\), then \(\Psi\le M_{h_{j+1}}\) and positive generator drift gives

\[
M_{s+T_j}\le A_j-d_{j+1}T_j\le-\frac12d_{j+1}T_j.
\]

The one-sided Freedman/Bernstein inequality for bounded-jump local martingales yields

\[
\mathbb P\{\text{no entry by }s+T_j,\ \text{no guard exit}\mid\mathcal F_s\}
\le\exp\left[-V\frac{d_{j+1}^2 T_j}{8(\mathcal B_j+J_jd_{j+1}/6)}\right].
\tag{4.2}
\]

Independently, the **outer guard** \(O_j\) has proper facets with uniform strict inward collars (Lemma 2.1). Starting in \(I_j\), their facet gaps are at least \(\rho_j>0\). N33's original molecular controlled-exit theorem therefore gives

\[
\mathbb P\{\tau_{O_j}\le s+T_j\mid\mathcal F_s\}
\le m_j e^{-\theta_j\rho_j V}+2m_j V\Lambda_j T_j e^{-c_jV},
\tag{4.3}
\]

with \(m_j<\infty,\theta_j,c_j,\Lambda_j>0\). For the starting stage \(D_0\subset K_{h_0}\), the initial buffer is even \(2\rho_0\). The estimate remains valid when \(s\) is a stopping time and future rates depend on the entire observed past, because the counting-process compensators and all drift bounds are conditional and predictable. The stopped process is nonexplosive on each guard; failure events include early escape or explosion beyond the protected domain.

There are finitely many stages. Combining (4.2)–(4.3) by conditional union bounds yields constants \(T_*=\sum_{j=0}^{N-1}T_j\), \(b_0,C_0,V_0>0\) such that every permitted chain hits the **last inner buffer** \(I_N\) by \(T_*\), without any previous guard escape, except on an event of probability at most \(C_0(1+V)e^{-b_0V}\). All constants are independent of the rate path and initial point in \(D_0\). Starting at the random final-entry time \(s_N\le T_*\), the guard \(O_N\) has at least \(\rho_N\) gap at all its facets. Apply the same conditional N33 exit bound to \(O_N\) over duration \(T_*+\exp(c_N V/2)\). Combining it with the preceding failure event proves (C1) with \(Q=O_N\) and \(a=c_N/2\), after reducing \(b>0\) if necessary. \(Q\) depends only on the diagram, rate box and positive class, *not* on \(D_0\). **QED, conditional on the cited N33 and martingale ingredients.**

### Source assumptions and limits of (C1)

- **Positive compact initial range:** removing compactness makes a uniform deadline false even for \(0\rightleftarrows A\) started at arbitrarily large concentration (entry delay grows with \(\log x_0\)).
- **Full positive rate box per ordinary-endotactic mode:** dropping a uniform inflow lower bound permits decay to zero; turning modes on/off arbitrarily is allowed only within the separate common-span switching structure which retains the inward margin.
- **Finite molecular jumps, integer complexes, predictable controls:** essential for the generator, factorial discrepancy and Freedman bounds. An arbitrary noisy diffusion or an anticipative controller is not covered.
- **No stochastic stationary inference:** finite \(e^{aV}\) safety can coexist with eventual extinction, transience, null recurrence or explosion outside the safe region. The counterexamples tracked in Astra N181 and stochastic CRN literature remain relevant.
- **No efficient compiler:** \(h_0\), \(|\Lambda|\), \(\eta\), \(\beta\), \(\rho_j\), \(V_*\), \(T_*\), \(a\), \(b\) exist but may be enormous or ineffective from a finite input unless the existing affine source is made constructive.

## 5. Fully explicit one-species falsification test, no dependence on hidden affine data

Consider the integer mass-action reactions \(0\to A\) and \(A\to0\), each with *arbitrary predictable* molecular rate in \([1,2]\). At volume \(V\), the count process has concentration \(X=Z/V\) with individual upward jumps \(+1/V\) at rate \(Vk_+(t,\mathrm{past})\) and downward jumps \(-1/V\) at rate \(Vk_-(t,\mathrm{past})X\). For every integer \(V\ge1200\) with initial \(X(0)\in[1/10,4]\cap V^{-1}\mathbb N\), let

\[
G=[1/5,61/20],\quad H=[1/16,5],\quad \tau_G=\inf\{t\ge0:X(t)\in G\}.
\]

**Proposition C2 (all controls, explicit uniform entrance).**

\[
\boxed{\displaystyle
\mathbb P\{\tau_G>8\}
\le e^{-3V/578}+2e^{-3V/320}+64V e^{-V/256}.}
\tag{5.1}
\]

This is a bound on **first entrance**, not on occupancy at time 8 without an additional residence argument. At \(V=5000\), its right-hand side is approximately \(1.054\times10^{-3}\); at \(V=10000\) it is \(6.9431\times10^{-12}\). Both are synthetic time units, not measured molecular rates.

*Complete proof.* Define the three-affine envelope and its regularization

\[
F(x)=\min\{0,x-1/4,3-x\},\quad
\Psi(x)=-\frac1{20}\log(1+e^{-20(x-1/4)}+e^{-20(3-x)}).
\]

Put \(A=e^{-20(x-1/4)},B=e^{-20(3-x)}\); then \(\Psi'=(A-B)/(1+A+B)\) and \(-20\le\Psi''\le0\), since the active slopes are \(\{-1,0,1\}\) and \(|\Psi''|=20\operatorname{Var}(r)\le20\). If \(x\le1/5\), then \(A\ge e>8/3\) and \(B\le e^{-56}<1/100\). Therefore

\[
\Psi'(x)\ge\frac{8/3-1/100}{1+8/3+1/100}
=\frac{797}{1103}>\frac7{10}.
\]

Likewise, if \(x\ge61/20\), then \(\Psi'(x)\le-7/10\). For the deterministic drift \(f=k_+-k_-x\), below \(G\) we have \(f\ge1-2/5=3/5\), and above \(G\) we have \(f\le2-61/20=-21/20\). Consequently \(\Psi'f\ge2/5\) everywhere in \(H\setminus G\), uniformly over the entire rate box. The scalar exponential comparisons above use rational series bounds: \(e>8/3\), \(e^5>100\), hence \(e^{-56}<1/100\).

The molecular rate total within \(H\) is at most \(12V\), and every jump has size \(1/V\). Taylor's theorem and \(|\Psi''|\le20\) show that the difference between \(\mathcal L^V\Psi\) and \(\Psi'f\) is at most \(120/V\), **without any factorial correction** (all sources have degree 0 or 1). Thus, for \(V\ge1200\),

\[
\mathcal L_t^V\Psi(x)\ge3/10
\qquad(x\in H\setminus G).
\tag{5.2}
\]

Also \(\Psi\le0\), and for \(x\in[1/10,4]\), \(F(x)\ge-1\), hence \(\Psi(x)\ge-1-(\log3)/20>-11/10\). Stop at \(\tau_G\wedge\tau_H\), where \(\tau_H\) denotes first exit from \(H\). Until then \(\Psi\) has martingale jumps at most \(1/V\) and predictable quadratic variation at most \(12t/V\). If neither stopping event occurs during the first 8 units, \(\Psi(X_8)\le0\) while integrated generator drift is at least \(8(3/10)=12/5\). The stopped martingale is therefore at most \(-1\). A one-sided bounded-jump Freedman inequality yields

\[
\mathbb P\{\tau_G>8,\tau_H>8\}\le
\exp\left[-\frac{V}{2(96+1/3)}\right]=e^{-3V/578}.
\]

For the exit guard \(H\), apply the established stopped exponential-boundary test to \(g_L=x-1/16,g_U=5-x\) with \(\theta=1/4\), left/right collars \(1/64,1/4\), and \(e^{1/4}\le4/3\). On the left collar, inward immigration dominates outward death by margin \(1-(4/3)2(5/64)=19/24>0\). On the right collar, inward death dominates outward immigration by margin \(19/4-(4/3)2=25/12>0\). Total scaled jump activity is at most 12. Each exponential face test has off-collar positive generator at most \(4V e^{-V/256}\), and the two tests initially sum to at most \(2e^{-3V/320}\). At the first exit one face test exceeds 1. Thus

\[
\mathbb P\{\tau_H\le8\}\le 2e^{-3V/320}+64V e^{-V/256}.
\]

Union with the non-entrance/no-exit event establishes (5.1), including all corners, feedback controls and finite jump overshoots. ∎

**Buffered exponential residence, also explicit.** On hitting \(G\), the gaps to \(H\)'s faces are at least \(11/80\) and \(39/20\), respectively. Restarting the same exponential guard at the random time \(\tau_G\le8\), for every \(V\ge1200\) and \(\mathcal T=\exp(V/1024)\),

\[
\mathbb P\{X(t)\in H\ \forall t\in[8,8+\mathcal T]\}
\ge 1-\left[e^{-3V/578}+2e^{-3V/320}+64Ve^{-V/256}
+2e^{-11V/320}+8V(8+e^{V/1024})e^{-V/256}\right].
\tag{5.3}
\]

At \(V=10000\), this yields a risk upper bound \(1.514\times10^{-8}\) over \(\mathcal T\approx17424\) nondimensional time units after the capture deadline. The bounds can be loose, and no stationary limit is asserted.

## 6. Independent deterministic test on the three-species synthetic fixture

To test whether the claimed entrance mechanism is substantive beyond initial safety, independently derive a class-uniform **deterministic** staging bound for the six-reaction model of Mislan, not a new network attributed to Astra:

\[
\dot a=c(k_1-k_2a^2),\quad
\dot b=ab(k_3-k_4b^2),\quad
\dot c=bc(k_5-k_6c^2),\quad k_i(t)\in[1/2,2].
\]

Every positive trajectory initially in \([1/10,10]^3\) stays there by scalar inward face signs. Let \(\sigma_a=\int_0^t c(s)ds\); then \(\sigma_a\ge t/10\) and the exact worst-case Riccati comparison bounds \(a\) between \(\tfrac12\tanh(\sigma_a+\operatorname{atanh}(1/5))\) and \(2\coth(\sigma_a+\operatorname{atanh}(1/5))\). The rational exponential inequality \(e^{13/5}>38/3\) proves \(9/20\le a(t)\le9/4\) for all \(t\ge13\). For \(u=b,c\) the transform \(z=u^{-2}\) obeys, in its operational clock \(\sigma\),

\[
\tfrac14-\tfrac{6}{25}e^{-4\sigma}
\le z\le4+96e^{-\sigma}.
\]

The inequality \(e^5>1944/19\) ensures \(9/20\le u\le9/4\) after an accumulated operational clock of 5. After time 13 the \(b\)-clock accumulates at least \((9/20)12=27/5>5\) over the next 12 units, hence \(b\in[9/20,9/4]\) for all \(t\ge25\). Repeating for \(c\) shows

\[
(a(t),b(t),c(t))\in[9/20,9/4]^3\quad\text{for all }t\ge37
\tag{6.1}
\]

uniformly over all measurable histories. The inner box has concentration gap at least \(1/20\) to the previously certified stochastic guard \([2/5,5/2]^3\). This supplies an independent concrete ODE entry test and shows what the general stochastic theorem needs to turn into an end-to-end finite-volume bound. A naïve whole-box Grönwall plus Freedman comparison yields a terribly small exponential confidence constant owing to high polynomial degrees and long clock stages. The softmin proof avoids relying on that worst-case trajectory-tracking exponent, **but an explicit optimized finite-V numerical constant for the full 3D capture process has not been acquired.** This remains a meaningful algorithmic gate, rather than a completed applied capability.

## 7. Adversarial validation, falsifiers and resource audit

1. **Tied and almost-active slopes:** The central danger is assuming drift positivity for labels that are inactive but nearly tied. Lemma 3.1 charges a *uniform near-active band* via compactness of a finite already-fixed family and compact rates; only after that is softmin \(\beta\) chosen. Reversing the order (softening an h-dependent or infinite uncontrolled family) invalidates the argument. The \(O(\beta/V)\) generator correction is essential.
2. **Neutral directions and different stoichiometric spans:** Neutral labels are excluded only **outside** an expanded plateau; this is why the stochastic theorem claims entrance to \(I_h\) rather than exact \(K_h\). Arbitrary switching among modes with different spans cannot simply use the main theorem: staying forever in a mode that leaves another component fixed defeats union-class absorption. A separate pointwise directional-coverage condition (earlier scoped result B) would be needed.
3. **Absorption is not stochastic recurrence:** The original N33 deterministic theorem plus exponential residence does not imply positive recurrence at fixed finite volume. Open networks may be transient or null recurrent, as shown by Astra N181; the preceding results are stopped finite-horizon statements.
4. **No unconditional infinite-dimensional spatial transfer:** The earlier scoped S3 two-site oblique-facet counterexample shows unequal species diffusion need not preserve an arbitrary N33 polytope. Spatial extension needs compatible facet normals, a bounded transport budget, or explicit quantitative domination.
5. **Non-effective acquisition:** \(\beta\) and \(V_*\) may be huge and derived from an existential compactness construction; no polynomial-time compiler, molecule-number budget, energy cost, or biochemical input data is obtained.
6. **Falsifier for the one-species test:** A legal count \(x\in[1/16,5]\setminus[1/5,61/20]\), \(V\ge1200\), and rates \(k_+,k_-\in[1,2]\) with \(\mathcal L^V\Psi(x)<3/10\) would invalidate (5.2). The exact inequalities rule this out analytically; the standard-library script also scans rate-box corners on the \(V=1200\) and \(V=10000\) count lattices, without using those finite scans as the proof.
7. **Historical originality remains unresolved:** Strong approximation, log-sum-exp smoothing, Foster drift and exponential-martingale escape are established; the scoped theorem's distinctive interface is N33's non-effective all-endotactic finite-affine source, positive-rate robust near-active normals, multiscale *stochastic* capture, and arbitrary history-dependent admissible controls. A deeper primary-literature priority investigation would be necessary before any publication as new research.

## 8. Reproduction and precise continuation

Run `python3 verify_softmin_capture.py` (standard library only) from this directory. `softmin_reproduction.json` records exact Fraction inequality checks, the controlled one-species hitting-time and residence bounds, the rational 3D clock inequalities, and **deterministic adversarial scans** for the minimum softmin generator over all four extreme rate pairs at thousands of count states. The scans are not Monte Carlo and do not prove the full theorem. No general Lean kernel check or independent replay of N33's source proof was performed this session; earlier audits and later registered comparator remain separately attributed.

**Next highest-value mathematical step:** independently formalize Lemma 3.1 (strict near-active band), Lemma 3.2 (finite-volume generator discrepancy), and the stopping-time conditional union argument, with particular emphasis on rates driven by the same stochastic history. Then attempt an **effective rational/interval-certified higher-dimensional softmin barrier** for a truly non-weakly-reversible network. The threshold is not more toy probability digits: success requires acquiring all slopes, offsets, \(h_j,\beta_j,\rho_j,V_*\), and a nontrivial confidence exponent at controlled bit cost. Next, demand an experimentally sourced integer-complex chemical/biological model with credible positive rate lower bounds, molecule numbers, feed/energy and physical timescale. If the effective/physical gates fail, retain C1 as a conditional mathematical theorem and stop promoting it as a technological opportunity.

**Checkpoint identifiers and preservation:** Full source anchors/hashes above. New append-only artifacts `SOFTMIN_STOCHASTIC_CAPTURE_REPORT.md`, `verify_softmin_capture.py`, `softmin_reproduction.json`, and `CHECKPOINT_SOFTMIN.md`. Earlier `REPORT.md`, `CHECKPOINT.md`, `SPATIAL_STOCHASTIC_EXTENSION.md`, and their evidence scripts remain unchanged. No old status record, proof, review, or gate was overwritten.