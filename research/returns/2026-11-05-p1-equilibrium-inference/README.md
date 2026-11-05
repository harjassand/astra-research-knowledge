# Inferring equilibrium before relaxation: a joint minimax effort law

The supplied, internally audited result determines the logarithmic minimax effort for estimating one equilibrium response from short scalar-port experiments on a reciprocal passive system. It includes an explicit finite-ramp experiment and positive finite hard systems that obstruct every permitted adaptive controller. The result establishes a theoretical resource law at its stated scope; practical acceleration, historical priority and civilisation-changing consequence remain unestablished.

Read the [complete report](package/equilibrium_inference_20261105.pdf), [editable proof](package/equilibrium_inference_20261105.tex), [independent approximation derivation](package/passive_programme/bandwidth_accuracy_theorem.md), [internal audit](package/passive_programme/independent_audit.md), [attaining experiment and full costs](operation-and-costs.md), and [separate quantum companion](quantum-companion.md). The [original ZIP](original/equilibrium_inference_20261105_package.zip), [complete captured return](P1_EQUILIBRIUM_INFERENCE_20261105_RETURN.txt) and [publication provenance](SOURCES.json) retain the supplied evidence.

The separate [local thermal-trial theorem](../2026-11-05-p2-local-thermal-trials/README.md) prepares a known randomized local input while keeping an unknown hidden ensemble. It has fresh-thermostat and reference-inclusive entropy premises and does not supply the zero-state trials granted by the minimax sensor-noise inference interface here. Its continuous heat and meter services must not be silently imported into this theorem or its upper-only thermal extension.

P1 later nominated a separate [three-dimensional thermal-memory opening](../2026-11-05-p1-thermal-memory-opening/README.md), with a source-conditional full-syndrome history compiler and reference-preserving loading operation. Existing sampler applicability and practical access remain unresolved; this is a new question selection, not a strengthening of the scalar-port inference theorem here. Earlier quantum and partial-SWAP results keep their own scopes.

## Model, access and target

The unknown system is `x'=-Ax+bu, y=b^T x`, with symmetric A, supplied bounds `mu I<=A<=Lambda I`, supplied `||b||=1`, and unknown hidden dimension, eigenvalues and modal weights. Its impulse response is a positive spectral mixture

```text
k_nu(t)=integral_[mu,Lambda] exp(-lambda t) dnu(lambda),
S(nu)=mu b^T A^-1 b=integral mu/lambda dnu(lambda),
kappa=Lambda/mu,     S in [1/kappa,1].
```

Each trial starts at zero, observes transients no older than T, and supplies `dY=(k_nu*u)dt+sigma dW`. Sensor noise is parameter-independent Gaussian noise, independent between trials. Inputs may use all past observations and feedback within a trial; computation and classical memory are unrestricted. Total squared-drive effort has an almost-sure cap:

```text
E=sum_trials integral u(t)^2 dt,     B=E/(sigma^2 mu^2).
```

Squared-drive effort is distinct from thermodynamic port work `integral uy dt`. T bounds transient age, not total laboratory time, repetitions or reset time. The theorem grants known rate bounds, coupling normalization and zero-state trials; arbitrary hardware calibration and fast resets are not derived.

## Uniform joint law and crossover

Let B_star be the least worst-case normalized effort for absolute error epsilon with success probability at least 3/4, uniformly over this class. With `s=mu T`, `L=log(1/epsilon)`, the report proves, for `0<s<=1/64`, `16<=kappa<=infinity`, and `0<epsilon<=1/16`,

```text
log(1+B_star)=Theta(Phi),
Phi=sqrt(kappa) L log(1+L/(s sqrt(kappa))).
For the unbounded upper-rate class: Phi=L^2/s.
```

The universal multiplicative constants apply to the logarithm of effort, not to effort itself. At fixed finite rate range and accuracy, sufficiently short horizons have polynomial inverse-horizon effort. When `s sqrt(kappa)` is comparable to or larger than L, the logarithmic cost reaches order `L^2/s`, allowing exponential inverse-horizon effort. The hard systems' fastest allowed rates and hidden order grow as the horizon shrinks in that latter family. A blanket exponential-in-1/T statement for a fixed rate range would be incorrect.

## Positive hard pairs and the adaptive converse

Classical reciprocal approximation gives

```text
E_m(K)=inf_deg(p)<=m ||1/x-p(x)||_[1,K]
      =(K-1)/(2K) * ((sqrt(K)-1)/(sqrt(K)+1))^m.
```

Alternation and interpolation produce two positive probability measures with equal moments through degree m and target gap `2 E_m(K)`, using m+2 support points in total. This is established approximation machinery, credited in the [source register](package/sources.json), rather than a newly invented reciprocal formula. A simple example is `nu_+=0.8 delta_1+0.2 delta_16` and `nu_-=delta_4`: equal mass and first moment, with S=0.8125 and 0.25 respectively.

The general construction matches enough moments that its whole-interval early kernel difference is exponentially small in Phi, while its target gap exceeds 4 epsilon. If that difference is at most eta, then

```text
||(Delta k)*u||_L2[0,T] <= T eta ||u||_2,
KL(P_+ || P_-) <= eta^2 T^2 E/(2 sigma^2)
               = eta^2 s^2 B/2.
```

On a common observed history a causal policy chooses the same input under both hypotheses. Gaussian change of measure therefore covers feedback, nonlinear estimators, adaptive trial allocation and full system identification. The almost-sure effort cap supplies the required integrability, with bounded stopping/localization for unbounded trial-count presentations. Extra hidden-state access, a known small model order, changes to A, or informative thermal fluctuations change this interface.

## Acceptance and attribution

The supplied [completed internal audit](package/passive_programme/independent_audit.md) found no central gap under these quantifiers and checked the main mathematical steps and compiler, plus a separate 120-case scalar challenge. That review supports acceptance at its actual internal scope. Capital ran no new scientific audit or numerical replay.

The attaining construction belongs to ordinary Chebyshev/optimal extrapolation; it does not outperform that comparator. Brown and Grabovsky's completely monotone extrapolation, Donoho's optimal recovery, and classical reciprocal approximation are especially relevant and explicitly credited. Specialist comparison is still needed for priority of this exact combined law. Waiting for relaxation can be cheaper when a longer observation window is available. The [earlier quantum compressor and general loss ledger](../2026-11-05-p1-joint-recovery/README.md) remain at their earned scope; their unrestricted joint memory/processing law is still open. Generated current retrieval was not rebuilt.
