# Thermal mechanism assessment: a pump-loss gate for frequency-converting refrigeration

ASTRA-FRESH-20261023, P2 bounded independent calculation. Status: **analytic reduced model, numerical cross-check, and proposed experiment only**. No measurements acquired, no apparatus operated, no new physical principle or practical advantage established. Root corpus revision: `e606bfc587c76bdcae8b8fa3ec33e721efa2fbac`.

## Decision

The most defensible thermal candidate investigated here is a resonant frequency converter that moves thermal quanta from a cold surface mode to a higher-frequency hot surface mode. This is **already a published mechanism**, not an Astra invention. The potentially useful remaining invention problem is its physical pump interface: low-loss modulation with complete energy accounting. I derived an exact gate in a narrow, explicit model; if a measured device fails that gate, increasing modulation amplitude cannot rescue it. This supplies a bounded material-development target, not a broad impossibility claim.

Closest precedents are Buddhiraju, Li & Fan (2020), *Photonic Refrigeration from Time-Modulated Thermal Emission*, PRL **124**, 077402, DOI https://doi.org/10.1103/PhysRevLett.124.077402; Yu & Fan (2024), *Time-modulated near-field radiative heat transfer*, PNAS **121**, e2401514121, DOI https://doi.org/10.1073/pnas.2401514121; and Khandekar, Messina & Rodriguez, *Near-field refrigeration and tunable heat exchange through four-wave mixing*, https://arxiv.org/abs/1712.03273. These precedents prevent claiming frequency-converting refrigeration itself as novel.

The read full preprint of Yu & Fan, https://arxiv.org/html/2310.08692v1, explicitly models a lossless modulated layer. It uses a 2.33 THz modulation, a 1 nm gap and a 4 nm modulation layer in the illustrative construction. Its reported cooling flux is theoretical. Work delivered by modulation to the electromagnetic field is counted, but the complete physical source and its absorption are a separate implementation obligation. This observation does not invalidate their modeled result.

## Mechanism and assumptions

There are M identical independent pairs of resonators: cold mode a at angular frequency wc, hot mode b at wh>wc, bath temperatures Tc<Th, and energy damping rates kc, kh. A physical pump at Omega=wh-wc has coherent occupation N and generates a resonant beam-splitter interaction:

`H_int / hbar = g (a† b + a b†)`, where `g = g0 sqrt(N)`.

The cold and hot bath Bose occupations are `nc=n(wc,Tc)` and `nh=n(wh,Th)`. The model assumes narrow bands, flat Markov baths over the small coupling-induced splitting, positive damping, stable difference-frequency conversion, negligible counter-rotating and other-sideband terms, and frequencies much larger than coupling and damping. The pump amplitude is maintained by a drive whose depletion is charged. Its irreversible absorption is `Pabs=hbar Omega kp N`. Here kp means the loss rate whose dissipated power is not recovered as coherent work. Recoverable output-port power must not be silently classified as absorption, or omitted if it is not actually recovered.

The fraction f of Pabs that heats the cold stage is included explicitly. A separate nonnegative passive heat load L flows into the cold stage. Source and control losses outside this pump are separately charged in wall power; any portion reaching the cold stage belongs in L or in a measured f-weighted loss law.

Necessary occupation condition:

`Delta_n = nc - nh > 0`, equivalently `wh/wc > Th/Tc`.

Each net converted quantum extracts `hbar wc` from the cold bath, accepts `hbar Omega` of work, and delivers `hbar wh` to the hot bath. The ideal coefficient of performance wc/Omega is less than Carnot when Delta_n>0; its Carnot limit is approached at vanishing occupation difference and cooling flux. Neither resonance matching nor nonreciprocity supplies free work.

## Exact steady-state current

The Langevin equations are:

```
da/dt = -kc a/2 - i g b + sqrt(kc) a_in
db/dt = -kh b/2 - i g a + sqrt(kh) b_in
```

Let J be the cold-to-hot photon number current per pair. The number balances give `n_a=nc-J/kc` and `n_b=nh+J/kh`. Eliminating the steady-state coherence gives `J=4 g^2 (n_a-n_b)/(kc+kh)`. Therefore, writing `C=4g0^2 N/(kc kh)`,

