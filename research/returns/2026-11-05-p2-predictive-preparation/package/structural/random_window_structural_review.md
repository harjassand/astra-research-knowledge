# Structural review of the random-window passive predictor

## Finding

The proposed random-window endpoint survives the missing-interface tests provided the physical plant has linear superposition, a genuinely unforced idle operation, and a known coercive quadratic storage with visible dissipation. It does not need a microscopic damping gap, a finite hidden dimension, a spectral bandwidth bound, a known memory kernel, or bounded total oscillator coupling. These last claims concern the abstract storage class below; they are not claims that its physical premises can be inferred from short data.

The decisive change from the earlier nonlinear passive bridge is to acquire the zero-state STEP RESPONSE directly and randomize the deployment time. Step-response convolution and energy averaging are standard ingredients. The distinct operation to assess is their composition with finite physical measurements on a retained unknown state, followed by a simultaneous guarantee for every admissible future input. No priority claim is established by this review.

## 1. A coordinate-free sufficient premise

Let an autonomous LTI passive plant have observed coordinate x, input force u and quadratic nonnegative storage H. Assume

\[
H\ge\frac\kappa2|x|^2,
\qquad\dot H\le u\dot x-\gamma\dot x^2,
\qquad \kappa,\gamma>0.
\tag{1}
\]

Zero state has x=H=0. The current retained state has H<=E, supplied independently of the observations used in this run. A quadratic state-space realization is one concrete meaning of linearity and storage; the hidden state may be infinite-dimensional. A merely nonlinear passive law does not provide the superposition step below.

Two consequences of (1) are immediate:

\[
u=0\Longrightarrow\int_0^\infty\dot x^2dt\le E/\gamma;
\quad
H(t)\le H(0)+\frac1{4\gamma}\int_0^t u^2ds.
\tag{2}
\]

Thus a finite actual probe has a paid energy increment. No claim is made that every hidden mode loses its energy.

## 2. The zero-state step is regular without a spectral bound

Let S be the coordinate response to unit force starting from zero state. During that constant input, the shifted storage H-x+1/(2kappa) is nonnegative because H>=kappa x^2/2. Its derivative is at most -gamma S'^2. Therefore

\[
\int_0^\infty |S'(t)|^2dt\le\frac1{2\gamma\kappa},
\quad
|S(t)-S(s)|\le\sqrt{\frac{|t-s|}{2\gamma\kappa}}.
\tag{3}
\]

The extension S(t)=0 for t<0 has the same Holder bound because S(0)=0. This yields finite uniform approximation by a time grid. The grid count is O(T/(gamma kappa eta^2)) for step-response accuracy eta. It is a sufficient count, not a claimed optimal count over the passive class.

A positive finite ramp of width h produces A int rho(s) S(t-s) ds, with rho>=0 and integral one. Its normalized difference from S is at most sqrt(h/(2gamma kappa)). A positive position-average window of width w contributes at most sqrt(w/(2gamma kappa)). Finite clock uncertainty produces the same square-root modulus. The experiment can therefore learn S without deconvolution, point sampling, velocity measurement or a supplied kernel oracle.

## 3. A private random window suppresses unknown initial output

For disjoint idle windows I_j of common length D, let

\[
L_j=\operatorname{osc}_{I_j}x.
\]

By Cauchy--Schwarz, L_j^2<=D int_{I_j}xdot^2. Thus the number with L_j>delta is at most ED/(gamma delta^2). If J is uniform on N windows and independent of the initial state,

\[
\Pr(L_J>\delta)\le\frac{ED}{\gamma N\delta^2}.
\tag{4}
\]

The physical protocol waits unforced to the chosen window, takes its baseline and probe there, and uses the unforced trajectory on that window as a counterfactual free response. The observed forced response is this same free response plus the zero-state response by LTI superposition. The unforced counterfactual is mathematically fixed before J, even though the actual probe changes the subsequent state.

Use a power-of-two N to generate J with exactly log2 N private unbiased bits. This gives finite randomization and a deterministic maximum waiting time. The clock, baseline, ramp and final averaging window all belong inside the charged window length D. A fresh private J is needed after a probe; condition on the retained state and use its updated energy bound.

The successful-window event is not an observed stopping certificate. A quiet past does not certify that its particular future is quiet. Equation (4) is a confidence guarantee over private timing for every fixed admitted initial state. It remains compatible with a delayed-echo impossibility at a prescribed deployment time.

## 4. The all-input endpoint

For a later force of bounded variation, extended by zero before time zero, the zero-state coordinate response is

\[
x_u=S*du.
\tag{5}
\]

