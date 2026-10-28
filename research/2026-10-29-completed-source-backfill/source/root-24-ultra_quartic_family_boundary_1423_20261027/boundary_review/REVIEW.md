# Complete internal acceptance of the sharp parameter-line theorem

Root review completed2026-10-28. The complete analytic proof in
../quartic_alternative/sector_boundary/PRIMARY_PROOF.md was read, including
its exact conventions, finite lift, parameter extension and fixed critical
pair. The accepted statement, for every real tau, is

    F_tau=u²+v²+3w²+tau q²+4q(u-v)
    is rank-one convex iff polyconvex iff quasiconvex
    iff tau>=89-12sqrt42.

The independently authored independent_boundary.py imports no source-author
verification, numerical face map, pickle or generator. It builds the literal
quartic and complex features in SymPy's QQ(sqrt42), a different exact engine
from the author's stdlib quadratic field. It checks the full boundary
support polynomial, both shifted positive Gram blocks (16 and6), all22 LDL
pivots and complete matrix reconstruction. Field signs use rational squared
comparisons in the positive real embedding. The checker initially required
a conversion fix for SymPy MPQ coefficients to Fraction; no certificate was
changed. Final complete replay passed in approximately3.07seconds.

The same checker separately differentiates the literal quartic's rank-one
curvature, reconstructs the critical acoustic matrix, and proves its fixed
kernel modulo z⁴-m_c z²+1. Exact signs establish m_c>5/2,z²>2 and the nonzero
cofactor pairing. The determinant-square rank-one update is independently
checked, giving a strict negative curvature for every tau below the edge.
The positive boundary certificate and critical-pair hashes are respectively
66901f304531cbc969ccc7f89e5a7e57091e57cefba21133355b0d2cb54be554 and
c57502de52215737c319374669a32b8e31983fbd7bc89c0fe6b8315aa0b36aa3.

The finite checks provide the exact algebraic facts; the following analytic
implications were also reviewed. Division of the norm multiplier is only
for X!=0, with zero increment handled directly. Supremum of affine minor
supports is a finite convex lift because any off-graph point is an average
of two determinant-graph points. Adding(tau-tau_c)q² preserves PC and adds
an explicit support square for all larger parameters. The determinant and
gradient means cancel on arbitrary stated zero-boundary/periodic W1,4
tests. A single exact critical pair excludes all lower parameters, so no
unverified all-parameter acoustic sufficiency claim is needed.

No mathematical gap remains at this actual scope. This is a full internal
proof acceptance, not merely a finite test of selected gradients. It does
not classify the full nine-coefficient cone, establish world priority, give
a physical capability or transfer the strict113/10 constants to the singular
edge. The earlier PC/non-SOS-PC35-dimensional neighborhood remains a
separate completed theorem. No frozen producer files were modified.