`J = [kc kh/(kc+kh)] [C/(1+C)] Delta_n`.

Define the large-C gross cooling scale

`Qstar = hbar wc M [kc kh/(kc+kh)] Delta_n`,

and dimensionless pump burden and leakage

```
alpha = f (Omega/wc) kp (kc+kh) / [4 M g0^2 Delta_n]
ell   = L/Qstar.
```

Then the **net** cold-stage cooling is exactly

`Qnet/Qstar = C/(1+C) - alpha C - ell`.

For `0<alpha<1`, its unconstrained maximum is

```
Copt = alpha^(-1/2) - 1
Qnet,max/Qstar = (1-sqrt(alpha))^2 - ell.
```

Thus some positive cooling is possible in this model precisely when

`alpha < 1` and `ell < (1-sqrt(alpha))^2`.

For alpha>=1 every positive drive produces nonpositive net cooling. For alpha=0 the supremum is 1-ell as C increases. With a physical maximum Cmax, replace Copt by min(Copt,Cmax) and evaluate the net-cooling formula; the unlimited-drive gate is only necessary when the optimum lies outside the permitted model or amplitude range.

**Interpretation:** conversion power saturates, whereas pump absorption continues growing with occupation. Higher drive cannot compensate for sufficiently bad nonlinear coupling, pump loss, thermal anchoring, or passive leakage. The gate can be tested with measured parameters before fabricating a complete refrigerator. Algebraic simplicity does not establish that the exact criterion is novel in the literature.

At quasistatic envelope modulation, C/(1+C) is concave. Consequently duty cycling at fixed average C cannot improve average cooling under this linear-loss model: Jensen's inequality favors constant C. This statement does not cover fast coherent pulses, changing bath coupling, nonlinear pump-loss laws, or designs that modify the mode spectrum during the cycle.

## Full operating-cycle cost

Define `r=kp(kc+kh)/(4 M g0^2 Delta_n)` so alpha=f(Omega/wc)r. The necessary net power delivered to the ideal pump plus its absorption is

`W = (Omega/wc) Qstar [C/(1+C) + r C]`.

The first term is useful frequency-conversion work; the second replenishes irreversible pump loss. A source efficiency eta gives `Pwall >= W/eta`, plus controls, unrecovered ports, maintenance and support. Hence

`COP_wall <= eta (wc/Omega) [C/(1+C)-alpha C-ell] / [C/(1+C)+r C]`.

With zero cold leakage, the C->0 limit is `eta (wc/Omega)(1-alpha)/(1+r)` and has zero cooling power. Moving all pump loss to the hot side sets alpha=0 but does not remove r or its efficiency penalty. An auxiliary cryogenic pump source requires its own refrigeration work, not merely a favorable f.

The chosen steady state is already a closed operating cycle: pump occupation and both mode occupations are constant. Reinitializing the drive or a reservoir is not an uncharged resource. Transient reservoir depletion would be a different device and must be charged.

## A concrete alternative interface: optical two-tone mixing

A pair of optical pumps can avoid a direct THz generator, but cannot be costed as a lossless low-frequency drive. For a four-wave interaction `g=chi sqrt(N1 N2)` and two pump frequencies wp1,wp2, the absorbed power is

`Pabs = hbar (wp1 kp1 N1 + wp2 kp2 N2)`.

At fixed coupling, the product `N1 N2=C kc kh/(4 chi^2)` is fixed. AM-GM gives the minimum

`Pabs,min = hbar sqrt(wp1 wp2 kp1 kp2 kc kh) sqrt(C) / |chi|`.

For equal cold-side heating fractions f, define the corresponding coefficient beta by `f Pabs,min/Qstar=beta sqrt(C)`. The optimized pump split obeys `wp1 kp1 N1=wp2 kp2 N2`. Then

`Qnet/Qstar <= C/(1+C) - beta sqrt(C) - ell`.

