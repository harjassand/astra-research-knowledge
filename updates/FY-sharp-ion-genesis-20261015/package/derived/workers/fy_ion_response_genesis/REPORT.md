# State-dependent Li/Na exchange: construction, evidence, and stopping decision

The strongest result is a restricted cyclic antiporter construction with exact
modeled reset, together with an acquisition test that does not assume flux
additivity. No new physical operation has been established. The gold/alumina
platform still lacks measured Li/Na species transport, species-selective state
control, full auxiliary reset and whole-cycle work. Existing Donnan dialysis
already performs Li/Na counterflow, and selective electrodialysis already acquires
useful lithium output. The exceptional-capability claim is rejected on current
evidence; a bounded experiment remains scientifically defensible.

Input: full incoming sources/physical_report.txt, treated as archival data;
read-only source checkout at b32943eeb62d0d79929a9e572a344219a785ebf9. Output:
this independent worker packet. No source checkout, incoming source, or Git writes
were made, and no other new worker reports were consulted.

## The operation beyond supplied convex averages

An internal carrier can load Li from the left, release Li to the right, load Na
from the right, and release Na to the left. The affinity and access gates change
between steps. This retains memory of loading, so the correct calculation uses
products of transition kernels and state-conditioned transport rewards.

In an exact synthetic three-state model, four finite reversible phases restore
the binding-state distribution (7,5,5)/17 and transfer

    (Li_R, Na_R, Cl_R) = (2/17, -2/17, 0)

per carrier site per cycle. Every held phase has zero steady transport. Thus
static convex response libraries can miss cyclic transport. This does not make
alternating access, stochastic pumping, or charge-silent antiport new physics.
The required exclusive species/access gates have not been demonstrated in the
source membrane. The calculation resets its modeled binding states, not a real
electrode or all unobserved physical inventories.

The proof packet also gives a general reset certificate: if exchange labels are
a linear combination of salt, charge and other restored-resource labels plus an
internal-state potential difference, no fully reset cycle in that acquired graph
can exchange cations. A measured transient can otherwise be finite storage.
Kernel perturbation and preparation bounds quantify the need to acquire the full
state response. See [proofs/STATE_DEPENDENT_EXCHANGE.md](proofs/STATE_DEPENDENT_EXCHANGE.md)
and [evidence/exact_cycle_results.json](evidence/exact_cycle_results.json).

