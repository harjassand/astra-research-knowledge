# Exact inverse-power spending by actual connector events

30 October 2026. Working consequence of the reviewed paired-profile proof; not independently reviewed. This is intended to replace probability-only bounds in the off-section phase processor.

For the complete local fast/clearing episode at fixed B=b>=q, including arbitrary repeated dormant/seeded transitions, stop at the first connector event. For every fixed s>=0, let f_s(A)=(1+A)^-s. Denote its immigration and activation subkernels by I_b and J_b.

The proposed actual kernel inequalities are

`I_b f_s <= C_s (b)_q^-1 f_(m+s)`,
`J_b f_s <= C_s b/(b)_q f_(m+s-1)`.

A first clearing has the already reviewed transport bound `D_b f_s<=C_s f_s`. The first two claims SPEND m and m-1 incoming inverse powers, respectively, rather than merely preserving the profile and multiplying by a separate rare probability.

## Compensator proof

At immigration, physical A_out=A+1. Thus

`I_b f_s = i E integral_0^tau f_s(A_t+1)dt`.

At activation, A_out=A+m-1, and

`J_b f_s = t b E integral_0^tau A_t f_s(A_t+m-1)dt`.

Use the reviewed paired profile at exponent p=m+s for the first running cost, and p=m+s-1 for the second. On large A its negative killed drift, after restoring the common clock, has magnitude at least `c (b)_q A^(m-p)`. This pays respectively f_s(A) and A f_s(A). On bounded A and large n, the strict paired/reaction-6 margin pays these bounded running costs. Finite shells are handled by actual finite-state values, not by scaling a wrong-sign drift formula.

At a dormant entrance, the associated continuation profile f_p is transported by the accepted small-return two-kernel construction. At d=0, the first physical waiting cost has the same f_p order, and both true seed outputs shift A by at most two. Consequently the full first-connector running-cost bound holds after all local dormant/seeded feedback is included. Substituting into the compensator identities proves the two displayed kernel inequalities.

These identities retain output correlations. They do not require a stationary fast law, a scalar gap on low-A inputs, or independent reset composition.

## Low phase

At 0<B<q, a noncompulsory immigration race has probability `i/(i+tAB)<=C/(1+A)` and increases A. Therefore its actual subkernel satisfies

`L_b f_s <= C_s f_(s+1)`.

Low activation and compulsory B=0 immigration have profile norm at most one. Only the latter is compulsory; it is r-neutral. A low-to-high inactive wrap must retain the previous V2 stopping designation rather than being called a rare active high event.

## Consequence for retained phase words

Any FIXED connector word can now be costed backward by adding its actual spent exponents: m for a high immigration, m-1 for a high activation, and one for each noncompulsory low immigration. Clearing transports the remaining exponent. A bounded collection of phase words of total degree at least m has joint weighted mass O(f_m(A_initial)), before any unearned continuation is appended.

The seed-interrupted phase budget in SEED_INTERRUPTED_SOURCE_V2.md is purely a connector/r geometry identity and survives fast positive-D interludes, since they preserve B and total composition. Thus the local ingredients for a full phase-word processor no longer require a separate small activation probability or an output-independent moment product.

## Remaining limitation

An UNBOUNDED collection of words still requires a proved summability/repair operator. Constants C_s depend on s and cannot be treated as one fixed geometric constant when the exponent grows with the number of events. Nor does stopping at the first costly word supply its later return to the section. The dormant Green handles one exact part of that continuation, not the entire positive-D process. These are the remaining full-cycle obligations.
