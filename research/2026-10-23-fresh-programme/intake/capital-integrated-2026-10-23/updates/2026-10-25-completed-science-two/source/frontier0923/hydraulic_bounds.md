# Bounds on local oxygen-dependent perfusate control

These are internally derived mathematical statements in the model below. External correctness and novelty are unverified. No biological intervention has been performed.

## Physical model and quantities

A straight extraction bed has axial coordinate x in [0,1], constant volumetric flow q>0, fixed geometry, inlet oxygen content c_a>0, and outlet c_v. The perfusate is incompressible, locally Newtonian, and its viscosity is a nonnegative function mu(c) of carried oxygen content. A positive local oxygen uptake law f(c) determines

    q dc/dx = -M f(c).

M is an uptake scale, not an acquired measurement of living tissue demand. It can incorporate a known uniform length density. A physically useful example is f(c)=c/(K+c). The pressure loss is

    p = kappa q integral_0^1 mu(c(x)) dx.

For a cylindrical bed, kappa=8L/(pi r^4). No endothelial response, collapse, clot, cell-free layer, cross-vessel oxygen diffusion, or reactive injury is included. Results concern this constitutive model; primary research establishes that the omitted mechanisms can matter.

Define the oxygen exposure coordinate

    z(c) = integral_c^c_a [1/f(s)] ds.

It increases as c falls, and z(c(x))=(M/q)x. Let g(z)=mu(c(z)), e=M/q, and A(e)=(1/e) integral_0^e g(z) dz. Then

    p/kappa = q A(M/q)
            = (q^2/M) integral_0^(M/q) g(z) dz.                 (1)

For f(c)=c/(K+c), z(c)=c_a-c+K log(c_a/c). If f(c) remains positive only for c>0 and z(0)=infinity, this parameterization covers every q>0 without a negative oxygen concentration. If constant uptake is instead clamped at c=0, append a plateau g(z)=mu(0) beyond c_a; the same algebra applies.

## Proposition 1: fixed-pressure dominance

If mu(c)>=mu_lo>0 throughout the branch, then p>=kappa mu_lo q. Therefore at the same pressure p, geometry, and oxygen carrying/uptake law,

    q_adaptive <= p/(kappa mu_lo) = q_uniform_low.

The outlet oxygen content is nondecreasing in q because z(c_v)=M/q. Consequently no local viscosity addition can improve branch outlet oxygen under these matched fixed-pressure assumptions. A purported gain must name a different binding resource: total-flow capacity, shared feeder loss, or a constraint on excess flow. This is not a no-go for vascular diameter control, recruitment, or restoration of flow in a physically obstructed bed.

## Proposition 2: universal upper differential gain

At differentiability points of A with A>0, differentiation of (1) gives

    E(q) := d log(p/kappa) / d log(q)
          = 2 - g(M/q)/A(M/q).                              (2)

For every nonnegative local viscosity law, E<=2. This upper bound does not require mu(c) to be monotone. If mu(c) is nondecreasing in oxygen content, g is nonincreasing, so 0<=g(e)<=A(e), and

    1 <= E(q) <= 2.                                       (3)

The lower bound gives a unique stable static pressure/flow relation. Making an oxygen switch arbitrarily steep does not make the macroscopic feedback arbitrarily strong: axial transport averages the constitutive response. Constant mu attains E=1; negligible low-state viscosity and a finite oxygenated high-viscosity segment can approach E=2. This is a physical spatial-averaging bound, not a bound on all oxygen feedback mechanisms.

The same statement holds almost everywhere for bounded monotone step laws. One can either differentiate between switch points or use absolute continuity of the integral in (1).

## Corollary: residual heterogeneity

Consider two parallel branches with the same M and inlet oxygen but geometry factors kappa_2>=kappa_1. At shared pressure, q_1>=q_2. Integrating (3) yields

    sqrt(kappa_2/kappa_1) <= q_1/q_2 <= kappa_2/kappa_1.      (4)