A common electric potential shifts ideal Li-bound and Na-bound energies equally,
so it cannot by itself switch their equilibrium selectivity. Kinetic or hydration
differences could escape this restricted model; the actual state response is the
missing measurement. The no-pumping cases in established theory similarly depend
on precise fixed-barrier/fixed-well assumptions, not a universal ban on nonlinear
ratchets. [Rahav et al.](https://arxiv.org/abs/0808.0015),
[Mandal and Jarzynski](https://arxiv.org/abs/1109.2871).

## Evidence actually obtained

Publisher source-data bytes for all four Kautz source-data workbooks and its SI
PDF were obtained with hashes. The Fig4b workbook contains 354 dilution and 354
reference conductance values plus 42,877 voltage values. Direct analysis gives a
minimum normalized dilution conductance 0.4934752 at 37.0051 h; the simultaneous
reference is 1.0013474. First crossing below 0.5 is bracketed by 36.0007 and
36.2518 h. The series returns toward equilibrium during later rest, reaching
0.907585 at 94.5253 h. Using the stated 1 mM, 0.63 mL and 0.16 cm2 with constant
volume/proportional-conductance assumptions implies 319.1 nmol removed and
8.62 nmol per elapsed hour, or 0.539 mmol m^-2 h^-1. This is KCl inference from
published conductance, not Li throughput or a pump-on rate. The SI confirms
conductance calibration; no Li/Na inventories or full work are in this workbook.
[Kautz et al.](https://www.nature.com/articles/s41563-026-02511-y).

![Published KCl source values](evidence/published_conductance.png)

Grossman's KCl bipotentiostatic record supplies complementary-surface voltage
control and current reversal, with sample degradation across experiments. The
Ag/AgCl output current measures a compensating difference between cation and
chloride transport. It supplies neither measured Li/Na antiport nor a closed
species inventory after removing that electrical boundary.
[Grossman et al.](https://arxiv.org/html/2511.20174v1).

The 2023 selective-ratchet theory is prior art for electrically retargetable
same-valence sorting. Its central imposed-potential model omits ion interactions
and screening; the later ambipolar model addresses coupled electrostatics but is
not a measured Li/Na specification. Both primary preprint PDFs were acquired.
[Herman et al. 2023](https://doi.org/10.1103/PRXEnergy.2.023001),
[Herman and Segev 2024](https://arxiv.org/abs/2402.09096).

## Incumbents that decide the claim

Abels, Yang and Tarpeh explicitly use Na draw-to-feed counterflow while Li moves
feed-to-draw through a cation-exchange membrane. The published abstract reports
7.6–18.9-fold Li concentration and 22–74% recovery. Acquired SI S2–S3 confirms
1–5 M NaCl draw solutions and the counterflow mechanism; SI S15 gives an example
complex-feed result after 268 h: 229 +/- 3 mM Li in the draw from 28.1 mM feed,
59 +/- 1% recovery, with substantial impurity transport. This consumes a chemical
gradient and has water flux, leakage and regeneration burdens. It is a direct
precedent for counterexchange, not a reset electrically driven separator or a
demonstrated complete-cost win. [Published paper](https://doi.org/10.1021/acs.iecr.4c03482),
[public SI](https://acs.figshare.com/articles/journal_contribution/28083343).

Selective ED provides a stronger measured Li-separation benchmark than the
ratchet's electrical signal. Bilal et al.'s acquired SI Table S3 reports Li flux
46 +/- 3 mmol m^-2 h^-1 at Na/Li=1, and 3.9 +/- 3 at Na/Li=80 for one cell
configuration. The sodium output is detection-limited, although the table calls
selectivity infinite; it must not be treated as mathematically zero. The SI fixes
the feed ratio as Na/Li=80, resolving an ambiguous ratio wording in the abstract.
SI S6 records acid/base pH corrections, and S8 describes about 20 h of ED use for
the aged membrane characterization. These are not unlimited-lifetime or
consumable-free results. No matched cost dominance over a future antiporter is
claimed. [Bilal et al.](https://doi.org/10.1021/acsami.5c20493),
[public SI](https://acs.figshare.com/articles/journal_contribution/31144398).

The 2025 nanocomposite ED paper provides another measured comparator. Its paired
feed/receiving assays and 120-minute experiments are useful acquisition precedents.
The downloaded XLSX has twelve LAMMPS coordinate/configuration sheets, not its
experimental concentration time series; it is labeled simulation source data.
No experimental re-fit was performed from that workbook.
[Nanocomposite membrane paper](https://www.nature.com/articles/s41467-025-63660-3).

For final lithium chemical product, the integrated intercalation/purification and
bipolar ED process in the incoming report remains a stronger endpoint benchmark:
reported battery-grade LiOH above 99.5% purity from Salton Sea brine. Its full
process was not replayed here. [Kong et al.](https://www.nature.com/articles/s41467-025-56071-x).

Li/Na 1:1 antiport is also old biological primary evidence. That establishes
operation-level precedent, not an industrial separator or a transferable
protein-to-alumina control interface. [Sarkadi et al. 1978](https://doi.org/10.1085/jgp.72.2.249).

## Decisive obtaining experiment

The next justified operation is a closed-cycle composition experiment on one
qualified mixture/device regime. Use the source electrical window only as a
fabrication starting point; remeasure it after changing electrolyte or shunts.
Acquire whole-cycle Li, Na, Cl, water, pH and electrode/reference/membrane
inventories for a small two-contact pulse library, with repeatable initial
loading/preparation and interleaved drift controls. Include the actual switching
and return-to-start action in each candidate cycle. Charge chemistry needed to
maintain electroneutrality must be present in both the experiment and the ledger.

The informative test compares complete state-dependent cycles with independently
prepared isolated phases, not a fitted weighted average of current traces. Freeze
a predicted cycle and uncertainty using discovery runs, then validate it on new
runs and at a developed Li/Na exchange affinity. Test a controller that reverses
reservoir assignments from matched initial compositions; reversing time order
alone need not reverse exchange, as the exact fixture demonstrates.

The incoming 25 nmol signal and 2.5 nmol residual targets can be retained as assay
design requirements, not forecasts. A positive result must give simultaneous
inventory confidence bounds, accumulated product beyond a conservatively bounded
initial stored inventory, restored auxiliaries across repeated collection, and
assayed isolated product after its wash/dead-volume/reset losses. Instrument
precision and recovery must be qualified in the actual matrix.

Compare that same collected output and feed against selective ED, Donnan dialysis
with its draw regeneration included, and intercalation where appropriate. Record
all electrical ports and switching work, direct chemical-gradient depletion,
pumping, preparation, sensing, calibration, isolation, consumables and replacement
per accepted product mole. Include rejected cycles and degradation in cumulative
yield and throughput. Zero mean current does not provide an energy estimate.

Stop the operation claim if full-cycle Li/Na exchange is unresolved, dependent
on depletion of finite inventory, absent against the developed total affinity,
lost on auxiliary reset, or dominated by a matched incumbent. The current packet
closes the algebra/source-access work only. Physical acquisition, historical
priority and practical superiority remain open.

## Replay and boundaries

Run code/check_cycle.py with Python 3. Run code/analyze_conductance.py using the
bundled workspace Python with openpyxl; plot_conductance.py uses system Matplotlib
because Matplotlib is absent in the bundled runtime. The source workbooks are
read-only. Original third-party bytes and acquisition failures are segregated in
third_party; extracted text, source coordinates, CSV values and derived results
are in evidence. PDF pages supporting the key SI tables were rendered and
visually checked. Source/data hashes establish documentary integrity only.

Current Astra N774 and its exact direct-force countermodel were read after the
independent construction. They reinforce that waveform signatures cannot identify
the intended mechanism without acquired alternatives. No beta-alumina parameters
or existing conditional lattice theorem were transferred into this membrane.
