CERTIFIED FIRST-PASSAGE LAWS FROM COMPRESSED RELAXATION

Read RESEARCH_REPORT.txt for the complete contract, proof, finite algorithms,
explicit conservative polynomial bit bound, scientific deductions, and limits.

Main result: explicitly encoded finite open zero-field Ising chains with
rational finite-temperature bonds and positive rational site clocks admit a
deterministic polynomial-bit finite-pattern first-passage operation. It returns
CDF enclosures, relative mean enclosures, entrance probabilities, and optionally
a finite rational uniform enclosure of the entire CDF. The target set is an
explicit list. A complex-time Pfaffian kernel and a finite target renewal matrix
supply the operation without enumerating the full state space or simulating
the waiting time.

This is not a general nucleation solver, a measured kinetic model, a global
design algorithm, an exact symbolic distribution, or a resolution of QUBO.
Historical priority and civilisation-changing practical capability are not
claimed. All eight predecessor archives remain unchanged.

Files:
  RESEARCH_REPORT.txt            Complete proof and resource contract.
  chain_passage.py               Rational/dyadic reference construction.
  run_validation.py             Exact competing-target comparisons and rare test.
  validate_cdf.py                Coupled-chain CDF versus a killed-state comparator.
  RESULTS.json                  Compact executed results and scope labels.
  *_record.json                 Full rational enclosures and measured costs.
  SOURCE_SCOPE.json              Primary/Astra credits and access distinctions.
  PREDECESSORS.json              Preserved archive identities and open questions.
  WORKING_MATHEMATICS.txt         Superseded working notes and retained attempts.
  SHA256_MANIFEST.json           Integrity hashes of packet members.

Execution uses Python 3 and NumPy; the executed environment was Python 3.12.14
and NumPy 2.3.5. The predictor uses NumPy object arrays of Python integers;
floating-point linear algebra is not used for its certificates. No package
installation, new infrastructure, physical experiment or additional worker
was used. Timings are wall-clock measurements in this runtime, not a portable
performance guarantee or physical time calibration.

Commands, from this directory:
  python run_validation.py competing
  python run_validation.py rare
  python validate_cdf.py

Example:
  from fractions import Fraction as F
  from chain_passage import Chain, first_passage_mean, passage_cdf
  chain = Chain([F(1,3), F(4,5)], [1, F(2,3), F(7,5)])
  initial = (-1,1,-1)
  targets = [(1,1,1),(-1,-1,-1)]
  result = first_passage_mean(chain, initial, targets, F(1,256))

The reference implementation is deliberately conservative. Full CDF inversion
can be costly even for very small chains. The optional compile_cdf construction
calls that complete predictor repeatedly and charges every call. It is proved
and implemented; a nontrivial whole-time record was not executed in this run.

The rare n=16 example uses an alternating target with stationary probability
1/50,960,793,600,000. Its mean is enclosed around 3.0765e12 model time units
using only 16-by-16 exponentials with at most 145 fractional bits per entry.
Exact Pfaffians use larger integers, whose full sizes are counted in the proof.
See RESULTS.json
for the exact interval and actual computation cost. This numerical example
checks an implementation; the all-input theorem rests on the proof.
