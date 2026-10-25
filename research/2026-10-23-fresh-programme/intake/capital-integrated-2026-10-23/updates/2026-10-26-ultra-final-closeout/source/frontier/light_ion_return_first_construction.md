# Local photon work for ionic restoration

The electrical-field bridge is retained. Its passive-channel ceiling counts bulk
Dirichlet loss in the connected cytosol/exterior; it does not cover an active
molecular pump. Existing field-driven Na/K ATPase and light-driven sodium pumps
are governing ordinary alternatives, not newly discovered mechanisms.

## First construction and question

Prepositioned outward sodium-pumping rhodopsin supplies a membrane-local work
input. Sodium export hyperpolarizes the cell; native K permeability (or a real
added inward rectifier if required) can then import K when Vm<EK. The same voltage
can drive Cl outward when Vm<ECl. This can in principle restore salt gradients
without ATP synthesis during that interval, although other metabolism, calcium,
protein injury and eventual support remain separate. Preexpression/retinal and
light delivery are actual supplied interfaces, not an emergency perfusate.

For source bad->healthy endpoints, export296.8273fmol Na, import214.3022fmol K
and export82.5179fmol Cl nearly balance charge. A pure Na-export pump plus
passive K/Cl therefore has an endpoint route; a capacitor alone cannot provide
it. Whether real permeabilities/voltage-dependent pump kinetics reach those
amounts without losing necessary function is the substantive question.

A healthy resting state with Vm>EK cannot be maintained by an outward-Na pump
and passive K alone while K leaks out. Continuous light may instead create a
hyperpolarized, altered ionic state. Passing a voltage or Nai threshold during
illumination is not evidence of restored healthy function. Count withdrawal and
subsequent ordinary pump support; do not call silencing repair.

## Existing physical interfaces and controls

