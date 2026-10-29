# Normally displayed final: formula text projection

Deterministic text/formula projection of the normally displayed final and short audit continuation, not an acquired theorem manuscript, code or review original. Raw visible text and private DOM are preserved separately.

ChatGPT said:ChatGPT

The strongest new opening is stationary-state learning with bounded quantum retention. I derived a matching source-call law under the original supplied Choi-floor promise. It identifies a resource that the earlier classical acquisition contract discarded: keeping the probe through several consecutive source calls before measuring it.

This came after substantive defeats of two candidates. The truncated-history alternative won on the old control benchmark. Ordinary process identification then beat the new Fourier-response construction. I preserved those comparisons and used them to change the operation.

1. New result: how probe retention changes stationary-state learning

Let the unknown, fixed, memoryless  $d$ -dimensional channel satisfy $J_{\mathcal E}\succeq \nu I_{d^2}/d^2.$ 

The task is to return a classical density-matrix estimate  $\widehat\rho$  of its unique stationary state, with $\|\widehat\rho-\rho_{\mathrm{ss}}\|_1\le\epsilon$ 

with probability at least  $2/3$ .

Acquisition uses fresh blocks. Within a block, a prepared probe passes through  $\mathcal E$  at most  $B$  consecutive times, then is measured or discarded. Classical choices may adapt between blocks. A fresh reference is allowed within a block for the lower bound. There are no intermediate controls or measurements, and no quantum memory carried between blocks.

For fixed  $d$ ,  $0<\nu\le1/20$ , and sufficiently small  $\epsilon$ , the derived minimax law is $\boxed{
N_{\mathrm{opt}}
=
\Theta_d\!\left(
\frac{1}
{\nu^2\min\{B,\nu^{-1}\}\epsilon^2}
\right).
}$ 

Here  $N_{\mathrm{opt}}$  is worst-case expected source calls. The upper construction has a deterministic acquisition budget.

 | Maximum retained block | Source-call scaling

 | Measure after every call,  $B=1$  |  $\Theta_d(\nu^{-2}\epsilon^{-2})$ 

 |  $1<B<\nu^{-1}$  |  $\Theta_d((B\nu^2\epsilon^2)^{-1})$ 

 | Retain through order  $\nu^{-1}$  calls |  $\Theta_d(\nu^{-1}\epsilon^{-2})$ 

The constants are dimension dependent. This is a learning result; the output is an approximate classical state description. The earlier exact batch-reproduction and timing results retain their separate contracts.

Constructive upper bound

The Choi promise gives the mathematical decomposition $\mathcal E=\nu\mathcal D+(1-\nu)\mathcal F,
\qquad
\mathcal D(X)=\operatorname{Tr}(X)I/d.$ 

It follows that  $\mathcal E$  contracts differences of states by at most  $1-\nu$ . The laboratory never needs to identify a reset or execute  $\mathcal F$ .

Choose $b=\min\{B,\lceil\nu^{-1}\rceil\},
\qquad
\mathcal G=\mathcal E^b,
\qquad
\gamma_b=1-(1-\nu)^b.$ 

Perform ordinary informationally complete process tomography on the actual block channel  $\mathcal G$ . Each observation costs  $b$  source calls and requires retaining the probe for those calls. Estimate  $\mathcal G$  to induced trace-norm error $\eta=O(\epsilon\gamma_b).$ 

For fixed dimension, this needs  $O_d(\eta^{-2})$  block observations at constant confidence.

There is a direct classical reconstruction that avoids assuming the fitted map is physical. Make the linear fit Hermiticity preserving and trace preserving. On traceless Hermitian matrices, it contracts by at most  $1-\gamma_b+\eta$ . Its trace-one affine fixed point  $\sigma$  therefore satisfies $\|\sigma-\rho_{\mathrm{ss}}\|_1
\le \frac{\eta}{\gamma_b-\eta}.$ 

Clip negative eigenvalues and renormalize. This increases the error by at most another copy of that bound: $\|\widehat\rho-\rho_{\mathrm{ss}}\|_1
\le \frac{2\eta}{\gamma_b-\eta}.$ 

Taking  $\eta=\epsilon\gamma_b/4$  is sufficient for  $\epsilon\le1$ . Consequently, $N=O_d\!\left(\frac{b}{\epsilon^2\gamma_b^2}\right),$ 

which gives the displayed law.

The enabling interface is concrete: known input preparations, ordinary output measurements, one retained  $d$ -level probe, a fixed-size tomography table, a linear solve on  $d^2-1$  coordinates, and a  $d\times d$  spectral projection. No source adjoint, inverse, labelled reset, shifted control, or channel-synthesis catalogue is required. Preparation, readout, arithmetic precision and holding time remain real costs.

Matching lower bound

The complementary review found a slow coherent family that penalizes immediate measurement. I extended it to the full-rank Choi-floor class.

Let  $X_2,Y_2,Z_2$  act on a two-dimensional subspace and vanish outside it. Set $s=2\nu,\qquad
\tau=\frac{I+\tfrac12 Z_2}{d},$ 

and consider $\mathcal E_u
=
\operatorname{Ad}_{e^{-isuY_2/2}}
\circ
\left[(1-s)\operatorname{Id}+s\mathcal R_\tau\right],
\qquad u\in[0.8,1.2].$ 

