# Graph instrument audit — frozen checkpoint

The proposed two precision ports do not yet establish a physical adaptive
acquisition advantage. I obtained an exact full-data thermal limitation
for the correctly routed, grounded-leaf configuration; a two-bus change
of measurement architecture can escape it, but needs extra hardware and
acquired membership. Giving the same interface full opening also admits
a strong ordinary nonadaptive resistance-measurement incumbent. Actual
instrument performance and any matched physical advantage remain UNKNOWN.
Mission: NOT_ACHIEVED. No equipment, purchases or third-party contact.

The earlier oxygen packet is preserved byte-for-byte outside this
directory. OXYGEN_FREEZE.json records that separate checkpoint; this
assignment neither supersedes its conditional results nor adds physical
evidence to them.

## Strongest results and their exact limits

1. **Full-data thermal information.** For the stipulated classical
uniform-temperature resistor model plus independent sensor spectra,
C_theta=nu M_theta+Sigma. A core edge changes BOTH mean and covariance.
The exact Gaussian KL includes1/2[z-ln(1+z)] even at zero command; the
fixed-iid-noise ANY-q obstruction must not be transferred. With two known
precision hubs g_h~d, grounded ordinary leaves, positive fixed ordinary
sensor noise s_o, and all terminal outputs used optimally, the exact
coefficient H=u^T C_0^-1u is Theta(1/d), including unequal hub/leaf sensor
floors. Thus this fixed configuration needs a conditional tradeoff
q/d^2+E_row/d=Omega(1), where E_row is duration-weighted squared voltage,
NOT Joules. Root's separately frozen uniform hub-precision bound is a
related conditional result, not a fresh review here. Full proof and
power restrictions: THERMAL_FULL_DATA.md.

2. **Explicit bus escape, with its preparation paid.** Once full star
membership is acquired, route all external ends in each star to a common
bus and sense current before fanout. Its exact core-present conductance
is [1/a+1/D_U+1/D_V+rho_U+rho_V]^-1, D_h=g_h+sum_j a_j/(1+a_j r_j).
Internal thermal currents cancel before independent ADC errors appear;
constant final DC signal/noise is possible in that changed model. It
requires n assignable bus connections and qualified off-load, not merely
two individually routable contacts. A conditional membership-current
test has a constant per-leaf gap, but its correctly routed hub drivers
still need O(a n A) current at O(1/(a n)) effective resistance. PhaseI,
switching, calibration, O(n C A^2) charge/reset energy and thermal recovery
remain paid and unacquired. Full process: TWO_BUS_INTERFACE.md.

3. **An opening interface strengthens the incumbent.** In W73's ideal
open, settled fixed-noise model a precommitted random pair continuity
test can distinguish the two-star family with constant action count at
fixed error. PAIR_BASELINE_RECONSTRUCTION.md gives a local proof and
explicit Gaussian repetition/error constants, crediting W73 for the
communicated comparator. This is ordinary switched resistance measurement. I derived
the exact received-current qualification when every unselected terminal
leaks conductance g to ground:

    J=a p^2 A/[(p+H)(p+H+2a)],
    p=a/(1+a r_s), H=g+(d-1)ag/(a+g).

Constant relative contrast needs dg=O(a); fixed positive g gives
Theta(d^-2) mean contrast. This is a receiver-mean circuit calculation,
not an all-data lower bound on the incumbent.

4. **Settling is not detection time.** With perfect DC opening but C on
each unselected leaf, an explicit reset-zero selected-leaf pair step has
two time constants Theta(d). Nevertheless its mean-only continuous
record under separately stipulated fixed white receiver noise has KL
asymptotic to a^2 p^4 A^2 T^5/(40 S C^4 d^4). It reaches constant mean KL
at Theta(d^(4/5)), earlier than full settling. Other preparations,
commands, transient and covariance sensing are not excluded. This
corrects the tempting but invalid claim of a universal linear detection
time. Exact equations: OPEN_TERMINAL_QUALIFICATION.md, frozen
SHA256149fb305e31dd169f00fa8f74e7cae7b2ad0382df85fe5043034db8a5d034740.

## Verification and provenance

replay_instrument.py performed2,344 exact Fraction assertions across40
full nodal circuit fixtures, plus8 Decimal transient-information roots
and3 independent full-leaf-state RK4 comparisons. The largest RK4 current
error was3.61e-16 in dimensionless fixtures. replay_two_bus.py performed
486 further exact assertions across18 weighted-star fixtures, including
an expanded circuit with physical aggregate series resistors and the
membership-current inequalities. These58 exact cases and11 transient
cases are finite synthetic verification, not physical experiments or
general proofs by enumeration.

Original primary bytes retained: Nyquist1928 full article scan; TI
SZZA030E revisionE; Keithley Switching Handbook sixth edition. Their
noise, burden, switching and ordinary resistance-measurement principles
are historical prior. Relevant source sections were read; no claim is
made to have read all194 pages of the handbook. ADI instrumentation
articles were read through the web and those tool extracts retained;
failed raw-HTML/PDF retrievals remain explicit. READ_LEDGER.json,
PRIMARY_ACQUISITION.json and PRIMARY_SOURCES.md bind source versions and
read scope. FAILED_INFERENCES.md preserves rejected shortcuts.

The generic thermal law and current aggregation are established prior;
the exact scoped formulas' external correctness and novelty are UNKNOWN.
There is no acquired n-port device netlist, current trace, qualified
switch matrix, measured covariance, actual energy/settling result or
physical advantage in this packet.

## Decisive next acquisition gate, not executed

Obtain a qualified driver/switch/sensor netlist or existing synchronized
terminal/bus traces for the SAME configurations. Acquire terminal
burden/compliance, joint current and source-voltage spectra versus gain,
temperature and routing, aggregate leakage/capacitance, settling and
reset tolerances, calibration drift and power. Determine whether noise
is added before or after aggregation and how many independent frequency
modes a record supplies. The stipulated iid, thermal-plus-ADC and bus
laws have materially different information content.

Then compare the grounded-leaf adaptive schedule, bus schedule, ordinary
open-pair continuity/precision switching and coded ordinary schedules
using equal hardware access, acquired calibration, elapsed time, Joules,
source/sink current, stored charge, precision/contact capacity and error.
No physical winner can be inferred before that common-interface gate.
Equipment operation is outside the present authorization and was not
attempted. Continuation is a frozen record only: the user instructed the
team to finish and idle, so no further mechanism or experiment is active.

Primary references: [Nyquist1928](https://doi.org/10.1103/PhysRev.32.110),
[TI signal-switch revisionE](https://www.ti.com/lit/an/szza030e/szza030e.pdf),
[Keithley Switching Handbook](https://download.tek.com/document/SwitchingHandbook.pdf).

Status: conditional local analytic results; fresh independent proof
review UNKNOWN; finite synthetic checks PASS; historical sources ACQUIRED;
physical experiment NOT_PERFORMED; practical advantage UNKNOWN; exact
novelty UNKNOWN; mission NOT_ACHIEVED; worker FROZEN_FOR_USER_DRAIN.
