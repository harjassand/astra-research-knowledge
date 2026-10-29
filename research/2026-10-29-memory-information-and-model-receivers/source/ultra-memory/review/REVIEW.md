# Independent whole review: accepted at the stated scope

29 October 2026. Reviewed A's complete `RETRACTION_PROOF.md`, SHA256
dc704f04c141b8312993ac772fdcfc5aec4b2c40dbbc3be90dd92178ebabd374,
and the full `compile_complex.py` / `check_retraction.py` code. Matched the
load-bearing definitions to the primary memory source2605.10943v1,
Sections3.2.2--3.2.7 and the actual five-qubit seed of Section3.3. Read the
relevant definitions, Lemma24 and formal AppendixC theorem of
[Yin--Lucas2411.01002v2](https://arxiv.org/html/2411.01002v2).

**Verdict:** the uniform polynomial check-soundness theorem and its qualified
zero-temperature spectral-stability consequence are mathematically accepted.
No substantive error or required change was found. This is a whole analytic
and implementation inspection, not an independent numerical replay of the
finite matrices. No new replacement level, trajectory or thermal experiment
was run. The actual contribution is the filling/retraction bridge; the
stability theorem itself is an established operation.

## Adversarial points resolved

**Actual family, not a convenient replacement variant.** The direct-sum
degree bases, doubled boundary cylinders, restrictions and dual replacement
match the primary definitions. The source seed matches the supplied [[5,1,2]]
seed up to labels. The independent `FAMILY_ADMISSION.md` proves preservation
of size-two overlaps, positive incidences and connected check links. Hence
the local H1(Yx)=0 fact and the natural square used by p2 are available at
all depths of THIS family. They are not inferred from finite ranks or
silently generalized to arbitrary overlap pairings.

**Disjoint projections.** Each selected Q point is used by only its own old
q. Each selected X edge lies on one x--q ray, is used only by q, and is in
one of two disjoint layers. Sharing the root vertex causes no collision of
degree-one coordinates. Therefore wt(p0 e)+wt(p1 e)<=wt(e) for all e, not
only cycles. Comparing two explicit projected words pays the adaptive layer
choice; no uniform layer is assumed beforehand.

**p2 telescope.** Start from a fine Z point, add all Q-edge rays from q to z,
then add the layer's subdivided squares of each old x,z intersection. The
Q vertices at z cancel; each square's q--z restriction rays cancel; its
x--q rays remain. This is exactly the old z row applied to p1. The one
size-two square per nonzero old x,z pair is essential. The F maps preserve
constants and satisfy the two displayed cochain identities.

**Full homotopy, not merely a cocycle decoder.** The X part of
e+d h1 e has a fundamental tree cycle as each coefficient row. H1(Yx)=0
fills that row in the SAME X-face pool. Integrating the Q-edge syndrome
along a Yq path then constructs the Q rows of h2. This gives the full
all-vector identity I-Fp=d h1+h2 d, whose transpose is legitimately used
in the opposite sector. A cocycle-only equality would not have justified
that transpose; the supplied proof does construct the needed full map.

**Rows versus columns and uniform constants.** F0 and h1 require column
bounds. p2 and h2 require row bounds, because their transposes lift Z-check
coefficients. An h2 row can use only one q's entire Q-edge pool and the
X-face pools of at most D old X neighbors. Repeated face appearances cancel
over F2; they do not multiply the pool bound by the path length. The stated
counts V*=2F*(t+1)^2, Fx*=2F*t(t+1), Eq*=D(2t+1) consequently bound all
four relevant costs independently of depth. F*<=D E=28 is conservative.
The ell3 value805 does not substitute for the primary's much larger fixed
geometric ell. In particular no favorable native perturbation constant is
being inferred from the finite consumer.

**Recurrence and logical transport.** RX contracts the X filling argument
and leaves the Z filling argument nonincreasing; RZ exchanges them. Whether
the contraction occurs before or after the noncontracting step, the paired
linear term is at most A(1+A)M and the recursive term is A^2 g(floor(M/2)).
The chosen p,K close the induction, including M=1 via g(0)=0. The degree-one
homotopy and pF=I give both cohomology and transposed homology equivalences;
both layer projections of a nonzero X logical class are nonzero. The
resulting distance lower bound2^k is valid. Binary phase transport is sound:
positive CSS generators commute and their group has no minus identity.

## The precise stability consequence

Yin--Lucas check soundness is a minimal GENERATOR-COUNT bound for stabilizers;
it is not syndrome expansion of arbitrary errors. A's proof establishes
exactly this bound, for both CSS parts and hence the whole group. For the
interaction graph, bounded-density finite-range Euclidean embedding bounds
balls by O((1+r)^3). Bounding each shell by the ball makes dimension parameter4
safe under that paper's definition. No unproved O(r^2) shell-area estimate or
inverse-Lipschitz spatial embedding is needed.

The formal theorem applies after a size-independent onset, with a positive
size-independent threshold in its strong-support, syndrome-resolved,
exponentially volume-weighted local norm. Its spectral splitting estimate
has an n prefactor times exp(-kappa ds/2); ds grows polynomially in n here,
so the prefactor can be absorbed for large n. The dressing statement is the
theorem's controlled projector approximation, not an invented exact local
unitary formula. Fixed-range bounded-incidence physical perturbations enter
that norm with a constant loss, whose value can be extremely poor.

The accepted result does not prove the original spatial TQO-2 statement,
a numerical threshold, efficient ground-state preparation, a perturbed
Davies generator, or a perturbed finite-temperature memory lifetime.
It does not acquire the primary Euclidean embedding at ell3 or a physical
Hamiltonian. Those are meaningful missing operations rather than reasons
to withhold acceptance of the proved zero-temperature bridge.

## Code scope and ordinary comparison

The Python consumer uses literal integer GF(2) vectors. The independently
inspected assertions compare full matrix products, not selected test words.
Its local h2 elimination uses only the claimed local pools; no hidden global
filling is used. The stored finite execution covers the retained RX and
dual-RX inputs, and demonstrates the implementation at those inputs. The
general conclusion rests on the symbolic identities and cell counts above.

This is not absorbed merely by the source's coarse-syndrome decoder or its
thermal theorem: check soundness concerns small stabilizers' generation
costs, a different degree/interface. Conversely, once that bridge and the
growth hypotheses are supplied, the spectral-stability conclusion is the
ordinary Yin--Lucas theorem. Priority of the new retraction proof remains
UNKNOWN; mathematical acceptance does not imply historical novelty or
hardware value.