Thus a 100-fold geometric resistance disparity cannot be reduced below a ten-fold flow disparity in this model, however large the local constitutive slope. A finite viscosity ratio makes the restriction stronger in many regimes.

For unequal M_i, write v_i=q_i/M_i and b_i=kappa_i M_i. Equation (1) becomes p/b_i=v_i A(1/v_i). The same bounds apply to relative supply v_i and burden b_i. The feedback compresses **supply relative to uptake scale**, not necessarily raw flow or capillary transit time. Equal flow is not the right objective when branch demands differ.

## Proposition 3: where high gain could live

Under oxygen-independent but spatially varying uptake m(x)>0, define cumulative extraction fraction a(x)=integral_0^x m(s)ds/M. Let h(a)>=0 be normalized hydraulic resistance per unit extraction fraction, with H(a)=integral_0^a h(s)ds and H(1)=1. In the oxygen-supported regime,

    c(a)=c_a-(M/q)a,
    p/kappa=q integral_0^1 h(a) mu(c_a-(M/q)a) da.

For a two-state local viscosity mu_lo+Delta_mu 1[c>c_*], let a_*=(c_a-c_*)q/M, within (0,1). Then

    A_h=mu_lo+Delta_mu H(a_*),
    E=1+Delta_mu a_* h(a_*)/A_h.                           (5)

For a general nondecreasing mu, represent it as a nonnegative mixture of such steps. If C_h=sup_(0<a<1,H(a)>0) a h(a)/H(a) is finite, then

    E <= 1+C_h.                                           (6)

Proof: each constituent step contributes H(a_*) to A_h and a_*h(a_*) to q dA_h/dq; bound the latter by C_h times the former, sum, and retain nonnegative mu_lo. Uniformly colocated extraction and resistance give h=1, C_h=1, recovering (3). If h(a)=(beta+1)a^beta, C_h=beta+1. Distal localization can evade the quadratic bound; it is an additional spatial interface, not a result of arbitrarily steep rheology alone.

The variable-uptake version uses z(c) rather than c if the uptake separates as m(x)f(c). Resistance localization is then measured against cumulative uptake scale; the local step crossing has the same form after replacing c_a-c_* by z(c_*).

## Pressure cost of the distal-gate escape

For a bed with an arterial resistor R_a, extraction bed, and venous resistor R_v, move a positive resistance delta_R from the arterial to venous side, keeping total resistance and q fixed. Every pressure inside the intervening extraction bed rises by

    delta p_cap = q delta_R.                              (7)

In a fixed-parameter Starling model J_f=L_p S[(p_cap-p_i)-sigma(pi_cap-pi_i)], filtration rises by L_p S q delta_R. Thus locating a sharp oxygen-responsive gate downstream can provide high feedback gain while imposing an independent capillary-pressure/edema cost. Equation (7) is circuit algebra; applying Starling parameters in injured tissue requires measurement. This does not assume that more pressure always worsens biological perfusion: recruitment can have an opposing benefit.

## An additional information limitation

An oxygen-only perfusate sees present extraction, not latent recoverability. Two branches with identical geometry and present uptake but different capacities to restart metabolism are indistinguishable to any deterministic rheology depending only on current oxygen. In particular, a metabolically silent salvageable bed and a nonconsuming irreversibly damaged bed can initially produce the same oxygen signal. A bootstrap route must use a second physical signal, a minimum delivery floor/challenge phase, or an independent upstream control interface. Calling oxygen extraction a viability sensor would be unjustified.

## What remains constructive

The surviving proposition is a bounded passive redistribution device under finite total flow, with a precise pressure cost and demand weighting. Computation should determine its useful region, including the gain achievable with realistic bounded viscosity and the feasibility of a floor-delivery recovery phase. A more ambitious high-gain device requires independently localizable arterial resistance controlled by downstream information, which is already a biological function of conducted vascular signaling and must be compared with that primary literature.

