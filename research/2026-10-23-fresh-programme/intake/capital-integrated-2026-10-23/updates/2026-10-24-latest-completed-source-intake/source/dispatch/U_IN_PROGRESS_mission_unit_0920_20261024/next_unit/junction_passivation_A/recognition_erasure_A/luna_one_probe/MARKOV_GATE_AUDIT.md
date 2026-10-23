# Recognition-erasure gate: minimal Markov audit

## Chosen graph and event definition

This is a single-binding-encounter, pseudo-first-order model. Rebinding after tag dissociation is omitted. Let \(E\) be the pre-admission template/RNA-tag complex, \(A\) the admitted but incomplete state with both the long DNA anchor and RNA recognition tag present, \(A_e\) the incomplete state after RNase-H has erased the tag while the DNA anchor remains, and \(C_t\) a completed product still held to template by its uncleaved recognition tag. The absorbing success state \(S\) is a completed product whose recognition tag has been cleaved; failures are early erasure/dissociation in \(E\), or loss of the productive DNA-anchor geometry before completion.

Transitions are
\[
E\xrightarrow{a}A,\quad E\xrightarrow{c_E}\text{early-erasure failure},\quad
E\xrightarrow{d_E}\text{dissociation failure};
\]
\[
A\xrightarrow{c_A}A_e,\quad A\xrightarrow{g}C_t,\quad
A\xrightarrow{d_A}\text{anchor-loss failure};
\]
\[
A_e\xrightarrow{g}S,\quad A_e\xrightarrow{d_A}\text{failure},\quad
C_t\xrightarrow{c_C}S,\quad C_t\xrightarrow{d_C}\text{uncleared-product outcome}.
\]
The \(C_t\) branch retains the path where forward completion occurs first: the recognition duplex holds the completed product/template complex until RNase-H clears it, but can itself dissociate first. We count that dissociation as an uncleared-product outcome; no rebinding is included. DNA-anchor detachment after entry to \(C_t\) does not undo completion or release the template because the recognition duplex still holds it. In this conservative graph, anchor loss before completion destroys the geometry needed for completion even if the RNA tag still physically binds.

## Exact eventual success probability

For an initial \(E\) encounter, admission wins the three-way race with probability
\[
P(E\to A)=\frac{a}{a+c_E+d_E}.
\]
From \(A\), cleavage before completion succeeds only if the DNA anchor survives the remaining completion race. If completion comes first, the product is retained by the recognition duplex and must be cleaved before that duplex dissociates. Thus, for unbounded observation time,
\[
\begin{aligned}
P(A\to S)
&=\frac{c_A}{c_A+g+d_A}\frac{g}{g+d_A}
 +\frac{g}{c_A+g+d_A}\frac{c_C}{c_C+d_C}\\
&=\frac{c_Ag/(g+d_A)+g c_C/(c_C+d_C)}{c_A+g+d_A}.
\end{aligned}
\]
Consequently the exact probability of correct admission followed eventually by erased completion in this graph is
\[
\boxed{P_{success}=\frac{a}{a+c_E+d_E}\,
\frac{c_Ag/(g+d_A)+g c_C/(c_C+d_C)}{c_A+g+d_A}}.
\]
The earlier cancellation of \(c_A\) required the idealized edge \(C_t\to S\) with no competing recognition dissociation. With \(c_A=c_C=c\) and \(d_C>0\), the post-completion route has probability \(c/(c+d_C)\), so total success tends to zero as \(c\to0\); conversely, making the same enzyme hazard large can increase premature loss through \(c_E\). High yield therefore requires admission selectivity and adequate post-completion tag residence/cleavage, as well as completion against anchor loss. If RNase-H cleavage is incomplete or fragments remain bound, the transitions to \(A_e\) or \(S\) are not instantaneous and this graph overestimates success.

For a target success \(1-\epsilon\), the exact condition is
\[
\frac{a}{a+c_E+d_E}\,
\frac{c_Ag/(g+d_A)+g c_C/(c_C+d_C)}{c_A+g+d_A}\ge1-\epsilon.
\]
A transparent sufficient allocation is to choose \(\epsilon_E,\epsilon_A\) with \(\epsilon_E+\epsilon_A-\epsilon_E\epsilon_A\le\epsilon\), and require the admission and post-admission factors respectively to be at least \(1-\epsilon_E\) and \(1-\epsilon_A\). The admission condition is
\[
a\ge\frac{1-\epsilon_E}{\epsilon_E}(c_E+d_E).
\]
For the post-admission condition use the displayed \(P(A\to S)\); it does not reduce to a single race when \(d_C>0\). Under a simplifying one-hazard assumption \(c_E=c_A=c_C=c\), high yield can require both \(a\gg c+d_E\) and \(c\gg d_C\), alongside sufficiently favorable completion versus anchor loss. A nonempty window depends on the actual rates and is not guaranteed by using the same bulk enzyme concentration.

