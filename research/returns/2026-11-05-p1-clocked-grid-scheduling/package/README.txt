ENERGY SCHEDULING FOR CLOCK-DRIVEN GRID DISTURBANCES
Research return, 5 November 2026 (Australia/Brisbane)
=================================================

OUTCOME

This work starts with measured one-minute disturbances in electricity grids
and a documented incomplete firmware mitigation. It provides a complete
conditional mathematical scheduling construction, exact rational software
certificates, public-data reanalysis, and explicit limits. It does not
establish a new physical source mechanism, historical priority, a deployed
UPS controller, or a civilization-changing breakthrough.

The question is: when diagnostic tasks are indivisible and must retain their
service cadence, what physical disturbance can timing control remove, and
what timing, calibration, controllability and execution resources are
indispensable? The answer is proved for recurring known waveform classes,
with a complementary arbitrary-waveform certificate for selected harmonics.

The observational anchor preceded Astra retrieval. Hartmann et al., Nature
Energy, published 30 October 2026, identify minute-locked disturbances in 12
grids. Their local UPS investigation traces a self-test-related signal to the
110-kV connection and includes clock and firmware interventions. They already
discuss random scheduling and timing remedies. We use the final paper rather
than mixing its claims with the materially different October 2025 preprint.

MEASUREMENTS AND RECALCULATIONS

The actual public data version is DOI 10.5281/zenodo.21997337, created
18 August 2026. Concept DOI 10.5281/zenodo.17366692 resolves to that version.
Selected unmodified source workbooks, extraction code and hashes are included.

1. The post-update column 'Current 3' has three large-event starts at 86, 145,
and 506 seconds, or phases 26, 25, and 26 seconds modulo 60. The detector uses
the start of each contiguous run above half the channel maximum. Its circular
concentration is 0.9987819015. This short-trace descriptive calculation
confirms retained phase locking already documented by the paper. It is not a
new causal experiment or population estimate. The supplement calls the
updated physical unit block 1; its mapping to the workbook channel is
unresolved, so the literal source-column label is retained.

2. The three building meters provide 16 weekly-labelled profiles each, with
20 samples at three-second resolution: 48 profiles and 960 power values.
In every week, the largest minute-frequency coefficient exceeds the sum of
the other two. For freely shiftable profiles, the exact best possible summed
fundamental magnitude is

    max(2 max_i |c_i| - sum_i |c_i|, 0).

The floor is 83.2045 to 99.1962 W in complex-coefficient magnitude, or
166.4091 to 198.3924 W in the peak amplitude of that sinusoid. We use
c_k=(1/L)sum_j p_j exp(-2*pi*i*k*j/L), so sinusoid peak amplitude is 2|c_k|.
The transformer profiles are aggregates. Independent phase control of all
three complete profiles is a generous counterfactual, not measured access.
These are sampled-profile results, not uncertainty-qualified bounds on
unmeasured continuous power. The final weekly label is 7 July, while the
documented acquisition ends 3 July 2024.

3. Exhaustive 20-slot phase optimization on each week reduces the first-three
harmonic RMS by 3.2 to 23.8 percent. Two weekly band optima nevertheless
increase sampled absolute peaks. Freezing the earliest week's optimum at
[0, 12, 45] seconds makes band RMS worse in 10 of the next 15 weeks. The
median ratio is 1.047742 and the worst ratio is 1.140773. This retrospective
out-of-week counterfactual is not a preregistered prospective test or an
independent experiment. It rejects an unqualified claim of lasting benefit
from a single calibration of these profiles.
This tests frozen relative offsets applied to changing weekly profiles. It
does not test an implemented controller enforcing absolute task launch times
or recalibrating the operating response.

4. The Irish monthly waveform half-ranges are 1.779898 mHz (December 2016)
and 7.012353 mHz (December 2021), ratio approximately 3.940. Half-range,
first-sample drop, and fundamental amplitude are different observables.

EXISTING EXPLANATION AND SYSTEMATICS

The source authors already establish the local clocked UPS mechanism.
Resonance, control changes, effective inertia, changing demand, other clocked
devices, and measurement resolution affect the grid response. Local UPS
attribution does not establish an exclusive worldwide UPS origin. Some
unaffected-campus measurements have higher noise, so absence of a visible
line is not proof that no small source exists.

