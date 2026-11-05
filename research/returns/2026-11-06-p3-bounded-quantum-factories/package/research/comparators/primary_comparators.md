# Primary comparators for bounded noisy Gibbs factories

Research note, 5 November 2026. This is a comparator and scope note, not a new
claim of priority for convex programming, noisy probabilistic synthesis,
thermal graph states, or Pauli convolution. Parent construction notes contain
the actual new operation.

## 1. The strongest directly overlapping framework

Tian-Ren Jin, Yu-Ran Zhang, Kai Xu, Heng Fan, **Noisy Probabilistic Error
Cancellation and Generalized Physical Implementability**, arXiv:2409.01000v2,
16 July 2025; Communications Physics 2025.

- Primary full text: <https://arxiv.org/html/2409.01000v2>.
- Journal: <https://doi.org/10.1038/s42005-025-02217-8>.
- Their framework allows an arbitrary convex set of experimentally accessible
  noisy states and operations. Eq. (1)-(2) explicitly distinguishes nonnegative
  coefficients, which implement an actual probabilistic channel mixture, from
  negative coefficients, which require signed observable estimation.
- Their noisy Pauli basis has an acquired linear noise map `Theta`. Eqs.
  (7)-(13) invert that map and optimize decompositions over actual noisy
  operations, rather than ideal correction gates.
- Thus it would be wrong to advertise “use a convex combination of actual noisy
  channels” or “include selector noise in the channel menu” as a new quantum
  idea by itself. The natural mathematical optimization already exists.
- Their general inverse-error operation is usually non-CP; its signed
  implementation does not deliver the target quantum state. That is a real
  distinction, but the framework also explicitly includes the positive case.
- The new uniform consequence must therefore come from proving that *all local
  channels needed by the many-body preparation have positive decompositions*,
  using a menu of fixed quantum size/lifetime, and then earning noisy classical
  programming, acquisition, record handling, and global composition. Those
  are not implied by merely writing the convex program.

Related primary framework: Leonardo Banchi, Jason Pereira, Seth Lloyd, Stefano Pirandola,
**Convex optimization of programmable quantum computers**, npj Quantum
Information 6, 42 (2020),
<https://www.nature.com/articles/s41534-020-0268-2>.
It makes optimal program-state selection a convex/semidefinite problem for a
given physical processor and compares teleportation-based and circuit-based
processors. A processor and programmable input states are supplied in that
formulation; it does not by itself earn a noisy classical menu interface or an
all-chain-length Gibbs preparation theorem.

Related primary framework: **Sparse Probabilistic Synthesis of Quantum
Operations**, PRX Quantum 5, 040352 (2024),
<https://journals.aps.org/prxquantum/abstract/10.1103/PRXQuantum.5.040352>.
It constructs an approximation library and optimizes sparse quasi-probability
decompositions, including exact average simulation at a measurement overhead.
Negative coefficients and measurement reweighting must not be confused with
physical raw-state delivery.

## 2. State precompensation was already established

Chengjie Zhang, Liangsheng Li, Guodong Lu, Haidong Yuan, Runyao Duan,
**Quantum error pre-compensation for quantum noisy channels**,
Phys. Rev. A 106, 042440 (2022), arXiv:2309.01434,
<https://arxiv.org/abs/2309.01434>.
The authors solve for a state input producing a given desired output through a
known channel, analytically when possible and otherwise via SDP fidelity
optimization. A new theorem must add its many-body uniform positive radius,
efficient source/finite-bit construction, and the actual noisy apparatus route;
the formal inverse equation is not new capability.

## 3. A graph-state source particularly close to the alternate fabric

Guedong Park, Jinzhao Sun, Hyunseok Jeong, **Low-overhead tailoring and learning
of noise in graph states**, arXiv:2503.12870v3, 15 October 2026,
<https://arxiv.org/html/2503.12870v3>.

This paper must be compared if using thermal graph states or Clifford fabrics:

- It explicitly obtains graph-basis diagonal noise by Pauli tailoring, derives
  a convolution equation, and learns it using Bell-type measurements and
  classical processing. Neither graph-basis Pauli convolution nor state
  twirling is a new mechanism.
