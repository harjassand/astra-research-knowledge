# Candidate selection, checked literature, and remaining requirements

## Broad screens before the selected construction

The pass considered different foundational bottlenecks rather than starting with
one proof target:

1. **Discontinuous/singular execution.** Numerical perturbations can alter event
   existence or order; derivatives may not exist. The precise candidate became
   ordered-germ execution of a native hybrid program. This was the strongest
   concrete construction and was developed, implemented and tested in depth.
2. **Multi-edit counterfactual execution.** Reconvergent branches can duplicate
   or cancel the effect of the same edit. An exact idempotent intervention
   algebra was developed independently, then shown to be a basis change of an
   explicit table of worlds. No non-enumerative compression was established.
3. **Historical revision after nonlinear loss of information.** A sequence of
   affine maps with saturation admits constant-size composition; a balanced
   tree supports old edits without replay. This reduces to established
   composition aggregation and retroactive-data-structure techniques.
4. **Preserving all future questions while discarding the past.** If future
   queries include individual input bits, a universal lossless summary must
   retain those bits. Restricted query families lead to existing sufficient
   summaries or knowledge compilation. No new escape mechanism was obtained.
5. **Reverse computation through large simulations.** Recovering observables
   rather than the full trajectory can sometimes exploit a small invariant
   subspace, but that direction reproduces adjoints, model reduction, and
   sufficient-state compression. No independent mechanism worth further
   development was identified, and it was not promoted.

Screens 2–4, including exact formulas, native assumptions and prior-art checks,
are fully documented in `independent_ideation/research_screen.md`.

## Selected construction: what was already known

Primary sources were checked after the mechanism had been specified. The
following matches narrow the novelty claim; they do not assert that each source
contains our exact restricted source language or our exact test cases.

- **Edelsbrunner and Mücke, _Simulation of Simplicity_ (1990).** Symbolically
  perturbing degenerate inputs and making consistent comparisons without
  choosing an actual tiny floating perturbation is established. Our parameter
  follows a specified model perturbation rather than an arbitrary tie-breaking
  perturbation, but that difference alone is not a new computational primitive.
  Primary paper: https://arxiv.org/abs/math/9410209
  Publisher-paper copy: https://www.sandia.gov/files/samitch/unm_math_579/p66_edelsbrunner_simulation_of_simplicity.pdf

- **Benveniste, Bourke, Caillaud and Pouzet, _Non-Standard Semantics of Hybrid
  Systems Modelers_ (2012; manuscript 2011).** Infinitesimals, constructive
  execution semantics and cascaded zero-crossings have already been integrated
  for hybrid modelers. The paper's infinitesimal base clock differs from the
  present input-parameter germ. It still rules out a broad claim that putting
  infinitesimals into hybrid execution is itself new.
  Author manuscript: https://www.di.ens.fr/~pouzet/bib/jcsspaper.pdf
  DOI: https://doi.org/10.1016/j.jcss.2011.08.009

- **Council, Revzen and Burden, _Representing and computing the B-derivative of
  an EC^r vector field's PC^r flow_ (2021 preprint).** Event-selected flows can
  have factorially many derivative pieces, yet evaluation on a tangent vector
  has a polynomial-time/space algorithm. This prevents presenting efficient
  directional execution through simultaneous events as unoccupied territory.
  Their transversality/piecewise-differentiability setting is not a blanket
  solution for our square-root grazing or jump example; that gap also does not
  establish novelty of our construction.
  Primary paper: https://arxiv.org/abs/2102.10702

- **Poteaux and Weimann, _Computing Puiseux series: a fast divide and conquer
  algorithm_ (2021; preprint 2017).** Efficient extraction of singular algebraic
  series from native bivariate polynomials is an established algorithmic
  subject. Their stated bounds depend on polynomial degree and discriminant/
  resultant valuation. A small circuit with exponentially large expanded
  degree needs separate representation accounting; our sparse monomial class
  does that trivially and does not supersede their algorithm.
  Primary paper: https://arxiv.org/abs/1708.09067
  Publication: https://archive.numdam.org/articles/10.5802/ahl.97/

- **Allender, Bürgisser, Kjeldgaard-Pedersen and Miltersen, _On the Complexity
  of Numerical Analysis_ (2009).** Exact sign computation for succinct
  numerical expressions has nontrivial complexity. Its square-root-sum and
  PosSLP context is directly relevant to the native quadratic-event reduction
  in `GENERALITY_BARRIER.md`. That reduction is our elementary derivation; this
  citation supplies numerical-complexity background, not an event-simulation
  lower-bound theorem.
  Author manuscript: https://people.cs.rutgers.edu/~allender/papers/slp.pdf
  DOI: https://doi.org/10.1137/070697926

No broad literature-absence claim is made. The search did not prove that the
exact prototype has appeared verbatim. The burden was to establish a new
important capability, and the constructed evidence does not do so.

## Distinct alternatives and their exact missing capabilities

### A. Multi-edit reconvergent computation

**Native inputs:** original circuit of size s, baseline input, identified edits,
and a downward-closed admissible family F; for a budget k,
D=|F|=sum_{j<=k} binomial(m,j).

**Developed mechanism:** an algebra with e_A e_B=e_(A union B), zeroed when the
union is inadmissible. Evaluation in each admissible edited world is a ring
homomorphism. The subset-zeta matrix is invertible, so the algebra is isomorphic
to R^F. This yields correctness, but evaluation still costs O(sD) ring operations
in the world basis, plus rational bit costs. It has not compressed D independent
answers.

**Prior-art obstruction:** deductive fault simulation handles shared one-fault
propagation; variability-aware execution splits/merges configurations; change
calculi and provenance already express finite effects and causes. See the
independent report for exact primary links and scoped comparisons.

**Missing consequential capability:** exact multi-edit answers with cost
controlled by a provably smaller structural parameter than explicit world
count, while allowing genuine reconvergence and nonlinear interactions.

**Native acquisition requirements:** discover and verify the useful structure
from the original circuit; charge compilation, equality/branch tests and
numerical bit growth. A supplied decision diagram, free factorization,
precompiled separator structure, or compact expression awaiting exponential
queries does not meet this requirement.

**Current credibility:** important unsolved target, but this pass produced no
mechanism or theorem for the missing compression. It is not a ready next
candidate with demonstrated leverage.

### B. Retroactive scalar saturation

**Native inputs:** rational transitions f_i(x)=clip(a_i x+b_i,L_i,U_i), plus a
historical insertion, deletion or replacement.

**Developed mechanism:** composition remains a clipped affine function with
four rational parameters; a balanced composition tree gives O(log n) scalar
operation edits. Negative slopes reverse the appropriate interval endpoints.

**Prior-art obstruction:** closure under clamp composition, monoid aggregation,
max-plus recurrences and retroactive data structures already occupy the
essential mechanism. Exact rational sizes also grow and cannot be charged as
constant bits.

**Missing consequential capability:** analogous compact composition for native
interacting multidimensional saturations or state-dependent branching, where
the number of affine regions can grow rapidly.

**Native acquisition requirements:** prove a bounded representation closed
under the actual transitions, derive it from supplied dynamics rather than an
oracle, and include region discovery, coefficient growth and exact comparisons.

**Current credibility:** no such higher-dimensional closure was found. The
scalar construction is established technique and not a live foundational lead.

## Decision

Close all mechanisms from this pass as invention claims. Preserve their exact
positive statements, counterexamples to overclaiming, code and test evidence.
Do not count additional synthetic cases or a renamed interface as new evidence
of originality or consequential capability.
