# Ordinary coded gradients through a warm linear medium

30 October 2026. Constructive ordinary alternative by the existing
record-geometry role. Root owns the passive supplier and its
energy-controlled learning theorem. Earlier files remain unchanged.

## 1. Actual task and ports

Minimize \(F(u)=\|Au-b_\star\|^2/2\), where the fixed unknown map
\(A:\mathbb R^d\to\mathbb R^m\) may act on finite waveforms.
Each actual pass supplies
\[
y=Ax+b_{\rm old}.
\tag{1}
\]
The background may depend on all preceding drives, observations,
decisions and hidden fields. It need not mix or have zero conditional
mean. It is independent of the fresh current phase, conditional on
the complete pre-pass state and history. Independent additive noise
can be included with the same conditional independence and integrability.

This is a supplied linear-source interface. State-dependent coefficients,
sign-dependent detector gain and nonlinear saturation are not included.
Signed waveform preparation/readout, calibrated gain and the actual
mode/energy inner product are required. Intensity-only sensing does
not supply these reports by itself.

Let \(\mathcal H\) contain all completed earlier records. The chosen
u may be any \(\mathcal H\)-measurable action. Every unbiasedness
claim below is conditional on this old history, not on selected
current-trial outcomes or its future signs.

## 2. Two fresh signs are ordinary sequential instruments

Draw a fresh fair sign sigma, drive sigma u, and read
\[
y=\sigma Au+b,\qquad
\widehat r=\sigma y-b_\star=Au-b_\star+\sigma b.
\tag{2}
\]
If an actual adjoint pass is supplied, draw a new fair sign tau
after this observation and drive \(\kappa\tau\widehat r\).
The calibrated report is
\[
z=\kappa\tau A^\mathsf T\widehat r+c.
\tag{3}
\]
Here c may remember sigma, y and the whole first experiment; only
independence from the new tau is required. The estimator
\[
g_{\rm adj}=\tau z/\kappa
=A^\mathsf T(Au-b_\star)+\sigma A^\mathsf Tb+\tau c/\kappa
\tag{4}
\]
satisfies
\[
E[g_{\rm adj}\mid\mathcal H]=\nabla F(u)
\tag{5}
\]
by first averaging tau, then sigma. This is sequential instrumental
demodulation, not physical inversion of attenuation. It uses no
independent specimen, hidden-state copy or inter-pass ringdown.

Passivity is unnecessary for this algebraic mean identity. It matters
for the complete field-energy and gradient-variance bill. Unbiasedness
alone gives no finite-precision learning guarantee.

## 3. A forward-only supplier for arbitrary linear A

After (2), choose a fresh unit direction v with
\(E[vv^\mathsf T]=I_d/d\), independently of the earlier record.
A uniformly selected coordinate vector suffices. For nonzero residual,
use a second forward pass
\[
x_2=\kappa\tau\|\widehat r\|v,\qquad
y_2=\kappa\tau\|\widehat r\|Av+c
\]
and return
\[
g_{\rm dir}=\frac d\kappa v
\left\langle\frac{\widehat r}{\|\widehat r\|},\,\tau y_2\right\rangle .
\tag{6}
\]
For zero residual, a zero-input pass can be run and its gradient set
to zero. Conditional tau averaging gives
\(d\,vv^\mathsf T A^\mathsf T\widehat r\).
Averaging v, then sigma, proves (5) again, without reciprocity.
There is no finite-difference bias or small-perturbation limit.

The two input energies are \(\|u\|^2\) and
\(\kappa^2\|\widehat r\|^2\), exactly as in the physical-adjoint pair.
In a cold noiseless pair, putting \(a=A^\mathsf T(Au-b_\star)\),
\[
E\|g_{\rm dir}\|^2=d\|a\|^2,\qquad
E\|g_{\rm dir}-a\|^2=(d-1)\|a\|^2.
\tag{7}
\]
In any warm pair,
\(\|g_{\rm dir}\|^2\le d^2\|y_2\|^2/\kappa^2\).
The physical adjoint has no cold direction noise and satisfies
\(\|g_{\rm adj}\|^2=\|z\|^2/\kappa^2\).
This is a comparison of these suppliers, not a minimax lower bound
against every forward-only method.

## 4. Stronger ordinary LTI coding

For a linear time-invariant medium, the full waveform dimension d
is often the wrong variance factor. Let p,q be input/output channel
counts and N the number of actual time samples per window.
Each block \(A_{\ell j}\) is a causal Toeplitz convolution matrix.
Let R reverse N stored samples and
\(R_p=I_p\otimes R,\ R_q=I_q\otimes R\). Then
\[
A_{\ell j}^\mathsf T=R A_{\ell j}R.
\tag{8}
\]
This reverses a drive waveform and a recorded waveform. It does not
run the unknown medium or its attenuation backward.

