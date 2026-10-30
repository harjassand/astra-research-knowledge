# Physical energy records can certify an adaptively learned inverse

30 October 2026. Root construction following the cumulative-energy theorem. This is a new proof scope, not covered by the first receiving review of `PASSIVE_PHYSICAL_LEARNING_WITHOUT_RELAXATION.md`. Existing proofs, reviews and numerical records are retained.

## 1. The additional consequence

The first theorem supplies an unbiased physical gradient and an expected convergence rate without a hidden relaxation time. A remaining operational question is whether the same experiments can tell the user when the learned answer is accurate. A population expectation or a separately assumed transmission-matrix calibration is insufficient for that task.

For the fixed quadratic inverse problem below, the recorded experiments themselves supply a simultaneous confidence bound on the optimum distance. The learner may stop when this bound is small. The answer and stopping time can both depend on the entire acquired record. No independent validation specimen, hidden reset, stationary hidden distribution or qualification against every future intervention is needed.

Fresh chronological signs produce conditionally symmetric martingale increments even though the source remembers earlier experiments. A quadratic task has an affine gradient, so the weighted average of the true gradients is exactly the gradient at the weighted average of the attempted inputs, including adaptive inputs. The physical energy record bounds the martingale's squared increments. Passivity then proves that the confidence radius shrinks during continued use.

The probability method and numerical optimizer are ordinary machinery. Any conventional controller with the same actual operations may use them. The candidate physical-learning principle is the combination of causal modulation, observed energy and task-specific algebra. No priority or practical speedup is asserted.

## 2. Actual source and task

Retain the complete source premises of the first theorem. In calibrated real finite-waveform Hilbert spaces, a fixed unknown contraction A has chronological calls

\[
y_i=\sigma_i A u_i+\beta_i,\quad r_i=\sigma_i y_i-b,
\quad z_i=\kappa\tau_i A^*r_i+\chi_i,
\qquad0<\kappa<1.                                    \tag{1}
\]

Sigma_i is fresh after u_i is chosen; tau_i is fresh only after the first read. Beta_i is fixed before sigma_i, and chi_i before tau_i, in a filtration including the unobserved physical state. Chi_i may depend on sigma_i and the whole first experiment. A deterministic passive linear source supplies this filtration directly. A stochastic supplier must warrant that revealing its relevant current background does not reveal or bias the subsequently used private sign.

Every actual call obeys

