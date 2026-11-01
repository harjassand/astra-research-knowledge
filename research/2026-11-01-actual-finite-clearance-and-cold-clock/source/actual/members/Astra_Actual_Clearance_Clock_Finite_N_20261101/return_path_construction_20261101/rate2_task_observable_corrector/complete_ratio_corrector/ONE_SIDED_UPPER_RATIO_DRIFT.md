# One-sided upper ratio drift without the adaptive A gate

**Author component, pending independent receipt.** This is a local upper-face
result for the same complete cubic F2. It preserves the broader-domain
counterexamples and the conditional two-sided adaptive result. It does not
assert a global lower-R restriction, a lower-R admission theorem, or acquisition
of the actual count/A/imbalance gates.

## 1. Local received domain and conclusion

At the state where the generator is tested, assume

    R=E²/(NL)∈[3/2,2], E/N<=1/100,
    A<=L/100, |Z|<=L/100, L>=100,
    E^5>=32N³, |S-N|<=E/100.                             (U)

Here S is the actual total count and N is fixed. **No bound on
A²N/(L³E) is assumed.** The count event must be acquired from the original
immigration/death ledgers. For example, the root's charged |S-N|<=C T entails
this count gate once T²>=50C, because E>=2T³. That implication is not a new
probability or entrance-preparation claim.

Then the canonical complete cubic observable constructed in
`COMPLETE_CUBIC_CONSTRUCTION_AND_OBSTRUCTIONS.md` satisfies

    GF2 < -(1/10) EL/N.                                 (26)

The local restriction R∈[3/2,2] specifies the upper-face neighborhood where the
drift is inward. It does not require the process to remain above R=1/2, or even
above R=3/2, at all earlier times. Using (26) to control repeated approaches to
the upper face still requires the root's stopped-excursion/localization join.

## 2. The exact favorable component

The rational factorization used for the complete correction was

    chi=u a[delta H_d+t H_t+u H_u]+u²a²H_2+u³a³H_3,

where r=R, u=E/N, t=1/L, a=A/L, delta=S/N-1 and

    P=r(1+delta-u)+2u²(1-t).

The apparently singular component has a much simpler exact expression:

    H_t=r^4/[(1+t)P³].                                  (27)

This identity is verified by cancelling the exact rational polynomials, not by
a small-t expansion. Consequently the corresponding part of chi is

    chi_t=u t a H_t=A N E³/[L²(L+1)k³],
    k=S+2L-E-2.                                         (28)

In the parameter-motion remainder, the post-jump A value is held fixed while
L,E,Z,S traverse their actual parameter segment. For that fixed A value,

    partial_L chi_t
       =-chi_t[2/L+1/(L+1)+6/k] <=0.                    (29)

All denominators remain positive on the one-step padded domain. Thus the
AE→2A reaction, whose L increment is +1, contributes a **nonpositive** chi_t
L-motion term. This is exactly the term that caused the S=N lower-face
obstruction. It is favorable for an upper-drift bound.

Equation (29) is valid along the entire parameter segment, not merely at its
start. The same reaction's E contribution is also favorable, but the proof
below conservatively continues to pay its absolute value. No cancellation or
independence of the actual martingales is asserted.

## 3. Recompute the upper bound, rather than reuse an adaptive premise

The full normalized drift is the actual identity

    GF2/(EL/N)=Dbar+frozen mismatch+parameter motion.

The coefficient majorants, mean bound, frozen mismatch, and E/Z/S parameter
bounds from the two-sided proof do not use the adaptive gate. Only one term in
the absolute L-motion bound used A²N/(L³E)<=1/100: the AE→2A chi_t contribution.
For the present upper bound discard that term by its exact sign (29), while
retaining absolute bounds on every remaining term.

The recomputed L-motion upper bound is not inferred from a sampled drift or
from an adaptive-domain conclusion. It is built directly from the same
continuous coefficient bounds, with no theta_A variable in its formula.
The resulting rational ceilings are

| normalized upper-error contribution | ceiling |
|---|---:|
| algebraic mean minus 4-3r-rt²/u | 8/25 |
| frozen mismatch | 1/10000 |
| remaining L parameter motion, upper bound | 1/20 |
| E parameter motion | 17/5000 |
| Z parameter motion | 1/100000000 |
| S parameter motion | 1/100000000 |

Their sum is strictly below 2/5. The non-rounded exact rational total is about
0.365403388; the decimal is not used to accept the inequality. Thus

    GF2/(EL/N) <=4-3R-RN/(EL²)+upper_error,
    upper_error<2/5.

On R>=3/2 the first two terms are at most -1/2 and the last displayed nominal
term is nonpositive. This proves (26).

`certify_one_sided_upper.py` verifies (27)-(29) symbolically and recomputes the
rational bound without an adaptive-A gate. It records the exact source hash of
the continuous coefficient certificate it receives. Its output is
`one_sided_upper_certificate.json`. No finite-grid positivity inference is used.

## 4. Endpoint and actual martingale costs

The previously frozen continuous-domain estimates on the larger local region
R∈[1/2,2] remain applicable on upper-face excursions and their one-jump exits:

    |F2-R|<1/1000,
    |Delta F2|<=2/T,
    Gamma(F2)<=50L^-2 q_LL+110[E/(NL)]²q_A.              (30)

The all-channel occupation integration and weighted-clock formulas (22)-(25)
in `ADAPTIVE_CONDITIONAL_DRIFT_AND_BRACKET.md` did not use the adaptive gate.
They can therefore be used on a stopped upper-face excursion with its own
received entrance and physical-domain stop. They must not be advertised as a
global pathwise bracket budget while the chain is allowed to spend unaccounted
time below that local region. A global cutoff/excursion join, including every
entrance charge or a directly global source budget, remains a separate step.

## 5. Precisely what this changes

A consumer that only needs an upper ratio ceiling need not buy the new
adaptive A envelope merely to turn this complete F2 into an upper-face barrier.
It still needs the original A<=L/100 and imbalance/count gates, and the actual
local-to-global stopping argument. This theorem does not validate the root's
separate inverse-cubic storage or global clock-tail derivative formulas; those
must receive their own proofs.

The lower-face counterexamples remain valid and informative. They are favorable
rather than harmful at the upper face, which is why changing the task's required
boundary can remove an operation that the two-sided representation had imposed.
