# A constructed thermal circulator, and a general limit on what switching buys

Stage 1 produced a complete mathematical/model object: governing proofs, an
executable arbitrary-network solver, exact circulator formulas, a finite-leakage
frontier and executed ordinary comparisons. **A new mission-level scientific
capability has not been established.** Thermal circulation already exists in
primary literature; the present physical implementation is unfinished and the
novelty of the precise mathematical identities is unestablished.

## Question and actual claim

I investigated whether scheduled reciprocal heat contacts, with fixed heat
capacities and fixed terminal temperatures, could create a useful DC thermal
circulator without mass advection or capacity modulation. The initial opening
was directional heat routing with ordinary contacts; a general improvement in
cooling was a separate hypothesis to test.

The result constructed here has two parts. A single fixed-capacity body with
three sequential contacts really does produce a nonreciprocal period-averaged
three-terminal response in its declared ideal circuit model. However, every
finite network in that class obeys an exact static-comparator identity and a
stronger directional-loss constraint. Let average terminal currents be Y theta,
and let Y_* be the ordinary static Kron reduction of the averaged contact graph.
Then

\[
 Y_*-\operatorname{sym}Y
 =\left\langle (X-X_*)^TA(t)(X-X_*)\right\rangle\succeq0,
 \qquad
 Y^TY_*^{-1}Y\preceq\operatorname{sym}Y.
\]

The inverse is on the terminal-temperature contrast space. In normalized
coordinates N=Y_*^(-1/2) Y Y_*^(-1/2),
\(\|\operatorname{skew}N\|_2\leq
\sqrt{\|I-\operatorname{sym}N\|_2}\).
These are quantified statements for arbitrary finite node and phase counts,
nonnegative periodic reciprocal conductances, constant positive heat capacities,
and a connected averaged graph. A uniformly elliptic continuum version is also
given. The proof is in PROOF.md; finite numerical agreement is not its proof.

An immediate physical consequence is that, for any subset of terminals held at
one hot temperature and all remaining terminals at one cold temperature, total
cycle-averaged hot-side heat extraction cannot exceed the averaged static graph.
This includes cooling one hot component into equal-temperature sinks. With many
distinct terminal temperatures, the theorem orders a quadratic Dirichlet form,
not each current individually. Directional routing can still be useful.

## Actual construction and failed first route

The initial two-phase commutator mechanism failed. Its sampled internal evolution
can be nonsymmetric, but reversing a periodic reciprocal network transposes its
DC terminal response. A two-phase protocol is its own reversal up to a time
shift, and therefore has a symmetric DC response. The saved five-node example
has internal monodromy antisymmetry norm 0.0233774 and DC antisymmetry 1.57e-16.
This rules out that entire two-phase route, not all time modulation.

The stronger construction uses one capacity C contacting terminals 0,1,2 in
order, each for P/3, with active conductance g. Put r=exp(-g P/(3 C)) and
\(a=C(1-r)/[P(1+r+r^2)]\). Its terminal matrix is

\[
 Y=a\begin{pmatrix}1+r&-r&-1\\-1&1+r&-r\\-r&-1&1+r\end{pmatrix}.
\]

Forward transfer is a, reverse transfer ar. Thus ideal isolation grows with
contact time, while useful forward throughput vanishes in the infinite-isolation
limit. Exact n-port and arbitrary positive unequal-contact formulas are supplied;
the zero-leak three-port orientation is not restricted to one symmetric fixture.
This is a multi-terminal DC circulation effect, not a two-terminal thermal diode
and not heat pumping between equal-temperature reservoirs.

Finite leakage is included rather than treated as an afterthought. For active
g_on, inactive g_off, total instantaneous conductance
G=g_on+2g_off and alpha=(g_on-g_off)/G, the exact equal-duty response is

\[
 Y_{leak}=\alpha^2Y_0+(1-\alpha^2)Y_*,\quad
 Y_*=(G/3)(I-\mathbf1\mathbf1^T/3),
\]

where Y0 is the exclusive-contact formula with g=G. At any fixed positive leak,
the isolation ratio returns toward one for very slow cycling. A reported
electrostatic thermal-switch on/off ratio of 1000 motivates the sensitivity value
g_off/g_on=.001; it does not validate the assembled device.

For C=1 and G=1 in consistent units, numerical optimization of the exact formula
over the declared finite-rate interval gives:

| Setting, off/on=.001 | z=G P/(3 C) | Forward/G | Reverse/G | Isolation | Hot-port cooling / matched static |
|---|---:|---:|---:|---:|---:|
| Largest isolation found | 6.24720 | 0.0534974 | 0.000766618 | 69.7837 | 0.244188 |
| Largest directional excess found | 1.87256 | 0.127850 | 0.0202166 | 6.32401 | 0.666299 |

These are deterministic model calculations. The one-dimensional numerical
search is not a proof of global optimality over every thermal architecture.

## Strong ordinary comparisons

