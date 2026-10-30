# A further established physical service: approximate complex conjugation

Read directly30October2026: Yoshida--Murao, *Optimal complex conjugation of
unknown isometry channels*, arXiv2607.29054v1, SectionIII-D/Corollary10 and
SectionIII-E/Corollary11, equations133--144.
https://arxiv.org/html/2607.29054v1

The prior supplies a REAL deterministic approximate conjugate-channel service,
not only virtual expectation estimates. For an unknown channel Lambda with
input dimension d_in, output dimension d_out and Kraus rank at most r,
Corollary11 constructs its complex conjugate

    conjugate(Lambda)(X)=conjugate[Lambda(conjugate(X))]

to HALF-diamond error at most epsilon from at most

    n<=d_in(r*d_out-d_in)/epsilon

parallel original calls when the dimension defect is positive. It first
acquires one COMMON random Stinespring frame, applies the known isometry-
conjugation circuit and discards its environment. Corollary10 pays the
covariance-based linear fidelity-to-diamond bound and polynomial known-CG
circuit construction. These are established mechanisms, not new discoveries
or executed circuits in this campaign.

For the present exact flat k->D source, substitution gives

    n<=k(rD-k)/epsilon.

At the smallest ambient D=kr this is k²(r²-1)/epsilon. The known controller
cost is polynomial in the isometry output rD and inverse precision; it is
not declared polynomial in log D. At larger ambient D this particular
service retains its D dependence. The earlier admitted flat inverse remains
a distinct full-throughput alternative with its own stronger output contract
and dimension/precision accounting.

Complex conjugation still maps k->D. Our requested arbitrary-payload decoder
maps D->k. An acquired conjugate query is not itself an adjoint/inverse,
and appending a probabilistic transpose must pay its success, error and
failure-state contract. No restoring draw or coherent inverse block is
provided by Corollary11. No better complete-recovery operation follows
without constructing that missing interface.

The paper proves constant-factor optimality for its GENERAL channel
conjugation service when r is CONSTANT. It does not supply a varying-r
quadratic lower bound for the present reversible-source recovery family.
Its exact finite-query no-conjugation statements and approximate protocol
must not be conflated. This source screen did not alter the completed
native exact-heralding theorem or the earned adaptive/parallel gap.

Only read-only primary retrieval and mathematical substitution were done;
no source, circuit, solver or model case was executed. Historical priority
of our separate results remains UNKNOWN.
