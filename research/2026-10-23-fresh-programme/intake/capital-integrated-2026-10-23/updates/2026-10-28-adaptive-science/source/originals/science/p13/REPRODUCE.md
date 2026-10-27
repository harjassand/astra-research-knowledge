# Reproduction and evidence

Run from this directory with Python 3. All paths below are owned copies;
supplied source scripts are never executed in place.

Core exact certificates use only the standard library:

    python3 helper/certify_dual.py
    python3 certify_finite_network.py
    python3 certify_envelope.py
    python3 certify_joint_cap.py
    python3 certify_boundary_split.py

They use integer/Fraction intervals, outward rounding, exact polynomial
sign brackets, positive Taylor remainders, and positive infinite-integral
series tails. No frequency grid is a proof. `intervals.py` documents the
owner's 85-decimal outward grid; the helper certificate uses unrounded
Fractions. Each script writes its CERTIFIED_*.txt evidence.

Nine nearby exact certificates use mpmath only to propose scalar brackets:

    python3 construct_joint_family.py
    python3 construct_joint_extended.py

The second script certifies five further finite-resource points. Exact
intervals subsequently prove root existence and positive finite
components. FAMILY_PROOF.md owns the universal all-frequency root bound,
globality, and the distinct analytic open-family claim.

Supplementary diagnostics:

    python3 check_asymptotic.py
    python3 explore_frontier.py

The first uses mpmath at 85 decimal digits for actual endpoint matrices
and every band in the proved small-C family; it is numerical corroboration.
The latter uses NumPy and attainable_design_owned.py to select openings.
Its scalar golden searches can be local and do not prove exclusions or
global optimality. The exact duals own all global claims.

Governing F,C,A,R,V,E,P blobs are preserved byte-for-byte in frozen_sources,
all from commit 2cba6a60646bb52982233c40d7ae941b266f0d5c. Exact original
provenance is in the case's SOURCES.json. The hashes of F,C,A are

    e039c3a8a70181d9b123ae8e4af7b3a7394386512afb12ca89e0bdb55d19b052
    6816ebac77da1b74a66be1e7d8adbfd1d7e6903295b7c24416cd04d23a819046
    655b9d232709d6f076279946327d31b7a7e149fcf82de15ebd3c12be8e1148ce

The inherited trace/log machinery, exact compliance identity, complete
Foster/Stieltjes inverse, and low-temperature obstruction are prior inputs.
This experiment adds the constrained dual constructions and connected
frontier statements. Historical priority has not been searched or cleared.

One same-settings helper developed the initial certificate and then
reviewed the integrated extensions. Its review files state the inspected
scope. These are exposed internal audits, not external acceptance,
material validation, or novelty clearance.
