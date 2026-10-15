# Control acquisition: an exact theorem, a real information gate, and a changed intervention

Date: 2026-10-15. Historical main inspected at
`33c1ff7ebd9411e9b8b4b0f951f62e36e631cb5d` in the supplied worktree. All new work
is confined to this worker directory.

**Verdict: no indispensable physical control was acquired.** The new binary
source proves conditional exact generic identifiability of the complete binary
response map. Its algorithm can require exponential or worse symbolic work and
arbitrarily ill-conditioned inversion. Its finite-noise obstruction remains
effective on the generic locus. The public-data gate explicitly remains NOT
PASSED; no raw hardware configuration-response or calibration record was
acquired in this work.

There is a substantive new mathematical intervention result, rather than just a
source summary: independently exciting the control-port directions, while
retaining one signed detector, removes the supplied hard family's exponential
acquisition barrier. The source-change operation is not supplied by passive
load tuning. The proof and numerical tests isolate the additional resource
precisely; they do not assert its physical availability.

## What the incoming sources actually change

The response-field proof constructs a list of actual binary configurations that
generates the complete response function field. Its bound is

    Q <= min(2^m, 1+m+m(m-1)+floor(m(m-1)*log2(m))).

I reconstructed the proof logic: choose a transcendence basis, bound its finite
extension degree by Bezout on an injective coordinate slice, and adjoin one
response at each proper field enlargement. Each enlargement at least halves
the remaining degree. Rational expressions then exist for every binary target
off finitely many proper algebraic exceptional sets. The source's independent
audit gives a valid explicit argument for why the slice embeds the entire
response field. This is stronger than parameter counting or local Jacobian rank.

The construction first enumerates all 2^m formal responses, then performs exact
field membership/elimination and rational reconstruction. It does not give a
practical schedule, polynomial running time, robust model selection, actuator
calibration, a noise separation margin, or efficient maximization over 2^m
actions. Genericity of an ambient unrestricted model does not certify a
reciprocal physical subclass. A strictly binary actuator no longer rules out
this exact mathematical operation, but the other physical and numerical gates
remain.

The practical two-anchor schedule supplies O(m^2) generic local identifiability
for m>=5 and a conditional linear pair solver after a common directed anchor
scaffold has been acquired. It does not acquire or globally align that scaffold.
The one-anchor schedule generically fails. The complete anchor response family
can have a finite but unenumerated competing-model fiber; optimizer termination
does not certify that all surviving models have the same future responses.

The shifted-margin estimate is a forward prediction certificate **after** a
valid parameter enclosure is acquired. A fitted center's positive shifted
margin proves stability of that center, not its distance to the real specimen.
Neither a small residual nor this certificate supplies the missing enclosure.

## The strong same-information comparator already wins the supplied design test

I recomputed the joint raw-fit summaries from the immutable 288-start JSON,
rather than relying on the weaker frozen-singleton comparison. This is a
recalculation of supplied synthetic results; no models were refitted here.

| Same raw data budget, 12 paired ground truths | Two anchors | Equal-count random |
|---|---:|---:|
| Median full-table RMSE | 0.006522924 | 0.000759163 |
| Worst full-table absolute error | 0.0440540 | 0.00463685 |
| Median heldout RMSE | 0.00721963 | 0.00101466 |
| Sum of recorded fit time over all starts | 20.5769 s | 12.3518 s |

Random wins the paired full-table RMSE comparison on all 12 instances. The
shared full table matters because each schedule has different heldouts. Both
use four independent raw reads per setting and jointly fit f0,a,B without truth
initialization. This small constructed ensemble does not establish a population
ranking or a global recovery guarantee, but it decisively removes a claimed
practical advantage for this particular two-anchor design. The source's exact
identifiability theorem survives that result.

The equally informed practical competitor is direct physical-model system
identification with raw-mean fitting, multistart optimization, independently
reserved joint-support responses, measured drift/noise, and the same calibration
and deployment costs. It must receive any response-field algebra or added
source access supplied to the candidate.

## Why stronger fitting cannot remove the original noisy obstruction

The explicit (m+2)-state accretive family has only m hidden bits and polynomial
matrix/port/control norms and condition bounds, yet satisfies

    sum_s F_s(u)=1, max_u F_s(u)>=1/2.

At any control vector, only a small number of plants have response above an
absolute noise floor. A valid zero-answer oracle can therefore conceal all but
O(Q/eta) labels along an adaptive transcript. This yields the exponential
uniform bounded-noise decision and prediction lower bounds. The independent
Gaussian chain-rule/KL argument yields an exponential inverse-variance budget
even when measurement precision is adapted to the transcript.

The full-matrix generic perturbation argument puts needles inside the source's
generic good locus without removing this information barrier. It depends on
source-specific exceptional-set degree bookkeeping, which is separately scoped.
The unperturbed noisy lower bound does not depend on that generic extension.
For the uniform hidden label used in the lower-bound proof, Bayesian or
optimization postprocessing, unlimited offline algebra and load dithering do
not supply the missing signal. A stronger informative prior changes the task.