At zero leakage, positive cooling exists only if beta<1/2, since `sqrt(C)/(1+C)<=1/2`. With leakage 0<=ell<1, the threshold is

```
y = [1+2ell+sqrt(1+8ell)]/[2(1-ell)]
beta_crit = sqrt(y)/(1+y) - ell/sqrt(y)
```

and beta must be less than beta_crit. These expressions assume unrestricted pump split and the stated perturbative nonlinear model. Unequal f values are included by weighting each pump's loss coefficient. Coherent outgoing optical pump power must actually be recovered to justify paying only the frequency difference for conversion; otherwise the full unrecovered carrier power also enters the wall-energy balance. This is a serious difference between a source-less modulation calculation and an implementable converter.

This two-tone alternative is plausible as an interface to investigate, but no actual material has yet been shown here to satisfy the threshold. No numerical material feasibility claim should be made without measured nonlinear coupling and loss at all participating frequencies.

## Numerical results and their limits

`check_model.py` solves the steady-state covariance equation directly for 300 random unequal-rate examples and compares it with the analytic J. Maximum relative current discrepancy: 2.514e-12; maximum relative cold/hot number-balance residual: 7.809e-12. It separately checks the power-optimal formula numerically. This validates arithmetic within the assumed equations, not the underlying physical approximations or a device.

An explicitly synthetic scale uses wc/(2pi)=20 THz, wh/(2pi)=22 THz, Tc=300 K, Th=310 K, and kc/(2pi)=kh/(2pi)=0.1 THz. It gives Delta_n=0.0082018, Qstar=3.41465e-11 W per mode pair, ideal COP=10 and Carnot COP=30. A heuristic one-polarization cutoff qmax=1/(100 nm) gives about 7.96e12 pairs/m^2 and Qstar approximately 272 W/m^2. This wave-vector count is only an illustration, not a full electromagnetic calculation or rigorous near-field bound. At alpha=0.1, ell=0.1, Copt=2.1623 and Qnet,max=0.36754 Qstar; at alpha=0.5, ell=0.1, net cooling is impossible.

One cannot rule out a macroscopic array by applying a single-mode pump-loss estimate independently to every pair: the same coherent pump can address many pairs. Conversely, area does not automatically improve the material figure: normalizing a larger common pump mode usually decreases g0^2 while increasing M. Their actual geometry-dependent product must be computed.

## Proposed decisive measurement, not performed

1. Characterize the two resonances, linewidths, thermal occupancies, and coherent conversion rate against supplied pump amplitude. Determine g0 and whether extra sidebands invalidate the two-mode reduction.
2. On the same modulation stack, measure irreversible pump absorption and the partition of that heat between cold and hot stages. Use net source power after any actual coherent power recovery, not nominal circulating optical power.
3. Measure the pump-off passive cold-stage heat load and all support conduction at the same temperature difference and gap.
4. Insert the measured values into the bounded-C cooling expression. If its maximum is negative, do not increase drive as the next experiment: change material coupling/loss, thermal anchoring, mode density, or passive leakage.
5. If the gate survives, use independent cold-stage calorimetry with a compensating heater. Test matched detuned modulation at the same absorbed power. Frequency conversion should peak at Omega=wh-wc and the energy balance should close with hot/cold quantum energies, while a pump-heating artifact will not obey the same spectral and energy relations.

## Continuation recommendation

Keep this as a **bounded interface investigation**, not the primary civilization-scale claim. Request a full-wave multi-mode calculation only after a specific material and modulation mechanism has a measured or tightly sourced nonlinear coefficient and loss tensor over all three (or four) frequencies. Next executable work is to fit those measurements, replace identical-pair parameters by mode-dependent integrals, and optimize net cooling and wall COP jointly. External measurement access is not presently available to this worker; independent literature/material analysis remains possible. No sibling programme has been messaged or reallocated by this calculation.

Available receipts: `check_model.py`, executed `results.json`, the tool-visible primary-source reads, and the pinned corpus revision. Token/spend totals are not exposed to this worker. Priority and novelty of the derived implementation criterion are UNKNOWN. The novelty and feasibility of any physical material solution are UNKNOWN.
