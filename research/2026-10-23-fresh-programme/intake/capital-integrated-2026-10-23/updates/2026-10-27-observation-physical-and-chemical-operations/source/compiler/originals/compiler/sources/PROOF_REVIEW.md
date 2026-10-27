# Scientific review of X13 and X68

**Decision: both achieve the frozen computational endpoint at its stated
scope.** I found no blocking mathematical gap in the global guarantees. Both
return valid all-reference conditional-Umegaki brackets and pass all four
asymmetric development inputs, all six originally frozen holdouts, and the
three controls. This is constructive computational success at the specified
positive rational 3x3 classical-channel interface. Historical theorem novelty,
physical advantage, general coherent-input results, and an advantage of a
research organisation are not established.

## Proof and source-bound decisions

- **X13:** the selected denominator-only covariance construction is sound,
  including singular K. The substantive sources are phase1/worker1/PROOF.md
  Sections 1–4 and its evaluator/verify.py, and the released phase2/PROOF.md.
  I independently derived its noncommutative block inverse, the Schur test
  T^*T<=cI iff TT^*<=cI, its completed-square identity, and the attained SDP
  dual proving center completeness. Phase two clarified an overbroad phrase
  about products and a dual sign convention; the precise valid argument was
  already recoverable without changing any formula or certificate. The two
  selected scientific Python files are byte-identical across the freeze.
  The final driver replaces nonfinite optional float displays with null for
  strict JSON; it does not change exact scientific fields.
- **X13 Gram alternative:** phase1/GRAM_SDP_PROOF.md is also correct. Its
  three 8x8 positive Gram matrices have an exact converse on the support of
  their sum; the linear inverse-action equations recover genuine effects
  and inverse solutions. Real-part reduction preserves the full complex
  optimum. The rational dual shift is fully charged by its valid scaled
  trace bound, and its rounded Gram lower witness is evaluated as an actual
  witness without assuming exact floating primal feasibility. A separate
  control replay certified width 8.71e-6 in the reviewer solver environment.
- **X68:** phase1/global_certificate/GENERAL_PROOF.md and PROOF.md establish
  a complete general 9x9 SDP, including singular K. I verified both the
  singular-value reduction and the degree-two moment converse. Given
  0<=Y<=diag(X_i) and (diag(X_i)-Y)E=0, the contraction/projection dilation
  reconstructs the required first and second moments even on singular
  supports. The compact normalized primal has a strict point, so the stated
  dual is exact and attained. Its 9x9 and 6x6 rational PSD checks are valid.
  The portable inverse-covariance and common-center proofs are also sound;
  a singular-K failure of inverse-K numerical coordinates retains a valid
  wider bound, and the general branch supplies the missing tight acquisition.

All arguments cover arbitrary finite complex Hermitian noncommuting effects.
Strict channel positivity keeps every output mixture uniformly invertible at
PSD effect boundaries. L's zero-sum injectivity gives a uniformly positive
denominator. Thus closure witnesses and faithful approximation are legitimate;
none of the arguments silently extends to singular channel outputs or an
uninformative L. Rational lower witnesses are genuine free witnesses and the
accepted active/vacuum lift supplies Umegaki supremum lower bounds. A boundary
quotient need not be attained by one finite faithful state pair.

The small subunit center argument additionally gives real active dimension at
most two here, improving the supplied active-three cutoff. Above one, scalar
vertices suffice. No new credit attaches to equality, binary or metric transfer:
N965, N970, the finite free formula and its refinements are accepted priors.
Detailed independent derivations are in DERIVATION.md.

## Checks and resource scope

I replayed isolated reviewer copies, then recomputed upper conditions and exact
witness ratios using a separately written checker. All thirteen inputs passed
for each candidate. H03 exercises the subunit branch; the quantum control has
an exactly noncommuting active-dimension-two lower witness. The ten asymmetric
cases are computational instances, not independent policy replications.

| Check | X13 | X68 |
|---|---:|---:|
| Largest width on ten asymmetric inputs | 2.654e-9 | 2.795e-8 |
| All-thirteen process clock before final serialization, including imports | 0.6012 | 0.2243 |
| Slowest of thirteen fresh processes, seconds | 0.5305 | 0.2368 |
| Six fresh reviewer inputs | all pass | all pass |

Fresh-process timing includes input preparation, startup, imports, construction,
the executable's exact checks, and serialization. These selected paths use the
inherited standard-library/NumPy/SciPy/SymPy runtime and need no new package
installation or instance answers/cache. Ordinary OS file caches were present;
no hardware-independent or all-rational-bit-length runtime claim follows.