For p=q=1, a second forward input
\(\kappa\tau R\widehat r\), followed by the returned estimate
\(R\tau y_2/\kappa\), already has mean \(A^\mathsf T\widehat r\).
Together with (2), it gives the exact warm-field gradient with the
same two passes and input energy, without a reverse port or a
waveform-dimension direction factor.

For MIMO, draw a fresh p-by-q matrix S of independent fair signs and
put \(K_S=S\otimes I_N\). Index contraction gives the block identities
\[
E_S[K_SAK_S]_{ij}=A_{ji},\qquad
R_pE_S[K_SAK_S]R_q=A^\mathsf T.
\tag{9}
\]
This is Aarnoudse--Oomen's established channel-adjoint randomization
[1]. The following adds explicit warm-field instruments and energy
normalization, without claiming new generic masks or adjoints.

For nonzero residual define
\[
a_S=\frac{\|K_SR_q\widehat r\|}{\|\widehat r\|}.
\]
When \(a_S>0\), use the same forward plant with
\[
x_2=\frac{\kappa\tau}{a_S}K_SR_q\widehat r,\qquad
g_S=\frac{a_S}{\kappa}R_pK_S(\tau y_2).
\tag{10}
\]
If the numerator or residual vanishes, use zero input and return zero;
the corresponding ideal \(K_SAK_SR_q\widehat r\) also vanishes.
Otherwise \(\|x_2\|=\kappa\|\widehat r\|\).

Conditional tau averaging removes the second warm field and cancels
the normalization factors in the signal term. Averaging S, then sigma,
proves (5). Since
\[
a_S\le\|S\|\le\sqrt{pq},\qquad
\|g_S\|^2\le(pq)^2\|y_2\|^2/\kappa^2,
\tag{11}
\]
the direct energy-to-gradient bound involves only spatial channel
count, not the temporal sample count N. It is deliberately conservative.
For p=q=1, channel randomization can be omitted.

These statements use real calibrated signals. Complex envelopes need
the corresponding conjugation for a Hermitian adjoint, or treatment
of both real quadratures as actual channels. The permitted waveform
spaces must support temporal reversal. A general time-varying medium
or a restricted mode menu need not obey (8); an actual reciprocal
return port can then supply a different operation.

## 5. Fixed phase cycling is not a universal exact cancellation

Consider the passive reciprocal scalar scattering cell
\[
\begin{pmatrix}x_{t+1}\\y_t\end{pmatrix}
=
\begin{pmatrix}\rho&\sqrt{1-\rho^2}\\
\sqrt{1-\rho^2}&-\rho\end{pmatrix}
\begin{pmatrix}x_t\\u_t\end{pmatrix},
\qquad0<\rho<1.
\tag{12}
\]
The full matrix is symmetric and orthogonal, with complete energy
accounting. Starting at \(x_0=0\), the first input sigma u gives
\(y_1=-\rho\sigma u\) and
\(x_1=\sqrt{1-\rho^2}\sigma u\). The second pass therefore already
has a background correlated with the first sign. Reusing tau=sigma
in the adjoint protocol gives
\[
E[g_{\rm reused}]
=\rho^2u+\rho b_\star+(1-\rho^2)u/\kappa.
\tag{13}
\]
The last term is an actual inter-pass-memory bias, even from a cold
start. An independent tau removes it.

A finite deterministic linear phase cycle also cannot cancel every
unknown initial tail. The arbitrary initial-state contribution to a
predetermined weighted report from (12) is
\[
\sqrt{1-\rho^2}\,x_0\sum_{t=0}^{n-1}w_t\rho^t .
\]
For this to vanish for every \(\rho\in(0,1)\), the polynomial must
be identically zero, forcing all weights to vanish. This restricted
impossibility concerns fixed finite linear combinations, not every
adaptive nonlinear identification procedure.
Fresh phases cancel the background in conditional expectation;
they do not remove it from every individual report.

## 6. Actual resource and scope comparison

All protocols retain old records and the persistent field. Their
conditional mean identities permit data-selected iterates.
Postselection on a favorable current output or its fresh phases
does not preserve the same identity.

Forward-only channel coding requires up to pq fresh bits, actual
channel mixing, N-sample recording/replay buffers, temporal reversal
and calibrated synthesis. The generic direction method needs its
random mode selection and output inner product. These are ordinary
computation/control costs, not hidden copying. A physical reciprocal
port can avoid the channel masks and their gradient-variance factor.
It does not uniquely enable removal of arbitrary warm backgrounds.

