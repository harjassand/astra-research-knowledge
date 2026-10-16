# Exact Schur refresh: result and reproduction

One internal Schur-dephasing node per coordinate now has an exact two-gap endpoint bound, including an explicit equality construction. The bound accommodates the actual channel produced by independent generator dephasing, rather than replacing it with a scalar full-pinch mixture.

For independent private nodes with the stated commutation and full-joint-channel assumptions, the inherited causal tester embedding gives the corresponding shared-bath coordinate product bound. This is a conditional mathematical statement; it does not qualify an experimental channel or establish a syndrome-history support theorem.

For equal generator multipliers, established Hamming-weight/permutation averaging reduces the exact value problem to m real variables with an m-by-m matrix. The 32-generator example eta=p=q=1/4 has the exact certified value 4305/8192; both a feasible lower bound and a global tangent upper bound coincide. This demonstrates polynomial representation and exact certification for this case, not a measured runtime speedup. Arbitrary unequal multipliers retain an exponential explicit representation.

## Start here

- PROOF.md: exact optimization, complex/singular cases, witnesses, generator formula, and conditional product.
- HOMOGENEOUS_SYMMETRY.md: symmetry reduction, computational costs, exact benchmark family.
- VALUE_SENSITIVITY.md: an elementary value perturbation bound under already-qualified channel models.
- check_exact.py and check_results.json: direct finite-dimensional channel checks.
- check_homogeneous.py and homogeneous_results.json: exact small full-matrix checks and bounded numerical search followed by exact rational certification.

From the extracted packet root, run:

    python general_schur_refresh_audit/check_exact.py
    python general_schur_refresh_audit/check_homogeneous.py

The first uses SymPy. The second uses NumPy and SciPy for a bounded candidate search and Python Fraction for its exact certificate. No packages are installed by either script. SHA256SUMS records every included source snapshot except itself. REPLAY.json records replay from a newly extracted ZIP.

## Established methods and scope

Permutation averaging and symmetry reduction are established methods. For general background, see Karin Gatermann and Pablo A. Parrilo, *Symmetry groups, semidefinite programs, and sums of squares*, Journal of Pure and Applied Algebra 192 (2004), 95–128: https://arxiv.org/abs/math/0211450 . The present note directly derives its elementary Hamming-weight counts and normalization; it does not assert priority for the symmetry method.

The causal product prerequisite is Gutoski and Watrous, *Toward a General Theory of Quantum Games* (2007), Theorem 9: https://cs.uwaterloo.ca/~watrous/Papers/GeneralTheoryQuantumGames.pdf . The included causal_refresh_product/PROOF.md records the inherited application and unchanged-action embedding.

Included prior proofs are unmodified snapshots with relative packet locations. They retain their original historical paths and scope statements. This packet makes no priority assertion and grants no new license to third-party source material.
