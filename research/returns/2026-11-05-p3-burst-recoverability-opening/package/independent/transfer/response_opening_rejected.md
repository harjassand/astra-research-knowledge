# Independent transfer construction: response acquisition during continued operation

Date: 5 November 2026. Scientific status: derived conditional operation; rejected as the winning question after comparison with existing semiparametric system identification. No other participant's new proposal was consulted in choosing this route.

## Question tested

Can finite local dissipation and fresh private excitation replace quiet-start preparation while acquiring a reusable response predictor during continued operation, even with unknown hidden dimension, arbitrarily slow modes and bounded continuing energy influx? A stronger promised endpoint would be useful closed-loop competence or absolute future prediction without equilibration. The construction below earns the response operation but does not earn that stronger endpoint.

## Physical contract

The complete controlled plant is causal and LTI, with scalar force f, observed displacement x, v=dx/dt, and storage E>=0. For every interval its energy balance obeys

E(t)-E(s) <= integral_s^t f v - Gamma integral_s^t v^2 + D(s,t), Gamma>0.

Initial storage is at most E0. Exogenous supplied energy is bounded pathwise by D(0,T)<=P_heat*T. This is a new supplied power-bound premise when continuing influx is present, not a consequence of P2's finite-total-energy theorem. If displacement range is required, retain the loaded-port bound E>=k x^2/2. The zero-storage response to the probe exists. No finite hidden dimension or relaxation rate is needed for the following estimate.

Divide acquisition into M blocks of duration H. Before block k, choose a baseline command g_k and draw a fresh private sign s_k in {-1,+1}. Apply f_k=g_k+s_k p, where p is one specified bounded, smooth, finite-slew probe. The baseline command and external disturbance path for this block must be fixed or independent of the new sign conditional on the preceding history. All reaction of the linear plant to the new sign belongs to its forced response. Arbitrary additional disturbances that adapt to the sign within the block are not covered.

Let J bound integral_0^H (g_k +/- p)^2 for either sign and every block, and let J_probe=integral p^2. Those bounds charge continuing operation and excitation together.

Use a linear displacement observation formed by the difference of two finite time averages within the same block. If both averaging windows lie in [0,H], its magnitude is at most sqrt(H) times the block L2 norm of v. Several such observations can be taken, indexed j=1,...,L. Difference-of-averages avoids an ideal instantaneous position measurement. Its zero-state response a_j is fixed across blocks.

## Constructed operation and proof

Linearity gives exactly

Y_kj = s_k a_j + z_kj,