\[
E(x')+\|\text{out}\|^2\le E(x)+\|\text{in}\|^2,
\qquad E\ge0.                                        \tag{2}
\]

The task is

\[
F(u)=\tfrac12\|Au-b\|^2+\tfrac\lambda2\|u\|^2,
\quad u\in D\subseteq\{\|u\|\le U\},\quad\lambda>0,    \tag{3}
\]

with D closed convex and unique minimizer u_*. Signed sensing, actual adjoint access, finite waveform operations, fixed loading, linearity and stable A are substantive supplied operations. The mechanical supplier and forward-only ordinary alternatives retain their different physical scopes.

The returned gradient g_i=tau_i z_i/kappa+lambda u_i satisfies the exact decomposition

\[
g_i-\nabla F(u_i)=\sigma_i A^*\beta_i+
\tau_i\chi_i/\kappa.                                \tag{4}
\]

The two terms are successive signed increments, not independent specimens. Their coefficients may be strongly dependent over time.

## 3. A self-contained ordinary martingale lemma

Let v_t be a predictable Hilbert-space vector, s_t a fresh fair sign, M_t=sum_{j<=t}s_j v_j and V_t=sum_{j<=t}||v_j||^2. For each fixed theta>0,

\[
W_t=\cosh(\theta\|M_t\|)\exp(-\theta^2V_t/2)           \tag{5}
\]

is a nonnegative supermartingale with W_0=1.

**Proof.** Expand cosh(theta sqrt(z)) in nonnegative powers of z. In the average at x+v and x-v, only even powers of <x,v> remain. Cauchy--Schwarz shows that this average is maximized for collinear vectors. Therefore

\[
\tfrac12\{\cosh(\theta\|x+v\|)+\cosh(\theta\|x-v\|)\}
\le\cosh(\theta\|x\|)\cosh(\theta\|v\|)
\le\cosh(\theta\|x\|)e^{\theta^2\|v\|^2/2}.
\]

Conditional averaging proves (5). This is an elementary instance of established exponential martingale methods in Hilbert spaces, not a claim of new probability theory. Pinelis's work and modern time-uniform martingale bounds are direct methodological predecessors.

For any observed process Q_t with V_t<=Q_t pathwise, the maximal inequality and cosh(x)>=exp(x)/2 give

\[
\Pr\left\{\exists t:\|M_t\|>
\frac\theta2Q_t+\frac{\log(2/\alpha)}\theta\right\}
\le\alpha.                                          \tag{6}
\]

Q_t may be read after the experiment; it need not be predictable. The increment coefficient v_t must be predictable. These are different conditions.

To select a useful slope without choosing theta after observing data, preallocate, in declared calibrated units,

\[
\theta_j=2^{-j},\quad
\alpha_j=\frac{6\alpha}{\pi^2(j+1)^2},\quad j=0,1,\ldots,
\]

and define

\[
\mathcal B_\alpha(q)=\inf_{j\ge0}
\left\{2^{-j-1}q+2^j\log\frac{\pi^2(j+1)^2}{3\alpha}\right\}.
                                                            \tag{7}
\]

A union bound proves (6) with B_alpha(Q_t) simultaneously at all times. Only finitely many slopes need evaluation at finite q: stop when the second summand alone exceeds the best value already found, because that summand increases with j. Any finite subset gives a valid, possibly weaker, radius. The confidence cost is logarithmic in 1/alpha with an iteration-logarithm overhead from the slope grid.

At a predeclared single time, a deterministic V_t<=v instead gives

\[
\Pr\{\|M_t\|>\sqrt{2v\log(2/\alpha)}\}\le\alpha.     \tag{8}
\]

All statements can be conditioned on an arbitrary completed old record satisfying the source and fresh-sign premises. Bounds selected from that old record are allowed. A mean energy bound alone does not permit replacing v by that mean in (8).

## 4. Observed gradient energy and adaptive inputs

Choose deterministic nonnegative weights w_i and S_n=sum_{i<=n}w_i>0. Predictable weights are also allowed algebraically; the finite-rate specialization uses w_i=i. Form actual averages

\[
\bar u_n=S_n^{-1}\sum_{i\le n}w_i u_i,\qquad
\bar g_n=S_n^{-1}\sum_{i\le n}w_i g_i.                \tag{9}
\]

The cumulative noise has successive coefficients w_i A^*beta_i and w_i chi_i/kappa. Its squared-increment process is bounded by the complete measured/commanded record

\[
V_n=\sum_{i\le n}w_i^2(\|A^*\beta_i\|^2+
\|\chi_i\|^2/\kappa^2)\le Q_n,                       \tag{10}
\]
\[
Q_n=2\sum_{i\le n}w_i^2
\left(\|y_i\|^2+\|u_i\|^2+
\frac{\|z_i\|^2}{\kappa^2}+\|r_i\|^2\right).          \tag{11}
\]

Indeed beta_i=y_i-sigma_i Au_i implies ||A^*beta_i||^2<=2||y_i||^2+2||u_i||^2. Likewise chi_i=z_i-kappa tau_i A^*r_i gives ||chi_i||^2/kappa^2<=2||z_i||^2/kappa^2+2||r_i||^2. Q_n uses no fitted or oracle matrix.

The affine-gradient identity holds pathwise:

\[
S_n^{-1}\sum_{i\le n}w_i\nabla F(u_i)=\nabla F(\bar u_n).
                                                            \tag{12}
\]

It remains true when u_i depends on earlier signs and observations. Combining (4), (7), (10) and (12), with probability at least 1-alpha,

\[
\boxed{\|\bar g_n-\nabla F(\bar u_n)\|\le
e_n:=\mathcal B_\alpha(Q_n)/S_n\quad\text{for every }n.} \tag{13}
\]

This certifies an adaptively constructed input from the same learning experiments. It does not assume independence between fitted input and validation data.

No initial-energy ceiling appears in the observable certificate (13). A warranted energy/range preparation remains necessary for a finite hardware range or an a priori cost bound. Arbitrarily large initial energy can produce arbitrarily large observed Q_n and trial costs.

### Passivity makes the radius shrink

Let B=||b||, a_kappa=(1-kappa^2)/2, d_kappa=kappa^2(1+kappa^2)/(1-kappa^2), and C=U^2+d_kappa B^2. The first theorem gives

\[
a_\kappa\sum_{i\le n}\|y_i\|^2+
\sum_{i\le n}\|z_i\|^2\le E_0+nC.                    \tag{14}
\]

For w_i=i, use ||r_i||^2<=2||y_i||^2+2B^2 and i^2<=n^2:

\[
Q_n\le n^2\{L_\kappa E_0+nH_1\},\qquad
L_\kappa=\max\{6/a_\kappa,2/\kappa^2\},\quad
H_1=L_\kappa C+2U^2+4B^2.                            \tag{15}
\]

For kappa=1/sqrt(7), L_kappa=14 and H_1=16U^2+(20/3)B^2. These are conservative sufficient constants. Since S_n=n(n+1)/2, the radius tends to zero at order sqrt((log(1/alpha)+log log n)/n); the initial-energy contribution is of order sqrt(E_0 log log n)/n. Neither hidden dimension nor a relaxation constant appears. Energy, measured mode counts and hardware range remain actual resources.

## 5. Stopping on the actual constrained inverse task

Set eta=1/(1+lambda). Since ||A||<=1, the exact projected-gradient map

\[
T(u)=\Pi_D\{u-\eta\nabla F(u)\}
\]

contracts by rho=1-eta lambda and has fixed point u_*. This includes an active constraint; the unconstrained gradient need not vanish.

Compute directly from the acquired record

\[
m_n=\|\bar u_n-\Pi_D(\bar u_n-\eta\bar g_n)\|,
\qquad
\mathcal R_n=\frac{m_n}{\eta\lambda}+\frac{e_n}\lambda.
                                                            \tag{16}
\]

On the single probability-1-alpha event in (13),

\[
\boxed{\|\bar u_n-u_*\|\le\mathcal R_n
\quad\text{for every }n.}                            \tag{17}
\]

**Proof.** The fixed-point contraction gives (1-rho)||u-u_*||<=||u-T(u)||. Replacing the true gradient by its estimate moves T(u) by at most eta e_n. Substitute (16) and 1-rho=eta lambda.

The learner can stop at the first declared checkpoint, or first round, with R_n<=epsilon. The returned input is within epsilon of the constrained regularized optimum with failure probability at most alpha. This spends confidence on the actual task and actual stopping history. It does not certify all future interventions, erase internal memory, or supply an unmeasured output port.

This rule consumes the first theorem's weighted-SGD records with no additional propagation call. A stronger ordinary optimizer can instead supply the u_i. The confidence event is valid for any adapted bounded u_i; convergence and efficiency of those choices are separate algorithmic questions.

For the weighted SGD, the pathwise cumulative gradient budget implies sum_i eta_i^2 E||g_i||^2<infinity by summation by parts. The standard nonnegative almost-supermartingale argument applied to the projected distance recurrence gives u_i->u_* almost surely: squared distance converges, sum_i eta_i||u_i-u_*||^2 is finite, and sum_i eta_i diverges. Its weighted average also converges. Applying the signed-martingale bound at a sequence of confidence levels tending to zero shows that the averaged gradient error tends to zero almost surely; (15) makes every fixed-level radius vanish. Thus the stopping criterion is eventually met almost surely under these exact-port assumptions. This is not a deterministic uniform deadline. The original finite expected-error bound, a declared cost cap, or fixed batches give separate probabilistic completion budgets.

## 6. A real receiving record, including optional stopping

After learning, select a fixed u using the whole completed record. Run a new batch of forward calls with fresh signs s_j and outputs y_j=s_j Au+beta_j. Put

\[
\widehat y_m=m^{-1}\sum_{j\le m}s_jy_j,
\qquad Q_m^{\rm read}=2\sum_{j\le m}\|y_j\|^2+2m\|u\|^2.
\]

The same lemma proves, conditionally on the completed learning record,

\[
\Pr\left\{\forall m:\
\|\widehat y_m-Au\|\le\mathcal B_\alpha(Q_m^{\rm read})/m
\ \middle|\ \text{old record}\right\}\ge1-\alpha.      \tag{18}
\]

The receiver may stop on this new record when the declared precision is reached. This optional-stopping scope is supplied by the new proof, not retrospectively attributed to the fixed-batch review. Subsequent queries can be chosen from prior completed batches with explicitly allocated conditional failure probabilities.

For a predeclared batch with an actual current energy bound E_start, passivity gives Q_m^read<=2E_start+4m||u||^2. The fixed-time radius is therefore

\[
\sqrt{2(2E_{\rm start}+4m\|u\|^2)\log(2/\alpha)}/m.   \tag{19}
\]

E_start is the current energy debit, not the initial calibration ceiling reused by declaration. An exact full-port ledger can supply it; partial outgoing measurements may yield a conservative ledger. Noisy squared readouts cannot simply be subtracted as lower bounds on true outgoing energy.

The received object is decoded incremental response. The instantaneous field remains s_j Au+beta_j. Raw focusing or total-field cancellation requires another physical operation.

## 7. Failures and changes in apparatus

**A nonlinear task lacks (12).** Mean gradients need not equal the gradient at the mean input. General nonlinear learning needs fixed-input batches, curvature/Jensen bounds or another representation. The same data cannot be relabeled as that stronger certificate.

**Old memory and operator drift differ.** If A changes, or the return call is not its actual adjoint, the bias in (4) is not the displayed symmetric noise. A warranted error envelope can be added; unrestricted drift cannot.

**The receiver is substantive.** Q_n uses calibrated waveforms. Unbiased noisy amplitudes alone do not upper-bound actual squared amplitudes. Saturation loses information. Finite-bandwidth projection, quantization and replay errors need their own joint guarantees.

**Energy is not a universal peak bound.** Residual replay may require range growing with the finite run length. The physical-mechanism role is constructing a different fixed-range route: weak or sparse signed forward probes and a clipped, quantized receiver, followed by ordinary numerical inversion. Its different precision rate and finite spatial acquisition cost are part of the comparison. Acquiring more of the finite boundary map can be preferable to a task-specific adjoint experiment.

**Ongoing input energy needs a budget.** Exogenous disturbances independent of current private signs can preserve the mean algebra. An almost-sure or high-confidence incoming-energy cap extends the rate proof with that debit. A mean energy bound alone does not imply the exponential tail above.

**Port energy is not the entire physical bill.** Fixed terminations, transducers, target access where used, phase references, sensing, randomization, waveform storage, latency, communication, computation and restoration remain real costs. A small number of propagation calls does not price every measured coefficient.

## 8. Primary comparison and actual read scope

1. Aarnoudse and Oomen, *Model-Free Learning for Massive MIMO Systems: Stochastic Approximation Adjoint Iterative Learning Control*, IEEE Control Systems Letters 5(6), 1946--1951 (2021), DOI 10.1109/LCSYS.2020.3046169. Root read the institutional full manuscript, including SISO reversal, MIMO randomization and the single additional experiment. Physical-gradient optimization and randomized adjoints are established.
2. Maruta and Sugie, *Reset-free Iterative Learning Control and Its Application to Continuous-time System Identification*, Transactions SICE 45(3), 144--152 (2009), DOI 10.9746/sicetr.45.144. Root read the official abstract and the lifted-state/control theorem in its official PDF. It retains cross-episode dynamics and uses a stabilizing robust servo with nonzero DC transfer; the text explicitly notes a plant-model requirement for controller design. Learning without reset or equilibrium waiting is established.
3. Simchowitz, Mania, Tu, Jordan and Recht, *Learning Without Mixing: Towards A Sharp Analysis of Linear System Identification*, COLT/PMLR 75, 439--473 (2018), https://proceedings.mlr.press/v75/simchowitz18a.html . Root read the introduction and state-observed OLS theorem from the official PDF. Learning without mixing is an established broader idea; that core theorem uses observed state trajectories and independent Gaussian innovations.
4. Pinelis, *Optimum bounds for the distributions of martingales in Banach spaces*, Annals of Probability 22(4), 1679--1706 (1994), with published correction; author's draft https://arxiv.org/abs/1208.2200 . Root read the author-supplied abstract and publication/correction metadata. The needed special lemma is proved in full above; the full Pinelis theorem was neither silently imported nor claimed read.
5. Pakshin et al., *Passivity based stabilization of repetitive processes and iterative learning control design* (2018), DOI 10.1016/j.sysconle.2018.09.003. The indexed publisher abstract confirms a passivity/ILC predecessor. The subsequent publisher open returned 403 and was not retried or bypassed. No theorem-level distinction from its unread body is asserted.

Broader wave-control predecessors and prior access failures remain in `physical_mechanism/PRIMARY_SOURCES.md`; constructive forward-only competitors are in `record_geometry/ORDINARY_CODED_GRADIENTS_WITH_WARM_FIELDS.md`. External priority of the combination remains unestablished. The useful result here is an explicit task-specific confidence and reuse proof for a persistent passive source, usable by ordinary algorithms.
