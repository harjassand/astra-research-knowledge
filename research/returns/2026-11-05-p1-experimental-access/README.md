# P1 — a physical access theorem for quantum experiments

Start with the **[complete proof report](package/Astra_P1_Quantum_Experimental_Access.pdf)** and its **[LaTeX source](package/Astra_P1_Quantum_Experimental_Access.tex)**. The supplied [independent constructive audit](package/proof_audit.txt) supports the main proof under the corrected conditions it records. It resolves full-retained-instrument covariance and classical-feedback subtleties; its acceptance does not imply historical priority, a working device or practical advantage.

## Main result and its scope

An initially unencoded n-qubit source experiences actual independent inaccessible Markov Z dephasing from time zero. Every retained output, classical record and controller is included in the access contract. Paid Hamiltonian terms act noncommutatively on at most k source sites and have a **summed term-norm budget** per site; a total commutator bound alone is insufficient. Downstream memory, computation, feedback and collective decoding may be arbitrary.

For Omega < 2 lambda, the report proves a time-uniform contraction bound on transverse sectors. The clean scaling statements use Omega <= lambda. Consequences include exponential copy requirements for fixed-k global coherence and worst-case constant-gap purity testing, with superpolynomial cost for k=o(n) in the stated regime. Explicit finite-slew local meters acquire fixed-weight properties with polynomial work. An actual native extensive interaction can access the selected global coherence with polynomial copies; that interaction is supplied as a different source resource, not compiled for free from local hardware or claimed as a universal polynomial purity estimator.

Omega=2 lambda is a boundary of this proof, not an established physical transition. The all-fixed-strength-ratio question remains open. These are theoretical access results, not a zero-capacity theorem, a strict hard-bandwidth device or an experimental demonstration.

## Exact supplied files

| Item | Read it |
|---|---|
| Main proof | [PDF](package/Astra_P1_Quantum_Experimental_Access.pdf), [LaTeX](package/Astra_P1_Quantum_Experimental_Access.tex) |
| Completed internal proof audit and resolved boundaries | [proof_audit.txt](package/proof_audit.txt) |
| Recorded finite-model checks | [verification_results.json](package/verification_results.json), [source figure](package/access_scaling.png) |
| Verification program, not executed during publication | [verify_access.py](package/verify_access.py) |
| Producer reproduction instructions and environment | [README](package/README.txt), [versions](package/environment_versions.txt) |
| Compact handoff and governing source links | [continuation_handoff.txt](package/continuation_handoff.txt) |
| Exact original archive | [Astra_P1_Quantum_Experimental_Access_Package.zip](original/Astra_P1_Quantum_Experimental_Access_Package.zip) |
| Visible answer and issued prompt | [Complete capture](P1_QUANTUM_EXPERIMENTAL_ACCESS_20261105_RETURN.txt) |
| Transport provenance and hashes | [SOURCES.json](SOURCES.json), [supplied SHA256SUMS](package/SHA256SUMS.txt) |

The numerical files report 24 triangular-meter cases and 60 finite source-receiver evolutions, with 16 scalar optima also recorded. They are floating-point falsification checks, not interval certificates or exhaustive tests. No scientific program, LaTeX build, reproof or novelty audit ran during this publication.

## Separate companion constructions

- [Causal reset/export decoder](package/causal_reset_decoder.txt): a structured discrete-circuit receiver with coherently accessible calibrated pure environment records. Its access differs from the main theorem's hidden-noise model; the generic continuous entangling-Hamiltonian extension is not supplied.
- [Expander rigidity and mixed-output memory](package/expander_mixed_bath_companion.txt): an independent construction using explicit expander assumptions and paid preparation/measurement resources. Constant sample count does not mean constant total physical cost. Its time-programmed collision source is not silently promoted to a stationary thermal Lindblad model.

The original ZIP and all 12 members are byte-exact. The public visible-answer wrapper changes only its local ZIP download locator; the exact private wrapper and both hashes are recorded. Its scientific text and rendered ending are unchanged. The separately linked PDF was not downloaded; the PDF above came from the supplied ZIP. Older unrelated source-transfer holds remain.

This package is directly available on GitHub. The generated retrieval index has not been rebuilt for this source publication. [Browse other supplied returns](../README.md).