The before-update trace contains seven absent timestamps and nine additional
missing values in one channel. The extraction preserves timestamps and
missing observations. Raw MODBUS DC currents require a 0.1 conversion, but
the ampere-labelled Figure 7 columns must not be blanket-rescaled. The
three-second building averages do not resolve subsecond pulse shapes or
certify millisecond dispatch. These limitations remain in every replay.

An elementary lattice calculation explains why irregular gaps can preserve
coherence. If tasks remain at times nT+phi with stationary ergodic energy
marks Q_n of mean e, their coefficient at k/T is

    (e/T) H(k/T) exp(-2*pi*i*k*phi/T).

Randomly skipping tasks while compensating their energy leaves this line
unchanged when the kernel shape is fixed, and can add broadband noise. A
changed pulse duration changes H and must be included. The published trace
does not establish an iid marking model; this is a conditional explanation,
not a fit to three events. See lattice_randomization.txt.

CONSTRUCTION AND EXACT THEOREM

In each class c, device i performs a causal signed waveform e_i h_c once
every T, where e_i>0 and integral |h_c|=1. The full diagnostic and recharge
response at the grid-facing interface belongs in h_c. Assign

    phi_i=T(sum_{j before i} e_j + e_i/2)/E_c,
    E_c=sum_{i in c} e_i.

For the weighted event train minus its uniform mean, a primitive F_c jumps
from -e_i/2 to +e_i/2 at event i and decreases linearly between events. Its
oscillation is exactly e_max,c. Every phase schedule has a jump at least
e_max,c, so the schedule is optimal for this cumulative event-energy metric.

If every event may move independently by at most delta, then on a sufficiently
long schedule the exact one-class minimax law is

    inf_phases sup_errors osc(F)=e_max+2(E/T)delta.

The upper bound follows by counting events between t-delta and t+delta.
Matching extremes follow by advancing events near one extremum and delaying
events near a distant extremum. The exact lower bound is not asserted for
one fixed offset per device or a short observation horizon.

Convolution with a signed unit-L1 event kernel preserves the centred bound.
For fixed repeated waveform errors r_i with integral|r_i|<=eta_i,

    B=sum_c[e_max,c+2 E_c delta_c/T]
      +sum_i[(1+2 delta_i/T)eta_i]

bounds the oscillation of a primitive of actual mean-removed power. The
factor multiplying eta_i accounts for timing error acting on that residual.
Arbitrary per-cycle changes require an additional cumulative-energy contract;
an unsupported stationarity assumption cannot supply an all-time guarantee.

For a supplied stable causal response kernel g of bounded variation,

    peak incremental frequency <= (B/2)(|g(0+)|+TV(g)).

For M*f_dot+D*f=-u, M,D>0, this is B/M. Initial response and uncontrolled
disturbances remain separate. The paper's static power-frequency slope does
not identify this dynamic kernel. Different injection locations need
compatible effective-response classes or a network model. Energy bounds
alone do not control instantaneous power or RoCoF. For BV kernels there is
also a power bound, with complete proof in theorem_energy.txt.

EXECUTION AND RESOURCE BILL

The scheduler changes task timing and needs manufacturer-supported control
that preserves diagnostic validity. It acquires no new high-bandwidth pulse
actuator. Calibration must cover the complete AC response, operating state,
recharge, temperature, clock drift, and firmware state. This software cannot
substitute for those physical measurements or access rights.

Midpoint construction takes O(N) arithmetic. Each endpoint retains its phase,
period, schedule version and executed-event state; no per-cycle central
message is needed. The supplied compiler uses exact rational arithmetic,
rounds to actual timer ticks, and verifies primitive extrema at event
boundaries without temporal sampling.

Commissioning advances tests with shorter permitted intervals until the new
phase is reached. The compiler takes the old nominal phase explicitly and
checks minimum recovery and maximum deadline with 2*delta guards. Nominal
work advances by less than one period, bringing at most one nominal extra
execution into the transition window. Timing and waveform uncertainty need
their own transient reserve. The balanced steady bound is not asserted
throughout migration. If spacing is immutably T and no early or late test is
allowed, no phase migration is possible.

Phase and event state must survive reboot. A burst replay of missed tasks
defeats balancing. Mandatory immediate safety tests after a simultaneous
restart form a separate load. Membership changes require recompilation or
a dropout budget. The mean power demand is not removed by scheduling.

