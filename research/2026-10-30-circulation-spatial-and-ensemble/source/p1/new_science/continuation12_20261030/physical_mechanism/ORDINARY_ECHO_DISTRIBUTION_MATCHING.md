# Strong ordinary consumer of the inherited physical echo oracle

30 October 2026. Complementary construction after root selected hidden-ensemble
learning as its central question. This note gives the ordinary competitor
the same real echo operations. It does not claim a new inner-product identity,
kernel method, or physical time reversal.

## 1. Same actual supplier

Let mu be the warranted baseline probability law. Every primitive P_a is
an actual finite-duration mu-reversible Markov kernel. For a chronological
word W=P_(a1)...P_(al), its adjoint W* is physically executed by calling
the same primitives in the opposite order. A fresh bath realization is
used; the earlier microscopic path is not reversed or replayed.

Candidate j starts from the physically prepared normalized density f_j
relative to mu, where f_j is known, visible and 0<=f_j<=L. It executes
word W_j. Its true final density is r_j=W_j* f_j. The target, indexed 0,
likewise has density r_0=W_0* f_0. Every actual initializer, including
visible rejection from fresh baseline specimens, has its own cost.
Merely knowing f_j is not that initializer. Frozen hidden variables
need not mix under the words.

In the standard L2(mu) convention, the inherited chronological echo gives

\[
 G_{ij}:=\langle r_i,r_j\rangle_\mu
 =\langle f_i,W_iW_j^*f_j\rangle_\mu
 =E_\mu[f_i(Y(X_0))f_j(Y(X_{\rm end}))].            \tag{1}
\]

The experiment executes W_i followed by the reversed-order W_j on one
persistent specimen, between the two visible reads. Its bounded output
lies in [0,L^2]. This is the established adjoint/Markov inner-product
construction already present in the Astra acquisition interface. The
literal order, common invariant law and actual adjoint access are essential.

## 2. Deterministic library selection already solves a useful receiver

For each candidate,

\[
 d_j^2=G_{jj}+G_{00}-2G_{j0}
      =\|r_j-r_0\|_2^2.                           \tag{2}
\]

Suppose simultaneous entry errors are at most eta. Then
|dhat_j^2-d_j^2|<=4eta, and

\[
 {\rm TV}(r_j\mu,r_0\mu)
 \le\tfrac12\sqrt{\max\{0,\widehat d_j^2+4\eta\}}. \tag{3}
\]

An ordinary finite-library search can select the cheapest candidate whose
upper certificate is below a requested tolerance. It needs only the m
target cross entries, m diagonal entries and one target diagonal, rather
than the full candidate Gram matrix. The actual selected program is
deterministic conditional on the retained calibration D.

Any common future physical controller, including its adaptive choices
and emitted records, is a Markov kernel from the initial microscopic
state to its complete record. Total variation contracts through it.
Thus (3) controls every such future at once, at any finite horizon, and
also any well-defined infinite record via finite-cylinder approximation.
No finite predictive-state closure is required.

This implication is ordinary data processing. Its useful force comes from
having acquired the full-density norm in (2), which generic visible-sample
kernel distances do not supply. A small characteristic-kernel MMD on one
visible snapshot does not quantitatively certify hidden-state TV.

The estimate holds jointly with D when the baseline initializer and device
law in each new assay/deployment are valid conditional on D. It is an
averaged joint guarantee, not an arbitrary rare-postselection claim.

## 3. Convex mixtures give the strongest conventional training family

Allow actual private random selection of candidate j with probabilities
w in the simplex. After execution, with the preparation selector withheld
from the subsequent service, the physical output has density

\[
 r_w=\sum_{j=1}^m w_jr_j.
\]

Put v(w)=(-1,w_1,...,w_m). Then

\[
 D(w)=\|r_w-r_0\|_2^2=v(w)^TGv(w),\qquad
 \|v(w)\|_1=2.                                   \tag{4}
\]

