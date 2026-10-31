# Acquired entropic conductance — scoped mathematical capability

## Useful result first

A raw-coefficient compiler acquires a special Gaussian-fiber structure and
certifies the full finite-rate diffusion conductance through an exponentially
rare **entropic** bottleneck. At beta=1 the exact full conductance is between
`9/17` and `1` times a scalar free-energy conductance. This factor does not
grow with dimension or barrier height and does not assume instantaneous
fiber equilibration. The actual coordinate process is not Markov.

The executed 129-dimensional input produces the rationally certified interval

    2.2772959737e-18 <= cap_mu(A,B)/mu(A) <= 4.3298080117e-18.

It used 8,193 exact arithmetic points and about 3.2--3.5 seconds of integration
on this machine, with <1% extra numerical width. A fully expanded rotated
five-dimensional input separately tests basis acquisition from 295 raw
monomials via the exact quadratic-Hessian nullspace. An additional fixture
has an irrational unit direction and irrational conditional eigenvalues.
The 3,556 author assertions, including receiving replays and independent-
review regression repairs, pass.

The method chooses the two full-fiber basins implied by its acquired input
grammar. It is NOT a solver for arbitrary basin shapes, pointwise mean
first-passage times, fixed-deadline hitting probabilities, noisy physical
models, or arbitrary nonlinear fibers. The large scaling examples are
coordinate-aligned sparse inputs; dense rotated acquisition is tested only
at small dimension. Conditional Gaussian elimination and classical
Dirichlet/Thomson methods get equal access and, augmented with the newly
constructed current/estimate, can reproduce the result. A prior source
giving this exact dimension-free lower certificate has not been located.
**No superiority over those strongest retaining alternatives, historical
novelty, physical realization, or civilisation-scale significance is claimed.**

## Read and replay

* `PROOF.md`: actual task, transport capacity sandwich, dimension-free
  resistance estimate, all-state normalization/nonexplosion, acquisition.
* `COSTS_AND_COMPARISONS.md`: complete acquisition/numerical/bit ledger,
  strongest alternatives and geometry failures.
* `SOURCES_AND_SCOPE.md`: pinned task-first Astra intake and primary sources.
* `capacity.py`: strict raw coefficient reader, symbolic acquisition and
  exact integer/outward-rational integral backend.
* `verify.py`: separate receiving entry point binding the raw input and
  external task to every accepted interval.
* `check.py`: exact symbolic/rounding/mutation tests and all saved replays.
* `capacity_results.json`, `dense_raw_input.json`, `dense_acquisition.json`,
  `check_results.json`, `irrational_geometry_fixture.json`: executed evidence.

In this directory, with already installed Python 3 and SymPy 1.14:

    python -B capacity.py
    python -B check.py

The first command regenerates reports including nondeterministic timing
fields. For independent review, copy the frozen directory to a temporary
working directory before running, or keep evidence outputs outside the
frozen source folder. No installation or network is required for replay.

Status at freeze: author proof and executed author tests; independent whole
review requested separately. Later review must state its exact file hashes.

The retained `*_gcd_v0.*` files are abandoned acquisition history, not
dependencies of the accepted candidate. The current nullspace/projector
route was identified by the root reviewer and is strictly simpler.
