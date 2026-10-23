# Ordinary retaining reconstruction matches the new acquired programs

## Result and scope

This **post-test baseline strengthening** reconstructed every available new
action and readout from retained raw TRAINING observations plus the shared
acquired chart/fiber. It did not read fitted new programs or audit outcomes in
the fitter, make source queries, open truth data, rerun the frozen experiment,
or execute DreamCoder. The seven cases and the original algorithm had already
been exposed; there is no new independent-confirmation claim.

All six available new-action programs and all seven readouts have exactly the
same canonical Boolean polynomial coefficients as the frozen programs. All
1,008 stored raw audit-row predictions agree. Therefore the reconstructed
programs inherit exactly the same 13 existing warrants, with no additional
confidence allocation. The seventh new action, in case_04, remains UNKNOWN.

| Case | Raw dimension | Fiber rank | Retained action training pairs | Retained readout training pairs | New-action result |
|---|---:|---:|---:|---:|---|
| case_01 | 8 | 3 | 7 | 7 | Exact canonical match |
| case_02 | 7 | 2 | 4 | 4 | Exact canonical match |
| case_03 | 10 | 3 | 7 | 7 | Exact canonical match |
| case_04 | 11 | 2 | 1 | 4 | Observed fiber escape; UNKNOWN preserved |
| case_05 | 9 | 3 | 7 | 7 | Exact canonical match |
| case_06 | 12 | 3 | 7 | 7 | Exact canonical match |
| case_07 | 20 | 10 | 56 | 56 | Exact canonical match |

Case_04's retained training response is raw input 979 to raw output 806. The
independent adapter maps output 806 to global chart value 2040; reduction against
the acquired fiber basis leaves nonzero remainder 4. The output is outside the
declared fiber. The procedure neither fills missing labels nor fabricates an
endomorphism, and issues no new-action warrant. Its readout still reconstructs
from its own four observations.

## Data separation

`prepare_inputs.py` selects new-action events solely by the released action ID
and phase `acquisition`. It selects readout events solely by phase
`new_readout_training`. The resulting `training_only.json` contains raw
input/output pairs, original paid-event provenance, and the shared chart/fiber.
It contains no fitted coefficients, transformed displacement values, audit
outcomes or truth answers. The projector parses existing result files but
passes none of those excluded fields to the fitter.

`fit_retaining.py` accepts only that training file. It constructs exact GF(2)
fiber coordinates independently, checks the prescribed raw query prefix,
performs ordinary degree-two Boolean Möbius interpolation, and saves
`reconstructed.json`. It neither imports the original shear learner nor reads
the original acquisition files. The only shared execution code is the acquired
chart implementation, whose version is hash-bound and whose acquisition is a
common paid input.

Only after the reconstruction file has been saved does `validate_identity.py`
read the frozen fitted programs and saved raw audit rows. It checks canonical
identity and replays those observations without calling a source. The sequence
and process receipts are preserved in `RUN_RECEIPT.json`.

## Why the coefficients must be canonical

Let the acquired raw chart be R, let y0 be the retained fiber anchor, and let B
contain independent fiber directions. The explicit fiber chart is

    C(t) = R^(-1)(y0 + B t),    t in F_2^r.

All additions are XOR. The acquired R is a proved executable bijection, and B
has independent columns. Hence C is a bijection onto the declared subset; exact
GF(2) elimination either returns the unique t or detects nonmembership.