Expected preparation cost is c dot w for supplied actual costs c_j.
Minimizing D over a cost simplex, minimizing cost at a certified D
tolerance, or minimizing c dot w+lambda D is a conventional convex
quadratic program. No gradient of the unknown material is needed.

Finite samples can make the symmetric estimate Ghat indefinite. Do not
call that numerical matrix an exact positive kernel. On a simultaneous
entry-error event, the true G is feasible in

\[
 \widetilde G\succeq0,\qquad
 \max_{i,j}|\widetilde G_{ij}-\widehat G_{ij}|\le\eta. \tag{5}
\]

Choose any feasible matrix by an ordinary semidefinite feasibility solve,
paying numerical precision and certificates. Then

\[
 \max_{i,j}|\widetilde G_{ij}-G_{ij}|\le2\eta,
 \qquad |v^T\widetilde Gv-D(w)|\le8\eta             \tag{6}
\]

uniformly over every simplex w. Consequently

\[
 {\rm TV}(r_w\mu,r_0\mu)
 \le\tfrac12\sqrt{v^T\widetilde Gv+8\eta}.         \tag{7}
\]

An exact minimizer of the repaired objective under a fixed cost constraint
has true squared-distance regret at most 16eta relative to the true best
mixture in that same feasible set. For a cost-at-tolerance problem, only
candidates satisfying the certified constraint are promised; one does
not compare their cost to points at an unpadded tolerance that may fail
the acquired constraint.

If feasibility or optimization is approximate, its certified residual
must be added. An entrywise bound, not uncontrolled eigenvalue clipping,
is the stated route.

## 4. Price and record boundary

For q distinct Gram entries and m0 fresh episodes per entry, Hoeffding
gives a simultaneous entry error eta with failure at most delta if

\[
 m_0\ge\frac{L^4}{2\eta^2}\log(2q/\delta).          \tag{8}
\]

Every episode costs a baseline preparation, two feature readings and
the durations/calls of both constituent words. A naive certificate of
TV epsilon near zero mismatch needs eta of order epsilon^2, hence a
conservative epsilon^(-4) sample budget. This is not claimed optimal.
Large density ceilings, long words and large libraries can destroy
usefulness even without hidden-state dimension.

The mixture selector must be actually isolated from the later controller
for (4) to be the relevant initial state. A public selector, timing leak,
or retained preparation record changes the comparison to a joint law.
If the reference retains the same independent selector, the natural
branchwise certificate is

\[
 \sum_jw_j{\rm TV}(r_j\mu,r_0\mu)
 \le\tfrac12\sum_jw_j\|r_j-r_0\|_2,               \tag{9}
\]

which cannot exploit cancellation among candidates. Unequal durations
do not supply a free holding/padding operation for common public
completion. Such controls must exist and be costed, or duration is part
of the record.

Candidate selection from calibration is different: conditional on D
it selects a fixed program, and can use (3), provided the conditional
preparation premise remains true. Neither route turns a frozen old
specimen into a new independent baseline population.

## 5. What the comparison changes

Once the actual hidden-density Gram oracle is available, ordinary
minimum-distance distribution matching supplies a convex full-state
preparation learner over finite randomized program libraries.
Gretton et al.'s Hilbert-distance/kernel-discrepancy formulation and
standard convex optimization are direct mathematical predecessors.
They do not provide the physical hidden-density oracle in (1), nor
generic TV control from a visible kernel.

The inherited echo construction can supply an otherwise unavailable
statistical kernel on physical programs. Generic claims that an unknown
material can provide gradients or that a Gram matrix can train mixtures
would not be the new consequence. A consequential claim must earn its
supplier, attainable program family, retained-record guarantee and
complete resource advantage or explanatory reach.

This comparator assumes no hidden-state copying, microscopic time
reversal, differentiable native force or finite latent model. It permits
all actual echoes and paid baseline preparations supplied to the proposed
method.