Its normalized Choi matrix has floor at least  $\nu I/d^2$ . Writing  $p=1-s$ , its stationary  $Z_2$  expectation is $f_s(u)=
\frac1d
\frac{s[\cos(su)-p]}
{1-2p\cos(su)+p^2},$ 

with  $|f_s'(u)|\ge1/(4d)$  throughout the stated range.

For a block of length  $b$ , strengthen the experimenter by revealing the last-reset branch at the end of the block. The surviving rotation length has the law $L=\min\{\operatorname{Geom}(s),b\},
\qquad
s^2\mathbb E L^2\le\min\{s^2b^2,2\}.$ 

For two nearby parameters separated by  $\Delta u$ , a bounded-generator purification argument gives block root fidelity at least $1-\frac{\Delta u^2}{8}\min\{s^2b^2,2\}.$ 

This remains valid with a fresh reference. Summing the resulting distinguishability budget across blocks bounds information per source call by a constant times $\Delta u^2\,s\min\{sB,1\}.$ 

Two parameters separated by order  $d\epsilon$  have stationary expectations separated by more than  $2\epsilon$ . Distinguishing them yields the matching lower bound. The internal review also checked the decision-tree extension to adaptive block lengths and worst-case expected cost.

This result is internally reviewed, not externally accepted or priority established. Optimizing coherent interrogation time under noise has substantial metrology predecessors; those precedents prevent presenting probe retention itself as a new idea. The specific result developed here is the stationary-state learning law, its Choi-floor lower family, and the fully charged block-tomography construction. arxiv.org+1

2. The comparisons that changed the attack

The ordinary alternatives received the information supplied by the theory.

The old control example did not require stationary-gradient accuracy. Its one-event objective and stationary objective are positive multiples of the same cosine. They have identical maximizers. In twenty matched-cost runs, the one-event controller’s mean stationary regret was approximately 0.000118, versus 0.09036 for the full-history controller. The analytical identity is more decisive than the numerical comparison.

The whole-response Fourier construction was valid but expensive. Finite dependence gave a bound on stationary Fourier coefficients, $|c_k|\le
\Pr\!\left(K\ge\left\lceil |k|/r\right\rceil\right),$ 

and hence a uniformly reusable response model. The actual experiment charged unlabelled full-channel updates, preparations and measurements. Its conservative  $0.022$  uniform objective certificate corresponded to approximately 4.295 billion updates.

Ordinary full-process identification, using the supplied control placement, obtained a  $0.0147$  uniform objective certificate with approximately 975 million calls. At smaller budgets it also gave much better empirical accuracy. Short-horizon response fitting won another comparison after matching updates, preparations and measurements. Fourier surrogates and classical inference after quantum acquisition are already established machinery. arxiv.org

These were useful failures: geometry alone was paying for histories that barely affected the observable.

3. A completed intermediate operation: validate an observable equation

I then constructed and executed a different certificate. For any proposed Hermitian  $A$  and scalar  $a$ , define $R=O-aI-(I-T^*)A.$ 

Every stationary state of the actual channel satisfies $\operatorname{Tr}(O\rho)-a=\operatorname{Tr}(R\rho).$ 

Thus a measured operator enclosure for  $R$  bounds the stationary observable without requiring a reset promise, a mixing gap, uniqueness, or correctness of the nominal model.

The implemented acquisition separated training from validation. Training proposed the observable potential; independent ordinary process probes validated its residual using a matrix-concentration bound. The same validation data supported a uniform control certificate. Known-model stationary-state dual constraints and finite-shot certification have direct predecessors; the tested interface was validation against an unknown actual process. arxiv.org+2

This operation also lost its general three-qubit cost comparison: approximately 1.219 billion calls gave a global regret certificate of 0.0412, while the ordinary process comparator was stronger at that scale.

Its useful consequence was the next mechanism: $R_b=O-aI-\bigl[I-(T^*)^b\bigr]A.$ 

A block residual has the same stationary identity, but validation uses retained  $b$ -step probes. The new learning law explains when paying for that retention improves acquisition, rather than merely shifting expense between terms in a proof.

4. What is saved and what remains blocked

The earlier constructions, experiments, reviews and losing comparisons were saved before the runtime interruption:

   Observable-residual proof,   runnable experiment, and   executed results

Those experiments used synthetic grouped Born observations, not hardware runs.

The final block-learning theorem is stated above because its file save and new runnable verification remain blocked. The access context returned, but the executor still failed to start. Its proof has received internal mathematical review; it has not been counted as a saved or executed experiment.

The consequential change is now precise: an approximate stationary-state learning task can gain a factor of order  $\nu^{-1}$  by retaining one probe across source calls, with no need to expose or execute the source’s reset decomposition. The remaining hard questions are dimension dependence, useful observable-specific block selection, and the broader control architectures excluded by the present lower bound.

The final internal audit confirms the stated minimax law, including the general-dimensional lower bound and the fixed-point clipping construction.

One technical distinction is preserved: repeated blocks improve trace-distance contraction to  $(1-\nu)^b$ ; they do not generally amplify the depolarizing Choi floor to  $1-(1-\nu)^b$ . The proof uses contraction throughout. Priority review, the final file save and runnable verification remain open.   results.mdDocumentOpen file   full_response_comparison.mdDocumentOpen file   full_process_comparator.mdDocumentOpen file4 more
