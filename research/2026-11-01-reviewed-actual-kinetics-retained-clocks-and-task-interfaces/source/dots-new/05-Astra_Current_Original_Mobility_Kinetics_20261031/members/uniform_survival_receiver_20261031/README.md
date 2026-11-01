# Uniform autonomous passage-time CDF receiver

Status: author candidate; independent spectral/corollary and whole receiving
acceptance pending. The underlying constant-SPD MFPT engine is separately
accepted at its doc-corrected v2 freeze. No previous freeze is changed.

Read `FINITE_RATE_SURVIVAL_COROLLARY.md`, the separately bound root spectral
proof, and `COSTS_SCOPE_AND_PRIORS.md`. The output is uniform ABSOLUTE CDF
accuracy against a single acquired exponential reference, not relative extreme-
tail accuracy, an exact exponential law or arbitrary-start kinetics. Exact FULL
Gibbs|A initialization and the actual constant-SPD model remain required.

From this directory:

    python receive_survival.py  # four actual cases
    python check.py             # 3809 author checks, all cases replayed

A small source-bound receiving replay uses literal external times/controls:

    from fractions import Fraction as F
    import json, receive_survival as c
    raw=json.load(open('small_raw_fixture.json'))
    cert=json.load(open('small_certificate.json'))
    c.verify(raw,cert,times=[F(0),F(10**8),F(3*10**8),F(10**9)],
             ks_error=F(1,100),query_absolute_width=F(1,50))

Do not adopt original controls from a certificate. The old MFPT and this
wrapper's extra exp products share one external total operation budget. Physical
membership, parameter accuracy and preparation are not authenticated. Later
well-redistribution/unit-mobility ideas are excluded from this receiver.
