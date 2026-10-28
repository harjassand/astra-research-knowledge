# Primary research and ordinary baseline notes

Research date: 2026-10-28. These notes belong to the authorized P3 continuation.
Recovered proofs and code were read but not modified. A source reporting a
theorem is distinguished below from the explicit evaluator reconstructed here.

## 1. The proposed E6 representation is established mathematics

Peter Magyar, Jerzy Weyman and Andrei Zelevinsky, *Multiple Flag Varieties of
Finite Type*, Advances in Mathematics 141 (1999), 97–118:

- Paper: https://arxiv.org/pdf/math/9805067
- Published DOI: https://doi.org/10.1006/aima.1998.1776

Theorem 2.2 explicitly lists the composition-length triple (2,3,3) as E6.
Thus one subspace J and two two-step flags F1 ⊆ E1, F2 ⊆ E2 in an ambient
space are precisely a classical finite-type multiple-flag problem. Theorem 2.3
classifies orbits by indecomposable multiplicities. Theorems 2.4 and 2.9 classify
the indecomposables and give explicit representatives; zero composition parts
allow repeated subspaces. The paper states an algebraically closed base field
in Section 2.1. It alone does not justify finite-field orbit counts.

Andrew Hubery, *Hall polynomials for affine quivers*:

- https://arxiv.org/pdf/math/0703178

Section 3, especially Lemma 3 (paper page 7), explicitly states the Dynkin
classification by positive-root multiplicities over **any field**. Its proof
uses exceptional indecomposables and field-independent Hom dimensions, and
establishes polynomial automorphism orders over finite fields. Theorem 4 proves
existence of Hall polynomials by reductions using Green's formula. The existence
theorem must not be substituted for an implemented evaluator or treated as a
unit-cost counting oracle.

Original reflection-functor source:

- Bernstein, Gel'fand and Ponomarev, *Coxeter functors and Gabriel's theorem*,
  Russian Mathematical Surveys 28:2 (1973), 17–32.
- https://doi.org/10.1070/RM1973v028n02ABEH001526
- Author PDF: https://www.math.tau.ac.il/~bernstei/Publication_list/publication_texts/BGG-CoxeterF-Usp.pdf
- Journal record: https://www.mathnet.ru/php/archive.phtml?jrnid=rm&option_lang=eng&paperid=4860&wshow=paper

The author PDF and journal page failed to retrieve in this session (timeouts,
then HTTP 503). Subsequently the original article's OCR text was found at
https://studyres.com/doc/18821376/coxeter-functors-and-gabriel-s-theorem .
Definitions 1.1, Theorem 1.1 and its proof, Lemma 2.3, and Theorem 3.1 and its
proof were read there. This is an unofficial transcription with damaged
mathematical symbols, so cite the primary article and retain Hubery's explicit
any-field statement. The original PDF itself was not retrieved. The MWZ and
Hubery full PDFs were retrieved and the governing sections above read.

The constructive mechanism in BGP uses kernels at sinks and cokernels at
sources. Except at the simple object annihilated by a reflection, these
operations preserve indecomposability and invert each other. For a Dynkin
graph, repeated admissible reflections must turn a positive dimension vector
nonpositive: otherwise summing a finite Coxeter orbit would give a nonzero
invariant vector, contrary to positivity of the associated form. Immediately
before annihilation the object is simple. Reversing the kernel/cokernel
operations both constructs and determines the original indecomposable.
These operations are linear algebra over the given field.

### Explicit specialization, reconstructed rather than a new oracle

Specializing the displayed standard forms gives 29 injective-flag
indecomposables. This is an independently checkable finite catalogue:

1. Eighteen ambient-dimension-one types. J is zero or the whole line. Each
   two-step flag enters that line at one of its three levels F, E, ambient.
2. Nine ambient-dimension-two types. J is a line, and the two flags have their
   proper lines in one of three possible composition placements each. The
   three proper lines can be represented by e1, e2, e1+e2.
3. Two ambient-dimension-three types. The two flags are opposite full flags.
   J is either span(e1+e2+e3) or span(e1+e2,e1+e3).

All entries are 0 or 1. An implementation should verify the catalogue's
dimension vectors, scalar endomorphism rings and Hom matrices over the actual
field. BGP/finite-Dynkin classification supplies completeness; checking a finite
catalogue's entries alone does not establish completeness.

