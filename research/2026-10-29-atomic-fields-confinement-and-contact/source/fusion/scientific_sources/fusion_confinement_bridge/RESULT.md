# Particle confinement in two explicit nonsymmetric vacuum constructions

The concrete López torus has a certified obstruction to enclosed averaged
passing-particle drift surfaces over a continuum of pitches. Its declared
guiding-center and full Lorentz launch sets all cross the source boundary.
The separate irrational Sengupta paraboloid behaves much better in the finite
guiding-center diagnostic, but four high-pitch launches cross the chosen
diagnostic tube after more than 100 bounces. Neither result establishes a
fusion technology or a general impossibility theorem.

All new work is in this folder. The previous X-ray and positive-current
constructions are frozen. Source-formula APIs and the Sengupta findings were
handed to the complementary worker; no files in its owned directories were
edited.

## The new construction and its scope

For [López, arXiv:2610.29921v1](https://arxiv.org/html/2610.29921v1), define
`h=|X_φ|=1/|B|` on the paper's certified domain
`Q=900(λ−.15)²+100(β−.02)²<1`. At energy `E=1/2`, the positive passing
transit action is

\[
 J(\lambda,\beta,\kappa)=\int_0^{2\pi}\sqrt{h^2-\kappa h}\,d\phi,
 \qquad\kappa=\mu/E.
\]

`verify_passing_action.py` constructs a directed interval enclosure on the
whole rectangle `[7/60,11/60]×[−.08,.12]`, which contains the source label
disk, and **every** `κ∈[0,.1]`. With 8×8 label boxes, 512 angular intervals
and 30-digit interval arithmetic it obtains

\[
 h\ge .1488166013419809>.1,\qquad
 J_\lambda\ge11.91784956603872>0.
\]

Thus these particles are uniformly passing in the frozen-line problem, and
their averaged action contours cannot close inside this volume. For either
parallel direction the leading physical-time transit displacement is
`Δβ=−2ελ J_λ+O(ε²)`. Selecting a different magnetic-surface label inside
the same volume does not restore the absent closed passing-action contours.
The elementary metric expression, exact equations within the first-order GC
model, drift-sign derivation and interval algorithm are in `DERIVATION.md`.

The enclosure concerns an analytic action and its averaged drift topology.
There is no quantitative averaging-remainder or validated-ODE bound here.
It does not establish all-initial-condition finite-ε loss, exclude exceptional
finite-ε islands, constrain other pitch ranges, or exclude useful confinement
in an enlarged continuation of the field.

## Unaveraged and full-orbit checks for López

The GC ensemble is declared by `guiding_center_ensemble.py`: nine label
positions (axis and two ellipse radii with four angles), four toroidal phases,
four uniformly passing pitches and both parallel signs give 288 launches.
An additional 54 initially trapped launches use three mirror-depth fractions
at each position and both signs. Every orbit is retained, including losses.

| Model and parameter | Declared count | Boundary crossings | Crossing-time range |
| --- | ---: | ---: | ---: |
| GC passing, ε=.004 | 288 | 288 | 4.674–31.176 |
| GC initially trapped, ε=.004 | 54 | 54 | 6.511–44.612 |
| GC passing, ε=.002 | 288 | 288 | 9.528–62.204 |
| GC initially trapped, ε=.002 | 54 | 54 | 12.459–88.563 |
| Full Lorentz, ε=.004 | 72 | 72 | 15.902–18.252 |
| Full Lorentz, ε=.002 | 72 | 72 | 32.029–36.566 |

All GC passing trajectories had no mirror bounce; all initially trapped
trajectories bounced. Halving the GC step preserves every crossing flag and
changes crossing times by at most `1.96e−5` (relative `1.32e−6`).

The full Lorentz set is independently specified at the GC axis: four toroidal
phases, `μ/E∈{0,.06,.1}`, both signs, and four gyro phases when perpendicular
speed is nonzero. The actual particle is displaced from the GC center by the
leading Larmor offset. `full_orbit_boris.py` uses a magnetic Boris integrator
and prescribed cubic-root continuation, without changing to a different
min-Q root after departure. A uniform-field center check has error
`3.71e−17` over 10,000 steps.

The maximum full-orbit/GC crossing-time disagreement falls from 1.844% to
.925% when ε halves. A 40-launch matched half-step Lorentz refinement
preserves every flag, with maximum crossing-time change .05045%. Full-orbit
speed-squared errors are at most `1.26e−13`; the largest Newton root-error
estimate is `3.15e−16`. These are numerical controls, not continuous-time
certificates. Instantaneous μ is not exactly conserved: its observed maximum
absolute deviation from the declared GC μ is `.00405` at ε=.004 and
`.00200` at ε=.002.

The observed local parameter `ε|∇B|/B²` is at most about `.0111` in the GC
tests and halves with ε. This is a local adiabatic diagnostic; it does not
certify all higher derivatives or long-time reduction error. Loss means an
endpoint crossing of the source's Q boundary with linearly interpolated time,
not proved escape from a globally realized magnetic device.

## The irrational Sengupta member is a separate diagnosis

`sengupta_paraboloid.py` independently implements equations (1), (2), (5)–(7)
of [Sengupta et al., arXiv:2610.28466v1](https://arxiv.org/html/2610.28466v1).
It uses the reference `ι=1/√5` paraboloidal member, `K′/K=5/2`,
`u0=acosh(√5 sech(2π/5))`, `v0=δ=0`, `κ_profile=2K′/π`. Complex Jacobi
functions are built from real addition identities and compared with mpmath
at 40 digits. The source minus sign in the second component of X is required
for its metric. Analytic field-strength and surface-label derivatives are
implemented. The relative finite-check `B·∇ψ` residual is `7.28e−14`.

This member is distinct from the paper's ellipsoidal N=3 trapped iso-action
example. That published class is established prior and is not claimed here as
a discovery. Complete construction/proof/code details are referenced by the
source to a companion article still listed as “in preparation”; this branch
uses the explicit formulas actually available in v1.

The declared diagnostic tube is `0≤ψ−ψ_axis<.2`, with
`ψ_axis=11.708211569340728`. A 4096-point boundary diagnostic checks the
source restrictions `u>|v|`, `|κ_profile(u−u0)|,|κ_profile v|<K` and has
substantial sampled margins; this is not a rigorous certificate of the whole
surface. A nominal `ρ/a=.005` is calibrated using the arclength-mean axis
field and the **sampled minimum local** boundary distance, giving
`ε=.0036062239615646907`. This is our calibration, not a matched reproduction
of the paper's different radius definition/member. Axis length is
`5.787486795595374`; its transit time at speed one is the clock used below.

The primary 432-launch design uses nine label positions, four distinct phases
`ζ∈{0,π/8,π/4,3π/8}`, perpendicular speed fractions
`χ∈{0,.05,.2,.5,.8,.95}`, and both parallel signs. It integrates 50 axis
transit times using the same vacuum GC equations in Cartesian form transformed
to source coordinates.

| Initial χ | Declared launches | Orbits with a bounce | Tube crossings |
| --- | ---: | ---: | ---: |
| 0 | 72 | 0 | 0 |
| .05 | 72 | 0 | 0 |
| .2 | 72 | 0 | 0 |
| .5 | 72 | 0 | 0 |
| .8 | 72 | 48 | 0 |
| .95 | 72 | 67 | 4 |

The four crossings occur at 41.57–44.63 axis transits, from label radius .7
and angle π/2, at ζ=π/4 or 3π/8, both parallel signs. They have 102–106
bounces before crossing. A predetermined 80-launch high-pitch subset at the
axis and all four outer label positions, rerun with half the step, reproduces
all four flags. The maximum crossing-time change is `1.14e−5` (relative
`4.68e−8`). Refined loss-orbit energy errors are below `1.83e−11` and their
observed local adiabatic parameter is about `.00159`. No source coordinate
regularity check failed. The remaining 428 launches survive inside the tube
at the stated finite horizon; this is not a proof of permanent confinement.

An initial 432-launch grid used phases `0,π/2,π,3π/2`, which all sample the
same high-field axis phase. It showed no exits. The weak phase coverage was
identified, the entire result and its 48-launch refinement were preserved as
`sengupta_ensemble_initial.json`, and their computation is charged. They are
not the primary conclusion. No failed or escaped orbit was selected away.

The four exits occur **while the source formulas remain regular**. They may
belong to larger closed drift surfaces outside our tube. No global escape,
whole-family loss, omnigenity classification, or full Lorentz result for this
member is established. Boundary geometry and ε differ from López; counts
cannot be treated as a matched performance comparison or probability.

## Ordinary comparator and capability assessment

Action-averaged confinement, quasisymmetry and alternative action closure are
established prior. [Sengupta, Bhattacharjee and Buller (2026)](https://arxiv.org/html/2608.20042v1)
already formulate iso-action as closure of the orbit-selected drift surface,
including branch changes. Requiring every local bounce action to be constant
on a magnetic surface would therefore impose a false prerequisite.

An equally informed ordinary comparator is optimized quasisymmetric or
quasi-isodynamic stellarator geometry, assessed with GC and full-orbit
particles and a realizable coil field. [Landreman and Paul (2022)](https://arxiv.org/abs/2108.03711)
already obtain highly precise numerical vacuum quasisymmetry over significant
volume. [Wechsung et al. (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9060451/)
add separated, low-curvature coils and reactor-scaled energetic-particle
simulations. Their reported best GC loss at midradius is .04% at 200 ms.
That source-specific result cannot be compared numerically with this branch's
deterministic, differently scaled launches.

The exact families remove an equilibrium/field-evaluation ambiguity, but
particle-safe action topology and finite orbit width remain separate design
operations. The constructive opening established here is an inexpensive
**continuum rejection certificate** for a proposed closed-line confinement
volume, plus replayable source-coordinate particle machinery. In the López
example it replaces selected favorable-orbit reasoning with a whole-volume,
whole-pitch-interval obstruction. This is new internal analysis of that source
example, not a claim that transit-action theory, interval arithmetic, GC
integrators or stellarator code benchmarks are novel. No exhaustive external
priority search for this particular derivative-sign certificate was performed.

For the irrational family the better operational target is closure of
orbit-selected actions *inside an available wall* across a declared pitch and
energy distribution. The present distinct-phase construction exposes an
actual wall/class failure instead of assuming that exact nested field lines
solve it. The complementary worker owns the next structural action/current
test. No demonstrated advantage over ordinary confinement optimization, no
reactor design and no civilisation-changing physical capability follow yet.

## Evidence, replay and costs

The actual used cores are `lopez_native.py`, `lopez_formula_snapshot.py`,
`sengupta_paraboloid.py`; actual used verifiers/drivers are
`verify_passing_action.py`, `verify_formulas.py`,
`guiding_center_ensemble.py`, `full_orbit_boris.py`, `sengupta_ensemble.py`.
The source-formula snapshot was copied read-only from the coil worker and
then checked independently. `formula_snapshot.json` pins its provenance.

`verification_results.json` reports replayed local formula checks.
`passing_action_interval.json` contains every interval box.
`guiding_center_results.json`, `full_orbit_results.json`, and both Sengupta
JSONs retain individual launch definitions and results. The two separate
convergence JSONs summarize the matched full-Lorentz and Sengupta refinements.
`run_manifest.json` records versions, code hashes and measured runtimes.

Replay from this workspace with `OPENBLAS_NUM_THREADS=2` and
`PYTHONDONTWRITEBYTECODE=1`, using Python 3.14.3/NumPy 2.5.3. The Sengupta
module and interval verifier load SciPy 1.18.1/mpmath 1.4.1 read-only from the
frozen sibling's `positive_current_operation/vendor` directory. Run each
named verifier/driver as a Python script. Formula checks take under a second;
the interval enclosure took about 6 seconds. The final López GC runs took
18.6 seconds, Lorentz runs 166.8 seconds, final Sengupta runs 150.5 seconds;
the retained weak-phase Sengupta diagnostic cost another 140.2 seconds.
Total recorded algorithm runtime is 482.1 seconds, excluding source retrieval,
derivation and tool overhead. These are local runtimes, not a speed advantage,
billable token count or full research cost estimate.

The two v1 HTML sources are pinned by URL, byte count and SHA256 in
`source_manifest.json`. No physical field was acquired. Coil realization and
metrology, rejected-particle recovery and wall loads, collisions, electric
fields, plasma response and finite pressure are all uncosted/unvalidated at
the device level. No physical experiment, purchase, paid compute, outreach or
public write was performed.