Grimm etal2018 [eKR2](https://doi.org/10.1038/s41598-018-27690-w) improved membrane
targeting, recorded sodium-dominated stationary photocurrents in mammalian cells
and reversible silencing in cultured mouse neurons. This directly defeats a
generic novelty claim for light-driven Na export/neural inhibition. It supplies
a real actuator family, not proof of recovery from ionic collapse or validated
rates at the whole required voltage/Na history.

Hososhima etal2021 [KR2](https://doi.org/10.1371/journal.pone.0256728) reports
Na-dependent photocycle recovery and current histories. Peak displacement
currents must be distinguished from sustained transported sodium. Ordinary
Na/K ATPase restoration plus transient Na-channel suppression is the strong
source-model comparator. Preloaded pump expression, retinal, incident photon
power, membrane density and light attenuation are counted additions.

The first conditional ODE will keep shared charge, Na/K/Cl amounts and water.
A bounded light-driven pump law will be labeled an added uncalibrated
constitutive choice, with finite photon energy and stalling at its load
affinity. It will not borrow an arbitrary current as an acquired eKR2 waveform.
The pump-off withdrawal and no-light/no-ATP controls decide whether a useful
operation exists before more elaborate delivery construction.

## Declared pump law and energy input

The added pump law used in `light_ion_return_model.py` is

    Delta_mu_Na = RT ln(Na_e/Na_i) - F Vm,
    A = mu_drive - Delta_mu_Na,
    I_R = light Imax Na_i/(Km+Na_i) [1-exp(-max(0,A)/(RT))].

It supplies outward Na only and stalls when the declared available work is
insufficient. Km=5mM and mu_drive=30kJ/mol are uncalibrated constitutive choices,
not fitted KR2 parameters. The default light switch is instantaneous; finite
photocycle activation, long illumination/desensitization and actual current
under the entire state history remain unacquired. Changing20/30/50kJ/mol is a
diagnostic of this added law, not a supplied tunable biological actuator.

For every productive outward Na, at least one525nm photon is charged:
E_gamma=227.860kJ/mol. The cumulative photon account uses GROSS pump turnover,
not net sodium loss. It is a minimum: futile photocycles, quantum yield below1,
unabsorbed illumination, attenuation, background absorption and expression/
retinal production add costs. The assumed30kJ/mol work reservoir is below this
photon energy. Its unused photon energy is heat, not free useful work.

The ion+mean-capacitor free energy is the same finite ideal-mixing/capacitor
expression retained in `finite_ion_checks.py`. During the ATPase-off interval,

    Gdot = J_R Delta_mu_Na - D_passive,
    D_passive >=0,
    J_R(mu_drive-Delta_mu_Na)>=0.

K/Cl channel, KCl cotransport and water losses enter D_passive. Productive photon
input minus all motor/passive/spill losses equals stored G. This accounting
does not acquire a real protein photocycle or include explicit gating-charge
work absent from the source neuron model.

## Exact stationary reduction

At a stationary ATPase-off state, K and Cl have no active work input. Their
channel/cotransport dissipations are nonnegative. Stationary K/Cl amounts and
IK+ICl=0 make the sum of those dissipations zero; positive leak conductances
therefore require

    Vm=EK=ECl, JKCl=0,
    r=exp(-F Vm/(RT))=Ki/Ke=Cle/Cli.                  (1)

This is a consequence of the declared passive transport network. It is not a
grant of independent K and Cl setpoints. Write intracellular/extracellular
water volumes w and u=Vtotal-w, and total K/Cl amounts Ktot/Cltot. Then

    nKi=Ktot r w/(r w+u),
    nCli=Cltot w/(w+r u),
    q=C Vm/F,
    nNai=Ai-nKi+nCli+q.                             (2)

Here q is expressed in fmol with the source pF/mV units. Equal osmotic pressures
give

    (nNai+nKi+nCli+Ai)/w = Omega_total/Vtotal.        (3)

Equations2/3 reduce the stationary composition to one scalar volume root at
each Vm. The required Imax then follows from I_R=-I_Na with actual stationary
source gate probabilities. `light_ion_stationary_curve.py` independently checks
the resulting full cell RHS; selected residuals are below3.2e-10 in its stated
mixed source coordinates.

For the declared finite bath and30kJ/mol pump law, native NaV gives static folds
at Vm=-58.7179mV,Imax=86.5029pA and Vm=-42.0929mV,Imax=327.1830pA.
At10% NaV permeability the folds are76.8953/84.0147pA; full NaV suppression
removes these folds in the sampled physical voltage interval. This explains a
large load created by the native NaV window rather than merely by Na leak.
These are folds of the exact STATIC curve. They do not alone prove stability,
a global basin boundary, a minimal arbitrary waveform, or a biological current
threshold.

A pure outward-Na pump with passive K/Cl cannot exactly maintain the ordinary
healthy resting state: at that state Vm is above EK and K leaks outward. The
pump-maintained states lie on a different stationary relation. Active K return,
a different transporter network or eventual ordinary ATPase support is required
for the complete healthy operation; none is supplied by labeling silencing as
repair.

## Finite-stock operation and withdrawal

All dynamic cases start from the same bare closed-bath600s ATPase arrest:
cell volume2418.40um3, Nai38.427mM, Ki116.573mM, and Ke116.510mM.
The extracellular allocation was0.5pL at the initial healthy state. There is no
new K stock, material, ionic feed or bath washout. This is DIFFERENT from the
already washed-out source bad root with Nai125mM/Ki30mM: the closed case has
retained nearly all exported K locally. Its intracellular Na amount starts at
92.9323fmol and K amount near281.93fmol. The opening296.8Na/214.3K endpoint
calculation describes that other washed-out preparation, not this operation.

ATPase is zero throughout illumination. At the declared handoff, light is
removed, NaV permeability restored to its source value, and ordinary ATPase
set to its original active level for1800s. That post-light metabolic work is
explicitly supplied; no autonomous post-illumination maintenance is claimed.

| Added operation before handoff | End-of-light observation | Outcome after the same handoff |
|---|---|---|
| Native NaV;20-200pA for1200s, or250-300pA for300s | Depolarized trapped branch | Returns to finite-bath bad attractor |
| Full NaV suppression;100pA for600s | Vm-66.934mV,Nai17.700mM,Ke11.282mM | FAILS: Vm-29.488mV,Nai33.172mM |
| Full NaV suppression;110pA for600s | More negative/K-cleared state | Reaches ordinary healthy attractor in this model |
| Full NaV suppression;150pA for200s | Vm-89.776mV,Nai19.612mM,Ki134.110mM,Ke5.175mM | Reaches ordinary healthy attractor in this model |
| Native NaV;350pA for120s | Strong hyperpolarization, near-180mV excursion | Same final healthy basin in all retained method/tolerance replays; transient dose not precisely converged |
| Ordinary restored ATPase plus300s NaV suppression; no light | Provisional ionic return around242s | Reaches ordinary healthy attractor |

The ordinary comparator is established in the source-model framework and
succeeds without the optopump when ATPase work is available. No exclusive
capability, time advantage or practical advantage over it is established here.
NaV suppression alone with ATPase still off does not restore the gradients.
The NaV control is the source permeability parameter, with imposed switching;
no actual blocker with that delivery, selectivity and withdrawal history is
acquired by this numerical comparison.

Passing the provisional V/Nai/Ki thresholds DURING illumination is insufficient.
The100pA+block case is a direct counterexample. The result files that record
`first_sampled_ionic_return_after_handoff_s=0` merely record the initial sample;
the final state must also be read. The later handoff/check files explicitly
retain the final classifier. No first-passage result is promoted to durable
restoration.

## A discriminating resource result

In tighter BDF/Radau replays, successful150pA+block200s expels260.4982fmol Na
through the photopump but reduces intracellular Na by only50.5716fmol.
Passive Na reentry accounts for most of this repeated turnover. It imports
7.7543fmol K and exports42.7987fmol Cl over that interval, keeping the finite
ion and charge inventories. The subsequent1800s active-ATPase handoff consumes
496.632fmol ATP, versus487.016fmol for the same duration at source rest.
Those ATP counts do not independently certify a maintained ATP free energy.

The successful light interval stores0.365377nJ additional ionic/capacitor free
energy, delivers3.311276nJ to ions through Na export, and dissipates2.945899nJ
through the passive network. Minimum productive photon input is59.357152nJ.
Net stored-gradient gain is only0.6156% of that minimum productive photon energy;
real incident-light conversion is less favorable. This is not a tissue heating
or damage prediction.

The FAILING100pA+block600s interval stores MORE total ionic/capacitor energy,
0.417412nJ, while using116.528312nJ minimum productive photon energy. It still
relapses after the same handoff. Thus total gradient energy and the provisional
scalar ion thresholds do not order recoverability in this model. The direction
of ion redistribution, extracellular state and the subsequent dynamical basin
matter. This is a finite model discrimination, not a new biological theorem or
a validated clinical threshold.

`light_ion_return_checks.py` retains independent complex-step derivatives of the
complete mixing/capacitor free energy, integrated passive heat, conserved mass/
water and charge, plus tighter BDF/Radau replays. In controlled150pA and100pA
cases, photon accounts agree to about1e-10 relative, local energy-rate errors
are below1e-26W and integrated energy errors below2e-18J. Mass/water identities
are algebraically conserved to roundoff; charge residual is below5e-8mV.
These validate only the declared equations and their numerical implementation.

Native350pA has a faster, gate-sensitive transient. All four retained replays
return to the healthy basin, but tightening tolerance/maximum step changes
minimum productive photon input from about80.8-80.9nJ to77.1nJ and net stored
gain from0.410-0.412nJ to0.506-0.507nJ. The refined BDF/Radau results are closer,
but this is not a certified error interval or a converged precise native dose.
The original logs/traces and the discrepancy are retained. The controlled
success and failure above do not rely on that native transient estimate.

## Physical evidence and the stronger ordinary optical alternative

The downloaded Grimm2018 original PDF and visually inspected Figs1/3 are kept
in `sources/`. Its stationary-current density is a few pA/pF on average at
symmetric110mM Na and0mV; the plotted voltage measurements span about-60 to+40mV.
This does not acquire the model's roughly120pA sustained current for200s while
Nai/Ke/water change, or the native route's near-180mV excursion. Its measured
light response is not a monotone unlimited amplitude knob. Source-cell20pF,
room-temperature pump recordings and the source310K channel model are separate
contexts. Photocurrent peaks and relaxation times are not substituted for
sustained Na transport or conversion speed.

A strong established alternative is mitochondrial photon work:
[2020 mitochondria-ON work](https://pmc.ncbi.nlm.nih.gov/articles/PMC7132214/) constructed
mitochondria-ON, increased PMF and supported ATP synthesis in C.elegans isolated
mitochondria without requiring ETC oxygen consumption for that light-derived
contribution. Later [2025 mammalian retinal work](https://doi.org/10.1038/s41392-025-02450-1)
also reports an engineered mitochondrial optoenergetic pump. These defeat any
generic novelty claim for oxygen-independent photon-supported cellular energy.
They are not whole-tissue resuscitation demonstrations.

Under the optimistic one-H/photon and11/3H per exported ATP accounts already
retained in the redox bridge, photon-supported ATPase gives9/11Na and6/11K per
photon at the native3Na/2K ratio. Actual coupling/leaks/light access decide the
comparison. We have not numerically matched either published optical ATP
actuator to this operation. Direct Na pumping has no established net photon
or biological advantage over that stronger alternative.

The preserved construction is therefore: a conditional membrane-local work
route can prepare some finite-inventory states inside the ordinary healthy
return basin while ATPase is off; other seemingly improved states fail on
withdrawal. Generic optopumping is established, the added long-duration state
law is unacquired, the field-access bound applies at its earlier passive-channel
scope, and tissue recovery/practical advantage remain UNKNOWN.

No additional line is opened. Outstanding physical obligations are retained:
prepositioning and correct membrane orientation/expression, retinal supply,
sustained pure-Na transport and load-dependent photocycle, finite switching/
recovery, protein density/packing, state sensing and withdrawal timing, optical
distribution/absorption, and the native capillary/ATP/calcium/biological recovery
interfaces absent from the source model.


