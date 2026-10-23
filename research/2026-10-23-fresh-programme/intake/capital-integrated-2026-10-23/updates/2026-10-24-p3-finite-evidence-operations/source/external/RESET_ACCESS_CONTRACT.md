# An obtainable reset is an operation, not a state label

Private P3 scientific-access assessment, 2026-10-23. This note assesses the
unknown-dimension renewal continuation proposed by the root and partial-operation
worker. It supplies an access obstruction and a possible controlled task, not
an application validation. No physical measurements were acquired here.

## 1. Macrostate readout can invalidate the basic composition inequality

The pure-port inequality `q_uv >= q_u q_v` does not extend automatically to a
preparation distribution and coarse readout. Let

\[
r=(1/2,1/2)^\top,\qquad c=(1,1)^\top,\qquad
P=\operatorname{diag}(1,0),\qquad Q=\operatorname{diag}(0,1).
\]

All maps are nonnegative and substochastic, and `c^T r=1`. The measured isolated
responses are `c^T P r=c^T Q r=1/2`, but

\[
c^\top QP r=0<1/4.
\]

There is also a strictly positive example: take
`P=[[0.9,0.1],[0.1,0.1]]` and `Q=[[0.1,0.1],[0.1,0.9]]` with the same r,c.
Then both isolated responses are `0.6`, but the concatenated response is
`0.2 < 0.36`. Thus a named
chemical species, a common fluorescence level, or a binary detector label
cannot be silently substituted for one hidden Markov state.

This is a real experimental issue. Lu, Xun, and Xie's 1998 single-enzyme
experiment found correlations between turnovers, attributed to slow
conformational fluctuations. Pressé, Lee, and Dill's 2013 primary methods paper
treats observed molecular states as potentially unresolved ensembles and
constructs memory-kernel representations. A same-information alternative can
therefore retain non-Markov kernels rather than force a pure-state renewal
model. Sources R1 and R2 below.

## 2. A controller can create the required interface

The useful contract can be stated without knowing the internal state dimension.
Each pulse/control `a` has a no-event map `N_a`, positive and substochastic, and
an event-and-reset map

\[
J_a(x)=r\,\ell_a(x),                                      \tag{1}
\]

where `r` is one fixed normalized preparation and `ell_a` is a nonnegative
functional. The combined instrument must respect total probability. Equation
(1) means that after detection the apparatus actively supplies the same
preparation, independently of the incoming hidden state. It is not merely a
passive claim that two outcomes have the same label.

For a word `a1...ak`, the first-event kernel is

\[
f(a_1\cdots a_k)=\ell_{a_k}N_{a_{k-1}}\cdots N_{a_1}r.     \tag{2}
\]

After that event, (1) resets the next segment to r, so probabilities of
specified successive event segments multiply. Summing over event locations
gives the ordinary renewal recursion. The internal model, rates, and dimension
need not be identified to estimate the kernels.

The same argument works on a quantum positive cone when `N_a` is a completely
positive trace-nonincreasing map and
`J_a(rho)=r tr(E_a rho)`, with a fixed density matrix r and effect `E_a`. This
is a statement about the whole measurement/reset instrument, not about a
state-vector measurement in isolation.

### What would be learned and reused

The learner can measure finite-control first-event kernels, retain their
confidence sets, and predict lower probabilities for new sequences by summing
only warranted event histories. Adding a new control requires measurements of
the previously unavailable mixed segments relevant to the new task. A complete
microscopic generator is unnecessary. This is a scoped acquired operation.

However, when the apparatus provides click times, first-event frequencies are
available directly. Direct retained first-event estimation and classical
renewal composition are therefore mandatory strong baselines. Endpoint
deconvolution must not manufacture an advantage by denying the baseline those
timestamps. Counting only a final outcome is a different, poorer acquisition
interface whose experimental rationale must be stated.

Reset duration, failed resets, fresh-sample consumption if used, detector
dead time, dark events, readout error, and any altered dynamics caused by
monitoring all belong to the acquisition-and-use cost. The controlled task
includes those resets; it is not a prediction of unmonitored biology.

## 3. A useful approximate contract

Exact reset is not essential for a finite-horizon probability target. Suppose
that at each reset, conditional on every allowed previous history, the actual
post-reset state is within total variation distance epsilon of r. In a quantum
model use half trace norm, including all state degrees of freedom relevant to
future evolution. Couple each actual reset to an ideal one, or telescope
contractive channels. For a protocol with at most H resets, the probability of
any final event differs by at most

\[
\min\{1,H\epsilon\}.                                    \tag{3}
\]

Thus an ideal lower probability bound can be reduced by H epsilon and clipped
at zero. This is a general elementary perturbation argument, not a new
learning principle. It is useful only if the uniform conditional reset defect
is itself warranted. A mean reset success rate under a small set of prepared
states does not imply such a bound on every reachable hidden state.

For a known two-level quantum state with ground-state population `1-p`, the
trace distance to the ground state can be as large as `sqrt(p)` when coherence
is allowed. With known diagonal states it equals p. Neither statement covers
unknown additional degrees of freedom. A reported excitation probability
cannot therefore be promoted to an unknown-dimensional reset-channel error
without additional assumptions or measurements.

## 4. Concrete experimental candidate and what it actually warrants

