# Acquisition, computation and unacquired costs

Actual primary inputs: public paper HTML/PDF bytes, saved under `sources/`; exact hashes are in the manifest. The first three endpoint downloads ran concurrently and took approximately 0.74 s, with individual durations/bytes in `sources/ACQUISITION.json`. Further primary PDFs/HTML and indexed primary passages were read; their total retrieval/model time was not separately instrumented. There were no random draws, experimental samples, cloud jobs or purchases.

Actual computation, from in-program timers:

* Full ell=3 complexes through n1336, exact chain/rank/face qualification and file writes: 0.54533 s. This initial run preceded the optional metadata-return wrapper added for the literal retractions; that wrapper does not alter the default complex construction.
* Both p/F/h local retractions and all-vector matrix identities on the already built replacements: 0.16831 s after imports.
* Single ell=5/t=2 interface control: 0.00445 s after imports.
* Earlier deterministic intrinsic-neighbourhood diagnostics and their receipts remain preserved. They are not premises of the theorem. They were small additional work, not a concealed physical sample acquisition or positivity oracle.

The prototype uses whole-space Python bitsets and some all-check-pair loops. Its worst-case storage and some operations are quadratic in the number of physical qubits; it is not an implemented compact linear-memory encoder. It does not store a quantum state vector. The all-level proof uses local cell pools of size polynomial in the **fixed** ell/degree constants, exact binary elimination within those pools, and sparse lifting. A locality-aware implementation can build the maps in O(n poly(A)) bit operations and O(n poly(A)) storage for fixed ell, but that asymptotic implementation is not benchmarked here. Producing a filling witness additionally pays the recursive projections, local corrections and output length; no global minimum-generator-count oracle is invoked.

Ordinary finite stabilizer elimination receives the same seed, matrices and word. It already gives finite membership and a witness with at most the rank many generators. No finite speed or memory advantage is claimed over it. Its generic bound grows with n, whereas the constructed recurrence pays the uniform check-soundness hypothesis for the existing stability theorem. The ordinary theory is therefore part of the result, not a weakened incumbent.

For ell=3, the conservative proof constants are A805, p21 and K at least 2*805*806. The physical existence application uses the source's fixed, much larger primary-qualified ell and embedding constants. The theorem consequently gives an implicit size-independent threshold, not a useful laboratory tolerance. Generating a practical 3D layout, multi-spin Hamiltonian, cold bath, coherent initial state, decoder/readout and experimentally warranted perturbation norm remains unpaid. The classical computation does not grant any of these interfaces.

The passive thermal lifetime is imported only for the **unperturbed** source model. There is no claimed full-cycle hardware performance, error-correction-energy saving, physical advantage over active QEC, or robust finite-temperature storage under a perturbed Davies generator.
