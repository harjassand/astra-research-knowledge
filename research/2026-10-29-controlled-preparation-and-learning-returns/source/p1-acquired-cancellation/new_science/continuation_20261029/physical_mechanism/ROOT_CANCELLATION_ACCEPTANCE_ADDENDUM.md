# Final receiving addendum: clarification and finite-word exclusion

29 October 2026. Actual focused continuation of the independent receiving
review. This addendum reviews the changes to the root document, not a new
external audit or a physical validation.

Reviewed final input:

    ACQUIRED_HIDDEN_RESPONSE_CANCELLATION.md
    sha256 c4d9c883fe9fd4eefac93d726e78483519d3d129eb43f4e1d16b7ff087a1d24c
    18419 bytes

The exact reviewed bytes are retained in
reviewed_versions/ACQUIRED_HIDDEN_RESPONSE_CANCELLATION_c4d9c883fe9f.md.
The prior full review and exact independent checks remain valid for their
earlier saved source version; this addendum assesses the specific changes.

## Verdict

**Accept the final scoped mathematical construction.** The root adopted the
two requested clarifications. The new Section 10 finite-word exclusion and
the conditional approximate comparator are correct. No further mathematical
correction is requested at this reviewed scope. This conclusion does not
establish historical novelty, an apparatus, favorable acquisition cost or
practical advantage.

## 1. Adopted clarifications

The injectivity boundary now explicitly requires injective self-adjoint
operators that are positive semidefinite in a common L2 geometry. For any
nonzero f, an injective PSD operator has <f,Tf> > 0, since zero would imply
T^(1/2)f=0 and then Tf=0. A positive convex mixture therefore also has a
strictly positive quadratic form on every nonzero f and is injective. The
previous transition-entry ambiguity is removed.

The finite nullspace basis now supplies a common exceptional mu-null set for
all zero-defect simplex configurations, including a continuum of candidates.
This is the correct way to avoid an uncountable union of null sets. It retains
the proof for arbitrary old records with only unconditional initial absolute
continuity.

The added configuration-selection qualification in Section 6 is also
appropriate: a deployment hidden-density ceiling must hold after conditioning
on the selected configuration, or a fixed finite menu must pay its entire row
envelope. A simultaneous Gram confidence statement alone does not establish
that selection/deployment premise.

## 2. New finite-word no-go in source B

Every source-B primitive is a symmetric binary stochastic matrix. Its constant
eigenvector has multiplier 1 and its centered eigenvector has

    lambda_j(h)=1-2u_j-2|v_j|h,

which is positive and strictly decreasing throughout [-1,1]. All conditional
binary matrices share these eigenvectors and therefore commute. A nonempty
finite word has multiplier equal to the product of its primitive multipliers.

For h1<h2, every factor at h1 is strictly larger than its positive factor at
h2. Their product is strictly larger. Any finite nonnegative mixture that
assigns positive mass to at least one nonempty word therefore also has a
strictly decreasing centered multiplier. An empty word contributes the
constant 1 and cannot reverse this strict inequality. This proves that the
next-label row cannot be independent of h except for the all-identity case.
Allowing word probabilities to depend on the initial visible label gives
the same argument separately for each source row.

The extension to arbitrary positive pulse durations in the stated generators
is correct: q_j(h) is strictly increasing and exp(-2tq_j(h)) is positive and
strictly decreasing for every t>0. Zero-duration factors contribute 1 and can
be omitted. The result excludes finite open-loop words and their stated
randomizations. It does not exclude outcome-conditioned stopping, intermediate
feedback, per-specimen identification or a new physical operation. Those
exclusions are explicit in the root document and must remain attached.

This is a stronger separation of the two sources than the single-call simplex
witness: source A has useful exact one-call compiled transitions, while source
B has none obtainable by the finite open-loop word construction. It remains
a supplied-source mathematical capability separation, not a proof of a new
laboratory route.

## 3. Waiting-plus-identity comparator

In source B, mode 0 has lambda(h) in [7/10,9/10]. For L repetitions and
a_L=E_nu lambda(H)^L, the proposed probability

    w=(c-a_L)/(1-a_L)

lies in [0,1] whenever a_L<=c<1. The compiled centered multiplier
w+(1-w)lambda(h)^L has nu mean exactly c. Its deviation from c is
(1-w)(lambda(h)^L-a_L), whose absolute value is bounded by
(1-w)(9/10)^L. A binary stochastic row's TV difference is half its centered
multiplier difference. This proves the stated per-step bound and its n-stage
adaptive hybrid extension, uniformly even if the old record identifies H.

The reference target may be obtained to finite accuracy but never exactly at
finite L unless the action is the trivial identity. The comparator therefore
properly prevents the claim that absence of an exact word compiler proves
absence of useful approximate control.

Physical qualification: an identity branch is an available empty word in the
stated endpoint-only mathematical language. If elapsed time is exposed, a
state-preserving delay/padding implementation must actually exist; the source
does not supply it merely by writing an identity matrix. The document's
explicit padding requirement records this condition. The approximate
comparison is not a hardware-cost advantage claim.

## 4. Verification status

The earlier independent rational checker already confirms weighted loop
orientation under different reversible weights, the two useful mixture
probabilities, the 1/600 source-B simplex lower bound, the 1/100 cross-return
separation, the 3/20 exposed-key discrepancy and positive Hankel determinants
at five finite sizes. Section 10 is established by the monotonicity argument
above; repeating numerical word enumeration would not strengthen that proof.
The mathematical source and physical interface assumptions remain the limits
of this acceptance.
