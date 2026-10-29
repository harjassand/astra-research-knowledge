# Prior, full cost, and disposition

The construction is positive at its admitted nonlinear impurity-response
scope. Its foundational novelty and broad predictive advantage are
NOT_ESTABLISHED. It should not be promoted as the missing general
finite-width-resonance operation.

## Controlling primary antecedents

1. **Yang eta symmetry / coherent eta states.**
   [Solomon and Penson, cond-mat/9712228](https://arxiv.org/abs/cond-mat/9712228),
   published J. Phys. A 31 (1998), explicitly constructs coherent eta
   pairing states and their dynamical-group description. The complete
   five-page primary was read; equations (7), (16), (17), (27) are the
   controlling algebra/coherent-state/evolution precedents. Our centered
   Hc has the uniform pair-rotation frequency removed. Neither the
   coherent state nor its symmetry rotation is a new representation.

2. **Exact eta-state linear response already becomes few-particle
   dynamics.** [Tsuji, Nakagawa and Ueda, arXiv:2103.01547](https://arxiv.org/abs/2103.01547).
   Read main page 2, supplementary two-particle reduction/evaluation,
   and charge response equations (S64)--(S72). Their charge/current
   linear-response correlator is exactly reduced to two-particle
   propagation at strong U. They use fixed-number eta states, while our
   main input is eta coherent (or its phase average). We therefore
   implemented the SAME-source two-particle first-order response as the
   baseline, instead of comparing against free dynamics or mean field.
   It is genuinely separated from the acquired nonlinear answer.

3. **Quantum-number Hamiltonian truncation is established.**
   [Tong, Albert, McClean, Preskill and Su, arXiv:2110.06942v2](https://arxiv.org/abs/2110.06942),
   Quantum 6, 816 (2022). Read common-structure equations (23)--(24),
   leakage and Hamiltonian-truncation sections, in particular Theorem 6.
   Their abstract graded framework includes bounded grade-changing
   source terms (r=0), not just boson square-root growth. Our elementary
   norm-one Dyson/boundary proof is a specialization. The return-path
   observable bound is a useful explicitly executed selection rule;
   priority of that generic refinement is not cleared and no new
   truncation principle is claimed.

4. **Rigorous weak-fermion algorithms are stronger on their admitted
   generic weak-interaction inputs.**
   [Zhao, Marvian and Tong, arXiv:2608.19448](https://arxiv.org/html/2608.19448),
   actual paper and theorem boundary were read in the preceding frozen
   sol23 wave, with the current primary opened again. They give local
   observable algorithms in the geometric weak-interaction regime and
   longer Frobenius-norm control. Here the quartic interaction is U=8,
   rather than a weak perturbation of quadratic hopping. Our algorithm
   works only because its special initial state admits an exact
   low-defect frame. The methods address different admitted input
   classes; this is not a measured speed comparison or a contradiction.

5. **Kinetic/pre-relaxation/normal-form methods.** The earlier read
   Bertini--Fagotti primary, arXiv:1501.07260, and the controlled
   kinetic limits cited by the Zhao--Marvian--Tong primary do not make
   a free collision closure available for arbitrary finite U=8,
   finite-time 2D impurity dynamics. Conversely, none of their weak
   homogeneous thermodynamic claims is supplied by our special-state
   calculation. The new construction avoids resonance resolution
   altogether, rather than improving a Boltzmann closure. The exact
   comparison is to symmetry-aware particle sectors, not to an
   under-informed kinetic approximation.

6. **Nonequilibrium DMFT is an established strong-interaction
   alternative.** [Aoki et al., arXiv:1310.5329v2 / RMP 86, 779](https://arxiv.org/abs/1310.5329).
   Its primary abstract/formal scope was checked, not its entire
   numerical implementation. The self-consistent impurity mapping
   supplies thermodynamic-limit strong-correlation predictions and is
   exact in its infinite-dimensional setting. No controlled finite-2D
   error for this eta-coherent local quench was acquired from it here.
   That fact does not establish superiority of our method over DMFT
   as a practical approximation. No DMFT run was performed.

The first three priors are saved as exact PDF bytes with acquisition
URLs, SHA256, timings and extracted text in `sources/`. Controlling
response/truncation pages were rendered and visually checked. Search
misses do not support a novelty claim. The task-first Astra entry and
bounded live search were acquired at revision
d6672151ce8e86d4af3e74b3b880abcdc82ae304, input version
9301bf5171d4110151e38e5ddebeb1212f593a1c14f7751e019e9a8264a3b8ef.
No returned unrelated packet was used as a theorem, and no corpus
completeness/absence claim is made.

## Equally informed strongest ordinary comparator

Give an ordinary solver precisely the same bipartite Hubbard model,
eta-coherent input, local density quench, and observable. Yang's eta
rotation followed by bounded-source Dyson/Fock truncation is available
to it. That ordinary solver produces the SAME finite-dimensional
problem and the SAME numerical answer. Our reduction versus
601080390 full balanced amplitudes is therefore NOT a new advantage
against this strongest comparator. The return-path tail improves a
naive state-error qualifier here; it does not create an exclusive
predictive operation.

For a more limited comparison, exact two-particle linear response costs
257 amplitudes and about .0105s. The nonlinear retained problem costs
328257 amplitudes and 10.7655s of propagation, about three orders of
magnitude more. It buys an actual density shift of .00888 relative to
linear response, well above the qualified .000453 error. This is the
paid nonlinear information gain, not free predictive speed.

TEBD/TDVP and other tensor-network solvers get the same simple physical
on-site product input. A 4x4 instance alone does not show they fail or
that our method wins. No matched tensor-network benchmark is acquired,
and none is needed to reject a general novelty/advantage promotion.

## Costs and acquired inputs

* Exact supplied input is a finite bipartite graph, U,J, a known eta
  coherent ray or phase-averaged eta ensemble, local source, and output.
  The finite description is O(L+|E|); this does not pay laboratory
  preparation or calibration. There is no physical record silently
  treated as the actual Hubbard device.
* Main sparse matrix: 328257 complex amplitudes, 5405735 entries,
  about 655 MB peak host RSS. Compile .1471s; 2160 sparse matvecs,
  propagation 10.7655s. Timings exclude imports, final serialization
  and prior/source reading. Receipts retain those distinctions.
* The small native exact-algebra check and 4x2 cost preview are both
  preserved; their outputs are not additional physical samples.
  The primary PDFs took the individually recorded acquisition times;
  task-first retrieval and proof effort are not included in a
  runtime-speed claim.
* Numerical qualification is a standard forward-error contract for
  binary64 sparse arithmetic plus exact scalar rational bounds. It is
  not a formal verification of SciPy or the CPU. Source/hardware-model
  errors are not folded into the mathematical error for free. An extra
  Hamiltonian error of global norm dH can cost 2t*dH in a norm-one
  expectation by Duhamel.

## Decisive failure and surviving improved question

The original generic finite-width cancellation problem is NOT_SOLVED.
The new frame replaces it only for a special symmetry-protected
background and a sparse symmetry-breaking source. An extensive
source makes the exact defect number binomial with mean proportional
to L; a fixed cutoff then fails. Same-sublattice hopping or generic
bulk eta-symmetry-breaking terms cannot be silently retained in Hc:
after rotation they are generally extensive pair sources. A generic
finite-density state does not supply the low-grade seed either.

The surviving useful target is **nonlinear impurity dynamics above
qualified symmetry-related backgrounds**, with exact interacting
few-defect dynamics and an output-sensitive cutoff. This wave actually
constructs and evaluates one such fixed-U, fixed-density interface.
It should be retained as an honest restricted benchmark/derivation and
DEPRIORITIZED as a new foundational capability: known symmetry plus
ordinary Dyson/Fock machinery already supplies its strongest operation.
No further huge-volume fixture, cutoff refinement or prefactor tuning
is warranted by the present result.