- The main algorithm expressly assumes noiseless tailoring operations (main
  text around lines 53 and 100 of the arXiv HTML). Appendix G treats noisy
  detection through probabilistic error cancellation, assuming free `X`
  operations and known/twirled gate noise. That gives estimators, not a
  delivered noiseless quantum state.
- The approximation method is efficient for small *total state infidelity*;
  efficient `l1` learning additionally requires polynomial support of the
  global graph-basis noise law. A fixed positive independent error probability
  on growing chains generally gives exponentially many supported syndromes
  and total infidelity tending to one. Local noise-factor structure is not
  literally the same premise as sparse global support.
- A fixed-template local calibration route followed by exact finite-width
  classical inverse sampling can avoid those global-learning premises. It
  must still pay for actual noisy local calibration and cannot inherit a
  noiseless measurement or Pauli selector from this paper.

Earlier thermal graph preparation/characterization sources:

- Akimoto, Tsuchiya, Yoshii, Takeuchi, **Passive verification protocol for
  thermal graph states**, PRA 106, 012405 (2022),
  <https://arxiv.org/abs/2202.10624>.
- Kay, Pachos, Duer, Briegel, **Optimal purification of thermal graph states**,
  NJP 8, 147 (2006), <https://arxiv.org/abs/quant-ph/0606177>.
- Cavalcanti et al., **Macroscopic bound entanglement in thermal graph states**,
  NJP 12, 025011 (2010), <https://arxiv.org/abs/0909.5609>.

These prevent an overstatement that connected entangled thermal graph states,
constant-depth ideal graph preparation, or their noisy phase representation
are themselves newly discovered.

## 4. Ideal all-temperature preparation incumbents

<https://arxiv.org/abs/2609.35973> gives an exact mixture of bounded contiguous
pure blocks at fixed temperature/range, constant ideal preparation depth, and
efficient classical preprocessing. The accepted uniformly mixed-block
extension is the stronger starting input here. The missing physical operation
is implementing the sampled ensemble under actual noisy programming and
cross-boundary joining errors, not proving bounded ideal blocks again.

Rouze and Stilck Franca, <https://arxiv.org/abs/2610.03578>, give logarithmic
mixing for finite-temperature one-dimensional systems and near-linear
`N polylog(N/epsilon)` ideal implementation under their bounded local-term
contract. Their Gibbs resets, quantum belief propagation, and KMS completion
are ideal/local primitive operations. A global noisy-delivery theorem requires
an actual implementation bridge. On the other hand, a new architecture cannot
claim an ideal-depth or ideal-sampling advantage over these incumbents.

## 5. Quantum fault tolerance and interfaces

Christandl, Fawzi, Goswami, <https://arxiv.org/abs/2602.16948> (v2, 29 September
2026), gives qLDPC state preparation with constant space overhead and gradual
decoding interfaces. Its residual physical output noise is local stochastic;
it is not automatically a known independent product channel admitting the
positive deconvolution used here. Conversely, it supplies a strong ordinary
fault-tolerant preparation comparator with actual input/output work counted.

Fault-tolerant quantum input/output, <https://arxiv.org/abs/2408.05260>, already
addresses the physical interface and unavoidable floors for raw unknown
quantum information. A known full-rank mixed target is a different task: its
intended mixedness can absorb a positive apparatus preimage. No assertion
about arbitrarily accurate arbitrary unknown pure-state delivery follows.

The matched comparison must grant ordinary methods the same cold resets,
couplers, noisy classical computation, fabrication precision, routing,
calibration, switching, target description and raw output access. In
particular, an equally informed fault-tolerant preparer is free to adopt the
same positive state-specific precompensation and thereby omit unnecessary
quantum encoding. There is no separation from that strongest method merely
because the new protocol is described without quantum codes.

## 6. Honest consequence statement

An all-chain-length theorem showing that growing *quantum* coherent modules
are unnecessary for known interacting thermal-state delivery is a substantive
resource-structure deduction. It can be scientifically useful even when
generic block constants and classical/calibration costs are prohibitive. It
does not establish a total-resource advantage, an arbitrary-noise threshold,
or an engineering design at currently useful rates. The actual positive
decomposition, full selector channel, finite-bit implementation, and the
complete execution ledger are the content that must distinguish it from the
already established convex programming machinery.
