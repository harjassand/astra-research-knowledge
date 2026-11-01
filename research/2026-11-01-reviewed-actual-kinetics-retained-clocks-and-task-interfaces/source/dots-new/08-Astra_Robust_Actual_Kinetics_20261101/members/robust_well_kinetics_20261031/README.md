# Localized geometric uncertainty: actual autonomous kinetics

Status: author candidate, independent theorem and complete executable review
pending. All earlier accepted files/packages are unchanged.

`LOCALIZED_DENSITY_ENVELOPE_CANDIDATE.md` supplies the actual global diffusion,
dominating-source current, lower-density price, full-Gibbs|A mean and all-time
CDF joins. `GENERAL_ENVELOPE_CONSERVATIVITY_NOTE.md` is a separate mathematical
extension candidate, NOT a broader input interface of this receiver.

The actual family is F=vU+defect*gV, with v=1+kappa(1-y^2)^2,
g=y^2(1-y^2)^2/(1+y^2), U an acquired positive quartic atom program, and
V=sum_i r_i c_i z^e_i. Each fixed real r_i remains in its declared interval
inside[0,1]. These are independent parameter slots, NOT a probability prior
or random independence assertion. The complete global program, all interval
endpoints and the actual constant isotropic/diagonal mobility are verified.
No microscopic point V is reconstructed. A generic unknown perturbation does
not qualify merely because a few measurements look small.

    python receive_robust.py  # three actual production-family certificates
    python check.py           # author proof/arithmetic/receiving checks

For the source-bound small replay use the literal ORIGINAL external task:

    from fractions import Fraction as F
    import json, receive_robust as c
    raw=json.load(open('small_raw_fixture.json'))
    cert=json.load(open('small_certificate.json'))
    c.verify(raw,cert,defect=F(1,1000),quad_relative=F(1,20),
             full_ratio=F(2),ks_error=F(3,4),query_absolute_width=F(1),
             times=[F(0),F(1000),F(10000)])

The main 513D output is much tighter: mean ratio1.00806405 and all-time absolute
CDF error0.00820975 for defect1/1000 and1,023 unidentified shape weights.
The reference law starts from EACH actual member's OWN EXACT FULL Gibbs|A.
This does not replace actual Gibbs by nominal Gibbs, authenticate physical
membership/preparation, give an arbitrary-start result or bound relative
extreme-tail errors/exponential moments. `times=None` means no optional finite
queries; the all-time mathematical statement still requires the full bounds.
