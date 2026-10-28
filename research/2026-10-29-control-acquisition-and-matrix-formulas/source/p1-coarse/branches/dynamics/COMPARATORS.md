# Primary comparators for scalar-word operator acquisition

Selective retrieval on 28 October 2026. This is a scoped prior-art comparison,
not an exhaustive novelty search. Sources below were opened or returned by
primary-source search. The March 2026 paper is particularly load-bearing.

## Existing noncommutative realization

Petreczky, Bako and van Schuppen, **Realization theory of discrete-time linear
switched systems**, Automatica 2013; preprint 2011/2012:
https://arxiv.org/html/1103.1343v2

The paper already characterizes switched input/output realizability by finite
rank of a generalized Hankel matrix, constructs state-space models from such
data, and proves minimality and uniqueness up to isomorphism. Its primitive
algebra is the product of noncommuting mode matrices. Therefore neither a
word-indexed scalar law, a Hankel representation, nor reconstruction of a
finite switched system is by itself a new principle.

## Switched models learned without access to system matrices

Gosea, Petreczky and Antoulas, **Data-driven model order reduction of linear
switched systems in the Loewner framework**, SISC 40(2), B572–B610, 2018:
https://arxiv.org/abs/1712.05740
https://pure.mpg.de/rest/items/item_2582694_5/component/file_2583337/content

This already builds switched state-space surrogates from generalized
input/output transfer-function samples without the original system matrices.
The paper's introduction explicitly discusses state components whose relevance
changes between modes. It compares with switched balanced truncation. Thus
the advantage cannot be stated as the first ability to learn switching
dynamics without identifying microscopic coordinates. The input interface
differs from physically acquired finite scalar echo words.

## Full-operator residuals from Gram matrices

Colbrook and Townsend, **Rigorous data-driven computation of spectral
properties of Koopman operators for dynamical systems**, CPAM 77(1),
221–283, 2024 (preprint 2021):
https://arxiv.org/abs/2111.14889
https://onlinelibrary.wiley.com/doi/full/10.1002/cpa.22125

Residual DMD uses Galerkin data for both K and K* K to compute residuals of
the full, potentially infinite-dimensional operator. It distinguishes these
from residuals of the finite fitted matrix, avoiding spectral pollution and
supporting dictionary verification. Hence the identity involving G, M and N,
and the importance of the extra second-moment matrix, have a direct strong
antecedent. Public implementation:
https://github.com/MColbrook/Residual-Dynamic-Mode-Decomposition

## Current direct comparator: invariance and multistep certificates

Conradie, Boulle, Loiseau, Brunton and Colbrook, **Trustworthy Koopman Operator
Learning: Invariance Diagnostics and Error Bounds**, 16 March 2026:
https://arxiv.org/html/2603.15091v1

The paper computes closure/invariance diagnostics from G,A,L; its Algorithm 3
uses the quadratic forms of L-K* G K along reduced trajectories to bound
multistep prediction errors. It also refines dictionaries using these
diagnostics. Its RKHS construction avoids the large-data limit needed for
quadrature-based L2 Grams. Thus a claim that finite Grams were previously
unable to certify projection error would be false. Its input data are state
snapshot pairs and dictionary/kernel evaluations. The prospective difference
here is the acquisition of the physical Hilbert products through calibrated
scalar reverse-word experiments, followed by bounded-error certificates for
arbitrary switching and a dual-corrected scalar output. These differences
must be proved and costed, not inferred from a renamed Gram matrix.

Implementation and dataset:
https://github.com/GustavConradie1/TrustKoopman
https://zenodo.org/records/19402733

## Nonintrusive sampling and certification

Pradovera, **Toward a certified greedy Loewner framework with minimal
sampling**, Advances in Computational Mathematics 49, 92, 2023:
https://arxiv.org/html/2303.01015v3

This derives a computable nonintrusive sampling indicator related to the
state residual. The scaling constant in its residual identity is generally
unavailable nonintrusively; the paper separates that sampling use from
termination strategies, and discusses noise/overfitting. It is a relevant
comparison for acquisition driven by measured residual geometry. The proposed
echo interface can supply particular norm constants directly, but only under
its supplied reciprocal contraction/preparation/receiver assumptions.

## Current structure-preserving data-driven reduction

Reiter and Werner, **Symmetric Hermite quadrature-based balanced truncation
for learning linear dynamical systems from derivative data**, 2026:
https://arxiv.org/abs/2606.00298

This constructs linear reduced models from transfer-function and derivative
data while preserving state-space Hermiticity and asymptotic stability. It
is another reason to avoid describing structure-preserving reduction from
scalar observations as generically new. Its derivative acquisition and
single-system transfer-function input are distinct costs/interfaces.

## Scope of an actual addition

The useful candidate is an experimental compiler for prescribed reciprocal
operations: execute words and their reversals to acquire true source Hilbert
products; allow an arbitrary proposed finite representation; evaluate its
defects from the same acquired scalar data; correct a specified terminal
quantity using a dual trajectory; and provide a source-valid bounded-error
certificate without an inferred finite hidden rank. The exact frozen-law
counterexample in CLIFFORD.md shows why mixed experiments supply information
absent from every frozen response law.

An existing ResDMD, reduced-basis, Hankel or Loewner program that is given and
uses these same new experimental operations may tie the result. That does
not erase an acquisition construction, but it does rule out claims of a
generic computational superiority based merely on different branding.

## Remaining consequential challenge

There is no general guarantee that a small dictionary suffices. Noncommuting
contractions can generate a large reachable word space. Sparse preparation,
long-word attenuation, calibration precision, reset cost and coefficient
growth can dominate reading count. A complete operational comparison must
include these costs and an equally informed method allowed to retain the
same scalar word data.