The jump from zero to u(0), if allowed, is included in the variation measure. A physical finite rise can instead be part of the actual input program. If ||S-Shat||infinity<=eta, then

\[
\|x_u-\widehat S*du\|_\infty\le\eta\,\operatorname{TV}(u).
\tag{6}
\]

On a fresh quiet deployment window, the free response differs from its observed initial level by at most delta. Adding baseline metrology and finite numerical convolution errors gives the actual trajectory certificate. The successful event is independent of the selected future input, so all counterfactual BV inputs in the declared variation ball share that event, even if selected after calibration.

No physical replay is inferred. Executing an input changes the retained state; the next actual deployment requires an updated energy account and its own window. A bounded force-amplitude promise alone does not bound total variation; actuator slew, horizon, and a finite program must supply the admitted input family.

## 5. Force-delivery errors and an important idle caveat

For a zero-state response to any force error w, completing the square in (1) gives

\[
\|\delta x\|_{\infty,[0,T]}
\le\frac{\|w\|_{L^2(0,T)}}{\sqrt{2\gamma\kappa}}.
\tag{7}
\]

This pays bounded active-drive error without assuming its time derivative or variation.

The idle operation must actually set u=0, or its total supplied energy must be counted. A persistent idle error bounded by xi over a wait W adds at most W xi^2/(4gamma). Substitution into the elementary energy-counting argument leaves a failure floor of order D^2 xi^2/(gamma^2 delta^2), rather than tending to zero with waiting. A physically locked viscous-support anchor provides a concrete zero-drive implementation in the mechanical architecture. It is stronger than saying a moving actuator's residual force is merely small.

At fixed actuator acceleration, shortening a ramp may require reducing its amplitude. For the elementary step approximation h=O(gamma kappa eta^2), a fixed acceleration cap can force A=O(h). Position calibration bias divided by A then imposes a real floor. Repetition reduces independent readout noise, not systematic bias. These are costs of the complete operation, not reasons to hide a discontinuous ideal step.

## 6. Comparison with strong existing approaches

The full sources below were inspected, including their main theorem conditions.

- Simchowitz et al., Learning Without Mixing (2018), establishes near-minimax OLS identification from a single observed trajectory without mixing-time arguments. It does not make the general idea of learning without mixing new. https://proceedings.mlr.press/v75/simchowitz18a.html
- Hazan et al., Spectral Filtering for General Linear Dynamical Systems (2018), gives online squared-error regret with no spectral-radius gap. Its constants depend on system dimension, bounded system matrices, diagonalization conditioning and a polynomial annihilating eigenvalue phases. It predicts the next output using past inputs and outputs. This is a stronger ordinary comparison than generic microscopic reconstruction. https://papers.nips.cc/paper_files/paper/2018/file/d6288499d0083cc34e60a077b7c4b3e1-Paper.pdf
- Hazan and Marsden, Spectral Filtering for Learning Quantum Dynamics, arXiv:2601.22400v1, studies a finite-window W convolution in linear response with sector-bounded discrete-time eigenvalues, and supplies cumulative squared prediction-error guarantees. The response equation and Theorem 5.1 explicitly use noiseless finite-window dynamics. It does not itself supply preparation from an arbitrary retained hidden energy state or a simultaneous physical guarantee for all future inputs. https://arxiv.org/html/2601.22400v1
- Shah et al., SpectraLDS (2025), learns/compiles symmetric LDS spectral representations with dimension-independent approximation structure. Its stated distillation bound retains the norm of a pseudoinverse. Section 5.3 treats a bounded pseudoinverse factor under overparameterization as experimentally supported. Do not erase that factor when comparing worst-case guarantees. https://arxiv.org/html/2505.17868v1
- Schadle, Lopez-Fernandez and Lubich, Fast and Oblivious Convolution Quadrature (2006), already gives O(N log N) arithmetic and O(log N) active memory from sectorial Laplace-transform access. Efficient memory convolution is established machinery. https://arxiv.org/abs/math/0504461
- Bockius et al. (2021) and Lei--Baker--Li (2016) already construct reduced Markov or rational GLE models from correlation data, including oscillatory response and positive-real realization. Their input data, equilibrium/statistical scope and model access must be compared to the actual random-window experiment. https://arxiv.org/abs/2101.02657 and https://pmc.ncbi.nlm.nih.gov/articles/PMC5167214/

The candidate's potentially distinct consequence is the energy-priced random timing plus finite step experiment and uniform future-input guarantee, independent of hidden order and microscopic damping. This review establishes that the proposed mathematical composition is coherent under its premises; it does not establish historical priority, optimal acquisition complexity, or civilisation-changing practical impact.
