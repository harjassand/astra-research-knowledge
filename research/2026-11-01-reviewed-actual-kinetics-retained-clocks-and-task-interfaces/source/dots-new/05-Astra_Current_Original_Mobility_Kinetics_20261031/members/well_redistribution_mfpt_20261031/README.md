# Explicit well-current receiver for ordinary unit-mobility mean passage time

Status: candidate; independent theorem and whole receiving review pending.

The actual ordinary generator is unchanged. A new full-state Poisson current
redistributes source energy in the well and carries fixed barrier-density flux
through the transition slab. With acquired positive quartic geometry and unit
mobility, the513D executed mean interval has total ratio1.006729781. This is not
capacity inversion or a new engineered diffusion.

Read `WELL_REDISTRIBUTION_CURRENT.md` and
`COSTS_COMPARISONS_AND_FAILURES.md`. All prior freezes remain unchanged. Exact
FULL Gibbs|A initialization is required, not a fixed ray or an approximate
preparation justified only by total variation. Physical membership is unauthenticated.

From this source directory:

    python receive_mfpt.py   # four actual examples
    python check.py         # source/algebra/numeric receiving tests and full replay

Small original-task replay:

    from fractions import Fraction as F
    import json, receive_mfpt as c
    raw=json.load(open('small_raw_fixture.json'))
    cert=json.load(open('small_certificate.json'))
    c.verify(raw,cert,beta=F(1),kappa=F(1),
             quad_relative=F(1,1000),full_ratio=F(11,10))

The separate-source fields matter. A future survival wrapper must not assume
Q_S<=eta^2 B_new; use its own explicitly received current bound. No such CDF
output is silently accepted by this mean receiver.