Drive energy depends on the actual residual. A hard residual clamp
changes the estimator unless its bias or exceptional event is bounded.
This file does not claim a universal bounded-peak-drive or
finite-detector-range theorem. Actual sensor noise, quantization and
port-calibration errors belong in the conditional source and learning
budget. No noise or initial-state independence is inferred from a
small measured average error.

Passivity does not supply a free bound on initial field energy or a
thermal preparation. Once its actual chronological inequality is
warranted, (11) transfers an energy bound to this ordinary supplier
with its stated spatial-channel multiplier. Root develops the
energy-controlled optimization theorem separately. A known
regularization term adds its deterministic gradient; it does not
remove small singular values or inverse-problem conditioning costs.

## 7. Primary predecessors and exact source scope

1. L. Aarnoudse and T. Oomen, *Model-Free Learning for Massive MIMO
   Systems: Stochastic Approximation Adjoint Iterative Learning Control*,
   IEEE Control Systems Letters 5, 1946--1951 (2021),
   DOI 10.1109/LCSYS.2020.3046169.
   https://pure.tue.nl/ws/files/193833656/Model_Free_Learning_for_Massive_MIMO_Systems_Stochastic_Approximation_Adjoint_Iterative_Learning_Control.pdf
   Primary full PDF read. Lemmas 2--3 give waveform reversal;
   Theorem 1 and Algorithm 1 give randomized channel coding with a
   single additional forward experiment. These directly preempt the
   ordinary LTI adjoint mechanism. Its displayed experiment model does
   not state arbitrary changing warm backgrounds.

2. L. Aarnoudse and T. Oomen, *Efficient MIMO Iterative Feedback Tuning
   via Randomization*, CDC 2023, published 2024,
   DOI 10.1109/CDC49753.2023.10383883.
   https://pure.tue.nl/ws/portalfiles/portal/317655420/2023-09-12_SAIFT_final_v3.pdf
   Primary accepted manuscript read. It supplies an unbiased randomized
   gradient experiment. Assumption 1 explicitly requires zero-mean
   disturbances with equal second-order statistics and mutually
   independent sequences across experiments. It does not itself prove
   the arbitrary warm-history replacement above.

3. C. Boesch, Y. Gediz, C. Wanjura and H. E. Tuereci,
   *Unifying Physical Backpropagation*, arXiv:2608.11585 (2026).
   This author listing follows the current primary group page:
   https://turecigroup.princeton.edu/publications/unifying-physical-backpropagation
   Only the author-page abstract was read. It explicitly permits
   damping/gain in linear reciprocal physical adjoints and a
   finite-amplitude experiment. An arXiv HTML attempt returned
   DisabledError; root also reports an earlier P1 full-source boundary.
   No subsequent PDF, mirror or other full-text retry was made.

4. M. Tanter, J.-L. Thomas and M. Fink, *Time reversal and the inverse
   filter*, JASA 108, 223--234 (2000),
   DOI 10.1121/1.429459.
   https://pubmed.ncbi.nlm.nih.gov/10923887/
   Primary abstract read. It distinguishes reciprocal matched filtering
   in dissipative/limited-aperture media from inversion of the
   propagation operator. The adjoint is not free inversion of loss.

Randomized IFT already appears in Gerencser, Vago and Hjalmarsson,
IFAC 2002, DOI 10.3182/20020721-6-ES-1901.01046, located here at
primary indexed-abstract scope. No exhaustive priority finding is made.

The arXiv HTML attempt for Tuxbury--Lin's
*Physical policy gradient theorem for in situ stochastic-adjoint
training*, arXiv:2609.05808, also returned DisabledError.
No alternate transfer or full-text theorem from it is used.

## 8. Check interface

The companion check_warm_coded_gradients.py constructs a reciprocal
passive state-space wave cell with persistent observable modes and
an exactly frozen hidden coordinate. It checks the physical reverse
port, generic direction and LTI channel-coded conditional expectations
against the model's oracle gradient.

Enumeration over signs and masks is a population identity check,
not a physical protocol that copies initial hidden states. Actual
state transitions within each enumerated chronological branch are
retained. The script also checks complete energy accounting,
finite-window transposition, cold direction variance and reused-phase
bias. Its oracle matrix is used only for verification, never supplied
to the proposed learner. No acquired precision, apparatus validation
or practical speedup is claimed.

Executed once on 30 October 2026. Three channel/window configurations
passed. The largest conditional-gradient identity residual was
\(7.53\times10^{-16}\); the largest complete per-step energy residual
was \(3.09\times10^{-14}\). All modeled frozen coordinates remained
unchanged. In the scalar counterexample the true and independently
demodulated gradient was 0.432, while reusing the phase gave 2.672.
The full population results and exact code hash are saved in
WARM_CODED_GRADIENT_CHECK_RESULTS.json.
