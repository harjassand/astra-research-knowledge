# Original unit-mobility autonomous passage CDF

Status: author candidate; the new well-current engine and this complete
separate-source wrapper need independent receiving. Previous accepted sources
remain unchanged. Read the source-bound whole receipts when delivered rather
than interpreting a later folder name as acceptance.

The task is the all-time ABSOLUTE CDF of a full-Gibbs|A initialized hitting time
for the actual ordinary constant-SPD Langevin model. The new A-current pays its
transverse redistribution in the well, not in the rare transition slab. The
S-current remains separate. This is a mathematical witness, not a changed
physical generator, an angular mixing oracle or engineered tensor actuation.

    python receive_survival.py  # four actual cases, including original M=I
    python check.py             # author exact/receiving checks plus all replays

Small source-bound replay, with ORIGINAL external controls:

    from fractions import Fraction as F
    import json, receive_survival as c
    raw=json.load(open('small_raw_fixture.json'))
    cert=json.load(open('small_certificate.json'))
    c.verify(raw,cert,times=[F(0),F(10**8),F(3*10**8),F(10**9)],
             ks_error=F(1,20),query_absolute_width=F(1,10),full_ratio=F(11,10))

The finite output is not an exact exponential law, relative extreme-tail
accuracy, arbitrary-start result, physical model identification or approximate
preparation guarantee. The same outer envelope across two raw angular models
does not assert identical actual distributions. The asymptotic universality
candidate is separately frozen and is NOT used by this finite receiver.