For a retained raw transition response x -> x', the training value is

    D(t) = C^(-1)(x') + t,    where t = C^(-1)(x).

If x' is outside the fiber, this value is undefined and the fit returns UNKNOWN.
Otherwise the data comprise D(1_T) for every subset T of size at most two. An
ordinary degree-two vector polynomial has the unique square-free form

    P(t) = XOR_(|S|<=2) c_S product_(i in S) t_i.

At a low-weight indicator 1_T, its value is the XOR of coefficients c_S with
S contained in T. Boolean Möbius inversion therefore gives

    c_S = XOR_(T subset S) D(1_T).

Over GF(2), this inverse has the same coefficients as the subset-sum transform:
an off-diagonal coefficient is counted 2^k times for k>0 and cancels, while a
diagonal coefficient is counted once. This proves uniqueness of the degree-two
interpolant to these training values, irrespective of whether the unknown true
source has degree two globally. The scalar readout uses the identical transform
with one-bit coefficients.

The independent fitter computes every coefficient, including zero coefficients.
The validator compares this complete canonical list with the frozen vector
polynomial b*f and frozen scalar readout. It also checks that the frozen support
lies within the degree-two masks. Equality of all coefficients proves equality
on every point of the declared fiber; exhaustive point enumeration is not
needed for this identity.

The candidate source agreement is still UNKNOWN outside the evidence supplied
by existing warrants. An ordinary interpolant always fits these prescribed
labels when they are present. That fact alone does not recognize a global
source class or rule out higher-degree terms invisible at the queried points.

## Involution and warranty transport

For action reconstruction, all nonzero vector coefficients must equal one
direction b. The fitter independently expands the Boolean polynomial
f(t+b)+f(t); it accepts the shear syntax only when every term cancels. Then

    T(t) = t + b*f(t)

is an involution: if f(t)=0 it fixes t; if f(t)=1, translation invariance makes
the second application add b again. Consequently it is a permutation of the
explicit fiber and may be composed using the same invariant-uniform-law proof.

More directly, let T_old be the candidate fixed before an original audit and
T_new the independently reconstructed candidate. Canonical equality proves
T_new = T_old everywhere on the audited domain. For the fixed true source F,
the disagreement sets

    {x: F(x) != T_new(x)} = {x: F(x) != T_old(x)}

are identical. The same statement holds for the reconstructed readout. Every
existing finite-population warrant, including its epsilon, failure bound,
domain and source version, therefore applies unchanged. This is transport by
proved functional identity, not a new statistical test after inspecting data.
The old candidate's pre-audit fixation and randomness conditions remain the
ones on which the warrant depends. The post-test choice to implement a baseline
does not create new independent evidence.

The validator's replay is a concrete implementation check of this identity on
all 1,008 retained/new audit rows. The global polynomial-identity argument is
what allows transfer beyond those checked rows. It does not transfer a warrant
to a different raw domain or source version.

## Acquisition and computation costs

There were 181 training-memory accesses: 89 action input/output pairs and 92
readout input/value pairs, totaling 4,421 declared payload bits. All 181 labels
were originally paid source responses; the retrospective reconstruction did
not make their acquisition free.

An online retaining learner can generate the identical query sequence from the
shared chart: the raw query for mask S is C(1_S). The saved records are checked
against this exact sequence. It stops on case_04's same first escape. Since the
other fitted functions are identical, it can then run the same retained audits
and obtain the same raw query sets and source costs.

Across the original seven-case pipeline, both methods share the following
comparison/transition/readout acquisition counts:

| Acquisition stage | Comparisons | Raw transitions | Readouts | Total |
|---|---:|---:|---:|---:|
| Common first stage | 4,614 | 3,035 | 0 | 7,649 |
| Second-stage fitting and warrants | 0 | 1,444 | 506 | 1,950 |
| Complete counted pipeline | 4,614 | 4,479 | 506 | 9,599 |

The public task-release metadata remains a shared supplied task input, and its
release calls remain in the original receipts. The table uses the original
comparison/transition/readout query-count convention. It does not add a second
acquisition bill merely for replaying saved labels.

For rank r, degree-two fitting uses Q=1+r+choose(r,2) labels and
1+2r+4*choose(r,2)=1+2r^2 coefficient XORs. Action coefficient XORs operate on
r-bit vectors; readout coefficient XORs operate on one-bit values. The adapter,
symbolic invariance check and exact shared-chart evaluations have additional
charged work. In this reconstruction, the recorded shared-chart counts are
270 forward calls, 181 inverse calls, 183,244 monomial tests, 3,712 word XORs and
207 elimination word XORs. Separate explicit interpolation/fiber logical
charges total 35,605 bit-work units. These counts are not a complete complexity
proof for Python hashing, allocation or integer-library internals.

Observed times from this single post-test execution:

| Work | Seconds | Scope |
|---|---:|---|
| All seven fits | 0.023738924 | Includes per-case shared-chart/fiber construction |
| Included chart/fiber construction | 0.000803163 | Subset of the preceding row |
| Fitter process | 0.068340510 | Includes startup, imports, input parsing and serialization |
| Projection process | 0.113516964 | Parses 11,237,937 saved bytes and writes the 59,697-byte training projection |
| Identity/audit-validation process | 0.283659813 | Includes loading frozen programs and replaying 1,008 stored audit rows |
| Successful orchestration body | 0.467762264 | All three subprocesses, artifact hashes and orchestration |
| Preserved failed attempt | 0.033277346 | Projection schema failure before fitting |
| Both attempt bodies | 0.501039610 | Includes the failed attempt; excludes authoring and tool-launch overhead |

The audit replay reads 50,240 declared row-payload bits. Actual file parsing and
serialization costs are also retained. These times describe the retrospective
reconstruction process. They are not an online end-to-end speed comparison:
the original paid oracle execution and common acquisition must still be included
in any such comparison. The result established here is identical attainable
programs and source-query requirements for an ordinary retaining learner.

## Preserved failed attempt and hashes

The first projector used the absent field `source_binding` where the source
oracle report uses `binding`. It failed before generating the training file or
running the fitter. Its five source/protocol files, freeze and failure receipt
are intact in `archive_attempt_1/`. The only correction was that field name;
the fitting algorithm, criterion and cases were unchanged. Version two was
frozen before execution at 2026-10-23 13:11:16 UTC.

| Artifact | SHA-256 |
|---|---|
| Version-two freeze | `dea81588ba92eda8657a2c37d01b4760d10b6b3b5a327ac95d9ba9e0be8827f7` |
| `training_only.json` | `630774d88435d983826e11848e846d555ef5aac25d8f43dc9728b7bed8fff482` |
| `reconstructed.json` | `c0f878fdd6a2661cb3f2d027d1697724b0401254b56bb89b7edf9bec1f03d75e` |
| `validation.json` | `2f7ee5d52c3f5d8847ab1265a480173464c632847f49ceb3cb3a6a121e80e3ab` |

The original frozen source/results were read only. Every fitted program,
coefficient, transformed training observation, audit replay row, failure and
timing remains in the accompanying JSON artifacts.

## Scientific attribution

The earlier comparison against an interpreter receiving already fitted programs
has now been strengthened: an ordinary retaining learner reconstructs the new
programs itself from the raw training data, using the same previously acquired
representation. Thus this benchmark does not establish an advantage over an
equally informed retaining library. It demonstrates executable reuse of an
acquired chart and domain, with explicit new evidence and operation-specific
warrants. That scoped capability remains useful; it is not a demonstrated
general-intelligence or architectural separation.
