# Odd-parity lift of a single-reset renewal process

**Status (15 October 2026):** self-contained analytic construction and exact rational check, with **novelty unknown and probably limited by older generalized-detailed-balance work**. The construction is a precise boundary on what a two-label waiting-time law can establish when microscopic time-reversal parity is left unspecified. It is neither a claim of free physical operation nor a contradiction of the existing even-variable result.

## The exact operation

Take any finite irreducible continuous-time Markov generator \(Q\) on \(\{a\}\cup B\), with \(a\) the *only* state observed as \(A\) and every state of \(B\) observed as \(B\). Let its strictly positive stationary row vector be \(\pi=(\pi_a,\pi_B)\). Write

\[
Q=\begin{pmatrix}-\lambda&\lambda\alpha\\t&S\end{pmatrix},\qquad
\lambda>0,\quad\alpha\mathbf1=1,\quad t=-S\mathbf1.
\]

The visible process is an alternating renewal process: an \(A\) dwell is exponential with rate \(\lambda\); the density of the following complete \(B\) dwell is

\[
f_B(u)=\alpha e^{Su}t. \tag{1}
\]

At every return to the singleton \(a\), the strong Markov property resets the cycle. Irreducibility makes \(S\) transient, so (1) is a probability density with finite mean.

Let \(Q^\dagger\) be the stationary time reversal, \(Q^\dagger_{ij}=\pi_jQ_{ji}/\pi_i\) for \(i\ne j\), with the same diagonal as \(Q\). Introduce two copies, \(+\) running \(Q\) and \(-\) running \(Q^\dagger\). Add only the two equal-rate transitions

\[
(a,+)\xrightleftharpoons[\varepsilon]{\varepsilon}(a,-),\qquad\varepsilon>0.
\]

Observe \((a,\pm)\) as \(A\) and \((i,\pm)\), \(i\in B\), as \(B\). Treat the sign as odd under time reversal: \(\theta(i,+)=(i,-)\), \(\theta(i,-)=(i,+)\). The resulting \(2|Q|\)-state generator \(L\) is irreducible, exactly reproduces the **entire stationary visible path law** of \(Q\), and its stationary path law is invariant under \(x(u)\mapsto\theta x(T-u)\) for every \(T\). Thus its path-space relative entropy against this parity-reversed path law is exactly zero on every finite interval.

This is an all-dimension statement for the single-reset class. It does not require the \(B\) phase representation to be minimal, diagonalizable, or bidirectionally supported. It does require exact stationarity, a genuine singleton reset, the specified parity assignment, exact reverse rates, and positive \(\varepsilon\).

## Proof of exact dwell and path-law preservation

Put \(D=\operatorname{diag}(\pi_B)\). Stationarity gives \(\pi_Bt=\pi_a\lambda\). Directly from the definition of \(Q^\dagger\), its \(B\) killed block, normalized entrance row, and exit column are

\[
S^\dagger=D^{-1}S^{\mathsf T}D,\qquad
\alpha^\dagger=\frac{t^{\mathsf T}D}{\pi_a\lambda},\qquad
t^\dagger=\pi_a\lambda D^{-1}\alpha^{\mathsf T}. \tag{2}
\]

The reverse \(A\) exit rate is \(\lambda\), because the diagonals of \(Q\) and \(Q^\dagger\) coincide; \(\alpha^\dagger\mathbf1=1\) by stationarity. Similarity of the killed semigroups gives the identity, for **every** \(u\ge0\),

\[
\begin{aligned}
\alpha^\dagger e^{S^\dagger u}t^\dagger
&=t^{\mathsf T}D( D^{-1}e^{S^{\mathsf T}u}D )D^{-1}\alpha^{\mathsf T}\\
&=t^{\mathsf T}e^{S^{\mathsf T}u}\alpha^{\mathsf T}
=\alpha e^{Su}t.
\end{aligned}\tag{3}
\]