Six deterministic fresh reviewer inputs include a genuine contraction, exactly
singular nonconstant K, and near-constant but informative L. The last has a
coefficient about 1.37e9; X68's width 1.22 still satisfies the specified relative
tolerance. The exact noncommutative identities also passed on genuinely complex
rational POVMs in dimensions two and three, including singular K. At 75 digits,
two arbitrary moment-cone reconstructions, one with singular first moments,
had residuals below 1.7e-75. These finite checks support the displayed proof.

I independently checked all thirteen separately delivered X68 general 9x9/6x6
matrices against the released inputs and already verified lower witnesses.
They all pass the width target. Evidence is in checks/INDEPENDENT_CHECKS.json,
INDEPENDENT_FINAL_AND_FRESH.json, INDEPENDENT_GENERAL_DELIVERY.json, and
COLD_FINAL_REPLAY.json. Candidate source setup costs remain as reported:
X13's optional Gram packages were separately provisioned; X68's optional
general-solver initial provisioning is UNKNOWN. Neither setup is needed for
the successful selected endpoint path.

## Strongest historical alternative and actual increment

The supplied baseline is a useful measured incumbent, but not the strongest
equally informed prior method. Helton–Klep–McCullough's **Theorem 1.1(2)**
already gives an exact bounded-degree SDP for matrix-polynomial positivity on
a monic free spectrahedron:
https://arxiv.org/html/1102.4859 and
https://doi.org/10.1016/j.aim.2012.04.028 . Volčič's rational convex
Positivstellensatz, **Theorem 5.2 and Section 5.5**, supplies a more general
rational route:
https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/hilberts-17th-problem-in-free-skew-fields/1DC74DC3E0E011210C826FF4DCA24DE1 .
The 2017 regular-rational predecessor cannot simply be invoked: the channel
row inverses can have poles outside the simplex.

Applicability is concrete. Translate Q_1=I/3+X_1, Q_2=I/3+X_2,
Q_3=I/3-X_1-X_2. The domain pencil is
diag(I+3X_1,I+3X_2,I-3X_1-3X_2), which is monic with interior. The audited
denominator-only Schur inequality is a symmetric 2x2 degree-two polynomial.
The 2012 theorem with d=1 therefore gives a coefficient-matching SDP with four
6x6 PSD Gram/localizing matrices and fifteen word coefficients through degree
three. It covers singular K and all complex levels by realification.

I instantiated this old machinery **after reading the candidate proofs**, using
their audited covariance linearization. The generic SOS upper constructor
rationally charges every coefficient residual. On all thirteen released inputs
it took 1.2043 seconds including imports, with maximum case work 0.0439 seconds;
its largest gap to the independently checked X13 lower witness was 1.724e-7.
It has no autonomous lower-witness collector, and reuses a post-exposure
linearization. It is not a frozen incumbent, team repair, or retroactive team
credit. Isolated reviewer dependency provisioning was uninstrumented/UNKNOWN;
an initial CVXPY/NumPy incompatibility was resolved locally. Full details and
primary-scope qualifications are in PRIOR_COMPARATOR.md and the OLD_SOS checks.

Thus the real increment relative to the displayed public priors is a completed,
efficient, exactly certified implementation and a small explicit covariance/
three-LMI specialization with a sharper dimension bound. Generic finite global
SDP machinery is established prior mathematics. Exact historical priority of
the specialized channel identity/small certificate remains UNKNOWN. Advantage
over the supplied baseline's wide upper bounds is established on these inputs;
advantage over the strongest historical certified evaluator is not established.

The supplied 9 October N405 source explicitly labels its universal Choi formula
an unreviewed theorem candidate. I did not assume that theorem correct or
transfer it from single-channel contraction to arbitrary K,L. Its centered
Gram geometry is relevant antecedent material, with that status retained.

## Exposure, remaining obligations, and next opening

I used general mathematical background, the common task/priors/baseline, the
authorized N405 extraction, both frozen scientific packages, and then the
explicitly released final packages/holdouts. Both phase-one packages were read
before the final release. Source prose revealed original identifiers and
worker structure, so this is label-masked, not fully blind. No policy key,
parent diagnosis, other review, original team directory, targeted memory
lookup, researcher contact, or delegation was used. The supplied general
session memory summary was visible but supplied no candidate-specific proof.

No scientific repair was required for the reported endpoint. Solver acquisition
can still return a wider valid interval; uniform narrowness/runtime over every
unbounded rational encoding remains unproved and was not the frozen endpoint.
The substantive internal audit is sufficient at this actual scope. The useful
next opening is a measured comparison with the instantiated generic free-SOS
method including independent lower acquisition, conditioning, exact arithmetic,
setup and full-cycle cost; extending the special identity to other channel
shapes would require a separate proof. Neither this audit nor one team pair
supports a research-policy, discovery-probability, or civilisation-scale claim.
