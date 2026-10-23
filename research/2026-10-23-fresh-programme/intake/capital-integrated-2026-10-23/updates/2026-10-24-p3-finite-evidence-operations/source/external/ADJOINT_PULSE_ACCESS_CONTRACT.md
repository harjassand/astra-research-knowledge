# Access audit: equilibrium and adjoint pulse correlations

Private P3 research note, 2026-10-23. This bounded assessment supports the
parent's correlation/residual construction. It adds no experimental data or
benchmark result. Source versions, precise support, and limitations are in
`ADJOINT_PULSE_SOURCES.json`. Earlier completed bundles are unchanged.

## 1. Result and scope

**An executable Markov adjoint is sufficient; individual reversibility is
not necessary.** Reverse-order compositions of individually reversible
updates provide an exact example. Gibbs updates supply an obtainable,
normalizer-free simulator contract. Passive isothermal RC networks supply
a defensible conditional physical contract if controls change conductance
without changing energy, temperature, or the readout process.

The attempted stronger physical justification fails: holding visible dot
potentials fixed does not hold the hidden energy spectrum fixed. Ordinary
physical time reversal also need not be an executable adjoint on the
unobserved state. No cited experiment establishes the full proposed
unknown-dimensional, partially observed, controlled common-equilibrium
interface. Its usefulness for a consequential physical computation is
**UNKNOWN**.

The positive identities below are standard operator facts. The information
access comparison is against retaining residual/variational kinetic models
given the same correlations and structural warrants. No architectural
advantage is asserted.

## 2. Exact access contract, including adjoints

Let all Markov operators act on the same real Hilbert space
\(L^2(\pi)\), preserve the probability law \(\pi\), and be contractions.
Neither the normalizing constant, hidden dimension, nor transition matrix
must be given to the learner. Let \(|f|\le B\) be an accessible observable.
For every action \(a\), suppose an executable action \(a^\dagger\) has

\[
P_{a^\dagger}=P_a^* \quad\text{on }L^2(\pi).
\]

Use the convention \(P_w=P_{a_1}\cdots P_{a_k}\) for chronological actions
\(w=a_1\cdots a_k\). Define
\(w^\dagger=a_k^\dagger\cdots a_1^\dagger\). Stationary endpoint products
give

\[
C(w)=\mathbb E_\pi[f(X_0)f(X_{|w|})]=\langle f,P_wf\rangle_\pi.
\]

For implicit features \(v_u=P_uf\), the identities are

\[
\begin{aligned}
G_{uv}&=\langle v_u,v_v\rangle=C(u^\dagger v),\\
(H_a)_{uv}&=\langle v_u,P_av_v\rangle=C(u^\dagger a v),\\
(J_a)_{uv}&=\langle P_av_u,P_av_v\rangle
             =C(u^\dagger a^\dagger a v).
\end{aligned}
\]

