# Controlling record-noise qualification

This addendum corrects one statement in Section4 of the frozen
CLOSED_BUS_ERASURE_CANDIDATE.md; its original bytes and manifest remain unchanged.
The five-point numerical gate budget does not use that extra-noise formula.

The statement that independent record noise of variance sigma^2 adds
k^2 sigma^2 to L_eff is EXACT only for independent ZERO-MEAN GAUSSIAN record
noise. For a general independent additive real noise xi, the corresponding
coherence multiplier between B-eigenvalues b,c is its characteristic function
E exp(i k(b-c)xi), with the sign fixed by the correction convention. Variance
alone does not determine this multiplier or make it Gaussian. A nonzero mean
also introduces a deterministic local-B phase and must be charged or corrected.

For example xi takes +/-sigma with equal probability. The multiplier is
cos(k(b-c)sigma). At k(b-c)sigma=pi it is -1, whereas the Gaussian multiplier
with the same variance is exp(-pi^2/2)>0. Thus replacing arbitrary record noise
by the Gaussian L_eff formula is not a valid receiving rule.

A separate conservative bound is available when xi is independent of data and
apparatus, centered, and has finite variance sigma^2. Taylor's integral remainder
for the unitary conjugation superoperator, followed by averaging, gives

  || E Ad_exp(i k xi B) - Id ||_diamond
       <= (k^2 sigma^2/2) diam(B)^2,

also capped at2. For B=Z1+Z2 this is at most8 k^2 sigma^2. This is an EXTRA
diamond-error budget, not an exact Gaussian dephasing parameter. The bound
uses ||ad_B||_diamond<=diam(B), after subtracting a scalar from B, and that
unitary conjugation has norm1 throughout the remainder integral.

Correlated controller/record faults require their actual joint instrument;
neither the Gaussian formula nor this independent-noise bound receives them.
No existing exact grid/certificate/test value is changed by this qualification.
All other physical-service, vacuum-versus-warm, and restricted-comparator
limitations of the frozen proof and independent audit remain in force.
