ASTRA — ACQUIRING REUSABLE SPECTRAL COMPUTATION AND ITS TRACE WEIGHTS
Research completed 31 October 2026

START HERE

The scientific target is a learner that acquires reusable numerical operations
for later, previously unspecified computations. This package develops a concrete
construction for large Hermitian matrix-vector oracles whose generated algebra
is small. Its proposed addition is a uniform trace acquisition theorem combining
learned noncommuting structure, exact multiplicity recovery by saturation, and
concentration of the unresolved central weights.

Read algebra_compiler/MAIN_PROOF.txt for the full ordinary construction and proof.
Read RESULTS.txt for executed checks, numerical evidence, and preserved failures.
Read SOURCES.txt for current Astra governing-source locators and primary research.

The claim is scoped. The algebraic compression machinery is established, and a
strong retaining conventional algebra learner can implement the construction.
Historical novelty of the combined theorem, a practical speed advantage, and
robust acquisition from approximate or noisy sources remain unestablished.
No civilisation-changing discovery or general theory of intelligence is claimed.

MAIN PROVED CONTRACT

For fixed Hermitian sources generating A = direct_sum_alpha M_ralpha(C) tensor
I_malpha, let d=sum r_alpha^2 and b be the number of simple components. With q
complex Gaussian probes, exact joint cyclic closure has dimension

  R = sum_alpha r_alpha min(m_alpha, q r_alpha) <= min(N, q d).

It takes exactly kR source matvec calls in the specified implementation. The
learner receives no useful block coordinates or multiplicities. It reconstructs
the centre from the acquired matrices and obtains a faithful representation.
The retained trace functional satisfies

  Pr[there exists X in A, X>=0, with
       |estimated_trace(X)-Tr(X)| > epsilon Tr(X)]
       <= 2b exp(-epsilon^2 q^2/4).

Thus q=ceil(2 sqrt(log(2b/delta))/epsilon) suffices. The event covers unlimited
adaptive future expressions within the fixed algebra. Their arithmetic, inverse
conditioning, expression size and requested outputs remain paid. The real
Gaussian convention in the numerical experiment uses denominator8, not4.

After acquisition, optional regular-representation recompression reduces the
retained matrix dimension to D=min(R,d). A future length-L expression then costs
O(L D^3) arithmetic in the stated conservative dense model. Its construction,
positive metric and trace functional are charged; this uses established regular
representation machinery. An exact nonorthonormal-coordinate check is included.

Small-multiplicity components become exact; each remaining component has enough
Gaussian energy coordinates for the q^2 concentration exponent. A retained joint
confidence set incorporates the known ambient dimension and permits signed trace
intervals without a new query failure budget.

The exact-root Gaussian model is distinguished from a finite-bit corollary for
exact rational sources and bounded integer probes. Floating-point closure is
not certified by small numerical residuals.

CONTENTS

algebra_compiler/
  MAIN_PROOF.txt                  Main synthesis, proofs, costs and limitations.
  cumulative_exact.py            Exact rational cumulative relation acquisition.
  cumulative_exact_results.json  Its full event record and separated source costs.
  check_regular_trace.py          Exact regular recompression and trace transfer.
  regular_trace_results.json      Eight coordinates reduced to five; trace10/3.

planning_agent/
  check_cyclic_exact.py           Fraction-arithmetic acquisition/intertwining.
  check_centre_exact.py           Exact learned centre and dimension inference.
  *_results.json                 Recorded outputs.
  *_AUDIT.md, *_REVIEW.md         Complementary mathematical reviews.
  final_review.md                Final fixes incorporated and scoped acceptance.
  COMMON_STATIONARY_PLANNING_OBSTRUCTION.md
  check_planning_obstruction.py   Four-state exact open-loop planning obstruction.

composition_agent/
  cyclic_algebra.py               Numerical joint closure implementation.
  hybrid_trace_four_blocks.py     Main nontrivial four-component experiment.
  hybrid_trace_four_blocks_results.json
  closure_comparison.json         Preserved numerical closure failure and repair.
  experiment_note.md              Interpretation and all principal qualifications.
  hybrid_trace_demo.py            Preliminary three-component experiment retained.
  hybrid_trace_results.json       Its known-dimension correction is documented.
  theorem_note.md, hybrid_trace_theorem.md  Intermediate constructive notes.

prize_agent/
  saturation_trace_theorem.md     Independent proof and comparator analysis.
  check_trace_theorem.py          Independent complex numerical checks.
  trace_confidence.py             Reusable numerical confidence-set module.
  check_trace_confidence.py       LP comparisons, intervals and adaptive queries.
  *_checks.json                  Saved check outputs.
  algebraic_geometry_notes.md     Other investigated openings and failure modes.

source_context/
  N1515_STABLE_CALCULUS_PROOF.txt  Retrieved Astra governing source.
  N1521_QUADRATIC_TASK_PROOF.txt   Retrieved Astra governing source.

REPRODUCING THE CHECKS

Run from the extracted package root. This environment used Python3.12.14,
NumPy2.3.5 and SciPy1.17.0. Fraction arithmetic uses the Python standard library;
some scripts import NumPy for numerical spectrum displays. No SymPy is required.

  python3 planning_agent/check_cyclic_exact.py
  python3 planning_agent/check_centre_exact.py
  python3 planning_agent/check_planning_obstruction.py
  python3 algebra_compiler/cumulative_exact.py
  python3 algebra_compiler/check_regular_trace.py
  python3 prize_agent/check_trace_theorem.py
  python3 prize_agent/check_trace_confidence.py

The main numerical experiment has fixed target/probe seeds and saves all120 runs:

  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 composition_agent/hybrid_trace_four_blocks.py

Rerunning scripts can overwrite their corresponding result JSON files. The
supplied result files preserve the executed run. Timings are environment-specific;
they are not an end-to-end comparison with optimized conventional methods.

The main proof is authoritative where intermediate notes describe an earlier
version. The concrete corrections and useful failures are retained in RESULTS.txt.
