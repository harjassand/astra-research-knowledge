# A non-Gaussian replicate-closure KL operation

27 October2026. Parent construction motivated by the completed covariance-only
counterfamily. It composes a standard antisymmetric-observable relative-entropy
inequality with a sensor-gain-invariant closure statistic. Historical novelty
and practical superiority over existing current/TUR inference are UNKNOWN.
No physical record law or entropy-production rate is acquired here.

Input: independent complex three-vectors Z with a specified physical reverse
involution Z->conjugate(Z), optionally with definite scalar parity signs.
Each channel has a fixed nonzero unknown complex gain, stable across replicate
records. Take three independent replicas a,b,c and define

    g=Im[(Z1_a conjugate(Z2_a))
          (Z2_b conjugate(Z3_b))
          (Z3_c conjugate(Z1_c))].

Under channel gains H1,H2,H3, g is multiplied by the POSITIVE factor
|H1 H2 H3|². All sensor phases cancel exactly. Under the physical reverse,
g changes sign; parity signs appear twice and cancel. With centred vectors,
E g is the imaginary covariance closure, but the bound below needs neither
Gaussianity nor centering. Define A=E g and M2=E g²<infinity.

For the three-replica forward law P3 and its reversed law Q3, Q3(g)=P3(-g).
Cauchy–Schwarz gives

    4A² <= [integral (p-q)²/(p+q)] * 2M2.

The pointwise logarithmic inequality gives Jeffreys divergence >= twice that
triangular discrimination. Forward/reverse KL divergences are equal by the
involution, hence D(P3||Q3)>=2A²/M2. Independence makes this

    D(P||P_reverse) >= (2/3) A²/M2.

The ratio cancels the unknown positive gain. This is an implemented per-vector
KL lower bound, not a covariance-only rate formula. The added second moment
of g is a high-order measurement requirement; second covariances do not supply
it. Unknown noise is not automatically reversible or gain-covariant.

## Conditional finite confidence and executed example

If |g|<=G is independently justified and m independent triples are acquired,
normalize z=g/G. The compiler uses exact rational outward radii

    rA>=sqrt(12/m), rM>=sqrt(3/m)

to return (2/3)(|mean z|-rA)_+²/min[1,mean(z²)+rM]. Hoeffding and e^6>400
give simultaneous failure probability<.01. The code verifies e^6>400 by a
rational Taylor partial sum. A maximum observed sample is not a bound G, and
the compiler does not test independence, unclipped gains or sampling laws.

An exact finite-vector fixture has types(1,1,1),(1,i,-1),(1,-i,-1) with
probabilities3/5,3/10,1/10. Optional common uniform phases can make vectors
centred without changing g; those irrelevant phases are analytically eliminated
from the example computation. Exact enumeration of27 type triples gives
A=-6/125,M2=12/25 and per-vector KL floor2/625. The true reverse KL is
(1/5)log3. Unknown example gains(2+i,-1+2i,3-2i) multiply g by325 and leave
the floor exactly unchanged.

The actual PRNG illustration generates600000 TYPE draws for200000 triples.
It returns a conditional IID confidence floor.00211635. It is an executed
abstract demonstration, not600000 physical records, a certified PRNG law or
evidence about an instrument. `bound.py` and `results.json` preserve all counts.

## Resource and physical interface

To convert this into a physical rate, each Z must be a genuinely acquired
length-T record observable with the stated reverse/filter law and an acquired
finite-record budget D_path<=sigma*T. Then sigma>=2A²/(3T M2). An asymptotic
entropy-rate definition alone does not supply that finite-T inequality. The
elementary floor is<=2/(3T); padding a record cannot create useful rate
information. Acquiring a confidence statement costs3m such records plus
preparation, separation/independence, settling and measurement costs.

Finite-window Fourier transforms do not automatically obey exact scalar sensor
gain multiplication. Window edges, spectral mixing, gain variation between
records, localization cross-talk, noise reversal and odd controls need their
actual contracts. A qualified finite-band null witness is a different operation
and cannot silently supply this transport. Those promises and a useful real
measurement advantage remain unacquired. The result is a constructive
additional-observable repair at a precise mathematical interface, with its
high-moment and acquisition price retained.
