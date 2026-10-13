# CRAY GENESIS — Thermodynamic conjugation for chemical sensitivity acquisition

Research date: 13 October 2026.

## Status

This packet contains a mathematical construction, proofs, exact counterexamples and executable synthetic checks. It does **not** establish a new practically consequential scientific capability, a physical experiment, a speedup over a specialised solver, or historical priority. The strongest constructive result is a kinetic-constant-free chemical conjugation and adjoint-readout operation under an explicit additional condition. Saturating enzyme kinetics generally violate its assumptions. A subsequent matched-task comparison also shows that the simpler finite-relocation construction already reaches all target states in the same nonzero-affinity cell under a total gate budget alone; the adjoint has not been shown to add a needed capability for that task.

The user's Astra repository was read at revision `74c2843bd224c2975c6e46735b30ae7c927f948b`. OpenAI/math was consulted for orientation, not used as an unverified theorem oracle. No repository was modified. No claim of exhaustive archive or literature review is made.

## 1. Exact task and acquisition contract

The target is local improvement of a prescribed differentiable **state-dependent** objective Phi(c) in a driven chemical system. Examples include a selected product concentration or a product/byproduct concentration ratio. This is not automatically a throughput, flux-selectivity, or global-optimality result.

The system is an isothermal, well-mixed, ideal mass-action model with n internal species and m reversible reaction pairs. Write the full concentration vector z=(c,u), with u externally maintained reservoirs. Reaction r has full reactant and product vectors a_r,b_r, internal parts y_r,y'_r, and internal change s_r=y'_r-y_r. All positive gates e_r are independently adjustable and multiply both directions equally:

\[
v_r^+=e_r k_r^+z^{a_r},\qquad v_r^-=e_r k_r^-z^{b_r},\qquad
j_r=v_r^+-v_r^-,\qquad F(c)=\sum_r s_rj_r.
\]

The acquisition interface consists of the known full stoichiometry; measured positive native steady concentrations z; calibrated gates e; and a measured or independently justified positive full detailed-balance reference q satisfying

\[
k_r^+q^{a_r}=k_r^-q^{b_r}=\kappa_r.
\]

The absolute constants k_r^+, k_r^-, kappa_r and baseline currents j_r are **not supplied to the controller**. They may still be used by a simulator to check a proposed controller, as in verify.py. The experiment must be able to set all required reservoirs and gates and prepare/read internal concentrations. These are major physical requirements, not free input oracles.

The full reference q need not be the operating state. Indeed, different reservoirs can maintain a nonequilibrium operating steady state. Assuming q does not establish that q can be obtained cheaply or that missing reactions are absent.

We treat an open system with full internal stoichiometric rank. Closed conservation classes need a restricted-coordinate treatment, which is not supplied here. We do not apply a nonsingular inverse to a closed-system Jacobian.

## 2. The exact conjugation

Let w=z/q componentwise and define

\[
\boxed{z^\dagger=q^2/z,\qquad e_r^\dagger=e_r w^{a_r+b_r}.}
\]

Then, without knowing kappa_r,

\[
v_r^{\dagger,+}=e_r\kappa_r w^{a_r+b_r}w^{-a_r}
=e_r\kappa_r w^{b_r}=v_r^-,
\]

and similarly v_r^{dagger,-}=v_r^+. Thus every elementary current is reversed. If c is a native steady state, the internal part d=q_internal^2/c of z^dagger is a steady state of the conjugate reactor:

\[
F^\dagger(d)=-F(c)=0.
\]

The unknown absolute reaction constants genuinely cancel. The gate recipe depends on full stoichiometry, including reservoirs. Omitting the reservoir factors is incorrect.

### Thermodynamic consistency

For dimensionless affinity A_r=log(v_r^+/v_r^-), conjugation gives A_r^dagger=-A_r and j_r^dagger=-j_r. Hence

\[
\sum_r j_r^\dagger A_r^\dagger=\sum_rj_rA_r\ge0.
\]

At the paired operating states, dimensionless dissipation is unchanged. This is not thermodynamic time reversal and does not extract energy from equilibrium. Reservoir provisioning, circulation, gate adjustment and state preparation remain real costs.

## 3. Current reversal is not generally an adjoint

Let J=DF(c), H=DF^dagger(d), C=diag(c), D=diag(d). Define

