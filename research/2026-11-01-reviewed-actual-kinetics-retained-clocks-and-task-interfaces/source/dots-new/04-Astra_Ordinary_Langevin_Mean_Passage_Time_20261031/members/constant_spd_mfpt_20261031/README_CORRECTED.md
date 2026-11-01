# Constant-SPD ordinary Langevin autonomous mean receiver

Status: doc-only v2 author freeze; whole audit found no code/endpoint change.
Use FROZEN_SHA256_v2.json. Original v1 files remain unchanged as history; the
root-call-count versus root-bit-complexity correction is explicit.

Main result: a full-state Poisson current bounds the EXACT FULL Gibbs|A mean
hitting time for ordinary constant-mobility quartic Langevin dynamics, without
angular mixing or energy Markov closure. At513 total dimensions and M=64I the
executed outer ratio is1.004780006. Unit M=I is retained with ratio1.256975784.
The raw coupling graph/strength may vary; equal certified intervals do NOT
assert equal actual means. No actual physical model or preparation is acquired.

Read `POISSON_CURRENT_CONSTANT_SPD_MFPT.md`, then
`ARITHMETIC_COSTS_AND_SCOPE_CORRECTED.md` and `PRIMARY_COMPARISON_LEDGER.md`.
`ZERO_GAP_SCOPE_NOTE.md` explains why finite source-specific mean does not imply
a positive killed/global spectral gap. All previous freezes remain unchanged.

Run from this directory, with source-relative dependencies preserved:

    python receive_mfpt.py  # production of all six cases
    python check.py         # 3678 author assertions; all saved cases replayed

For a small exact receiving replay without regenerating large fixtures:

    from fractions import Fraction as F
    import json, receive_mfpt as r
    raw=json.load(open('small_raw_fixture.json'))
    cert=json.load(open('small_certificate.json'))
    r.verify(raw, cert, beta=F(1), kappa=F(1),
             quad_relative=F(1,1000), full_ratio=F(11,10))

The literal external task above is intentional: do not adopt purported original
controls from an untrusted certificate. The accepted kinetic energy parser and
frozen scalar helper are byte-hash checked on import. This does not transfer an
earlier model's physics or initialization. The receiver's actual mobility must
be constant isotropic or diagonal and positive, and all quartic energy terms
must satisfy the acquired complete-program grammar.