Conditioned on reaching \(C_t\), the probability that cleavage occurs before recognition dissociation and by deadline \(t_r\) is
\[
\frac{c_C}{c_C+d_C}\left(1-e^{-(c_C+d_C)t_r}\right).
\]
A release target must meet this finite-deadline probability, not just a cleavage-only exponential. This is a throughput/release requirement in addition to eventual correctness.

## Scope of the rate model

The rates \(c_E,c_A,c_C\) are effective cleavage hazards at the stated enzyme concentration, not rates guaranteed equal merely because the bulk enzyme concentration is the same; hybrid geometry, accessibility, enzyme binding, and product-fragment release can differ by state. A mechanistic model would include enzyme-bound complexes and released RNA fragments explicitly. Premature cleavage in \(E\) creates an erased input and fragment waste; successful cleavage in \(A\) or \(C_t\) also produces fragments and temporarily occupies enzyme. RNase-H turnover, enzyme sequestration, incomplete-cleavage fragments, tag rebinding, and the adapter/lock waste balance are not priced by this graph. Evidence for a DNA-target reset in another system (including CPT) does not establish the same operation on this host. The result is exact only for the stated minimal graph, not a claim that its state transitions or rates are acquired for a compatible assembly platform.

## Retry graph with free-site return

The preceding single-encounter probability treats early cleavage or dissociation as failure. A distinct repeated-attempt graph shows why early cleavage alone need not make long chains fail exponentially when the site can be restored and fed again. Let \(F\) be a free template site, \(E\) a captured input, \(D\) a cut/fragment-held site, and \(A\) absorbing admission. Use constant positive rates
\[
F\xrightarrow{\kappa}E,\qquad
E\xrightarrow{a}A,\quad E\xrightarrow{c}D,\quad E\xrightarrow{d}F,
\qquad D\xrightarrow{\rho}F.
\]
Here return from \(D\) is an explicit idealized fragment-clearance/reset event; dissociation from \(E\) returns an unconsumed input. Put \(\Lambda=a+c+d\). The mean-time first-step equations are \(T_F=1/\kappa+T_E\), \(T_E=1/\Lambda+(dT_F+cT_D)/\Lambda\), and \(T_D=1/\rho+T_F\). They give the mean time to admission from \(F\):
\[
\boxed{T_F=\frac{\Lambda}{a\kappa}+\frac1a+\frac{c}{a\rho}}.
\]
The expected number of early-destroyed inputs before eventual admission is \((\Lambda/a)(c/\Lambda)=c/a\), and there is exactly one final admitted input; dissociated unconsumed attempts are excluded from this destroyed/consumed count. The number of visits to \(E\) is \(\Lambda/a\) in expectation, so capture and clearance delays remain resource costs even though admission occurs eventually.

For the admission-time Laplace transforms, \(\phi_F=\kappa\phi_E/(\kappa+s)\), \(\phi_E=(a+d\phi_F+c\phi_D)/(\Lambda+s)\), and \(\phi_D=\rho\phi_F/(\rho+s)\). Eliminating \(\phi_E,\phi_D\) gives
\[
\boxed{\phi_F(s)=\frac{\kappa a(\rho+s)}
{(\kappa+s)(a+c+d+s)(\rho+s)-\kappa d(\rho+s)-\kappa c\rho}}.
\]
It satisfies \(\phi_F(0)=1\), consistent with certain eventual admission for positive \(\kappa,a,\rho\) and finite competing rates. If an independent chain-front loss occurs at constant hazard \(h\) throughout one retry cycle, that cycle succeeds without loss with probability \(\phi_F(h)<1\) for \(h>0\); for \(N\) identical independent steps the no-loss factor is \(\phi_F(h)^N\). Thus retries remove early-cut-only exponential failure when \(h=0\), but do not remove exponential loss under a fixed positive independent front hazard. These conclusions are conditional on the graph: physical readmission, fragment clearance, finite-bath depletion, and the finite rates \(\kappa,a,c,d,\rho\) remain unknown.