Thus a \(B\) excursion has the same complete-duration law in either orientation. While in either \(A\) state, the rate of a *visible* exit to \(B\) is \(\lambda\), independent of the sign, even though hidden sign flips occur at rate \(\varepsilon\). Conditional on the entire visible and hidden past at an entrance to \(A\), the next \(A\) duration is therefore \(\mathrm{Exp}(\lambda)\). The sign selected at the subsequent visible exit may depend on that duration, but (3) makes the conditional \(B\) duration distribution independent of that sign. Hence the pair of successive \(A,B\) durations has the same product law \(\mathrm{Exp}(\lambda)\otimes f_B\) conditional on every prior cycle. Induction gives the same iid cycle sequence as \(Q\). Its unique stationary time placement is determined by the cycle-length bias, so the stationary visible càdlàg path laws, not merely marginal waiting-time histograms, agree.

The stationary law of the lift is \(\rho_{i,+}=\rho_{i,-}=\pi_i/2\). Within each copy stationarity follows from \(\pi Q=\pi Q^\dagger=0\); the two reset flips balance. Irreducibility follows because each copy is irreducible and the reset flips connect them. For any within-copy edge, the defining identity of \(Q^\dagger\) yields

\[
\rho_xL_{xy}=\rho_{\theta y}L_{\theta y,\theta x}. \tag{4}
\]

For either reset flip, (4) holds directly. Also \(\rho_x=\rho_{\theta x}\) and \(L_{xx}=L_{\theta x,\theta x}\), including at \(a\), where both diagonals gain \(-\varepsilon\). Multiplying (4) along a finite jump path, with the holding-time factors and initial stationary mass, proves equality of the forward path density and its parity-reversed density. Therefore the parity path KL is \(0\) for every \(T\), including on edges that were one-way in \(Q\). This is a statement about a specified path involution. It does not assert that ordinary even-variable entropy production vanishes.

## Exact non-Markov example and executed check