For representatives I1,...,Ir with End(Ia)=Fq, compute every Hom dimension hab
by solving the actual arrow-commutation linear equations. Given multiplicities
m=(m1,...,mr), the endomorphism dimension is

    e(m) = sum_ab ma mb hab.

The semisimple quotient of End(⊕ Ia^ma) is ∏ Mat_ma(Fq). The kernel is its
radical, of dimension e(m)-sum_a ma². Lifting units across this nilpotent radical
therefore gives the explicit formula

    aut(m) = q^(e(m)-sum_a ma²) ∏_a |GL_ma(q)|,
    |GL_t(q)| = ∏_(i=0)^(t-1) (q^t-q^i).

This derivation is ordinary finite-dimensional algebra; it exposes every
quantity that has to be evaluated. No Hall-number query remains.

Let M be the acquired pair of actual flags, an A5 object, and let T be a
candidate E6 multiplicity type whose restriction after deleting J is M.
The group Aut(M) acts on possible J. The stabilizer of a J of type T is
Aut(T), because all flag arrows are injective and the maps on their vertices
are restrictions of the ambient map. Consequently that orbit contributes

    number of J of type T = aut(M) / aut(T).

Its J dimension and all four dimensions dim(J∩Fi), dim(J∩Ei) are additive
statistics of the indecomposable catalogue. Enumerating bounded multiplicity
vectors, rejecting incorrect A5 restrictions, and summing these explicit
positive integers gives the joint-intersection census. A fixed 29-entry
catalogue gives a polynomial-in-ambient-dimension enumeration with a large
fixed exponent; it does not imply a useful small exponent or fast observed
implementation. Field arithmetic, integer bit lengths, catalogue acquisition,
actual-flag recognition, and output size must all be charged.

### What this removes and what it does not

The E6 census can remove the recovered diamond theorem's common-target-carrier
hypothesis for two factors, provided the rest of its Fourier/rank derivation
is checked with separate Ei. This is a substantial specific barrier in the
P3 pipeline. The finite-type representation, classification and orbit-size
formula are not themselves new mathematics. Novelty of a raw-circuit compiler
using them is not established by these searches.

E7 and E8 in MWZ have flag-length triples (2,3,4) and (2,3,5). They suggest
further fixed-depth constructions when the acquired problem really has those
flags. Arbitrary numbers or lengths of flags do not inherit finite type.
Extra conditional constraints can change the representation category.

## 2. Positive intermediate sampling versus original-input sampling

**Subsequent continuation update:** the separate generic low-c row-prefix
method in `../affine_sampler/affine_slice_prefix_sampler.py` now addresses
original-input sampling through direct positive completion counts. See
`AFFINE_PREFIX_PRIOR_ART_AND_COMPARISON.md`. The caution below concerns
sampling directly from the E6 orbit/Fourier census; it does not deny the
new method's proved bounded/logarithmic-c constructive scope.

There is a direct constructive sampler for the *subspace census* above.
Select an admitted type T with probability proportional to aut(M)/aut(T).
Transport a canonical representative to the acquired actual pair of flags.
Then act on its J by a uniformly random element of Aut(M). Every J in an
orbit has the same stabilizer, so the orbit sample is uniform.

One can generate that group element without rejection from all ambient
matrices. In a known indecomposable decomposition of M, the endomorphism
algebra splits as a block-diagonal semisimple matrix algebra plus its radical
as a vector space. Draw the radical coordinates uniformly and each diagonal
GL block uniformly. Their sum is a unit, and this parameterization has equal
fibers (indeed it is unique after fixing the complement). A uniform GL block
can be built column by column, each column uniform outside the current span.
Choosing a uniformly nonzero complement coordinate and arbitrary span
coordinates implements that step directly. The chosen bases and transport
maps must themselves be acquired by linear algebra.

This is a reconstruction of a standard group-orbit sampling argument, not a
claim that a full original-input sampler has now been implemented. In
particular, the recovered matrix-product count uses signed Fourier sums.
Negative character contributions are not probabilities. Uniformly sampling
its census intermediates does **not** automatically sample accepted original
Boolean assignments. A genuine final sampler still needs positive fiber
counts or a proved family closed under the necessary original-input
conditionings. Repeatedly invoking a counting theorem outside its hypotheses
would leave an unacquired operation.