An exact rational query can encode all bits of the promised needle family. This
needs exponentially small absolute error tolerance, which still requires only
polynomially many binary precision bits. It is the independently noisy reading
or inverse-variance resource that is exponential under the stated interface;
do not confuse absolute tolerance with bit length, or impose a universal
precision-to-energy law.

## A different intervention that genuinely changes the information

`PORT_PROBE_PROOF.md` gives a self-contained construction. Turn off the original
source and inject epsilon*p_j independently at selected control port j, keeping
the fixed signed detector. The local response is

    h_j(u)=(1-2s_j)*epsilon/(epsilon+u_j)
                         * product_(i later than j) r_(s_i)(u_i).

When later stages are set to their matching bits and u_j=0, its sign gives s_j
with amplitude at least 4/5. Known stage order needs exactly m probes. With
unknown order, roundwise probing of unresolved ports exposes at least one new
bit per round and needs at most m(m+1)/2 probes. The recovered action attains the
original fixed-source response at least 1/2. This operation works by driving a
latent coordinate that the original source may barely excite.

The derivative identity

    d f/du_j=-(c^T M^-1 p_j)*(p_j^T M^-1 b)

explains why passive load dithering is not equivalent: the desired port-to-output
factor is multiplied by the possibly vanishing local state under the original
source. Calibrated shunt control does not imply a nonzero independently
addressable drive through p_j. This is the specific missing resource, rather
than a vague appeal to more data.

The procedure tolerates constant absolute output error. In the constant-margin
normalization it uses source and detector norms O(m), actuator norm O(m^2), and
only inverse-polynomial direction/value calibration, including O(m^-3) off-state
control leakage. Conditional independent Gaussian averaging gives a polynomial
reading/exposure upper bound. `complexity.csv` compares raw readings and
inverse-variance budgets in matching units and at the same target probability;
it is analytic accounting, not measured instrument time or a hardware benchmark.
Conservative upper-bound constants do not imply improvement at every finite m.

Checks in `RESULTS.json` include 3,586 exact rational probe identities; all 510
labels for m=1,...,8 in both recovery procedures and adversarial |error|=3/16;
independent dense matrix solves with maximum probe-formula discrepancy
5.56e-17; and 40 unknown-order, full-matrix-perturbed, leaky, constant-margin
cases through m=64. The numerical perturbations are not a certificate of the
original generic conditions. All observations are synthetic.

The strongest competitor with the same local sources and chain-family promise
uses the same sign procedure. Thus this is a polynomial-versus-exponential
separation between instrument contracts on the supplied hard family, not an
advantage over equally informed system identification and not arbitrary-plant
identification. A real specimen additionally needs evidence for the restricted
chain-family promise.

## A decisive failure: readout phase remains an acquisition resource

Intensity-only probing fails already at m=1: +1 and -1 local responses both
produce intensity 1. A known coherent reference permits a cross-term identity,
but adds physical phase stability, source addition and calibration. This is
standard network-analysis territory, not a free repair.

Live primary-source reading found an additional strong comparator:
[Virtual VNA 3.1](https://arxiv.org/html/2504.11790v1) experimentally combines
coherent inputs, intensity readout and a known added multiport network to remove
phase ambiguity in a nonreciprocal eight-port system. Its intervention contract
is richer than one fixed scalar binary-load oracle. No raw data were acquired.

[Virtual VNA 3.0](https://arxiv.org/html/2503.07239v1) explicitly distinguishes
loadable ports from ports that can be excited or received, and explains that
connecting external lines can alter a DUT. That distinction directly blocks
assuming the proposed source injections already exist in a metasurface.
[Sol et al. 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC10987616/) remains the
direct experimental binary physical-model-fitting comparator. Its published
availability statement directs readers to the paper/supplement and code by
request; this limited reading/search did not obtain a raw response array.

## Historical-main comparison and operational decision

The actual main's FU measurement analysis already separates information in a
static record from a response revealed only after an extra measurement/control.
Its Clifford countermodel cannot be repaired by scalar smoothing. That is an
analogous contract lesson, not a theorem about the present classical plant.

FV's physical-operation decision remains NO_NEW_PHYSICAL_OPERATION_ACQUIRED:
its proposed salt cycle lacks a same-specimen selective interface and full
restoration accounting. Its root synthesis also warns that missing directional
information, network acquisition and stronger baselines erased apparent gains.
These records do not validate or invalidate the port-probe algebra; they support
keeping actual coupled operations separate from synthetic access changes.

Proceed only if an actual apparatus can independently drive the load ports
without changing the plant. Acquire source direction/gain and detector sign,
control-state calibration, sequence/time, repeats, drift, settling/reset, and
held-out original-source joint-load responses. Compare one-port sequential
probing against the best available multiport/VNA or direct-fit method at the same
complete task and costs. Instrument modification, source-routing calibration,
source/readout energy, precision, reconnection disturbance and reuse must be
charged. The present packet acquires none of these physical records.

The new control source is therefore useful conditional mathematics with a
sharper experimental intervention target. It does not close the physical-control
gate or establish a consequential new capability.