where z_kj is independent of the new sign conditional on prior information (equivalently predictable in an enlarged filtration containing the block's precommitted disturbance). Let

a_hat_j = (1/M) sum_k s_k Y_kj.

The energy inequality and Young's inequality give

integral_0^(MH) v^2 <= 2 E0/Gamma + M[2 P_heat H/Gamma + J/Gamma^2].

For the mathematical zero-state probe, passivity gives integral v_p^2 <= J_probe/Gamma^2. It follows, simultaneously for all sign histories, that

sum_k z_kj^2 <= Q_M,

Q_M = 4 H E0/Gamma + M[4 P_heat H^2/Gamma + 2 H(J+J_probe)/Gamma^2].

Indeed sum Y_kj^2 is at most H times the actual velocity-energy bound, a_j^2 <= H J_probe/Gamma^2, and z_kj^2 <= 2Y_kj^2+2a_j^2. The exponential martingale for s_k z_kj then proves

Pr(max_j |a_hat_j-a_j| > sqrt(2 Q_M log(2L/delta))/M) <= delta.

If each reported linear observation has an arbitrary error bounded by eta, add eta to the displayed radius. No stochastic sensor-noise assumption can remove that systematic floor. Bounded current-block force-tracking error contributes an additional zero-state response error bounded through the same induced L2 gain; previous tracking errors belong to the predictable baseline.

Writing Q_M=A+BM, a sufficient trial count for error epsilon above the metrology floor is

M >= max{2 sqrt(A log(2L/delta))/epsilon, 4 B log(2L/delta)/epsilon^2}.

The physical operation therefore does not need an off period, equilibrium preparation or a bound on the slowest mode. It does pay M H time, the continuing baseline and probe energy, M private signs, M L metrology observations and finite running sums. The input-power convention, causal independence, physical actuator and metrology interfaces remain substantive. Merely continuing the baseline command does not prove that every useful service requirement remains satisfied under the perturbations; that needs an actual task margin or robust operating guarantee.

## Reuse and exact limit of the result

The estimate is for a forced response functional. The zero-state probe response is Holder-continuous with modulus at most sqrt(J_probe)/Gamma times sqrt(|t-s|). A finite grid plus averaging-window/anchor error bounds can therefore yield a finite-horizon response table. If future allowed controls are sums of translated probe waveforms with coefficient absolute sum at most B_var, a uniform response error epsilon gives forced-component error at most B_var*epsilon, on one common acquisition event. The exact finite averaging convention must be retained when making this deduction.

This does not predict an arbitrary future free continuation. Continuing exogenous energy influx can cause later unannounced visible motion. Removing that uncertainty requires a separate physical premise or operation. Likewise it does not supply unrestricted infinite-horizon closed-loop performance from a finite acquired response window.

## Primary kill-test

Simchowitz, Boczar and Recht (2019), *Learning Linear Dynamical Systems with Semi-Parametric Least Squares*, COLT/PMLR 99, already formulate y_t=G u_t+delta_t with predictable delayed nuisance, and estimate the finite response without a worst-case mixing-time dependence. Their general regression theorem does not require a finite hidden realization; their specialized dynamical results cover partially observed marginally stable systems and stochastic or worst-case disturbances. In the general theorem, a nuisance matrix with norm O(sqrt(M)) gives an O(M^-1/2) rate. Our dissipation inequality supplies precisely such a nuisance bound. Fresh random excitation and cancellation of a predictable baseline are therefore established central machinery. The physical energy-bound instantiation is not evidence of a major new mechanism.

Primary source: https://proceedings.mlr.press/v99/simchowitz19a.html
Full paper: https://proceedings.mlr.press/v99/simchowitz19a/simchowitz19a.pdf
Relevant locations: equation (1.1), Theorem 1.1 and its discussion; these explicitly expose the nuisance-norm dependence. Browser references retrieved by this constructor: turn34search0, turn39view0. Parent must open a source before citing its reference.

Related primary sources:
- Simchowitz et al. (2018), *Learning Without Mixing*, https://proceedings.mlr.press/v75/simchowitz18a.html (turn34search1).
- Mania, Jordan and Recht (2022), *Active Learning for Nonlinear System Identification with Guarantees*, https://www.jmlr.org/beta/papers/v23/20-807.html (turn26view2). Its known finite feature embedding is a substantive different premise.
- Classical worst-case fading-memory identification already pays exponential history-covering complexity without added structure: full primary paper retrieved at https://citeseerx.ist.psu.edu/document?doi=60ddf9b5995eecbaaef3a26150ea0f74fa02fa82&repid=rep1&type=pdf (turn26view3, especially the concluding complexity discussion). No general nonlinear escape is inferred here.

## A concrete obstruction to the stronger promise

A passive delay line with reflection factor r has scattering response b(t)=r a(t-tau), with |r|<1 and zero initial field. Storage in the traveling field satisfies dS/dt <= |a|^2-|b|^2. A matched termination has r=0. The two devices give exactly the same observations before time tau, for every bounded adaptive input started from zero. This remains true with perfect measurements and no unknown initial energy.

In force-velocity variables a reference impedance c>0 converts the delayed reflection to the positive-real impedance

Z_line(s)=c(1+r exp(-s tau))/(1-r exp(-s tau)).

Attach the same local damper Gamma and permanent spring k to both alternatives:

Z_total(s)=Gamma+k/s+Z_line(s).

Their complete storage obeys the loaded-port inequality with E>=k x^2/2 and local dissipation Gamma v^2. Thus this is a real bridge to the loaded LTI class, not a conflation with the productive Markov model.

Let a0=Gamma+c. For a unit force step, on the first-return interval tau<t<2tau the displacement difference from the matched load is exactly

x_r(t)-x_0(t) = -(2 c r/a0^2)(t-tau) exp[-k(t-tau)/a0].

At t=tau+a0/k, provided tau>a0/k, its magnitude is 2cr/(a0 k e). A finite-slew exponential ramp replaces this expression by convolution with a positive narrow exponential kernel, retaining a constant-size separation. In particular a ramp time ell<=a0/(10k) retains at least cr(1-exp(-5))/(a0 k e) at that time. The two plants still agree exactly before tau.

Consequently finite acquisition independent of the hidden delay cannot certify every future forced response or arbitrary long-horizon feedback performance. The large delay has real hardware/propagation extent; neither its presence nor its absence follows from local passivity. A declared finite task horizon is a genuine resource convention.

## Selection judgment

Preserve the finite response-acquisition theorem as a useful conditional companion. Reject it as the winning scientific question: its central statistical operation is available in strong existing semiparametric identification, and the full future/control consequence is not earned. The strongest remaining obstacle is not a better estimator or concentration constant; it is a physically justified finite causal-memory or task-relevant predictability condition that permits a consequential control operation while retaining continued operation, noise and full acquisition costs. No such new sufficient condition or complete controller is claimed by this route.
