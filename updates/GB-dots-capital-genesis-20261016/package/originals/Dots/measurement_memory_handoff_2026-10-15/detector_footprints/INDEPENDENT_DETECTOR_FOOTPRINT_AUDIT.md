# Independent detector-footprint audit

## Result

PASS. Independent reconstruction reads the original HX_33.json and HZ_33.json, but neither imports nor executes check_complete_detectors.py. It uses lowest-pivot binary elimination instead of the submitted highest-pivot implementation. Run `python independent_audit_detector_footprints.py`; detailed verified counts are in independent_audit_detector_footprints.json.

- 33 physical qubits; X and Z ranks 16 each; all X/Z rows commute; k=1.
- Pure X and Z logical enumeration finds none at weights 1–3 and exactly four weight-4 representatives of each type. This proves distance four also for mixed Paulis: a mixed logical must have at least one nontrivial pure component, whose support is a subset of its support.
- All 40 target check supports are correctable.
- The 32 weight-four targets each require seven selected original checks; the smallest detector union has 14 qubits. Across these targets: 4,096 minimum sets, 2,048 correctable sets, 3,456 distinct target/union certificates, 1,856 correctable unions.
- The eight weight-five targets each require nine selected original checks; the smallest detector union has 18 qubits. Across these targets: 57,600 minimum sets and 21,864 distinct target/union certificates, all uncorrectable.
- Total: 61,696 minimum sets and 25,320 target/union certificates. Every union, multiplicity histogram, check basis, logical quotient dimension, and stored logical witness was verified independently. Witness verification checks support containment, commutation with all opposite-type checks, and exclusion from the appropriate full stabilizer row span.
- All stored illustrative expansion certificates and all overlap-closure chains were verified.

## GF(2) criterion and what is minimized

For a CSS code, let H_t be the full check matrix of type t and d=|D|. The dimension of pure-type-t centralizers supported on D is d−rank(H_opposite restricted to D). The dimension of pure-type-t stabilizers supported on D is rank(H_t)−rank(H_t restricted to D-complement), by rank-nullity of the puncturing map on the stabilizer row space. Their difference is exactly the logical quotient dimension used by the submitted script. D is correctable precisely when both differences vanish. Mixed Paulis introduce no additional exception because the two CSS components separate.

For a correctable target A, completeness of selected code checks against every nonstabilizer Pauli on A is equivalent to their restricted kernels equaling the full-check restricted kernels. Since selected checks are a subset of the full checks, this is equivalent to equality of restricted row spaces, hence restricted ranks, independently for X and Z. Therefore the minimum number of selected original X/Z checks is the sum of the two restricted ranks, attained by choosing one restricted row basis of each type. The enumeration exhausts every such choice.

The recorded minimum union size is initially computed among minimum-cardinality sets. It is also the minimum over all complete subsets of the original checks: any complete subset contains a restricted basis of each type, whose support union is contained in the original union. Likewise every complete superset for a weight-five target is uncorrectable, since its contained minimum-basis union already supports a logical operator. These statements concern selection from the supplied original generators, not replacement by arbitrary products of generators.

## General self-contained reservation theorem

Work modulo Pauli phases. Let D contain d qubits, and let G be an abelian stabilizer group supported wholly in D, of rank g. Assume

Pauli(D) intersect Centralizer(G) is contained in S_code.

Write S_D for the code stabilizers supported wholly in D, with rank s. The left side has binary symplectic dimension 2d−g. Since G is abelian, G lies in that left side; therefore the hypothesis itself implies G is a subgroup of S_D. Thus

g ≤ s ≤ d and 2d−g ≤ s.

These inequalities force g=s=d. Consequently G=S_D is maximal on D and fixes a unique pure stabilizer state |phi_D>. The code subspace factorizes exactly as |phi_D> tensor C_(D-complement). Equivalently, any other stabilizer's restriction to D centralizes this maximal group and can be canceled by a member of S_D. Conversely such a pure factor admits a self-contained complete detector group.

This proof does not require G⊆S_code as a separate premise: abelianness and the stated containment already imply it. It does require a valid stabilizer group, without −I, and the usual phase-insensitive Pauli identification.

## Why the overlap graph closes every nonempty reservation

For a pure stabilizer factor on D, every full-code check restricted to D belongs to the same maximal commuting stabilizer space. Thus any restricted X and Z checks must commute, so |supp(X) intersect supp(Z) intersect D| is even.

Independently, every nonempty X/Z intersection in these matrices has exactly two vertices. There are 112 distinct edges, their binary incidence row rank is 32, and direct breadth-first connectivity reaches all 33 vertices. Even intersection with D means both endpoints of every edge have the same membership in D. Connectivity therefore forces D to be empty or all 33 qubits. The full code has rank 32<33, so the all-qubit set cannot satisfy the pure-factor theorem. No nonempty self-contained complete detector reservation exists. This establishes the obstruction for arbitrary stabilizer detector groups as well as for subsets of the listed original checks.

## Scope

This is an obstruction to a full-Pauli, entire-detector-footprint, zero-good-support certificate of the stated kind. It does not rule out noisy quantum error correction, correction with nonzero residual good support, probabilistic or restricted fault models, recovery-based certificates, temporal extraction methods, or any other construction not satisfying that premise. Correctable weight-four detector unions do exist; their correctability alone does not mean their selected checks are complete on the enlarged union. The self-contained theorem and connected overlap graph explain why further completion cannot terminate at a nonempty self-contained region.