The same-topology static incumbent uses G/3 for each of the three contacts. It
requires the same total mean conductance and has the same internal body. It is
the **global static optimum for worst-hot-port cooling** under that budget: any
static star with contact vector k has terminal matrix diag(k)-k k^T/G, trace at
most 2G/3 and therefore smallest diagonal at most 2G/9; the uniform star attains
2G/9 for all three ports. The general identity shows that switching cannot beat
this optimum. This is stronger than comparing against an arbitrary weak static
example. If independent contacts can all remain closed, the all-on installed
graph is a further incumbent; its actual holding cost and simultaneous-closure
feasibility must be checked in a physical design.

The contact-control class also admits an ordinary numerical design procedure.
I executed differential-evolution schedule selection using a separate scalar
time-domain integration, allowing all six contact orders, period and unequal
duty fractions, with identical C, contacts, leakage, phase count and information.
It reaches minimum cyclic directional excess 0.107633302231956 G. The derived
equal-duty construction gives 0.107633302255366 G, a difference of 2.34e-11 G.
The ordinary controller therefore reproduces the demonstrated performance.
There is no demonstrated algorithmic or throughput advantage over that control
procedure. The numerical search itself is not a global-optimality certificate.

The mean-conductance comparator is physically admissible only when the resource
set permits its contact values. It must not be substituted for an interlocked
binary switch or a nonlinear material budget without justification. For example,
the recent [autonomous thermal-switching preprint](https://arxiv.org/html/2610.24589v1)
uses a barrier-lowering budget and a spectral-gap objective; exponential rates
make its admissible frozen set different from this convex conductance class.
The present DC theorem does not defeat that result.

## Primary-literature and capability boundary

Static network elimination is established [Kron reduction](https://arxiv.org/abs/1102.2950).
Actual three-port thermal circulation has already been reported with
[convective metadevices](https://doi.org/10.1002/adma.202309835), and a recent
[diffusive circulation proposal](https://doi.org/10.1016/j.ijheatmasstransfer.2026.128474)
modulates conductivity and capacity. Older time-varying circuit circulators are
also close prior art. Consequently the broad operation cannot be presented as
this trial's invention. Whether the precise comparison identities or finite-leak
formula are new remains unresolved; no novelty claim follows from the searches.
SOURCES.md gives exact primary links, inspected versions and retrieval limits.

The remaining physical operation is concrete: realize three independently timed
high-contrast reciprocal contacts to the same retained-capacity body, at a useful
g/C rate, while measuring actuator work, clock energy, parasitic heat and extra
switch storage, and preserving the off/on contrast during the full cycle.
The [measured switch component](https://doi.org/10.1063/1.5009618) does not alone
provide that whole operation. No source data establish its compatible three-port
assembly, full-cycle energy cost, useful throughput or advantage over the existing
physical circulators. Those are not supplied by the ideal equations.

Periodicity also matters: the model pays no repeated benefit from an initially
pre-cooled body. For the equal-contact model, initial-state error contracts by
exp(-G P/C) per complete cycle. Finite preparation and its stored heat must be
counted in a physical full-cycle comparison.

## Executed verification and saved objects

The general solver uses exact segment matrix exponentials and solves the periodic
fixed point. Independent adaptive DOP853 integrations from zero initial conditions
agree within 2.28e-13 in the two-phase case and 7.83e-15 in the leaky circulator.
Eighty equal-contact closed-form cases agree within 8.61e-16; sixty nonuniform
contact cases within 2.50e-15. On 120 varied graphs with 3/4/6 ports, 1/2/4/7
internal nodes and 2/3/5/8 phases, maximum relative reversal and gap-identity
errors are 3.61e-16 and 5.75e-16. Dominance and circle-bound eigenvalues are
nonnegative to double-precision roundoff (worst -1.03e-15). These checks diagnose
the implementation; they do not replace the proof or establish physical validity.
Host matrix-multiplication warnings are retained in run_stderr.txt; explicit
finite-value checks and independent integration found no nonfinite result.

The reproducible files are:

- PROOF.md: governing mathematics, exact scope, continuum extension and comparator.
- thermal_network.py and run_study.py: general solver and scientific calculations.
- ordinary_control_comparison.py: executed ordinary control incumbent.
- NUMERICAL_RESULTS.txt, ORDINARY_COMPARISON.txt and the CSV files: actual outputs.
- two_phase_counterexample.npz and three_port_example.npz: inspectable matrices.
- thermal_tradeoff.svg and thermal_tradeoff.png: plotted finite-leakage frontier.
- RESEARCH_NOTES.md: failed constructions, pivots, resource distinctions and limits.
- SOURCES.md: exact primary provenance.

Reproduce with the supplied /usr/local/bin/python3 by executing run_study.py and
ordinary_control_comparison.py in this folder. No installation is required.

The completed contribution is the explicit operation plus its general limiting
theory and matched comparisons. The experiment's stronger mission remains
unachieved: no novel broadly superior physical capability or established novel
theoretical advance is claimed.