With Q=T/q timer slots, midpoint rounding gives event span at most e_max+E/Q
before other errors; some slot carries at least E/Q energy. Fixed timing
precision therefore does not guarantee fixed absolute accuracy as a fleet
grows on the same grid. Independent systematic waveform errors also add in
the worst case. Actual smoothing can reduce slot aliases, but must be
measured rather than inferred from an unresolved sampled waveform.
Shared errors can be less harmful: a constant common time offset only shifts
the whole schedule, and a common positive energy gain within a class simply
rescales its bound. The independent adversarial error floor is not universal
over all correlation structures or over grids whose physical response scales.

NUMERICAL EXECUTIONS

Synthetic single-class instances used 16, 64, 256, 1024 and 4096 devices with
integer weights from 5 to 100 J, T=60 seconds and a 1 ms timer. At 4096
devices, event-energy spans were: aligned 213849 J; one independent-random
draw 6335.321 J; weighted midpoint 103.3783 J. These are mathematical
instances, not UPS measurements, random-phase percentiles, or observed grid
improvements. The ideal exact bound is 100 J; timer rounding is charged.
Signed-kernel and illustrative first-order replays satisfy the bounds.

For a fabricated population of 200 replicated measured templates, K=3 and
20 allowed phases, the harmonic constructor leaves six fractional devices
before deterministic rounding. Final band RMS is 133.684 W, compared with
an independent-random root-mean-square reference of 1338.191 W. Full sampled
RMS is still 741.459 W. This verifies the implementation and the distinction
between a selected-band and whole-waveform claim. Replicas are not observed
devices or independent experimental units. The current demonstration code's
support scans give O((NM)^2+NM(2K)^3) arithmetic; an active support list can
remove the quadratic scan overhead. No exact bit-complexity claim is made.

ALTERNATIVES AND NOVELTY

The source paper already proposes desynchronization and reports an update.
Independent random fixed phases give expected squared harmonic amplitude
sum_i |c_i|^2 and may already be operationally adequate. Asymmetric converter
interleaving, distributed DESYNC, weighted fair queuing, network-calculus
jitter bounds, and Shapley-Folkman load aggregation are established. We do
not claim their discovery or an exclusive ability to mitigate this problem.

The combined resource law, compiler, whole-response bound and data checks
are a specialized construction. Priority of the exact combination remains
unestablished. The observed failure does not imply new microscopic physics.

ASTRA USE

After the empirical question was anchored, Astra was pinned at revision
2d22b00d4ec6ce4cd894a345c900d53de79ea631. Relevant current packets and actual
governing sources were read. U1042's checked-proposal/exact-certificate
discipline informs direct verification of the rational schedule. No N24
signing theorem is imported or strengthened. U1683's response/metrology
distinction is relevant, but its reciprocal thermal-RC assumptions do not
apply to an arbitrary grid; its response guarantee is not imported. See
astra_retrieval.txt for immutable URLs and source hashes.

REPRODUCTION

With Python 3, numpy, scipy, matplotlib and openpyxl:

    python reproduce.py
    python harmonic_replay.py
    python compile_schedule.py fleet_input.json fleet_schedule.json

These regenerate measurements, exact synthetic checks, figures, selected-band
comparisons, and a four-device example at phases 6,24,39,51 seconds. The
example's full primitive-span budget is 20.2033466667 J with explicitly
synthetic input. The code operates no UPS or grid and requires no network
after extraction of the included inputs.

Full proofs: theorem_energy.txt and math_note_harmonic.txt.
Evidence audit: evidence_note.txt. Lattice calculation: lattice_randomization.txt.
Numerical outputs: results.json and harmonic_results.json.
Data and provenance: data/ and astra_retrieval.txt.

DATA ATTRIBUTION

Edoardo De Din, Daniele Carta and Carsten Hartmann, Data for 'One-minute
frequency disturbances from unintended synchronization in cyber-physical
power systems', DOI 10.5281/zenodo.21997337, CC BY 4.0. Included source
workbooks are unmodified. Extracted tables, Fourier calculations, event
detection and figures are transformations described by the supplied code.
Paper: https://doi.org/10.1038/s41560-026-02144-0.
Data: https://doi.org/10.5281/zenodo.21997337.
License: https://creativecommons.org/licenses/by/4.0/.

SCIENTIFIC DESTINATION

The conditional scheduling problem is resolved mathematically and its
uncertainty costs are explicit. Deployment-specific firmware access, full
waveform metrology and grid response remain unacquired. The evidence supports
a consequential engineering problem, but the present result does not yet
establish the requested civilization-changing physical capability.
