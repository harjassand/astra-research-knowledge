# A printed local pressure drive: constructive interface, not a closed printer

27October2026. This protected replacement follows the independently locked FIRST_CONSTRUCTION.md. It does not reopen parked routes. The initial generic chiplet-assembly proposal was rejected when an actual programmable transfer→bonding→working-display incumbent was acquired; see ../programmable_chiplet_release/GENERIC_JOIN_ALREADY_SUPPLIED.md.

**Outcome:** a concrete composition can remove the *electronic commutator and fast remote pressure lines* from a candidate all-plastic rotary drive. It joins a printed pneumatic controller/relay to a bearingless, magnet-free, FDM-made motor. I reconstructed the exact pressure-to-wrench interface, proved a nonvanishing rotating-field construction under explicit waveform contracts, and replayed primary dimensional/torque data. The **loaded composed drive has not been demonstrated or qualified**. Nor has it reproduced a productive printer/tool. A common FDM printer already makes active pneumatic devices; that established service composition is the stronger actual productive-tool comparator. No civilisation-level manufacturing closure or superiority is claimed.

## Primary operations: the hidden nonprinted parts matter

[Kendre et al., FDM-Printed CMOS Logic Gates, DOI10.1002/aisy.202400468](https://doi.org/10.1002/aisy.202400468): source is the authors'16-page manuscript (2024-hosted version), SHA6ded0394d4b6271f0874008265dfc90065213e69a006c83b3858ed0d8a150ccb. Governing sections2,3.1,3.2 and fabrication/data methods were read; actual Fig5 was rendered. A3-inverter ring supplies oscillations; a separate printed relay powers a200kPa linear robot from a180kPa clock rail. The rotary demonstration has **embedded disc magnets and a purchased ball bearing**. “All components printed” in one methods sentence cannot override that explicit parts bill. The unscaled pressure sketch in Fig5B is not a recorded calibrated three-channel waveform.

[Farimani and Misra, Introducing PneuAct, ICRA2018](https://ieeexplore.ieee.org/document/8462697): primary author PDF SHA8537862ed31ff6a6947a7c3d347a3e19caddd3db72878420f5d30a1f7efb0add. Governing design, pneumatic model, Fig7/9/10 and control schematic read. The ABSplus-P430 motor and worm gearing are FDM-made without separate seals, bearings or lubricant. **Its demonstrated commutator uses three solenoid valves, an Arduino and regulated air.** The source reports120degree full-pitch and60degree half-pitch crank drive, reduced to3/1.5degree nominal increments by40:1 gearing. Resolution is not a transferable positioning-accuracy guarantee.

The published experimental repository was acquired at **066f640644178dd853d2783d6095dd54a2201905**: [source data](https://github.com/Foadsf/PneuAct_ICRA2018/tree/066f640644178dd853d2783d6095dd54a2201905). Selected data and their original server/tree blob identities are retained; locally saved text normalizes trailing newlines. No repository/archive build was performed. Fig9's actual measured pressure/holding-torque pairs are in its README. Fig7 explicitly calls gaps nominal CAD values. Fig10's raw timing header has no unit: I do not call those numbers measured Hz.

[Zhai et al., Science Robotics2023, DOI10.1126/scirobotics.adg3792](https://doi.org/10.1126/scirobotics.adg3792), abstract scope only, already supplies an electronics-free monolithically FFF-printed autonomous gripper. This is an actual useful manipulation operation. No claim to have invented printable active pneumatic control follows from putting these sources next to each other.

## Proposed acquired-component composition and its missing join

Use a printed ring/controller locally, three printed pressure buffers/relays, and the all-plastic mechanical PneuAct. A steady high-pressure utility rail powers the buffers; a lower clock rail drives their control actuators. A phase reversal would exchange two pressure outputs; an implemented start/stop/reversal circuit is not acquired here. The useful target is a locally commutated, counted rotary drive, with actual torque, missed-step and endurance specifications. Supplying a clock does not supply that productive output.

The meaningful compatibility is: actual chamber pressures and flow, sufficient venting, rotor mechanical work and friction, not merely logic-level pressure. Moving the commutator near the motor can replace three long rapidly charged/exhausted signal tubes with a steady supply route and short local outputs. DC supply regulation, local gas storage, bleeding losses and initial filling remain resources. The input is compressed air, not free energy.

Both papers use additive manufacturing, but their material/process promises are different: industrial FDM ABSplus motor parts versus desktop FDM compliant PLA/TPU mechanisms and commodity tubing. This does not acquire identical clearances, surface friction, airtightness or lifetime on a common maker. No hot FFF nozzle, heater, bearing-quality stage, extruder feeder or assembly mechanism is reproduced by the composition.

## Exact pressure-to-wrench operation

For the ideal source scotch-yoke geometry, let crank pin phases be phi_j=2pi*j/3 and piston displacements x_j=x0+r*cos(theta−phi_j). Actual chamber gauge pressures p_j give the virtual-work torque

    tau_pressure = A*r*Im(z*exp(−i*theta)),
    z = sum_j p_j*exp(i*phi_j).

Thus the desired stable direction is arg(z), and pressure-wrench amplitude is A*r*|z|. Friction and external load are additional terms. A common pressure offset cancels from z; it does not cancel gas consumption or contact forces/friction. This is the ordinary three-phase space-vector/Clarke representation used here as a construction tool, not claimed as new mathematics.

The binary sequence

    100 → 110 → 010 → 011 → 001 → 101 → 100

has command phasors P*exp(i*k*pi/3). It gives half-pitch drive without zero-vector states. The source's50percent-duty three-phase idea is therefore compatible with this *geometrical* motor interface, provided its delivered pressure trajectory and loaded mechanical response are separately qualified.

### A source-independent waveform result, including unequal charging/venting

Let f be a continuous periodic pressure waveform of periodT, strictly increasing from its unique minimum to its unique maximum on one circular arc, and strictly decreasing on the other. The two arc lengths need not agree. Define

    p_j(t)=f(t−j*T/3),    z(t)=sum_j p_j(t)*exp(2pi*i*j/3).

Then **z never vanishes and winds once in the positive direction per period**.

Proof: the real linear map from(p0,p1,p2) toz has nullspace exactly the constant triples. A value of a strictly unimodal circular function has at most two preimages, so three distinctT/3-spaced samples cannot be equal. For winding, express f=fmin+(fmax−fmin)*(1−cos(phi(t)))/2 with a continuous strictly increasing phase lift phi(t+T)=phi(t)+2pi. Homotope that lift to2pi*t/T. Every intermediate waveform remains strictly unimodal, so no correspondingz crosses zero. The sinusoidal endpoint hasz=−3*(fmax−fmin)*exp(2pi*i*t/T)/4 and winding+1. Winding need not mean a monotonically turning direction for every admissible waveform; it certainly does not by itself mean a turning rotor.

If additionally |f'|≥m>0 along both monotone arcs (piecewise derivatives suffice), two of the three sample points lie on one arc with arc separation at leastT/3. Their pressure difference is at leastm*T/3. Since

    |z|² = ((p0−p1)²+(p1−p2)²+(p2−p0)²)/2,

minimizing over the third pressure gives **|z|≥sqrt(3)*m*T/6**. Smooth waveforms with zero slope at turning points may have m=0; nonvanishing still holds, but this particular quantitative lower bound then supplies nothing.

For phasewise errors |delta p_j|≤Delta, the sharp bound is |delta z|≤2Delta: maximize the norm of the linear map on the pressure-error cube; its eight vertices give0 or2Delta. A continuous periodic perturbation therefore preserves a nonzero field and its winding whenever2Delta is smaller than a qualified ideal radius floor. If amplitude error is bounded byepsilon and phase-time error byeta with a Lipschitz waveform boundM, one may use Delta=epsilon+M*eta. Those are acquisition/structural promises, not values inferred from gate-threshold standard deviations.

### Exact filtered witness

For identical first-order channels tau*p_dot=P*b−p and six command states each held forh, put q=exp(−h/tau), omega=exp(i*pi/3), c=(1−q)/(omega−q). The unique positive periodic pressure state has

    z_k(s)=P*omega^k*[1+(c−1)*exp(−s/tau)],  0≤s≤h.

Every segment is an exponentially traversed chord of a regular hexagon. Hence its angle turns forward, its winding is1 and

    min |z| = P*(1−q)*sqrt(3)/(2*sqrt(1+q²−q)).

Atq=1/2 the minimum is exactlyP/2. The executed independent three-real-pressure recurrence agrees with the complex formula to6.8e−16 (unit pressure), closes exactly at the printed precision, and winds once. The numerical minimum0.50000007 approaches the exact0.5.

The code also constructs an explicitly unequal-rate positive example (tau_up=1,tau_down=1/2,h=log2). It closes and winds once; sampled radius minimum0.543875. The monotone-slope theorem gives a conservative, valid0.032892 lower. Neither example is a fit or measured behaviour of a printed loaded controller.

## Source-scaled computation and real-data discrimination

The2018 source's empirical rise law for4mm-ID tubes, lengths1–8m and input2–7bar, has tau=20*exp(l/3)ms and common delay=(10/3)*exp(l/3)ms. It was fitted with electronic valves; it is not a response law for printed relays, symmetric venting or moving motor chambers.

As a clearly conditional numerical composition, combine its3m timing constant with the2025 author's observed4.2Hz ring rate and a proposed200kPa power rail. The exact filter witness gives q=0.481948, ideal radius103.588kPa and83.588kPa remaining after a **supplied**, not measured,10kPa per-channel tracking allowance. Applying source crank geometry(A=15mm×15mm,r=3mm) gives0.06992Nm ideal pressure-wrench amplitude before friction, leakage effects on chamber pressure, loads or gearing. This is not usable output torque.

That constant-volume isothermal model cycles at least45.52L/min of ambient-equivalent air solely through three source-length tubes (37.70mL each). Steady bleeding, chamber motion, pressure losses and compressor inefficiency add costs. Shortening each output to30mm reduces its geometrical volume to0.377mL, a factor100. I **do not extrapolate the source time law below its1m calibration range**, or infer a100fold speed/efficiency gain. A regulated steady utility feed still has flow/energy requirements.

Actual Fig7 dimensional data were replayed: across15 nominal specimens, measured XY dimension minus nominal has mean0.044mm, range−0.02…0.15mm; the Z difference has mean0.382mm, range0.28…0.55mm. These are not actual clearances: the mating bore is not specified by that table. They do show why “another FDM printer” cannot silently supply the nominal150µm mechanical interface.

The10 actual Fig9 holding-torque pairs were extracted without fitting: e.g1.69bar→0.0097119Nm,2.01bar→0.0315882Nm,3.61bar→0.116739Nm in the source's tested setup. They are not measurements under our new commutator. Fig10 has63 nonempty torque entries. Comparing its published fit under two header interpretations gives RMSE0.03726Nm for “header=Hz” versus0.004375Nm for “1000/header=Hz.” This supports a timing-coordinate issue but **does not acquire a header-unit conversion**. No loaded frequency/torque guarantee is claimed from that diagnostic. The additional actual rise/fall logs are preserved but their unlabelled columns were not promoted into a calibrated time/pressure interface.

## Why a winding field does not close productive output

An explicit countermodel is a motor with admissible static friction at least A*r*max|z|. It can stay still throughout the same prescribed pressure cycle. In the source-scaled ideal example that bound is0.08074Nm at the crank. This is not the actual source friction; it proves that the pressure-only construction cannot substitute for a delivered-load qualification. Stored/regulated pressure can hide dissipation, and moving chambers change the required flow.

A sufficient model-level following gate can be stated if an independently qualified overdamped receiver obeys b*theta_dot=kappa*|z|*sin(arg(z)−theta)−tau_L with forward field phase speed≤Omega. If kappa*r_min*sin(delta_max)>tau_L+b*Omega, the phase-lag interval[0,delta_max] is forward invariant: evaluate the lag derivative at its two boundaries. A periodic locked response then advances one turn per field cycle. **The source does not acquire that overdamped receiver law or its parameters for our composition.** Actual stall/step tests under the printed buffer/load are the required physical output.

The shortest coupled operation is therefore the printed three-channel relay driving the actual bearingless motor, measuring actual chamber pressures, flow, counted output rotation and torque on the same assembly. A source-like external electronic commutator with identical motor, tubing, pressure and load is the strong actuator comparator. A constant-pressure printed turbine or a mechanical distributor is also entitled to the same resources when counted positioning is not required. The scientific target must not be weakened to mere spinning to escape those alternatives.

## Productive-tool ceiling and disposition

The strongest *demonstrated productive-tool* comparator remains the conventional FDM printer plus its actual extruder/heater/electronics, already able to manufacture active pneumatic devices, including the published autonomous gripper. Making more active pneumatic devices through that fixed service is an **acquired, useful restricted maker→service expansion**. It is not disqualified because the bootstrap printer contains electronics. A completely reproduced printer is not a requirement imposed here. The question is what additional useful productive class this new rotary composition earns beyond that established operation.

If every produced module requires tau_seed of a nonreplicated hotend/cure service and that service supplies total available dutyB, output count is at mostB/tau_seed. Extra printed motion/control modules do not repeal that particular manufacturing bottleneck. This bound does **not** cap aggregate operating output of already-made pumps/grippers or refute useful fixed-seed maintenance/expansion. It only prevents crediting unacquired extra manufacturing-service capacity. The proposed drive still has no source-qualified deposition/nozzle/positioning interface capable of producing its own required precision parts, no all-part assembly operation, and no reproduced thermal service. Its pressure supply and commodity tubing also remain explicit inputs. Neither lifetime nor common-maker fidelity is acquired.

**Natural endpoint:** there is a constructive conditional local-drive interface and genuine source-bound corrections/data replay, but no newly acquired productive-tool closure. A coupled load demonstration would change the actuator question. A same-process productive head plus its actual service/assembly bill would be necessary to change civilisation-level manufacturing priority. More ideal phase/rate tuning would not supply either gate. No claim that this already beats ordinary replicated printers, printed autonomous grippers or standard pneumatic drives is justified.

## Files and retrieval scope

Run python3 phase_drive_join.py; output phase_drive_join_results.json. Primary PDFs, rendered Fig5, selected original data and pinned source-tree metadata are in sources/. Current Astra00_START_HERE was read atf9558b967f5014eced96f229cf89cc4aa7f3490b. The task-first query returned U1022/N755/N796 for lexical terms; none supplies the physical motor/tool interface, and none was imported as a scientific prerequisite. Selected current metadata/shards were checked using the official retrieval code; no original archive or full build was performed. All physical/acquisition/practical limitations above remain.