## 3. Rank-metric Fourier ingredients are classical

Philippe Delsarte, *Bilinear forms over a finite field, with applications to
coding theory*, J. Combinatorial Theory A 25 (1978):

- https://doi.org/10.1016/0097-3165(78)90015-8

The primary publisher record identifies the bilinear-forms association scheme,
its generalized q-Krawtchouk eigenvalues and the MacWilliams transform. This
matches the mathematical role of the recovered local signed-rank polynomial;
the full 1978 article was not obtained in this session.

Kumar Balasubramanian, Krishna Kaipa and Himanshi Khurana, *On the cardinality
of matrices with prescribed rank and partial trace over a finite field*:

- Full paper: https://arxiv.org/pdf/2407.14273
- https://doi.org/10.1016/j.laa.2024.10.011

Theorem 1.1 expresses counts for trace zero or a fixed nonzero trace through
the total rank-r count and a character sum. Its generating polynomial has
the factorization A_(n-k)(q^k T)∏_(i=0)^(k-1)(1-q^i T), and the paper also
treats rectangular matrices. These identities are useful positive local
fiber ingredients; they do not alone solve the global dependent-target
or original-input conditioning problem.

## 4. Strong ordinary implementations and the matched task

Official code repositories and primary descriptions:

- d4: https://github.com/crillab/d4
  Exact count: `d4 -mc file.cnf`.
  Compilation: `d4 -dDNNF file.cnf -out=file.nnf`.
- d4v2: https://github.com/crillab/d4v2
  Its documented BC-S1.2 input supports input declarations, AND/OR/identity
  gates, negated literals and a target; XOR can be expanded locally.
- SharpSAT-TD: https://github.com/Laakeri/sharpsat-td
  Primary paper: https://arxiv.org/abs/2308.15819
  Exact unweighted counting with tree-decomposition-guided decisions and
  preprocessing; decomposition time is part of the instance time.
- decdnnf_rs: https://github.com/crillab/decdnnf_rs
  Primary tool paper: https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2026.38
  The official implementation supports exact model count, conditioned model
  extraction, direct model access and uniform sampling of decision-DNNF.
  Its `--n-vars` option matters when the compiler's output omits variables.
- Sharma, Gupta, Roy and Meel, *Knowledge Compilation meets Uniform Sampling*:
  https://www.cs.toronto.edu/~meel/Papers/lpar18.pdf
  Official KUS code: https://github.com/meelgroup/KUS
- Kiesel and Eiter, *Knowledge Compilation and More with SharpSAT-TD*:
  https://proceedings.kr.org/2023/40/kr2023-0040-kiesel-et-al.pdf
  In particular Lemma 7 treats forgetting functionally defined auxiliary
  variables in the compilation setting.

The tested circuit is the **unaltered recovered**
`work_phase_diamond/matrix_affine_diamond_native_n72.json`: 72 original inputs,
24,676 gates, one accepted output. The expected count supplied by the recovered
research is 71,210,970,084,540,416. A large number alone does not establish
comparative capability.

`../baselines/circuit_to_cnf.py` uses a fresh variable for every gate and a
**full Boolean equivalence** for that gate, then forces the actual output true.
Each original assignment has one internal extension, so counting all CNF
variables is exactly the requested original-input task. Uniform CNF models,
if acquired, would project uniformly to original inputs for the same reason.
Each supported gate template is truth-table checked before conversion.

The exporter records source/CNF SHA256, number of declared variables and
clauses, byte count and translation time. `run_timed.py` records solver wall
and CPU time, Linux child peak RSS, timeout, memory bound, exit status and
the complete log. Solver parsing and preprocessing are within its timer.
Build/download setup is separated and identified, not hidden in solver time.
Check the adjacent baseline JSON/log files for measured results; no solver
success is asserted merely because compilation was attempted.

An ordinary count timeout does not prove a general speed separation, and no
successful original witness or uniform sample is claimed without executing
and validating it. A single fixture and two solvers support only a statement
about those measured routes, versions, parameters, machine and time budget.