The proof is moving operators across the inner product. It does not
condition on, observe, or copy a hidden state. The extra matrix \(J_a\)
is consequently accessible from one forward trajectory per endpoint
product, given the adjoint contract and a stationary start. This is a
different acquisition route to the squared conditional-mean matrix used
by stochastic ResDMD; it does not create a different residual algebra.
See [ResDMD, sections 1.3, 3.2 and 4.2](https://arxiv.org/html/2308.10697v3).

Full hidden reversibility is a sufficient warrant, not logically necessary
for every task. It suffices that the required adjoint identities hold on
the relevant observable subspace. A hidden sector which is provably
decoupled from that subspace need not be identified. Merely observing
unchanged marginal distributions of \(f\) does not prove this decoupling.

### Costs which the formula does not remove

- The initial sample must have the stipulated equilibrium law, or a
  quantified bias. If \(\|\nu-\pi\|_{\rm TV}\le\epsilon\), with TV defined
  as a supremum over events, then
  \(|C_\nu(w)-C_\pi(w)|\le2B^2\epsilon\). This follows by applying TV
  duality to \(f(x)P_wf(x)\), whose absolute value is at most \(B^2\).
- Multiple trajectory products are not independent merely because their
  marginal law is stationary. Independent preparation, or a justified
  dependent-data confidence analysis, must be charged.
- A reading at the start must implement the stipulated observation
  channel. Detector backaction, finite bandwidth, misclassification,
  correlated noise, drift, and switching transients are not sampling
  error automatically covered by concentration of endpoint products.
- Equality of a few reversed correlations and positive semidefiniteness
  of a measured Gram matrix are useful falsification checks, not a
  uniform certificate of arbitrary hidden-state adjoint access.

## 3. Quantum dots: demonstrated control, missing full-equilibrium warrant

[Rochette et al. (2019)](https://arxiv.org/html/1707.03895v2) demonstrate
reservoir-to-dot tunnel-rate control with a second gate compensating the
dot chemical potential, and use a proximal charge sensor. Their paper
also characterizes gate-dependent valley splitting. The latter result
does not establish that the exact compensated rate sweep changes that
splitting; it does establish why charge occupation alone does not specify
the entire internal energy structure.

The decisive, more direct warning comes from
[Hsiao et al. (2020), page 4](https://arxiv.org/pdf/2001.07671): virtual
barrier gates vary tunnel couplings while keeping dot potentials fixed,
and thereby also vary spin exchange couplings. Their calibration reduces
measured tunnel crosstalk; those crosstalk percentages are not bounds on
the change in the full equilibrium measure.

A weak-coupling, sequential-tunneling approximation could have forward
and reverse rates scaled by the same kinetic factor at fixed reservoir
temperature and fixed relevant energy differences. That would preserve
the corresponding classical equilibrium distribution. It remains a
conditional model contract, requiring control of all energy changes
relevant to the observed cyclic subspace. It is not obtained by declaring
all unobserved spin, valley, reservoir, and detector variables irrelevant.

[Hofmann et al. (2016)](https://arxiv.org/html/1504.04949v1) provide a
valuable calibrated simple regime: one reservoir, measured tunneling
rates, charge readout, and a detailed-balance rate relation with a measured
degeneracy factor. Their energy drive does not preserve a common
equilibrium law. Their preparation waits, detection bandwidth, and drift
correction also show why these operations have costs. A rate-equation
model is a strong tailored baseline in that low-dimensional regime.

## 4. Conditional physical positive class: passive isothermal RC

Consider hidden capacitor-charge coordinates \(q\), a fixed confining
energy \(U(q)\), and a common bath temperature \(T\). Assume that action
\(a\) changes only a constant symmetric positive semidefinite conductance
mobility \(M_a\), with matched thermal noise:

\[
dq_t=-M_a\nabla U(q_t)\,dt+
             \sqrt{2k_BT M_a}\,dW_t.
\]

Under boundary and regularity conditions which justify integration by
parts, \(\pi(dq)=Z^{-1}e^{-U(q)/(k_BT)}dq\) is common to every action, and

\[
\langle h,L_ag\rangle_\pi
=-k_BT\int (\nabla h)^\top M_a\nabla g\,d\pi.
\]

Thus \(L_a\) is selfadjoint and nonpositive, and each finite pulse
\(e^{tL_a}\) has the required common-equilibrium reversibility. The proof
does not require the learner to know \(U\), \(Z\), topology, capacitances,
conductances, or hidden dimension numerically. It does require a justified
physical class. A bounded voltage detector, for example a calibrated
clipped voltage, supplies a bounded observable without measuring all
capacitor charges.

[Chiang et al. (2017)](https://arxiv.org/pdf/1703.10762) experimentally
study a capacitively coupled RC network driven by real resistor thermal
noise. Inductive effects are negligible in their model. Their equal-bath
case is consistent with equilibrium detailed balance; unequal baths
produce circulating probability flow. They do **not** demonstrate the
proposed pulse experiment with switched conductances at fixed energy.

[Osborne and Lucas](https://arxiv.org/html/2406.11796v1) supply a systematic
thermal circuit model and explicitly state its Gaussian Markov noise
assumption. The RC restriction above is a mathematical specialization,
not a device certification supplied by their theory.

An attempted implementation therefore needs a charged warrant for fixed
energy/capacitance, equal temperature, conductance/noise matching, absence
or bounded effect of inductive memory, readout loading, DC bias, pulse
transients, and drift. Observed port noise and covariance are useful
checks. They do not alone bound arbitrary hidden departures from the
class. Changing capacitances changes energy; adding unmatched artificial
noise changes the stationary law. Neither operation inherits this proof.

This is a credible acquisition experiment, not yet a consequential
application. Linear RC networks have strong linear-system and
fluctuation-dissipation baselines. Unknown internal state dimension does
not by itself make the learned representation practically superior.

## 5. Beyond reversible pulses: exactly what can be reversed

### 5.1 Reverse the order of warranted elementary stages

If \(K_1,\ldots,K_m\) are selfadjoint contractions on the same
\(L^2(\pi)\), the generally nonreversible pulse
\(P=K_1\cdots K_m\) has executable adjoint
\(P^*=K_m\cdots K_1\). Thus a nonreversible composite physical protocol
can qualify when every elementary stage has the RC-type warrant above.
The common measure and elementary adjoints, rather than visual reversal
of a waveform, justify the operation.

### 5.2 Hidden parity cannot be dropped, even for an even observable

For equilibrium inertial dynamics, microscopic time reversal commonly
has the form \(P_t^*=\Theta P_t\Theta\), where \(\Theta\) reverses momentum
or flux. Equation (9) and section 3.3.4 of Osborne--Lucas explicitly
include this parity: charge is even and flux is odd. Reading only charge
does not implement \(\Theta\) on the internal state.

Here is a bounded-observable obstruction. For a deterministic harmonic
oscillator at canonical equilibrium, set \(f(q,p)=\operatorname{sign}(q)\).
At a quarter-period \(t\),

\[
\|P_tf\|_\pi^2=1,
\qquad
\langle f,P_{2t}f\rangle_\pi=-1.
\]

The false forward-double-pulse Gram diagonal is negative. The example is
not an artifact of zero damping. For the thermal Langevin oscillator

\[
dq=p\,dt,\qquad
dp=-\omega^2q\,dt-\gamma p\,dt+\sqrt{2\gamma T}\,dW,
\quad \omega^2=1+\gamma^2/4,
\]

the stationary position correlation coefficient is

\[
\rho(s)=e^{-\gamma s/2}
       \left(\cos s+\tfrac\gamma2\sin s\right).
\]

For \(t=\pi/2\), the bounded sign observable consequently gives

\[
\langle f,P_{2t}f\rangle
=\frac2\pi\arcsin\!\left(-e^{-\gamma\pi/2}\right)<0,
\]

while the true squared norm is nonnegative. The sign formula follows by
integrating a centered bivariate Gaussian, or by differentiating its
positive-quadrant probability with respect to its correlation and using
the independent case. This is an exact counterexample, not simulation.
Although \(\Theta f=f\), the propagated function \(P_tf\) need not be
\(\Theta\)-even. That is precisely the missing step.

No source checked here establishes a general physical operation which
reverses every relevant hidden momentum or flux without observing it.
This is **not established**, rather than a claim of physical impossibility.

### 5.3 Drift reversal is sufficient only with a stationary-current warrant

For a diffusion generator \(L=S+c\cdot\nabla\), where \(S=S^*\) in
\(L^2(\pi)\) and \(\nabla\cdot(\pi c)=0\), integration by parts gives
\(L^*=S-c\cdot\nabla\). A control which genuinely flips only this
weighted divergence-free current implements the adjoint. Merely calling
a force nonconservative does not establish the condition.

A source-bound low-dimensional illustration is the toroidal optical
trap of [Gomez-Solano et al.](https://fys.kuleuven.be/english/staff/christ/files/pdf/pub/lyonjstatmech.pdf).
They measure angular trajectories and infer a stationary density and
current for \(d\theta=b(\theta)dt+\sqrt{2D}\,dW\). On the circle, the
adjoint drift relative to its stationary density \(\rho\) is

\[
b^*(\theta)=-b(\theta)+2D\partial_\theta\log\rho(\theta)
            =b(\theta)-2j/\rho(\theta).
\]

This follows directly from \(j=b\rho-D\rho'\). For the ideal uniform
ring, \(b=F\) and \(\rho\) is uniform, so force reversal is sufficient.
For the paper's nonuniform potential, reversing the constant drive alone
is generally not the adjoint. The experiment reports static optical
distortions and calibrates them. It does not claim to implement this
adjoint. Acquiring and applying \(b^*\) generally needs resolved position,
calibrated density/current, and force control: stronger access than a
hidden-state scalar endpoint interface. This is not a demonstrated route
to an arbitrary hidden-dimensional adjoint.

## 6. Exact normalizer-free simulator contract: Gibbs and reversed sweeps

Let a scientific target law have an unnormalized density \(\widetilde\pi\),
and let an implementation sample exact block conditionals. For block
\(i\),

\[
(K_ig)(x)=\mathbb E_\pi[g(X)\mid X_{-i}=x_{-i}].
\]

Conditional expectation is an orthogonal projection in \(L^2(\pi)\):
\(K_i^2=K_i=K_i^*\). For example, if \(\mathcal F_i\) is generated by
\(X_{-i}\),

\[
\mathbb E[h\,K_ig]
=\mathbb E[\mathbb E[h\mid\mathcal F_i]
            \mathbb E[g\mid\mathcal F_i]]
=\mathbb E[(K_ih)g].
\]

The global normalizer cancels in each conditional. Every block shares
the same \(\pi\), and a systematic sweep has the reverse-order sweep as
its adjoint. Exact Metropolis--Hastings updates with known proposal and
acceptance rules provide another standard common-target reversible
primitive. A learner may use these verified update implementations as
black boxes without knowing their enormous transition matrix or fitting
an explicit source equation.

These facts are established machinery, not a novelty claim. For a primary
operator treatment, [Tan, Jones and Hobert, section 4](https://arxiv.org/html/1206.4770v1)
explicitly distinguish reversible random scan from generally nonreversible
deterministic scan and express norms using stationary correlations and
conditional variances. They cite Liu--Wong--Kong (1994, 1995); the latter
paper is retained in the source ledger, with the limitation that its
scanned body was not reliably text-accessible in this audit.

There is a real computational question: different scan schedules can
have different statistical efficiency and hardware costs.
[He et al. (2016)](https://arxiv.org/pdf/1606.03432) give counterexamples
with polynomial differences and make the hardware/statistical distinction
explicit. The present interface could certify a selected observable's
finite-lag relaxation or response to new update schedules. It does not
certify global mixing, equilibrium accuracy from an arbitrary start, or
unobserved slow modes.

### The two serious qualifications

1. **Stationary initialization is not supplied by invariance.** Establishing
   a stationary target for every update does not tell us how long to run
   before correlation acquisition. Perfect sampling can sometimes supply
   exact starts; [Propp--Wilson](https://www.stat.berkeley.edu/~aldous/206-RWG/RWGpapers/propp_wilson.pdf)
   requires coupled update access and a certifiable coalescence event,
   not just an arbitrary endpoint API. Its random run time, failed
   coalescence attempts, saved randomness, and applicable structural
   conditions must be charged. Otherwise use a justified initialization
   bias bound or state that equilibrium preparation remains unresolved.
2. **The baseline may copy simulator state.** When states can be saved and
   cloned, stochastic ResDMD's independent-futures access is ordinarily
   available. The baseline gets it, along with the same retained endpoint
   correlations and update proofs. Reverse-pulse access could still trade
   memory, restart costs, or protocol lengths differently, but it is not
   new information available only to the proposed learner.

## 7. Decision for the research claim

| Claim | Status after this audit |
|---|---|
| Executable common-measure adjoints acquire implicit feature Gram and propagated-Gram matrices | Exact conditional identity; no novelty claimed for the algebra |
| Reverse order of reversible stages suffices for nonreversible composite pulses | Proven; available for verified Gibbs/Metropolis implementations and conditional physical stages |
| Fixed visible dot potentials imply a common hidden equilibrium | Unsupported; exchange-control evidence directly blocks the inference |
| Microscopic reversibility means forward waveform reversal supplies an adjoint | False without the needed parity/control operation; bounded counterexample above |
| Passive conductance-only thermal RC control is a candidate physical interface | Defensible component-based contract; complete pulse experiment and calibration not demonstrated here |
| Simulator update invariance makes stationary samples free | False; initialization and dependence remain charged |
| Same-information retaining residual/Galerkin modelling is beaten | No; it reproduces the inference and may have additional ordinary cloning access |
| A consequential scientific computation is newly tractable | UNKNOWN; no application or efficiency advantage established by this access audit |

The strongest justified next comparison is the full acquisition cost of
adjoint endpoint products versus independent-futures residual estimation
on an externally chosen task where their access costs genuinely differ.
For a physical experiment, obtain a component-based common-measure or
restricted-subspace adjoint warrant before interpreting residual intervals
as certificates. An unverified hidden-equilibrium promise would move the
scientific difficulty into the input rather than resolve it.