**Controlled microwave-photon detection and reset.** Inomata et al. (2016)
demonstrated a detector that uses a Raman transition for a click and an inverse
Raman pulse for active reset. They report roughly 400 ns reset time and residual
measured excitation `0.017 +/- 0.002`. The physical experiment makes reset a
real, charged operation. A sensible downstream target is a lower probability
of useful detection events or readiness under a specified pulse-and-reset
schedule. Source R3.

This source does not establish equation (1) for an arbitrary unknown-dimensional
device, or the uniform conditional defect required by (3). Its measurements
and model cannot be used as a free oracle for those claims. A practical project
would need a bounded operating domain, independent preparation/readout
calibration, and held-out multicycle protocols testing the target guarantee.
No such data have been obtained by P3. A claim of reliable photon capture must
also distinguish true photons from detector clicks and include calibration of
dark counts and missed events.

**An alternative port.** Thalakulam et al. (2011) physically load and unload
individual electrons using gate pulses and resolve the empty dot using a charge
sensor. Fricke et al. (2013) directly count electron capture outcomes and compare
competing initialization models. These establish obtainable charge preparation,
perturbation, and output measurement. They do not prove memorylessness of all
hidden environmental states. The strongest baseline is their retained counting
statistics and tailored rate/initialization model, not an estimator forced to
relearn each pulse independently. Sources R4 and R5.

Lower empty-state return alone does not certify successful electron transfer:
a device that never loaded also ends empty. A transfer-yield task must acquire
the relevant transfer/count observation or augment the event definition. This
prevents a convenient scalar return target from being substituted for the
consequential scientific task.

## 5. Direct prior prevents a generic novelty claim

Kiilerich and Mølmer (2014) exploit reset to the same ground state to reduce
photon-count records to waiting-time distributions and derive parameter
estimators, including imperfect detection. This is direct precedent for
retaining a kernel instead of a full trajectory. Conversely, Hegerfeldt (1993)
shows that a general post-detection atomic reset can depend on its previous
state. A generic photon click is not a rank-one reset certificate. Sources R6
and R7.

Accordingly, a new claim must concern the exact partial-information guarantee,
its robustness or acquisition economy on changed tasks, beyond classical
renewal estimation and retained program composition. Merely expressing an
experiment as a renewal process does not substantiate cumulative intelligence.

## 6. Scientific decision

The controlled-reset task has a more obtainable interface than unmonitored
hidden-conformation biology. It remains a conditional candidate. The present
evidence does not clear a practical advantage or a newly tractable experimental
application. Preserving a sharp, dimension-independent theorem can still be
valuable; it should be presented at that level until a measured task and reset
contract are available.

### Primary sources inspected

* **R1:** H. P. Lu, L. Xun, X. S. Xie, *Single-Molecule Enzymatic Dynamics*,
  Science 282 (1998). Author-institution primary abstract:
  https://www.pnnl.gov/publications/single-molecule-enzymatic-dynamics .
  Read status: abstract, not the full paper.
* **R2:** S. Pressé, J. Lee, K. A. Dill, *Extracting Conformational Memory from
  Single-Molecule Kinetic Data*, J. Phys. Chem. B 117, 495-502 (2013),
  DOI `10.1021/jp309420u`.
  https://escholarship.org/content/qt3ds8t8t0/qt3ds8t8t0.pdf .
  Read status: primary full text, particularly model assumptions and noisy
  kernel inversion. Its illustrative results are simulations, not new P3 data.
* **R3:** K. Inomata et al., *Single microwave-photon detector using an artificial
  Lambda-type three-level system*, Nature Communications 7,12303 (2016),
  DOI `10.1038/ncomms12303`.
  https://www.nature.com/articles/ncomms12303 ; full primary PDF inspected at
  https://dspace.mit.edu/server/api/core/bitstreams/c6eadc1d-a005-464c-ba0d-ccb9f7c09610/content .
* **R4:** M. Thalakulam et al., *Single-shot measurement and tunnel-rate
  spectroscopy of a Si/SiGe few-electron quantum dot*, Physical Review B 84,
  045307 (2011), DOI `10.1103/PhysRevB.84.045307`.
  Primary accepted manuscript inspected:
  https://link.aps.org/accepted/10.1103/PhysRevB.84.045307 .
* **R5:** L. Fricke et al., *Counting Statistics for Electron Capture in a Dynamic
  Quantum Dot*, Physical Review Letters 110,126803 (2013),
  DOI `10.1103/PhysRevLett.110.126803`.
  Primary preprint `1211.1781v1` read:
  https://arxiv.org/html/1211.1781v1 .
  The HTML regeneration date is not the original publication date.
* **R6:** A. H. Kiilerich, K. Mølmer, *Estimation of atomic interaction parameters
  by photon counting*, Physical Review A 89,052110 (2014),
  DOI `10.1103/PhysRevA.89.052110`.
  Primary preprint `1403.1192v2` read:
  https://arxiv.org/html/1403.1192v2 .
* **R7:** G. C. Hegerfeldt, *How to reset an atom after a photon detection:
  Applications to photon-counting processes*, Physical Review A 47,449 (1993),
  DOI `10.1103/PhysRevA.47.449`.
  Primary abstract inspected:
  https://journals.aps.org/pra/abstract/10.1103/PhysRevA.47.449 .
