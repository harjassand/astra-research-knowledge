# What the completed operation changes

30 October2026. The completed operation returns a reusable, classically
stored physical Clifford decoder from fresh opaque-source Bell records.
All source use finishes before the unknown payload. It applies to a
mixed Clifford encoding whose logical Pauli images have warranted small
patches, with arbitrary mixed/entangled junk and actual coherent or
dissipative source calibration. Quality follows from fresh actual-channel
tests, not from assuming an exactly identified hidden encoder.

The exact finite128-output computation returned five nearest-neighbor
gates, including two CNOTs. It consumed995328 discovery records and131072
fresh validation records. Its Bell-fidelity lower bound is.9915913 and
its general all-input halfdiamond bound is.1833979. The source is a
computational Born-law backend; no laboratory calls, calibrated detector,
native noisy gate or physical decoder performance were acquired.

## The strongest same-information ordinary route

The local candidate search is ordinary product-Pauli estimation followed
by symplectic synthesis. Huang--Kueng--Preskill's classical-shadow
construction [arXiv:2002.08953v2](https://arxiv.org/html/2002.08953v2),
Supplement Lemma3/EqS50, gives squared shadow norm3^w for a weight-w
Pauli. Global random local-Pauli measurements share copies across MANY
patches. Thus an equally informed ordinary receiver is allowed that
sharing; it is not charged n independent calibrations. Our one-patch
stratified3^w-setting execution is a simple deterministic local-tomography
implementation, not an advantage over optimized shadows or measurement
scheduling.

Leitch--Tirukkovalluri--Ouyang's product-measurement code learner
[arXiv:2609.04997v2](https://arxiv.org/html/2609.04997v2), SectionsII.3--4,
Theorems1/5/6, already estimates candidate low-weight stabilizer parities
and pays depolarizing readout visibility. Its source is stabilizer states
in a code; our source can have arbitrary nonstabilizer mixed junk. The
ordinary measurements themselves transfer directly: one need only learn
the2q Bell-labelled logical directions, rather than the whole junk or
full code. The final theorem does not test membership by a presumed
zero-versus-one expectation gap.

If all n inputs of the unknown Clifford were controllable, the ordinary
pure-Choi Clifford learner is stronger: Chang--Caro--Larocca--West
[arXiv:2609.10974v1](https://arxiv.org/html/2609.10974v1), Theorem1 and
Corollary1, give2n+ceil(log2(1/delta))+4 forward queries. That access is
not supplied by q logical inputs plus fixed opaque mixed junk. Conversely,
our patch and native-control promises are real extra structure and must
not be silently granted to an arbitrary hidden Clifford.

## What was already absorbed, and the generic-noise barrier

The first clean Bell-difference/annihilator proposal in
C_FIRST_MECHANISM.md is already supplied by the character-measurement
logic of the mixed/approximate StateHSP primary
[arXiv:2505.15770v3](https://arxiv.org/html/2505.15770v3), Theorem5,
Lemma4 and SectionII.4. The elementary union bound extends to the
four-copy mixed representation because the exact Bell graph has
expectation-one symmetries. Mere conjugation invariance of an arbitrary
mixed state is weaker and is expressly not enough in that source.
No clean Bell-learning invention is claimed here.

Tang--Steckmann's noise-robust stabilizer learner
[arXiv:2610.03307v2](https://arxiv.org/html/2610.03307v2), ProblemII.1,
TheoremsII.2--5 and Eq27, is a strong modern incumbent. It treats a pure
pre-noise state of bounded stabilizer nullity under specified Pauli or
global depolarizing noise, with polynomial/exponential regimes paid as
stated. Its quartic Bell-difference identity is imported ordinary
machinery. Arbitrary large mixed junk and coherent local calibration do
not inherit its useful low-nullity polynomial regime from its title.
We also do not infer that no other robust learner covers our restricted
operation: product tomography already does.

Root's separate `root_classical_decoder/NATIVE_NOISY_PARITY.md` derives
the full-source noisy-parity reduction for maximally mixed hidden junk
and a controlled-Z Clifford. That is a conditional algorithmic barrier
via quantum LPN, not a proven hardness result. The known-code,
single-noisy-random-codeword LSN problem is not substituted for it.
The local-patch restriction is a paid way around that source family,
not a solution of arbitrary noisy hidden-Clifford learning.

## Resources, survival and decision

At fixed patch width w and q, discovery/sample processing and the literal
Clifford compiler are finite and polynomial in n and precision parameters.
The exponential3^w/4^w acquisition/processing costs remain explicit.
Unknown arbitrary weight-w supports require the ordinary choose(n,w)
candidate search, although global shadows can still share samples; known
patches remove that combinatorial processing. Routing distant gates can
cost their distance. The compiler emits O(qW) gates with union width W,
which can be O(q^2 w), rather than automatically O(qw).

The computational instance stores a five-gate decoder and no quantum
program. It has zero late-payload source calls. Fresh sequential training
programs need only one(n+q)-qubit carrier at a time. The supplier must
still create/reset its full mixed junk and encoding on EACH call; its
actual preparation time and physical loss/readout costs are not known.
The exact rational backend exploited the producer's known model only to
generate/audit records; the receiver had no such model access.

Source errors may be local across128 outputs without a small global
diamond distance. PROOF Section6 pays local visibility and gives a
separate decoder-relevant all-input perturbation bound when actually
warranted. The executed all-input.1834 qualification uses neither a
hidden global-error promise nor that optional sharper transfer. Reuse
means the same fixed memoryless channel and stored circuit; unlimited
noise accumulation, drift and a noisy-memory threshold are not inferred.

Decision: this is a completed restricted acquisition-to-controller
operation, not merely a proposed generic source factory. The independent
architecture removes streamed coherent program storage for a meaningful
structured source class and handles actual source calibration through
fresh tests. Its strongest equally informed ordinary route supplies the
same core method. No sample/runtime advantage, new learning primitive,
world priority or hardware benefit is established. The next real gate
would be an acquired device's small useful logical-lightcone/frame plus
native detector/control error budget, or a different source intervention
that defeats the noisy-parity obstruction. Additional shots on this
same backend would not pay that gate.