For the ring family used in [Aznagulov's preprint, §8.5 and §8.8](https://arxiv.org/html/2609.14623), choose clockwise rate \(1\), counterclockwise rate \(q\in(0,1)\), and \(a=0\):

\[
Q_q=\begin{pmatrix}-(1+q)&1&q\\q&-(1+q)&1\\1&q&-(1+q)\end{pmatrix},\quad
\pi=(1/3,1/3,1/3).
\]

Writing \(s=1+q\), its \(B\) representation is \(\alpha=(1,q)/s\), \(S=\left(\begin{smallmatrix}-s&1\\q&-s\end{smallmatrix}\right)\), \(t=(q,1)^{\mathsf T}\). Direct matrix inversion gives

\[
\widehat f_B(z)=\frac{(2q/s)z+(1+q+q^2)}{z^2+2sz+(1+q+q^2)}. \tag{5}
\]

At \(q=1/20\), \(f_B(0)=2/21\) and \(f'_B(0)=341/400>0\). Let \(g(u)=\Pr\{\text{the entered }B\text{ dwell exceeds }u\}\). Then \(g'(0)=-2/21\), \(g''(0)=-341/400\), and for all sufficiently small \(h>0\),

\[
g(2h)-g(h)^2
=-\left(\frac{341}{400}+\frac4{441}\right)h^2+O(h^3)<0. \tag{6}
\]

Equation (6) is a concrete visible path event: after the process has survived \(h\) in \(B\), its chance of surviving another \(h\) is lower than it was on entering \(B\). A two-state time-homogeneous Markov process would have equality by exponential memorylessness. Both the original ring and the six-state parity lift generate the same strict inequality. Thus the lift preserves a genuinely non-Markov observation, not just a two-point statistic.

The file [verify_odd_lift.py](verify_odd_lift.py) uses Python Fraction arithmetic for \(q=1/20\), \(\varepsilon=1/7\). Its saved [output](verify_odd_lift.json) verifies row sums, stationarity, parity-paired holding rates and all 30 off-diagonal parity-balance identities, plus equality of the first nine \(B\)-density Taylor coefficients. These finite checks are reproducibility support; equations (2)–(4) are the proof for arbitrary finite dimension.

The original ring and the lifted model have the same **ordinary** entropy-production rate, \((1-q)\log(1/q)=(19/20)\log20\approx2.84594566\) at \(q=1/20\). The two half-weight branches each contribute half of the original cost, and the reset flips contribute none to ordinary edge cost. The lift's extra stationary microscopic jump activity is \(\varepsilon\pi_a=1/21\), in addition to the ring's \(s=21/20\). The flip rate can tend to zero, but the sign-mixing time then diverges; \(\varepsilon=0\) is a reducible stationary mixture and does not meet the theorem's irreducibility assumption.

## Comparator, prior art, and physical boundary

The strongest equally informed simple competitor is the original three-state ring itself: it exactly produces the whole renewal law with half the states and no parity-register control. The six-state lift changes the *definition of microscopic reversal*, not the visible task or the ordinary cost. A [3 October 2026 unrefereed candidate release](https://www.evidencepress.org/releases/hidden-dissipation-floor/) states an all-dimension positive ordinary/even-reversal lower bound \(V_\infty(P_{1/20})>0.017568198744\) and explicitly excludes odd-variable extensions. Our construction lies outside that reversal convention, so the bound and this exact zero parity-path KL can coexist. The earlier preprint states \(V_\infty(P_{1/20})=0\) only as a conjecture (§6, lines 239–242); the later candidate claims to refute it under its stated even-variable assumptions. Neither item is a laboratory measurement or an externally peer-reviewed validation of this lift.

The broad idea is substantially anticipated. [Barra, Clerc and Tirapegui (1997), *Detailed balance in non-equilibrium systems*](https://doi.org/10.1080/02681119708806236) says in its [author-uploaded abstract](https://www.researchgate.net/publication/245326839_Detailed_balance_in_non-equilibrium_systems) that a stationary Markov process can be put in generalized detailed balance by adding odd parameters. The full paper could not be retrieved here, so its exact construction and whether it contains the single-reset, irreducible, whole-observation-law specialization remain unverified. [Lee, Kwon and Park (2012), equations 3–9 and 19](https://arxiv.org/html/1209.0543) explicitly define parity-flipped path reversal and require both generalized detailed balance and parity-symmetric stationary distribution for equilibrium; (4) and \(\rho_x=\rho_{\theta x}\) satisfy those mathematical requirements. [Skinner and Dunkel (2021), pp. 1–3](https://math.mit.edu/~dunkel/Papers/2021SkDu_PRL.pdf) already use nonmonotone waiting-time densities as ordinary-reversal nonequilibrium evidence. The initial attempt here to derive a dimension-independent ordinary-reversal floor by additive symmetrization was independently reproduced but preempted by the October release's same construction and stronger certified bound. Its novelty is not claimed.

The additional sign must correspond to an actual microscopic odd variable for generalized reversal to have thermodynamic meaning. Naming a hidden bit “odd” is not a physical implementation. A physical realization would have to acquire or calibrate \(\pi\), synthesize the exact reversed rates \(Q^\dagger\), sustain two matched branch architectures, cause sign flips only at the \(A\) reset, and verify the parity of the hidden variable under genuine time reversal. Those preparation, sensing, control, and reliability costs are unmeasured here. A rate mismatch generically breaks (3) or (4). Without a reservoir-resolved local-detailed-balance model, zero parity path KL cannot be promoted to zero energy use or a working device. No experiment was performed.

**Decisive next test:** obtain the full 1997 paper and compare its construction line by line; then demand a concrete physical odd coordinate and reservoir-resolved transition model for the six-state example. If no physically admissible parity assignment realizes (4), the mathematical countermodel remains valid but does not weaken an experimentally grounded dissipation inference. If such an assignment exists, check whole-path observed dwell correlations and measured heat against the exact rates; any disagreement falsifies the proposed physical mapping.