## Proposition 4: an oxygenated common feeder does not remove the fixed-pressure defeat

Add an upstream common geometric resistor R_a. If the adaptive fluid is fully oxygenated in that feeder, its viscosity there is mu_hi=gamma mu_lo. Let Q_0(p) be total flow of the parallel tissue beds with uniform low viscosity at bed pressure p; let Q_A(p) be the adaptive total flow. Since mu_lo<=mu(c)<=gamma mu_lo,

    Q_0(p)/gamma <= Q_A(p) <= Q_0(p).

At a fixed bed pressure p, the required total inlet pressure obeys

    P_A(p)=p+gamma R_a Q_A(p) >= p+R_a Q_0(p)=P_0(p).

Both maps increase when the desired-sign viscosity law is monotone. Thus at fixed inlet pressure P the adaptive bed pressure cannot exceed the low-viscosity bed pressure; every adaptive branch flow is again no greater than the uniform-low-viscosity flow. The shared-feeder “steal” intuition is insufficient when the same oxygenated rheological premium acts in the feeder. If the material has low viscosity specifically at inlet saturation, or the feeder contains a distinct fluid, this statement need not apply; that is a changed constitutive/interface hypothesis.

## Proposition 5: a work requirement that survives arbitrary timing and local controllers

Consider a lumped tissue oxygen store c_i(t) in [0,1] with storage scale V_i and uptake scale M_i:

    V_i dc_i/dt=q_i(t)(1-c_i)-M_i f(c_i),

where f is nondecreasing. If c_i>=c_min throughout an interval of duration T, integration gives

    average(q_i) >= M_i f(c_min)/(1-c_min)
                    + V_i[c_i(T)-c_i(0)]/[(1-c_min)T].     (11)

This follows from q_i(1-c_i)<=(1-c_min)q_i and f(c_i)>=f(c_min). A finite recovery interval can borrow stored oxygen; the boundary term must not be dropped. In a steady or periodic sustained state it vanishes. Define q_i,req=M_i f(c_min)/(1-c_min).

If the fixed tissue bed has hydraulic resistance R_i and passive components add only nonnegative losses, any local or global pumping architecture has mean hydraulic dissipation at least

    sum_i R_i average(q_i^2) >= sum_i R_i average(q_i)^2.

Hence sustained adequacy in all critical territories requires

    mean hydraulic power >= sum_i R_i q_i,req^2.           (12)

This bound permits independent pumps, arbitrary valve timing, feedback, and pressure pulses. A common pressure source with metering valves normally pays an additional loss. It does not cover an intervention which changes R_i, changes actual oxygen demand, supplies oxygen by a different physical route, or draws down a finite oxygen store. Those are substantive new physical operations rather than a better allocation algorithm.

For the illustrative f(c)=c/(K+c), K=.05 and c_min=.2, q_i,req=M_i exactly. Therefore the sum R_i M_i^2 is an immediate lower work requirement for sustained oxygen adequacy. It is not a biological survival criterion; it only tests consistency of that oxygen model.

### Independent oxygen-mass crosscheck supplied by root

After the preceding target-oxygen derivation, root independently supplied the broader conservation form. Let m_i(t) be actual oxygen uptake, inlet oxygen content be bounded by c_a, and usable initial oxygen store be S_i(0)>=0. With nonnegative flow and no other oxygen source, oxygen balance implies

    integral_0^T q_i dt >= [integral_0^T m_i dt-S_i(0)]_+/c_a.

Jensen then yields

    W_hyd >= sum_i R_i [integral_0^T m_i dt-S_i(0)]_+^2/(T c_a^2). (18)

This independent check retains finite oxygen storage explicitly and does not need a particular uptake law or tissue oxygen threshold. It is looser than a justified local-oxygen requirement, and it still concerns supplied intrinsic resistances/actual uptake, not a biological recovery criterion. It does not apply unchanged when recruitment alters R_i or oxygen arrives through a distinct route.