\[
M=\sum_rj_r\left(y'_ry_r'^T-y_ry_r^T\right).
\]

Then

\[
\boxed{CJ^T=HD+M.}\tag{1}
\]

**Proof.** Mass action gives

\[
JC=\sum_rs_r(v_r^+y_r^T-v_r^-y_r'^T),\qquad
HD=\sum_rs_r(v_r^-y_r^T-v_r^+y_r'^T).
\]

For a single pair, subtract the second term from the transpose of the first. Using s=y'-y, the result is (v^+-v^-)(y'y'^T-yy^T). Sum over r. No equilibrium, stability, sparsity or small-affinity approximation is used.

Equation (1) isolates exactly what the physical construction fails to provide. Flux reversal alone is insufficient, even when both reactors are stable and all rates are positive.

### Sufficient condition and acquisition of the condition

If M=0, the exact weighted-transpose relation holds. Complex balance of the **internal-complex graph** is sufficient: when every complex has equal total incoming and outgoing reaction flow, grouping the terms in M by complex makes every coefficient vanish. This is not the same as detailed balance of every pair, and circulating steady currents may be nonzero.

M=0 is strictly weaker than complex balance at a particular state. For example, complex imbalances (-1,3,-3,1) on 0,X,2X,3X have vanishing zeroth, first and second moments but third moment 6. This formal higher-order example is not an elementary-chemistry demonstration.

Do not infer complex balance from species balance Sj=0. They are different conditions. To avoid assuming unknown currents, a sufficient acquisition-free structural test is available. Let S have columns s_r, and let R have columns vec_sym(y'_ry_r'^T-y_ry_r^T). Then

\[
\ker S\subseteq\ker R
\]

is equivalent to the existence of L with R=LS. If it holds, Sj=0 implies M=0 for every possible current vector. This is an exact rational linear-algebra test on supplied stoichiometry, not a low-rank approximation. Building R and doing rank tests has nonzero preprocessing and memory cost; the controller's sparse arithmetic cost does not include these for free. The test is sufficient for an actual steady state, and necessary only for the stronger property involving *every* current in ker S. Failure of this test does not prove that M is nonzero at the operating state.

Alternatively, a justified structural complex-balance theorem for a specific network may establish the condition. Neither a few measured currents nor a few passing simulations establishes it for an unknown real network.

## 4. Stability follows algebraically under the stated condition

Set

\[
B=\sum_r(v_r^++v_r^-)s_rs_r^T.
\]

Direct expansion gives

\[
JC+CJ^T+B=M.\tag{2}
\]

When M=0 and span{s_r}=R^n, B is positive definite because all one-way rates are positive. Thus

\[
JC+CJ^T=-B,\qquad HD+DH^T=-B.
\]

Since C,D are positive definite, both J and H are Hurwitz, by applying the standard Lyapunov criterion to J^T,H^T. This provides local stability and invertibility. It does not supply a numerical decay rate, a global basin, or an upper bound on the time required to reach the steady state. The absolute rates still control those costs.

## 5. Physical acquisition of a decision-specific adjoint

Choose a=grad_c Phi(c). Hold the compiled conjugate controls fixed and add a small calibrated constant signed source epsilon C a to its internal dynamics. Let d(epsilon) be the nearby equilibrium branch. The implicit-function theorem gives

\[
H d'(0)+Ca=0.
\]

Under M=0, define

\[
\boxed{\lambda=D^{-1}d'(0).}
\]

Then CJ^T lambda=HD lambda=-Ca, hence

\[
J^T\lambda=-a.
\]

A chemical response has supplied the adjoint needed for the selected output, without fitting J or all rate constants. A baseline plus one-sided perturbation is a limiting mathematical operation; a practical central estimate requires equilibria at both positive and negative source amplitudes and their concentration readouts. An n-component observation is not one scalar measurement.

Signed constant sources must be physically implemented. Withdrawal proportional to concentration is a different perturbation and changes the Jacobian. A target d may also be unreachable under the available preparation controls.

## 6. A rate-free ascent law and its exact limits

Let theta_r=log e_r. Because the gate scales both reaction directions,

\[
\frac{\partial\Phi}{\partial\theta_r}=j_rs_r^T\lambda.\tag{3}
\]

The affinity

\[
A_r=(a_r-b_r)^T\log(z/q)
\]

is available from the input interface. Its sign equals the sign of j_r. Set

\[
u_r=A_rs_r^T\lambda.
\]

Then

\[
\frac{d\Phi}{dt}=\sum_rj_r A_r(s_r^T\lambda)^2\ge0
\]

under the formal quasistatic update theta_dot=u. Unknown current magnitudes are not needed to choose this ascent direction.

For a fixed **linear gate budget** E=sum_r omega_r e_r, define

\[
\bar u=\frac{\sum_r\omega_re_ru_r}{E},\qquad
\boxed{\dot\theta_r=u_r-\bar u.}
\]

This preserves E. Moreover, sum_r partial_Phi/partial_theta_r=lambda^T F(c)=0, so subtracting bar u does not change the nonnegative objective derivative.

An implementable finite update is

\[
e_r^{new}=\frac{E\,e_r\exp(h u_r)}{\sum_s\omega_se_s\exp(h u_s)}.
\]

It preserves the budget exactly. Strict positive directional derivative ensures improvement for a sufficiently small step, but the theorem does not give a computable safe step without curvature information or measured backtracking.

**Limits.** All dynamics must be included in the collectively scalable gates. Uncontrolled inflows, dilution or background reactions generally invalidate the budget projection. Phi must depend only on c; a flux objective with direct gate dependence requires an additional term. This is local ascent, not a global optimum. A state-specific M=0 need not persist after a step. Gate cost equals total enzyme-protein cost only when a justified physical model makes them proportional; this is false in the occupancy-clamped extension discussed below.

## 7. Exact wrong-sign counterexample

Use two internal species and reversible pairs

\[
0\rightleftharpoons2A,\qquad A\rightleftharpoons B,\qquad B\rightleftharpoons0.
\]

At c=(1,1), take forward fluxes (2,3,3), backward fluxes (1,1,1), and unit baseline gates. Each pair can have a separate reversible fuel/waste reservoir, with unit reference q and equal microscopic forward/reverse constants. Net currents are (1,2,2), giving F=0.

The native and conjugate Jacobians are

\[
J=\begin{pmatrix}-7&1\\3&-4\end{pmatrix},\qquad
H=\begin{pmatrix}-9&3\\1&-4\end{pmatrix},\qquad
M=\begin{pmatrix}2&0\\0&0\end{pmatrix}.
\]

Both Jacobians are Hurwitz. For Phi=A+(3/5)B, the true log-gate derivative for A<->B is

\[
-6/125=-0.048.
\]

The uncorrected conjugate-adjoint prediction is

\[
2/55\approx0.03636.
\]

It recommends the wrong direction. verify.py checks this with exact rational arithmetic, not a numerical sign inference.

## 8. Saturation exposes the central remaining physical obstruction

Consider reversible Michaelis-Menten-type one-way rates

\[
v^+=e\kappa s/Z(s,p),\qquad
v^-=e\kappa p/Z(s,p),\qquad
Z=1+s/K_S+p/K_P,
\]

with net equilibrium ratio one. At (s,p,e)=(2,1,1), both of these models have exactly the same forward/backward fluxes (2,1):

- K_S=K_P=1 and kappa=4;
- K_S=K_P=10 and kappa=13/10.

The mass-action conjugation sets (s^dagger,p^dagger,e^dagger)=(1/2,1,2) and predicts net current -1. The actual currents are respectively -8/5 and -26/23. Thus even identical baseline concentrations, thermodynamics, gates **and one-way fluxes** do not determine the transformed response under unknown saturation.

More generally, suppose a reversible pair has a common positive denominator Z_r(z). Net current reversal can be recovered at a selected state by multiplying the mass-action gate recipe by Z_r(z^dagger)/Z_r(z). That ratio is new information; it cannot be assumed known.

Even this is not enough for the adjoint. Define internal logarithmic denominator elasticities ell_r=grad_log_c log Z_r and ell_r^dagger=grad_log_d log Z_r. With gates fixed after the corrected compilation,

\[
CJ^T-HD
=M-\sum_rj_r\left(\ell_rs_r^T+s_r(\ell_r^\dagger)^T\right).
\]

Hidden saturation therefore changes both the required gate setting and the transpose defect. Measuring a single denominator ratio does not remove the derivative obstruction.

### Attempted constructive rescue: free-enzyme clamping

There is a narrow exact rescue, but it is not established as a new capability. Suppose a module has one exposed free-enzyme state E, hidden states h, and substrate/product binding only from E. All hidden transition rates and return rates are independent of s,p. With free-enzyme concentration f clamped,

\[
\dot h=Qh+f(b_s s+b_p p),
\]

where Q is a stable transient generator. At steady state, h=-fQ^{-1}(b_s s+b_p p), and the product current has the form j=f(alpha s-beta p). Thermodynamic consistency relates beta/alpha to the known net equilibrium constant. Hidden-state elimination is exact at steady state; no fast-timescale approximation is needed for this algebraic statement.

Consequently, clamping the free active enzyme rather than its total amount restores effective mass action for this restricted module. However, sensing and controlling f for every enzyme is an additional physical interface. Full coupled/clamp stability and settling time are not proved by the reduced steady-state calculation. The total enzyme cost is f+1^T h, not f. Also, this class already admits a low-parameter Michaelis-Menten description through established linear elimination. It is unfair to compare the proposed clamp only against identifying every hidden microscopic rate.

Multiple binding-competent free states, additional concentration-dependent internal transitions, unmeasured driven cycles, shared pools and enzyme-enzyme interactions are outside this rescue.

## 9. A second operation: finite flux-preserving relocation

Independently of the adjoint condition, a mass-action network allows a finite state relocation with no absolute kinetic constants. Keep reservoirs fixed, set c'=c exp(h), and consider a channel with nonzero j_r. Let A_r be its native affinity. Then

\[
\boxed{\rho_r(h)=\frac{e'_r}{e_r}
=\frac{1-e^{-A_r}}
{e^{y_r^Th}-e^{-A_r+y_r'^Th}}.}
\]

Substitution shows j'_r=j_r. Thus a steady native state gives a steady target state without measuring the individual current magnitudes. Positivity requires that A_r-s_r^Th retain the original sign. A zero-current channel requires s_r^Th=0; its formula is not evaluated as 0/0.

Orient nonzero channels so A_r>0. Then

\[
\log\rho_r=-y_r^Th+\log(1-e^{-A_r})
-\log(1-e^{-(A_r-s_r^Th)}).
\]

This is convex on the thermodynamically feasible halfspace, so the linear enzyme/gate cost sum omega_r e_r rho_r(h) is convex. Scaling every relocated gate by gamma scales all currents by gamma, and under an exactly linear total gate budget the supremal common throughput multiplier is the available budget divided by the infimum relocation cost. It is attained only when an admissible minimiser exists, for example under suitable compact bounds away from forbidden affinity faces. This preserves the entire flux-ratio pattern; it cannot design new flux selectivity.

### Stronger matched-task consequence: the simpler operation can make the adjoint unnecessary

For any admitted h, write B(h)=sum_r omega_r e_r rho_r(h) and E=sum_r omega_r e_r. The explicit controls

\[
\boxed{e'_r=\frac{E}{B(h)}e_r\rho_r(h)}
\]

have exactly the original total gate budget, and at c'=c exp(h) the entire current vector is (E/B(h))j. Therefore F(c')=0. When all relevant native currents are nonzero, **every** target in the same affinity-sign cell is constructively reachable under this budget-only model. Zero-current channels add the constraints already stated above. This is a steady-state existence/design statement, not a proof of dynamical reachability or experimental stability.

Thus, for the selected state-only objective and these constraints, the physical adjoint is not automatically necessary: a target state can already be converted directly into a gate allocation with the same information interface. This is a substantive failure of the original capability claim, not just an unmeasured speed constant. Independent gate caps, additional fixed chemistry, changing flux ratios or saturation would make a different and harder task, but the present rate-free budgeted theorem does not solve those extensions in general.

This is a useful input-cancellation observation, but **not an independent claim of a new optimisation principle**. It falls directly alongside established enzyme cost minimisation in logarithmic metabolite coordinates. The fair baseline is ECM with the same reference-state calibration and rate law, not brute-force search over all microscopic parameters. Saturation adds unknown denominator ratios here too. The numerical fixture tests the identity, not a practical advantage.

## 10. Full operational accounting

Let L be the number of nonzero entries in the supplied stoichiometry, including reservoirs.

**Representation and discovery.** Unknown reactions, hidden intermediates and rate-law validity are unresolved model acquisition. The operation does not infer the reaction list. A missing reaction can change both F and M. No universal error envelope for unqueried chemistry is supplied.

**Thermodynamic calibration.** q requires equilibrium measurements or externally validated thermodynamic information. Infeasible equilibrium states, very small concentrations, conserved amounts and uncertain activities can make this costly or impossible with the available apparatus.

**Controller work.** Once its prerequisites are genuinely acquired, conjugate gate computation and reaction-wise score evaluation use O(L+n+m) arithmetic and storage. This excludes structural verification, experimental acquisition and high-precision transcendental work. Logarithmic compilation avoids avoidable overflow, but not physical dynamic-range requirements.

**Control range.** log(e_r^dagger/e_r)=(a_r+b_r)^T log(z/q). Even low molecularity does not bound this without a measured concentration range. The simple fixture requires a largest reciprocal gate fold change of approximately 13.149. That is a fixture fact, not a representative biochemical estimate.

**Errors.** If log-gate, log-concentration and log-reference errors are respectively bounded by delta_e, delta_z, delta_q, the compiled log-gate error is at most delta_e+||a_r+b_r||_1(delta_z+delta_q), before actuator error. Obtaining those bounds is not free.

**Readout and finite perturbations.** A central estimate reads n concentrations in each of two perturbed equilibria. If each concentration reading has deterministic absolute error at most sigma and ||d'''(epsilon)||_infty<=K_3 throughout the chosen interval, then, with d_min=min_i d_i and all other quantities exact,

\[
\|\widehat\lambda-\lambda\|_\infty
\le \frac{\sigma}{\epsilon d_{min}}+
\frac{K_3\epsilon^2}{6d_{min}}.
\]

Calibration, incomplete settling and model error must be added. Taking epsilon to zero amplifies sensor error. Agreement between two perturbation scales is a useful diagnostic, not a proof of a third-derivative bound or absence of hidden modes.

**Time.** Positive stability does not give a usable relaxation time. Slow chemistry can make each equilibrium expensive. A rate-independent experiment-count claim is not a rate-independent wall-clock claim.

**Work and consumables.** Account for reservoir maintenance, preparation of the conjugate mixture, enzyme/catalyst reconfiguration, discarded replicates, sampling volume, temperature control, energy and sensor calibration.

**Outputs.** All m actuator decisions require at least m output/actuation work. The operation does not provide an exponentially compressed physical control panel.

## 11. Matched competitors and novelty boundary

1. **Digital adjoints:** KPP already generates tangent-linear and discrete-adjoint chemical integrators. Once a reliable kinetic model exists, obtaining sensitivities does not require a separate full simulation per parameter. The proposal targets acquisition of that model, not invention of adjoints.
2. **Physical backpropagation:** Hamiltonian echo and in-situ adjoint methods precede this work. The August 2026 preprint *Unifying Physical Backpropagation* explicitly develops general intertwining conditions. The general idea of making physics implement a transpose is prior art.
3. **Model-free perturbations:** Simultaneous perturbation stochastic approximation already makes a two-objective-measurement gradient estimate per iteration. A two-condition chemical adjoint is not automatically a better optimiser: it has different observation, variance, configuration and calibration costs.
4. **ECM:** Fixed-flux enzyme allocation is already a convex specialisation for important rate laws. The finite-relocation formula must be compared with it using the same acquired inputs.
5. **Hidden-enzyme reduction:** Gunawardena's linear framework already eliminates internal enzyme complexity. The free-state-clamp algebra is not evidence that every hidden rate needs identification by the baseline.

The potentially distinctive part is the explicit chemical gate-and-reservoir compilation, its exact second-complex-moment defect and its rate-free budgeted direction. Historical priority for this combination is unresolved. No broad novelty claim follows from not finding an identical formula during this search.

## 12. Executed evidence

Run `python verify.py --output results.json`. The implementation requires numpy, scipy and sympy. It uses no external data or internet access.

Executed tests include: an exact rational wrong-sign counterexample; 200 generated complex-balanced nonlinear fixtures; current swapping and both matrix identities; agreement of the conjugate response with an oracle adjoint; positivity of the budgeted directional derivative; central-nudge error at four amplitudes; one finite exactly-budget-preserving design step; the finite relocation identity; and the two exact saturation counterexamples.

For the 200 generated fixtures, the largest absolute matrix-identity residual was approximately 1.42e-14 and the largest adjoint discrepancy approximately 2.44e-15. Those fixtures use small generated models with exact architectural assumptions, not experimentally identified pathways. Their purpose is to catch sign, transpose and scaling errors. They do not establish accuracy for real chemistry, global proofs by numerical testing, performance superiority or historical novelty.

In the explicit three-species fixture, the rate-free directional gain was 0.2764159221 in its arbitrary units. A normalised step of size 0.001 changed Phi by 0.0002764308254 while preserving the gate budget to floating precision. No comparison of that arbitrary gain to an industrial productivity objective is justified.

## 13. Decisive real test and stopping rule

The next scientific test is not a larger random network. It is a blind experiment on a characterised, independently actuated, reversible cell-free network with a useful state-dependent target. The controller receives only the permitted stoichiometry, reference thermodynamics, gates and measured steady concentrations. Kinetic fitting is reserved for a separate comparator team or simulator, not leaked into the controller.

First measure whether the compiled perturbation obeys the required weighted reciprocity. For independent source directions v,w, native and conjugate static response operators are R_N=-J^{-1}, R_C=-H^{-1}. Under M=0,

\[
R_C=D R_N^T C^{-1},\qquad
w^TR_N v=v^T D^{-1}R_C Cw.
\]

This supplies a falsifiable paired-response test without a full fitted Jacobian. A few directions can falsify the law but cannot certify it universally. Saturation, gate cross-coupling, finite sources and sampling errors must be recorded, not absorbed into a favourable fit.

For admitted conditions, use the acquired adjoint to propose a budget-preserving step and compare the measured objective change against prespecified confidence thresholds. Compare total experimental effort and achieved decision accuracy against digital-adjoint modelling, appropriately tuned simultaneous perturbation and ECM where applicable. Count thermodynamic calibration and conjugate hardware preparation in the proposed method's budget.

Stop the claim of a useful generic biochemical adjoint if the physical interface requires reconstructing all the same hidden kinetics, if transformed conditions leave the validated regime, or if matched methods reach the decision more cheaply. A successful small reciprocity experiment would establish physical operation only, not the user's civilisation-enabling completion standard.

## 14. Sources consulted

These are contextual prior-art sources, not proof premises for the algebra above.

- Unsleber, Grimmel and Reiher, *Chemoton 2.0: Autonomous Exploration of Chemical Reaction Networks*, JCTC 18 (2022), 5393. DOI: 10.1021/acs.jctc.2c00193. https://arxiv.org/abs/2202.13011
- Noor et al., *The Protein Cost of Metabolic Fluxes: Prediction from Enzymatic Rate Laws and Cost Minimization*, PLOS Computational Biology 12 (2016), e1005167. https://doi.org/10.1371/journal.pcbi.1005167
- Liebermeister and Noor, *The enzyme cost of given metabolic flux distributions, as a function of logarithmic metabolite levels, is convex*, 2015. https://arxiv.org/abs/1501.02454
- Lopez-Pastor and Marquardt, *Self-Learning Machines Based on Hamiltonian Echo Backpropagation*, Physical Review X 13 (2023), 031020. https://doi.org/10.1103/PhysRevX.13.031020
- *Unifying Physical Backpropagation*, arXiv:2608.11585, first submitted 12 August 2026. This was consulted as a preprint, not an independently verified general theorem. https://arxiv.org/abs/2608.11585
- KPP official documentation, tangent-linear and discrete-adjoint methods. https://kpp.readthedocs.io/en/latest/
- Spall, *Multivariate stochastic approximation using a simultaneous perturbation gradient approximation*, IEEE Transactions on Automatic Control 37 (1992), 332-341. https://doi.org/10.1109/9.119632
- Gunawardena, *A linear elimination framework*, arXiv:1109.6231. https://arxiv.org/abs/1109.6231

## Final assessment

The work supplies a constructive cancellation of unknown elementary rate constants and an exact criterion governing when a physical chemical response becomes a useful adjoint. It also disproves two unjustified extensions: that current reversal is enough, and that baseline thermodynamics and fluxes make saturation irrelevant. The original budget-only state-design target is additionally weakened by a simpler rate-free relocation competitor, which can make the adjoint unnecessary. What is still missing is a harder consequential matched task and an experimentally feasible interface that retains the cancellation for real chemistry at an end-to-end advantage. That missing capability has not been replaced by an assumed oracle.
