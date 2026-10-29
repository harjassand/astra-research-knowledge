# Strong prior, actual gain and retained costs

29 October 2026. This packet concerns conditional weak-product-clock Gibbs
preparation. It does not sample the full source-syndrome law. It preserves
the frozen zero-T/finite-T storage packages without promoting their unpaid
physical interfaces.

## 1. Strong ordinary constructions already available

The following primary papers were actually read at their governing scopes;
raw versioned HTML and extracted text are saved in sources/.

* [Ding--Li--Lin, 2404.05998v5](https://arxiv.org/html/2404.05998v5),
  Theorem10, Sections3.1--3.3 and Assumption13/Proposition15, already supply
  flexible exact KMS jumps, their tanh coherent correction, compact-frequency
  cutoffs, and efficient block encodings. Their notion of efficient means
  efficient simulation GIVEN a mixing time. It does not give this cold
  weak-product mixing theorem. Their exact complexity theorem imposes a
  particular separable Gevrey weighting assumption. Our band filter and its
  temperature dependence are therefore paid independently by finite derivative
  recurrences and a slower polynomial-precision circuit; no theorem is invoked
  after silently changing its constants or weighting function.
* [Smid--Meister--Berta--Bondesan, 2510.04954v2](https://arxiv.org/html/2510.04954v2),
  TheoremIII.3, LemmasIII.1--III.2 and AppendixA, already prove rapid mixing
  for weakly interacting qudits at any FIXED finite temperature. Their displayed
  generic mode coefficient has exp(2t DeltaE) and their perturbation constants
  depend on t. Those bounds do not qualify the coupled regime t=O(lambda^-8)
  as lambda decreases. Their oscillator/partial-CP proof is a controlling
  antecedent, not an absent ordinary method. We use explicit norm<=2 vacuum
  modes and prove the perturbation inequality directly. The new local smallness
  input is obtained by number dressing, a flat transition band, and TOTAL-N
  coherent cancellation, rather than generic KMS eigenbasis conditioning.
* [Zhan et al., 2503.15827v3](https://arxiv.org/html/2503.15827v3), SectionVI.2
  and discussion, prove rapid ground cooling of weakly interacting spin systems
  with negative-frequency filters. That is already a powerful ordinary option.
  It alone prepares neither the full finite-t state for unbounded n nor its
  positive-temperature excited density. The present exact KMS upward partner
  and coherent-correction estimate pay that missing step.
* [Abanin--De Roeck--Ho--Huveneers, 1509.05386v3](https://arxiv.org/html/1509.05386v3),
  Theorem3.1, is stronger than our finite-order integer-number normal form.
  It uses interaction norms, not a globally isolated spectral band. Only its
  elementary fixed-order homological mechanism is needed here, and the actual
  finite word/charge-projector compiler is described. We do not treat the
  prethermal change of representation as freely supplied data.

The finite circuit uses ordinary LCU and
[Low--Chuang Hamiltonian simulation by qubitization](https://quantum-journal.org/papers/q-2019-07-12-163/).
The reset-dilation implementation is elementary and intentionally slower than
the strongest simulation algorithms. A competitor given OUR normal-form,
filter and oscillator estimates can use the same or better ordinary circuits.
No circuit-level advantage over that equally informed competitor is claimed.

The low-temperature partition-function result of
[Helmuth--Mann, Quantum7:1155](https://doi.org/10.22331/q-2023-10-25-1155)
was identified through the primary reference list of
[2501.01412v2](https://arxiv.org/html/2501.01412v2). Its full proof has not
been imported here. In particular we do not infer that quantum state
preparation is absent or classically hard from a partition-function scope.
Broader priority and the strongest possible competing product-phase Gibbs
algorithm remain UNKNOWN. This is not a novelty clearance.

## 2. Precisely what the new composition changes

It supplies a finite quantum preparation operation for the FULL conditional
clock Gibbs state at fixed coupling/penalty independent of n, in a cold
polynomial window, from the native local term list and known signs. All
clock levels, exact upward heating and the full coherent correction remain.
The proof neither approximates the state by its global ground band nor
uses n exp(-t gap). At any fixed physical beta, sufficiently small FIXED
lambda makes the native t=beta/(4lambda^8) lie in the proved window.

This is different from choosing a penalty that increases with log(n/epsilon).
It also differs from computing scalar logZ, from a gapped path without mixing,
and from a supplied dressed Hamiltonian or initial overlap. The additional
lambda_cool gate is computable in the construction but UNEVALUATED. Thus
the literal previous lambda_T is NOT qualified. A new smaller fixed lambda
would have to satisfy the intersection of thermal and cooling gates; lambda_FF
is a further distinct gate if zero-T perturbation stability is also wanted.

This does NOT yet compose the whole physical Gibbs initialization: its
syndrome weights are proportional to the FULL clock trace Z_s, not just
exp(-t E_s). Root's separate full-thermal-weight construction owns that
marginal. Nor does the sampler prove native Davies/bath behavior, arbitrary
physical-error finite-T stability, or an efficient classical sampler.

## 3. What was and was not executed

Executed: compile_preparation.py computed exact integer flat-filter bounds
through order161, the order116 cold-window choice/margin3, the norm2 oscillator
threshold eta<=1/756 for L8, and the scalar finite error receiver. Its
COMPILER_RECEIPT.json records 0.039175957994302735 seconds after imports.
The common fourth-derivative envelope C_* has44bits; the highest recorded
filter majorant has2639bits. The exact summed displayed error upper bound
is193epsilon/1024. These computations are representation/resource arithmetic;
they are NOT many-body dynamics or quantum-state preparation.

Not executed: the native order116 SW coefficient catalogue, a numerical
lambda_cool qualification, quantum gates, any trajectory, source-syndrome
sampling, or physical clock preparation. No new Hamiltonian fixture, code
level, parameter grid, paid compute or physical experiment was acquired.

Full formal resources are retained in IMPLEMENTATION.md: connected coefficient
words through fixed order p; optional local matrices L^(q p), or the charged
operator-word alternative; native Hamiltonian simulation; scalar coefficient
quadrature; explicit O(K) table-state preparation without QRAM; jump/reset and
coherent circuit simulation; all per-query finite precisions; inverse dressing;
and the original finite-depth physical prefix gauge. There is no partition-
function, energy-level resolution, successful-postselection or initial-overlap
oracle hidden in that contract.

The polynomial temperature dependence is not cheap. The conservative receiver
has time-grid length O(t^36) before additional polynomial coefficient/circuit
costs, and t for the earlier tiny clock parameters is enormous. We assert no
useful numerical/hardware budget or practical advantage. The present result is
a general fixed-coupling initialization theorem with paid algorithmic primitives,
not a presently executed memory device. Filter and local-compiler constants
can be improved without changing this boundary, but no such optimization is
needed for the current theorem.

Public-source retrieval and analytical reasoning were not individually timed;
imports and JSON output are excluded from the reported scalar function time.
No end-to-end measured speedup is reported.
